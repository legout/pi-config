---
name: br
description: >-
  Use br (beads_rust) as the local issue tracker for AI coding agents. Trigger
  when the user mentions issues, tickets, backlog, triage, dependencies,
  blocking, ready work, or any task involving tracking work items in a git repo.
  Also trigger when the user wants to plan work, pick next tasks, manage a
  dependency graph of issues, or coordinate across multiple agents. Use this
  skill for commands like br create, br ready, br close, br dep, br sync, and
  any br CLI interaction. Even if the user just says "what should I work on
  next" or "create a ticket for this", use this skill to ensure correct br
  usage patterns.
---

# br — Local-First Issue Tracker for AI Agents

br is a CLI issue tracker (binary: `br`) that stores issues in SQLite with JSONL
export for git collaboration. It's designed specifically for AI coding agents
with structured JSON output, dependency-aware work queues, and non-invasive
operation.

## Critical Rules

These rules exist because violating them causes real problems in agent
workflows — broken sync, blocked sessions, or corrupted data:

| Rule | Why it matters |
|------|----------------|
| Binary is **`br`** (never `bd`) | `bd` is the original Go version — it has different behavior |
| **Always use `--json`** | Structured output for parsing; human output formats change |
| **Never run bare `bv`** | `bv` is an interactive TUI that blocks the agent session forever |
| **Sync is explicit** | `br sync --flush-only` exports DB to JSONL — nothing else does |
| **Git is your job** | br never runs git commands — you must `git add .beads/ && git commit` |
| **No dependency cycles** | `br dep cycles` must always return empty or the ready queue breaks |
| **Set actor identity** | Use `--actor "$ACTOR"` or `BR_ACTOR` env var for audit trail attribution |
| **Suppress Rust noise** | `RUST_LOG=error br ...` keeps stderr clean for agent parsing |

## Standard Workflow

This is the lifecycle every issue follows. Agents should stick to this pattern
to maintain a clean backlog and reliable sync state:

```bash
ACTOR="${BR_ACTOR:-assistant}"

# 1. Find actionable work (unblocked, open issues)
br ready --json

# 2. Claim an issue atomically (assignee + status in one step)
br update --actor "$ACTOR" <id> --claim

# 3. Implement the task...
#    Discover new issues? Create them linked to current work:
br create --actor "$ACTOR" "Edge case found" -t bug -p 1 \
  --deps discovered-from:<id> --json

# 4. Close with evidence
br close --actor "$ACTOR" <id> --reason "Implemented X in commit abc123"

# 5. Sync to git (ALWAYS before committing)
br sync --flush-only
git add .beads/ && git commit -m "Update issues"
```

## Essential Commands

All commands below accept `--json` for structured output. Always use it when
the output will be parsed programmatically.

### Issue Lifecycle

```bash
ACTOR="${BR_ACTOR:-assistant}"

br init                                              # Initialize .beads/ in a repo
br create --actor "$ACTOR" "Title" -p 1 -t task      # Create (priority 0-4)
br q --actor "$ACTOR" "Quick note"                   # Quick capture (prints ID only)
br show <id> --json                                  # Full issue details
br update --actor "$ACTOR" <id> --status in_progress  # Change status
br update --actor "$ACTOR" <id> --priority 0         # Reprioritize
br update --actor "$ACTOR" <id> --claim               # Atomic claim-and-start
br close --actor "$ACTOR" <id> --reason "Done"       # Close with reason
br close --actor "$ACTOR" <id1> <id2> --reason "..."  # Close multiple at once
br reopen --actor "$ACTOR" <id>                       # Reopen closed issue
```

### Creating Issues

```bash
br create --actor "$ACTOR" "Title" \
  --priority 1 \              # 0-4 (0=critical, 4=backlog)
  --type task \               # task, bug, feature, epic, question, docs
  --assignee "user@..." \     # Optional assignee
  --labels backend,auth \     # Comma-separated labels
  --description "..."         # Detailed description
```

### Querying

```bash
br ready --json                                # Unblocked actionable issues
br list --json                                 # All issues
br list --status open --sort priority --json    # Filtered + sorted
br list --priority 0-1 --json                  # Priority range filter
br list --assignee alice --json                # By assignee
br blocked --json                              # Blocked issues and why
br search "keyword" --json                     # Full-text search
br show <id> --json                            # Single issue with deps
br stale --days 30 --json                      # Stale issues
br count --by status --json                    # Count with grouping
```

### Dependency Management

The dependency graph is what makes br powerful for agents — it answers "what
can I work on right now?" without human triage.

```bash
br dep add <child> <parent>          # child depends on parent (parent blocks child)
br dep add <id> <dep> --type blocks  # Explicit block type
br dep remove <child> <parent>       # Remove dependency
br dep list <id> --json              # Dependencies for one issue
br dep tree <id> --json              # Full dependency tree
br dep cycles --json                 # Find cycles (MUST return empty!)
```

When closing an issue, use `--suggest-next` to discover newly-unblocked work:
```bash
br close --actor "$ACTOR" <id> --reason "Done" --suggest-next --json
# Returns: { "closed": "bd-123", "unblocked": ["bd-456", "bd-789"] }
```

### Labels and Comments

```bash
br label add <id> backend auth       # Add labels
br label remove <id> urgent          # Remove label
br label list <id>                   # Issue's labels
br label list-all                    # All project labels

ACTOR="${BR_ACTOR:-assistant}"
br comments add --actor "$ACTOR" <id> --message "Note" --json
br comments list <id> --json
```

### Sync (Explicit — Never Automatic)

br separates tracking (SQLite) from collaboration (JSONL via git). You must
bridge them explicitly:

```bash
br sync --flush-only                 # Export DB → JSONL (before git commit)
br sync --import-only                # Import JSONL → DB (after git pull)
br sync --status                     # Check sync state
```

**After making changes:**
```bash
br sync --flush-only
git add .beads/ && git commit -m "Update issues"
```

**After pulling from remote:**
```bash
git pull
br sync --import-only
```

### Diagnostics

```bash
br doctor                            # Full health check
br stats --json                      # Project statistics
br config list                       # Show all configuration
br config get id.prefix              # Get specific value
br config set defaults.priority=1    # Set value
br where                             # Show workspace paths
br version                           # Version info
br lint --json                       # Lint issues for problems
```

## Priority Scale

| # | Meaning | When to use |
|---|---------|-------------|
| 0 | Critical | Production down, data loss, security issue |
| 1 | High | Important, should be done soon |
| 2 | Medium | Default — normal work |
| 3 | Low | Nice to have, when time permits |
| 4 | Backlog | Future consideration, not planned |

## Issue Types

`task`, `bug`, `feature`, `epic`, `question`, `docs`

## Output Formats

| Flag | Use case |
|------|----------|
| `--json` | Default for agents — full structured data |
| `--format toon` | Token-optimized (decode with `tru --decode \| jq`) |
| (no flag) | Human-readable with colors — for user display only |

## bv Integration (beads_viewer)

**CRITICAL: Never run bare `bv`** — it launches an interactive TUI that blocks
the agent session. Always use robot-mode flags:

```bash
bv --robot-next                      # Single top pick + claim command
bv --robot-triage                    # Full triage with recommendations
bv --robot-plan                      # Parallel execution tracks
bv --robot-insights | jq '.Cycles'   # Graph health check
bv --robot-priority                  # Priority misalignment detection
bv --robot-alerts                    # Stale issues, blocking cascades
```

## Error Handling

br uses structured exit codes and JSON error objects:

| Code | Category | Example |
|------|----------|---------|
| 0 | Success | Command completed |
| 1 | Internal | Unexpected error |
| 2 | Database | Not initialized, locked |
| 3 | Issue | Not found, ambiguous ID |
| 4 | Validation | Invalid priority value |
| 5 | Dependency | Cycle detected |
| 6 | Sync/JSONL | Parse error |
| 7 | Config | Missing configuration |
| 8 | I/O | File system error |

Error JSON shape (on stderr or stdout depending on command):
```json
{
  "error_code": 3,
  "kind": "not_found",
  "message": "Issue not found: bd-xyz999",
  "recovery_hints": ["Check the issue ID spelling", "Use 'br list' to find valid IDs"]
}
```

Always check exit codes before parsing output. The `recovery_hints` array
contains actionable suggestions the agent can follow to self-recover.

## Session End Checklist

Before ending any work session, run this sequence to ensure clean state:

```bash
br sync --flush-only
git add .beads/ && git commit -m "Update issues"
git status  # Verify clean state
```

## Triage Decision Matrix

When classifying issues during triage, each issue goes into exactly one bucket:

| Classification | Action |
|---------------|--------|
| Implemented | Close with evidence (commit hash, PR, file path) |
| Out of scope | Close with explicit boundary reason |
| Needs clarification | Add a comment with specific unanswered questions |
| Actionable | Keep open; correct status/priority/labels/dependencies |

During large triage efforts, checkpoint every few updates:
```bash
br ready --json && br blocked --json
```

## Anti-Patterns

Avoid these — they cause real problems:

- Running `br sync` without `--flush-only` or `--import-only` (undefined behavior)
- Forgetting sync before git commit (other agents can't see your changes)
- Creating circular dependencies (breaks the ready queue)
- Running bare `bv` (blocks the agent session)
- Assuming br auto-commits (it never does)
- Inventing evidence for closure — if unsure, add a comment instead
- Modifying unrelated issues during triage (scope creep)
- Adding speculative dependencies (over-constrains the graph)

## Storage Layout

```
.beads/
  beads.db        # SQLite database (primary source of truth)
  beads.db-shm    # SQLite shared memory (WAL mode)
  beads.db-wal    # SQLite write-ahead log
  issues.jsonl    # JSONL export (for git collaboration)
  config.yaml     # Project configuration
  metadata.json   # Workspace metadata
```

## Quick Troubleshooting

```bash
br doctor                    # Full diagnostics — run this first
br dep cycles                # Must return empty
br config list               # Check settings
which br                     # Verify installed
```

**"Database locked"**: Another br process is running. Check with `pgrep -f "br "`.

**"Not initialized"**: Run `br init` in the repo root.

**Verbose debugging**: `RUST_LOG=debug br <command>` or `br -vv <command>`.
