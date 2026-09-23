#!/usr/bin/env python3
"""
Performance Under Pressure: the Gazing Performance Systems model redrawn in
the NZ Army house style for internal use.

    python3 build_performance_under_pressure.py
        -> output/performance-under-pressure.pdf (+ .png preview)

Content follows the Gazing sheet (2010).  Two items on the source copy were
under glare and are reconstructed: the left-hand header ("OFF TASK / Outcome",
mirroring "ON TASK / Process") and the second word of "Filters · Choices".
"""

import math

import pymupdf

from army_onepager import (ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, MID, PALE, SWAMP, WHITE,
                           Page, rgb)
from build_army_combat_mindset_development_system import reversed_logo_png

OUT = "./output/performance-under-pressure.pdf"
PNG = "./output/performance-under-pressure.png"
W, H = 842, 595
M = 40
CW = W - 2 * M
R = 6

TITLE = "Performance Under Pressure"
SUBTITLE = "The prime issue is control of attention"
ORIGINATOR = "Army Command School"
DATE = "September 2026"
FOOTER_LEFT = "Performance Under Pressure | Internal use only"
FOOTER_RIGHT = "Adapted from Gazing Performance Systems, 2010"

# the model's own red/blue semantics, held to muted tones
BLUE = rgb("2F5D8A")
BLUE_PALE = rgb("D6E0EA")
RED_PALE = rgb("EFD3D3")
PURPLE = rgb("74567F")
GREY = rgb("5F5F5A")


# ---- primitives ------------------------------------------------------------
def circle(pg, cx, cy, r, fill=None, stroke=None, width=1):
    sh = pg.p.new_shape()
    sh.draw_circle((cx, cy), r)
    sh.finish(color=stroke, fill=fill, width=width)
    sh.commit()


def poly(pg, pts, fill=None, stroke=None, width=1):
    sh = pg.p.new_shape()
    sh.draw_polyline(pts)
    sh.finish(color=stroke, fill=fill, width=width, closePath=True)
    sh.commit()


def head(pg, x, y, size, color, angle):
    """Filled arrowhead with its tip at (x, y), pointing along `angle` (radians, 0 = right)."""
    ux, uy = math.cos(angle), math.sin(angle)
    px, py = -uy, ux
    bx, by = x - ux * size * 1.4, y - uy * size * 1.4
    poly(pg, [(bx + px * size * 0.8, by + py * size * 0.8), (bx - px * size * 0.8, by - py * size * 0.8), (x, y)], fill=color)


def arrow(pg, x0, y0, x1, y1, color, width=1.2, size=4):
    ang = math.atan2(y1 - y0, x1 - x0)
    pg.line(x0, y0, x1 - math.cos(ang) * size, y1 - math.sin(ang) * size, color, width=width)
    head(pg, x1, y1, size, color, ang)


def letter_row(pg, x, y, letter, word, color, size=7.5):
    """Coloured initial in a disc, then the rest of the word."""
    circle(pg, x + 5.5, y - 2.6, 5.5, fill=color)
    pg.text(x + 5.5, y - 0.4, letter, 6.2, WHITE, bold=True, align=1)
    pg.text(x + 15, y, word, size, INK)


def centred_lines(pg, cx, y, lines, size, color, bold=False, lh=None):
    lh = lh or size * 1.25
    for s in lines:
        pg.text(cx, y, s, size, color, bold=bold, align=1)
        y += lh
    return y


def node(pg, cx, cy, lines, color, w=58, h=22):
    pg.box(cx - w / 2, cy - h / 2, w, h, fill=WHITE, stroke=color, width=1, radius=h / 2)
    y = cy - (len(lines) - 1) * 3.6 + 2.3
    for s in lines:
        pg.text(cx, y, s, 5.8, BLACK, bold=True, align=1)
        y += 7.2


def ring(pg, cx, cy, r, color, accent, width=7, arrows=3, clockwise=True):
    circle(pg, cx, cy, r, stroke=color, width=width)
    for k in range(arrows):
        a = -math.pi / 2 + k * 2 * math.pi / arrows + math.pi / arrows
        tx, ty = cx + r * math.cos(a), cy + r * math.sin(a)
        tangent = a + (math.pi / 2 if clockwise else -math.pi / 2)
        head(pg, tx + math.cos(tangent) * 4, ty + math.sin(tangent) * 4, 5, accent, tangent)


def gradient_axis(pg, x0, x1, y, h=5, steps=48):
    for i in range(steps):
        t = i / (steps - 1)
        c = tuple(ARMY_RED[k] + (BLUE[k] - ARMY_RED[k]) * t for k in range(3))
        xa = x0 + (x1 - x0) * i / steps
        xb = x0 + (x1 - x0) * (i + 1) / steps
        pg.box(xa, y - h / 2, xb - xa + 0.4, h, fill=c, stroke=None)
    head(pg, x0 - 6, y, 6, ARMY_RED, math.pi)
    head(pg, x1 + 6, y, 6, BLUE, 0)


# ---- page furniture --------------------------------------------------------
def masthead(pg):
    pg.text(W / 2, 20, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 22, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(M, H - 11, FOOTER_LEFT, 7.5, BLACK)
    pg.text(W / 2, H - 11, "ACS 2026", 7.5, BLACK, align=1)
    pg.text(W - M, H - 11, FOOTER_RIGHT, 7.5, BLACK, align=2)

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


def side_header(pg, cx, y, title, sub, color):
    w, h = 112, 30
    pg.box(cx - w / 2, y, w, h, fill=color, stroke=None, radius=4)
    pg.text(cx, y + 12.5, title, 8.5, WHITE, bold=True, align=1)
    pg.box(cx - w / 2 + 4, y + 17, w - 8, 10, fill=WHITE, stroke=None, radius=2)
    pg.text(cx, y + 24.5, sub, 6.6, BLACK, align=1)
    return y + h


def underlined(pg, cx, y, title, sub, half=72):
    pg.text(cx, y, title, 8, BLACK, bold=True, align=1)
    pg.line(cx - half, y + 4, cx + half, y + 4, BLACK, width=0.8)
    pg.text(cx, y + 15, sub, 7.2, INK, align=1)


# ---- build -----------------------------------------------------------------
def build():
    doc = pymupdf.open()
    pg = Page(doc, W, H)
    masthead(pg)

    cx = W / 2
    lx, rx = 180, W - 180           # centres of the two side panels

    # ---- centre: pressure -> thinking -> action, standing on the triangle ----
    y = 106
    for letter, word in (("E", "xpectation"), ("S", "crutiny"), ("C", "onsequences")):
        letter_row(pg, cx - 40, y, letter, word, BLACK, size=8)
        y += 14
    y = 150
    pg.box(cx - 66, y, 132, 26, fill=ARMY_RED, stroke=None, radius=R)
    pg.text(cx, y + 17.5, "PRESSURE", 11, WHITE, bold=True, align=1)
    arrow(pg, cx, y + 30, cx, y + 52, ARMY_RED, width=2.2, size=6)

    axis_y = 238
    gradient_axis(pg, 300, 542, axis_y)
    pg.text(304, axis_y - 6, "0%", 6.5, ARMY_RED, bold=True)
    pg.text(538, axis_y - 6, "100%", 6.5, BLUE, bold=True, align=2)

    # head silhouette
    hr = 36
    hy = 236
    circle(pg, cx, hy, hr, fill=BLACK)
    pg.box(cx - 12, hy + hr - 6, 24, 18, fill=BLACK, stroke=None)
    pg.text(cx, hy - 17, "THINKING", 7, WHITE, bold=True, align=1)
    pg.text(cx, hy - 5, "1.  RED  →  BLUE", 6.6, WHITE, bold=True, align=1)
    pg.text(cx, hy + 6, "2.  DECIDE", 6.6, WHITE, bold=True, align=1)
    pg.text(cx, hy + 17, "3.  DO", 6.6, WHITE, bold=True, align=1)
    head_bottom = hy + hr + 12

    # structure feeds thinking
    arrow(pg, cx, 326, cx, head_bottom + 6, BLUE, width=2.2, size=6)
    pg.text(cx, 340, "Structure", 8, BLACK, bold=True, align=1)

    # performance triangle
    apex, base, half = 348, 430, 66
    poly(pg, [(cx, apex), (cx + half, base), (cx - half, base)], fill=FAINT, stroke=BLUE, width=1.6)
    pg.text(cx, 397, "PERFORMANCE", 7.2, SWAMP, bold=True, align=1)
    pg.text(cx, 407, "TRIANGLE", 7.2, SWAMP, bold=True, align=1)
    pg.text(cx - half - 6, base + 12, "Skillset", 8, BLACK, bold=True, align=1)
    pg.text(cx + half + 6, base + 12, "Mindset", 8, BLACK, bold=True, align=1)
    # locus of control
    cy = 490
    for dx, fill, lines in ((-52, ARMY_RED, ["CAN'T", "CONTROL"]), (0, PURPLE, ["CAN", "INFLUENCE"]), (52, BLUE, ["CAN", "CONTROL"])):
        circle(pg, cx + dx, cy, 21, fill=fill)
        centred_lines(pg, cx + dx, cy - 1.5, lines, 5.6, WHITE, bold=True, lh=7)

    # ---- left: the myth ----------------------------------------------------
    y = side_header(pg, lx, 100, "OFF TASK", "Outcome", ARMY_RED)
    pg.text(lx, y + 18, "Filters  •  Choices", 7.2, BLACK, bold=True, align=1)
    lcy = 212
    ring(pg, lx, lcy, 40, RED_PALE, ARMY_RED, width=8)
    centred_lines(pg, lx, lcy - 6, ["NEGATIVE", "CONTENT", "LOOP"], 7.4, ARMY_RED, bold=True, lh=8.6)
    node(pg, lx, lcy - 40, ["Negative", "Perception"], ARMY_RED)
    node(pg, lx - 40, lcy + 26, ["Unhelpful", "Behaviours"], ARMY_RED)
    node(pg, lx + 40, lcy + 26, ["Emotional", "Response"], ARMY_RED)
    for i, (letter, word) in enumerate((("F", "IGHT"), ("F", "LIGHT"), ("F", "REEZE"))):
        letter_row(pg, 46, lcy - 6 + i * 15, letter, word, ARMY_RED)
    y = centred_lines(pg, lx, lcy + 62, ["Overload / Overwhelm", "Disconnect", "Past / Future"], 7.2, INK, lh=10.5)
    underlined(pg, lx, 344, "Attention split + fixated", "Assumptions  •  Expectations")
    for i, (letter, word) in enumerate((("A", "ggressive"), ("P", "assive"), ("E", "scape"))):
        letter_row(pg, lx - 34, 388 + i * 15, letter, word, BLACK, size=8)
    pg.text(lx, 500, "MYTH", 24, BLACK, bold=True, align=1)

    # ---- right: the reality -----------------------------------------------
    y = side_header(pg, rx, 100, "ON TASK", "Process", BLUE)
    pg.text(rx, y + 18, "Clarity  •  Decision", 7.2, BLACK, bold=True, align=1)
    rcy = 212
    ring(pg, rx, rcy, 40, BLUE_PALE, BLUE, width=8)
    node(pg, rx, rcy - 34, ["Situational", "Awareness"], BLUE)
    node(pg, rx, rcy + 34, ["Execution", "Accuracy"], BLUE)
    arrow(pg, rx, rcy - 4, rx, rcy - 20, BLUE, width=2, size=5)
    arrow(pg, rx, rcy + 4, rx, rcy + 20, BLUE, width=2, size=5)
    for i, (letter, word) in enumerate((("C", "LARITY"), ("I", "NTENSITY"), ("A", "CCURACY"))):
        letter_row(pg, rx + 62, rcy - 6 + i * 15, letter, word, BLUE)
    centred_lines(pg, rx, rcy + 62, ["Drivers  •  Threshold", "Connect", "Present"], 7.2, INK, lh=10.5)
    underlined(pg, rx, 344, "Attention focused + directed", "Adapt  •  Improvise  •  Overcome")
    for i, (letter, word) in enumerate((("A", "ccurate perception"), ("C", "hoice"), ("T", "ask focus"))):
        letter_row(pg, rx - 44, 388 + i * 15, letter, word, BLACK, size=8)
    pg.text(rx, 500, "REALITY", 24, BLACK, bold=True, align=1)

    doc.set_metadata({"title": "Performance Under Pressure", "author": "Army Command School"})
    doc.save(OUT, garbage=3, deflate=True)
    pymupdf.open(OUT)[0].get_pixmap(dpi=200).save(PNG)
    print(f"Saved {OUT} and {PNG}")


if __name__ == "__main__":
    build()
