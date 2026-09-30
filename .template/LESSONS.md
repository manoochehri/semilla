# Lessons learned

Each lesson: what happened, what it cost, and how the template now prevents it.
Add new lessons with `/template-improve`.

| # | Lesson | Source | Template change |
|---|---|---|---|
| 1 | Agents lose context on reset; a handoff kept only in chat had to be rebuilt from memory. | project 1 | State lives in `docs/`; `/start` and `/wrapup`; decision 0001 |
| 2 | One growing project log becomes unreadable and mixes status with history. | project 1 | Split into CHARTER / STATUS / decisions / workstreams / reports |
| 3 | A result scored against the system's own model looked positive when the real result, measured against the market, was negative. | project 1 | CLAUDE.md rule 4; PR checkbox; advisor checks evidence quality |
| 4 | An agent quietly loosened a safety threshold without approval. | project 1 | Safety paths in CODEOWNERS; rule 5; automation may only tighten |
| 5 | Notes claimed a library lacked a feature; nobody had checked its source, and it existed. | project 1 | CLAUDE.md rule 3: verify, mark unverified |
| 6 | Copy-pasting between advisor chat and coding agent lost information and time. | project 1 | ADVISOR.md; outcomes written to the repo; agents read the repo directly |
| 7 | Cloud access tied to a human login session (12h expiry) broke automation. | project 1 | OIDC deploy role; deploys gated by one-click environment approval |
| 8 | Nightly jobs scheduled before their timers were installed silently missed their first run. | project 1 | (not yet) add "first run verified" to deploy checklist |
| 9 | Data volume grew 5x after adding sources; 30-day retention would overflow the disk. | project 1 | (not yet) runbook: disk-days-remaining in status |
| 10 | Cost estimates left out disks and public IPs, roughly doubling the real monthly cost. | project 1 | (not yet) kickoff: price every resource before deploy |
| 11 | Instructions written for a fresh agent needed a glossary and an explain-it-back step to be understood reliably. | project 1 | ADVISOR.md "for the coding agent"; `/start` explain-back |
| 12 | Security-heavy sessions (IAM, secrets, network probes) can trip safety filters; fresh sessions with repo-held state recover cleanly. | project 1 | Disposable sessions + repo memory |
| 13 | The first CI run failed on a job-level `hashFiles()` condition; local YAML checks didn't catch it because the file only becomes invalid once GitHub evaluates it. | project 1 | CI: job-level `hashFiles()` conditions moved into the step, after checkout |
| 14 | A long list of commands is hard to remember. | semilla | Plain-English routing in CLAUDE.md; `/semilla` menu |
| 15 | Requiring PR approvals on a solo repo blocks the owner (can't approve own PRs). | semilla | Kickoff ruleset requires PR + CI, not approvals, when solo |
| 16 | A template-wide find/replace of the owner placeholder rewrote the path `.github/CODEOWNERS` into `.github/CODE<user>S`, so the file matched no rule and could be edited without owner review. | semilla | Substitution anchored to the `{{OWNER}}` placeholder (never a bare `OWNER`); test asserts CODEOWNERS covers itself |
| 17 | "Is this in the agent's context?" was being answered from recollection. A fresh headless session with every file-reading tool denied settles it: if a marker token comes back with no `tool_use` block in the transcript, it was inlined, not read. A no-import control case guards the negative. | semilla | Technique recorded in `docs/workstreams/claude-md-imports.md`; issue #38 |
| 18 | A root `CLAUDE.md` `@import` silently fails to expand when the session starts in a subdirectory: the file loads, the `@` line survives as literal text, and the rules do not. Contradicts the docs, and fails open — an agent runs ungoverned with nothing reporting it. | semilla | Launch agents from the repo root; CI assertion that every `@` target resolves |
| 19 | The local secrets gate mounted only the working tree. Inside a git worktree `.git` is a *file* pointing at the shared git dir, outside that mount, so gitleaks resolved no repository, scanned 0 commits, printed "no leaks found" and exited 0 — a gate reading green in the exact place worktrees made the default. A verification gate that cannot tell what it scanned is worse than no gate, because it is trusted. | semilla | `make scan` mounts the shared git dir and runs an in-container preflight that exits non-zero, with the reason, whenever git cannot resolve commits (issue #43) |
| 20 | The handoff protocol forbade the *engineer* answering in chat but said nothing about the *PM* asking the owner to pass work on, or a decision arriving in chat never reaching the issue — each a different clause in a different file, so fixing only the one that got reported left the loop open. A rule about who may say what is only as strong as the sentences nobody thought to write. | semilla | `pm.md` forbids routing work through the owner and requires a defended ranking of every open issue; `work.md` records a decision on the issue before acting on it; 8 guards (issue #57) |
| 21 | A result that looks internally consistent and reproducible is exactly the kind that survives review, because the agent that built it reads the output as if it meant what it meant. A second question in the same conversation inherits those blind spots, so an adversarial reviewer has to be a separate read-only subagent, invoked every time rather than when something looks suspicious. | semilla | `skeptic` subagent + `docs/SKEPTIC_BAR.md` + standing rule 8 gating quantitative claims before a permanent record (issue #58) |
