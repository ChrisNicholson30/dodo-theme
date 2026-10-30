# shellcheck shell=bash
# shellcheck disable=SC2034  # colours & lists are used by the scripts that source this
# ─────────────────────────────────────────────────────────────────────────────
#  Dodo · shared library for install.sh / update.sh / uninstall.sh
#  Bash 3.2 compatible (the bash macOS still ships), no GNU-only flags.
# ─────────────────────────────────────────────────────────────────────────────

DODO_REPO_URL="${DODO_REPO_URL:-https://github.com/chrisnicholson30/dodo-theme.git}"
DODO_STATE="${XDG_CONFIG_HOME:-$HOME/.config}/dodo-theme"
DODO_MANIFEST="$DODO_STATE/manifest"
DODO_PREFS="$DODO_STATE/prefs"
DODO_COMPONENTS="$DODO_STATE/components"
DODO_LOGDIR="${XDG_STATE_HOME:-$HOME/.local/state}/dodo-theme"
DODO_MARK="added by dodo-theme"
DODO_OS="$(uname -s)"
DODO_VERSION="$(cat "$DODO_HOME/VERSION" 2>/dev/null || echo dev)"
DODO_DARK_VARIANTS="Dusk Night Obsidian"
DODO_LIGHT_VARIANTS="Dawn Mist"
TAB="$(printf '\t')"

is_mac() { [ "$DODO_OS" = Darwin ]; }

# ── colour & glyphs ─────────────────────────────────────────────────────────

dodo_ui_init() {
  COLOR=0
  if [ -t 1 ] && [ -z "${NO_COLOR:-}" ] && [ "${TERM:-dumb}" != dumb ]; then COLOR=1; fi
  DEPTH=256
  case "${COLORTERM:-}" in truecolor | 24bit) DEPTH=24bit ;; esac
  case "${TERM_PROGRAM:-}" in iTerm.app | WezTerm | ghostty | vscode | zed | WarpTerminal | Hyper) DEPTH=24bit ;; esac
  [ -n "${KITTY_WINDOW_ID:-}" ] && DEPTH=24bit

  if [ "$COLOR" = 1 ]; then
    B=$'\033[1m' D=$'\033[2m' I=$'\033[3m' R=$'\033[0m'
    if [ "$DEPTH" = 24bit ]; then
      C_ACC=$'\033[38;2;217;119;87m' C_GOLD=$'\033[38;2;232;185;110m'
      C_FEATHER=$'\033[38;2;143;159;202m' C_SAGE=$'\033[38;2;169;197;139m'
      C_RED=$'\033[38;2;229;122;108m' C_MUTED=$'\033[38;2;140;135;124m'
      C_FAINT=$'\033[38;2;95;91;84m' C_TEXT=$'\033[38;2;235;231;222m'
      C_TEAL=$'\033[38;2;126;198;183m' C_LAV=$'\033[38;2;190;165;234m'
    else
      C_ACC=$'\033[38;5;173m' C_GOLD=$'\033[38;5;179m' C_FEATHER=$'\033[38;5;110m'
      C_SAGE=$'\033[38;5;150m' C_RED=$'\033[38;5;167m' C_MUTED=$'\033[38;5;102m'
      C_FAINT=$'\033[38;5;240m' C_TEXT=$'\033[38;5;254m' C_TEAL=$'\033[38;5;115m'
      C_LAV=$'\033[38;5;146m'
    fi
  else
    B='' D='' I='' R='' C_ACC='' C_GOLD='' C_FEATHER='' C_SAGE='' C_RED=''
    C_MUTED='' C_FAINT='' C_TEXT='' C_TEAL='' C_LAV=''
  fi
  QUIET="${QUIET:-0}"
}

out() { [ "$QUIET" = 1 ] || printf '%s\n' "$*"; }
step() { out "" && out "  ${C_ACC}◆${R} ${B}${C_TEXT}$*${R}"; }
ok() { out "    ${C_SAGE}✓${R} $*"; }
warn() { out "    ${C_GOLD}!${R} $*"; }
fail() { printf '%s\n' "    ${C_RED}✗${R} $*" >&2; }
note() { out "    ${C_FAINT}·${R} ${C_MUTED}$*${R}"; }
rule() { out "  ${C_FAINT}────────────────────────────────────────────────────────────${R}"; }
log() { [ "$QUIET" = 1 ] && printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; return 0; }

# A row with a dotted leader:  name ········ status
item() {
  local name="$1" status="$2" width=34 pad dots=""
  pad=$((width - ${#name}))
  [ "$pad" -lt 2 ] && pad=2
  while [ "$pad" -gt 0 ]; do dots="$dots·"; pad=$((pad - 1)); done
  out "    ${C_TEXT}${name}${R} ${C_FAINT}${dots}${R} $status"
}

# Prompts read from the terminal even when the script itself was piped in.
_tty_read() {
  local _ans=""
  if [ -r /dev/tty ]; then IFS= read -r _ans </dev/tty || true; else IFS= read -r _ans || true; fi
  printf '%s' "$_ans"
}

interactive() { [ "${ASSUME_YES:-0}" != 1 ] && [ "$QUIET" != 1 ] && { [ -t 0 ] || [ -r /dev/tty ]; }; }

# ask "Question" Y|N  → returns 0 for yes
ask() {
  local q="$1" def="${2:-Y}" hint ans
  if ! interactive; then [ "$def" = Y ]; return; fi
  if [ "$def" = Y ]; then hint="Y/n"; else hint="y/N"; fi
  printf '%s' "  ${C_GOLD}?${R} ${C_TEXT}${q}${R} ${C_FAINT}[${hint}]${R} "
  ans="$(_tty_read)"
  case "$ans" in
    [Yy]*) return 0 ;;
    [Nn]*) return 1 ;;
    *) [ "$def" = Y ] ;;
  esac
}

# choose "Prompt" default opt1 opt2 …   → echoes the chosen option
choose() {
  local prompt="$1" def="$2" i=1 ans opt
  shift 2
  if ! interactive; then printf '%s' "$def"; return; fi
  printf '%s\n' "  ${C_GOLD}?${R} ${C_TEXT}${prompt}${R}" >/dev/tty 2>/dev/null || true
  for opt in "$@"; do
    if [ "$opt" = "$def" ]; then
      printf '%s\n' "      ${C_ACC}${i}${R}  ${C_TEXT}${opt}${R} ${C_FAINT}(default)${R}" >/dev/tty
    else
      printf '%s\n' "      ${C_ACC}${i}${R}  ${C_MUTED}${opt}${R}" >/dev/tty
    fi
    i=$((i + 1))
  done
  printf '%s' "    ${C_FAINT}›${R} " >/dev/tty
  ans="$(_tty_read)"
  i=1
  for opt in "$@"; do
    if [ "$ans" = "$i" ] || [ "$ans" = "$opt" ]; then printf '%s' "$opt"; return; fi
    i=$((i + 1))
  done
  printf '%s' "$def"
}

# spin "label" cmd args…   — runs a command behind a braille spinner.
spin() {
  local label="$1" logf pid rc i=0
  local -a frames=(⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏)
  shift
  logf="$(mktemp "${TMPDIR:-/tmp}/dodo.XXXXXX")"
  if [ "$COLOR" != 1 ] || [ "$QUIET" = 1 ]; then
    "$@" >"$logf" 2>&1
    rc=$?
  else
    "$@" >"$logf" 2>&1 &
    pid=$!
    printf '\033[?25l'
    while kill -0 "$pid" 2>/dev/null; do
      printf '\r    %s%s%s %s%s%s' "$C_ACC" "${frames[i % 10]}" "$R" "$C_MUTED" "$label" "$R"
      i=$((i + 1))
      sleep 0.08
    done
    wait "$pid"
    rc=$?
    printf '\r\033[K\033[?25h'
  fi
  if [ "$rc" -ne 0 ]; then
    fail "$label"
    sed 's/^/        /' "$logf" | tail -n 8 >&2
  fi
  rm -f "$logf"
  return "$rc"
}

# ── banner ─────────────────────────────────────────────────────────────────

_read_lines() { # _read_lines file → fills _LINES array
  _LINES=()
  local n=0 line
  [ -f "$1" ] || return 0
  while IFS= read -r line || [ -n "$line" ]; do _LINES[n]="$line"; n=$((n + 1)); done <"$1"
}

dodo_banner() { # install | update | uninstall
  [ "$QUIET" = 1 ] && return 0
  local mode="$1" grey="" tag1 tag2 cols art_w i n
  local -a art word right
  [ "$mode" = uninstall ] && grey="grey-"
  case "$mode" in
    install) tag1="A theme suite for Zed · Terminal · Xcode"
             tag2="five variants  ·  three dark  ·  two light" ;;
    update) tag1="Keeping the flock up to date"
            tag2="one pull  ·  every app refreshed" ;;
    uninstall) tag1="Going extinct… (on this machine only)"
               tag2="Your own configs stay yours. Only Dodo leaves." ;;
  esac
  cols="$(tput cols 2>/dev/null || echo 80)"
  printf '\n'
  if [ "$COLOR" != 1 ]; then
    _read_lines "$DODO_HOME/assets/term/wordmark-plain.txt"
    for i in "${_LINES[@]}"; do printf '  %s\n' "$i"; done
    printf '\n  %s\n  %s\n\n' "$tag1" "$tag2"
    return 0
  fi
  _read_lines "$DODO_HOME/assets/term/wordmark-${grey}${DEPTH}.ans"
  word=("${_LINES[@]}")
  if [ "$cols" -lt 76 ]; then
    for i in "${word[@]}"; do printf '  %s\n' "$i"; done
    printf '\n  %s\n  %s%s%s\n\n' "${B}${C_TEXT}${tag1}${R}" "$C_MUTED" "$tag2" "$R"
    return 0
  fi
  _read_lines "$DODO_HOME/assets/term/dodo-${grey}${DEPTH}.ans"
  art=("${_LINES[@]}")
  art_w="$(cat "$DODO_HOME/assets/term/WIDTH" 2>/dev/null || echo 28)"
  right=("" "" "" "")
  for i in "${word[@]}"; do right[${#right[@]}]="$i"; done
  right[${#right[@]}]=""
  right[${#right[@]}]="${B}${C_TEXT}${tag1}${R}"
  right[${#right[@]}]="${C_MUTED}${tag2}${R}"
  right[${#right[@]}]=""
  right[${#right[@]}]="${C_FAINT}v${DODO_VERSION}  ·  ${DODO_OS}  ·  ${DEPTH} colour${R}"
  n=${#art[@]}
  [ ${#right[@]} -gt "$n" ] && n=${#right[@]}
  i=0
  while [ "$i" -lt "$n" ]; do
    if [ -n "${art[i]:-}" ]; then printf '  %s' "${art[i]}"; else printf '  %*s' "$art_w" ''; fi
    printf '   %s\n' "${right[i]:-}"
    i=$((i + 1))
  done
  printf '\n'
}

# ── state ──────────────────────────────────────────────────────────────────

state_init() { mkdir -p "$DODO_STATE" "$DODO_STATE/backups"; touch "$DODO_MANIFEST"; }

manifest_add() { # kind path
  state_init
  grep -qxF "$1${TAB}$2" "$DODO_MANIFEST" 2>/dev/null || printf '%s\t%s\n' "$1" "$2" >>"$DODO_MANIFEST"
}

manifest_drop() { # kind path
  [ -f "$DODO_MANIFEST" ] || return 0
  grep -vxF "$1${TAB}$2" "$DODO_MANIFEST" >"$DODO_MANIFEST.tmp" || true
  mv "$DODO_MANIFEST.tmp" "$DODO_MANIFEST"
}

component_add() {
  state_init
  touch "$DODO_COMPONENTS"
  grep -qx "$1" "$DODO_COMPONENTS" || echo "$1" >>"$DODO_COMPONENTS"
}

pref_get() { # key default
  local v=""
  [ -f "$DODO_PREFS" ] && v="$(sed -n "s/^$1=//p" "$DODO_PREFS" | tail -n 1)"
  printf '%s' "${v:-$2}"
}

pref_set() { # key value
  state_init
  touch "$DODO_PREFS"
  grep -v "^$1=" "$DODO_PREFS" >"$DODO_PREFS.tmp" || true
  printf '%s=%s\n' "$1" "$2" >>"$DODO_PREFS.tmp"
  mv "$DODO_PREFS.tmp" "$DODO_PREFS"
}

backup_path() { # original → a unique path inside the state dir
  state_init
  printf '%s/backups/%s.%s' "$DODO_STATE" "$(basename "$1")" "$(date +%Y%m%d-%H%M%S)"
}

# link_into src dest — symlink, so `git pull` updates the theme in place.
link_into() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")" || return 1
  if [ -L "$dest" ]; then
    rm -f "$dest"
  elif [ -e "$dest" ]; then
    mv "$dest" "$(backup_path "$dest")" || return 1
  fi
  ln -s "$src" "$dest" && manifest_add link "$dest"
}

copy_into() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")" || return 1
  [ -L "$dest" ] && rm -f "$dest"
  cp -f "$src" "$dest" && manifest_add copy "$dest"
}

# ── detection ──────────────────────────────────────────────────────────────

has_cmd() { command -v "$1" >/dev/null 2>&1; }
has_app() { # mac .app names
  local a
  for a in "$@"; do
    [ -d "/Applications/$a.app" ] || [ -d "$HOME/Applications/$a.app" ] && return 0
  done
  return 1
}

XDG_CFG="${XDG_CONFIG_HOME:-$HOME/.config}"
XDG_DATA="${XDG_DATA_HOME:-$HOME/.local/share}"

zed_data_dirs() {
  if is_mac; then
    if [ -d "$HOME/Library/Application Support/Zed" ] || has_app Zed "Zed Preview" || has_cmd zed; then
      echo "$HOME/Library/Application Support/Zed"
    fi
  else
    if [ -d "$XDG_DATA/zed" ] || has_cmd zed || has_cmd zeditor; then echo "$XDG_DATA/zed"; fi
    [ -d "$HOME/.var/app/dev.zed.Zed" ] && echo "$HOME/.var/app/dev.zed.Zed/data/zed"
  fi
  return 0
}

detect() { # target → 0 if present on this machine
  case "$1" in
    zed) [ -n "$(zed_data_dirs)" ] ;;
    terminal-app) is_mac ;;
    iterm2) is_mac && { has_app iTerm || [ -d "$HOME/Library/Application Support/iTerm2" ]; } ;;
    ghostty) has_cmd ghostty || has_app Ghostty || [ -d "$XDG_CFG/ghostty" ] ;;
    kitty) has_cmd kitty || has_app kitty || [ -d "$XDG_CFG/kitty" ] ;;
    alacritty) has_cmd alacritty || has_app Alacritty || [ -d "$XDG_CFG/alacritty" ] ;;
    wezterm) has_cmd wezterm || has_app WezTerm || [ -d "$XDG_CFG/wezterm" ] || [ -f "$HOME/.wezterm.lua" ] ;;
    warp) has_app Warp || has_cmd warp-terminal || [ -d "$HOME/.warp" ] || [ -d "$XDG_DATA/warp-terminal" ] ;;
    xcode) is_mac && { ls -d /Applications/Xcode*.app >/dev/null 2>&1 || [ -d "$HOME/Library/Developer/Xcode" ]; } ;;
    *) return 1 ;;
  esac
}

TERMINAL_TARGETS="terminal-app iterm2 ghostty kitty alacritty wezterm warp"

pretty() {
  case "$1" in
    zed) echo "Zed" ;; terminal-app) echo "Terminal.app" ;; iterm2) echo "iTerm2" ;;
    ghostty) echo "Ghostty" ;; kitty) echo "Kitty" ;; alacritty) echo "Alacritty" ;;
    wezterm) echo "WezTerm" ;; warp) echo "Warp" ;; xcode) echo "Xcode" ;; *) echo "$1" ;;
  esac
}

# ── installers (idempotent; safe to re-run from update.sh) ──────────────────

install_zed() {
  local d n=0
  while IFS= read -r d; do
    [ -n "$d" ] || continue
    link_into "$DODO_HOME/zed" "$d/extensions/installed/dodo-theme" || return 1
    n=$((n + 1))
  done <<EOF
$(zed_data_dirs)
EOF
  [ "$n" -gt 0 ]
}

_link_each() { # srcdir destdir
  local f
  for f in "$1"/*; do
    [ -e "$f" ] || continue
    link_into "$f" "$2/$(basename "$f")" || return 1
  done
}

install_ghostty() { _link_each "$DODO_HOME/terminal/ghostty" "$XDG_CFG/ghostty/themes"; }
install_kitty() { _link_each "$DODO_HOME/terminal/kitty" "$XDG_CFG/kitty/themes"; }
install_alacritty() { link_into "$DODO_HOME/terminal/alacritty" "$XDG_CFG/alacritty/themes/dodo"; }
install_wezterm() { _link_each "$DODO_HOME/terminal/wezterm" "$XDG_CFG/wezterm/colors"; }

warp_dir() { if is_mac; then echo "$HOME/.warp/themes"; else echo "$XDG_DATA/warp-terminal/themes"; fi; }
install_warp() { _link_each "$DODO_HOME/terminal/warp" "$(warp_dir)"; }

# iTerm2 Dynamic Profiles reload live whenever this file changes.
install_iterm2() {
  copy_into "$DODO_HOME/terminal/iterm2/dodo-dynamic-profiles.json" \
    "$HOME/Library/Application Support/iTerm2/DynamicProfiles/dodo-theme.json"
}

xcode_dir() { echo "$HOME/Library/Developer/Xcode/UserData/FontAndColorThemes"; }
install_xcode() {
  local f
  for f in "$DODO_HOME"/xcode/*.xccolortheme; do
    copy_into "$f" "$(xcode_dir)/$(basename "$f")" || return 1
  done
}

# Terminal.app imports a profile by opening it, which also opens a preview
# window. We note the windows that already exist, import, then close only
# the new ones — your own windows are never touched.
install_terminal_app() {
  local before f
  before="$(osascript -e 'tell application "Terminal" to get id of every window' 2>/dev/null || true)"
  for f in "$DODO_HOME"/terminal/terminal-app/*.terminal; do
    open -g "$f" || return 1
    manifest_add terminal-app "$(basename "$f" .terminal)"
  done
  sleep 2
  osascript >/dev/null 2>&1 <<EOF || true
tell application "Terminal"
  set keep to {${before}}
  repeat with w in (every window)
    if keep does not contain (id of w) then close w
  end repeat
end tell
EOF
  return 0
}

install_target() { # target
  case "$1" in
    zed) install_zed ;; terminal-app) install_terminal_app ;; iterm2) install_iterm2 ;;
    ghostty) install_ghostty ;; kitty) install_kitty ;; alacritty) install_alacritty ;;
    wezterm) install_wezterm ;; warp) install_warp ;; xcode) install_xcode ;;
  esac
}

# ── applying (opt-in edits, always marked so uninstall can undo them) ─────

zed_settings() { echo "$XDG_CFG/zed/settings.json"; }

apply_zed() { # dark light → 0 applied, 1 left alone
  local f dark="Dodo $1" light="Dodo $2" body
  f="$(zed_settings)"
  body="  \"theme\": { \"mode\": \"system\", \"light\": \"$light\", \"dark\": \"$dark\" }, // $DODO_MARK
  \"icon_theme\": { \"mode\": \"system\", \"light\": \"$light Icons\", \"dark\": \"$dark Icons\" }, // $DODO_MARK"
  mkdir -p "$(dirname "$f")"
  if [ ! -s "$f" ] || [ -z "$(sed -e 's://.*$::' "$f" | tr -d ' \t\r\n{}')" ]; then
    [ -s "$f" ] && cp "$f" "$(backup_path "$f")"
    printf '{\n%s\n}\n' "$body" >"$f"
  elif grep -Eq '"(icon_)?theme"[[:space:]]*:' "$f"; then
    if grep -q "$DODO_MARK" "$f"; then
      grep -v "$DODO_MARK" "$f" >"$f.dodo.tmp" && mv "$f.dodo.tmp" "$f"
      apply_zed "$1" "$2"
      return
    fi
    return 1
  elif grep -Eq '^[[:space:]]*\{[[:space:]]*$' "$f"; then
    cp "$f" "$(backup_path "$f")"
    awk -v body="$body" 'done!=1 && /^[[:space:]]*\{[[:space:]]*$/ {print; print body; done=1; next} {print}' \
      "$f" >"$f.dodo.tmp" && mv "$f.dodo.tmp" "$f"
  else
    return 1
  fi
  manifest_add edit-zed "$f"
}

ghostty_config() {
  if is_mac && [ -f "$HOME/Library/Application Support/com.mitchellh.ghostty/config" ] \
    && [ ! -f "$XDG_CFG/ghostty/config" ]; then
    echo "$HOME/Library/Application Support/com.mitchellh.ghostty/config"
  else
    echo "$XDG_CFG/ghostty/config"
  fi
}

apply_ghostty() { # dark light
  local f
  f="$(ghostty_config)"
  if [ -f "$f" ] && grep -q "$DODO_MARK" "$f"; then
    awk -v m="# $DODO_MARK" '$0==m {skip=1; next} skip==1 {skip=0; next} {print}' "$f" >"$f.dodo.tmp" \
      && mv "$f.dodo.tmp" "$f"
  fi
  if [ -f "$f" ] && grep -Eq '^[[:space:]]*theme[[:space:]]*=' "$f"; then return 1; fi
  mkdir -p "$(dirname "$f")"
  [ -s "$f" ] && [ -n "$(tail -c 1 "$f")" ] && echo >>"$f"
  printf '# %s\ntheme = light:Dodo %s,dark:Dodo %s\n' "$DODO_MARK" "$2" "$1" >>"$f"
  manifest_add edit-ghostty "$f"
}

apply_terminal_app() { # profile
  osascript >/dev/null 2>&1 <<EOF
tell application "Terminal"
  set default settings to settings set "Dodo $1"
  set startup settings to settings set "Dodo $1"
end tell
EOF
}

# ── auto-update scheduling ─────────────────────────────────────────────────

LAUNCHD_LABEL="com.dodo-theme.update"
launchd_plist() { echo "$HOME/Library/LaunchAgents/$LAUNCHD_LABEL.plist"; }
SYSTEMD_DIR="$XDG_CFG/systemd/user"

auto_enable() { # daily | weekly | hourly
  local freq="${1:-daily}" plist sched oncal
  mkdir -p "$DODO_LOGDIR"
  auto_disable >/dev/null 2>&1
  if is_mac; then
    plist="$(launchd_plist)"
    case "$freq" in
      hourly) sched="<key>StartInterval</key><integer>3600</integer>" ;;
      weekly) sched="<key>StartCalendarInterval</key><dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>10</integer><key>Minute</key><integer>17</integer></dict>" ;;
      *) sched="<key>StartCalendarInterval</key><dict><key>Hour</key><integer>10</integer><key>Minute</key><integer>17</integer></dict>" ;;
    esac
    mkdir -p "$(dirname "$plist")"
    cat >"$plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LAUNCHD_LABEL</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>$DODO_HOME/update.sh</string><string>--auto-run</string></array>
  $sched
  <key>RunAtLoad</key><false/>
  <key>ProcessType</key><string>Background</string>
  <key>LowPriorityIO</key><true/>
  <key>StandardOutPath</key><string>$DODO_LOGDIR/update.log</string>
  <key>StandardErrorPath</key><string>$DODO_LOGDIR/update.log</string>
</dict>
</plist>
EOF
    launchctl bootstrap "gui/$(id -u)" "$plist" 2>/dev/null || launchctl load -w "$plist" 2>/dev/null
    manifest_add auto-launchd "$plist"
  elif has_cmd systemctl && systemctl --user show-environment >/dev/null 2>&1; then
    case "$freq" in hourly) oncal=hourly ;; weekly) oncal=weekly ;; *) oncal=daily ;; esac
    mkdir -p "$SYSTEMD_DIR"
    cat >"$SYSTEMD_DIR/dodo-theme-update.service" <<EOF
[Unit]
Description=Dodo theme auto-update

[Service]
Type=oneshot
ExecStart=/bin/bash "$DODO_HOME/update.sh" --auto-run
StandardOutput=append:$DODO_LOGDIR/update.log
StandardError=append:$DODO_LOGDIR/update.log
EOF
    cat >"$SYSTEMD_DIR/dodo-theme-update.timer" <<EOF
[Unit]
Description=Check for Dodo theme updates ($oncal)

[Timer]
OnCalendar=$oncal
Persistent=true
RandomizedDelaySec=45m

[Install]
WantedBy=timers.target
EOF
    systemctl --user daemon-reload && systemctl --user enable --now dodo-theme-update.timer >/dev/null 2>&1
    manifest_add auto-systemd "$SYSTEMD_DIR/dodo-theme-update.timer"
  elif has_cmd crontab; then
    case "$freq" in hourly) sched="17 * * * *" ;; weekly) sched="17 10 * * 1" ;; *) sched="17 10 * * *" ;; esac
    { crontab -l 2>/dev/null | grep -v "dodo-theme-auto-update"
      echo "$sched /bin/bash \"$DODO_HOME/update.sh\" --auto-run >>\"$DODO_LOGDIR/update.log\" 2>&1 # dodo-theme-auto-update"
    } | crontab -
    manifest_add auto-cron "crontab"
  else
    return 1
  fi
  pref_set auto_update "$freq"
}

auto_disable() {
  local plist
  if is_mac; then
    plist="$(launchd_plist)"
    if [ -f "$plist" ]; then
      launchctl bootout "gui/$(id -u)/$LAUNCHD_LABEL" 2>/dev/null || launchctl unload -w "$plist" 2>/dev/null
      rm -f "$plist"
    fi
    manifest_drop auto-launchd "$plist"
  fi
  if [ -f "$SYSTEMD_DIR/dodo-theme-update.timer" ]; then
    systemctl --user disable --now dodo-theme-update.timer >/dev/null 2>&1
    rm -f "$SYSTEMD_DIR/dodo-theme-update.timer" "$SYSTEMD_DIR/dodo-theme-update.service"
    systemctl --user daemon-reload >/dev/null 2>&1
    manifest_drop auto-systemd "$SYSTEMD_DIR/dodo-theme-update.timer"
  fi
  if has_cmd crontab && crontab -l 2>/dev/null | grep -q "dodo-theme-auto-update"; then
    crontab -l 2>/dev/null | grep -v "dodo-theme-auto-update" | crontab -
    manifest_drop auto-cron crontab
  fi
  pref_set auto_update off
  return 0
}

auto_status() {
  local f
  f="$(pref_get auto_update off)"
  if [ "$f" = off ]; then echo "off"; else echo "$f"; fi
}

notify() { # title message
  if is_mac; then
    osascript -e "display notification \"$2\" with title \"$1\"" >/dev/null 2>&1 || true
  elif has_cmd notify-send; then
    notify-send "$1" "$2" >/dev/null 2>&1 || true
  fi
}
