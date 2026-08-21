"""Guards on the machine-readable layer: JSON-LD, canonicals, and the sitemap."""

import json
import re

import pytest

from build import build_context, render_site


@pytest.fixture(scope="module")
def rendered(tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    render_site(out_dir=out)
    return out


def _json_ld(markup):
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', markup, re.S
    )
    return [json.loads(block) for block in blocks]


def test_home_declares_a_person(rendered):
    blocks = _json_ld((rendered / "index.html").read_text(encoding="utf-8"))
    person = [b for b in blocks if b.get("@type") == "Person"]
    assert person, "no Person JSON-LD on the home page"
    assert person[0]["affiliation"]["name"] == "EDHEC Business School"
    assert person[0]["sameAs"], "profiles must be listed in sameAs"


def test_research_declares_every_published_paper(rendered):
    blocks = _json_ld((rendered / "research.html").read_text(encoding="utf-8"))
    graph = next(b["@graph"] for b in blocks if "@graph" in b)
    articles = [n for n in graph if n.get("@type") == "ScholarlyArticle"]
    published = build_context()["grouped"]["published"]
    assert len(articles) == len(published)
    for article in articles:
        assert article["name"]
        assert article["author"]
        assert article["datePublished"]


def test_scholarly_article_resolves_the_self_token(rendered):
    blocks = _json_ld((rendered / "research.html").read_text(encoding="utf-8"))
    graph = next(b["@graph"] for b in blocks if "@graph" in b)
    names = {author["name"] for node in graph for author in node["author"]}
    assert "SELF" not in names
    assert "Juan Felipe Imbet" in names


def test_every_page_has_a_canonical_and_description(rendered):
    for name in ("index.html", "research.html"):
        markup = (rendered / name).read_text(encoding="utf-8")
        assert 'rel="canonical"' in markup
        assert 'name="description"' in markup


def test_canonicals_are_page_specific(rendered):
    canonicals = {}
    for name in ("index.html", "research.html"):
        markup = (rendered / name).read_text(encoding="utf-8")
        canonicals[name] = re.search(
            r'<link rel="canonical" href="([^"]+)"', markup
        ).group(1)
    assert len(set(canonicals.values())) == 2, canonicals
    assert canonicals["research.html"].endswith("/research.html")
    assert canonicals["index.html"] == "https://jfimbett.github.io/"


def test_sitemap_lists_pages_and_excludes_the_archive(rendered):
    sitemap = (rendered / "sitemap.xml").read_text(encoding="utf-8")
    # The CV is a PDF, not a page: 7f47a15 dropped cv.html.
    for name in ("research.html", "cv.pdf"):
        assert name in sitemap
    assert "archive" not in sitemap
    assert "wedding" not in sitemap


def test_sitemap_omits_the_teaching_page_while_there_are_no_courses(rendered):
    sitemap = (rendered / "sitemap.xml").read_text(encoding="utf-8")
    assert build_context()["has_teaching"] is False
    assert "teaching.html" not in sitemap


def test_robots_points_at_the_sitemap():
    from build import ROOT

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    assert "Sitemap: https://jfimbett.github.io/sitemap.xml" in robots
    assert "Disallow: /archive/" in robots


def test_no_dead_assets_referenced(rendered):
    for name in ("index.html", "research.html"):
        markup = (rendered / name).read_text(encoding="utf-8")
        assert "custom.css" not in markup
        assert "js/main.js" not in markup
