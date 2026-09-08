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

# One entry per LDF transition (the gap between level i and i+1).  Cells
# carry what the 9 Sep 2026 NZALC meeting (Mike and Dave) stated about each
# transition, tagged STATED 9 SEP until checked against promotion policy and
# the promotion-course data sheets.  Rank pairings follow the meeting (WO2 is
# the Lead Systems tick, WO1 the Lead Capability tick); the LDS poster calls
# its own rank mapping an estimate.
TAG_MEETING = "STATED 9 SEP"
TAG_CONFIRM = "TO CONFIRM"
TAG_DATA = "DATA REQUIRED"

ENTRY_SOLDIER = "On entry (civilian to soldier): Lead Self is compulsory, delivered through train-the-trainer."
ENTRY_OFFICER = "On entry (civilian to OCDT): Lead Self is compulsory, as for soldiers."

SOLDIER = [
    dict(frm="PTE", to="LCPL", state="MANDATED",
         dev="A1530 JNCO Course includes ELDA Lead Teams (A18011), embedded as the performance-under-pressure "
             "module, with LDS Lead Teams (D03020) sequenced alongside. Qualifying on the course qualifies the leadership content.",
         tag=TAG_MEETING),
    dict(frm="CPL", to="SGT", state="MANDATED IN PROMOTION POLICY",
         dev="Promotion to SGT requires the SNCO course (A1531), which carries ELDA Lead Leaders (A18008) and "
             "LDS Lead Leaders (D03030). 'Very clear on the NCO front.'",
         tag=TAG_MEETING),
    dict(frm="SSGT", to="WO2", state="ELDA MANDATED; LDS PREREQUISITE TO CHECK",
         dev="ELDA Lead Systems (A18010) is mandated on the WO course (A1532). LDS Lead Systems is delivered by ILD "
             "(tri-service) and Army cannot guarantee seats, so it is routinely done before or after the promotion course. "
             "Whether it is a prerequisite for WO2: Dave to check the CDS.",
         tag=TAG_MEETING),
    dict(frm="WO2", to="WO1", state="EXPECTED; NOT IN POLICY?",
         dev="LDS Lead Capability, ILD tri-service course. WO1 is the Lead Capability tick and the course is expected "
             "for promotion, but 'pretty sure' it is not mandated in policy. Most attend, subject to an ILD seat.",
         tag=TAG_MEETING),
    dict(frm="WO1", to="Senior WO1", state="MANDATE NOT STATED; FULL ATTENDANCE",
         dev="LDS Lead Integrated Capability: one ELDA week (ALC caving or Navy sailing) and one LDS week in Wellington, "
             "both run and funded by ILD. 12 to 16 students a course; WO1s attend without exception.",
         tag=TAG_MEETING),
    dict(frm="Senior WO1", to="SMA-level appointments", state="MANDATE NOT STATED; FULL ATTENDANCE",
         dev="LDS Lead Organisation with an ELDA component (retreat setting, equine behaviour, psychometric profiling, "
             "external facilitation). For those considered for the senior appointments; all complete it well before they need to.",
         tag=TAG_MEETING),
]
OFFICER = [
    dict(frm="OCDT", to="2LT", state="EMBEDDED IN NZCC",
         dev="NZCC includes ELDA Lead Teams (the former Nemesis, rebranded with the same learning outcomes) and "
             "LDS Lead Teams, delivered by ALC at OCS in March, two years running. Qualifying on NZCC qualifies both.",
         tag=TAG_MEETING),
    dict(frm="2LT / LT", to="CAPT", state="RECOMMENDED, NOT MANDATED",
         dev="ELDA Lead Leaders (A18008) and LDS Lead Leaders are recommended, not in promotion policy. Policed in "
             "function by OCS and COs: in practice no 2LT or LT promotes without it. 'Super murky on the officer front.' "
             "This is the substantive CAPT request.",
         tag=TAG_MEETING),
    dict(frm="CAPT", to="MAJ", state="NOT MANDATED; NOT POLICED; LOW UPTAKE",
         dev="Neither ELDA Lead Systems (A18010) nor the ILD LDS Lead Systems course is mandated, and neither is policed "
             "in function. Uptake is self-selecting: those inclined attend, those who most need it opt out. CAPT to OC is "
             "the largest single jump in scope of influence.",
         tag=TAG_MEETING),
    dict(frm="MAJ", to="LTCOL", state="NOT MANDATED; MOST ATTEND",
         dev="LDS Lead Capability (ILD). Not mandated; the impression is that MAJ to LTCOL all complete it. "
             "Self-selected and scrutinised at this level.",
         tag=TAG_MEETING),
    dict(frm="LTCOL", to="COL", state="MANDATE NOT STATED; FULL ATTENDANCE",
         dev="LDS Lead Integrated Capability (ILD): the ELDA week plus the Wellington week, as for the soldier side. "
             "LTCOL and COL attend without exception.",
         tag=TAG_MEETING),
    dict(frm="COL", to="BRIG", state="MANDATE NOT STATED; FULL ATTENDANCE",
         dev="LDS Lead Organisation with ELDA component. COL and BRIG considered for the senior appointments; "
             "all do it, well before it is required.",
         tag=TAG_MEETING),
]
# Where the meeting said the gap bites: officer transitions 2 and 3.
OFFICER_GAP = (1, 2)


class Page:
    def __init__(self, doc, number, title, purpose):
        self.p = doc.new_page(width=W, height=H)
        self.text(M, 22, f"WIREFRAME {number} OF 3", 7, MID)
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

    def chip(self, x, y, s, fill=FILL2, color=INK, right=False):
        w = pymupdf.get_text_length(s, fontname="helvetica-bold", fontsize=5.5) + 8
        if right:
            x = x - w
        self.box(x, y, w, 9, fill=fill, stroke=None)
        self.text(x + 4, y + 6.8, s, 5.5, color, bold=True)
        return w

    def note(self, x, y, w, s):
        self.text(x, y + 8, "VISUAL LOGIC", 6.5, NOTE, bold=True)
        self.textbox(x, y + 12, w, 120, s, 6.8, NOTE)


def side(pg, entries, x, w, y_of, mandated_style, title, entry, gap=()):
    """One continuum column: rank -> development box -> next rank, aligned
    to the LDF transition rows."""
    pg.labelled(x, 92, w, 18, title, fill=DARK, size=7.5, bold=True, color=WHITE, stroke=None)
    pg.textbox(x + 4, 112, w - 8, 14, entry, 5.4, MID, align=1)
    for i, e in enumerate(entries):
        y = y_of(i)
        # rank line
        pg.text(x + w / 2, y - 6, f"{e['frm']}   >   {e['to']}", 7, INK, bold=True, align=1)
        # development box
        bx, by, bw, bh = x + 8, y + 2, w - 16, 42
        in_gap = i in gap
        if mandated_style:
            pg.box(bx, by, bw, bh, fill=FILL2, stroke=DARK)
        else:
            pg.box(bx, by, bw, bh, fill=WHITE, stroke=INK if in_gap else DARK,
                   width=1.6 if in_gap else 0.8, dashes="[3 2] 0")
        pg.text(bx + 5, by + 8, e["state"], 6, INK, bold=True)
        cw = pg.chip(bx + bw - 4, by + 2.5, e["tag"], fill=FILL2 if e["tag"] == TAG_MEETING else WHITE, color=MID, right=True)
        pg.textbox(bx + 5, by + 11, bw - 10, bh - 11, e["dev"], 5.3, DARK, lh=1.12)
    if gap:
        y0, y1 = y_of(gap[0]) - 12, y_of(gap[-1]) + 46
        pg.line(x - 10, y0, x - 10, y1, INK, width=1.4)
        pg.line(x - 10, y0, x - 4, y0, INK, width=1.4)
        pg.line(x - 10, y1, x - 4, y1, INK, width=1.4)
        pg.p.insert_text((x - 13, (y0 + y1) / 2 + 40), "THE GAP: THE MIDDLE CREW", fontsize=5.5,
                         fontname="helvetica-bold", color=INK, rotate=90)


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

    side(pg, OFFICER, M + 14, side_w - 14, y_of, mandated_style=False, title="OFFICER CONTINUUM",
         entry=ENTRY_OFFICER, gap=OFFICER_GAP)
    side(pg, SOLDIER, spine_x + spine_w + 24, side_w, y_of, mandated_style=True, title="SOLDIER CONTINUUM",
         entry=ENTRY_SOLDIER)

    pg.text(M, 500, "Rank pairings follow the 9 Sep meeting (WO2 is the Lead Systems tick, WO1 the Lead Capability tick); the LDS poster calls its own "
                    "rank mapping an estimate. They place the comparison; they do not assert equivalence.", 6, MID)
    # bottom question band
    pg.box(M, 506, W - 2 * M, 42, fill=DARK, stroke=None)
    pg.text(M + 10, 518, "THE QUESTION", 6, FILL2, bold=True)
    pg.textbox(M + 10, 521, W - 2 * M - 20, 28, PAGE1_QUESTION, 8.5, WHITE, bold=True, lh=1.2)
    pg.note(M, 552, W - 2 * M,
            "Read across any row: same LDF transition, what does Army require of a soldier, what does it require of an officer? "
            "Solid boxes are the soldier side; dashed boxes are the officer side, where development exists but the link to promotion "
            "is the thing under test. The heavy dashed boxes are where the meeting said the gap bites. STATED 9 SEP marks a fact "
            "stated at the NZALC meeting of 9 Sep 2026 and not yet verified against promotion policy or a course data sheet; the "
            "polished version carries verified sources only.")


def page2(doc):
    pg = Page(doc, 2, "The discrepancy",
              "The answer emerging from page 1, drawn as two flows. The background decision-makers should have. Then the challenge, in COMDT's posture.")
    colw = 300
    xs = {"SOLDIER": W / 2 - colw - 30, "OFFICER": W / 2 + 30}
    flows = {
        "SOLDIER": (["PROMOTION POINT", "DEVELOPMENT MANDATED IN POLICY", "DEVELOPMENT COMPLETED", "PROMOTION"], "DELIBERATE LINK", True),
        "OFFICER": (["PROMOTION POINT", "DEVELOPMENT EXISTS, RECOMMENDED", "NOT IN POLICY: POLICED IN FUNCTION (T2),\nSELF-SELECTED (T3 AND ABOVE)", "PROMOTION"], "UNCLEAR LINK", False),
    }
    for name, (steps, verdict, solid) in flows.items():
        x = xs[name]
        pg.labelled(x, 74, colw, 18, name, fill=DARK, size=8, bold=True, color=WHITE, stroke=None)
        y = 102
        for j, s in enumerate(steps):
            dashed = None if (solid or j in (0, 3)) else "[3 2] 0"
            pg.labelled(x + 40, y, colw - 80, 26, s, fill=FILL2 if solid else WHITE, size=6.5, bold=True, dashes=dashed, stroke=DARK)
            if j < 3:
                pg.arrow(x + colw / 2, y + 26, x + colw / 2, y + 40)
            y += 40
        pg.labelled(x + 60, y + 2, colw - 120, 20, verdict, fill=INK if solid else WHITE, size=8, bold=True,
                    color=WHITE if solid else INK, stroke=INK, dashes=None if solid else "[3 2] 0")
    pg.text(W / 2, 170, "same LDF transition", 6.5, MID, align=1)
    pg.line(W / 2, 176, W / 2, 262, LIGHT, dashes="[2 2] 0")

    # background strip: what decision-makers should know before deciding
    by = 300
    pg.text(M, by - 4, "BACKGROUND THE DECISION-MAKERS SHOULD HAVE (STATED 9 SEP; TO BE VERIFIED)", 6.5, INK, bold=True)
    cols = [
        ("WHAT HAS BEEN TRIED",
         "A two-year pilot attached Lead Leaders to Grade 2 and 3 coursing; withdrawn as untenable time away from units. "
         "A distributed, self-scheduled approach was agreed instead. The Post Commissioning Programme put every junior "
         "officer through Lead Leaders, but before unit experience: the wrong time."),
        ("WHY IT STALLED",
         "AITC agreed in principle that officers should complete it; the proposal was parked in a headquarters restructure. "
         "ACS was not at the table for later course redesigns, so no coordinated look at where the training nests. "
         "Above Lead Leaders, delivery passed to ILD in 2012 and Army cannot guarantee seats."),
        ("THE EXPLANATION OFFERED (NOT ESTABLISHED)",
         "'A scheduling oversight in the face of tempo': training that is not required is the training that gets bumped. "
         "Senior leaders complete everything and may assume everyone does. The middle, 2LT to MAJ, is where it is missed, "
         "and it is the formative first years in unit."),
    ]
    cw = (W - 2 * M - 20) / 3
    for k, (head, body) in enumerate(cols):
        x = M + k * (cw + 10)
        pg.box(x, by, cw, 78, fill=WHITE, stroke=LIGHT)
        pg.text(x + 6, by + 10, head, 6, INK, bold=True)
        pg.textbox(x + 6, by + 14, cw - 12, 62, body, 6, DARK, lh=1.25)

    # the challenge
    pg.box(M, 390, W - 2 * M, 110, fill=FILL, stroke=None)
    pg.text(W / 2, 414, "IS THIS DIFFERENCE A CONSCIOUS CHOICE?", 13, INK, bold=True, align=1)
    pg.textbox(M + 40, 428, (W - 2 * M - 100) / 2, 60,
               "IF SO:\nwhat is the rationale for treating Officer and Soldier leadership development differently?", 8, INK, lh=1.3)
    pg.textbox(W / 2 + 10, 428, (W - 2 * M - 100) / 2, 60,
               "IF NOT:\nshould Army apply a more consistent principle to development before progression into increased leadership responsibility?", 8, INK, lh=1.3)
    pg.text(W / 2, 490, "No recommendation. The organisation answers. Page 3 shows what 'yes' would look like, if asked.", 7, MID, align=1)
    pg.note(M, 508, W - 2 * M,
            "Two flows, identical steps, one difference: the soldier flow is solid at every step and ends in a deliberate link; "
            "the officer flow goes dashed at the point under test and ends in an unclear link. The background strip is there so the "
            "discussion does not retread ground already tried; the explanation offered at the meeting is shown as a candidate, not a "
            "finding. The question is posed in COMDT's posture, both branches given equal weight.")


FUTURE = [
    # transition, soldier: rank, course and delivery, mandate now, desired; officer: same
    ("Entry\nLead Self", "Civilian > PTE", "Lead Self; train-the-trainer (TAD, ACS)", "Compulsory", "No change",
     "Civilian > OCDT", "Lead Self; as for soldiers", "Compulsory", "No change"),
    ("T1\nLead Teams", "PTE > LCPL", "ELDA + LDS Lead Teams; inside JNCO course (ALC)", "Mandated", "No change",
     "OCDT > 2LT", "ELDA + LDS Lead Teams; inside NZCC (ALC at OCS)", "Embedded", "No change"),
    ("T2\nLead Leaders", "CPL > SGT", "ELDA + LDS Lead Leaders; inside SNCO course (ALC)", "Mandated in policy", "No change",
     "2LT / LT > CAPT", "ELDA + LDS Lead Leaders; distributed window after 2 years in unit (ALC)", "Recommended; policed in function", "Mandated in policy for substantive CAPT"),
    ("T3\nLead Systems", "SSGT > WO2", "ELDA Lead Systems inside WO course (ALC); LDS Lead Systems (ILD)", "ELDA mandated; LDS prerequisite to check", "LDS prerequisite confirmed; ILD seats aligned to promotion timing",
     "CAPT > MAJ", "ELDA Lead Systems (ALC); LDS Lead Systems (ILD)", "Not mandated; self-selected", "Mandated in policy before OC appointment"),
    ("T4\nLead Capability", "WO2 > WO1", "LDS Lead Capability (ILD)", "Expected; not in policy?", "Mandated in policy; ILD seat guaranteed",
     "MAJ > LTCOL", "LDS Lead Capability (ILD)", "Not mandated; most attend", "Mandated in policy"),
    ("T5\nLead Integrated\nCapability", "WO1 > Senior WO1", "LDS LIC: ELDA week (ALC / Navy) + LDS week (ILD)", "Not stated; full attendance", "Stated in policy",
     "LTCOL > COL", "LDS LIC: ELDA week (ALC / Navy) + LDS week (ILD)", "Not stated; full attendance", "Stated in policy"),
    ("T6\nLead Organisation", "Senior WO1", "LDS Lead Organisation + ELDA (ILD; contracted facilitation)", "Not stated; full attendance", "Stated in policy",
     "COL > BRIG", "LDS Lead Organisation + ELDA (ILD; contracted facilitation)", "Not stated; full attendance", "Stated in policy"),
]


def page3(doc):
    pg = Page(doc, 3, "Current and desired: one page",
              "The future state the meeting described: course, transition, who delivers, and the mandate written into promotion policy. Detachable; tabled only if AITC asks what 'yes' means.")
    heads = ["LDF TRANSITION", "SOLDIER: RANK", "COURSE AND DELIVERY", "MANDATE NOW", "DESIRED",
             "OFFICER: RANK", "COURSE AND DELIVERY", "MANDATE NOW", "DESIRED"]
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
        for k, (cell, x, wd) in enumerate(zip(row, xs, widths)):
            changed = k in (4, 8) and cell != "No change"
            fill = FILL2 if k == 0 else (FILL if changed else WHITE)
            pg.box(x, y, wd, rowh, fill=fill, stroke=LIGHT)
            if k == 0:
                pg.textbox(x + 3, y + 4, wd - 6, rowh - 6, cell, 5.8, INK, bold=True, lh=1.15)
            else:
                pg.textbox(x + 3, y + 4, wd - 6, rowh - 6, cell, 5.6, INK if changed else DARK, bold=changed, lh=1.15)
            if changed:
                pg.chip(x + wd - 3, y + rowh - 11, "CHANGE", fill=INK, color=WHITE, right=True)
        y += rowh
    pg.line(xs[5] - 1, 72, xs[5] - 1, y, DARK, width=1.2)

    y += 10
    pg.box(M, y, W - 2 * M, 54, fill=FILL, stroke=None)
    pg.text(M + 10, y + 13, "WHAT CHANGES, AND WHAT DOES NOT", 7, INK, bold=True)
    pg.textbox(M + 10, y + 17, W - 2 * M - 20, 36,
               "No new courses and no new money: ILD and NZLC already deliver every course on this page. The change is procedural: "
               "the mandate written into promotion policy at each transition, for both continuums, with ILD seat allocation aligned to Army "
               "promotion timing and the officer window placed after unit experience, not at OCS. Completion then becomes a reportable metric.",
               6.5, DARK, lh=1.3)
    pg.note(M, y + 62, W - 2 * M,
            "Shaded DESIRED cells are the change; unshaded rows already match. Content is the future state as described at the 9 Sep "
            "meeting and is not an endorsed position. It exists to answer the AITC action 'develop a visual mapping of the current versus "
            "desired framework' and stays off the table unless the room answers page 2 with 'not a conscious choice'.")


def build():
    doc = pymupdf.open()
    page1(doc)
    page2(doc)
    page3(doc)
    doc.set_metadata({"title": "Officer and Soldier Leadership Development: Wireframes", "author": "NZALC"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
