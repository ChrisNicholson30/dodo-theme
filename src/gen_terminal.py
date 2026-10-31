"""Terminal themes: Terminal.app, iTerm2, Ghostty, Kitty, Alacritty, WezTerm, Warp."""

from __future__ import annotations

import json
import plistlib
from pathlib import Path

from colors import mix, rgbf
from palette import Variant

ORDER = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]


def ansi16(v: Variant) -> list[str]:
    return [v.ansi[n] for n in ORDER] + [v.ansi[f"bright_{n}"] for n in ORDER]


def roles(v: Variant) -> dict[str, str]:
    u = v.ui
    return dict(
        bg=u["base"],
        fg=u["text"],
        bold=v.ansi["bright_white"] if v.is_dark else u["text"],
        cursor=v.accent,
        cursor_text=u["base"],
        selection=mix(u["base"], v.accent, 0.26 if v.is_dark else 0.2),
        selection_text=u["text"],
        link=v.syntax["link_uri"],
        dim=u["muted"],
        mantle=u["mantle"],
        crust=u["crust"],
        border=u["border"],
        surface=u["surface1"],
    )


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-")


# ── Terminal.app ────────────────────────────────────────────────────────────

def _archive(obj: dict, classname: str) -> bytes:
    obj = dict(obj)
    obj["$class"] = plistlib.UID(2)
    return plistlib.dumps({
        "$archiver": "NSKeyedArchiver",
        "$version": 100000,
        "$top": {"root": plistlib.UID(1)},
        "$objects": ["$null", obj, {"$classname": classname, "$classes": [classname, "NSObject"]}],
    }, fmt=plistlib.FMT_BINARY)


def ns_color(hex_: str) -> bytes:
    r, g, b = rgbf(hex_)
    # NSColorSpace 2 = device RGB: hex values land on screen as written.
    return _archive({"NSColorSpace": 2, "NSRGB": f"{r:.6f} {g:.6f} {b:.6f}\x00".encode()}, "NSColor")


def ns_font(name: str, size: float) -> bytes:
    return _archive({"NSName": name, "NSSize": size, "NSfFlags": 16}, "NSFont")


def terminal_app(v: Variant) -> bytes:
    r = roles(v)
    names = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]
    p: dict = {
        "name": v.name,
        "type": "Window Settings",
        "ProfileCurrentVersion": 2.07,
        "BackgroundColor": ns_color(r["bg"]),
        "TextColor": ns_color(r["fg"]),
        "TextBoldColor": ns_color(r["bold"]),
        "CursorColor": ns_color(r["cursor"]),
        "SelectionColor": ns_color(r["selection"]),
        "Font": ns_font("SFMono-Regular", 13.0),
        "FontAntialias": True,
        "FontWidthSpacing": 1.0,
        "FontHeightSpacing": 1.1,
        "CursorType": 0,  # Block cursor.
        "CursorBlink": True,
        "UseBrightBold": True,
        "columnCount": 120,
        "rowCount": 34,
        "BackgroundBlur": 0.0,
        "ShowActiveProcessInTitle": True,
        "ShowWindowSettingsNameInTitle": False,
    }
    for i, n in enumerate(names):
        p[f"ANSI{n}Color"] = ns_color(v.ansi[n.lower()])
        p[f"ANSIBright{n}Color"] = ns_color(v.ansi[f"bright_{n.lower()}"])
    return plistlib.dumps(p, fmt=plistlib.FMT_XML)


# ── iTerm2 ─────────────────────────────────────────────────────────────────

def _it(hex_: str, a: float = 1.0) -> dict:
    r, g, b = rgbf(hex_)
    return {"Red Component": r, "Green Component": g, "Blue Component": b,
            "Alpha Component": a, "Color Space": "sRGB"}


def iterm_colors(v: Variant) -> dict:
    r = roles(v)
    d = {f"Ansi {i} Color": _it(c) for i, c in enumerate(ansi16(v))}
    d.update({
        "Background Color": _it(r["bg"]),
        "Foreground Color": _it(r["fg"]),
        "Bold Color": _it(r["bold"]),
        "Cursor Color": _it(r["cursor"]),
        "Cursor Text Color": _it(r["cursor_text"]),
        "Selection Color": _it(r["selection"]),
        "Selected Text Color": _it(r["selection_text"]),
        "Link Color": _it(r["link"]),
        "Badge Color": _it(v.accent, 0.5),
        "Cursor Guide Color": _it(v.ui["text"], 0.06),
        "Match Background Color": _it(v.syntax["function"], 0.35),
        "Tab Color": _it(r["mantle"]),
        "Underline Color": _it(v.accent),
    })
    return d


def iterm_dynamic_profiles(variants: list[Variant]) -> dict:
    by = {v.slug: v for v in variants}
    profiles = []
    for v in variants:
        prof = {
            "Name": v.name,
            "Guid": f"dodo-theme-{v.slug}",
            "Dynamic Profile Parent Name": "Default",
            "Tags": ["Dodo"],
            "Use Separate Colors for Light and Dark Mode": False,
            "Use Tab Color": False,
            "Minimum Contrast": 0,
            "Use Bright Bold": True,
        }
        prof.update(iterm_colors(v))
        profiles.append(prof)
    # Follow-the-system pairs: macOS appearance switches the palette live.
    pairs = [(d.slug, li.slug) for d in variants if d.is_dark for li in variants if not li.is_dark]
    for dark, light in pairs:
        prof = {
            "Name": f"Dodo Auto ({by[dark].name.split()[-1]} ⇄ {by[light].name.split()[-1]})",
            "Guid": f"dodo-theme-auto-{dark}-{light}",
            "Dynamic Profile Parent Name": "Default",
            "Tags": ["Dodo"],
            "Use Separate Colors for Light and Dark Mode": True,
            "Use Bright Bold": True,
        }
        for k, val in iterm_colors(by[dark]).items():
            prof[f"{k} (Dark)"] = val
        for k, val in iterm_colors(by[light]).items():
            prof[f"{k} (Light)"] = val
        profiles.append(prof)
    return {"Profiles": profiles}


# ── text-based terminals ───────────────────────────────────────────────────

def ghostty(v: Variant) -> str:
    r = roles(v)
    lines = [f"# {v.name} — {v.tagline}", "# https://github.com/chrisnicholson30/dodo-theme", ""]
    lines += [f"palette = {i}={c}" for i, c in enumerate(ansi16(v))]
    lines += [
        f"background = {r['bg']}",
        f"foreground = {r['fg']}",
        f"cursor-color = {r['cursor']}",
        f"cursor-text = {r['cursor_text']}",
        f"selection-background = {r['selection']}",
        f"selection-foreground = {r['selection_text']}",
        f"split-divider-color = {r['border']}",
    ]
    return "\n".join(lines) + "\n"


def kitty(v: Variant) -> str:
    r = roles(v)
    a = ansi16(v)
    out = [
        f"## name: {v.name}",
        "## author: Chris Nicholson",
        "## license: MIT",
        "## upstream: https://github.com/chrisnicholson30/dodo-theme",
        f"## blurb: {v.tagline}",
        "",
        f"foreground            {r['fg']}",
        f"background            {r['bg']}",
        f"selection_foreground  {r['selection_text']}",
        f"selection_background  {r['selection']}",
        f"cursor                {r['cursor']}",
        f"cursor_text_color     {r['cursor_text']}",
        f"url_color             {r['link']}",
        f"active_border_color   {v.accent}",
        f"inactive_border_color {r['border']}",
        f"bell_border_color     {v.status['warning']}",
        f"wayland_titlebar_color {r['crust']}",
        f"macos_titlebar_color  {r['crust']}",
        f"tab_bar_background    {r['crust']}",
        f"active_tab_foreground   {r['fg']}",
        f"active_tab_background   {r['bg']}",
        f"inactive_tab_foreground {r['dim']}",
        f"inactive_tab_background {r['mantle']}",
        f"mark1_foreground {r['bg']}",
        f"mark1_background {v.accent}",
        f"mark2_foreground {r['bg']}",
        f"mark2_background {v.syntax['function']}",
        f"mark3_foreground {r['bg']}",
        f"mark3_background {v.syntax['type']}",
        "",
    ]
    out += [f"color{i:<2} {c}" for i, c in enumerate(a)]
    return "\n".join(out) + "\n"


def alacritty(v: Variant) -> str:
    r = roles(v)

    def block(prefix: str) -> list[str]:
        return [f'{n} = "{v.ansi[prefix + n]}"' for n in ORDER]

    dim = [f'{n} = "{mix(v.ansi[n], r["bg"], 0.35)}"' for n in ORDER]
    return "\n".join([
        f"# {v.name} — {v.tagline}",
        "# https://github.com/chrisnicholson30/dodo-theme",
        "",
        "[colors.primary]",
        f'background = "{r["bg"]}"',
        f'foreground = "{r["fg"]}"',
        f'dim_foreground = "{r["dim"]}"',
        f'bright_foreground = "{v.ansi["bright_white"]}"',
        "",
        "[colors.cursor]",
        f'cursor = "{r["cursor"]}"',
        f'text = "{r["cursor_text"]}"',
        "",
        "[colors.vi_mode_cursor]",
        f'cursor = "{v.syntax["function"]}"',
        f'text = "{r["cursor_text"]}"',
        "",
        "[colors.selection]",
        f'background = "{r["selection"]}"',
        f'text = "{r["selection_text"]}"',
        "",
        "[colors.search.matches]",
        f'background = "{mix(r["bg"], v.syntax["function"], 0.35)}"',
        f'foreground = "{r["fg"]}"',
        "",
        "[colors.search.focused_match]",
        f'background = "{v.accent}"',
        f'foreground = "{r["bg"]}"',
        "",
        "[colors.footer_bar]",
        f'background = "{r["mantle"]}"',
        f'foreground = "{r["fg"]}"',
        "",
        "[colors.hints.start]",
        f'background = "{v.syntax["function"]}"',
        f'foreground = "{r["bg"]}"',
        "",
        "[colors.hints.end]",
        f'background = "{r["surface"]}"',
        f'foreground = "{r["fg"]}"',
        "",
        "[colors.normal]", *block(""), "",
        "[colors.bright]", *block("bright_"), "",
        "[colors.dim]", *dim, "",
    ])


def wezterm(v: Variant) -> str:
    r = roles(v)
    a = ansi16(v)
    q = lambda xs: "[" + ", ".join(f'"{x}"' for x in xs) + "]"  # noqa: E731
    return "\n".join([
        f"# {v.name} — {v.tagline}",
        "[colors]",
        f'foreground = "{r["fg"]}"',
        f'background = "{r["bg"]}"',
        f'cursor_bg = "{r["cursor"]}"',
        f'cursor_fg = "{r["cursor_text"]}"',
        f'cursor_border = "{r["cursor"]}"',
        f'selection_fg = "{r["selection_text"]}"',
        f'selection_bg = "{r["selection"]}"',
        f'scrollbar_thumb = "{r["surface"]}"',
        f'split = "{r["border"]}"',
        f'compose_cursor = "{v.syntax["function"]}"',
        f"ansi = {q(a[:8])}",
        f"brights = {q(a[8:])}",
        "",
        "[colors.tab_bar]",
        f'background = "{r["crust"]}"',
        f'inactive_tab_edge = "{r["border"]}"',
        "",
        "[colors.tab_bar.active_tab]",
        f'bg_color = "{r["bg"]}"',
        f'fg_color = "{r["fg"]}"',
        "",
        "[colors.tab_bar.inactive_tab]",
        f'bg_color = "{r["mantle"]}"',
        f'fg_color = "{r["dim"]}"',
        "",
        "[colors.tab_bar.inactive_tab_hover]",
        f'bg_color = "{r["surface"]}"',
        f'fg_color = "{r["fg"]}"',
        "",
        "[colors.tab_bar.new_tab]",
        f'bg_color = "{r["crust"]}"',
        f'fg_color = "{r["dim"]}"',
        "",
        "[colors.tab_bar.new_tab_hover]",
        f'bg_color = "{r["surface"]}"',
        f'fg_color = "{r["fg"]}"',
        "",
        "[metadata]",
        f'name = "{v.name}"',
        'author = "Chris Nicholson"',
        'origin_url = "https://github.com/chrisnicholson30/dodo-theme"',
        "",
    ])


def warp(v: Variant) -> str:
    r = roles(v)

    def block(prefix: str) -> list[str]:
        return [f"    {n}: '{v.ansi[prefix + n]}'" for n in ORDER]

    return "\n".join([
        f"# {v.name} — {v.tagline}",
        f"name: {v.name}",
        f"accent: '{v.accent}'",
        f"cursor: '{r['cursor']}'",
        f"background: '{r['bg']}'",
        f"foreground: '{r['fg']}'",
        f"details: {'darker' if v.is_dark else 'lighter'}",
        "terminal_colors:",
        "  normal:", *block(""),
        "  bright:", *block("bright_"),
        "",
    ])


def build(variants: list[Variant], root: Path) -> None:
    dirs = {k: root / k for k in ("terminal-app", "iterm2", "ghostty", "kitty", "alacritty", "wezterm", "warp")}
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    for v in variants:
        (dirs["terminal-app"] / f"{v.name}.terminal").write_bytes(terminal_app(v))
        (dirs["iterm2"] / f"{v.name}.itermcolors").write_bytes(
            plistlib.dumps(iterm_colors(v), fmt=plistlib.FMT_XML))
        (dirs["ghostty"] / v.name).write_text(ghostty(v))
        (dirs["kitty"] / f"{v.name}.conf").write_text(kitty(v))
        (dirs["alacritty"] / f"{slugify(v.name)}.toml").write_text(alacritty(v))
        (dirs["wezterm"] / f"{v.name}.toml").write_text(wezterm(v))
        (dirs["warp"] / f"{slugify(v.name).replace('-', '_')}.yaml").write_text(warp(v))
    (dirs["iterm2"] / "dodo-dynamic-profiles.json").write_text(
        json.dumps(iterm_dynamic_profiles(variants), indent=2, ensure_ascii=False) + "\n")
