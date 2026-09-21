#!/usr/bin/env python3
"""
Army Leadership Centre, HQ ACS: organisation chart in the house style.

    python3 build_nzalc_hq_org_chart.py
        -> output/nzalc-hq-org-chart.pdf (+ .png preview)
"""

import io

import pymupdf
from PIL import Image

from army_onepager import ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, MID, PALE, SWAMP, WHITE, Page, rgb

OUT = "./output/nzalc-hq-org-chart.pdf"
PNG = "./output/nzalc-hq-org-chart.png"
PHOTOS = "./assets/nzalc-hq-photos"
LOGO_REVERSED = "./assets/nz-army-logo-white.png"
W, H = 842, 595
M = 36
CW = W - 2 * M
R = 6
GREY = rgb("5F5F5A")

TITLE = "Army Leadership Centre"
SUBTITLE = "HQ ACS organisation  ·  21 September 2026"
FOOTER_LEFT = "NZALC | Organisation"

# (service no, rank, name, role, position no)
CI = ("P1023697", "MAJ", "Michael Coom", "Chief Instructor NZALC", "00114491")
STOREPERSON = ("N1035127", "", "Emma Pritchard", "Storeperson NZALC", "00114506")
WINGS = [
    ("ELDA Wing", ("D1030725", "CAPT", "Tony Calder-St…", "Senior Instructor ELDA Wing", "00114497"), [
        ("Q1066064", "", "Dave Ryan", "Instructor ELDA Wing", "00109524"),
        ("S1066066", "", "Katherine Beckett", "Instructor ELDA Wing", "00109525"),
        ("V1066161", "", "Phil Johnston-Coates", "Instructor ELDA Wing", "00109751"),
        ("W1062758", "", "Jonathan Harding", "Instructor NZALC", "00114498"),
        ("Q1066133", "", "James Geddes", "Instructor NZALC", "00114499"),
        ("H1058030", "", "David van der Gulik", "Instructor NZALC", "00114500"),
        ("W1058963", "", "Asher March", "Instructor NZALC", "00114501"),
        ("W1062551", "", "Pip Rees", "Instructor NZALC", "00114502"),
        ("J1058031", "", "Edward Murphy", "Instructor NZALC", "00114503"),
    ]),
    ("Leadership Development Wing", ("V56369", "WO2", "Grant Matthews", "Senior Instructor NZALC", "00114492"), [
        ("R1006909", "SSGT", "Skeltz Skelton", "Instructor NZALC", "00114493"),
        ("H1030384", "", "Shane Carson", "Instructor NZALC", "00114494"),
        ("D1060188", "", "Hilary Cave", "Instructor NZALC", "00114495"),
    ]),
    ("Training", ("H1023944", "", "Dave Moore", "Training Manager NZALC", "00114507"), []),
]
SAFETY_CELL = ("ELDA Safety Management Cell", ("Q50200", "", "Jim Masson", "ELDA Safety Manager NZALC", "00114496"))


def photo_png(service_no):
    im = Image.open(f"{PHOTOS}/{service_no}.jpg").convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue()


def reversed_logo_png():
    im = Image.open(LOGO_REVERSED).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue(), im.size


def masthead(pg):
    pg.text(W / 2, 20, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 22, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(M, H - 11, FOOTER_LEFT, 7.5, BLACK)
    pg.text(W / 2, H - 11, "ACS 2026", 7.5, BLACK, align=1)
    pg.text(W - M, H - 11, "Page 1 of 1", 7.5, BLACK, align=2)
    top, hh, brand_w = 30, 46, 138
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
    pg.text(tx, top + 39, SUBTITLE, 7.5, INK)
    return top + hh


def person_card(pg, x, y, w, h, person, lead=False):
    """Photo, rank and name, role, position number.  Lead cards carry a black spine."""
    sn, rank, name, role, pos = person
    pg.box(x, y, w, h, fill=FAINT, stroke=None, radius=R)
    ph = h - 10
    px = x + 6
    pg.p.insert_image(pymupdf.Rect(px, y + 5, px + ph, y + 5 + ph), stream=photo_png(sn))
    tx = px + ph + 7
    label = f"{rank} {name}".strip()
    size = 8.2 if lead else 7.6
    while pg.width(label, size, True) > w - (tx - x) - 6 and size > 6.4:
        size -= 0.2
    pg.text(tx, y + 16, label, size, BLACK, bold=True)
    pg.text(tx, y + 26.5, role, 6.6, SWAMP)
    pg.text(tx, y + 36, f"{sn}  ·  {pos}", 5.8, GREY)


def unit_band(pg, x, y, w, name):
    pg.box(x, y, w, 16, fill=BLACK, stroke=None, radius=4)
    pg.text(x + w / 2, y + 11, name, 7.6, WHITE, bold=True, align=1)
    return y + 16


def vline(pg, x, y0, y1):
    pg.line(x, y0, x, y1, GOLD, width=1)


def hline(pg, x0, x1, y):
    pg.line(x0, y, x1, y, GOLD, width=1)


def build():
    doc = pymupdf.open()
    pg = Page(doc, W, H)
    y0 = masthead(pg)

    card_h = 44
    gap = 7
    # ---- chief instructor, centred; storeperson reports directly to the CI ----
    ci_w = 210
    ci_x = M + (CW - ci_w) / 2
    ci_y = y0 + 20
    unit_band(pg, ci_x, ci_y, ci_w, "Army Leadership Centre HQ ACS")
    person_card(pg, ci_x, ci_y + 16, ci_w, card_h, CI, lead=True)
    ci_bottom = ci_y + 16 + card_h
    ci_cx = ci_x + ci_w / 2

    # ---- columns: ELDA Wing (two sub-columns), LDW, Training, direct reports ----
    col_gap = 12
    sub_gap = 6
    col_w = 150
    elda_w = col_w * 2 + sub_gap
    total = elda_w + 3 * col_w + 3 * col_gap
    x0 = M + (CW - total) / 2
    col_x = [x0, x0 + elda_w + col_gap, x0 + elda_w + col_gap + col_w + col_gap,
             x0 + elda_w + col_gap + 2 * (col_w + col_gap)]
    col_top = ci_bottom + 34
    rail_y = ci_bottom + 17

    # connector rail from the CI to each column
    heads = [x0 + elda_w / 2, col_x[1] + col_w / 2, col_x[2] + col_w / 2, col_x[3] + col_w / 2]
    vline(pg, ci_cx, ci_bottom, rail_y)
    hline(pg, min(heads), max(heads), rail_y)
    for hx in heads:
        vline(pg, hx, rail_y, col_top)

    # ELDA Wing
    name, lead, members = WINGS[0]
    y = unit_band(pg, x0, col_top, elda_w, name)
    person_card(pg, x0, y, elda_w, card_h, lead, lead=True)
    y += card_h + 8
    lead_bottom = y - 8
    left, right = members[:5], members[5:]
    sub_x = [x0, x0 + col_w + sub_gap]
    # short rail from the SI into the two instructor sub-columns
    vline(pg, x0 + elda_w / 2, lead_bottom, lead_bottom + 4)
    hline(pg, sub_x[0] + col_w / 2, sub_x[1] + col_w / 2, lead_bottom + 4)
    for sx, group in zip(sub_x, (left, right)):
        vline(pg, sx + col_w / 2, lead_bottom + 4, y)
        yy = y
        for m in group:
            person_card(pg, sx, yy, col_w, card_h, m)
            yy += card_h + gap
    elda_end = y + 5 * (card_h + gap)
    # safety cell under the ELDA Wing, beneath the right-hand sub-column
    sc_name, sc_lead = SAFETY_CELL
    sc_y = y + 4 * (card_h + gap) + 4
    yy = unit_band(pg, sub_x[1], sc_y, col_w, sc_name)
    person_card(pg, sub_x[1], yy, col_w, card_h, sc_lead, lead=True)
    elda_end = max(elda_end, yy + card_h)

    # Leadership Development Wing
    name, lead, members = WINGS[1]
    y = unit_band(pg, col_x[1], col_top, col_w, name)
    person_card(pg, col_x[1], y, col_w, card_h, lead, lead=True)
    y += card_h + 8
    vline(pg, col_x[1] + col_w / 2, y - 8, y)
    for m in members:
        person_card(pg, col_x[1], y, col_w, card_h, m)
        y += card_h + gap

    # Training
    name, lead, members = WINGS[2]
    y = unit_band(pg, col_x[2], col_top, col_w, name)
    person_card(pg, col_x[2], y, col_w, card_h, lead, lead=True)

    # direct report to the CI
    y = unit_band(pg, col_x[3], col_top, col_w, "HQ Support")
    person_card(pg, col_x[3], y, col_w, card_h, STOREPERSON)

    print(f"content ends at y={elda_end:.0f}, footer marking at {H - 30}")
    doc.set_metadata({"title": "Army Leadership Centre: HQ ACS organisation", "author": "Army Command School"})
    doc.save(OUT, garbage=3, deflate=True)
    pymupdf.open(OUT)[0].get_pixmap(dpi=200).save(PNG)
    print(f"Saved {OUT} and {PNG}")


if __name__ == "__main__":
    build()
