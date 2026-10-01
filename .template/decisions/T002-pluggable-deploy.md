# T002: Cloud-neutral core, no shipped deploy target

**Date:** 2026-09-27  **Status:** superseded
The core (Python, Docker, CI, secrets rules) never depends on a cloud. Each target in `infra/` implements one contract (secrets, build, gated deploy, status, rollback, budget, teardown). Kickoff keeps one target and deletes the rest. Default: none.

**Superseded 2026-10-01 (#103).** The decision to keep the core cloud-neutral stands. Shipping
provider trees did not: `infra/` was three deploy targets for a repository that deploys nothing,
and a host inherited AWS bootstrap YAML it had no reason to keep. The deploy contract above is
still what a host should satisfy for whichever provider it chooses, but it is now guidance
recorded in `docs/RUNBOOK.md` rather than a directory Trazo ships.
