# Deploy targets (pluggable)

The core project is cloud-neutral: a Docker image, CI, and secrets kept out of git.
Each folder here is an **optional deploy target**. Kickoff keeps the one you choose and deletes the rest.

| Target | Best for | Status in template |
|---|---|---|
| none | Local-only projects, scripts, research | Default; delete `infra/` |
| `fly/` | Simplest cloud: small always-on or on-demand containers, cheap | Ready |
| `aws/` | Needs AWS services, specific regions, tight IAM | Ready (bootstrap + OIDC) |
| `gcp/` | Google Cloud (Cloud Run) | Stub: kickoff fills in when chosen |

## The contract every target implements
1. **Secrets:** stored in the target's secret store, injected at runtime; never in git or images. The human enters them via a script.
2. **Build:** CI builds the Docker image and tags it with the commit SHA.
3. **Deploy:** a `deploy` workflow in `.github/workflows/`, gated by the GitHub `production` environment (requires owner approval), with no long-lived cloud keys where the target supports OIDC.
4. **Status:** one command shows what's running, version, health, and cost if available.
5. **Rollback:** redeploy the previous SHA.
6. **Budget:** a spend alert set at kickoff.
7. **Teardown:** one documented command removes everything.

Document the chosen target's commands in `docs/RUNBOOK.md` and its layout in `docs/ARCHITECTURE.md`.
