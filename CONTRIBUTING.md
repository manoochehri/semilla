# Contributing to Trazo

Trazo is mounted onto a host repo, not forked from a template, so there is no automated
path for a host project to send a change back. If a mounted project learns something
reusable, note it in that project's own decision records — and when you are working **in
Trazo**, promote what is worth promoting, by hand, on a branch like any other change.

Every change should:
- solve a problem that actually happened (add a row to `.template/LESSONS.md`)
- keep the core cloud-neutral and lean (optional things go in `infra/<target>/` or behind kickoff questions)
- keep working for a host repo that already has its own runtime, docs and conventions
- bump `.template/VERSION` and add a `.template/CHANGELOG.md` entry
- contain no secrets, real data, or project-specific names (CI runs gitleaks)
