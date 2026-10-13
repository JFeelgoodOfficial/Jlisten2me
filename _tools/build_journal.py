#!/usr/bin/env python3
"""Build the Jlisten2me journal from _journal/articles/*.md.

Only articles whose `date` is on or before today (US Central time) are published.
Everything else stays in _journal/, which neither GitHub Pages (Jekyll skips folders
that start with an underscore) nor Vercel (.vercelignore) serves. A weekly GitHub
Action runs this script, so each article goes live on its date without anyone
touching the repo.

Writes:
  journal/index.html            journal index
  journal/<slug>/index.html     one page per published article
  journal/journal.css           shared styles, copied from index.html's marked blocks
  journal/site.js               palette and light/dark controls
  journal/feed.xml              RSS feed
  sitemap.xml, llms.txt, llms-full.txt
  index.html                    the "From the journal" block between its markers

Usage: python3 _tools/build_journal.py [--today YYYY-MM-DD] [--check]
  --today  pretend it's a different day (preview a future week)
  --check  lint every article against _journal/GUIDELINES.md and exit
Standard library only.
"""

import argparse
import datetime as dt
import html
import json
import math
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_journal" / "articles"
OUT = ROOT / "journal"
SITE = "https://jlisten2me.com"
TZ = ZoneInfo("America/Chicago")
AUTHOR = "JFeelgood"

HOME_DEF = (
    "Jlisten2me is a confidential one-hour listening service in Austin, Texas, by phone or "
    "in person. Not therapy, not coaching. Nothing recorded, no notes kept."
)


# ---------------------------------------------------------------- parsing

class Article:
    def __init__(self, path):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            sys.exit(f"{path.name}: missing front matter")
        meta = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        for key in ("title", "slug", "description", "date"):
            if not meta.get(key):
                sys.exit(f"{path.name}: front matter needs '{key}'")
        if meta["slug"] != path.stem:
            sys.exit(f"{path.name}: slug '{meta['slug']}' must match the file name")
        self.path = path
        self.title = meta["title"]
        self.slug = meta["slug"]
        self.description = meta["description"]
        self.date = dt.date.fromisoformat(meta["date"])
        self.updated = dt.date.fromisoformat(meta["updated"]) if meta.get("updated") else self.date
        body = m.group(2).strip()
        body = re.sub(r"^# .*\n+", "", body)  # the title lives in front matter
        self.body_md = body
        self.words = len(re.findall(r"[A-Za-z0-9'’]+", body))
        self.url = f"{SITE}/journal/{self.slug}/"
        self.path_url = f"/journal/{self.slug}/"

    @property
    def minutes(self):
        return max(1, math.ceil(self.words / 230))

    def plain_text(self):
        t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", self.body_md)
        t = re.sub(r"\*\*?([^*]+)\*\*?", r"\1", t)
        return t


def inline(text):
    out = html.escape(text, quote=False)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                 lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![*\w])\*([^*]+)\*(?![*\w])", r"<em>\1</em>", out)
    return out


def render_body(md):
    """Headings (##), paragraphs, and multi-line paragraphs that show one sentence per line."""
    parts = []
    for block in re.split(r"\n\s*\n", md.strip()):
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        if lines[0].startswith("## "):
            parts.append(f"<h2>{inline(lines[0][3:])}</h2>")
            lines = lines[1:]
            if not lines:
                continue
        if len(lines) == 1:
            parts.append(f"<p>{inline(lines[0])}</p>")
        else:
            spans = "".join(f'<span class="line">{inline(l)}</span>' for l in lines)
            parts.append(f'<p class="lines">{spans}</p>')
    return "\n".join(parts)


def load_articles():
    arts = [Article(p) for p in sorted(SRC.glob("*.md"))]
    slugs = [a.slug for a in arts]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        sys.exit(f"duplicate slugs: {dupes}")
    return arts


# ---------------------------------------------------------------- linting

BANNED_PHRASES = [
    "navigate", "journey", "landscape", "unpack", "holistic", "self-care", "hold space",
    "safe space", "it's important to", "at the end of the day", "you've got this",
    "studies show", "research shows", "experts agree", "delve", "leverage", "testament",
]
ANTITHESIS = [
    r"\bit'?s not\b[^.]*,\s*it'?s\b",
    r"\bisn't\b[^.]*\.\s+it'?s\b",
    r"\bnot (?:just |only |because )[^.]*\b(?:but|because)\b",
    r"\bnot because\b[^.]*\.\s+because\b",
    r"\bbut rather\b",
    r"\bnot [a-z]+, but\b",
    r"\bthe (?:problem|point|question|issue) isn't\b",
    r"\bthis isn't about\b",
]


def lint(a):
    problems = []
    body = a.body_md
    for ch, name in (("—", "em dash"), (" – ", "spaced en dash"), ("--", "double hyphen")):
        if ch in body or ch in a.title or ch in a.description:
            problems.append(f"contains {name}")
    low = body.lower()
    for phrase in BANNED_PHRASES:
        if phrase in low:
            problems.append(f"banned phrase: '{phrase}'")
    for pat in ANTITHESIS:
        for m in re.finditer(pat, low):
            problems.append(f"possible antithetical: '{m.group(0)[:70]}'")
    if not (650 <= a.words <= 1150):
        problems.append(f"{a.words} words, outside 700 to 1,100")
    if "988" not in body:
        problems.append("no 988 line")
    if "/#book" not in body:
        problems.append("no booking link to /#book")
    if re.search(r"^\s*(?:[-*]|\d+\.)\s", body, re.M):
        problems.append("contains a list")
    if len(a.description) > 160:
        problems.append(f"description is {len(a.description)} characters, keep under 155")
    if re.search(r"\b(?:a client|one client|someone i spoke|a founder i|a woman i|a man i|someone once told me)\b", low):
        problems.append("reads like a client story")
    return problems


# ---------------------------------------------------------------- shared assets

def shared_css():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    blocks = re.findall(r"/\* @shared-css-start[^*]*\*/\n(.*?)\s*/\* @shared-css-end \*/", src, re.S)
    if len(blocks) < 3:
        sys.exit("index.html: expected three @shared-css blocks")
    return BASE_CSS + "\n".join(b.rstrip() for b in blocks) + "\n" + JOURNAL_CSS


BASE_CSS = """*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url('/fonts/inter-latin-wght-normal.woff2') format('woff2');
}
"""


JOURNAL_CSS = """
/* ---- Journal ---- */
html { scroll-padding-top: calc(var(--header-h) + 12px); }
main.j { padding: calc(var(--header-h) + 3.5rem) 2rem 5rem; }
.j-wrap { max-width: 680px; margin: 0 auto; }
a.skip:focus { position: fixed; top: 8px; left: 8px; width: auto; height: auto; clip: auto; padding: 0.5rem 1rem; background: var(--bg); border: 1px solid var(--accent); border-radius: 6px; z-index: 200; }
.crumbs { font-size: 0.78rem; color: var(--text-3); margin-bottom: 1.6rem; }
.crumbs a { color: var(--text-2); text-decoration: none; }
.crumbs a:hover { color: var(--text); }
.crumbs span { margin: 0 0.45rem; }
.j-eyebrow { font-size: 0.72rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); font-weight: 500; margin-bottom: 0.9rem; }
.j h1 { font-size: clamp(2rem, 5.4vw, 3rem); font-weight: 300; letter-spacing: -0.035em; line-height: 1.15; margin-bottom: 1rem; }
.j-meta { font-size: 0.82rem; color: var(--text-3); margin-bottom: 2.6rem; }
.j-body p { color: var(--text-2); font-size: 1.04rem; line-height: 1.85; margin-bottom: 1.25rem; }
.j-body p.lines { color: var(--text); font-size: 1.12rem; font-weight: 300; margin-bottom: 1.8rem; }
.line { display: block; }
.line + .line { margin-top: 0.35em; }
.j-body h2 { font-size: 1.32rem; font-weight: 500; letter-spacing: -0.015em; line-height: 1.35; margin: 2.6rem 0 0.9rem; }
.j-body a { color: var(--accent-soft); text-underline-offset: 3px; }
.j-note { margin-top: 2.4rem; padding: 1.1rem 1.3rem; border: 1px dashed var(--border); border-radius: 8px; font-size: 0.84rem; color: var(--text-2); line-height: 1.65; }
.j-cta { margin-top: 2.4rem; padding: 1.8rem; background: var(--surface); border: 1px solid var(--border); border-left: 3px solid var(--accent); border-radius: var(--radius); }
.j-cta h2 { font-size: 1.1rem; font-weight: 500; margin: 0 0 0.4rem; letter-spacing: -0.01em; }
.j-cta p { font-size: 0.9rem; color: var(--text-2); margin-bottom: 1.2rem; }
.j-more { margin-top: 3.4rem; border-top: 1px solid var(--border); padding-top: 2rem; }
.j-more h2 { font-size: 0.72rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); font-weight: 500; margin-bottom: 1rem; }
.j-list { list-style: none; display: grid; gap: 1rem; }
.j-item a { display: block; padding: 1.4rem 1.5rem; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); text-decoration: none; transition: border-color 0.25s, transform 0.2s; }
.j-item a:hover { border-color: var(--accent); transform: translateY(-2px); }
.j-item h3 { font-size: 1.02rem; font-weight: 500; letter-spacing: -0.01em; margin-bottom: 0.35rem; line-height: 1.4; }
.j-item p { font-size: 0.87rem; color: var(--text-2); line-height: 1.6; }
.j-item time { display: block; font-size: 0.74rem; color: var(--text-3); margin-top: 0.6rem; }
.j-intro { color: var(--text-2); margin-bottom: 2.6rem; }
.j-intro p + p { margin-top: 0.9rem; }
.j-empty { color: var(--text-3); font-size: 0.9rem; }
[data-theme="light"] .j-item a, [data-theme="light"] .j-cta { box-shadow: 0 1px 2px rgba(15,23,35,0.04), 0 10px 26px rgba(15,23,35,0.055); }
@media (max-width: 800px) {
  :root { --header-h: 130px; }
  .nav-row { padding: 0.85rem 1.25rem; }
  .nav-links { display: none; }
  .palette-bar { padding: 0.5rem 1.25rem 0.6rem; gap: 0.6rem; row-gap: 0.55rem; flex-wrap: wrap; overflow-x: visible; }
  .palette-q { font-size: 0.75rem; width: 100%; white-space: normal; }
  .swatch { width: 24px; height: 24px; }
  main.j { padding: calc(var(--header-h) + 2.2rem) 1.25rem 4rem; }
  .j-body p { font-size: 1rem; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
"""

SITE_JS = """/* Palette and light/dark controls for journal pages. The choice is shared with the home page. */
(function () {
  var root = document.documentElement;
  var PALETTES = ["tide","moss","ember","plum","clay","ink"];
  var THEME_COLORS = {
    tide:{dark:"#0f1923",light:"#f6f9fc"}, moss:{dark:"#0f1a16",light:"#f5faf7"},
    ember:{dark:"#1a1310",light:"#fdf8f4"}, plum:{dark:"#16121f",light:"#faf8fd"},
    clay:{dark:"#1c1315",light:"#fdf7f8"}, ink:{dark:"#121416",light:"#f7f8f9"}
  };
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function sync() {
    var set = THEME_COLORS[root.dataset.palette] || THEME_COLORS.tide;
    var meta = document.getElementById("themeColorMeta");
    if (meta) meta.setAttribute("content", set[root.dataset.theme] || set.dark);
    document.querySelectorAll(".swatch").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.palette === root.dataset.palette));
    });
    var t = document.getElementById("modeToggle");
    if (t) {
      var dark = root.dataset.theme === "dark";
      t.setAttribute("aria-pressed", String(dark));
      t.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
      document.getElementById("modeLabel").textContent = dark ? "Dark" : "Light";
    }
  }
  document.querySelectorAll(".swatch").forEach(function (b) {
    b.addEventListener("click", function () {
      if (PALETTES.indexOf(b.dataset.palette) < 0) return;
      root.dataset.palette = b.dataset.palette; store("j2m-palette", b.dataset.palette); sync();
    });
  });
  var toggle = document.getElementById("modeToggle");
  if (toggle) toggle.addEventListener("click", function () {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    store("j2m-theme", root.dataset.theme); sync();
  });
  sync();
})();
"""

# Runs in <head> so the saved palette applies before first paint.
THEME_BOOT = (
    "<script>(function(){var r=document.documentElement,p,t;"
    "try{p=localStorage.getItem('j2m-palette');t=localStorage.getItem('j2m-theme');}catch(e){}"
    "if(p&&/^(tide|moss|ember|plum|clay|ink)$/.test(p))r.dataset.palette=p;"
    "r.dataset.theme=t==='light'||t==='dark'?t:(window.matchMedia&&matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');"
    "})();</script>"
)

ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' "
        "rx='7' fill='%235b8db8'/%3E%3Cpath d='M8 13v6M12 10v12M16 12.5v7M20 9v14M24 13v6' stroke='%23fff' "
        "stroke-width='2.4' stroke-linecap='round'/%3E%3C/svg%3E")

HEADER = """<a class="sr-only skip" href="#main">Skip to the content</a>
<header class="site">
  <div class="nav-row">
    <a href="/" class="nav-logo">Jlisten2me</a>
    <nav aria-label="Main"><ul class="nav-links">
      <li><a href="/#who">Who it's for</a></li>
      <li><a href="/#how">How it works</a></li>
      <li><a href="/#trust">Confidentiality</a></li>
      <li><a href="/#faq">FAQ</a></li>
      <li><a href="/#pricing">Pricing</a></li>
      <li><a href="/journal/">Journal</a></li>
      <li><a href="/#book">Book</a></li>
    </ul></nav>
  </div>
  <div class="palette-bar">
    <span class="palette-q" id="paletteQ">What color are you feeling today?</span>
    <div class="swatches" role="group" aria-labelledby="paletteQ">
      <button class="swatch sw-tide"  data-palette="tide"  aria-pressed="true"  title="Tide"><span class="sr-only">Tide</span></button>
      <button class="swatch sw-moss"  data-palette="moss"  aria-pressed="false" title="Moss"><span class="sr-only">Moss</span></button>
      <button class="swatch sw-ember" data-palette="ember" aria-pressed="false" title="Ember"><span class="sr-only">Ember</span></button>
      <button class="swatch sw-plum"  data-palette="plum"  aria-pressed="false" title="Plum"><span class="sr-only">Plum</span></button>
      <button class="swatch sw-clay"  data-palette="clay"  aria-pressed="false" title="Clay"><span class="sr-only">Clay</span></button>
      <button class="swatch sw-ink"   data-palette="ink"   aria-pressed="false" title="Ink"><span class="sr-only">Ink</span></button>
    </div>
    <button class="mode-toggle" id="modeToggle" aria-pressed="true">
      <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
      <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2M12 20v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2 12h2M20 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>
      <span id="modeLabel">Dark</span>
    </button>
  </div>
</header>"""

FOOTER = """<footer>
  <div class="footer-inner">
    <span class="footer-brand">Jlisten2me</span>
    <ul class="footer-links">
      <li><a href="/#who">Who it's for</a></li>
      <li><a href="/#how">How it works</a></li>
      <li><a href="/#trust">Confidentiality</a></li>
      <li><a href="/#faq">FAQ</a></li>
      <li><a href="/#pricing">Pricing</a></li>
      <li><a href="/journal/">Journal</a></li>
      <li><a href="/#book">Book</a></li>
      <li><a href="https://instagram.com/JFeelgoodOfficial" target="_blank" rel="noopener">Instagram</a></li>
    </ul>
    <p class="footer-policy">Reschedule free up to 24 hours before your session. Cancellations inside 24 hours aren't refunded.</p>
    <p class="footer-copy">YEAR Jlisten2me · JFeelgood · Austin, TX · Not therapy, not legal or financial advice. In a crisis, call or text 988.</p>
  </div>
</footer>"""


def head(title, description, canonical, og_type, extra_meta="", jsonld=None):
    e = html.escape
    ld = ""
    if jsonld:
        ld = '\n  <script type="application/ld+json">\n' + json.dumps(jsonld, indent=2, ensure_ascii=False) + "\n  </script>"
    return f"""<!DOCTYPE html>
<html lang="en" data-palette="tide" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}" />
  <meta name="author" content="{AUTHOR}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="theme-color" content="#0f1923" id="themeColorMeta" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:site_name" content="Jlisten2me" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(description)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:image" content="{SITE}/og.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="Jlisten2me. Say it out loud. Confidential listening by phone or in person in Austin." />{extra_meta}
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{e(title)}" />
  <meta name="twitter:description" content="{e(description)}" />
  <meta name="twitter:image" content="{SITE}/og.png" />
  <link rel="alternate" type="application/rss+xml" title="Jlisten2me Journal" href="{SITE}/journal/feed.xml" />
  <link rel="icon" href="{ICON}" />
  <link rel="preload" href="/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="/journal/journal.css" />
  {THEME_BOOT}{ld}
</head>
<body>
{HEADER}
"""


def tail(year):
    return FOOTER.replace("YEAR", str(year)) + '\n<script src="/journal/site.js" defer></script>\n</body>\n</html>\n'


def human_date(d):
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def item_html(a):
    return (f'      <li class="j-item"><a href="{a.path_url}">'
            f"<h3>{html.escape(a.title)}</h3><p>{html.escape(a.description)}</p>"
            f'<time datetime="{a.date.isoformat()}">{human_date(a.date)}</time></a></li>')


# ---------------------------------------------------------------- pages

PERSON = {"@type": "Person", "@id": f"{SITE}/#person", "name": AUTHOR, "url": f"{SITE}/#about",
          "sameAs": ["https://instagram.com/JFeelgoodOfficial"]}
ORG_REF = {"@id": f"{SITE}/#service"}
BLOG_ID = f"{SITE}/journal/#blog"


def article_page(a, published, today):
    idx = published.index(a)
    # Neighbours first, then the most recent, never anything unpublished.
    picks = []
    for cand in [published[idx - 1] if idx > 0 else None,
                 published[idx + 1] if idx + 1 < len(published) else None] + published:
        if cand and cand is not a and cand not in picks:
            picks.append(cand)
        if len(picks) == 3:
            break
    more = ""
    if picks:
        more = ('  <section class="j-more" aria-labelledby="more-h">\n    <h2 id="more-h">More from the journal</h2>\n'
                '    <ul class="j-list">\n' + "\n".join(item_html(p) for p in picks) + "\n    </ul>\n  </section>\n")

    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "@id": a.url + "#article",
                "headline": a.title,
                "description": a.description,
                "datePublished": a.date.isoformat(),
                "dateModified": a.updated.isoformat(),
                "wordCount": a.words,
                "inLanguage": "en-US",
                "url": a.url,
                "mainEntityOfPage": a.url,
                "image": f"{SITE}/og.png",
                "author": PERSON,
                "publisher": ORG_REF,
                "isPartOf": {"@id": BLOG_ID},
                "about": {"@type": "Thing", "name": "Confidential listening"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Journal", "item": f"{SITE}/journal/"},
                    {"@type": "ListItem", "position": 3, "name": a.title, "item": a.url},
                ],
            },
        ],
    }
    extra = (f'\n  <meta property="article:published_time" content="{a.date.isoformat()}" />'
             f'\n  <meta property="article:modified_time" content="{a.updated.isoformat()}" />'
             f'\n  <meta property="article:author" content="{AUTHOR}" />'
             f'\n  <meta property="article:section" content="Journal" />')
    title = a.title[0].upper() + a.title[1:]
    page = head(f"{title} | Jlisten2me", a.description, a.url, "article", extra, jsonld)
    page += f"""<main class="j" id="main">
<article class="j-wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/journal/">Journal</a></nav>
  <p class="j-eyebrow">Journal</p>
  <h1>{html.escape(title)}</h1>
  <p class="j-meta">By <a href="/#about">{AUTHOR}</a> · <time datetime="{a.date.isoformat()}">{human_date(a.date)}</time> · {a.minutes} min read</p>
  <div class="j-body">
{render_body(a.body_md)}
  </div>
  <p class="j-note">Journal articles describe situations in general. None of them is drawn from a session, and nothing anyone says in an hour ever appears here. Jlisten2me is not therapy, and not legal or financial advice.</p>
  <aside class="j-cta" aria-labelledby="cta-h">
    <h2 id="cta-h">An hour that belongs to you</h2>
    <p>Phone $60 an hour, in person in Austin $100, five hours for $225. Book under a first name. Nothing recorded, nothing kept.</p>
    <a class="btn btn-primary" href="/#book">Pick a time</a>
  </aside>
{more}</article>
</main>
"""
    return page + tail(today.year)


def index_page(published, today):
    items = "\n".join(item_html(a) for a in published) or '      <li class="j-empty">The first article is on its way.</li>'
    desc = ("Articles from Jlisten2me on carrying things you can't hand to the people around you: "
            "decisions you can't share yet, marriages, family, big changes, and moments you need to rehearse.")
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Blog",
                "@id": BLOG_ID,
                "name": "Jlisten2me Journal",
                "url": f"{SITE}/journal/",
                "description": desc,
                "inLanguage": "en-US",
                "author": PERSON,
                "publisher": ORG_REF,
                "blogPost": [{"@type": "BlogPosting", "@id": a.url + "#article", "headline": a.title,
                              "url": a.url, "datePublished": a.date.isoformat()} for a in published],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Journal", "item": f"{SITE}/journal/"},
                ],
            },
        ],
    }
    page = head("Journal | Jlisten2me", desc, f"{SITE}/journal/", "website", "", jsonld)
    page += f"""<main class="j" id="main">
<div class="j-wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a></nav>
  <p class="j-eyebrow">Journal</p>
  <h1>Things people carry alone</h1>
  <div class="j-intro">
    <p>Each article describes one situation from the inside: the decision you can't share yet, the worry you don't want to bring home, the conversation you've rehearsed forty times.</p>
    <p>None of them is drawn from a session. Nothing anyone says in an hour ever appears here, with or without a name. A new article goes up every Tuesday.</p>
  </div>
  <ul class="j-list">
{items}
  </ul>
</div>
</main>
"""
    return page + tail(today.year)


def feed(published, now):
    def rfc822(d):
        return dt.datetime(d.year, d.month, d.day, 6, 0, tzinfo=TZ).strftime("%a, %d %b %Y %H:%M:%S %z")
    items = "".join(
        f"""
    <item>
      <title>{html.escape(a.title)}</title>
      <link>{a.url}</link>
      <guid isPermaLink="true">{a.url}</guid>
      <pubDate>{rfc822(a.date)}</pubDate>
      <description>{html.escape(a.description)}</description>
    </item>""" for a in published[:20])
    last = rfc822(published[0].date) if published else rfc822(now)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Jlisten2me Journal</title>
    <link>{SITE}/journal/</link>
    <atom:link href="{SITE}/journal/feed.xml" rel="self" type="application/rss+xml" />
    <description>Articles on carrying things you can't hand to the people around you.</description>
    <language>en-us</language>
    <lastBuildDate>{last}</lastBuildDate>{items}
  </channel>
</rss>
"""


def sitemap(published, home_lastmod):
    urls = [(f"{SITE}/", home_lastmod, "1.0"),
            (f"{SITE}/journal/", published[0].date.isoformat() if published else home_lastmod, "0.8")]
    urls += [(a.url, a.updated.isoformat(), "0.7") for a in published]
    body = "".join(f"""
  <url>
    <loc>{u}</loc>
    <lastmod>{d}</lastmod>
    <priority>{p}</priority>
  </url>""" for u, d, p in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}\n</urlset>\n'


def replace_between(text, start, end, new):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pat.search(text):
        sys.exit(f"marker {start} not found")
    return pat.sub(lambda _: start + new + end, text)


def update_llms(published):
    p = ROOT / "llms.txt"
    s = p.read_text(encoding="utf-8")
    lines = "\n".join(f"- [{a.title}]({a.url}): {a.description}" for a in published)
    block = ("\n## Journal\n\nArticles by JFeelgood describing hard situations in general. None is drawn from a session. "
             f"Index: {SITE}/journal/ . Full text of every published article: {SITE}/llms-full.txt\n\n"
             + (lines + "\n" if lines else ""))
    p.write_text(replace_between(s, "<!-- journal:start -->", "<!-- journal:end -->", block), encoding="utf-8")

    full = [f"# Jlisten2me Journal, full text\n\n> {HOME_DEF}\n\nEvery published journal article, newest first. "
            "None is drawn from a session.\n"]
    for a in published:
        full.append(f"\n---\n\n## {a.title}\n\nURL: {a.url}\nPublished: {a.date.isoformat()}\nAuthor: {AUTHOR}\n\n{a.plain_text()}\n")
    (ROOT / "llms-full.txt").write_text("".join(full), encoding="utf-8")


def update_home(published):
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    latest = published[:3]
    if latest:
        items = "\n".join(item_html(a) for a in latest)
        block = f"""
<section id="journal" aria-labelledby="journal-h">
  <div class="container">
    <div class="section-header fade-up">
      <p class="section-label">Journal</p>
      <h2 id="journal-h">Things people carry alone.</h2>
      <p class="lede"><span class="line">A new article every Tuesday.</span><span class="line">None of them is drawn from a session.</span></p>
    </div>
    <ul class="j-list home-j fade-up">
{items}
    </ul>
    <p class="how-note fade-up"><a href="/journal/">Read the journal</a></p>
  </div>
</section>
"""
    else:
        block = "\n"
    p.write_text(replace_between(s, "<!-- journal-latest:start -->", "<!-- journal-latest:end -->", block), encoding="utf-8")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", type=dt.date.fromisoformat)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    today = args.today or dt.datetime.now(TZ).date()

    arts = load_articles()
    bad = {a.slug: lint(a) for a in arts}
    bad = {k: v for k, v in bad.items() if v}
    if args.check:
        for slug, probs in bad.items():
            print(f"{slug}:")
            for pr in probs:
                print(f"  - {pr}")
        dates = sorted(a.date for a in arts)
        print(f"{len(arts)} articles, {len(arts) - len(bad)} clean. Dates {dates[0]} to {dates[-1]}." if arts else "no articles")
        sys.exit(1 if bad else 0)

    published = sorted([a for a in arts if a.date <= today], key=lambda a: (a.date, a.slug), reverse=True)
    for a in published:
        if a.slug in bad:
            sys.exit(f"{a.slug} is due to publish but fails the guidelines: {bad[a.slug]}")

    OUT.mkdir(exist_ok=True)
    (OUT / "journal.css").write_text(shared_css(), encoding="utf-8")
    (OUT / "site.js").write_text(SITE_JS, encoding="utf-8")
    keep = {a.slug for a in published}
    for d in OUT.iterdir():
        if d.is_dir() and d.name not in keep and (d / "index.html").exists():
            (d / "index.html").unlink()
            d.rmdir()
    for a in published:
        (OUT / a.slug).mkdir(exist_ok=True)
        (OUT / a.slug / "index.html").write_text(article_page(a, published, today), encoding="utf-8")
    (OUT / "index.html").write_text(index_page(published, today), encoding="utf-8")
    (OUT / "feed.xml").write_text(feed(published, today), encoding="utf-8")

    home_lastmod = dt.date.fromtimestamp((ROOT / "index.html").stat().st_mtime).isoformat()
    old = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    m = re.search(r"<loc>https://jlisten2me.com/</loc>\s*<lastmod>([\d-]+)</lastmod>", old)
    if m:
        home_lastmod = m.group(1)
    if published and published[0].date.isoformat() > home_lastmod:
        home_lastmod = published[0].date.isoformat()  # the home page lists the latest articles
    (ROOT / "sitemap.xml").write_text(sitemap(published, home_lastmod), encoding="utf-8")
    update_llms(published)
    update_home(published)
    upcoming = sorted(a.date for a in arts if a.date > today)
    print(f"published {len(published)} of {len(arts)}; next: {upcoming[0] if upcoming else 'none scheduled'}")


if __name__ == "__main__":
    main()
