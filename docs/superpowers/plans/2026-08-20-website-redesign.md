# Website Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Bootstrap academic site with an EDHEC-branded static site generated from YAML, featuring an embedding-space generative hero and progressive-enhancement semantic search.

**Architecture:** Content lives in three YAML files. `build.py` validates them and renders Jinja2 templates to HTML committed alongside the source, so GitHub Pages serves files directly and a broken build cannot take the site down. A separate Node tool precomputes paper embeddings, feeding both the hero canvas and the search re-ranker. All client JavaScript is vanilla ES modules with no framework.

**Tech Stack:** Python 3.9 + Jinja2 + PyYAML (build), pytest (Python tests), Node 22 built-in test runner (JS tests), transformers.js (embeddings, build-time and client-side), vanilla CSS and Canvas 2D.

**Spec:** `docs/superpowers/specs/2026-08-20-website-redesign-design.md`

## Global Constraints

- **Python floor is 3.9.** The machine has only Python 3.9.19; `pyproject.toml` currently declares `^3.11` and must be lowered. No `match` statements, no `X | Y` runtime annotations, no `dict[str, int]` builtin generics without `from __future__ import annotations`.
- **Build dependencies are Jinja2 and PyYAML only.** Nothing else may be imported by `build.py`.
- **Generated HTML is committed.** Never add generated pages to `.gitignore`.
- **No CDN on the critical path.** Google Fonts is the only permitted external stylesheet. Bootstrap and Font Awesome must be gone.
- **Brand tokens, exact values:** grenat `#5F1937`, ink `#0E0E0E`, paper `#FFFFFF`, grenat-pastel `#ECE4E7`, coral `#FF6E6E`, bleu `#00B9FF`, border `#DCDCDC`, muted `#5A5A5A`. Dark theme: grenat lifts to `#D4849F`, paper `#0E0E0E`, ink `#F2ECEE`.
- **Interactive colour variants (accessibility correction to spec §4.2).** EDHEC's coral `#FF6E6E` is only 2.72:1 on white and its bleu `#00B9FF` only 2.24:1 — both fail AA for text and fail the 3:1 minimum for focus indicators. Coral and bleu are therefore **decorative fills only**. Interactive states use `--coral-ink: #A63446` (6.56:1 on white, 5.25:1 on pastel) and `--bleu-ink: #007FB0` (4.50:1). Under the dark theme both revert to the bright originals, which pass there (7.09:1 and 8.63:1). Never use raw `--coral` or `--bleu` for text, focus rings, or any boundary that identifies a control.
- **Fonts:** Montserrat 600/700 (display/UI), Open Sans 400/600 (body).
- **Identity, exact values:** name `Juan Felipe Imbet`, title `Assistant Professor of Finance`, institution `EDHEC Business School`, email `juan.imbet@edhec.edu`. Dauphine is historical only. No office address.
- **Nine papers:** 3 published, 4 working, 2 work-in-progress.
- **The `SELF` token** in an `authors` list renders as the site owner's name in bold.
- **WCAG AA** for every foreground/background pair; zero axe-core violations.
- **Never touch** `wedding/`, `blog/`, `code.html`, `scripts/`.

## Deviation from the spec, requiring sign-off

Spec section 7.3 specifies `embed.py` using Python `sentence-transformers`. **This plan uses `tools/embed.mjs` (Node + transformers.js) instead.**

Rationale: `sentence-transformers` pulls PyTorch, roughly 2GB, onto the author's machine for a script that runs a few times a year. More importantly, the spec itself flags "query and document vectors must share an embedding space" as a silent-failure risk. Running the *same* transformers.js library and the *same* ONNX model at build time and in the browser eliminates that risk structurally rather than by convention. Node 22 is already installed.

Cost: `tools/` gets its own `package.json` and a gitignored `node_modules/`. The author runs `npm install` once, inside `tools/`, and never again. `build.py` remains pure Jinja2 + PyYAML.

## File Structure

| Path | Responsibility |
|---|---|
| `build.py` | Load, validate, render. The only script the author runs routinely. |
| `tests/test_content.py` | Validation rules for the content model. |
| `tests/test_render.py` | Rendering and conditional-page behaviour. |
| `content/site.yml` | Identity, contact, profile links, bio. |
| `content/papers.yml` | All nine papers. |
| `content/courses.yml` | Empty list; gates the Teaching page. |
| `templates/base.html.j2` | Document shell, nav, footer, meta, JSON-LD. |
| `templates/index.html.j2` | Hero, bio, selected work, contact. |
| `templates/research.html.j2` | Publications, working papers, work in progress. |
| `templates/cv.html.j2` | Readable CV plus PDF link. |
| `templates/teaching.html.j2` | Courses; rendered only when `courses.yml` is non-empty. |
| `templates/partials/paper.html.j2` | One paper entry, shared by index and research. |
| `templates/partials/icons.html.j2` | Inline SVG icon definitions. |
| `assets/css/site.css` | The entire design system. No other stylesheet. |
| `assets/js/bm25.js` | Pure ranking logic, no DOM. Node-testable. |
| `assets/js/search.js` | Search UI, keyboard handling, tier upgrade. |
| `assets/js/hero.js` | Canvas particle field. |
| `assets/js/semantic.js` | Tier 2 model loading and cosine re-ranking. |
| `tools/embed.mjs` | Precomputes embeddings and PCA coordinates. |
| `tools/pca.mjs` | Pure PCA, Node-testable. |
| `tools/test/*.test.mjs` | Node tests for `bm25.js` and `pca.mjs`. |
| `assets/data/search.json` | Generated. BM25 corpus. |
| `assets/data/embeddings.json` | Generated. Document vectors. |
| `assets/data/hero.json` | Generated. 2-D anchor coordinates. |
| `archive/` | Moved legacy material. Unlinked, noindex. |

---

### Task 1: Content model and validation

**Files:**
- Create: `build.py`
- Create: `tests/test_content.py`
- Modify: `pyproject.toml`
- Create: `pytest.ini`

**Interfaces:**
- Consumes: nothing.
- Produces: `ContentError(Exception)`; `load_yaml(path: Path) -> Any`; `validate_papers(papers: list) -> list`; `validate_site(site: dict) -> dict`; `validate_courses(courses: list) -> list`. Module constants `VALID_STATUS: set`, `SELF: str = "SELF"`, `ROOT: Path`, `CONTENT: Path`.

- [ ] **Step 1: Lower the Python floor and add build dependencies**

The machine has only Python 3.9.19. Edit `pyproject.toml`, changing the dependencies block to:

```toml
[tool.poetry.dependencies]
python = "^3.9"
Jinja2 = "^3.1"
PyYAML = "^6.0"

[tool.poetry.group.dev.dependencies]
python-semantic-release = "^9.8.7"
pytest = "^7.4"
```

- [ ] **Step 2: Configure pytest**

Create `pytest.ini` so `build.py` at the repository root is importable from tests:

```ini
[pytest]
testpaths = tests
pythonpath = .
```

- [ ] **Step 3: Write the failing tests**

Create `tests/test_content.py`:

```python
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
```

- [ ] **Step 4: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_content.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'build'`

- [ ] **Step 5: Implement the validators**

Create `build.py`:

```python
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
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_content.py -v`
Expected: PASS, 15 passed

- [ ] **Step 7: Commit**

```bash
git add build.py tests/test_content.py pyproject.toml pytest.ini
git commit -m "feat: add content model validation for the site build"
```

---

### Task 2: Author the content

**Files:**
- Create: `content/site.yml`
- Create: `content/papers.yml`
- Create: `content/courses.yml`
- Create: `tests/test_real_content.py`

**Interfaces:**
- Consumes: `validate_papers`, `validate_site`, `validate_courses`, `load_yaml`, `CONTENT` from Task 1.
- Produces: the three YAML files, and the guarantee that real content passes validation.

All paper text is transcribed from the existing `index.html` and `cv.tex`. Do not paraphrase abstracts — copy them verbatim. The `summary` field is new writing: one short paragraph per paper, plain language, aimed at a journalist, no jargon, no equations.

- [ ] **Step 1: Write the failing test**

Create `tests/test_real_content.py`:

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tests/test_real_content.py -v`
Expected: FAIL — `ContentError: content/site.yml does not exist`

- [ ] **Step 3: Write `content/site.yml`**

Note the quoted `detail:` values under `education`. An unquoted internal
colon (`Advisor: Javier`) makes YAML read the rest as a nested mapping key
and the file fails to parse. Quote any value containing `: `.

```yaml
name: Juan Felipe Imbet
short_name: Juan F. Imbet
title: Assistant Professor of Finance
institution: EDHEC Business School
email: juan.imbet@edhec.edu
office: ""
photo: assets/images/profile.jpg
cv: cv.pdf
tagline: Finance, computation, and machine intelligence.
research_interests:
  - Corporate Finance
  - Asset Pricing
  - Computational Finance
bio: |
  I am an Assistant Professor of Finance at EDHEC Business School. My research
  sits at the intersection of corporate finance, asset pricing, and
  computational finance.

  Two agendas run through most of my work. The first studies how the offshore
  finance industry shapes what firms actually do — how they invest, how they
  are taxed, and what happens when secrecy breaks down. The second studies how
  social media moves capital, from mutual fund flows to the speed of a bank
  run.

  Increasingly, both use large language models as research instruments rather
  than as objects of study. I teach that toolkit at the Barcelona School of
  Economics, and I hold a PhD in Finance from Universitat Pompeu Fabra.
profiles:
  scholar: https://scholar.google.com/citations?user=0nHr8-4AAAAJ
  orcid: https://orcid.org/0000-0003-4970-3711
  github: https://github.com/jfimbett
  linkedin: https://www.linkedin.com/in/juan-f-imbet-0b053079/
  x: https://twitter.com/JuanImbett
  ssrn: ""
  # repec: https://ideas.repec.org/e/pim50.html
  # researchgate: https://www.researchgate.net/profile/Juan-Imbet
previous_affiliations:
  - institution: Université Paris Dauphine–PSL
    role: Assistant Professor of Finance
    years: 2021–2026
  - institution: Institute for Advanced Studies, Luxembourg
    role: External Member of the Scientific Council
    years: 2024–2028
education:
  - institution: Universitat Pompeu Fabra
    detail: "PhD in Finance (cum laude). Advisor: Javier Gil-Bazo"
    years: 2016–2021
  - institution: The Wharton School, University of Pennsylvania
    detail: "Visiting PhD student in Finance. Sponsor: Winston Dou"
    years: 2020
  - institution: Universitat Pompeu Fabra
    detail: MRes in Finance
    years: 2015–2016
  - institution: Barcelona School of Economics
    detail: MSc in Finance
    years: 2014–2015
  - institution: Universidad de los Andes
    detail: BA in Economics; BSc in Industrial Engineering; Minor in Mathematics
    years: 2008–2013
```

- [ ] **Step 4: Write `content/courses.yml`**

```yaml
# Courses are hidden while this list is empty: build.py emits no teaching.html
# and no Teaching nav item. Add an entry and rebuild to turn the page on.
#
# - id: llm-finance
#   title: Large Language Models in Finance
#   institution: Barcelona School of Economics
#   level: Summer School
#   years: [2025, 2026]
#   url: https://jfimbett.github.io/llm-finance-book
#   description: One or two sentences.
[]
```

- [ ] **Step 5: Write `content/papers.yml`**

Nine entries. Copy each `abstract` verbatim from the corresponding block in the existing `index.html`. Write each `summary` fresh.

```yaml
- id: social-media-bank-run
  title: Social Media as a Bank Run Catalyst
  authors: [J. Anthony Cookson, Corbin Fox, Javier Gil-Bazo, SELF, Christoph Schiller]
  status: published
  venue: Journal of Financial Economics
  detail: Volume 176, 2026, 104218
  year: 2026
  doi: https://www.sciencedirect.com/science/article/pii/S0304405X25002260
  ssrn: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4422754
  topics: [social media, banking, bank runs]
  abstract: |
    <verbatim from index.html>
  summary: |
    When Silicon Valley Bank collapsed, the banks that suffered most were not
    simply the weakest ones — they were the ones whose depositors were already
    talking on Twitter. Banks with high pre-existing Twitter exposure lost 4.3
    percentage points more market value during the run. What mattered was
    attention rather than anger: negative sentiment did not predict damage, but
    sustained attention from tech-community users, and tweets explicitly about
    running, did. Social media has made deposit flight faster than the
    regulatory tools designed to contain it.
  media:
    - {outlet: Wall Street Journal, title: "The Surprising Risk That Turbocharged a $142 Billion Bank Run", url: "https://www.wsj.com/articles/silicon-valley-bank-run-twitter-59061759"}
    - {outlet: Financial Times, title: "Wake up to the dangers of digital bank runs", url: "https://www.ft.com/content/a60e543d-c950-4ebb-8da9-d6b0b359ad7b"}
    - {outlet: Financial Times, title: "A hat-trick of genuinely interesting papers relevant to the banking mess", url: "https://www.ft.com/content/adb0ca9e-010b-4861-a2b5-ec0e30916956#comments-anchor"}
    - {outlet: The New York Times, title: "A social-media-powered bank run (DealBook)", url: "https://www.nytimes.com/2023/04/21/business/dealbook/buzzfeed-news-shuts-down.html"}
    - {outlet: CNBC, title: "Social media raises bank run risk, fueled SVB's collapse, paper says", url: "https://www.cnbc.com/2023/04/24/social-media-raises-bank-run-risk-fueled-svbs-collapse-paper-says.html"}
    - {outlet: Fortune, title: "Twitter poses a risk to the financial system and helped fuel the SVB run", url: "https://fortune.com/2023/04/24/twitter-financial-system-risk-silicon-valley-bank-run-study/"}
    - {outlet: Axios, title: "Twitter fueled run on Silicon Valley Bank, new paper finds", url: "https://www.axios.com/2023/04/24/twitter-svb-bank-run"}
    - {outlet: Money, title: "Study Finds Twitter Chatter Fueled SVB Collapse", url: "https://money.com/twitter-svb-collapse-study/"}
    - {outlet: Kiplinger, title: "Did Tweets Help Crash Silicon Valley Bank?", url: "https://www.nasdaq.com/articles/did-tweets-help-crash-silicon-valley-bank-paper-shows-new-social-media-risks"}
    - {outlet: TechNewsWorld, title: "Social Media Fueled the Run on Silicon Valley Bank: Study", url: "https://www.technewsworld.com/story/social-media-fueled-the-run-on-silicon-valley-bank-study-178230.html"}
  regulators:
    - {body: "California DFPI", title: "Review of DFPI's Oversight and Regulation of Silicon Valley Bank", url: "https://dfpi.ca.gov/wp-content/uploads/sites/337/2023/05/Review-of-DFPIs-Oversight-and-Regulation-of-Silicon-Valley-Bank.pdf"}
    - {body: "Banco de la República de Colombia", title: "Reporte de Estabilidad Financiera", url: "https://repositorio.banrep.gov.co/bitstream/handle/20.500.12134/10638/reporte-estabilidad-financiera-primer-semestre-2023.pdf?sequence=1"}

- id: tweeting-for-money
  title: "Tweeting for Money: Social Media and Mutual Fund Flows"
  authors: [Javier Gil-Bazo, SELF]
  status: published
  venue: Management Science
  detail: Published online 18 November 2025
  year: 2025
  doi: https://pubsonline.informs.org/doi/10.1287/mnsc.2024.07584
  ssrn: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3719169
  topics: [social media, mutual funds, fund flows]
  abstract: |
    <verbatim from index.html>
  summary: |
    Asset managers talk to investors on social media, and it works. Across more
    than 1.6 million posts by US mutual fund families, both how much a family
    posts and how positive it sounds predict the money flowing into its funds.
    This is not just advertising by another name: the effect survives
    controlling for marketing spend, and intraday ETF trades let us watch
    tweets move investor decisions directly. What it does not appear to be is
    helpful — the evidence does not support the idea that these posts are
    lowering search costs for investors trying to find the right fund.

- id: short-term-options
  title: The Forecasting Power of Short-Term Options
  authors: [Arthur Böök, SELF, Martin Reinke, Carlo Sala]
  status: published
  venue: The Journal of Derivatives
  detail: Spring 2025, 32(3), 80–116
  year: 2025
  ssrn: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3622433
  topics: [derivatives, options, forecasting]
  abstract: |
    <verbatim from index.html>
  summary: |
    Option prices encode what the market expects to happen, but the standard
    ways of extracting that expectation are fragile. We build measures of
    expected volatility, skewness and kurtosis from weekly S&P 500 options
    using quantiles rather than the usual machinery, fitted with a smoothing
    technique that is fast and cannot imply arbitrage. The resulting
    forward-looking indicators predict the US equity risk premium over short,
    medium and long horizons, in and out of sample, and they beat the
    equivalent measures built from past returns.

- id: offshore-data-leaks
  title: "The Real Effects of Offshore Data Leaks: Evidence from Private Firms"
  authors: [Marcelo Ortiz M., SELF]
  status: working
  year: 2024
  ssrn: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4557679
  topics: [offshore finance, tax evasion, corporate investment]
  abstract: |
    <verbatim from index.html>
  summary: |
    Leaks like the Panama Papers did more than embarrass their subjects. Matching
    leaked records to company accounts reveals thousands of small private firms
    using tax havens — and shows that before the leaks these firms invested more
    in plant and people, with the least productive firms benefiting most. After
    exposure, their investment fell sharply. Offshore tax evasion was quietly
    subsidising domestic investment by firms that would not otherwise have
    justified it.

- id: dynamic-contracting-tax
  title: Dynamic Contracting and Corporate Tax Strategies
  authors: [SELF, Marcelo Ortiz M., Vincent Tena]
  status: working
  year: 2024
  ssrn: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4872375
  topics: [corporate taxation, contract theory, moral hazard]
  abstract: |
    <verbatim from index.html>
  summary: |
    Why do firms evade less tax than a pure cost-benefit calculation predicts?
    Because someone has to be paid to do it. Modelling tax strategy as a task an
    owner delegates to an agent they cannot monitor, under the threat of random
    audits, shows that a cautious owner may decline to contract on tax
    aggressiveness at all — a contractual explanation for the long-standing
    puzzle of corporate under-sheltering.

- id: stroke-of-a-pen
  title: "Stroke of a Pen: Investment and Stock Returns under Energy Policy Uncertainty"
  authors: [SELF]
  status: working
  year: 2020
  ssrn: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3711536
  topics: [asset pricing, energy policy, uncertainty, investment]
  abstract: |
    <verbatim from index.html>
  summary: |
    Uncertainty usually makes firms wait. Energy policy uncertainty does the
    opposite: when it is unclear whether a president will sign an energy
    executive order, firms invest more, not less, because energy-efficient
    capital is worth more precisely when energy policy might change. The effect
    is strongest for growth firms, and it shows up in stock returns.

- id: competitive-executive-compensation
  title: Competitive Executive Compensation with Profitability Shocks
  authors: [Gilles Chemla, SELF, Marcelo Ortiz, Vincent Tena]
  status: working
  year: 2025
  url: https://drive.google.com/file/d/18IGmIvlAZbVYd16BJVoUoldJhJD2vGV8/view
  topics: [executive compensation, contract theory, labor markets]
  abstract: |
    <verbatim from index.html>
  summary: |
    Conventional wisdom says executives should not be paid for luck. This model
    says otherwise once the labour market is competitive and replacing an
    executive is costly: an industry-wide profit shock raises what rivals will
    pay your CEO, so paying for luck becomes a retention cost rather than a
    governance failure. The prediction is sharp — pay should respond to
    industry-wide shocks but not to firm-specific ones.

- id: theories-as-regularizers
  title: Theories as Regularizers
  authors: [Amedeo Andriollo, SELF]
  status: wip
  topics: [machine learning, asset pricing, methodology]
  summary: |
    Using economic theory not as a hypothesis to be tested but as a constraint
    that disciplines a machine learning model — keeping the flexibility of
    modern methods while refusing predictions the theory rules out.

- id: liquid-assets
  title: Liquid Assets
  authors: [SELF, Roman Kräussl, Ilaria Piatti, Roberto Steri]
  status: wip
  topics: [alternative assets, liquidity, asset pricing]
```

Note that `theories-as-regularizers` carries a `summary` with no `abstract`, and `liquid-assets` carries neither. Both are valid: `test_every_paper_with_an_abstract_has_a_summary` only constrains papers that have an abstract.

- [ ] **Step 6: Transcribe the abstracts**

Replace every `<verbatim from index.html>` placeholder with the real abstract text, and finish the two incomplete summaries. Extract them with:

```bash
python3 - <<'EOF'
import html, re
source = open("index.html", encoding="utf-8").read()
for match in re.finditer(r'<strong>Abstract:</strong>(.*?)</p>', source, re.S):
    text = re.sub(r'\s+', ' ', html.unescape(match.group(1))).strip()
    print(text, "\n---\n")
EOF
```

Only the `<verbatim from index.html>` markers remain to be replaced; every
`summary` above is already final prose. Verify nothing was missed:

```bash
! grep -n "verbatim from index.html\|<Complete\|<One plain-language" content/papers.yml
```

Expected: exit status 0 (no matches found).

Then confirm all nine abstracts are non-trivial:

```bash
python3 -c "
import yaml
papers = yaml.safe_load(open('content/papers.yml'))
for p in papers:
    a = (p.get('abstract') or '').strip()
    print('%-34s abstract=%4d summary=%4d' % (p['id'], len(a), len((p.get('summary') or '').strip())))
"
```

Expected: seven papers with an abstract over 400 characters (the two
work-in-progress entries have none), and every paper with an abstract also
showing a non-zero summary length.

- [ ] **Step 7: Run the tests to verify they pass**

Run: `python3 -m pytest tests/ -v`
Expected: PASS, all tests

- [ ] **Step 8: Commit**

```bash
git add content/ tests/test_real_content.py
git commit -m "feat: author site, paper, and course content as YAML"
```

---

### Task 3: The design system stylesheet

**Files:**
- Create: `assets/css/site.css`
- Create: `tests/test_css.py`

**Interfaces:**
- Consumes: nothing.
- Produces: the class vocabulary every template uses — `.wrap`, `.site-nav`, `.hero`, `.hero__canvas`, `.hero__portrait`, `.rule`, `.entry`, `.entry__num`, `.entry__body`, `.entry__title`, `.entry__authors`, `.entry__venue`, `.entry__links`, `.section`, `.section--tint`, `.section__title`, `.eyebrow`, `.skip-link`, `.profile-links`, `.summary`, `.chip`.

This is one file and one responsibility: the entire visual system. No other stylesheet exists.

- [ ] **Step 1: Write the failing test**

Contrast bugs are silent and this file is the only place colour is defined, so guard the tokens directly. Create `tests/test_css.py`:

```python
"""Guards on the design tokens. Contrast failures are invisible in review."""

import re
from pathlib import Path

import pytest

CSS = Path(__file__).parent.parent / "assets" / "css" / "site.css"


@pytest.fixture(scope="module")
def css():
    return CSS.read_text(encoding="utf-8")


def _srgb_to_linear(channel):
    channel = channel / 255.0
    if channel <= 0.04045:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4


def _luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return (
        0.2126 * _srgb_to_linear(r)
        + 0.7152 * _srgb_to_linear(g)
        + 0.0722 * _srgb_to_linear(b)
    )


def contrast(foreground, background):
    light, dark = sorted((_luminance(foreground), _luminance(background)))
    return (dark + 0.05) / (light + 0.05)


LIGHT = {"grenat": "#5F1937", "ink": "#0E0E0E", "paper": "#FFFFFF",
         "pastel": "#ECE4E7", "muted": "#5A5A5A",
         "coral_ink": "#A63446", "bleu_ink": "#007FB0"}
DARK = {"grenat": "#D4849F", "ink": "#F2ECEE", "paper": "#0E0E0E",
        "coral": "#FF6E6E", "bleu": "#00B9FF"}


@pytest.mark.parametrize(
    "foreground,background,minimum",
    [
        (LIGHT["ink"], LIGHT["paper"], 4.5),
        (LIGHT["muted"], LIGHT["paper"], 4.5),
        (LIGHT["grenat"], LIGHT["paper"], 4.5),
        (LIGHT["grenat"], LIGHT["pastel"], 4.5),
        (LIGHT["ink"], LIGHT["pastel"], 4.5),
        (DARK["ink"], DARK["paper"], 4.5),
        (DARK["grenat"], DARK["paper"], 4.5),
        # Interactive variants: link hover text and the focus ring.
        (LIGHT["coral_ink"], LIGHT["paper"], 4.5),
        (LIGHT["coral_ink"], LIGHT["pastel"], 4.5),
        (LIGHT["bleu_ink"], LIGHT["paper"], 3.0),
        (DARK["coral"], DARK["paper"], 4.5),
        (DARK["bleu"], DARK["paper"], 4.5),
    ],
)
def test_contrast_meets_wcag_aa(foreground, background, minimum):
    ratio = contrast(foreground, background)
    assert ratio >= minimum, "{} on {} is {:.2f}:1".format(
        foreground, background, ratio
    )


def test_all_brand_tokens_are_defined(css):
    for token in (
        "--grenat", "--ink", "--paper", "--grenat-pastel",
        "--coral", "--bleu", "--border", "--muted",
    ):
        assert "{}:".format(token) in css, "missing token {}".format(token)


def test_exact_brand_values_are_used(css):
    for value in ("#5F1937", "#0E0E0E", "#ECE4E7", "#FF6E6E", "#00B9FF", "#DCDCDC"):
        assert value in css, "missing EDHEC brand value {}".format(value)


def test_raw_coral_and_bleu_are_never_used_for_text_or_focus(css):
    """Raw coral is 2.72:1 and raw bleu 2.24:1 on white: decorative fills only.

    Anchored to declaration starts, so a shorthand that merely *contains* a
    colour (border-left: 3px solid var(--coral)) is not mistaken for a text
    colour. Only `color`, `outline`, and `outline-color` identify text or a
    focus indicator.
    """
    offenders = []
    for head, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        for prop, value in re.findall(
            r"(?:^|;)\s*(color|outline|outline-color)\s*:\s*([^;]+)", body
        ):
            if "var(--coral)" in value or "var(--bleu)" in value:
                offenders.append(
                    "{} -> {}: {}".format(head.strip(), prop, value.strip())
                )
    assert not offenders, "raw decorative tokens used for text/focus: {}".format(
        offenders
    )


def test_interactive_variants_are_defined(css):
    assert "--coral-ink:" in css
    assert "--bleu-ink:" in css
    assert "#A63446" in css
    assert "#007FB0" in css


def test_dark_theme_is_defined(css):
    assert "prefers-color-scheme: dark" in css
    assert "#D4849F" in css, "dark theme must lift grenat for contrast"


def test_reduced_motion_is_respected(css):
    assert "prefers-reduced-motion" in css


def test_no_bootstrap_or_fontawesome_remains(css):
    lowered = css.lower()
    assert "bootstrap" not in lowered
    assert "font-awesome" not in lowered
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tests/test_css.py -v`
Expected: FAIL — `FileNotFoundError` for `assets/css/site.css`

- [ ] **Step 3: Write the stylesheet**

Create `assets/css/site.css`. Delete the old `assets/css/custom.css` in Task 11, not here.

```css
/* ==========================================================================
   Juan Felipe Imbet — design system
   Palette and type pairing taken from EDHEC's production theme:
   https://www.edhec.edu/themes/custom/edhec/css/variables.css
   ========================================================================== */

:root {
  --grenat: #5F1937;
  --ink: #0E0E0E;
  --paper: #FFFFFF;
  --grenat-pastel: #ECE4E7;
  --coral: #FF6E6E;        /* decorative fills only — 2.72:1 on white */
  --bleu: #00B9FF;         /* decorative fills only — 2.24:1 on white */
  --coral-ink: #A63446;    /* interactive text/borders — 6.56:1 on white */
  --bleu-ink: #007FB0;     /* focus rings — 4.50:1 on white */
  --border: #DCDCDC;
  --muted: #5A5A5A;

  --display: "Montserrat", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --body: "Open Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;

  --step--1: clamp(0.80rem, 0.77rem + 0.15vw, 0.88rem);
  --step-0:  clamp(1.00rem, 0.96rem + 0.20vw, 1.13rem);
  --step-1:  clamp(1.25rem, 1.18rem + 0.35vw, 1.45rem);
  --step-2:  clamp(1.56rem, 1.44rem + 0.60vw, 1.94rem);
  --step-3:  clamp(1.95rem, 1.74rem + 1.05vw, 2.63rem);
  --step-4:  clamp(2.44rem, 2.08rem + 1.80vw, 3.75rem);

  --wrap: 1200px;
  --gutter: clamp(1.25rem, 4vw, 3rem);
  --rhythm: clamp(3rem, 7vw, 6rem);
}

@media (prefers-color-scheme: dark) {
  :root {
    --grenat: #D4849F;
    --ink: #F2ECEE;
    --paper: #0E0E0E;
    --grenat-pastel: #1B1216;
    --border: #33282C;
    --muted: #A79AA0;
    /* On near-black these pass comfortably, so the bright originals return. */
    --coral-ink: #FF6E6E;
    --bleu-ink: #00B9FF;
  }
}

*, *::before, *::after { box-sizing: border-box; }

html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--body);
  font-size: var(--step-0);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4 {
  font-family: var(--display);
  font-weight: 700;
  line-height: 1.15;
  color: var(--grenat);
  margin: 0 0 0.5em;
  letter-spacing: -0.015em;
}

p { margin: 0 0 1.15em; max-width: 68ch; }

a { color: var(--grenat); text-decoration-thickness: 1px; text-underline-offset: 0.18em; }
a:hover { color: var(--coral-ink); }

:focus-visible {
  outline: 3px solid var(--bleu-ink);
  outline-offset: 2px;
  border-radius: 2px;
}

img { max-width: 100%; height: auto; }

.wrap { width: 100%; max-width: var(--wrap); margin-inline: auto; padding-inline: var(--gutter); }

.skip-link {
  position: absolute; left: -9999px;
  background: var(--grenat); color: #FFFFFF;
  padding: 0.75rem 1.25rem; z-index: 100;
}
.skip-link:focus { left: 1rem; top: 1rem; }

/* --- Navigation ---------------------------------------------------------- */

.site-nav {
  position: sticky; top: 0; z-index: 50;
  background: color-mix(in srgb, var(--paper) 88%, transparent);
  backdrop-filter: saturate(180%) blur(12px);
  border-bottom: 1px solid var(--border);
}
.site-nav__inner {
  display: flex; align-items: center; justify-content: space-between;
  gap: 1.5rem; min-height: 4.25rem;
}
.site-nav__brand {
  font-family: var(--display); font-weight: 700; font-size: var(--step--1);
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--grenat); text-decoration: none; white-space: nowrap;
}
.site-nav__links { display: flex; gap: clamp(1rem, 3vw, 2.25rem); align-items: center; }
.site-nav__links a {
  font-family: var(--display); font-weight: 600; font-size: var(--step--1);
  color: var(--ink); text-decoration: none;
  padding-block: 0.35rem; border-bottom: 2px solid transparent;
}
.site-nav__links a:hover { color: var(--grenat); border-bottom-color: var(--coral-ink); }
.site-nav__links a[aria-current="page"] { color: var(--grenat); border-bottom-color: var(--grenat); }

/* --- Hero ---------------------------------------------------------------- */

.hero { padding-block: clamp(3rem, 8vw, 6rem) clamp(2rem, 5vw, 4rem); }
.hero__grid {
  display: grid; gap: clamp(2rem, 5vw, 4rem);
  grid-template-columns: 1fr;
  align-items: center;
}
@media (min-width: 900px) {
  .hero__grid { grid-template-columns: 1.15fr 0.85fr; }
}
.hero__title {
  font-size: var(--step-4); margin-bottom: 0.35em;
  text-wrap: balance;
}
.hero__role {
  font-family: var(--display); font-weight: 600; font-size: var(--step-1);
  color: var(--ink); margin: 0 0 0.15em;
}
.hero__institution { color: var(--muted); font-size: var(--step-0); margin-bottom: 1.5rem; }

.rule { border: 0; height: 3px; width: 4.5rem; background: var(--coral); margin: 1.75rem 0; }

.hero__figure { position: relative; }
.hero__canvas {
  display: block; width: 100%; aspect-ratio: 1 / 1;
  background: var(--grenat-pastel);
}
.hero__portrait {
  /* Native size is 369x560; never upscale it. */
  display: block; width: min(100%, 369px); margin-inline: auto;
  border: 1px solid var(--border);
}
.hero__anchor-label {
  position: absolute; pointer-events: none;
  font-family: var(--mono); font-size: var(--step--1);
  background: var(--grenat); color: #FFFFFF;
  padding: 0.3rem 0.55rem; opacity: 0; transition: opacity 120ms;
}
.hero__anchor-label[data-visible="true"] { opacity: 1; }

/* --- Sections ------------------------------------------------------------ */

.section { padding-block: var(--rhythm); }
.section--tint { background: var(--grenat-pastel); }
.eyebrow {
  font-family: var(--display); font-weight: 700; font-size: var(--step--1);
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--muted); margin-bottom: 0.75rem;
}
.section__title { font-size: var(--step-3); margin-bottom: 2.5rem; }

/* --- Numbered entries ---------------------------------------------------- */

.entry {
  display: grid; gap: 0.5rem 2rem;
  grid-template-columns: 1fr;
  padding-block: 2.25rem;
  border-top: 1px solid var(--border);
}
.entry:last-child { border-bottom: 1px solid var(--border); }
@media (min-width: 760px) {
  .entry { grid-template-columns: 4.5rem 1fr; }
}
.entry__num {
  font-family: var(--display); font-weight: 700; font-size: var(--step-1);
  color: var(--grenat); font-variant-numeric: tabular-nums; line-height: 1.2;
}
.entry__title { font-size: var(--step-1); margin-bottom: 0.35rem; }
.entry__title a { text-decoration: none; }
.entry__title a:hover { text-decoration: underline; }
.entry__authors { color: var(--ink); margin-bottom: 0.2rem; }
.entry__authors strong { font-weight: 600; }
.entry__venue {
  font-family: var(--display); font-weight: 600; font-size: var(--step--1);
  color: var(--muted); margin-bottom: 0.9rem;
}
.summary {
  border-left: 3px solid var(--coral);
  padding-left: 1.15rem; margin-block: 1.1rem;
  color: var(--ink);
}
.summary p { margin-bottom: 0; }

.entry details { margin-block: 0.75rem; }
.entry summary {
  cursor: pointer; font-family: var(--display); font-weight: 600;
  font-size: var(--step--1); color: var(--grenat);
  list-style: none; padding-block: 0.35rem;
}
.entry summary::-webkit-details-marker { display: none; }
.entry summary::before { content: "+ "; font-variant-numeric: tabular-nums; }
.entry details[open] summary::before { content: "− "; }

.entry__links { display: flex; flex-wrap: wrap; gap: 0.5rem 1.25rem; margin-top: 0.75rem; }
.entry__links a {
  font-family: var(--display); font-weight: 600; font-size: var(--step--1);
  text-decoration: none; border-bottom: 1px solid var(--border);
  padding-bottom: 2px;
}
.entry__links a:hover { border-bottom-color: var(--coral-ink); }

.chip {
  display: inline-block; font-family: var(--mono); font-size: var(--step--1);
  color: var(--muted); border: 1px solid var(--border);
  padding: 0.1rem 0.5rem; margin-right: 0.35rem;
}

/* --- Footer -------------------------------------------------------------- */

.site-footer {
  border-top: 1px solid var(--border);
  padding-block: var(--rhythm) 2.5rem;
  margin-top: var(--rhythm);
}
.profile-links { display: flex; gap: 1.25rem; align-items: center; }
.profile-links a { color: var(--ink); display: inline-flex; }
.profile-links a:hover { color: var(--coral-ink); }
.profile-links svg { width: 22px; height: 22px; fill: currentColor; }

.colophon { color: var(--muted); font-size: var(--step--1); margin-top: 2rem; }
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m pytest tests/test_css.py -v`
Expected: PASS

If a contrast assertion fails, adjust the token in **both** `site.css` and the test's `LIGHT`/`DARK` dictionaries, and record the new value in the spec's Section 4.2 table. Never relax the threshold.

- [ ] **Step 5: Commit**

```bash
git add assets/css/site.css tests/test_css.py
git commit -m "feat: add EDHEC-derived design system stylesheet"
```

---

### Task 4: Templates and page rendering

**Files:**
- Create: `templates/base.html.j2`, `templates/index.html.j2`, `templates/research.html.j2`, `templates/cv.html.j2`, `templates/teaching.html.j2`
- Create: `templates/partials/paper.html.j2`, `templates/partials/icons.html.j2`
- Modify: `build.py`
- Modify: `assets/css/site.css` (Step 10 appends the `.visually-hidden` and `.site-nav__search` rules)
- Create: `tests/test_render.py`

**Interfaces:**
- Consumes: `load_yaml`, `validate_*`, `CONTENT`, `ROOT`, `SELF` from Task 1; the class vocabulary from Task 3; the content from Task 2.
- Produces: `format_authors(authors: list, self_name: str) -> str` (returns HTML, `SELF` becomes `<strong>`); `partition(papers: list) -> dict` with keys `published`, `working`, `wip`; `build_context() -> dict`; `render_site(out_dir: Path = ROOT) -> list` returning the paths written; `main() -> int`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_render.py`:

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_render.py -v`
Expected: FAIL — `ImportError: cannot import name 'format_authors' from 'build'`

- [ ] **Step 3: Extend `build.py` with rendering**

Append to `build.py` (keep the existing validators above), and add `import html`, `import json`, `import sys` and `from jinja2 import Environment, FileSystemLoader, select_autoescape` to the imports:

```python
TEMPLATES = ROOT / "templates"

PAGES = [
    ("index.html.j2", "index.html", "home"),
    ("research.html.j2", "research.html", "research"),
    ("cv.html.j2", "cv.html", "cv"),
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
    }


def _environment():
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html"]),
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

    return written


def main():
    try:
        written = render_site()
    except ContentError as exc:
        sys.stderr.write("Content validation failed:\n{}\n".format(exc))
        return 1
    for path in written:
        print("wrote {}".format(path.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Write `templates/partials/icons.html.j2`**

Inline SVG replaces Font Awesome. One macro per profile.

```jinja
{% macro icon(name) -%}
{% if name == 'scholar' %}
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3L1 9l11 6 9-4.9V17h2V9L12 3zM5 13.2V17c0 1.7 3.1 3 7 3s7-1.3 7-3v-3.8l-7 3.8-7-3.8z"/></svg>
{% elif name == 'orcid' %}
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.6 0 12 0zM7.7 17.9H6V7.6h1.7v10.3zM6.8 6.3a1.1 1.1 0 110-2.2 1.1 1.1 0 010 2.2zm10.6 11.6h-3.9V7.6h3.7c3.6 0 5.2 2.5 5.2 5.1 0 2.9-2.2 5.2-5 5.2zm-.2-8.7h-2v7.1h2c2 0 3.4-1.4 3.4-3.6 0-2-1.2-3.5-3.4-3.5z"/></svg>
{% elif name == 'github' %}
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .3a12 12 0 00-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 016 0C17.3 4.7 18.3 5 18.3 5c.6 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0012 .3z"/></svg>
{% elif name == 'linkedin' %}
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.4 20.4h-3.6v-5.6c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9v5.7H9.4V9h3.4v1.6h.1a3.7 3.7 0 013.4-1.8c3.6 0 4.2 2.4 4.2 5.5v6.1zM5.3 7.4a2.1 2.1 0 112.1-2.1 2.1 2.1 0 01-2.1 2.1zM7.1 20.4H3.6V9h3.5v11.4zM22.2 0H1.8A1.8 1.8 0 000 1.8v20.4A1.8 1.8 0 001.8 24h20.4a1.8 1.8 0 001.8-1.8V1.8A1.8 1.8 0 0022.2 0z"/></svg>
{% elif name == 'x' %}
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.2 2.3h3.4l-7.4 8.4 8.7 11.5h-6.8l-5.3-7-6.1 7H1.3l7.9-9-8.3-10.9h7l4.8 6.4 5.5-6.4zm-1.2 17.9h1.9L7.1 4.2H5l12 16z"/></svg>
{% elif name == 'ssrn' %}
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 3h16v2H4zm0 5h16v2H4zm0 5h10v2H4zm0 5h10v2H4z"/></svg>
{% elif name == 'email' %}
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 4h20v16H2V4zm2 2v.5l8 5 8-5V6H4zm16 3l-8 5-8-5v9h16V9z"/></svg>
{% endif %}
{%- endmacro %}

{% set profile_labels = {
  'scholar': 'Google Scholar', 'orcid': 'ORCID', 'github': 'GitHub',
  'linkedin': 'LinkedIn', 'x': 'X', 'ssrn': 'SSRN'
} %}
{#
  base.html.j2 must import BOTH names:
    {% from 'partials/icons.html.j2' import icon, profile_labels with context %}
  Importing only `icon` leaves profile_labels undefined at render time —
  verified against Jinja2 3.1.2, which raises UndefinedError.
#}
```

- [ ] **Step 5: Write `templates/base.html.j2`**

```jinja
{% from 'partials/icons.html.j2' import icon, profile_labels with context %}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% block title %}{{ site.name }}{% endblock %}</title>
<meta name="description" content="{% block description %}{{ site.name }}, {{ site.title }} at {{ site.institution }}. Research in corporate finance, asset pricing, and computational finance.{% endblock %}">
<link rel="canonical" href="{{ canonical | default('https://jfimbett.github.io/') }}">

<meta property="og:type" content="website">
<meta property="og:title" content="{{ self.title() }}">
<meta property="og:description" content="{{ self.description() }}">
<meta property="og:image" content="https://jfimbett.github.io/{{ site.photo }}">
<meta name="twitter:card" content="summary">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
<link href="{{ prefix | default('') }}assets/css/site.css" rel="stylesheet">
{% block head %}{% endblock %}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<nav class="site-nav">
  <div class="wrap site-nav__inner">
    <a class="site-nav__brand" href="index.html">{{ site.short_name }}</a>
    <div class="site-nav__links">
      <a href="index.html"{% if page == 'home' %} aria-current="page"{% endif %}>About</a>
      <a href="research.html"{% if page == 'research' %} aria-current="page"{% endif %}>Research</a>
      {% if has_teaching %}
      <a href="teaching.html"{% if page == 'teaching' %} aria-current="page"{% endif %}>Teaching</a>
      {% endif %}
      <a href="cv.html"{% if page == 'cv' %} aria-current="page"{% endif %}>CV</a>
      <button type="button" id="search-open" class="site-nav__search" aria-label="Search this site" aria-expanded="false">⌕</button>
    </div>
  </div>
</nav>

<main id="main">
{% block content %}{% endblock %}
</main>

<footer class="site-footer">
  <div class="wrap">
    <h2 class="eyebrow">Contact</h2>
    <p>
      <a href="mailto:{{ site.email }}">{{ site.email }}</a><br>
      {{ site.title }}, {{ site.institution }}
      {% if site.office %}<br>{{ site.office }}{% endif %}
    </p>
    <div class="profile-links">
      {% for key, url in site.profiles.items() %}
      {% if url %}
      <a href="{{ url }}" rel="me noopener" target="_blank" title="{{ profile_labels[key] }}">
        <span class="visually-hidden">{{ profile_labels[key] }}</span>{{ icon(key) }}
      </a>
      {% endif %}
      {% endfor %}
    </div>
    <p class="colophon">© {{ year }} {{ site.name }}. Built from YAML with a small Python script; source on <a href="{{ site.profiles.github }}/jfimbett.github.io">GitHub</a>.</p>
  </div>
</footer>

<script type="module" src="{{ prefix | default('') }}assets/js/search.js"></script>
{% block scripts %}{% endblock %}
</body>
</html>
```

Add `"year": 2026` to the dictionary returned by `build_context()` so the colophon renders. Use a fixed value rather than `datetime.now()`: the output is committed, and a moving year would produce a spurious diff on every build.

- [ ] **Step 6: Write `templates/partials/paper.html.j2`**

```jinja
{% macro entry(paper, number) %}
<article class="entry" id="{{ paper.id }}">
  <div class="entry__num" aria-hidden="true">{{ '%02d' % number }}</div>
  <div class="entry__body">
    <h3 class="entry__title">
      {% if paper.doi or paper.ssrn or paper.url %}
      <a href="{{ paper.doi or paper.ssrn or paper.url }}" target="_blank" rel="noopener">{{ paper.title }}</a>
      {% else %}
      {{ paper.title }}
      {% endif %}
    </h3>
    <p class="entry__authors">{{ paper.authors_html | safe }}</p>
    {% if paper.venue %}
    <p class="entry__venue">{{ paper.venue }}{% if paper.detail %} · {{ paper.detail }}{% endif %}</p>
    {% elif paper.status == 'working' %}
    <p class="entry__venue">Working paper</p>
    {% elif paper.status == 'wip' %}
    <p class="entry__venue">Work in progress</p>
    {% endif %}

    {% if paper.summary %}
    <div class="summary"><p>{{ paper.summary | trim }}</p></div>
    {% endif %}

    {% if paper.abstract %}
    <details>
      <summary>Abstract</summary>
      <p>{{ paper.abstract | trim }}</p>
    </details>
    {% endif %}

    {% if paper.media %}
    <details>
      <summary>Media coverage ({{ paper.media | length }})</summary>
      <ul>
        {% for item in paper.media %}
        <li><a href="{{ item.url }}" target="_blank" rel="noopener">{{ item.title }}</a> — {{ item.outlet }}</li>
        {% endfor %}
      </ul>
    </details>
    {% endif %}

    {% if paper.regulators %}
    <details>
      <summary>Cited by regulators ({{ paper.regulators | length }})</summary>
      <ul>
        {% for item in paper.regulators %}
        <li><a href="{{ item.url }}" target="_blank" rel="noopener">{{ item.title }}</a> — {{ item.body }}</li>
        {% endfor %}
      </ul>
    </details>
    {% endif %}

    <div class="entry__links">
      {% if paper.doi %}<a href="{{ paper.doi }}" target="_blank" rel="noopener">Published version</a>{% endif %}
      {% if paper.ssrn %}<a href="{{ paper.ssrn }}" target="_blank" rel="noopener">SSRN</a>{% endif %}
      {% if paper.url and not paper.doi and not paper.ssrn %}<a href="{{ paper.url }}" target="_blank" rel="noopener">Paper</a>{% endif %}
    </div>

    {% if paper.topics %}
    <p>{% for topic in paper.topics %}<span class="chip">{{ topic }}</span>{% endfor %}</p>
    {% endif %}
  </div>
</article>
{% endmacro %}
```

- [ ] **Step 7: Write `templates/index.html.j2`**

```jinja
{% extends 'base.html.j2' %}
{% from 'partials/paper.html.j2' import entry %}
{% block title %}{{ site.name }} | {{ site.title }}{% endblock %}

{% block head %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": {{ site.name | tojson }},
  "jobTitle": {{ site.title | tojson }},
  "email": {{ ('mailto:' ~ site.email) | tojson }},
  "url": "https://jfimbett.github.io/",
  "affiliation": {"@type": "Organization", "name": {{ site.institution | tojson }}},
  "sameAs": {{ (site.profiles.values() | select | list) | tojson }}
}
</script>
{% endblock %}

{% block content %}
<section class="hero">
  <div class="wrap hero__grid">
    <div>
      <h1 class="hero__title">{{ site.tagline }}</h1>
      <hr class="rule">
      <p class="hero__role">{{ site.name }}</p>
      <p class="hero__institution">{{ site.title }}, {{ site.institution }}</p>
      <p><a href="research.html">Research</a> · <a href="{{ site.cv }}">CV (PDF)</a> · <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    </div>
    <figure class="hero__figure">
      <canvas class="hero__canvas" id="hero-canvas" role="img"
              aria-label="An animated field of particles positioned by the similarity of this researcher's papers."></canvas>
      <div class="hero__anchor-label" id="hero-label" aria-hidden="true"></div>
    </figure>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h2 class="section__title">Biography</h2>
    <div class="hero__grid">
      <div>
        {% for paragraph in site.bio.strip().split('\n\n') %}
        <p>{{ paragraph }}</p>
        {% endfor %}
        <p>{% for interest in site.research_interests %}<span class="chip">{{ interest }}</span>{% endfor %}</p>
      </div>
      <img class="hero__portrait" src="{{ site.photo }}" width="369" height="560"
           alt="Portrait of {{ site.name }}" loading="lazy">
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">Selected work</p>
    <h2 class="section__title">Publications</h2>
    {% for paper in grouped.published %}
    {{ entry(paper, loop.index) }}
    {% endfor %}
    <p style="margin-top:2.5rem"><a href="research.html">All research →</a></p>
  </div>
</section>
{% endblock %}

{% block scripts %}
<script type="module" src="assets/js/hero.js"></script>
{% endblock %}
```

- [ ] **Step 8: Write `templates/research.html.j2`**

```jinja
{% extends 'base.html.j2' %}
{% from 'partials/paper.html.j2' import entry %}
{% block title %}Research | {{ site.name }}{% endblock %}

{% block head %}
<script type="application/ld+json">
{{ {
  "@context": "https://schema.org",
  "@graph": papers | map(attribute='id') | list
} | tojson }}
</script>
{% endblock %}

{% block content %}
<section class="section">
  <div class="wrap">
    <p class="eyebrow">Research</p>
    <h2 class="section__title">Publications</h2>
    {% for paper in grouped.published %}{{ entry(paper, loop.index) }}{% endfor %}
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <h2 class="section__title">Working papers</h2>
    {% for paper in grouped.working %}{{ entry(paper, loop.index) }}{% endfor %}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="section__title">Work in progress</h2>
    {% for paper in grouped.wip %}{{ entry(paper, loop.index) }}{% endfor %}
  </div>
</section>
{% endblock %}
```

The `@graph` above is a placeholder shape only. Task 11 replaces it with real `ScholarlyArticle` objects; leaving it as a bare id list here keeps this task's diff focused on layout.

- [ ] **Step 9: Write `templates/cv.html.j2` and `templates/teaching.html.j2`**

`cv.html.j2`:

```jinja
{% extends 'base.html.j2' %}
{% block title %}CV | {{ site.name }}{% endblock %}
{% block content %}
<section class="section">
  <div class="wrap">
    <p class="eyebrow">Curriculum vitae</p>
    <h2 class="section__title">{{ site.name }}</h2>
    <p><a href="{{ site.cv }}">Download the full CV (PDF)</a></p>
    <hr class="rule">

    <h3>Appointments</h3>
    <article class="entry">
      <div class="entry__num" aria-hidden="true">01</div>
      <div class="entry__body">
        <h4 class="entry__title">{{ site.institution }}</h4>
        <p class="entry__venue">{{ site.title }} · 2026–present</p>
      </div>
    </article>
    {% for post in site.previous_affiliations %}
    <article class="entry">
      <div class="entry__num" aria-hidden="true">{{ '%02d' % (loop.index + 1) }}</div>
      <div class="entry__body">
        <h4 class="entry__title">{{ post.institution }}</h4>
        <p class="entry__venue">{{ post.role }} · {{ post.years }}</p>
      </div>
    </article>
    {% endfor %}

    <h3 style="margin-top:3rem">Education</h3>
    {% for item in site.education %}
    <article class="entry">
      <div class="entry__num" aria-hidden="true">{{ '%02d' % loop.index }}</div>
      <div class="entry__body">
        <h4 class="entry__title">{{ item.institution }}</h4>
        <p class="entry__venue">{{ item.detail }} · {{ item.years }}</p>
      </div>
    </article>
    {% endfor %}
  </div>
</section>
{% endblock %}
```

`teaching.html.j2`:

```jinja
{% extends 'base.html.j2' %}
{% block title %}Teaching | {{ site.name }}{% endblock %}
{% block content %}
<section class="section">
  <div class="wrap">
    <p class="eyebrow">Teaching</p>
    <h2 class="section__title">Courses</h2>
    {% for course in courses %}
    <article class="entry" id="{{ course.id }}">
      <div class="entry__num" aria-hidden="true">{{ '%02d' % loop.index }}</div>
      <div class="entry__body">
        <h3 class="entry__title">
          {% if course.url %}<a href="{{ course.url }}" target="_blank" rel="noopener">{{ course.title }}</a>
          {% else %}{{ course.title }}{% endif %}
        </h3>
        <p class="entry__venue">
          {{ course.institution }}{% if course.level %} · {{ course.level }}{% endif %}
          {% if course.years %} · {{ course.years | join(', ') }}{% endif %}
        </p>
        {% if course.description %}<p>{{ course.description }}</p>{% endif %}
      </div>
    </article>
    {% endfor %}
  </div>
</section>
{% endblock %}
```

- [ ] **Step 10: Add the `visually-hidden` utility**

The base template uses `.visually-hidden` for icon labels. Append to `assets/css/site.css`:

```css
.visually-hidden {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}
.site-nav__search {
  background: none; border: 1px solid var(--border); cursor: pointer;
  color: var(--ink); font-size: var(--step-1); line-height: 1;
  padding: 0.15rem 0.6rem; font-family: var(--body);
}
.site-nav__search:hover { border-color: var(--coral-ink); color: var(--grenat); }
```

- [ ] **Step 11: Run the tests to verify they pass**

Run: `python3 -m pytest tests/ -v`
Expected: PASS, all tests

- [ ] **Step 12: Generate the real pages and inspect them**

Run: `python3 build.py`
Expected: prints `wrote index.html`, `wrote research.html`, `wrote cv.html` and nothing about teaching.

Open `index.html` in a browser. Confirm: nav has four items with no Teaching, the hero reads EDHEC, the portrait is crisp, publications are numbered, and abstracts expand via `<details>` with JavaScript disabled.

- [ ] **Step 13: Verify the build is idempotent**

```bash
python3 build.py && git status --porcelain && python3 build.py && git diff --stat
```

Expected: the second run produces no diff. A non-empty `git diff` here means non-deterministic output — find it and remove it before continuing.

- [ ] **Step 14: Commit**

```bash
git add templates/ build.py tests/test_render.py assets/css/site.css index.html research.html cv.html
git commit -m "feat: render site pages from templates with conditional teaching"
```

---

### Task 5: Search index and BM25 ranking

**Files:**
- Create: `assets/js/package.json`
- Create: `assets/js/bm25.js`
- Create: `tools/test/bm25.test.mjs`
- Modify: `build.py`
- Modify: `tests/test_render.py`

**Interfaces:**
- Consumes: `build_context` from Task 4.
- Produces (JS): `tokenize(text: string) -> string[]`; `buildIndex(docs: {id, text}[]) -> {entries, df, avgdl, N}`; `search(index, query, opts?) -> {id, score}[]` sorted descending. Produces (Python): `write_search_index(context: dict, out_dir: Path) -> Path` writing `assets/data/search.json` as `{"docs": [{"id", "title", "authors", "venue", "status", "topics", "summary", "text"}]}`.

`bm25.js` holds ranking logic only and never touches the DOM, which is what makes it testable under Node.

**Pre-verified.** The `bm25.js` and `pca.mjs` implementations and their tests
were extracted from this plan and executed against Node 22.14.0 before it was
finalised: 8/8 and 6/6 pass exactly as printed. A failure means the
transcription diverged from what is written here.

- [ ] **Step 1: Write the failing JS test**

Create `tools/test/bm25.test.mjs`:

```javascript
import test from 'node:test';
import assert from 'node:assert/strict';
import { tokenize, buildIndex, search } from '../../assets/js/bm25.js';

const DOCS = [
  { id: 'bank-run', text: 'Social Media as a Bank Run Catalyst. Twitter exposure predicted deposit outflows at regional banks.' },
  { id: 'fund-flows', text: 'Tweeting for Money. Social media activity and mutual fund flows.' },
  { id: 'energy', text: 'Stroke of a Pen. Investment and stock returns under energy policy uncertainty.' },
];

test('tokenize lowercases, strips punctuation and drops stopwords', () => {
  const tokens = tokenize('The Bank, of England!');
  assert.ok(tokens.includes('bank'));
  assert.ok(tokens.includes('england'));
  assert.ok(!tokens.includes('the'));
  assert.ok(!tokens.includes('of'));
});

test('tokenize folds accents', () => {
  assert.deepEqual(tokenize('Université'), ['universite']);
});

test('search ranks the obviously relevant document first', () => {
  const index = buildIndex(DOCS);
  assert.equal(search(index, 'bank run deposit')[0].id, 'bank-run');
  assert.equal(search(index, 'mutual fund flows')[0].id, 'fund-flows');
  assert.equal(search(index, 'energy policy uncertainty')[0].id, 'energy');
});

test('search returns nothing for an empty or stopword-only query', () => {
  const index = buildIndex(DOCS);
  assert.deepEqual(search(index, ''), []);
  assert.deepEqual(search(index, 'the of and'), []);
});

test('search returns nothing when no term matches', () => {
  const index = buildIndex(DOCS);
  assert.deepEqual(search(index, 'photosynthesis chlorophyll'), []);
});

test('rarer terms outrank common ones', () => {
  // "social" appears in two documents, "catalyst" in one.
  const index = buildIndex(DOCS);
  assert.equal(search(index, 'catalyst')[0].id, 'bank-run');
  assert.equal(search(index, 'catalyst').length, 1);
});

test('results are sorted by descending score', () => {
  const index = buildIndex(DOCS);
  const results = search(index, 'social media');
  for (let i = 1; i < results.length; i += 1) {
    assert.ok(results[i - 1].score >= results[i].score);
  }
});

test('limit is respected', () => {
  const index = buildIndex(DOCS);
  assert.equal(search(index, 'social media', { limit: 1 }).length, 1);
});
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `node --test tools/test/bm25.test.mjs`
Expected: FAIL — cannot find module `assets/js/bm25.js`

- [ ] **Step 3: Declare `assets/js/` as an ES module directory**

`bm25.js` uses `export`. Node treats a `.js` file as ESM only if the nearest
`package.json` says so. On Node 22 this currently works via syntax
auto-detection, but that is version-dependent and breaks outright if any
`package.json` above it declares `"type": "commonjs"` — verified. Pin it.

Create `assets/js/package.json`:

```json
{
  "type": "module"
}
```

The browser never requests this file; `<script type="module">` already tells
it what to do. It exists purely so Node resolves these files consistently.

- [ ] **Step 4: Implement `assets/js/bm25.js`**

```javascript
/**
 * BM25 ranking over a small in-memory corpus.
 * Pure logic, no DOM: this file is unit-tested under Node.
 */

const STOPWORDS = new Set([
  'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can',
  'her', 'was', 'one', 'our', 'out', 'his', 'has', 'had', 'were', 'they',
  'this', 'that', 'with', 'from', 'their', 'which', 'when', 'what', 'have',
  'been', 'more', 'than', 'them', 'these', 'those', 'into', 'also', 'such',
  'does', 'how', 'why', 'who', 'its', 'it', 'as', 'at', 'by', 'in', 'of',
  'on', 'or', 'to', 'is', 'be', 'we', 'an', 'a',
]);

export function tokenize(text) {
  return String(text)
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .split(/[^a-z0-9]+/)
    .filter((token) => token.length > 1 && !STOPWORDS.has(token));
}

export function buildIndex(docs) {
  const df = new Map();
  const entries = docs.map((doc) => {
    const tokens = tokenize(doc.text);
    const tf = new Map();
    tokens.forEach((token) => tf.set(token, (tf.get(token) || 0) + 1));
    tf.forEach((_, token) => df.set(token, (df.get(token) || 0) + 1));
    return { id: doc.id, tf, length: tokens.length };
  });

  const total = entries.reduce((sum, entry) => sum + entry.length, 0);
  return {
    entries,
    df,
    N: entries.length,
    avgdl: entries.length ? total / entries.length : 0,
  };
}

export function search(index, query, options = {}) {
  const { k1 = 1.5, b = 0.75, limit = 10 } = options;
  const terms = tokenize(query);
  if (terms.length === 0) return [];

  const results = [];
  index.entries.forEach((entry) => {
    let score = 0;
    terms.forEach((term) => {
      const freq = entry.tf.get(term);
      if (!freq) return;
      const n = index.df.get(term) || 0;
      const idf = Math.log(1 + (index.N - n + 0.5) / (n + 0.5));
      const norm = 1 - b + (b * entry.length) / (index.avgdl || 1);
      score += idf * ((freq * (k1 + 1)) / (freq + k1 * norm));
    });
    if (score > 0) results.push({ id: entry.id, score });
  });

  return results.sort((a, b2) => b2.score - a.score).slice(0, limit);
}
```

- [ ] **Step 5: Run the test to verify it passes**

Run: `node --test tools/test/bm25.test.mjs`
Expected: PASS, 8 tests

- [ ] **Step 6: Emit `search.json` from the build**

Add to `build.py`:

```python
DATA_DIR = "assets/data"


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
```

Call it from `render_site`, just before the return, and append its path to `written`:

```python
    written.append(write_search_index(context, out_dir))
```

- [ ] **Step 7: Add the Python-side test**

Append to `tests/test_render.py`:

```python
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
```

- [ ] **Step 8: Run every test**

Run: `python3 -m pytest tests/ -v && node --test tools/test/*.test.mjs`
Expected: PASS on both

- [ ] **Step 9: Commit**

```bash
git add assets/js/package.json assets/js/bm25.js tools/test/bm25.test.mjs build.py tests/test_render.py assets/data/search.json
git commit -m "feat: add BM25 search index generation and ranking"
```

---

### Task 6: Search interface

**Files:**
- Create: `assets/js/search.js`
- Modify: `assets/css/site.css`

**Interfaces:**
- Consumes: `buildIndex`, `search` from `bm25.js`; `assets/data/search.json`; the `#search-open` button in `base.html.j2`.
- Produces: a global search dialog. Exposes `window.__searchRerank` as the hook Task 9 overrides to add semantic re-ranking.

Tier 1 only. The page must never fetch anything until the visitor opens search.

- [ ] **Step 1: Write `assets/js/search.js`**

```javascript
/**
 * Site search. Tier 1: BM25 over a ~30KB index, fetched on first open.
 * Task 9 upgrades ranking in place by replacing window.__searchRerank.
 */
import { buildIndex, search } from './bm25.js';

const state = { index: null, docs: null, open: false, loading: false };

window.__searchRerank = null;

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(attrs).forEach(([key, value]) => {
    if (key === 'class') node.className = value;
    else if (key === 'text') node.textContent = value;
    else node.setAttribute(key, value);
  });
  children.forEach((child) => node.appendChild(child));
  return node;
}

const dialog = el('div', {
  class: 'search', id: 'search', role: 'dialog',
  'aria-modal': 'true', 'aria-label': 'Search this site', hidden: '',
});
const input = el('input', {
  class: 'search__input', type: 'search', id: 'search-input',
  placeholder: 'Ask a question, or search by keyword…',
  autocomplete: 'off', role: 'combobox', 'aria-expanded': 'false',
  'aria-controls': 'search-results', 'aria-autocomplete': 'list',
});
const results = el('ul', { class: 'search__results', id: 'search-results', role: 'listbox' });
const status = el('p', { class: 'search__status', role: 'status', 'aria-live': 'polite' });
dialog.append(el('div', { class: 'search__panel' }, [input, status, results]));
document.body.appendChild(dialog);

let active = -1;

function render(hits) {
  results.textContent = '';
  active = -1;
  hits.forEach((hit, i) => {
    const doc = state.docs.get(hit.id);
    const link = el('a', { href: 'research.html#' + doc.id });
    link.appendChild(el('span', { class: 'search__title', text: doc.title }));
    link.appendChild(el('span', { class: 'search__meta', text: doc.venue }));
    const item = el('li', { class: 'search__result', role: 'option', id: 'search-opt-' + i, 'aria-selected': 'false' }, [link]);
    results.appendChild(item);
  });
  input.setAttribute('aria-expanded', hits.length ? 'true' : 'false');
  status.textContent = hits.length
    ? hits.length + (hits.length === 1 ? ' result' : ' results')
    : (input.value.trim() ? 'No results' : '');
}

function highlight(next) {
  const items = [...results.children];
  if (!items.length) return;
  if (active >= 0) items[active].setAttribute('aria-selected', 'false');
  active = (next + items.length) % items.length;
  items[active].setAttribute('aria-selected', 'true');
  items[active].scrollIntoView({ block: 'nearest' });
  input.setAttribute('aria-activedescendant', items[active].id);
}

async function ensureIndex() {
  if (state.index || state.loading) return;
  state.loading = true;
  status.textContent = 'Loading…';
  try {
    const response = await fetch('assets/data/search.json');
    const payload = await response.json();
    state.docs = new Map(payload.docs.map((doc) => [doc.id, doc]));
    state.index = buildIndex(payload.docs);
    status.textContent = '';
    if (window.__loadSemantic) window.__loadSemantic();
  } catch (error) {
    status.textContent = 'Search is unavailable.';
  } finally {
    state.loading = false;
  }
}

async function run() {
  if (!state.index) return;
  const query = input.value.trim();
  if (!query) { render([]); return; }
  let hits = search(state.index, query, { limit: 8 });
  if (window.__searchRerank) {
    try {
      hits = await window.__searchRerank(query, hits, state.docs);
    } catch (error) {
      /* Tier 1 results stand. */
    }
  }
  render(hits);
}

function open() {
  state.open = true;
  dialog.hidden = false;
  document.getElementById('search-open').setAttribute('aria-expanded', 'true');
  input.focus();
  ensureIndex();
}

function close() {
  state.open = false;
  dialog.hidden = true;
  const button = document.getElementById('search-open');
  button.setAttribute('aria-expanded', 'false');
  button.focus();
}

document.getElementById('search-open').addEventListener('click', open);
dialog.addEventListener('click', (event) => { if (event.target === dialog) close(); });

let timer;
input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(run, 90); });

input.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowDown') { event.preventDefault(); highlight(active + 1); }
  else if (event.key === 'ArrowUp') { event.preventDefault(); highlight(active - 1); }
  else if (event.key === 'Enter' && active >= 0) {
    event.preventDefault();
    results.children[active].querySelector('a').click();
  } else if (event.key === 'Escape') { close(); }
});

document.addEventListener('keydown', (event) => {
  const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName);
  if (event.key === '/' && !state.open && !typing) { event.preventDefault(); open(); }
  else if (event.key === 'Escape' && state.open) { close(); }
});
```

- [ ] **Step 2: Add the search styles**

Append to `assets/css/site.css`:

```css
.search {
  position: fixed; inset: 0; z-index: 90;
  background: color-mix(in srgb, var(--ink) 55%, transparent);
  display: flex; justify-content: center; padding: 10vh 1rem 1rem;
}
.search[hidden] { display: none; }
.search__panel {
  background: var(--paper); border: 1px solid var(--border);
  width: min(100%, 640px); max-height: 70vh; overflow: auto; padding: 1.25rem;
}
.search__input {
  width: 100%; font-family: var(--body); font-size: var(--step-1);
  padding: 0.65rem 0.5rem; color: var(--ink); background: transparent;
  border: 0; border-bottom: 2px solid var(--bleu-ink);
}
.search__input:focus { outline: none; }
.search__status { color: var(--muted); font-size: var(--step--1); margin: 0.75rem 0 0; }
.search__results { list-style: none; margin: 0.75rem 0 0; padding: 0; }
.search__result a {
  display: block; padding: 0.7rem 0.5rem; text-decoration: none;
  border-bottom: 1px solid var(--border);
}
.search__result[aria-selected="true"] a,
.search__result a:hover { background: var(--grenat-pastel); }
.search__title { display: block; font-family: var(--display); font-weight: 600; color: var(--grenat); }
.search__meta { display: block; font-size: var(--step--1); color: var(--muted); }
```

- [ ] **Step 3: Verify by hand**

Run: `python3 -m http.server 8000` and open `http://localhost:8000`.

Confirm each of these:
- The Network tab shows **no** request for `search.json` on page load.
- Pressing `/` opens search and focuses the input; `search.json` is fetched exactly once.
- Typing `bank run` ranks the SVB paper first.
- Arrow keys move the selection, `Enter` navigates, `Escape` closes and returns focus to the ⌕ button.
- Clicking the backdrop closes the dialog.
- With the network throttled to offline after first load, search still works.

- [ ] **Step 4: Commit**

```bash
git add assets/js/search.js assets/css/site.css
git commit -m "feat: add keyboard-accessible site search"
```

---

### Task 7: Embeddings and PCA

**Files:**
- Create: `tools/package.json`, `tools/pca.mjs`, `tools/embed.mjs`
- Create: `tools/test/pca.test.mjs`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: `assets/data/search.json` from Task 5.
- Produces: `pca2(vectors: number[][]) -> number[][]` (n×2, deterministic); `normalizeCoords(points: number[][]) -> number[][]` scaled into `[-1, 1]`. Writes `assets/data/embeddings.json` as `{"model": string, "dims": number, "vectors": {id: number[]}}` and `assets/data/hero.json` as `{"anchors": [{id, x, y, label, href}]}`.

**This task implements the spec deviation.** Embedding runs in Node using the same transformers.js library and model the browser will use, which makes an embedding-space mismatch structurally impossible.

- [ ] **Step 1: Write the failing PCA test**

Determinism matters more than accuracy here: the output is committed, so a random initialisation would produce a spurious diff on every run.

Create `tools/test/pca.test.mjs`:

```javascript
import test from 'node:test';
import assert from 'node:assert/strict';
import { pca2, normalizeCoords } from '../pca.mjs';

function embed3in6(points) {
  // Lift 2-D points into 6-D by a fixed linear map plus a constant offset.
  return points.map(([x, y]) => [x, y, 0.5 * x, -0.25 * y, 1, 1]);
}

test('pca2 returns one 2-D coordinate per input vector', () => {
  const out = pca2(embed3in6([[0, 0], [1, 0], [0, 1], [1, 1]]));
  assert.equal(out.length, 4);
  out.forEach((point) => assert.equal(point.length, 2));
});

test('pca2 is deterministic across runs', () => {
  const data = embed3in6([[0, 0], [2, 1], [-1, 3], [4, -2], [1, 1]]);
  assert.deepEqual(pca2(data), pca2(data));
});

test('pca2 preserves the relative spread of well-separated clusters', () => {
  const cluster = [[0, 0], [0.1, 0.1], [-0.1, 0], [10, 10], [10.1, 9.9], [9.9, 10]];
  const out = pca2(embed3in6(cluster));
  const within = Math.hypot(out[0][0] - out[1][0], out[0][1] - out[1][1]);
  const between = Math.hypot(out[0][0] - out[3][0], out[0][1] - out[3][1]);
  assert.ok(between > within * 5, `between=${between} within=${within}`);
});

test('normalizeCoords maps everything into [-1, 1]', () => {
  const out = normalizeCoords([[0, 0], [50, -30], [-10, 90]]);
  out.forEach(([x, y]) => {
    assert.ok(x >= -1 && x <= 1, `x=${x}`);
    assert.ok(y >= -1 && y <= 1, `y=${y}`);
  });
});

test('normalizeCoords touches both extremes on the widest axis', () => {
  const out = normalizeCoords([[0, 0], [10, 1], [-10, -1]]);
  const xs = out.map((point) => point[0]);
  assert.ok(Math.abs(Math.min(...xs) + 1) < 1e-9);
  assert.ok(Math.abs(Math.max(...xs) - 1) < 1e-9);
});

test('normalizeCoords survives a degenerate single point', () => {
  const out = normalizeCoords([[5, 5]]);
  assert.equal(out.length, 1);
  assert.ok(Number.isFinite(out[0][0]) && Number.isFinite(out[0][1]));
});
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `node --test tools/test/pca.test.mjs`
Expected: FAIL — cannot find module `../pca.mjs`

- [ ] **Step 3: Implement `tools/pca.mjs`**

```javascript
/**
 * Two-component PCA by power iteration with deflation.
 * Deterministic by construction: the initial vector is a fixed function of
 * the index, never random, because the output is committed to the repository.
 */

function normalise(vector) {
  let norm = 0;
  for (let i = 0; i < vector.length; i += 1) norm += vector[i] * vector[i];
  norm = Math.sqrt(norm) || 1;
  for (let i = 0; i < vector.length; i += 1) vector[i] /= norm;
  return vector;
}

function dot(a, b) {
  let total = 0;
  for (let i = 0; i < a.length; i += 1) total += a[i] * b[i];
  return total;
}

export function pca2(vectors, iterations = 300) {
  const n = vectors.length;
  if (n === 0) return [];
  const d = vectors[0].length;

  const mean = new Float64Array(d);
  vectors.forEach((vector) => {
    for (let i = 0; i < d; i += 1) mean[i] += vector[i];
  });
  for (let i = 0; i < d; i += 1) mean[i] /= n;

  const centred = vectors.map((vector) =>
    Float64Array.from({ length: d }, (_, i) => vector[i] - mean[i]));

  let residual = centred.map((row) => Float64Array.from(row));
  const components = [];

  for (let c = 0; c < 2; c += 1) {
    let w = normalise(Float64Array.from({ length: d }, (_, i) => Math.sin(i + 1 + c * 7)));
    for (let iter = 0; iter < iterations; iter += 1) {
      const next = new Float64Array(d);
      residual.forEach((row) => {
        const projection = dot(row, w);
        for (let i = 0; i < d; i += 1) next[i] += projection * row[i];
      });
      w = normalise(next);
    }
    components.push(w);
    residual = residual.map((row) => {
      const projection = dot(row, w);
      return Float64Array.from({ length: d }, (_, i) => row[i] - projection * w[i]);
    });
  }

  return centred.map((row) => components.map((w) => dot(row, w)));
}

export function normalizeCoords(points) {
  if (points.length === 0) return [];
  const xs = points.map((p) => p[0]);
  const ys = points.map((p) => p[1]);
  const spread = Math.max(
    Math.max(...xs) - Math.min(...xs),
    Math.max(...ys) - Math.min(...ys),
  ) || 1;
  const cx = (Math.max(...xs) + Math.min(...xs)) / 2;
  const cy = (Math.max(...ys) + Math.min(...ys)) / 2;
  return points.map(([x, y]) => [
    (2 * (x - cx)) / spread,
    (2 * (y - cy)) / spread,
  ]);
}
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `node --test tools/test/pca.test.mjs`
Expected: PASS, 6 tests

- [ ] **Step 5: Set up `tools/package.json` and ignore `node_modules`**

```json
{
  "name": "jfimbett-tools",
  "private": true,
  "type": "module",
  "scripts": {
    "embed": "node embed.mjs",
    "test": "node --test test/*.test.mjs"
  },
  "dependencies": {
    "@huggingface/transformers": "^3.0.0"
  }
}
```

Append to `.gitignore`:

```
# Build-time embedding tool
tools/node_modules/
```

Run: `cd tools && npm install`
Expected: completes; `tools/node_modules/` exists and is ignored by git.

If `@huggingface/transformers` fails to install or the model cannot be fetched, **stop and report**. Do not fall back to a hand-rolled embedding — a wrong vector space produces plausible, silently incorrect search results.

- [ ] **Step 6: Implement `tools/embed.mjs`**

```javascript
/**
 * Precompute paper embeddings and the hero's 2-D layout.
 *
 * Run from tools/:  npm run embed
 *
 * MODEL_ID is the single source of truth for which model is used. The browser
 * loads the same identifier in assets/js/semantic.js. If these two ever
 * diverge, similarity scores become meaningless without any visible error, so
 * changing one means changing the other.
 */
import { readFile, writeFile } from 'node:fs/promises';
import { pipeline } from '@huggingface/transformers';
import { pca2, normalizeCoords } from './pca.mjs';

export const MODEL_ID = 'Xenova/all-MiniLM-L6-v2';

const DATA = new URL('../assets/data/', import.meta.url);

const round = (value) => Math.round(value * 10000) / 10000;

async function main() {
  const payload = JSON.parse(await readFile(new URL('search.json', DATA), 'utf8'));
  const docs = payload.docs;
  console.log(`Embedding ${docs.length} papers with ${MODEL_ID}…`);

  const extractor = await pipeline('feature-extraction', MODEL_ID);

  const vectors = [];
  for (const doc of docs) {
    const output = await extractor(doc.text, { pooling: 'mean', normalize: true });
    vectors.push(Array.from(output.data));
    console.log(`  ${doc.id}`);
  }

  const embeddings = {
    model: MODEL_ID,
    dims: vectors[0].length,
    vectors: Object.fromEntries(
      docs.map((doc, i) => [doc.id, vectors[i].map(round)]),
    ),
  };
  await writeFile(
    new URL('embeddings.json', DATA),
    JSON.stringify(embeddings, null, 1),
    'utf8',
  );

  const coords = normalizeCoords(pca2(vectors));
  const hero = {
    model: MODEL_ID,
    anchors: docs.map((doc, i) => ({
      id: doc.id,
      x: round(coords[i][0]),
      y: round(coords[i][1]),
      label: doc.title,
      href: `research.html#${doc.id}`,
    })),
  };
  await writeFile(new URL('hero.json', DATA), JSON.stringify(hero, null, 1), 'utf8');

  console.log(`Wrote embeddings.json (${embeddings.dims} dims) and hero.json`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```

- [ ] **Step 7: Generate the data**

Run: `cd tools && npm run embed`
Expected: nine lines of paper ids, then the summary. `assets/data/embeddings.json` and `assets/data/hero.json` exist.

Sanity-check that the layout separates the two research agendas:

```bash
python3 -c "
import json
data = json.load(open('assets/data/hero.json'))
for a in data['anchors']:
    print('%7.3f %7.3f  %s' % (a['x'], a['y'], a['id']))
"
```

The three social-media papers should sit closer to each other than to the offshore/tax papers. If the layout looks arbitrary, note it — Section 12 of the spec permits hand-adjusting `hero.json`.

- [ ] **Step 8: Warn on stale embeddings**

Add to `build.py`, and call it from `main()` after a successful render:

```python
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
```

- [ ] **Step 9: Run every test**

Run: `python3 -m pytest tests/ -v && node --test tools/test/*.test.mjs`
Expected: PASS on both

- [ ] **Step 10: Commit**

```bash
git add tools/ .gitignore build.py assets/data/embeddings.json assets/data/hero.json
git commit -m "feat: precompute paper embeddings and hero layout"
```

---

### Task 8: The generative hero

**Files:**
- Create: `assets/js/hero.js`
- Modify: `templates/index.html.j2`

**Interfaces:**
- Consumes: `assets/data/hero.json` from Task 7; `#hero-canvas` and `#hero-label` from `index.html.j2`.
- Produces: a self-starting canvas animation. No exports.

- [ ] **Step 1: Implement `assets/js/hero.js`**

```javascript
/**
 * Hero: a curl-noise particle field whose anchor points are this site's
 * papers, positioned by PCA over their embeddings (assets/data/hero.json).
 *
 * The field periodically relaxes so drifting particles settle toward the
 * anchors, then resumes drifting.
 */

const canvas = document.getElementById('hero-canvas');
const label = document.getElementById('hero-label');

const GRENAT = [95, 25, 55];
const CORAL = [255, 110, 110];

function mix(a, b, t) {
  return `rgb(${Math.round(a[0] + (b[0] - a[0]) * t)},` +
         `${Math.round(a[1] + (b[1] - a[1]) * t)},` +
         `${Math.round(a[2] + (b[2] - a[2]) * t)})`;
}

/** Cheap, seeded value noise. No dependency, and stable across reloads. */
function noise(x, y, t) {
  return (
    Math.sin(x * 1.7 + t) * Math.cos(y * 1.3 - t * 0.7) +
    Math.sin((x + y) * 0.9 + t * 1.3) * 0.5
  );
}

async function start(target) {
  const context = target.getContext('2d', { alpha: false });
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  let anchors = [];
  try {
    const response = await fetch('assets/data/hero.json');
    anchors = (await response.json()).anchors || [];
  } catch (error) {
    anchors = []; // The field still renders; it simply has no anchors.
  }

  let width = 0;
  let height = 0;
  let particles = [];

  function resize() {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    const rect = target.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    target.width = Math.round(width * ratio);
    target.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);

    const count = Math.min(2600, Math.round((width * height) / 260));
    particles = Array.from({ length: count }, (_, i) => ({
      // Deterministic placement: a golden-angle spiral, not Math.random,
      // so the first painted frame is identical on every load.
      x: (0.5 + 0.45 * Math.cos(i * 2.39996) * Math.sqrt(i / count)) * width,
      y: (0.5 + 0.45 * Math.sin(i * 2.39996) * Math.sqrt(i / count)) * height,
      vx: 0,
      vy: 0,
    }));
  }

  const toScreen = (anchor) => ({
    x: (anchor.x * 0.42 + 0.5) * width,
    y: (anchor.y * 0.42 + 0.5) * height,
  });

  const styles = getComputedStyle(document.documentElement);
  const background = styles.getPropertyValue('--grenat-pastel').trim() || '#ECE4E7';

  function frame(time) {
    const t = time * 0.00012;
    // Cycles between drifting (0) and gathering toward anchors (1).
    const gather = Math.max(0, Math.sin(t * 0.6)) ** 3;

    context.fillStyle = background;
    context.fillRect(0, 0, width, height);

    const screenAnchors = anchors.map(toScreen);

    particles.forEach((particle) => {
      const nx = particle.x / width;
      const ny = particle.y / height;
      let ax = noise(nx * 3, ny * 3, t) * 0.06;
      let ay = noise(ny * 3 + 5.2, nx * 3 - 2.1, t) * 0.06;

      if (gather > 0.01 && screenAnchors.length) {
        let best = screenAnchors[0];
        let bestDistance = Infinity;
        screenAnchors.forEach((anchor) => {
          const distance = (anchor.x - particle.x) ** 2 + (anchor.y - particle.y) ** 2;
          if (distance < bestDistance) { bestDistance = distance; best = anchor; }
        });
        ax += ((best.x - particle.x) / width) * gather * 0.9;
        ay += ((best.y - particle.y) / height) * gather * 0.9;
      }

      particle.vx = (particle.vx + ax) * 0.94;
      particle.vy = (particle.vy + ay) * 0.94;
      particle.x += particle.vx;
      particle.y += particle.vy;

      if (particle.x < 0) particle.x += width;
      if (particle.x > width) particle.x -= width;
      if (particle.y < 0) particle.y += height;
      if (particle.y > height) particle.y -= height;

      const speed = Math.min(1, Math.hypot(particle.vx, particle.vy) * 6);
      context.fillStyle = mix(GRENAT, CORAL, speed);
      context.globalAlpha = 0.35 + speed * 0.45;
      context.fillRect(particle.x, particle.y, 1.4, 1.4);
    });

    context.globalAlpha = 1;
    screenAnchors.forEach((anchor) => {
      context.beginPath();
      context.arc(anchor.x, anchor.y, 4.5, 0, Math.PI * 2);
      context.fillStyle = mix(GRENAT, CORAL, 0.25);
      context.fill();
    });
  }

  let running = false;
  let handle = 0;

  function loop(time) {
    frame(time);
    handle = requestAnimationFrame(loop);
  }

  function play() {
    if (running || reduced) return;
    running = true;
    handle = requestAnimationFrame(loop);
  }

  function pause() {
    running = false;
    cancelAnimationFrame(handle);
  }

  resize();
  frame(0);

  if (!reduced) {
    window.addEventListener('resize', () => { resize(); });
    new IntersectionObserver((entries) => {
      entries[0].isIntersecting ? play() : pause();
    }).observe(target);
    document.addEventListener('visibilitychange', () => {
      document.hidden ? pause() : play();
    });
  }

  // Anchor hover and click.
  target.addEventListener('mousemove', (event) => {
    const rect = target.getBoundingClientRect();
    const mx = event.clientX - rect.left;
    const my = event.clientY - rect.top;
    const hit = anchors.find((anchor) => {
      const point = toScreen(anchor);
      return Math.hypot(point.x - mx, point.y - my) < 14;
    });
    if (hit) {
      label.textContent = hit.label;
      label.style.left = `${mx + 12}px`;
      label.style.top = `${my - 8}px`;
      label.dataset.visible = 'true';
      target.style.cursor = 'pointer';
    } else {
      label.dataset.visible = 'false';
      target.style.cursor = 'default';
    }
  });

  target.addEventListener('click', (event) => {
    const rect = target.getBoundingClientRect();
    const mx = event.clientX - rect.left;
    const my = event.clientY - rect.top;
    const hit = anchors.find((anchor) => {
      const point = toScreen(anchor);
      return Math.hypot(point.x - mx, point.y - my) < 14;
    });
    if (hit) window.location.href = hit.href;
  });
}

// Kick off last: start() closes over GRENAT and CORAL, which are in the
// temporal dead zone until this point in the module.
if (canvas && canvas.getContext) {
  start(canvas);
}
```

- [ ] **Step 2: Give the hero a text equivalent**

The canvas must not be the only place the anchor titles exist. In `templates/index.html.j2`, add inside `<figure class="hero__figure">`, after the label div:

```jinja
<figcaption class="visually-hidden">
  Papers shown in the field:
  <ul>{% for paper in papers %}<li><a href="research.html#{{ paper.id }}">{{ paper.title }}</a></li>{% endfor %}</ul>
</figcaption>
```

- [ ] **Step 3: Verify by hand**

Run: `python3 build.py && python3 -m http.server 8000`

Confirm each of these:
- The field animates smoothly and periodically gathers toward nine brighter points.
- Hovering a bright point shows the paper title; clicking navigates to it on the research page.
- Under macOS System Settings → Accessibility → Display → Reduce motion, exactly one static frame renders and the CPU stays idle.
- Scrolling the hero out of view stops the animation (verify in the browser's performance profiler).
- Switching to another tab stops it.
- Renaming `assets/data/hero.json` temporarily leaves the field running with no anchors and no console error.
- The canvas resizes cleanly between 360px and 1920px viewport widths.

- [ ] **Step 4: Commit**

```bash
git add assets/js/hero.js templates/index.html.j2 index.html
git commit -m "feat: add embedding-space generative hero"
```

---

### Task 9: Semantic re-ranking

**Files:**
- Create: `assets/js/semantic.js`
- Modify: `templates/base.html.j2`

**Interfaces:**
- Consumes: `window.__searchRerank` and `window.__loadSemantic` hooks from Task 6; `assets/data/embeddings.json` from Task 7; `MODEL_ID` must equal the value in `tools/embed.mjs`.
- Produces: nothing exported. Replaces `window.__searchRerank` once the model is ready.

Purely additive. If anything in this task fails, Tier 1 keyword search continues to work and the visitor sees no error.

- [ ] **Step 1: Implement `assets/js/semantic.js`**

```javascript
/**
 * Tier 2 search: re-rank BM25 hits by embedding similarity.
 *
 * MODEL_ID must match tools/embed.mjs exactly. Document vectors were computed
 * there with the same library; a mismatch yields meaningless scores with no
 * visible error, so this constant is not to be changed on one side alone.
 */
const MODEL_ID = 'Xenova/all-MiniLM-L6-v2';
const LIBRARY = 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0';

let ready = null;

function cosine(a, b) {
  let dot = 0;
  let na = 0;
  let nb = 0;
  for (let i = 0; i < a.length; i += 1) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  return dot / (Math.sqrt(na) * Math.sqrt(nb) || 1);
}

async function load() {
  const [{ pipeline }, response] = await Promise.all([
    import(/* webpackIgnore: true */ LIBRARY),
    fetch('assets/data/embeddings.json'),
  ]);
  const store = await response.json();

  if (store.model !== MODEL_ID) {
    throw new Error(
      `embeddings.json was built with ${store.model} but this page expects ${MODEL_ID}`,
    );
  }

  const extractor = await pipeline('feature-extraction', MODEL_ID);
  return { extractor, vectors: store.vectors };
}

window.__loadSemantic = () => {
  if (ready) return;
  ready = load().then(({ extractor, vectors }) => {
    window.__searchRerank = async (query, hits, docs) => {
      const output = await extractor(query, { pooling: 'mean', normalize: true });
      const queryVector = Array.from(output.data);

      // Score every document, not only the BM25 hits: the whole point is to
      // surface papers that share no vocabulary with the query.
      const scored = Object.entries(vectors)
        .map(([id, vector]) => ({ id, score: cosine(queryVector, vector) }))
        .filter((hit) => docs.has(hit.id) && hit.score > 0.15)
        .sort((a, b) => b.score - a.score)
        .slice(0, 8);

      return scored.length ? scored : hits;
    };
  }).catch(() => {
    // Tier 1 stands. Deliberately silent: the visitor has working search.
    ready = null;
  });
};
```

- [ ] **Step 2: Load it from the base template**

In `templates/base.html.j2`, after the `search.js` script tag:

```html
<script type="module" src="{{ prefix | default('') }}assets/js/semantic.js"></script>
```

`semantic.js` only defines `window.__loadSemantic`; nothing is fetched until `search.js` calls it, which happens on first search open.

- [ ] **Step 3: Verify both tiers by hand**

Run: `python3 build.py && python3 -m http.server 8000`

Tier 1 in isolation — in DevTools, block the request pattern `cdn.jsdelivr.net/*`, then:
- Open search, type `bank run`. Results appear immediately, SVB paper first.
- No error is shown to the visitor.

Tier 2 — unblock, hard-reload, then:
- On page load, confirm **no** request to jsdelivr or for `embeddings.json`.
- Open search; both begin loading.
- Once loaded, type `how does Twitter affect banks`. **The SVB paper must rank first** despite the query sharing no distinctive terms with the indexed text. This is the acceptance criterion for the whole feature; if it fails, verify `store.model` matches and that `embed.mjs` used `pooling: 'mean', normalize: true`.
- Type `tax havens` and confirm the offshore papers rank first.

- [ ] **Step 4: Commit**

```bash
git add assets/js/semantic.js templates/base.html.j2 index.html research.html cv.html
git commit -m "feat: upgrade search with client-side semantic re-ranking"
```

---

### Task 10: Archive the legacy material

**Files:**
- Move: `teaching/`, `courses/`, `talks/` → `archive/`
- Create: seven meta-refresh stubs under `teaching/`
- Create: `archive/index.html`
- Create: `tests/test_archive.py`

**Interfaces:**
- Consumes: nothing.
- Produces: the `archive/` tree and redirect stubs. No build integration; these files are static and hand-written.

Do not touch `wedding/`, `blog/`, `code.html`, or `scripts/`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_archive.py`:

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tests/test_archive.py -v`
Expected: FAIL — `archive/teaching missing`

- [ ] **Step 3: Move the directories**

```bash
mkdir -p archive
git mv teaching archive/teaching
git mv courses archive/courses
git mv talks archive/talks
```

`git mv` preserves history. Verify with `git log --follow archive/teaching/index.html`.

- [ ] **Step 4: Generate the redirect stubs**

```bash
python3 - <<'EOF'
from pathlib import Path

STUBS = [
    "teaching/index.html",
    "teaching/python-conda-course.html",
    "teaching/empirical_asset_pricing/index.html",
    "teaching/investment_funds_risks/index.html",
    "teaching/python_m1/index.html",
    "teaching/python_m2/index.html",
    "teaching/python_m2_203/index.html",
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=/{target}">
<link rel="canonical" href="https://jfimbett.github.io/{target}">
<title>Moved</title>
</head>
<body>
<p>This course material has been archived. If you are not redirected,
<a href="/{target}">open it here</a>.</p>
</body>
</html>
"""

for stub in STUBS:
    target = "archive/" + stub
    assert Path(target).exists(), "missing archive target: " + target
    path = Path(stub)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE.format(target=target), encoding="utf-8")
    print("stub", stub, "->", target)
EOF
```

- [ ] **Step 5: Add an archive landing page**

Create `archive/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<title>Archive</title>
<link rel="stylesheet" href="../assets/css/site.css">
</head>
<body>
<main class="wrap section">
  <p class="eyebrow">Archive</p>
  <h1>Archived material</h1>
  <p>Teaching material and conference slides from 2018–2026, kept online so
  existing links keep working. Not maintained, and not linked from the main
  site. See <a href="../index.html">the current site</a>.</p>
</main>
</body>
</html>
```

- [ ] **Step 6: Run the test to verify it passes**

Run: `python3 -m pytest tests/test_archive.py -v`
Expected: PASS

- [ ] **Step 7: Check the redirects in a browser**

Run: `python3 -m http.server 8000`, then visit `http://localhost:8000/teaching/` and each of the other six stub paths. Each must land on the archived page.

- [ ] **Step 8: Commit**

```bash
git add -A archive teaching tests/test_archive.py
git commit -m "refactor: archive legacy teaching, course, and talk material"
```

---

### Task 11: Structured data, sitemap, and cleanup

**Files:**
- Modify: `templates/research.html.j2`, `templates/base.html.j2`, `build.py`
- Create: `robots.txt`
- Delete: `assets/css/custom.css`, `assets/js/main.js`, `MAINTENANCE_GUIDE.md`, `scripts/build.py`, `blog.html`
- Rewrite: `README.md`
- Create: `tests/test_seo.py`

**Interfaces:**
- Consumes: `build_context`, `render_site` from Task 4.
- Produces: `write_sitemap(context: dict, out_dir: Path) -> Path`; a `scholarly_article(paper, site) -> dict` Jinja global for JSON-LD.

Note `blog.html` is deleted but the `blog/` **directory** is kept: `blog.html` is the index that linked the drafts from the old nav, and nothing else references it.

- [ ] **Step 1: Write the failing test**

Create `tests/test_seo.py`:

```python
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


def test_every_page_has_a_canonical_and_description(rendered):
    for name in ("index.html", "research.html", "cv.html"):
        markup = (rendered / name).read_text(encoding="utf-8")
        assert 'rel="canonical"' in markup
        assert 'name="description"' in markup


def test_sitemap_lists_pages_and_excludes_the_archive(rendered):
    sitemap = (rendered / "sitemap.xml").read_text(encoding="utf-8")
    for name in ("index.html", "research.html", "cv.html"):
        assert name in sitemap or name == "index.html"
    assert "archive" not in sitemap
    assert "wedding" not in sitemap


def test_no_dead_assets_referenced(rendered):
    for name in ("index.html", "research.html", "cv.html"):
        markup = (rendered / name).read_text(encoding="utf-8")
        assert "custom.css" not in markup
        assert "js/main.js" not in markup
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tests/test_seo.py -v`
Expected: FAIL — no `Person` JSON-LD or no `sitemap.xml`

- [ ] **Step 3: Add `scholarly_article` and `write_sitemap` to `build.py`**

```python
SITE_URL = "https://jfimbett.github.io/"


def scholarly_article(paper, site):
    """Schema.org ScholarlyArticle for one paper."""
    authors = [
        site["name"] if name == SELF else name for name in paper.get("authors", [])
    ]
    node = {
        "@type": "ScholarlyArticle",
        "name": paper["title"],
        "author": [{"@type": "Person", "name": name} for name in authors],
        "url": SITE_URL + "research.html#" + paper["id"],
    }
    if paper.get("year"):
        node["datePublished"] = str(paper["year"])
    if paper.get("venue"):
        node["publication"] = paper["venue"]
    if paper.get("abstract"):
        node["abstract"] = paper["abstract"].strip()
    same_as = [paper.get(key) for key in ("doi", "ssrn", "url")]
    same_as = [value for value in same_as if value]
    if same_as:
        node["sameAs"] = same_as
    return node


def write_sitemap(context, out_dir):
    """List the public pages. The archive and wedding site are excluded."""
    pages = ["", "research.html", "cv.html"]
    if context["has_teaching"]:
        pages.append("teaching.html")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page in pages:
        lines.append("  <url><loc>{}{}</loc></url>".format(SITE_URL, page))
    lines.append("</urlset>")
    lines.append("")

    path = Path(out_dir) / "sitemap.xml"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
```

Register the helper as a Jinja global inside `_environment()`:

```python
    env.globals["scholarly_article"] = scholarly_article
```

And in `render_site`, alongside the search index:

```python
    written.append(write_sitemap(context, out_dir))
```

- [ ] **Step 4: Replace the placeholder JSON-LD on the research page**

In `templates/research.html.j2`, replace the whole `{% block head %}` with:

```jinja
{% block head %}
<script type="application/ld+json">
{{ {"@context": "https://schema.org",
    "@graph": grouped.published | map('scholarly_article_for', site) | list} | tojson }}
</script>
{% endblock %}
```

Jinja filters take the value first, so register a filter wrapper rather than reusing the global directly. Add to `_environment()`:

```python
    env.filters["scholarly_article_for"] = scholarly_article
```

- [ ] **Step 5: Write `robots.txt`**

```
User-agent: *
Allow: /
Disallow: /archive/
Disallow: /wedding/

Sitemap: https://jfimbett.github.io/sitemap.xml
```

- [ ] **Step 6: Delete the superseded files**

```bash
git rm assets/css/custom.css assets/js/main.js MAINTENANCE_GUIDE.md scripts/build.py blog.html
```

`assets/js/main.js` existed only to drive Bootstrap collapse toggles, now replaced by native `<details>`. `scripts/build.py` invokes a `fetch_ssrn_data.py` that no longer exists.

Confirm nothing still references them:

```bash
! grep -rn "custom.css\|js/main.js\|blog.html" --include="*.html" --include="*.j2" . | grep -v archive/ | grep -v wedding/
```

Expected: exit status 0.

- [ ] **Step 7: Rewrite `README.md`**

```markdown
# jfimbett.github.io

Academic site for Juan Felipe Imbet. Static HTML generated from YAML and
served by GitHub Pages.

## Adding a paper

1. Add an entry to `content/papers.yml`:

   ```yaml
   - id: my-new-paper
     title: The Title
     authors: [Coauthor Name, SELF]
     status: working          # published | working | wip
     year: 2026
     ssrn: https://papers.ssrn.com/...
     topics: [asset pricing]
     abstract: |
       ...
     summary: |
       One plain-language paragraph.
   ```

   `SELF` renders as your name in bold. Published papers also need `venue`
   and `year`.

2. Rebuild and refresh the search index:

   ```bash
   python3 build.py
   cd tools && npm run embed && cd ..
   ```

3. Commit everything, including the regenerated HTML and JSON.

## Adding a course

Add an entry to `content/courses.yml` and rebuild. The Teaching page and its
nav link appear automatically; while the file is an empty list, neither
exists.

## Commands

| Command | Purpose |
|---|---|
| `python3 build.py` | Regenerate the site. Run after any content change. |
| `cd tools && npm run embed` | Recompute embeddings. Run after adding or editing a paper. |
| `python3 -m pytest tests/` | Python tests. |
| `node --test tools/test/*.test.mjs` | JavaScript tests. |
| `python3 -m http.server 8000` | Preview locally. |

`build.py` warns when `papers.yml` is newer than the embeddings.

## Layout

```
content/      YAML source — the only files you normally edit
templates/    Jinja2 templates
build.py      Renders templates to HTML
tools/        Embedding and PCA tooling (Node)
assets/       CSS, JS, images, generated JSON
archive/      Old teaching material and talks; unlinked, kept for old URLs
*.html        Generated. Do not edit by hand.
```

## Design

Colour and type follow EDHEC's brand: grenat `#5F1937`, Montserrat and
Open Sans. Tokens are defined once at the top of `assets/css/site.css`.

The full design rationale is in
`docs/superpowers/specs/2026-08-20-website-redesign-design.md`.
```

- [ ] **Step 8: Run every test**

Run: `python3 build.py && python3 -m pytest tests/ -v && node --test tools/test/*.test.mjs`
Expected: PASS on all

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "feat: add structured data and sitemap; remove superseded files"
```

---

### Task 12: Final verification

**Files:**
- Create: `tests/test_links.py`
- Modify: none unless a check fails

**Interfaces:**
- Consumes: everything.
- Produces: a recorded verification result for each item in spec Section 11.

No claim of completion may be made until every command below has been run and its output observed. Record actual numbers, not impressions.

- [ ] **Step 1: Add the link integrity test**

Create `tests/test_links.py`:

```python
"""Every internal link and anchor must resolve."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
PAGES = ["index.html", "research.html", "cv.html"]

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
```

Run: `python3 -m pytest tests/test_links.py -v`
Expected: PASS. Fix any broken reference before continuing.

- [ ] **Step 2: Run the full test suite**

```bash
python3 build.py && python3 -m pytest tests/ -v && node --test tools/test/*.test.mjs
```

Record the counts. Expected: all pass.

- [ ] **Step 3: Verify the build fails correctly on bad content**

Fault injection, one at a time, restoring `content/papers.yml` after each:

```bash
cp content/papers.yml /tmp/papers.bak

# 1. duplicate id
python3 - <<'EOF'
import shutil
text = open("content/papers.yml").read()
open("content/papers.yml", "a").write("\n- id: social-media-bank-run\n  title: Dup\n  authors: [SELF]\n  status: wip\n")
EOF
python3 build.py; echo "exit=$?"   # expect exit=1 and "duplicate id"

cp /tmp/papers.bak content/papers.yml

# 2. unknown status
sed -i '' '0,/status: working/s//status: draft/' content/papers.yml
python3 build.py; echo "exit=$?"   # expect exit=1 and "unknown status 'draft'"

cp /tmp/papers.bak content/papers.yml
python3 build.py; echo "exit=$?"   # expect exit=0
```

Confirm each failing run wrote **no** output: `git status --porcelain` must show no modified HTML after a failed build.

- [ ] **Step 4: Verify the teaching toggle end to end**

```bash
cat > content/courses.yml <<'EOF'
- id: llm-finance
  title: Large Language Models in Finance
  institution: Barcelona School of Economics
  level: Summer School
  years: [2025, 2026]
  url: https://jfimbett.github.io/llm-finance-book
  description: Building and evaluating LLM pipelines on financial text.
EOF
python3 build.py
grep -c "teaching.html" index.html    # expect >= 1
test -f teaching.html && echo "teaching page created"

echo "[]" > content/courses.yml
python3 build.py
grep -c "teaching.html" index.html    # expect 0
test ! -f teaching.html && echo "teaching page removed"
```

Then restore the commented template form of `content/courses.yml` from Task 2.

- [ ] **Step 5: Validate the HTML**

```bash
npx --yes html-validate index.html research.html cv.html
```

Expected: zero errors. If `html-validate` is unavailable offline, use the W3C validator at https://validator.w3.org/nu/ by uploading each file, and record the result.

- [ ] **Step 6: Run the accessibility audit**

```bash
npx --yes @axe-core/cli http://localhost:8000/ http://localhost:8000/research.html http://localhost:8000/cv.html
```

(with `python3 -m http.server 8000` running.)

Expected: zero violations. Record the actual count. Any violation must be fixed, not waived.

- [ ] **Step 7: Run Lighthouse**

```bash
npx --yes lighthouse http://localhost:8000/ --only-categories=performance,accessibility,best-practices,seo --output=json --output-path=/tmp/lh.json --chrome-flags="--headless"
python3 -c "
import json
report = json.load(open('/tmp/lh.json'))
for key, category in report['categories'].items():
    print('%-16s %d' % (key, round(category['score'] * 100)))
"
```

Record the four scores. Target 100 on each; anything below 95 must be explained in the completion report, not silently accepted.

- [ ] **Step 8: Check the transfer budget**

In DevTools, hard-reload the home page with the cache disabled. Record the transferred bytes before the hero canvas initialises. Target: under 50KB excluding fonts and the portrait.

- [ ] **Step 9: Responsive check**

View `index.html`, `research.html` and `cv.html` at 360, 768, 1280 and 1920 pixels wide. Confirm at every width: no horizontal scrolling, the entry number never collides with the title, the nav stays usable, and the hero canvas keeps its aspect ratio.

- [ ] **Step 10: Verify both colour schemes**

Toggle macOS between light and dark appearance. Confirm on all pages: text is legible, the coral and blue accents remain visible, the hero background matches the page, and no element disappears into its background.

- [ ] **Step 11: Confirm nothing protected was touched**

```bash
git diff --stat master -- wedding/ blog/ code.html scripts/
```

Expected: `scripts/build.py` deleted (Task 11), and **no other changes** under those paths.

- [ ] **Step 12: Final commit**

```bash
python3 build.py
git add -A
git commit -m "test: add link integrity checks and complete verification pass"
```

- [ ] **Step 13: Write the completion report**

Report, with actual observed values:

- Test counts: pytest passed/failed, node passed/failed
- Lighthouse: four scores
- axe-core: violation count per page
- HTML validation: error count
- Transfer size before hero init
- Semantic search: whether `how does Twitter affect banks` ranked the SVB paper first
- Anything deferred or failing, stated plainly

Do not claim completion for any item not actually run.

---

## Post-implementation follow-ups

Not in scope, but worth recording:

- `content/papers.yml` `summary` fields are drafted for the site owner to edit; they are the author's voice and should be reviewed before the site is publicised.
- The SSRN author page URL is still unknown; `site.profiles.ssrn` is an empty string and renders nothing until filled in.
- `scripts/` holds 22MB of unrelated research code that is neither linked nor served. Cleaning it up is a separate decision.
- The `blog/` drafts remain unlinked. Turning them into a Writing page is a separate piece of work.
