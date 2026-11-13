---
name: portfolio-updater
description: Keeps Manikant Lab's portfolio site (github.com/manikant-sharma-ai/portfolio) current. Use this whenever something new happens — a project ships, a skill is published, a tool is added, a new thing is learned, a number changes, or the owner asks to "update my portfolio". It knows the exact file map, the design tokens, the counting rules, the honesty rules and the commit order, so a change lands consistently instead of quietly breaking the site.
---

# Portfolio updater

The owner is **Manikant Sharma**; the brand on the site is **Manikant Lab**. He builds with AI
rather than writing code by hand, so this skill exists to make updates safe and repeatable without
him having to remember the structure.

## What this is for

Any change to the portfolio: a new project, a new downloadable skill, a new journey entry, a new
tool in the tools table, corrected numbers, copy edits, a new photo. One skill, one workflow, so the
site stays consistent as it grows.

## When to use it

- "I built something new — add it to my portfolio."
- "Add this skill so people can download it."
- "Update the journey / the numbers / the tools table."
- "The site needs this changed" — any content request.
- Do **not** use it for: changing hosting, renaming the repository, or anything involving the
  `CNAME` file. Those need the owner's explicit decision first (see Guardrails).

## What it needs before it starts

- **Access:** the GitHub integration, with push rights to `manikant-sharma-ai/portfolio`.
- **From the owner:** the facts of the change. Never invent a number, a date, a metric or a quote.
  If he has not given a figure, the answer is "I don't have that number yet", not a guess.
- **If a screenshot or photo is needed:** ask him. He sends them through Google Drive or attaches
  them in chat. Do not generate a picture of a person and present it as him.

## The file map

```
portfolio/
  index.html                  home: hero + portrait band + 4 discipline cards
                              + 3 project cards + subscribe + contact strip
  about.html                  About text, fact table, portrait, Journey timeline
  libraries.html              the four discipline cards on their own page
  tools.html                  the nine-row tools table
  work.html                   the three project cards on their own page
  skills.html                 downloadable skills, prompt pack, SKILL.md template
  build.html                  the five gates ("How I build")
  contact.html                contact links + subscribe
  prompt-library.html         discipline page: prompt
  context-library.html        discipline page: context
  loop-library.html           discipline page: loop
  graph-library.html          discipline page: graph
  work-employee-hub.html      project page
  work-truepick.html          project page
  work-social-skill.html      project page
  assets/site.css             all styling, design tokens in :root
  assets/site.js              mobile menu, scroll reveal, copy buttons, text-to-speech
  assets/frames/f01..f47.webp the hero frames, in order
  assets/img/                 portrait.webp, logo-mark.webp, logo-full.webp, favicon.png
  assets/downloads/           prompt-pack.md, skill-template.md
  netlify.toml                publish = "."
  README.md                   the repo readme
```

Two files that exist but are **not** used by the pages: `assets/img/about.webp` (an older square
portrait, superseded by `portrait.webp`). Leave it or ask before deleting.

## The design system (do not invent new values)

```
--bg #04060b   --surface rgba(10,15,24,.72)   --line rgba(255,255,255,.08)
--text #eef3f9  --dim #93a3b8  --dim2 #5f7086  --cyan #0ea5e9  --blue #2a7fdc
--sans Sora    --serif "Instrument Serif" (italic, cyan, for the highlighted word in a heading)
--mono "JetBrains Mono" (eyebrows, labels, chips, numbers)
--max 1200px   --r 14px
```

House patterns: `.container`, `.section`, `.section__head`, `.num` (the `01 — About` eyebrow),
`.card`, `.wcard`, `.chips`/`.chip`, `.stats`, `.gate`, `.link`, `.btn`/`.btn--ghost`,
`.prompt` + `.prompt__why`, `.callout`, `.pagehead` + `.crumb`, `.note`.

Every inner page starts with `.pagehead`: a back-to-home crumb, the section number, an `<h1>` with
one `<em>` word, and one line of intro. Never repeat that heading inside the section below it.

## The honesty rules — these are not negotiable

1. **Every number is a real count, files only.** Count blobs in the repo tree, never folders and
   never tree entries. A folder counted as a file is how "864 files" happened when the truth was
   716. Recount at the moment of writing, and write the number you just counted.
2. **No business metrics he cannot defend.** No "hours saved", no "% faster", no invented users or
   revenue, unless he supplies the figure and says where it came from.
3. **No availability claims.** The site says *building for myself*. Never add "open to work",
   "available for freelance", or a hiring badge unless he asks for it in writing.
4. **No private work.** The mail client lives in a private repository and must never appear on the
   site. Before adding any project, confirm the repository is public.
5. **Nothing finished-looking that is not finished.** Feedfy appears as "designed, not built yet"
   with no date. Keep that shape until it ships.
6. **No text burned into images.** All copy is real HTML: selectable, searchable, screen-readable.
7. **Brand vs person.** Header and footer carry **Manikant Lab**. The person **Manikant Sharma**
   appears in About, the portrait caption, and the footer copyright line.

## Workflows

### A. Add a new project

1. Confirm the repository is public and note its owner/name.
2. Recount, files only: total files, HTML pages, markdown files, and anything else you plan to show.
3. Copy an existing project page as the template — `work-truepick.html` is the plainest one. Change:
   the `<title>` (no `<em>` tags inside a title — plain text, under 60 characters), the `og:title`,
   the `og:description`, the crumb, the `<h1>`, the intro, the chips, the `.stats` row, the body
   sections, and the "Source" callout with the real repo URL.
4. Add the card in **two** places: the `.work` grid in `index.html`, and the same grid in
   `work.html`. Number the kicker (`01 ·`, `02 ·`) so the order still reads.
5. Add a Journey entry in `about.html` with the real date and a "Built with" chip row.
6. If it can be downloaded, add a card to `skills.html` with a `Download .zip` link pointing at
   `https://github.com/<owner>/<repo>/archive/refs/heads/main.zip`.
7. Update the counts on every page that mentions them (grep for the old number).

### B. Add a journey entry

In `about.html`, inside `.journey`, add a `.jrow` block: `.jdate` (a real date), `.jbody` with an
`<h3>`, one paragraph, and a `.chips` row starting with `<span class="built">Built with</span>`.
Newest goes at the bottom; the last row stays `jrow--next` for what is planned.

### C. Add a downloadable skill

1. Put the file in `assets/downloads/` if it is a small text file, or link the GitHub archive if it
   is a whole repository.
2. Add a `.wcard` to `skills.html`: kicker, license chip, `<h3>`, two lines of what it does, chips,
   then two buttons — `Download` and `View on GitHub` (or `See them explained`).
3. Say plainly whether it is a finished skill or a template. A scaffold labelled as a skill is a
   lie with good manners.

### D. Change the tools table

One `<tr>` per tool in `tools.html`: name, what he uses it for, `class="yes"`/`class="no"` for
connector support, and what he uses instead when it cannot reach the repo. Keep the note under the
table honest: free tiers change, so the table says what he uses today.

### E. Change the hero

The hero is 47 WebP frames at 1600 px wide, `assets/frames/f01.webp … f47.webp`, swapped by scroll
position. If he sends new frames: keep the count and the names, convert to WebP (quality ~84,
background `#04060b` flattened), and keep every frame free of text. If the count changes, update the
`/ 47` counter in `index.html` and the `f01..f47` reference in the README.

## Commit order (this is what keeps the site unbroken)

1. **Assets first** — images, downloads, `site.css`, `site.js`.
2. **Inner pages** — everything except `index.html`.
3. **`index.html` last.**

The page must never point at a file that does not exist yet. One commit per group, with a message
that says what changed and why, in plain words.

## How to check it worked

- Open the page in a browser engine at **390×844, 768×1024, 1024×768, 1600×900**.
- Click every link on the pages you touched; confirm none 404.
- Check that the reveal animation still shows content (content must be visible without JavaScript —
  `.js .rv` is the only thing that hides it).
- Recount every number you wrote. Read them back against the tree.
- Report to the owner what changed, in his language, and tell him plainly what you could **not**
  verify. Chromium is the only engine available in the sandbox — Firefox and Safari are his to test.

## Guardrails

- **Never delete a file you did not create** without asking. That includes `CNAME`, `netlify.toml`
  and anything in `assets/`.
- **Never touch `CNAME`.** It currently points at a custom domain that does not resolve. Changing or
  deleting it moves the live site. Only the owner decides that.
- **Never rename the repository** — the Pages URL is built from the name.
- **Never force-push, never rewrite history, never delete a branch** he did not ask about.
- **Never expose credentials**; no API keys in files, no tokens in commits.
- **Never claim a browser test you did not run.**
- If a change needs a fact you do not have, stop and ask. A missing number is recoverable; an
  invented one is not.

## Notes to keep

- `notes/changelog.md` — dated, one line per change, so he can see the history without reading git.
- `notes/open-questions.md` — what is waiting on him (currently: the Mailchimp form URL, and how
  much of his age/audience to make public). No LinkedIn: the owner is 14 and LinkedIn does not
  allow accounts at that age. Do not add a LinkedIn link, a CV, a phone number or a notice-period
  line, and do not write the copy for recruiters — it is not a job-search site.
- When a change lands, tell him in Hindi what you did and why, and update the Hindi notes document
  he reads.

## The owner is 14 — read this before writing anything

- **No LinkedIn, no CV, no phone number, no "open to roles".** He cannot hold those accounts and the
  site is not a job-search asset.
- **Do not publish his age** unless he asks in writing, and if he does, say plainly that it is public
  for anyone to see and he may want a parent's view first.
- **Keep the public footprint small.** Email, GitHub and X are enough. If he asks, suggest dropping
  Facebook and Reddit from the site: a public minor with five contact channels is five doors.
- **No payments, no domain purchases, no hosting plans in his name.** Those need an adult.
- **Encourage the work, not the persona.** The honest line is that he builds real things and checks
  them; it does not need to be dressed as a career.

## House style for the copy

Short sentences. No jargon where a plain word exists. One idea per card. Never write "passionate",
"leverage", "cutting-edge" or "unlock". If a sentence could appear on any other portfolio, rewrite
it until it could only be his.
