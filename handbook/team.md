# The team

semilla runs a small team: you plus several Claude roles, talking to each other through GitHub, not through chat memory.

## Agents

| Agent | Model | Use for | Edits code? |
|---|---|---|---|
| (main session) | default (Sonnet) | Building: code, tests, git, pull requests | Yes |
| `pm` | Opus | Status, planning, priorities, "is this result real?", charter/budget/stop rule, writing issues | No |
| `reviewer` | Opus | Reviewing pull requests and diffs before merge | No |
| `security` | Opus | Secrets, permissions, workflows, dependencies, infra, repo security settings | No |

They're defined in `.claude/agents/` and can't edit code — only the main Claude Code session (the engineer) does. In one Claude Code window, ask by name ("have security check this") or just describe the job; Claude Code hands off to the matching agent.

## Commands

You don't need to memorize these — `CLAUDE.md` maps plain-English requests to the right one, and `/semilla` shows a menu. Typing `/` in Claude Code lists all of them.

| Command | Does |
|---|---|
| `/semilla` | Menu of what you can do right now |
| `/start` / `/wrapup` | Begin / end a work session |
| `/work 12` | Implement issue #12 → pull request (reviewer checks it first) |
| `/check-pr 15` | Review pull request #15 (reviewer, plus security if needed) |
| `/pm` | Talk to the PM agent |
| `/brief` | Quick status, changes nothing |
| `/decide …` | Draft a decision record |
| `/kickoff` | New-project setup |
| `/template-improve` / `/template-sync` | Send lessons to semilla / pull its updates |

## Plain English → routine

The owner shouldn't need to remember commands. `CLAUDE.md` maps requests like these to a routine or agent:

| If you say something like… | It does |
|---|---|
| "catch me up", "where are we", "what's next" | `/start` routine (or the `pm` agent for strategy questions) |
| "what can I do", "help", "menu" | `/semilla` |
| "work on issue 12", "fix X" | `/work` routine |
| "is this PR ok", "review #15", "can I merge" | `/check-pr` routine |
| "is this secure", "check permissions" | `security` agent |
| "should we…", "is this worth it", "plan the next milestone" | `pm` agent |
| "we decided…" | `/decide` routine |
| "wrap up", "done for today" | `/wrapup` routine |
| "GitHub/CI says …" (settings, failures) | handled directly; `security` for protection/permission settings |

See the [playbook](playbook.md) for how this plays out over a normal day, and the [guide](guide.md) for setting up the optional GitHub Actions versions of the PM and reviewer.
