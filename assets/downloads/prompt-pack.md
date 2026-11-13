# Manikant Lab — prompt pack

Four prompts I actually use, plus two workflows. Copy them, change the brackets, keep the last line
of each one. That last line is the part people skip and the part that stops the model inventing
numbers.

---

## 1. The base template (any job)

```
You are a [role] with [X years] of experience in [field].

Situation: [what is actually going on, in plain sentences].
Constraint: [the real limit — budget, time, audience, tone, tools I have].
The problem: [one question, stated once].

Give me back:
- [format — a list of 5, a table, 200 words, a script]
- [what each item must contain]
- If you do not know something, say "unknown" and tell me what you would need to find out.
Do not invent numbers, names or sources.
```

---

## 2. Testing a script against a real audience

```
You are a social media growth specialist with more than five years of experience.

I will share my profile ID. Analyse every post and tell me which ones work and which do not,
look at my followers, and build a virtual simulation of my audience: what they care about,
what they scroll past, what makes them comment.

Then I will paste a script. Judge it as that audience would, not as a writer would.
Give me the top 10 problems with it, in order of how much they cost me.
If something is fine, say nothing about it.
```

---

## 3. The fetch, file, email loop

```
Do this every time I give you a topic:

1. Find the content — from the sources I named, not from your memory.
2. Write it into a Google Doc in my Drive, inside the folder "Inbox", dated in the title.
3. Add a three-line summary at the top: what it is, why it matters to me, what to do next.
4. Email me the link with the summary in the body.
5. If a source fails, say which one failed and give me what you have. Do not fill the gap.

Stop when the doc exists and the email is sent. Maximum 3 attempts per source.
```

---

## 4. Writer, cleaner, guard (a graph, not a loop)

```
Three separate steps. Do not merge them.

STEP 1 — WRITER
Write the [post / script / reply] for [audience], in the style of the examples I gave you.

STEP 2 — CLEANER (a fresh pass, not the same pass)
Read the output from step 1 and remove: invented facts, numbers without a source,
any text I did not ask for, and anything that reveals internal notes or credentials.

STEP 3 — GUARD (do not skip, do not negotiate)
Check the cleaned output against these rules. If it fails one, reject it and say which:
- every claim is traceable to something I supplied
- no score was assigned by the writer
- length and format match what I asked for

The final decision is mine. Do not mark the work as passed on my behalf.
```

---

## The rules behind all four

1. **Describe the job until guessing is impossible.** If you cannot, the model fills the gap.
2. **Hand over the material, not just the words.** Examples beat adjectives.
3. **Give it a loop with a stop condition** — written before the first run.
4. **Put the examiner outside the loop**, and keep the final call human.

Free to use. If one of these saves you an hour, tell me which one.
