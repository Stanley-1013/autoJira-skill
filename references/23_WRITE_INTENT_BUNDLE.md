# Canonical “write-intent” bundle (SSOT)

> Purpose: a single, reviewable structure that captures **exactly what will be written to Jira**.
>
> Use it for:
> - Confirm-before-write (show user a diff + payload before any write)
> - No-token / no-MCP mode (output an executable plan + payload skeleton, but do not write)
> - Execute + verify (read-back checks after writing)

## Bundle schema

```yaml
write_intent:
  action: transition|update_fields|add_comment|create_issue|assign|labels|bulk
  targets:
    issues: ["PROJ-123"]          # bulk: list all keys explicitly
    project: "PROJ"              # create_issue only
  read_back_required:
    - read_issue
    - list_transitions            # transition only
    - required_fields_if_any
  diff:
    status: "TODO -> IN_PROGRESS" # optional
    fields:
      assignee: "alice -> bob"    # optional
      priority: "P2 -> P1"        # optional
  payload:
    json: {"...":"..."}          # exact JSON that will be sent (or skeleton in no-token)
  guards:
    - "transition exists"
    - "required fields satisfied"
    - "scope minimal"
  risks:
    - "may move ticket unexpectedly if workflow differs"
  rollback:
    - "if wrong transition, stop + ask; do not attempt blind reverse"
  verify:
    - "read issue and confirm status/fields/comment match diff"
```

## Rules

- If token/permission is missing: you may still emit the bundle, but **must not execute**.
- For any write: show the bundle + a human-readable diff, then wait for explicit user confirmation.
