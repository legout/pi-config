# Secrets handling

Tracked config in this repo is sanitized.

## Files with placeholders

These tracked files may contain `__REQUIRED__` placeholders:

- `config/models.json`
- `config/mcp.json`
- `config/web-search.json`

## Local-only secret copies

When you run `./sync.sh export` on a configured machine, real secret-bearing copies are written to:

- `private/models.json`
- `private/mcp.json`
- `private/web-search.json`

`private/` is gitignored and never committed.

## Bootstrap helper

Use `./bootstrap-secrets.sh` to manage local secret-bearing config:

```bash
./bootstrap-secrets.sh status
./bootstrap-secrets.sh capture
./bootstrap-secrets.sh install
```

### Typical flow

On a machine that already has working pi config:

1. `./bootstrap-secrets.sh capture`
2. keep `private/` local or sync it with your own secure file-sync method

After a restore or reset on that same machine:

1. `./restore.sh`
2. `./bootstrap-secrets.sh install`

## Restore behavior

`./restore.sh` prefers local `private/*.json` files when present.

If `private/` is missing, restore uses the sanitized tracked config and prints warnings. In that case you must re-add secrets locally.

## Auth

`auth.json` is not exported or restored by this project.
