"""`make scan` must never report success after scanning nothing (issue #43).

Inside a git worktree `.git` is a *file* whose `gitdir:` points at
`<main>/.git/worktrees/<name>`, outside the working tree. The old target mounted
only the working tree, so the container's git resolved no repository, gitleaks
scanned 0 commits, printed "no leaks found" and exited 0 — a secrets gate that read
green while checking nothing, in the location worktrees made the default place to
work.

Two surfaces are pinned here, both without needing Docker (the real end-to-end run
is done by hand, since it needs the gitleaks image):

  - `scripts/scan.sh` mounts the shared git dir when it is run from a worktree;
  - `scripts/scan-preflight.sh`, which runs *inside* the container, exits non-zero
    and never reaches gitleaks when the git dir is unreachable or holds no commits.

`docker` and `gitleaks` are stubbed; `git` is real, so the worktree detection is
exercised for real.
"""

import os
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCAN = REPO_ROOT / "scripts" / "scan.sh"
PREFLIGHT = REPO_ROOT / "scripts" / "scan-preflight.sh"

GIT = shutil.which("git")
SH = shutil.which("sh")
BASH = shutil.which("bash")


def _env(**extra: str) -> dict[str, str]:
    """Isolate git from the host's config, hooks, and commit signing."""
    return {
        **os.environ,
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        **extra,
    }


def _git(cwd: Path, *args: str) -> str:
    assert GIT, "git is required"
    done = subprocess.run(  # noqa: S603 - our own argv, throwaway repos under tmp_path
        [GIT, *args], cwd=cwd, env=_env(), capture_output=True, text=True, check=True
    )
    return done.stdout.strip()


def _init_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q", "-b", "main")
    (path / "file.txt").write_text("hello\n", encoding="utf-8")
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", "initial")


def _worktree(main: Path, path: Path, branch: str = "wt") -> None:
    _git(main, "worktree", "add", "-q", "-b", branch, str(path))


def _stub(bindir: Path, tool: str, log: Path, exit_code: int) -> None:
    """A fake `docker`/`gitleaks` on PATH that logs its argv and exits `exit_code`."""
    bindir.mkdir(parents=True, exist_ok=True)
    stub = bindir / tool
    stub.write_text(
        f'#!/bin/sh\nprintf "%s\\n" "$@" >> "{log}"\nexit {exit_code}\n', encoding="utf-8"
    )
    stub.chmod(0o755)


def _run_scan(cwd: Path, bindir: Path) -> subprocess.CompletedProcess[str]:
    assert BASH, "bash is required to run scripts/scan.sh"
    return subprocess.run(  # noqa: S603 - our own argv, stubbed PATH, throwaway cwd
        [BASH, str(SCAN)],
        cwd=cwd,
        env=_env(PATH=f"{bindir}{os.pathsep}{os.environ['PATH']}"),
        capture_output=True,
        text=True,
        check=False,
    )


def _run_preflight(repo: Path, bindir: Path) -> subprocess.CompletedProcess[str]:
    assert SH, "sh is required"
    return subprocess.run(  # noqa: S603 - our own argv, stubbed PATH
        [SH, str(PREFLIGHT), str(repo)],
        cwd=repo,
        env=_env(PATH=f"{bindir}{os.pathsep}{os.environ['PATH']}"),
        capture_output=True,
        text=True,
        check=False,
    )


def test_scan_remounts_the_shared_git_dir_from_a_worktree(tmp_path: Path):
    main = tmp_path / "main"
    _init_repo(main)
    wt = tmp_path / "wt"
    _worktree(main, wt)

    bindir = tmp_path / "bin"
    log = bindir / "docker.log"
    _stub(bindir, "docker", log, 0)

    result = _run_scan(wt, bindir)

    assert result.returncode == 0
    argv = log.read_text(encoding="utf-8")
    root = _git(wt, "rev-parse", "--show-toplevel")
    common = _git(wt, "rev-parse", "--git-common-dir")
    # The working tree and, crucially, the shared git dir that `.git` points at.
    assert f"-v\n{root}:/repo" in argv
    assert f"-v\n{common}:{common}" in argv
    assert "/scan-preflight.sh" in argv


def test_scan_does_not_remount_in_the_main_worktree(tmp_path: Path):
    main = tmp_path / "main"
    _init_repo(main)

    bindir = tmp_path / "bin"
    log = bindir / "docker.log"
    _stub(bindir, "docker", log, 0)

    result = _run_scan(main, bindir)

    assert result.returncode == 0
    argv = log.read_text(encoding="utf-8")
    root = _git(main, "rev-parse", "--show-toplevel")
    assert f"-v\n{root}:/repo" in argv
    assert f"{main / '.git'}:{main / '.git'}" not in argv


def test_scan_fails_loudly_outside_a_git_repository(tmp_path: Path):
    cwd = tmp_path / "not-a-repo"
    cwd.mkdir()
    bindir = tmp_path / "bin"
    log = bindir / "docker.log"
    _stub(bindir, "docker", log, 0)

    result = _run_scan(cwd, bindir)

    assert result.returncode == 2
    assert "not inside a git repository" in result.stderr
    assert not log.exists(), "docker must not run when the repository cannot be resolved"


def test_preflight_fails_when_the_git_dir_is_unreachable(tmp_path: Path):
    """The exact container view during #43: a `.git` file whose gitdir is absent."""
    repo = tmp_path / "wt"
    repo.mkdir()
    (repo / ".git").write_text("gitdir: /nonexistent/semilla/.git/worktrees/wt\n", encoding="utf-8")
    bindir = tmp_path / "bin"
    log = bindir / "gitleaks.log"
    _stub(bindir, "gitleaks", log, 0)

    result = _run_preflight(repo, bindir)

    assert result.returncode == 2
    assert "cannot resolve a repository" in result.stderr
    assert not log.exists(), "gitleaks must not run when git cannot resolve the repository"


def test_preflight_fails_when_there_are_no_commits(tmp_path: Path):
    repo = tmp_path / "empty"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    bindir = tmp_path / "bin"
    log = bindir / "gitleaks.log"
    _stub(bindir, "gitleaks", log, 0)

    result = _run_preflight(repo, bindir)

    assert result.returncode == 2
    assert "no commits to scan" in result.stderr
    assert not log.exists()


def test_preflight_scans_history_from_a_worktree(tmp_path: Path):
    main = tmp_path / "main"
    _init_repo(main)
    wt = tmp_path / "wt"
    _worktree(main, wt)
    bindir = tmp_path / "bin"
    log = bindir / "gitleaks.log"
    _stub(bindir, "gitleaks", log, 0)

    result = _run_preflight(wt, bindir)

    assert result.returncode == 0
    argv = log.read_text(encoding="utf-8")
    assert f"git\n{_git(wt, 'rev-parse', '--show-toplevel')}" in argv


def test_preflight_propagates_a_gitleaks_finding(tmp_path: Path):
    main = tmp_path / "main"
    _init_repo(main)
    bindir = tmp_path / "bin"
    log = bindir / "gitleaks.log"
    _stub(bindir, "gitleaks", log, 1)

    result = _run_preflight(main, bindir)

    assert result.returncode == 1
