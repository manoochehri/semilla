#!/usr/bin/env bash
# One-time: publish this folder as your public GitHub template repo, on branch "main".
# Usage: scripts/publish_template.sh <github-username> [repo-name]
set -euo pipefail
owner="${1:?usage: publish_template.sh <github-username> [repo-name]}"
name="${2:-semilla}"
for f in .github/CODEOWNERS LICENSE .template/UPSTREAM README.md; do
  sed -i.bak "s/OWNER/${owner}/g" "$f" && rm -f "$f.bak"
done
[ -d .git ] || git init -b main
git checkout -B main
git add -A
git commit -m "${name} $(cat .template/VERSION)"
gh repo create "${owner}/${name}" --public --source=. --remote=origin --push
gh repo edit "${owner}/${name}" --template --default-branch main
echo "Published https://github.com/${owner}/${name} (template, default branch: main)"
