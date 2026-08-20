#!/usr/bin/env python3
"""Static site generator for jfimbett.github.io.

Reads YAML from content/, validates it, and renders Jinja2 templates to
HTML committed alongside the source. Run: python3 build.py
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"

SELF = "SELF"
VALID_STATUS = {"published", "working", "wip"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


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

        _check_required(paper, ("id", "title", "authors", "status"), where, errors)
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
