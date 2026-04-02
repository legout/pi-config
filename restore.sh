#!/usr/bin/env bash
set -euo pipefail

PI_HOME="${PI_HOME:-$HOME/.pi/agent}"
PI_ROOT="${PI_ROOT:-$HOME/.pi}"
AGENTS_SKILLS="${AGENTS_SKILLS:-$HOME/.agents/skills}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }
step()  { echo -e "${BLUE}[STEP]${NC} $*"; }

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || { error "Missing required command: $1"; exit 1; }
}

backup_if_exists() {
    local path="$1"
    if [ -e "$path" ] || [ -L "$path" ]; then
        cp -R "$path" "$path.bak" 2>/dev/null || true
        warn "  Backed up existing $(basename "$path") -> $(basename "$path").bak"
    fi
}

copy_config_with_private() {
    local name="$1"
    local target="$2"
    local tracked="$CONFIG_DIR/config/$name"
    local private="$CONFIG_DIR/private/$name"
    local source="$tracked"

    [ -f "$tracked" ] || return 0
    if [ -f "$private" ]; then
        source="$private"
        info "  $name <- private/$name"
    else
        info "  $name <- config/$name"
        if grep -q "__REQUIRED__" "$tracked" 2>/dev/null; then
            warn "  $name still contains placeholders; add local secrets after restore"
        fi
    fi

    backup_if_exists "$target"
    mkdir -p "$(dirname "$target")"
    cp "$source" "$target"
}

prune_unmanaged_files() {
    local repo_dir="$1"
    local target_dir="$2"
    local pattern="$3"
    local skip_symlinks="${4:-0}"

    mkdir -p "$target_dir"
    for target in "$target_dir"/$pattern; do
        [ -e "$target" ] || continue
        if [ "$skip_symlinks" = "1" ] && [ -L "$target" ]; then
            continue
        fi
        local base
        base="$(basename "$target")"
        if [ ! -e "$repo_dir/$base" ]; then
            rm -rf "$target"
            info "  pruned $base"
        fi
    done
}

# Safety check
if [ ! -f "$CONFIG_DIR/config/settings.json" ]; then
    error "No exported config found in $CONFIG_DIR/config/"
    echo "Run ./sync.sh export first on the source machine."
    exit 1
fi

require_cmd jq

echo "=========================================="
echo "       Pi Config Restore"
echo "       Target: $PI_HOME"
echo "=========================================="
echo ""

step "Ensuring directories exist"
mkdir -p "$PI_HOME"/{agents,prompts,themes,skills,bin,extensions,.pi/todos}
mkdir -p "$AGENTS_SKILLS"
mkdir -p "$PI_ROOT"/{todos,history}

step "Restoring config files"
copy_config_with_private "settings.json" "$PI_HOME/settings.json"
copy_config_with_private "models.json" "$PI_HOME/models.json"
copy_config_with_private "mcp.json" "$PI_HOME/mcp.json"
copy_config_with_private "web-search.json" "$PI_ROOT/web-search.json"

for f in root-skill-lock.json skills-lock.json; do
    src="$CONFIG_DIR/config/$f"
    [ -f "$src" ] || continue
    if [ "$f" = "root-skill-lock.json" ]; then
        target="$HOME/.agents/.skill-lock.json"
    else
        target="$AGENTS_SKILLS/skills-lock.json"
    fi
    mkdir -p "$(dirname "$target")"
    cp "$src" "$target"
    info "  $f -> $target"
done

step "Pruning removed repo-managed files"
prune_unmanaged_files "$CONFIG_DIR/agents" "$PI_HOME/agents" "*.md" 1
prune_unmanaged_files "$CONFIG_DIR/prompts" "$PI_HOME/prompts" "*.md" 0
prune_unmanaged_files "$CONFIG_DIR/themes" "$PI_HOME/themes" "*.json" 0

step "Restoring custom agents"
agent_count=0
for f in "$CONFIG_DIR"/agents/*.md; do
    [ -f "$f" ] || continue
    name="$(basename "$f")"
    target="$PI_HOME/agents/$name"
    if [ -L "$target" ]; then
        warn "  Skipping $name (symlink to git package)"
        continue
    fi
    cp "$f" "$target"
    info "  $name"
    ((agent_count++)) || true
done
info "  Restored $agent_count agents"

step "Restoring custom prompts"
prompt_count=0
for f in "$CONFIG_DIR"/prompts/*.md; do
    [ -f "$f" ] || continue
    name="$(basename "$f")"
    cp "$f" "$PI_HOME/prompts/$name"
    info "  $name"
    ((prompt_count++)) || true
done
info "  Restored $prompt_count prompts"

step "Restoring themes"
for f in "$CONFIG_DIR"/themes/*.json; do
    [ -f "$f" ] || continue
    name="$(basename "$f")"
    cp "$f" "$PI_HOME/themes/$name"
    info "  $name"
done

step "Restoring custom skills"
skill_count=0
for d in "$CONFIG_DIR"/skills/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    target="$PI_HOME/skills/$name"
    if [ -L "$target" ]; then
        warn "  Skipping $name (symlink to installed package)"
        continue
    fi
    rm -rf "$target"
    cp -R "$d" "$target"
    info "  $name"
    ((skill_count++)) || true
done
info "  Restored $skill_count custom skills"

step "Restoring installed skills (~/.agents/skills)"
installed_count=0
if [ -d "$CONFIG_DIR/installed-skills" ]; then
    for d in "$CONFIG_DIR"/installed-skills/*/; do
        [ -d "$d" ] || continue
        name="$(basename "$d")"
        [[ "$name" == .* ]] && continue
        target="$AGENTS_SKILLS/$name"
        rm -rf "$target"
        cp -R "$d" "$target"
        info "  $name"
        ((installed_count++)) || true
    done
    for f in "$CONFIG_DIR"/installed-skills/*.json; do
        [ -f "$f" ] || continue
        name="$(basename "$f")"
        cp "$f" "$AGENTS_SKILLS/$name"
    done
fi
info "  Restored $installed_count installed skills"

step "Recreating skill symlinks"
link_count=0
while IFS= read -r skill_ref; do
    if [[ "$skill_ref" =~ \.\./\.\./\.agents/skills/([^/]+)/SKILL\.md ]]; then
        skill_name="${BASH_REMATCH[1]}"
        link="$PI_HOME/skills/$skill_name"
        target="$HOME/.agents/skills/$skill_name"
        if [ -d "$target" ]; then
            ln -sfn "$target" "$link"
            info "  $skill_name -> ~/.agents/skills/$skill_name"
            ((link_count++)) || true
        fi
    fi
done < <(jq -r '.skills[]? // empty' "$CONFIG_DIR/config/settings.json" 2>/dev/null)
info "  Ensured $link_count symlinks"

step "Restoring custom binaries"
for f in "$CONFIG_DIR"/bin/*; do
    [ -f "$f" ] || continue
    name="$(basename "$f")"
    cp "$f" "$PI_HOME/bin/$name"
    chmod +x "$PI_HOME/bin/$name"
    info "  $name"
done

echo ""
echo "=========================================="
echo "       Restore Complete"
echo "=========================================="
echo ""
warn "auth.json is still not restored by this project."
warn "If private/ is absent, sanitized placeholder config was restored."
info "Restart pi after restore."
