#!/usr/bin/env python3
"""
Low-fidelity wireframes for the LDF alignment discussion piece: seven
landscape pages drawn directly as a PDF with PyMuPDF.  Deliberately grey
and boxy so the conversation stays on structure, not styling.

    python3 build_ldf_wireframes.py   ->  output/ldf-alignment-wireframes.pdf
"""

import pymupdf

OUT = "./output/ldf-alignment-wireframes.pdf"
W, H = 842, 595                      # A4 landscape, points
M = 36                               # margin

INK = (0.12, 0.12, 0.12)
MID = (0.45, 0.45, 0.45)
LIGHT = (0.80, 0.80, 0.80)
FILL = (0.94, 0.94, 0.94)
FILL2 = (0.88, 0.88, 0.88)
DARK = (0.30, 0.30, 0.30)
NOTE = (0.55, 0.36, 0.08)            # annotation colour, one only
WHITE = (1, 1, 1)

LEVELS = ["LEAD SELF", "LEAD TEAMS", "LEAD LEADERS", "LEAD SYSTEMS",
          "LEAD CAPABILITY", "LEAD INTEGRATED CAPABILITY", "LEAD ORGANISATION"]
SHORT = ["SELF", "TEAMS", "LEADERS", "SYSTEMS", "CAPABILITY",
         "INTEGRATED CAP.", "ORGANISATION"]
SHIFTS = [
    "Deliver on intent as an effective individual",
    "Accountable for others: get things done through others",
    "Get things done through other leaders; think in systems",
    "Run an entire system with delegated autonomy",
    "Build and sustain capability beyond your tenure",
    "Integrate capability at enterprise level",
    "Steward the institution and set the strategic agenda",
]
TRANSITIONS = [f"T{i}" for i in range(1, 7)]
CATEGORIES = ["Rank / career point", "Appointment / responsibility",
              "Formal development", "Career linkage", "Timing", "Assurance"]
GAPS = ["DEVELOPMENT", "ALIGNMENT", "TIMING", "CONSEQUENCE", "ASSURANCE", "DATA"]


class Page:
    def __init__(self, doc, number, title, purpose):
        self.p = doc.new_page(width=W, height=H)
        self.number = number
        # frame: page chrome
        self.text(M, 22, f"WIREFRAME {number} OF 7", 7, MID)
        self.text(W - M, 22, "LDF ALIGNMENT  ·  DESIGN DRAFT  ·  LOW FIDELITY", 7, MID, align=2)
        self.text(M, 40, title.upper(), 9, INK, bold=True)
        self.text(M, 52, purpose, 7.5, MID)
        self.line(M, 58, W - M, 58, LIGHT)

    # --- primitives ---------------------------------------------------
    def text(self, x, y, s, size=9, color=INK, bold=False, align=0, width=None):
        font = "helvetica-bold" if bold else "helvetica"
        if width:
            rect = pymupdf.Rect(x, y - size, x + width, y + size * 6)
            self.p.insert_textbox(rect, s, fontsize=size, fontname=font,
                                  color=color, align=align)
            return
        if align == 2:
            tw = pymupdf.get_text_length(s, fontname=font, fontsize=size)
            x = x - tw
        elif align == 1:
            tw = pymupdf.get_text_length(s, fontname=font, fontsize=size)
            x = x - tw / 2
        self.p.insert_text((x, y), s, fontsize=size, fontname=font, color=color)

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

    def labelled_box(self, x, y, w, h, label, fill=FILL, size=7.5, bold=False,
                     color=INK, stroke=MID, dashes=None, align=1):
        self.box(x, y, w, h, fill=fill, stroke=stroke, dashes=dashes)
        lines = label.split("\n")
        total = len(lines) * (size + 2)
        ty = y + h / 2 - total / 2 + size
        for ln in lines:
            tx = x + w / 2 if align == 1 else x + 6
            self.text(tx, ty, ln, size, color, bold=bold, align=align)
            ty += size + 2

    def placeholder(self, x, y, w, h, label="PLACEHOLDER"):
        self.box(x, y, w, h, fill=None, stroke=LIGHT, dashes="[3 3] 0")
        self.line(x, y, x + w, y + h, LIGHT, 0.5)
        self.line(x, y + h, x + w, y, LIGHT, 0.5)
        self.text(x + w / 2, y + h / 2 + 2.5, label, 6.5, MID, align=1)

    def arrow(self, x0, y0, x1, y1, color=DARK):
        sh = self.p.new_shape()
        sh.draw_line((x0, y0), (x1, y1))
        sh.finish(color=color, width=0.9)
        # simple arrow head
        import math
        ang = math.atan2(y1 - y0, x1 - x0)
        for d in (2.6, -2.6):
            sh.draw_line((x1, y1), (x1 - 6 * math.cos(ang + d), y1 - 6 * math.sin(ang + d)))
        sh.finish(color=color, width=0.9)
        sh.commit()

    def chip(self, x, y, s, fill=FILL2, color=INK):
        w = pymupdf.get_text_length(s, fontname="helvetica-bold", fontsize=5.5) + 8
        self.box(x, y, w, 9, fill=fill, stroke=None)
        self.text(x + 4, y + 6.8, s, 5.5, color, bold=True)
        return w

    def note(self, x, y, w, s, title="VISUAL LOGIC"):
        """Annotation panel in the one accent colour."""
        self.box(x, y, w, 0.1, stroke=None)
        self.text(x, y + 8, title, 6.5, NOTE, bold=True)
        rect = pymupdf.Rect(x, y + 12, x + w, y + 200)
        self.p.insert_textbox(rect, s, fontsize=6.8, fontname="helvetica",
                              color=NOTE, lineheight=1.25)


# ----------------------------------------------------------------------
def page1(doc):
    pg = Page(doc, 1, "The question",
              "One page. One question. Nothing competes with it.")
    pg.box(M, 80, W - 2 * M, 430, fill=None, stroke=LIGHT)
    q = ("Does the Army's promotion and career-development continuum "
         "deliberately prepare, select and develop its people for the changes "
         "in leadership purpose, mindset, behaviours, scope and scale required "
         "at each LDF transition?")
    rect = pymupdf.Rect(M + 90, 150, W - M - 90, 420)
    pg.p.insert_textbox(rect, q, fontsize=22, fontname="helvetica-bold",
                        color=INK, align=1, lineheight=1.25)
    pg.text(W / 2, 445, "AITC discussion piece  ·  NZALC  ·  DRAFT", 8, MID, align=1)
    pg.placeholder(M + 20, 95, 90, 28, "logo")
    pg.text(W / 2, 470, "[No subtitle. No agenda. No sources. Those come on page 2.]", 7, NOTE, align=1)
    pg.note(M, 520, W - 2 * M,
            "The reader should be able to repeat the question from memory after this page. "
            "Type only, generous white space, one weight. The word 'deliberately' may be set "
            "heavier than the rest in the polished version; it is the hinge of the analysis.")


def page2(doc):
    pg = Page(doc, 2, "The system we already have",
              "Six constant elements + seven progressive levels + increasing scope. Source material simplified into one picture.")
    # Left: six constant elements as a ring of boxes
    cx, cy, r = 150, 250, 78
    import math
    pg.text(cx, 118, "SIX KEY ELEMENTS", 8, INK, bold=True, align=1)
    pg.text(cx, 128, "constant at every level", 6.5, MID, align=1)
    elems = ["Ethos &\nValues", "Think\nSmart", "Influence\nOthers", "Develop\nTeams", "Positive\nCulture", "Mission\nFocus"]
    for i, e in enumerate(elems):
        a = -math.pi / 2 + i * 2 * math.pi / 6
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        pg.labelled_box(x - 30, y - 14, 60, 28, e, fill=FILL, size=6.5)
    pg.labelled_box(cx - 34, cy - 12, 68, 24, "LEADERSHIP\nFRAMEWORK", fill=FILL2, size=6, bold=True)
    pg.text(cx, 360, "'The framework remains constant.'", 7, NOTE, align=1)

    # Centre: seven-level staircase with environment bands
    x0, y0 = 300, 330
    stepw, steph = 62, 26
    envs = [("FOUNDATIONAL", 0, 3, "tone"), ("OPERATIONAL", 3, 5, "climate"), ("STRATEGIC", 5, 7, "culture")]
    for name, a, b, word in envs:
        pg.box(x0 + a * stepw, 100, (b - a) * stepw, 258, fill=None, stroke=LIGHT, dashes="[2 2] 0")
        pg.text(x0 + a * stepw + 4, 110, name, 6, MID, bold=True)
        pg.text(x0 + a * stepw + 4, 118, f"({word})", 5.5, MID)
    for i, s in enumerate(SHORT):
        x = x0 + i * stepw
        y = y0 - i * steph
        pg.labelled_box(x, y, stepw - 3, steph - 3, s, fill=FILL2 if i % 2 else FILL, size=6, bold=True)
        if i < 6:
            pg.text(x + stepw - 6, y - 6, ">", 9, DARK)
    pg.text(x0, 372, "SEVEN LEADERSHIP LEVELS", 8, INK, bold=True)
    pg.text(x0, 382, "'Its expression changes as responsibility increases.'", 7, NOTE)

    # Right: the axis of change
    ax = 760
    pg.arrow(ax, 340, ax, 105)
    for i, t in enumerate(["scope", "scale", "complexity", "consequence", "time horizon"]):
        pg.text(ax + 8, 330 - i * 40, t, 7, DARK)
    pg.text(ax - 6, 352, "INCREASING", 6, MID, bold=True, align=2)

    # Bottom message band
    pg.labelled_box(M, 410, W - 2 * M, 44,
                    "THE FRAMEWORK REMAINS CONSTANT.   ITS EXPRESSION CHANGES AS LEADERSHIP RESPONSIBILITY INCREASES.",
                    fill=DARK, size=9, bold=True, color=WHITE, stroke=None)
    pg.note(M, 470, W - 2 * M,
            "Three source posters become one picture: the ring (what), the staircase (progression), the "
            "axis (why the progression is hard). The three LDF environments are shown as faint bands so the "
            "reader sees that Foundational, Operational and Strategic are where mindset changes cluster. "
            "No behaviour statements appear here; they live in the source document, not the brief.")


def page3(doc):
    pg = Page(doc, 3, "What actually changes?",
              "Seven levels, one line each. Promotion into greater responsibility is a developmental transition, not a change of rank.")
    colw = (W - 2 * M) / 7
    for i, (lvl, shift) in enumerate(zip(SHORT, SHIFTS)):
        x = M + i * colw
        pg.labelled_box(x + 3, 80, colw - 6, 30, lvl, fill=DARK, size=6.5, bold=True, color=WHITE, stroke=None)
        pg.text(x + colw / 2, 128, "VALUE ADD", 5.5, MID, align=1)
        rect = pymupdf.Rect(x + 6, 134, x + colw - 6, 220)
        pg.p.insert_textbox(rect, shift, fontsize=8, fontname="helvetica-bold", color=INK, align=1, lineheight=1.2)
        pg.placeholder(x + 8, 210, colw - 16, 60, "3-4 source\nvalue-add\nheadings")
        if i < 6:
            # transition gate between columns
            gx = x + colw
            pg.line(gx, 78, gx, 300, LIGHT, dashes="[2 2] 0")
            pg.labelled_box(gx - 11, 290, 22, 14, TRANSITIONS[i], fill=WHITE, size=6, bold=True, stroke=DARK)
    pg.text(M, 330, "T1 to T6 are the six transitions. From page 4 onward the TRANSITION, not the level, is the row.", 7.5, NOTE)
    # bottom: mindset strip
    pg.text(M, 360, "WHAT THE LDF SAYS SHIFTS AT EACH STEP (from the Value Adds and level introductions)", 6.5, MID, bold=True)
    strip = ["intent & mastery", "through others", "through leaders;\nsystems thinking", "run the system;\nsuccession", "beyond tenure;\nadvise upward", "enterprise;\nexternal partners", "stewardship;\nministerial trust"]
    for i, s in enumerate(strip):
        x = M + i * colw
        pg.labelled_box(x + 3, 370, colw - 6, 30, s, fill=FILL, size=6)
    pg.note(M, 420, W - 2 * M,
            "Each column carries one bold sentence, verified against the level's Value Adds. The dashed "
            "placeholders hold the three or four Value Add headings from the source so the sentence is "
            "traceable, not invented. The T1 to T6 gates are introduced here and reused on every following page.")


def matrix(pg, mode="populate"):
    """The centrepiece grid used by pages 4, 5 and 6.
    mode: populate | align | gaps"""
    top, left = 78, M
    spine_w = 150
    side_w = (W - 2 * M - spine_w) / 2
    rowh = 56
    catw = side_w / 6
    # headers
    pg.labelled_box(left, top, side_w, 18, "OFFICER CONTINUUM", fill=DARK, size=7.5, bold=True, color=WHITE, stroke=None)
    pg.labelled_box(left + side_w, top, spine_w, 18, "NZDF LDF TRANSITIONS", fill=INK, size=7.5, bold=True, color=WHITE, stroke=None)
    pg.labelled_box(left + side_w + spine_w, top, side_w, 18, "OTHER RANK CONTINUUM", fill=DARK, size=7.5, bold=True, color=WHITE, stroke=None)
    # category headers mirrored (officer columns read right-to-left toward the spine)
    for i, c in enumerate(CATEGORIES):
        xo = left + side_w - (i + 1) * catw
        xr = left + side_w + spine_w + i * catw
        for x in (xo, xr):
            pg.box(x, top + 18, catw, 22, fill=FILL2, stroke=WHITE)
            rect = pymupdf.Rect(x + 2, top + 20, x + catw - 2, top + 42)
            pg.p.insert_textbox(rect, c, fontsize=5.2, fontname="helvetica-bold", color=INK, align=1, lineheight=1.1)
    # rows = transitions
    y = top + 40
    known = {(0, "O", 2): "embedded in\nsingle-Service\ncourses (LDS)", (0, "R", 2): "embedded in\nsingle-Service\ncourses (LDS)",
             (1, "O", 2): "single-Service\nprovider (LDS)", (1, "R", 2): "single-Service\nprovider (LDS)",
             (2, "O", 2): "ILD delivers\nLDS course", (2, "R", 2): "ILD delivers\nLDS course",
             (3, "O", 2): "ILD delivers\nLDS course", (3, "R", 2): "ILD delivers\nLDS course",
             (4, "O", 2): "ILD delivers\nLDS course", (4, "R", 2): "ILD delivers\nLDS course",
             (5, "O", 2): "ILD delivers\nLDS course", (5, "R", 2): "ILD delivers\nLDS course",
             (0, "O", 0): "OCDT > JO\n(LDS estimate)", (0, "R", 0): "PTE > LCPL/CPL\n(LDS estimate)",
             (1, "O", 0): "JO\n(LDS estimate)", (1, "R", 0): "SGT/SSGT\n(LDS estimate)",
             (2, "O", 0): "MAJ\n(LDS estimate)", (2, "R", 0): "WO\n(LDS estimate)",
             (3, "O", 0): "LTCOL\n(LDS estimate)", (3, "R", 0): "Tier 5 WO\n(LDS estimate)",
             (4, "O", 0): "COL\n(LDS estimate)", (4, "R", 0): "Tier 4 WO\n(LDS estimate)",
             (5, "O", 0): "BRIG+\n(LDS estimate)", (5, "R", 0): "Tier 3 WO+\n(LDS estimate)"}
    for t in range(6):
        # spine cell: FROM -> shift -> TO
        sx = left + side_w
        pg.box(sx, y, spine_w, rowh, fill=FILL, stroke=WHITE)
        pg.labelled_box(sx + 4, y + 4, 22, 14, TRANSITIONS[t], fill=WHITE, size=6, bold=True, stroke=DARK)
        pg.text(sx + 32, y + 13, f"{SHORT[t]}  >  {SHORT[t + 1]}", 6.5, INK, bold=True)
        rect = pymupdf.Rect(sx + 6, y + 20, sx + spine_w - 6, y + rowh - 2)
        pg.p.insert_textbox(rect, "WHAT CHANGES: " + SHIFTS[t + 1], fontsize=5.6, fontname="helvetica", color=DARK, lineheight=1.15)
        for side in ("O", "R"):
            for c in range(6):
                x = left + side_w - (c + 1) * catw if side == "O" else left + side_w + spine_w + c * catw
                pg.box(x, y, catw, rowh, fill=WHITE, stroke=LIGHT)
                key = (t, side, c)
                if mode == "populate":
                    if key in known:
                        rect = pymupdf.Rect(x + 2, y + 4, x + catw - 2, y + rowh - 12)
                        pg.p.insert_textbox(rect, known[key], fontsize=5.2, fontname="helvetica", color=INK, align=1, lineheight=1.15)
                        pg.chip(x + 3, y + rowh - 12, "TO CONFIRM", fill=FILL2)
                    else:
                        pg.chip(x + 3, y + rowh - 12, "DATA REQUIRED", fill=FILL2, color=MID)
                        pg.text(x + catw / 2, y + rowh / 2, "·", 8, LIGHT, align=1)
                elif mode == "align":
                    # only cells with a demonstrable connection are drawn solid; the rest fade
                    if c == 2 and t <= 1:
                        pg.box(x, y, catw, rowh, fill=FILL2, stroke=DARK)
                        pg.chip(x + 3, y + rowh - 12, "ALIGNED?", fill=DARK, color=WHITE)
                    else:
                        pg.text(x + catw / 2, y + rowh / 2, "·", 8, LIGHT, align=1)
                elif mode == "gaps":
                    tag = GAPS[(t + c) % 6] if (c in (3, 4, 5)) else "DATA"
                    fill = FILL2 if tag != "DATA" else WHITE
                    pg.box(x, y, catw, rowh, fill=fill, stroke=LIGHT)
                    pg.chip(x + 3, y + rowh - 12, tag, fill=DARK if tag != "DATA" else FILL2, color=WHITE if tag != "DATA" else MID)
        y += rowh
    return y


def page4(doc):
    pg = Page(doc, 4, "Two career systems. One leadership framework.",
              "The centrepiece. Officer left, Other Rank right, the LDF spine fixed in the middle. Rows are transitions, not levels.")
    y = matrix(pg, "populate")
    pg.text(M, y + 12, "Status chips: KNOWN (from source)  ·  TO CONFIRM (source is an estimate or a session document)  ·  DATA REQUIRED (nothing in hand). Colour comes later; the chip text is the primary signal.", 6.5, NOTE)
    pg.note(M, y + 22, W - 2 * M,
            "Reading order is deliberate: the eye lands on the dark spine, reads a transition and 'what changes', "
            "then looks left (officer) and right (OR) to test whether each system prepares for that change. Officer "
            "columns run right-to-left so the two sides mirror around the spine and the same category sits at the same "
            "distance from it. Populated cells here are limited to what the four sources state: the LDS course "
            "delivery model per level and the rank-to-level estimate from the Leadership Levels poster (itself marked "
            "'only an estimation'). Everything else is a grey DATA REQUIRED chip.")


def page5(doc):
    pg = Page(doc, 5, "Where do the systems align?",
              "Same matrix. Only demonstrable connections stay solid; everything else recedes.")
    y = matrix(pg, "align")
    pg.text(M, y + 12, "Solid cell = evidence in hand that development, career point and consequence connect. Faded cell = not shown on this page, not 'no'.", 6.5, NOTE)
    pg.note(M, y + 22, W - 2 * M,
            "This page is the positive case. It uses the identical grid so the reader is not re-orienting, and "
            "simply removes what is not aligned. In the polished version aligned cells are green and linked to the "
            "spine with a short connector; nothing else is coloured. The two cells shown solid are illustrative "
            "of the treatment only; which cells qualify is decided by the data, not by this wireframe.")


def page6(doc):
    pg = Page(doc, 6, "Where are the gaps?",
              "Same matrix. Each gap is named by type, so the reader sees the nature of the problem, not just a red cell.")
    y = matrix(pg, "gaps")
    # legend
    lx = M
    pg.text(lx, y + 14, "GAP TAXONOMY", 6.5, INK, bold=True)
    defs = ["no deliberate development for the transition", "development exists but does not match the LDF shift",
            "development occurs after the transition", "development has no formal link to promotion or appointment",
            "no mechanism establishes readiness", "insufficient information"]
    for i, (g, d) in enumerate(zip(GAPS, defs)):
        cx = lx + (i % 3) * 255
        cy = y + 26 + (i // 3) * 13
        w = pg.chip(cx, cy - 8, g, fill=DARK if g != "DATA" else FILL2, color=WHITE if g != "DATA" else MID)
        pg.text(cx + w + 4, cy, d, 6.3, DARK)
    pg.note(M, y + 62, W - 2 * M,
            "Tags shown here are placeholders to test density, not findings. Amber and red are reserved for this "
            "page and page 5; the tag text carries the meaning so the page still works in greyscale. Officer-versus-OR "
            "asymmetries are read across a row: the same transition, two different answers. Where evidence is thin the "
            "tag is DATA, never a judgement.")


def page7(doc):
    pg = Page(doc, 7, "The question for Army",
              "End at the strategic level. No answer is predetermined.")
    pg.box(M, 80, W - 2 * M, 300, fill=None, stroke=LIGHT)
    q = ("If the LDF defines the leadership transitions Army expects its people to make, "
         "how deliberately should promotion, appointment and professional development "
         "be aligned to those transitions?")
    rect = pymupdf.Rect(M + 80, 120, W - M - 80, 330)
    pg.p.insert_textbox(rect, q, fontsize=19, fontname="helvetica-bold", color=INK, align=1, lineheight=1.25)
    # three levers, no options
    lv = ["PROMOTION", "APPOINTMENT", "PROFESSIONAL DEVELOPMENT"]
    lw = (W - 2 * M - 40) / 3
    for i, l in enumerate(lv):
        x = M + i * (lw + 20)
        pg.labelled_box(x, 400, lw, 34, l, fill=FILL2, size=8, bold=True)
        pg.text(x + lw / 2, 450, "[the three levers AITC controls; no recommendation attached]", 6, MID, align=1)
    pg.note(M, 480, W - 2 * M,
            "Mirror of page 1: type only, one question. The three levers are named because they are the "
            "decision space, but no option, model or preferred answer is shown. The page exists to hand the "
            "discussion to AITC, not to close it.")


def build():
    doc = pymupdf.open()
    for fn in (page1, page2, page3, page4, page5, page6, page7):
        fn(doc)
    doc.set_metadata({"title": "LDF Alignment Wireframes", "author": "NZALC"})
    doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
