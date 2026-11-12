#!/usr/bin/env sh
set -eu

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/fish"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
FILES="functions/pacspin.py functions/pacman.fish functions/paru.fish functions/sudo.fish functions/_pacspin_wanted.fish conf.d/pacspin.fish"

log() { printf '%s\n' "$*"; }
fail() { printf 'error: %s\n' "$*" >&2; exit 1; }

require() {
    command -v "$1" >/dev/null 2>&1 || fail "missing dependency: $1"
}

install_files() {
    require fish
    require python3
    command -v pacman >/dev/null 2>&1 || log "warning: pacman not found, pacspin only does something on Arch-based systems"

    mkdir -p "$CONFIG_DIR/functions" "$CONFIG_DIR/conf.d"
    for file in $FILES; do
        [ -f "$SOURCE_DIR/$file" ] || fail "file not found in repo: $file"
        cp "$SOURCE_DIR/$file" "$CONFIG_DIR/$file"
        log "installed $CONFIG_DIR/$file"
    done
    log "done. open a new fish shell or run: exec fish"
}

uninstall_files() {
    for file in $FILES; do
        if [ -f "$CONFIG_DIR/$file" ]; then
            rm "$CONFIG_DIR/$file"
            log "removed $CONFIG_DIR/$file"
        fi
    done
    log "done. open a new fish shell or run: exec fish"
}

case "${1:-install}" in
    install) install_files ;;
    uninstall|--uninstall) uninstall_files ;;
    -h|--help) log "usage: ./install.sh [install|uninstall]" ;;
    *) fail "unknown option: $1" ;;
esac
