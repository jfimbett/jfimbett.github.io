"""Guards on the actual content, not just the schema."""

import json

import pytest

from build import (
    AGENDAS,
    CONTENT,
    DATA_DIR,
    ROOT,
    VALID_AGENDA,
    load_yaml,
    validate_courses,
    validate_papers,
    validate_site,
)


@pytest.fixture(scope="module")
def papers():
    return validate_papers(load_yaml(CONTENT / "papers.yml"))


def test_site_is_valid():
    site = validate_site(load_yaml(CONTENT / "site.yml"))
    assert site["institution"] == "EDHEC Business School"
    assert site["email"] == "juan.imbet@edhec.edu"


def test_there_are_nine_papers(papers):
    assert len(papers) == 9


def test_status_counts_match_the_spec(papers):
    counts = {}
    for paper in papers:
        counts[paper["status"]] = counts.get(paper["status"], 0) + 1
    assert counts == {"published": 3, "working": 4, "wip": 2}


def test_published_papers_all_have_a_link(papers):
    for paper in papers:
        if paper["status"] == "published":
            assert paper.get("doi") or paper.get("ssrn"), paper["id"]


def test_every_paper_with_an_abstract_has_a_summary(papers):
    for paper in papers:
        if paper.get("abstract"):
            assert paper.get("summary"), "{} needs a summary".format(paper["id"])


def test_no_dauphine_email_remains(papers):
    site = load_yaml(CONTENT / "site.yml")
    assert "dauphine" not in site["email"].lower()


def test_courses_is_empty_for_now():
    assert validate_courses(load_yaml(CONTENT / "courses.yml")) == []


# --- Research map ---------------------------------------------------------
# The hero scatter needs three things to line up: a valid agenda on every
# paper, a colour token for every agenda, and a hero.json that still describes
# the papers currently in papers.yml.


@pytest.fixture(scope="module")
def hero():
    return json.loads((ROOT / DATA_DIR / "hero.json").read_text(encoding="utf-8"))


def test_every_paper_has_a_known_agenda(papers):
    for paper in papers:
        assert paper["agenda"] in VALID_AGENDA, paper["id"]


def test_every_agenda_is_used_by_at_least_one_paper(papers):
    used = {paper["agenda"] for paper in papers}
    assert used == VALID_AGENDA


def test_short_labels_stay_short_enough_to_plot(papers):
    for paper in papers:
        assert len(paper["short"]) <= 26, paper["id"]


def test_every_agenda_has_a_plot_colour_token():
    css = (ROOT / "assets" / "css" / "site.css").read_text(encoding="utf-8")
    for slug, _ in AGENDAS:
        assert "--plot-{}:".format(slug) in css, slug


def test_hero_json_matches_the_papers(papers, hero):
    anchors = {anchor["id"]: anchor for anchor in hero["anchors"]}
    assert set(anchors) == {paper["id"] for paper in papers}
    for paper in papers:
        anchor = anchors[paper["id"]]
        assert anchor["agenda"] == paper["agenda"]
        assert anchor["label"] == paper["short"]
        assert anchor["title"] == paper["title"]
        assert -1 <= anchor["x"] <= 1 and -1 <= anchor["y"] <= 1
