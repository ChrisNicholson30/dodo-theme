"""Zed theme family + extension manifest."""

from __future__ import annotations

from colors import alpha, mix
from palette import Variant

TRANSPARENT = "#00000000"


def _status(v: Variant, key: str, bg_a: float, border_a: float) -> dict[str, str]:
    c = v.status[key]
    return {key: c, f"{key}.background": alpha(c, bg_a), f"{key}.border": alpha(c, border_a)}


def style(v: Variant) -> dict:
    u, s, a, st = v.ui, v.syntax, v.ansi, v.status
    dark = v.is_dark
    acc = v.accent
    # Overlays are neutral (text-coloured) so hover/active never tints the UI.
    over = lambda x: alpha(u["text"], x)  # noqa: E731

    style: dict = {
        "background.appearance": "opaque",
        "accents": [alpha(c, 0.85 if dark else 0.9) for c in (
            s["function"], s["keyword"], s["type"], s["number"], s["string"], s["property"],
        )],
        # ── chrome ──────────────────────────────────────────────────────────
        "background": u["mantle"],
        "surface.background": u["mantle"],
        "elevated_surface.background": u["surface0"],
        "border": u["border"],
        "border.variant": u["border_variant"],
        "border.focused": alpha(acc, 0.55),
        "border.selected": alpha(acc, 0.7),
        "border.transparent": TRANSPARENT,
        "border.disabled": u["border_variant"],
        "element.background": u["surface0"],
        "element.hover": over(0.06 if dark else 0.05),
        "element.active": over(0.10 if dark else 0.08),
        "element.selected": over(0.09 if dark else 0.07),
        "element.selection_background": alpha(acc, 0.28 if dark else 0.22),
        "element.disabled": alpha(u["surface0"], 0.5),
        "drop_target.background": alpha(acc, 0.12),
        "drop_target.border": alpha(acc, 0.6),
        "ghost_element.background": TRANSPARENT,
        "ghost_element.hover": over(0.06 if dark else 0.05),
        "ghost_element.active": over(0.10 if dark else 0.08),
        "ghost_element.selected": over(0.08 if dark else 0.065),
        "ghost_element.disabled": TRANSPARENT,
        "text": u["text"],
        "text.muted": u["subtext"],
        "text.placeholder": u["muted"],
        "text.disabled": u["faint"],
        "text.accent": acc,
        "icon": u["subtext"],
        "icon.muted": u["muted"],
        "icon.disabled": u["faint"],
        "icon.placeholder": u["muted"],
        "icon.accent": acc,
        "debugger.accent": st["error"],
        "status_bar.background": u["crust"],
        "title_bar.background": u["crust"],
        "title_bar.inactive_background": u["crust"],
        "toolbar.background": u["base"],
        "tab_bar.background": u["mantle"],
        "tab.inactive_background": u["mantle"],
        "tab.active_background": u["base"],
        "search.match_background": alpha(s["function"], 0.22 if dark else 0.28),
        "search.active_match_background": alpha(acc, 0.42 if dark else 0.36),
        "panel.background": u["mantle"],
        "panel.focused_border": alpha(acc, 0.65),
        "panel.indent_guide": alpha(u["text"], 0.07),
        "panel.indent_guide_hover": alpha(u["text"], 0.2),
        "panel.indent_guide_active": alpha(u["text"], 0.14),
        "panel.overlay_background": u["surface0"],
        "panel.overlay_hover": u["surface1"],
        "pane.focused_border": alpha(acc, 0.35),
        "pane_group.border": u["border"],
        "scrollbar.thumb.background": over(0.10 if dark else 0.14),
        "scrollbar.thumb.hover_background": over(0.18 if dark else 0.22),
        "scrollbar.thumb.active_background": over(0.26 if dark else 0.3),
        "scrollbar.thumb.border": TRANSPARENT,
        "scrollbar.track.background": TRANSPARENT,
        "scrollbar.track.border": TRANSPARENT,
        "minimap.thumb.background": over(0.08 if dark else 0.1),
        "minimap.thumb.hover_background": over(0.14 if dark else 0.16),
        "minimap.thumb.active_background": over(0.2 if dark else 0.22),
        "minimap.thumb.border": TRANSPARENT,
        # ── editor ──────────────────────────────────────────────────────────
        "editor.foreground": u["text"],
        "editor.background": u["base"],
        "editor.gutter.background": u["base"],
        "editor.subheader.background": u["mantle"],
        "editor.active_line.background": over(0.035 if dark else 0.04),
        "editor.highlighted_line.background": alpha(acc, 0.08),
        "editor.debugger_active_line.background": alpha(st["warning"], 0.12),
        "editor.line_number": u["faint"],
        "editor.active_line_number": u["subtext"],
        "editor.hover_line_number": u["muted"],
        "editor.invisible": alpha(u["muted"], 0.45),
        "editor.wrap_guide": alpha(u["text"], 0.05),
        "editor.active_wrap_guide": alpha(u["text"], 0.1),
        "editor.indent_guide": alpha(u["text"], 0.06),
        "editor.indent_guide_active": alpha(u["text"], 0.16),
        "editor.document_highlight.read_background": alpha(s["property"], 0.14 if dark else 0.16),
        "editor.document_highlight.write_background": alpha(s["keyword"], 0.16 if dark else 0.16),
        "editor.document_highlight.bracket_background": alpha(acc, 0.18),
        "editor.code_lens.foreground": u["muted"],
        "editor.diff_hunk.added.background": alpha(st["added"], 0.10 if dark else 0.13),
        "editor.diff_hunk.added.hollow_background": alpha(st["added"], 0.04),
        "editor.diff_hunk.added.hollow_border": alpha(st["added"], 0.4),
        "editor.diff_hunk.deleted.background": alpha(st["deleted"], 0.10 if dark else 0.12),
        "editor.diff_hunk.deleted.hollow_background": alpha(st["deleted"], 0.04),
        "editor.diff_hunk.deleted.hollow_border": alpha(st["deleted"], 0.4),
        "link_text.hover": s["link_uri"],
        # ── terminal ────────────────────────────────────────────────────────
        "terminal.background": u["base"],
        "terminal.ansi.background": u["base"],
        "terminal.foreground": u["text"],
        "terminal.bright_foreground": a["bright_white"],
        "terminal.dim_foreground": u["muted"],
        # ── version control ────────────────────────────────────────────────
        "version_control.added": st["added"],
        "version_control.modified": st["modified"],
        "version_control.deleted": st["deleted"],
        "version_control.renamed": st["renamed"],
        "version_control.conflict": st["conflict"],
        "version_control.ignored": u["faint"],
        "version_control.word_added": alpha(st["added"], 0.28),
        "version_control.word_deleted": alpha(st["deleted"], 0.28),
        "version_control.conflict_marker.ours": alpha(st["added"], 0.16),
        "version_control.conflict_marker.theirs": alpha(st["info"], 0.16),
        # ── vim / helix mode pills ─────────────────────────────────────────
        "vim.normal.background": alpha(acc, 0.18),
        "vim.normal.foreground": acc,
        "vim.insert.background": alpha(st["success"], 0.18),
        "vim.insert.foreground": st["success"],
        "vim.replace.background": alpha(st["error"], 0.18),
        "vim.replace.foreground": st["error"],
        "vim.visual.background": alpha(s["number"], 0.18),
        "vim.visual.foreground": s["number"],
        "vim.visual_line.background": alpha(s["number"], 0.18),
        "vim.visual_line.foreground": s["number"],
        "vim.visual_block.background": alpha(s["number"], 0.18),
        "vim.visual_block.foreground": s["number"],
        "vim.helix_normal.background": alpha(acc, 0.18),
        "vim.helix_normal.foreground": acc,
        "vim.helix_select.background": alpha(s["number"], 0.18),
        "vim.helix_select.foreground": s["number"],
        "vim.yank.background": alpha(s["function"], 0.25),
        "vim.helix_jump_label.foreground": st["error"],
    }

    for name in ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"):
        style[f"terminal.ansi.{name}"] = a[name]
        style[f"terminal.ansi.bright_{name}"] = a[f"bright_{name}"]
        style[f"terminal.ansi.dim_{name}"] = mix(a[name], u["base"], 0.35)

    for key, bg_a, bd_a in (
        ("error", 0.10, 0.45), ("warning", 0.10, 0.45), ("info", 0.10, 0.45),
        ("success", 0.10, 0.45), ("hint", 0.08, 0.35),
    ):
        style.update(_status(v, key, bg_a, bd_a))
    for key, src in (("created", "added"), ("modified", "modified"), ("deleted", "deleted"),
                     ("renamed", "renamed"), ("conflict", "conflict")):
        c = st[src]
        style.update({key: c, f"{key}.background": alpha(c, 0.1), f"{key}.border": alpha(c, 0.45)})
    for key, c in (("hidden", u["faint"]), ("ignored", u["faint"]),
                   ("predictive", u["muted"]), ("unreachable", u["muted"])):
        style.update({key: c, f"{key}.background": alpha(c, 0.08), f"{key}.border": alpha(c, 0.3)})

    style["players"] = [
        {"cursor": c, "background": c, "selection": alpha(c, 0.26 if dark else 0.2)}
        for c in v.players
    ]
    style["syntax"] = syntax(v)
    return style


def _tok(color: str, italic: bool = False, weight: int | None = None) -> dict:
    t: dict = {"color": color}
    if italic:
        t["font_style"] = "italic"
    if weight:
        t["font_weight"] = weight
    return t


def syntax(v: Variant) -> dict:
    s = v.syntax
    u = v.ui
    return {
        "attribute": _tok(s["attribute"], italic=True),
        "boolean": _tok(s["constant"]),
        "comment": _tok(s["comment"], italic=True),
        "comment.doc": _tok(s["comment_doc"], italic=True),
        "constant": _tok(s["constant"]),
        "constant.builtin": _tok(s["constant"]),
        "constructor": _tok(s["function"]),
        "embedded": _tok(u["text"]),
        "emphasis": _tok(s["parameter"], italic=True),
        "emphasis.strong": _tok(s["function"], weight=700),
        "enum": _tok(s["type"]),
        "function": _tok(s["function"]),
        "function.builtin": _tok(s["function"]),
        "function.call": _tok(s["function"]),
        "function.definition": _tok(s["function"]),
        "function.method": _tok(s["function"]),
        "function.macro": _tok(s["preproc"]),
        "function.special": _tok(s["preproc"]),
        "hint": _tok(v.status["hint"], italic=True),
        "keyword": _tok(s["keyword"]),
        "keyword.control": _tok(s["keyword"], italic=True),
        "keyword.import": _tok(s["keyword"], italic=True),
        "keyword.exception": _tok(s["keyword"], italic=True),
        "keyword.return": _tok(s["keyword"], italic=True),
        "keyword.operator": _tok(s["operator"]),
        "label": _tok(s["label"], italic=True),
        "link_text": _tok(s["link"], italic=True),
        "link_uri": _tok(s["link_uri"]),
        "namespace": _tok(s["namespace"]),
        "module": _tok(s["namespace"]),
        "number": _tok(s["number"]),
        "operator": _tok(s["operator"]),
        "predictive": _tok(u["muted"], italic=True),
        "preproc": _tok(s["preproc"]),
        "primary": _tok(u["text"]),
        "property": _tok(s["property"]),
        "punctuation": _tok(s["punctuation"]),
        "punctuation.bracket": _tok(s["bracket"]),
        "punctuation.delimiter": _tok(s["punctuation"]),
        "punctuation.list_marker": _tok(s["list_marker"]),
        "punctuation.markup": _tok(s["list_marker"]),
        "punctuation.special": _tok(s["string_escape"]),
        "selector": _tok(s["selector"]),
        "selector.pseudo": _tok(s["selector_pseudo"], italic=True),
        "string": _tok(s["string"]),
        "string.doc": _tok(s["comment_doc"], italic=True),
        "string.escape": _tok(s["string_escape"]),
        "string.regex": _tok(s["regex"]),
        "string.special": _tok(s["string_special"]),
        "string.special.symbol": _tok(s["constant"]),
        "string.special.path": _tok(s["link_uri"]),
        "string.special.url": _tok(s["link_uri"]),
        "tag": _tok(s["tag"]),
        "tag.doctype": _tok(s["punctuation"], italic=True),
        "text.literal": _tok(s["literal"]),
        "title": _tok(s["heading"], weight=700),
        "type": _tok(s["type"]),
        "type.builtin": _tok(s["type"], italic=True),
        "type.interface": _tok(s["type"], italic=True),
        "type.super": _tok(s["type"], italic=True),
        "variable": _tok(s["variable"]),
        "variable.member": _tok(s["property"]),
        "variable.parameter": _tok(s["parameter"], italic=True),
        "variable.special": _tok(s["variable_special"], italic=True),
        "variable.builtin": _tok(s["variable_special"], italic=True),
        "variant": _tok(s["constant"]),
        "diff.plus": _tok(v.status["added"]),
        "diff.minus": _tok(v.status["deleted"]),
        "attribute.jsx": _tok(s["attribute"], italic=True),
    }


def theme_family(variants: list[Variant]) -> dict:
    return {
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": "Dodo",
        "author": "Chris Nicholson",
        "themes": [
            {"name": v.name, "appearance": v.appearance, "style": style(v)} for v in variants
        ],
    }


def extension_toml(version: str) -> str:
    return f'''id = "dodo-theme"
name = "Dodo"
version = "{version}"
schema_version = 1
authors = ["Chris Nicholson"]
description = "Dodo — five island-inspired themes (Dusk, Night, Obsidian, Dawn, Mist) with quiet mineral surfaces and matching file icons."
repository = "https://github.com/chrisnicholson30/dodo-theme"
'''
