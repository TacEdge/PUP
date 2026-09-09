#!/usr/bin/env python3
"""
The two-page AITC discussion piece in the NZALC house style: same content
and geometry as the wireframes (imported from build_ldf_wireframes), drawn
with the palette, Arial, the NZ Army logo and the protective marking used
on the course data sheets.

    python3 build_ldf_discussion_piece.py -> output/ldf-alignment-discussion-piece.pdf
"""

import io
import math

import pymupdf
from PIL import Image

import build_ldf_wireframes as wf

OUT = "./output/ldf-alignment-discussion-piece.pdf"
LOGO_FILE = "./assets/nz-army-logo.png"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FOOTER_LEFT = "NZALC | Leadership Development Discussion Piece"
FOOTER_REF = "ACS 2026"
MARKING = "UNCLASSIFIED"
ORIGINATOR = "New Zealand Army Leadership Centre | Army Command School"
DATE = "September 2026"
STATUS = "Draft for AITC discussion"
KICKER = "AITC DISCUSSION PIECE"

W, H = 842, 595
M = 40


def rgb(hexs):
    return tuple(int(hexs[i:i + 2], 16) / 255 for i in (0, 2, 4))


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

_reg = pymupdf.Font(fontfile=FONT_REG)
_bold = pymupdf.Font(fontfile=FONT_BOLD)


def logo_png():
    im = Image.open(LOGO_FILE).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue(), im.size


class Page:
    def __init__(self, doc, number, total, title, subtitle):
        self.p = doc.new_page(width=W, height=H)
        self.p.insert_font(fontname="Arial", fontfile=FONT_REG)
        self.p.insert_font(fontname="Arial-Bold", fontfile=FONT_BOLD)
        # protective marking, top and bottom
        self.text(W / 2, 24, MARKING, 8.5, BLACK, bold=True, align=1)
        self.text(W / 2, H - 28, MARKING, 8.5, BLACK, bold=True, align=1)
        # footer
        self.text(M, H - 16, FOOTER_LEFT, 8, BLACK)
        self.text(W / 2, H - 16, FOOTER_REF, 8, BLACK, align=1)
        self.text(W - M, H - 16, f"Page {number} of {total}", 8, BLACK, align=2)
        # letterhead
        png, (iw, ih) = logo_png()
        lh = 22
        self.p.insert_image(pymupdf.Rect(M, 32, M + lh * iw / ih, 32 + lh), stream=png)
        self.spaced(M, 68, KICKER, 7, SWAMP, bold=True, spacing=1.6)
        self.text(M, 86, title, 17, BLACK, bold=True)
        self.spaced(M, 99, subtitle.upper(), 7, SWAMP, bold=True, spacing=1.2)
        self.line(M, 105, W - M, 105, ARMY_RED, width=2)
        self.text(M, 116, ORIGINATOR, 8, SWAMP)
        x = W - M
        for s, bold, col in ((STATUS, True, ARMY_RED), ("Status: ", True, BLACK), ("   ·   ", False, MID),
                             (DATE, False, BLACK), ("Date: ", True, BLACK)):
            x -= self.width(s, 7.5, bold)
            self.text(x, 116, s, 7.5, col, bold=bold)

    # --- primitives
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

    def textbox(self, x, y, w, h, s, size=8, color=INK, bold=False, align=0, lh=1.25):
        self.p.insert_textbox(pymupdf.Rect(x, y, x + w, y + h), s, fontsize=size,
                              fontname="Arial-Bold" if bold else "Arial", color=color, align=align, lineheight=lh)

    def line(self, x0, y0, x1, y1, color=GRID, width=0.8, dashes=None):
        sh = self.p.new_shape()
        sh.draw_line((x0, y0), (x1, y1))
        sh.finish(color=color, width=width, dashes=dashes)
        sh.commit()

    def box(self, x, y, w, h, fill=None, stroke=GRID, width=0.8, dashes=None):
        sh = self.p.new_shape()
        sh.draw_rect(pymupdf.Rect(x, y, x + w, y + h))
        sh.finish(color=stroke, fill=fill, width=width, dashes=dashes)
        sh.commit()

    def polygon(self, pts, fill=None, stroke=None, width=0.8):
        sh = self.p.new_shape()
        sh.draw_polyline(pts + [pts[0]])
        sh.finish(color=stroke, fill=fill, width=width, closePath=True)
        sh.commit()

    def arrow(self, x0, y0, x1, y1, color=GOLD, width=1.1):
        sh = self.p.new_shape()
        sh.draw_line((x0, y0), (x1, y1))
        ang = math.atan2(y1 - y0, x1 - x0)
        for d in (2.6, -2.6):
            sh.draw_line((x1, y1), (x1 - 6 * math.cos(ang + d), y1 - 6 * math.sin(ang + d)))
        sh.finish(color=color, width=width)
        sh.commit()

    def labelled(self, x, y, w, h, label, fill, size, color, bold=True, stroke=None, spaced=0):
        self.box(x, y, w, h, fill=fill, stroke=stroke)
        lines = label.split("\n")
        ty = y + h / 2 - len(lines) * (size + 2) / 2 + size
        for ln in lines:
            if spaced:
                self.spaced(x + w / 2, ty, ln, size, color, bold=bold, spacing=spaced, align=1)
            else:
                self.text(x + w / 2, ty, ln, size, color, bold=bold, align=1)
            ty += size + 2


def cell(pg, x, y, w, h, entry):
    rank, course, status, qual = entry
    mandated = status == "MANDATED"
    pg.box(x, y, w, h, fill=PALE if mandated else WHITE, stroke=SWAMP if mandated else MOAWHANGO,
           width=1.1 if mandated else 0.9)
    pg.text(x + w / 2, y + 11, rank, 8.5, BLACK, bold=True, align=1)
    pg.text(x + w / 2, y + 19.5, course, 7, INK, align=1)
    pg.spaced(x + w / 2, y + 29.5, status, 8, SWAMP if mandated else INK, bold=True, spacing=0.8, align=1)
    if qual:
        pg.text(x + w / 2, y + 35.8, qual, 5.8, MID, align=1)


def page1(doc):
    pg = Page(doc, 1, 2, "Two continuums. One leadership framework.", wf.HEADLINE)
    spine_x, spine_w = W / 2 - 66, 132
    col_w = spine_x - M - 30
    top, rowh, lvl_h = 142, 56, 15
    pg.labelled(M, top - 18, col_w, 14, "OFFICER CONTINUUM", SWAMP, 6.5, WHITE, spaced=1.2)
    pg.labelled(spine_x, top - 18, spine_w, 14, "LEADERSHIP FRAMEWORK", SWAMP, 6.5, WHITE, spaced=1.2)
    pg.labelled(W - M - col_w, top - 18, col_w, 14, "SOLDIER CONTINUUM", SWAMP, 6.5, WHITE, spaced=1.2)
    for i, lvl in enumerate(wf.LEVELS):
        y = top + i * rowh
        pg.labelled(spine_x + 8, y, spine_w - 16, lvl_h, lvl.replace("\n", " "), MOAWHANGO, 6.2, SWAMP)
        if i < 6:
            ty, th = y + lvl_h + 2, rowh - lvl_h - 4
            mid = ty + th / 2
            pg.line(M, mid, W - M, mid, GRID, dashes="[1 2] 0")
            pg.arrow(W / 2, y + lvl_h, W / 2, y + rowh - 1)
            pg.text(W / 2 + 8, mid + 2, f"T{i + 1}", 6, MID)
            cell(pg, M, ty, col_w, th, wf.OFFICER[i])
            cell(pg, W - M - col_w, ty, col_w, th, wf.SOLDIER[i])
    y = top + 6 * rowh + lvl_h + 7
    pg.box(M, y, W - 2 * M, 26, fill=SWAMP, stroke=None)
    pg.spaced(W / 2, y + 17.5, wf.PAGE1_CLOSE.upper(), 10.5, WHITE, bold=True, spacing=0.6, align=1)
    pg.text(M, y + 35, "Shaded: mandated in policy or embedded in the qualifying course. Rank pairings follow the NZALC review of "
                       "9 September 2026 and place the comparison; they do not assert that a rank equals a level.", 6.3, MID)


def band(pg, y_mid, entries):
    n = len(entries)
    gapx = 12
    stw = (W - 2 * M - gapx * (n - 1)) / n
    xs = [M + k * (stw + gapx) for k in range(n)]
    top, bot = [], []
    for k, (_, status) in enumerate(entries):
        half = 4 + wf.LEVEL[status] * 7
        cx = xs[k] + stw / 2
        top.append((cx, y_mid - half))
        bot.append((cx, y_mid + half))
    top = [(M, top[0][1])] + top + [(W - M, top[-1][1])]
    bot = [(M, bot[0][1])] + bot + [(W - M, bot[-1][1])]
    pg.polygon(top + bot[::-1], fill=MOAWHANGO, stroke=None)
    for k, (rank, status) in enumerate(entries):
        cx = xs[k] + stw / 2
        pg.spaced(cx, y_mid + 2.5, status, 7, SWAMP, bold=True, spacing=0.7, align=1)
        pg.text(cx, y_mid + 42, rank, 6.8, INK, align=1)
    return xs, stw


def page2(doc):
    pg = Page(doc, 2, 2, "Where is development deliberately linked to progression?",
              "The two continuums at the same transitions, then the question for Army")
    n = len(wf.STAGES)
    gapx = 12
    stw = (W - 2 * M - gapx * (n - 1)) / n
    for k, t in enumerate(wf.STAGES):
        pg.text(M + k * (stw + gapx) + stw / 2, 134, t, 6.5, MID, bold=True, align=1)
        if k:
            xk = M + k * (stw + gapx) - gapx / 2
            pg.line(xk, 128, xk, 336, GRID, dashes="[1 2] 0")
    pg.spaced(M, 148, "OFFICER", 7, SWAMP, bold=True, spacing=1.2)
    band(pg, 182, wf.OFFICER_STAGES)
    pg.spaced(M, 248, "SOLDIER", 7, SWAMP, bold=True, spacing=1.2)
    band(pg, 282, wf.SOLDIER_STAGES)
    pg.text(M, 344, "Band thickness is the strength of the link between the development and the career transition: "
                    "mandated, functionally required, expected, self-selected.", 6.3, MID)

    pg.box(M, 356, W - 2 * M, 30, fill=WHITE, stroke=SWAMP, width=1.4)
    pg.textbox(M + 12, 362, W - 2 * M - 24, 22, wf.PAGE2_STATEMENT, 8.5, SWAMP, bold=True, align=1, lh=1.2)

    fy = 404
    cw = (W - 2 * M - 24) / 3
    for k, (head, body) in enumerate(wf.FACTS):
        x = M + k * (cw + 12)
        pg.spaced(x, fy, head, 6.5, SWAMP, bold=True, spacing=1.2)
        pg.textbox(x, fy + 5, cw, 30, body, 7.8, INK, lh=1.25)

    qy = 444
    pg.box(M, qy, W - 2 * M, 82, fill=SWAMP, stroke=None)
    pg.spaced(W / 2, qy + 24, "IS THIS A CONSCIOUS CHOICE?", 15, WHITE, bold=True, spacing=0.8, align=1)
    half = (W - 2 * M - 100) / 2
    pg.text(M + 40, qy + 42, "IF YES", 7, MOAWHANGO, bold=True)
    pg.textbox(M + 40, qy + 46, half, 32, wf.IF_YES, 8, WHITE, lh=1.25)
    pg.text(W / 2 + 10, qy + 42, "IF NO", 7, MOAWHANGO, bold=True)
    pg.textbox(W / 2 + 10, qy + 46, half, 32, wf.IF_NO, 8, WHITE, lh=1.25)
    pg.text(W / 2, qy + 96, "No recommendation. The organisation answers.", 7, MID, align=1)


def build():
    doc = pymupdf.open()
    page1(doc)
    page2(doc)
    doc.set_metadata({"title": "Officer and Soldier Leadership Development: AITC Discussion Piece",
                      "author": "New Zealand Army Leadership Centre"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
