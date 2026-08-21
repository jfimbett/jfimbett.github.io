import pytest

from build import build_context, format_authors, partition, render_site


def test_format_authors_bolds_self():
    result = format_authors(["Ada Lovelace", "SELF"], "Juan Felipe Imbet")
    assert "<strong>Juan Felipe Imbet</strong>" in result
    assert "Ada Lovelace" in result
    assert "SELF" not in result


def test_format_authors_escapes_html():
    result = format_authors(["<script>", "SELF"], "Juan Felipe Imbet")
    assert "<script>" not in result
    assert "&lt;script&gt;" in result


def test_partition_groups_by_status():
    papers = [
        {"id": "a", "status": "published"},
        {"id": "b", "status": "working"},
        {"id": "c", "status": "wip"},
        {"id": "d", "status": "published"},
    ]
    grouped = partition(papers)
    assert [p["id"] for p in grouped["published"]] == ["a", "d"]
    assert [p["id"] for p in grouped["working"]] == ["b"]
    assert [p["id"] for p in grouped["wip"]] == ["c"]


def test_context_reports_teaching_disabled_when_courses_empty():
    context = build_context()
    assert context["has_teaching"] is False


def test_render_writes_the_core_pages(tmp_path):
    written = render_site(out_dir=tmp_path)
    names = {path.name for path in written}
    assert {"index.html", "research.html"} <= names


def test_render_omits_teaching_when_courses_empty(tmp_path):
    written = render_site(out_dir=tmp_path)
    assert "teaching.html" not in {path.name for path in written}
    for path in written:
        if path.suffix == ".html":
            assert "teaching.html" not in path.read_text(encoding="utf-8")


def test_render_emits_teaching_when_a_course_exists(tmp_path, monkeypatch):
    import build

    real = build.load_yaml

    def fake(path):
        if path.name == "courses.yml":
            return [{"id": "llm-finance", "title": "LLMs in Finance"}]
        return real(path)

    monkeypatch.setattr(build, "load_yaml", fake)
    written = build.render_site(out_dir=tmp_path)
    assert "teaching.html" in {path.name for path in written}
    index = tmp_path / "index.html"
    assert "teaching.html" in index.read_text(encoding="utf-8")

    # The conditional page must meet the same heading contract as the
    # always-present pages: exactly one h1. Regression guard — teaching.html
    # is invisible to the parametrized h1 test because it only exists when
    # courses.yml is non-empty.
    teaching = (tmp_path / "teaching.html").read_text(encoding="utf-8")
    assert teaching.count("<h1") == 1, "teaching.html has {} h1 elements".format(
        teaching.count("<h1")
    )


def test_no_bootstrap_or_fontawesome_in_output(tmp_path):
    for path in render_site(out_dir=tmp_path):
        if path.suffix == ".html":
            text = path.read_text(encoding="utf-8").lower()
            assert "bootstrap" not in text
            assert "font-awesome" not in text


def test_edhec_is_the_current_affiliation(tmp_path):
    render_site(out_dir=tmp_path)
    index = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert "EDHEC Business School" in index
    assert "juan.imbet@edhec.edu" in index


def test_every_paper_appears_on_the_research_page(tmp_path):
    render_site(out_dir=tmp_path)
    research = (tmp_path / "research.html").read_text(encoding="utf-8")
    for paper in build_context()["papers"]:
        assert 'id="{}"'.format(paper["id"]) in research


def test_hostile_content_is_escaped_in_rendered_pages(tmp_path, monkeypatch):
    """Autoescape must cover ordinary fields, not just the hand-escaped authors.

    Regression: select_autoescape(["html"]) never fires for *.html.j2 names,
    which silently disabled escaping for the entire site.
    """
    import build

    real = build.load_yaml

    def fake(path):
        data = real(path)
        if path.name == "papers.yml":
            data[0] = dict(data[0], title="Bank <script>alert(1)</script> Runs")
        return data

    monkeypatch.setattr(build, "load_yaml", fake)
    build.render_site(out_dir=tmp_path)
    markup = (tmp_path / "research.html").read_text(encoding="utf-8")
    assert "<script>alert(1)</script>" not in markup
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in markup


@pytest.mark.parametrize("page", ["index.html", "research.html"])
def test_every_page_has_exactly_one_h1(tmp_path, page):
    render_site(out_dir=tmp_path)
    markup = (tmp_path / page).read_text(encoding="utf-8")
    assert markup.count("<h1") == 1, "{} has {} h1 elements".format(
        page, markup.count("<h1")
    )


def test_search_index_covers_every_paper(tmp_path):
    import json

    render_site(out_dir=tmp_path)
    payload = json.loads(
        (tmp_path / "assets" / "data" / "search.json").read_text(encoding="utf-8")
    )
    ids = {doc["id"] for doc in payload["docs"]}
    assert ids == {paper["id"] for paper in build_context()["papers"]}
    for doc in payload["docs"]:
        assert doc["text"].strip(), "{} has empty search text".format(doc["id"])


def _render_home_with_map(flag, tmp_path):
    """Render index.html with site.show_research_map forced to `flag`."""
    import build

    real_build_context = build.build_context

    def patched():
        context = real_build_context()
        context["site"] = dict(context["site"], show_research_map=flag)
        return context

    build.build_context = patched
    try:
        render_site(out_dir=tmp_path)
    finally:
        build.build_context = real_build_context
    return (tmp_path / "index.html").read_text(encoding="utf-8")


def test_research_map_is_omitted_when_the_flag_is_off(tmp_path):
    markup = _render_home_with_map(False, tmp_path)
    assert "plot-canvas" not in markup
    assert "hero.js" not in markup


def test_research_map_returns_when_the_flag_is_on(tmp_path):
    markup = _render_home_with_map(True, tmp_path)
    assert 'id="plot-canvas"' in markup
    assert "assets/js/hero.js" in markup
    assert "plot__legend" in markup


def test_the_nav_does_not_duplicate_the_cv_link(tmp_path):
    """The CV lives in the hero's link row; a second copy in the nav is noise."""
    import re

    render_site(out_dir=tmp_path)
    markup = (tmp_path / "index.html").read_text(encoding="utf-8")
    nav = re.search(r'<div class="site-nav__links">(.*?)</div>', markup, re.S).group(1)
    assert "cv.pdf" not in nav
