# Git ↔ Jira Integration Workflow

> 把 Jira issue key 當成 Git ↔ Jira 的 join key，用命名規範 + MR 模板 + 自動 transition 實現專案管理自動化。

## Core Principle

**每一段 Git 活動都要能對到 Jira key**

不管是 GitLab Jira integration 還是 Jira Automation triggers，都依賴「能從 branch / commit / MR 找到 Jira issue key」。

---

## 0.5) Agent-side State Machine Spec（Git 事件 → Jira 建議動作）

> 目標：把「敘述性流程」改成 **可執行/可檢查** 的狀態機規格。
> - 本段是 **agent 的決策規格**（要不要寫入 Jira、寫什麼、何時停下來問使用者）。
> - 任何 Jira 寫入（transition/update/comment/create）都必須遵守：
>   - SKILL Guardrails：先讀再寫、最小變更、**Confirm-before-write**。
>   - No-token mode：只能輸出 plan/payload，不可真的寫入。

### A) State（狀態集合，抽象層）

Jira workflows 各家不同，這裡定義「抽象狀態」供對應：
- `TODO`
- `IN_PROGRESS`
- `IN_REVIEW`
- `DONE`

> Mapping 原則：以 Jira status category（To Do / In Progress / Done）優先；
> 若有自訂（例如 QA / UAT / Deployed），視團隊規範擴充，但仍要映射回上述抽象狀態，避免 agent 幻覺 transition 名稱。

### B) Events（事件集合，來源於 Git）

- `BRANCH_CREATED`：新分支建立（或首次 checkout 到帶 key 的 branch）
- `COMMIT`：commit message 含 key
- `PUSH`：push 到 remote（可選，不一定對 Jira 產生寫入）
- `MR_OPENED`：MR/PR opened（title/description 含 key）
- `MR_UPDATED`：MR 更新（new commits / label / reviewer changes）
- `MR_MERGED`：MR merged
- `MR_CLOSED_NOT_MERGED`：MR closed but not merged

### C) Transition Rules（規則：guard → propose → confirm → execute）

每個事件都遵守同一個 **canonical flow (SSOT)**：
- `references/24_CONFIRM_BEFORE_WRITE_FLOW.md`（read → propose → confirm → execute → verify）

#### Execution Checklist（每次事件處理的最小清單）

1) **Extract keys**（依優先序）：MR title → branch name → commit message → user provided
2) **Classify event**（BRANCH_CREATED / COMMIT / MR_OPENED / MR_MERGED / MR_CLOSED_NOT_MERGED）
3) **Read-before-write**（若可讀 Jira）：
   - read issue（status / assignee / labels / required fields）
   - list transitions（只採用「回傳中存在」的 transition）
4) **Propose**（輸出 *即將做什麼* 的摘要）：
   - status change? comment? fields update?
   - why now?（避免因單一 commit 亂跳狀態）
5) **Confirm-before-write**（任何寫入都必須）：
   - 使用 `references/templates/comment_templates.md` 的模板
   - 以 **write-intent bundle**（單一 SSOT）呈現：action/targets/read-back/diff/payload/guards/rollback/verify
     - SSOT：`references/23_WRITE_INTENT_BUNDLE.md`
   - 顯示 diff（current → target）+ 受影響欄位 + stop conditions
6) **Execute**（若使用者確認且具寫入權限）
7) **Read-back verify**（寫入後立刻回讀核對；不一致就停）

#### Decision Table（抽象狀態 × 事件 → 建議動作）

> 註：這是「建議」而非硬性 transition；實作時仍需依專案 transitions 回傳結果決定。

- **BRANCH_CREATED**
  - Current `TODO` → propose transition → `IN_PROGRESS`（可選 comment）。Verify：status moved 或 stop w/ reason。
  - Current `IN_PROGRESS` → no status change（可選 comment）。
  - Current `IN_REVIEW` → no status change；提醒避免 parallel work。
  - Current `DONE` → no status change；建議走 reopen flow（先問使用者）。

- **COMMIT**
  - Any current state → add comment only（commit 不代表狀態變更）。Verify：comment 出現在 issue。

- **MR_OPENED**
  - Current `TODO` / `IN_PROGRESS` → propose transition → `IN_REVIEW` + comment（含 MR URL）。Verify：status in review + comment present。
  - Current `IN_REVIEW` → add comment only（避免重複 transitions）。Verify：comment present。

- **MR_MERGED**
  - Current `IN_REVIEW` / `IN_PROGRESS` → propose transition → `DONE` + comment（merge SHA + MR URL）。Verify：status done + comment present。
  - Current `TODO` → 先 read-back 確認 readiness，再提案 DONE；不確定就 stop + ask。Verify：status done 或 stop + ask。

- **MR_CLOSED_NOT_MERGED**
  - Any current state → 不做 auto-DONE；若要打回 `IN_PROGRESS` 必須 user confirm。Verify：status unchanged unless user approved。

#### Rule summary (de-duplicated)

The **Decision Table** above is the SSOT summary of event → proposed action.
If you need more “worked examples”, use the no-token playbook:
- `references/22_NO_TOKEN_PLAYBOOK.md`

### D) No-token / No-MCP behavior（離線行為）

當 Jira MCP token/權限不可用（或使用者要求 offline only）時：
- **不做任何 Jira 寫入**（create/update/transition/comment 全部禁止）
- 仍然照同一個四段式輸出，但只到 **Propose**：
  - Guard → Propose →（Confirm 模板只作為「日後要問的提示」）→ **不 Execute**
- 請輸出可直接複製使用的 *offline bundle*：
  - 讀取計畫（read-back plan）
  - 變更 diff（current → target）
  - payload skeleton（JSON placeholders）
  - verification checklist

Playbook：`references/22_NO_TOKEN_PLAYBOOK.md`
Confirm-before-write template：`references/templates/comment_templates.md` → **Confirm-before-write**（含 no-token/dry-run DRAFT variant）

> 重要：這裡故意偏保守（少自動 transition，多要求確認），避免「流程不同步」造成大量錯誤寫入。

---

## Legacy appendix (non-SSOT, examples only)

> ⚠️ The SSOT for agent behavior is **Section 0.5 (Agent-side State Machine Spec)**.
Everything below is **non-SSOT** and intentionally kept short to avoid drift/duplication.

If you need detailed conventions/templates, use these dedicated docs (preferred):
- Branch + commit conventions → `references/15_GIT_COMMIT.md`
- MR/PR title + description templates → `references/16_GIT_MR.md`
- Automation / integration notes → `references/17_GIT_AUTOMATION.md`

Minimal reminders:
- Always include the Jira issue key in **branch name** and **commit message**.
- Prefer conservative transitions: commit never implies status change; MR merged is the strongest DONE signal.
- When in doubt: **read → propose → confirm → execute → verify** (and stop on 401/403/missing transition).

