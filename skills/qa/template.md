# QA Issue Template

Copy the block below into the project's tracker (Linear / Jira / GitHub Issues) when filing a durable issue from a QA session. Use the project's domain language from `CONTEXT.md`.

---

```markdown
**Title:** <user-observable, present-tense — readable on its own>

**What's happening:**
<one paragraph in domain language — describe what the user sees, not what you guess is broken>

**What should happen:**
<one paragraph — the expected behavior. Reference PRD / spec section if relevant.>

**Repro:**
1. <step>
2. <step>
3. <step>

**Evidence:**
- <screenshot / log line / file:line>
- <traceback excerpt if any>

**Suspected area:** <path/to/file.py:NNN> *(optional — only if confident; don't guess)*

**Failing test sketch:**
```
<one-liner: what the test would assert, using the public interface>
```

**Domain terms used:**
- <term from CONTEXT.md>
- <term from CONTEXT.md>

**Severity:** blocker / high / medium / low
```

---

## Field guidance

**Title.** Must be understandable without reading the body. "Pipeline page" is bad. "Pipeline page crashes when revision has no location" is good.

**What's happening vs What should happen.** Two paragraphs. Resist the urge to merge them — the split forces clarity on the gap.

**Repro.** Exact, copy-pasteable steps. If you can't repro, the issue isn't durable — go back to QA and clarify.

**Evidence.** A repro without evidence is hearsay. A log line or screenshot anchors it in reality.

**Suspected area.** Optional and *only* if you traced it. Bad suspicions waste the next person's time more than no suspicion at all.

**Failing test sketch.** This is the bridge to `tdd`. Even a one-line pseudo-assertion makes the next step obvious: *"the test that would catch this"* → write it → red → fix → green.

**Domain terms.** If a term isn't in `CONTEXT.md`, either add it (with a one-line definition) or use a term that is. Drifting vocabulary is how issues stop being durable.

**Severity heuristic.**
- **blocker** — production down, data loss, or fully blocks a critical user journey.
- **high** — degrades a critical journey but workaround exists; or a non-critical journey is fully broken.
- **medium** — visible bug, workaround easy, no journey blocked.
- **low** — cosmetic, edge case, or quality-of-life.
