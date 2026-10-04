---
name: code-review
description: >-
  Two-axis review of the diff since a fixed point: Standards (applicable
  repository guidance plus a general engineering-quality baseline) and Spec
  (Jira Story / PRD). Use when the user says "/code-review", "review this
  branch", or after implement in a fresh session.
---

# Code Review

Review the three-dot diff from a fixed point to HEAD on **two axes**, in parallel so neither pollutes the other. Do not merge or rerank findings across axes.

Pin a **non-empty** diff first. If implement has not committed, commit or stash is the human's job — this skill will not invent a baseline.

## Axes

- **Standards:** how well the change is engineered.
  1. Discover and apply repository guidance relevant to the changed files:
     AGENTS.md, applicable .cursor/rules (including path-scoped rules),
     CONTRIBUTING.md, coding standards, and ADRs. Repository guidance overrides
     the general baseline. Reference the relevant rule when reporting a rule
     violation. Skip checks already enforced by formatters and linters.
  2. Apply general engineering judgement where repository guidance is silent:
     correctness and edge-case safety; clarity, cohesion, and maintainability;
     appropriate coupling and duplication; KISS and YAGNI; focused tests that
     provide meaningful confidence without redundant setup or assertions
     (overlapping twins of the same assertion; tests that never execute a
     changed production path);
     sound error handling and trust-boundary validation; compatibility with
     existing public contracts and conventions; and proportionality between
     implementation/test volume, risk, and changed behavior.
  3. Fowler code smells may be used as vocabulary for maintainability findings,
     not as an exhaustive checklist or proof that code is wrong.

- **Spec:** whether the change implements the originating ticket and PRD. The ticket is the markdown INDEX when the project uses one, or the Jira issue when that is the tracker.
  Report missing or partial requirements, scope creep, and incorrect behavior.
  Quote the relevant specification line. Spec does not grade test volume or
  style.

## Process

1. Fixed point: user-supplied SHA / branch / main. Default: merge-base with the default branch. Confirm git rev-parse and a non-empty three-dot diff.
2. Spec source: Story key in commits or the ticket implement used; else ask.
3. Spawn two subagents (Standards / Spec). Instruct each to return under 400 words.
   - Standards: provide the applicable repository rules and instruct it to use
     the Standards quality baseline above. Exclude product-requirement review.
   - Spec: provide the product contract and restrict it to the Spec axis above.
     Exclude code-quality review.
4. Report under the headings Standards and Spec. One-line count per axis. Do not pick a winner across axes.
5. Do not implement. Report findings only. Do not write product code, tests, or "while we're here" patches in this chat — even when the author agrees with a finding. Follow-up is a new /implement chat (or the human). Agreeing is not a request to patch here. If the user asks to fix a finding in this chat, refuse product code. Point at a new /implement chat. Ticket/context edits are OK when asked.

Format explanation, recommendation, and the chat report:
Markdown code spans for identifiers, paths, routes, flags, and symbols;
Markdown bold only for a true stress; blank lines start paragraphs. No
raw HTML. Title stays a short plain sentence.

A change can pass Standards and fail Spec (wrong thing, clean code) or the reverse. That split is the point.

## Nested under BUILD-PROGRAM

When the parent is a long-running coordinator:

- The coordinator is the review lead. It launches Standards and Spec
  reviewers directly. Do not spawn a further review-lead wrapper.
- If you are one axis: review only that axis, return under 400 words, do not
  spawn further agents.
- Return findings only. Do not patch product code or tests.
- Do not tell the user to open a new implement chat. The coordinator decides
  remediation.
- Do not publish or attach the result anywhere unless the frozen run
  manifest names that exact write.
