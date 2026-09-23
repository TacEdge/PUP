#!/usr/bin/env python3
"""
NZALC S6: a day in the life.  One landscape page in the house style, two
photographs and a few lines of copy.

    python3 build_nzalc_s6_day_in_the_life.py
        -> output/nzalc-s6-day-in-the-life.pdf (+ .png preview)
"""

import io

import pymupdf
from PIL import Image, ImageOps

from army_onepager import ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, SWAMP, WHITE, Page, rgb
from build_army_combat_mindset_development_system import reversed_logo_png, wrapped

OUT = "./output/nzalc-s6-day-in-the-life.pdf"
PNG = "./output/nzalc-s6-day-in-the-life.png"
W, H = 842, 595
M = 40
CW = W - 2 * M
R = 6
GREY = rgb("5F5F5A")

TITLE = "A Day in the Life: NZALC S6"
SUBTITLE = "New Zealand Army Leadership Centre"
DATE = "September 2026"
FOOTER_LEFT = "NZALC | A Day in the Life"
STRAP = "Every course NZALC runs starts and ends here: the kit that leaves the store, and the kit that comes back."

PHOTOS = [
    ("assets/nzalc-s6/s6-return.jpg", "THE RETURN",
     "After a course, everything comes back at once: radios, cables, chargers, projectors, cases. Every item is checked, tested and accounted for before it goes anywhere near a shelf."),
    ("assets/nzalc-s6/s6-store.jpg", "THE STANDARD",
     "Cases labelled, batteries charged, cables coiled, every item in its place. The next course draws its kit in minutes, not hours."),
]
CARDS = [
    ("ISSUE AND RETURN", "Kit drawn for every course and checked back in on return, with faults tagged for repair rather than discovered in the field."),
    ("POWER AND CONNECTIVITY", "Charging, cabling and communications, so instructors stay connected in the classroom and on the ground."),
    ("ACCOUNTABILITY", "Every serial number tracked. Stocktakes and audits are met from the register, not from a scramble."),
]


def cover_jpeg(path, w, h, px=1600):
    """Crop to the frame's aspect and return JPEG bytes."""
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    im = ImageOps.fit(im, (px, round(px * h / w)), method=Image.LANCZOS, centering=(0.5, 0.45))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=86)
    return buf.getvalue()


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
    pg.text(tx, top + 39, f"{SUBTITLE}  ·  {DATE}", 7.5, INK)
    return top + hh


def marker(pg, x, y, n):
    sh = pg.p.new_shape()
    sh.draw_circle((x, y), 9)
    sh.finish(color=None, fill=BLACK)
    sh.commit()
    pg.text(x, y + 3, str(n), 8, WHITE, bold=True, align=1)


def build():
    doc = pymupdf.open()
    pg = Page(doc, W, H)
    y = masthead(pg) + 24
    pg.text(W / 2, y, STRAP, 9.5, SWAMP, bold=True, align=1)
    y += 14

    # two photographs, side by side, numbered
    gap = 16
    pw = (CW - gap) / 2
    ph = pw * 0.76
    for i, (path, label, caption) in enumerate(PHOTOS):
        x = M + i * (pw + gap)
        pg.p.insert_image(pymupdf.Rect(x, y, x + pw, y + ph), stream=cover_jpeg(path, pw, ph))
        marker(pg, x + 14, y + 14, i + 1)
    cy = y + ph + 16
    for i, (path, label, caption) in enumerate(PHOTOS):
        x = M + i * (pw + gap)
        pg.text(x, cy, str(i + 1), 9, GOLD, bold=True)
        pg.spaced(x + 12, cy, label, 7, SWAMP, bold=True, spacing=1.6)
        ty = cy + 13
        for line in wrapped(pg, caption, 8, pw):
            pg.text(x, ty, line, 8, INK)
            ty += 10.5
    y = cy + 13 + 3 * 10.5 + 8

    # what the day is made of
    n = len(CARDS)
    cgap = 12
    cw = (CW - cgap * (n - 1)) / n
    ch = min(66, H - 44 - y)
    for i, (label, text) in enumerate(CARDS):
        x = M + i * (cw + cgap)
        pg.box(x, y, cw, ch, fill=FAINT, stroke=None, radius=R)
        pg.spaced(x + 12, y + 16, label, 5.8, SWAMP, bold=True, spacing=1.4)
        ty = y + 30
        for line in wrapped(pg, text, 7.6, cw - 24):
            pg.text(x + 12, ty, line, 7.6, INK)
            ty += 10
    print(f"cards {ch:.0f} high, end {y + ch:.0f}, footer marking at {H - 30}")

    doc.set_metadata({"title": TITLE, "author": "New Zealand Army Leadership Centre"})
    doc.save(OUT, garbage=3, deflate=True)
    pymupdf.open(OUT)[0].get_pixmap(dpi=200).save(PNG)
    print(f"Saved {OUT} and {PNG}")


if __name__ == "__main__":
    build()
