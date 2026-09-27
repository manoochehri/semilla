# CLAUDE.md

**Read first, every session:** `docs/CHARTER.md` and `docs/STATUS.md`. Then open GitHub issues for the current milestone.

## Where things live
| Doc | Purpose |
|---|---|
| `docs/CHARTER.md` | Why, goal, success criteria, budget, hard constraints, stop rule |
| `docs/PLAN.md` | Milestones and timeline |
| `docs/ARCHITECTURE.md` | How the system is built (with diagram) |
| `docs/STATUS.md` | Current state only; replaced each session |
| `docs/RUNBOOK.md` | How to run, test, deploy, roll back, recover |
| `docs/decisions/` | Numbered decision records. Append-only; supersede, never edit |
| `docs/workstreams/` | One file per feature/experiment/strategy, with status and evidence |
| `docs/reports/` | Dated reports and generated results |
| `docs/ADVISOR.md` | The advisor/PM role |
| GitHub Issues | Tasks. Labels: bug, feature, research, infra, needs-decision |

## Standing rules
1. **Secrets:** never read, print, log, commit, or paste secrets. Never open `.env` or anything in `secrets/`. The human enters secrets with `scripts/put_secret.sh`. New config goes in `.env.example` as a placeholder.
2. **Work on branches.** Open pull requests; never push to `main`. CI must pass.
3. **Verify, don't assume.** Check library source, live APIs, and real data before relying on behavior. Mark anything unverified.
4. **Measure against reality.** Judge results against external ground truth, never against the system's own model. Every number comes with its sample size.
5. **Safety limits are human-only.** Anything in `CODEOWNERS` (limits, infra, workflows) changes only with the owner's review. Automation may tighten, never loosen.
6. **Ask before guessing.** For anything expensive, irreversible, or ambiguous, stop and ask. Label the issue `needs-decision`.
7. **Leave state in the repo.** Decisions become decision records; design changes update ARCHITECTURE; end every session with `/wrapup`. Nothing important lives only in chat.
