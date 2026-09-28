<img src="handbook/assets/logo.svg" width="64" height="64" alt="semilla logo">

# semilla

**A self-improving template for starting software projects with AI coding agents.**

*Semilla* is Spanish for "seed." Every project grows from it, and each one sends what it learned back, so the next seed is better.

You bring an idea. A Claude session interviews you, writes a charter and plan, creates the repo, sets up tests, CI, containers, secrets handling, and (optionally) cloud deployment, then keeps the project organized day to day. Every project records what it learned, and those lessons flow back into this template, so the next project starts smarter.

> Status: early. Distilled from one real project; expect rough edges. See [`.template/VERSION`](.template/VERSION) for the current template version.

📖 **[Full documentation](https://manoochehri.github.io/semilla/)** — or read it here: **new here? [the guide](handbook/guide.md).** Already running a project? [the playbook](handbook/playbook.md) covers the daily loop.

---

## Why this exists

Working with AI agents on a real project runs into the same problems again and again:

- **Agents forget.** Sessions end, contexts reset, and plans or decisions kept only in chat are lost.
- **Copy-paste glue.** Moving notes between an "advisor" chat and a coding agent by hand loses information.
- **Secrets leak easily.** Keys end up in `.env` files, logs, commits, or chat.
- **No project management.** No charter, no milestones, no record of *why* something was decided.
- **Results look better than they are.** Agents grade work against their own assumptions instead of reality.
- **Safety limits drift.** An agent "helpfully" loosens a threshold nobody approved.

This template's answer: **the repo is the memory; agents are disposable.** Everything durable (goals, plans, design, decisions, status, results) lives in the repo as plain markdown. Any fresh agent session reads it and picks up where the last one stopped.

---

## What you get

| Area | What's included |
|---|---|
| **Project state** | `docs/`: charter, plan, architecture, status, runbook, numbered decision records, workstreams, reports |
| **Advisor role** | `docs/ADVISOR.md` turns any fresh session into the project's PM/advisor |
| **AI team** | Subagents in `.claude/agents/`: `pm`, `reviewer`, `security` (Opus, read-only) |
| **Commands** | `/semilla`, `/kickoff`, `/start`, `/work`, `/check-pr`, `/pm`, `/wrapup`, `/brief`, `/decide`, `/template-improve`, `/template-sync` (or just ask in plain English) |
| **Secrets from day one** | `.gitignore`, `.env.example`, gitleaks (pre-commit + CI), Claude Code blocked from reading `.env`, `scripts/put_secret.sh` |
| **Python** | uv, pytest, ruff, `src/` layout, Makefile |
| **Containers** | Dockerfile (non-root, uv), `compose.yaml` |
| **CI** | GitHub Actions on every PR: secret scan, lint, tests, Docker build, infra lint, docs-updated check |
| **Deploy (optional)** | Pluggable targets: none, Fly.io, AWS (budget alerts + GitHub OIDC + ECR), GCP (stub) |
| **Guardrails** | CODEOWNERS on safety-critical paths, PR template with doc checkboxes, branch protection at kickoff |
| **Self-improvement** | `.template/`: version, changelog, lessons learned, and design decisions for the template itself |

---

## Requirements

- A GitHub account and the [GitHub CLI](https://cli.github.com/) (`gh auth login`)
- [Claude Code](https://docs.claude.com/) (or another agent that can read `CLAUDE.md` and run commands)
- [uv](https://docs.astral.sh/uv/) and Docker
- Optional: a Fly.io, AWS, or GCP account if the project deploys somewhere

---

## Quick start

### Option A: let Claude do it (recommended)
In a Claude session that has the **project-kickoff** skill, say:

> Let's kick off a new project.

It interviews you, writes the charter and plan for your approval, creates the repo from this template, and sets everything up.

### Option B: by hand
```bash
gh repo create my-project --private --template manoochehri/semilla --clone
cd my-project
make setup          # installs dependencies and git hooks
claude              # start Claude Code in the repo
```
Then type `/kickoff`.

Kickoff asks about: the idea, measurable success criteria, budget and deadline, hard constraints, a stop rule, UI needs, and where it runs. It shows you the charter and plan before building anything, and shows every cloud resource and its cost before creating it.

---

## Day-to-day workflow

```
/start    → agent reads the docs, summarizes state, proposes the session's work, waits for OK
   ...work on a branch, open a pull request...
/wrapup   → agent updates STATUS, records decisions, updates issues, pushes, opens/updates the PR
```

- **Tasks** live in GitHub Issues, grouped by milestone. Anything waiting on you is labeled `needs-decision`.
- **Advice:** start a fresh session (a strong reasoning model works best) and say *"act as advisor per docs/ADVISOR.md"*. It reviews progress, evidence quality, safety, cost, and the stop rule, and writes its conclusions into the repo.
- **Decisions:** `/decide <what>` drafts a numbered decision record for your approval.

### How state is organized

| File | Changes | Answers |
|---|---|---|
| `docs/CHARTER.md` | Rarely | Why, goal, success criteria, budget, constraints, stop rule |
| `docs/PLAN.md` | When dates or scope change | Milestones and risks |
| `docs/ARCHITECTURE.md` | When the system changes | How it's built (with diagram) |
| `docs/STATUS.md` | Every session (replaced) | Where things stand right now |
| `docs/decisions/` | Append-only | What was decided and why |
| `docs/workstreams/` | As work progresses | Each feature/experiment: hypothesis, test, evidence, status |
| `docs/reports/` | Generated | Results over time |
| `docs/RUNBOOK.md` | When procedures change | How to run, deploy, roll back, recover |
| GitHub Issues | Constantly | What's being done, by when |

---

## Secrets

Secrets never go in git, images, logs, or chat.

- **Local:** copy `.env.example` to `.env` (git-ignored; Claude Code is denied read access).
- **Cloud:** the provider's secret store, injected at runtime. For AWS: `scripts/put_secret.sh <name>` prompts without echoing.
- **Enforced by:** gitleaks as a pre-commit hook and in CI (full history), GitHub secret scanning and push protection (turned on at kickoff), and `make scan` for a manual check.

---

## CI and deployment

CI runs on GitHub's own servers (no extra system needed). Workflows live in `.github/workflows/`; results appear in the repo's **Actions** tab and on each pull request.

Every pull request runs: gitleaks, ruff, pytest, a Docker build, cfn-lint (if AWS infra exists), and a check that infra changes come with ARCHITECTURE or RUNBOOK updates.

**Deploy targets** are pluggable (`infra/README.md`). The core never depends on a cloud; kickoff keeps the target you choose and deletes the rest:

| Target | Best for |
|---|---|
| none | Local tools, scripts, research (default) |
| Fly.io | Simplest cloud containers |
| AWS | AWS services, specific regions, fine-grained permissions |
| GCP | Cloud Run (stub, filled in at kickoff) |

Deploys are gated by a GitHub `production` environment that requires your approval: one click, no cloud login. On AWS, GitHub authenticates with OIDC, so no long-lived cloud keys are stored anywhere.

Suggested branch flow:
```
feature branch → pull request (CI) → main → deploy branch → approve → deployed
```

---

## Self-improving

This template carries its own memory in `.template/`:

| File | Purpose |
|---|---|
| `VERSION` | Template version a project was created from |
| `CHANGELOG.md` | What changed, by version |
| `LESSONS.md` | Real problems from real projects, and how the template now prevents them |
| `decisions/` | Why the template is designed this way |
| `UPSTREAM` | Where the template lives |

- **`/template-improve`** (run inside any project) reviews what that project learned, proposes reusable lessons, and opens a pull request against this template.
- **`/template-sync`** pulls newer template versions into an existing project, without overwriting the project's own docs or code.

---

## Repository layout

```
CLAUDE.md                  index + standing rules for agents
docs/                      project state (see table above)
.claude/                   Claude Code commands and permissions
.github/                   CI, PR template, CODEOWNERS, issue templates, Dependabot
.template/                 the template's own memory
infra/                     optional deploy targets (fly/, aws/, gcp/)
scripts/                   helper scripts (put_secret.sh)
src/app/, tests/           Python package and tests
Dockerfile, compose.yaml   containers
Makefile, pyproject.toml   tooling
```

---

## FAQ

**Can I use this for private projects?** Yes. Create a private repo from this public template.

**Do I need Claude?** The docs, CI, and structure work with any agent or none. The commands in `.claude/` and the kickoff skill are Claude-specific.

**Does it cost anything?** The template is free. GitHub Actions is free for public repos and includes a monthly allowance for private ones. Cloud costs depend on your deploy target; kickoff sets a budget alert first.

**Not Python?** Swap `pyproject.toml`, the Makefile targets, and the CI test job. Everything else is language-neutral.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The easiest path is `/template-improve` from a real project.

## License

[MIT](LICENSE)
