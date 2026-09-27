# Lessons learned

Each lesson: what happened, what it cost, and how the template now prevents it.
Add new lessons with `/improve-template`.

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
