# Jlisten2me - Active Listening Service

Single-page landing site for listen2me.com - offering confidential, non-judgmental 1-hour listening sessions.

## Pricing
- **Phone**: $20/hr (voice only)
- **Video**: $25/hr (Zoom/Google Meet) 
- **Coffee Shop**: $60/hr (Austin public location)
- **Priority Daytime**: +$100 add-on (same-day response)
- **Priority Day + Night**: +$300 add-on (24/7 window)

## Features
- Pure HTML/CSS/JS - 25KB gzipped, no frameworks
- Mobile-responsive, SEO-optimized for "active listening service Austin"
- Inter font via Google Fonts CDN
- Smooth scroll, fade-up animations, backdrop-blur nav
- Client-side contact form (Formspree-ready)
- GitHub Pages/Vercel deploy-ready

## Deploy
1. Drop `index.html` in repo root
2. GitHub Pages: Settings → Pages → Source: Deploy from branch `main`
3. Vercel: Connect GitHub repo, deploy instantly

## Customization
```
<!-- Form backend - swap to Formspree -->
<form action="https://formspree.io/f/YOUR_ID" method="POST">
```

```
<!-- Calendly embed - replace form -->
<div class="calendly-inline-widget" data-url="https://calendly.com/your-link" style="min-width:320px;height:700px;"></div>
<script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>
```

## crystal.html
Standalone, private page at `/crystal.html` (marked `noindex`) for Crystal M. Pratt. Three parts and nothing else:

1. **Ten ways to make your hours count** — positioning and work-finding tips. Each card expands on a **Tell me more** button to a 5 to 7 step how-to guide plus a note field.
2. **Work for yourself** — four self-employment options (a delivery round, power washing, setup packages, and a hybrid running all three). Each expands to stat tiles, a setup guide, a caveat, and two tabbed month plans taking her from $0 to $1,000 and from $0 to $4,000.
3. **Your notebook** — free-form timestamped notes, deletable, added by button or Ctrl/Cmd+Enter.

- Everything autosaves to `localStorage` under `crystal-page-review-v1`. Nothing leaves the browser.
- **Export Markdown** writes `crystal-ideas-YYYY-MM-DD.md` with all three sections; notes also export alone as `crystal-notes-YYYY-MM-DD.md`.
- **Print or save as PDF** builds a separate `#printSheet` (also on `beforeprint`, so Ctrl+P works) that `@media print` swaps in: black on white, tick boxes beside every step, and only the plans she has not ruled out.
- Content lives in the `SECTIONS` and `SPINOFFS` arrays near the top of the script. The footer carries a version stamp; bump it with each change.

## wiredwright.html
Standalone, private page at `/wiredwright.html` (marked `noindex`) for Wired Wright, an electrical contractor covering greater Austin. It is a content-intake tool, not the public landing page: he answers it once, exports the brief, and whoever builds the site works from that.

- **Hero**: a three.js particle plug (body, three prongs, curving cord) that morphs into the words WIRED WRIGHT on a loop. Falls back to plain styled type if WebGL or the CDN fails, and holds the text still under `prefers-reduced-motion`.
- **28 questions** in seven parts, ordered the way a visitor reads a landing page: first screen, trust strip, services, proof, price and form, FAQ, footer and local search. Each question carries the research note behind it (license-badge lift, four-field forms, Austin Energy EV rebate rules, TECL placement).
- Each question has **tap-to-load recommended answers** that drop into the composer for editing, a **chat box** that saves answers as a thread, and per-answer edit and delete.
- Everything autosaves to `localStorage` under `wiredwright-content-v1`. Nothing leaves the browser.
- **Download Markdown** writes `wiredwright-content-YYYY-MM-DD.md` with every answer, the research note per question, a build order for the page, the still-open questions, and the source list. Copy-to-clipboard and a live preview sit beside it.
- Conversion figures come from marketing-agency and vendor blogs, not audited research, and the page says so. Austin Energy rebate caps and funding change, so re-verify before publishing them anywhere public.
- Content lives in the `SECTIONS` and `BUILD_ORDER` arrays at the top of the second script block.

## Meta Tags
- OpenGraph/Twitter cards ready
- Keywords target Austin active listening search
- Domain-ready for listen2me.com

Built by JFeelgoodOfficial - indie dev/artist in Austin, TX.
