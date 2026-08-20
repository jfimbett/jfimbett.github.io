"""Guards on the actual content, not just the schema."""

import pytest

from build import (
    CONTENT,
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
