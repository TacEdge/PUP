#!/usr/bin/env python3
"""
Combat Mindset conceptual baseline on one page: the need, the capability,
and how Army builds it.  Drawn directly as an A4 PDF in the house style.

    python3 build_combat_mindset_baseline.py -> output/combat-mindset-conceptual-baseline.pdf
"""

import pymupdf

from army_onepager import (ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, MID, MOAWHANGO, PALE,
                           SWAMP, WHITE, Page, logo_png, rgb)

rgb_grey = rgb("EDEDEA")

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

STEPS = [
    ("1", "Understand Self", "Recognise how pressure affects your body, thinking and behaviour."),
    ("2", "Regulate Self", "Control your response so your capability remains available."),
    ("3", "Perform Under Pressure", "Practise fulfilling the requirements of your role in controlled but demanding situations."),
    ("4", "Combat Mindset", "Perform your role effectively under operational demands."),
]
PATHWAY_TITLE = "How Combat Mindset Develops"
PATHWAY_LEAD = ("Combat Mindset is a role-performance capability, not a leadership capability. The role changes by rank, "
                "appointment and function. The requirement does not: perform your role effectively under operational demands.")
PATHWAY_LINE = "Understand yourself  \u2192  regulate yourself  \u2192  perform under pressure  \u2192  perform your role under operational demands"
ROLE_NOTE = ("What effective performance looks like depends on role and responsibility. It may involve leading others, "
             "but leadership is not a requirement for Combat Mindset.")
ROLE_EXAMPLES = ("For some people the role includes leading and influencing others. For others it means applying technical "
                 "or tactical skills, following direction, communicating clearly and contributing to team performance.")
ROLES = ["Private soldier", "Section 2IC", "Platoon commander", "Specialist", "Brigade commander"]
PATHWAY_BOTTOM = ("The final step is Combat Mindset. The pathway is the same for a private soldier, a section 2IC, a platoon "
                  "commander, a specialist or a brigade commander. Leadership is not the organising feature of the capability.")

RESP_TITLE = "Proposed Responsibilities"
RESP_LEAD = ("Four organisations carry the Framework. Each has one role, and the roles run in one direction: "
             "direction, oversight, delivery, with specialist expertise supporting all three.")
RESPONSIBILITIES = [
    ("G7", "Doctrine and policy", "Sets Army direction for Combat Mindset."),
    ("ATG", "Training authority", "Oversees the training approach and approves changes."),
    ("ACS", "Learning provider", "Develops, integrates and delivers the learning."),
]
ENABLERS = ("SPECIALIST ENABLERS", "ILD  \u00b7  APS  \u00b7  HPC", "Provide specialist expertise, evidence and support.")
RESP_BOTTOM = ("G7 sets the direction. ATG oversees the training. ACS develops and delivers it. Specialist enablers "
               "provide the expertise and evidence that support the system.")

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


def letterhead(doc, kicker, title, page_label):
    pg = Page(doc, W, H)
    pg.text(W / 2, 28, "UNCLASSIFIED", 9, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 34, "UNCLASSIFIED", 9, BLACK, bold=True, align=1)
    pg.text(M, H - 20, FOOTER_LEFT, 8, BLACK)
    pg.text(W / 2, H - 20, "ACS 2026", 8, BLACK, align=1)
    pg.text(W - M, H - 20, page_label, 8, BLACK, align=2)
    png, (iw, ih) = logo_png()
    lh = 26
    pg.p.insert_image(pymupdf.Rect(M, 56, M + lh * iw / ih, 56 + lh), stream=png)
    pg.spaced(M, 108, kicker, 8, SWAMP, bold=True, spacing=1.8)
    pg.text(M, 134, title, 22, BLACK, bold=True)
    pg.line(M, 144, W - M, 144, ARMY_RED, width=2)
    pg.text(M, 160, ORIGINATOR, 9, SWAMP)
    x = M
    for s, bold, col in (("Reference: ", True, BLACK), (REFERENCE, False, BLACK), ("   ·   ", False, MID),
                         ("Date: ", True, BLACK), (DATE, False, BLACK)):
        pg.text(x, 174, s, 8, col, bold=bold)
        x += pg.width(s, 8, bold)
    return pg


def arrow_right(pg, x0, x1, y):
    pg.line(x0, y, x1 - 5, y, GOLD, width=1.2)
    sh = pg.p.new_shape()
    sh.draw_polyline([(x1 - 6, y - 3.5), (x1 - 6, y + 3.5), (x1, y)])
    sh.finish(color=None, fill=GOLD, closePath=True)
    sh.commit()


def pathway_page(doc):
    pg = letterhead(doc, KICKER + "  \u00b7  DEVELOPMENTAL PATHWAY", PATHWAY_TITLE, "Page 2 of 3")
    cw = W - 2 * M
    y = 206
    for line in wrapped_lines(pg, PATHWAY_LEAD, 10, cw):
        pg.text(M, y, line, 10, INK)
        y += 14
    y += 22

    # the rising steps: bottom aligned, each taller than the last; the final step is black
    n = len(STEPS)
    gap = 14
    sw = (cw - gap * (n - 1)) / n
    base_h, rise = 118, 24
    bottom = y + base_h + rise * (n - 1)
    for i, (num, name, desc) in enumerate(STEPS):
        h = base_h + rise * i
        x = M + i * (sw + gap)
        top = bottom - h
        final = i == n - 1
        pg.box(x, top, sw, h, fill=BLACK if final else FAINT, stroke=None, radius=CARD_R)
        pg.text(x + 14, top + 30, num, 22, GOLD, bold=True)
        ty = top + 52
        for line in wrapped_lines(pg, name, 10.5, sw - 26, bold=True):
            pg.text(x + 14, ty, line, 10.5, WHITE if final else BLACK, bold=True)
            ty += 13.5
        ty += 3
        for line in wrapped_lines(pg, desc, 8.6, sw - 26):
            pg.text(x + 14, ty, line, 8.6, GRID if final else INK)
            ty += 11.5
        if final:
            pg.spaced(x + 14, bottom - 14, "THE CAPABILITY", 6.2, GOLD, bold=True, spacing=1.4)
        else:
            arrow_right(pg, x + sw + 2, x + sw + gap - 2, top + 26)
    y = bottom + 24

    # the intuitive line
    pg.text(W / 2, y, PATHWAY_LINE, 8.2, SWAMP, bold=True, align=1)
    y += 28

    # role clarification
    nl = wrapped_lines(pg, ROLE_NOTE, 10, cw - 36)
    nh = 16 + len(nl) * 14 + 4
    pg.box(M, y, cw, nh, fill=PALE, stroke=None, radius=6)
    ly = y + 20
    for line in nl:
        pg.text(M + 18, ly, line, 10, SWAMP, bold=True)
        ly += 14
    y += nh + 16
    for line in wrapped_lines(pg, ROLE_EXAMPLES, 10, cw):
        pg.text(M, y, line, 10, INK)
        y += 14
    y += 14

    # the same pathway, whatever the role
    pg.spaced(M, y, "THE SAME PATHWAY, WHATEVER THE ROLE", 6.6, SWAMP, bold=True, spacing=1.5)
    y += 12
    pw = [pg.width(r, 8.6) + 22 for r in ROLES]
    pgap = 8
    x = M
    for r, w in zip(ROLES, pw):
        pg.box(x, y, w, 20, fill=WHITE, stroke=GRID, width=0.8, radius=10)
        pg.text(x + w / 2, y + 13.5, r, 8.6, INK, align=1)
        x += w + pgap
    y += 20 + 24

    card_h = 82
    pg.box(M, y, cw, card_h, fill=MOAWHANGO, stroke=None, radius=8)
    pg.textbox(M + 18, y + 16, cw - 36, card_h - 16, PATHWAY_BOTTOM, 11, SWAMP, bold=True, lh=1.35)
    print(f"page 2 content ends at y={y + card_h:.0f}")


def responsibilities_page(doc):
    pg = letterhead(doc, KICKER + "  \u00b7  PROPOSED RESPONSIBILITIES", RESP_TITLE, "Page 3 of 3")
    cw = W - 2 * M
    # for-confirmation pill beside the title
    label = "FOR CONFIRMATION"
    lw = sum(pg.width(ch, 6.4, True) + 1.4 for ch in label) + 20
    tx = M + pg.width(RESP_TITLE, 22, True) + 14
    pg.box(tx, 120, lw, 16, fill=rgb_grey, stroke=None, radius=8)
    pg.spaced(tx + 10, 131, label, 6.4, MID, bold=True, spacing=1.4)

    y = 206
    for line in wrapped_lines(pg, RESP_LEAD, 10, cw):
        pg.text(M, y, line, 10, INK)
        y += 14
    y += 22

    # three organisations in a row, direction flowing left to right
    n = len(RESPONSIBILITIES)
    gap = 18
    bw = (cw - gap * (n - 1)) / n
    bh = 128
    for i, (org, role, desc) in enumerate(RESPONSIBILITIES):
        x = M + i * (bw + gap)
        pg.box(x, y, bw, bh, fill=FAINT, stroke=None, radius=CARD_R)
        pg.box(x, y, bw, 34, fill=BLACK, stroke=None, radius=CARD_R)
        pg.box(x, y + 20, bw, 14, fill=BLACK, stroke=None)
        pg.text(x + 14, y + 23, org, 13, WHITE, bold=True)
        pg.spaced(x + 14, y + 56, role.upper(), 6.6, SWAMP, bold=True, spacing=1.4)
        ty = y + 76
        for line in wrapped_lines(pg, desc, 10, bw - 28):
            pg.text(x + 14, ty, line, 10, INK)
            ty += 14
        if i < n - 1:
            arrow_right(pg, x + bw + 3, x + bw + gap - 3, y + 17)
    y += bh + 18

    # specialist enablers span the row and support all three
    eh = 78
    pg.box(M, y, cw, eh, fill=PALE, stroke=None, radius=CARD_R)
    pg.spaced(M + 16, y + 24, ENABLERS[0], 8, SWAMP, bold=True, spacing=1.8)
    pg.text(M + 16, y + 44, ENABLERS[1], 11, BLACK, bold=True)
    pg.text(M + 16, y + 62, ENABLERS[2], 10, INK)
    pg.spaced(W - M - 16, y + 24, "SUPPORTS ALL THREE", 6.6, MID, bold=True, spacing=1.4, align=2)
    # three short gold ties up to the organisations above
    for i in range(n):
        cx = M + i * (bw + gap) + bw / 2
        pg.line(cx, y, cx, y - 18, GOLD, width=1.2)
    y += eh + 26

    card_h = 66
    pg.box(M, y, cw, card_h, fill=MOAWHANGO, stroke=None, radius=8)
    pg.textbox(M + 18, y + 16, cw - 36, card_h - 16, RESP_BOTTOM, 11, SWAMP, bold=True, lh=1.35)
    print(f"page 3 content ends at y={y + card_h:.0f}")


def build():
    doc = pymupdf.open()
    pg = letterhead(doc, KICKER, TITLE, "Page 1 of 3")

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

    pathway_page(doc)
    responsibilities_page(doc)
    doc.set_metadata({"title": "Combat Mindset Framework: Conceptual Baseline",
                      "author": "New Zealand Army Leadership Centre"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}  (content ends at y={y + card_h:.0f})")


if __name__ == "__main__":
    build()
