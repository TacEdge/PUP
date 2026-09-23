#!/usr/bin/env python3
"""
Combat Mindset Conditioning: the product in one picture.

    python3 build_cmc_one_pager.py
        -> output/combat-mindset-conditioning-model.pdf (+ .png preview)

Five bands, top to bottom: what we develop, what the individual does when
performance degrades, what we observe, how we condition it, and the outcome.
Elements derived from COGCON are drawn with a dashed gold outline so the
provenance is visible; Army architecture is drawn solid.
"""

import pymupdf

from army_onepager import (ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, MID, MOAWHANGO, PALE,
                           SWAMP, WHITE, Page, rgb)
from build_army_combat_mindset_development_system import (arrow_down, dashed_box, label_chip,
                                                          reversed_logo_png, wrapped)

OUT = "./output/combat-mindset-conditioning-model.pdf"
PNG = "./output/combat-mindset-conditioning-model.png"
W, H = 842, 595
M = 40
CW = W - 2 * M
R = 6
GREY = rgb("5F5F5A")

TITLE = "Combat Mindset Conditioning"
SUBTITLE = "An Army training product within the Army Combat Mindset System"
ORIGINATOR = "Army Command School"
DATE = "23 September 2026"
FOOTER_LEFT = "Combat Mindset Conditioning | Draft for discussion"
STRAP = "The deliberate practice used to develop the capacity: what we develop, what we do when it drops, what we observe, how we train it, how we maintain the standard."

# (band label, role, element name, items, arrows between items, provenance)
BANDS = [
    ("PILLARS", "What we develop", "Combat Mindset Training Pillars",
     ["Self-Awareness", "Arousal Control", "Operational Habit", "Working Memory", "Attentional Control", "Cognitive Control"],
     False, "cogcon"),
    ("RESET", "What we do when it drops", "Combat Mindset Reset",
     ["Recognise", "Regulate", "Reorient", "Re-engage"], True, "cogcon"),
    ("STATES", "What effective performance looks like", "Combat Mindset Performance States",
     ["Task Focus", "Command Presence", "Situational Awareness", "Resilience"], False, "cogcon"),
    ("METHOD", "How we progressively condition it under pressure", "CMC Training Methodology",
     ["Learn", "Practise", "Pressure", "Apply", "Reinforce"], True, "army"),
    ("ASSURANCE", "How Army teaches, assesses and maintains the standard", "CMC Coaching and Assurance",
     ["CMC Coach", "CMC Lead Coach", "Observed assessment", "Recertification", "Quality assurance"], False, "cogcon"),
]
OUTCOME = ("OUTCOME", "COMBAT MINDSET", "The capacity to regulate and sustain effective performance under operational pressure.")
LEGEND = [("cogcon", "Derived from COGCON: substance preserved, labels working, subject to adaptation and IP agreement with Ken Franks"),
          ("army", "Army architecture")]


def masthead(pg):
    pg.text(W / 2, 20, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 22, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(M, H - 11, FOOTER_LEFT, 7.5, BLACK)
    pg.text(W / 2, H - 11, "ACS 2026", 7.5, BLACK, align=1)
    pg.text(W - M, H - 11, "Page 1 of 1", 7.5, BLACK, align=2)
    top, hh = 30, 46
    brand_w = 138
    pg.box(M, top, CW, hh, fill=FAINT, stroke=None, radius=R)
    pg.box(M, top, brand_w + R, hh, fill=ARMY_RED, stroke=None, radius=R)
    pg.box(M + brand_w, top, R + 1, hh, fill=FAINT, stroke=None)
    png, (iw, ih) = reversed_logo_png()
    lh = 27
    lw = lh * iw / ih
    pg.p.insert_image(pymupdf.Rect(M + (brand_w - lw) / 2, top + (hh - lh) / 2,
                                   M + (brand_w + lw) / 2, top + (hh + lh) / 2), stream=png)
    tx = M + brand_w + 18
    pg.text(tx, top + 27, TITLE, 18, BLACK, bold=True)
    pg.text(tx, top + 39, f"{SUBTITLE}  ·  {ORIGINATOR}  ·  {DATE}", 7.5, INK)
    return top + hh


def item_chip(pg, x, y, w, h, text, provenance):
    """A named element: solid pale card for Army architecture, dashed gold
    outline on white for COGCON-derived elements."""
    if provenance == "cogcon":
        pg.box(x, y, w, h, fill=WHITE, stroke=None, radius=R)
        dashed_box(pg, x, y, w, h, radius=R)
    else:
        pg.box(x, y, w, h, fill=PALE, stroke=None, radius=R)
    lines = wrapped(pg, text, 8, w - 14, bold=True)
    ty = y + h / 2 + 3 - (len(lines) - 1) * 5
    for line in lines:
        pg.text(x + w / 2, ty, line, 8, BLACK, bold=True, align=1)
        ty += 10


def gold_arrow_right(pg, x0, x1, y):
    pg.line(x0, y, x1 - 4, y, GOLD, width=1.1)
    sh = pg.p.new_shape()
    sh.draw_polyline([(x1 - 5.2, y - 3.2), (x1 - 5.2, y + 3.2), (x1, y)])
    sh.finish(color=None, fill=GOLD, closePath=True)
    sh.commit()


def band(pg, y, h, label, role, sub, items, arrows, provenance):
    spine = 96
    pg.box(M, y, CW, h, fill=FAINT, stroke=None, radius=R)
    pg.box(M, y, spine + R, h, fill=BLACK, stroke=None, radius=R)
    pg.box(M + spine, y, R + 1, h, fill=FAINT, stroke=None)
    pg.text(M + spine / 2, y + h / 2 + 3.5, label, 9.5 if len(label) > 7 else 11, WHITE, bold=True, align=1)
    ix = M + spine + 14
    iw_total = CW - spine - 28
    pg.spaced(ix, y + 13, sub.upper(), 5.6, SWAMP, bold=True, spacing=1.3)
    pg.text(ix + pg.width(sub.upper(), 5.6, True) + len(sub) * 1.3 + 10, y + 13, role, 7, GREY)
    n = len(items)
    gap = 18 if arrows else 8
    cw = (iw_total - gap * (n - 1)) / n
    cy = y + 19
    ch = h - 26
    for i, text in enumerate(items):
        x = ix + i * (cw + gap)
        item_chip(pg, x, cy, cw, ch, text, provenance)
        if arrows and i < n - 1:
            gold_arrow_right(pg, x + cw + 3, x + cw + gap - 3, cy + ch / 2)
    return y + h


def build():
    doc = pymupdf.open()
    pg = Page(doc, W, H)
    y = masthead(pg) + 22

    # strapline: the product in one sentence
    pg.text(W / 2, y, STRAP, 9.5, SWAMP, bold=True, align=1)
    y += 16

    bh = 54
    gap = 12
    for label, role, sub, items, arrows, prov in BANDS:
        y = band(pg, y, bh, label, role, sub, items, arrows, prov)
        arrow_down(pg, M + 48, y, y + gap)
        y += gap

    # outcome: black band, the capacity the product exists to build
    oh = 50
    spine = 96
    pg.box(M, y, CW, oh, fill=BLACK, stroke=None, radius=R)
    pg.text(M + spine / 2, y + oh / 2 + 4, OUTCOME[0], 11, GOLD, bold=True, align=1)
    pg.line(M + spine + 3, y + 10, M + spine + 3, y + oh - 10, GOLD, width=0.8)
    pg.text(M + spine + 14, y + 22, OUTCOME[1], 12, WHITE, bold=True)
    pg.text(M + spine + 14, y + 38, OUTCOME[2], 8.5, GRID)
    y += oh + 14

    # legend
    x = M
    for prov, text in LEGEND:
        item_chip(pg, x, y, 30, 13, "", prov)
        pg.text(x + 38, y + 9.5, text, 7, INK)
        x += 38 + pg.width(text, 7) + 22
    end = y + 13
    print(f"content ends {end:.0f}, footer marking at {H - 30}")

    doc.set_metadata({"title": "Combat Mindset Conditioning: the product in one picture",
                      "author": "Army Command School"})
    doc.save(OUT, garbage=3, deflate=True)
    pymupdf.open(OUT)[0].get_pixmap(dpi=200).save(PNG)
    print(f"Saved {OUT} and {PNG}")


if __name__ == "__main__":
    build()
