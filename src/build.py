#!/usr/bin/env python3
"""Build every Dodo artefact from src/palette.py.

    python3 src/build.py            # regenerate everything
    python3 src/build.py --check    # also print a WCAG contrast report

Outputs (all committed, so end users never need Python):
    zed/            Zed extension: themes, icon themes, 16px SVG icons
    terminal/       Terminal.app, iTerm2, Ghostty, Kitty, Alacritty, WezTerm, Warp
    xcode/          .xccolortheme files
    assets/term/    half-block dodo art used by install/update/uninstall
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import gen_art  # noqa: E402
import gen_icons  # noqa: E402
import gen_terminal  # noqa: E402
import gen_xcode  # noqa: E402
import gen_zed  # noqa: E402
from colors import contrast  # noqa: E402
from palette import VARIANTS  # noqa: E402


def version() -> str:
    return (ROOT / "VERSION").read_text().strip()


def contrast_report() -> None:
    print("\n  WCAG contrast against the editor background")
    for v in VARIANTS:
        bg = v.ui["base"]
        worst = sorted(((contrast(c, bg), k) for k, c in v.syntax.items()))[:3]
        print(f"  {v.name:<14} text {contrast(v.ui['text'], bg):5.2f}  "
              f"comment {contrast(v.syntax['comment'], bg):4.2f}  lowest: "
              + ", ".join(f"{k} {r:.2f}" for r, k in worst))


def validate(zed: Path) -> None:
    """Fail loudly on anything Zed/Xcode/terminals would silently ignore."""
    import plistlib
    import re
    import tomllib

    hexre = re.compile(r"^#[0-9a-f]{6}([0-9a-f]{2})?$")
    errors: list[str] = []

    def walk(node, where):
        if isinstance(node, dict):
            for k, val in node.items():
                walk(val, f"{where}.{k}")
        elif isinstance(node, list):
            for i, val in enumerate(node):
                walk(val, f"{where}[{i}]")
        elif isinstance(node, str) and node.startswith("#") and not hexre.match(node):
            errors.append(f"bad colour {node!r} at {where}")

    themes = json.loads((zed / "themes" / "dodo.json").read_text())
    walk(themes, "themes")
    icons = json.loads((zed / "icon_themes" / "dodo-icons.json").read_text())
    for t in icons["themes"]:
        paths = [d["path"] for d in t["file_icons"].values()]
        for group in [t["directory_icons"], t["chevron_icons"], *t["named_directory_icons"].values()]:
            paths += [p for p in group.values() if p]
        errors += [f"missing icon {p}" for p in paths if not (zed / p).is_file()]
        errors += [f"unmapped key {k}" for k in set(t["file_suffixes"].values()) | set(t["file_stems"].values())
                   if k not in t["file_icons"]]
    manifest = tomllib.loads((zed / "extension.toml").read_text())
    if manifest.get("schema_version") != 1 or manifest.get("id") != "dodo-theme":
        errors.append("extension.toml: unexpected id/schema_version")
    for f in [*(ROOT / "xcode").glob("*.xccolortheme"), *(ROOT / "terminal").rglob("*.terminal"),
              *(ROOT / "terminal").rglob("*.itermcolors")]:
        plistlib.loads(f.read_bytes())
    for f in [*(ROOT / "terminal" / "alacritty").glob("*.toml"), *(ROOT / "terminal" / "wezterm").glob("*.toml")]:
        tomllib.loads(f.read_text())
    if errors:
        raise SystemExit("validation failed:\n  " + "\n  ".join(errors))


def main() -> None:
    zed = ROOT / "zed"
    shutil.rmtree(zed / "icons", ignore_errors=True)
    (zed / "themes").mkdir(parents=True, exist_ok=True)
    (zed / "icon_themes").mkdir(parents=True, exist_ok=True)

    (zed / "themes" / "dodo.json").write_text(
        json.dumps(gen_zed.theme_family(VARIANTS), indent=2) + "\n")
    (zed / "icon_themes" / "dodo-icons.json").write_text(
        json.dumps(gen_icons.icon_theme_family(VARIANTS, zed), indent=2) + "\n")
    (zed / "extension.toml").write_text(gen_zed.extension_toml(version()))
    shutil.copy(ROOT / "LICENSE", zed / "LICENSE")

    gen_terminal.build(VARIANTS, ROOT / "terminal")
    gen_xcode.build(VARIANTS, ROOT / "xcode")
    gen_art.build(ROOT / "assets" / "dodo.png", ROOT / "assets" / "term")
    gen_art.build_wordmark(ROOT / "assets" / "term")

    validate(zed)
    n_icons = len(list((zed / "icons").rglob("*.svg")))
    print(f"  ✓ Zed     {len(VARIANTS)} themes, {len(VARIANTS)} icon themes, {n_icons} SVGs")
    print(f"  ✓ Terminal  {len(list((ROOT / 'terminal').rglob('*.*')))} files across 7 apps")
    print(f"  ✓ Xcode   {len(VARIANTS)} .xccolortheme")
    print("  ✓ Art     assets/term/*.ans")
    print("  ✓ Valid   colours, icon paths, plists, TOML")
    if "--check" in sys.argv:
        contrast_report()


if __name__ == "__main__":
    main()
