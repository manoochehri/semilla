"""Guards for the agent-to-agent handoff protocol (issues #35, #36).

The protocol is prose in `.claude/`, so nothing but a test stops it from being
edited back into "ask the owner in chat" — the failure mode #35 was opened for.
These checks assert the load-bearing pieces are still there, not the exact wording.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORK = REPO_ROOT / ".claude" / "commands" / "work.md"
PM_AGENT = REPO_ROOT / ".claude" / "agents" / "pm.md"
PM_ROLE = REPO_ROOT / ".claude" / "commands" / "pm.md"

# The scoped grant lives in exactly one file. Restating it is how the two PM surfaces
# drifted apart in the first place (see #36).
GRANT_FLAGS = (
    "--add-label",
    "--remove-label",
    "--parent",
    "--add-sub-issue",
    "--add-blocked-by",
    "--add-blocking",
    "--milestone",
    "--add-assignee",
    "gh label create",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_engineer_posts_blockers_to_the_issue() -> None:
    """The blocked path routes through GitHub, not chat."""
    work = _text(WORK)
    assert "gh issue comment" in work
    assert "--add-label needs-pm" in work
    assert re.search(r"`pm` subagent", work)


def test_engineer_has_the_does_it_block_progress_test() -> None:
    assert "progress stops" in _text(WORK)


def test_engineer_does_not_classify_owner_calls() -> None:
    """Under-labelling is silent, so this call belongs to the PM (#35)."""
    assert re.search(r"never classify", _text(WORK), re.IGNORECASE)


def test_pm_may_maintain_the_issue_graph() -> None:
    pm = _text(PM_AGENT)
    assert "gh issue edit" in pm
    for flag in ("--add-label", "--remove-label", "--parent", "--add-blocked-by", "--milestone"):
        assert flag in pm, flag
    assert "gh label create" in pm


def test_pm_may_not_rewrite_specs_or_close_issues() -> None:
    pm = _text(PM_AGENT)
    assert "--body" in pm
    assert "gh issue close" in pm


def test_pm_never_removes_the_owners_gate() -> None:
    """`needs-decision` is the owner's gate; escalation is one-way."""
    pm = _text(PM_AGENT)
    assert re.search(r"[Nn]ever remove \*{0,2}`needs-decision`", pm)
    assert "never the reverse" in pm


def test_pm_has_the_handoff_duties() -> None:
    pm = _text(PM_AGENT)
    assert re.search(r"Classify blockers", pm)
    assert re.search(r"never hand the owner text to paste", pm, re.IGNORECASE)
    assert "GitHub state" in pm


def test_pm_role_command_forbids_file_edits() -> None:
    """Load-bearing here: the role command runs in the main session, which has Edit/Write.

    The subagent's frontmatter grants no editing tools at all, so the same sentence is
    only belt-and-braces on that surface.
    """
    role = _text(PM_ROLE)
    assert re.search(r"do NOT edit code or config", role)
    assert "`Edit`" in role and "`Write`" in role


def test_pm_role_command_defers_rather_than_restating_the_grant() -> None:
    """Guarding only the subagent would have passed while the two files contradicted."""
    role = _text(PM_ROLE)
    assert ".claude/agents/pm.md" in role
    for flag in GRANT_FLAGS:
        assert flag not in role, f"{flag} belongs only in .claude/agents/pm.md"
