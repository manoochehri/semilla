---
description: Implement a GitHub issue on an isolated worktree branch and open a pull request
---
Implement issue $ARGUMENTS.

1. Read the issue (`gh issue view`), CLAUDE.md rules, and any docs it links.
2. Explain your plan in a few lines and list anything unclear. Wait for my OK.
3. Always branch from fresh `origin/main` in a dedicated worktree:
   `git fetch origin && git worktree add .worktrees/issue-<number>-<short-name> -b issue-<number>-<short-name> origin/main`
   Work inside that worktree directory. Each worktree has its own environment (run `make setup`). Make the first commit of the change (it doesn't need to be complete).
4. Push and open a pull request against base `main` that closes the issue, right after that first commit — so there's something for the reviewer/security subagents to comment on. Give me the link.
5. Finish the change with tests, running `make test` and `make lint` as you go and fixing failures. Update docs the PR template asks for (do not update VERSION/CHANGELOG in feature PRs; those are managed separately on release to avoid branch collision). Push additional commits to the same branch/PR.
6. Ask the **reviewer** subagent to review the PR; verify that the PR base branch is `main`. The subagent posts its verdict directly on the PR with `gh pr review --approve` or `gh pr review --request-changes` (not just a chat summary). Fix must-fix items and push. If the change touches secrets, permissions, workflows, dependencies, or infra, also ask the **security** subagent — it posts findings tied to this PR the same way via `gh pr review`; a security finding unrelated to this PR becomes its own GitHub issue instead.
7. Summarize what changed, how it was tested, and the review verdict. Give me the PR link.
