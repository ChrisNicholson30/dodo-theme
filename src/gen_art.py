"""Turn the dodo mascot into half-block terminal art for the scripts' banners.

Each character cell shows two vertical pixels using ▀ / ▄ with separate
foreground and background colours. We emit four flavours:
  dodo-24bit.ans      truecolor
  dodo-256.ans        xterm-256 fallback (e.g. Terminal.app on older macOS)
  dodo-grey-24bit.ans desaturated ("extinct") for the uninstaller
  dodo-grey-256.ans
All lines are padded to the same visible width so scripts can place text
beside the bird.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from colors import desaturate, mix, rgb, to_hex, xterm256
from palette import DUSK

ESC = "\x1b"


def _load(src: Path, cols: int) -> tuple[list[list[tuple[int, int, int, int]]], int, int]:
    im = Image.open(src).convert("RGBA")
    alpha = im.getchannel("A").point(lambda a: 255 if a > 200 else 0)
    im = im.crop(alpha.getbbox())
    w, h = im.size
    rows_px = round(h / w * cols)
    rows_px += rows_px % 2
    small = im.convert("RGBa").resize((cols, rows_px), Image.LANCZOS).convert("RGBA")
    px = [[small.getpixel((x, y)) for x in range(cols)] for y in range(rows_px)]
    return px, cols, rows_px


def _grey(p):
    r, g, b, a = p
    y = int(0.299 * r + 0.587 * g + 0.114 * b)
    y = int(y * 0.85 + 20)
    return (y, y, y, a)


def render(px, cols: int, rows_px: int, mode: str, grey: bool) -> str:
    def code(p, layer: str) -> str:
        r, g, b, _ = _grey(p) if grey else p
        if mode == "24bit":
            return f"{ESC}[{38 if layer == 'fg' else 48};2;{r};{g};{b}m"
        return f"{ESC}[{38 if layer == 'fg' else 48};5;{xterm256(to_hex(r, g, b))}m"

    lines = []
    for y in range(0, rows_px, 2):
        line = ""
        for x in range(cols):
            top, bot = px[y][x], px[y + 1][x]
            t_on, b_on = top[3] >= 110, bot[3] >= 110
            if t_on and b_on:
                line += code(top, "fg") + code(bot, "bg") + "▀"
            elif t_on:
                line += f"{ESC}[49m" + code(top, "fg") + "▀"
            elif b_on:
                line += f"{ESC}[49m" + code(bot, "fg") + "▄"
            else:
                line += f"{ESC}[0m "
        lines.append(line + f"{ESC}[0m")
    # Trim fully blank rows at top/bottom.
    while lines and lines[0].replace(f"{ESC}[0m", "").strip() == "":
        lines.pop(0)
    while lines and lines[-1].replace(f"{ESC}[0m", "").strip() == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def build(src: Path, out_dir: Path, cols: int = 28) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    px, w, h = _load(src, cols)
    for grey in (False, True):
        for mode in ("24bit", "256"):
            name = f"dodo-{'grey-' if grey else ''}{mode}.ans"
            (out_dir / name).write_text(render(px, w, h, mode, grey))
    (out_dir / "WIDTH").write_text(f"{w}\n")


# ── wordmark ────────────────────────────────────────────────────────────────

_D = ["██████╗ ", "██╔══██╗", "██║  ██║", "██║  ██║", "██████╔╝", "╚═════╝ "]
_O = [" ██████╗ ", "██╔═══██╗", "██║   ██║", "██║   ██║", "╚██████╔╝", " ╚═════╝ "]
WORDMARK = [d + " " + o + " " + d + " " + o for d, o in zip(_D, _O)]

# Feather → lagoon → beak gold, following the house palette.
STOPS = [DUSK.feather, DUSK.accent, DUSK.syntax["function"]]
SHADOW = DUSK.ui["faint"]


def _grad(t: float) -> str:
    if t <= 0.5:
        return mix(STOPS[0], STOPS[1], t / 0.5)
    return mix(STOPS[1], STOPS[2], (t - 0.5) / 0.5)


def wordmark(mode: str, grey: bool) -> str:
    width = max(len(line) for line in WORDMARK)
    out = []
    for row, line in enumerate(WORDMARK):
        s = ""
        for x, ch in enumerate(line):
            if ch == " ":
                s += " "
                continue
            colour = _grad(x / (width - 1)) if ch == "█" else SHADOW
            if ch == "█" and row >= 3:  # subtle vertical falloff
                colour = mix(colour, "#000000", 0.08 * (row - 2))
            if grey:
                colour = desaturate(colour, 1.0)
            r, g, b = rgb(colour)
            code = f"38;2;{r};{g};{b}" if mode == "24bit" else f"38;5;{xterm256(colour)}"
            s += f"{ESC}[{code}m{ch}"
        out.append(s + f"{ESC}[0m")
    return "\n".join(out) + "\n"


def build_wordmark(out_dir: Path) -> None:
    for grey in (False, True):
        for mode in ("24bit", "256"):
            (out_dir / f"wordmark-{'grey-' if grey else ''}{mode}.ans").write_text(wordmark(mode, grey))
    (out_dir / "wordmark-plain.txt").write_text("\n".join(WORDMARK) + "\n")
