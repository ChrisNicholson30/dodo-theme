#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
#  Dodo · installer
#
#    ./install.sh                 interactive: detects your apps, asks first
#    ./install.sh --all --yes     everything found, no questions
#    ./install.sh --zed           just Zed (also: --terminal, --xcode)
#
#  Remote one-liner (clones to ~/.dodo-theme, then runs this script):
#    bash -c "$(curl -fsSL https://raw.githubusercontent.com/chrisnicholson30/dodo-theme/main/install.sh)"
# ─────────────────────────────────────────────────────────────────────────────

usage() {
  cat <<'EOF'
Usage: install.sh [options]

  Components (default: everything detected)
    --zed               Zed theme + icon themes (linked, so updates are live)
    --terminal          Terminal.app, iTerm2, Ghostty, Kitty, Alacritty, WezTerm, Warp
    --xcode             Xcode colour themes
    --all               All of the above
    --force             Install even for apps that weren't detected

  Behaviour
    -y, --yes           Don't ask; accept defaults
    --dark NAME         Favourite dark variant: Dusk | Night | Obsidian
    --light NAME        Favourite light variant: Dawn | Mist
    --apply / --no-apply
                        Switch Dodo on in Zed, Ghostty and Terminal.app (default: ask)
    --auto-update[=daily|weekly|hourly] / --no-auto-update
    --list              Show which apps were detected, then exit
    -q, --quiet         No banner or chatter (used by update.sh)
    -h, --help          This help
EOF
}

# ASSUME_YES / QUIET are read by lib/dodo.sh.
# shellcheck disable=SC2034
main() {
  local want_zed=0 want_term=0 want_xcode=0 force=0 list=0 refresh=0 reimport_terminal=0
  local apply="" auto="" dark="" light="" arg
  ASSUME_YES=0
  QUIET=0
  for arg in "$@"; do
    case "$arg" in
      --zed) want_zed=1 ;;
      --terminal) want_term=1 ;;
      --xcode) want_xcode=1 ;;
      --all) want_zed=1 want_term=1 want_xcode=1 ;;
      --force) force=1 ;;
      -y | --yes) ASSUME_YES=1 ;;
      --apply) apply=1 ;;
      --no-apply) apply=0 ;;
      --auto-update) auto=daily ;;
      --auto-update=*) auto="${arg#*=}" ;;
      --no-auto-update) auto=off ;;
      --dark=*) dark="${arg#*=}" ;;
      --light=*) light="${arg#*=}" ;;
      --dark | --light) fail "use $arg=NAME"; exit 2 ;;
      --list) list=1 ;;
      --refresh) refresh=1 QUIET=1 ;;
      --terminal-app) reimport_terminal=1 ;;
      -q | --quiet) QUIET=1 ;;
      -h | --help) usage; exit 0 ;;
      *) printf 'Unknown option: %s\n\n' "$arg" >&2; usage >&2; exit 2 ;;
    esac
  done
  if [ "$want_zed$want_term$want_xcode" = 000 ]; then want_zed=1 want_term=1 want_xcode=1; fi

  dodo_ui_init

  # ── update.sh path: re-run what's already installed, silently ──────────────
  if [ "$refresh" = 1 ]; then
    local t rc=0
    [ -f "$DODO_COMPONENTS" ] || exit 0
    while IFS= read -r t; do
      [ -n "$t" ] || continue
      if [ "$t" = terminal-app ] && [ "$reimport_terminal" != 1 ]; then continue; fi
      if install_target "$t" >/dev/null 2>&1; then log "refreshed $(pretty "$t")"; else log "FAILED $(pretty "$t")"; rc=1; fi
    done <"$DODO_COMPONENTS"
    exit "$rc"
  fi

  dodo_banner install

  # ── what's on this machine? ───────────────────────────────────────────────
  local targets="" found="" missing="" t
  [ "$want_zed" = 1 ] && targets="zed"
  if [ "$want_term" = 1 ]; then
    for t in $TERMINAL_TARGETS; do
      case "$t" in terminal-app | iterm2) is_mac || continue ;; esac
      targets="$targets $t"
    done
  fi
  [ "$want_xcode" = 1 ] && is_mac && targets="$targets xcode"

  step "Looking around this $(is_mac && echo Mac || echo machine)"
  for t in $targets; do
    if detect "$t"; then
      found="$found $t"
      item "$(pretty "$t")" "${C_SAGE}found${R}"
    elif [ "$force" = 1 ]; then
      found="$found $t"
      item "$(pretty "$t")" "${C_GOLD}not found · forced${R}"
    else
      missing="$missing $t"
      item "$(pretty "$t")" "${C_FAINT}not installed${R}"
    fi
  done
  if [ "$want_xcode" = 1 ] && ! is_mac; then item "Xcode" "${C_FAINT}macOS only${R}"; fi
  [ "$list" = 1 ] && { out ""; exit 0; }

  if [ -z "${found// /}" ]; then
    out ""
    warn "Nothing to theme here yet. Install Zed or a terminal, or re-run with ${B}--force${R}."
    out ""
    exit 1
  fi

  # ── confirm ───────────────────────────────────────────────────────────────
  out ""
  local chosen="$found" count
  count=$(echo "$found" | wc -w | tr -d ' ')
  if ! ask "Install Dodo into the $count app$([ "$count" = 1 ] || echo s) found?" Y; then
    if interactive; then
      chosen=""
      for t in $found; do ask "  $(pretty "$t")?" Y && chosen="$chosen $t"; done
    else
      exit 0
    fi
  fi
  [ -z "${chosen// /}" ] && { note "Nothing selected — the dodo waddles off."; exit 0; }

  # ── install ───────────────────────────────────────────────────────────────
  step "Installing"
  state_init
  local installed="" failed=""
  for t in $chosen; do
    if spin "$(pretty "$t")" install_target "$t"; then
      component_add "$t"
      installed="$installed $t"
      case "$t" in
        zed) item "Zed" "${C_SAGE}✓ linked${R} ${C_FAINT}· 5 themes · 5 icon themes${R}" ;;
        terminal-app) item "Terminal.app" "${C_SAGE}✓ 5 profiles imported${R}" ;;
        iterm2) item "iTerm2" "${C_SAGE}✓ 11 dynamic profiles${R}" ;;
        xcode) item "Xcode" "${C_SAGE}✓ 5 themes${R} ${C_FAINT}· restart Xcode${R}" ;;
        *) item "$(pretty "$t")" "${C_SAGE}✓ 5 themes${R}" ;;
      esac
    else
      failed="$failed $t"
    fi
  done

  # ── favourites ────────────────────────────────────────────────────────────
  step "Your flock"
  dark="${dark:-$(pref_get dark "")}"
  light="${light:-$(pref_get light "")}"
  if [ -z "$dark" ] && interactive; then
    note "Dusk — warm charcoal & Claude coral   Night — cool slate   Obsidian — near-black, amber-lit"
    # shellcheck disable=SC2086
    dark="$(choose "Favourite dark variant?" Dusk $DODO_DARK_VARIANTS)"
  fi
  if [ -z "$light" ] && interactive; then
    note "Dawn — ivory & terracotta   Mist — cool grey & slate ink"
    # shellcheck disable=SC2086
    light="$(choose "Favourite light variant?" Dawn $DODO_LIGHT_VARIANTS)"
  fi
  dark="${dark:-Dusk}" light="${light:-Dawn}"
  pref_set dark "$dark"
  pref_set light "$light"
  ok "Dodo $dark by night, Dodo $light by day"

  # ── switch it on (opt-in, reversible) ─────────────────────────────────────
  local applied="" apply_targets=""
  for t in $installed; do case "$t" in zed | ghostty | terminal-app) apply_targets="$apply_targets $t" ;; esac; done
  if [ -n "$apply_targets" ]; then
    if [ -z "$apply" ]; then
      ask "Switch Dodo on now in $(for t in $apply_targets; do pretty "$t"; done | paste -sd, - | sed 's/,/, /g')? (marked edits, undone by uninstall.sh)" Y && apply=1 || apply=0
    fi
    if [ "$apply" = 1 ]; then
      for t in $apply_targets; do
        case "$t" in
          zed) if apply_zed "$dark" "$light"; then ok "Zed follows your system: $dark ⇄ $light (+ icons)"; applied="$applied zed"
               else note "Zed already has a theme set — left untouched (snippet below)"; fi ;;
          ghostty) if apply_ghostty "$dark" "$light"; then ok "Ghostty follows your system: $dark ⇄ $light"; applied="$applied ghostty"
                   else note "Ghostty already sets a theme — left untouched (snippet below)"; fi ;;
          terminal-app) if apply_terminal_app "$dark"; then ok "Terminal.app default profile → Dodo $dark"; applied="$applied terminal-app"
                        else note "Couldn't set Terminal.app's default (pick it in Settings › Profiles)"; fi ;;
        esac
      done
    fi
  fi

  # ── auto-update ───────────────────────────────────────────────────────────
  if git -C "$DODO_HOME" rev-parse --git-dir >/dev/null 2>&1; then
    local current
    current="$(auto_status)"
    if [ -z "$auto" ] && [ "$current" = off ]; then
      if ask "Keep Dodo fresh automatically? (a quiet daily git pull; ./update.sh --auto off to stop)" Y; then
        auto=daily
      else
        auto=off
      fi
    fi
    if [ -n "$auto" ] && [ "$auto" != off ]; then
      if auto_enable "$auto"; then ok "Auto-update: $auto"; else warn "Couldn't schedule auto-updates on this system"; fi
    elif [ "$auto" = off ] && [ "$current" != off ]; then
      auto_disable && note "Auto-update switched off"
    fi
  fi

  finish "$installed" "$applied" "$dark" "$light" "$failed"
}

finish() {
  local installed="$1" applied="$2" dark="$3" light="$4" failed="$5" t
  out ""
  rule
  out "  ${C_ACC}◆${R} ${B}${C_TEXT}Done.${R} ${C_MUTED}Here's how to wear it:${R}"
  rule
  for t in $installed; do
    case " $applied " in *" $t "*) continue ;; esac
    case "$t" in
      zed)
        out "  ${C_FEATHER}Zed${R}        ${C_MUTED}⌘K ⌘T for themes, or in settings.json:${R}"
        out "             ${C_TEXT}\"theme\":${R} ${C_GOLD}{ \"mode\": \"system\", \"light\": \"Dodo $light\", \"dark\": \"Dodo $dark\" }${R},"
        out "             ${C_TEXT}\"icon_theme\":${R} ${C_GOLD}{ \"mode\": \"system\", \"light\": \"Dodo $light Icons\", \"dark\": \"Dodo $dark Icons\" }${R}" ;;
      ghostty) out "  ${C_FEATHER}Ghostty${R}    ${C_TEXT}theme = light:Dodo $light,dark:Dodo $dark${R}" ;;
      kitty) out "  ${C_FEATHER}Kitty${R}      ${C_TEXT}kitten themes --reload-in=all \"Dodo $dark\"${R}" ;;
      alacritty) out "  ${C_FEATHER}Alacritty${R}  ${C_TEXT}general.import = [\"~/.config/alacritty/themes/dodo/dodo-$(echo "$dark" | tr '[:upper:]' '[:lower:]').toml\"]${R}" ;;
      wezterm) out "  ${C_FEATHER}WezTerm${R}    ${C_TEXT}config.color_scheme = \"Dodo $dark\"${R}" ;;
      warp) out "  ${C_FEATHER}Warp${R}       ${C_MUTED}Settings › Appearance › Themes › ${C_TEXT}Dodo $dark${R}" ;;
      iterm2) out "  ${C_FEATHER}iTerm2${R}     ${C_MUTED}Settings › Profiles › ${C_TEXT}Dodo Auto ($dark ⇄ $light)${R} ${C_MUTED}follows macOS appearance${R}" ;;
      terminal-app) out "  ${C_FEATHER}Terminal${R}   ${C_MUTED}Settings › Profiles › ${C_TEXT}Dodo $dark${R} ${C_MUTED}› Default${R}" ;;
      xcode) out "  ${C_FEATHER}Xcode${R}      ${C_MUTED}Settings › Themes › ${C_TEXT}Dodo $dark${R} ${C_MUTED}(restart Xcode first)${R}" ;;
    esac
  done
  if [ -n "$applied" ]; then
    out "  ${C_SAGE}Already on${R} ${C_MUTED}in $(for t in $applied; do pretty "$t"; done | paste -sd, - | sed 's/,/, /g') — enjoy.${R}"
  fi
  rule
  out "  ${C_MUTED}update${R}  ${C_TEXT}./update.sh${R}     ${C_MUTED}remove${R}  ${C_TEXT}./uninstall.sh${R}     ${C_FAINT}${DODO_HOME/#$HOME/~}${R}"
  if [ -n "$failed" ]; then
    out ""
    fail "Some steps failed: $(for t in $failed; do pretty "$t"; done | paste -sd, - | sed 's/,/, /g') — re-run to retry."
    out ""
    exit 1
  fi
  out ""
}

# ── bootstrap: piped from curl? fetch the repo first, then run from it ──────
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"
if [ -z "$SELF_DIR" ] || [ ! -f "$SELF_DIR/lib/dodo.sh" ]; then
  DODO_HOME="${DODO_HOME:-$HOME/.dodo-theme}"
  if [ ! -d "$DODO_HOME/.git" ]; then
    command -v git >/dev/null 2>&1 || { echo "Dodo needs git to install. Please install git first." >&2; exit 1; }
    printf '\n  ◆ Fetching Dodo into %s …\n' "$DODO_HOME"
    git clone --quiet "${DODO_REPO_URL:-https://github.com/chrisnicholson30/dodo-theme.git}" "$DODO_HOME" || exit 1
  fi
  exec bash "$DODO_HOME/install.sh" "$@"
fi

DODO_HOME="$SELF_DIR"
# shellcheck source=lib/dodo.sh
. "$DODO_HOME/lib/dodo.sh"
main "$@"
exit $?
