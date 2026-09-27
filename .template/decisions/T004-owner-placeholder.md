# T004: The owner placeholder is `{{OWNER}}`, never a bare `OWNER`

**Date:** 2026-09-27  **Status:** accepted

The template writes the owner's GitHub username into files at publish and kickoff time. A bare `OWNER`
token is unsafe: it is a substring of `CODEOWNERS`, so `s/OWNER/<user>/g` rewrote the path
`.github/CODEOWNERS` into `.github/CODE<user>S`, leaving the file covered by no rule at all (issue #14,
present from 0.1.0). Rejected: word-boundary sed (`\b` is not portable between BSD and GNU sed, and
prose mentions of "owner" still match); per-file patterns (the same bug returns the first time a file
mentions CODEOWNERS). A token nobody types by accident keeps one substitution rule for every file, and
`tests/test_publish_template.py` pins the behavior.
