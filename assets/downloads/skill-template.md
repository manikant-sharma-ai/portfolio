# SKILL.md — a blank template

This is a scaffold, not a finished skill. Copy it, fill the brackets, delete what you do not need.
A skill is a job description that an AI agent can actually follow: what it is for, what it needs,
what it must do, and what it must never do.

---

```markdown
# [Skill name]

## What this is for
[One paragraph. The real job, in plain words. If you cannot write this paragraph, the skill is not
ready.]

## When to use it
- [Trigger 1 — the thing a user would say]
- [Trigger 2]
- Do not use it when: [the case where another tool is better]

## What it needs before it starts
- Connectors: [what must be authorised, by name]
- Inputs from the user: [files, links, examples]
- If a connector is missing: [say so by name, and offer a manual fallback. Never guess the data.]

## The workflow
1. [Step one — what it checks first]
2. [Step two]
3. [Step three]
4. [Stop. State the condition that ends the work.]

## Standards
- [What good output looks like — length, format, tone]
- [What every answer must contain]

## Guardrails — never do this
- Never invent numbers, names, sources or dates.
- Never claim an action was taken when it was not.
- Never publish, send or delete anything without explicit approval.
- Never store credentials.

## Notes it keeps
- `notes/learnings.md` — what worked, what failed, what to do differently next time.
- `notes/decisions.md` — dated decisions and the reason.

## How to check it worked
- [The test you would run before trusting it]
```

---

## Why the sections are in this order

Trigger first, because a skill that does not know when it should fire never fires.
Inputs second, because most agent failures are missing-data failures wearing a confident voice.
Guardrails third-to-last, because they are the only part that protects you when everything else is
right but the model is in a helpful mood.

MIT licensed template — use it, change it, ship it.
