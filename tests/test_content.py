import pytest

from build import ContentError, validate_papers, validate_site, validate_courses


def _paper(**over):
    base = {
        "id": "a-paper",
        "title": "A Paper",
        "authors": ["Someone", "SELF"],
        "status": "working",
    }
    base.update(over)
    return base


def test_valid_paper_passes():
    assert validate_papers([_paper()])


def test_duplicate_id_is_rejected():
    with pytest.raises(ContentError, match="duplicate id 'a-paper'"):
        validate_papers([_paper(), _paper(title="Another")])


def test_missing_title_is_rejected():
    paper = _paper()
    del paper["title"]
    with pytest.raises(ContentError, match="missing required field 'title'"):
        validate_papers([paper])


def test_unknown_status_is_rejected():
    with pytest.raises(ContentError, match="unknown status 'draft'"):
        validate_papers([_paper(status="draft")])


def test_published_requires_venue_and_year():
    with pytest.raises(ContentError) as exc:
        validate_papers([_paper(status="published")])
    assert "requires 'venue'" in str(exc.value)
    assert "requires 'year'" in str(exc.value)


def test_published_with_venue_and_year_passes():
    assert validate_papers([_paper(status="published", venue="JFE", year=2026)])


def test_non_url_safe_id_is_rejected():
    with pytest.raises(ContentError, match="not URL-safe"):
        validate_papers([_paper(id="A Paper!")])


def test_authors_must_include_self():
    with pytest.raises(ContentError, match="must include the token"):
        validate_papers([_paper(authors=["Someone Else"])])


def test_all_errors_are_reported_together():
    paper = _paper(status="draft")
    del paper["title"]
    with pytest.raises(ContentError) as exc:
        validate_papers([paper])
    message = str(exc.value)
    assert "missing required field 'title'" in message
    assert "unknown status 'draft'" in message


def test_papers_must_be_a_list():
    with pytest.raises(ContentError, match="must contain a list"):
        validate_papers({"id": "nope"})


def test_site_requires_core_identity_fields():
    with pytest.raises(ContentError, match="missing required field 'email'"):
        validate_site({"name": "X", "title": "Y", "institution": "Z"})


def test_site_with_all_required_fields_passes():
    assert validate_site(
        {"name": "X", "title": "Y", "institution": "Z", "email": "a@b.c"}
    )


def test_empty_courses_list_is_valid():
    assert validate_courses([]) == []


def test_course_requires_id_and_title():
    with pytest.raises(ContentError, match="missing required field 'title'"):
        validate_courses([{"id": "a-course"}])


def test_duplicate_course_id_is_rejected():
    course = {"id": "a-course", "title": "A Course"}
    with pytest.raises(ContentError, match="duplicate id 'a-course'"):
        validate_courses([course, dict(course, title="Another")])
