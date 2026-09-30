"""Guards for the `.trazo/` layout (issue #50).

The move in #50 is the kind of change that looks finished the moment the files are in
place, and is actually finished weeks later when some doc still points at a path that no
longer exists. `docs/CHARTER.md` was referenced from 29 tracked files; the failure mode is
not a broken build, it is a doc that quietly tells a future session to read a file that is
not there.

Two properties are asserted:

1. **No tracked file points at a path that does not exist.** The issue's own done-when.
   The exceptions are deliberate and listed, so a new exception has to be argued for.
2. **The moved trees are where the rules say they are, and the old paths are gone.**
   Otherwise a half-finished move leaves both copies, and the next agent reads whichever
   it finds first.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_TOKENS = ("NNNN", "TODO", "YYYY")

TEXT_SUFFIXES = {".md", ".py", ".toml", ".yml", ".yaml", ".json", ".sh", ".cfg", ".txt"}

# The paths that moved in #50, and where they went.
MOVED = (
    "docs/CHARTER.md",
    "docs/ARCHITECTURE.md",
    "docs/ADVISOR.md",
    "docs/decisions/",
    "docs/workstreams/",
)

# Deliberately still in docs/: operational and session state, not design records.
KEPT_IN_DOCS = ("docs/PLAN.md", "docs/STATUS.md", "docs/RUNBOOK.md", "docs/SKEPTIC_BAR.md")


def _tracked() -> list[Path]:
    """Every tracked path, without a subprocess.

    Walking the tree and filtering out `.git` and `.worktrees` is deliberate: shelling
    out to `git ls-files` is a subprocess (S603, a rule worth keeping) and this repo
    already carries a guard that every path reference resolves to a real file, so the
    test does not need an authoritative index -- it needs the set of files a reader could
    follow. That set *is* the working tree, minus the two directories that are not part
    of the project.
    """
    skip = {".git", ".worktrees", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
    found = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if skip & set(path.relative_to(REPO_ROOT).parts):
            continue
        found.append(path)
    return found


def _text_files() -> list[Path]:
    return [p for p in _tracked() if p.suffix in TEXT_SUFFIXES and p.is_file()]


def test_the_overlay_layout_exists() -> None:
    """The layout from #50, asserted rather than assumed."""
    for rel in (
        ".trazo/rules.md",
        ".trazo/charter/charter.md",
        ".trazo/ARCHITECTURE.md",
        ".trazo/ADVISOR.md",
        ".trazo/adr/0000-template.md",
        ".trazo/workstreams/_template.md",
    ):
        assert (REPO_ROOT / rel).exists(), f"{rel} is missing; the move is incomplete"


def test_no_file_points_at_a_path_that_does_not_exist() -> None:
    """The issue's done-when. A dangling path is a doc that lies to the next session."""
    dangling: list[str] = []
    pattern = re.compile(r"\.trazo/[A-Za-z0-9_./-]+")
    for path in _text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, ValueError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for raw in pattern.findall(line):
                ref = raw.rstrip(".,;:)`\"'")
                if not ref or any(t in ref for t in TEMPLATE_TOKENS):
                    continue
                # A bare directory or a shorthand like `.trazo/adr/0003` is prose.
                if not (REPO_ROOT / ref).exists() and "." not in Path(ref).name:
                    continue
                if not (REPO_ROOT / ref).exists():
                    dangling.append(f"{path.relative_to(REPO_ROOT)}:{lineno}: {ref}")

    assert not dangling, "paths that do not exist (issue #50 done-when):\n" + "\n".join(dangling)


def test_the_old_paths_are_gone() -> None:
    """A half-finished move leaves two copies and the next agent reads whichever it finds.

    Asserted as "no *files* remain" rather than "the directory does not exist": git does
    not track empty directories, so `git mv` leaves them behind in the working tree
    uncommitted and invisible to a fresh clone. A clone would never see the stale
    directory, but a session working in this tree would, and `ls docs/` showing
    `decisions/` that is not there is exactly the kind of thing that sends an agent
    looking for a file that moved.
    """
    for old in MOVED:
        root = REPO_ROOT / old
        stale = (
            [str(p.relative_to(REPO_ROOT)) for p in root.rglob("*") if p.is_file()]
            if (root.exists())
            else []
        )
        assert not stale, f"{old} still has files: {stale}"
        refs = [
            str(p.relative_to(REPO_ROOT))
            for p in _text_files()
            # This file names the old paths on purpose -- they are the assertion.
            if p.name != Path(__file__).name
            and old in p.read_text(encoding="utf-8", errors="ignore")
        ]
        assert not refs, f"{old} is still referenced by: {refs}"


def test_operational_state_stays_in_docs() -> None:
    """The judgement call from #50, asserted so a later session does not quietly move
    them: PLAN/STATUS/RUNBOOK are session and operational state for the host repo, and
    shipping the harness's own scratch space into every mounted repo is the opposite of a
    blank template."""
    for rel in KEPT_IN_DOCS:
        assert (REPO_ROOT / rel).exists(), f"{rel} moved; #50's plan keeps it in docs/"
    assert (REPO_ROOT / "docs" / "reports").is_dir(), "docs/reports/ should still exist"


def test_the_rules_file_is_the_tool_neutral_core() -> None:
    """The issue requires `.trazo/rules.md` to carry the mount-time contract, and
    requires that it does not mandate a tool for mounted repos."""
    rules = (REPO_ROOT / ".trazo" / "rules.md").read_text(encoding="utf-8")
    assert "one-command" in rules, "the mount-time environment contract is missing"
    assert re.search(r"hermetic", rules, re.IGNORECASE), "the contract must say hermetic"
    for tool in ("Docker", "nix", "devcontainer", "Makefile"):
        assert tool.lower() in rules.lower(), f"{tool} must be named as a valid option"
    assert re.search(r"do \*\*not\*\* mandate", rules, re.IGNORECASE), (
        "the contract must explicitly refuse to mandate a tool -- that is the mistake "
        "this pivot exists to fix"
    )


def test_claude_md_is_the_adapter_not_the_rules() -> None:
    """CLAUDE.md is a thin adapter; the rules live once, tool-neutral.

    The mechanical form of that -- the `@.trazo/rules.md` import, and the guards that keep
    it from silently failing open -- live in `test_adapter_import.py`.
    """
    claude = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    assert ".trazo/rules.md" in claude, "the adapter must point at the rules"
    assert "adapter" in claude.lower(), "CLAUDE.md must say what it now is"
    # The judgment layer must not be reduced to specs + ADRs (#0005).
    assert ".trazo/charter/" in claude, "the charter must stay visible from the adapter"
    assert ".trazo/specs/" in claude, "specs are part of the layout"
    assert ".trazo/adr/" in claude and ".trazo/workstreams/" in claude


def test_codeowners_still_protects_the_charter() -> None:
    """The charter is a judgment-layer path and was owner-protected under its old name.
    Moving the path without moving the rule would silently drop that protection -- the
    exact 'a path that matches no rule protects nothing' failure of issue #14."""
    codeowners = (REPO_ROOT / ".github" / "CODEOWNERS").read_text(encoding="utf-8")
    assert "docs/CHARTER.md" not in codeowners, "the old protected path is still listed"
    assert re.search(r"/\.trazo/charter/\s+@\S+", codeowners), (
        "the charter's new path is unprotected -- a moved path that matches no rule "
        "protects nothing (issue #14)"
    )


def test_the_docs_updated_ci_gate_followed_the_move() -> None:
    """ci.yml greps changed files for the architecture doc. ARCHITECTURE moved, so a
    stale pattern turns the gate into a no-op that still reports success."""
    ci = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert ".trazo/ARCHITECTURE.md" in ci, "the docs-updated gate does not watch the new path"
    assert "docs/RUNBOOK.md" in ci, "the gate lost the runbook"
    assert not re.search(r"\^docs/\(ARCHITECTURE", ci), "the stale pattern is still there"
