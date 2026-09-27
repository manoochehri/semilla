# .template: the template's own memory

This folder is about **semilla itself**, not the project built from it.
It travels with every project so the template can improve from real use.

**New here? Read [the guide](GUIDE.md).**

- `VERSION`: template version this project was created from (or last synced to)
- `CHANGELOG.md`: what changed in the template, by version
- `LESSONS.md`: lessons learned from real projects, each tied to a template change (or "not yet")
- `decisions/`: why the template is the way it is
- `UPSTREAM`: the template repo (`owner/semilla`)

Commands:
- `/improve-template`: turn lessons from this project into a PR against the template repo
- `/sync-template`: pull newer template improvements into this project

When working **on the template repo itself**, `CLAUDE.md`'s "project" means the template, and `docs/` stays as blank scaffolding for future projects: don't fill it in.
