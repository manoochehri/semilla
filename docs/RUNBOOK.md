# Runbook

## Local
```
make setup     # deps + git hooks (gitleaks, ruff)
make test
make run
make build     # docker image
make scan      # scan git history for secrets
```

## Secrets
- Local: copy `.env.example` to `.env` and fill in. `.env` is git-ignored and blocked from Claude Code.
- AWS: `scripts/put_secret.sh <secret-name>` (you run it; it prompts without echoing).

## Deploy
TODO once infra exists: branch → PR → CI → merge to main → merge main into `deploy` → approve in GitHub → deploy workflow.

## Roll back
TODO

## Recurring
- Daily advisor review: TODO (scheduled task / GitHub Action)
- Weekly: dependency PRs from Dependabot

## Teardown
TODO
