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
     agenda: asset-pricing    # colours the point on the research map
     short: New Paper         # its label on the map, ~25 characters
     abstract: |
       ...
     summary: |
       One plain-language paragraph.
   ```

   `SELF` renders as your name in bold. Published papers also need `venue`
   and `year`. `agenda` must be one of the slugs in `AGENDAS` in `build.py`;
   adding a new one means adding a `--plot-<slug>` colour to
   `assets/css/site.css` and a shape to `SHAPES` in `assets/js/hero.js`.

2. Rebuild and refresh the search index and the map:

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
| `python3 -m http.server 8899` | Preview locally at 127.0.0.1:8899. |

`build.py` warns when `papers.yml` is newer than the embeddings.

## Layout

```
content/      YAML source — the only files you normally edit
templates/    Jinja2 templates
build.py      Renders templates to HTML, and writes search.json + sitemap.xml
tools/        Embedding and PCA tooling (Node)
assets/       CSS, JS, images, generated JSON
archive/      Old teaching material and talks; unlinked, kept for old URLs
blog/, code.html, wedding/   Older hand-written pages, left as they were
*.html        Generated. Do not edit by hand.
```

`assets/css/custom.css` and `assets/js/main.js` belong to those older
hand-written pages, not to the generated site.

## Design

Colour and type follow EDHEC's brand: grenat `#5F1937`, Montserrat and
Open Sans. Tokens are defined once at the top of `assets/css/site.css`.

The full design rationale is in
`docs/superpowers/specs/2026-08-20-website-redesign-design.md`.
