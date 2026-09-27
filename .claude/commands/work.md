---
description: Implement a GitHub issue on a branch and open a pull request
---
Implement issue $ARGUMENTS.

1. Read the issue (`gh issue view`), CLAUDE.md rules, and any docs it links.
2. Explain your plan in a few lines and list anything unclear. Wait for my OK.
3. Create a branch `issue-<number>-<short-name>`. Make the change with tests.
4. Run `make test` and `make lint`. Fix failures.
5. Update docs the PR template asks for.
6. Ask the **reviewer** subagent to review the diff; fix must-fix items. If it touches secrets, permissions, workflows, dependencies, or infra, also ask the **security** subagent.
7. Push and open a pull request that closes the issue, with a summary of what changed, how it was tested, and the review results. Give me the link.
