#!/usr/bin/env python3
"""
NZALC S6: a day in the life.  One landscape page in the house style: two
photographs, before and after.

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
STRAP = "NZALC\u2019s own S6, Asher March, doing what he does best"

PHOTOS = [
    ("assets/nzalc-s6/s6-return.jpg", "BEFORE"),
    ("assets/nzalc-s6/s6-store.jpg", "AFTER"),
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

    # two photographs, side by side, labelled before and after
    gap = 16
    pw = (CW - gap) / 2
    avail = H - 44 - 30 - y           # leave room for the label beneath
    ph = min(avail, pw * 0.92)
    y += (avail - ph) / 2             # centre the pair in the space
    for i, (path, label) in enumerate(PHOTOS):
        x = M + i * (pw + gap)
        pg.p.insert_image(pymupdf.Rect(x, y, x + pw, y + ph), stream=cover_jpeg(path, pw, ph))
        marker(pg, x + 14, y + 14, i + 1)
    ly = y + ph + 22
    for i, (path, label) in enumerate(PHOTOS):
        x = M + i * (pw + gap)
        pg.text(x, ly, str(i + 1), 11, GOLD, bold=True)
        pg.spaced(x + 16, ly, label, 10, SWAMP, bold=True, spacing=2.4)
    print(f"photos {ph:.0f} high, labels at {ly:.0f}, footer marking at {H - 30}")

    doc.set_metadata({"title": TITLE, "author": "New Zealand Army Leadership Centre"})
    doc.save(OUT, garbage=3, deflate=True)
    pymupdf.open(OUT)[0].get_pixmap(dpi=200).save(PNG)
    print(f"Saved {OUT} and {PNG}")


if __name__ == "__main__":
    build()
