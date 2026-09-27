# Using semilla

A practical guide: how to start a project, run it day to day, and get unstuck.
For what semilla is and what's included, see the [README](../README.md).

---

## 1. Who does what

semilla is designed around two kinds of AI sessions plus you.

| | Claude (desktop/web app) | Claude Code (in VS Code or terminal) | You |
|---|---|---|---|
| **Role** | Advisor and project lead | Builder | Owner |
| **Good at** | Planning, deciding, reviewing results, writing instructions | Changing files, running tests, git, pushing, opening PRs | Goals, money, approvals, anything irreversible |
| **Reads** | The repo (if GitHub is connected), docs you share | `CLAUDE.md` automatically, then `docs/` | Everything |
| **Uses** | The **project-kickoff** skill; `docs/ADVISOR.md` | `/start`, `/wrapup`, `/status`, `/decide`, `/kickoff`, `/improve-template`, `/sync-template` | GitHub, cloud consoles |

**Neither AI keeps memory between sessions.** The repo does. That's why every session starts by reading the docs and ends by updating them.

**Tip:** connect GitHub to Claude under *claude.ai Settings → Connectors*. Then the advisor can read the repo directly instead of you copying text between windows.

---

## 2. Start a new project

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

## 3. Day to day

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

## 4. Handing instructions from the advisor to the builder

When the advisor writes instructions for Claude Code, good instructions:
- **Stand alone.** A fresh session must understand them without the chat.
- **Define terms and include the numbers.** Don't say "the usual threshold."
- **Say what to verify** before relying on it.
- **Ask for the plan back first.** "Before starting, explain your plan and list anything unclear. Wait for my OK."
- **End with `/wrapup`**, so results land in the repo.

Better still: have the advisor open GitHub issues with those instructions, then tell Claude Code *"work the open issues in the current milestone."*

---

## 5. Secrets

- **Never paste a secret into any chat**, including this one. If you do by accident, replace (rotate) that key.
- **Local:** copy `.env.example` to `.env` and fill it in. It's git-ignored, and Claude Code is blocked from reading it.
- **Cloud:** use the provider's secret store. AWS: `scripts/put_secret.sh <name>`. Fly.io: `fly secrets set NAME=value`.
- **Check anytime:** `make scan` searches the whole git history for leaked secrets. CI runs the same check on every pull request.

---

## 6. CI, pull requests, and Dependabot

- **CI** runs on GitHub's servers every time you push or open a pull request. Results show on the pull request and in the **Actions** tab. You don't host anything.
- **Red X?** Click it, open the failed job, and paste the error to Claude Code: *"CI failed with this, fix it."*
- **Dependabot** opens pull requests weekly when tools have newer versions (grouped by type). If CI is green, merge. If red, the new version changed something; let Claude Code look.
- **Branch protection** (set at kickoff) means nothing reaches `main` without a passing pull request.

---

## 7. Deploying

Kickoff sets up at most one deploy target (see `infra/README.md`). Typical flow:
```
feature branch → pull request (CI) → merge to main → merge main into deploy → you click Approve on GitHub → deployed
```
Every target has: a budget alert, a status command, rollback to the previous version, and a one-command teardown. All are in `docs/RUNBOOK.md`.

**Cost tip:** estimates often miss disks, public IP addresses, and storage. Ask for a per-resource price list before approving.

---

## 8. Improving semilla

When a project teaches you something reusable (a mistake that cost time or money, or a rule that saved you):
1. In that project, run `/improve-template`.
2. Pick which lessons to keep.
3. It opens a pull request on semilla with the change, a new row in `.template/LESSONS.md`, and a version bump.

To bring improvements into an existing project: `/sync-template`. It never overwrites your project's own docs or code.

**Working on semilla itself:** open the semilla repo in Claude Code as you would any project. Its `docs/` folder stays blank; it's scaffolding for future projects. Changes go through pull requests like anything else.

---

## 9. Troubleshooting

| Problem | What to do |
|---|---|
| **The AI forgot what we were doing** | Start a fresh session. Claude Code: `/start`. Advisor: point it at `docs/ADVISOR.md`. That's what the docs are for. |
| **A session got long and confused** | Same: start fresh. Long sessions degrade; the repo doesn't. |
| **"Safeguards flagged this message" errors** | Sessions heavy on security topics (keys, permissions, network setup) can trip automatic filters by mistake. Start a fresh session; state is in the repo. |
| **Cloud login expired** | Sign in again (e.g., `aws login --profile <name>`). For deploys, use the GitHub workflow instead; it doesn't need your login. |
| **A scheduled job didn't run** | Check whether it was installed after its scheduled time. Ask for a "first run verified" check. |
| **Disk or cost growing unexpectedly** | Ask for status with disk-days-remaining and month-to-date cost. Recheck retention settings. |
| **An agent wants to loosen a safety limit** | Only you change those: CODEOWNERS requires your review. Ask it to show the evidence and write a decision record first. |
| **Results look great** | Ask how they're measured. Against external reality, with sample sizes? Or against the system's own assumptions? |

---

## 10. Glossary

- **Charter:** the one-page why/goal/constraints/stop-rule document.
- **Decision record:** a short numbered file explaining one decision; never edited, only superseded.
- **Workstream:** one feature, experiment, or strategy, with its hypothesis, tests, and evidence.
- **CI:** automatic checks on every change (tests, lint, secret scan, build).
- **Pull request (PR):** a proposed change, reviewed and checked before merging into `main`.
- **Dependabot:** GitHub's bot that proposes version updates.
- **Deploy target:** where the project runs (none, Fly.io, AWS, GCP).
- **OIDC:** lets GitHub deploy to a cloud without storing cloud passwords or keys.
- **Stop rule:** the evidence, decided in advance, that means stop or rethink.
