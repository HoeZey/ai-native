---
name: code-review
description: >-
  Two-axis review of the diff since a fixed point: Standards (repo conventions
  plus a Fowler-smell baseline) and Spec (does it match the Jira Story / PRD?).
  Use when the user says "/code-review", "review this branch", or after
  implement in a fresh session.
---

# Code Review

Review `git diff <fixed-point>...HEAD` on **two axes**, in parallel so neither pollutes the other. Do not merge or rerank findings across axes.

Pin a **non-empty** diff first. If `implement` has not committed, commit or stash is the human's job — this skill will not invent a baseline.

## Axes

- **Standards:** repo coding docs (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, ADRs) plus judgement-call Fowler smells (mysterious name, duplication, feature envy, data clumps, primitive obsession, repeated switches, shotgun surgery, divergent change, speculative generality, message chains, middle man). Repo docs override the baseline. Skip what tooling already enforces.
- **Spec:** the originating Jira Story + PRD section. Missing / partial requirements, scope creep, wrong implementation. Quote the spec line.

## Process

1. Fixed point: user-supplied SHA / branch / `main`. Default: merge-base with the default branch. Confirm `git rev-parse` and a non-empty three-dot diff.
2. Spec source: Story key in commits or the ticket `implement` used; else ask.
3. Spawn two sub-agents (Standards / Spec), each under 400 words.
4. Report under `## Standards` and `## Spec`. One-line count per axis. Do not pick a winner across axes.
5. Do not implement. Report findings only. Do not write product code, tests, or "while we're here" patches in this chat — even when the author agrees with a finding. Follow-up is a new `/implement` chat (or the human). Agreeing is not a request to patch here.

A change can pass Standards and fail Spec (wrong thing, clean code) or the reverse. That split is the point.
