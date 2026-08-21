"""Every internal link and anchor must resolve."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
PAGES = ["index.html", "research.html"]

HREF = re.compile(r'href="([^"]+)"')
SRC = re.compile(r'src="([^"]+)"')
ANCHOR_ID = re.compile(r'id="([^"]+)"')


def _internal(reference):
    return not reference.startswith(
        ("http://", "https://", "mailto:", "#", "data:", "//")
    )


@pytest.mark.parametrize("page", PAGES)
def test_internal_links_resolve(page):
    markup = (ROOT / page).read_text(encoding="utf-8")
    missing = []
    for reference in HREF.findall(markup) + SRC.findall(markup):
        if not _internal(reference):
            continue
        target = reference.split("#")[0].split("?")[0]
        if not target:
            continue
        if not (ROOT / target).exists():
            missing.append(reference)
    assert not missing, "{}: broken -> {}".format(page, missing)


@pytest.mark.parametrize("page", PAGES)
def test_same_page_anchors_exist(page):
    markup = (ROOT / page).read_text(encoding="utf-8")
    ids = set(ANCHOR_ID.findall(markup))
    missing = [
        ref for ref in HREF.findall(markup)
        if ref.startswith("#") and ref != "#" and ref[1:] not in ids
    ]
    assert not missing, "{}: dangling anchors {}".format(page, missing)


def test_cross_page_anchors_exist():
    research_ids = set(
        ANCHOR_ID.findall((ROOT / "research.html").read_text(encoding="utf-8"))
    )
    for page in PAGES:
        markup = (ROOT / page).read_text(encoding="utf-8")
        for reference in HREF.findall(markup):
            if reference.startswith("research.html#"):
                anchor = reference.split("#", 1)[1]
                assert anchor in research_ids, "{} -> {}".format(page, reference)


def test_hero_json_anchors_resolve_on_the_research_page():
    """The scatter navigates by href; a stale id would send visitors nowhere."""
    import json

    hero = json.loads(
        (ROOT / "assets" / "data" / "hero.json").read_text(encoding="utf-8")
    )
    research_ids = set(
        ANCHOR_ID.findall((ROOT / "research.html").read_text(encoding="utf-8"))
    )
    for anchor in hero["anchors"]:
        target = anchor["href"].split("#", 1)[1]
        assert target in research_ids, anchor["href"]
