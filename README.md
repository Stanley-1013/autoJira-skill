# Jira MCP Optimizer Skill

讓 AI Agent 以「少 token、少往返、可驗證」的方式操作 Jira / Confluence（查票、建票、改狀態、Sprint 規劃、PRD 審核、進度追蹤、風險分析、Git ↔ Jira 同步、文件導入）。

> Note: **This Skill requires Jira MCP Server tools (`mcp__Jira__*`)**. Without MCP credentials, the Skill can still help draft JQL / plans / payloads, but cannot perform write operations.

## Prerequisites
- Jira MCP Server（提供 `mcp__Jira__*` 工具）
- Jira/Confluence credentials（Jira base url / email / api token 等，依你使用的 MCP server 設定）

## How to use
- 核心入口：`SKILL.md`
- 需要查細節時：請看 `references/00_INDEX.md`

## Install
把整個資料夾放到你的 skills 目錄中（平台不同路徑不同），並確保 Agent 能讀到 `SKILL.md` 與 `references/`、`scripts/`。

## Repository hygiene
- 這個 repo 只放「skill 必要內容」（SKILL.md / references / scripts / templates）。
- 任何執行產物（logs/reports）請放 CI artifacts 或本機，不要 commit。
