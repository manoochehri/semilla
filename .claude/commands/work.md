---
description: Implement a GitHub issue on an isolated worktree branch and open a pull request
---
Implement issue $ARGUMENTS.

1. Read the issue (`gh issue view`), CLAUDE.md rules, and any docs it links.
2. Explain your plan in a few lines and list anything unclear. If I'm in the conversation, wait for my OK. If the run is unattended — `@claude` on an issue, a schedule, or I simply don't answer — post the plan to the issue with `gh issue comment` and carry on. The plan goes on the ticket, not only in chat.
3. Always branch from fresh `origin/main` in a dedicated worktree:
   `git fetch origin && git worktree add .worktrees/issue-<number>-<short-name> -b issue-<number>-<short-name> origin/main`
   Work inside that worktree directory. Each worktree has its own environment (run `make setup`). Make the first commit of the change (it doesn't need to be complete).
4. Push and open a pull request against base `main` that closes the issue, right after that first commit — so there's something for the reviewer/security subagents to comment on. Give me the link.
5. Finish the change with tests, running `make test` and `make lint` as you go and fixing failures. Update docs the PR template asks for (do not update VERSION/CHANGELOG in feature PRs; those are managed separately on release to avoid branch collision). Push additional commits to the same branch/PR.
6. Ask the **reviewer** subagent to review the PR; verify that the PR base branch is `main`. The subagent posts its verdict directly on the PR with `gh pr review --approve` or `gh pr review --request-changes` (not just a chat summary). Fix must-fix items and push. If the change touches secrets, permissions, workflows, dependencies, or infra, also ask the **security** subagent — it posts findings tied to this PR the same way via `gh pr review`; a security finding unrelated to this PR becomes its own GitHub issue instead.
7. Summarize what changed, how it was tested, and the review verdict. Give me the PR link.

## When you hit something that blocks progress

The test for "blocked" is whether **progress stops**, not whether you have a question. Choices you can make yourself — library, naming, file layout, test structure — you make yourself, and you note them in the pull request.

When progress does stop:

1. **Post the question to the issue** with `gh issue comment`. Include what you tried, what you verified, the options you see, and which one you would pick. Do not put it only in chat.
2. **Label it:** `gh issue edit <n> --add-label needs-pm`.
3. **Call the `pm` subagent** for an assist, pointing it at the issue number.
4. **If it answers,** continue from that answer, and remove `needs-pm` if it is still on the issue (`gh issue edit <n> --remove-label needs-pm`).
5. **If it judges the call to be the owner's,** it applies `needs-decision` and assigns the owner. You stop there. Say so in chat in one line, with the issue link.

You never classify whether something is the owner's call yourself: you apply `needs-pm` and let the PM decide. While you wait, keep building anything that doesn't depend on the answer.
