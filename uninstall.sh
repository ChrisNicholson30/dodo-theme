#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
#  Dodo · uninstaller
#
#    ./uninstall.sh           shows exactly what will go, then asks
#    ./uninstall.sh --yes     no questions
#    ./uninstall.sh --purge   also delete this Dodo folder
#
#  Removes only what install.sh recorded: its symlinks, the files it copied,
#  the lines it marked "added by dodo-theme", and the auto-update schedule.
#  Anything you edited by hand is left alone; replaced files are restored.
# ─────────────────────────────────────────────────────────────────────────────

# ASSUME_YES / QUIET are read by lib/dodo.sh.
# shellcheck disable=SC2034
main() {
  local purge=0 arg
  ASSUME_YES=0
  QUIET=0
  for arg in "$@"; do
    case "$arg" in
      -y | --yes) ASSUME_YES=1 ;;
      --purge) purge=1 ;;
      -h | --help) sed -n '3,12p' "$0" | sed 's/^#  \{0,1\}//'; exit 0 ;;
      *) printf 'Unknown option: %s\n' "$arg" >&2; exit 2 ;;
    esac
  done

  dodo_ui_init
  dodo_banner uninstall

  [ -f "$DODO_MANIFEST" ] || scan_for_strays

  step "What will be removed"
  local kind path n=0 count where
  if [ -s "$DODO_MANIFEST" ]; then
    while IFS="$TAB" read -r count kind where; do
      [ -n "$count" ] || continue
      n=$((n + count))
      if [ "$count" = 1 ]; then item "$(short "$where")" "${C_MUTED}${kind}${R}"
      else item "$(short "$where")/" "${C_MUTED}${count} ${kind}s${R}"; fi
    done <<EOF
$(grouped)
EOF
    while IFS="$TAB" read -r kind path; do
      case "$kind" in
        terminal-app) n=$((n + 1)); item "Terminal.app › $path" "${C_MUTED}profile${R}" ;;
        edit-zed | edit-ghostty) n=$((n + 1)); item "$(short "$path")" "${C_MUTED}marked lines only${R}" ;;
        auto-*) n=$((n + 1)); item "Auto-update schedule" "${C_MUTED}${kind#auto-}${R}" ;;
      esac
    done <"$DODO_MANIFEST"
  fi
  if [ "$n" = 0 ]; then
    out ""
    ok "Nothing of Dodo's is installed. The dodo is already extinct here."
    out ""
    exit 0
  fi
  out ""
  ask "Remove all of the above?" Y || { note "Spared. The dodo lives on."; out ""; exit 0; }

  step "Removing"
  auto_disable >/dev/null 2>&1 && ok "Auto-update schedule"
  local terminal_profiles="" failed=0
  while IFS="$TAB" read -r kind path; do
    [ -n "$kind" ] || continue
    case "$kind" in
      link)
        if [ -L "$path" ]; then rm -f "$path"; restore_backup "$path"; fi ;;
      copy)
        [ -f "$path" ] && rm -f "$path" ;;
      edit-zed)
        if [ -f "$path" ] && grep -q "$DODO_MARK" "$path"; then
          grep -v "$DODO_MARK" "$path" >"$path.dodo.tmp" && mv "$path.dodo.tmp" "$path" \
            && ok "$(short "$path") ${C_FAINT}(Zed falls back to its default theme)${R}"
        fi ;;
      edit-ghostty)
        if [ -f "$path" ] && grep -q "$DODO_MARK" "$path"; then
          awk -v m="# $DODO_MARK" '$0==m {skip=1; next} skip==1 {skip=0; next} {print}' "$path" \
            >"$path.dodo.tmp" && mv "$path.dodo.tmp" "$path" && ok "$(short "$path")"
        fi ;;
      terminal-app) terminal_profiles="$terminal_profiles${path}${TAB}" ;;
    esac
  done <"$DODO_MANIFEST"

  while IFS="$TAB" read -r count kind where; do
    [ -n "$count" ] || continue
    if [ "$count" = 1 ]; then ok "$(short "$where")"; else ok "$(short "$where")/ ${C_FAINT}(${count})${R}"; fi
  done <<EOF
$(grouped)
EOF

  if [ -n "$terminal_profiles" ]; then
    remove_terminal_profiles "$terminal_profiles" || failed=1
  fi

  rm -rf "$DODO_STATE"
  ok "Dodo's notes in $(short "$DODO_STATE")"

  if [ "$purge" = 1 ] || { [ "$DODO_HOME" = "$HOME/.dodo-theme" ] && ask "Also delete the Dodo folder itself ($(short "$DODO_HOME"))?" N; }; then
    rm -rf "$DODO_HOME" && ok "$(short "$DODO_HOME")"
  fi

  out ""
  rule
  out "  ${C_MUTED}◇${R} ${B}${C_TEXT}The dodo has left the building.${R} ${C_MUTED}Restart Zed/Xcode to let go fully.${R}"
  out "    ${C_FAINT}Missed it already? ./install.sh brings it back from extinction.${R}"
  rule
  out ""
  return "$failed"
}

short() { printf '%s' "${1/#$HOME/~}"; }

# Links & copies, collapsed per folder:  count<TAB>symlink|file<TAB>path-or-folder
grouped() {
  awk -F'\t' '$1=="link" || $1=="copy" {
      d = $2; sub(/\/[^\/]*$/, "", d); n[d]++; one[d] = $2; k[d] = ($1 == "link" ? "symlink" : "file")
    }
    END { for (d in n) printf "%d\t%s\t%s\n", n[d], k[d], (n[d] == 1 ? one[d] : d) }' "$DODO_MANIFEST" | sort -t"$TAB" -k3
}

restore_backup() { # put back whatever install.sh moved aside
  local base latest
  base="$(basename "$1")"
  # shellcheck disable=SC2012
  latest="$(ls -1d "$DODO_STATE/backups/$base."* 2>/dev/null | tail -n 1)"
  if [ -n "$latest" ] && [ ! -e "$1" ]; then
    mv "$latest" "$1" && note "restored your previous $(short "$1")"
  fi
}

# Terminal.app keeps profiles in its preferences. It will rewrite them on quit,
# so we only edit them while Terminal is closed; otherwise we ask it nicely.
remove_terminal_profiles() {
  local list="$1" name prefs="$HOME/Library/Preferences/com.apple.Terminal.plist" left=""
  is_mac || return 0
  local IFS="$TAB"
  for name in $list; do
    [ -n "$name" ] || continue
    if osascript -e "tell application \"Terminal\" to delete settings set \"$name\"" >/dev/null 2>&1; then
      ok "Terminal.app › $name"
    elif ! pgrep -xq Terminal && /usr/libexec/PlistBuddy -c "Delete ':Window Settings:$name'" "$prefs" >/dev/null 2>&1; then
      ok "Terminal.app › $name"
    else
      left="$left $name,"
    fi
  done
  if [ -n "$left" ]; then
    warn "Terminal.app is busy, so these profiles stay:${left%,}"
    note "Remove them in Terminal › Settings › Profiles (select, then −)."
  fi
  return 0
}

# No manifest (e.g. installed by an older Dodo)? Find our links by where they point.
scan_for_strays() {
  local f d
  state_init
  for f in "$XDG_CFG"/ghostty/themes/* "$XDG_CFG"/kitty/themes/* "$XDG_CFG"/wezterm/colors/* \
    "$XDG_CFG/alacritty/themes/dodo" "$(warp_dir)"/* ; do
    [ -L "$f" ] && case "$(readlink "$f")" in "$DODO_HOME"/*) manifest_add link "$f" ;; esac
  done
  while IFS= read -r d; do
    [ -n "$d" ] && [ -L "$d/extensions/installed/dodo-theme" ] && manifest_add link "$d/extensions/installed/dodo-theme"
  done <<EOF
$(zed_data_dirs)
EOF
  if is_mac; then
    [ -f "$HOME/Library/Application Support/iTerm2/DynamicProfiles/dodo-theme.json" ] \
      && manifest_add copy "$HOME/Library/Application Support/iTerm2/DynamicProfiles/dodo-theme.json"
    for f in "$(xcode_dir)"/Dodo\ *.xccolortheme; do [ -f "$f" ] && manifest_add copy "$f"; done
  fi
  [ -f "$(zed_settings)" ] && grep -q "$DODO_MARK" "$(zed_settings)" && manifest_add edit-zed "$(zed_settings)"
  [ -f "$(ghostty_config)" ] && grep -q "$DODO_MARK" "$(ghostty_config)" && manifest_add edit-ghostty "$(ghostty_config)"
  return 0
}

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
DODO_HOME="$SELF_DIR"
# shellcheck source=lib/dodo.sh
. "$DODO_HOME/lib/dodo.sh"
main "$@"
exit $?
