# Jlisten2me - Confidential Listening Sessions

Single-page landing site for jlisten2me.com. A private hour with someone who has no stake in the
outcome: for leaders carrying a decision alone, people mid-divorce or mid-upheaval, anyone
prepping for the moment that matters, and anyone who just needs to vent or be hyped up.
Confidential: nothing recorded, no notes kept, nothing repeated.

## Pricing
- **By phone**: $60/hr
- **In person**: $100/hr (Austin, public location)
- **Five-hour bundle**: $45/hr, $225 prepaid (phone hours; swap one for in person by paying the difference)

## Features
- Pure HTML/CSS/JS in one file, no frameworks, no build step
- **Palette picker** in the header ("What color are you feeling today?") with six palettes
  (Tide, Moss, Ember, Plum, Clay, Ink) plus a **light/dark toggle**. Both persist in
  `localStorage` (`j2m-palette`, `j2m-theme`) and dark/light defaults to the OS preference
  on a first visit. `<meta name="theme-color">` follows the selection.
- **Cal.com** inline embed for scheduling, themed to match the current light/dark mode,
  with a fallback panel if the embed is blocked. It doesn't download until the booking
  section is near the viewport or a "Book" link is clicked; it's the heaviest thing on the
  page and most visits never reach it.
- **Stripe**: payment at booking through Cal.com's Stripe app for the hourly rates, and a
  Stripe Payment Link for the bundle
- **Inter self-hosted** from `fonts/` (variable, latin, 48 KB, SIL OFL) with `preload` and
  `font-display: swap`. No Google Fonts request, no third-party origin before first paint.
- **Structured data**: one JSON-LD block with `ProfessionalService`, three `Offer`s,
  `Person`, and `FAQPage` mirroring the eight on-page questions
- `og.png` (1200×630) for link previews, `robots.txt`, `sitemap.xml`, `llms.txt`, and an
  inline SVG favicon
- Every palette's caption colour (`--text-3`) clears WCAG AA 4.5:1 in both light and dark
- Mobile-responsive, `prefers-reduced-motion` respected
- GitHub Pages / Vercel deploy-ready

## Deploy
1. Drop `index.html` in repo root
2. GitHub Pages: Settings → Pages → Source: Deploy from branch `main`
3. Vercel: Connect GitHub repo, deploy instantly

## Going live

Full step-by-step setup (Stripe, Cal.com, domain, and an end-to-end test
checklist) lives in [SETUP.md](SETUP.md). The short version of the code side:

### The CONFIG block

Everything you need to edit sits in one object near the top of the `<script>` in `index.html`:

```js
const CONFIG = {
  calOrigin: "https://app.cal.com",
  calLink: "jfeelgood/listening-hour",   // your cal.com event path
  checkout: {
    phone:    null,   // "https://buy.stripe.com/..."
    inperson: null,
    bundle:   null
  }
};
```

**Cal.com** — create an event type (60 min) at cal.com, then set `calLink` to the
`username/event-slug` from its public URL. Add a required booking question for
"Phone or in person?" and another for "Hyped up or venting?" so the answers arrive
with the booking. If you self-host Cal, change `calOrigin` too.

**Stripe** — the recommended setup is Cal.com's Stripe app, which takes payment at the
moment of booking, so `phone` and `inperson` stay `null` and those buttons route to the
calendar. The five-hour bundle has no booking to attach to, so it needs its own Stripe
Payment Link (Dashboard → Payment Links → Create) pasted into `bundle`. Any entry left as
`null` makes that button scroll to the calendar instead of dead-ending, so the page stays
usable at every stage of setup. Payment Links are hosted by Stripe, so no server and no
keys live in this repo. SETUP.md walks through both paths and why.

**Palettes** — each palette is two CSS blocks, `[data-palette="name"][data-theme="dark"]`
and `[...][data-theme="light"]`, defining the same eleven custom properties. To add one,
copy a pair, add the name to the `PALETTES` array and `THEME_COLORS` map in the script,
and add a `.swatch` button plus a `.sw-name` gradient rule. Check the new `--text-3`
against `--bg` for 4.5:1; it's the only token that runs close.

**Domain** — `canonical`, `og:url`, `og:image`, `twitter:image`, `robots.txt`, `sitemap.xml`
and the JSON-LD all assume `https://jlisten2me.com/`. Moving domains means changing all of
them; a grep for `jlisten2me.com` finds every spot.

**og.png** — regenerate by editing the template the card was rendered from (the hero
wordmark, the definition line, and the rates on a Tide-dark background) and screenshotting
it at 1200×630 with headless Chromium. It's a plain HTML page, no image editor involved.

## Copy notes
The "Who's listening" bio is the line from the original page and is the one paragraph only
Jonny can write. An HTML comment marks it. The definition sentence above it is written to be
lifted whole by search and answer engines; keep it plain and factual if it changes.

The confidentiality section states the one limit (credible threat of serious harm) and
points to 988. Keep it. An unqualified "100% confidential, no exceptions" claim is the
kind of promise that reads well and defends badly.

The site does not offer an NDA. It was on the page and came off: promising a signed mutual
PDF means building and running a signing workflow before launch, and the confidentiality
policy carries the same weight to a reader without that overhead. Signing a corporate
client's own NDA case by case is still fine. Advertising one is what requires the process.

## Meta Tags
- OpenGraph/Twitter cards with a real `og:image`
- No `meta keywords`; search engines have ignored it since 2009
- Domain-ready for jlisten2me.com

Built by JFeelgoodOfficial - indie dev/artist in Austin, TX.
