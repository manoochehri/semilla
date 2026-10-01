# Trazo changelog

## 0.9.0 (2026-09-30)
- **Brand mark.** `handbook/assets/logo.svg` and `favicon.svg` are now the badge from the
  brand style guide — Cochineal Crimson `#C8102E`, Mayan Blue `#1FBCB3` — replacing the
  stroked `currentColor` wordmark. The badge is square and self-coloured, so it works as the
  site header, the favicon and a 16px GitHub glyph without inheriting a colour.
- **GitHub App assets** in `handbook/assets/brand/`: transparent PNGs at 16, 32, 64, 128,
  256, 512 and 1024. Use `trazo-1024.png` for the App icon and the org avatar.
- `test_the_logo_is_not_the_old_pun` no longer asserts the mark is wider than tall or uses
  `currentColor` — neither holds for a filled badge, and neither should. It now asserts the
  square viewBox and the brand palette, and a new test asserts the header mark and the
  favicon draw the **same** mark, since `mkdocs.yml` points at two separate files and
  nothing else would catch them drifting apart.
- The horizontal wordmark lockup is **not** included. It needs a real type tool to draw
  well, and the badge carries the identity on its own. Tracked in issue #83.

## 0.8.0 (2026-09-30)
- **`.claude/` is documented as an optional adapter, not part of the overlay.**
  `.trazo/adr/0007-claude-is-an-adapter.md` supersedes the "`.trazo/` plus `.claude/`"
  clause of ADR 0005, which contradicted 0005's own mount-time contract: naming
  `.claude/` as part of the overlay mandates a tool, in the sentence saying not to.
- `handbook/index.md`, `handbook/guide.md` and `README.md` now say to copy `.trazo/` and
  add the adapter for whichever agent you use, with `.claude/` scoped to Claude Code, and
  to merge into an existing adapter rather than replace it. **README had this wrong in
  three places**, including a FAQ answer, all inherited from ADR 0005.
- ADR 0007 also records that `AGENTS.md` is a different thing: it *describes a codebase*
  (commands, style, gotchas) and is rewritten as the project changes, while Trazo
  *governs the work on it* (roles, human-only limits, append-only decision records) and
  accumulates. They are not alternatives.
- `tests/test_claude_adapter_optional.py` pins the corrected phrasing so the universal
  claim cannot return. Verified by reinstating the exact wording from ADR 0005.

## 0.7.0 (2026-09-30)
- **`CLAUDE.md` now imports the rules instead of restating them.** It was a markdown link
  plus seven duplicated rules. Issue #53 called that "the same advisory-versus-mechanical
  failure this framework exists to prevent"; #38 then verified the mechanical form
  (`.trazo/workstreams/claude-md-imports.md`). The adapter is now one `@.trazo/rules.md`
  line, plus a table of where *this* tool satisfies each rule — no second statement of any
  rule, so the two cannot drift.
- **The fail-open guard #38 called mandatory is in place.** A missing or mistyped import
  target produces no error, no warning, and exit 0 — the session simply runs with no rules
  at all. `tests/test_adapter_import.py` now asserts every `@` target resolves, that the
  target still carries real content rather than an empty file, and that the duplicated rule
  list has not come back. Verified by breaking both on purpose and confirming the guards
  fail.
- `handbook/overlay.md` and `README.md` describe `CLAUDE.md` as an adapter that imports the
  rules, not as the place the rules live.

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
