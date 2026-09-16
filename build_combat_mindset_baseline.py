#!/usr/bin/env python3
"""
Combat Mindset conceptual baseline on one page: the need, the capability,
and how Army builds it.  Drawn directly as an A4 PDF in the house style.

    python3 build_combat_mindset_baseline.py -> output/combat-mindset-conceptual-baseline.pdf
"""

import pymupdf

from army_onepager import (ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, MID, MOAWHANGO, PALE,
                           SWAMP, WHITE, Page, logo_png)

OUT = "./output/combat-mindset-conceptual-baseline.pdf"
W, H = 595, 842
M = 56

KICKER = "COMBAT MINDSET FRAMEWORK"
TITLE = "Conceptual Baseline"
ORIGINATOR = "New Zealand Army Leadership Centre | Army Command School"
REFERENCE = "Working baseline for the Framework"
DATE = "September 2026"
FOOTER_LEFT = "Combat Mindset Framework | Conceptual Baseline"

LEAD = ("The Framework rests on three statements. Each answers one question, and each depends on the one before it. "
        "Everything else in the Framework is tested against them.")

BLOCKS = [
    ("1", "THE NEED", "Operational imperative",
     "Under operational pressure, trained individuals and teams do not always retain access to their full "
     "capability. Army must prepare its people to remain effective and act decisively and ethically despite "
     "that pressure.", None),
    ("2", "THE CAPABILITY", "Combat Mindset",
     "Performance Under Pressure applied to the demands of military operations, with combat representing "
     "its most demanding expression.",
     "Performance Under Pressure sits within this definition. It is not a separate layer of the Framework."),
    ("3", "HOW ARMY BUILDS IT", "Combat Mindset Framework",
     "Army's approach for progressively developing, embedding and measuring Combat Mindset through "
     "existing training.", None),
]

BOTTOM = ("Working baseline. Any element of the Framework that does not serve the need, define the capability, "
          "or describe how Army builds it is simplified or removed.")

SPINE_W = 132
CARD_R = 7


def wrapped_lines(pg, text, size, avail, bold=False):
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


def card(pg, x, y, w, h, num, role, term, definition, note):
    # body: soft-cornered pale panel; spine: black block sharing the left corners
    pg.box(x, y, w, h, fill=FAINT, stroke=None, radius=CARD_R)
    pg.box(x, y, SPINE_W + CARD_R, h, fill=BLACK, stroke=None, radius=CARD_R)
    pg.box(x + SPINE_W, y, CARD_R + 1, h, fill=FAINT, stroke=None)
    pg.text(x + 18, y + 34, num, 26, GOLD, bold=True)
    pg.spaced(x + 18, y + h - 18, role, 6.6, WHITE, bold=True, spacing=1.5)
    tx = x + SPINE_W + 20
    tw = w - SPINE_W - 40
    pg.text(tx, y + 26, term, 12.5, BLACK, bold=True)
    ty = y + 44
    for line in wrapped_lines(pg, definition, 10.5, tw):
        pg.text(tx, ty, line, 10.5, INK)
        ty += 14.5
    if note:
        ny = ty + 6
        nl = wrapped_lines(pg, note, 8.6, tw - 24)
        nh = 14 + len(nl) * 11.5
        pg.box(tx, ny, tw, nh, fill=PALE, stroke=None, radius=4)
        ly = ny + 15
        for line in nl:
            pg.text(tx + 12, ly, line, 8.6, SWAMP)
            ly += 11.5


def connector(pg, x, y0, y1):
    pg.line(x, y0, x, y1 - 5, GOLD, width=1.4)
    sh = pg.p.new_shape()
    sh.draw_polyline([(x - 4.5, y1 - 7), (x + 4.5, y1 - 7), (x, y1)])
    sh.finish(color=None, fill=GOLD, closePath=True)
    sh.commit()


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
    for s, bold, col in (("Reference: ", True, BLACK), (REFERENCE, False, BLACK), ("   ·   ", False, MID),
                         ("Date: ", True, BLACK), (DATE, False, BLACK)):
        pg.text(x, 174, s, 8, col, bold=bold)
        x += pg.width(s, 8, bold)

    y = 206
    for line in wrapped_lines(pg, LEAD, 10, W - 2 * M):
        pg.text(M, y, line, 10, INK)
        y += 14
    y += 10

    cw = W - 2 * M
    gap = 26
    spine_cx = M + SPINE_W / 2
    for k, (num, role, term, definition, note) in enumerate(BLOCKS):
        body_lines = wrapped_lines(pg, definition, 10.5, cw - SPINE_W - 40)
        h = 44 + len(body_lines) * 14.5 + 22
        if note:
            h += 14 + len(wrapped_lines(pg, note, 8.6, cw - SPINE_W - 64)) * 11.5
        h = max(h, 92)
        card(pg, M, y, cw, h, num, role, term, definition, note)
        if k < len(BLOCKS) - 1:
            connector(pg, spine_cx, y + h, y + h + gap)
        y += h + gap

    # the read-across in one line
    chain = [("THE NEED", None), ("THE CAPABILITY", None), ("HOW ARMY BUILDS IT", None)]
    parts = [c for c, _ in chain]
    widths = [sum(pg.width(ch, 7, True) + 1.5 for ch in s) for s in parts]
    arrow_w = 34
    total = sum(widths) + arrow_w * (len(parts) - 1)
    x = W / 2 - total / 2
    for i, (s, wdt) in enumerate(zip(parts, widths)):
        pg.spaced(x, y + 8, s, 7, SWAMP, bold=True, spacing=1.5)
        x += wdt
        if i < len(parts) - 1:
            pg.line(x + 9, y + 5, x + arrow_w - 12, y + 5, GOLD, width=1.2)
            sh = pg.p.new_shape()
            sh.draw_polyline([(x + arrow_w - 14, y + 1.5), (x + arrow_w - 14, y + 8.5), (x + arrow_w - 9, y + 5)])
            sh.finish(color=None, fill=GOLD, closePath=True)
            sh.commit()
            x += arrow_w
    y += 30

    card_h = 60
    pg.box(M, y, cw, card_h, fill=MOAWHANGO, stroke=None, radius=8)
    pg.textbox(M + 18, y + 14, cw - 36, card_h - 16, BOTTOM, 11, SWAMP, bold=True, lh=1.35)

    doc.set_metadata({"title": "Combat Mindset Framework: Conceptual Baseline",
                      "author": "New Zealand Army Leadership Centre"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}  (content ends at y={y + card_h:.0f})")


if __name__ == "__main__":
    build()
