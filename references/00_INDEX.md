# Jira MCP Optimizer — References Index

## Core Documents
- `01_TOOL_MAP.md` — MCP 工具對照表（最重要）：把 MCP tool 名稱映射到概念動作
- `02_JQL_COOKBOOK.md` — JQL 常用範本與除錯技巧
- `03_FIELD_SCHEMA.md` — 欄位/狀態/transition/自訂欄位清單

## Workflows
- `04_WORKFLOWS.md` — Triage / Sprint planning / Bug→Task / PR→Issue / Release notes
- `14_WORKFLOW_GIT_INTEGRATION.md` — Git ↔ Jira 完整參考（SSOT）
- `15_GIT_COMMIT.md` — 輕量：commit message 格式
- `16_GIT_MR.md` — 輕量：MR 模板
- `17_GIT_AUTOMATION.md` — 輕量：自動化設置
- `18_WORKFLOW_DOC_IMPORT.md` — 文件導入流程：PRD/需求文件批量導入 Jira

## SSOT Safety / Write Guardrails
- `24_CONFIRM_BEFORE_WRITE_FLOW.md` — Canonical flow：read → propose → confirm → execute → verify（SSOT）
- `23_WRITE_INTENT_BUNDLE.md` — Canonical write-intent payload（SSOT）
- `22_NO_TOKEN_PLAYBOOK.md` — No-token / No-MCP 行為（dry-run plan + draft payloads）

## Prompts
- `05_PROMPTS.md` — 可直接貼給 agent 的 prompts（含輸入/輸出格式）

## Operations
- `06_TROUBLESHOOTING.md` — 授權、權限、rate limit、常見錯誤處理

## Templates
- `templates/issue_description_templates.md` — Issue 描述模板（Bug/Task/Story）
- `templates/acceptance_criteria_templates.md` — 驗收標準模板
- `templates/comment_templates.md` — 評論模板（含 confirm-before-write 範例）
- `templates/dashboard_template.html` — Dashboard HTML 模板（Chart.js + CSS Grid）

## Roles
- `07_ROLE_DECISION_DIRECTOR.md` — 決策導演（DACI）
- `08_ROLE_WORK_ORGANIZER.md` — 工作組織者
- `09_ROLE_PRD_GUIDE.md` — PRD 專家
- `10_ROLE_WORK_ITEM_PLANNER.md` — 工作規劃器
- `11_ROLE_READINESS_CHECKER.md` — 就緒檢查器（DoR）
- `12_ROLE_PROGRESS_TRACKER.md` — 進度追蹤器
- `13_ROLE_BUG_REPORT_ASSISTANT.md` — Bug 報告助手
- `19_ROLE_IMPORT_VALIDATOR.md` — 導入驗證器
- `20_ROLE_RISK_ANALYST.md` — 風險分析師
- `21_ROLE_DASHBOARD_BUILDER.md` — 儀表板建構師

## Scripts
- `../scripts/pack_issue.py` — 把 Jira issue JSON 壓縮成最小上下文 Markdown
- `../scripts/pack_search.py` — 把搜尋結果列表壓成可掃描摘要
- `../scripts/normalize_fields.py` — 把 customfield 轉成友善名稱
- `../scripts/pack_dashboard.py` — 彙整 Jira 數據為 Chart.js Dashboard HTML
- `../scripts/git_helpers.py` — Git 輔助（validate/branch/mr-desc/create-bug）

## Quick Navigation

### 我要查票
1) 看 `02_JQL_COOKBOOK.md` 找 JQL 模板
2) 搜尋後用 `pack_search.py` 壓縮結果
3) 需要詳情時讀單一 issue 並用 `pack_issue.py` 壓縮

### 我要建票
1) 看 `03_FIELD_SCHEMA.md` 確認必填欄位
2) 用 `templates/issue_description_templates.md` 產出內容
3) 看 `01_TOOL_MAP.md` 找對應的 create tool

### 我要改票
1) 先讀票確認目前狀態
2) 列出可用 transitions（以 API 回傳為準）
3) 走 SSOT：`24_CONFIRM_BEFORE_WRITE_FLOW.md`

### 我要做 Sprint Planning
1) 看 `04_WORKFLOWS.md` 的 Sprint Planning workflow
2) 用 JQL 拉 backlog
3) 按 workflow 步驟執行

### 我要 Git ↔ Jira 連動
- 只需要 commit 格式 → `15_GIT_COMMIT.md`
- 只需要 MR 模板 → `16_GIT_MR.md`
- 只需要自動化設置 → `17_GIT_AUTOMATION.md`
- 要完整（含 state machine + no-token 行為）→ `14_WORKFLOW_GIT_INTEGRATION.md`

### 我要導入文件到 Jira
1) 看 `18_WORKFLOW_DOC_IMPORT.md` 了解導入流程
2) PRD Guide (09) 解析文件結構
3) Work Item Planner (10) 分解任務
4) 批量建票（若可寫入）
5) Import Validator (19) 驗證結果

### 我要做風險分析
1) 看 `20_ROLE_RISK_ANALYST.md` 了解風險框架
2) 收集 Sprint/Project 數據（JQL）
3) 識別風險指標
4) 產出風險報告

### 我要產出視覺化儀表板
1) 看 `21_ROLE_DASHBOARD_BUILDER.md` 了解儀表板架構
2) 收集 Sprint/Project 數據
3) 用 `pack_dashboard.py` 產出 HTML
4) 瀏覽器開啟檢視
