#!/usr/bin/env python3
"""
Low-fidelity wireframes for the AITC discussion piece on Officer and
Soldier leadership development: three landscape pages drawn as a PDF with
PyMuPDF.  Grey and boxy on purpose, so the conversation stays on
structure.

    python3 build_ldf_wireframes.py   ->  output/ldf-alignment-wireframes.pdf

Evidence base: the four source documents, the NZALC course data sheets,
and the transcript of the NZALC meeting of 9 Sep 2026 (Mike and Dave).
Where the transcript and the auto-generated meeting notes differ, the
transcript governs.
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
PAGE2_STATEMENT = ("The issue may not be an absence of leadership development. It is the absence of a "
                   "consistently deliberate mechanism linking the right development to the right career transition.")
IF_YES = "What is the rationale for treating Officer and Soldier leadership development differently?"
IF_NO = ("Should Army establish a more consistent mechanism for ensuring development occurs "
         "before increased leadership responsibility?")
LEVELS = ["LEAD SELF", "LEAD TEAMS", "LEAD LEADERS", "LEAD SYSTEMS",
          "LEAD CAPABILITY", "LEAD INTEGRATED\nCAPABILITY", "LEAD ORGANISATION"]

# Career linkage: the strength of the link between the development and the
# career transition, on a scale rather than a yes / no.  The meter in each
# box shows the level; pending segments are outlined where a policy check
# is still owed.
LINKAGE = {
    "FORMALLY MANDATED": 4,        # in promotion policy or embedded in the qualifying course
    "FUNCTIONALLY REQUIRED": 3,    # not in policy, but policed as if it were
    "EXPECTED": 2,                 # self-selected, high uptake
    "SELF-SELECTED": 1,            # self-selected, uptake rests on inclination
    "UNCONNECTED": 0,
}
LEGEND = ("CAREER LINKAGE METER: 4 formally mandated (in policy or embedded in the qualifying course) · "
          "3 functionally required (policed, not in policy) · 2 expected (self-selected, high uptake) · "
          "1 self-selected (uptake by inclination) · 0 unconnected · outlined segment: policy check owed")

TAG_MEETING = "STATED 9 SEP"
TAG_CONFIRM = "TO CONFIRM"

ENTRY_SOLDIER = "On entry (civilian to soldier): Lead Self is compulsory, delivered through train-the-trainer."
ENTRY_OFFICER = "On entry (civilian to OCDT): Lead Self is compulsory, as for soldiers."

# One entry per LDF transition.  dev: the development; link: the career
# linkage state; pend: meter segments outlined as pending a policy check;
# note: the one line of evidence behind the state; tag: evidence status.
SOLDIER = [
    dict(frm="PTE", to="LCPL", dev="ELDA Lead Teams (A18011) + LDS Lead Teams (D03020), inside the JNCO course (A1530)",
         link="FORMALLY MANDATED", pend=0,
         note="Embedded in the qualification: qualifying on the course qualifies the leadership content.", tag=TAG_MEETING),
    dict(frm="CPL", to="SGT", dev="ELDA Lead Leaders (A18008) + LDS Lead Leaders (D03030), inside the SNCO course (A1531)",
         link="FORMALLY MANDATED", pend=0,
         note="In promotion policy: 'very clear on the NCO front'.", tag=TAG_MEETING),
    dict(frm="SSGT", to="WO2", dev="ELDA Lead Systems (A18010) on the WO course (A1532); LDS Lead Systems (ILD)",
         link="FORMALLY MANDATED", pend=1,
         note="ELDA mandated on the WO course. Whether ILD LDS Lead Systems is a WO2 prerequisite: check the CDS (Dave). Army cannot guarantee an ILD seat.", tag=TAG_CONFIRM),
    dict(frm="WO2", to="WO1", dev="LDS Lead Capability (ILD)",
         link="EXPECTED", pend=1,
         note="Expected for WO1; 'pretty sure' not in policy. Most attend, subject to an ILD seat. Confirm against policy.", tag=TAG_CONFIRM),
    dict(frm="WO1", to="Senior WO1", dev="LDS Lead Integrated Capability: ELDA week (ALC / Navy) + LDS week (ILD)",
         link="EXPECTED", pend=0,
         note="ILD pathway; attendance without exception. Mandate not stated.", tag=TAG_MEETING),
    dict(frm="Senior WO1", to="Senior appointments", dev="LDS Lead Organisation + ELDA component (ILD)",
         link="EXPECTED", pend=0,
         note="Senior selection pathway: all complete it well before required.", tag=TAG_MEETING),
]
OFFICER = [
    dict(frm="OCDT", to="2LT", dev="ELDA Lead Teams (the former Nemesis) + LDS Lead Teams, inside NZCC (ALC at OCS)",
         link="FORMALLY MANDATED", pend=0,
         note="Embedded in the commissioning qualification: qualifying on NZCC qualifies both.", tag=TAG_MEETING),
    dict(frm="2LT / LT", to="CAPT", dev="ELDA Lead Leaders (A18008) + LDS Lead Leaders, distributed and self-scheduled",
         link="FUNCTIONALLY REQUIRED", pend=1,
         note="Not in promotion policy, but policed by OCS and COs: in practice no 2LT or LT promotes without it. The substantive CAPT request.", tag=TAG_CONFIRM),
    dict(frm="CAPT", to="MAJ", dev="ELDA Lead Systems (A18010, ALC); LDS Lead Systems (ILD)",
         link="SELF-SELECTED", pend=0,
         note="Not mandated and not policed. Uptake rests on inclination; those who most need it opt out. CAPT to OC is the largest jump in scope.", tag=TAG_MEETING),
    dict(frm="MAJ", to="LTCOL", dev="LDS Lead Capability (ILD)",
         link="EXPECTED", pend=1,
         note="Not mandated; the impression is that all complete it. Self-selected and scrutinised. Confirm against policy.", tag=TAG_CONFIRM),
    dict(frm="LTCOL", to="COL", dev="LDS Lead Integrated Capability: ELDA week (ALC / Navy) + LDS week (ILD)",
         link="EXPECTED", pend=0,
         note="ILD pathway; LTCOL and COL attend without exception. Mandate not stated.", tag=TAG_MEETING),
    dict(frm="COL", to="BRIG", dev="LDS Lead Organisation + ELDA component (ILD)",
         link="EXPECTED", pend=0,
         note="Senior selection pathway: all complete it well before required.", tag=TAG_MEETING),
]
OFFICER_GAP = (1, 2)   # where the meeting said the gap bites


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

    def meter(self, x, y, level, pend=0, seg=11, h=6, gap=2):
        """Four segments, filled to `level`; `pend` further segments outlined."""
        for k in range(4):
            sx = x + k * (seg + gap)
            if k < level:
                self.box(sx, y, seg, h, fill=INK, stroke=None)
            elif k < level + pend:
                self.box(sx, y, seg, h, fill=WHITE, stroke=INK, dashes="[1.5 1] 0")
            else:
                self.box(sx, y, seg, h, fill=WHITE, stroke=LIGHT)
        return 4 * (seg + gap) - gap

    def note(self, x, y, w, s):
        self.text(x, y + 8, "VISUAL LOGIC", 6.5, NOTE, bold=True)
        self.textbox(x, y + 12, w, 120, s, 6.8, NOTE)


def side(pg, entries, x, w, y_of, soldier, title, entry, gap=()):
    """One continuum column: rank, then a development box carrying the
    development, the career-linkage state and its meter, aligned to the
    LDF transition rows."""
    pg.labelled(x, 92, w, 18, title, fill=DARK, size=7.5, bold=True, color=WHITE, stroke=None)
    pg.textbox(x + 4, 112, w - 8, 14, entry, 5.4, MID, align=1)
    for i, e in enumerate(entries):
        y = y_of(i)
        pg.text(x + w / 2, y - 6, f"{e['frm']}   >   {e['to']}", 7, INK, bold=True, align=1)
        bx, by, bw, bh = x + 8, y + 2, w - 16, 44
        in_gap = i in gap
        level = LINKAGE[e["link"]]
        if soldier:
            pg.box(bx, by, bw, bh, fill=FILL2, stroke=DARK)
        else:
            pg.box(bx, by, bw, bh, fill=WHITE, stroke=INK if in_gap else DARK,
                   width=1.6 if in_gap else 0.8, dashes="[3 2] 0")
        # row 1: development
        pg.text(bx + 5, by + 8.5, "DEVELOPMENT", 4.8, MID, bold=True)
        pg.textbox(bx + 48, by + 3.2, bw - 52, 12, e["dev"], 5.4, INK, lh=1.1)
        # row 2: career linkage state + meter
        pg.text(bx + 5, by + 20, "CAREER LINKAGE", 4.8, MID, bold=True)
        pg.text(bx + 54, by + 20, e["link"], 6.2, INK, bold=True)
        pg.meter(bx + bw - 5 - 50, by + 14.5, level, e["pend"])
        # row 3: the evidence line and the tag
        pg.chip(bx + bw - 4, by + bh - 11.5, e["tag"], fill=FILL2 if e["tag"] == TAG_MEETING else WHITE, color=MID, right=True)
        pg.textbox(bx + 5, by + 23, bw - 70, bh - 24, e["note"], 5.0, DARK, lh=1.12)
    if gap:
        y0, y1 = y_of(gap[0]) - 12, y_of(gap[-1]) + 48
        pg.line(x - 10, y0, x - 10, y1, INK, width=1.4)
        pg.line(x - 10, y0, x - 4, y0, INK, width=1.4)
        pg.line(x - 10, y1, x - 4, y1, INK, width=1.4)
        pg.p.insert_text((x - 13, (y0 + y1) / 2 + 40), "THE GAP: THE MIDDLE CREW", fontsize=5.5,
                         fontname="helvetica-bold", color=INK, rotate=90)


def page1(doc):
    pg = Page(doc, 1, "Two continuums. One leadership framework.",
              "One visual. The LDF is the common spine; the two Army promotion continuums are mapped against it, each box giving the development and the strength of its link to the career transition.")
    pg.textbox(M, 62, W - 2 * M, 30, HEADLINE, 11, INK, bold=True, align=1, lh=1.2)

    spine_x, spine_w = W / 2 - 70, 140
    side_w = spine_x - M - 24
    top, rowh = 118, 58

    def y_of(i):
        return top + i * rowh + 30

    pg.labelled(spine_x, 92, spine_w, 18, "LEADERSHIP DEVELOPMENT FRAMEWORK", fill=INK, size=6.5, bold=True, color=WHITE, stroke=None)
    for i, lvl in enumerate(LEVELS):
        y = top + i * rowh
        pg.labelled(spine_x + 10, y, spine_w - 20, 22, lvl, fill=FILL2 if i % 2 else FILL, size=6.5, bold=True)
        if i < 6:
            pg.arrow(W / 2, y + 22, W / 2, y + rowh - 1, color=DARK)
            pg.text(W / 2 + 6, y + rowh / 2 + 12, f"T{i + 1}", 5.5, MID)
    for i in range(6):
        y = y_of(i) + 24
        pg.line(spine_x - 16, y, spine_x, y, LIGHT)
        pg.line(spine_x + spine_w, y, spine_x + spine_w + 16, y, LIGHT)

    side(pg, OFFICER, M + 14, side_w - 14, y_of, soldier=False, title="OFFICER CONTINUUM",
         entry=ENTRY_OFFICER, gap=OFFICER_GAP)
    side(pg, SOLDIER, spine_x + spine_w + 24, side_w, y_of, soldier=True, title="SOLDIER CONTINUUM",
         entry=ENTRY_SOLDIER)

    pg.text(M, 495, LEGEND, 5.6, INK)
    pg.text(M, 503, "Rank pairings follow the 9 Sep meeting (WO2 is the Lead Systems tick, WO1 the Lead Capability tick); the LDS poster calls its own "
                    "rank mapping an estimate. They place the comparison; they do not assert equivalence.", 5.6, MID)
    pg.box(M, 508, W - 2 * M, 40, fill=DARK, stroke=None)
    pg.text(M + 10, 519, "THE QUESTION", 6, FILL2, bold=True)
    pg.textbox(M + 10, 522, W - 2 * M - 20, 26, PAGE1_QUESTION, 8.5, WHITE, bold=True, lh=1.2)
    pg.note(M, 552, W - 2 * M,
            "Read across any row: same LDF transition, what does Army require of a soldier, what does it require of an officer? "
            "The comparison is no longer mandated versus not mandated: each box places the link on a scale from formally mandated "
            "to unconnected, because the evidence (the 9 Sep transcript, which governs over the generated notes) shows a spectrum. "
            "Heavy dashed boxes are where the gap bites. STATED 9 SEP: stated at the meeting, not yet verified. TO CONFIRM: a policy "
            "check is owed before the state can stand. Nothing here is asserted as a finding.")


# Page 2: the officer continuum drawn horizontally, five stages, with the
# linkage level giving the band its shape.  Level values follow LINKAGE.
STAGES = [
    ("T1", "COMMISSIONING\nOCDT > 2LT", 4, "STRUCTURED", "Lead Teams embedded in NZCC"),
    ("T2", "LT > CAPT", 3, "FUNCTIONALLY ENFORCED", "Lead Leaders policed, not policy-embedded"),
    ("T3", "CAPT > MAJ", 1, "WEAKEST LINKAGE", "Lead Systems self-selected; not policed"),
    ("T4", "MAJ > LTCOL", 2, "PARTICIPATION STRENGTHENS", "Lead Capability: most attend"),
    ("T5 / T6", "SENIOR OFFICER\nLTCOL > COL > BRIG+", 2, "STRONG PARTICIPATION", "Selection effects; attendance without exception"),
]
SOLDIER_STRIP = [
    ("T1", "PTE > LCPL", "Mandated (JNCO course)"),
    ("T2", "CPL > SGT", "Mandated in policy (SNCO course)"),
    ("T3", "SSGT > WO2", "Likely linked; confirm policy"),
    ("T4", "WO2 > WO1", "Expected, high uptake; confirm policy"),
    ("T5 / T6", "WO1 and senior WO1", "ILD pathway; senior selection"),
]
HISTORY = [
    ("WHAT WAS TRIED",
     "Intent and senior buy-in existed. Lead Leaders was attached to Grade 2 and 3 coursing for a two-year trial; the extra time "
     "away from units was judged untenable. A distributed model was preferred, leaving officers to schedule the development themselves."),
    ("WHY NO INTEGRATED SOLUTION EMERGED",
     "Later restructuring and course redesigns proceeded without ACS at the table, so nobody looked at where the training should nest. "
     "Above Lead Leaders, delivery passed to ILD in 2012 and Army cannot guarantee seats."),
    ("THE ASSESSMENT OFFERED (CONTEXT, NOT ALC'S FINDING)",
     "'A scheduling oversight in the face of tempo': when development is not formally required it is what gets displaced. "
     "Senior leaders, who all attend, may assume the same is happening throughout Army."),
]


def page2(doc):
    pg = Page(doc, 2, "The officer development gap",
              "The shape of the gap: strong at commissioning, hollow in the operational middle, strong again at the top. Then the history, then COMDT's question.")
    n = len(STAGES)
    gapx = 12
    stw = (W - 2 * M - gapx * (n - 1)) / n
    xs = [M + k * (stw + gapx) for k in range(n)]
    band_top, band_bot = 118, 196        # the band's outer extent; thickness follows linkage level
    mid = (band_top + band_bot) / 2
    # the band: thickness proportional to linkage level at each stage centre
    pts_top, pts_bot = [], []
    for k, (_, _, lvl, _, _) in enumerate(STAGES):
        half = 6 + lvl * 9
        cx = xs[k] + stw / 2
        pts_top.append((cx, mid - half))
        pts_bot.append((cx, mid + half))
    pts_top = [(M, pts_top[0][1])] + pts_top + [(W - M, pts_top[-1][1])]
    pts_bot = [(M, pts_bot[0][1])] + pts_bot + [(W - M, pts_bot[-1][1])]
    pg.polygon(pts_top + pts_bot[::-1], fill=FILL2, stroke=None)
    pg.text(M, 76, "OFFICER CONTINUUM: STRENGTH OF THE LINK BETWEEN DEVELOPMENT AND THE CAREER TRANSITION", 6.5, INK, bold=True)
    for k, (t, name, lvl, verdict, evidence) in enumerate(STAGES):
        x = xs[k]
        hollow = k == 2
        pg.text(x + stw / 2, 90, t, 6, MID, align=1)
        pg.labelled(x, 96, stw, 22, name, fill=WHITE, size=6.5, bold=True, stroke=INK if hollow else DARK,
                    width=1.6 if hollow else 0.8, dashes=None if k == 0 else "[3 2] 0")
        if k < n - 1:
            pg.arrow(x + stw + 1, 107, x + stw + gapx - 1, 107)
        pg.meter(x + stw / 2 - 25, mid - 3, lvl)
        pg.text(x + stw / 2, 216, verdict, 6.5, INK, bold=True, align=1)
        pg.textbox(x, 220, stw, 24, evidence, 5.8, DARK, align=1, lh=1.15)
    # hollow-middle callout
    cx = xs[2] + stw / 2
    pg.box(cx - 62, 246, 124, 13, fill=INK, stroke=None)
    pg.text(cx, 255, "THE HOLLOW MIDDLE", 6.5, WHITE, bold=True, align=1)
    pg.text(cx, 268, "the operational middle: officers doing the enabling and leading of Army, without a systematic training link", 5.6, DARK, align=1)

    # soldier strip for contrast
    sy = 280
    pg.text(M, sy - 3, "SOLDIER CONTINUUM AT THE SAME TRANSITIONS", 6, MID, bold=True)
    for k, (t, ranks, state) in enumerate(SOLDIER_STRIP):
        x = xs[k]
        pg.box(x, sy + 2, stw, 20, fill=FILL, stroke=LIGHT)
        pg.text(x + 4, sy + 10, f"{t}  {ranks}", 5.4, MID, bold=True)
        pg.text(x + 4, sy + 18, state, 5.6, INK)

    # the statement
    pg.box(M, 312, W - 2 * M, 30, fill=WHITE, stroke=INK, width=1.2)
    pg.textbox(M + 10, 318, W - 2 * M - 20, 22, PAGE2_STATEMENT, 8.5, INK, bold=True, align=1, lh=1.2)

    # history strip
    hy = 356
    pg.text(M, hy - 4, "HOW IT AROSE (FROM THE 9 SEP TRANSCRIPT; TO BE VERIFIED AGAINST THE AITC RECORD)", 6, INK, bold=True)
    cw = (W - 2 * M - 20) / 3
    for k, (head, body) in enumerate(HISTORY):
        x = M + k * (cw + 10)
        pg.box(x, hy, cw, 60, fill=WHITE, stroke=LIGHT)
        pg.text(x + 6, hy + 10, head, 5.8, INK, bold=True)
        pg.textbox(x + 6, hy + 13, cw - 12, 46, body, 5.8, DARK, lh=1.22)

    # the challenge
    pg.box(M, 426, W - 2 * M, 96, fill=FILL, stroke=None)
    pg.text(W / 2, 448, "IS THIS A CONSCIOUS CHOICE?", 13, INK, bold=True, align=1)
    pg.textbox(M + 40, 460, (W - 2 * M - 100) / 2, 50, "IF YES:\n" + IF_YES, 8, INK, lh=1.3)
    pg.textbox(W / 2 + 10, 460, (W - 2 * M - 100) / 2, 50, "IF NO:\n" + IF_NO, 8, INK, lh=1.3)
    pg.text(W / 2, 514, "No recommendation. The organisation answers. Page 3 shows what 'no' would lead to, if asked.", 7, MID, align=1)
    pg.note(M, 530, W - 2 * M,
            "The band's thickness is the career-linkage level from page 1, so the waist is the finding: not soldiers developed and officers "
            "not, but junior development, a hollow operational middle, and strong participation again at the top, with CAPT to MAJ the "
            "sharpest point. The soldier strip keeps the asymmetry in view. The history is carried as context so the room does not "
            "retread it; the assessment offered at the meeting is not put forward as ALC's finding. The question stays the centrepiece.")


FUTURE = [
    ("Entry\nLead Self", "Civilian > PTE", "Lead Self; train-the-trainer (TAD, ACS)", "Compulsory", "No change",
     "Civilian > OCDT", "Lead Self; as for soldiers", "Compulsory", "No change"),
    ("T1\nLead Teams", "PTE > LCPL", "ELDA + LDS Lead Teams; inside JNCO course (ALC)", "Formally mandated", "No change",
     "OCDT > 2LT", "ELDA + LDS Lead Teams; inside NZCC (ALC at OCS)", "Formally mandated (embedded)", "No change"),
    ("T2\nLead Leaders", "CPL > SGT", "ELDA + LDS Lead Leaders; inside SNCO course (ALC)", "Formally mandated", "No change",
     "2LT / LT > CAPT", "ELDA + LDS Lead Leaders; distributed window after 2 years in unit (ALC)", "Functionally required; not in policy", "Formally mandated for substantive CAPT"),
    ("T3\nLead Systems", "SSGT > WO2", "ELDA Lead Systems inside WO course (ALC); LDS Lead Systems (ILD)", "ELDA mandated; LDS to confirm", "LDS prerequisite confirmed; ILD seats aligned to promotion timing",
     "CAPT > MAJ", "ELDA Lead Systems (ALC); LDS Lead Systems (ILD)", "Self-selected; not policed", "Formally mandated before OC appointment"),
    ("T4\nLead Capability", "WO2 > WO1", "LDS Lead Capability (ILD)", "Expected; policy to confirm", "Formally mandated; ILD seat guaranteed",
     "MAJ > LTCOL", "LDS Lead Capability (ILD)", "Expected; policy to confirm", "Formally mandated"),
    ("T5\nLead Integrated\nCapability", "WO1 > Senior WO1", "LDS LIC: ELDA week (ALC / Navy) + LDS week (ILD)", "Expected; full attendance", "Stated in policy",
     "LTCOL > COL", "LDS LIC: ELDA week (ALC / Navy) + LDS week (ILD)", "Expected; full attendance", "Stated in policy"),
    ("T6\nLead Organisation", "Senior WO1", "LDS Lead Organisation + ELDA (ILD; contracted facilitation)", "Expected; full attendance", "Stated in policy",
     "COL > BRIG", "LDS Lead Organisation + ELDA (ILD; contracted facilitation)", "Expected; full attendance", "Stated in policy"),
]


def page3(doc):
    pg = Page(doc, 3, "Current and desired: one page",
              "The future state the meeting described: course, transition, who delivers, and the linkage written into promotion policy. Detachable; tabled only if AITC asks what 'no' leads to.")
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
               "the linkage written into promotion policy at each transition, for both continuums, with ILD seat allocation aligned to Army "
               "promotion timing and the officer window placed after unit experience, not at OCS. Completion then becomes a reportable metric.",
               6.5, DARK, lh=1.3)
    pg.note(M, y + 62, W - 2 * M,
            "Shaded DESIRED cells are the change; unshaded rows already match. Content is the future state as described at the 9 Sep "
            "meeting and is not an endorsed position. It exists to answer the AITC action 'develop a visual mapping of the current versus "
            "desired framework' and stays off the table unless the room answers page 2 with 'no'.")


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
