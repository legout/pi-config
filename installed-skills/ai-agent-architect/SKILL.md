---
name: ai-agent-architect
description: Design and implement practical AI agents using a production-oriented framework. Use this skill whenever the user wants to build an AI agent, decide whether a workflow should become an agent, choose between single-agent and multi-agent designs, define tools/instructions/guardrails, add human-in-the-loop controls, or scaffold an agentic workflow for real systems. Trigger for requests about agents, copilots, tool-using assistants, orchestration, handoffs, manager-worker patterns, agent guardrails, or productionizing multi-step LLM workflows even when the user does not explicitly ask for an “agent architecture.”
---

# AI Agent Architect

Use this skill to help the user design, review, or implement an AI agent grounded in the principles from *A Practical Guide to Building Agents*.

If the user is vague, do not jump straight into code. First determine whether the problem actually needs an agent and what level of autonomy is appropriate.

## Core principles

1. **Do not force an agent where deterministic software is enough.**
   Prefer conventional automation when the workflow is simple, stable, and rule-based.

2. **Start with a single agent.**
   Maximize a single agent with clear tools and instructions before splitting into multiple agents.

3. **Separate the design into model, tools, and instructions.**
   Treat these as independent design decisions.

4. **Use layered guardrails.**
   Combine prompt-level guidance, rules-based checks, safety checks, tool restrictions, and human intervention.

5. **Design for iteration.**
   Start with a capable model, establish a quality baseline with evals, then optimize for cost and latency.

6. **Prefer practical deliverables.**
   Give the user an architecture, decision rationale, guardrails, eval plan, and an implementation scaffold when requested.

## Start by identifying the user’s stage

Classify the request into one of these modes and adapt your response:

- **Suitability check** — “Should this even be an agent?”
- **Architecture design** — Define workflow, tools, prompts, orchestration, and risks.
- **Implementation scaffold** — Produce code, pseudocode, or project structure.
- **Hardening/review** — Improve guardrails, failure handling, evals, and rollout plan.

## Questions to ask when context is missing

Ask only the questions needed to unblock a good design.

1. What user goal should the system complete end-to-end?
2. What decisions require judgment rather than fixed rules?
3. What inputs are structured vs. unstructured?
4. Which systems, APIs, databases, documents, or UIs must the agent read from?
5. Which systems must it write to or act on?
6. What actions are sensitive, expensive, irreversible, or customer-facing?
7. What should happen when the agent is uncertain or fails repeatedly?
8. What does success look like: accuracy, speed, conversion, deflection, cycle time, etc.?
9. Is this an MVP, an internal tool, or a production deployment?
10. Does the user want a plan only, or a concrete implementation scaffold?

## Decide whether this should be an agent

Recommend an agent only when the workflow clearly benefits from one or more of these:

- **Complex decision-making** with exceptions, tradeoffs, or context-sensitive judgment
- **Difficult-to-maintain rules** where deterministic logic is brittle or costly to update
- **Heavy use of unstructured data** such as natural language, PDFs, tickets, emails, or conversations

If the use case does **not** meet these criteria, explicitly recommend a simpler deterministic approach.

## Design workflow

When designing the solution, work through these steps in order.

### 1) Define the workflow boundary

State:
- the user goal
- what the agent owns
- what remains outside scope
- the completion condition
- the failure / escalation condition

### 2) Choose the model strategy

Default approach:
- Start prototyping with the most capable model available for all important reasoning steps.
- Establish a baseline with evals.
- Replace easier subtasks with cheaper/faster models only after quality is acceptable.

Call out where the workflow needs:
- heavy reasoning
- classification/routing
- retrieval/summarization
- multimodality
- low latency

### 3) Define tools

Group tools into these categories:

- **Data tools** — retrieve context, search systems, read docs, query databases
- **Action tools** — update records, create tickets, send emails, execute workflows
- **Orchestration tools** — specialized sub-agents invoked as tools when justified

For each tool, specify:
- name
- purpose
- inputs/outputs
- when to use it
- whether it is read-only or write-capable
- risk level: low / medium / high

If many tools overlap semantically or confuse routing, recommend simplifying or splitting agents.

### 4) Write instructions as an agent routine

Convert policies, SOPs, and help-center documents into numbered, unambiguous instructions.

Good instructions:
- break the task into explicit steps
- map each step to a clear action or output
- anticipate missing information and common edge cases
- define when to ask the user a question
- define when to call a tool
- define when to stop

If the user provides source documents, transform them into an agent-ready numbered routine.

### 5) Choose an orchestration pattern

Default recommendation: **single agent first**.

Only recommend multiple agents when complexity clearly justifies it.

#### Use a single agent when
- the workflow is still manageable
- the toolset is distinct and understandable
- one agent can maintain the full context without confusion

#### Use a manager pattern when
- one central agent should remain in control
- specialized agents are best treated like callable tools
- the user experience should feel unified and synthesized

#### Use a decentralized / handoff pattern when
- specialist agents should fully take over parts of the workflow
- the workflow resembles triage or domain routing
- no central agent needs to keep synthesizing every response

Explain *why* the chosen pattern fits.

### 6) Add guardrails

Always propose layered guardrails. At minimum, consider:

- relevance checks
- safety / prompt-injection / jailbreak detection
- PII handling
- moderation / content safety
- tool safeguards based on risk
- rules-based protections such as regex, allowlists, deny-lists, and length limits
- output validation for policy, tone, and structure

For high-risk tools, require extra review, confirmations, or human approval.

### 7) Plan human intervention

Define concrete triggers for handing control back to a human or the user, especially for:
- repeated failures or retry thresholds
- high-risk, irreversible, or financially sensitive actions
- low-confidence decisions
- missing permissions or broken dependencies

### 8) Define evals and rollout

Always recommend a lightweight evaluation plan before broad rollout.

Include:
- 3-5 representative tasks
- success criteria
- failure cases / adversarial cases
- tool-selection correctness
- guardrail tests
- escalation tests
- latency / cost checkpoints after quality is acceptable

## Response format

When the user wants a plan or architecture, prefer this structure:

# Agent recommendation
## 1. Should this be an agent?
## 2. Proposed workflow boundary
## 3. Model strategy
## 4. Tool inventory
## 5. Agent instructions / routine
## 6. Orchestration pattern
## 7. Guardrails
## 8. Human intervention triggers
## 9. Evals and rollout plan
## 10. MVP implementation steps

## Implementation guidance

If the user asks for code or a scaffold:

1. Start with the **smallest viable agent architecture**.
2. Prefer a single runnable loop before building handoffs.
3. Stub tools cleanly with obvious interfaces.
4. Mark high-risk actions behind approval gates.
5. Include exit conditions, retries, and escalation hooks.
6. Keep prompts/instructions explicit and maintainable.
7. If the framework is unspecified, provide framework-agnostic pseudocode or a minimal Python scaffold.

## Review guidance

When reviewing an existing agent design or codebase, check for:

- an agent being used where deterministic automation would be simpler
- vague instructions that do not map to clear actions
- overlapping tools that cause routing ambiguity
- multi-agent complexity introduced too early
- missing completion conditions or retry limits
- missing guardrails around risky tools
- no human-in-the-loop path
- no eval plan or no baseline before optimization

## Reference material

If you need the condensed source guidance, read:
- `references/practical-guide-summary.md`

Use it when you want sharper decision criteria, orchestration heuristics, or a guardrail checklist.
