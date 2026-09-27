---
description: "Set up a new project: interview, charter, plan, repo settings, first issues"
---
Run project kickoff for this repo (created from semilla).

1. Interview me briefly (one message, numbered questions): the idea, goal, measurable success criteria, budget (money/time), deadline, hard constraints (legal, location, platform terms), what we'll never do, the stop rule, whether it needs a UI, and where it runs (none/local, Fly.io, AWS, GCP; see infra/README.md).
2. Draft docs/CHARTER.md and docs/PLAN.md from my answers. Show me; wait for OK.
3. After OK: fill ARCHITECTURE, STATUS, RUNBOOK. Replace my name where the template owner left it: the `{{OWNER}}` placeholder and the owner's `@handle` (`.github/CODEOWNERS`, LICENSE, `.template/UPSTREAM`, README), plus the TODO names in README and pyproject (name/description). In `.github/CODEOWNERS` change only the handles — the paths must keep pointing at real files, and the file must still match a rule itself (`make test` checks this). Never run a plain find/replace of the word OWNER over that file: `CODEOWNERS` contains `OWNER`, which is exactly how issue #14 broke it.
4. Create GitHub labels (bug, feature, research, infra, needs-decision), milestones from PLAN, and issues for the first milestone. Create a Project board if gh supports it on my account.
5. Once CI is green on main, add a ruleset for main (block force pushes and deletion, require a pull request and passing CI checks by their exact job names; do NOT require approvals if I'm the only collaborator, since GitHub won't let me approve my own PRs). Turn on secret scanning and push protection (`gh api` or tell me the settings page if my plan doesn't allow it).
6. Run `make setup`, `make test`, `make scan`. Fix anything failing.
7. Keep only the chosen deploy target in `infra/` and delete the others (or all of `infra/` if local-only). For the chosen target, follow its README; show me every resource and permission and the monthly cost before deploying anything.
8. Keep `.template/` as is (it records which template version this project came from). Write decision records for each tooling choice you made. Then /wrapup.
