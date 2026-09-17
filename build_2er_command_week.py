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
KICKER = "NZALC LEADERSHIP DEVELOPMENT SUPPORT TO 2 ER"
TITLE = "Te Whi\u0101 Command Week 2026"
ORIGINATOR = "New Zealand Army Leadership Centre | Army Command School"
DATE = "September 2026"
FOOTER_LEFT = "NZALC | Te Whi\u0101 Command Week 2026"

PURPOSE = "To outline NZALC's contribution to Te Whi\u0101 Command Week 2026."
CONTEXT = ("2 ER intends to bring its new and future command teams together in a relaxed environment away from normal "
           "unit routines. The emphasis is on connection and reflection: building self-awareness, examining individual "
           "leadership styles and personality preferences, and strengthening key command relationships.")
PROGRAMME_LEAD = "NZALC will support this through two linked phases."
PROGRAMME = [
    ("MON 16 NOV", "1200 \u2013 1700", "Leadership Personality Report",
     "Facilitated exploration of individual leadership preferences, strengths, potential limitations and impact on "
     "others, including the implications for command relationships."),
    ("TUE 17 NOV", "0800 \u2013 1200", "ROCKET Model",
     "Facilitated application of the ROCKET Model to establish the conditions required for effective command teams."),
]
FLEX_NOTE = ("The period 1200 to 1400 Tuesday will be retained as flexibility to continue productive discussion or "
             "consolidate learning if required.")
PROGRAMME_NOTE = ("NZALC support will conclude no later than 1400 Tuesday 17 November. The remainder of Command Week "
                  "will continue under 2 ER command arrangements.")
DELIVERY = [
    ("DELIVERED BY", "Leadership Development Wing, NZALC"),
    ("PARTICIPANTS", "Up to 17 personnel drawn from 2 ER unit and sub-unit command teams and relevant principal staff."),
    ("LOCATION", "Off-site venue in the Palmerston North area; exact location to be confirmed."),
    ("PARTICIPANT REQUIREMENT", "Each participant is to complete a Leadership Personality Report before the facilitated session."),
]
COORD_LEAD = "2 ER and NZALC are to confirm:"
COORD = [
    "final participant numbers and nominal roll;",
    "relevant command relationships and team transitions;",
    "venue and available training facilities;",
    "arrangements and timelines for completing the Leadership Personality Reports; and",
    "any specific command outcomes that should inform the facilitation.",
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
    lh = lh or size * 1.28
    for line in wrapped(pg, text, size, avail, bold):
        pg.text(x, y, line, size, color, bold=bold)
        y += lh
    return y


def heading(pg, y, text):
    pg.text(M, y, text, 12, BLACK, bold=True)
    return y + 15


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
    pg.spaced(M, 108, KICKER, 8, SWAMP, bold=True, spacing=1.8)
    pg.text(M, 134, TITLE, 22, BLACK, bold=True)
    pg.line(M, 144, W - M, 144, ARMY_RED, width=2)
    pg.text(M, 160, ORIGINATOR, 9, SWAMP)
    x = M
    for s, bold in (("Date: ", True), (DATE, False)):
        pg.text(x, 174, s, 8, BLACK, bold=bold)
        x += pg.width(s, 8, bold)

    # purpose and context
    y = heading(pg, 202, "Purpose")
    y = para(pg, M, y + 5, PURPOSE, 10, CW) + 8
    y = heading(pg, y, "Context")
    y = para(pg, M, y + 5, CONTEXT, 10, CW) + 8

    # programme: two timed cards with a black time block
    y = heading(pg, y, "Programme")
    y = para(pg, M, y + 5, PROGRAMME_LEAD, 10, CW) + 1
    spine = 92
    r = 6
    for day, time, activity, focus in PROGRAMME:
        lines = wrapped(pg, focus, 9.2, CW - spine - 28)
        h = max(46, 28 + len(lines) * 12 + 6)
        pg.box(M, y, CW, h, fill=FAINT, stroke=None, radius=r)
        pg.box(M, y, spine + r, h, fill=BLACK, stroke=None, radius=r)
        pg.box(M + spine, y, r + 1, h, fill=FAINT, stroke=None)
        pg.spaced(M + 12, y + 19, day, 6.4, GOLD, bold=True, spacing=1.4)
        pg.text(M + 12, y + 34, time, 10, WHITE, bold=True)
        tx = M + spine + 14
        pg.text(tx, y + 19, activity, 10.5, BLACK, bold=True)
        ty = y + 33
        for line in lines:
            pg.text(tx, ty, line, 9.2, INK)
            ty += 12
        y += h + 6
    y += 4
    y = para(pg, M, y, FLEX_NOTE, 9.6, CW) + 3
    y = para(pg, M, y, PROGRAMME_NOTE, 9.6, CW, color=SWAMP) + 8

    # delivery: two-column field grid
    y = heading(pg, y, "Delivery")
    y += 6
    col_w = CW / 2
    row_y = y
    max_end = y
    for i, (label, value) in enumerate(DELIVERY):
        cx = M + (i % 2) * col_w
        if i % 2 == 0 and i:
            row_y = max_end + 8
        pg.spaced(cx, row_y, label, 6.4, SWAMP, bold=True, spacing=1.4)
        end = para(pg, cx, row_y + 13, value, 9.6, col_w - 18, lh=12)
        max_end = max(max_end, end)
    y = max_end + 12

    # coordination required
    y = heading(pg, y, "Coordination Required")
    y += 4
    y = para(pg, M, y, COORD_LEAD, 10, CW) + 1
    for item in COORD:
        pg.text(M + 4, y, "•", 10, SWAMP, bold=True)
        y = para(pg, M + 18, y, item, 10, CW - 18)
        y += 1
    print(f"content ends at y={y:.0f}")

    doc.set_metadata({"title": "Te Whi\u0101 Command Week 2026: NZALC Leadership Development Support to 2 ER",
                      "author": "New Zealand Army Leadership Centre"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
