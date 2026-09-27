---
description: Review a pull request and recommend merge or not
---
Review pull request $ARGUMENTS (if none given, list open PRs and ask which).

Use the **reviewer** subagent. If the PR touches secrets, permissions, `.github/workflows/`, dependencies, or `infra/`, also use the **security** subagent. Summarize both in under 15 lines: verdict, must-fix items, and whether CI is green. Ask whether to post the review as a PR comment, and whether to merge (only if verdict is merge and CI is green).
