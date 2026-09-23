#!/usr/bin/env python3
"""
Combat Mindset Conditioning: the product description as a staff document
drawn in the same design language as the Army Combat Mindset System
one-pager (split masthead, numbered tracked section labels, spine cards,
chips, pale panels).

    python3 build_cmc_staff_document.py
        -> output/combat-mindset-conditioning.pdf (+ .png of page 1)

Portrait A4, flowing layout: every block measures itself and moves to a new
page when it will not fit.
"""

import pymupdf

from army_onepager import (ARMY_RED, BLACK, FAINT, FONT_BOLD, FONT_REG, GOLD, GRID, INK, MID,
                           PALE, SWAMP, WHITE, Page, rgb)
from build_army_combat_mindset_development_system import (arrow_head_right, dashed_box,
                                                          label_chip, reversed_logo_png,
                                                          wrapped)

OUT = "./output/combat-mindset-conditioning.pdf"
PNG = "./output/combat-mindset-conditioning.png"
W, H = 595, 842
M = 40
CW = W - 2 * M
R = 6
GREY = rgb("5F5F5A")
OLIVE_LIGHT = rgb("E3E6D3")

TITLE = "Combat Mindset Conditioning"
SUBTITLE = "An Army training product within the Army Combat Mindset System"
ORIGINATOR = "Army Command School"
DATE = "23 September 2026"
STATUS = "Draft for discussion"
FOOTER_LEFT = "Combat Mindset Conditioning | Draft for discussion"

BODY = 8.4
LH = 11.2

# ---- content ---------------------------------------------------------------
CM_DEF = "The capacity to regulate and sustain effective performance under operational pressure."
CMR_DEF = "A simple, repeatable method for restoring regulation and effective performance under pressure."
PATHWAY = ["Understand Self", "Regulate Self", "Perform Under Pressure", "Combat Mindset"]
TERMS = [
    ("COGCON", "Combat Mindset Conditioning (CMC)", "Proposed"),
    ("COG6, the six cognitive pillars", "Combat Mindset Training Pillars", "Proposed"),
    ("Operational Reset Tool", "Combat Mindset Reset (CMR)", "Proposed"),
    ("OPS4, the Operational Performance States", "Combat Mindset Performance States", "Proposed"),
    ("COGCON Coach", "CMC Coach", "Working"),
    ("COGCON Level 1 and Level 2", "CMC Coach and CMC Lead Coach", "Working"),
    ("Master COGCON Doctrine", "CMC Training Doctrine, or CMC Training Standard", "Working"),
]
VOCAB = ["Pillars", "Reset", "States", "Methodology", "Assurance"]
PILLARS = [
    ("Self-Awareness", "Recognise changes in physiological, cognitive and emotional state."),
    ("Arousal Control", "Regulate physiological activation to maintain access to effective performance."),
    ("Operational Habit", "Develop effective responses that remain available as conscious capacity reduces under pressure."),
    ("Working Memory", "Retain and manipulate relevant information while operating under load."),
    ("Attentional Control", "Direct, maintain and shift attention appropriately despite distraction, pressure and threat."),
    ("Cognitive Control", "Inhibit ineffective responses and retain deliberate control over behaviour and decisions."),
]
RESET = ["Recognise", "Regulate", "Reorient", "Re-engage"]
STATES = [
    ("Task Focus", "Task focus and deliberate action.", "Proposed Army label for COGCON's Performance Mindset"),
    ("Command Presence", "Controlled posture, communication and pacing.", "COGCON name retained"),
    ("Situational Awareness", "Active scanning, information gathering and resistance to fixation.", "COGCON name retained"),
    ("Resilience", "Rapid recovery following error, correction or performance disruption.", "COGCON name retained"),
]
METHOD = ["Learn", "Practise", "Pressure", "Apply", "Reinforce"]
COACH_LOOP = ["Observe", "Identify", "Intervene", "Reset", "Reassess"]
ASSURANCE = ["Training sequence", "Instructor competence", "Pressure progression", "Reset integrity",
             "Behavioural standards", "Assessment consistency"]
STAGES = [
    ("1", "Understand Self", "Recognise your response.", "Introduces self-awareness and understanding of individual responses to pressure."),
    ("2", "Regulate Self", "Control that response.", "Develops practical regulation skills and the Combat Mindset Reset."),
    ("3", "Perform Under Pressure", "Sustain performance under pressure.", "Progressively conditions those capacities under increasing and varied forms of load."),
    ("4", "Combat Mindset", "Apply it to operational demands.", "Integrated into representative military training so the individual practises maintaining effective performance under increasingly realistic operational demands."),
]
ARCH = [
    ("SYSTEM", "Army Combat Mindset System", "The overarching Army training system."),
    ("PRODUCT", "Combat Mindset Conditioning", "The deliberate practice used to develop the capacity."),
    ("ELEMENT", "Combat Mindset Training Pillars", "What we develop."),
    ("ELEMENT", "Combat Mindset Reset", "How we restore performance when it drops."),
    ("ELEMENT", "Combat Mindset Performance States", "What effective performance looks like."),
    ("ELEMENT", "CMC Training Methodology", "How we progressively condition it under pressure."),
    ("ELEMENT", "CMC Coaching and Assurance", "How Army teaches, assesses and maintains the standard."),
    ("OUTCOME", "Combat Mindset", CM_DEF),
]


# ---- document: pages, cursor and page furniture ---------------------------
class Doc:
    def __init__(self):
        self.doc = pymupdf.open()
        self.pages = []
        self.pg = None
        self.y = 0
        self.bottom = H - 44

    def new_page(self):
        self.pg = Page(self.doc, W, H)
        self.pages.append(self.pg)
        pg = self.pg
        pg.text(W / 2, 20, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
        if len(self.pages) == 1:
            self.y = masthead(pg) + 24
        else:
            pg.text(M, 40, TITLE, 7.5, GREY)
            pg.text(W - M, 40, f"{ORIGINATOR}  ·  {DATE}", 7.5, GREY, align=2)
            pg.line(M, 46, W - M, 46, GRID, width=0.6)
            self.y = 66

    def ensure(self, h):
        if self.pg is None or self.y + h > self.bottom:
            self.new_page()

    def finish(self):
        """Footers last, once the page count is known.  Earlier page handles
        go stale as pages are added, so each page is re-fetched from the
        document and wrapped afresh."""
        n = len(self.doc)
        for i in range(n):
            pg = Page.__new__(Page)
            pg.p = self.doc[i]
            pg.p.insert_font(fontname="Arial", fontfile=FONT_REG)
            pg.p.insert_font(fontname="Arial-Bold", fontfile=FONT_BOLD)
            pg.text(W / 2, H - 22, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
            pg.text(M, H - 11, FOOTER_LEFT, 7.5, BLACK)
            pg.text(W / 2, H - 11, "ACS 2026", 7.5, BLACK, align=1)
            pg.text(W - M, H - 11, f"Page {i + 1} of {n}", 7.5, BLACK, align=2)


def masthead(pg):
    top, hh = 30, 46
    brand_w = 118
    pg.box(M, top, CW, hh, fill=FAINT, stroke=None, radius=R)
    pg.box(M, top, brand_w + R, hh, fill=ARMY_RED, stroke=None, radius=R)
    pg.box(M + brand_w, top, R + 1, hh, fill=FAINT, stroke=None)
    png, (iw, ih) = reversed_logo_png()
    lh = 24
    lw = lh * iw / ih
    pg.p.insert_image(pymupdf.Rect(M + (brand_w - lw) / 2, top + (hh - lh) / 2,
                                   M + (brand_w + lw) / 2, top + (hh + lh) / 2), stream=png)
    tx = M + brand_w + 16
    pg.text(tx, top + 22, TITLE, 16, BLACK, bold=True)
    pg.text(tx, top + 33, SUBTITLE, 7.5, INK)
    pg.text(tx, top + 42, f"{ORIGINATOR}  ·  {DATE}  ·  {STATUS}", 6.8, GREY)
    return top + hh


# ---- blocks ------------------------------------------------------------------
def heading(d, num, label, desc, need=60):
    """Section label; `need` is the least height of following content that
    must share the page, so a heading never strands at a page foot."""
    d.ensure(27 + need)
    if d.y > (66 if len(d.pages) > 1 else 100):
        d.y += 8
    pg = d.pg
    pg.text(M, d.y, num, 9, GOLD, bold=True)
    pg.spaced(M + 17, d.y, label, 7.6, SWAMP, bold=True, spacing=1.8)
    pg.text(M + 17, d.y + 10.5, desc, 7, GREY)
    d.y += 27


def para(d, text, size=BODY, color=INK, bold=False, after=7, x=M, avail=CW):
    lines = wrapped(d.pg, text, size, avail, bold)
    d.ensure(min(len(lines), 3) * LH + after)   # never strand a heading; allow long paragraphs to flow
    for line in lines:
        if d.y + LH > d.bottom:
            d.new_page()
        d.pg.text(x, d.y, line, size, color, bold=bold)
        d.y += LH
    d.y += after


def callout(d, spine, title, text):
    """Black spine card carrying a definition."""
    d.ensure(0)
    spine_w = 52
    bx, bw = M + spine_w + 12, CW - spine_w - 22
    lines = wrapped(d.pg, text, BODY, bw)
    h = 22 + len(lines) * LH
    d.ensure(h + 10)
    pg, y = d.pg, d.y
    pg.box(M, y, CW, h, fill=FAINT, stroke=None, radius=R)
    pg.box(M, y, spine_w + R, h, fill=BLACK, stroke=None, radius=R)
    pg.box(M + spine_w, y, R + 1, h, fill=FAINT, stroke=None)
    pg.text(M + spine_w / 2, y + h / 2 + 4, spine, 11, GOLD, bold=True, align=1)
    pg.text(bx, y + 14, title, 9, BLACK, bold=True)
    ty = y + 26
    for line in lines:
        pg.text(bx, ty, line, BODY, INK)
        ty += LH
    d.y = y + h + 15


def chain(d, items, numbered=False, dark_last=False, h=24, after=15, provenance=None):
    """Row of chips joined by gold arrows: a sequence."""
    d.ensure(h + after)
    pg, y = d.pg, d.y
    n = len(items)
    gap = 16
    cw = (CW - gap * (n - 1)) / n
    for i, text in enumerate(items):
        x = M + i * (cw + gap)
        final = dark_last and i == n - 1
        if provenance == "cogcon":
            pg.box(x, y, cw, h, fill=WHITE, stroke=None, radius=R)
            dashed_box(pg, x, y, cw, h, radius=R)
        else:
            pg.box(x, y, cw, h, fill=BLACK if final else FAINT, stroke=None, radius=R)
        if numbered:
            pg.text(x + 9, y + h / 2 + 3.5, str(i + 1), 9, GOLD, bold=True)
            pg.text(x + 22, y + h / 2 + 3, text, 8, WHITE if final else BLACK, bold=True)
        else:
            pg.text(x + cw / 2, y + h / 2 + 3, text, 8, WHITE if final else BLACK, bold=True, align=1)
        if i < n - 1:
            pg.line(x + cw + 3, y + h / 2, x + cw + gap - 7, y + h / 2, GOLD, width=1.1)
            arrow_head_right(pg, x + cw + gap - 3, y + h / 2)
    d.y = y + h + after


def status_chip(pg, cx, cy, text):
    w, h = 50, 13
    if text == "Proposed":
        pg.box(cx - w / 2, cy - h / 2, w, h, fill=BLACK, stroke=None, radius=h / 2)
        pg.text(cx, cy + 2.4, text, 6.6, WHITE, bold=True, align=1)
    else:
        pg.box(cx - w / 2, cy - h / 2, w, h, fill=WHITE, stroke=MID, width=0.8, radius=h / 2)
        pg.text(cx, cy + 2.4, text, 6.6, INK, align=1)


def table(d, widths, header, rows, chip_col=None, first_bold=True, after=15):
    """Designed table: black header row, pale first column, light rules."""
    d.ensure(0)
    pg = d.pg
    pad, size, lh = 7, 7.6, 9.6

    def row_lines(row):
        return [wrapped(pg, str(c), size, w - 2 * pad, bold=(j == 0 and first_bold))
                for j, (c, w) in enumerate(zip(row, widths))]

    # header
    hh = 17
    d.ensure(hh + 40)
    y = d.y
    def header_row(y):
        pg.box(M, y, CW, hh, fill=BLACK, stroke=None, radius=4)
        x = M
        for j, (text, w) in enumerate(zip(header, widths)):
            if chip_col is not None and j == chip_col:
                pg.text(x + w / 2, y + 11.5, text, 7, WHITE, bold=True, align=1)
            else:
                pg.text(x + pad, y + 11.5, text, 7, WHITE, bold=True)
            x += w
        return y + hh

    y = header_row(y)
    for r_idx, row in enumerate(rows):
        cells = row_lines(row)
        rh = max(len(c) for c in cells) * lh + 2 * pad - 1
        if y + rh > d.bottom:
            d.new_page()
            y = d.y
            pg = d.pg
            y = header_row(y)
            cells = row_lines(row)
        pg.box(M, y, widths[0], rh, fill=FAINT, stroke=None)
        pg.line(M, y + rh, M + CW, y + rh, GRID, width=0.5)
        x = M
        for j, (lines, w) in enumerate(zip(cells, widths)):
            if chip_col is not None and j == chip_col:
                status_chip(pg, x + w / 2, y + rh / 2, row[j])
            else:
                ty = y + pad + 6.5
                for line in lines:
                    pg.text(x + pad, ty, line, size, BLACK if j == 0 else INK, bold=(j == 0 and first_bold))
                    ty += lh
            x += w
        y += rh
    d.y = y + after


def cards(d, items, cols, provenance=None, note_index=None, after=15):
    """Grid of pale cards: bold name, wrapped description, optional note."""
    d.ensure(0)
    pg = d.pg
    gap = 8
    cw = (CW - gap * (cols - 1)) / cols
    size, lh = 7.4, 9.4
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    # the grid moves as one
    total = 0
    for row in rows:
        total += max(26 + len(wrapped(pg, it[1], size, cw - 20)) * lh
                     + (4 + len(wrapped(pg, it[2], 6.2, cw - 20)) * 8 if len(it) > 2 else 0) for it in row) + gap
    d.ensure(total)
    pg = d.pg
    for row in rows:
        prepared = []
        for it in row:
            lines = wrapped(pg, it[1], size, cw - 20)
            note = wrapped(pg, it[2], 6.2, cw - 20) if len(it) > 2 else []
            prepared.append((it[0], lines, note))
        rh = max(26 + len(p[1]) * lh + (4 + len(p[2]) * 8 if p[2] else 0) for p in prepared)
        d.ensure(rh + gap)
        pg, y = d.pg, d.y
        for i, (name, lines, note) in enumerate(prepared):
            x = M + i * (cw + gap)
            if provenance == "cogcon":
                pg.box(x, y, cw, rh, fill=WHITE, stroke=None, radius=R)
                dashed_box(pg, x, y, cw, rh, radius=R)
            else:
                pg.box(x, y, cw, rh, fill=FAINT, stroke=None, radius=R)
            pg.text(x + 10, y + 15, name, 8.5, BLACK, bold=True)
            ty = y + 27
            for line in lines:
                pg.text(x + 10, ty, line, size, INK)
                ty += lh
            ny = ty + 3
            for nline in note:
                pg.text(x + 10, ny, nline, 6.2, GOLD if note[0].startswith("Proposed") else GREY)
                ny += 8
        d.y = y + rh + gap
    d.y += after - gap


def requirement(d, text):
    """Army design requirement: dashed gold box, the open decision."""
    d.ensure(0)
    lines = wrapped(d.pg, text, BODY, CW - 24)
    h = 20 + len(lines) * LH
    d.ensure(h + 10)
    pg, y = d.pg, d.y
    dashed_box(pg, M, y, CW, h, radius=R)
    pg.spaced(M + 12, y + 13, "ARMY DESIGN REQUIREMENT", 5.6, GOLD, bold=True, spacing=1.3)
    ty = y + 26
    for line in lines:
        pg.text(M + 12, ty, line, BODY, INK)
        ty += LH
    d.y = y + h + 15


def chips_row(d, items, after=15):
    d.ensure(20 + after)
    pg = d.pg
    x, y = M, d.y
    for text in items:
        w = pg.width(text, 6.8) + 14
        if x + w > M + CW:
            x = M
            y += 17
            d.ensure(0)
        x += label_chip(pg, x, y, text) + 5
    d.y = y + 13 + after


def stages(d, after=15):
    """Progressive development: numbered stage chips with the CMC contribution."""
    d.ensure(0)
    pg = d.pg
    left_w = 150
    total = sum(max(34, 16 + len(wrapped(pg, c, BODY, CW - left_w - 22)) * LH) + 6 for *_, c in STAGES)
    d.ensure(total)
    for num, name, step, contrib in STAGES:
        lines = wrapped(pg, contrib, BODY, CW - left_w - 22)
        h = max(34, 16 + len(lines) * LH)
        d.ensure(h + 6)
        pg, y = d.pg, d.y
        final = num == "4"
        pg.box(M, y, CW, h, fill=FAINT, stroke=None, radius=R)
        pg.box(M, y, left_w + R, h, fill=BLACK if final else OLIVE_LIGHT, stroke=None, radius=R)
        pg.box(M + left_w, y, R + 1, h, fill=FAINT, stroke=None)
        pg.text(M + 10, y + 15, num, 10, GOLD, bold=True)
        pg.text(M + 24, y + 15, name, 8.5, WHITE if final else BLACK, bold=True)
        pg.text(M + 24, y + 26, step, 6.8, GRID if final else GREY)
        ty = y + 15
        for line in lines:
            pg.text(M + left_w + 12, ty, line, BODY, INK)
            ty += LH
        d.y = y + h + 6
    d.y += after - 6


def architecture(d, after=15):
    """Layered vocabulary: layer label, element, role."""
    d.ensure(0)
    pg = d.pg
    lw, ew = 66, 190
    total = sum(max(24, 12 + len(wrapped(pg, r, 7.6, CW - lw - ew - 24)) * 9.6) + 4 for *_, r in ARCH)
    d.ensure(total)
    for layer, element, role in ARCH:
        lines = wrapped(pg, role, 7.6, CW - lw - ew - 24)
        h = max(24, 12 + len(lines) * 9.6)
        d.ensure(h + 4)
        pg, y = d.pg, d.y
        dark = layer in ("SYSTEM", "OUTCOME")
        pg.box(M, y, CW, h, fill=FAINT, stroke=None, radius=4)
        pg.box(M, y, lw + 4, h, fill=BLACK if dark else OLIVE_LIGHT, stroke=None, radius=4)
        pg.box(M + lw, y, 5, h, fill=FAINT, stroke=None)
        pg.spaced(M + 8, y + h / 2 + 2.2, layer, 5.6, GOLD if dark else SWAMP, bold=True, spacing=1.3)
        pg.text(M + lw + 12, y + h / 2 + 3, element, 8, BLACK, bold=True)
        ty = y + h / 2 + 3 - (len(lines) - 1) * 4.8
        for line in lines:
            pg.text(M + lw + ew, ty, line, 7.6, INK)
            ty += 9.6
        d.y = y + h + 4
    d.y += after - 4


# ---- build -----------------------------------------------------------------
def build():
    d = Doc()
    d.new_page()

    heading(d, "01", "PURPOSE", "Why CMC exists and what it develops.")
    para(d, "Combat Mindset Conditioning (CMC) is the deliberate practice of an individual's capacity to regulate and sustain effective performance under operational pressure. It provides a structured method for developing Combat Mindset.")
    callout(d, "CM", "Combat Mindset", CM_DEF)
    para(d, "CMC is nested within the Army Combat Mindset System (ACMS) and supports its developmental pathway.", after=6)
    chain(d, PATHWAY, numbered=True, dark_last=True)
    para(d, "Its purpose is not simply to teach individuals about pressure. It is to progressively condition the capacity to recognise, regulate and sustain performance as pressure and operational demands increase.")

    heading(d, "02", "WORKING TERMINOLOGY", "Army language for a product derived from COGCON.")
    para(d, "If CMC is to be an Army product rather than COGCON delivered under another logo, its vocabulary should cohere with the ACMS. The substance of COGCON's architecture is preserved; the question is whether each label becomes Army language. The first four translations are proposed; the remainder are working terms and not yet locked.")
    table(d, [170, 245, 100], ["COGCON term", "CMC working term", "Status"], TERMS, chip_col=2)
    para(d, "Together these give CMC a coherent vocabulary. In plain terms: what we develop, what we do when it drops, what we observe, how we train it, and how we maintain the standard.", after=6)
    chain(d, VOCAB, h=20)

    heading(d, "03", "COMBAT MINDSET TRAINING PILLARS", "What we develop.", need=200)
    para(d, "CMC develops the underlying capacities required to maintain performance under pressure. The initial architecture draws directly from the six COGCON pillars, which COGCON treats as interdependent capacities in a deliberate sequence: self-awareness and arousal control are the foundation for downstream cognitive performance.")
    cards(d, PILLARS, 3, provenance="cogcon")
    para(d, "The collective construct is renamed; the individual pillars are not renamed mechanically. COGCON holds that the pillars and their sequencing are part of the underlying mechanism rather than arbitrary categories, so the substance is preserved first and the language reviewed second. Several names, such as Self-Awareness, Working Memory and Attentional Control, may already be adequate for Army use.")
    requirement(d, "With Ken Franks, confirm whether each pillar needs an Army-facing name, and whether the set is adopted directly, consolidated or supplemented.")

    heading(d, "04", "COMBAT MINDSET RESET", "What we do when it drops.")
    callout(d, "CMR", "Combat Mindset Reset", CMR_DEF)
    para(d, "The Reset gives the individual a short sequence that can be employed independently and under load. In use it should be as plain as: “Recognise the drop. Combat Mindset Reset. Re-engage.”", after=6)
    chain(d, RESET, provenance="cogcon")
    para(d, "The Reset is derived from COGCON's Operational Reset Tool, whose mechanism incorporates appraisal of state, perceptual reorientation, physiological modulation and re-anchoring attention onto the next relevant action. The detailed sequence is retained within the COGCON Master Doctrine and accredited coaching material. COGCON's internal terminology for the mechanism need not be exposed at Army level: the mechanism can remain substantially derived from COGCON while the Army-facing construct is the Combat Mindset Reset.")
    requirement(d, "Work with Ken Franks to develop or adapt the Army-owned Reset and its terminology within the agreed IP arrangements.")

    heading(d, "05", "COMBAT MINDSET PERFORMANCE STATES", "What effective performance looks like.", need=150)
    para(d, "CMC requires performance to be observable under pressure, not simply understood theoretically. The Performance States are the observable behavioural expression of the underlying regulation capacity. They answer a direct instructor question, “what does Combat Mindset look like?”, with “we observe it through the Combat Mindset Performance States.”")
    cards(d, STATES, 4, provenance="cogcon")
    para(d, "Command Presence, Situational Awareness and Resilience are already readily understood Army concepts. Performance Mindset is the one label scrutinised: alongside Combat Mindset and Performance Under Pressure it is one “mindset” too many, and COGCON notes it was chosen internally to avoid collision with Army's umbrella term. Task Focus is the cleaner behavioural label.")
    requirement(d, "Confirm the four states and their behavioural markers. They may be derived from OPS4 but should describe the behaviours Army expects to observe from its people under operational pressure.")

    heading(d, "06", "CMC TRAINING METHODOLOGY", "How we progressively condition it under pressure.")
    para(d, "CMC is conditioning through deliberate practice, not simply education about stress or cognition. Training progresses from understanding and practising the component skills in controlled conditions toward their application under increasingly representative pressure.", after=6)
    chain(d, METHOD, dark_last=True)
    para(d, "Pressure is introduced progressively through physical, cognitive, emotional, environmental and task demands appropriate to the training context.")
    para(d, "CMC does not need to exist solely as a standalone course. Once foundational skills have been taught, they can be deliberately practised and reinforced within existing Army training. COGCON argues explicitly for this approach: conditioning should occur within existing training, under the load that training already generates, rather than remaining a separate classroom activity. This allows CMC to be reinforced through PT, leadership training, field exercises and other individual and collective training as the system matures. The ACMS already anticipates this model of deliberate instruction followed by continued practice and application.")

    heading(d, "07", "CMC COACHING AND ASSURANCE", "How Army teaches, assesses and maintains the standard.")
    para(d, "CMC uses trained coaches and instructors to work a simple loop. Assessment focuses on whether the individual can demonstrate the required behaviours while under appropriate pressure, rather than simply recalling CMC knowledge.", after=6)
    chain(d, COACH_LOOP, h=20)
    para(d, "COGCON provides a useful starting model: Level 1 Coach, Level 2 Coach and Specialist, supported by observed assessment, recertification and quality assurance. The working CMC equivalents are CMC Coach and CMC Lead Coach. CMC does not necessarily need to replicate COGCON's tiers.")
    para(d, "CMC should be capable of both formal instruction and distributed reinforcement. Initially, specialist CMC instructors deliver foundational training and develop Army instructor capability. As proficiency develops, trained instructors and commanders reinforce CMC through existing training environments.")
    para(d, "A defined assurance system protects:", after=5)
    chips_row(d, ASSURANCE)
    para(d, "This is an area where COGCON gives Army a significant head start: its existing architecture already contains coach accreditation, recertification, quality assurance and drift control.")
    requirement(d, "Determine a coach and instructor model that fits existing Army instructor qualification, assurance and training-management systems.")

    heading(d, "08", "PROGRESSIVE DEVELOPMENT", "How CMC supports the ACMS developmental pathway.", need=190)
    stages(d)

    heading(d, "09", "PRODUCT ARCHITECTURE", "One vocabulary, nested in the system.", need=270)
    para(d, "The vocabulary nests the product inside the system and gives each element one job.", after=6)
    architecture(d)
    para(d, "This is the architecture to take into the next conversation with Ken Franks: not “we are renaming your product”, but “here is how your proven architecture could translate into an Army-owned training product nested within the ACMS.”")

    # sources and status, with the provenance key
    d.ensure(60)
    d.y += 4
    pg = d.pg
    pg.line(M, d.y, M + CW, d.y, GRID, width=0.6)
    d.y += 14
    pg.spaced(M, d.y, "SOURCES AND STATUS", 5.6, SWAMP, bold=True, spacing=1.3)
    d.y += 11
    para(d, "Derived from the COGCON Phase 2 Discussion Document (Ken Franks) and the Army Combat Mindset System one-pager (Army Command School, 2026). Elements derived from COGCON are subject to adaptation and to the IP arrangements agreed with Ken Franks. Working terminology is proposed for discussion and is not yet locked. The Army design requirements identify the elements Army still needs to design and endorse.", size=7.4, color=GREY, after=6)
    x, y = M, d.y
    pg.box(x, y, 26, 12, fill=WHITE, stroke=None, radius=4)
    dashed_box(pg, x, y, 26, 12, radius=4)
    pg.text(x + 34, y + 9, "Derived from COGCON: substance preserved, labels working", 7, INK)
    x += 34 + pg.width("Derived from COGCON: substance preserved, labels working", 7) + 20
    pg.box(x, y, 26, 12, fill=FAINT, stroke=None, radius=4)
    pg.text(x + 34, y + 9, "Army architecture", 7, INK)

    d.finish()
    d.doc.set_metadata({"title": "Combat Mindset Conditioning", "author": "Army Command School"})
    d.doc.save(OUT, garbage=3, deflate=True)
    saved = pymupdf.open(OUT)
    saved[0].get_pixmap(dpi=200).save(PNG)
    print(f"Saved {OUT} ({saved.page_count} pages) and {PNG}")


if __name__ == "__main__":
    build()
