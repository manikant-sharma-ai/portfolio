# Context filters

What to strip, what to reinterpret, and what does not exist. One dated block per prompt the owner
shares. Newest last. Read this before acting on any context prompt.

## 2026-11-15 — job-search context prompt (first entry)

### Personal data stripped
- Email address, account IDs and any login detail → `[owner email]` / `[account]`. Never written into
  a skill, a note or a draft.
- "matricul account" read as **metrics accounts** — Google Search Console and Google Analytics. No
  credential or account name is stored anywhere.
- Age, school and birthday stay off every public artefact (portfolio, LinkedIn post, application).

### Instructions reinterpreted, not copied
- "I cannot coder" → written as **builds products with AI, does not write code by hand**. True,
  specific, and it is the selling point rather than an apology.
- "you cannot use this account memory; you can work now" → each run starts from the files in this
  repo (`notes/`, the site's own pages, the public repos), never from an earlier chat.
- "resilience to AI changes" → turned into a test: if one prompt does the core task, the role is not
  resilient. Otherwise the phrase means nothing and the shortlist fills with noise.
- "top ten roles" → ten **verified, openable** roles, or fewer with the reason stated. A number is not
  a target to hit by inventing rows.

### Contradiction resolved
- The prompt both allowed and forbade browser use. Resolved to: **no browser automation on job
  boards** (terms of service, unverifiable listings); public pages and connectors only.

### Connectors that do not exist here
- **Indeed, Apna, Naukri, make.com** — no connector in this account. Discovery for those boards goes
  through web search of their public pages, and an unopenable listing is dropped, not guessed at.
- **LinkedIn** — connected, but only for his own profile and for posting; there is no job-search
  endpoint. LinkedIn Jobs can only be read as a public web page.

### Standing filters for every future prompt
1. Anything that would cost money becomes a question for him and a parent, never an action.
2. Anything personal (email, phone, IDs, tokens, other people's details) becomes `[brackets]`.
3. Any claimed capability is checked against the connector list before it is written into a skill.
4. Any instruction that contradicts another is resolved once, here, with the reason.
5. Any prompt that asks for a number of results gets a rule about what counts as a real result.

## 2026-11-15 — second entry: the same prompt, corrected by the owner

He clarified where the prompt came from and why it was worded that way. Everything below overrides
anything above that it contradicts.

### It is a ChatGPT prompt, not a workspace instruction
- The job-board, Metricool and social connectors exist in ChatGPT. Here they do not. So the prompt is
  kept twice: `notes/prompts/chatgpt-job-search-prompt.md` for pasting into ChatGPT, and
  `skill/career-agent/SKILL.md` for the run in this workspace. **Change one, change both.**
- A pasted prompt must never assume a connector is present. The connector list is written as optional,
  with a one-line "not connected, carrying on" fallback that degrades to web search.

### The browser clause is deleted, not softened
- His reason: browser use is for **applying**, and this is only searching; and it was burning connector
  credits. That is a cost decision, and a good one.
- Also: not every account will have that connector, so a rule about it does not belong in a portable
  prompt. The rule is now "search here, do not apply, do not spend credits on repeated calls" — with
  no lecture about job-board terms attached.

### Metricool is a signal, not a stray name
- He is starting **content creation**, which is why it appeared. Content is therefore a workstream in
  the career agent, not a footnote: public posts are proof of work for job applications.
- No Metricool connector exists in this account, so this stays a note until one is connected. Do not
  invent posting data.

### What he would have added if he had them
- Search Console and Analytics access, so the agent knows the site more deeply. Those **are** connected
  here, which means this workspace version of the agent can go deeper than the ChatGPT one. Say that
  plainly rather than pretending the two are identical.

### New standing filter
6. When a prompt arrives from another tool, ask which account it was written for before judging what
   it left out — a missing connector there may be a deliberate cost choice, not an oversight.
7. `notes/` lives inside the public site repo. Every file here is readable by anyone, so personal
   data never lands in it — only rules, logs and prompts.
