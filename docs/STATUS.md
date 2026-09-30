# Status

> Replaced (not appended) at the end of every session by `/wrapup`. Keep under one screen.

**Updated:** 2026-09-30 by engineer (Claude Code)
**Phase / milestone:** handoff protocol (#35) landing; Trazo pivot (#48) awaiting the owner

## Running now
- Nothing in flight. No open PRs, no worktrees left from this session.

## Recently done
- **#36 merged (#41): agents hand off through GitHub, not through the owner.** `work.md` routes blockers to the issue (`needs-pm` → `pm` subagent → continue, or stop on `needs-decision`); `agents/pm.md` gained a scoped `gh issue edit` grant with `--body`/`gh issue close` withheld and a never-remove-`needs-decision` carve-out; `commands/pm.md` no longer contradicts it. 17 tests guard both surfaces.
- `kickoff.md` created `needs-decision` but not `needs-pm`/`P0`/`P1`/`P2`/`epic`, so in any derived project the protocol's first `gh` call would have failed and the engineer would have fallen back to stopping in chat — the `mmbot #13` failure #35 exists to kill. Caught in review, fixed in #41.
- The protocol was exercised on its own issue rather than demonstrated: a real scope blocker went to #36, got `needs-pm`, and the PM resolved it in the ticket.
- #38 merged (#46): CLAUDE.md `@import` behaviour verified.

## Blocked / needs a decision
- **#45 — owner review isn't enforced.** Verified: ruleset `protect main` is active with `required_approving_review_count: 0`, `require_code_owner_review: false`, `bypass_actors: []`. CODEOWNERS is advisory, and it omits `.claude/` and `CLAUDE.md` — the files that *are* the agent permission model. Adding those paths is safe now. **Do not raise the approval count first:** sole collaborator is `manoochehri`, who authors every PR, and GitHub refuses self-approval, so `1` would make every PR unmergeable. Blocked-by #44.
- **#44 — agents share the owner's GitHub identity.** The `needs-decision` gate is unauditable, and #36's proposed guard workflow cannot fire (the PM removing a label *is* the owner to `github.event.sender.login`). Needs a bot account + fine-grained PAT. The honour-system nature must be written down so it isn't mistaken for enforcement.
- **#42 — semilla has no charter of its own**, and the shipped stubs are the template's artifact. Note the conflict: #42 argues filling them here breaks the template, but #28 has already filled `.trazo/charter/charter.md` with semilla-specific content, so a fresh clone now inherits semilla's charter rather than a stub. `docs/PLAN.md` and this file remain stubs. Worth resolving together.
- **#48 — the Trazo pivot epic** carries `needs-decision`; #33's brief is written but unapproved. #49–#53 hang off it.
- Draft **decision 0005** (the `needs-decision` mechanic) is written and awaiting the owner's wording approval; not yet a file in `.trazo/adr/`.

## Next
1. **#43 (P0)** — `make scan` resolves no gitdir inside a worktree, scans 0 commits, prints "no leaks found" and exits 0. Since #19 made worktrees the default place engineers work, the local secrets gate reads green while checking nothing. CI still scans history, so nothing is exposed. Top engineer-actionable item; the fix must make the silent case exit non-zero.
2. **#47 (P1)** — six operative files tell subagents to post verdicts with `gh pr review --approve`/`--request-changes`, which GitHub refuses on self-authored PRs, i.e. every PR here. Both subagents hit it live this session and fell back to `--comment`. Document the fallback so each agent stops rediscovering it. Sub-issue of #44; `.trazo/adr/0003` is append-only and must stay byte-identical.
3. **#37 (P1)** — surface the work queue in `/start` (ready / blocked / waiting on owner). Unblocked now that #36 has merged.
4. **#39, #40, #34 (P2)** — the drift and docs cleanups #36 deliberately left out of scope.
