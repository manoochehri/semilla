# The team

semilla runs a small team: you plus several Claude roles, talking to each other through GitHub, not through chat memory.

## Roles and agents

| Role / Agent | Command | Model | Use for | Edits code? |
|---|---|---|---|---|
| Engineer (main session) | `/eng` | default (Sonnet) | Building: code, tests, git, pull requests | Yes |
| PM / advisor | `/pm` | Opus | Status, planning, priorities, "is this result real?", charter/budget/stop rule, writing issues | No |
| Reviewer | subagent only | Opus | Reviewing pull requests and diffs before merge | No |
| Security | subagent only | Opus | Secrets, permissions, workflows, dependencies, infra, repo security settings | No |
| Skeptic | subagent only | Opus | Breaking a research/analysis result before it is acted on | No |

They can be used in two ways:
1. **Direct role switching:** Type `/pm` in Claude Code to switch into the PM role for the rest of the conversation; `/eng` returns to building. Reviewer, security, and skeptic are subagent-only — never role-switch commands — so a review can't grade the same conversation's own work (see `.trazo/adr/0003-review-security-github-tracked.md`).
2. **Subagent delegation:** Roles are also defined in `.claude/agents/` as read-only Opus subagents. In engineer mode, Claude Code delegates to reviewer and security automatically as part of `/work` and `/check-pr`, or ad hoc, without switching the whole conversation.

## Commands

You don't need to memorize these — `CLAUDE.md` maps plain-English requests to the right one, and `/semilla` shows a menu. Typing `/` in Claude Code lists all of them.

| Command | Does |
|---|---|
| `/semilla` | Menu of what you can do right now |
| `/start` / `/wrapup` | Begin / end a work session |
| `/work 12` | Implement issue #12 → pull request (reviewer checks it first) |
| `/check-pr 15` | Review pull request #15 (reviewer, plus security if needed) |
| `/pm` | Switch session to PM role (planning, priorities, issues) |
| `/eng` | Return session to engineer role (code, tests, PRs) |
| ask the **security** subagent | Secrets, permissions, infra (no role switch) |
| ask the **reviewer** subagent | PRs, diffs, safety (no role switch) |
| ask the **skeptic** subagent | Break a research/analysis result before it counts (no role switch) |
| `/brief` | Quick status, changes nothing |
| `/decide …` | Draft a decision record |
| `/kickoff` | New-project setup |
| `/template-improve` / `/template-sync` | Send lessons to semilla / pull its updates |

## Plain English → routine

The owner shouldn't need to remember commands. `CLAUDE.md` maps requests like these to a routine or role:

| If you say something like… | It does |
|---|---|
| "catch me up", "where are we", "what's next" | `/start` routine (or `/pm` for strategy questions) |
| "what can I do", "help", "menu" | `/semilla` |
| "work on issue 12", "fix X" | `/work` routine |
| "is this PR ok", "review #15", "can I merge" | `/check-pr` routine (or ask the **reviewer** subagent directly) |
| "is this secure", "check permissions" | ask the **security** subagent |
| "is this number real?", "poke holes in this analysis" | ask the **skeptic** subagent |
| "should we…", "is this worth it", "plan the next milestone" | `/pm` |
| "back to building", "ready to code" | `/eng` |
| "we decided…" | `/decide` routine |
| "wrap up", "done for today" | `/wrapup` routine |
| "GitHub/CI says …" (settings, failures) | handled directly; ask the **security** subagent for protection/permission settings |

See the [playbook](playbook.md) for how this plays out over a normal day, and the [guide](guide.md) for setting up the optional GitHub Actions versions of the PM and reviewer.
