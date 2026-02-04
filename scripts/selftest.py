#!/usr/bin/env python3
"""Lightweight offline self-test for scripts.

Goal: verify scripts run in a no-token environment, without large outputs.

Usage:
  python3 scripts/selftest.py

This test is intentionally small and fast.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=str(ROOT), check=True, stdout=subprocess.DEVNULL)


def main() -> int:
    # 1) help flags
    run(["python3", "scripts/pack_issue.py", "--help"])
    run(["python3", "scripts/pack_search.py", "--help"])
    run(["python3", "scripts/pack_dashboard.py", "--help"])
    run(["python3", "scripts/normalize_fields.py", "--help"])
    run(["python3", "scripts/git_helpers.py", "--help"])

    # 2) minimal functional smoke
    issue = {
        "key": "PROJ-1",
        "fields": {
            "summary": "Smoke test",
            "status": {"name": "To Do"},
            "issuetype": {"name": "Task"},
            "priority": {"name": "Medium"},
            "description": "hello\nworld",
        },
    }

    search = {
        "issues": [
            {
                "key": "PROJ-1",
                "fields": {
                    "summary": "Smoke test",
                    "issuetype": {"name": "Task"},
                    "status": {"name": "To Do"},
                    "priority": {"name": "Medium"},
                    "assignee": {"displayName": "Unassigned"},
                },
            }
        ],
        "total": 1,
        "startAt": 0,
        "maxResults": 50,
    }

    with tempfile.TemporaryDirectory() as td:
        p_issue = Path(td) / "issue.json"
        p_search = Path(td) / "search.json"
        p_issue.write_text(json.dumps(issue, ensure_ascii=False), encoding="utf-8")
        p_search.write_text(json.dumps(search, ensure_ascii=False), encoding="utf-8")

        # pack_issue / pack_search should run without error
        subprocess.run(["python3", "scripts/pack_issue.py", str(p_issue)], cwd=str(ROOT), check=True)
        subprocess.run(["python3", "scripts/pack_search.py", str(p_search)], cwd=str(ROOT), check=True)

        # pack_dashboard should run with a tiny synthetic data set
        dashboard_data = {
            "project": {"key": "PROJ", "name": "Sample Project"},
            "sprint": {"name": "Sprint 1", "issues": {"total": 10, "done": 7}},
            "issues": {"total": 120, "done": 80, "active": 40},
            "velocity": {"completed": [18, 20, 22], "committed": [20, 22, 24]},
            "quality": {"weekly_new_bugs": [4, 6, 5], "reopen_rate": [0.03, 0.04, 0.05], "high_pri_bugs": [2, 4, 3]},
            "scope": {"mid_sprint_add_rate": [0.08, 0.12, 0.10]},
            "resource": {"max_wip_per_person": [4, 6, 5], "unassigned_rate": [0.08, 0.12, 0.10]},
            "schedule": {"blocked_rate": [0.03, 0.08, 0.06], "not_started_rate": [0.25, 0.35, 0.30]},
        }
        p_dash = Path(td) / "dashboard.json"
        p_dash_out = Path(td) / "dashboard.html"
        p_dash.write_text(json.dumps(dashboard_data, ensure_ascii=False), encoding="utf-8")
        subprocess.run(
            [
                "python3",
                "scripts/pack_dashboard.py",
                "--data",
                str(p_dash),
                "--output",
                str(p_dash_out),
                "--offline",
            ],
            cwd=str(ROOT),
            check=True,
            stdout=subprocess.DEVNULL,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
