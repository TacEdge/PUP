#!/usr/bin/env python3
"""
Combat Mindset Conditioning: the product in one picture.

    python3 build_cmc_one_pager.py
        -> output/combat-mindset-conditioning-model.pdf (+ .png preview)

Five bands, top to bottom: what we develop, how we restore performance, what
effective performance looks like, how we condition it, how we maintain the
standard, and the outcome.  Derived architecture (COGCON, adapted by Army) is
drawn with a dashed gold outline; Army integration architecture is drawn solid.
"""

import pymupdf

from army_onepager import (ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, MID, MOAWHANGO, PALE,
                           SWAMP, WHITE, Page, rgb)
from build_army_combat_mindset_development_system import (arrow_down, dashed_box, label_chip,
                                                          reversed_logo_png, wrapped)

OUT = "./output/combat-mindset-conditioning-model.pdf"
PNG = "./output/combat-mindset-conditioning-model.png"

# Page numbering: a combined pack sets these so numbering runs across documents.
PAGE_OFFSET = 0
PAGE_TOTAL = None


def page_label(i, n):
    return f"Page {PAGE_OFFSET + i} of {PAGE_TOTAL or n}"

W, H = 842, 595
M = 40
CW = W - 2 * M
R = 6
GREY = rgb("5F5F5A")

TITLE = "Combat Mindset Conditioning (CMC)"
SUBTITLE = "An Army training product within the Army Combat Mindset System"
ORIGINATOR = "Army Command School"
DATE = "23 September 2026"
STRAP = "The deliberate practice of an individual\u2019s capacity to regulate and sustain effective performance under operational pressure."
FOOTER_LEFT = "Combat Mindset Conditioning | Design and development draft"

# (band label, role, element name, items, arrows between items, provenance, note)
#   provenance: "derived" = COGCON architecture adapted by Army;
#               "army"    = Army integration architecture (how ACS nests and delivers it);
#               "working" = a working conceptual model, not yet the resolved mechanism
BANDS = [
    ("PILLARS", "What we develop", "Combat Mindset Pillars",
     ["Self-Awareness", "Arousal Control", "Operational Habit", "Working Memory", "Attentional Control", "Cognitive Control"],
     False, "derived", None),
    ("RESET", "How we restore performance", "Combat Mindset Reset",
     [], False, "seb", None),
    ("STATES", "What effective performance looks like", "Combat Mindset Performance States",
     ["Task Focus", "Command Presence", "Situational Awareness", "Resilience"], False, "derived", None),
    ("METHOD", "How we condition it under pressure", "CMC Training Methodology",
     [("Sequenced Development", "Develop the capacities in the required order."),
      ("Progressive Load", "Condition them under increasing levels of pressure."),
      ("Integrated Training", "Practise them within the training where they need to function."),
      ("Conditioned Response", "Build effective responses that remain available when conscious capacity reduces."),
      ("Behavioural Assessment", "Assess observable performance under load.")],
     False, "army", None),
    ("ASSURANCE", "How we maintain the standard", "CMC Coaching and Assurance",
     [], False, "army",
     ("Army teaches, assesses and maintains the standard through trained CMC coaches, observed assessment, recertification and quality assurance.",
      "Draws on COGCON\u2019s existing coach accreditation and assurance architecture")),
]
# The SEB Cycle: the method through which the Combat Mindset Reset is executed.
# Re-engage is the outcome of completing the cycle, not a fourth letter.
SEB = [("S", "STATE", "Recognise your state"),
       ("E", "EYES UP", "Orient to your environment"),
       ("B", "BREATHE & BODY", "Regulate your state")]
SEB_OUTCOME = ("RE-ENGAGE", "Return attention to what matters now")
OUTCOME = ("OUTCOME", "COMBAT MINDSET", "The capacity to regulate and sustain effective performance under operational pressure.")
LEGEND = [("derived", "Derived architecture: COGCON, adapted by Army under the agreed IP arrangements"),
          ("army", "Army integration architecture: how ACS nests and delivers it")]


def masthead(pg):
    pg.text(W / 2, 20, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 22, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(M, H - 11, FOOTER_LEFT, 7.5, BLACK)
    pg.text(W / 2, H - 11, "ACS 2026", 7.5, BLACK, align=1)
    pg.text(W - M, H - 11, page_label(1, 1), 7.5, BLACK, align=2)
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
    pg.text(tx, top + 30, TITLE, 18, BLACK, bold=True)
    return top + hh


def item_chip(pg, x, y, w, h, text, provenance):
    """A named element: solid pale card for Army architecture, dashed gold
    outline on white for COGCON-derived elements."""
    if provenance == "derived":
        pg.box(x, y, w, h, fill=WHITE, stroke=None, radius=R)
        dashed_box(pg, x, y, w, h, radius=R)
    else:
        pg.box(x, y, w, h, fill=PALE, stroke=None, radius=R)
    if isinstance(text, tuple):
        # a principle: name, then a one-line descriptor
        name, desc = text
        pg.text(x + 9, y + 15, name, 7.4, BLACK, bold=True)
        ty = y + 26
        for line in wrapped(pg, desc, 6.2, w - 18):
            pg.text(x + 9, ty, line, 6.2, GREY)
            ty += 8
        return
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


def seb_band(pg, x, y, w, h):
    """S, E and B grouped as the cycle (derived, dashed gold), then Re-engage
    as the outcome of completing it."""
    out_w = 150
    gap = 22
    group_w = w - out_w - gap
    pg.box(x, y, group_w, h, fill=WHITE, stroke=None, radius=R)
    dashed_box(pg, x, y, group_w, h, radius=R)
    pg.spaced(x + 10, y + 11, "SEB CYCLE", 5.6, GOLD, bold=True, spacing=1.3)
    n = len(SEB)
    inner_gap = 8
    top = y + 16
    ch = h - 22
    cw = (group_w - 20 - inner_gap * (n - 1)) / n
    for i, (letter, name, line) in enumerate(SEB):
        cx = x + 10 + i * (cw + inner_gap)
        pg.box(cx, top, cw, ch, fill=FAINT, stroke=None, radius=4)
        pg.text(cx + 9, top + ch / 2 + 5.5, letter, 15, GOLD, bold=True)
        pg.text(cx + 27, top + ch / 2 - 1, name, 7.6, BLACK, bold=True)
        pg.text(cx + 27, top + ch / 2 + 9, line, 6.4, GREY)
        if i < n - 1:
            gold_arrow_right(pg, cx + cw + 1, cx + cw + inner_gap - 1, top + ch / 2)
    ax = x + group_w
    gold_arrow_right(pg, ax + 3, ax + gap - 3, y + h / 2)
    ox = ax + gap
    pg.box(ox, y, out_w, h, fill=BLACK, stroke=None, radius=R)
    pg.text(ox + 12, y + h / 2 - 1, SEB_OUTCOME[0], 8.5, WHITE, bold=True)
    pg.text(ox + 12, y + h / 2 + 10, SEB_OUTCOME[1], 6.4, GRID)


def band(pg, y, h, label, role, sub, items, arrows, provenance, note=None):
    spine = 96
    pg.box(M, y, CW, h, fill=FAINT, stroke=None, radius=R)
    pg.box(M, y, spine + R, h, fill=BLACK, stroke=None, radius=R)
    pg.box(M + spine, y, R + 1, h, fill=FAINT, stroke=None)
    pg.text(M + spine / 2, y + h / 2 + 3.5, label, 9.5 if len(label) > 7 else 11, WHITE, bold=True, align=1)
    ix = M + spine + 14
    iw_total = CW - spine - 28
    pg.spaced(ix, y + 13, sub.upper(), 5.6, SWAMP, bold=True, spacing=1.3)
    pg.text(ix + pg.width(sub.upper(), 5.6, True) + len(sub) * 1.3 + 10, y + 13, role, 7, GREY)
    cy = y + 19
    ch = h - 26
    if provenance == "seb":
        seb_band(pg, ix, cy, iw_total, ch)
        return y + h
    if not items:
        # a statement band: the element is described, not itemised
        pg.text(ix, cy + 13, note[0], 8.5, BLACK, bold=True)
        pg.text(ix, cy + 25, note[1], 7, GREY)
        return y + h
    n = len(items)
    gap = 18 if arrows else 8
    cw = (iw_total - gap * (n - 1)) / n
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

    bh = 52
    gap = 11
    for label, role, sub, items, arrows, prov, note in BANDS:
        tall = prov == "seb" or (items and isinstance(items[0], tuple))
        y = band(pg, y, bh + 22 if tall else bh, label, role, sub, items, arrows, prov, note)
        arrow_down(pg, M + 48, y, y + gap)
        y += gap

    # outcome: black band, the capacity the product exists to build
    oh = 48
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
