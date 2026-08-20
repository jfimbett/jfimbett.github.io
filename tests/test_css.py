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
