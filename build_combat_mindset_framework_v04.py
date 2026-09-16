#!/usr/bin/env python3
"""
Combat Mindset Framework v0.4, AITC Discussion Draft: the Framework on a
Page, drawn as one A4 landscape sheet in the house style.

    python3 build_combat_mindset_framework_v04.py -> output/combat-mindset-framework-v0.4.pdf
"""

import pymupdf

from army_onepager import (ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, MID, MOAWHANGO, PALE,
                           SWAMP, WHITE, Page, logo_png)

OUT = "./output/combat-mindset-framework-v0.4.pdf"
W, H = 842, 595
M = 40
CW = W - 2 * M
R = 6

KICKER = "COMBAT MINDSET FRAMEWORK  ·  V0.4  ·  AITC DISCUSSION DRAFT"
TITLE = "Combat Mindset"
ORIGINATOR = "New Zealand Army Leadership Centre | Army Command School"
DATE = "September 2026"
FOOTER_LEFT = "Combat Mindset Framework v0.4 | AITC Discussion Draft"

MODEL = [
    ("1", "THE NEED", "Operational imperative",
     "Under operational pressure, trained individuals and teams can lose access to their full capability. "
     "Army must prepare them to remain effective and act decisively and ethically."),
    ("2", "THE CAPABILITY", "Combat Mindset",
     "Performance Under Pressure applied to military operations, with combat its most demanding test."),
    ("3", "HOW ARMY BUILDS IT", "Army Combat Mindset Development System",
     "How Army progressively develops Combat Mindset."),
]
STEPS = [
    ("1", "Understand Self", "Recognise how pressure affects your body, thinking and behaviour."),
    ("2", "Regulate Self", "Control your response so your capability remains available."),
    ("3", "Perform Under Pressure", "Practise performing effectively in controlled but demanding situations."),
    ("4", "Combat Mindset", "Perform your role effectively under operational demands."),
]
STEPS_NOTE = ("Steps 1 to 3 build Performance Under Pressure. Step 4 applies that capability under operational "
              "demands. That is Combat Mindset.")
RESPONSIBILITIES = [
    ("G7", "Doctrine and policy", "Sets Army direction for Combat Mindset."),
    ("ATG", "Training authority", "Oversees the training approach and approves changes."),
    ("ACS", "Learning provider", "Develops, integrates and delivers the learning."),
]
ENABLERS = ("SPECIALIST ENABLERS", "ILD  ·  APS  ·  HPC",
            "Provide specialist expertise, evidence and support across the system.")
WHERE_SUB = "EMBEDDED ACROSS EXISTING ACS TRAINING  ·  NOT A STANDALONE COURSE"
MATRIX_COLS = ["Understand Self", "Regulate Self", "Perform Under Pressure", "Combat Mindset"]
MATRIX = [
    ("NZALC", "LDS and ELDA", ["Trains", "Trains", "Trains", "Contributes"]),
    ("HPC", "COGCON", ["Reinforces", "Trains", "Trains", "Contributes"]),
    ("NCO School", "JNCO and SNCO", ["Reinforces", "Reinforces", "Reinforces", "Contributes"]),
    ("OCS", "Officer Cadet School", ["Trains", "Reinforces", "Trains", "Contributes"]),
]
VERBS = [
    ("Trains", "deliberate instruction and practice"),
    ("Reinforces", "further practice and application"),
    ("Contributes", "prepares for operational demands"),
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
    lh = lh or size * 1.3
    for line in wrapped(pg, text, size, avail, bold):
        pg.text(x, y, line, size, color, bold=bold)
        y += lh
    return y


def arrow_right(pg, x0, x1, y):
    pg.line(x0, y, x1 - 4, y, GOLD, width=1.1)
    sh = pg.p.new_shape()
    sh.draw_polyline([(x1 - 5, y - 3), (x1 - 5, y + 3), (x1, y)])
    sh.finish(color=None, fill=GOLD, closePath=True)
    sh.commit()


def arrow_down(pg, x, y0, y1):
    pg.line(x, y0, x, y1 - 4, GOLD, width=1.1)
    sh = pg.p.new_shape()
    sh.draw_polyline([(x - 3, y1 - 5), (x + 3, y1 - 5), (x, y1)])
    sh.finish(color=None, fill=GOLD, closePath=True)
    sh.commit()


def section(pg, x, y, num, label):
    pg.text(x, y, num, 9, GOLD, bold=True)
    pg.spaced(x + 12, y, label, 7, SWAMP, bold=True, spacing=1.6)


def verb_pill(pg, cx, cy, verb, w=64, h=15, size=7.4):
    x, y = cx - w / 2, cy - h / 2
    if verb == "Trains":
        pg.box(x, y, w, h, fill=BLACK, stroke=None, radius=h / 2)
        pg.text(cx, cy + 2.7, verb, size, WHITE, bold=True, align=1)
    elif verb == "Reinforces":
        pg.box(x, y, w, h, fill=MOAWHANGO, stroke=None, radius=h / 2)
        pg.text(cx, cy + 2.7, verb, size, SWAMP, bold=True, align=1)
    else:
        pg.box(x, y, w, h, fill=WHITE, stroke=GRID, width=0.8, radius=h / 2)
        pg.text(cx, cy + 2.7, verb, size, MID, align=1)


def letterhead(pg):
    pg.text(W / 2, 22, "UNCLASSIFIED", 8.5, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 24, "UNCLASSIFIED", 8.5, BLACK, bold=True, align=1)
    pg.text(M, H - 13, FOOTER_LEFT, 7.5, BLACK)
    pg.text(W / 2, H - 13, "ACS 2026", 7.5, BLACK, align=1)
    pg.text(W - M, H - 13, "Page 1 of 1", 7.5, BLACK, align=2)
    png, (iw, ih) = logo_png()
    lh = 22
    pg.p.insert_image(pymupdf.Rect(M, 30, M + lh * iw / ih, 30 + lh), stream=png)
    pg.text(M, 88, TITLE, 18, BLACK, bold=True)
    pg.line(M, 96, W - M, 96, ARMY_RED, width=2)
    pg.text(M, 108, ORIGINATOR, 8, SWAMP)
    x = W - M
    for s, bold in ((DATE, False), ("Date: ", True)):
        x -= pg.width(s, 7.5, bold)
        pg.text(x, 108, s, 7.5, BLACK, bold=bold)
    return 126


def build():
    doc = pymupdf.open()
    pg = Page(doc, W, H)
    y = letterhead(pg)

    # 1  the model: three cards across, black spines, gold arrows
    section(pg, M, y, "1", "THE MODEL")
    y += 8
    gap = 22
    cw = (CW - gap * 2) / 3
    spine = 28
    h = 68
    for i, (num, role, term, desc) in enumerate(MODEL):
        x = M + i * (cw + gap)
        pg.box(x, y, cw, h, fill=FAINT, stroke=None, radius=R)
        pg.box(x, y, spine + R, h, fill=BLACK, stroke=None, radius=R)
        pg.box(x + spine, y, R + 1, h, fill=FAINT, stroke=None)
        pg.text(x + spine / 2, y + 22, num, 13, GOLD, bold=True, align=1)
        # body area to the right of the spine; text block left aligned and vertically centred
        bx = x + spine + 10
        bw = cw - spine - 18
        heads = wrapped(pg, term, 9.5, bw, bold=True)
        body = wrapped(pg, desc, 6.9, bw)
        block = 13 + len(heads) * 11 + 1 + len(body) * 8.6
        top_pad = (h - block) / 2
        pg.spaced(bx, y + top_pad + 5, role, 5.6, SWAMP, bold=True, spacing=1.3)
        ty = y + top_pad + 18
        for line in heads:
            pg.text(bx, ty, line, 9.5, BLACK, bold=True)
            ty += 11
        ty += 1
        for line in body:
            pg.text(bx, ty, line, 6.9, INK)
            ty += 8.6
        if i < 2:
            arrow_right(pg, x + cw + 4, x + cw + gap - 4, y + h / 2)
    y += h + 18

    # 2  the developmental pathway: four steps, the last black
    section(pg, M, y, "2", "THE INDIVIDUAL DEVELOPMENTAL PATHWAY")
    y += 8
    gap = 16
    sw = (CW - gap * 3) / 4
    h = 62
    for i, (num, name, desc) in enumerate(STEPS):
        x = M + i * (sw + gap)
        final = i == 3
        pg.box(x, y, sw, h, fill=BLACK if final else FAINT, stroke=None, radius=R)
        pg.text(x + 10, y + 20, num, 13, GOLD, bold=True)
        pg.text(x + 26, y + 20, name, 9.5, WHITE if final else BLACK, bold=True)
        para(pg, x + 10, y + 36, desc, 6.9, sw - 20, color=GRID if final else INK, lh=8.6)
        if i < 3:
            arrow_right(pg, x + sw + 3, x + sw + gap - 3, y + 16)
    y += h + 12
    pg.text(M, y, STEPS_NOTE, 7.2, SWAMP)
    y += 20

    # 3 and 4 side by side
    top = y
    lw = 268
    rx = M + lw + 24
    rw = CW - lw - 24

    section(pg, M, top, "3", "WHO IS RESPONSIBLE")
    y = top + 8
    rh = 36
    for i, (org, role, desc) in enumerate(RESPONSIBILITIES):
        pg.box(M, y, lw, rh, fill=FAINT, stroke=None, radius=R)
        pg.box(M, y, 54 + R, rh, fill=BLACK, stroke=None, radius=R)
        pg.box(M + 54, y, R + 1, rh, fill=FAINT, stroke=None)
        pg.text(M + 27, y + 23, org, 10.5, WHITE, bold=True, align=1)
        pg.spaced(M + 64, y + 13, role.upper(), 5.6, SWAMP, bold=True, spacing=1.3)
        para(pg, M + 64, y + 25, desc, 7.2, lw - 72, lh=9)
        if i < 2:
            arrow_down(pg, M + 27, y + rh, y + rh + 8)
        y += rh + 8
    y += 2
    eh = 46
    pg.box(M, y, lw, eh, fill=PALE, stroke=None, radius=R)
    pg.spaced(M + 12, y + 14, ENABLERS[0], 6, SWAMP, bold=True, spacing=1.5)
    pg.text(M + 12, y + 27, ENABLERS[1], 8.5, BLACK, bold=True)
    para(pg, M + 12, y + 38, ENABLERS[2], 6.9, lw - 24, lh=8.4)
    left_end = y + eh

    section(pg, rx, top, "4", "WHERE COMBAT MINDSET IS DEVELOPED")
    y = top + 18
    label_w = 98
    col_w = (rw - label_w) / 4
    hh = 30
    for j, name in enumerate(MATRIX_COLS):
        x = rx + label_w + j * col_w
        final = j == 3
        pg.box(x + 2, y, col_w - 4, hh, fill=BLACK if final else FAINT, stroke=None, radius=4)
        pg.text(x + 8, y + 13, str(j + 1), 8.5, GOLD, bold=True)
        lines = wrapped(pg, name, 6.6, col_w - 16, bold=True)
        ty = y + 22 if len(lines) == 1 else y + 18
        for line in lines:
            pg.text(x + 8, ty, line, 6.6, WHITE if final else BLACK, bold=True)
            ty += 7.8
    pg.spaced(rx, y + hh - 6, "ACS PROVIDER", 5.6, SWAMP, bold=True, spacing=1.3)
    y += hh + 4
    rh = 27
    for org, sub, verbs in MATRIX:
        pg.box(rx, y, rw, rh, fill=FAINT, stroke=None, radius=4)
        pg.text(rx + 8, y + 12.5, org, 7.8, BLACK, bold=True)
        pg.text(rx + 8, y + 21.5, sub, 6, MID)
        for j, verb in enumerate(verbs):
            verb_pill(pg, rx + label_w + j * col_w + col_w / 2, y + rh / 2, verb)
        y += rh + 4
    y += 8
    x = rx
    for verb, definition in VERBS:
        verb_pill(pg, x + 24, y + 1, verb, w=48, h=13, size=6.4)
        pg.text(x + 54, y + 3.3, definition, 6.4, INK)
        x += 54 + pg.width(definition, 6.4) + 12
    right_end = y + 8
    print(f"left ends {left_end:.0f}, right ends {right_end:.0f}, footer marking at {H - 30}")

    doc.set_metadata({"title": "Combat Mindset Framework v0.4: The Framework on a Page",
                      "author": "New Zealand Army Leadership Centre"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
