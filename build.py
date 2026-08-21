#!/usr/bin/env python3
"""Static site generator for jfimbett.github.io.

Reads YAML from content/, validates it, and renders Jinja2 templates to
HTML committed alongside the source. Run: python3 build.py
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"

SELF = "SELF"
VALID_STATUS = {"published", "working", "wip"}
# Research agendas, in legend order. The slug colours a paper's point in the
# hero scatter (assets/js/hero.js reads a --plot-<slug> custom property), and
# the label names it in the legend rendered by templates/index.html.j2.
AGENDAS = (
    ("social-media", "Social media and markets"),
    ("corporate-finance", "Corporate finance"),
    ("asset-pricing", "Asset pricing"),
    ("computational-finance", "Computational finance"),
)
VALID_AGENDA = {slug for slug, _ in AGENDAS}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATA_DIR = "assets/data"


class ContentError(Exception):
    """Raised when content files fail validation.

    Carries every problem found, not just the first, so one build run
    surfaces all of them.
    """


def load_yaml(path):
    """Parse a YAML file, raising ContentError if it is missing or malformed."""
    if not path.exists():
        raise ContentError("{} does not exist".format(path))
    try:
        with path.open(encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        raise ContentError("{} is not valid YAML: {}".format(path, exc))


def _check_required(entry, fields, where, errors):
    for field in fields:
        if not entry.get(field):
            errors.append("{}: missing required field '{}'".format(where, field))


def _check_id(entry, seen, index, where, errors):
    identifier = entry.get("id")
    if not identifier:
        return
    if not ID_RE.match(str(identifier)):
        errors.append(
            "{}: id '{}' is not URL-safe (use lowercase-with-hyphens)".format(
                where, identifier
            )
        )
    if identifier in seen:
        errors.append(
            "{}: duplicate id '{}', first seen at index {}".format(
                where, identifier, seen[identifier]
            )
        )
    else:
        seen[identifier] = index


def validate_papers(papers):
    """Validate papers.yml. Returns the list, or raises ContentError."""
    if not isinstance(papers, list):
        raise ContentError("papers.yml must contain a list")

    errors = []
    seen = {}
    for index, paper in enumerate(papers):
        if not isinstance(paper, dict):
            errors.append("papers[{}]: expected a mapping".format(index))
            continue

        label = paper.get("id") or paper.get("title") or "<untitled>"
        where = "papers[{}] ({})".format(index, label)

        _check_required(
            paper,
            ("id", "title", "authors", "status", "agenda", "short"),
            where,
            errors,
        )
        _check_id(paper, seen, index, where, errors)

        status = paper.get("status")
        if status and status not in VALID_STATUS:
            errors.append(
                "{}: unknown status '{}' (expected one of {})".format(
                    where, status, sorted(VALID_STATUS)
                )
            )
        if status == "published":
            for field in ("venue", "year"):
                if not paper.get(field):
                    errors.append(
                        "{}: published papers requires '{}'".format(where, field)
                    )

        agenda = paper.get("agenda")
        if agenda and agenda not in VALID_AGENDA:
            errors.append(
                "{}: unknown agenda '{}' (expected one of {})".format(
                    where, agenda, sorted(VALID_AGENDA)
                )
            )

        authors = paper.get("authors")
        if isinstance(authors, list) and SELF not in authors:
            errors.append(
                "{}: authors must include the token '{}'".format(where, SELF)
            )

    if errors:
        raise ContentError("\n".join(errors))
    return papers


def validate_site(site):
    """Validate site.yml. Returns the mapping, or raises ContentError."""
    if not isinstance(site, dict):
        raise ContentError("site.yml must contain a mapping")
    errors = []
    _check_required(
        site, ("name", "title", "institution", "email"), "site.yml", errors
    )
    if errors:
        raise ContentError("\n".join(errors))
    return site


def validate_courses(courses):
    """Validate courses.yml. An empty list is valid and suppresses the page."""
    if courses is None:
        return []
    if not isinstance(courses, list):
        raise ContentError("courses.yml must contain a list")

    errors = []
    seen = {}
    for index, course in enumerate(courses):
        if not isinstance(course, dict):
            errors.append("courses[{}]: expected a mapping".format(index))
            continue
        label = course.get("id") or course.get("title") or "<untitled>"
        where = "courses[{}] ({})".format(index, label)
        _check_required(course, ("id", "title"), where, errors)
        _check_id(course, seen, index, where, errors)

    if errors:
        raise ContentError("\n".join(errors))
    return courses


TEMPLATES = ROOT / "templates"

PAGES = [
    ("index.html.j2", "index.html", "home"),
    ("research.html.j2", "research.html", "research"),
]
TEACHING_PAGE = ("teaching.html.j2", "teaching.html", "teaching")


def format_authors(authors, self_name):
    """Render an author list as HTML, bolding the SELF token.

    Everything is escaped: author names come from YAML and are interpolated
    into a template marked safe.
    """
    parts = []
    for author in authors:
        if author == SELF:
            parts.append("<strong>{}</strong>".format(html.escape(self_name)))
        else:
            parts.append(html.escape(str(author)))
    return ", ".join(parts)


def partition(papers):
    """Group papers by status, preserving file order within each group."""
    grouped = {"published": [], "working": [], "wip": []}
    for paper in papers:
        grouped[paper["status"]].append(paper)
    return grouped


def _search_text(paper):
    """Everything a keyword query might reasonably match."""
    parts = [
        paper.get("title", ""),
        " ".join(str(a) for a in paper.get("authors", []) if a != SELF),
        paper.get("venue", "") or "",
        " ".join(paper.get("topics", []) or []),
        paper.get("summary", "") or "",
        paper.get("abstract", "") or "",
    ]
    return " ".join(part.strip() for part in parts if part).strip()


def write_search_index(context, out_dir):
    """Write the BM25 corpus consumed by assets/js/search.js."""
    site = context["site"]
    docs = []
    for paper in context["papers"]:
        docs.append({
            "id": paper["id"],
            "title": paper["title"],
            "authors": format_authors(paper["authors"], site["name"]),
            "venue": paper.get("venue") or paper["status"],
            "status": paper["status"],
            "topics": paper.get("topics", []) or [],
            "agenda": paper["agenda"],
            "short": paper["short"],
            "summary": (paper.get("summary") or "").strip(),
            "text": _search_text(paper),
        })

    directory = Path(out_dir) / DATA_DIR
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "search.json"
    path.write_text(
        json.dumps({"docs": docs}, ensure_ascii=False, indent=1, sort_keys=True),
        encoding="utf-8",
    )
    return path


def build_context():
    """Load and validate every content file into one render context."""
    site = validate_site(load_yaml(CONTENT / "site.yml"))
    papers = validate_papers(load_yaml(CONTENT / "papers.yml"))
    courses = validate_courses(load_yaml(CONTENT / "courses.yml"))

    for paper in papers:
        paper["authors_html"] = format_authors(paper["authors"], site["name"])

    return {
        "site": site,
        "papers": papers,
        "grouped": partition(papers),
        "courses": courses,
        "has_teaching": bool(courses),
        "agendas": [{"id": slug, "label": label} for slug, label in AGENDAS],
        "year": 2026,
    }


def _environment():
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    return env


def render_site(out_dir=None):
    """Render every page. Returns the list of paths written.

    Nothing is written until every template has rendered successfully, so a
    failure cannot leave a half-generated site on disk.
    """
    out_dir = Path(out_dir) if out_dir else ROOT
    context = build_context()
    env = _environment()

    pages = list(PAGES)
    if context["has_teaching"]:
        pages.append(TEACHING_PAGE)

    rendered = {}
    for template_name, output_name, page_id in pages:
        template = env.get_template(template_name)
        rendered[output_name] = template.render(page=page_id, **context)

    written = []
    out_dir.mkdir(parents=True, exist_ok=True)
    for output_name, markup in rendered.items():
        path = out_dir / output_name
        path.write_text(markup, encoding="utf-8")
        written.append(path)

    stale = out_dir / "teaching.html"
    if not context["has_teaching"] and stale.exists():
        stale.unlink()

    written.append(write_search_index(context, out_dir))
    return written


def warn_if_embeddings_are_stale():
    """Warn, but never fail, when papers.yml is newer than embeddings.json."""
    papers = CONTENT / "papers.yml"
    embeddings = ROOT / DATA_DIR / "embeddings.json"
    if not embeddings.exists():
        sys.stderr.write(
            "warning: assets/data/embeddings.json is missing; "
            "run `cd tools && npm run embed`\n"
        )
        return
    if papers.stat().st_mtime > embeddings.stat().st_mtime:
        sys.stderr.write(
            "warning: papers.yml is newer than embeddings.json; "
            "run `cd tools && npm run embed` to refresh search and the hero\n"
        )


def main():
    try:
        written = render_site()
    except ContentError as exc:
        sys.stderr.write("Content validation failed:\n{}\n".format(exc))
        return 1
    for path in written:
        print("wrote {}".format(path.relative_to(ROOT)))
    warn_if_embeddings_are_stale()
    return 0


if __name__ == "__main__":
    sys.exit(main())
