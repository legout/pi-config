#!/usr/bin/env bash
set -euo pipefail

PI_HOME="${PI_HOME:-$HOME/.pi/agent}"
PI_ROOT="${PI_ROOT:-$HOME/.pi}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRIVATE_DIR="$SCRIPT_DIR/private"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }
step()  { echo -e "${BLUE}[STEP]${NC} $*"; }

has_placeholders() {
    local file="$1"
    [ -f "$file" ] && grep -q '__REQUIRED__' "$file"
}

copy_if_exists() {
    local src="$1"
    local dst="$2"
    [ -f "$src" ] || return 0
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
}

show_status() {
    echo "Secrets Bootstrap Status"
    echo "========================"
    echo ""
    echo "Repo private dir: $PRIVATE_DIR"
    echo "Live pi config:   $PI_HOME"
    echo "Live web search:  $PI_ROOT/web-search.json"
    echo ""

    for name in models.json mcp.json web-search.json; do
        local_private="$PRIVATE_DIR/$name"
        case "$name" in
            web-search.json) local_live="$PI_ROOT/$name" ;;
            *) local_live="$PI_HOME/$name" ;;
        esac

        printf '%-16s' "$name"
        if [ -f "$local_private" ]; then
            if has_placeholders "$local_private"; then
                echo " private: placeholder-only"
            else
                echo " private: present"
            fi
        else
            echo -n " private: missing"
            if [ -f "$local_live" ]; then
                if has_placeholders "$local_live"; then
                    echo " | live: placeholder-only"
                else
                    echo " | live: present"
                fi
            else
                echo " | live: missing"
            fi
        fi
    done

    echo ""
    warn "auth.json is not managed by this script."
}

capture() {
    step "Capturing live secret-bearing config into private/"
    mkdir -p "$PRIVATE_DIR"

    local count=0
    for name in models.json mcp.json; do
        src="$PI_HOME/$name"
        dst="$PRIVATE_DIR/$name"
        if [ -f "$src" ]; then
            copy_if_exists "$src" "$dst"
            if has_placeholders "$dst"; then
                warn "  $name copied, but still contains placeholders"
            else
                info "  captured $name"
            fi
            count=$((count + 1))
        else
            warn "  missing live file: $src"
        fi
    done

    if [ -f "$PI_ROOT/web-search.json" ]; then
        copy_if_exists "$PI_ROOT/web-search.json" "$PRIVATE_DIR/web-search.json"
        if has_placeholders "$PRIVATE_DIR/web-search.json"; then
            warn "  web-search.json copied, but still contains placeholders"
        else
            info "  captured web-search.json"
        fi
        count=$((count + 1))
    else
        warn "  missing live file: $PI_ROOT/web-search.json"
    fi

    info "Captured $count files into $PRIVATE_DIR"
    warn "private/ is gitignored; sync it with your secure personal file sync if desired."
}

install() {
    step "Installing private config into live pi config"

    if [ ! -d "$PRIVATE_DIR" ]; then
        error "No private/ directory found."
        echo "Run: ./bootstrap-secrets.sh capture"
        exit 1
    fi

    local installed=0
    for name in models.json mcp.json; do
        src="$PRIVATE_DIR/$name"
        dst="$PI_HOME/$name"
        if [ -f "$src" ]; then
            mkdir -p "$PI_HOME"
            cp "$src" "$dst"
            if has_placeholders "$dst"; then
                warn "  installed $name, but it still contains placeholders"
            else
                info "  installed $name"
            fi
            installed=$((installed + 1))
        else
            warn "  missing private file: $src"
        fi
    done

    if [ -f "$PRIVATE_DIR/web-search.json" ]; then
        mkdir -p "$PI_ROOT"
        cp "$PRIVATE_DIR/web-search.json" "$PI_ROOT/web-search.json"
        if has_placeholders "$PI_ROOT/web-search.json"; then
            warn "  installed web-search.json, but it still contains placeholders"
        else
            info "  installed web-search.json"
        fi
        installed=$((installed + 1))
    else
        warn "  missing private file: $PRIVATE_DIR/web-search.json"
    fi

    info "Installed $installed files"
    warn "auth.json is still not installed by this script."
}

help_text() {
    cat <<'EOF'
Usage: ./bootstrap-secrets.sh {status|capture|install}

Commands:
  status   Show whether private/ and live config have usable secret-bearing files
  capture  Copy current live pi secret-bearing config into local gitignored private/
  install  Copy local private/ secret-bearing config back into live pi locations

Notes:
  - auth.json is not managed here
  - private/ is gitignored
  - install does not modify tracked sanitized files under config/
EOF
}

case "${1:-status}" in
    status) show_status ;;
    capture) capture ;;
    install) install ;;
    *) help_text; exit 1 ;;
esac
