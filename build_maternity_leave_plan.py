#!/usr/bin/env python3
"""
Maternity leave plan one-pager in the NZ Army house style: letterhead,
status block, leave timeline and leave sequence.

    python3 build_maternity_leave_plan.py -> output/kate-beckett-maternity-leave-plan.pdf
"""

import datetime as dt
import io

import pymupdf
from PIL import Image

OUT = "./output/kate-beckett-maternity-leave-plan.pdf"
LOGO_FILE = "./assets/nz-army-logo.png"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

KICKER = "MATERNITY LEAVE PLAN"
TITLE = "Mrs Kate Beckett"
SUBTITLE = "Status as at 10 September 2026   ·   Planned return to work: 28 January 2028"
ORIGINATOR = "Army Command School"
DATE = "September 2026"
FOOTER_LEFT = "Kate Beckett | Maternity Leave Plan"
FOOTER_REF = "ACS 2026"
MARKING = "UNCLASSIFIED"

STATUS = [
    ("CURRENT STATUS", "Working as normal. Leave commences 21 December 2026."),
    ("RETURN", "28 January 2028. FTE to be confirmed in late November 2027."),
    ("COURSE DELIVERY", "Covered by Preferred Contractors throughout the absence."),
]
COVER_LABEL = "Course delivery covered by Preferred Contractors"

D = dt.date
SPAN = (D(2026, 9, 1), D(2028, 1, 31))
TODAY = D(2026, 9, 10)
CONFIRM_FTE = (D(2027, 11, 20), "Late Nov 2027: confirm FTE")
RETURN = (D(2028, 1, 28), "RETURN 28 JAN 2028")

# (start, end inclusive, label, short label for the bar, colour key)
LEAVE = [
    (D(2026, 12, 21), D(2027, 1, 11), "Christmas leave (Annual leave)", "Christmas leave", "pale"),
    (D(2027, 1, 12), D(2027, 1, 12), "Equivalent leave", "", "grid"),
    (D(2027, 1, 13), D(2027, 1, 29), "Stand-down leave", "Stand-down", "grid"),
    (D(2027, 1, 30), D(2027, 2, 18), "Special parental leave", "Special parental", "gold"),
    (D(2027, 2, 19), D(2027, 4, 12), "Annual leave", "Annual leave", "moawhango"),
    (D(2027, 4, 13), D(2028, 1, 27), "Parental leave", "Parental leave", "swamp"),
]

W, H = 842, 595
M = 40


def rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


ARMY_RED = rgb("C62026")
BLACK = rgb("000000")
WHITE = rgb("FFFFFF")
SWAMP = rgb("002516")
GOLD = rgb("A89662")
MOAWHANGO = rgb("CDD2B7")
PALE = rgb("EEF1E5")
GRID = rgb("D9D9D2")
MID = rgb("8A8A8A")
INK = rgb("222222")
COLOURS = {"pale": (PALE, SWAMP), "grid": (GRID, INK), "gold": (GOLD, WHITE),
           "moawhango": (MOAWHANGO, SWAMP), "swamp": (SWAMP, WHITE)}

_reg = pymupdf.Font(fontfile=FONT_REG)
_bold = pymupdf.Font(fontfile=FONT_BOLD)


def logo_png():
    im = Image.open(LOGO_FILE).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue(), im.size


class Page:
    def __init__(self, doc):
        self.p = doc.new_page(width=W, height=H)
        self.p.insert_font(fontname="Arial", fontfile=FONT_REG)
        self.p.insert_font(fontname="Arial-Bold", fontfile=FONT_BOLD)

    def width(self, s, size, bold=False):
        return (_bold if bold else _reg).text_length(s, fontsize=size)

    def text(self, x, y, s, size=9, color=INK, bold=False, align=0):
        if align:
            tw = self.width(s, size, bold)
            x = x - tw if align == 2 else x - tw / 2
        self.p.insert_text((x, y), s, fontsize=size, fontname="Arial-Bold" if bold else "Arial", color=color)

    def spaced(self, x, y, s, size, color, bold=False, spacing=1.0, align=0):
        font = _bold if bold else _reg
        total = sum(font.text_length(c, fontsize=size) + spacing for c in s) - spacing
        if align:
            x = x - total if align == 2 else x - total / 2
        for c in s:
            self.p.insert_text((x, y), c, fontsize=size, fontname="Arial-Bold" if bold else "Arial", color=color)
            x += font.text_length(c, fontsize=size) + spacing
        return total

    def line(self, x0, y0, x1, y1, color=GRID, width=0.8, dashes=None):
        sh = self.p.new_shape()
        sh.draw_line((x0, y0), (x1, y1))
        sh.finish(color=color, width=width, dashes=dashes)
        sh.commit()

    def box(self, x, y, w, h, fill=None, stroke=GRID, width=0.8, radius=0):
        sh = self.p.new_shape()
        r = pymupdf.Rect(x, y, x + w, y + h)
        if radius:
            sh.draw_rect(r, radius=(min(radius / w, 0.5), min(radius / h, 0.5)))
        else:
            sh.draw_rect(r)
        sh.finish(color=stroke, fill=fill, width=width)
        sh.commit()


def letterhead(pg):
    pg.text(W / 2, 24, MARKING, 8.5, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 28, MARKING, 8.5, BLACK, bold=True, align=1)
    pg.text(M, H - 16, FOOTER_LEFT, 8, BLACK)
    pg.text(W / 2, H - 16, FOOTER_REF, 8, BLACK, align=1)
    pg.text(W - M, H - 16, "Page 1 of 1", 8, BLACK, align=2)
    png, (iw, ih) = logo_png()
    lh = 22
    pg.p.insert_image(pymupdf.Rect(M, 32, M + lh * iw / ih, 32 + lh), stream=png)
    pg.spaced(M, 68, KICKER, 7, SWAMP, bold=True, spacing=1.6)
    pg.text(M, 86, TITLE, 17, BLACK, bold=True)
    pg.line(M, 94, W - M, 94, ARMY_RED, width=2)
    pg.text(M, 105, ORIGINATOR, 8, SWAMP)
    x = W - M
    for s, bold in ((DATE, False), ("Date: ", True)):
        x -= pg.width(s, 7.5, bold)
        pg.text(x, 105, s, 7.5, BLACK, bold=bold)


def status_block(pg, y):
    h = 16 * len(STATUS) + 12
    pg.box(M, y, W - 2 * M, h, fill=PALE, stroke=None, radius=3)
    pg.box(M, y + 4, 3.5, h - 8, fill=SWAMP, stroke=None)
    for k, (label, value) in enumerate(STATUS):
        ly = y + 17 + k * 16
        pg.spaced(M + 14, ly, label, 7, SWAMP, bold=True, spacing=1.4)
        pg.text(M + 120, ly, value, 9, INK)
    return y + h


def timeline(pg, y, h):
    x0, x1 = M, W - M
    total = (SPAN[1] - SPAN[0]).days

    def xof(d):
        return x0 + (d - SPAN[0]).days / total * (x1 - x0)

    # month grid and labels
    d = D(SPAN[0].year, SPAN[0].month, 1)
    months = []
    while d <= SPAN[1]:
        months.append(d)
        d = D(d.year + (d.month == 12), d.month % 12 + 1, 1)
    bar_y, bar_h = y + 50, 34
    for k, m in enumerate(months):
        mx = xof(m)
        pg.line(mx, y + 26, mx, y + h, GRID, width=0.5)
        nxt = months[k + 1] if k + 1 < len(months) else D(2028, 2, 1)
        cx = (mx + xof(min(nxt, SPAN[1] + dt.timedelta(days=1)))) / 2
        pg.text(cx, y + 22, m.strftime("%b"), 6.5, MID, align=1)
        if m.month == 1 or k == 0:
            pg.text(cx, y + 11, str(m.year), 7, SWAMP, bold=True, align=1)
    # working period before leave, as a faint bar
    pg.box(x0, bar_y, xof(LEAVE[0][0]) - x0, bar_h, fill=rgb("F6F6F3"), stroke=None)
    pg.text((x0 + xof(LEAVE[0][0])) / 2, bar_y + bar_h / 2 + 3, "Working as normal", 7, MID, align=1)
    # leave segments; short ones get a staggered callout beneath the bar
    callout = 0
    for start, end, label, short, key in LEAVE:
        fill, col = COLOURS[key]
        sx, ex = xof(start), xof(end + dt.timedelta(days=1))
        pg.box(sx, bar_y, ex - sx, bar_h, fill=fill, stroke=WHITE, width=0.6)
        if not short:
            continue
        wide = ex - sx
        if wide > 60:
            pg.text((sx + ex) / 2, bar_y + bar_h / 2 - 1, short, 7.5, col, bold=True, align=1)
            pg.text((sx + ex) / 2, bar_y + bar_h / 2 + 9, f"{start:%-d %b} to {end:%-d %b %Y}", 6, col, align=1)
        else:
            cx = sx + wide / 2
            ly = bar_y + bar_h + 14 + callout * 13
            pg.line(cx, bar_y + bar_h, cx, ly - 2, MID, width=0.6)
            pg.line(cx, ly - 2, cx + 6, ly - 2, MID, width=0.6)
            pg.text(cx + 9, ly, f"{short}   {start:%-d %b} to {end:%-d %b %Y}", 6.5, INK)
            callout += 1
    # cover band across the absence
    csx, cex = xof(LEAVE[0][0]), xof(LEAVE[-1][1] + dt.timedelta(days=1))
    cy = bar_y - 14
    pg.box(csx, cy, cex - csx, 10, fill=WHITE, stroke=SWAMP, width=0.7, radius=2)
    pg.text((csx + cex) / 2, cy + 7.3, COVER_LABEL.upper(), 5.6, SWAMP, bold=True, align=1)
    # markers
    tx = xof(TODAY)
    pg.line(tx, y + 28, tx, y + h, ARMY_RED, width=1.2)
    pg.text(tx + 3, y + h - 3, "TODAY", 6.5, ARMY_RED, bold=True)
    cx = xof(CONFIRM_FTE[0])
    pg.line(cx, y + 28, cx, y + h, BLACK, width=0.8, dashes="[3 2] 0")
    pg.text(cx - 3, bar_y + bar_h + 14, CONFIRM_FTE[1], 6.5, BLACK, bold=True, align=2)
    rx = xof(RETURN[0])
    pg.line(rx, y + 28, rx, y + h, SWAMP, width=1.4)
    pg.text(rx - 3, y + h - 3, RETURN[1], 6.5, SWAMP, bold=True, align=2)
    return y + h


def sequence(pg, y):
    pg.spaced(M, y, "LEAVE SEQUENCE", 7, SWAMP, bold=True, spacing=1.6)
    pg.line(M, y + 5, W - M, y + 5, GRID)
    cols = 3
    cw = (W - 2 * M) / cols
    for k, (start, end, label, short, key) in enumerate(LEAVE):
        cx = M + (k % cols) * cw
        cy = y + 22 + (k // cols) * 30
        fill, col = COLOURS[key]
        pg.box(cx, cy - 8, 8, 8, fill=fill, stroke=None, radius=2)
        dates = f"{start:%-d %b %y}" if start == end else f"{start:%-d %b %y} to {end:%-d %b %y}"
        pg.text(cx + 14, cy, dates, 8, BLACK, bold=True)
        pg.text(cx + 14, cy + 11, label, 8, INK)


def build():
    doc = pymupdf.open()
    pg = Page(doc)
    letterhead(pg)
    y = status_block(pg, 119)
    y = timeline(pg, y + 16, 156)
    sequence(pg, y + 34)
    doc.set_metadata({"title": "Kate Beckett: Maternity Leave Plan", "author": "Army Command School"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
