Pull newer template improvements into this project.

1. Read `.template/VERSION` and `.template/UPSTREAM`. Fetch the upstream template and read its `.template/CHANGELOG.md` for versions newer than ours.
2. Summarize what changed and which files it touches. Mark anything that conflicts with this project's own choices (its decision records win).
3. After my OK, apply the changes on a branch `template-sync-<version>`: template-owned files (`.template/`, `.claude/commands/`, `.github/` templates, CI, `infra/README.md`) are updated; project-owned files (`docs/*` content, `src/`, `CLAUDE.md` project rules) are merged by hand, never overwritten.
4. Update `.template/VERSION`, run tests, open a PR.
