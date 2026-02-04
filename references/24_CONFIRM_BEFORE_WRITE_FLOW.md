# Canonical flow: read → propose → confirm → execute → verify (SSOT)

> Purpose: single source of truth for **agent UX** and safety flow for any Jira write.
> This flow is intentionally conservative.

## 0) Stop conditions (always)

Stop and ask the user (no write) if:
- auth/token missing (401/403)
- rate limited / throttled (429) or request repeatedly fails
- no-MCP / no-token mode is in effect → output a dry-run plan + draft payloads (see `references/22_NO_TOKEN_PLAYBOOK.md`)
- issue key is missing/ambiguous
- transition not available (not returned by list_transitions)
- required fields are unknown or unmet
- the user did not explicitly confirm

## 1) Read (read-back required)

Before any write, gather current state:
- read issue (status, assignee, labels, required fields if relevant)
- list transitions (for status changes)

## 2) Propose (human summary)

Emit a short intent summary:
- what action(s) you propose and **why now**
- what will *not* be changed (scope boundaries)

## 3) Confirm (confirm-before-write)

Use the confirm template and include:
- human diff (current → proposed)
- **write-intent bundle (SSOT)**: `references/23_WRITE_INTENT_BUNDLE.md`
- explicit reply controls: **OK** to proceed / **NO** to abort

Batching guidance (recommended):
- If you plan multiple writes (e.g., add 3 evidence comments + transition), bundle them into **one** confirmation.
- Before proposing evidence comments, apply de-dup/idempotency checks.

De-dup SSOT: `references/25_IDEMPOTENCY_DEDUP.md`

## 4) Execute

Only after the user replies OK (and you have write permission):
- execute the single minimal write implied by the bundle

## 5) Verify (read-back)

Immediately read-back and verify:
- status / fields / comment match the diff
- if mismatch: stop; do not attempt blind “fixups”
