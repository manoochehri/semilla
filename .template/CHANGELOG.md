# Template changelog

## 0.3.0 (2026-09-27)
- Add `.template/PLAYBOOK.md`: the daily loop (the "game loop" diagram), the team table, and
  an FAQ covering planning, building, reviewing, deploying, money/safety, and troubleshooting.
  Linked from both READMEs and cross-linked with `.template/GUIDE.md`.

## 0.2.0 (2026-09-27)
- Subagents in `.claude/agents/`: pm, reviewer, security (Opus, read-only).
- Commands streamlined: `/semilla` (menu), `/work`, `/check-pr`, `/pm`, `/brief` (was `/status`, which clashed with a built-in); `/improve-template` and `/sync-template` renamed `/template-improve` and `/template-sync`.
- `CLAUDE.md` gains a team table and a plain-English → routine map, so commands are optional.
- Kickoff: branch-protection ruleset with a solo-owner caveat (no required approvals, since GitHub won't let an owner approve their own PR).
- `.template/GUIDE.md` rewritten: the AI team, subagents, the GitHub Actions engineer/reviewer/PM setup, and an expanded command table.

## 0.1.1 (2026-09-27)
Fixed the first-run CI failure: a job-level `hashFiles()` condition is invalid on GitHub
Actions and was moved inside the step. Switched gitleaks in CI from a Docker container to
a downloaded binary (the container tripped git's "dubious ownership" check on runners).
Fixed the Dockerfile so `uv run` doesn't try to write to the root-owned venv as a non-root
user (venv's `bin` added to `PATH`, entrypoint runs `python` directly). Grouped Dependabot
updates (uv, GitHub Actions). Updated pre-commit hook versions. Added `.template/GUIDE.md`,
linked from both READMEs.

## 0.1.0 (2026-09-27)
Initial version, distilled from a real project: docs-as-code state, decision records,
workstreams, advisor role, secrets-first setup, Python/uv/Docker, CI with gitleaks,
pluggable deploy targets (Fly, AWS; GCP stub), Claude Code session commands.
