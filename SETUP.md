# Setting up Jlisten2me

Everything needed to take the landing page from a static file to taking real bookings and
real money. Budget about two hours for the first pass, most of it waiting on Stripe's
identity verification.

Work through it in order. Steps 1 through 4 can't be skipped. Step 7 (deploy) is the point
at which it's public, so do 1 through 6 first and don't rush past step 8.

A note on accuracy: the Stripe and Cal.com flows below were checked against their current
docs, but both companies move buttons around. If a label doesn't match, the concept still
holds. Search their help center for the phrase in bold and you'll land on the right page.

---

## 0. Decide how payment and booking fit together

This is the one real decision, and everything else follows from it.

**Option A, payment at booking (recommended).** Cal.com has a Stripe app. You connect
Stripe once, set a price on an event type, and the booker pays as part of picking their
time. One flow, no chance of someone booking and never paying, no reconciling two systems.

**Option B, separate payment links.** The buyer clicks a price card, pays on a Stripe-hosted
page, then separately books a slot. Two steps, two places to drop off, and you have to
check that everyone on the calendar actually paid.

Take Option A for the hourly rates. The page is already built for it: leave the `phone` and
`inperson` entries in `CONFIG.checkout` set to `null` and those buttons scroll to the
calendar, where Cal collects the money.

The five-hour bundle is different and needs Option B. A bundle isn't a booking, it's a
prepayment for five future bookings, so there's no single calendar slot to attach it to.
Step 5 covers how to handle it.

---

## 1. Stripe account

1. Sign up at **stripe.com**. Use a real business email you'll keep.
2. Complete **account activation**: legal name, address, SSN or EIN, and a bank account for
   payouts. Stripe will not release funds until this is done, and it can take a day or two
   to verify. Start this first so it's finishing in the background while you do the rest.
3. Set your **public business name** to `Jlisten2me` under Settings → Business. This is what
   shows on the customer's card statement. Getting it right matters more than usual here:
   a client going through a divorce does not want an unexplained charge on a shared card,
   and a vague descriptor invites exactly the question you don't want asked. Consider
   something deliberately bland instead, and say on the site what the charge will read as.
4. Under Settings → **Customer emails**, turn on receipts for successful payments.
5. Leave **test mode** on for now. The toggle is in the top bar. Everything below works the
   same in test mode with card number `4242 4242 4242 4242`, any future expiry, any CVC.

---

## 2. Cal.com account and three event types

1. Sign up at **cal.com**. The free plan covers everything here.
2. Pick your username carefully; it's in every booking URL you'll ever send. `jfeelgood`
   is what the code currently assumes.
3. Connect your calendar (Google, Apple, or Outlook) so Cal blocks out times you're busy.
   Skip this and you will get double-booked.
4. Set your **availability**: Availability → set real hours, including the evenings and
   weekends the site promises. The site says evenings and weekends are available, so either
   make that true or change the copy.
5. Create three event types, all 60 minutes:

   | Event type | Slug | Location | Price |
   | --- | --- | --- | --- |
   | Listening hour, phone | `phone-hour` | Attendee phone number | $60 |
   | Listening hour, in person | `in-person-hour` | Attendee address / custom text | $100 |
   | Bundle hour | `bundle-hour` | Attendee phone number | $0, hidden |

   For the in-person one, set the location to "Somewhere else" or a custom text field so you
   can agree the spot after booking, rather than publishing a fixed address.

   Mark **Bundle hour** as hidden (the toggle on the event type list). Hidden events don't
   appear on your public page but the direct link still works, which is exactly what you
   want: only people who bought the bundle get the link.

6. Add a **buffer** of 15 minutes after each event and a **minimum notice** of a few hours.
   Back-to-back emotional hours with no gap is a mistake you only make once.

---

## 3. Connect Stripe to Cal.com

Verified against Cal.com's current help docs:

1. In Cal.com, go to **Apps** in the sidebar, then **App Store**.
2. Filter to the **Payment** category, open **Stripe**, click **Install**.
3. You'll be sent to Stripe to authorize the connection. Approve it and you'll land back in
   Cal.com with Stripe listed under your connected apps.
4. Open the **Listening hour, phone** event type, go to its **Apps** tab, enable Stripe, set
   the price to **60** and the currency to **USD**, and save.
5. Do the same for **Listening hour, in person** at **100**.
6. Leave **Bundle hour** with no Stripe app enabled. It's already paid for.

Payment is taken at the moment of booking. An unpaid booking never lands on your calendar,
which is the whole point.

Two things to settle now rather than during your first awkward cancellation. Decide your
refund rule and write it into each event type's description — the site currently promises
free rescheduling up to 12 hours out, so at minimum honor that. And decide what happens on
a no-show. Cal.com supports charging a cancellation or no-show fee via Stripe if you want
it; it's optional and adds friction, so only turn it on if no-shows actually become a problem.

---

## 4. Booking questions

On each event type, open **Advanced → Booking questions** and add these. They arrive with
every booking so you walk in knowing what the hour is for.

1. "Phone or in person?" — only needed if you'd rather run one event type instead of two.
   With separate event types, skip it.
2. "Do you want to be hyped up, or do you want to vent?" — radio with a third option like
   "not sure yet", not required. The site makes a promise about this; the question is how
   you keep it.
3. "Anything you want me to know first?" — long text, optional.

Keep the required list short. Every required field costs you bookings, and someone in a bad
week has a low tolerance for forms.

---

## 5. The five-hour bundle

The bundle is a Stripe Payment Link, because there's no single booking to attach it to.

Verified against Stripe's docs: Payment Links are created in the Dashboard with no code and
no server.

1. In the Stripe Dashboard, go to **Payment Links** and click **Create**.
2. Add a new product: name it `Five listening hours`, price **$225**, one-time.
3. Under **After the payment**, choose **Confirmation page** and either write a custom
   message containing your `bundle-hour` Cal.com link, or redirect to a small thank-you page
   on your own site that carries the link. The custom message is simpler and needs no extra
   page.
4. Optionally add a **custom field** asking for the buyer's first name, so you know who the
   prepaid hours belong to.
5. Copy the resulting `https://buy.stripe.com/...` URL.

Redemption works like this: they pay once, get the hidden `bundle-hour` link, and book five
free sessions with it whenever they want. You track the count.

Five is small enough for a note in a spreadsheet or a Stripe customer note. Don't build
anything. If the bundle takes off and counting becomes a chore, that's a good problem and
you can solve it then.

One gap to be aware of: nothing stops someone from booking a sixth free hour on that link.
At this volume it's a trust problem, not an engineering one. If you'd rather close it, the
cheapest fix is to stop sharing a standing link and instead send a single-use booking link
after each session.

---

## 6. Wire up index.html

One object, near the top of the `<script>` block in `index.html`:

```js
const CONFIG = {
  calOrigin: "https://app.cal.com",
  calLink: "jfeelgood/phone-hour",   // username/event-slug from your public Cal URL
  checkout: {
    phone:    null,   // null on purpose: Cal.com takes payment at booking
    inperson: null,   // same
    bundle:   "https://buy.stripe.com/xxxxxxxxxxxx"   // from step 5
  }
};
```

`calLink` is whatever comes after `cal.com/` on your public booking URL. If your page is
`cal.com/jfeelgood/phone-hour`, the value is `jfeelgood/phone-hour`.

The embedded calendar shows one event type. Point it at the phone hour, since that's where
most people start; the in-person card's button still sends people to the calendar, and they
can switch event from inside the embed. If you'd rather each card open its own calendar,
that's a small change to the page and worth asking for.

A `null` checkout entry makes that button scroll to the calendar instead of dead-ending, so
the page works at every stage of this setup.

## 7. Deploy

The site is one HTML file, so this is the easy part. Pick one.

**GitHub Pages.** Repo → Settings → Pages → Source: Deploy from branch, `main`, root. Live
at `jfeelgoodofficial.github.io/Jlisten2me` in a minute or two. Free, no account needed
beyond GitHub.

**Vercel.** Import the GitHub repo at vercel.com, accept the defaults, deploy. Also free,
and it gives you preview URLs on every branch, which is genuinely useful when you want to
see a change before it's public.

For the custom domain `listen2me.com`: add it in whichever host you picked, then create the
DNS records that host tells you to at your registrar. Propagation is usually minutes,
occasionally hours. Both hosts issue an HTTPS certificate automatically once DNS resolves;
don't buy one.

The page's `<link rel="canonical">` and `og:url` both point at `https://listen2me.com`.
If you end up on a different domain, update those two lines or search engines will index
the wrong address.

---

## 8. Test it end to end before telling anyone

With Stripe still in **test mode**:

1. Open the live site on your phone, not just your laptop. Most of your traffic will be
   someone sitting in a car.
2. Cycle every palette and flip light/dark. Reload. The choice should survive.
3. Book a phone hour with card `4242 4242 4242 4242`. Confirm the charge appears in Stripe,
   the booking appears in Cal.com, the event lands on your real calendar, and you get the
   confirmation email.
4. Cancel that test booking and confirm the refund behaves the way you decided in step 3.
5. Click the bundle button. Confirm it opens the Stripe Payment Link and that the
   confirmation message contains the working `bundle-hour` link.
6. Book a bundle hour with that link and confirm it takes no payment.
7. Switch Stripe to **live mode**, recreate the Payment Link there (test-mode links do not
   work in live mode — this catches people out), paste the new URL into `CONFIG`, and run
   one real booking with your own card. Refund yourself afterward.

Step 7 is not optional. A test-mode Payment Link left in production is the single most
common way this goes wrong.

---

## 9. Still open

Things the site currently asserts that only you can make true:

- Evenings and weekends really being on the calendar.
- The bundle's "swap an hour for in person by paying the difference" — decide how you
  collect that $55. Simplest is a one-off Stripe invoice.
- The testimonials section is gone. Ask your first few clients, in writing, whether you may
  quote them anonymously, and only use what you're given. Given what the service is, expect
  most to say no, and treat that as normal rather than a problem.
- The page claims Austin and surrounding area for in-person. Decide how far that goes and
  whether travel time is billed.
- The site no longer offers an NDA. If a corporate client asks for one anyway, you can
  still sign theirs case by case — just don't advertise it until signing one is a routine
  you actually have.
