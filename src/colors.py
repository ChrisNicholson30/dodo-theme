"""Small colour toolkit used by every Dodo generator.

Everything works on "#rrggbb" / "#rrggbbaa" hex strings so the palette
file stays readable and diff-friendly.
"""

from __future__ import annotations


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def rgb(hex_: str) -> tuple[int, int, int]:
    h = hex_.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgbf(hex_: str) -> tuple[float, float, float]:
    r, g, b = rgb(hex_)
    return r / 255, g / 255, b / 255


def to_hex(r: float, g: float, b: float) -> str:
    return "#{:02x}{:02x}{:02x}".format(
        round(_clamp(r, 0, 255)), round(_clamp(g, 0, 255)), round(_clamp(b, 0, 255))
    )


def alpha(hex_: str, a: float | int) -> str:
    """Return #rrggbbaa. `a` is 0..1 (float) or 0..255 (int)."""
    if isinstance(a, float):
        a = round(_clamp(a) * 255)
    return "#" + hex_.lstrip("#")[:6] + "{:02x}".format(a)


def opaque(hex_: str) -> str:
    return "#" + hex_.lstrip("#")[:6]


def mix(a: str, b: str, t: float) -> str:
    """Linear sRGB-space blend: t=0 → a, t=1 → b."""
    ar, ag, ab = rgb(a)
    br, bg, bb = rgb(b)
    return to_hex(ar + (br - ar) * t, ag + (bg - ag) * t, ab + (bb - ab) * t)


def flatten(fg_with_alpha: str, bg: str) -> str:
    """Composite an #rrggbbaa colour over an opaque background."""
    h = fg_with_alpha.lstrip("#")
    a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return mix(bg, "#" + h[:6], a)


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_: str) -> float:
    r, g, b = (_lin(c) for c in rgbf(hex_))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def desaturate(hex_: str, t: float) -> str:
    """Pull a colour toward its own grey by t (0..1)."""
    r, g, b = rgb(hex_)
    y = 0.299 * r + 0.587 * g + 0.114 * b
    return to_hex(r + (y - r) * t, g + (y - g) * t, b + (y - b) * t)


def xterm256(hex_: str) -> int:
    """Nearest xterm-256 index (cube or grey ramp) for 256-colour fallbacks."""
    r, g, b = rgb(hex_)
    steps = [0, 95, 135, 175, 215, 255]

    def nearest(v: int) -> int:
        return min(range(6), key=lambda i: abs(steps[i] - v))

    ci = (nearest(r), nearest(g), nearest(b))
    cube = (steps[ci[0]], steps[ci[1]], steps[ci[2]])
    cube_idx = 16 + 36 * ci[0] + 6 * ci[1] + ci[2]
    grey_level = round((((r + g + b) / 3) - 8) / 10)
    grey_level = max(0, min(23, grey_level))
    grey = 8 + grey_level * 10
    grey_idx = 232 + grey_level

    def dist(c: tuple[int, int, int]) -> int:
        return (c[0] - r) ** 2 + (c[1] - g) ** 2 + (c[2] - b) ** 2

    return cube_idx if dist(cube) <= dist((grey, grey, grey)) else grey_idx
