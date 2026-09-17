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
Standalone, private review page at `/crystal.html` (marked `noindex`) for Crystal M. Pratt's landing page. It carries the review notes into a form she can answer: the two outstanding questions, the seven changes made to her answers, four judgement calls, what the page deliberately leaves out, and ten ways to get more out of eight to ten hours a week.

- Field types are `text`, `textarea`, `select`, `radio` (single choice) and `checks` (multi-select). Long-form questions carry **starter chips** that drop suggested wording into the box; clicking a second chip appends rather than replaces.
- Answers autosave to the browser's `localStorage` under the key `crystal-page-review-v1`. Nothing leaves the browser.
- **Export Markdown** downloads `crystal-page-review-YYYY-MM-DD.md` with every question and answer; unanswered ones are marked `_No answer yet_`. A copy-to-clipboard button covers browsers that block downloads.
- Under the export button, a **"Have you thought of trying:"** block holds three self-employment spin-offs from the `SPINOFFS` array. Each shows a one-sentence pitch and expands on click to a five step plan plus a "before you start" caveat and a note field. Open/closed state persists alongside the answers.
- Content lives in the `SECTIONS` array near the top of the script. Blocks are `note` (context callout), `field` (a question) or `idea` (a suggestion card, which generates its own interest radio and note field).

## Meta Tags
- OpenGraph/Twitter cards ready
- Keywords target Austin active listening search
- Domain-ready for listen2me.com

Built by JFeelgoodOfficial - indie dev/artist in Austin, TX.
