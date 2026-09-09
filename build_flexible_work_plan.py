#!/usr/bin/env python3
"""
James Geddes, 2027 Flexible Work Arrangement: one-pager in the NZ Army
house style.

    python3 build_flexible_work_plan.py -> output/james-geddes-flexible-work-arrangement.pdf
"""

import datetime as dt

import pymupdf

from army_onepager import (ARMY_RED, BLACK, FAINT, GRID, INK, M, MID, MOAWHANGO, SWAMP, W, WHITE,
                           Page, letterhead, month_axis, section_heading, status_block)

OUT = "./output/james-geddes-flexible-work-arrangement.pdf"

KICKER = "2027 FLEXIBLE WORK ARRANGEMENT"
TITLE = "James Geddes"
ORIGINATOR = "Army Command School"
DATE = "September 2026"
FOOTER_LEFT = "James Geddes | 2027 Flexible Work Arrangement"

CONTEXT = [
    "Family relocating to Auckland for his wife's employment, commencing February 2027.",
    "James remains in Christchurch in early 2027 to prepare the family home for sale and cover",
    "the first NZALC course round under his normal contract.",
]

D = dt.date
SPAN = (D(2026, 9, 1), D(2027, 12, 31))
TODAY = D(2026, 9, 10)
PERIODS = [
    (SPAN[0], D(2027, 2, 28), "NORMAL WORKING ARRANGEMENT", "Christchurch  ·  includes the January to February NZALC course round", MOAWHANGO, SWAMP),
    (D(2027, 3, 1), SPAN[1], "FLEXIBLE WORK ARRANGEMENT", "Auckland-based  ·  March to December 2027  ·  no extension beyond December 2027", SWAMP, WHITE),
]
REVIEWS = [(D(2027, 6, 15), "3-MONTH REVIEW  ·  JUNE"), (D(2027, 9, 15), "6-MONTH REVIEW  ·  SEPTEMBER")]
END_LABEL = "ARRANGEMENT ENDS DEC 2027"

PARAMETERS = [
    ("JAN TO FEB 2027", "Normal contract", "Christchurch-based; covers the first NZALC course round."),
    ("FROM MAR 2027", "Flexible location", "Works from Auckland; the employment arrangement otherwise continues."),
    ("JUNE 2027", "3-month review", "Formal check of operational workability."),
    ("SEPTEMBER 2027", "6-month review", "Second formal check of operational workability."),
    ("DECEMBER 2027", "End point", "The arrangement is temporary and will not extend beyond December 2027."),
]


def timeline(pg, y, h):
    x0, x1 = M, W - M
    total = (SPAN[1] - SPAN[0]).days

    def xof(d):
        return x0 + (d - SPAN[0]).days / total * (x1 - x0)

    month_axis(pg, y, h, SPAN, xof)
    bar_y, bar_h = y + 58, 40
    for start, end, label, detail, fill, col in PERIODS:
        sx, ex = xof(start), xof(end + dt.timedelta(days=1))
        pg.box(sx, bar_y, ex - sx, bar_h, fill=fill, stroke=WHITE, width=0.6)
        pg.spaced((sx + ex) / 2, bar_y + bar_h / 2 - 1, label, 7.5, col, bold=True, spacing=1.2, align=1)
        pg.text((sx + ex) / 2, bar_y + bar_h / 2 + 10, detail, 6.3, col, align=1)
    tx = xof(TODAY)
    pg.line(tx, y + 28, tx, y + h, ARMY_RED, width=1.2)
    pg.text(tx + 3, y + h - 3, "TODAY", 6.5, ARMY_RED, bold=True)
    for d, label in REVIEWS:
        rx = xof(d)
        pg.line(rx, y + 28, rx, y + h, BLACK, width=0.8, dashes="[3 2] 0")
        lw = pg.width(label, 6.5, True) + 10
        pg.box(rx - lw / 2, y + 36, lw, 11, fill=WHITE, stroke=None)
        pg.text(rx, y + 44, label, 6.5, BLACK, bold=True, align=1)
    ex = xof(SPAN[1] + dt.timedelta(days=1))
    pg.line(ex, y + 28, ex, y + h, SWAMP, width=1.4)
    pg.text(ex - 3, y + h - 3, END_LABEL, 6.5, SWAMP, bold=True, align=2)
    return y + h


def parameters(pg, y):
    section_heading(pg, y, "KEY PARAMETERS")
    cols = 3
    cw = (W - 2 * M) / cols
    for k, (when, what, detail) in enumerate(PARAMETERS):
        cx = M + (k % cols) * cw
        cy = y + 24 + (k // cols) * 42
        pg.spaced(cx, cy, when, 6.5, SWAMP, bold=True, spacing=1.2)
        pg.text(cx, cy + 12, what, 8.5, BLACK, bold=True)
        pg.textbox(cx, cy + 16, cw - 16, 24, detail, 7.5, INK, lh=1.25)


def build():
    doc = pymupdf.open()
    pg = Page(doc)
    y = letterhead(pg, KICKER, TITLE, ORIGINATOR, DATE, FOOTER_LEFT)
    y = status_block(pg, y, [("CONTEXT", CONTEXT)])
    y = timeline(pg, y + 16, 150)
    parameters(pg, y + 30)
    doc.set_metadata({"title": "James Geddes: 2027 Flexible Work Arrangement", "author": "Army Command School"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
