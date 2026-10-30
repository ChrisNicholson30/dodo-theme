<p align="center">
  <img src="assets/dodo.png" width="220" alt="Dodo, the mascot">
</p>

<h1 align="center">Dodo</h1>

<p align="center">
  <b>A matching theme suite for Zed, your terminal, and Xcode.</b><br>
  Claude Dark at heart · five variants · three dark, two light · hand-drawn file icons
</p>

<p align="center">
  <img src="assets/previews/zed-dusk.png" alt="Dodo Dusk in Zed">
</p>

---

## The flock

Each variant is a quiet grey canvas with a hint of warmth or coolness. The
colour lives in your code, not in a tint across the whole screen. Every
variant builds its syntax colours around its own accent, so they share a
family resemblance but aren't just the same theme at different brightness.

| | Variant | Mood | Accent | Canvas |
|---|---|---|---|---|
| 🌆 | **Dodo Dusk** | The original. Warm charcoal, an homage to Claude Dark | Claude coral `#d97757` | `#262624` |
| 🌌 | **Dodo Night** | Cool slate plumage after sundown | feather periwinkle `#8fa6ee` | `#1b1c21` |
| 🌋 | **Dodo Obsidian** | Near-black (OLED-friendly) and restrained, lit by one amber ember | beak amber `#eda157` | `#111111` |
| 🌅 | **Dodo Dawn** | Ivory paper and terracotta, Claude's light mode | terracotta `#c15f3c` | `#faf9f5` |
| 🌫️ | **Dodo Mist** | Cool sea-fog grey with slate-feather ink | slate blue `#4d63b3` | `#f7f8fa` |

<table>
  <tr>
    <td><img src="assets/previews/zed-night.png" alt="Dodo Night"></td>
    <td><img src="assets/previews/zed-obsidian.png" alt="Dodo Obsidian"></td>
  </tr>
  <tr>
    <td><img src="assets/previews/zed-dawn.png" alt="Dodo Dawn"></td>
    <td><img src="assets/previews/zed-mist.png" alt="Dodo Mist"></td>
  </tr>
</table>

### Colours taken from the bird

| Part of the dodo | Used for |
|---|---|
| slate-blue **feathers** | folders, properties, links |
| honey-gold **beak** | functions, in every variant |
| **ember**, Claude coral | the accent: cursor, keywords (Dusk) |
| cream **belly** | the foreground text |
| Mauritius **lagoon** teal | types |
| cinnamon **eye** | parameters (in italics) |

## What's inside

| | |
|---|---|
| **Zed** | 5 themes plus 5 matching **icon themes**: 168 hand-tuned 16px SVGs per variant (840 in total), covering 400+ file names and extensions, with tinted folders for 140+ well-known directory names |
| **Terminal** | Terminal.app · iTerm2 (with light/dark **auto-switching** profiles) · Ghostty · Kitty · Alacritty · WezTerm · Warp |
| **Xcode** | 5 `.xccolortheme`s. Your own symbols are shown in full colour and Apple's SDK symbols in a softer shade, so your code stands out |
| **Scripts** | `install.sh` · `update.sh` (with optional automatic updates) · `uninstall.sh` |

<p align="center"><img src="assets/previews/icons.png" alt="The Dodo icon sets, one per variant"></p>

### The details

Ideas borrowed from the best themes around, then adapted:

- **Neutral overlays** (from Rosé Pine). Hover, active and selected states are
  tints of the text colour, not the accent, so the UI never takes on a colour
  cast.
- **Dimmed punctuation** (from Tokyo Night). Brackets and commas fade back so
  identifiers stand out. Brackets are one step brighter than delimiters.
- **Italics with a purpose** (from Catppuccin). Comments, parameters, `self`/`this`,
  control flow (`return`, `await`, `if`, `import`) and built-in types are
  italic. Plain keywords are not.
- **One ember** (from Vesper). Obsidian holds back on colour on purpose: amber
  keywords, wheat-coloured functions, and very little else.
- **Layered depth** (from Claude). The title bar and status bar sit darkest,
  then panels, then the editor, with popovers floating just above it.
- **Thought-out extras**: different colours for read and write highlights,
  rainbow-bracket accents, vim/helix mode pills, diff hunks, conflict
  markers, eight distinct collaborator cursors, inlay hints in a soft pill,
  and translucent scrollbars and minimap.
- **Checked contrast**: body text is 12–14:1 on every variant. Each build
  prints a WCAG report (`python3 src/build.py --check`).
- **Icons that vary a little per theme**: language badges are tinted
  rounded squares (the radius and fill weight change per variant). Folders
  are feather-blue with a small tab in the variant's accent colour. Obsidian
  uses outlined folders. `CLAUDE.md` / `AGENTS.md` get their own coral spark.

## Install

```bash
git clone https://github.com/chrisnicholson30/dodo-theme ~/.dodo-theme
~/.dodo-theme/install.sh
```

or in one line (this clones into `~/.dodo-theme` for you):

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/chrisnicholson30/dodo-theme/main/install.sh)"
```

<p align="center"><img src="assets/previews/banner-install.png" width="720" alt="The installer"></p>

The installer:

1. **detects** which of Zed, Terminal.app, iTerm2, Ghostty, Kitty, Alacritty,
   WezTerm, Warp and Xcode you have;
2. **asks before doing anything**, and lets you pick individual apps;
3. **links** the Zed extension and the terminal themes back to this folder
   (copying only where an app requires it), so updates arrive in place;
4. asks for your **favourite dark and light variants**, and can switch Dodo
   on in Zed, Ghostty and Terminal.app straight away. Zed and Ghostty then
   follow your system's light/dark setting. Every edit it makes is marked
   `added by dodo-theme` and is reversed by `uninstall.sh`. If you have
   already set a theme yourself, it leaves it alone;
5. offers **automatic updates**.

```text
install.sh [--zed] [--terminal] [--xcode] [--all] [--force]
           [-y|--yes] [--dark=Dusk|Night|Obsidian] [--light=Dawn|Mist]
           [--apply|--no-apply] [--auto-update[=daily|weekly|hourly]|--no-auto-update]
           [--list] [-q|--quiet]
```

### Turning it on by hand

| App | How |
|---|---|
| Zed | `⌘K ⌘T` → *Dodo …*, and *icon theme selector: toggle* → *Dodo … Icons*. Or in `settings.json`:<br>`"theme": { "mode": "system", "light": "Dodo Dawn", "dark": "Dodo Dusk" },`<br>`"icon_theme": { "mode": "system", "light": "Dodo Dawn Icons", "dark": "Dodo Dusk Icons" }` |
| Ghostty | `theme = light:Dodo Dawn,dark:Dodo Dusk` |
| iTerm2 | Settings › Profiles › **Dodo Auto (Dusk ⇄ Dawn)** (follows the macOS appearance), or any single variant |
| Terminal.app | Settings › Profiles › *Dodo Dusk* › **Default** |
| Kitty | `kitten themes --reload-in=all "Dodo Dusk"` |
| Alacritty | `general.import = ["~/.config/alacritty/themes/dodo/dodo-dusk.toml"]` |
| WezTerm | `config.color_scheme = "Dodo Dusk"` |
| Warp | Settings › Appearance › Themes › *Dodo Dusk* |
| Xcode | restart Xcode → Settings › Themes › *Dodo Dusk* |

## Update

```bash
~/.dodo-theme/update.sh            # pull, then refresh every installed app
~/.dodo-theme/update.sh --check    # is anything new? (exit code 10 = yes)
```

Zed and the text-based terminals are **symlinked** to this folder, so a
`git pull` updates them immediately (Zed reloads the theme while it's
running). Copies that apps require (Xcode, iTerm2) are refreshed.
Terminal.app profiles are re-imported only when they actually changed. The
updater fast-forwards only: it never overwrites local edits or rewrites your
history, and it tells you if something is in the way.

### Automatic updates

```bash
~/.dodo-theme/update.sh --auto daily    # or weekly / hourly
~/.dodo-theme/update.sh --auto status
~/.dodo-theme/update.sh --auto off
```

This uses a **launchd** agent on macOS, a **systemd user timer** on Linux, and
**cron** as a fallback. It runs quietly, logs to
`~/.local/state/dodo-theme/update.log`, and shows a desktop notification
when a new version arrives.

## Uninstall

```bash
~/.dodo-theme/uninstall.sh          # shows exactly what will go, then asks
~/.dodo-theme/uninstall.sh --purge  # …and deletes the Dodo folder too
```

It removes only what the installer recorded: its own symlinks and copies,
the lines it marked, and the update schedule. It also puts back any file
the installer had moved aside. The banner turns grey, because the dodo is
going extinct again.

## Make it yours

Every file is generated from a single palette:

```bash
pip install pillow           # fonttools / pygments are only needed for glyphs & previews
$EDITOR src/palette.py       # change a hex value
python3 src/build.py --check # regenerate Zed + icons + 7 terminals + Xcode, then check contrast
python3 src/preview.py && node src/shoot.cjs   # re-render the README screenshots
```

```
src/palette.py      the five variants: UI greys, accent, syntax, ANSI, icon colours
src/gen_zed.py      Zed theme family (every style key Zed currently supports)
src/gen_icons.py    the 16px icon system + 400+ file associations
src/gen_terminal.py Terminal.app · iTerm2 · Ghostty · Kitty · Alacritty · WezTerm · Warp
src/gen_xcode.py    Xcode themes
src/gen_art.py      the half-block pixel dodo + gradient wordmark used by the scripts
lib/dodo.sh         shared shell library (bash 3.2-safe, so it runs on stock macOS)
```

## Credits

- The dodo mascot is by the author.
- The badge lettering is built from outlines of **Inter Display** by Rasmus
  Andersson (SIL Open Font License 1.1).
- Inspired by Claude's own dark and light themes, and by Catppuccin, Rosé
  Pine, Tokyo Night, Vesper and Kanagawa.

MIT © Chris Nicholson
