---
description: Send lessons from this project back to semilla as a pull request
---
Improve the upstream template (repo in `.template/UPSTREAM`) using what this project learned. $ARGUMENTS

1. Review this project's docs/decisions/, docs/STATUS.md history (git log), closed issues, and our conversation for reusable lessons: mistakes that cost time or money, workarounds, rules that helped. Skip anything project-specific.
2. List candidate lessons for me in one message: what happened, what it cost, and the proposed template change (a rule, a file, a check, a command). Wait for my picks.
3. For the chosen ones: clone the upstream template to a temp folder, branch `lesson/<short-name>`, make the changes, add rows to `.template/LESSONS.md` (project name, lesson, change), bump `.template/VERSION` (patch for docs/rules, minor for new files/commands), add a `.template/CHANGELOG.md` entry, and add a `.template/decisions/T###` record for any design change.
4. Never copy secrets, real data, or project-specific names into the template. Run gitleaks on the diff.
5. Open a PR on the template repo and give me the link.
