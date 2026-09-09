#!/usr/bin/env python3
"""
Maternity leave plan one-pager in the NZ Army house style: letterhead,
status block, leave timeline and leave sequence.

    python3 build_maternity_leave_plan.py -> output/kate-beckett-maternity-leave-plan.pdf
"""

import datetime as dt

import pymupdf

from army_onepager import (ARMY_RED, BLACK, GOLD, GRID, INK, M, MID, MOAWHANGO, PALE, SWAMP, W, WHITE, FAINT,
                           Page, letterhead, month_axis, section_heading, status_block)

OUT = "./output/kate-beckett-maternity-leave-plan.pdf"

KICKER = "MATERNITY LEAVE PLAN"
TITLE = "Mrs Kate Beckett"
SUBTITLE = "Status as at 10 September 2026   ·   Planned return to work: 28 January 2028"
ORIGINATOR = "Army Command School"
DATE = "September 2026"
FOOTER_LEFT = "Kate Beckett | Maternity Leave Plan"
FOOTER_REF = "ACS 2026"
MARKING = "UNCLASSIFIED"

STATUS = [
    ("CURRENT STATUS", "Working as normal. Leave commences 21 December 2026."),
    ("RETURN", "28 January 2028. FTE to be confirmed in late November 2027."),
    ("COURSE DELIVERY", "Covered by Preferred Contractors throughout the absence."),
]
COVER_LABEL = "Course delivery covered by Preferred Contractors"

D = dt.date
SPAN = (D(2026, 9, 1), D(2028, 1, 31))
TODAY = D(2026, 9, 10)
CONFIRM_FTE = (D(2027, 11, 20), "Late Nov 2027: confirm FTE")
RETURN = (D(2028, 1, 28), "RETURN 28 JAN 2028")

# (start, end inclusive, label, short label for the bar, colour key)
LEAVE = [
    (D(2026, 12, 21), D(2027, 1, 11), "Christmas leave (Annual leave)", "Christmas leave", "pale"),
    (D(2027, 1, 12), D(2027, 1, 12), "Equivalent leave", "", "grid"),
    (D(2027, 1, 13), D(2027, 1, 29), "Stand-down leave", "Stand-down", "grid"),
    (D(2027, 1, 30), D(2027, 2, 18), "Special parental leave", "Special parental", "gold"),
    (D(2027, 2, 19), D(2027, 4, 12), "Annual leave", "Annual leave", "moawhango"),
    (D(2027, 4, 13), D(2028, 1, 27), "Parental leave", "Parental leave", "swamp"),
]

COLOURS = {"pale": (PALE, SWAMP), "grid": (GRID, INK), "gold": (GOLD, WHITE),
           "moawhango": (MOAWHANGO, SWAMP), "swamp": (SWAMP, WHITE)}


def timeline(pg, y, h):
    x0, x1 = M, W - M
    total = (SPAN[1] - SPAN[0]).days

    def xof(d):
        return x0 + (d - SPAN[0]).days / total * (x1 - x0)

    month_axis(pg, y, h, SPAN, xof)
    bar_y, bar_h = y + 50, 34
    # working period before leave, as a faint bar
    pg.box(x0, bar_y, xof(LEAVE[0][0]) - x0, bar_h, fill=FAINT, stroke=None)
    pg.text((x0 + xof(LEAVE[0][0])) / 2, bar_y + bar_h / 2 + 3, "Working as normal", 7, MID, align=1)
    # leave segments; short ones get a staggered callout beneath the bar
    callout = 0
    for start, end, label, short, key in LEAVE:
        fill, col = COLOURS[key]
        sx, ex = xof(start), xof(end + dt.timedelta(days=1))
        pg.box(sx, bar_y, ex - sx, bar_h, fill=fill, stroke=WHITE, width=0.6)
        if not short:
            continue
        wide = ex - sx
        if wide > 60:
            pg.text((sx + ex) / 2, bar_y + bar_h / 2 - 1, short, 7.5, col, bold=True, align=1)
            pg.text((sx + ex) / 2, bar_y + bar_h / 2 + 9, f"{start:%-d %b} to {end:%-d %b %Y}", 6, col, align=1)
        else:
            cx = sx + wide / 2
            ly = bar_y + bar_h + 14 + callout * 13
            pg.line(cx, bar_y + bar_h, cx, ly - 2, MID, width=0.6)
            pg.line(cx, ly - 2, cx + 6, ly - 2, MID, width=0.6)
            pg.text(cx + 9, ly, f"{short}   {start:%-d %b} to {end:%-d %b %Y}", 6.5, INK)
            callout += 1
    # cover band across the absence
    csx, cex = xof(LEAVE[0][0]), xof(LEAVE[-1][1] + dt.timedelta(days=1))
    cy = bar_y - 14
    pg.box(csx, cy, cex - csx, 10, fill=WHITE, stroke=SWAMP, width=0.7, radius=2)
    pg.text((csx + cex) / 2, cy + 7.3, COVER_LABEL.upper(), 5.6, SWAMP, bold=True, align=1)
    # markers
    tx = xof(TODAY)
    pg.line(tx, y + 28, tx, y + h, ARMY_RED, width=1.2)
    pg.text(tx + 3, y + h - 3, "TODAY", 6.5, ARMY_RED, bold=True)
    cx = xof(CONFIRM_FTE[0])
    pg.line(cx, y + 28, cx, y + h, BLACK, width=0.8, dashes="[3 2] 0")
    pg.text(cx - 3, bar_y + bar_h + 14, CONFIRM_FTE[1], 6.5, BLACK, bold=True, align=2)
    rx = xof(RETURN[0])
    pg.line(rx, y + 28, rx, y + h, SWAMP, width=1.4)
    pg.text(rx - 3, y + h - 3, RETURN[1], 6.5, SWAMP, bold=True, align=2)
    return y + h


def sequence(pg, y):
    section_heading(pg, y, "LEAVE SEQUENCE")
    cols = 3
    cw = (W - 2 * M) / cols
    for k, (start, end, label, short, key) in enumerate(LEAVE):
        cx = M + (k % cols) * cw
        cy = y + 22 + (k // cols) * 30
        fill, col = COLOURS[key]
        pg.box(cx, cy - 8, 8, 8, fill=fill, stroke=None, radius=2)
        dates = f"{start:%-d %b %y}" if start == end else f"{start:%-d %b %y} to {end:%-d %b %y}"
        pg.text(cx + 14, cy, dates, 8, BLACK, bold=True)
        pg.text(cx + 14, cy + 11, label, 8, INK)


def build():
    doc = pymupdf.open()
    pg = Page(doc)
    y = letterhead(pg, KICKER, TITLE, ORIGINATOR, DATE, FOOTER_LEFT)
    y = status_block(pg, y, STATUS)
    y = timeline(pg, y + 16, 156)
    sequence(pg, y + 34)
    doc.set_metadata({"title": "Kate Beckett: Maternity Leave Plan", "author": "Army Command School"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
