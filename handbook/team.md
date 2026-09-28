# The team

semilla runs a small team: you plus several Claude roles, talking to each other through GitHub, not through chat memory.

## Roles and agents

| Role / Agent | Command | Model | Use for | Edits code? |
|---|---|---|---|---|
| Engineer (main session) | `/eng` | default (Sonnet) | Building: code, tests, git, pull requests | Yes |
| PM / advisor | `/pm` | Opus | Status, planning, priorities, "is this result real?", charter/budget/stop rule, writing issues | No |
| Reviewer | `/reviewer` | Opus | Reviewing pull requests and diffs before merge | No |
| Security | `/security` | Opus | Secrets, permissions, workflows, dependencies, infra, repo security settings | No |

They can be used in two ways:
1. **Direct role switching:** Type `/pm`, `/security`, or `/reviewer` in Claude Code to switch into that role for the rest of the conversation; `/eng` returns to building.
2. **Subagent delegation:** Roles are also defined in `.claude/agents/` as read-only Opus subagents. In engineer mode, Claude Code can delegate one-off reviews or checks to them without switching the whole conversation.

## Commands

You don't need to memorize these — `CLAUDE.md` maps plain-English requests to the right one, and `/semilla` shows a menu. Typing `/` in Claude Code lists all of them.

| Command | Does |
|---|---|
| `/semilla` | Menu of what you can do right now |
| `/start` / `/wrapup` | Begin / end a work session |
| `/work 12` | Implement issue #12 → pull request (reviewer checks it first) |
| `/check-pr 15` | Review pull request #15 (reviewer, plus security if needed) |
| `/pm` | Switch session to PM role (planning, priorities, issues) |
| `/security` | Switch session to security reviewer role (secrets, permissions, infra) |
| `/reviewer` | Switch session to code reviewer role (PRs, diffs, safety) |
| `/eng` | Return session to engineer role (code, tests, PRs) |
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
| "is this PR ok", "review #15", "can I merge" | `/check-pr` routine (or `/reviewer`) |
| "is this secure", "check permissions" | `/security` |
| "should we…", "is this worth it", "plan the next milestone" | `/pm` |
| "back to building", "ready to code" | `/eng` |
| "we decided…" | `/decide` routine |
| "wrap up", "done for today" | `/wrapup` routine |
| "GitHub/CI says …" (settings, failures) | handled directly; `/security` for protection/permission settings |

See the [playbook](playbook.md) for how this plays out over a normal day, and the [guide](guide.md) for setting up the optional GitHub Actions versions of the PM and reviewer.
