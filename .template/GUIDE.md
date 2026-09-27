# Using semilla

A practical guide: how to start a project, run it day to day, and get unstuck.
For what semilla is and what's included, see the [README](../README.md). For the daily loop and a full FAQ once a project is running, see the [playbook](PLAYBOOK.md).

---

## 1. The AI team

semilla runs a small team: you plus several Claude roles. **The agents don't talk to each other directly; they communicate through GitHub.** The PM writes issues, the engineer turns issues into pull requests, the reviewer comments on pull requests, and you approve and merge. Everything is visible, and nothing depends on a chat surviving.

| Role | Who | Where they work | Triggered by |
|---|---|---|---|
| **Owner** | You | GitHub (phone or laptop), Claude app | You |
| **PM / advisor** | Claude, strong model (e.g., Opus) | Claude chat; scheduled GitHub runs | You, or a daily schedule |
| **Engineer** | Claude Code (e.g., Sonnet) | VS Code on your machine, or GitHub Actions | You, or `@claude` on an issue |
| **Reviewer** | Claude (e.g., Opus) | GitHub pull requests | Automatically on every pull request |

**Neither AI keeps memory between sessions.** The repo does. Every session starts by reading the docs and ends by updating them.

| | Claude (desktop/web app) | Claude Code (VS Code / terminal / GitHub) |
|---|---|---|
| **Good at** | Planning, deciding, reviewing results, writing issues | Changing files, running tests, git, pull requests |
| **Reads** | The repo (connect GitHub under *claude.ai Settings → Connectors*) | `CLAUDE.md` automatically, then `docs/` |
| **Uses** | The **project-kickoff** skill; `docs/ADVISOR.md` | Subagents `pm`, `reviewer`, `security`; commands (type `/`, or `/semilla` for a menu) |

---

### Subagents: the team inside Claude Code
Roles live in `.claude/agents/`: **pm**, **reviewer**, and **security** run on Opus and can't edit code; the main session is the engineer. In one Claude Code window, ask by name ("have security check this") or just describe the job; Claude Code hands off to the matching agent, which works in its own fresh context and reports back. Manage them with the built-in `/agents` command.

**You don't need to memorize commands.** Talk normally ("catch me up", "work on issue 12", "can I merge #15?", "wrap up"); `CLAUDE.md` maps requests to routines. If you want a menu, type `/semilla`. Typing `/` lists every command.

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

**Several windows?** Fine for talking and reviewing in parallel. Two windows *editing* the same folder will collide; use git worktrees for parallel building.

## 2. How you interact

Your two main tools: **a Claude chat for thinking, GitHub for approving.**

| You want to… | Do this |
|---|---|
| Think through an idea or problem | In Claude Code, `/pm` or just ask a planning question (the pm agent answers). From the Claude app: *"Act as the advisor for <owner>/<repo> per docs/ADVISOR.md."* |
| Add a task | Create a GitHub issue yourself, or ask the PM to. |
| Get work done (hands-on) | Open Claude Code in the repo and say *"work on issue 12"* (or `/work 12`). |
| Get work done (hands-off) | Comment `@claude implement this` on the issue. It opens a pull request when done. |
| Approve work | Read the reviewer's comments and CI result on the pull request, then merge. |
| Make a call | Answer `needs-decision` issues in a comment. |
| Know what's going on | Read the daily review on the pinned "Daily review" issue, or `docs/STATUS.md`. |

A typical loop:
```
you + PM (chat)  →  issues  →  engineer  →  pull request  →  reviewer + CI  →  you merge
                                    ↑                                              |
                                    └──────── daily PM review flags what's next ───┘
```

---

## 3. Setting up the automated team (GitHub Actions)

The automatic parts run on GitHub using Anthropic's official Claude Code GitHub Action. Three workflows:

| Workflow | Role | Runs when |
|---|---|---|
| `.github/workflows/claude.yml` | Engineer | Someone writes `@claude` in an issue or pull request |
| `.github/workflows/claude-review.yml` | Reviewer | A pull request is opened or updated |
| `.github/workflows/daily-review.yml` | PM | Every morning on a schedule (cron), plus a manual "Run workflow" button |

### One-time setup
1. **API key:** create one in the Anthropic Console. Usage is billed per token, separately from a Claude subscription. **Set a monthly spending limit in the Console.**
2. **Install the Claude GitHub app** on the repo. In Claude Code, run `/install-github-app`; it walks you through the app and the `ANTHROPIC_API_KEY` secret.
3. **Add the three workflows.** Ask Claude Code: *"Add claude.yml, claude-review.yml and daily-review.yml per .template/GUIDE.md section 3, using the current Claude Code Action docs. PM and reviewer on Opus, engineer on Sonnet. Cap turns per run. The daily review reads docs/ADVISOR.md and posts to a pinned 'Daily review' issue."*
4. **Test:** comment `@claude what's in this repo?` on any issue, and use "Run workflow" on the daily review.

### Guardrails
- The engineer only opens pull requests; branch protection means nothing reaches `main` without CI and your merge.
- CODEOWNERS still requires you for safety-critical paths, whoever wrote the change.
- Workflows get the minimum GitHub permissions they need.
- Cap turns/time per run and set the Console spending limit, so a loop can't run up a bill.

### Alternative: scheduled Claude tasks
The Claude app can also run scheduled tasks: a fresh session on a timer, with the repo attached (needs GitHub connected to Claude). Simpler to start, but it lives in your Claude account rather than the repo, so it doesn't copy to other projects. The GitHub workflows are the portable default.

---
## 4. Start a new project

### Option A: from a Claude chat (recommended)
1. Make sure the **project-kickoff** skill is saved in your Claude account.
2. Start a new chat: *"Let's kick off a new project."*
3. Answer its interview (idea, success criteria, budget, deadline, constraints, stop rule, UI, where it runs).
4. Approve the charter and plan it shows you.
5. It creates the repo and sets things up, or gives you instructions to paste into Claude Code.

### Option B: from Claude Code
```bash
gh repo create my-project --private --template <owner>/semilla --clone
cd my-project
make setup
claude
```
Then type `/kickoff`.

### What you'll be asked to do yourself
- Approve the charter, plan, and any cloud resources (with their monthly cost)
- Enter secrets (never in chat; kickoff tells you how)
- Confirm alert emails from your cloud provider (otherwise no alerts arrive)
- Turn on settings your GitHub plan doesn't allow via the API (kickoff will say which)

---

## 5. Day to day

### A work session (Claude Code)
```
/start      reads the docs, summarizes state, proposes work, waits for your OK
  ...it works on a branch and opens a pull request...
/wrapup     updates STATUS, records decisions, updates issues, pushes
```
Then review the pull request on GitHub. If CI is green and it looks right, merge.

### Getting advice (Claude)
Start a **fresh** chat and say:
> Act as the advisor for <owner>/<repo> per docs/ADVISOR.md.

Ask it what you'd ask a PM: *Are we on track? Is this result real? What should we do next? Is this worth the cost?* It writes conclusions back into the repo (decision records, issues, reports).

### Making a decision
In Claude Code: `/decide <what you decided>`. It drafts a numbered record with context, alternatives, and consequences for you to approve.

### Where to look
| Question | Look at |
|---|---|
| What's going on right now? | `docs/STATUS.md` |
| What's left to do? | GitHub Issues (filter by milestone) |
| What needs me? | Issues labeled `needs-decision` |
| Why did we do X? | `docs/decisions/` |
| How is experiment Y going? | `docs/workstreams/` |
| How do I deploy / roll back? | `docs/RUNBOOK.md` |
| Is the code healthy? | The **Actions** tab on GitHub |

---

## 6. Handing instructions from the advisor to the builder

When the advisor writes instructions for Claude Code, good instructions:
- **Stand alone.** A fresh session must understand them without the chat.
- **Define terms and include the numbers.** Don't say "the usual threshold."
- **Say what to verify** before relying on it.
- **Ask for the plan back first.** "Before starting, explain your plan and list anything unclear. Wait for my OK."
- **End with `/wrapup`**, so results land in the repo.

Better still: have the advisor open GitHub issues with those instructions, then tell Claude Code *"work the open issues in the current milestone."*

---

## 7. Secrets

- **Never paste a secret into any chat**, including this one. If you do by accident, replace (rotate) that key.
- **Local:** copy `.env.example` to `.env` and fill it in. It's git-ignored, and Claude Code is blocked from reading it.
- **Cloud:** use the provider's secret store. AWS: `scripts/put_secret.sh <name>`. Fly.io: `fly secrets set NAME=value`.
- **Check anytime:** `make scan` searches the whole git history for leaked secrets. CI runs the same check on every pull request.

---

## 8. CI, pull requests, and Dependabot

- **CI** runs on GitHub's servers every time you push or open a pull request. Results show on the pull request and in the **Actions** tab. You don't host anything.
- **Red X?** Click it, open the failed job, and paste the error to Claude Code: *"CI failed with this, fix it."*
- **Dependabot** opens pull requests weekly when tools have newer versions (grouped by type). If CI is green, merge. If red, the new version changed something; let Claude Code look.
- **Branch protection** (set at kickoff) means nothing reaches `main` without a passing pull request.

---

## 9. Deploying

Kickoff sets up at most one deploy target (see `infra/README.md`). Typical flow:
```
feature branch → pull request (CI) → merge to main → merge main into deploy → you click Approve on GitHub → deployed
```
Every target has: a budget alert, a status command, rollback to the previous version, and a one-command teardown. All are in `docs/RUNBOOK.md`.

**Cost tip:** estimates often miss disks, public IP addresses, and storage. Ask for a per-resource price list before approving.

---

## 10. Improving semilla

When a project teaches you something reusable (a mistake that cost time or money, or a rule that saved you):
1. In that project, run `/template-improve`.
2. Pick which lessons to keep.
3. It opens a pull request on semilla with the change, a new row in `.template/LESSONS.md`, and a version bump.

To bring improvements into an existing project: `/template-sync`. It never overwrites your project's own docs or code.

**Working on semilla itself:** open the semilla repo in Claude Code as you would any project. Its `docs/` folder stays blank; it's scaffolding for future projects. Changes go through pull requests like anything else.

---

## 11. Troubleshooting

| Problem | What to do |
|---|---|
| **The AI forgot what we were doing** | Start a fresh session. Claude Code: `/start`. Advisor: point it at `docs/ADVISOR.md`. That's what the docs are for. |
| **A session got long and confused** | Same: start fresh. Long sessions degrade; the repo doesn't. |
| **"Safeguards flagged this message" errors** | Sessions heavy on security topics (keys, permissions, network setup) can trip automatic filters by mistake. Start a fresh session; state is in the repo. |
| **Cloud login expired** | Sign in again (e.g., `aws login --profile <name>`). For deploys, use the GitHub workflow instead; it doesn't need your login. |
| **A scheduled job didn't run** | Check whether it was installed after its scheduled time. Ask for a "first run verified" check. |
| **Disk or cost growing unexpectedly** | Ask for status with disk-days-remaining and month-to-date cost. Recheck retention settings. |
| **An agent wants to loosen a safety limit** | Only you change those: CODEOWNERS requires your review. Ask it to show the evidence and write a decision record first. |
| **`@claude` does nothing** | Check the Claude GitHub app is installed, the `ANTHROPIC_API_KEY` secret exists, and the workflow run in the Actions tab for errors. |
| **API bill surprise** | Set a Console spending limit; cap turns per workflow run; turn off workflows you don't use. |
| **Results look great** | Ask how they're measured. Against external reality, with sample sizes? Or against the system's own assumptions? |

---

## 12. Glossary

- **Charter:** the one-page why/goal/constraints/stop-rule document.
- **Decision record:** a short numbered file explaining one decision; never edited, only superseded.
- **Workstream:** one feature, experiment, or strategy, with its hypothesis, tests, and evidence.
- **CI:** automatic checks on every change (tests, lint, secret scan, build).
- **Pull request (PR):** a proposed change, reviewed and checked before merging into `main`.
- **Dependabot:** GitHub's bot that proposes version updates.
- **Deploy target:** where the project runs (none, Fly.io, AWS, GCP).
- **OIDC:** lets GitHub deploy to a cloud without storing cloud passwords or keys.
- **GitHub Action / workflow:** an automated job defined in `.github/workflows/`, run by GitHub on its own servers.
- **`@claude`:** mentioning Claude in an issue or pull request, which triggers the engineer workflow.
- **Stop rule:** the evidence, decided in advance, that means stop or rethink.
