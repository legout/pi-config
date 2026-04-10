# Pi Config Sync

Centralized pi coding agent configuration — sync your full pi setup across machines, safely.

All tracked config files are **sanitized**: real API keys are replaced with `__REQUIRED__` placeholders before they ever reach git. Your actual secrets live only in local gitignored files under `private/`.

---

## Table of Contents

- [Repository Structure](#repository-structure)
- [Security Model](#security-model)
- [Required API Keys](#required-api-keys)
- [Setup on a Brand-New Machine](#setup-on-a-brand-new-machine)
- [Updating an Existing Machine](#updating-an-existing-machine)
- [Exporting Config from a Machine](#exporting-config-from-a-machine)
- [Secret Bootstrap Workflow](#secret-bootstrap-workflow)
- [What Gets Synced](#what-gets-synced)

---

## Repository Structure

```text
pi-config/
├── config/                  # Tracked, sanitized config (safe to commit)
│   ├── settings.json        # pi settings, packages, skills list, theme
│   ├── models.json          # model providers — apiKeys replaced with __REQUIRED__
│   ├── mcp.json             # MCP servers — tokens replaced with __REQUIRED__
│   ├── web-search.json      # web search — Gemini key replaced with __REQUIRED__
│   ├── SECRETS.md           # internal docs on how secrets handling works
│   ├── skills-lock.json
│   └── root-skill-lock.json
├── private/                 # Local-only secret-bearing config (gitignored, NEVER committed)
│   ├── models.json
│   ├── mcp.json
│   └── web-search.json
├── agents/                  # Custom agent definitions
├── prompts/                 # Custom prompt templates
├── themes/                  # Custom themes
├── skills/                  # Custom non-symlink skills
├── installed-skills/        # Mirror of ~/.agents/skills/
├── scripts/
│   └── sanitize_configs.py  # Strips API keys during export
├── bin/                     # Local binaries (gitignored where needed)
├── sync.sh                  # Export current machine config → this repo
├── restore.sh               # Restore config from this repo → a machine
├── bootstrap-secrets.sh     # Manage local private/ secrets
└── .gitignore               # Blocks private/, auth.json, sessions, caches
```

---

## Security Model

| Layer | What happens |
|---|---|
| **Export** (`sync.sh export`) | Copies live config to `private/` (real keys), then runs `sanitize_configs.py` to write `config/` with `__REQUIRED__` placeholders |
| **Restore** (`restore.sh`) | Prefers `private/` if present (real keys). Falls back to `config/` (placeholders) and warns you |
| **Bootstrap** (`bootstrap-secrets.sh`) | Captures/installs `private/` locally without touching tracked files |
| **Git** | `private/` is gitignored and has **never** been committed. `auth.json` is gitignored too |

`auth.json` (pi's own auth) is **never** exported, synced, or restored by this project.

---

## Required API Keys

The tracked config files contain `__REQUIRED__` placeholders wherever an API key is needed. Below is the complete list. You must replace each one with a real key for the corresponding service to work.

### `config/models.json` — Model Providers

| Placeholder location | Service | Key format | Where to get a key |
|---|---|---|---|
| `providers.openrouter.apiKey` | **OpenRouter** | `sk-or-v1-...` | [openrouter.ai/keys](https://openrouter.ai/keys) |
| `providers.siemens.apiKey` | **Siemens AI API** | `SIAK-...` | Internal Siemens developer portal |
| `providers.zai.apiKey` | **Z.ai** | Hex string | Z.ai developer console |

> **Note:** The `ollama` provider uses `"apiKey": "none"` (local-only, no key needed).

### `config/web-search.json` — Web Search

| Placeholder location | Service | Key format | Where to get a key |
|---|---|---|---|
| `geminiApiKey` | **Google Gemini** | `AIzaSy...` | [Google AI Studio](https://aistudio.google.com/apikey) |

### `config/mcp.json` — MCP Servers

| Placeholder location | Service | Key format | Where to get a key |
|---|---|---|---|
| `mcpServers.zai-web-reader.headers.Authorization` | **Z.ai Web Reader** | `Bearer ...` (same Z.ai key as above) | Same Z.ai key as `providers.zai.apiKey` |
| `mcpServers.zai-vision.env.Z_AI_API_KEY` | **Z.ai Vision MCP** | Same Z.ai key | Same Z.ai key as `providers.zai.apiKey` |

> **Tip:** The Z.ai key is shared across 3 locations. Once you have it, replace all three `__REQUIRED__` entries.

### Summary of keys you need

| # | Key | Used in | Free tier? |
|---|---|---|---|
| 1 | Google Gemini API key | `web-search.json` | ✅ Yes |
| 2 | OpenRouter API key | `models.json` | ✅ Free models available |
| 3 | Z.ai API key | `models.json`, `mcp.json` (×2) | Check Z.ai |
| 4 | Siemens AI API key | `models.json` | Internal only |

---

## Setup on a Brand-New Machine

Use this when you have a fresh machine with pi installed but no config yet.

### 1. Clone the repo

```bash
git clone https://github.com/legout/pi-config.git ~/coding/pi-config
cd ~/coding/pi-config
```

### 2. Restore config (sanitized version)

```bash
./restore.sh
```

This copies all agents, prompts, skills, themes, and sanitized config to `~/.pi/agent/` and `~/.pi/`. It also runs `pi update` to install configured packages and extensions.

If you'd rather run `pi update` yourself later:

```bash
RUN_PI_UPDATE=0 ./restore.sh
```

### 3. Add your API keys

Since there is no `private/` directory yet, `restore.sh` installs the sanitized config with `__REQUIRED__` placeholders. You need to add real keys:

**Option A — Edit the live config files directly:**

```bash
# Model providers
nano ~/.pi/agent/models.json

# MCP servers
nano ~/.pi/agent/mcp.json

# Web search
nano ~/.pi/web-search.json
```

Replace every `__REQUIRED__` with your actual key (see the [Required API Keys](#required-api-keys) table above).

**Option B — Use the bootstrap helper (recommended):**

If you have the keys handy:

```bash
# Create private/ with real keys (you'll need to create the files manually)
mkdir -p private

# For each file, copy the sanitized version and fill in real keys:
cp config/models.json private/models.json
cp config/mcp.json private/mcp.json
cp config/web-search.json private/web-search.json

# Now edit private/*.json and replace __REQUIRED__ with real keys
nano private/models.json
nano private/mcp.json
nano private/web-search.json

# Install into live pi config
./bootstrap-secrets.sh install
```

### 4. Verify everything works

```bash
pi                          # Should start with your configured default model
./bootstrap-secrets.sh status   # Should show "present" (not "placeholder-only")
```

---

## Updating an Existing Machine

Use this when you've already set up this machine before and want to pull the latest config changes.

### If you already have `private/` with real keys

```bash
cd ~/coding/pi-config
git pull
./restore.sh
```

`restore.sh` will automatically use your existing `private/*.json` (real keys) over the sanitized `config/*.json`. No re-keying needed.

### If you made changes on another machine

On the **source** machine (where the changes live):

```bash
cd ~/coding/pi-config
./sync.sh export            # Re-export all config + agents + skills
git add -A
git commit -m "sync: update config"
git push
```

Then on **every other** machine:

```bash
cd ~/coding/pi-config
git pull
./restore.sh
```

### Quick check: is everything in sync?

```bash
./bootstrap-secrets.sh status
```

This shows whether `private/` and the live pi config have real keys or still contain placeholders.

---

## Exporting Config from a Machine

Run this on a machine that has a working pi setup to capture its config into this repo:

```bash
cd ~/coding/pi-config
./sync.sh export
```

This will:

1. **Wipe** the repo's generated directories (agents, prompts, skills, etc.) for a clean state
2. **Copy** live config from `~/.pi/agent/` and `~/.pi/`
3. **Save** real secret-bearing copies to `private/` (gitignored)
4. **Sanitize** and write tracked copies to `config/` (safe to commit)

After export:

```bash
git add -A
git commit -m "sync: $(date +%Y-%m-%d)"
git push
```

> **Never** commit the `private/` directory. The `.gitignore` blocks it, but always double-check with `git status` before pushing.

---

## Secret Bootstrap Workflow

The `bootstrap-secrets.sh` helper manages the `private/` directory without touching tracked files:

```bash
# Show current state of private/ and live config
./bootstrap-secrets.sh status

# Capture live secrets from ~/.pi into local private/
./bootstrap-secrets.sh capture

# Install private/ secrets into live ~/.pi (e.g. after a restore or reset)
./bootstrap-secrets.sh install
```

### Typical workflows

**First setup on a machine:**

```bash
./restore.sh                  # Installs sanitized config
# Edit private/*.json with real keys
./bootstrap-secrets.sh install
```

**After a pi reset on the same machine (private/ still exists):**

```bash
./restore.sh                  # Automatically uses private/ for real keys
```

**Switching machines and want to bring keys along:**

You need to securely transfer `private/` yourself (USB, encrypted archive, password manager, etc.). This repo deliberately does not handle key transport.

---

## What Gets Synced

| Synced (tracked in git) | Not synced (gitignored) |
|---|---|
| pi settings (`settings.json`) | `auth.json` |
| Sanitized model provider config | `private/` (real API keys) |
| Sanitized MCP server config | Session data, history |
| Sanitized web search config | Crash logs, caches |
| Custom agents, prompts, themes | `bin/fd` and other binaries |
| Custom non-symlink skills | |
| Installed skills from `~/.agents/skills/` | |
| Skill lock files | |

---

## Scripts Reference

| Script | Purpose |
|---|---|
| `sync.sh export` | Export live pi config from this machine into the repo (sanitized to `config/`, real to `private/`) |
| `sync.sh status` | Show what exists in live pi config vs. repo |
| `restore.sh` | Restore repo config onto this machine (prefers `private/` if present) |
| `bootstrap-secrets.sh status` | Show whether `private/` and live config have real keys or placeholders |
| `bootstrap-secrets.sh capture` | Copy live pi secrets into local `private/` |
| `bootstrap-secrets.sh install` | Copy `private/` secrets into live pi config |
| `scripts/sanitize_configs.py` | Strip API keys from JSON config (used internally by `sync.sh`) |
