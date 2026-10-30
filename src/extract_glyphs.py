"""Bake the handful of letter outlines the badge icons need into glyphs.json.

Run once (needs `pip install fonttools` and Inter Display installed); the
JSON is committed so normal builds have no font dependency.
Lettering: Inter Display ExtraBold, © The Inter Project Authors, SIL OFL 1.1.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

CHARS = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789#+λ."
)

CANDIDATES = [
    "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf",
    str(Path.home() / "Library/Fonts/InterDisplay-ExtraBold.otf"),
    "/Library/Fonts/InterDisplay-ExtraBold.otf",
]


def main() -> None:
    path = next((p for p in CANDIDATES if Path(p).exists()), None)
    if not path:
        sys.exit("Inter Display ExtraBold not found — glyphs.json is already committed, no need to re-run.")
    font = TTFont(path)
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    out = {
        "unitsPerEm": font["head"].unitsPerEm,
        "capHeight": font["OS/2"].sCapHeight,
        "xHeight": font["OS/2"].sxHeight,
        "glyphs": {},
    }
    for ch in CHARS:
        name = cmap.get(ord(ch))
        if not name:
            continue
        pen = SVGPathPen(gs, ntos=lambda n: f"{n:g}")
        gs[name].draw(pen)
        out["glyphs"][ch] = {"d": pen.getCommands(), "adv": gs[name].width}
    dest = Path(__file__).with_name("glyphs.json")
    dest.write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False))
    print(f"wrote {dest} ({len(out['glyphs'])} glyphs)")


if __name__ == "__main__":
    main()
