#!/usr/bin/env bash
# One-time: publish this folder as your public GitHub template repo, on branch "main".
# Usage: scripts/publish_template.sh <github-username> [repo-name]
set -euo pipefail
owner="${1:?usage: publish_template.sh <github-username> [repo-name]}"
name="${2:-semilla}"
# The username placeholder is "{{OWNER}}" — never a bare "OWNER". The path
# ".github/CODEOWNERS" contains "OWNER", so a plain s/OWNER/<user>/g rewrote the path
# to ".github/CODE<user>S" and the file stopped being covered by its own rules (issue #14).
replaced=0
for f in .github/CODEOWNERS LICENSE .template/UPSTREAM README.md; do
  if grep -q '{{OWNER}}' "$f"; then
    sed -i.bak "s/{{OWNER}}/${owner}/g" "$f" && rm -f "$f.bak"
    replaced=1
  fi
done
[ "$replaced" = 1 ] || echo "warning: no {{OWNER}} placeholder found; nothing to substitute" >&2
[ -d .git ] || git init -b main
git checkout -B main
git add -A
git commit -m "${name} $(cat .template/VERSION)"
gh repo create "${owner}/${name}" --public --source=. --remote=origin --push
gh repo edit "${owner}/${name}" --template --default-branch main
echo "Published https://github.com/${owner}/${name} (template, default branch: main)"
