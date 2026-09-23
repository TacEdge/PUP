# NZALC 360 Feedback Tool — prototype design note

Prototype only. Synthetic data. No Defence accreditation is implied.

## Information architecture

Three role surfaces, one hash-routed static app (`360/index.html`):

| Route | Role | Purpose |
|---|---|---|
| `#/r/<token>` | Rater | Landing → statements → three short prompts → submit → done |
| `#/me` | Participant | My 360: purpose, progress by rater group, nominate raters, self-assessment, report when released |
| `#/admin` | NZALC staff | Active 360s list |
| `#/admin/a/<id>` | NZALC staff | One 360: completion by group, raters, reminders, close, preview report |
| `#/report/<id>` | Participant / staff | The feedback report |

A development-only "View as" bar at the foot of every screen switches role and
resets the demo data. There is no authentication.

## Core journeys

1. **Staff** creates a 360 for a participant on a course, sets a close date,
   adds raters by relationship. Each rater gets a link (email simulated).
2. **Participant** sees purpose, progress and close date, can nominate further
   raters, completes a short self-assessment on the same instrument.
3. **Rater** opens the link, sees who / why / how long, rates 15 statements one
   at a time, answers two or three short prompts, submits. About four minutes.
4. **Staff** monitors completion, sends reminders, closes the 360.
5. **Participant** receives the report: at a glance, dimensions, strengths,
   development opportunities, perception gaps, written feedback.

## Feedback interaction model

- One statement per screen. Dimension shown as an eyebrow, statement as the
  headline. Four large targets (Rarely, Sometimes, Usually, Consistently) plus a
  quieter "Not observed". Keys 1–4 and N on desktop.
- Selecting auto-advances after a short pause; Back always available; progress
  bar and "n of 15" text.
- Three prompts at the end: Keep doing / More effective if / Anything else
  (optional). Short answers explicitly welcomed.
- Submit screen restates confidentiality and how the feedback is used.

## Instrument (placeholder content)

Four dimensions, 15 statements, in `src/data/instrument.js`. This is
provisional developmental content, not NZ Army doctrine. The app reads the
instrument as data so an approved NZALC framework can replace it without UI
changes. Scale: Rarely (1) – Sometimes (2) – Usually (3) – Consistently (4),
Not observed excluded from averages.

## Privacy rules (in `src/lib/report.js`)

- Individual rater responses are never rendered anywhere in the participant UI.
- Peer, Subordinate and Other groups are reported only when at least three
  responses exist; smaller groups fold into "Other raters" or are withheld.
- Superior feedback is reported as a group of any size; raters in that group
  are told this before they begin.
- Written comments are pooled and shuffled without relationship labels.
- Participants see group completion counts, never per-person completion.

## Visual direction

Published NZ Army palette as used elsewhere in this repository: Army Red
(#D31145) as a sparing marker, the four Army greens, ink on white for text.
Neue Haas Grotesk with Helvetica/Arial fallback. Whitespace and type carry the
hierarchy; boxes and borders are rare. Red never exceeds a few per cent of any
screen. Rater screens are mobile-first; staff and participant screens are
desktop-first and responsive.

## Assumptions

- A rater link is a capability: whoever holds it can respond once.
- Staff and participant identity is simulated; the participant view is Capt
  Alex Morgan unless another participant is chosen from the View-as bar.
- Reminders and invitations are logged, not sent.
- Persistence is browser localStorage; "Reset demo data" restores the seed.
