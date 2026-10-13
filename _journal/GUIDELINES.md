# Journal guidelines

Every Jlisten2me journal article follows this document. Read it before writing one, and run
the checklist at the bottom before publishing.

## What the journal is for

Each article describes one hard situation from the inside, the way it feels to the person
carrying it, and then says plainly what an hour of being listened to is and isn't. A reader
should finish thinking "that's my week," and know that a phone hour is $60 and can be booked
under a first name.

Search brings most readers here. They type their situation in their own words, like "who do
I talk to before layoffs" or "can't tell my wife about money worries." The title and the
first paragraph should sound like what they typed.

## What an article is

- One situation per article. "Carrying a decision you can't share yet" is one. "Stress at
  work" is a category, and too broad.
- Written by JFeelgood, in the first person, to one reader addressed as "you."
- About the situation in general. The reader supplies the details from their own life.
- Between 700 and 1,100 words.
- Honest about the limits. Every article says what the hour won't do and names who to see
  instead when that's what the reader needs.

## What an article is not

- **A client story.** No article is drawn from a session. There are no characters, no "a
  founder I spoke with," no composite cases, no "someone once told me." The home page
  promises nothing is used as an example, and invented examples look the same as real ones
  to a reader.
- **Advice.** No numbered steps, no frameworks, no "five ways to cope." The service is
  listening, so the articles don't tell people what to do with their lives.
- **Therapy or health content.** No diagnoses, no clinical terms used as labels (depression,
  anxiety disorder, trauma, burnout as a condition), no claims that a session treats,
  heals, or fixes anything.
- **An outcome promise.** Describe what happens in the hour. Don't promise what happens
  after it. "You'll hear yourself say it in order" is fine. "You'll leave with clarity" is a
  promise you can't keep.
- **Research dressed up.** No "studies show" or "experts agree." If a number or a finding
  matters, name the source and link it. Otherwise leave it out.
- **News or a dated post.** No "this week," no references to current events. Articles
  should read the same in three years.
- **A sales page.** One booking mention, at the end, in plain words. No urgency, no
  discounts, no "spots are filling up."

## Hard rules on writing

These are absolute. An article that breaks one of them doesn't get published until it's
fixed.

### No em dashes

Don't use the em dash (—), the en dash used as a dash ( – ), or a double hyphen (--) as
punctuation. Use a period, a comma, a colon, or rewrite the sentence.

| Instead of | Write |
| --- | --- |
| You know the number — nobody else does. | You know the number. Nobody else does. |
| Three people – your cofounder, your board, your spouse – all have a stake. | Your cofounder, your board, and your spouse all have a stake. |

En dashes inside number ranges (9–5) are fine, though a plain hyphen or "to" is simpler.

### No antitheticals

An antithetical sets up a claim only to knock it down: "It's not X, it's Y." "Not X, but Y."
"X isn't the problem. Y is." "This isn't about A. It's about B." "Not because X. Because Y."
They sound like ad copy, and readers recognise them. State the thing that's true and stop.

| Instead of | Write |
| --- | --- |
| It's not weakness, it's being human. | Anyone carrying this alone gets tired. |
| This isn't therapy. It's an hour of being heard. | An hour of being heard, by someone with no stake in it. |
| Not because they don't care. Because it lands somewhere. | They care, and that's why it lands somewhere. |
| The problem isn't the decision. It's that you're making it alone. | Making it alone is the hard part. |

Plain negatives are fine when they carry information on their own: "I don't take notes."
"Nothing is recorded." "I won't tell you what to do." What's banned is a negative used to set
up a contrast.

### Other writing rules

- No bullet lists in the body. Prose only. Subheadings are allowed, two to four per article.
- Short paragraphs. Each sentence of the opening paragraph may sit on its own line, matching
  the home page intros.
- Contractions are fine, and preferred.
- American spelling.
- No filler words: "navigate," "journey," "landscape," "unpack," "holistic," "self-care,"
  "space" meaning a feeling ("hold space," "safe space"), "it's important to," "at the end
  of the day," "you've got this."
- No rhetorical question as the opening line.
- No closing summary. End on the booking line.

## Structure

1. **Title.** What the reader would type or say. Lowercase after the first word except names.
   Example: "When you have to decide and can't tell anyone yet."
2. **Opening.** Two to five short lines putting the reader inside the situation. Concrete
   detail: the spreadsheet, the Monday meeting, the kitchen table at 2 a.m.
3. **Why the usual people can't take it.** Go through who the reader would normally talk to
   and why each one has a stake. This section is the reason the service exists, so it gets
   the most room.
4. **What saying it out loud does.** Describe the experience of putting it into words for
   another person. Stay with what happens in the room.
5. **What the hour looks like.** Phone or in person, no notes, no advice unless asked, first
   name is fine, hype or vent.
6. **What it won't do.** Name the limit for this specific situation and who to see instead:
   an employment lawyer, a financial advisor, a licensed therapist, a doctor. Always
   include: "If you're in crisis, call or text 988 in the US."
7. **Booking line.** One or two sentences with the price and a link to the booking section.

## Files, metadata, and the release schedule

Each article is one Markdown file in `_journal/articles/`, named after its slug:
`_journal/articles/decision-you-cant-share.md`. The file starts with front matter:

```
---
title: When you have to decide and can't tell anyone yet
slug: decision-you-cant-share
description: One sentence under 155 characters, in the reader's words.
date: 2026-10-13
---
```

- `slug`: lowercase words joined by hyphens, no dates. Must match the file name.
- `date`: the Tuesday the article goes live. Give each new article the Tuesday after the
  last one scheduled. Nothing appears on the site before its date.
- `updated`: optional. Add it with the date of any real revision after publishing.
- Body: `## ` for subheadings, a blank line between paragraphs. Lines in the same paragraph
  without a blank line between them show one sentence per line, which is how the opening is
  written. Links are `[text](/#book)`.

`python3 _tools/build_journal.py --check` checks every article against the hard rules in
this document and lists anything to fix. The build refuses to
publish an article that fails.

A GitHub Action runs the build every Tuesday at about 6 a.m. Central. It publishes
whatever is due and regenerates the journal index, the article pages, the RSS feed,
`sitemap.xml`, `llms.txt`, `llms-full.txt`, and the "From the journal" block on the home
page. The page title, canonical URL, Open Graph tags, and the `BlogPosting` and breadcrumb
structured data all come from the front matter, so there's nothing to add by hand.

To preview a future week locally: `python3 _tools/build_journal.py --today 2026-12-01`,
then put things back with a plain `python3 _tools/build_journal.py`.

## Topics

Start from the "Who it's for" cards on the home page. Each card can carry one article.

| Card | Working title |
| --- | --- |
| The call stops with you | When you have to decide and can't tell anyone yet |
| You don't want to hand it to your spouse | When you don't want your worry to become theirs |
| You're in the middle of a divorce | When everyone in your life has picked a side |
| Everything is changing at once | When everything changes in the same month |
| Tomorrow is the big one | When you need to say it out loud before you say it for real |
| Hype or vent | When you just need an hour to swear about it |

New topics beyond these are fine if they pass the "what it is not" section above.

## Before publishing

- [ ] `python3 _tools/build_journal.py --check` reports the article clean.
- [ ] Search the file for `—`, ` – `, and `--`. Zero results.
- [ ] Search for `not `, `isn't`, `n't just`, `but rather`. Read each hit and confirm none
      sets up a contrast.
- [ ] No characters, cases, or "someone I spoke with."
- [ ] No numbered advice, no clinical labels, no outcome promises.
- [ ] Every number or finding has a named, linked source, or it's gone.
- [ ] The limits section names who to see instead, and 988 appears.
- [ ] One booking mention, at the end.
- [ ] 700 to 1,100 words.
- [ ] Read it aloud once. Anything you wouldn't say across a table gets cut.
