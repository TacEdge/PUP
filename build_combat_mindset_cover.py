#!/usr/bin/env python3
"""
Cover page for the Combat Mindset pack: plain, landscape, in the house style.

    python3 build_combat_mindset_cover.py
        -> output/combat-mindset-cover.pdf (+ .png preview)
"""

import pymupdf

from army_onepager import ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, SWAMP, WHITE, Page, rgb
from build_army_combat_mindset_development_system import reversed_logo_png

OUT = "./output/combat-mindset-cover.pdf"
PNG = "./output/combat-mindset-cover.png"

# Page numbering: a combined pack sets these so numbering runs across documents.
PAGE_OFFSET = 0
PAGE_TOTAL = None


def page_label(i, n):
    return f"Page {PAGE_OFFSET + i} of {PAGE_TOTAL or n}"

W, H = 842, 595
M = 40
CW = W - 2 * M
R = 6
GREY = rgb("5F5F5A")

TITLE = "Combat Mindset"
DEFINITION = "The capacity to regulate and sustain effective performance under operational pressure."
ORIGINATOR = "Army Command School"
FOOTER_LEFT = "Army Combat Mindset | Design and development draft"


def build():
    doc = pymupdf.open()
    pg = Page(doc, W, H)
    pg.text(W / 2, 20, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 22, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(M, H - 11, FOOTER_LEFT, 7.5, BLACK)
    pg.text(W / 2, H - 11, "ACS 2026", 7.5, BLACK, align=1)
    pg.text(W - M, H - 11, page_label(1, 1), 7.5, BLACK, align=2)

    # brand block, top left: the only red on the page
    top, hh = 30, 46
    brand_w = 138
    pg.box(M, top, brand_w, hh, fill=ARMY_RED, stroke=None, radius=R)
    png, (iw, ih) = reversed_logo_png()
    lh = 27
    lw = lh * iw / ih
    pg.p.insert_image(pymupdf.Rect(M + (brand_w - lw) / 2, top + (hh - lh) / 2,
                                   M + (brand_w + lw) / 2, top + (hh + lh) / 2), stream=png)

    # the title alone, set low in the page with the field above it left empty
    y = 300
    pg.text(M, y, TITLE, 40, BLACK, bold=True)
    pg.line(M, y + 22, M + 60, y + 22, GOLD, width=1.4)
    pg.text(M, y + 50, DEFINITION, 13, INK)

    doc.set_metadata({"title": "Army Combat Mindset", "author": ORIGINATOR})
    doc.save(OUT, garbage=3, deflate=True)
    pymupdf.open(OUT)[0].get_pixmap(dpi=200).save(PNG)
    print(f"Saved {OUT} and {PNG}")


if __name__ == "__main__":
    build()
