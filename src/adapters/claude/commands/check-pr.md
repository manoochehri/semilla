---
description: Review a pull request and recommend merge or not
---
Review pull request $ARGUMENTS (if none given, list open PRs and ask which).

Use the **reviewer** subagent. If the PR touches secrets, permissions, `.github/workflows/`, or dependencies, also use the **security** subagent. Each posts its verdict on the PR as a real `gh pr review --comment` — that's not optional — with the verdict word as the first line of the body. Not `--approve` / `--request-changes`: GitHub refuses both while the agent and the PR author are the same account, i.e. every PR here (#44). Summarize both in under 15 lines: verdict, must-fix items, and whether CI is green. Ask whether to merge (only if verdict is merge/approve and CI is green).
