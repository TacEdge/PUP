#!/usr/bin/env python3
"""
Low-fidelity wireframes for the AITC discussion piece on Officer and
Soldier leadership development: two landscape pages drawn as a PDF with
PyMuPDF.  Grey and boxy on purpose, so the conversation stays on
structure.

    python3 build_ldf_wireframes.py   ->  output/ldf-alignment-wireframes.pdf
"""

import math

import pymupdf

OUT = "./output/ldf-alignment-wireframes.pdf"
W, H = 842, 595
M = 36

INK = (0.12, 0.12, 0.12)
MID = (0.45, 0.45, 0.45)
LIGHT = (0.80, 0.80, 0.80)
FILL = (0.94, 0.94, 0.94)
FILL2 = (0.88, 0.88, 0.88)
DARK = (0.30, 0.30, 0.30)
NOTE = (0.55, 0.36, 0.08)
WHITE = (1, 1, 1)

HEADLINE = ("How deliberately does Army link leadership development to "
            "progression through its Officer and Soldier promotion continuums?")
PAGE1_QUESTION = ("If Army deliberately mandates leadership development for soldiers as they "
                  "progress through increased leadership responsibility, why is the same "
                  "principle not applied consistently to officers?")
LEVELS = ["LEAD SELF", "LEAD TEAMS", "LEAD LEADERS", "LEAD SYSTEMS",
          "LEAD CAPABILITY", "LEAD INTEGRATED\nCAPABILITY", "LEAD ORGANISATION"]

# One entry per LDF transition (the gap between level i and i+1).  Text is
# limited to what the four sources and the NZALC course data sheets support;
# everything else is a placeholder.  Rank pairings are the LDS poster's own
# estimate, so every rank line is TO CONFIRM.
SOLDIER = [
    dict(frm="PTE", to="LCPL / CPL", dev="A1530 JNCO Course includes\nELDA Lead Teams (A18011)\nand LDS Lead Teams (D03020)", state="MANDATED?", tag="TO CONFIRM"),
    dict(frm="CPL", to="SGT", dev="A1531 SNCO Course;\nELDA Lead Leaders (A18008);\nLDS Lead Leaders (D03030) prerequisite", state="MANDATED?", tag="TO CONFIRM"),
    dict(frm="SSGT / WO2", to="WO1", dev="A1532 WO Course;\nELDA Lead Systems (A18010)", state="MANDATED?", tag="TO CONFIRM"),
    dict(frm="WO1", to="Tier 5 WO", dev="LDS Lead Capability\n(ILD delivered)", state="?", tag="DATA REQUIRED"),
    dict(frm="Tier 5 WO", to="Tier 4 WO", dev="LDS Lead Integrated\n(ILD delivered)", state="?", tag="DATA REQUIRED"),
    dict(frm="Tier 4 WO", to="Tier 3 WO+", dev="LDS Lead Organisation\n(ILD delivered)", state="?", tag="DATA REQUIRED"),
]
OFFICER = [
    dict(frm="OCDT", to="2LT", dev="Commissioning course;\nLDS Lead Teams embedded?", state="?", tag="DATA REQUIRED"),
    dict(frm="2LT / LT", to="CAPT", dev="ELDA Lead Leaders (A18008)\ntargets 2LT and LT.\nLink to substantive CAPT: the live request", state="NOT MANDATED?", tag="TO CONFIRM"),
    dict(frm="CAPT", to="MAJ", dev="ELDA Lead Systems (A18010)\ntargets CAPT pre-MAJ;\nA1302 Staff and Tactics referenced", state="NOT MANDATED?", tag="TO CONFIRM"),
    dict(frm="MAJ", to="LTCOL", dev="LDS Lead Capability\n(ILD delivered)", state="?", tag="DATA REQUIRED"),
    dict(frm="LTCOL", to="COL", dev="LDS Lead Integrated\n(ILD delivered)", state="?", tag="DATA REQUIRED"),
    dict(frm="COL", to="BRIG+", dev="LDS Lead Organisation\n(ILD delivered)", state="?", tag="DATA REQUIRED"),
]


class Page:
    def __init__(self, doc, number, title, purpose):
        self.p = doc.new_page(width=W, height=H)
        self.text(M, 22, f"WIREFRAME {number} OF 2", 7, MID)
        self.text(W - M, 22, "OFFICER AND SOLDIER LEADERSHIP DEVELOPMENT  ·  AITC DISCUSSION PIECE  ·  LOW FIDELITY", 7, MID, align=2)
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

    def labelled(self, x, y, w, h, label, fill=FILL, size=7.5, bold=False,
                 color=INK, stroke=MID, dashes=None):
        self.box(x, y, w, h, fill=fill, stroke=stroke, dashes=dashes)
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

    def chip(self, x, y, s, fill=FILL2, color=INK):
        w = pymupdf.get_text_length(s, fontname="helvetica-bold", fontsize=5.5) + 8
        self.box(x, y, w, 9, fill=fill, stroke=None)
        self.text(x + 4, y + 6.8, s, 5.5, color, bold=True)
        return w

    def note(self, x, y, w, s):
        self.text(x, y + 8, "VISUAL LOGIC", 6.5, NOTE, bold=True)
        self.textbox(x, y + 12, w, 120, s, 6.8, NOTE)


def side(pg, entries, x, w, y_of, mandated_style, title):
    """One continuum column: rank -> development box -> next rank, aligned
    to the LDF transition rows."""
    pg.labelled(x, 92, w, 18, title, fill=DARK, size=7.5, bold=True, color=WHITE, stroke=None)
    for i, e in enumerate(entries):
        y = y_of(i)
        # rank line
        pg.text(x + w / 2, y - 6, f"{e['frm']}   >   {e['to']}", 7, INK, bold=True, align=1)
        # development box
        bx, by, bw, bh = x + 8, y + 2, w - 16, 40
        if mandated_style:
            pg.box(bx, by, bw, bh, fill=FILL2, stroke=DARK)
        else:
            pg.box(bx, by, bw, bh, fill=WHITE, stroke=DARK, dashes="[3 2] 0")
        pg.text(bx + 5, by + 8, e["state"], 6.5, INK, bold=True)
        pg.textbox(bx + 5, by + 11, bw - 10, bh - 12, e["dev"], 5.6, DARK, lh=1.15)
        pg.chip(bx + bw - 62, by + bh - 10, e["tag"], fill=FILL2 if e["tag"] == "TO CONFIRM" else WHITE, color=MID)


def page1(doc):
    pg = Page(doc, 1, "Two continuums. One leadership framework.",
              "One visual. The LDF is the common spine; the two Army promotion continuums are mapped against it, side by side.")
    # headline
    pg.textbox(M, 62, W - 2 * M, 30, HEADLINE, 11, INK, bold=True, align=1, lh=1.2)

    spine_x, spine_w = W / 2 - 70, 140
    side_w = spine_x - M - 24
    top, rowh = 118, 58

    def y_of(i):            # y of transition i sits between level i and i+1
        return top + i * rowh + 30

    # spine: seven levels, arrows between
    pg.labelled(spine_x, 92, spine_w, 18, "LEADERSHIP DEVELOPMENT FRAMEWORK", fill=INK, size=6.5, bold=True, color=WHITE, stroke=None)
    for i, lvl in enumerate(LEVELS):
        y = top + i * rowh
        pg.labelled(spine_x + 10, y, spine_w - 20, 22, lvl, fill=FILL2 if i % 2 else FILL, size=6.5, bold=True)
        if i < 6:
            pg.arrow(W / 2, y + 22, W / 2, y + rowh - 1, color=DARK)
            pg.text(W / 2 + 6, y + rowh / 2 + 12, f"T{i + 1}", 5.5, MID)
    # connectors from each transition to both sides
    for i in range(6):
        y = y_of(i) + 22
        pg.line(spine_x - 16, y, spine_x, y, LIGHT)
        pg.line(spine_x + spine_w, y, spine_x + spine_w + 16, y, LIGHT)

    side(pg, OFFICER, M, side_w, y_of, mandated_style=False, title="OFFICER CONTINUUM")
    side(pg, SOLDIER, spine_x + spine_w + 24, side_w, y_of, mandated_style=True, title="SOLDIER CONTINUUM")

    pg.text(M, 500, "Rank pairings are the LDS poster's estimate of rank to level and are shown to place the comparison, not to assert equivalence.", 6, MID)
    # bottom question band
    pg.box(M, 506, W - 2 * M, 42, fill=DARK, stroke=None)
    pg.text(M + 10, 518, "THE QUESTION", 6, FILL2, bold=True)
    pg.textbox(M + 10, 521, W - 2 * M - 20, 28, PAGE1_QUESTION, 8.5, WHITE, bold=True, lh=1.2)
    pg.note(M, 552, W - 2 * M,
            "Read across any row: same LDF transition, what does Army require of a soldier, what does it require of an officer? "
            "Solid boxes are the soldier side (development inside the promotion course); dashed boxes are the officer side, "
            "where development exists but the link to promotion is the thing under test. Chips mark the evidence state. The "
            "polished version carries confirmed course codes and drops the placeholders; nothing here asserts a finding.")


def page2(doc):
    pg = Page(doc, 2, "The discrepancy",
              "The answer emerging from page 1, drawn as two flows. Then the challenge, in COMDT's posture: is this a conscious choice?")
    colw = 300
    xs = {"SOLDIER": W / 2 - colw - 30, "OFFICER": W / 2 + 30}
    flows = {
        "SOLDIER": (["PROMOTION POINT", "MANDATED DEVELOPMENT", "DEVELOPMENT COMPLETED", "PROMOTION"], "DELIBERATE LINK", True),
        "OFFICER": (["PROMOTION POINT", "DEVELOPMENT EXISTS", "NOT MANDATED?", "PROMOTION"], "UNCLEAR LINK", False),
    }
    for name, (steps, verdict, solid) in flows.items():
        x = xs[name]
        pg.labelled(x, 80, colw, 20, name, fill=DARK, size=8, bold=True, color=WHITE, stroke=None)
        y = 116
        for j, s in enumerate(steps):
            dashed = None if (solid or j in (0, 3)) else "[3 2] 0"
            pg.labelled(x + 60, y, colw - 120, 26, s, fill=FILL2 if solid else WHITE, size=7.5, bold=True, dashes=dashed, stroke=DARK)
            if j < 3:
                pg.arrow(x + colw / 2, y + 26, x + colw / 2, y + 44)
            y += 46
        pg.labelled(x + 60, y + 6, colw - 120, 22, verdict, fill=INK if solid else WHITE, size=8, bold=True,
                    color=WHITE if solid else INK, stroke=INK, dashes=None if solid else "[3 2] 0")
    pg.text(W / 2, 200, "same LDF transition", 6.5, MID, align=1)
    pg.line(W / 2, 208, W / 2, 300, LIGHT, dashes="[2 2] 0")

    # the challenge
    pg.box(M, 342, W - 2 * M, 150, fill=FILL, stroke=None)
    pg.text(W / 2, 372, "IS THIS DIFFERENCE A CONSCIOUS CHOICE?", 13, INK, bold=True, align=1)
    pg.textbox(M + 40, 392, (W - 2 * M - 100) / 2, 80,
               "IF SO:\nwhat is the rationale for treating Officer and Soldier leadership development differently?", 8, INK, lh=1.3)
    pg.textbox(W / 2 + 10, 392, (W - 2 * M - 100) / 2, 80,
               "IF NOT:\nshould Army apply a more consistent principle to development before progression into increased leadership responsibility?", 8, INK, lh=1.3)
    pg.text(W / 2, 480, "No recommendation. The organisation answers.", 7, MID, align=1)
    pg.note(M, 500, W - 2 * M,
            "Two flows, identical steps, one difference: the soldier flow is solid at every step and ends in a deliberate link; "
            "the officer flow goes dashed at the point under test and ends in an unclear link. The question is posed in COMDT's "
            "posture (are we consciously choosing to deviate, and if so why?), with both branches given equal weight so the "
            "page does not argue that the officer system is wrong. It requires Army to articulate the reason, or the change.")


def build():
    doc = pymupdf.open()
    page1(doc)
    page2(doc)
    doc.set_metadata({"title": "Officer and Soldier Leadership Development: Wireframes", "author": "NZALC"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
