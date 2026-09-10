#!/usr/bin/env python3
"""
Direction to ELDA Wing on physical preparedness, drawn directly as a
one-page A4 PDF in the house style so the bottom-line card can carry
rounded corners.

    python3 build_elda_direction_pdf.py -> output/elda-physical-preparedness-direction.pdf
"""

import pymupdf

from army_onepager import ARMY_RED, BLACK, GRID, INK, MID, MOAWHANGO, SWAMP, WHITE, Page, logo_png

OUT = "./output/elda-physical-preparedness-direction.pdf"
W, H = 595, 842
M = 56

KICKER = "DIRECTION TO ELDA WING"
TITLE = "Physical Preparedness"
SUBTITLE = "COMDT ACS DIRECTION OF 10 SEPTEMBER 2026 APPLIED TO ELDA DELIVERY"
ORIGINATOR = "New Zealand Army Leadership Centre | Army Command School"
REFERENCE = "COMDT ACS discussion, 10 September 2026"
DATE = "September 2026"
STATUS = "For action"
FOOTER_LEFT = "NZALC | Direction to ELDA Wing"

CONTEXT = ("COMDT ACS has identified a need to strengthen physical preparedness across promotion training. His direction is "
           "that soldiers should arrive on promotion courses having already met the required Army physical standards, with "
           "assurance of those standards sitting with units and NCO School. ELDA is not to become an additional point of "
           "physical fitness assessment.")
LEAD = "Accordingly, the following applies to ELDA delivery."
POINTS = [
    ("ELDA remains a leadership development environment.", "Physical pressure is used deliberately to create interference and develop leadership under pressure."),
    ("Do not assess or grade physical fitness.", "ELDA instructors are not to apply additional or informal fitness standards."),
    ("Allow legitimate teamwork.", "Load sharing and supporting team members are appropriate where they contribute to achieving the task."),
    ("Preserve the developmental environment.", "Instructors remain coaches and facilitators. Fitness assessment must not undermine openness, reflection or psychological safety."),
    ("Report significant concerns.", "Genuine concerns regarding a learner's physical preparedness are to be reported discreetly to SI ELDA, who will report directly to SI NCO School for follow-up."),
]
BOTTOM_LINE = ("Continue to use physical pressure where it supports the learning outcome. Our role is to develop and "
               "observe leadership under pressure, not to assess physical fitness.")


def heading(pg, y, text):
    pg.text(M, y, text, 12, BLACK, bold=True)
    return y + 16


def paragraph(pg, y, text, size=10, lh=1.32):
    box_h = 200
    pg.textbox(M, y - size, W - 2 * M, box_h, text, size, INK, lh=lh)
    # estimate the height used: wrap by measuring
    words = text.split()
    lines, cur = 1, 0
    for w in words:
        ww = pg.width(w + " ", size)
        if cur + ww > W - 2 * M:
            lines += 1
            cur = ww
        else:
            cur += ww
    return y + lines * size * lh


def build():
    doc = pymupdf.open()
    pg = Page(doc, W, H)
    pg.text(W / 2, 28, "UNCLASSIFIED", 9, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 34, "UNCLASSIFIED", 9, BLACK, bold=True, align=1)
    pg.text(M, H - 20, FOOTER_LEFT, 8, BLACK)
    pg.text(W / 2, H - 20, "ACS 2026", 8, BLACK, align=1)
    pg.text(W - M, H - 20, "Page 1 of 1", 8, BLACK, align=2)
    png, (iw, ih) = logo_png()
    lh = 26
    pg.p.insert_image(pymupdf.Rect(M, 56, M + lh * iw / ih, 56 + lh), stream=png)
    pg.spaced(M, 108, KICKER, 8, SWAMP, bold=True, spacing=1.8)
    pg.text(M, 134, TITLE, 22, BLACK, bold=True)
    pg.spaced(M, 152, SUBTITLE, 7.5, SWAMP, bold=True, spacing=1.4)
    pg.line(M, 160, W - M, 160, ARMY_RED, width=2)
    pg.text(M, 176, ORIGINATOR, 9, SWAMP)
    x = M
    for s, bold, col in (("Reference: ", True, BLACK), (REFERENCE, False, BLACK), ("   ·   ", False, MID),
                         ("Date: ", True, BLACK), (DATE, False, BLACK), ("   ·   ", False, MID),
                         ("Status: ", True, BLACK), (STATUS, True, ARMY_RED)):
        pg.text(x, 190, s, 8, col, bold=bold)
        x += pg.width(s, 8, bold)

    y = heading(pg, 226, "Context")
    y = paragraph(pg, y + 6, CONTEXT) + 14
    y = heading(pg, y, "Direction")
    y = paragraph(pg, y + 6, LEAD) + 6
    for k, (lead, body) in enumerate(POINTS):
        pg.text(M, y, f"{k + 1}.", 10, INK)
        pg.text(M + 20, y, lead, 10, BLACK, bold=True)
        rest_x = M + 20 + pg.width(lead, 10, True) + 4
        # wrap the body after the bold lead, continuing on the following lines at the indent
        words = body.split()
        line, cur_x, ly = [], rest_x, y
        avail = W - M
        for w in words:
            ww = pg.width(w + " ", 10)
            if cur_x + ww > avail:
                pg.text(rest_x if ly == y else M + 20, ly, " ".join(line), 10, INK)
                line, cur_x, ly = [w], M + 20 + ww, ly + 13.5
            else:
                line.append(w)
                cur_x += ww
        pg.text(rest_x if ly == y else M + 20, ly, " ".join(line), 10, INK)
        y = ly + 20
    y += 4
    y = heading(pg, y, "Bottom Line")
    card_h = 74
    pg.box(M, y + 2, W - 2 * M, card_h, fill=MOAWHANGO, stroke=None, radius=8)
    pg.textbox(M + 18, y + 16, W - 2 * M - 36, card_h - 20, BOTTOM_LINE, 11.5, SWAMP, bold=True, lh=1.35)
    doc.set_metadata({"title": "Direction to ELDA Wing: Physical Preparedness", "author": "New Zealand Army Leadership Centre"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
