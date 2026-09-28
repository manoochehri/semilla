---
description: Implement a GitHub issue on an isolated worktree branch and open a pull request
---
Implement issue $ARGUMENTS.

1. Read the issue (`gh issue view`), CLAUDE.md rules, and any docs it links.
2. Explain your plan in a few lines and list anything unclear. Wait for my OK.
3. Always branch from fresh `origin/main` in a dedicated worktree:
   `git fetch origin && git worktree add .worktrees/issue-<number>-<short-name> -b issue-<number>-<short-name> origin/main`
   Work inside that worktree directory. Each worktree has its own environment (run `make setup`). Make the change with tests.
4. Run `make test` and `make lint`. Fix failures.
5. Update docs the PR template asks for (do not update VERSION/CHANGELOG in feature PRs; those are managed separately on release to avoid branch collision).
6. Ask the **reviewer** subagent to review the diff; verify that the PR base branch is `main` and fix must-fix items. If it touches secrets, permissions, workflows, dependencies, or infra, also ask the **security** subagent.
7. Push and open a pull request against base `main` that closes the issue, with a summary of what changed, how it was tested, and the review results. Give me the link.
