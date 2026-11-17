#!/usr/bin/env python3
"""Rebuild tools.html from the free-ai-models sheet + published benchmark numbers."""
import html, io, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools.html")

# ---------------------------------------------------------------- chart engine
def chart(rows, vmax, fmt="{:.1f}", label_w=216, pad_r=62, row_h=30, grad="cg1",
          highlight=0, aria=""):
    """rows: list of (label, value). Horizontal bars, one scale, one source."""
    W = 760
    px = label_w + 12
    pw = W - px - pad_r
    H = 16 + row_h * len(rows) + 26
    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(aria)}">']
    s.append(f'<defs><linearGradient id="{grad}" x1="0" x2="1">'
             f'<stop offset="0" stop-color="#0ea5e9"/><stop offset="1" stop-color="#2a7fdc"/>'
             f'</linearGradient></defs>')
    for i in range(5):
        x = px + pw * i / 4
        s.append(f'<line class="cg" x1="{x:.1f}" y1="10" x2="{x:.1f}" y2="{H-22:.1f}"/>')
        s.append(f'<text class="cax" x="{x:.1f}" y="{H-8}" text-anchor="middle">'
                 f'{vmax*i/4:g}</text>')
    for i, (label, val) in enumerate(rows):
        y = 16 + i * row_h
        w = max(2.0, pw * val / vmax)
        cls = "cb hi" if i == highlight else "cb"
        s.append(f'<text class="cl" x="0" y="{y+12.5}">{html.escape(label)}</text>')
        s.append(f'<rect class="{cls}" x="{px}" y="{y}" width="{w:.1f}" height="17" rx="3" '
                 f'fill="url(#{grad})"/>')
        s.append(f'<text class="cv" x="{px+w+7:.1f}" y="{y+12.5}">{fmt.format(val)}</text>')
    s.append('</svg>')
    return "".join(s)


# ---------------------------------------------------------------- data
# Artificial Analysis Intelligence Index v5.0.1, open weights, read 7 Nov 2026.
AA = [
    ("Kimi K3.1 Pro", 46.5), ("DeepSeek V4.1 Flash", 32.6), ("GLM-5.3", 31.7),
    ("MiMo-V2.6-Pro", 29.9), ("Ling 3.1 Flash", 29.6), ("MiniMax M3.1 Flash", 29.1),
    ("Step 5 Preview", 28.5), ("GLM-5.3 Flash", 27.8), ("MiMo-V2.6 Flash", 26.7),
    ("Mistral Large 4", 26.1), ("Muse Spark Open", 24.9), ("DeepSeek V4 Pro", 23.1),
    ("Nanbeige4.3-33B", 20.4), ("Qwen3.8 27B", 20.1),
]
# Same source, same run: USD to complete the nine-eval index once.
COST = [
    ("Kimi K3.1 Pro", 3.68), ("DeepSeek V4.1 Flash", 0.60), ("GLM-5.3", 5.01),
    ("MiMo-V2.6-Pro", 0.26), ("Ling 3.1 Flash", 3.19), ("MiniMax M3.1 Flash", 0.49),
    ("Step 5 Preview", 2.35), ("GLM-5.3 Flash", 0.58), ("MiMo-V2.6 Flash", 0.13),
    ("Mistral Large 4", 2.06), ("Muse Spark Open", 2.02), ("DeepSeek V4 Pro", 1.77),
    ("Qwen3.8 27B", 3.53),
]
SPEED = [
    ("Nemotron 3.5 Super VL", 424), ("Nemotron 3.5 Lightning", 270),
    ("DeepSeek V4.1 Flash", 174), ("Nemotron 3 Ultra", 161), ("GLM-5.3", 88),
    ("DeepSeek V4 Pro", 73), ("GLM-5.3 Flash", 64), ("MiMo-V2.6-Pro", 53),
    ("Qwen3.8 27B", 38), ("Kimi K3.1 Pro", 30),
]
GPQA = [
    ("Kimi K3.1 Pro", 94.2), ("Qwen3.8 Max", 92.6), ("DeepSeek V4.1 Flash", 92.2),
    ("GLM-5.3", 91.7), ("Qwen3.8-Flash-Next", 91.7), ("DeepSeek V4-Flash", 89.9),
    ("Qwen3.8-27B", 89.2), ("Muse Spark Open", 89.0), ("GLM-5.3 Flash", 86.4),
    ("gpt-oss-120b", 80.1), ("gpt-oss-20b", 71.5),
]

# name, maker, params, ctx, licence, runs-on, best-for, benchmark, price, link
OPEN = [
    ("Kimi K3.1 Pro", "Moonshot AI", "2.8T / 104B active", "1M",
     "Kimi K3.1-Pro licence", "1.56 TB of weights &mdash; practical only through an API",
     "The hardest reasoning, long agent runs, refactoring a big repo, research",
     "AA Index 46.5, best open model (7 Nov 2026); GPQA Diamond 94.2; HLE 52.5; DeepSWE v1.1 75.5; Terminal-Bench 4.0 65.7",
     "$2 / $10", "https://huggingface.co/moonshotai/Kimi-K3.1-Pro"),
    ("DeepSeek V4.1 Flash", "DeepSeek", "552B backbone / 16B active", "1M",
     "MIT", "Server class, ~763B total",
     "Agentic coding inside a repo, cheap high volume, text plus image",
     "GPQA 90.9; Terminal-Bench 2.1 90.6 (DSH Minimal); DeepSWE v1.1 74.2; Codeforces 3471",
     "$0.30 / $1.20", "https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash"),
    ("Qwen3.8 Max", "Alibaba Qwen", "2.4T / 95B active", "1M",
     "Qwen3.8-Max licence", "Server class",
     "Maths and exam-style reasoning, multilingual work",
     "GPQA 92.6; AIME 2025 99.4; SWE-bench Verified 85.6; LiveCodeBench 87.8; MMLU-Pro 88.6; LMArena 1484",
     "&mdash;", "https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B"),
    ("GLM-5.3", "Z.ai", "753B / 40B active", "1M",
     "GLM-5.3 licence", "Server class",
     "Long-horizon coding, tool use, agent loops",
     "Terminal-Bench 2.1 88.2; Terminal-Bench 3.0 28.3 (open SOTA); DeepSWE 66.9; Toolathlon 73.0; CyberGym 84.5",
     "$1.40 / $4.40", "https://huggingface.co/zai-org/GLM-5.3"),
    ("GLM-5.3 Flash", "Z.ai", "321B / 18B active", "1M",
     "MIT", "Server class, the cheapest of the serious ones",
     "Everyday work, a cheap near-frontier daily driver",
     "GPQA 86.4; ahead of GLM-5.2 on every benchmark at about a tenth of the price; multimodal",
     "$0.15 / $0.50", "https://huggingface.co/zai-org/GLM-5.3-Flash"),
    ("Muse Spark Open", "Meta", "816B / 42B active", "&mdash;",
     "Check the model card", "Server class",
     "Safety and refusal behaviour, anywhere a wrong answer is expensive",
     "GPQA 89.0; Terminal-Bench 2.1 76.4 (Terminus 2); StrongREJECT v2 0.5 &mdash; lower is better",
     "&mdash;", "https://huggingface.co/models?search=Muse%20Spark%20Open"),
    ("Mistral Large 4", "Mistral AI", "&mdash;", "&mdash;",
     "Check the card", "Server class",
     "Cost efficiency &mdash; getting a job done in fewer tokens",
     "AA Index 26.1; DeepSWE ~62; AA Coding Agent Index 48% on 47% fewer tokens per task (Mistral's claim)",
     "$1.40 / $4.40", "https://huggingface.co/models?search=Mistral%20Large%204"),
    ("Tencent Hy4", "Tencent", "&mdash;", "1M",
     "Check the card", "Server class",
     "Cheap long context",
     "AA Index 34.6 as printed on the LMSA board (second open model) &mdash; a different index from the one charted above, so do not read the two together",
     "~$0.42 / $1.25", "https://huggingface.co/models?search=Hy4"),
    ("MiMo-V2.6-Pro", "Xiaomi", "1.02T / 42B active", "1M",
     "MIT", "Server class",
     "New and lightly tested &mdash; one to experiment with",
     "AA Index 29.9; $0.26 per index task, the best score-per-dollar in the top five",
     "$0.435 / $0.87", "https://huggingface.co/models?search=MiMo-V2.6"),
    ("MiniMax M3.1 Flash", "MiniMax", "428B / 23B active", "1M",
     "MiniMax community licence", "Server class",
     "Bulk, high-volume cheap work",
     "AA Index 29.1; Code Arena 1584",
     "$0.15 / $0.60", "https://huggingface.co/models?search=MiniMax%20M3.1"),
    ("gpt-oss-120b", "OpenAI", "117B / 5.1B active", "128K",
     "Apache 2.0", "One 80 GB GPU",
     "Local agentic coding on your own machine",
     "GPQA 80.1 without tools; SWE-bench Verified 62.4; AIME 2025 97.9 with tools; MMLU 90.0 (arXiv 2508.10925)",
     "&mdash;", "https://huggingface.co/openai/gpt-oss-120b"),
    ("gpt-oss-20b", "OpenAI", "21B / 3.6B active", "128K",
     "Apache 2.0", "A 16 GB laptop",
     "An assistant that runs on a laptop, offline",
     "GPQA 71.5; SWE-bench Verified 60.7; AIME 2025 98.7 with tools; MMLU 85.3",
     "&mdash;", "https://huggingface.co/openai/gpt-oss-20b"),
    ("gemma-4-31B-it", "Google DeepMind", "31B", "256K",
     "Apache 2.0", "A high-memory Mac",
     "The best small all-rounder; image and video input",
     "OpenWeightsBench 99.3 overall, 94.7 on hard questions &mdash; 270 items, code-checked, 16 Nov 2026",
     "&mdash;", "https://huggingface.co/models?search=gemma-4-31B-it"),
    ("Qwen3.8-27B", "Alibaba Qwen", "28B", "&mdash;",
     "Apache 2.0", "32 GB Mac, or one GPU at 4-bit",
     "A local coding assistant that runs all day",
     "GPQA 89.2; SWE-bench Pro 61.7; LiveCodeBench v6 90.3; AA Index 20.1",
     "&mdash;", "https://huggingface.co/Qwen/Qwen3.8-27B"),
    ("Qwen3.8-Flash-Next", "Alibaba Qwen", "180B", "&mdash;",
     "Qwen licence", "Server class",
     "Tool calling and function use, agent workflows",
     "GPQA 91.7; SWE-bench Pro 62.5; DeepSWE 58.7; LiveCodeBench v6 91.9; Toolathlon 73.5",
     "&mdash;", "https://huggingface.co/Qwen/Qwen3.8-Flash-Next"),
    ("Nanbeige4.3-33B", "Nanbeige", "33B", "&mdash;",
     "Apache 2.0", "A 128 GB machine at 4-bit",
     "Local work when the GPU is small",
     "AA Index 20.4 &mdash; level with Qwen3.8-27B at 33B",
     "&mdash;", "https://huggingface.co/models?search=Nanbeige4.3-33B"),
    ("DeepSeek V4-Flash", "DeepSeek", "284B / 13B active", "128K",
     "MIT", "Server class",
     "The older cheap DeepSeek, for a side-by-side with V4.1",
     "GPQA 89.9; Terminal-Bench 2.1 82.7; DeepSWE 54.4",
     "&mdash;", "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash"),
    ("Devstral-2-123B", "Mistral AI", "123B", "&mdash;",
     "Modified MIT", "~65 GB of memory",
     "A local coding agent over your own codebase",
     "Coding-focused; the card carries its own set of numbers",
     "&mdash;", "https://huggingface.co/models?search=Devstral-2-123B"),
]

FREE = [
    ("Nemotron 3 Ultra", "NVIDIA", "550B / 55B active", "1M",
     "Prototyping, a free taste of a big reasoning model",
     "3, 6", "The <code>:free</code> suffix is part of the id. 20 requests a minute, 50 a day; put $10 of credit on the account once and it becomes 1,000 a day."),
    ("Nemotron 3.5 Super VL", "NVIDIA", "120B / 12B active", "1M",
     "Reading screenshots, pulling data out of documents",
     "8, 9", "Text, image, document, GUI screenshot and video in. Rate-limited on the free variant."),
    ("ERNIE-5.5-Flash-Preview", "Baidu", "&mdash;", "&mdash;",
     "General work, multilingual",
     "3, 9", "A preview &mdash; it can disappear without notice."),
    ("Dots3-Note Preview", "Dots Studio", "280B / 16B active", "512K",
     "Understanding notes and long documents",
     "3, 10", "Free only until 31 December 2026."),
    ("Gemma 4 26B A4B / 31B", "Google", "26B / 31B", "256K",
     "Everyday small jobs, vision",
     "9, 3", "Image and video input, small and fast. Rate-limited on the free variant."),
    ("Nemotron 3.5 Lightning", "NVIDIA", "30B / 3B active", "1M",
     "Bulk work where speed matters more than accuracy",
     "6, 12", "Very fast, very light, and less accurate &mdash; cheap bulk only."),
    ("openrouter/free", "OpenRouter", "&mdash;", "&mdash;",
     "When you cannot be bothered to pick a model",
     "&mdash;", "Put this in the model field and it picks any free model. The trap: if the account balance is negative, even free models return a 402."),
]

TESTS = [
    ("Fit", "Weight size in GB, quantisation, KV cache per token. Try it on the machine you actually want to run it on.",
     "GB, quant, time to first token, tok/s"),
    ("Licence", "Read the LICENSE file on the model card. MIT and Apache ship. The maker's own licence gets read first.",
     "Licence name and whether commercial use is allowed"),
    ("Repeatability", "Run the same prompt three times at default temperature.",
     "Do the three answers agree? Yes or no"),
    ("Your own benchmark", "Ten questions whose answers you already know &mdash; your repo's CSS bug, the file count, the Netlify config.",
     "Pass@1, out of ten. This is the only number that is yours"),
    ("Contamination", "Ask something made today, that cannot be in any training set.",
     "Right or wrong, and whether it hedged or went straight at it"),
    ("Tokens per task", "Finish one real job, then count total input plus output tokens.",
     "Tokens per task, and what those tokens cost"),
    ("Tool calling", "A five-step loop on a real repo: read, edit, run tests, fix, report.",
     "How many steps completed, and where the thread was lost"),
    ("Long context", "Hide a fact at 100K, then at 800K. Ask for it back.",
     "How deep it still answers correctly"),
    ("Hindi and Hinglish", "The same instruction in Hindi, in Hinglish, and in English.",
     "Does it stay in the language? Does the tone survive?"),
    ("Honesty", "A question it cannot possibly know &mdash; a private file, a number that does not exist.",
     "&ldquo;I don't know&rdquo;, or a confident invention"),
    ("Refusal", "One prompt that should be refused, one harmless prompt that should not be.",
     "Both handled correctly?"),
    ("Speed", "Time to first token, plus output tok/s, on the tier you will use every day.",
     "Seconds (TTFT) and tok/s"),
]

PLACES = [
    ("Hugging Face &mdash; trending", "The newest open-weight models, with downloads and likes",
     "https://huggingface.co/models?sort=trending", "What just landed &mdash; the first stop"),
    ("OpenWeightsBench", "228 models, 270 questions, 13 categories, all on the same battery and code-checked. Has a hardware picker",
     "https://openweightsbench.com/", "Choosing a model that has to run on your machine"),
    ("Artificial Analysis", "The AA Intelligence Index, run by them, not the vendors. The open-weights page is separate",
     "https://artificialanalysis.ai/", "Comparing real capability"),
    ("LMArena", "Human votes, text and code arena",
     "https://arena.ai/", "Which model people actually prefer &mdash; use the code arena for coding"),
    ("LMSA leaderboard", "AA plus arena plus price plus context, in one table",
     "https://lmsa.app/leaderboard/", "Building a shortlist at a glance"),
    ("ModelCap &mdash; open weights", "223 open models with licence and price",
     "https://modelcap.ai/rankings/open-weights", "Filtering by what the licence allows"),
    ("OpenRouter &mdash; free models", "Everything going for $0, ranked by usage",
     "https://openrouter.ai/collections/free-models", "Trying a model with no money and no GPU"),
    ("Ollama library", "One command per model: <code>ollama run &lt;model&gt;</code>",
     "https://ollama.com/library", "The easiest way to run something locally"),
    ("LM Studio", "A GUI for local models on Mac (MLX) and Windows",
     "https://lmstudio.ai/", "When you would rather not touch a terminal"),
    ("AIMap &mdash; free open-weight", "85 free open-weight models, verified",
     "https://aimap.page/en/free-models/category/open-weights/", "The whole free list in one place"),
]


# ---------------------------------------------------------------- render
def rows_open():
    out = []
    for i, (n, maker, params, ctx, lic, runs, best, bench, price, link) in enumerate(OPEN, 1):
        out.append(f"""          <tr>
            <td><a href="{link}" rel="noopener">{n}</a><span class="sub">{maker}</span></td>
            <td class="mono-cell">{params}<span class="sub">context {ctx}</span></td>
            <td>{lic}</td>
            <td>{runs}</td>
            <td>{best}</td>
            <td class="bench-cell">{bench}</td>
          </tr>""")
    return "\n".join(out)


def rows_free():
    out = []
    for i, (n, maker, params, ctx, good, tests, limit) in enumerate(FREE, 1):
        out.append(f"""          <tr>
            <td>{n}<span class="sub">{maker}</span></td>
            <td class="mono-cell">{params}<span class="sub">context {ctx}</span></td>
            <td>{good}</td>
            <td class="mono-cell">#{tests}</td>
            <td>{limit}</td>
          </tr>""")
    return "\n".join(out)


def gates():
    return "\n".join(f"""      <div class="gate">
        <div class="gate__n">{i:02d}</div>
        <div><h3>{t}</h3><p>{how}</p><p class="rec"><span>Record</span> {rec}</p></div>
      </div>""" for i, (t, how, rec) in enumerate(TESTS, 1))


def places():
    return "\n".join(f"""        <li><a href="{u}" rel="noopener"><b>{n}</b> &mdash; {w}</a>
        <span class="when">{when}</span></li>""" for n, w, u, when in PLACES)


c1 = chart(AA, 50, "{:.1f}", highlight=0,
           aria="Artificial Analysis Intelligence Index for 14 open-weight models, Kimi K3.1 Pro highest at 46.5")
c2 = chart(COST, 5.2, "${:.2f}", grad="cg2", highlight=0,
           aria="Cost in dollars to run the intelligence index once, Kimi K3.1 Pro 3.68 dollars, MiMo-V2.6 Flash 13 cents")
c3 = chart(SPEED, 450, "{:.0f}", grad="cg3", highlight=0,
           aria="Output tokens per second on hosted APIs, Nemotron 3.5 Super VL fastest at 424")
c4 = chart(GPQA, 100, "{:.1f}", grad="cg4", highlight=0,
           aria="GPQA Diamond scores, Kimi K3.1 Pro 94.2 down to gpt-oss-20b 71.5")

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Free AI models — benchmarks, tests, and the ones worth your time — Manikant Lab</title>
<meta name="description" content="Eighteen open-weight models and seven free APIs, charted from published benchmarks with the source and date on every number — plus the twelve tests I run before I trust one.">
<meta property="og:title" content="Free AI models — the numbers, and the tests behind them">
<meta property="og:description" content="Eighteen open-weight models and seven free APIs, charted from published benchmarks with the source and date on every number.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Manikant Lab">
<meta property="og:url" content="https://manikantlab.devs.surf/tools.html">
<meta property="og:image" content="https://manikantlab.devs.surf/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://manikantlab.devs.surf/assets/img/og.jpg">
<link rel="canonical" href="https://manikantlab.devs.surf/tools.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" href="assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/favicon.png">
<link rel="stylesheet" href="assets/site.css">
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QEKFFVFTN0"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', 'G-QEKFFVFTN0');
</script>
</head>
<body>
<canvas id="net" aria-hidden="true"></canvas>
<a class="skiplink" href="#main">Skip to content</a>
<header class="nav" id="nav">
  <div class="container nav__in">
    <a class="brand" href="index.html" aria-label="Manikant Lab — home">
      <img class="brand__mark" src="assets/img/logo-mark.webp" alt="" width="320" height="320">
      <span>Manikant<i>&nbsp;Lab</i></span>
    </a>
    <nav class="nav__links" aria-label="Main">
      <a href="about.html">About</a>
      <a href="libraries.html">Libraries</a>
      <a href="tools.html" aria-current="page">Tools</a>
      <a href="work.html">Work</a>
      <a href="skills.html">Skills</a>
      <a href="about.html#journey">Journey</a>
      <a href="build.html">How I build</a>
      <a href="contact.html">Contact</a>
    </nav>
    <button class="nav__toggle" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>
</header>
<main id="main">

<section class="pagehead">
  <div class="container">
    <a class="crumb" href="index.html">&larr; Home</a>
    <span class="num" style="display:block;margin-top:22px">03 &mdash; The tools</span>
    <h1>I test the free tier of everything and keep what <em>earns</em> its place.</h1>
    <p>Eighteen open-weight models, seven free APIs, and the twelve tests I run before I trust any of
    them. The charts below are built from published numbers, with the source and the date on every
    one. The last table is empty on purpose &mdash; that part is my own testing, and I have not run it yet.</p>
    <div class="stats stats--page">
      <div><strong>46.5</strong>Best open index</div>
      <div><strong>18</strong>Open-weight models</div>
      <div><strong>7</strong>Free APIs, no card</div>
      <div><strong>12</strong>Tests I run myself</div>
    </div>
  </div>
</section>

<section class="section" id="how-to-read" style="padding-top:0">
  <div class="container">
    <div class="prose rv">
      <h2 style="margin-top:0">Read a number like this, or do not read it at all</h2>
      <p>Leaderboard numbers move when the harness, the checkpoint or the reasoning effort changes.
      Kimi K3.1 Pro's Terminal-Bench 2.1 reads 88.3 on Moonshot's card and 85.0 on Meta's. That is the
      same model, the same benchmark, three points apart. A one-point gap is noise.</p>
      <div class="callout"><b>So every number here carries its benchmark version and who measured it,</b>
      and no chart blends two harnesses to make a nicer shape. Where a maker only published some of
      the numbers, the cell says so rather than filling the gap with a guess.</div>
      <p>Two things no leaderboard shows: whether a model answers the same way twice, and whether it
      will invent an answer rather than admit it does not know. Those are tests 3 and 10 below, and
      the only way to get them is to run the model on your own work.</p>
    </div>
  </div>
</section>

<section class="section" id="benchmarks" style="padding-top:0">
  <div class="container">
    <div class="section__head rv">
      <span class="eyebrow">Benchmarks</span>
      <h2>Four charts, four questions.</h2>
      <p>Who is smartest. What smart costs. How fast it talks. How much it actually knows. Each chart
      is one source at one version, so the bars inside it are comparable and the bars between charts
      are not.</p>
    </div>

    <figure class="figure rv">
      <figcaption><span>01</span> Who is smartest &mdash; Artificial Analysis Intelligence Index v5.0.1, open weights</figcaption>
      <div class="chartwrap">{c1}</div>
      <p class="fignote">Nine evaluations run by Artificial Analysis itself, not vendor numbers:
      AA-Briefcase, AutomationBench, Terminal-Bench 4.0, FrontierCode 2.0, AA-Omniscience,
      GDP.pdf, HLE-Diamond, CritPt v2 and Terminal-Bench-Science. Read 7 November 2026. Kimi K3.1 Pro
      is 13.9 points clear of the next open model &mdash; and 13.6 points behind the best closed one.</p>
    </figure>

    <figure class="figure rv">
      <figcaption><span>02</span> What smart costs &mdash; dollars to complete that index once</figcaption>
      <div class="chartwrap">{c2}</div>
      <p class="fignote">Same source, same run, same order as the chart above, so you can read straight
      across. Kimi K3.1 Pro costs $3.68 for a 46.5. DeepSeek V4.1 Flash costs $0.60 for 32.6 &mdash; 70%
      of the score for 16% of the money. MiMo-V2.6 Flash is 13 cents. Cost per task is not the same as
      the sticker price per token, because a chatty model spends more of them.</p>
    </figure>

    <figure class="figure rv">
      <figcaption><span>03</span> How fast it talks &mdash; output tokens per second, hosted</figcaption>
      <div class="chartwrap">{c3}</div>
      <p class="fignote">Speed on the hosted API, not on your own hardware. Kimi K3.1 Pro is the
      smartest open model and the slowest thing in this chart; the free Nemotron models are five to
      fourteen times faster and a long way behind on the index. If a model takes 40 minutes per index
      task, that is a working day gone before you have an answer.</p>
    </figure>

    <figure class="figure rv">
      <figcaption><span>04</span> How much it knows &mdash; GPQA Diamond</figcaption>
      <div class="chartwrap">{c4}</div>
      <p class="fignote">Graduate-level science questions. Every number is from the maker's own card,
      which means different harnesses and different reasoning budgets &mdash; read this as a range, not
      a ranking. Seven of these models sit between 86 and 94, and that spread is smaller than the
      difference a harness can make. What the chart does say honestly: the laptop-sized gpt-oss-20b at
      71.5 is not in the same league, and the 27B Qwen at 89.2 is.</p>
    </figure>

    <div class="callout callout--wide rv"><b>What none of these charts can tell you.</b> Whether it
    answers the same way twice. Whether it says &ldquo;I don't know&rdquo; when it doesn't. Whether it
    keeps its Hindi when the question is in Hinglish. Whether it loses the thread four steps into a
    tool loop. Those are the four things that decide whether a model survives a working week, and they
    are all measured by hand, on your own repository. That is the table below.</div>
  </div>
</section>

<section class="section" id="open-weights" style="padding-top:0">
  <div class="container">
    <div class="section__head rv">
      <span class="eyebrow">Open weights</span>
      <h2>Eighteen models whose weights you can download.</h2>
      <p>Open means the weights are there. It does not mean the licence lets you ship. Six of the top
      ten are MIT or Apache; the rest are the maker's own licence, and you read that one before
      commercial use. Prices are per million input and output tokens on the cheapest hosted API.</p>
    </div>
    <div class="tablewrap tablewrap--wide rv">
      <table class="models">
        <thead>
          <tr><th>Model</th><th>Size &middot; context</th><th>Licence</th><th>Where it runs</th><th>Best for</th><th>Published benchmark</th></tr>
        </thead>
        <tbody>
{rows_open()}
        </tbody>
      </table>
    </div>
    <p class="note">Prices in the model column are per million tokens, input / output. Where a maker
    published only some numbers, the benchmark cell says what was published and nothing else.</p>
  </div>
</section>

<section class="section" id="free-api" style="padding-top:0">
  <div class="container">
    <div class="section__head rv">
      <span class="eyebrow">Free API</span>
      <h2>Seven models you can call today with no card and no GPU.</h2>
      <p>OpenRouter's free tier, November 2026. These are for trying a model before you decide
      anything &mdash; the rate limits are the price you pay instead of money.</p>
    </div>
    <div class="tablewrap tablewrap--wide rv">
      <table class="models">
        <thead>
          <tr><th>Model</th><th>Size &middot; context</th><th>What it is good at</th><th>Tests</th><th>The limit to know</th></tr>
        </thead>
        <tbody>
{rows_free()}
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section" id="tests" style="padding-top:0">
  <div class="container">
    <div class="section__head rv">
      <span class="eyebrow">The battery</span>
      <h2>Twelve tests, the same order every time.</h2>
      <p>This is the benchmark that counts, because it is the only one measured on your work. Run them
      in this order &mdash; a model that fails the fit test never gets to the interesting ones.</p>
    </div>
    <div class="gates rv">
{gates()}
    </div>
  </div>
</section>

<section class="section" id="feedback" style="padding-top:0">
  <div class="container">
    <div class="section__head rv">
      <span class="eyebrow">My feedback</span>
      <h2>What I write down the same day I run a model.</h2>
      <p>Fill this in before the number fades, in your own words. It copies as a block of text &mdash;
      paste it into an email or a note. Nothing here is sent anywhere by itself.</p>
    </div>
    <form class="fb rv" id="fbform" novalidate>
      <div class="fb__grid">
        <label class="fb__f"><span>Model</span>
          <input type="text" name="model" placeholder="DeepSeek V4.1 Flash" autocomplete="off"></label>
        <label class="fb__f"><span>Test date</span>
          <input type="date" name="date"></label>
        <label class="fb__f"><span>Harness / tool</span>
          <input type="text" name="harness" placeholder="Claude Code, Ollama, OpenRouter" autocomplete="off"></label>
        <label class="fb__f"><span>Hardware or API tier</span>
          <input type="text" name="hardware" placeholder="M2 32 GB, 4-bit / free tier" autocomplete="off"></label>
        <label class="fb__f"><span>Which tests (#)</span>
          <input type="text" name="tests" placeholder="1, 3, 4, 10" autocomplete="off"></label>
        <label class="fb__f"><span>Would I use it again?</span>
          <select name="again">
            <option value="">&mdash;</option>
            <option>Yes</option>
            <option>Only for one job</option>
            <option>No</option>
          </select></label>
      </div>
      <label class="fb__f"><span>Results, as numbers</span>
        <input type="text" name="results" placeholder="Pass@1 7/10, TTFT 1.2 s, 41 tok/s, 18k tokens per task" autocomplete="off"></label>
      <label class="fb__f"><span>My take, in my own words</span>
        <textarea name="take" rows="5" placeholder="What it did well, where it broke, whether the number matched what it felt like."></textarea></label>
      <div class="fb__bar">
        <button class="btn" type="submit">Copy my feedback</button>
        <a class="btn btn--ghost" id="fbsend" href="mailto:manikantsharma.com@zoho.in">Send it to me</a>
        <span class="fb__state" id="fbstate" role="status"></span>
      </div>
    </form>
  </div>
</section>

<section class="section" id="where" style="padding-top:0">
  <div class="container">
    <div class="section__head rv">
      <span class="eyebrow">Where to look next</span>
      <h2>Ten places I check before I download anything.</h2>
    </div>
    <ol class="places rv">
{places()}
    </ol>
    <div class="callout callout--wide rv"><b>One thing to carry away.</b> Leaderboard numbers move when
    the harness and the checkpoint change. Write the benchmark version and who measured it next to
    every number you keep, and treat a one-point gap as noise. A model that is two points behind and
    ten times cheaper is usually the better model for the work you actually have.</div>
    <div class="pager">
      <a href="libraries.html">&larr; The four disciplines</a>
      <a href="contact.html">Tell me what it scored &rarr;</a>
    </div>
  </div>
</section>
</main>

<footer class="foot">
  <div class="container foot__in">
    <span class="foot__brand">
      <img src="assets/img/logo-full.webp" alt="Manikant Lab — AI engineer, agent systems"
           width="1000" height="193" loading="lazy">
      <em>&copy; 2026 &middot; Manikant Sharma</em>
    </span>
    <span><a href="mailto:manikantsharma.com@zoho.in">Email</a> &middot;
          <a href="https://github.com/manikant-sharma-ai" rel="noopener">GitHub</a> &middot;
          <a href="https://huggingface.co/manikant-openlab" rel="noopener">Hugging Face</a> &middot;
          <a href="https://x.com/ManikantSharmaX" rel="noopener">X</a> &middot;
          <a href="https://www.instagram.com/manikantsharma.ai" rel="noopener">Instagram</a> &middot;
          <a href="https://www.reddit.com/user/ManikantSharma/" rel="noopener">Reddit</a> &middot;
          <a href="https://facebook.com/people/Manikant-Sharma/61595821115608/" rel="noopener">Facebook</a></span>
  </div>
</footer>
<script src="assets/site.js"></script>
<script>
(function(){{
  var f = document.getElementById('fbform');
  if(!f) return;
  var state = document.getElementById('fbstate');
  var send = document.getElementById('fbsend');

  function build(){{
    var g = function(n){{ var el = f.elements[n]; return el && el.value ? el.value.trim() : ''; }};
    var L = [];
    L.push('Model: ' + (g('model') || '-'));
    L.push('Test date: ' + (g('date') || '-'));
    L.push('Harness / tool: ' + (g('harness') || '-'));
    L.push('Hardware or API tier: ' + (g('hardware') || '-'));
    L.push('Tests run: ' + (g('tests') || '-'));
    L.push('Results: ' + (g('results') || '-'));
    L.push('');
    L.push('My take:');
    L.push(g('take') || '-');
    L.push('');
    L.push('Would I use it again: ' + (g('again') || '-'));
    return L.join('\\n');
  }}

  function flash(msg, ok){{
    state.textContent = msg;
    state.className = 'fb__state' + (ok ? ' ok' : '');
    setTimeout(function(){{ state.textContent = ''; }}, 2600);
  }}

  f.addEventListener('submit', function(e){{
    e.preventDefault();
    var text = build();
    var done = function(){{ flash('Copied. Paste it anywhere.', true); }};
    if(navigator.clipboard && navigator.clipboard.writeText){{
      navigator.clipboard.writeText(text).then(done).catch(function(){{ fallback(); }});
    }} else {{ fallback(); }}
    function fallback(){{
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try{{ document.execCommand('copy'); }}catch(err){{}}
      document.body.removeChild(ta); done();
    }}
  }});

  f.addEventListener('input', function(){{
    send.href = 'mailto:manikantsharma.com@zoho.in?subject='
      + encodeURIComponent('Model feedback — ' + (f.elements.model.value || 'untitled'))
      + '&body=' + encodeURIComponent(build());
  }});
  f.dispatchEvent(new Event('input'));
}})();
</script>
</body>
</html>
"""

with io.open(OUT, "w", encoding="utf-8") as fh:
    fh.write(PAGE)
print("wrote", OUT, len(PAGE), "bytes")
