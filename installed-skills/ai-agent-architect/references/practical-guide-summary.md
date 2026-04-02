# Practical Guide Summary for Building Agents

This reference distills the key ideas from *A Practical Guide to Building Agents* into a compact checklist for skill usage.

## What makes something an agent?

An agent is not just a chatbot or one-shot LLM call. It is a system that:

1. Uses an LLM to manage workflow execution and make decisions
2. Knows when the workflow is complete
3. Can recover, halt, or hand control back when needed
4. Uses tools to gather context and take actions inside guardrails

## When to build an agent

Prefer an agent when the workflow involves at least one of these:

- **Complex decision-making** — nuanced judgment, exceptions, contextual tradeoffs
- **Brittle or expensive rule systems** — hard-to-maintain rulesets
- **Unstructured inputs** — emails, tickets, PDFs, documents, conversations, natural language

Prefer deterministic software when the task is straightforward, predictable, and easy to encode as rules.

## Core design building blocks

Every agent design should identify:

### 1) Model
Choose model(s) based on reasoning difficulty, latency, and cost.

Recommended sequence:
1. Start with the strongest model to establish quality
2. Build evals
3. Swap easier subtasks to smaller models if quality holds

### 2) Tools
Tools generally fall into three groups:

- **Data tools** — retrieve information
- **Action tools** — change state or perform work
- **Orchestration tools** — other agents used as tools

Good tools are:
- clearly named
- well described
- tested
- reusable
- explicit about inputs and outputs

### 3) Instructions
Instructions should be turned into a concrete routine.

Best practices:
- use existing SOPs, policies, or help docs when available
- convert dense documents into numbered steps
- map each step to a concrete action or output
- include branches for edge cases and missing information

## Orchestration decision guide

### Start here: single agent
Use a single agent unless you have strong evidence that more separation is needed.

A single agent usually works well when:
- tools are distinct
- instructions are still understandable
- one place should own the workflow loop

### Split into multiple agents when
- prompts accumulate too many branches
- tool choice remains poor even after improving descriptions
- specialized domains need clean separation
- you need either central delegation or explicit handoffs

## Multi-agent patterns

### Manager pattern
A central agent delegates to specialist agents as tools.

Use it when:
- one agent should remain the coordinator
- outputs from specialists need synthesis
- the user should experience one unified conversation

### Decentralized / handoff pattern
Agents transfer control to one another.

Use it when:
- triage/routing is the main problem
- specialists should fully take over their section of work
- a central synthesizer is unnecessary

## Guardrail checklist

Use layered defenses rather than relying on one mechanism.

Possible layers:
- relevance classifier
- safety / jailbreak / prompt-injection classifier
- PII filter
- moderation checks
- rules-based checks: regex, allow/deny lists, input length limits
- tool safeguards
- output validation

### Tool safeguard heuristic
Rate tools by risk:
- **Low** — read-only, reversible, low impact
- **Medium** — writes state but is recoverable
- **High** — irreversible, sensitive, financial, or external-impact actions

High-risk tools should usually require extra verification, approval, or escalation.

## Human intervention triggers

Add clear escalation rules for:
- repeated failed attempts
- uncertainty or low confidence
- risky actions
- permission failures
- broken dependencies or inconsistent tool results

## Eval and rollout checklist

Before optimizing cost, verify quality.

Recommended eval dimensions:
- representative happy-path tasks
- edge cases
- adversarial / unsafe inputs
- tool-routing correctness
- completion accuracy
- escalation correctness
- latency and token/cost after baseline quality is met

## Practical default output

When helping a user design an agent, aim to produce:

1. A recommendation on whether this should be an agent
2. Workflow boundary and completion criteria
3. Model strategy
4. Tool inventory with risk levels
5. Draft numbered instructions
6. Orchestration choice with rationale
7. Guardrails and human-in-the-loop plan
8. Eval and rollout plan
9. Optional implementation scaffold
