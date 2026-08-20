# Website Redesign — Design Document

**Date:** 2026-08-20
**Repository:** `jfimbett/jfimbett.github.io`
**Status:** Approved for implementation

## 1. Purpose

Replace the current Bootstrap-based academic site with a professionally
designed, EDHEC-branded static site that reflects the owner's public
identity as a finance researcher working with AI.

The current site works but reads as a template: CDN Bootstrap, generic cards,
collapsed abstracts behind toggle buttons, placeholder social links, a
Dauphine affiliation that is now historical, and no visual signal of the
computational side of the research.

### Goals

1. Look designed, not templated — at the standard of a research institution's
   own site.
2. Carry EDHEC's real brand identity (verified against their live theme CSS).
3. Present the AI dimension of the work through something functional, not
   decorative.
4. Make adding a paper a six-line YAML edit rather than an HTML copy-paste.
5. Hide legacy teaching material without destroying it or breaking inbound links.

### Non-goals

- No CMS, no server, no database, no authentication.
- No blog rewrite. Existing drafts stay where they are, unlinked.
- No changes to `wedding/`.
- No redesign of the externally-hosted course repositories.

## 2. Constraints

**GitHub Pages serves static files only.** No server-side rendering, no
runtime secrets, no API keys reachable from the page. Every dynamic feature
must run either at build time (on the author's machine) or client-side in
the visitor's browser.

**Committed output.** The repository contains both the YAML source and the
generated HTML. GitHub Pages serves the committed HTML directly; no GitHub
Action is involved in deployment. A broken build therefore cannot take the
live site down.

**No third-party runtime dependencies on the critical path.** Bootstrap and
Font Awesome are removed. Google Fonts is the only external stylesheet, and
every font has a system fallback stack.

## 3. Decisions taken

These were settled with the site owner before design and are not open
questions:

| Decision | Choice |
|---|---|
| Build | Python + Jinja2, output committed to the repo |
| Visual direction | Editorial and confident; grenat, generous whitespace, asymmetric grid |
| Affiliation | EDHEC Business School as current; Dauphine appears only in history |
| Email | `juan.imbet@edhec.edu` |
| AI features | Generative hero + semantic search + plain-language summaries. No separate "AI" nav section. |
| Teaching | Page and nav item suppressed while empty; trivially re-enabled later |
| Legacy content | `teaching/`, `courses/`, `talks/` moved to `archive/`, unlinked |
| Photo | Existing 369x560 image, used at native size |
| Office address | Omitted (not yet known) |

## 4. Brand and visual system

### 4.1 Provenance

The palette and type pairing were extracted from EDHEC's live theme at
`https://www.edhec.edu/themes/custom/edhec/css/variables.css` and
`.../typo.css`. These are EDHEC's actual production tokens, not an
approximation.

### 4.2 Color tokens

Light theme:

| Token | Value | Role |
|---|---|---|
| `--grenat` | `#5F1937` | Headings, rules, brand marks |
| `--ink` | `#0E0E0E` | Body text |
| `--paper` | `#FFFFFF` | Page canvas |
| `--grenat-pastel` | `#ECE4E7` | Tinted section bands |
| `--coral` | `#FF6E6E` | Single bright accent: active nav, hover, hero rule |
| `--bleu` | `#00B9FF` | Reserved exclusively for search UI |
| `--border` | `#DCDCDC` | Hairline rules |
| `--muted` | `#5A5A5A` | Secondary metadata text |

Dark theme redefines the same tokens. `--grenat` at `#5F1937` fails contrast
on a dark canvas, so it lifts to `#D4849F`; `--paper` becomes `#0E0E0E` and
`--ink` becomes `#F2ECEE`. `--coral` and `--bleu` are already legible on dark
and carry through unchanged.

Every foreground/background pair used in the design must meet WCAG AA
(4.5:1 for body text, 3:1 for large text and UI boundaries). This is verified
as part of implementation, not assumed.

Theme selection follows `prefers-color-scheme` with no manual toggle. A toggle
adds state, a control, and persistence for a preference the operating system
already expresses.

### 4.3 Typography

Montserrat (600, 700) for display and UI; Open Sans (400, 600) for body — the
exact pairing EDHEC uses. Loaded from Google Fonts with `display=swap` and a
full system fallback stack so text renders immediately.

A fluid type scale built on `clamp()`, ranging from a hero display size down
to small metadata. Body copy at a comfortable measure (65–75 characters) and
generous line height (1.65).

### 4.4 Layout

Content max-width 1200px. An asymmetric two-column grid: a narrow left gutter
carrying an index number, and a wide content column.

The **numbered index** is the recurring editorial motif. Papers, courses, and
CV entries are numbered `01`, `02`, `03` … in grenat Montserrat in the gutter,
with content offset to the right. On narrow viewports the gutter collapses and
the number sits inline above the title.

No cards, no drop shadows, no rounded rectangles. Structure comes from
hairline rules, type hierarchy, and whitespace. Abstracts use a native
`<details>` element rather than JavaScript toggles.

## 5. The generative hero

### 5.1 Concept

A canvas particle field in which the anchor points are the site owner's actual
papers positioned in embedding space. It is a map of the research, animated —
not a generic particle effect.

### 5.2 Data

`embed.py` (Section 7.3) computes a sentence embedding per paper, reduces the
set to two dimensions, normalises the coordinates to `[-1, 1]`, and writes
`assets/data/hero.json`:

```json
{
  "anchors": [
    {"id": "social-media-bank-run", "x": -0.42, "y": 0.31,
     "label": "Social Media as a Bank Run Catalyst", "href": "research.html#social-media-bank-run"}
  ]
}
```

With nine papers, PCA is the appropriate reduction — UMAP and t-SNE are not
meaningful at that sample size and their stochasticity would make the layout
change on every run. PCA is deterministic, which matters because the output is
committed.

### 5.3 Rendering

Vanilla `<canvas>` 2D, no library, target ~120 lines:

- A few thousand particles advected by a smooth curl-noise flow field.
- Particle color interpolates along a grenat → coral ramp by velocity.
- Paper anchors render as brighter, larger points. The flow field periodically
  weakens so the drifting particles settle toward the anchors, then resumes.
- Hovering an anchor surfaces the paper title; clicking navigates to it.
- Device-pixel-ratio aware; resizes with the viewport.

### 5.4 Degradation

| Condition | Behaviour |
|---|---|
| `prefers-reduced-motion: reduce` | One static frame is rendered; no animation loop |
| Canvas unsupported | A static SVG fallback is shown |
| `hero.json` fails to load | Particles render without anchors; the page is unaffected |

The animation loop pauses via `IntersectionObserver` when the hero scrolls out
of view, and via `visibilitychange` when the tab is backgrounded. An
always-running RAF loop is a battery drain with no benefit.

Anchor titles must also exist as real text in the DOM so the hero is not the
sole carrier of that information for screen readers.

## 6. Content model

Three YAML files under `content/`.

### 6.1 `content/site.yml`

```yaml
name: Juan Felipe Imbet
short_name: Juan F. Imbet
title: Assistant Professor of Finance
institution: EDHEC Business School
email: juan.imbet@edhec.edu
office: ""            # renders nothing while blank
photo: assets/images/profile.jpg
tagline: Finance, computation, and machine intelligence.
bio: |
  Multi-paragraph biography.
research_interests: [Corporate Finance, Asset Pricing, Computational Finance]
profiles:
  scholar: https://scholar.google.com/citations?user=0nHr8-4AAAAJ
  orcid: https://orcid.org/0000-0003-4970-3711
  github: https://github.com/jfimbett
  linkedin: https://www.linkedin.com/in/juan-f-imbet-0b053079/
  x: https://twitter.com/JuanImbett
  ssrn: ""            # not yet located; renders nothing while blank
  # repec: https://ideas.repec.org/e/pim50.html
  # researchgate: https://www.researchgate.net/profile/Juan-Imbet
previous_affiliations:
  - institution: Université Paris Dauphine–PSL
    role: Assistant Professor of Finance
    years: 2021–2026
```

Blank string values render nothing. The footer shows Scholar, ORCID, GitHub,
LinkedIn and X; RePEc and ResearchGate are present but commented out.

### 6.2 `content/papers.yml`

A single ordered list. `status` partitions it into the three sections.

```yaml
- id: social-media-bank-run
  title: Social Media as a Bank Run Catalyst
  authors: [J. Anthony Cookson, Corbin Fox, Javier Gil-Bazo, SELF, Christoph Schiller]
  status: published            # published | working | wip
  venue: Journal of Financial Economics
  detail: Volume 176, 2026, 104218
  year: 2026
  doi: https://www.sciencedirect.com/science/article/pii/S0304405X25002260
  ssrn: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4422754
  topics: [social media, banking]
  abstract: |
    Full abstract text.
  summary: |
    Plain-language paragraph for journalists and practitioners.
  media:
    - {outlet: Wall Street Journal, title: "...", url: "..."}
  regulators:
    - {body: "DFPI", title: "...", url: "..."}
```

Field rules:

- The literal token `SELF` in `authors` renders as the site owner's name in
  bold. This keeps the YAML free of markup and makes the self-reference
  impossible to typo.
- `status` is the only required discriminator. `published` entries appear
  under Publications, `working` under Working Papers, `wip` under Work in
  Progress.
- `summary` is drafted from the abstract during implementation and edited by
  the site owner. It is optional; entries without one simply omit the block.
- `media` and `regulators` are optional lists.
- Every `id` must be unique and URL-safe; it becomes the anchor fragment.

Required fields are `id`, `title`, `authors` and `status`. Published entries
additionally require `venue` and `year`. Everything else is optional.

The build fails loudly on a duplicate `id`, a missing required field, an
`id` that is not URL-safe, or a `status` outside `published | working | wip`. Silent omission of a paper would be worse than a broken
build, because the build output is committed and reviewed.

### 6.3 `content/courses.yml`

Ships as an empty list. Schema:

```yaml
- id: llm-finance
  title: Large Language Models in Finance
  institution: Barcelona School of Economics
  level: Summer School
  years: [2025, 2026]
  url: https://jfimbett.github.io/llm-finance-book
  description: One or two sentences.
```

**Conditional rendering.** When `courses.yml` is empty, `build.py` does not
emit `teaching.html` and the Teaching nav item is absent from every page. Add
one entry and rebuild, and both appear. This satisfies "drop it for now, make
it easy to add later" with no dead page and no maintenance burden.

## 7. Build pipeline

### 7.1 Layout

```
content/            papers.yml, courses.yml, site.yml
templates/          base.html.j2, index.html.j2, research.html.j2,
                    teaching.html.j2, cv.html.j2, partials/*.j2
build.py            renders templates -> HTML + search index
embed.py            computes embeddings (run only when papers change)
assets/css/site.css
assets/js/hero.js, search.js
assets/data/        search.json, embeddings.json, hero.json
assets/vendor/      transformers.min.js
index.html          generated, committed
research.html       generated, committed
cv.html             generated, committed
teaching.html       generated only when courses.yml is non-empty
```

### 7.2 `build.py`

Reads the three YAML files, validates them, renders the Jinja2 templates, and
writes the HTML plus `assets/data/search.json`. Dependencies: `Jinja2` and
`PyYAML` only. Added to the existing Poetry project.

```
$ python build.py
$ git add -A && git commit && git push
```

Exit code is non-zero on any validation failure, and no output files are
written in that case — a partial render must never be committed.

### 7.3 `embed.py`

Kept separate so the everyday build never needs PyTorch:

1. Load `sentence-transformers/all-MiniLM-L6-v2`.
2. Embed each paper's title + abstract + topics.
3. Write `assets/data/embeddings.json` (9 papers x 384 dims as float,
   rounded to 4 decimal places; roughly 25KB). Quantisation is deliberately
   avoided: at this size it saves a negligible number of bytes and would
   require carrying scale factors that both sides must agree on.
4. PCA-reduce to 2D, normalise, write `assets/data/hero.json`.

Run manually after adding or editing a paper. `build.py` warns — but does not
fail — when `papers.yml` is newer than `embeddings.json`, so a stale index is
visible without blocking a routine text edit.

The model identifier is pinned in `embed.py`, and the same model is loaded
client-side, so query and document vectors share an embedding space. A
mismatch here would silently produce meaningless similarity scores, so the
identifier is defined once and referenced by both sides.

## 8. Search

Three tiers of progressive enhancement. The visitor always has working search;
it silently gets better.

| Tier | Trigger | Cost | Capability |
|---|---|---|---|
| 0 | Page load | 0 KB | Search UI is inert; no assets fetched |
| 1 | Search opened | ~30 KB | BM25 keyword search, instant |
| 2 | Model loaded in background | ~23 MB, first use only | True semantic matching |

**Tier 1** ranks `search.json` (title, authors, venue, abstract, topics,
summary) with a compact BM25 implementation, roughly 40 lines of JavaScript.

**Tier 2** lazily loads a quantised MiniLM via transformers.js, embeds the
query, and re-ranks by cosine similarity against the precomputed vectors. This
is what lets *"how does Twitter affect banks"* surface the SVB paper despite
sharing no terms with it.

The transformers.js library is vendored into `assets/vendor/`; only the model
weights come from a CDN. If the model fails to load, or the visitor is
offline, or the CDN is blocked, Tier 1 remains and no error surfaces. The
upgrade must never cause visible result-reshuffling mid-keystroke.

Search is keyboard accessible: `/` focuses, `Escape` closes, arrow keys
traverse results, `Enter` navigates. The results list is an ARIA listbox with
a live region announcing the result count.

## 9. Archive and migration

`git mv` preserves history for:

```
teaching/  -> archive/teaching/
courses/   -> archive/courses/
talks/     -> archive/talks/
```

Nothing in `archive/` is linked from any generated page, and `archive/` is
excluded from the sitemap and marked `noindex`.

**Inbound-link preservation.** Old course pages are plausibly linked from
syllabi and student email. Meta-refresh stub files remain at the old paths for
the previously-linked index pages:

```
teaching/index.html
teaching/python-conda-course.html
teaching/empirical_asset_pricing/index.html
teaching/investment_funds_risks/index.html
teaching/python_m1/index.html
teaching/python_m2/index.html
teaching/python_m2_203/index.html
```

These seven paths are the full set of course landing pages that currently
exist under `teaching/`, verified against the working tree. Deeper pages
(`python_m2_203/oop/index.html`, `python_m2_203/final_project.html`,
`python_m2/oop/index.html`, `python_m2/templates/hello.html`) do not get
stubs; they were reachable only by navigating from a landing page, so the
landing-page stub is sufficient to carry a visitor through.

Each stub is a minimal HTML document with `<meta http-equiv="refresh">` to the
archived location, a `<link rel="canonical">`, and a visible link for anyone
whose browser blocks the refresh.

**Untouched:** `wedding/`, `blog/`, `code.html`, `scripts/`. These stop being
linked from navigation but remain byte-identical at their current URLs.

**Removed:** `MAINTENANCE_GUIDE.md` (superseded by the rewritten `README.md`),
the Bootstrap and Font Awesome CDN references, `assets/js/main.js` (its only
job was Bootstrap collapse toggles, replaced by `<details>`), and the stale
`scripts/build.py`, which invokes a `fetch_ssrn_data.py` that no longer exists.

## 10. Metadata, accessibility, performance

**Structured data.** JSON-LD `Person` on the home page, and one
`ScholarlyArticle` per entry on the research page, each carrying `author`,
`name`, `datePublished`, `sameAs` and DOI where available. Also Open Graph and
Twitter Card tags, plus `sitemap.xml` and `robots.txt`. Academic sites almost
never do this, and it is the cheapest available improvement to discoverability.

**Accessibility.** Semantic landmarks, a skip link, visible focus rings meeting
3:1 contrast, `<details>` for disclosure rather than scripted toggles, alt text
on all imagery, and full keyboard operation of search. Target: zero axe-core
violations.

**Performance budget.** Under 50 KB transferred before the hero canvas
initialises; no render-blocking JavaScript; fonts with `display=swap`; the
portrait served at its native 369x560 with explicit `width`/`height` to
reserve layout space. Target Lighthouse 100 across all four categories on the
home page.

## 11. Verification

Implementation is not complete until all of the following have been run and
their output observed:

1. `python build.py` exits 0 and regenerates every page.
2. Deliberate fault injection: a duplicate `id`, a missing `title`, and an
   unknown `status` each fail the build with a clear message and write no
   output.
3. Emptying and repopulating `courses.yml` correctly removes and restores
   `teaching.html` and its nav item.
4. Every internal link and anchor resolves; no 404s. Every external link
   returns a non-error status.
5. The four meta-refresh stubs land on their archived targets.
6. Rendered pages validate as HTML5.
7. axe-core reports zero violations on all pages.
8. Contrast pairs verified in both light and dark themes.
9. Lighthouse run on the home page; scores recorded.
10. Search verified at Tier 1 with the model blocked, and at Tier 2 with it
    available, including the cross-vocabulary query above.
11. Hero verified under `prefers-reduced-motion`, at mobile and desktop
    widths, and with `hero.json` removed.
12. Site rendered at 360px, 768px, 1280px and 1920px.

## 12. Risks

| Risk | Mitigation |
|---|---|
| 23 MB model download feels heavy | Never fetched until the visitor opens search; Tier 1 is fully functional without it |
| Model CDN blocked or offline | Tier 1 BM25 remains; no error surfaces |
| PCA on 8 points gives an arbitrary layout | Layout is deterministic and committed; it can be hand-adjusted in `hero.json` if it reads badly |
| Committed HTML drifts from YAML | `build.py` is idempotent; a dirty diff after a no-op build reveals drift immediately |
| Embeddings go stale after a paper edit | `build.py` warns on an out-of-date `embeddings.json` |
| Canvas hero costs battery | Paused off-screen and on hidden tabs; static under reduced-motion |
| Archived URLs break inbound links | Meta-refresh stubs at the previously-linked paths |
