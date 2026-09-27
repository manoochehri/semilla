# Contributing to semilla

Improvements come from real projects. The easiest path: in a project made from this template, run `/template-improve`; it proposes lessons, makes the change here on a branch, and opens a PR.

Every change should:
- solve a problem that actually happened (add a row to `.template/LESSONS.md`)
- keep the core cloud-neutral and lean (optional things go in `infra/<target>/` or behind kickoff questions)
- bump `.template/VERSION` and add a `.template/CHANGELOG.md` entry
- contain no secrets, real data, or project-specific names (CI runs gitleaks)
