---
name: ralph-wiggum
description: "Ralph-Wiggum ticket loop — auto-implement all ready tk tickets with worker + reviewer cycle"
---
# Ralph-Wiggum Ticket Implementation Loop

The Ralph-Wiggum loop automatically implements tk tickets one by one until all are closed.
Each iteration: pick a ready ticket → implement → review → close (or retry with feedback).

## Loop Protocol

Execute these steps in order. If any step fails, stop and report the error.

### Step 1: Pick a ticket

```bash
tk ready
```

**If the output is empty (no tickets):** You are done. Do nothing — no file changes means the loop converges and stops.

**If tickets are listed:** Pick the first one. Extract the ticket ID (e.g., `PR-xxxx`).

Run `tk start <TICKET_ID>` to mark it in_progress.

Check how many times this ticket has been reviewed:

```bash
tk notes <TICKET_ID>
```

Count reviews (lines containing "Gate:"). If the ticket has been reviewed **3 or more times**, it is stuck — skip it and move to the next ticket:

```bash
tk add-note <TICKET_ID> "BLOCKED: Escalated after 3 review cycles. Requires human intervention."
```

### Step 2: Implement the ticket (Worker Subagent)

Read the ticket file and any prior notes first:

```bash
tk show <TICKET_ID>
tk notes <TICKET_ID>
```

Then delegate implementation to the **worker** agent using the `subagent` tool:

```
subagent({
  agent: "worker",
  task: "Implement ticket <TICKET_ID>. Read the ticket at .tickets/<TICKET_ID>.md for full requirements and acceptance criteria.\n\nPRIOR ATTEMPTS — read these notes from previous iterations carefully:\n<tk notes output>\n\nIf this is a retry (notes show prior failures), reflect on what went wrong before coding:\n- What specific issues did the reviewer flag?\n- What approach was tried?\n- What must be done differently this time?\nDo NOT repeat the same failing approach.\n\nAfter implementing:\n1. Run `ty check` to lint — fix any errors\n2. Run `mypy src/` for type checking — fix any errors\n3. Run `pytest tests/ -x -v` to test — fix failures until all tests pass\n4. Re-run linters after any fixes\n\nDo NOT close the ticket. Just implement and verify.",
  context: "fresh"
})
```

Wait for the worker to complete. If the worker fails or crashes, retry once. If it fails again, add a note and move to the next ticket.

### Step 3: Review the implementation (Reviewer Subagent)

Delegate the review to the **rw-reviewer** agent:

```
subagent({
  agent: "rw-reviewer",
  task: "Review the implementation of ticket <TICKET_ID>. The ticket file is at .tickets/<TICKET_ID>.md.\n\nVerify all acceptance criteria are met. Check code quality. Run git diff to see all changes.\n\nOutput your review in this exact format:\n\n## Gate: PASS | NITS | REVISE | ESCALATE\n\n### Findings\n\nFor each finding, use this format:\n- **[CRITICAL|HIGH|MEDIUM|LOW]** Title\n  - File: <path>:<line>\n  - Evidence: <concrete observation>\n  - Remediation: <specific fix>\n\nIf Gate is PASS or NITS, briefly confirm acceptance criteria are met.\nIf Gate is REVISE, list only Critical and High findings.\nIf Gate is ESCALATE, explain why human intervention is needed.",
  context: "fresh"
})
```

### Step 4: Handle review result

Parse the reviewer's output for the **Gate** line. Record a structured note with iteration context:

**If Gate: PASS or NITS:**
```bash
tk add-note <TICKET_ID> "Review #<N>: Gate: PASS. <brief summary of what was implemented>"
tk close <TICKET_ID>
```

**If Gate: REVISE:**
```bash
tk add-note <TICKET_ID> "Review #<N>: Gate: REVISE. Issues to fix:\n\n<paste Critical and High findings with file refs and remediation>"
```
Keep the ticket in_progress. The next loop iteration will pick it up again.

**If Gate: ESCALATE:**
```bash
tk add-note <TICKET_ID> "Review #<N>: Gate: ESCALATE. Reason: <explanation>. Requires human intervention."
```
Move to the next ticket. Do not retry automatically.

### Step 5: Done

Report what happened this iteration (ticket ID, gate result, key findings). The loop will continue automatically if there are more tickets.

## Important Rules

1. **Always run `tk ready` first** — never assume which ticket to work on
2. **One ticket per iteration** — the loop handles repetition
3. **Worker must pass lint + typecheck + tests** before review
4. **Reviewer is read-only** — it never modifies files
5. **Only close on PASS or NITS** — REVISE means retry, ESCALATE means human needed
6. **Use `context: "fresh"`** for both subagents — they start clean
7. **If `tk ready` is empty, do nothing** — convergence stops the loop
8. **Max 3 review cycles per ticket** — after that, escalate and skip
9. **Worker gets prior notes on retry** — must reflect before re-attempting
10. **Reviewer output must be structured** — severity, file, evidence, remediation

## Gate Reference

| Gate | Meaning | Action |
|------|---------|--------|
| **PASS** | All acceptance criteria met, no issues | Close ticket |
| **NITS** | Acceptance criteria met, minor polish items | Close ticket (nits are optional) |
| **REVISE** | Critical or High issues found | Feed back to worker, retry |
| **ESCALATE** | Fundamentally blocked, needs human | Skip ticket, note why |

## tk CLI Reference

| Command | Purpose |
|---------|---------|
| `tk ready` | List tickets with all deps resolved (ready to work on) |
| `tk start <id>` | Set ticket to in_progress |
| `tk close <id>` | Set ticket to closed |
| `tk show <id>` | Display ticket details |
| `tk notes <id>` | Show ticket notes (prior iteration history) |
| `tk add-note <id> [text]` | Append timestamped note |
| `tk blocked` | List tickets with unresolved deps |
| `tk ls` | List all open tickets |
| `tk dep tree <id>` | Show dependency tree |
