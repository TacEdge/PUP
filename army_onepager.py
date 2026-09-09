"""
Shared house-style primitives for one-page NZ Army documents drawn with
PyMuPDF: palette, Arial via Liberation Sans, the NZ Army logo letterhead,
protective marking and the three-part footer.
"""

import io

import pymupdf
from PIL import Image

LOGO_FILE = "./assets/nz-army-logo.png"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MARKING = "UNCLASSIFIED"

W, H = 842, 595          # A4 landscape
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
FAINT = rgb("F6F6F3")

_reg = pymupdf.Font(fontfile=FONT_REG)
_bold = pymupdf.Font(fontfile=FONT_BOLD)


def logo_png():
    im = Image.open(LOGO_FILE).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue(), im.size


class Page:
    def __init__(self, doc, width=W, height=H):
        self.p = doc.new_page(width=width, height=height)
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

    def textbox(self, x, y, w, h, s, size=8, color=INK, bold=False, align=0, lh=1.25):
        self.p.insert_textbox(pymupdf.Rect(x, y, x + w, y + h), s, fontsize=size,
                              fontname="Arial-Bold" if bold else "Arial", color=color, align=align, lineheight=lh)

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


def letterhead(pg, kicker, title, originator, date, footer_left, footer_ref="ACS 2026",
               page_label="Page 1 of 1", subtitle=None):
    """Logo, marking top and bottom, kicker, title, optional subtitle, red rule,
    originator and date, footer.  Returns the y where content may start."""
    pg.text(W / 2, 24, MARKING, 8.5, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 28, MARKING, 8.5, BLACK, bold=True, align=1)
    pg.text(M, H - 16, footer_left, 8, BLACK)
    pg.text(W / 2, H - 16, footer_ref, 8, BLACK, align=1)
    pg.text(W - M, H - 16, page_label, 8, BLACK, align=2)
    png, (iw, ih) = logo_png()
    lh = 22
    pg.p.insert_image(pymupdf.Rect(M, 32, M + lh * iw / ih, 32 + lh), stream=png)
    pg.spaced(M, 68, kicker, 7, SWAMP, bold=True, spacing=1.6)
    pg.text(M, 86, title, 17, BLACK, bold=True)
    y = 94
    if subtitle:
        pg.text(M, 99, subtitle, 8.5, SWAMP)
        y = 105
    pg.line(M, y, W - M, y, ARMY_RED, width=2)
    pg.text(M, y + 11, originator, 8, SWAMP)
    x = W - M
    for s, bold in ((date, False), ("Date: ", True)):
        x -= pg.width(s, 7.5, bold)
        pg.text(x, y + 11, s, 7.5, BLACK, bold=bold)
    return y + 25


def status_block(pg, y, rows, label_width=120):
    """Pale green panel with a Swamp Green edge: letterspaced labels, plain values.
    A value may be a list of lines."""
    lines = [(label, v if isinstance(v, list) else [v]) for label, v in rows]
    n = sum(len(v) for _, v in lines)
    h = 16 * n + 12
    pg.box(M, y, W - 2 * M, h, fill=PALE, stroke=None, radius=3)
    pg.box(M, y + 4, 3.5, h - 8, fill=SWAMP, stroke=None)
    ly = y + 17
    for label, values in lines:
        pg.spaced(M + 14, ly, label, 7, SWAMP, bold=True, spacing=1.4)
        for v in values:
            pg.text(M + label_width, ly, v, 9, INK)
            ly += 16
    return y + h


def month_axis(pg, y, h, span, xof):
    """Year and month labels with a faint month grid over the timeline area."""
    import datetime as dt
    d = dt.date(span[0].year, span[0].month, 1)
    months = []
    while d <= span[1]:
        months.append(d)
        d = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    for k, m in enumerate(months):
        mx = xof(m)
        pg.line(mx, y + 26, mx, y + h, GRID, width=0.5)
        nxt = months[k + 1] if k + 1 < len(months) else dt.date(m.year + (m.month == 12), m.month % 12 + 1, 1)
        cx = (mx + xof(min(nxt, span[1] + dt.timedelta(days=1)))) / 2
        pg.text(cx, y + 22, m.strftime("%b"), 6.5, MID, align=1)
        if m.month == 1 or k == 0:
            pg.text(cx, y + 11, str(m.year), 7, SWAMP, bold=True, align=1)


def section_heading(pg, y, label):
    pg.spaced(M, y, label, 7, SWAMP, bold=True, spacing=1.6)
    pg.line(M, y + 5, W - M, y + 5, GRID)
