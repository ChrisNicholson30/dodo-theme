"""Xcode .xccolortheme files.

Xcode separates *your* symbols from *system* (SDK) symbols. Dodo keeps your
code in full colour and renders Apple's SDK symbols in a softened tone of
the same hue — so the eye lands on what you wrote.
"""

from __future__ import annotations

import plistlib
from pathlib import Path

from colors import mix, rgbf
from palette import Variant

MONO = "SFMono-Regular"
SIZE = 13.0


def col(hex_: str, a: float = 1.0) -> str:
    r, g, b = rgbf(hex_)
    return f"{r:.6f} {g:.6f} {b:.6f} {a:g}"


def font(face: str = "Regular", size: float = SIZE) -> str:
    return f"SFMono-{face} - {size:.1f}"


def theme(v: Variant) -> bytes:
    u, s, st = v.ui, v.syntax, v.status
    system = lambda c: mix(c, u["subtext"], 0.38)  # noqa: E731

    colors = {
        "xcode.syntax.plain": s["variable"],
        "xcode.syntax.comment": s["comment"],
        "xcode.syntax.comment.doc": s["comment_doc"],
        "xcode.syntax.comment.doc.keyword": s["preproc"],
        "xcode.syntax.mark": v.accent,
        "xcode.syntax.keyword": s["keyword"],
        "xcode.syntax.preprocessor": s["preproc"],
        "xcode.syntax.attribute": s["attribute"],
        "xcode.syntax.string": s["string"],
        "xcode.syntax.character": s["string_escape"],
        "xcode.syntax.number": s["number"],
        "xcode.syntax.url": s["link_uri"],
        "xcode.syntax.markup.code": s["string_special"],
        "xcode.syntax.regex": s["regex"],
        "xcode.syntax.regex.capturename": s["property"],
        "xcode.syntax.regex.charname": s["string_escape"],
        "xcode.syntax.regex.number": s["number"],
        "xcode.syntax.regex.other": s["punctuation"],
        "xcode.syntax.declaration.type": s["type"],
        "xcode.syntax.declaration.other": s["function"],
        "xcode.syntax.identifier.class": s["type"],
        "xcode.syntax.identifier.class.system": system(s["type"]),
        "xcode.syntax.identifier.type": s["type"],
        "xcode.syntax.identifier.type.system": system(s["type"]),
        "xcode.syntax.identifier.function": s["function"],
        "xcode.syntax.identifier.function.system": system(s["function"]),
        "xcode.syntax.identifier.constant": s["constant"],
        "xcode.syntax.identifier.constant.system": system(s["constant"]),
        "xcode.syntax.identifier.variable": s["property"],
        "xcode.syntax.identifier.variable.system": system(s["property"]),
        "xcode.syntax.identifier.macro": s["preproc"],
        "xcode.syntax.identifier.macro.system": system(s["preproc"]),
    }
    italic = {"xcode.syntax.comment", "xcode.syntax.comment.doc", "xcode.syntax.attribute"}
    semibold = {"xcode.syntax.keyword", "xcode.syntax.declaration.type"}
    bold = {"xcode.syntax.mark", "xcode.syntax.comment.doc.keyword"}

    def face(k: str) -> str:
        if k in italic:
            return font("RegularItalic")
        if k in bold:
            return font("Bold")
        if k in semibold:
            return font("Semibold")
        return font()

    sel = mix(u["base"], v.accent, 0.28 if v.is_dark else 0.2)
    sys_ui = ".AppleSystemUIFont"
    p = {
        "DVTFontAndColorVersion": 1,
        "DVTLineSpacing": 1.15,
        "DVTSourceTextBackground": col(u["base"]),
        "DVTSourceTextCurrentLineHighlightColor": col(u["text"], 0.045),
        "DVTSourceTextInsertionPointColor": col(v.accent),
        "DVTSourceTextInvisiblesColor": col(u["faint"]),
        "DVTSourceTextSelectionColor": col(sel),
        "DVTSourceTextBlockDimBackgroundColor": col(u["muted"]),
        "DVTSourceTextSyntaxColors": {k: col(c) for k, c in colors.items()},
        "DVTSourceTextSyntaxFonts": {k: face(k) for k in colors},
        "DVTDebuggerInstructionPointerColor": col(st["success"]),
        "DVTScrollbarMarkerAnalyzerColor": col(s["number"]),
        "DVTScrollbarMarkerBreakpointColor": col(v.accent),
        "DVTScrollbarMarkerDiffColor": col(st["modified"]),
        "DVTScrollbarMarkerDiffConflictColor": col(st["conflict"]),
        "DVTScrollbarMarkerErrorColor": col(st["error"]),
        "DVTScrollbarMarkerRuntimeIssueColor": col(s["number"]),
        "DVTScrollbarMarkerSourceControlColor": col(u["muted"]),
        "DVTScrollbarMarkerWarningColor": col(st["warning"]),
        # Console
        "DVTConsoleTextBackgroundColor": col(u["base"]),
        "DVTConsoleTextInsertionPointColor": col(v.accent),
        "DVTConsoleTextSelectionColor": col(sel),
        "DVTConsoleDebuggerInputTextColor": col(u["text"]),
        "DVTConsoleDebuggerInputTextFont": font("Semibold"),
        "DVTConsoleDebuggerOutputTextColor": col(u["subtext"]),
        "DVTConsoleDebuggerOutputTextFont": font(),
        "DVTConsoleDebuggerPromptTextColor": col(v.accent),
        "DVTConsoleDebuggerPromptTextFont": font("Bold"),
        "DVTConsoleExectuableInputTextColor": col(u["text"]),
        "DVTConsoleExectuableInputTextFont": font(),
        "DVTConsoleExectuableOutputTextColor": col(u["text"]),
        "DVTConsoleExectuableOutputTextFont": font(),
        # Rendered documentation comments / playground markup
        "DVTMarkupTextBackgroundColor": col(u["mantle"]),
        "DVTMarkupTextBorderColor": col(u["border"]),
        "DVTMarkupTextCodeFont": font(size=11.0),
        "DVTMarkupTextEmphasisColor": col(u["text"]),
        "DVTMarkupTextEmphasisFont": f"{sys_ui}-Italic - 11.0",
        "DVTMarkupTextInlineCodeColor": col(s["string_special"]),
        "DVTMarkupTextLinkColor": col(s["link"]),
        "DVTMarkupTextLinkFont": f"{sys_ui} - 11.0",
        "DVTMarkupTextNormalColor": col(u["text"]),
        "DVTMarkupTextNormalFont": f"{sys_ui} - 11.0",
        "DVTMarkupTextOtherHeadingColor": col(u["text"], 0.75),
        "DVTMarkupTextOtherHeadingFont": f"{sys_ui} - 15.4",
        "DVTMarkupTextPrimaryHeadingColor": col(s["heading"]),
        "DVTMarkupTextPrimaryHeadingFont": f"{sys_ui} - 26.4",
        "DVTMarkupTextSecondaryHeadingColor": col(u["text"]),
        "DVTMarkupTextSecondaryHeadingFont": f"{sys_ui} - 19.8",
        "DVTMarkupTextStrongColor": col(u["text"]),
        "DVTMarkupTextStrongFont": f"{sys_ui}-Bold - 11.0",
    }
    return plistlib.dumps(p, fmt=plistlib.FMT_XML)


def build(variants: list[Variant], root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for v in variants:
        (root / f"{v.name}.xccolortheme").write_bytes(theme(v))
