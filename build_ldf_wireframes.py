#!/usr/bin/env python3
"""
Low-fidelity wireframes for the AITC discussion piece on Officer and
Soldier leadership development: two landscape pages, drawn as a PDF with
PyMuPDF.  Grey and boxy on purpose, so the conversation stays on
structure.  A separate working paper carries the current-versus-desired
mapping, which is not part of the discussion piece.

    python3 build_ldf_wireframes.py
        -> output/ldf-alignment-wireframes.pdf            (two pages)
        -> output/ldf-alignment-future-state-working-paper.pdf

Evidence base: the four source documents, the NZALC course data sheets,
and the transcript of the NZALC meeting of 9 Sep 2026.  Evidence status
per cell is held in the data register, not on the page.
"""

import math

import pymupdf

OUT = "./output/ldf-alignment-wireframes.pdf"
OUT_WP = "./output/ldf-alignment-future-state-working-paper.pdf"
W, H = 842, 595
M = 36

INK = (0.12, 0.12, 0.12)
MID = (0.45, 0.45, 0.45)
LIGHT = (0.80, 0.80, 0.80)
FILL = (0.94, 0.94, 0.94)
FILL2 = (0.86, 0.86, 0.86)
DARK = (0.30, 0.30, 0.30)
NOTE = (0.55, 0.36, 0.08)
WHITE = (1, 1, 1)

HEADLINE = ("How deliberately does Army link leadership development to "
            "progression through its Officer and Soldier promotion continuums?")
PAGE1_CLOSE = "Same leadership framework. Different mechanisms for ensuring development occurs."
PAGE2_STATEMENT = ("The issue may not be an absence of leadership development. It is the absence of a "
                   "consistently deliberate mechanism linking the right development to the right career transition.")
FACTS = [
    ("SOLDIERS", "Leadership development is deliberately embedded in key promotion pathways."),
    ("OFFICERS", "Equivalent development exists, but its linkage to career progression varies considerably across the continuum."),
    ("THE QUESTION", "Is that difference deliberate, and if so, what is the rationale?"),
]
IF_YES = "What is the rationale for treating Officer and Soldier leadership development differently?"
IF_NO = ("Should Army establish a more consistent mechanism for ensuring development occurs "
         "before increased leadership responsibility?")
LEVELS = ["LEAD SELF", "LEAD TEAMS", "LEAD LEADERS", "LEAD SYSTEMS",
          "LEAD CAPABILITY", "LEAD INTEGRATED\nCAPABILITY", "LEAD ORGANISATION"]

# Career linkage states and their level (the band thickness on page 2).
LEVEL = {"MANDATED": 4, "FUNCTIONALLY REQUIRED": 3, "EXPECTED": 2, "SELF-SELECTED": 1}

# One entry per LDF transition Ti (level i to level i+1).  Every row on
# page 1 is one LDF transition read across two career systems: the
# officer entry and the soldier entry at index i sit on the same line.
# rank, course, status, qualifier (one line, or empty).
OFFICER = [
    ("OCDT  >  2LT", "ELDA / LDS Lead Teams", "MANDATED", "Embedded in NZCC"),
    ("2LT / LT  >  CAPT", "ELDA / LDS Lead Leaders", "FUNCTIONALLY REQUIRED", "Not mandated in promotion policy"),
    ("CAPT  >  MAJ", "ELDA / LDS Lead Systems", "SELF-SELECTED", "Not mandated; not policed"),
    ("MAJ  >  LTCOL", "LDS Lead Capability", "EXPECTED", "Not mandated; high uptake"),
    ("LTCOL  >  COL", "LDS Lead Integrated Capability", "EXPECTED", "Full attendance"),
    ("COL  >  BRIG", "LDS Lead Organisation", "EXPECTED", "Full attendance"),
]
SOLDIER = [
    ("PTE  >  LCPL", "ELDA / LDS Lead Teams", "MANDATED", "Embedded in JNCO course"),
    ("CPL  >  SGT", "ELDA / LDS Lead Leaders", "MANDATED", "In promotion policy (SNCO course)"),
    ("SSGT  >  WO2", "ELDA / LDS Lead Systems", "MANDATED", "ELDA on WO course; LDS prerequisite to confirm"),
    ("WO2  >  WO1", "LDS Lead Capability", "EXPECTED", "Not in policy; high uptake (to confirm)"),
    ("WO1  >  Senior WO1", "LDS Lead Integrated Capability", "EXPECTED", "Full attendance"),
    ("Senior WO1", "LDS Lead Organisation", "EXPECTED", "Full attendance"),
]

# Page 2: five stages, T5 and T6 merged as the senior stage.
STAGES = ["T1", "T2", "T3", "T4", "T5 / T6"]
OFFICER_STAGES = [("OCDT > 2LT", "MANDATED"), ("2LT / LT > CAPT", "FUNCTIONALLY REQUIRED"),
                  ("CAPT > MAJ", "SELF-SELECTED"), ("MAJ > LTCOL", "EXPECTED"), ("LTCOL > COL > BRIG", "EXPECTED")]
SOLDIER_STAGES = [("PTE > LCPL", "MANDATED"), ("CPL > SGT", "MANDATED"),
                  ("SSGT > WO2", "MANDATED"), ("WO2 > WO1", "EXPECTED"), ("WO1 and senior WO1", "EXPECTED")]


class Page:
    def __init__(self, doc, number, total, title, purpose, tag="AITC DISCUSSION PIECE  ·  LOW FIDELITY"):
        self.p = doc.new_page(width=W, height=H)
        self.text(M, 22, f"WIREFRAME {number} OF {total}", 7, MID)
        self.text(W - M, 22, "OFFICER AND SOLDIER LEADERSHIP DEVELOPMENT  ·  " + tag, 7, MID, align=2)
        self.text(M, 40, title.upper(), 9, INK, bold=True)
        self.text(M, 52, purpose, 7.5, MID)
        self.line(M, 58, W - M, 58, LIGHT)

    def text(self, x, y, s, size=9, color=INK, bold=False, align=0):
        font = "helvetica-bold" if bold else "helvetica"
        if align:
            tw = pymupdf.get_text_length(s, fontname=font, fontsize=size)
            x = x - tw if align == 2 else x - tw / 2
        self.p.insert_text((x, y), s, fontsize=size, fontname=font, color=color)

    def textbox(self, x, y, w, h, s, size=8, color=INK, bold=False, align=0, lh=1.25):
        font = "helvetica-bold" if bold else "helvetica"
        self.p.insert_textbox(pymupdf.Rect(x, y, x + w, y + h), s, fontsize=size,
                              fontname=font, color=color, align=align, lineheight=lh)

    def line(self, x0, y0, x1, y1, color=MID, width=0.8, dashes=None):
        sh = self.p.new_shape()
        sh.draw_line((x0, y0), (x1, y1))
        sh.finish(color=color, width=width, dashes=dashes)
        sh.commit()

    def box(self, x, y, w, h, fill=None, stroke=MID, width=0.8, dashes=None):
        sh = self.p.new_shape()
        sh.draw_rect(pymupdf.Rect(x, y, x + w, y + h))
        sh.finish(color=stroke, fill=fill, width=width, dashes=dashes)
        sh.commit()

    def polygon(self, pts, fill=None, stroke=None, width=0.8):
        sh = self.p.new_shape()
        sh.draw_polyline(pts + [pts[0]])
        sh.finish(color=stroke, fill=fill, width=width, closePath=True)
        sh.commit()

    def labelled(self, x, y, w, h, label, fill=FILL, size=7.5, bold=False,
                 color=INK, stroke=MID, dashes=None, width=0.8):
        self.box(x, y, w, h, fill=fill, stroke=stroke, dashes=dashes, width=width)
        lines = label.split("\n")
        ty = y + h / 2 - len(lines) * (size + 2) / 2 + size
        for ln in lines:
            self.text(x + w / 2, ty, ln, size, color, bold=bold, align=1)
            ty += size + 2

    def arrow(self, x0, y0, x1, y1, color=DARK, width=0.9):
        sh = self.p.new_shape()
        sh.draw_line((x0, y0), (x1, y1))
        ang = math.atan2(y1 - y0, x1 - x0)
        for d in (2.6, -2.6):
            sh.draw_line((x1, y1), (x1 - 6 * math.cos(ang + d), y1 - 6 * math.sin(ang + d)))
        sh.finish(color=color, width=width)
        sh.commit()

    def chip(self, x, y, s, fill=FILL2, color=INK, right=False):
        w = pymupdf.get_text_length(s, fontname="helvetica-bold", fontsize=5.5) + 8
        if right:
            x = x - w
        self.box(x, y, w, 9, fill=fill, stroke=None)
        self.text(x + 4, y + 6.8, s, 5.5, color, bold=True)
        return w

    def note(self, x, y, w, s):
        self.text(x, y + 8, "VISUAL LOGIC", 6.5, NOTE, bold=True)
        self.textbox(x, y + 12, w, 60, s, 6.8, NOTE)


def cell(pg, x, y, w, h, entry, soldier):
    """One transition cell: rank transition, course, one status, one qualifier."""
    rank, course, status, qual = entry
    mandated = status == "MANDATED"
    pg.box(x, y, w, h, fill=FILL2 if mandated else WHITE, stroke=INK if mandated else DARK,
           width=1.0, dashes=None if mandated else "[3 2] 0")
    pg.text(x + w / 2, y + 11, rank, 8, INK, bold=True, align=1)
    pg.text(x + w / 2, y + 20, course, 6.5, DARK, align=1)
    pg.text(x + w / 2, y + 31, status, 8, INK, bold=True, align=1)
    if qual:
        pg.text(x + w / 2, y + 39, qual, 5.8, MID, align=1)


def page1(doc):
    pg = Page(doc, 1, 2, "Two continuums. One leadership framework.",
              "Officer continuum, common LDF spine, Soldier continuum. Every row is one LDF transition read across two career systems.")
    pg.textbox(M, 62, W - 2 * M, 30, HEADLINE, 11, INK, bold=True, align=1, lh=1.2)

    spine_x, spine_w = W / 2 - 66, 132
    col_w = spine_x - M - 30
    top, rowh, lvl_h = 100, 64, 18
    pg.labelled(M, top - 16, col_w, 14, "OFFICER CONTINUUM", fill=DARK, size=7, bold=True, color=WHITE, stroke=None)
    pg.labelled(spine_x, top - 16, spine_w, 14, "LDF", fill=INK, size=7, bold=True, color=WHITE, stroke=None)
    pg.labelled(W - M - col_w, top - 16, col_w, 14, "SOLDIER CONTINUUM", fill=DARK, size=7, bold=True, color=WHITE, stroke=None)

    for i, lvl in enumerate(LEVELS):
        y = top + i * rowh
        pg.labelled(spine_x + 8, y, spine_w - 16, lvl_h, lvl, fill=FILL if i % 2 else FILL2, size=6.5, bold=True)
        if i < 6:
            # the transition row: one line across the whole page, both cells centred on it
            ty = y + lvl_h + 2
            th = rowh - lvl_h - 4
            mid = ty + th / 2
            pg.line(M, mid, W - M, mid, LIGHT, dashes="[1 2] 0")
            pg.arrow(W / 2, y + lvl_h, W / 2, y + rowh - 1, color=DARK)
            pg.text(W / 2 + 8, mid + 2, f"T{i + 1}", 6, MID)
            cell(pg, M, ty, col_w, th, OFFICER[i], soldier=False)
            cell(pg, W - M - col_w, ty, col_w, th, SOLDIER[i], soldier=True)

    # close
    y = top + 6 * rowh + lvl_h + 10
    pg.box(M, y, W - 2 * M, 30, fill=INK, stroke=None)
    pg.text(W / 2, y + 20, PAGE1_CLOSE.upper(), 11, WHITE, bold=True, align=1)
    pg.text(M, y + 40, "Shaded: mandated in policy or embedded in the qualifying course. Ranks per the 9 Sep meeting. Sources and evidence status: data register.", 6, MID)
    pg.note(M, y + 46, W - 2 * M,
            "One status per transition, readable from three metres. Everything that explained a cell (course codes, delivery, evidence tags) "
            "is out of the graphic and in the register or speaker notes.")


def band(pg, y_mid, stages, entries, ranks_inside):
    """A horizontal band whose thickness at each stage is the linkage level."""
    n = len(stages)
    gapx = 12
    stw = (W - 2 * M - gapx * (n - 1)) / n
    xs = [M + k * (stw + gapx) for k in range(n)]
    top, bot = [], []
    for k, (_, status) in enumerate(entries):
        half = 4 + LEVEL[status] * 7
        cx = xs[k] + stw / 2
        top.append((cx, y_mid - half))
        bot.append((cx, y_mid + half))
    top = [(M, top[0][1])] + top + [(W - M, top[-1][1])]
    bot = [(M, bot[0][1])] + bot + [(W - M, bot[-1][1])]
    pg.polygon(top + bot[::-1], fill=FILL2, stroke=None)
    for k, (rank, status) in enumerate(entries):
        cx = xs[k] + stw / 2
        pg.text(cx, y_mid + 2.5, status, 7, INK, bold=True, align=1)
        pg.text(cx, y_mid + 42, rank, 6.5, DARK, align=1)
    return xs, stw


def page2(doc):
    pg = Page(doc, 2, 2, "Where is development deliberately linked to progression?",
              "The two continuums at the same transitions, then the question for Army. No recommendation.")
    n = len(STAGES)
    gapx = 12
    stw = (W - 2 * M - gapx * (n - 1)) / n
    for k, t in enumerate(STAGES):
        pg.text(M + k * (stw + gapx) + stw / 2, 72, t, 6.5, MID, bold=True, align=1)
        if k:
            pg.line(M + k * (stw + gapx) - gapx / 2, 66, M + k * (stw + gapx) - gapx / 2, 300, LIGHT, dashes="[1 2] 0")
    pg.text(M, 86, "OFFICER", 7, INK, bold=True)
    band(pg, 122, STAGES, OFFICER_STAGES, True)
    pg.text(M, 194, "SOLDIER", 7, INK, bold=True)
    band(pg, 230, STAGES, SOLDIER_STAGES, True)
    pg.text(M, 290, "Band thickness is the strength of the link between the development and the career transition: mandated, functionally required, expected, self-selected.", 6, MID)

    # statement
    pg.box(M, 306, W - 2 * M, 30, fill=WHITE, stroke=INK, width=1.2)
    pg.textbox(M + 10, 312, W - 2 * M - 20, 22, PAGE2_STATEMENT, 8.5, INK, bold=True, align=1, lh=1.2)

    # three facts
    fy = 348
    cw = (W - 2 * M - 20) / 3
    for k, (head, body) in enumerate(FACTS):
        x = M + k * (cw + 10)
        pg.text(x, fy, head, 7, INK, bold=True)
        pg.textbox(x, fy + 4, cw, 34, body, 7.5, DARK, lh=1.25)

    # the question
    pg.box(M, 398, W - 2 * M, 104, fill=FILL, stroke=None)
    pg.text(W / 2, 424, "IS THIS A CONSCIOUS CHOICE?", 15, INK, bold=True, align=1)
    pg.textbox(M + 40, 438, (W - 2 * M - 100) / 2, 50, "IF YES:\n" + IF_YES, 8, INK, lh=1.3)
    pg.textbox(W / 2 + 10, 438, (W - 2 * M - 100) / 2, 50, "IF NO:\n" + IF_NO, 8, INK, lh=1.3)
    pg.text(W / 2, 494, "No recommendation. The organisation answers.", 7, MID, align=1)
    pg.note(M, 512, W - 2 * M,
            "The officer band narrows at CAPT to MAJ and widens again at the top; the soldier band beneath is the comparator. "
            "Neither band is labelled a gap or a finding. History and the assessment offered at the meeting are speaker notes.")


# Working paper: current and desired, held back from the discussion piece.
FUTURE = [
    ("Entry\nLead Self", "Civilian > PTE", "Lead Self; train-the-trainer (TAD, ACS)", "Compulsory", "No change",
     "Civilian > OCDT", "Lead Self; as for soldiers", "Compulsory", "No change"),
    ("T1\nLead Teams", "PTE > LCPL", "ELDA + LDS Lead Teams; inside JNCO course (ALC)", "Mandated", "No change",
     "OCDT > 2LT", "ELDA + LDS Lead Teams; inside NZCC (ALC at OCS)", "Mandated (embedded)", "No change"),
    ("T2\nLead Leaders", "CPL > SGT", "ELDA + LDS Lead Leaders; inside SNCO course (ALC)", "Mandated", "No change",
     "2LT / LT > CAPT", "ELDA + LDS Lead Leaders; distributed window after 2 years in unit (ALC)", "Functionally required; not in policy", "Mandated for substantive CAPT"),
    ("T3\nLead Systems", "SSGT > WO2", "ELDA Lead Systems inside WO course (ALC); LDS Lead Systems (ILD)", "ELDA mandated; LDS to confirm", "LDS prerequisite confirmed; ILD seats aligned to promotion timing",
     "CAPT > MAJ", "ELDA Lead Systems (ALC); LDS Lead Systems (ILD)", "Self-selected; not policed", "Mandated before OC appointment"),
    ("T4\nLead Capability", "WO2 > WO1", "LDS Lead Capability (ILD)", "Expected; policy to confirm", "Mandated; ILD seat guaranteed",
     "MAJ > LTCOL", "LDS Lead Capability (ILD)", "Expected; policy to confirm", "Mandated"),
    ("T5\nLead Integrated\nCapability", "WO1 > Senior WO1", "LDS LIC: ELDA week (ALC / Navy) + LDS week (ILD)", "Expected; full attendance", "Stated in policy",
     "LTCOL > COL", "LDS LIC: ELDA week (ALC / Navy) + LDS week (ILD)", "Expected; full attendance", "Stated in policy"),
    ("T6\nLead Organisation", "Senior WO1", "LDS Lead Organisation + ELDA (ILD; contracted facilitation)", "Expected; full attendance", "Stated in policy",
     "COL > BRIG", "LDS Lead Organisation + ELDA (ILD; contracted facilitation)", "Expected; full attendance", "Stated in policy"),
]


def working_paper(doc):
    pg = Page(doc, 1, 1, "Current and desired: working paper",
              "The future state as described at the 9 Sep meeting. Not part of the discussion piece; not an endorsed position. Held until AITC has answered the question on page 2.",
              tag="WORKING PAPER  ·  NOT FOR TABLING")
    heads = ["LDF TRANSITION", "SOLDIER: RANK", "COURSE AND DELIVERY", "LINKAGE NOW", "DESIRED",
             "OFFICER: RANK", "COURSE AND DELIVERY", "LINKAGE NOW", "DESIRED"]
    widths = [56, 56, 122, 78, 90, 56, 122, 78, 90]
    xs = [M]
    for wd in widths[:-1]:
        xs.append(xs[-1] + wd)
    y = 72
    for h, x, wd in zip(heads, xs, widths):
        pg.labelled(x, y, wd, 16, h, fill=DARK, size=5.5, bold=True, color=WHITE, stroke=WHITE)
    y += 16
    rowh = 42
    for row in FUTURE:
        for k, (c, x, wd) in enumerate(zip(row, xs, widths)):
            changed = k in (4, 8) and c != "No change"
            fill = FILL2 if k == 0 else (FILL if changed else WHITE)
            pg.box(x, y, wd, rowh, fill=fill, stroke=LIGHT)
            pg.textbox(x + 3, y + 4, wd - 6, rowh - 6, c, 5.8 if k == 0 else 5.6,
                       INK if (k == 0 or changed) else DARK, bold=(k == 0 or changed), lh=1.15)
            if changed:
                pg.chip(x + wd - 3, y + rowh - 11, "CHANGE", fill=INK, color=WHITE, right=True)
        y += rowh
    pg.line(xs[5] - 1, 72, xs[5] - 1, y, DARK, width=1.2)

    y += 10
    pg.box(M, y, W - 2 * M, 54, fill=FILL, stroke=None)
    pg.text(M + 10, y + 13, "WHAT THIS WOULD INVOLVE, AND WHAT IS NOT YET KNOWN", 7, INK, bold=True)
    pg.textbox(M + 10, y + 17, W - 2 * M - 20, 36,
               "No new course would need designing: ILD and NZLC already deliver each course on this page. The change is the linkage written "
               "into promotion policy, ILD seat allocation aligned to Army promotion timing, and the officer window placed after unit experience. "
               "Whether guaranteed seats and aligned timing carry a capacity or resource implication is not known and must be tested before any of this is proposed.",
               6.5, DARK, lh=1.3)
    pg.note(M, y + 62, W - 2 * M,
            "Shaded DESIRED cells are the change. This page answers the meeting action for a current-versus-desired mapping and stays "
            "an ALC working paper: COMDT asked whether the difference is deliberate, and Army has not yet answered.")


def build():
    doc = pymupdf.open()
    page1(doc)
    page2(doc)
    doc.set_metadata({"title": "Officer and Soldier Leadership Development: Wireframes", "author": "NZALC"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")
    wp = pymupdf.open()
    working_paper(wp)
    wp.set_metadata({"title": "Officer and Soldier Leadership Development: Future State Working Paper", "author": "NZALC"})
    wp.save(OUT_WP, garbage=3, deflate=True)
    print(f"Saved {OUT_WP}")


if __name__ == "__main__":
    build()
