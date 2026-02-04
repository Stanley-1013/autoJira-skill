# autojira-skill (lab)

讓「人類工程師使用 Codex/Claude Code 等開發時」能用 **Jira MCP** 把專案管理融入日常 Git 流程：
- 查票 / 建票 / 改狀態 / 補 evidence comment
- Git ↔ Jira 同步（branch / commit / MR opened / MR merged / squash commit）
- 強制 read→propose→confirm→execute→verify（避免亂改票）
- 支援去重/冪等（rerun 不會重複貼一樣的 evidence）

> Requires Jira MCP tools (`mcp__Jira__*`). Without MCP credentials, the skill can still draft JQL / plans / payloads, but **must not write** to Jira.

## Prerequisites
- Jira MCP Server（提供 `mcp__Jira__*` 工具）
- Jira credentials（base url / email / api token 等，依你使用的 MCP server 設定）

## Quickstart (engineers)
入口：`SKILL.md`

常用範例（直接複製貼給 agent）：
- 「把 QQ-14 同步一下：我在 branch feature/QQ-14-squash，補上最新 commit evidence，狀態轉進行中。」
- 「QQ-14 MR 開了：<MR URL>。請在 Jira 補 MR opened evidence，狀態維持/轉到進行中。」
- 「QQ-14 MR merged：<MR URL>，squash commit <SHA>。請補 MR merged + commit evidence，然後轉完成。」

更多細節：`references/00_INDEX.md`

## Install (clone)

### Option A — general (any environment)
> Clone to any folder, then copy/symlink it into your agent’s skills directory.

```bash
git clone git@github.com:Stanley-1013/autoJira-skill.git
cd autoJira-skill
```

### Option B — Moltbot (Linux/macOS)
> Default Moltbot shared skills dir: `~/.clawdbot/skills/`

```bash
mkdir -p ~/.clawdbot/skills
cd ~/.clawdbot/skills
git clone git@github.com:Stanley-1013/autoJira-skill.git autojira-skill
```

### Option C — no SSH key (HTTPS)
```bash
git clone https://github.com/Stanley-1013/autoJira-skill.git
```

After install, restart/reload your agent (depends on host app), then verify the skill is visible.

## Repository hygiene
- Repo 只放「skill 必要內容」（SKILL.md / references / scripts / templates）。
- 本機 worklog / 執行產物不要 commit。
