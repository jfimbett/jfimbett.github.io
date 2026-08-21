"""The archive must be reachable by URL but invisible to the site."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent

STUBS = [
    "teaching/index.html",
    "teaching/python-conda-course.html",
    "teaching/empirical_asset_pricing/index.html",
    "teaching/investment_funds_risks/index.html",
    "teaching/python_m1/index.html",
    "teaching/python_m2/index.html",
    "teaching/python_m2_203/index.html",
]

GENERATED = ["index.html", "research.html", "cv.html"]


def test_archive_directory_exists():
    for name in ("teaching", "courses", "talks"):
        assert (ROOT / "archive" / name).is_dir(), "archive/{} missing".format(name)


@pytest.mark.parametrize("stub", STUBS)
def test_stub_redirects_into_the_archive(stub):
    path = ROOT / stub
    assert path.exists(), "{} missing".format(stub)
    text = path.read_text(encoding="utf-8")
    assert "http-equiv=\"refresh\"" in text
    assert "/archive/" in text or "archive/" in text
    assert "noindex" in text


@pytest.mark.parametrize("stub", STUBS)
def test_stub_target_actually_exists(stub):
    text = (ROOT / stub).read_text(encoding="utf-8")
    match = re.search(r'url=([^"\'>\s]+)', text)
    assert match, "no refresh target in {}".format(stub)
    target = match.group(1).lstrip("/")
    assert (ROOT / target).exists(), "{} points at missing {}".format(stub, target)


@pytest.mark.parametrize("page", GENERATED)
def test_generated_pages_never_link_to_the_archive(page):
    text = (ROOT / page).read_text(encoding="utf-8")
    assert "archive/" not in text
    assert "/talks/" not in text
    assert "/courses/" not in text


def test_untouched_directories_survive():
    assert (ROOT / "wedding" / "index.html").exists()
    assert (ROOT / "blog").is_dir()
    assert (ROOT / "code.html").exists()


def test_archive_index_is_noindex():
    text = (ROOT / "archive" / "index.html").read_text(encoding="utf-8")
    assert "noindex" in text
