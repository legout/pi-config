# Pi Config Sync

Centralized pi coding agent configuration for syncing across machines.

## Structure

```text
pi-config/
├── config/                  # Tracked, sanitized config files
│   ├── settings.json
│   ├── models.json          # sanitized
│   ├── mcp.json             # sanitized
│   ├── web-search.json      # sanitized
│   └── SECRETS.md           # how local secrets work
├── private/                 # Local-only real secret-bearing config (gitignored)
├── agents/                  # Custom agent definitions
├── prompts/                 # Custom prompt templates
├── themes/                  # Custom themes
├── skills/                  # Custom non-symlink skills
├── installed-skills/        # Mirror of ~/.agents/skills
├── scripts/
│   └── sanitize_configs.py  # export-time secret scrubbing
├── bin/                     # Local binaries (some may be gitignored)
├── sync.sh                  # Export current machine config into this repo
├── restore.sh               # Restore config onto a machine
├── bootstrap-secrets.sh     # Manage local private secret-bearing config
└── .gitignore
```

## Security model

Tracked config is **sanitized**.

Real secrets are written only to local gitignored files under:

- `private/models.json`
- `private/mcp.json`
- `private/web-search.json`

`auth.json` is **not** exported or restored.

## Quick start

### On the source machine

```bash
cd ~/coding/pi-config
./sync.sh export

git add -A
git commit -m "sync pi config"
git push
```

### On another machine

```bash
git clone git@github.com:legout/pi-config.git ~/coding/pi-config
cd ~/coding/pi-config
./restore.sh
./bootstrap-secrets.sh status
```

If `private/` is absent on that machine, `restore.sh` will restore sanitized config and warn you to add secrets locally.

## Secret bootstrap workflow

```bash
# Inspect whether local private config exists
./bootstrap-secrets.sh status

# Capture current live secrets into local gitignored private/
./bootstrap-secrets.sh capture

# Reinstall local private secrets into ~/.pi after restore or reset
./bootstrap-secrets.sh install
```

This is useful when a machine already has working provider config and you want to persist it locally without ever committing those secrets.

## Determinism

Recent improvements:

- `sync.sh export` wipes generated repo mirrors before re-exporting, so removed files do not linger in git.
- `restore.sh` now **replaces** existing installed skills instead of skipping them.
- `restore.sh` prunes removed repo-managed agents/prompts/themes before restoring.
- skill symlinks are recreated with `ln -sfn`, so they converge on the repo state.

## What is synced

- pi settings and sanitized config
- custom agents
- custom prompts
- themes
- custom non-symlink skills
- installed skills from `~/.agents/skills`
- skill lock files

## What is not synced

- `auth.json`
- session/history/cache files
- crash logs
- local secret-bearing files in `private/`
- ignored binaries like `bin/fd`
