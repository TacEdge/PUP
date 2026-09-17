#!/usr/bin/env python3
"""
2nd Engineer Regiment Command Week: NZALC leadership development support,
initiating one-pager.  Drawn directly as an A4 PDF in the house style.

    python3 build_2er_command_week.py -> output/2er-command-week-nzalc-support.pdf
"""

import pymupdf

from army_onepager import ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, MID, MOAWHANGO, PALE, SWAMP, WHITE, Page, logo_png

OUT = "./output/2er-command-week-nzalc-support.pdf"
W, H = 595, 842
M = 56
CW = W - 2 * M

KICKER = "NZALC LEADERSHIP DEVELOPMENT SUPPORT  ·  INITIATING ONE-PAGER"
TITLE = "2 ER Command Off-site"
ORIGINATOR = "New Zealand Army Leadership Centre | Army Command School"
DATE = "September 2026"
FOOTER_LEFT = "NZALC | 2 ER Command Off-site"

PURPOSE = [
    "NZALC will support the 2 ER Command Off-site by delivering a two-phase leadership development package "
    "for up to 18 personnel.",
    "The package is designed to build individual self-awareness before shifting the focus to team effectiveness "
    "and collective performance.",
]
PROGRAMME = [
    ("MON 16 NOV", "1200 – 1700", "Leadership Personality Report",
     "Facilitated exploration of individual leadership preferences, strengths, potential limitations and impact on others."),
    ("TUE 17 NOV", "0800 – 1200", "ROCKET Model",
     "Facilitated team development session focused on the conditions required for effective team performance."),
    ("TUE 17 NOV", "1200 – 1400", "Protected white space",
     "Available if required to continue productive discussion, consolidate learning or explore issues arising during the session."),
]
PROGRAMME_NOTE = ("NZALC's contribution will conclude no later than 1400 Tuesday. The remainder of the week will "
                  "continue under 2 ER's command arrangements.")
DELIVERY = [
    ("DELIVERED BY", "Leadership Development Wing, NZALC"),
    ("PARTICIPANTS", "Up to 18 personnel"),
    ("LOCATION", "Off-site venue in the Palmerston North area; exact location to be confirmed"),
    ("REQUIREMENT", "Each participant will complete a Leadership Personality Report before the facilitated session"),
]
COORD_LEAD = "2 ER and NZALC are to confirm:"
COORD = [
    "final participant numbers and nominal roll;",
    "off-site venue and available training facilities;",
    "arrangements and timelines for completing the Leadership Personality Reports; and",
    "any specific command outcomes or team issues that should inform the facilitation.",
]


def wrapped(pg, text, size, avail, bold=False):
    words, lines, cur, cur_w = text.split(), [], [], 0
    for w in words:
        ww = pg.width(w + " ", size, bold)
        if cur and cur_w + ww > avail:
            lines.append(" ".join(cur))
            cur, cur_w = [w], ww
        else:
            cur.append(w)
            cur_w += ww
    if cur:
        lines.append(" ".join(cur))
    return lines


def para(pg, x, y, text, size, avail, color=INK, bold=False, lh=None):
    lh = lh or size * 1.32
    for line in wrapped(pg, text, size, avail, bold):
        pg.text(x, y, line, size, color, bold=bold)
        y += lh
    return y


def heading(pg, y, text):
    pg.text(M, y, text, 12, BLACK, bold=True)
    return y + 16


def build():
    doc = pymupdf.open()
    pg = Page(doc, W, H)
    pg.text(W / 2, 28, "UNCLASSIFIED", 9, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 34, "UNCLASSIFIED", 9, BLACK, bold=True, align=1)
    pg.text(M, H - 20, FOOTER_LEFT, 8, BLACK)
    pg.text(W / 2, H - 20, "ACS 2026", 8, BLACK, align=1)
    pg.text(W - M, H - 20, "Page 1 of 1", 8, BLACK, align=2)
    png, (iw, ih) = logo_png()
    lh = 26
    pg.p.insert_image(pymupdf.Rect(M, 56, M + lh * iw / ih, 56 + lh), stream=png)
    pg.text(M, 134, TITLE, 22, BLACK, bold=True)
    pg.line(M, 144, W - M, 144, ARMY_RED, width=2)
    pg.text(M, 160, ORIGINATOR, 9, SWAMP)
    x = M
    for s, bold in (("Date: ", True), (DATE, False)):
        pg.text(x, 174, s, 8, BLACK, bold=bold)
        x += pg.width(s, 8, bold)

    # purpose
    y = heading(pg, 206, "Purpose")
    y += 6
    for p in PURPOSE:
        y = para(pg, M, y, p, 10, CW) + 6
    y += 2

    # programme: three timed cards with a black time block
    y = heading(pg, y, "Programme")
    y += 4
    spine = 92
    r = 6
    for day, time, activity, focus in PROGRAMME:
        lines = wrapped(pg, focus, 9.2, CW - spine - 28)
        h = max(52, 30 + len(lines) * 12 + 10)
        pg.box(M, y, CW, h, fill=FAINT, stroke=None, radius=r)
        pg.box(M, y, spine + r, h, fill=BLACK, stroke=None, radius=r)
        pg.box(M + spine, y, r + 1, h, fill=FAINT, stroke=None)
        pg.spaced(M + 12, y + 20, day, 6.4, GOLD, bold=True, spacing=1.4)
        pg.text(M + 12, y + 36, time, 10, WHITE, bold=True)
        tx = M + spine + 14
        pg.text(tx, y + 20, activity, 10.5, BLACK, bold=True)
        ty = y + 35
        for line in lines:
            pg.text(tx, ty, line, 9.2, INK)
            ty += 12
        y += h + 7
    y += 9
    y = para(pg, M, y, PROGRAMME_NOTE, 9.2, CW, color=SWAMP) + 12

    # delivery: two-column field grid
    y = heading(pg, y, "Delivery")
    y += 8
    col_w = CW / 2
    row_y = y
    max_end = y
    for i, (label, value) in enumerate(DELIVERY):
        cx = M + (i % 2) * col_w
        if i % 2 == 0 and i:
            row_y = max_end + 10
        pg.spaced(cx, row_y, label, 6.4, SWAMP, bold=True, spacing=1.4)
        end = para(pg, cx, row_y + 14, value, 9.6, col_w - 18, lh=12.5)
        max_end = max(max_end, end)
    y = max_end + 18

    # coordination required
    y = heading(pg, y, "Coordination Required")
    y += 6
    y = para(pg, M, y, COORD_LEAD, 10, CW) + 2
    for item in COORD:
        pg.text(M + 4, y, "•", 10, SWAMP, bold=True)
        y = para(pg, M + 18, y, item, 10, CW - 18)
        y += 2
    print(f"content ends at y={y:.0f}")

    doc.set_metadata({"title": "2 ER Command Off-site: NZALC Leadership Development Support",
                      "author": "New Zealand Army Leadership Centre"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
