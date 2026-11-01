#!/usr/bin/env python3
"""Render README previews: a Zed-style mock per variant + an icon sheet.

    python3 src/preview.py && node src/shoot.cjs

Needs `pip install pygments` (only for previews; not for building themes).
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from pygments.lexers import TypeScriptLexer  # noqa: E402
from pygments.token import Token  # noqa: E402

from colors import alpha, flatten, mix  # noqa: E402
from palette import VARIANTS, Variant  # noqa: E402

OUT = ROOT / "assets" / "previews"

CODE = '''import { Flock, type Bird } from "./mauritius";

/** A dodo never forgets where it left the theme. */
export class Dodo implements Bird {
  private readonly feathers = new Map<string, number>();
  static extinct = false;

  constructor(public name: string, private age = 1662) {}

  async waddle(steps: number): Promise<string> {
    const pattern = /^(left|right)+$/gi;
    for (let i = 0; i < steps; i++) {
      if (this.age > 400 && !Dodo.extinct) {
        await this.rest(`step ${i}\\n`);
      }
    }
    return this.name ?? "anonymous dodo";
  }
}
'''

TREE = [
    (0, "folder_open", "dodo-theme", True),
    (1, "folder_orange", ".github", False),
    (1, "folder_teal_open", "src", True),
    (2, "typescript", "dodo.ts", False),
    (2, "react_ts", "Flock.tsx", False),
    (2, "rust", "beak.rs", False),
    (2, "python", "plumage.py", False),
    (2, "swift", "Island.swift", False),
    (2, "test", "dodo.test.ts", False),
    (1, "folder_green", "tests", False),
    (1, "folder_purple", "assets", False),
    (1, "folder_gray", "node_modules", False),
    (1, "agent", "AGENTS.md", False),
    (1, "readme", "README.md", False),
    (1, "package", "package.json", False),
    (1, "tsconfig", "tsconfig.json", False),
    (1, "lock", "pnpm-lock.yaml", False),
    (1, "docker", "Dockerfile", False),
    (1, "terminal", "install.sh", False),
    (1, "license", "LICENSE", False),
    (1, "vcs", ".gitignore", False),
]


def tok_color(v: Variant, ttype, text: str, nxt: str, prev: str) -> tuple[str, bool]:
    s = v.syntax
    t = str(ttype)
    if ttype in Token.Comment:
        return (s["comment_doc"] if text.startswith("/**") else s["comment"]), True
    if ttype in Token.Keyword.Constant:
        return s["constant"], False
    if ttype in Token.Keyword.Type:
        return s["type"], True
    if ttype in Token.Keyword:
        italic = text in ("return", "await", "if", "for", "import", "export", "from")
        return s["keyword"], italic
    if ttype in Token.String.Regex:
        return s["regex"], False
    if ttype in Token.String.Escape:
        return s["string_escape"], False
    if ttype in Token.String:
        return s["string"], False
    if ttype in Token.Number:
        return s["number"], False
    if ttype in Token.Operator:
        return s["operator"], False
    if ttype in Token.Punctuation:
        return (s["bracket"] if text in "(){}[]<>" else s["punctuation"]), False
    if ttype in Token.Name.Builtin.Pseudo or text == "this":
        return s["variable_special"], True
    if ttype in Token.Name:
        if nxt.startswith("(") or nxt.startswith("<string"):
            return s["function"], False
        if text[:1].isupper():
            return s["type"], False
        if prev == ".":
            return s["property"], False
        if text in ("steps", "name", "age"):
            return s["parameter"], True
        return s["variable"], False
    return v.ui["text"], False


def highlight(v: Variant, code: str = CODE) -> list[str]:
    toks = list(TypeScriptLexer().get_tokens(code))
    lines, cur = [], ""
    for i, (tt, text) in enumerate(toks):
        nxt = toks[i + 1][1] if i + 1 < len(toks) else ""
        prev = toks[i - 1][1] if i else ""
        parts = text.split("\n")
        for j, part in enumerate(parts):
            if j:
                lines.append(cur)
                cur = ""
            if part:
                c, it = tok_color(v, tt, part, nxt, prev)
                style = f"color:{c}" + (";font-style:italic" if it else "")
                cur += f'<span style="{style}">{html.escape(part)}</span>'
    if cur:
        lines.append(cur)
    return lines


def icon(v: Variant, name: str, size: int = 16) -> str:
    return f'<img src="../../zed/icons/{v.slug}/{name}.svg" width="{size}" height="{size}">'


def zed_mock(v: Variant) -> str:
    th = json.loads((ROOT / "zed/themes/dodo.json").read_text())
    st = next(t for t in th["themes"] if t["name"] == v.name)["style"]
    u = v.ui
    bg = u["base"]
    sel = flatten(st["players"][0]["selection"], bg)
    active = flatten(st["editor.active_line.background"], bg)
    hover = flatten(st["ghost_element.selected"], u["mantle"])

    rows = []
    for depth, ic, name, opened in TREE:
        chev = "chevron_down" if opened else ("chevron_right" if ic.startswith("folder") else None)
        chev_html = icon(v, chev, 14) if chev else '<span style="width:14px;display:inline-block"></span>'
        selected = name == "dodo.ts"
        rows.append(
            f'<div class="row" style="padding-left:{8 + depth * 14}px;'
            f'{"background:" + hover + ";box-shadow:inset 1px 0 0 " + v.accent if selected else ""}">'
            f'{chev_html}{icon(v, ic)}<span style="color:{u["text"] if selected else u["subtext"]}">{name}</span></div>')

    code_lines = highlight(v)
    gutter_marks = {3: "added", 4: "added", 11: "modified", 12: "modified", 13: "modified"}
    editor = []
    for i, line in enumerate(code_lines):
        n = i + 1
        is_active = n == 11
        mark = gutter_marks.get(n)
        bar = f'<span class="gm" style="background:{v.status[mark]}"></span>' if mark else '<span class="gm"></span>'
        ln_col = st["editor.active_line_number"] if is_active else st["editor.line_number"]
        content = line or "&nbsp;"
        if n == 10:
            content = content.replace("waddle", f'<span style="background:{sel}">waddle</span>', 1)
        cursor = f'<span class="cur" style="background:{v.accent}"></span>' if is_active else ""
        hint = (f' <span style="color:{v.status["hint"]};background:{alpha(v.status["hint"], 0.12)};'
                f'font-style:italic;border-radius:3px;padding:0 4px;font-size:11px">: RegExp</span>') if n == 11 else ""
        diag = (f' <span style="color:{v.status["warning"]};font-style:italic;opacity:.85;font-size:11.5px">'
                f'  ● `age` is suspiciously ancient</span>') if n == 13 else ""
        editor.append(
            f'<div class="cl" style="{"background:" + active if is_active else ""}">{bar}'
            f'<span class="ln" style="color:{ln_col}">{n}</span><span class="code">{content}{cursor}{hint}{diag}</span></div>')

    a = v.ansi
    term = f'''
<div><span style="color:{a["green"]}">➜</span> <span style="color:{a["cyan"]};font-weight:600">dodo-theme</span> <span style="color:{a["blue"]}">git:(</span><span style="color:{a["red"]}">main</span><span style="color:{a["blue"]})</span> <span style="color:{a["yellow"]}">✗</span> ./install.sh --all</div>
<div><span style="color:{v.accent}">◆</span> <span style="color:{u["text"]}">Zed</span> <span style="color:{a["bright_black"]}">·····························</span> <span style="color:{a["green"]}">✓ linked</span></div>
<div><span style="color:{v.accent}">◆</span> <span style="color:{u["text"]}">Ghostty · Kitty · iTerm2</span> <span style="color:{a["bright_black"]}">·············</span> <span style="color:{a["green"]}">✓ 15 themes</span></div>
<div><span style="color:{v.accent}">◆</span> <span style="color:{u["text"]}">Xcode</span> <span style="color:{a["bright_black"]}">···························</span> <span style="color:{a["yellow"]}">! restart Xcode</span></div>
<div style="margin-top:6px">{"".join(f'<span class="sw" style="background:{a[k]}"></span>' for k in ["black","red","green","yellow","blue","magenta","cyan","white"])}</div>
<div>{"".join(f'<span class="sw" style="background:{a["bright_" + k]}"></span>' for k in ["black","red","green","yellow","blue","magenta","cyan","white"])}</div>'''

    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1280px;height:800px;background:{st["background"]};font:13px/1 "Inter",system-ui,sans-serif;color:{u["text"]};overflow:hidden}}
.title{{height:34px;background:{st["title_bar.background"]};border-bottom:1px solid {st["border"]};display:flex;align-items:center;padding:0 14px;gap:8px;color:{u["subtext"]};font-size:12.5px}}
.dot{{width:12px;height:12px;border-radius:50%;display:inline-block}}
.main{{display:flex;height:calc(800px - 34px - 26px)}}
.panel{{width:250px;background:{st["panel.background"]};border-right:1px solid {st["border"]};padding-top:6px}}
.row{{height:24px;display:flex;align-items:center;gap:6px;font-size:13px}}
.row img{{flex:none}}
.right{{flex:1;display:flex;flex-direction:column;min-width:0}}
.tabs{{height:34px;background:{st["tab_bar.background"]};display:flex;border-bottom:1px solid {st["border"]}}}
.tab{{display:flex;align-items:center;gap:6px;padding:0 14px;font-size:12.5px;color:{u["muted"]};border-right:1px solid {st["border"]}}}
.tab.on{{background:{st["tab.active_background"]};color:{u["text"]};margin-bottom:-1px}}
.crumbs{{height:30px;display:flex;align-items:center;gap:6px;padding:0 14px;color:{u["muted"]};font-size:12px;background:{st["toolbar.background"]}}}
.editor{{flex:1;background:{st["editor.background"]};font:13.5px/21px "JetBrains Mono",monospace;padding-top:4px;overflow:hidden}}
.cl{{display:flex;align-items:center;height:21px;white-space:pre}}
.gm{{width:3px;height:21px;margin-left:4px;margin-right:6px;display:inline-block;border-radius:1px}}
.ln{{width:30px;text-align:right;margin-right:22px;font-size:12.5px}}
.cur{{display:inline-block;width:2px;height:17px;vertical-align:-3px;margin-left:-1px}}
.term{{height:190px;background:{st["terminal.background"]};border-top:1px solid {st["border"]};font:13px/20px "JetBrains Mono",monospace;padding:8px 16px;color:{st["terminal.foreground"]}}}
.term .tbar{{font:12px "Inter",system-ui,sans-serif;color:{u["muted"]};margin-bottom:6px;display:flex;gap:14px}}
.sw{{display:inline-block;width:34px;height:14px;margin-right:4px;border-radius:3px}}
.status{{height:26px;background:{st["status_bar.background"]};border-top:1px solid {st["border"]};display:flex;align-items:center;padding:0 12px;gap:16px;color:{u["muted"]};font-size:12px}}
.pill{{padding:2px 8px;border-radius:4px;background:{st["vim.normal.background"]};color:{st["vim.normal.foreground"]};font-weight:600;font-size:11px}}
</style></head><body>
<div class="title"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span>
<span style="margin-left:14px;color:{u["text"]};font-weight:600">dodo-theme</span><span>›</span><span>{icon(v, "vcs", 14)}</span><span>main</span>
<span style="margin-left:auto;color:{v.accent};font-weight:600">{v.name}</span></div>
<div class="main"><div class="panel">{"".join(rows)}</div>
<div class="right"><div class="tabs">
<div class="tab on">{icon(v, "typescript")}dodo.ts</div><div class="tab">{icon(v, "rust")}beak.rs</div><div class="tab">{icon(v, "markdown")}CHANGES.md</div><div class="tab">{icon(v, "toml")}Cargo.toml</div></div>
<div class="crumbs">src <span>›</span> {icon(v, "typescript", 14)} dodo.ts <span>›</span> <span style="color:{v.syntax["type"]}">Dodo</span> <span>›</span> <span style="color:{v.syntax["function"]}">waddle</span></div>
<div class="editor">{"".join(editor)}</div>
<div class="term"><div class="tbar"><span style="color:{u["text"]}">Terminal</span><span>zsh</span></div>{term}</div></div></div>
<div class="status"><span class="pill">NORMAL</span><span style="color:{v.status["error"]}">⨯ 0</span><span style="color:{v.status["warning"]}">⚠ 1</span>
<span style="margin-left:auto">Ln 11, Col 28</span><span>TypeScript</span><span style="color:{v.accent}">◆ Dodo</span></div>
</body></html>'''


def icon_sheet() -> str:
    data = json.loads((ROOT / "zed/icon_themes/dodo-icons.json").read_text())
    keys = sorted(data["themes"][0]["file_icons"].keys())
    cols = []
    for v in VARIANTS:
        folder = ["folder", "folder_open"] + [f"folder_{r}" for r in
                                              ("teal", "green", "blue", "purple", "orange", "gray", "brown",
                                               "yellow", "sky", "pink", "lavender", "red", "amber", "accent")]
        cells = "".join(f'<div class="c" title="{k}">{icon(v, k, 32)}<span>{k}</span></div>' for k in folder + keys)
        cols.append(f'<section style="background:{v.ui["mantle"]};color:{v.ui["muted"]}">'
                    f'<h2 style="color:{v.ui["text"]}">{v.name} <em style="color:{v.accent}">Icons</em></h2>'
                    f'<div class="g">{cells}</div></section>')
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;box-sizing:border-box}} body{{width:1600px;font:11px Inter,sans-serif;background:#000}}
section{{padding:22px 26px}} h2{{font:600 18px Inter;margin-bottom:14px}} h2 em{{font-style:normal}}
.g{{display:grid;grid-template-columns:repeat(16,1fr);gap:10px 6px}}
.c{{display:flex;flex-direction:column;align-items:center;gap:5px;text-align:center;overflow:hidden}}
.c span{{font-size:9.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:92px}}
</style></head><body>{"".join(cols)}</body></html>'''


def palette_sheet() -> str:
    cards = []
    for v in VARIANTS:
        u, s = v.ui, v.syntax
        swatches = "".join(
            f'<div class="swatch"><i style="background:{c}"></i><span>{name}</span>'
            f'<code>{c}</code></div>' for name, c in [
                ("Accent", v.accent), ("Canvas", u["base"]),
                ("Functions", s["function"]), ("Types", s["type"]),
                ("Strings", s["string"]), ("Comments", s["comment"]),
            ])
        sample = "\n".join(highlight(v, '''/** At home on the island. */
export class Dodo {
  readonly home = "Mauritius";
  readonly feathers = 42;

  waddle(steps: number): string {
    return `steps: ${steps}`;
  }
}
'''))
        cards.append(f'<section style="background:{u["base"]};color:{u["text"]};'
                     f'border-color:{u["border"]}"><h2 style="color:{v.accent}">{v.name}</h2>'
                     f'<p style="color:{u["subtext"]}">{v.tagline}</p><div class="swatches">{swatches}</div>'
                     f'<pre>{sample}</pre></section>')
    return '''<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0}body{width:1600px;padding:36px;background:#e6e9e3;
color:#293229;font:14px system-ui,sans-serif}header{display:flex;align-items:center;gap:20px;margin-bottom:28px}
header img{width:66px;height:72px;object-fit:contain}h1{font-size:32px;letter-spacing:-1px}
header p{margin-top:5px;color:#52604e}.cards{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
section{padding:22px 18px;border:1px solid;border-radius:10px;overflow:hidden}h2{font-size:21px}
section p{font-size:13px;line-height:1.6;min-height:64px;margin-top:10px}.swatches{display:grid;gap:10px;margin:10px 0 24px}
.swatch{display:flex;align-items:center;gap:8px;font-size:12px}.swatch i{width:18px;height:18px;
border-radius:4px;box-shadow:inset 0 0 0 1px #88888844}.swatch code{margin-left:auto;font-size:11px}
pre{font:10px/1.9 "SFMono-Regular",monospace;white-space:pre-wrap;overflow-wrap:anywhere}
</style></head><body><header><img src="../dodo.png" alt="Dodo"><div><h1>The island palette</h1>
<p>Five quiet canvases. Lagoon teal, feather blue, sand gold, olive and sea fog.</p></div></header>
<div class="cards">''' + "".join(cards) + "</div></body></html>"


def ansi_html(text: str) -> str:
    """Render the SGR subset used by the generated 24-bit terminal art."""
    chunks, styles, pos = [], {}, 0
    for match in re.finditer(r"\x1b\[([0-9;]*)m", text):
        chunks.append(f'<span style="{";".join(f"{k}:{v}" for k, v in styles.items())}">'
                      f'{html.escape(text[pos:match.start()])}</span>')
        codes = [int(c) for c in match[1].split(";") if c]
        if not codes or codes == [0]:
            styles.clear()
        elif codes[0] in (38, 48) and len(codes) == 5 and codes[1] == 2:
            styles["color" if codes[0] == 38 else "background"] = f'rgb({codes[2]},{codes[3]},{codes[4]})'
        elif codes == [49]:
            styles.pop("background", None)
        pos = match.end()
    chunks.append(html.escape(text[pos:]))
    return "".join(chunks)


def banner_mock(mode: str) -> str:
    v = VARIANTS[0]
    grey = "grey-" if mode == "uninstall" else ""
    art = (ROOT / f"assets/term/dodo-{grey}24bit.ans").read_text().splitlines()
    word = (ROOT / f"assets/term/wordmark-{grey}24bit.ans").read_text().splitlines()
    title = "A theme suite for Zed · Terminal · Xcode" if mode == "install" else "Going extinct… (on this machine only)"
    subtitle = "five variants · three dark · two light" if mode == "install" else "Your own configs stay yours. Only Dodo leaves."
    right = [""] * 4 + word + ["", title, subtitle]
    bird_width = int((ROOT / "assets/term/WIDTH").read_text())
    lines = [ansi_html(art[i] if i < len(art) else " " * bird_width) + "   "
             + ansi_html(right[i] if i < len(right) else "") for i in range(max(len(art), len(right)))]
    if mode == "install":
        detail = "".join(f'<div style="color:{a.accent if a.is_dark else mix(a.accent, v.ui["text"], 0.55)}"><b>{a.name}</b>'
                         f'<span style="color:{v.ui["subtext"]}">  {a.tagline}</span></div>' for a in VARIANTS)
        detail += '<p>./install.sh &nbsp; · &nbsp; ./update.sh &nbsp; · &nbsp; ./uninstall.sh</p>'
    else:
        detail = '<b>The dodo has left the building.</b><p>Missed it already? ./install.sh brings it back from extinction.</p>'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0}}body{{width:1600px;padding:36px;background:{v.ui["base"]};
color:{v.ui["text"]};font:17px/1.6 Menlo,monospace}}
pre{{font:17px/20px Menlo,monospace;margin-bottom:30px}}p{{color:{v.ui["muted"]};margin-top:18px}}
</style></head><body><pre>{"\n".join(lines)}</pre><div>{detail}</div></body></html>'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for v in VARIANTS:
        (OUT / f"zed-{v.slug}.html").write_text(zed_mock(v))
    (OUT / "icons.html").write_text(icon_sheet())
    (OUT / "palettes.html").write_text(palette_sheet())
    for mode in ("install", "uninstall"):
        (OUT / f"banner-{mode}.html").write_text(banner_mock(mode))
    print(f"wrote previews to {OUT}")


if __name__ == "__main__":
    main()
