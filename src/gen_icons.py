"""Dodo file icons for Zed — one hand-tuned 16px set per theme variant.

Design language
  • Languages wear a *soft badge*: a tinted rounded square with crisp
    letters, so dozens of them read as one family instead of a logo zoo.
  • Everything else is a 1.25px round-capped pictogram.
  • Folders are dodo-feather blue with a tiny accent-coloured tab — the
    tab (and the badge corner radius / weight) changes per variant, so each
    theme's icons are ever-so-slightly its own.
"""

from __future__ import annotations

import colorsys
import json
import math
import re
from pathlib import Path

from colors import mix, rgbf
from palette import Variant

GLYPHS = json.loads(Path(__file__).with_name("glyphs.json").read_text())

# Per-variant icon personality.
STYLE = {
    "dusk":     dict(radius=3.6, fill=0.17, ring=0.55, folder="solid"),
    "night":    dict(radius=3.0, fill=0.19, ring=0.6, folder="solid"),
    "obsidian": dict(radius=2.4, fill=0.10, ring=0.7, folder="outline"),
    "dawn":     dict(radius=3.6, fill=0.13, ring=0.5, folder="solid"),
    "mist":     dict(radius=2.8, fill=0.11, ring=0.55, folder="solid"),
}

SW = 1.25  # pictogram stroke width


# ── svg helpers ─────────────────────────────────────────────────────────────

def svg(body: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" '
        f'viewBox="0 0 16 16" fill="none">{body}</svg>\n'
    )


def S(d: str, c: str, w: float = SW, op: float = 1.0) -> str:
    o = f' stroke-opacity="{op:g}"' if op < 1 else ""
    return (f'<path d="{d}" stroke="{c}" stroke-width="{w:g}" '
            f'stroke-linecap="round" stroke-linejoin="round"{o}/>')


def F(d: str, c: str, op: float = 1.0) -> str:
    o = f' fill-opacity="{op:g}"' if op < 1 else ""
    return f'<path d="{d}" fill="{c}"{o}/>'


def circ(cx: float, cy: float, r: float, c: str, fill: bool = True, w: float = SW, op: float = 1.0) -> str:
    if fill:
        o = f' fill-opacity="{op:g}"' if op < 1 else ""
        return f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="{c}"{o}/>'
    return f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" stroke="{c}" stroke-width="{w:g}"/>'


def rrect(x, y, w, h, r, stroke=None, fill=None, fill_op=1.0, sw=SW, stroke_op=1.0) -> str:
    a = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}"'
    if fill:
        a += f' fill="{fill}"' + (f' fill-opacity="{fill_op:g}"' if fill_op < 1 else "")
    if stroke:
        a += f' stroke="{stroke}" stroke-width="{sw:g}"' + (
            f' stroke-opacity="{stroke_op:g}"' if stroke_op < 1 else "")
    return a + "/>"


# ── text → path (lettering baked from Inter Display ExtraBold) ─────────────

_TOK = re.compile(r"[MLHVCQZ]|-?\d*\.?\d+(?:e-?\d+)?")


def _xform(d: str, ox: float, oy: float, s: float) -> str:
    out, cmd, nums = [], None, []

    def flush():
        if cmd is None:
            return
        if cmd == "Z":
            out.append("Z")
            return
        if cmd == "H":
            out.append("H" + " ".join(f"{ox + n * s:.2f}" for n in nums))
        elif cmd == "V":
            out.append("V" + " ".join(f"{oy - n * s:.2f}" for n in nums))
        else:
            pts = [f"{ox + nums[i] * s:.2f} {oy - nums[i + 1] * s:.2f}" for i in range(0, len(nums), 2)]
            out.append(cmd + " ".join(pts))

    for t in _TOK.findall(d):
        if t.isalpha():
            flush()
            cmd, nums = t, []
        else:
            nums.append(float(t))
    flush()
    return "".join(out)


def text_paths(label: str, cx: float, cy: float, cap: float, max_w: float,
               track: float = -0.02) -> list[tuple[str, str]]:
    """Return [(char, path_d)] for `label` centred on (cx, cy)."""
    upm = GLYPHS["unitsPerEm"]
    has_caps = any(ch.isupper() or ch.isdigit() or ch in "#+λ" for ch in label)
    ref_h = GLYPHS["capHeight"] if has_caps else GLYPHS["xHeight"]
    s = cap / ref_h
    adv = [GLYPHS["glyphs"][ch]["adv"] for ch in label]
    total = sum(adv) + track * upm * (len(label) - 1)
    if total * s > max_w:
        s = max_w / total
    h = ref_h * s
    x = cx - total * s / 2
    base = cy + h / 2
    out = []
    for ch, a in zip(label, adv):
        out.append((ch, _xform(GLYPHS["glyphs"][ch]["d"], x, base, s)))
        x += (a + track * upm) * s
    return out


# ── icon catalogue ──────────────────────────────────────────────────────────
# Badges: key → (label, colour role | tuple of per-letter roles)
BADGES: dict[str, tuple[str, object]] = {
    "typescript": ("TS", "blue"),
    "typescript_def": ("DT", "sky"),
    "javascript": ("JS", "yellow"),
    "python": ("Py", ("blue", "yellow")),
    "rust": ("RS", "orange"),
    "go": ("GO", "sky"),
    "c": ("C", "blue"),
    "cpp": ("C++", "lavender"),
    "csharp": ("C#", "purple"),
    "objc": ("OC", "sky"),
    "java": ("J", "red"),
    "kotlin": ("K", "purple"),
    "scala": ("SC", "red"),
    "swift": ("SW", "orange"),
    "php": ("php", "lavender"),
    "lua": ("Lu", "blue"),
    "luau": ("Lu", "sky"),
    "zig": ("Z", "amber"),
    "dart": ("D", "sky"),
    "haskell": ("λ", "purple"),
    "erlang": ("E", "red"),
    "ocaml": ("ML", "orange"),
    "elm": ("E", "sky"),
    "gleam": ("GL", "pink"),
    "nim": ("N", "yellow"),
    "r": ("R", "blue"),
    "fsharp": ("F#", "sky"),
    "crystal": ("CR", "gray"),
    "cairo": ("CA", "orange"),
    "ballerina": ("BA", "teal"),
    "bicep": ("BI", "sky"),
    "cue": ("CU", "teal"),
    "kdl": ("KD", "amber"),
    "metal": ("MT", "gray"),
    "odin": ("OD", "blue"),
    "puppet": ("PP", "amber"),
    "roc": ("RC", "purple"),
    "solidity": ("SO", "gray"),
    "surrealql": ("SQ", "pink"),
    "tcl": ("TC", "blue"),
    "v": ("V", "sky"),
    "vyper": ("VY", "teal"),
    "wgsl": ("WG", "lavender"),
    "vue": ("V", "green"),
    "svelte": ("Sv", "orange"),
    "astro": ("A", "purple"),
    "sass": ("S", "pink"),
    "coffeescript": ("Co", "brown"),
    "bun": ("B", "cream"),
    "heroku": ("H", "purple"),
    "visualstudio": ("VS", "purple"),
    "wasm": ("WA", "purple"),
    "proto": ("PB", "teal"),
    "gradle": ("GR", "teal"),
    "clojure": ("CL", "green"),
    "perl": ("PL", "blue"),
    "ruby_erb": ("RB", "red"),
    "hcl": ("HC", "purple"),
    "stylelint": ("SL", "gray"),
    "matlab": ("M", "orange"),
    "assembly": ("AS", "gray"),
    "fortran": ("F", "purple"),
    "groovy": ("GV", "teal"),
    "racket": ("RK", "red"),
    "scheme": ("λ", "red"),
    "lisp": ("λ", "teal"),
    "powershell": ("PS", "blue"),
    "latex": ("Tx", "teal"),
    "typst": ("T", "teal"),
    "d": ("D", "red"),
    "zon": ("Z", "brown"),
    "mojo": ("MO", "orange"),
}


def badge(label: str, roles, c: dict, st: dict) -> str:
    roles = (roles,) * len(label) if isinstance(roles, str) else roles
    base_col = c[roles[0]]
    out = rrect(2, 2, 12, 12, st["radius"], stroke=base_col, fill=base_col,
                fill_op=st["fill"], sw=1, stroke_op=st["ring"])
    n = len(label)
    cap = {1: 6.6, 2: 5.6, 3: 4.6}.get(n, 4.2)
    max_w = {1: 7.5, 2: 9.0, 3: 9.6}.get(n, 9.8)
    for (ch, d), role in zip(text_paths(label, 8, 8.05, cap, max_w), roles):
        out += F(d, c[role])
    return out


# Pictograms: functions of (colours, style) → svg body.
DOC = "M4.25 1.75h4.9l3.6 3.6v8.4a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5V2.25a.5.5 0 0 1 .5-.5z"
FOLD = "M9.1 1.9v2.85a.6.6 0 0 0 .6.6h2.9"


def doc(col, lines=()):
    out = S(DOC, col) + S(FOLD, col)
    for y, x2 in lines:
        out += S(f"M5.75 {y}H{x2}", col)
    return out


def frame(col):
    return rrect(1.75, 2.75, 12.5, 10.5, 2, stroke=col)


def gear(cx, cy, r_out, r_in, teeth, col):
    pts = []
    for i in range(teeth * 2):
        ang = math.pi * i / teeth
        r = r_out if i % 2 == 0 else r_in
        for da in (-0.28, 0.28):
            a = ang + da * (math.pi / teeth)
            pts.append(f"{cx + r * math.cos(a):.2f} {cy + r * math.sin(a):.2f}")
    return S("M" + "L".join(pts) + "Z", col, 1.1) + circ(cx, cy, r_in * 0.42, col, fill=False, w=1.1)


def asterisk(cx, cy, col, n=8, r1=1.3, r2=6.1, w=1.55):
    out = ""
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        r = r2 if i % 2 == 0 else r2 * 0.78
        out += S(f"M{cx + r1 * math.cos(a):.2f} {cy + r1 * math.sin(a):.2f}"
                 f"L{cx + r * math.cos(a):.2f} {cy + r * math.sin(a):.2f}", col, w)
    return out


def hexagon(cx, cy, r, col, w=SW):
    pts = [f"{cx + r * math.cos(math.pi / 6 + i * math.pi / 3):.2f} "
           f"{cy + r * math.sin(math.pi / 6 + i * math.pi / 3):.2f}" for i in range(6)]
    return S("M" + "L".join(pts) + "Z", col, w)


def ellipse_rot(cx, cy, rx, ry, deg, col, w=1.1):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({deg} {cx} {cy})" '
            f'stroke="{col}" stroke-width="{w}"/>')


def text_fill(label, col, cx=8, cy=8, cap=6.0, max_w=12):
    return "".join(F(d, col) for _, d in text_paths(label, cx, cy, cap, max_w))


def pictograms(c: dict, st: dict, accent: str, feather: str) -> dict[str, str]:
    p: dict[str, str] = {}
    p["default"] = doc(c["gray"])
    p["text"] = doc(c["gray"], [(8.5, 10.25), (10.75, 9)])
    p["document"] = doc(c["blue"], [(8.25, 10.25), (10.5, 10.25), (12.5, 8.5)])
    p["pdf"] = doc(c["red"], [(8.25, 10.25), (10.5, 10.25), (12.5, 8.5)])
    p["markdown"] = (rrect(1.75, 3.25, 12.5, 9.5, 2, stroke=c["sky"])
                     + S("M4.25 10.25v-4.5l1.9 2.25 1.9-2.25v4.5", c["sky"])
                     + S("M11 5.75v4.5M9.4 8.75 11 10.3l1.6-1.55", c["sky"]))
    p["readme"] = (S("M8 4.4C6.7 3.4 4.9 2.9 2.25 2.9v9.3c2.65 0 4.45.5 5.75 1.5 1.3-1 3.1-1.5 5.75-1.5V2.9C11.1 2.9 9.3 3.4 8 4.4z", accent)
                   + S("M8 4.4v9.2", accent))
    p["license"] = (circ(8, 6.25, 3.6, c["yellow"], fill=False)
                    + circ(8, 6.25, 1.3, c["yellow"])
                    + S("M5.9 9.2 5.25 14l2.75-1.4 2.75 1.4-.65-4.8", c["yellow"]))
    p["changelog"] = (S("M2.6 8a5.4 5.4 0 1 0 1.6-3.85", c["green"])
                      + S("M2.4 2.6v2.3h2.3", c["green"])
                      + S("M8 5.3V8l1.9 1.4", c["green"]))
    p["json"] = (S("M5.75 2.5h-.5C4.2 2.5 3.8 3.1 3.8 4.2v1.6c0 1.05-.45 1.8-1.4 2.2.95.4 1.4 1.15 1.4 2.2v1.6c0 1.1.4 1.7 1.45 1.7h.5", c["yellow"])
                 + S("M10.25 2.5h.5c1.05 0 1.45.6 1.45 1.7v1.6c0 1.05.45 1.8 1.4 2.2-.95.4-1.4 1.15-1.4 2.2v1.6c0 1.1-.4 1.7-1.45 1.7h-.5", c["yellow"])
                 + circ(8, 8, 0.95, c["yellow"]))
    p["yaml"] = (S("M2.75 3.75h6.5", c["pink"]) + S("M5.25 8h8", c["pink"])
                 + S("M5.25 12.25h5", c["pink"]) + circ(2.9, 8, 0.85, c["pink"], op=0.6)
                 + circ(2.9, 12.25, 0.85, c["pink"], op=0.6))
    p["toml"] = (S("M4.75 2.75h-2v10.5h2", c["brown"]) + S("M11.25 2.75h2v10.5h-2", c["brown"])
                 + S("M6 6h4M6 8h4M6 10h2.5", c["brown"]))
    p["settings"] = gear(8, 8, 6.1, 4.3, 7, c["lavender"])
    p["plist"] = (S("M2.75 4.5h10.5M2.75 8h10.5M2.75 11.5h10.5", c["teal"])
                  + circ(10.25, 4.5, 1.6, c["teal"]) + circ(5.5, 8, 1.6, c["teal"])
                  + circ(9, 11.5, 1.6, c["teal"]))
    p["tsconfig"] = (S("M2.75 4.5h10.5M2.75 8h10.5M2.75 11.5h10.5", c["blue"])
                     + circ(10.25, 4.5, 1.6, c["blue"]) + circ(5.5, 8, 1.6, c["blue"])
                     + circ(9, 11.5, 1.6, c["blue"]))
    p["key"] = (circ(5.1, 8, 2.9, c["amber"], fill=False)
                + S("M8 8h6M12.25 8v2.4M14 8v1.6", c["amber"]) + circ(5.1, 8, 0.9, c["amber"]))
    p["lock"] = (rrect(3.25, 7, 9.5, 7, 1.6, stroke=c["gray"])
                 + S("M5.4 7V5.1a2.6 2.6 0 0 1 5.2 0V7", c["gray"])
                 + S("M8 9.75v1.5", c["gray"]))
    p["vcs"] = (circ(4.75, 3.9, 1.65, c["orange"], fill=False) + circ(4.75, 12.1, 1.65, c["orange"], fill=False)
                + circ(11.25, 6.1, 1.65, c["orange"], fill=False)
                + S("M4.75 5.55v4.9", c["orange"])
                + S("M11.25 7.75c0 2-2.6 2.3-5.4 3.1", c["orange"]))
    p["terminal"] = (frame(c["green"]) + S("M4.6 6.1 6.5 8l-1.9 1.9", c["green"])
                     + S("M8.4 10.1h3", c["green"]))
    p["docker"] = (S("M1.6 9.6h12.8c-.4 2.6-2.8 4.15-6.4 4.15S2 12.2 1.6 9.6z", c["sky"])
                   + rrect(3, 6.3, 2.6, 2.3, 0.4, stroke=c["sky"], sw=1)
                   + rrect(6.7, 6.3, 2.6, 2.3, 0.4, stroke=c["sky"], sw=1)
                   + rrect(10.4, 6.3, 2.6, 2.3, 0.4, stroke=c["sky"], sw=1)
                   + rrect(6.7, 3, 2.6, 2.3, 0.4, stroke=c["sky"], sw=1))
    p["storage"] = ('<ellipse cx="8" cy="4.1" rx="5" ry="1.85" stroke="{0}" stroke-width="1.25"/>'.format(c["amber"])
                    + S("M3 4.1v7.8c0 1.02 2.24 1.85 5 1.85s5-.83 5-1.85V4.1", c["amber"])
                    + S("M3 8c0 1.02 2.24 1.85 5 1.85S13 9.02 13 8", c["amber"]))
    p["table"] = (rrect(2, 2.75, 12, 10.5, 1.75, stroke=c["green"])
                  + S("M2 6.25h12M2 9.75h12M6.25 6.25v7", c["green"]))
    p["image"] = (frame(c["purple"]) + S("M2.4 12.4 6.1 8.5l2.6 2.6 1.6-1.6 3.3 3.1", c["purple"])
                  + circ(10.6, 5.9, 1.25, c["purple"]))
    p["svg"] = (S("M3.4 12.1C3.9 6.8 7.3 4.1 12.6 3.9", c["amber"])
                + rrect(1.75, 11.25, 3, 3, 0.6, stroke=c["amber"], sw=1.1)
                + rrect(11.25, 1.75, 3, 3, 0.6, stroke=c["amber"], sw=1.1)
                + S("M3.25 3.1h3.5M12.9 9.25v3.5", c["amber"], op=0.55))
    p["video"] = frame(c["red"]) + F("M6.4 5.5v5l4.2-2.5z", c["red"])
    p["audio"] = (S("M6.25 12V4.1l7-1.6v8", c["pink"]) + circ(4.4, 12, 1.85, c["pink"])
                  + circ(11.4, 10.5, 1.85, c["pink"]))
    p["font"] = text_fill("Aa", c["red"], 8, 8.4, 7.2, 13)
    p["archive"] = (rrect(2.5, 2.25, 11, 11.5, 2, stroke=c["brown"])
                    + S("M8 2.6v1M8 4.9v1M8 7.2v.8", c["brown"])
                    + rrect(6.75, 8.4, 2.5, 3.2, 0.6, stroke=c["brown"], sw=1.1))
    p["html"] = S("M5.3 4.4 1.9 8l3.4 3.6M10.7 4.4 14.1 8l-3.4 3.6M9.1 3.2 6.9 12.8", c["orange"])
    p["template"] = S("M5.3 4.4 1.9 8l3.4 3.6M10.7 4.4 14.1 8l-3.4 3.6", c["amber"])
    p["code"] = S("M5.3 4.4 1.9 8l3.4 3.6M10.7 4.4 14.1 8l-3.4 3.6", c["gray"])
    p["css"] = S("M6.3 2.4 5.1 13.6M11 2.4 9.8 13.6M2.9 5.9h11M2.2 10.1h11", c["blue"])
    p["react"] = (ellipse_rot(8, 8, 6.2, 2.4, 0, c["sky"]) + ellipse_rot(8, 8, 6.2, 2.4, 60, c["sky"])
                  + ellipse_rot(8, 8, 6.2, 2.4, 120, c["sky"]) + circ(8, 8, 1.2, c["sky"]))
    p["react_ts"] = (ellipse_rot(8, 8, 6.2, 2.4, 0, c["blue"]) + ellipse_rot(8, 8, 6.2, 2.4, 60, c["blue"])
                     + ellipse_rot(8, 8, 6.2, 2.4, 120, c["blue"]) + circ(8, 8, 1.2, c["blue"]))
    p["ruby"] = S("M4.5 2.9h7l2.6 3.3L8 13.4 1.9 6.2zM1.9 6.2h12.2M6.2 2.9l-.9 3.3L8 13.4l2.7-7.2-.9-3.3", c["red"], 1.15)
    p["elixir"] = S("M8 1.75C5.5 4.75 3.5 7.8 3.5 10.1a4.5 4.5 0 0 0 9 0c0-2.3-2-5.35-4.5-8.35z", c["purple"]) + \
        S("M6.1 10.6c.1.9.7 1.6 1.6 1.8", c["purple"], op=0.6)
    p["phoenix"] = S("M8 1.75C5.5 4.75 3.5 7.8 3.5 10.1a4.5 4.5 0 0 0 9 0c0-2.3-2-5.35-4.5-8.35z", c["orange"])
    p["julia"] = circ(8, 4.6, 2.3, c["green"]) + circ(4.4, 10.9, 2.3, c["red"]) + circ(11.6, 10.9, 2.3, c["purple"])
    nix = ""
    for i in range(3):
        a = math.pi / 3 * i
        dx, dy = math.cos(a), math.sin(a)
        nix += S(f"M{8 - 5.6 * dx:.2f} {8 - 5.6 * dy:.2f}L{8 + 5.6 * dx:.2f} {8 + 5.6 * dy:.2f}", c["sky"])
    for i in range(6):
        a = math.pi / 3 * i
        bx, by = 8 + 3.6 * math.cos(a), 8 + 3.6 * math.sin(a)
        for s_ in (-1, 1):
            b = a + s_ * math.pi / 3.2
            nix += S(f"M{bx:.2f} {by:.2f}L{bx + 1.7 * math.cos(b):.2f} {by + 1.7 * math.sin(b):.2f}", c["sky"], 1.1)
    p["nix"] = nix
    tri = "M8 4.1 11.4 10H4.6z"
    p["graphql"] = hexagon(8, 8, 5.6, c["pink"], 1.1) + S(tri, c["pink"], 1.1) + "".join(
        circ(8 + 5.6 * math.cos(math.pi / 6 + i * math.pi / 3), 8 + 5.6 * math.sin(math.pi / 6 + i * math.pi / 3), 1.05, c["pink"])
        for i in range(6))
    p["prisma"] = S("M7.6 1.9 2.9 12.2l5.8 1.9 4.4-1.9z", c["teal"]) + S("M7.6 1.9l1.1 12.2", c["teal"])
    p["terraform"] = (F("M2.4 2.3l3.6 2.1v4.1L2.4 6.4z", c["purple"]) + F("M6.6 4.7l3.6 2.1v4.1L6.6 8.8z", c["purple"])
                      + F("M10.8 6.8 14.4 4.7v4.1l-3.6 2.1z", c["purple"], 0.55)
                      + F("M6.6 9.5l3.6 2.1v4.1l-3.6-2.1z", c["purple"]))
    helm = circ(8, 8, 3.2, c["blue"], fill=False)
    for i in range(8):
        a = math.pi / 4 * i
        helm += S(f"M{8 + 3.2 * math.cos(a):.2f} {8 + 3.2 * math.sin(a):.2f}L{8 + 5.9 * math.cos(a):.2f} {8 + 5.9 * math.sin(a):.2f}", c["blue"])
    p["helm"] = helm + circ(8, 8, 1, c["blue"])
    p["eslint"] = hexagon(8, 8, 6, c["purple"]) + hexagon(8, 8, 2.9, c["purple"], 1.1)
    p["prettier"] = (S("M2.5 3.5h5", c["teal"]) + S("M9.5 3.5h4", c["yellow"])
                     + S("M2.5 6.5h8", c["pink"]) + S("M2.5 9.5h3", c["yellow"])
                     + S("M7.5 9.5h6", c["teal"]) + S("M2.5 12.5h6.5", c["purple"]))
    p["editorconfig"] = frame(c["gray"]) + S("M6.6 5.3h2.8M6.6 10.7h2.8M8 5.3v5.4", c["gray"])
    p["diff"] = S("M5 2.75v5M2.5 5.25h5", c["green"]) + S("M8.75 11.25h5", c["red"]) + S("M12.4 2.9 3.6 13.1", c["gray"], 1.1)
    p["log"] = (circ(3.3, 4.5, 0.95, c["gray"]) + circ(3.3, 8, 0.95, c["gray"]) + circ(3.3, 11.5, 0.95, c["gray"])
                + S("M6 4.5h7.5M6 8h5.5M6 11.5h7", c["gray"]))
    p["notebook"] = (rrect(3.5, 1.9, 9.5, 12.2, 1.6, stroke=c["orange"])
                     + S("M2.4 4.75h2.2M2.4 8h2.2M2.4 11.25h2.2", c["orange"])
                     + S("M7 5.5h3.5", c["orange"], op=0.6))
    p["package"] = (S("M8 1.8 13.6 4.85v6.3L8 14.2l-5.6-3.05v-6.3z", c["green"])
                    + S("M2.4 4.85 8 7.9l5.6-3.05M8 7.9v6.3", c["green"]))
    p["cargo"] = (S("M8 1.8 13.6 4.85v6.3L8 14.2l-5.6-3.05v-6.3z", c["orange"])
                  + S("M2.4 4.85 8 7.9l5.6-3.05M8 7.9v6.3", c["orange"]))
    p["swiftpm"] = (S("M8 1.8 13.6 4.85v6.3L8 14.2l-5.6-3.05v-6.3z", c["orange"])
                    + S("M2.4 4.85 8 7.9l5.6-3.05M8 7.9v6.3", c["orange"]) + S("M5.2 3.3l5.6 3.05", c["orange"], 1, 0.55))
    p["node"] = hexagon(8, 8, 6, c["green"]) + text_fill("N", c["green"], 8, 8.05, 5.2, 6)
    p["vite"] = F("M9.2 1.6 3.6 9h4.1l-1.1 5.4L12.4 7H8.3z", c["purple"])
    p["test"] = (S("M6 1.9h4M6.75 1.9v3.9L3.05 12.4a1.25 1.25 0 0 0 1.1 1.85h7.7a1.25 1.25 0 0 0 1.1-1.85L9.25 5.8V1.9", c["green"])
                 + S("M4.7 9.6h6.6", c["green"]))
    p["tailwind"] = (S("M1.9 7.1C3.4 4.6 5.2 4.3 7.15 5.85 9 7.3 10.5 7.6 12.5 5.6", c["sky"])
                     + S("M3.5 11.6C5 9.1 6.8 8.8 8.75 10.35c1.85 1.45 3.35 1.75 5.35-.25", c["sky"]))
    p["make"] = (S("M9.6 2.3a3.3 3.3 0 0 0-3.9 4.3L2.2 10.1a1.4 1.4 0 0 0 2 2l3.5-3.5a3.3 3.3 0 0 0 4.3-3.9l-2 2-1.9-.4-.4-1.9z", c["brown"]))
    p["xcode"] = (rrect(2, 2, 12, 12, 3, stroke=c["blue"])
                  + S("M5.6 5.4 8 10.6l2.4-5.2M6.4 9h3.2", c["blue"]))
    p["layout"] = rrect(1.75, 2.75, 12.5, 10.5, 2, stroke=c["blue"]) + S("M1.75 5.9h12.5M6 5.9v7.35", c["blue"])
    p["i18n"] = (circ(8, 8, 5.9, c["sky"], fill=False)
                 + '<ellipse cx="8" cy="8" rx="2.5" ry="5.9" stroke="{0}" stroke-width="1.1"/>'.format(c["sky"])
                 + S("M2.3 6h11.4M2.3 10h11.4", c["sky"], 1.1))
    p["binary"] = text_fill("01", c["gray"], 8, 8, 6.2, 11)
    p["claude"] = asterisk(8, 8, accent)
    p["dodo"] = asterisk(8, 8, feather)
    p["github"] = (circ(8, 8, 5.9, c["gray"], fill=False)
                   + S("M6.1 13.4v-1.6c0-.6.2-1 .5-1.3-1.7-.2-3-1-3-3 0-.6.2-1.2.6-1.6-.1-.3-.2-1 .1-1.7 0 0 .6-.2 1.8.6a6 6 0 0 1 3.2 0c1.2-.8 1.8-.6 1.8-.6.3.7.2 1.4.1 1.7.4.4.6 1 .6 1.6 0 2-1.3 2.8-3 3 .3.3.5.8.5 1.4v1.5", c["gray"], 1))
    p["ignore"] = doc(c["gray"]) + S("M5.4 11.9 10.9 6.4", c["gray"], 1.1)
    return p


# ── folders ────────────────────────────────────────────────────────────────

FOLDER_BODY = ("M1.75 4.25a1.5 1.5 0 0 1 1.5-1.5h2.88c.4 0 .78.16 1.06.44l1.06 1.06h4.5a1.5 1.5 0 0 1 1.5 1.5v6.5"
               "a1.5 1.5 0 0 1-1.5 1.5H3.25a1.5 1.5 0 0 1-1.5-1.5z")
FOLDER_TAB = "M3.25 2.75h2.88c.4 0 .78.16 1.06.44l1.06 1.06H1.75a1.5 1.5 0 0 1 1.5-1.5z"
OPEN_BACK = ("M1.75 11.9V4.25a1.5 1.5 0 0 1 1.5-1.5h2.88c.4 0 .78.16 1.06.44l1.06 1.06h4.5a1.5 1.5 0 0 1 1.5 1.5v.9")
OPEN_FRONT = ("M3.55 7.25a1.5 1.5 0 0 1 1.4-.97h9.2a.75.75 0 0 1 .7 1.02l-1.85 4.95a1.5 1.5 0 0 1-1.4.97H2.1"
              "a.5.5 0 0 1-.47-.68z")


def folder(col: str, tab: str, st: dict, open_: bool) -> str:
    outline = st["folder"] == "outline"
    if not open_:
        if outline:
            return F(FOLDER_BODY, col, 0.14) + S(FOLDER_BODY, col, 1.1) + F(FOLDER_TAB, tab)
        return F(FOLDER_BODY, col, 0.92) + F(FOLDER_TAB, tab)
    if outline:
        return (S(OPEN_BACK, col, 1.1) + F(OPEN_FRONT, col, 0.18) + S(OPEN_FRONT, col, 1.1)
                + F(FOLDER_TAB, tab))
    return (F(FOLDER_BODY, col, 0.42) + F(FOLDER_TAB, tab) + F(OPEN_FRONT, col, 0.95))


# Folder colour roles + the names that wear them.
FOLDER_GROUPS: dict[str, list[str]] = {
    "teal": ["src", "source", "sources", "lib", "libs", "app", "apps", "pkg", "internal", "cmd",
             "crates", "packages", "core", "Sources"],
    "green": ["test", "tests", "__tests__", "spec", "specs", "e2e", "fixtures", "__mocks__",
              "Tests", "testdata", "benches", "bench"],
    "blue": ["docs", "doc", "documentation", "wiki", "guides", "examples", "example"],
    "purple": ["assets", "images", "img", "icons", "public", "static", "media", "fonts", "Resources",
               "resources", "Assets.xcassets"],
    "orange": [".git", ".github", ".gitlab", ".husky", ".circleci", "workflows", ".forgejo"],
    "gray": ["node_modules", "vendor", "target", ".venv", "venv", "deps", ".cache", "__pycache__",
             ".pytest_cache", "Pods", "DerivedData", ".build", ".swiftpm", "tmp", "temp", "logs"],
    "brown": ["build", "dist", "out", "bin", "obj", ".next", ".nuxt", ".output", "release", "coverage",
              "generated", "gen"],
    "yellow": ["config", ".config", "configs", "settings", ".vscode", ".zed", ".idea", "env", ".devcontainer"],
    "sky": ["scripts", "script", "tools", "tooling", "bin-scripts", ".cargo", "ci", "hooks", ".claude-hooks"],
    "pink": ["styles", "css", "scss", "theme", "themes", "sass"],
    "lavender": ["components", "ui", "views", "pages", "routes", "screens", "layouts", "widgets", "Views"],
    "red": ["api", "server", "services", "backend", "functions", "handlers", "middleware", "controllers"],
    "amber": ["models", "types", "schemas", "schema", "db", "database", "migrations", "prisma", "entities",
              "Model", "Models", "data"],
    "accent": [".claude", ".dodo"],
}


def folder_tab(v: Variant) -> str:
    """The variant's signature tab colour — accent unless it's too close to feather."""
    ha = colorsys.rgb_to_hls(*rgbf(v.accent))[0]
    hf = colorsys.rgb_to_hls(*rgbf(v.feather))[0]
    if min(abs(ha - hf), 1 - abs(ha - hf)) < 30 / 360:
        return v.icons["amber"]
    return v.accent


# ── file associations ──────────────────────────────────────────────────────

SUFFIXES: dict[str, list[str]] = {
    "typescript": ["ts", "cts", "mts"],
    "typescript_def": ["d.ts", "d.mts", "d.cts"],
    "javascript": ["js", "cjs", "mjs"],
    "react": ["jsx", "cjsx", "mjsx"],
    "react_ts": ["tsx", "ctsx", "mtsx"],
    "python": ["py", "pyi", "pyw", "pyx", "pxd", "ipy"],
    "rust": ["rs"],
    "go": ["go", "mod", "work", "go.mod", "go.sum", "go.work"],
    "c": ["c", "h"],
    "cpp": ["c++", "h++", "cc", "cpp", "cppm", "cxx", "hh", "hpp", "hxx", "inl", "ixx", "ino"],
    "csharp": ["cs", "csx"],
    "objc": ["m", "mm"],
    "java": ["java", "jar", "class"],
    "kotlin": ["kt", "kts"],
    "scala": ["scala", "sc", "sbt"],
    "swift": ["swift"],
    "php": ["php", "phtml"],
    "lua": ["lua"],
    "luau": ["luau"],
    "zig": ["zig"],
    "zon": ["zon", "zig.zon"],
    "dart": ["dart"],
    "haskell": ["hs", "lhs", "cabal"],
    "erlang": ["erl", "hrl", "escript", "xrl", "yrl", "app.src", "rebar.config"],
    "elixir": ["ex", "exs", "eex", "leex", "neex"],
    "phoenix": ["heex"],
    "ocaml": ["ml", "mli", "mlx"],
    "elm": ["elm"],
    "gleam": ["gleam"],
    "nim": ["nim", "nims", "nimble"],
    "r": ["r", "R", "rmd", "Rmd"],
    "julia": ["jl"],
    "fsharp": ["fs", "fsi", "fsx"],
    "crystal": ["cr", "ecr"],
    "cairo": ["cairo"],
    "ballerina": ["bal"],
    "bicep": ["bicep"],
    "cue": ["cue"],
    "kdl": ["kdl"],
    "metal": ["metal"],
    "odin": ["odin"],
    "puppet": ["pp"],
    "roc": ["roc"],
    "solidity": ["sol"],
    "surrealql": ["surql"],
    "tcl": ["tcl"],
    "v": ["v", "vsh", "vv"],
    "vyper": ["vy", "vyi"],
    "wgsl": ["wgsl", "glsl", "hlsl", "frag", "vert", "shader"],
    "vue": ["vue"],
    "svelte": ["svelte"],
    "astro": ["astro"],
    "sass": ["sass", "scss", "less", "styl"],
    "css": ["css", "pcss", "postcss"],
    "html": ["htm", "html", "xhtml"],
    "template": ["hbs", "handlebars", "xml", "xsd", "xsl", "ejs", "njk", "liquid", "jinja", "j2", "tmpl",
                 "tpl", "mustache", "erb", "twig"],
    "coffeescript": ["coffee"],
    "bun": ["bun.lock"],
    "visualstudio": ["csproj", "fsproj", "vbproj", "sln", "suo", "slnx"],
    "wasm": ["wasm", "wat"],
    "proto": ["proto"],
    "gradle": ["gradle"],
    "clojure": ["clj", "cljs", "cljc", "edn"],
    "perl": ["pl", "pm"],
    "hcl": ["hcl"],
    "matlab": ["mat"],
    "assembly": ["asm", "s", "S", "nasm"],
    "fortran": ["f", "f90", "f95", "for"],
    "groovy": ["groovy"],
    "racket": ["rkt"],
    "scheme": ["scm", "ss"],
    "lisp": ["lisp", "el", "lsp", "fnl"],
    "powershell": ["ps1", "psm1", "psd1"],
    "latex": ["tex", "sty", "cls", "bib"],
    "typst": ["typ"],
    "d": ["d"],
    "mojo": ["mojo", "🔥"],
    "markdown": ["md", "markdown", "mdx", "mdc", "rst", "adoc", "org"],
    "json": ["json", "jsonc", "json5", "jsonl", "ndjson", "webmanifest", "har"],
    "yaml": ["yaml", "yml"],
    "toml": ["toml"],
    "settings": ["conf", "ini", "cfg", "properties", "prefs", "config"],
    "plist": ["plist", "entitlements", "xcprivacy"],
    "xcode": ["pbxproj", "xcconfig", "xcscheme", "xcworkspacedata", "xctestplan", "xcsettings"],
    "layout": ["storyboard", "xib", "nib"],
    "i18n": ["xcstrings", "strings", "stringsdict", "po", "pot", "ftl", "arb", "xliff", "xlf", "http", "rest"],
    "terminal": ["sh", "bash", "zsh", "fish", "nu", "ksh", "csh", "tcsh", "bat", "cmd", "command",
                 "bash_aliases", "bash_login", "bash_logout", "bash_profile", "bashrc", "brushrc",
                 "profile", "zlogin", "zlogout", "zprofile", "zsh_aliases", "zsh_histfile",
                 "zsh_history", "zshenv", "zshrc", "zimrc", "inputrc", "envrc"],
    "terraform": ["tf", "tfvars", "tfstate"],
    "graphql": ["gql", "graphql", "graphqls"],
    "prisma": ["prisma"],
    "nix": ["nix"],
    "storage": ["db", "sqlite", "sqlite3", "sql", "dat", "dbf", "mdb", "accdb", "pdb", "sav", "sdf",
                "RData", "rdata", "parquet", "arrow", "avro", "duckdb", "realm"],
    "table": ["csv", "tsv", "psv", "ssv", "xls", "xlsx", "numbers", "ods"],
    "document": ["doc", "docx", "odt", "rtf", "pages", "ppt", "pptx", "odp", "epub"],
    "pdf": ["pdf"],
    "text": ["txt", "text", "nfo"],
    "image": ["avif", "bmp", "gif", "heic", "heif", "ico", "icns", "j2k", "jfif", "jp2", "jpeg", "jpg",
              "jxl", "png", "psd", "qoi", "tiff", "tif", "webp", "raw", "cr2", "nef", "dng", "xcf",
              "sketch", "fig", "afdesign", "afphoto"],
    "svg": ["svg", "svgz", "eps", "ai"],
    "video": ["avi", "m4v", "mkv", "mov", "mp4", "webm", "wmv", "flv", "mpg", "mpeg", "gifv"],
    "audio": ["aac", "flac", "m4a", "mka", "mp3", "ogg", "opus", "wav", "wma", "wv", "aiff", "aif",
              "mid", "midi", "caf"],
    "font": ["otf", "ttf", "woff", "woff2", "eot", "ttc"],
    "archive": ["zip", "tar", "gz", "tgz", "bz2", "xz", "zst", "7z", "rar", "dmg", "pkg", "deb",
                "rpm", "apk", "ipa", "xip", "iso", "jar.gz", "tar.gz", "tar.xz", "tar.zst"],
    "lock": ["lock", "lockb", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "Cargo.lock",
             "Gemfile.lock", "Podfile.lock", "composer.lock", "poetry.lock", "uv.lock",
             "flake.lock", "mix.lock", "Package.resolved", "go.sum", "pubspec.lock", "deno.lock"],
    "key": ["pem", "key", "crt", "cer", "der", "p12", "pfx", "pub", "gpg", "asc", "sig", "keystore", "jks",
            "env", "env.local", "env.development", "env.production", "env.test", "env.example",
            "env.sample", "env.staging", "dev.vars"],
    "vcs": ["gitignore", "gitattributes", "gitmodules", "gitkeep", "gitconfig", "mailmap",
            "git-blame-ignore-revs", "COMMIT_EDITMSG", "EDIT_DESCRIPTION", "MERGE_MSG",
            "NOTES_EDITMSG", "TAG_EDITMSG", "patch", "gitlab-ci.yml", "gitlab-ci.yaml"],
    "ignore": ["dockerignore", "npmignore", "prettierignore", "eslintignore", "vscodeignore",
               "stylelintignore", "slugignore", "helmignore", "ignore", "rgignore", "fdignore"],
    "diff": ["diff", "rej", "orig"],
    "log": ["log", "out", "trace"],
    "notebook": ["ipynb"],
    "binary": ["exe", "dll", "so", "dylib", "o", "a", "lib", "bin", "obj", "elf", "wasm.bin", "class.bin"],
    "editorconfig": ["editorconfig"],
    "eslint": ["eslintrc", "eslintrc.js", "eslintrc.cjs", "eslintrc.json", "eslintrc.yml",
               "eslintrc.yaml", "eslint.config.js", "eslint.config.cjs", "eslint.config.mjs",
               "eslint.config.ts", "eslint.config.mts", "eslint.config.cts"],
    "prettier": ["prettierrc", "prettierrc.js", "prettierrc.cjs", "prettierrc.mjs", "prettierrc.json",
                 "prettierrc.json5", "prettierrc.toml", "prettierrc.yaml", "prettierrc.yml",
                 "prettier.config.js", "prettier.config.cjs", "prettier.config.mjs", "prettier.config.ts"],
    "stylelint": ["stylelintrc", "stylelintrc.js", "stylelintrc.cjs", "stylelintrc.mjs", "stylelintrc.json",
                  "stylelintrc.yaml", "stylelintrc.yml", "stylelint.config.js", "stylelint.config.cjs",
                  "stylelint.config.mjs"],
    "test": ["test.ts", "spec.ts", "test.tsx", "spec.tsx", "test.js", "spec.js", "test.jsx", "spec.jsx",
             "test.mjs", "spec.mjs", "test.cjs", "test.mts", "spec.mts", "e2e.ts", "e2e-spec.ts",
             "jest.config.js", "jest.config.ts", "jest.config.mjs", "jest.config.cjs",
             "vitest.config.ts", "vitest.config.js", "vitest.config.mts", "vitest.config.mjs",
             "playwright.config.ts", "playwright.config.js", "cypress.config.ts", "cypress.config.js",
             "karma.conf.js", "pytest.ini", "conftest.py", "snap"],
    "vite": ["vite.config.ts", "vite.config.js", "vite.config.mjs", "vite.config.mts", "vite.config.cjs"],
    "tailwind": ["tailwind.config.js", "tailwind.config.ts", "tailwind.config.cjs", "tailwind.config.mjs"],
    "tsconfig": ["tsconfig.json", "jsconfig.json", "tsconfig.base.json", "tsconfig.build.json",
                 "tsconfig.app.json", "tsconfig.node.json", "tsconfig.spec.json", "deno.json", "deno.jsonc"],
    "package": ["package.json", "bower.json", "composer.json", "pyproject.toml", "setup.py", "setup.cfg",
                "requirements.txt", "Pipfile", "pubspec.yaml", "mix.exs", "build.zig", "gleam.toml",
                "deps.edn", "project.clj", "build.sbt", "pom.xml", "gemspec"],
    "cargo": ["Cargo.toml", "rust-toolchain", "rust-toolchain.toml", "rustfmt.toml", "clippy.toml"],
    "swiftpm": ["Package.swift"],
    "node": ["nvmrc", "node-version", "npmrc", "yarnrc", "yarnrc.yml", "pnpmfile.cjs", "pnpm-workspace.yaml"],
    "storage_sql": [],
}

STEMS: dict[str, list[str]] = {
    "docker": ["Dockerfile", "Containerfile", "docker-compose.yml", "docker-compose.yaml",
               "compose.yml", "compose.yaml", "dockerfile"],
    "ruby": ["Gemfile", "Rakefile", "Podfile", "Brewfile", "Fastfile", "Appfile", "Matchfile",
             "Dangerfile", "Guardfile", "Vagrantfile", "config.ru"],
    "heroku": ["Procfile"],
    "make": ["Makefile", "makefile", "GNUmakefile", "justfile", "Justfile", ".justfile",
             "CMakeLists.txt", "Taskfile.yml", "Taskfile.yaml", "meson.build", "BUILD", "BUILD.bazel",
             "WORKSPACE", "Earthfile", "Tiltfile"],
    "readme": ["README", "README.md", "README.markdown", "README.txt", "README.rst", "readme.md",
               "Readme.md", "README.mdx"],
    "license": ["LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "LICENCE.md", "COPYING",
                "COPYING.md", "UNLICENSE", "license", "license.md", "NOTICE", "AUTHORS"],
    "changelog": ["CHANGELOG", "CHANGELOG.md", "CHANGES.md", "HISTORY.md", "RELEASES.md",
                  "changelog.md", "NEWS.md"],
    "claude": ["CLAUDE.md", "CLAUDE.local.md", "AGENTS.md", "AGENT.md", ".claude.json",
               "claude.json", ".mcp.json", "llms.txt"],
    "github": ["CODEOWNERS", "FUNDING.yml", "dependabot.yml", "pull_request_template.md",
               "PULL_REQUEST_TEMPLATE.md", "ISSUE_TEMPLATE.md"],
    "helm": ["Chart.yaml", "Chart.yml", "Chart.lock", "values.yaml", "values.yml", "helmfile.yaml",
             "helmfile.yml"],
    "settings": [".DS_Store", "Thumbs.db", "desktop.ini"],
    "dodo": ["dodo.json", "dodo.toml", ".dodo"],
}

# Every key we draw must resolve. Note `storage_sql` placeholder is dropped.
SUFFIXES.pop("storage_sql")


def associations() -> tuple[dict[str, str], dict[str, str]]:
    suffixes = {s: k for k, vals in SUFFIXES.items() for s in vals}
    stems = {s: k for k, vals in STEMS.items() for s in vals}
    return stems, suffixes


def build_icons(v: Variant, out_dir: Path) -> dict[str, str]:
    """Write the SVGs for one variant; return {icon_key: filename}."""
    st = STYLE[v.slug]
    c = dict(v.icons)
    c["accent"] = v.accent
    c["feather"] = v.feather
    out_dir.mkdir(parents=True, exist_ok=True)
    files: dict[str, str] = {}

    def write(name: str, body: str) -> str:
        (out_dir / f"{name}.svg").write_text(svg(body))
        return name

    for key, (label, roles) in BADGES.items():
        files[key] = write(key, badge(label, roles, c, st))
    for key, body in pictograms(c, st, v.accent, v.feather).items():
        files[key] = write(key, body)

    tab = folder_tab(v)
    write("folder", folder(v.feather, tab, st, False))
    write("folder_open", folder(v.feather, tab, st, True))
    for role in FOLDER_GROUPS:
        col = c[role]
        write(f"folder_{role}", folder(col, tab, st, False))
        write(f"folder_{role}_open", folder(col, tab, st, True))

    chev = mix(v.ui["muted"], v.ui["subtext"], 0.3)
    write("chevron_right", S("M6.25 4.25 10 8l-3.75 3.75", chev))
    write("chevron_down", S("M4.25 6.25 8 10l3.75-3.75", chev))
    return files


def icon_theme_family(variants: list[Variant], root: Path) -> dict:
    stems, suffixes = associations()
    themes = []
    for v in variants:
        rel = f"./icons/{v.slug}"
        files = build_icons(v, root / "icons" / v.slug)
        missing = {k for k in list(stems.values()) + list(suffixes.values()) if k not in files}
        if missing:
            raise SystemExit(f"icon keys without artwork: {sorted(missing)}")
        named = {}
        for role, names in FOLDER_GROUPS.items():
            for n in names:
                named[n] = {"collapsed": f"{rel}/folder_{role}.svg",
                            "expanded": f"{rel}/folder_{role}_open.svg"}
        themes.append({
            "name": f"{v.name} Icons",
            "appearance": v.appearance,
            "directory_icons": {"collapsed": f"{rel}/folder.svg", "expanded": f"{rel}/folder_open.svg"},
            "named_directory_icons": named,
            "chevron_icons": {"collapsed": f"{rel}/chevron_right.svg", "expanded": f"{rel}/chevron_down.svg"},
            "file_stems": stems,
            "file_suffixes": suffixes,
            "file_icons": {k: {"path": f"{rel}/{f}.svg"} for k, f in sorted(files.items())},
        })
    return {
        "$schema": "https://zed.dev/schema/icon_themes/v0.3.0.json",
        "name": "Dodo Icons",
        "author": "Chris Nicholson",
        "themes": themes,
    }
