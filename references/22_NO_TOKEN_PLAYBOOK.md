# No-token / No-MCP Playbook (離線模式)

> 目的：當 Jira MCP token/權限不可用（或使用者要求不碰 Jira）時，仍能完成「可執行的計畫 + 可驗證的 payload」，但**不做任何寫入**。

## When to enter no-token mode

- Jira MCP tools unavailable / auth failed (401/403)
- User explicitly says: "don’t call Jira" / "offline only" / "no token"
- Environment cannot reach Jira

## Operating rules

1) **No writes**: do NOT call create/update/transition/comment.
2) **Be explicit**: say you are in no-token mode.
3) **Output executable artifacts**:
   - JQL drafts (scoped + with limits)
   - Proposed field changes (as a diff)
   - Proposed transition intent (abstract state)
   - Draft JSON payload(s) (for later execution)
4) **Always add verification steps** (what to read/check before running writes later).

## Template: offline output bundle

### 1) Assumptions (ask if missing)

- Jira base URL: …
- Project key(s): …
- Issue type(s): …
- Workflow status names (if known): … (otherwise use abstract states)
- Required fields policy: …

### 2) Read plan (what to fetch once token is available)

- Issue read-back:
  - fields: status, assignee, priority, labels, components, fixVersions, customfields involved
- Available transitions
- Field schema (create/editmeta)

### 3) Proposed change (diff)

- Status: [TODO/IN_PROGRESS/IN_REVIEW/DONE] (abstract) → [target]
- Assignee: … → …
- Fields:
  - fieldA: old → new
  - fieldB: old → new

### 4) Draft payload(s)

Prefer emitting a single **write-intent bundle** (SSOT) that contains both the human diff and the JSON payload skeleton:
- SSOT: `references/23_WRITE_INTENT_BUNDLE.md`

Rules:
- In no-token mode, `payload.json` is allowed to be a **skeleton** (placeholders), but it should still be copy/paste-ready.
- Keep the payload minimal: only the fields you intend to change.

### 5) Safety / verification checklist

- [ ] Confirm issue key(s) are correct
- [ ] Confirm transitions exist for each issue
- [ ] Confirm required fields are present before transition
- [ ] Confirm scope is minimal (only necessary fields)
- [ ] Run writes one-by-one unless explicitly approved for bulk

### 6) Confirmation prompt

Use the skill’s Confirm-before-write template (see: `references/templates/comment_templates.md`).

---

## Worked Examples (離線示例)

### Example A: BRANCH_CREATED (feature/PROJ-123-*)

**Input**
- Event: `BRANCH_CREATED`
- Branch: `feature/PROJ-123-user-auth`

**Offline output bundle**
- Mode: no-token (no Jira calls)
- Proposed intent:
  - Issue: `PROJ-123`
  - Abstract status: TODO → IN_PROGRESS (proposal only)
  - Comment draft: “Started work on branch feature/PROJ-123-user-auth”
- Read plan (when token is available):
  - read issue `PROJ-123` (status/assignee/labels)
  - list transitions (to find a real transition that maps to IN_PROGRESS)
- Draft payloads (placeholders until transitions are known):
  - transition payload:
    ```json
    {"transition": {"id": "<transitionIdForInProgress>"}}
    ```
  - comment body:
    ```text
    Started work on branch: feature/PROJ-123-user-auth
    ```
- Verification:
  - Ensure `PROJ-123` exists and is not already DONE
  - Ensure an IN_PROGRESS-mapped transition exists

### Example B: COMMIT (PROJ-123 …)

**Input**
- Event: `COMMIT`
- Commit msg: `PROJ-123 feat(auth): add OAuth callback handler`
- Commit SHA: `abc1234` (example)

**Offline output bundle**
- Proposed intent: comment-only (no status change)
- Comment draft:
  ```text
  Commit abc1234: feat(auth): add OAuth callback handler
  ```
- Read plan (when token is available): read issue + confirm comment permission

### Example C: MR_MERGED ([PROJ-123] …)

**Input**
- Event: `MR_MERGED`
- MR URL: `https://git.example.com/org/repo/-/merge_requests/77`
- Merge SHA: `def5678` (example)

**Offline output bundle**
- Proposed intent:
  - Abstract status: IN_REVIEW/IN_PROGRESS → DONE (proposal only)
  - Comment draft includes MR URL + merge SHA
- Draft payloads (placeholders):
  ```json
  {"transition": {"id": "<transitionIdForDone>"}}
  ```
- Verification:
  - Fetch transitions first; confirm DONE mapping
  - If required fields are missing for DONE, stop and ask before writing

---

## Notes

- If a rule depends on workflow names (e.g., "In Review"), keep it abstract until transitions are fetched.
- Prefer conservative defaults: propose comment-only instead of transitions when unsure.
