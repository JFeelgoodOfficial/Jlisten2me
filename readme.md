# Jlisten2me - Confidential Listening Sessions

Single-page landing site for listen2me.com. A private hour with someone who has no stake in the
outcome: for leaders carrying a decision alone, people mid-divorce or mid-upheaval, anyone
prepping for the moment that matters, and anyone who just needs to vent or be hyped up.
Confidential, mutual NDA available at no charge.

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
  with a fallback panel if the embed is blocked
- **Stripe Payment Links** on each pricing card
- Mobile-responsive, `prefers-reduced-motion` respected, SEO/OG meta updated
- GitHub Pages / Vercel deploy-ready

## Deploy
1. Drop `index.html` in repo root
2. GitHub Pages: Settings → Pages → Source: Deploy from branch `main`
3. Vercel: Connect GitHub repo, deploy instantly

## Going live

Full step-by-step setup (Stripe, Cal.com, the NDA, domain, and an end-to-end test
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
"Phone or in person?" and another for "Do you want the NDA signed first?" so the
answers arrive with the booking. If you self-host Cal, change `calOrigin` too.

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
and add a `.swatch` button plus a `.sw-name` gradient rule.

## Copy notes
The confidentiality section states the one limit on confidentiality (credible threat of
serious harm) and points to 988. Keep it. An unqualified "100% confidential, no exceptions"
claim next to an NDA offer is the kind of promise that reads well and defends badly.

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
Standalone, private page at `/wiredwright.html` (marked `noindex`) for Wired Wright, an electrical contractor covering greater Austin. It is a content-intake tool, not the public landing page: he answers it once, exports the brief, and Jonny builds the site from that.

- Typeface is Source Sans 3 at 17px, chosen for reading comfort over Inter's tighter grotesque.
- **Hero**: a three.js particle plug (body, three prongs, curving cord) that morphs into the words WIRED WRIGHT on a loop. Falls back to plain styled type if WebGL or the CDN fails, and holds the text still under `prefers-reduced-motion`.
- **28 questions** in seven parts, ordered the way a visitor reads a landing page: first screen, trust strip, services, proof, price and form, FAQ, footer and local search. Each question carries the research note behind it (license-badge lift, four-field forms, Austin Energy EV rebate rules, TECL placement).
- Each question has **tap-to-load recommended answers** that drop into the composer for editing, a **chat box** that saves answers as a thread, and per-answer edit and delete.
- Everything autosaves to `localStorage` under `wiredwright-content-v1`. Nothing leaves the browser.
- **Download Markdown** writes `wiredwright-content-YYYY-MM-DD.md` with every answer, the research note per question, a build order for the page, the still-open questions, and the source list. Copy-to-clipboard and a live preview sit beside it.
- Beneath the export buttons sits a **research panel**: eleven findings as stat cards (conversion lift, license-badge specificity, mobile share, form abandonment, the Austin Energy rebate, review volume) with the source named on each.
- Conversion figures come from marketing-agency and vendor blogs, not audited research, and the page says so. Austin Energy rebate caps and funding change, so re-verify before publishing them anywhere public.
- Content lives in the `SECTIONS` and `BUILD_ORDER` arrays at the top of the second script block.

## Meta Tags
- OpenGraph/Twitter cards ready
- Keywords target Austin active listening search
- Domain-ready for listen2me.com

Built by JFeelgoodOfficial - indie dev/artist in Austin, TX.
