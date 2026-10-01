# Trazo changelog

## 0.6.0 (2026-09-30)
- **A release is now a git tag.** `make release` validates the tree, the version, and
  the changelog, then creates and pushes annotated tag `vX.Y.Z`. `latest` means the
  highest release tag. Until this shipped the repository had **zero tags**, so no host
  could pin a version — see `.trazo/adr/0006-release-process.md`.
- New rule in `.trazo/rules.md`: *releases are immutable tags* — never a branch, never a
  moved tag, always cut from an already-pushed commit.
- `CONTRIBUTING.md` records that the version bump and the changelog entry ship in the
  same commit, and that the release is cut after merge.
- **0.1.0 through 0.5.0 were never tagged** and are not backfilled. Tagging commits that
  were released under an earlier process would fabricate a release record. `0.6.0` is
  the first version released as a tag.

---

## Versions withdrawn on 2026-10-01

**There is no released version above `0.6.0`.** This section records what the file used to
claim, and why it no longer does.

Entries `0.7.0`, `0.8.0` and `0.9.0` appeared here as released versions. Two of them
(`v0.7.0`, `v0.9.0`) were cut as tags; `0.8.0` never was. **Both tags were deleted on
2026-10-01** because the product was not finished, and nobody could have been holding
them: no installer resolved tags (#53 is open), and no script in `scripts/` reads a ref.

Leaving the entries above would make the changelog claim releases that a consumer cannot
resolve, which is the exact defect this file exists to prevent. The work described in
those entries was real and is preserved in git history; it simply was not a release.

See `.trazo/adr/0009-tag-immutability-binds-from-first-consumer.md`: a tag is immutable
from the first *external consumer*, and there is not one yet. The next entry written here
will be the first honest one.

## 0.5.0 (2026-09-28)
- Role commands: `/pm`, `/security`, `/reviewer`, and `/eng` in `.claude/commands/`.
  Each command switches the session into that role directly for subsequent conversation turns
  until another role command is used.
- One-liner prompt response pattern: when invoked without arguments, roles reply with a brief
  one-liner acknowledgment and model switch tip (e.g., `(tip: /model opus)`) rather than
  printing unprompted reports; when invoked with arguments, they answer immediately.
- Non-engineer roles (`pm`, `security`, `reviewer`) enforce read-only instructions (no code or config edits).
- Preserved `.claude/agents/*.md` for one-off subagent delegation from the engineer session.
- Updated documentation across `CLAUDE.md`, `README.md`, handbook (`index.md`, `guide.md`, `playbook.md`, `team.md`),
  and `.claude/commands/semilla.md`.

## 0.4.0 (2026-09-27)
- Docs site: MkDocs + Material, source in `handbook/` (not `docs/`, which stays project
  scaffolding). Moved `GUIDE.md` and `PLAYBOOK.md` into `handbook/`; added a Home page, a
  team page, and pages that include (not copy) `.template/LESSONS.md`, `CHANGELOG.md`, and
  `CONTRIBUTING.md`. Converted the playbook's ASCII game-loop diagram to Mermaid.
- Added an original flat SVG logo (seed/sprout) as the site logo, favicon, and README mark.
- `.github/workflows/docs.yml`: builds on every PR (`mkdocs build --strict`, fails on broken
  links) and deploys to GitHub Pages on merge to `main`, gated to `manoochehri/semilla` so
  projects created from the template don't publish by accident.
- `make docs` to preview locally. Kickoff gained an optional "publish a docs site?" question
  (default no); saying no removes `handbook/`, `mkdocs.yml`, and the docs workflow.

## 0.3.0 (2026-09-27)
- Add `.template/PLAYBOOK.md`: the daily loop (the "game loop" diagram), the team table, and
  an FAQ covering planning, building, reviewing, deploying, money/safety, and troubleshooting.
  Linked from both READMEs and cross-linked with `.template/GUIDE.md`.

## 0.2.1 (2026-09-27)
- Fixed `.github/CODEOWNERS` not protecting itself: the publish-time find/replace had rewritten
  the path to `.github/CODE<user>S`, so the file matched no rule and could be edited without owner
  review (issue #14, present since 0.1.0).
- `scripts/publish_template.sh` now substitutes the `{{OWNER}}` placeholder — never a bare `OWNER`,
  which is a substring of `CODEOWNERS` — and warns when there is nothing to replace.
- `/kickoff` replaces placeholders and `@handles` only, never the paths in CODEOWNERS.
- Tests: CODEOWNERS must cover itself and its paths must not contain the owner's name (issue #14);
  the publish script is exercised against a throwaway fixture with stub `git`/`gh`.

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
