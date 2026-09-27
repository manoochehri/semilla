# Fly.io target

Setup (human, once): `brew install flyctl`, `fly auth login`, then `fly launch --no-deploy` (creates `fly.toml`; pick a region near your data/APIs).
- Secrets: `fly secrets set NAME=value` (run it yourself; never paste values into chat).
- CI deploy: create a deploy token (`fly tokens create deploy`) and store it as the GitHub **environment** secret `FLY_API_TOKEN` in the `production` environment.
- Deploy workflow: `.github/workflows/deploy-fly.yml` (rename to activate).
- Status: `fly status`, `fly logs`. Rollback: `fly deploy --image <previous image>`.
- Budget: set a spending limit/alert in the Fly dashboard.
- Teardown: `fly apps destroy <app>`.
