# T002: Cloud-neutral core, pluggable deploy targets

**Date:** 2026-09-27  **Status:** accepted
The core (Python, Docker, CI, secrets rules) never depends on a cloud. Each target in `infra/` implements one contract (secrets, build, gated deploy, status, rollback, budget, teardown). Kickoff keeps one target and deletes the rest. Default: none.
