#!/usr/bin/env python3
"""
Page 1 of the AITC discussion piece, rebuilt from structured data:
Officer continuum | LDF spine | Soldier continuum, one LDF transition per
horizontal band, with the rank transition and each development
intervention (ELDA, LDS) as separate cards.

    python3 build_ldf_page1.py
        -> output/ldf-alignment-page1.pdf        (A3 landscape)
        -> output/ldf-alignment-page1-data.json  (the data behind every card)

Every field is taken from the source material listed in SOURCES below.
A field the sources do not establish is "To confirm".  Nothing on the
page is inferred from the design sketch.
"""

import io
import json
import math

import pymupdf
from PIL import Image

import ldf_icons

OUT = "./output/ldf-alignment-page1.pdf"
OUT_DATA = "./output/ldf-alignment-page1-data.json"
LOGO_FILE = "./assets/nz-army-logo.png"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

SOURCES = {
    "LDF": "NZDF Leadership Framework v2 (10 Oct 2025): level names and value-add headings",
    "LDS": "NZDF Leadership Development System poster: which LDS course exists at each level and who delivers it",
    "LEVELS": "NZDF Leadership Levels poster: rank to transition alignment (stated by the poster to be an estimation)",
    "CDS": "NZALC course data sheets A18011, A18008, A18010: duration, provider, target learners, prerequisites, included courses",
    "MTG": "NZALC review of 9 Sep 2026 (transcript): mandate position and delivery practice as stated by ACS staff",
    "LSW": "Lead Self Workbook (TAD) 2026: LDS Lead Self forms part of the LDS and is designed for Regular Force personnel enlisting into the NZDF",
    "AMEND": "Amendments from ACS (ALC), 9 Sep 2026: ELDA Command at T4 (7 days, NZALC, on request); LDS Lead Teams and LDS Lead Leaders embedded in the JNCO and SNCO Courses; officer LDS Lead Leaders routinely enforced in practice; at Lead Integrated Capability and Lead Organisation both Officers and Other Ranks are selected to attend",
}

TITLE = "Two promotion continuums. One leadership development framework."
SUBTITLE = "How do Officer and Other Rank promotion continuums align to the intent and design of the LDF?"
OBSERVATION = [
    "Other Rank leadership development appears deliberately embedded within key promotion pathways.",
    "Equivalent officer leadership development exists at comparable LDF transitions, but its formal linkage to promotion varies across the continuum.",
]
OBSERVATION_CAVEAT = "An observation from the mapping, not yet a policy conclusion."
STATUS_MEANING = {"Mandated": "promotion prerequisite or embedded requirement",
                  "Not mandated": "development available but not required",
                  "Selected": "attendance by selection, not by mandate",
                  "To confirm": "policy position not yet verified"}

TC = "To confirm"

# LDF levels: name and the first value-add heading from the LDF (source: LDF).
LEVELS = [
    ("LEAD SELF", "Follow leader's intent"),
    ("LEAD TEAMS", "Get things done through others"),
    ("LEAD LEADERS", "Get things done through other leaders"),
    ("LEAD SYSTEMS", "Run an entire system"),
    ("LEAD CAPABILITY", "Turn strategy into action"),
    ("LEAD INTEGRATED CAPABILITY", "Lead at enterprise level"),
    ("LEAD ORGANISATION", "Evolve the organisation"),
]


def course(name, mandate, duration, delivered, embedded=None, note=None, src=()):
    return dict(course=name, mandate=mandate, duration=duration, delivered=delivered,
                embedded=embedded, note=note, sources=list(src))


NO_ELDA = dict(course=None, mandate=None, duration=None, delivered=None, embedded=None,
               note="No ELDA course at this level", sources=["CDS", "MTG"])

# One entry per LDF transition T1..T6.  Each side: rank transition, ELDA
# card, LDS card.  Mandate is the policy position: Mandated / Not mandated /
# To confirm.  A note records practice where the sources state it.
DATA = [
    dict(transition="Entry", frm="Civilian", to="LEAD SELF",
         officer=dict(
             rank="Civilian > OCDT", rank_src=["MTG"],
             elda=NO_ELDA,
             lds=course("LDS Lead Self", "Mandated", TC, TC, embedded="NZCC",
                        note=None, src=["LDS", "MTG"])),
         soldier=dict(
             rank="Civilian > PTE", rank_src=["MTG", "LSW"],
             elda=NO_ELDA,
             lds=course("LDS Lead Self", "Mandated", TC, "TAD", embedded="Recruit Training",
                        note=None, src=["LDS", "LSW", "MTG"]))),
    dict(transition="T1", frm="LEAD SELF", to="LEAD TEAMS",
         officer=dict(
             rank="OCDT > 2LT", rank_src=["LEVELS", "MTG"],
             elda=course("ELDA Lead Teams", "Mandated", TC, TC, embedded="NZCC",
                         note=None, src=["MTG"]),
             lds=course("LDS Lead Teams", "Mandated", TC, "NZALC", embedded="NZCC",
                        note=None, src=["LDS", "MTG"])),
         soldier=dict(
             rank="PTE > LCPL", rank_src=["LEVELS", "MTG"],
             elda=course("ELDA Lead Teams", "Mandated", "6 training days", "NZALC", embedded="JNCO Course (A1530)",
                         note=None, src=["CDS", "MTG"]),
             lds=course("LDS Lead Teams", "Mandated", TC, TC, embedded="JNCO Course (A1530)",
                        note=None, src=["LDS", "CDS", "AMEND"]))),
    dict(transition="T2", frm="LEAD TEAMS", to="LEAD LEADERS",
         officer=dict(
             rank="2LT / LT > CAPT", rank_src=["LEVELS", "MTG"],
             elda=course("ELDA Lead Leaders", "Not mandated", "6 training days", "NZALC",
                         note='Enforced in practice', src=["CDS", "MTG"]),
             lds=course("LDS Lead Leaders", "Not mandated", TC, TC,
                        note='Enforced in practice', src=["LDS", "CDS", "MTG", "AMEND"])),
         soldier=dict(
             rank="CPL > SGT", rank_src=["LEVELS", "MTG"],
             elda=course("ELDA Lead Leaders", "Mandated", "6 training days", "NZALC", embedded="SNCO Course (A1531)",
                         note=None, src=["CDS", "MTG"]),
             lds=course("LDS Lead Leaders", "Mandated", TC, TC, embedded="SNCO Course (A1531)",
                        note=None, src=["LDS", "CDS", "MTG", "AMEND"]))),
    dict(transition="T3", frm="LEAD LEADERS", to="LEAD SYSTEMS",
         officer=dict(
             rank="CAPT > MAJ", rank_src=["LEVELS", "MTG"],
             elda=course("ELDA Lead Systems", "Not mandated", "7 training days", "NZALC",
                         note='Self-selected', src=["CDS", "MTG"]),
             lds=course("LDS Lead Systems", "Not mandated", TC, "ILD",
                        note='Self-selected', src=["LDS", "MTG"])),
         soldier=dict(
             rank="SSGT > WO2", rank_src=["LEVELS", "MTG"],
             elda=course("ELDA Lead Systems", "Mandated", "7 training days", "NZALC", embedded="WO Course (A1532)",
                         note=None, src=["CDS", "MTG"]),
             lds=course("LDS Lead Systems", TC, TC, "ILD",
                        note='Check WO Course CDS', src=["LDS", "MTG"]))),
    dict(transition="T4", frm="LEAD SYSTEMS", to="LEAD CAPABILITY",
         officer=dict(
             rank="MAJ > LTCOL", rank_src=["LEVELS", "MTG"],
             elda=course("ELDA Command", "Not mandated", "7 training days", "NZALC",
                         note="On request", src=["CDS", "AMEND"]),
             lds=course("LDS Lead Capability", TC, TC, "ILD",
                        note=None, src=["LDS", "MTG"])),
         soldier=dict(
             rank="WO2 > WO1", rank_src=["LEVELS", "MTG"],
             elda=course("ELDA Command", "Not mandated", "7 training days", "NZALC",
                         note="On request", src=["CDS", "AMEND"]),
             lds=course("LDS Lead Capability", TC, TC, "ILD",
                        note=None, src=["LDS", "MTG"]))),
    dict(transition="T5", frm="LEAD CAPABILITY", to="LEAD INTEGRATED CAPABILITY",
         officer=dict(
             rank="LTCOL > COL", rank_src=["LEVELS", "MTG"],
             elda=course("ELDA component", "Selected", "1 week", "ILD",
                         embedded="LDS LIC Course", note=None, src=["MTG", "AMEND"]),
             lds=course("LDS Lead Integrated Capability", "Selected", "1 week", "ILD",
                        note=None, src=["LDS", "MTG"])),
         soldier=dict(
             rank="Tier 5 WO > Tier 4 WO", rank_src=["LEVELS"],
             elda=course("ELDA component", "Selected", "1 week", "ILD",
                         embedded="LDS LIC Course", note=None, src=["MTG", "AMEND"]),
             lds=course("LDS Lead Integrated Capability", "Selected", "1 week", "ILD",
                        note=None, src=["LDS", "MTG"]))),
    dict(transition="T6", frm="LEAD INTEGRATED CAPABILITY", to="LEAD ORGANISATION",
         officer=dict(
             rank="COL > BRIG+", rank_src=["LEVELS", "MTG"],
             elda=course("ELDA component", "Selected", TC, TC,
                         embedded="Lead Organisation Course", note=None, src=["MTG"]),
             lds=course("LDS Lead Organisation", "Selected", TC, "ILD",
                        note=None, src=["LDS", "MTG"])),
         soldier=dict(
             rank="Tier 4 WO > Tier 3 WO+", rank_src=["LEVELS"],
             elda=course("ELDA component", "Selected", TC, TC,
                         embedded="Lead Organisation Course", note=None, src=["MTG"]),
             lds=course("LDS Lead Organisation", "Selected", TC, "ILD",
                        note=None, src=["LDS", "MTG"]))),
]

# ------------------------------------------------------------------ drawing
W, H = 1191, 842          # A3 landscape
M = 44


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
PALE_RED = rgb("F7E4E4")
NEUTRAL = rgb("F1F1EF")
CARD = rgb("FAFAF8")

PALE_GOLD = rgb("F3EEDF")
DARK_GOLD = rgb("7A6535")
STATUS_STYLE = {
    "Mandated": (PALE, SWAMP),
    "Not mandated": (PALE_RED, ARMY_RED),
    "Selected": (PALE_GOLD, DARK_GOLD),
    TC: (NEUTRAL, MID),
}
DELIVERY_STYLE = {"NZALC": SWAMP, "ILD": GOLD}

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

    def textbox(self, x, y, w, h, s, size=8, color=INK, bold=False, align=0, lh=1.25):
        self.p.insert_textbox(pymupdf.Rect(x, y, x + w, y + h), s, fontsize=size,
                              fontname="Arial-Bold" if bold else "Arial", color=color, align=align, lineheight=lh)

    def line(self, x0, y0, x1, y1, color=GRID, width=0.8, dashes=None):
        sh = self.p.new_shape()
        sh.draw_line((x0, y0), (x1, y1))
        sh.finish(color=color, width=width, dashes=dashes)
        sh.commit()

    def box(self, x, y, w, h, fill=None, stroke=GRID, width=0.8, dashes=None, radius=0):
        """radius is in points; PyMuPDF takes it as a fraction of width and height."""
        sh = self.p.new_shape()
        r = pymupdf.Rect(x, y, x + w, y + h)
        if radius:
            sh.draw_rect(r, radius=(min(radius / w, 0.5), min(radius / h, 0.5)))
        else:
            sh.draw_rect(r)
        sh.finish(color=stroke, fill=fill, width=width, dashes=dashes)
        sh.commit()

    def arrow(self, x0, y0, x1, y1, color=GOLD, width=1.2):
        sh = self.p.new_shape()
        sh.draw_line((x0, y0), (x1, y1))
        ang = math.atan2(y1 - y0, x1 - x0)
        for d in (2.6, -2.6):
            sh.draw_line((x1, y1), (x1 - 7 * math.cos(ang + d), y1 - 7 * math.sin(ang + d)))
        sh.finish(color=color, width=width)
        sh.commit()

    def pill(self, x, y, label, right=False, size=6.6):
        fill, col = STATUS_STYLE[label]
        w = self.width(label.upper(), size, True) + 14
        if right:
            x -= w
        self.box(x, y, w, 12, fill=fill, stroke=None, radius=3)
        self.text(x + 7, y + 8.8, label.upper(), size, col, bold=True)
        return w


def letterhead(pg):
    pg.text(W / 2, 26, "UNCLASSIFIED", 9, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 30, "UNCLASSIFIED", 9, BLACK, bold=True, align=1)
    pg.text(M, H - 17, "Leadership Development Framework Discussion", 8.5, BLACK)
    pg.text(W / 2, H - 17, "ACS 2026", 8.5, BLACK, align=1)
    pg.text(W - M, H - 17, "Page 1 of 2", 8.5, BLACK, align=2)
    png, (iw, ih) = logo_png()
    lh = 26
    pg.p.insert_image(pymupdf.Rect(M, 34, M + lh * iw / ih, 34 + lh), stream=png)
    pg.text(M, 88, TITLE, 20, BLACK, bold=True)
    pg.text(M, 106, SUBTITLE, 11, SWAMP)
    pg.line(M, 115, W - M, 115, ARMY_RED, width=2.2)
    pg.text(M, 127, "Army Command School", 8.5, SWAMP)
    x = W - M
    for s, bold, col in (("September 2026", False, BLACK), ("Date: ", True, BLACK)):
        x -= pg.width(s, 8, bold)
        pg.text(x, 127, s, 8, col, bold=bold)


def field(pg, x, y, label, value, value_color=INK, bold=False):
    pg.spaced(x, y, label, 5.4, MID, bold=True, spacing=0.9)
    lw = pg.width(label, 5.4, True) + len(label) * 0.9 + 6
    pg.text(x + lw, y, value, 7.4, value_color, bold=bold)
    return lw + pg.width(value, 7.4, bold)


def course_card(pg, x, y, w, h, c):
    """A capability card: name, mandate as the hero, one row of facts."""
    if c["course"] is None:
        pg.box(x, y, w, h, fill=WHITE, stroke=GRID, dashes="[2 2] 0", radius=3)
        pg.text(x + w / 2, y + h / 2 + 2.5, c["note"], 7.2, MID, align=1)
        return
    fill, col = STATUS_STYLE[c["mandate"]]
    pg.box(x, y, w, h, fill=CARD, stroke=GRID, radius=3)
    pg.box(x, y + 3, 3.5, h - 6, fill=col, stroke=None)                     # status accent bar
    pg.spaced(x + 12, y + 13.5, c["course"].upper(), 8.2, BLACK, bold=True, spacing=0.5)
    pw = pg.width(c["mandate"].upper(), 8, True) + 18
    pg.box(x + w - 8 - pw, y + 4.5, pw, 15, fill=fill, stroke=None, radius=3)
    pg.text(x + w - 8 - pw / 2, y + 15.3, c["mandate"].upper(), 8, col, bold=True, align=1)
    fx, fy = x + 12, y + 27
    fx += field(pg, fx, fy, "DURATION", c["duration"], MID if c["duration"] == TC else INK) + 14
    dcol = DELIVERY_STYLE.get(c["delivered"], MID if c["delivered"] == TC else INK)
    fx += field(pg, fx, fy, "DELIVERY", c["delivered"], dcol, bold=c["delivered"] in DELIVERY_STYLE) + 14
    if c["embedded"]:
        field(pg, fx, fy, "EMBEDDED", c["embedded"], MID if c["embedded"] == TC else INK)
    if c["note"]:
        pg.text(x + w - 8, fy, c["note"], 6.2, MID, align=2)


def rank_card(pg, x, y, w, h, rank):
    pg.box(x, y, w, h, fill=WHITE, stroke=BLACK, width=1.1, radius=3)
    parts = [t.strip() for t in rank.split(">")]
    if len(parts) == 2:
        pg.text(x + w / 2, y + h / 2 - 7, parts[0], 10, BLACK, bold=True, align=1)
        pg.text(x + w / 2, y + h / 2 + 2.5, "\u2193", 9, GOLD, bold=True, align=1)
        pg.text(x + w / 2, y + h / 2 + 12.5, parts[1], 10, BLACK, bold=True, align=1)
    else:
        pg.text(x + w / 2, y + h / 2 + 4, parts[0], 10.5, BLACK, bold=True, align=1)


def side_rows(pg, data_key, x0, x1, y0, band_h, bandh, mirror):
    rw, gap = 92, 8
    cw = (x1 - x0) - rw - gap
    if mirror:
        rx, cx = x0, x0 + rw + gap
    else:
        cx, rx = x0, x1 - rw
    for i, t in enumerate(DATA):
        y = y0 + i * bandh
        s = t[data_key]
        rank_card(pg, rx, y, rw, band_h, s["rank"])
        ch = (band_h - 5) / 2
        course_card(pg, cx, y, cw, ch, s["elda"])
        course_card(pg, cx, y + ch + 5, cw, ch, s["lds"])


def transition_block(pg, x, y, w, h, label, level_index, name, desc):
    """The unit of analysis: one LDF transition, shown as the level it enters."""
    pg.box(x, y, w, h, fill=BLACK, stroke=None, radius=3)
    br = 15
    ldf_icons.badge(pg.p, x + 8 + br, y + h / 2, br, level_index, BLACK, WHITE, ring=True)
    tw = w - 8 - 2 * br
    tx = x + 8 + 2 * br + tw / 2
    cy = y + h / 2
    pg.spaced(tx, cy - 11, label, 6, GOLD, bold=True, spacing=1.6, align=1)
    size = 9.5
    while pg.width(name, size, True) > tw - 10 and size > 7:
        size -= 0.25
    pg.text(tx, cy + 5, name, size, WHITE, bold=True, align=1)
    pg.textbox(x + 8 + 2 * br + 2, cy + 9, tw - 6, 30, desc, 6.4, GRID, align=1, lh=1.2)



def main():
    doc = pymupdf.open()
    pg = Page(doc)
    letterhead(pg)
    spine_w = 184
    spine_x = W / 2 - spine_w / 2
    side_gap = 16
    ox0, ox1 = M, spine_x - side_gap
    sx0, sx1 = spine_x + spine_w + side_gap, W - M

    hy = 140
    for x, w, label, fill in ((ox0, ox1 - ox0, "OFFICER PROMOTION CONTINUUM", SWAMP),
                              (spine_x, spine_w, "LEADERSHIP DEVELOPMENT FRAMEWORK", BLACK),
                              (sx0, sx1 - sx0, "OTHER RANK PROMOTION CONTINUUM", SWAMP)):
        pg.box(x, hy, w, 18, fill=fill, stroke=None, radius=3)
        pg.spaced(x + w / 2, hy + 12.5, label, 7.2 if fill is SWAMP else 6.4, WHITE, bold=True,
                  spacing=0.6 if fill is BLACK else 1.6, align=1)

    top, bandh = hy + 26, 80
    band_h = bandh - 6
    for i, row in enumerate(DATA):
        y = top + i * bandh
        name, desc = LEVELS[i]
        label = "ENTRY" if row["transition"] == "Entry" else f"TRANSITION {row['transition'][1:]}"
        transition_block(pg, spine_x, y, spine_w, band_h, label, i, name, desc)
        mid = y + band_h / 2
        pg.line(ox0, mid, ox1, mid, GRID, dashes="[1 3] 0")
        pg.line(sx0, mid, sx1, mid, GRID, dashes="[1 3] 0")
        if i < len(DATA) - 1:
            pg.arrow(W / 2, y + band_h, W / 2, y + bandh - 1)
    side_rows(pg, "officer", ox0, ox1, top, band_h, bandh, mirror=False)
    side_rows(pg, "soldier", sx0, sx1, top, band_h, bandh, mirror=True)

    # legend
    ly = top + len(DATA) * bandh + 2
    lx = M
    pg.spaced(lx, ly + 9, "READ THIS PAGE LEFT TO RIGHT", 5.6, INK, bold=True, spacing=1.2)
    lx += 128
    for st in ("Mandated", "Not mandated", "Selected", TC):
        fill, col = STATUS_STYLE[st]
        pg.box(lx, ly + 1, 9, 9, fill=fill, stroke=None, radius=2)
        pg.text(lx + 13, ly + 9, st, 6.6, col, bold=True)
        lx += pg.width(st, 6.6, True) + 16
        pg.text(lx, ly + 9, STATUS_MEANING[st], 6.2, MID)
        lx += pg.width(STATUS_MEANING[st], 6.2) + 12
    lx += 8
    pg.text(lx, ly + 9, "NZALC", 6.6, SWAMP, bold=True)
    lx += pg.width("NZALC", 6.6, True) + 3
    pg.text(lx, ly + 9, "delivered", 6.2, MID)
    lx += pg.width("delivered", 6.2) + 14
    pg.text(lx, ly + 9, "ILD", 6.6, GOLD, bold=True)
    lx += pg.width("ILD", 6.6, True) + 3
    pg.text(lx, ly + 9, "delivered (Institute for Leader Development, tri-Service)", 6.2, MID)

    # emerging observation
    oy = ly + 18
    oh = 46
    pg.box(M, oy, W - 2 * M, oh, fill=PALE, stroke=None, radius=3)
    pg.box(M, oy + 4, 3.5, oh - 8, fill=SWAMP, stroke=None)
    pg.spaced(M + 14, oy + 13, "EMERGING OBSERVATION", 6.2, SWAMP, bold=True, spacing=1.6)
    pg.text(M + 14, oy + 26, OBSERVATION[0], 8, BLACK)
    pg.text(M + 14, oy + 37.5, OBSERVATION[1], 8, BLACK)
    pg.text(W - M - 10, oy + 13, OBSERVATION_CAVEAT, 6.4, MID, align=2)

    doc.set_metadata({"title": "Officer and Other Rank Leadership Development: Page 1",
                      "author": "New Zealand Army Leadership Centre"})
    doc.save(OUT, garbage=3, deflate=True)
    with open(OUT_DATA, "w", encoding="utf-8") as fh:
        json.dump({"sources": SOURCES, "levels": LEVELS, "transitions": DATA}, fh, indent=2)
    print(f"Saved {OUT} and {OUT_DATA}")


if __name__ == "__main__":
    main()
