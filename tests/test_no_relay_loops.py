"""Guards against routing work and decisions through the owner (issue #57).

Both reported failures are loops, not one bug: the PM handed the owner a message to
carry to the engineer, and decisions taken in chat never reached the issue. #36/#47
already forbade the engineer answering in chat, so a presence test over the whole
corpus would have stayed green while both loops kept running.

These assert the *operative* bullet in each file, not the word "ping" appearing
somewhere: a prohibition and an instruction mentioning the same phrase are opposites,
and only the right one satisfies the behaviour.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PM_AGENT = REPO_ROOT / ".claude" / "agents" / "pm.md"
ADVISOR = REPO_ROOT / "docs" / "ADVISOR.md"
WORK = REPO_ROOT / ".claude" / "commands" / "work.md"
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _bullet(text: str, marker: str) -> str:
    """The one line of `text` carrying `marker`, so the phrase cannot be satisfied
    from the wrong bullet -- a mention in an example is not a prohibition."""
    lines = [ln for ln in text.splitlines() if marker in ln]
    assert len(lines) == 1, f"expected exactly one {marker!r} bullet, found {len(lines)}"
    return lines[0]


def test_pm_may_not_route_work_through_the_owner() -> None:
    """The #57 loop: PM asks the owner to ping the engineer. The owner is a decision
    gate, not a message bus."""
    bullet = _bullet(_text(PM_AGENT), "Never route work through the owner")
    for phrase in ("ask eng", "tell eng", "ping eng"):
        assert phrase in bullet, f"{phrase!r} is the reported phrasing and must be named"
    assert "decision gate" in bullet, "the rule must say what the owner IS for"
    assert "/work" in bullet, "the rule must route work to a routine, not to a person"


def test_pm_routes_work_by_naming_the_next_item() -> None:
    """A prohibition alone still leaves the PM with nothing to do but ask. It must
    have a positive instruction: name the next item, addressed to the session."""
    bullet = _bullet(_text(PM_AGENT), "Never route work through the owner")
    assert "single next item" in bullet
    assert "priority" in bullet, "the next item is named with its priority, not bare"


def test_pm_ranks_every_open_issue_and_says_why() -> None:
    """ "Every single task needs to be rigorously prioritized" -- so the ranking is
    mandatory, exactly one priority each, and must be defensible."""
    bullet = _bullet(_text(PM_AGENT), "Rank every open issue")
    for label in ("P0", "P1", "P2"):
        assert label in bullet, f"{label} missing: a task with no label cannot be ranked"
    assert "unlabeled" in bullet, "unlabeled issues are the defect; they must be fixed on triage"
    assert "unblocks" in bullet and "cost" in bullet, "the ranking must state its basis"
    assert "never as prose" in bullet, "ranking is GitHub state, not a report paragraph"


def test_pm_keeps_dependencies_as_github_state() -> None:
    """The pre-existing rule this PR rebuilt: dependencies, like priority, are labels."""
    bullet = _bullet(_text(PM_AGENT), "Rank every open issue")
    # "milestone" not "--milestone": the bullet names the dependency graph, and a test
    # demanding a specific spelling would just get edited to match the typo.
    for flag in ("--parent", "--add-blocked-by", "milestone"):
        assert flag in bullet, f"{flag} belongs to the ranking rule"
    assert "Re-rank on triage" in bullet, "re-ranking is event-driven, not continuous"


def test_advisor_role_doc_carries_the_same_two_rules() -> None:
    """ADVISOR.md is what a fresh PM session reads first. If only the agent file has
    the rule, the loop survives for anyone who starts from the role doc (issue #36's
    exact drift, in a new place)."""
    never = _text(ADVISOR).split("## Never", 1)[1]
    assert re.search(r'no "ask eng", "tell eng", "ping eng"', never), (
        "the role doc must name the reported phrasing"
    )
    assert re.search(r"[Ll]eave an open issue unranked", never), (
        "the role doc must require a ranking"
    )


def test_decisions_are_recorded_on_the_issue_before_being_acted_on() -> None:
    """The #57 loop: eng pastes a PM decision in chat and the issue stays empty, so
    the next session re-asks a settled question."""
    section = _text(WORK).split("## When a decision arrives", 1)[1]
    assert "gh issue comment" in section, "the decision is written to the issue"
    assert "before" in section.lower(), "recorded *before* acting on it, not after"
    assert "never the record" in section, "the chat line is a pointer, not the record"
    for route in ("pm` subagent", "chat", "/decide"):
        assert route in section, f"a decision arriving via {route} must be covered too"


def test_the_answered_blocker_path_records_the_answer() -> None:
    """Step 4 of the handoff protocol is where a PM's answer lands. If it says only
    'continue from that answer', the answer stays in the session."""
    step = _bullet(_text(WORK), "**If it answers,**")
    assert "gh issue comment" in step, "the answer must be commented onto the issue"
    # Positional, not a magic word: the record has to precede acting on the answer,
    # whichever way the file phrases "first"/"before".
    assert step.index("gh issue comment") < step.index("continue from"), (
        "the answer must be recorded before work continues from it"
    )


def test_claude_md_states_the_decision_goes_on_the_issue() -> None:
    """Rule 7 is the standing rule every session reads, whichever routine it runs."""
    rule = _bullet(_text(CLAUDE_MD), "Leave state in the repo")
    assert "issue" in rule, "a decision must be recorded on the issue it came from"


def test_claude_md_lists_the_labels_the_protocol_depends_on() -> None:
    """`/start` sorts by P0/P1/P2 and both queues run on needs-pm/needs-decision.
    A session that only reads CLAUDE.md cannot rank or route without these."""
    table = _text(CLAUDE_MD).split("## Where things live", 1)[1].split("## The team", 1)[0]
    for label in ("needs-decision", "needs-pm", "P0", "P1", "P2", "epic"):
        assert label in table, f"CLAUDE.md does not list the {label} label"
