#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
#  Dodo · updater
#
#    ./update.sh                 pull the latest Dodo and refresh every install
#    ./update.sh --check         just say whether an update is waiting
#    ./update.sh --auto daily    schedule quiet background updates
#    ./update.sh --auto off      …and switch them off again
#    ./update.sh --auto status
#
#  Zed, Ghostty, Kitty, Alacritty, WezTerm and Warp are symlinked to this
#  folder, so a pull alone updates them. Copies (Xcode, iTerm2) are refreshed;
#  Terminal.app profiles are re-imported only when they actually changed.
# ─────────────────────────────────────────────────────────────────────────────

usage() {
  sed -n '3,15p' "$0" | sed 's/^#  \{0,1\}//'
}

# ASSUME_YES / QUIET are read by lib/dodo.sh.
# shellcheck disable=SC2034
main() {
  local check=0 force=0 auto_arg="" arg
  QUIET=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --check) check=1 ;;
      --force) force=1 ;;
      --auto) auto_arg="${2:-status}"; shift ;;
      --auto=*) auto_arg="${1#*=}" ;;
      --auto-run) QUIET=1 ;;
      -q | --quiet) QUIET=1 ;;
      -h | --help) usage; exit 0 ;;
      *) printf 'Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
    esac
    shift
  done
  arg=""

  dodo_ui_init

  if [ -n "$auto_arg" ]; then
    case "$auto_arg" in
      status)
        local s
        s="$(auto_status)"
        if [ "$s" = off ]; then out "  ${C_MUTED}Auto-update is${R} ${B}off${R}"
        else out "  ${C_SAGE}●${R} Auto-update is ${B}on${R} ${C_MUTED}($s) · log: ${DODO_LOGDIR/#$HOME/~}/update.log${R}"; fi ;;
      off | disable | no) auto_disable && out "  ${C_SAGE}✓${R} Auto-update switched off" ;;
      on | enable | yes | daily | weekly | hourly)
        [ "$auto_arg" = daily ] || [ "$auto_arg" = weekly ] || [ "$auto_arg" = hourly ] || auto_arg=daily
        if auto_enable "$auto_arg"; then
          out "  ${C_SAGE}✓${R} Auto-update: $auto_arg ${C_MUTED}· log: ${DODO_LOGDIR/#$HOME/~}/update.log${R}"
        else
          fail "No scheduler found (launchd, systemd --user or cron) — run ./update.sh by hand instead."
          exit 1
        fi ;;
      *) fail "--auto takes daily | weekly | hourly | off | status"; exit 2 ;;
    esac
    exit $?
  fi

  dodo_banner update
  log "checking for updates"

  if ! git -C "$DODO_HOME" rev-parse --git-dir >/dev/null 2>&1; then
    fail "$DODO_HOME isn't a git checkout, so it can't pull updates."
    note "Re-install with:  bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/chrisnicholson30/dodo-theme/main/install.sh)\""
    exit 1
  fi

  local upstream old new behind ahead
  upstream="$(git -C "$DODO_HOME" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null)"
  [ -n "$upstream" ] || upstream="origin/main"

  step "Checking the flock"
  if ! spin "Fetching ${upstream}" git -C "$DODO_HOME" fetch --quiet --prune "${upstream%%/*}"; then
    log "fetch failed"
    exit 1
  fi
  old="$(git -C "$DODO_HOME" rev-parse HEAD)"
  behind="$(git -C "$DODO_HOME" rev-list --count "HEAD..$upstream" 2>/dev/null || echo 0)"
  ahead="$(git -C "$DODO_HOME" rev-list --count "$upstream..HEAD" 2>/dev/null || echo 0)"

  if [ "$behind" = 0 ]; then
    ok "You're on the latest Dodo ${C_FAINT}(v${DODO_VERSION} · $(git -C "$DODO_HOME" rev-parse --short HEAD))${R}"
    log "up to date"
    [ "$check" = 1 ] && exit 0
    if [ "$force" = 1 ]; then
      refresh_installs "$old" "$old" 1
    fi
    out ""
    exit 0
  fi

  item "New changes" "${C_GOLD}${behind} commit$([ "$behind" = 1 ] || echo s)${R}"
  git -C "$DODO_HOME" log --format='%s' "HEAD..$upstream" 2>/dev/null | head -n 12 | while IFS= read -r arg; do
    out "      ${C_ACC}›${R} ${C_TEXT}${arg}${R}"
  done
  if [ "$check" = 1 ]; then
    out ""
    note "Run ./update.sh to bring them in."
    out ""
    exit 10
  fi

  if [ "$ahead" != 0 ]; then
    warn "Your copy has $ahead local commit(s) that aren't upstream."
    note "Dodo won't rewrite your history. Resolve in ${DODO_HOME/#$HOME/~} with git, then re-run."
    log "diverged: ahead=$ahead behind=$behind — skipped"
    [ "$QUIET" = 1 ] && notify "Dodo" "Update waiting — your local copy has diverged; run ./update.sh"
    exit 1
  fi
  if ! git -C "$DODO_HOME" diff --quiet || ! git -C "$DODO_HOME" diff --cached --quiet; then
    warn "You have local edits in ${DODO_HOME/#$HOME/~} — keeping them safe, not updating."
    note "Commit or stash them (git stash), then run ./update.sh again."
    log "local edits — skipped"
    [ "$QUIET" = 1 ] && notify "Dodo" "Update waiting — local edits are in the way"
    exit 1
  fi

  step "Updating"
  if ! spin "Pulling ${behind} commit(s)" git -C "$DODO_HOME" merge --ff-only --quiet "$upstream"; then
    log "fast-forward failed"
    exit 1
  fi
  new="$(git -C "$DODO_HOME" rev-parse HEAD)"
  DODO_VERSION="$(cat "$DODO_HOME/VERSION" 2>/dev/null || echo dev)"
  ok "Now on v${DODO_VERSION} ${C_FAINT}($(git -C "$DODO_HOME" rev-parse --short HEAD))${R}"
  log "updated $(git -C "$DODO_HOME" rev-parse --short "$old") → $(git -C "$DODO_HOME" rev-parse --short "$new")"

  # Hand over to the *new* installer so new targets/variants are picked up.
  refresh_installs "$old" "$new" 0
  [ "$QUIET" = 1 ] && notify "Dodo updated" "Now on v${DODO_VERSION} — your themes refreshed themselves."
  out ""
  rule
  out "  ${C_ACC}◆${R} ${B}${C_TEXT}The flock is fresh.${R} ${C_MUTED}Zed reloads by itself; restart Xcode to see its changes.${R}"
  rule
  out ""
}

refresh_installs() { # old new force
  local flags=""
  if [ "$3" = 1 ] || ! git -C "$DODO_HOME" diff --quiet "$1" "$2" -- terminal/terminal-app 2>/dev/null; then
    flags="--terminal-app"
  fi
  if [ ! -f "$DODO_COMPONENTS" ]; then
    note "Nothing installed yet — run ./install.sh"
    return 0
  fi
  if spin "Refreshing installed apps" bash "$DODO_HOME/install.sh" --refresh $flags; then
    ok "Refreshed: $(tr '\n' ' ' <"$DODO_COMPONENTS" | sed 's/ $//' | sed 's/ /, /g')"
  else
    warn "Some apps couldn't be refreshed — run ./install.sh to repair"
  fi
}

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
DODO_HOME="$SELF_DIR"
# shellcheck source=lib/dodo.sh
. "$DODO_HOME/lib/dodo.sh"
# Everything runs inside main(), which bash has fully parsed before the pull
# rewrites this very file on disk.
main "$@"
exit $?
