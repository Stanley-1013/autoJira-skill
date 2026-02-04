# Idempotency / De-dup (SSOT guidance)

> Goal: avoid duplicate Jira comments/transitions when the same Git event is processed multiple times.
> This is critical for human-in-the-loop workflows (Codex/CLI), where retries and reruns are common.

## 1) What must be idempotent

### A) Evidence comments
Evidence comments (branch / commit / MR opened / MR merged / merge/squash commit) should be **idempotent**.

**Rule:** before adding an evidence comment, the agent must check whether the same event has already been recorded on the issue.

### B) Status transitions
Transitions should also be idempotent:
- If issue is already in the target status (or same status category), **do not transition**.
- Prefer to add a clarifying comment over forcing a status flip.

## 2) Canonical tagging format (recommended)

Use a short first-line tag so duplicates can be detected reliably.

**Tag line (first line of the Jira comment):**
- `AUTOJIRA: EVIDENCE <EVENT> <KEY>`

Where:
- `<EVENT>` one of: `BRANCH`, `COMMIT`, `MR_OPENED`, `MR_MERGED`, `MERGE_COMMIT`, `SQUASH_COMMIT`
- `<KEY>` is a stable unique key:
  - BRANCH: branch name
  - COMMIT: 40-char SHA
  - MR_*: MR URL
  - *_COMMIT: 40-char SHA

**Example (MR opened):**
- `AUTOJIRA: EVIDENCE MR_OPENED https://gitlab.com/org/repo/-/merge_requests/11`
- `MR opened: https://gitlab.com/org/repo/-/merge_requests/11`

## 3) How to detect duplicates (agent behavior)

Before writing:
1) Read the issue (at minimum: recent comments; if tooling doesn’t support comment search, read the latest N comments).
2) If an identical tag line exists → **skip** writing that comment.
3) If no tag exists (legacy comments), fall back to a best-effort match:
   - MR URL already present in a prior comment for the same event type → skip.

## 4) Batch confirmation (ties into confirm-before-write)

When multiple writes are planned (e.g., add 3 evidence comments + transition), bundle them into **one confirmation**:
- One write-intent bundle listing multiple actions (or a bulk section)
- One user OK
- Then execute sequentially with read-back verification

Reference:
- Confirm-before-write flow (SSOT): `references/24_CONFIRM_BEFORE_WRITE_FLOW.md`
- Write-intent bundle (SSOT): `references/23_WRITE_INTENT_BUNDLE.md`
