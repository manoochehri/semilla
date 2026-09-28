# semilla

**A self-improving template for starting software projects with AI coding agents.**

Every project grows from it, and each one sends what it learned back, so the next one starts smarter.

[:material-source-repository: Use this template](https://github.com/manoochehri/semilla/generate){ .md-button .md-button--primary }
[:material-book-open-page-variant: Read the playbook](playbook.md){ .md-button }

---

## The problem

Working with AI agents on a real project runs into the same problems again and again:

- **Agents forget.** Sessions end, contexts reset, and plans or decisions kept only in chat are lost.
- **Copy-paste glue.** Moving notes between an "advisor" chat and a coding agent by hand loses information.
- **Secrets leak easily.** Keys end up in `.env` files, logs, commits, or chat.
- **No project management.** No charter, no milestones, no record of *why* something was decided.
- **Results look better than they are.** Agents grade work against their own assumptions instead of reality.
- **Safety limits drift.** An agent "helpfully" loosens a threshold nobody approved.

semilla's answer: **the repo is the memory; agents are disposable.** Everything durable — goals, plans, design, decisions, status, results — lives in the repo as plain markdown. Any fresh agent session reads it and picks up where the last one stopped.

## How it works

A small team, talking to each other through GitHub — never through chat memory that can vanish with a closed window.

```mermaid
flowchart LR
    Owner(["You (owner)<br/>decide, approve, merge"])
    PM["PM role (/pm)<br/>plans, prioritizes, writes issues"]
    Engineer["Engineer role (/eng)<br/>builds, opens pull requests"]
    Reviewer["Reviewer role (/reviewer)<br/>checks pull requests"]
    Security["Security role (/security)<br/>checks secrets, permissions, infra"]
    GitHub[("GitHub<br/>issues · pull requests · docs/")]

    Owner <--> GitHub
    PM <--> GitHub
    Engineer <--> GitHub
    Reviewer <--> GitHub
    Security <--> GitHub
    GitHub -.->|assigns work| Engineer
    Engineer -.->|opens PR| Reviewer
    Reviewer -.->|flags risk| Security
    Reviewer -.->|verdict| Owner
```

The PM writes issues, the engineer turns issues into pull requests, the reviewer comments on pull requests, and you approve and merge. You can switch between roles directly in Claude Code (`/pm`, `/security`, `/reviewer`, `/eng`), or let the engineer delegate checks to subagents. Everything is visible, and nothing depends on a chat surviving. See [the team](team.md) for the full roster, and the [playbook](playbook.md) for how a normal day actually runs.

## A normal day

```
you + PM (/pm)  →  issues  →  engineer (/eng)  →  pull request  →  reviewer (/reviewer) + CI  →  you merge
```

Ten to fifteen minutes of your attention: a morning briefing, a decision or two, a merge or two, and a one-line "wrap up" at the end. The [playbook](playbook.md) walks through the whole loop and has an FAQ for everything in between.

## Quick start

1. **Create a repo from this template:**
   ```bash
   gh repo create my-project --private --template manoochehri/semilla --clone
   cd my-project && make setup
   ```
   Or click **Use this template** above.
2. **Open it in Claude Code** and run `/kickoff`. It interviews you (idea, success criteria, budget, deadline, constraints, stop rule, where it runs), shows you the charter and plan, and sets everything up.
3. **Start working:** `/start` reads the docs and proposes what to do next; approve it and it opens a pull request when done.

See the [guide](guide.md) for the full setup walkthrough, including the optional GitHub Actions automation.
