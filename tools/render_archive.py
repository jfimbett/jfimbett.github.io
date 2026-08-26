"""
Render the archived course decks under archive/ to static HTML.

These are Marp slide decks kept as Markdown. GitHub Pages used to turn them
into pages by running Jekyll over the whole repository, which also swept in
every other Markdown file in the repo and broke the build whenever one of them
contained Liquid-like syntax. Rendering them here instead means the published
site is entirely static and Jekyll can stay switched off for good.

Run from the repository root:  python tools/render_archive.py

Only Markdown files with no sibling .html are rendered, so hand-written pages
are never overwritten. Output paths match the URLs Jekyll used to serve.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent

FRONT_MATTER = re.compile(r"\A---\r?\n.*?\r?\n---[ \t]*\r?\n", re.S)
SLIDE_BREAK = re.compile(r"^[ \t]*---[ \t]*$", re.M)
FENCED = re.compile(r"^([ \t]*)(`{3,}|~{3,})([^\n]*)\n(.*?)^[ \t]*\2[ \t]*$", re.M | re.S)
DISPLAY_MATH = re.compile(r"\$\$(.+?)\$\$", re.S)
INLINE_MATH = re.compile(r"(?<![\$\w])\$(?!\s)([^\$\n]+?)(?<!\s)\$(?![\$\w])")
# "a minimum price of $1 or $5" is prose about money, not a formula. Only treat
# a $...$ span as maths when it either holds a TeX construct or is a bare
# symbol; anything with a space and no TeX in it is left as literal text.
TEX_MARKER = re.compile(r"[\\^_{}]")
LIST_ITEM = re.compile(r"^[ \t]*(?:[-*+]\s|\d+[.)]\s)")
TITLE_IN_FM = re.compile(r"^(?:header|title):\s*['\"]?(.+?)['\"]?\s*$", re.M)
HEADING = re.compile(r"^#{1,3}\s+(.+?)\s*#*\s*$", re.M)

# Placeholders survive the Markdown pass untouched: no punctuation for the
# parser to interpret, and a shape that cannot occur in prose.
CODE_TOKEN = "zzcodeblockzz{}zz"
MATH_TOKEN = "zzmathspanzz{}zz"


def protect(text):
    """Pull fenced code and math out of the text before Markdown runs.

    Markdown would mangle both: underscores and asterisks inside TeX become
    emphasis, and math inside code should stay literal. Code is taken first so
    that a dollar sign inside a code block is never treated as math.
    """
    codes, maths = [], []

    def take_code(match):
        codes.append((match.group(3).strip(), match.group(4)))
        return CODE_TOKEN.format(len(codes) - 1)

    text = FENCED.sub(take_code, text)

    def take_math(match):
        maths.append(match.group(0))
        return MATH_TOKEN.format(len(maths) - 1)

    def take_inline_math(match):
        body = match.group(1)
        if " " in body and not TEX_MARKER.search(body):
            return match.group(0)
        return take_math(match)

    text = DISPLAY_MATH.sub(take_math, text)
    text = INLINE_MATH.sub(take_inline_math, text)
    return text, codes, maths


def separate_lists(text):
    """Put a blank line between a paragraph and a list that follows it.

    Marp renders through CommonMark, where a bullet list may interrupt a
    paragraph. Python-Markdown requires the blank line, and without it the
    bullets are swallowed into the preceding sentence as running text.
    """
    lines = text.split("\n")
    out = []
    for line in lines:
        if (
            out
            and out[-1].strip()
            and LIST_ITEM.match(line)
            and not LIST_ITEM.match(out[-1])
        ):
            out.append("")
        out.append(line)
    return "\n".join(out)


def restore(body, codes, maths):
    for i, raw in enumerate(maths):
        body = body.replace(MATH_TOKEN.format(i), raw)
    for i, (lang, code) in enumerate(codes):
        cls = ' class="language-{}"'.format(html.escape(lang.split()[0])) if lang else ""
        block = "<pre><code{}>{}</code></pre>".format(cls, html.escape(code))
        # Markdown wraps a bare token in a paragraph; swap the whole thing.
        token = CODE_TOKEN.format(i)
        body = body.replace("<p>{}</p>".format(token), block).replace(token, block)
    return body


def title_for(source, text):
    match = TITLE_IN_FM.search(text.split("---", 2)[1]) if text.lstrip().startswith("---") else None
    if match and match.group(1).strip():
        return match.group(1).strip()
    match = HEADING.search(FRONT_MATTER.sub("", text))
    if match:
        return match.group(1).strip()
    return source.stem.replace("_", " ").replace("-", " ").title()


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Juan F. Imbet</title>
<meta name="robots" content="noindex">
<link rel="icon" href="{prefix}assets/images/favicon.svg" type="image/svg+xml">
<link href="{prefix}assets/css/site.css" rel="stylesheet">
<style>
  /* site.css styles the main pages; course notes also need code and tables. */
  .archive {{ padding-block: 3rem 5rem; }}
  .archive pre {{
    background: var(--grenat-pastel); border: 1px solid var(--border);
    padding: 0.9rem 1rem; overflow-x: auto; border-radius: 3px;
    font-size: 0.9em; line-height: 1.5;
  }}
  .archive code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
  .archive :not(pre) > code {{
    background: var(--grenat-pastel); padding: 0.1em 0.35em; border-radius: 3px;
  }}
  .archive table {{ border-collapse: collapse; margin: 1.25rem 0; display: block; overflow-x: auto; }}
  .archive th, .archive td {{ border: 1px solid var(--border); padding: 0.45rem 0.7rem; text-align: left; }}
  .archive hr {{ border: 0; border-top: 1px solid var(--border); margin: 2.5rem 0; }}
  .archive img {{ max-width: 100%; height: auto; }}
  .archive__note {{ color: var(--muted); font-size: 0.9em; }}
</style>
<script>
  window.MathJax = {{ tex: {{ inlineMath: [['$', '$']], displayMath: [['$$', '$$']] }} }};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
<main class="wrap archive">
<p class="archive__note"><a href="{prefix}index.html">Juan F. Imbet</a> · archived course notes</p>
{body}
</main>
</body>
</html>
"""


def render(source):
    text = source.read_text(encoding="utf-8", errors="replace")
    title = title_for(source, text)
    text = FRONT_MATTER.sub("", text)

    body, codes, maths = protect(text)
    # Marp separates slides with a bare ---. Left alone, Markdown reads that as
    # a setext heading whenever prose sits directly above it, which silently
    # promotes a line of body text to a heading. Make the rule explicit first.
    body = SLIDE_BREAK.sub("\n<hr>\n", body)
    body = separate_lists(body)
    body = markdown.markdown(body, extensions=["fenced_code", "tables", "sane_lists"])
    body = restore(body, codes, maths)

    depth = len(source.relative_to(ROOT).parts) - 1
    page = PAGE.format(title=html.escape(title), prefix="../" * depth, body=body)
    target = source.with_suffix(".html")
    target.write_text(page, encoding="utf-8", newline="\n")
    return target


def main():
    tracked = subprocess.run(
        ["git", "ls-files", "archive"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.split("\n")

    sources = [
        ROOT / f
        for f in tracked
        if f.endswith(".md") and not (ROOT / f).with_suffix(".html").exists()
    ]
    if not sources:
        print("nothing to render; every archived deck already has a page")
        return 0

    for source in sorted(sources):
        target = render(source)
        print("wrote {}".format(target.relative_to(ROOT).as_posix()))
    print("{} pages rendered".format(len(sources)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
