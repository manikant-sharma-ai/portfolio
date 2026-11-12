# Manikant Sharma — portfolio site

A dark, single-page-at-a-time portfolio for **Manikant Sharma**, an AI generalist working in
prompt, context, loop and graph engineering, automation and agent building.

Live: deployed from this repository with Netlify (`publish = "."`).

## Pages

| File | What it is |
| --- | --- |
| `index.html` | Home: scroll hero (47-frame sequence), About, four disciplines, tools table, selected work, how I build, contact |
| `prompt-library.html` | What a prompt is, with a copy-ready template |
| `context-library.html` | What context is, with the audience-test prompt |
| `loop-library.html` | What a loop is, with the fetch-file-email loop |
| `graph-library.html` | Writer / cleaner / guard, and the documented examiner case |
| `work-employee-hub.html` | Project page — AI employees, 864 files |
| `work-truepick.html` | Project page — affiliate storefront + admin |
| `work-social-skill.html` | Project page — social media manager skill (MIT) |

## Stack

Plain HTML, CSS and vanilla JavaScript. No framework, no build step, no dependencies.
Fonts come from Google Fonts (Sora, Instrument Serif, JetBrains Mono).

```
index.html
*.html                      the eight pages
assets/site.css             all styling, one file
assets/site.js              mobile menu, scroll reveal, copy-to-clipboard
assets/frames/f01..f47.webp the hero frames, in order
netlify.toml                publish = "."
```

## How the hero works

The hero is a 47-frame clip scrubbed by scroll position, not a video. Each frame is a WebP image;
JavaScript swaps them as you scroll, easing toward the scroll position so a fast flick still plays
smoothly. The copy is real HTML on top of the frames — never burned into the images — so it stays
selectable, searchable and readable by a screen reader. On phones the layout becomes a column:
words first, then the clip in its own panel.

## Editing

- **Words:** everything is plain HTML. Search for the text and change it.
- **Colours:** the design tokens are the `:root` variables at the top of `assets/site.css`.
- **Tools table:** one `<tr>` per tool in `index.html`, under `#tools`.
- **Hero frames:** replace `assets/frames/f01..f47.webp` with the same number of frames, same names.

## Honesty rules this site follows

- Every number is a real count from a repository — no invented business metrics.
- No availability claims: the site says *building for myself*.
- No project appears here unless it is public and finished.

## Local preview

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8080
```
