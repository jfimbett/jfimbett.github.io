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
    assert {"index.html", "research.html", "cv.html"} <= names


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
