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
| `docs/SKEPTIC_BAR.md` | The bar a result must clear before the skeptic passes it; filled in per project |
| GitHub Issues | Tasks. Labels: bug, feature, research, infra, needs-decision |

## The team (subagents in `.claude/agents/`, role commands in `.claude/commands/`)
Role commands (`/pm`) switch the session's role for the rest of the conversation until another role command is used; `/eng` returns to building. `reviewer`, `security`, and `skeptic` are subagent-only (never role-switch commands) — the engineer role delegates one-off checks to them, invoked ad hoc or as part of the `/work` and `/check-pr` routines. A review that grades the same conversation that produced the work is not a review. Every subagent verdict on a pull request posts as a real `gh pr review --comment`, with the verdict word as the first line of the body; `--approve` / `--request-changes` are refused while the agent and the PR author are the same account, i.e. every PR here (#44). A security finding not tied to a PR becomes a GitHub issue. See `docs/decisions/0003-review-security-github-tracked.md`.

| Role / Agent | Command | Model | Use for | Edits code? |
|---|---|---|---|---|
| Engineer (main session) | `/eng` | default (Sonnet) | Building: code, tests, git, pull requests | Yes |
| PM / advisor | `/pm` | Opus | Status, planning, priorities, "is this result real?", charter/budget/stop rule, writing issues | No |
| Reviewer (subagent only) | ask the **reviewer** subagent | Opus | Reviewing pull requests and diffs before merge | No |
| Security (subagent only) | ask the **security** subagent | Opus | Secrets, permissions, workflows, dependencies, infra, repo security settings | No |
| Skeptic (subagent only) | ask the **skeptic** subagent | Opus | Breaking a research/analysis result before it is acted on (rule 8) | No |

## Plain English → routine
The owner shouldn't need to remember commands. Map requests to routines:
| If the owner says something like… | Do |
|---|---|
| "catch me up", "where are we", "what's next" | `/start` routine (or `/pm` for strategy questions) |
| "what can I do", "help", "menu" | `/semilla` |
| "work on issue 12", "fix X" | `/work` routine — the commit message carries `Closes #12`, or a squash merge drops it and the issue stays open (#61) |
| "is this PR ok", "review #15", "can I merge" | `/check-pr` routine (or ask the **reviewer** subagent directly) |
| "is this secure", "check permissions" | ask the **security** subagent |
| "is this number real?", "poke holes in this analysis", "what would make this wrong?" | ask the **skeptic** subagent (rule 8) |
| "should we…", "is this worth it", "plan the next milestone" | `/pm` |
| "back to building", "ready to code" | `/eng` |
| "we decided…" | `/decide` routine |
| "wrap up", "done for today" | `/wrapup` routine |
| "GitHub/CI says …" (settings, failures) | handle it directly; ask the **security** subagent for protection/permission settings |

## Standing rules
1. **Secrets:** never read, print, log, commit, or paste secrets. Never open `.env` or anything in `secrets/`. The human enters secrets with `scripts/put_secret.sh`. New config goes in `.env.example` as a placeholder.
2. **Work on branches.** Open pull requests; never push to `main`. CI must pass.
3. **Verify, don't assume.** Check library source, live APIs, and real data before relying on behavior. Mark anything unverified.
4. **Measure against reality.** Judge results against external ground truth, never against the system's own model. Every number comes with its sample size.
5. **Safety limits are human-only.** Anything in `CODEOWNERS` (limits, infra, workflows) changes only with the owner's review. Automation may tighten, never loosen.
6. **Ask before guessing.** For anything expensive, irreversible, or ambiguous, stop and ask. Label the issue `needs-decision`.
7. **Leave state in the repo.** Decisions become decision records; design changes update ARCHITECTURE; end every session with `/wrapup`. Nothing important lives only in chat.
8. **A result is not a result until the skeptic has cleared it.** Any quantitative, experimental, or empirical claim — a measured number, a benchmark, a backtest, an A/B result, a performance or cost claim — goes to the **skeptic** subagent, which checks it against `docs/SKEPTIC_BAR.md` and returns *holds* / *holds with caveats* / *does not hold*. This is a gate, not advice: until it clears, the claim does not reach a decision-maker or a permanent record (`docs/decisions/`, `docs/workstreams/`, `docs/reports/`, `.template/LESSONS.md`), and nothing is built or deployed on the strength of it. Invoke it every time, not only when something looks suspicious — the failure it exists for is the result that looks fine. If it cannot run, say the result is unverified rather than proceeding. Record the verdict on the issue or PR; a verdict in chat gates nothing.
