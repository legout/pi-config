#!/usr/bin/env bash
set -euo pipefail

PI_HOME="${PI_HOME:-$HOME/.pi/agent}"
PI_ROOT="${PI_ROOT:-$HOME/.pi}"
AGENTS_SKILLS="${AGENTS_SKILLS:-$HOME/.agents/skills}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR"
SANITIZER="$CONFIG_DIR/scripts/sanitize_configs.py"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || { error "Missing required command: $1"; exit 1; }
}

reset_dir() {
    local dir="$1"
    mkdir -p "$dir"
    find "$dir" -mindepth 1 -maxdepth 1 -exec rm -rf {} + 2>/dev/null || true
}

clean_tree() {
    local dir="$1"
    [ -d "$dir" ] || return 0
    find "$dir" \( -name '.DS_Store' -o -name '*.pyc' \) -type f -delete 2>/dev/null || true
    find "$dir" \( -name '__pycache__' -o -name '.git' \) -type d -prune -exec rm -rf {} + 2>/dev/null || true
}

export_config() {
    require_cmd python3
    [ -f "$SANITIZER" ] || { error "Missing sanitizer script: $SANITIZER"; exit 1; }

    info "Exporting pi config from $PI_HOME to $CONFIG_DIR"

    # Reset generated directories so export is deterministic.
    reset_dir "$CONFIG_DIR/agents"
    reset_dir "$CONFIG_DIR/prompts"
    reset_dir "$CONFIG_DIR/themes"
    reset_dir "$CONFIG_DIR/skills"
    reset_dir "$CONFIG_DIR/installed-skills"
    reset_dir "$CONFIG_DIR/bin"
    mkdir -p "$CONFIG_DIR/config" "$CONFIG_DIR/private"
    rm -f "$CONFIG_DIR/config/settings.json" \
          "$CONFIG_DIR/config/models.json" \
          "$CONFIG_DIR/config/mcp.json" \
          "$CONFIG_DIR/config/web-search.json" \
          "$CONFIG_DIR/config/root-skill-lock.json" \
          "$CONFIG_DIR/config/skills-lock.json"
    rm -f "$CONFIG_DIR/private/models.json" \
          "$CONFIG_DIR/private/mcp.json" \
          "$CONFIG_DIR/private/web-search.json"

    # Config files
    info "  Config files"
    cp "$PI_HOME/settings.json" "$CONFIG_DIR/config/settings.json"

    # Save local secret-bearing copies, then write sanitized tracked versions.
    cp "$PI_HOME/models.json" "$CONFIG_DIR/private/models.json"
    python3 "$SANITIZER" models "$PI_HOME/models.json" "$CONFIG_DIR/config/models.json"

    if [ -f "$PI_HOME/mcp.json" ]; then
        cp "$PI_HOME/mcp.json" "$CONFIG_DIR/private/mcp.json"
        python3 "$SANITIZER" mcp "$PI_HOME/mcp.json" "$CONFIG_DIR/config/mcp.json"
    fi

    if [ -f "$PI_ROOT/web-search.json" ]; then
        cp "$PI_ROOT/web-search.json" "$CONFIG_DIR/private/web-search.json"
        python3 "$SANITIZER" web-search "$PI_ROOT/web-search.json" "$CONFIG_DIR/config/web-search.json"
    fi

    [ -f "$HOME/.agents/.skill-lock.json" ] && cp "$HOME/.agents/.skill-lock.json" "$CONFIG_DIR/config/root-skill-lock.json"
    [ -f "$AGENTS_SKILLS/skills-lock.json" ] && cp "$AGENTS_SKILLS/skills-lock.json" "$CONFIG_DIR/config/skills-lock.json"

    # Custom agents (non-symlink files only)
    info "  Custom agents"
    for entry in "$PI_HOME"/agents/*; do
        [ -L "$entry" ] && continue
        [ -f "$entry" ] && cp "$entry" "$CONFIG_DIR/agents/"
    done

    # Custom prompts (non-symlink files only)
    info "  Custom prompts"
    for entry in "$PI_HOME"/prompts/*; do
        [ -L "$entry" ] && continue
        [ -f "$entry" ] && cp "$entry" "$CONFIG_DIR/prompts/"
    done

    # Themes
    info "  Themes"
    for entry in "$PI_HOME"/themes/*; do
        [ -f "$entry" ] && cp "$entry" "$CONFIG_DIR/themes/"
    done

    # Custom skills (only real directories, not symlinks)
    info "  Custom skills (non-symlink only)"
    custom_count=0
    for entry in "$PI_HOME"/skills/*; do
        [ -L "$entry" ] && continue
        [ -d "$entry" ] || continue
        name="$(basename "$entry")"
        file_count=$(find "$entry" -type f -not -name '.DS_Store' | wc -l | tr -d ' ')
        if [ "$file_count" -gt 0 ]; then
            info "    $name ($file_count files)"
            cp -R "$entry" "$CONFIG_DIR/skills/$name"
            clean_tree "$CONFIG_DIR/skills/$name"
            ((custom_count++)) || true
        fi
    done
    info "  Exported $custom_count custom skills"

    # Installed skills from ~/.agents/skills/
    info "  Installed skills from ~/.agents/skills"
    installed_count=0
    if [ -d "$AGENTS_SKILLS" ]; then
        for entry in "$AGENTS_SKILLS"/*; do
            [ -L "$entry" ] && continue
            name="$(basename "$entry")"
            [[ "$name" == .* ]] && continue
            if [ -d "$entry" ]; then
                cp -R "$entry" "$CONFIG_DIR/installed-skills/$name"
                clean_tree "$CONFIG_DIR/installed-skills/$name"
                ((installed_count++)) || true
            elif [ -f "$entry" ]; then
                cp "$entry" "$CONFIG_DIR/installed-skills/"
            fi
        done
        info "  Exported $installed_count installed skills"
    else
        warn "  ~/.agents/skills not found, skipping"
    fi

    # Custom binaries (kept local, git may ignore some entries)
    info "  Custom binaries"
    for entry in "$PI_HOME"/bin/*; do
        [ -f "$entry" ] && cp "$entry" "$CONFIG_DIR/bin/"
    done

    echo ""
    info "Export complete"
    du -sh "$CONFIG_DIR/config" "$CONFIG_DIR/agents" "$CONFIG_DIR/prompts" \
           "$CONFIG_DIR/themes" "$CONFIG_DIR/skills" "$CONFIG_DIR/installed-skills" \
           "$CONFIG_DIR/bin" 2>/dev/null | while read -r size path; do
        echo "  $size  $(basename "$path")"
    done
    echo ""
    echo "Tracked config is sanitized. Local secret-bearing copies are in:"
    echo "  $CONFIG_DIR/private"
}

show_status() {
    echo "Pi Config Sync Status"
    echo "====================="
    echo ""
    echo "Source:  $PI_HOME"
    echo "Target:  $CONFIG_DIR"
    echo ""
    echo "Custom agents:     $(find "$PI_HOME/agents" -maxdepth 1 -name '*.md' ! -type l 2>/dev/null | wc -l | tr -d ' ')"
    echo "Custom prompts:    $(find "$PI_HOME/prompts" -maxdepth 1 -name '*.md' ! -type l 2>/dev/null | wc -l | tr -d ' ')"
    echo "Custom themes:     $(find "$PI_HOME/themes" -maxdepth 1 -name '*.json' 2>/dev/null | wc -l | tr -d ' ')"
    echo "Skill symlinks:    $(find "$PI_HOME/skills" -maxdepth 1 -type l 2>/dev/null | wc -l | tr -d ' ')"
    echo "Custom skills:     $(find "$PI_HOME/skills" -maxdepth 1 -type d ! -type l 2>/dev/null | wc -l | tr -d ' ')"
    echo "Installed skills:  $(find "$AGENTS_SKILLS" -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')"
    echo ""
    echo "Config files:"
    [ -f "$PI_HOME/settings.json" ] && echo "  [OK] settings.json" || echo "  [--] settings.json"
    [ -f "$PI_HOME/models.json" ] && echo "  [OK] models.json" || echo "  [--] models.json"
    [ -f "$PI_HOME/mcp.json" ] && echo "  [OK] mcp.json" || echo "  [--] mcp.json"
    [ -f "$PI_ROOT/web-search.json" ] && echo "  [OK] web-search.json" || echo "  [--] web-search.json"
    [ -d "$CONFIG_DIR/private" ] && echo "  [OK] local private/ dir" || echo "  [--] local private/ dir"
    [ -f "$PI_HOME/auth.json" ] && echo "  [OK] auth.json (NOT synced)" || echo "  [--] auth.json"
}

case "${1:-export}" in
    export) export_config ;;
    status) show_status ;;
    *)      echo "Usage: $0 {export|status}"; exit 1 ;;
esac
