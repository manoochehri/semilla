---
description: "Set up a new project: interview, charter, plan, repo settings, first issues"
---
Run project kickoff for this repo (created from semilla).

1. Interview me briefly (one message, numbered questions): the idea, goal, measurable success criteria, budget (money/time), deadline, hard constraints (legal, location, platform terms), what we'll never do, the stop rule, whether it needs a UI, where it runs (none/local, Fly.io, AWS, GCP; see infra/README.md), and whether to publish a docs site for this project on GitHub Pages (default no).
2. Draft docs/CHARTER.md and docs/PLAN.md from my answers. Show me; wait for OK.
3. After OK: fill ARCHITECTURE, STATUS, RUNBOOK; replace TODOs in README, pyproject (name/description), CODEOWNERS (my GitHub username).
4. Create GitHub labels (bug, feature, research, infra, needs-decision), milestones from PLAN, and issues for the first milestone. Create a Project board if gh supports it on my account.
5. Once CI is green on main, add a ruleset for main (block force pushes and deletion, require a pull request and passing CI checks by their exact job names; do NOT require approvals if I'm the only collaborator, since GitHub won't let me approve my own PRs). Turn on secret scanning and push protection (`gh api` or tell me the settings page if my plan doesn't allow it).
6. Run `make setup`, `make test`, `make scan`. Fix anything failing.
7. Keep only the chosen deploy target in `infra/` and delete the others (or all of `infra/` if local-only). For the chosen target, follow its README; show me every resource and permission and the monthly cost before deploying anything.
8. Docs site: if I said no (the default), delete `handbook/`, `mkdocs.yml`, `.github/workflows/docs.yml`, and the `docs` dependency group in `pyproject.toml` — they came from semilla's own template docs and don't apply to this project. If I said yes: rewrite `handbook/index.md` for this project (from the charter, not semilla's), keep `handbook/team.md`, `lessons.md`, `changelog.md`, `contributing.md` if they still make sense here or delete them if they don't, enable Pages (`gh api repos/{owner}/{repo}/pages` with `build_type: workflow`, or tell me the settings page if that fails), and set the repo homepage to the Pages URL (`gh repo edit --homepage`).
9. Keep `.template/` as is (it records which template version this project came from). Write decision records for each tooling choice you made. Then /wrapup.
