---
description: "End a work session: update STATUS, decisions, issues; push"
---
End a work session.
1. Rewrite docs/STATUS.md (replace, don't append; keep under one screen): date, milestone, running now, recently done, blocked/needs-decision, next.
2. For each decision made this session, add a numbered file in docs/decisions/ (use the template). Ask me to confirm the wording first.
3. Update any docs/workstreams/ file whose status or evidence changed, and ARCHITECTURE/RUNBOOK if the system changed.
4. Close finished issues with a one-line comment; open issues for new work; label needs-decision where I must choose.
5. Commit on the current branch, push, and open or update the PR. Report the PR link and anything I need to do.
6. Teardown / cleanup: for any merged feature branch that used an isolated worktree, remove the worktree and clean up the local branch:
   `git worktree remove .worktrees/<name> && git branch -d <name>`
   Run `git worktree prune` to keep worktree tracking clean.
