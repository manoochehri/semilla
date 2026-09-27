"""The publish-time owner substitution must never rewrite `.github/CODEOWNERS` (issue #14).

`scripts/publish_template.sh` runs inside a throwaway copy of the template with stub
`git` and `gh` on PATH, so nothing here touches this repository or GitHub.
"""

import os
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "publish_template.sh"

FIXTURE = {
    ".github/CODEOWNERS": (
        "# Owner must review safety-critical paths. Replace {{OWNER}} at kickoff.\n"
        "/infra/                  @{{OWNER}}\n"
        "/.github/workflows/      @{{OWNER}}\n"
        "/.github/CODEOWNERS      @{{OWNER}}\n"
    ),
    "LICENSE": "Copyright (c) 2026 {{OWNER}}\n",
    ".template/UPSTREAM": "{{OWNER}}/semilla\n",
    ".template/VERSION": "0.0.0\n",
    "README.md": (
        "| **Guardrails** | CODEOWNERS on safety-critical paths |\n"
        "\n"
        "gh repo create my-project --template {{OWNER}}/semilla --clone\n"
    ),
}


def _write(root: Path, files: dict[str, str]) -> None:
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _stub(bindir: Path, tool: str) -> None:
    """No-op `git`/`gh` on PATH, logging its arguments."""
    stub = bindir / tool
    stub.write_text(f'#!/bin/sh\necho {tool} "$@" >> "{bindir}/{tool}.log"\n', encoding="utf-8")
    stub.chmod(0o755)


def _run(root: Path, owner: str = "newuser") -> subprocess.CompletedProcess[str]:
    bash = shutil.which("bash")
    assert bash, "bash is required to run scripts/publish_template.sh"
    bindir = root / "bin"
    bindir.mkdir(exist_ok=True)
    for tool in ("git", "gh"):
        _stub(bindir, tool)
    env = {**os.environ, "PATH": f"{bindir}{os.pathsep}{os.environ['PATH']}"}
    result = subprocess.run(  # noqa: S603 - our own argv, stub PATH, throwaway cwd
        [bash, str(SCRIPT), owner, "myproject"],
        cwd=root,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return result


def test_substitution_replaces_placeholder_and_keeps_the_path(tmp_path: Path):
    _write(tmp_path, FIXTURE)

    _run(tmp_path)

    codeowners = (tmp_path / ".github/CODEOWNERS").read_text(encoding="utf-8")
    assert "/.github/CODEOWNERS      @newuser" in codeowners
    assert "{{OWNER}}" not in codeowners
    assert (tmp_path / ".template/UPSTREAM").read_text(encoding="utf-8") == "newuser/semilla\n"
    assert "2026 newuser" in (tmp_path / "LICENSE").read_text(encoding="utf-8")
    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "CODEOWNERS on safety-critical paths" in readme
    assert "--template newuser/semilla" in readme
    # The stubs ran, so no real git or gh command touched anything.
    assert "init" in (tmp_path / "bin" / "git.log").read_text(encoding="utf-8")
    assert "repo create" in (tmp_path / "bin" / "gh.log").read_text(encoding="utf-8")


def test_substitution_warns_when_there_is_no_placeholder(tmp_path: Path):
    _write(tmp_path, {".github/CODEOWNERS": "/infra/                  @manoochehri\n"})

    result = _run(tmp_path)

    assert "no {{OWNER}} placeholder found" in result.stderr
    assert (tmp_path / ".github/CODEOWNERS").read_text(encoding="utf-8") == (
        "/infra/                  @manoochehri\n"
    )
