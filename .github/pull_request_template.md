## What and why
Closes #<issue-number> in the **commit message** too, not just here — a squash merge drops the PR body's keyword and the issue stays open (#61).

## Checks
- [ ] Tests added/updated and passing
- [ ] No secrets, keys, or real data in the diff
- [ ] Changed the system's shape? Updated `.trazo/ARCHITECTURE.md`
- [ ] Changed how to run/deploy/recover? Updated `docs/RUNBOOK.md`
- [ ] Made a decision? Added `.trazo/adr/NNNN-*.md`
- [ ] Changed a workstream's status or evidence? Updated `.trazo/workstreams/`
- [ ] Numbers reported with sample sizes and measured against external reality
- [ ] Learned something reusable? Added to `.template/LESSONS.md`
