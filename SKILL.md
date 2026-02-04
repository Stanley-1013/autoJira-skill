---
name: autojira-skill
description: |
  Lab version of our Git ↔ Jira automation skill for Codex + Moltbot.
  Use when: acting as an engineer in Codex, doing git workflow (branch/commit/MR/merge) that contains a Jira issue key (e.g. QQ-9 / PROJ-123), and you need Jira to be synced via Jira MCP.
  Expected outputs: Jira status transitions + evidence comments (branch name, commit SHA, MR link, merge commit).
  Workflow fallback: if Jira has only 待辦事項/進行中/完成 (no In Review), treat MR-open as 進行中 and communicate via comments.
---

# autojira-skill (lab)

## 0) Purpose（目的）
用 Jira MCP 進行：查票、建票、改狀態、寫 comment、規劃 sprint、整理需求。

優化重點（Optimization goals）：
- 少 token（token-efficient）
- 少往返（fewer round-trips）
- 每一步可驗證（verifiable steps）
- 避免亂改票（safe write guardrails）

## 1) Tooling（你可以用什麼）
- **mcp__Jira__\***：所有 Jira MCP 工具（read/search/create/update/comment/agile）
- **Read/Glob/Grep**：讀取本 skill 的 `references/`、`templates/`、`assets/`
- **Bash**：執行 `scripts/*.py`（壓縮/驗證/產生 payload）
- **Write**：輸出 dashboard HTML 或匯入報告等檔案

> ⚠️ No-MCP / No-token mode：若 Jira MCP token/權限不可用，本 skill 仍可做 **JQL 草擬、欄位/流程設計、issue 描述模板化、匯入前驗證**；
> 但任何 Jira 寫入（create/update/transition/comment）都必須停止，改輸出「待執行 plan + payload」。
> - Playbook：`references/22_NO_TOKEN_PLAYBOOK.md`
> - Canonical payload format (SSOT)：`references/23_WRITE_INTENT_BUNDLE.md`

## 2) Guardrails（必遵守）
1. **先讀再寫**（Read before write）：任何 update/transition/comment 前必先讀取 issue 目前狀態/欄位。
2. **最小變更**（Minimal change）：一次只改必要欄位；多欄位變更要分步並檢查結果。
3. **寫入前確認**（Confirm before write）：任何 Jira 寫入操作，先展示摘要與 diff，等待使用者確認（回 **OK** 才執行；回 **NO** 立即中止）。
   - SSOT flow：`references/24_CONFIRM_BEFORE_WRITE_FLOW.md`
   - SSOT write-intent：`references/23_WRITE_INTENT_BUNDLE.md`
   - Example template：`references/templates/comment_templates.md` → **Confirm-before-write**
   - 去重/冪等（避免重複留言/重複轉狀態）：`references/25_IDEMPOTENCY_DEDUP.md`
4. **限制查詢範圍**（Scope the query）：JQL 先小範圍（project + recent + limit），必要才擴大。
5. **避免幻想欄位/流程**：欄位/transition 以 schema 與工具對照表為準（見 references）。
6. **遇到 401/403、transition 不存在、issue 不存在**：立即停止寫入，改回報可用選項。

## 3) Quickstart（工程師 + Codex 日常用法）
> 目標：把 Jira 專案管理融入日常開發，不用開瀏覽器點 Jira。
> 原則：先用最少查詢拿到「可決策資訊」，需要再擴大。

### A) 最常見：把開發事件同步回 Jira（建議一口氣批次）
把你正在做的事情丟一句話給 agent，讓它：
- 讀票（status/assignee/transitions）
- 產出「將要寫入」的摘要（confirm-before-write）
- 你回 **OK** 後：一次把 evidence comments + status transition 做完

可直接複製的 prompts（範例）：
1) **開始開發（branch/commits 已有）**
   - 「把 QQ-14 同步一下：我在 branch feature/QQ-14-squash，補上最新 commit evidence，狀態轉進行中。」
2) **開 MR 後**
   - 「QQ-14 MR 開了：<MR URL>。請在 Jira 補 MR opened evidence，狀態維持/轉到進行中。」
3) **MR 合併後（含 squash/merge commit）**
   - 「QQ-14 MR merged：<MR URL>，squash commit <SHA>。請補 MR merged + commit evidence，然後轉完成。」

### B) 建票/補需求（需要時才用）
- 「幫我把這段需求整理成 Jira 任務（project QQ），含 description + acceptance criteria，先給我確認稿。」

### C) 查票/查進度
- 「列出 project=QQ 最近 10 張票：key / summary / status。」

---

### A) Search（用自然語言找票 → JQL）
1) 將需求轉成 JQL（see: `references/02_JQL_COOKBOOK.md`）
2) 搜尋：限制欄位、限制筆數（top 10 / top 20）
3) 需要彙整時：用 `scripts/pack_search.py` 壓縮結果再摘要

### B) Triage / Create（把一段描述變成可開發的 Issue）
1) 釐清：project / issue type / priority / assignee / labels
2) 用模板產出 description + acceptance criteria（see: `references/templates/*`）
3) 建票 → 回讀確認 → 補 labels/comment

### C) Update / Transition（改狀態/指派/補資訊）
1) 讀 issue（status、assignee、必填欄位、可用 transitions）
2) 產出「要改什麼」的 diff（現狀 → 目標）
3) 執行更新
4) 回讀確認

### D) Doc Import（PRD/需求文件 → 批量建票）
1) 解析文件（Role: PRD Guide / Work Item Planner）
2) 產出匯入 payload（先 dry plan）
3) 批量建立（若可寫入）
4) Import Validator 驗證完整性

### E) Risk / Dashboard（風險分析 / 儀表板）
1) 先用 JQL 收集小樣本資料（避免一次抓全量）
2) 需要報表時用 pack scripts 壓縮
3) Dashboard Builder 產出 HTML（如需要）

## 4) Git ↔ Jira Auto Sync（自動同步：SSOT）
**Issue Key 抽取順序**：MR title → branch name → commit message → 手動指定。

Git ↔ Jira 的 SSOT 已收斂到 **agent-side state machine spec**：
- `references/14_WORKFLOW_GIT_INTEGRATION.md`（完整：guard → propose → confirm-before-write → execute → read-back verify；含 no-token/no-MCP 行為）
- `references/15_GIT_COMMIT.md` / `references/16_GIT_MR.md` / `references/17_GIT_AUTOMATION.md`（輕量）

> 直覺預設（仍以 state machine + transitions 回傳為準）：
> - branch created → propose IN_PROGRESS
> - MR opened → propose IN_REVIEW
> - MR merged → propose DONE
> - commit → comment only（避免 noisy flip）

## 5) Roles（角色導向）
使用方式：**識別任務類型 → 載入對應 Role 文件 → 遵循 Role 工作流 → 使用模板輸出**。

- Decision Director（DACI）：`references/07_ROLE_DECISION_DIRECTOR.md`
- Work Organizer：`references/08_ROLE_WORK_ORGANIZER.md`
- PRD Guide：`references/09_ROLE_PRD_GUIDE.md`
- Work Item Planner：`references/10_ROLE_WORK_ITEM_PLANNER.md`
- Readiness Checker：`references/11_ROLE_READINESS_CHECKER.md`
- Progress Tracker：`references/12_ROLE_PROGRESS_TRACKER.md`
- Bug Report Assistant：`references/13_ROLE_BUG_REPORT_ASSISTANT.md`
- Import Validator：`references/19_ROLE_IMPORT_VALIDATOR.md`
- Risk Analyst：`references/20_ROLE_RISK_ANALYST.md`
- Dashboard Builder：`references/21_ROLE_DASHBOARD_BUILDER.md`

## 6) References（從這裡開始深入）
- **入口索引（start here）**：`references/00_INDEX.md`
- **工具對照表（最重要）**：`references/01_TOOL_MAP.md`
- **JQL cookbook**：`references/02_JQL_COOKBOOK.md`
- **Field schema / transitions**：`references/03_FIELD_SCHEMA.md`
- **Troubleshooting（權限 / rate limit）**：`references/06_TROUBLESHOOTING.md`
- **Scripts（token 壓縮）**：`scripts/pack_issue.py` / `scripts/pack_search.py` / `scripts/normalize_fields.py`

