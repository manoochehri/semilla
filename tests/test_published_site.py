"""Guards the published docs site (issue #75).

The site kept describing a product that no longer existed, and nothing failed. The repo
was renamed to trazo (#52), the delivery model became a mountable overlay (#0005), the
flywheel commands were removed (#73), and the `/semilla` command was renamed (#72) — while
`handbook/`, which is `docs_dir`, went on publishing:

    <title>semilla</title>
    "A self-improving template for starting software projects"
    "Every project grows from it, and each one sends what it learned back"

None of that is checkable by a build. A rename PR can leave it behind, and the only thing
that caught it was curling the live page — the same out-of-band class as #52's workflow
gate and #61's squash merge.

So these assert the invariants that made the drift possible:

1. **The site's identity matches the repository.** `site_name` becomes the `<title>` on
   every page, and `site_description` the meta description.
2. **No published page claims a delivery model that was removed.** "Template" and the
   lesson-flywheel sentence are the two claims that went false, and a substitution cannot
   fix either — they have to be rewritten, which is what this issue did.
3. **The overlay is actually documented.** `.trazo/` is the product, and before this
   nothing on the site explained what it was or what contract a mounted repo must satisfy.
4. **The logo is not the old pun.** The mark was a seed/sprout, because the repo used to
   be called *semilla*.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MKDOCS = REPO_ROOT / "mkdocs.yml"
HANDBOOK = REPO_ROOT / "handbook"
LOGO = HANDBOOK / "assets" / "logo.svg"
FAVICON = HANDBOOK / "assets" / "favicon.svg"

# Every file `docs_dir` publishes. lessons.md and changelog.md are `--8<--` includes of
# .template/, so they follow automatically and are excluded here.
PUBLISHED = ("index.md", "guide.md", "playbook.md", "team.md", "overlay.md")

# Spelling here so the scan below does not match this file's own source.
OLD_NAME = "sem" + "illa"


def _text_files() -> list[Path]:
    return [HANDBOOK / name for name in PUBLISHED if (HANDBOOK / name).exists()]


def test_site_identity_matches_the_repository() -> None:
    """`site_name` becomes the `<title>` on every page. This is the drift itself."""
    mkdocs = MKDOCS.read_text(encoding="utf-8")
    name = re.search(r"^site_name:\s*(.+)$", mkdocs, re.MULTILINE)
    assert name, "no site_name in mkdocs.yml"
    assert name.group(1).strip() == "Trazo", (
        f"site_name is {name.group(1).strip()!r}; it is the <title> on every page"
    )
    desc = re.search(r"^site_description:\s*(.+)$", mkdocs, re.MULTILINE)
    assert desc, "no site_description"
    assert OLD_NAME not in desc.group(1), "site_description still names the old project"
    assert "overlay" in desc.group(1).lower(), (
        "the description must lead with the overlay; that is what the project is now"
    )


def test_no_published_page_names_the_old_project() -> None:
    offenders = []
    for path in _text_files():
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(rf"\b{OLD_NAME}\b", line, re.IGNORECASE):
                offenders.append(f"{path.name}:{lineno}: {line.strip()[:70]}")
    assert not offenders, "published pages still call the project the old name:\n" + "\n".join(
        offenders
    )


def test_no_page_claims_a_flywheel_that_was_removed() -> None:
    """`/template-improve` and `/template-sync` were deleted in #73. The sentence
    "each one sends what it learned back" advertised exactly that, and a find-and-replace
    would have left it in place."""
    for path in _text_files():
        text = path.read_text(encoding="utf-8").lower()
        assert "sends what it learned back" not in text, (
            f"{path.name} still promises an automatic lesson flywheel that no longer exists"
        )
        assert "template-improve" not in text
        assert "template-sync" not in text


def test_the_overlay_is_documented_and_reachable() -> None:
    """The gap that made the site wrong: `.trazo/` is the product and nothing explained
    it -- not the layout, and not the one contract a mounted repo must satisfy."""
    overlay = HANDBOOK / "overlay.md"
    assert overlay.exists(), "handbook/overlay.md is missing; the overlay is undocumented"
    text = overlay.read_text(encoding="utf-8")

    assert "mount-time contract" in text.lower(), "the contract is what makes mounting work"
    assert re.search(r"hermetic", text, re.IGNORECASE), "the contract must state hermetic"
    for path in ("rules.md", "charter/", "adr/", "workstreams/"):
        assert path in text, f"the layout omits {path}"
    assert "judgment" in text.lower(), "the judgment layer is the differentiator; say so"
    assert "stop rule" in text.lower()

    # Reachable: in the nav, and linked from the home page.
    mkdocs = MKDOCS.read_text(encoding="utf-8")
    assert "overlay.md" in mkdocs, "overlay.md is not in mkdocs nav, so it is unreachable"
    assert "overlay.md" in (HANDBOOK / "index.md").read_text(encoding="utf-8"), (
        "the home page must link it, or a reader never finds out the product exists"
    )


def test_the_home_page_leads_with_the_overlay_not_the_cloud() -> None:
    """AWS is still true and still supported, but it is a deploy choice for a Trazo-owned
    repo -- it stopped being the headline qualifier at the pivot, and leading with it
    describes the old product."""
    index = (HANDBOOK / "index.md").read_text(encoding="utf-8")
    assert "overlay" in index.lower(), "the home page does not say it is an overlay"
    # The tagline is the first bolded paragraph after the H1, not the whole page: AWS is
    # legitimately discussed further down in its own section.
    tagline = next((ln for ln in index.splitlines()[1:] if ln.strip().startswith("**")), "").lower()
    assert tagline, "no bolded tagline under the H1"
    assert "aws" not in tagline, (
        "AWS is in the tagline again; that is the pre-pivot pitch, where the cloud choice "
        "was the headline qualifier instead of the overlay"
    )
    assert "skeptic" in index.lower(), "the judgment layer is not mentioned on the home page"


def test_the_logo_is_not_the_old_pun() -> None:
    """It was a seed/sprout, because the repo used to be called *semilla*. A wordmark now
    spells the name, so the mark and the product cannot drift apart the way a pun can."""
    for path in (LOGO, FAVICON):
        assert path.exists(), f"{path.name} is missing"
    svg = LOGO.read_text(encoding="utf-8")
    assert "Trazo" in svg, "the wordmark does not spell the name"
    # The old mark was 64x64 with filled green paths. A wordmark is wide and stroked.
    viewbox = re.search(r'viewBox="([^"]+)"', svg)
    assert viewbox, "no viewBox"
    _, _, w, h = (float(v) for v in viewbox.group(1).split())
    assert w > h, f"viewBox is {w}x{h}; the old mark was square (64x64)"
    assert "currentColor" in svg, (
        "the wordmark must use currentColor so it works in light and dark; a hard-coded "
        "colour is invisible on one of them"
    )
