#!/usr/bin/env python3
"""
Army Combat Mindset System, AITC Discussion: the system on a page, drawn
as one A4 landscape sheet in the house style.

    python3 build_army_combat_mindset_development_system.py
        -> output/army-combat-mindset-development-system.pdf
        -> output/army-combat-mindset-development-system.png (preview, 200 dpi)
"""

import pymupdf

from army_onepager import (ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, MID, MOAWHANGO, PALE,
                           SWAMP, WHITE, Page, logo_png, rgb)

OUT = "./output/army-combat-mindset-development-system.pdf"
PNG = "./output/army-combat-mindset-development-system.png"

# Page numbering: a combined pack sets these so numbering runs across documents.
PAGE_OFFSET = 0
PAGE_TOTAL = None


def page_label(i, n):
    return f"Page {PAGE_OFFSET + i} of {PAGE_TOTAL or n}"

W, H = 842, 595
M = 40
CW = W - 2 * M
R = 6
OLIVE_LIGHT = rgb("E3E6D3")   # third step of the staircase, between PALE and MOAWHANGO
CHARCOAL = rgb("222222")
GREY = rgb("5F5F5A")       # secondary text: subtitles and provider descriptors

TITLE = "Combat Mindset System (CMS)"
ORIGINATOR = "Army Command School"
DATE = "September 2026"
FOOTER_LEFT = "Army Combat Mindset System | AITC Discussion"

# ---- locked content --------------------------------------------------------
MODEL = [
    ("1", "THE NEED", "Operational imperative",
     "Under pressure, trained individuals and teams can lose access to their full capability. "
     "Army must prepare them to remain effective and act decisively and ethically."),
    ("2", "THE CAPABILITY", "Combat Mindset",
     "The capacity to regulate and sustain effective performance under operational pressure."),
    ("3", "HOW ARMY BUILDS IT", "Army Combat Mindset System",
     "The training pathway that progressively builds this capacity, from understanding self to applying it under operational demands."),
]
STEPS = [
    ("1", "Understand Self", "Recognise your response."),
    ("2", "Regulate Self", "Manage response and redirect attention."),
    ("3", "Perform Under Pressure", "Practise sustaining performance under pressure across contexts."),
    ("4", "Combat Mindset", "Apply it to operational demands."),
]
STEPS_REINFORCE = ("Performance Under Pressure is a trainable capacity. It can be developed in any demanding context and "
                   "applied to increasingly realistic operational demands.")
RESPONSIBILITIES = [
    # spine, function, role
    ("G7", "Army direction", "Sets the Army requirement, doctrine and policy direction."),
    ("ATG HQ", "Training governance", "Governs the training response, assurance and approval of changes."),
    ("COMDT ACS", "Army sponsor", "Accountable sponsor for the Combat Mindset System."),
    ("PROVIDERS", "Learning providers", "Develop and deliver the learning."),
]
PROVIDER_CHIPS = ["NZALC", "OCS", "NCO School", "External providers"]
ADVISERS = ("SPECIALIST ADVISERS", ["HPC", "APS", "ILD"],
            "Provide specialist advice, evidence and support.")
MATRIX_COLS = ["Understand Self", "Regulate Self", "Perform Under Pressure", "Combat Mindset"]
MATRIX = [
    ("NZALC", "LDS and ELDA", ["Trains", "Trains", "Trains", "Trains"]),
    ("NCO School", "JNCO and SNCO", ["Reinforces", "Reinforces", "Reinforces", "Reinforces"]),
    ("OCS", "Combat Mindset Conditioning", ["Trains", "Trains", "Trains", "Trains"]),
]
# Scale option: what delivery looks like beyond ACS.  Drawn as a proposal,
# outside the three ACS rows, so current delivery is never read as wider.
MATRIX_SCALE = ("Army-wide delivery", "Units \u00b7 PT \u00b7 exercises \u00b7\nother training establishments",
                ["Reinforces", "Reinforces", "Trains", "Trains"])
SCALE_LABEL = "BEYOND ACS  \u00b7  SCALE OPTION"
SCALE_NOTE = "proposed, not current delivery"
VERBS = [
    ("Trains", "deliberate instruction and practice"),
    ("Reinforces", "further practice and application"),
]
SECTIONS = {
    1: ("01", "MODEL", "What it is and why Army needs it.", "model"),
    2: ("02", "DEVELOPMENT", "How the capability develops through training.", "development"),
    3: ("03", "RESPONSIBILITY", "Who directs, sponsors and supports it.", "responsibility"),
    4: ("04", "DELIVERY", "Where it is trained and reinforced.", "delivery"),
}


# ---- helpers ---------------------------------------------------------------
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


def arrow_head_right(pg, x, y, size=4):
    sh = pg.p.new_shape()
    sh.draw_polyline([(x - size * 1.3, y - size * 0.8), (x - size * 1.3, y + size * 0.8), (x, y)])
    sh.finish(color=None, fill=GOLD, closePath=True)
    sh.commit()


def arrow_head_down(pg, x, y, size=4):
    sh = pg.p.new_shape()
    sh.draw_polyline([(x - size * 0.8, y - size * 1.3), (x + size * 0.8, y - size * 1.3), (x, y)])
    sh.finish(color=None, fill=GOLD, closePath=True)
    sh.commit()


def arrow_right(pg, x0, x1, y):
    pg.line(x0, y, x1 - 4, y, GOLD, width=1.1)
    arrow_head_right(pg, x1, y)


def arrow_down(pg, x, y0, y1):
    pg.line(x, y0, x, y1 - 4, GOLD, width=1.1)
    arrow_head_down(pg, x, y1)


def dashed(pg, x0, y0, x1, y1):
    pg.line(x0, y0, x1, y1, GOLD, width=0.9, dashes="[2.5 2.5] 0")


def dashed_box(pg, x, y, w, h, radius=0):
    """Dashed gold outline: used where something is proposed rather than in place."""
    sh = pg.p.new_shape()
    r = pymupdf.Rect(x, y, x + w, y + h)
    if radius:
        sh.draw_rect(r, radius=(min(radius / w, 0.5), min(radius / h, 0.5)))
    else:
        sh.draw_rect(r)
    sh.finish(color=GOLD, fill=None, width=0.9, dashes="[2.5 2.5] 0")
    sh.commit()


def nav_icon(pg, kind, x, y, s=11):
    """One monochrome line icon per section header; x, y is the icon box top-left."""
    sh = pg.p.new_shape()
    if kind == "model":            # three connected nodes: a system of relationships
        a, b, c = (x + s * 0.18, y + s * 0.82), (x + s * 0.5, y + s * 0.18), (x + s * 0.82, y + s * 0.82)
        sh.draw_line(a, b); sh.draw_line(b, c); sh.draw_line(a, c)
        for p in (a, b, c):
            sh.draw_circle(p, s * 0.14)
    elif kind == "development":    # rising steps
        sh.draw_polyline([(x, y + s), (x + s / 3, y + s), (x + s / 3, y + 2 * s / 3), (x + 2 * s / 3, y + 2 * s / 3),
                          (x + 2 * s / 3, y + s / 3), (x + s, y + s / 3), (x + s, y)])
    elif kind == "responsibility": # command chain: one node over two
        sh.draw_circle((x + s / 2, y + s * 0.2), s * 0.15)
        sh.draw_circle((x + s * 0.2, y + s * 0.82), s * 0.15)
        sh.draw_circle((x + s * 0.8, y + s * 0.82), s * 0.15)
        sh.draw_line((x + s / 2, y + s * 0.35), (x + s / 2, y + s * 0.55))
        sh.draw_line((x + s * 0.2, y + s * 0.55), (x + s * 0.8, y + s * 0.55))
        sh.draw_line((x + s * 0.2, y + s * 0.55), (x + s * 0.2, y + s * 0.67))
        sh.draw_line((x + s * 0.8, y + s * 0.55), (x + s * 0.8, y + s * 0.67))
    elif kind == "delivery":       # instruction: board on a stand
        sh.draw_rect(pymupdf.Rect(x, y, x + s, y + s * 0.62))
        sh.draw_line((x + s * 0.2, y + s * 0.24), (x + s * 0.8, y + s * 0.24))
        sh.draw_line((x + s * 0.2, y + s * 0.4), (x + s * 0.62, y + s * 0.4))
        sh.draw_line((x + s / 2, y + s * 0.62), (x + s / 2, y + s * 0.78))
        sh.draw_line((x + s * 0.3, y + s), (x + s / 2, y + s * 0.78))
        sh.draw_line((x + s * 0.7, y + s), (x + s / 2, y + s * 0.78))
    sh.finish(color=SWAMP, fill=WHITE if kind == "model" else None, width=0.9, closePath=False, lineJoin=1, lineCap=1)
    sh.commit()


def section(pg, x, y, n):
    num, label, desc, _ = SECTIONS[n]
    pg.text(x, y, num, 9, GOLD, bold=True)
    pg.spaced(x + 17, y, label, 7.6, SWAMP, bold=True, spacing=1.8)
    pg.text(x + 17, y + 10.5, desc, 7, GREY)


def chip(pg, cx, cy, verb, w=64, h=15, size=7.4, proposed=False):
    """Status chip.  Meaning is carried by the word; fill and outline only reinforce it."""
    x, y = cx - w / 2, cy - h / 2
    if proposed:
        ink = BLACK if verb == "Trains" else SWAMP
        pg.box(x, y, w, h, fill=WHITE, stroke=ink, width=0.8, radius=h / 2)
        pg.text(cx, cy + size * 0.36, verb, size, ink, bold=True, align=1)
        return
    if verb == "Trains":
        pg.box(x, y, w, h, fill=BLACK, stroke=None, radius=h / 2)
        pg.text(cx, cy + size * 0.36, verb, size, WHITE, bold=True, align=1)
    elif verb == "Reinforces":
        pg.box(x, y, w, h, fill=MOAWHANGO, stroke=None, radius=h / 2)
        pg.text(cx, cy + size * 0.36, verb, size, SWAMP, bold=True, align=1)
    else:
        pg.box(x, y, w, h, fill=WHITE, stroke=MID, width=0.8, radius=h / 2)
        pg.text(cx, cy + size * 0.36, verb, size, INK, align=1)


def label_chip(pg, x, y, text, size=6.8, h=13, pad=7):
    """Small outlined label chip; returns its width."""
    w = pg.width(text, size) + pad * 2
    pg.box(x, y, w, h, fill=WHITE, stroke=GRID, width=0.8, radius=h / 2)
    pg.text(x + pad, y + h / 2 + size * 0.36, text, size, INK)
    return w


def spine_card(pg, x, y, w, h, spine_w, spine_text, spine_size=9.5):
    """Pale card with a black spine on the left carrying a short identifier."""
    pg.box(x, y, w, h, fill=FAINT, stroke=None, radius=R)
    pg.box(x, y, spine_w + R, h, fill=BLACK, stroke=None, radius=R)
    pg.box(x + spine_w, y, R + 1, h, fill=FAINT, stroke=None)
    pg.text(x + spine_w / 2, y + h / 2 + spine_size * 0.36, spine_text, spine_size, WHITE, bold=True, align=1)


# ---- page ------------------------------------------------------------------
LOGO_REVERSED = "./assets/nz-army-logo-white.png"


def reversed_logo_png():
    import io
    from PIL import Image
    im = Image.open(LOGO_REVERSED).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue(), im.size


def masthead(pg):
    """Compact split masthead: Army-red brand block with the reversed logo,
    then a pale title field.  The only red on the page."""
    pg.text(W / 2, 20, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 22, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(M, H - 11, FOOTER_LEFT, 7.5, BLACK)
    pg.text(W / 2, H - 11, "ACS 2026", 7.5, BLACK, align=1)
    pg.text(W - M, H - 11, page_label(1, 1), 7.5, BLACK, align=2)

    top, hh = 30, 46
    brand_w = 138
    # one softened band: pale field with rounded outer corners, red brand block sharing
    # the left corners and meeting the field on a straight seam
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


def build():
    doc = pymupdf.open()
    pg = Page(doc, W, H)
    y = masthead(pg) + 24

    # ---- 01 MODEL: three cards in sequence, the third opens the system ----
    section(pg, M, y, 1)
    y += 18
    gap = 22
    cw = (CW - gap * 2) / 3
    spine = 26
    h = 58
    for i, (num, role, term, desc) in enumerate(MODEL):
        x = M + i * (cw + gap)
        pg.box(x, y, cw, h, fill=FAINT, stroke=None, radius=R)
        pg.box(x, y, spine + R, h, fill=BLACK, stroke=None, radius=R)
        pg.box(x + spine, y, R + 1, h, fill=FAINT, stroke=None)
        pg.text(x + spine / 2, y + 22, num, 13, GOLD, bold=True, align=1)
        bx, bw = x + spine + 10, cw - spine - 18
        pg.spaced(bx, y + 14, role, 5.6, SWAMP, bold=True, spacing=1.3)
        pg.text(bx, y + 27, term, 9.5, BLACK, bold=True)
        para(pg, bx, y + 39, desc, 6.9, bw, lh=8.6)
        if i < 2:
            arrow_right(pg, x + cw + 4, x + cw + gap - 4, y + h / 2)
    model_bottom = y + h
    third_cx = M + 2 * (cw + gap) + cw / 2

    # continuation: from the third card down and across into 02, the start of the system
    y = model_bottom + 9
    sec2_y = y + 17

    # ---- 02 DEVELOPMENT: a rising staircase, stage 4 the destination ----
    section(pg, M, sec2_y, 2)
    y = sec2_y + 10
    gap = 14
    sw = (CW - gap * 3) / 4
    base_h, rise = 44, 6
    fills = [FAINT, PALE, OLIVE_LIGHT, BLACK]
    bottom = y + base_h + rise * 3
    for i, (num, name, desc) in enumerate(STEPS):
        hh = base_h + rise * i
        top = bottom - hh
        x = M + i * (sw + gap)
        final = i == 3
        pg.box(x, top, sw, hh, fill=fills[i], stroke=None, radius=R)
        pg.text(x + 12, top + 18, num, 12, GOLD, bold=True)
        pg.text(x + 28, top + 18, name, 9.5, WHITE if final else BLACK, bold=True)
        para(pg, x + 12, top + 32, desc, 7, sw - 24, color=GRID if final else INK, lh=8.6)
        if i < 3:
            arrow_right(pg, x + sw + 3, x + sw + gap - 3, top + 14)
    # anchor statement: a quiet band closing the pathway
    y = bottom + 7
    band_h = 20
    pg.box(M, y, CW, band_h, fill=PALE, stroke=None, radius=R)
    pg.text(W / 2, y + band_h / 2 + 3.3, STEPS_REINFORCE, 9, SWAMP, bold=True, align=1)
    y += band_h

    # ---- 03 RESPONSIBILITY (left) and 04 DELIVERY (right) ----
    top = y + 26
    lw = 300
    rx = M + lw + 30
    rw = CW - lw - 30

    section(pg, M, top, 3)
    y = top + 18
    sp = 70
    rh = 30
    gapv = 6
    n = len(RESPONSIBILITIES)
    chain_x = M + sp / 2
    for i, (org, func, role) in enumerate(RESPONSIBILITIES):
        last = i == n - 1
        hh = 42 if last else rh
        spine_card(pg, M, y, lw, hh, sp, org, spine_size=8.5 if len(org) > 6 else 9.5)
        pg.spaced(M + sp + 10, y + 11, func.upper(), 5.6, SWAMP, bold=True, spacing=1.3)
        pg.text(M + sp + 10, y + 22, role, 7, INK)
        if last:
            cx = M + sp + 10
            for name in PROVIDER_CHIPS:
                cx += label_chip(pg, cx, y + 27, name) + 5
        if not last:
            arrow_down(pg, chain_x, y + hh, y + hh + gapv)
        y += hh + gapv
    chain_bottom = y - gapv
    # advisers sit beside the chain, not in it: a dashed connector from the chain's right edge
    y += 4
    eh = 34
    pg.box(M, y, lw, eh, fill=WHITE, stroke=GRID, width=0.8, radius=R)
    pg.spaced(M + 12, y + 12, ADVISERS[0], 5.8, SWAMP, bold=True, spacing=1.5)
    cx = M + 12
    for name in ADVISERS[1]:
        cx += label_chip(pg, cx, y + 17, name) + 5
    pg.text(cx + 4, y + 26.5, ADVISERS[2], 7, INK)
    adv_mid = y + eh / 2
    dx = M + lw + 10
    top_mid = top + 18 + rh / 2
    dashed(pg, M + lw, top_mid, dx, top_mid)
    dashed(pg, dx, top_mid, dx, adv_mid)
    dashed(pg, M + lw, adv_mid, dx, adv_mid)
    left_end = y + eh

    section(pg, rx, top, 4)
    y = top + 20
    label_w = 96
    col_w = (rw - label_w) / 4
    hh = 32
    for j, name in enumerate(MATRIX_COLS):
        x = rx + label_w + j * col_w
        final = j == 3
        pg.box(x + 2, y, col_w - 4, hh, fill=BLACK if final else FAINT, stroke=None, radius=4)
        pg.text(x + 8, y + 11.5, str(j + 1), 8, GOLD, bold=True)
        lines = wrapped(pg, name, 6.8, col_w - 16, bold=True)
        ty = y + 23 if len(lines) == 1 else y + 19.5
        for line in lines:
            pg.text(x + 8, ty, line, 6.8, WHITE if final else BLACK, bold=True)
            ty += 8
    pg.spaced(rx, y + hh - 6, "ACS DELIVERY", 5.6, SWAMP, bold=True, spacing=1.3)
    y += hh + 4
    rh = 28
    for org, sub, verbs in MATRIX:
        pg.box(rx, y, rw, rh, fill=FAINT, stroke=None, radius=4)
        pg.text(rx + 10, y + 12, org, 8, BLACK, bold=True)
        pg.text(rx + 10, y + 22, sub, 6.8, GREY)
        if sub == "Combat Mindset Conditioning":
            # red outline: points the reader to the CMC page in the pack
            tw = max(pg.width(org, 8, True), pg.width(sub, 6.8))
            pg.box(rx + 5, y + 2.5, tw + 9, rh - 5, fill=None, stroke=ARMY_RED, width=1.1, radius=3)
        for j, verb in enumerate(verbs):
            chip(pg, rx + label_w + j * col_w + col_w / 2, y + rh / 2, verb)
        y += rh + 4

    # ---- scale option: delivery beyond ACS, drawn as a proposal ----
    y += 8
    lab_w = pg.spaced(rx, y, SCALE_LABEL, 5.6, GOLD, bold=True, spacing=1.3)
    pg.text(rx + lab_w + 8, y, SCALE_NOTE, 6.4, GREY)
    y += 6
    org, sub, verbs = MATRIX_SCALE
    srh = 32
    dashed_box(pg, rx, y, rw, srh, radius=4)
    pg.text(rx + 10, y + 12, org, 8, SWAMP, bold=True)
    sy = y + 21
    for line in sub.split("\n"):
        pg.text(rx + 10, sy, line, 6.2, GREY)
        sy += 7.5
    for j, verb in enumerate(verbs):
        chip(pg, rx + label_w + j * col_w + col_w / 2, y + srh / 2, verb, proposed=True)
    y += srh + 8

    x = rx
    for verb, definition in VERBS:
        item_w = 50 + pg.width(definition, 6.8)
        if x + item_w > rx + rw:
            x = rx
            y += 15
        chip(pg, x + 22, y + 1, verb, w=44, h=13, size=6.4)
        pg.text(x + 50, y + 3.4, definition, 6.8, INK)
        x += item_w + 12
    right_end = y + 8
    print(f"left ends {left_end:.0f}, right ends {right_end:.0f}, footer marking at {H - 30}")

    doc.set_metadata({"title": "Army Combat Mindset System: AITC Discussion",
                      "author": "Army Command School"})
    doc.save(OUT, garbage=3, deflate=True)
    pymupdf.open(OUT)[0].get_pixmap(dpi=200).save(PNG)
    print(f"Saved {OUT} and {PNG}")


if __name__ == "__main__":
    build()
