# NZALC 360 Feedback Tool — prototype

A working prototype of a lightweight 360-degree leadership feedback tool for
the NZ Army Leadership Centre. Static, no build step, synthetic data only.

## Run it

Serve the repository root with any static server and open `/360/`:

```
cd PUP
python3 -m http.server 8000
# then open http://localhost:8000/360/
```

Opening `360/index.html` directly from disk will not work, because the app
uses ES modules. On GitHub Pages the app lives at `<site>/360/`.

## Demonstrating it

The dark bar at the foot of every screen is the development-only role
switcher. Use it to move between:

- **NZALC staff** — Active 360s, one 360's detail, report preview.
- **Participant** — My 360 for any seeded participant; Hana Rewiti's 360 is
  closed so her report is visible.
- **Rater** — any rater link. Outstanding links for Alex Morgan are
  `#/r/alx-peer-4` and `#/r/alx-sub-4`.

"Reset" restores the seed data. State persists in the browser's localStorage.

## Where things are

| Path | What |
|---|---|
| `DESIGN.md` | Information architecture, journeys, interaction model, privacy rules |
| `src/data/instrument.js` | The placeholder instrument: dimensions, statements, scale, prompts, privacy thresholds |
| `src/data/seed.js` | Synthetic courses, participants, raters, responses |
| `src/lib/store.js` | Persistence and mutations |
| `src/lib/report.js` | Aggregation, group-size rules, strengths/gaps logic |
| `src/views/*.js` | Rater, participant, staff and report screens |
| `styles.css` | The whole visual system |

## Testing

An end-to-end Playwright script was used during development to exercise all
three journeys at phone and desktop widths and check for runtime errors. It is
not committed; the app has no test dependencies.
