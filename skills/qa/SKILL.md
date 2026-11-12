---
name: qa
description: >-
  Run the current ticket's AC in the browser with the repo Playwright setup,
  then report per AC.
---

# QA

Run the current ticket's acceptance criteria in the browser. Report each criterion. The user makes the pass or fail call.

## Workflow

1. Setup check. Look for a repo skill at .cursor/skills/*-playwright/SKILL.md or .agents/skills/*-playwright/SKILL.md. Read its Project line and confirm that path exists. If either is missing, stop, flag it, and use AskQuestion to offer two options: build the Playwright setup first, or stop. Do not write tests ad hoc. The check does not depend on language. On "build first", end with this fenced paste prompt:

```text
Build a self-contained Playwright setup in this repo for /qa: a <repo>-playwright skill at .cursor/skills/<repo>-playwright/SKILL.md, the Playwright project, a login seed, and selector rules (data-test-id, then role, then label, then text; locator assertions; no fixed waits; keep the assertion on a failure), and a helper that screenshots each finished action after its assertion passes. The skill starts with Project, Acceptance scratch, Report, and Evidence lines. Do not install third-party Playwright skill packs or the Playwright planner, generator, or healer.
```

2. Resolve the ticket in this order: the argument, the tcd-NNNN in the branch name, the epic INDEX ticket field, then ask.
3. Read the AC from the local ticket INDEX ac section. With no local ticket, read the tracker (read-only).
4. Map each AC bullet to one scenario with preconditions, steps, and expected outcome. Mark a bullet "not browser-testable" when it is BE-only, and point to the tests listed in the INDEX tests field. Show the table and get one confirm.
5. Run the repo skill's preflight. Write the scratch tests in the place the repo skill names, and follow its rules. Each test ends with the repo's evidence helper, called after the AC's assertion, whenever the finished state is visible on screen.
6. Run the tests, with the evidence folder pointed at <ticket dir>/acceptance/ in the way the repo skill's Evidence line says. Only fix locator mistakes, with at most two reruns per test. Keep the assertions. Do not skip, xfail, fixme, or add sleeps. If a precondition is cheap, create its data in the test. If not, mark the AC blocked and name the missing data.
7. Write ACCEPTANCE.md in the ticket dir from acceptance-template.md in this skill folder. The verdict per AC is pass, fail, blocked, or not browser-testable. A pass embeds its screenshot, or says "no screenshot" with the reason. A fail links its failure screenshot and trace, plus the error line. Also record the commit SHA, BASE_URL, and date. End with a PR evidence block: the passed ACs in order, with one line of AC text and one image line each, ready for the user to paste into the PR description.
8. The user makes the pass or fail call. Do not tick AC, change status, or write to the tracker unless the user asks.
9. Phase exit: on any fail, paste /multi-agent-implement KEY with "read ACCEPTANCE.md". When all pass, emit no paste.
