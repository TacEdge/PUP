#!/usr/bin/env python3
"""
Combat Mindset Framework v0.2, AITC Discussion Draft: a seven-page visual
draft in the NZ Army house style, drawn with PyMuPDF.

    python3 build_combat_mindset_framework.py -> output/combat-mindset-framework-v0.2.pdf

Sources: NZ Army Combat Mindset Framework Proposal V1.0 (August 2026) and
the COMDT ACS discussion of 10 September 2026 as summarised by ACS (ALC).
Content that rests on the meeting summary is marked "proposed".
"""

import pymupdf

from army_onepager import (ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, MID, MOAWHANGO, PALE, SWAMP, WHITE,
                           Page, logo_png, rgb)

OUT = "./output/combat-mindset-framework-v0.2.pdf"
W, H = 595, 842                 # A4 portrait
M = 40
TOTAL = 7
OLIVE = rgb("4A5A1E")
CHARCOAL = rgb("2B2B2B")

DOC_NAME = "Combat Mindset Framework v0.2"
FOOTER_LEFT = "Combat Mindset Framework v0.2, AITC Discussion Draft"
KICKER = "COMBAT MINDSET FRAMEWORK  V0.2   ·   AITC DISCUSSION DRAFT"

STEPS = [
    ("1", "UNDERSTAND SELF", "Recognise physiological and cognitive responses to pressure.",
     "Stress response, arousal, attention narrowing, working-memory load; the Performance = Potential minus Interference model; Red Head and Blue Head.",
     "Recruit and initial training; Lead Self", "Lead Self"),
    ("2", "REGULATE SELF", "Control the response so capability stays available.",
     "Breathing, arousal control, attention, posture and presence, cognitive control; Prepare, Perform, Recover; practised routinely under genuine physical interference.",
     "Physical training; Lead Self and Lead Teams; performance cognition (developmental)", "Lead Self"),
    ("3", "PERFORM UNDER PRESSURE", "Apply those capabilities while fatigued, overloaded and stressed.",
     "Task performance and decision-making under load; peer performance and recovery cycles; experiential activity with structured reflection.",
     "JNCO course and ELDA Lead Teams; NZCC; unit training", "Lead Teams"),
    ("4", "LEAD UNDER PRESSURE", "Maintain command presence, judgement, communication and influence.",
     "Leading others while regulating self; interpersonal and decision pressure; setting tone and climate when interference is high.",
     "SNCO and WO courses; ELDA Lead Leaders and Lead Systems; command training", "Lead Leaders to Lead Systems"),
    ("5", "PERFORM IN COMBAT CONDITIONS", "Apply the capability under threat, uncertainty, consequence and ethical load.",
     "The combat-specific expression: opposition or threat, significant mission or human consequence, and ethical load, represented or deliberately simulated.",
     "Field, tactical and collective training; mission-specific preparation", "All levels"),
]

PATHWAYS = [
    ("Physical training", "Routine practice of physiological regulation, composure, attention, communication and presence under genuine physical interference", [2, 1, 1, 0, 0]),
    ("Recruit and initial training", "LDS Lead Self; first exposure to the model and the language", [2, 1, 0, 0, 0]),
    ("JNCO, SNCO and WO promotion courses", "NZALC LDS and ELDA Lead Teams, Lead Leaders and Lead Systems", [1, 2, 2, 2, 1]),
    ("Officer commissioning and ELDA", "NZCC with ELDA and LDS Lead Teams; ELDA Lead Leaders and Lead Systems", [1, 2, 2, 2, 1]),
    ("Performance cognition (HPC)", "COGCON: developmental; role, evidence, ownership and scale assessed in Phase 2", [1, 2, 1, 0, 0]),
    ("Army Psychology Services", "Mental skills, psychological support and professional advice", [2, 2, 1, 1, 0]),
    ("Field, tactical and collective training", "Application against the defining demands of combat; unit-owned", [0, 1, 2, 2, 2]),
    ("ILD, Lead Systems and above", "Tri-Service leadership development at senior levels", [0, 0, 1, 2, 1]),
]

GOVERNANCE = [
    ("G7", "Doctrine and policy owner", "Owns Combat Mindset doctrine and policy; approves the framework as Army doctrine"),
    ("ARMY TRAINING GROUP", "Training governance and approval", "Governs training; approves course data sheet changes through the ATRB"),
    ("ARMY COMMAND SCHOOL", "Learning provider", "Sponsors the framework; provides the learning system through which it is delivered"),
    ("NZALC AND ACS ELEMENTS", "Development, delivery and integration", "Develops the framework; delivers and integrates it through the leadership development system and course pathways"),
]
ADVISERS = [("ARMY PSYCHOLOGY SERVICES", "Psychological and mental-skills expertise"),
            ("HUMAN PERFORMANCE CELL", "Human-performance and performance-cognition expertise"),
            ("ILD AND OTHER SMEs", "Tri-Service leadership development; evidence and assurance")]

CDS_ROWS = [
    ("Recruit training", "Lead Self", "1, 2", "Amend: carry Understand Self and Regulate Self outcomes"),
    ("Unit physical training programme", "PT policy and unit programmes", "2", "Direct: embed regulation practice; no new course"),
    ("A1530 JNCO Course with ELDA Lead Teams", "Lead Teams", "2, 3", "Amend A1530 and A18011 to carry the outcomes"),
    ("NZCC with ELDA and LDS Lead Teams", "Lead Teams", "2, 3", "Amend NZCC CDS to carry the outcomes"),
    ("A1531 SNCO Course with ELDA Lead Leaders", "Lead Leaders", "3, 4", "Amend A1531 and A18008 to carry the outcomes"),
    ("A1532 WO Course with ELDA Lead Systems", "Lead Systems", "4", "Amend A1532 and A18010 to carry the outcomes"),
    ("ELDA Command", "Command teams", "4, 5", "Amend A18009; collective application under representative demands"),
    ("COGCON", "Developmental", "2", "Hold: Phase 2 assessment decides role, owner and scale"),
    ("Field, tactical and collective training", "Unit-owned", "5", "Guidance: combat-specific application standards; no new course"),
]

TIMELINE = [
    ("10 SEP", "COMDT ACS discussion", "Construct endorsed; governance and delivery direction given"),
    ("SEP", "Define and Understand sprint", "Product and evidence baseline; governance confirmed with G7 and ATG; v0.2 to v0.3 with stakeholders"),
    ("14 OCT", "AITC", "Framework v0.3 tabled; decisions sought"),
    ("OCT TO NOV", "Validate", "Stakeholder validation; bounded pilots: PT-embedded practice and one JNCO or ELDA serial"),
    ("LATE NOV", "Framework v1.0", "Validated framework, governance model and implementation plan to COMDT ACS"),
    ("2027", "Implement", "CDS amendments through ATRB; assurance baseline; evidence development continues"),
]

AITC_DECISIONS = [
    "Endorse the framework construct and the working definitions.",
    "Endorse the five-step developmental architecture as the basis for outcomes.",
    "Endorse the governance model in principle: G7, ATG, ACS, NZALC, with technical advisers.",
    "Direct the embedded delivery approach: outcomes carried in existing pathways, no standalone course.",
    "Note the validation plan and the intent to return Framework v1.0 in late November.",
]


class Doc:
    def __init__(self):
        self.doc = pymupdf.open()
        self.n = 0

    def page(self, title, purpose):
        self.n += 1
        pg = Page(self.doc, W, H)
        pg.text(W / 2, 24, "UNCLASSIFIED", 8.5, BLACK, bold=True, align=1)
        pg.text(W / 2, H - 28, "UNCLASSIFIED", 8.5, BLACK, bold=True, align=1)
        pg.text(M, H - 16, FOOTER_LEFT, 7.5, BLACK)
        pg.text(W / 2, H - 16, "ACS 2026", 7.5, BLACK, align=1)
        pg.text(W - M, H - 16, f"Page {self.n} of {TOTAL}", 7.5, BLACK, align=2)
        png, (iw, ih) = logo_png()
        lh = 20
        pg.p.insert_image(pymupdf.Rect(M, 34, M + lh * iw / ih, 34 + lh), stream=png)
        pg.spaced(M, 68, KICKER, 6.2, SWAMP, bold=True, spacing=1.4)
        pg.text(M, 86, title, 16, BLACK, bold=True)
        pg.text(M, 98, purpose, 8, SWAMP)
        pg.line(M, 104, W - M, 104, ARMY_RED, width=2)
        return pg


def label_pill(pg, cx, y, s, fill=BLACK, color=WHITE):
    w = pg.width(s, 6, True) + len(s) * 1.0 + 18
    pg.box(cx - w / 2, y, w, 12, fill=fill, stroke=None, radius=6)
    pg.spaced(cx, y + 8.5, s, 6, color, bold=True, spacing=1.0, align=1)


def block(pg, y, h, fill, head, sub, tag, tag_fill=BLACK, head_size=15):
    pg.box(M, y, W - 2 * M, h, fill=fill, stroke=None, radius=4)
    label_pill(pg, W / 2, y - 6, tag, fill=tag_fill, color=WHITE if tag_fill is not GOLD else BLACK)
    pg.text(W / 2, y + h / 2 + (4 if sub else 5), head, head_size, WHITE, bold=True, align=1)
    if sub:
        pg.text(W / 2, y + h / 2 + 16, sub, 7, MOAWHANGO, align=1)
    return y + h


# ------------------------------------------------------------------ pages ---
def page1(d):
    pg = d.page("The Framework on a Page", "Warfighting imperative, enabling capability, organising system, developmental architecture, delivery and governance.")
    y = 130
    y = block(pg, y, 72, BLACK, "COMBAT MINDSET", "Remain effective. Act decisively. Harder to kill.", "1   WARFIGHTING IMPERATIVE", tag_fill=ARMY_RED, head_size=22) + 28
    y = block(pg, y, 56, SWAMP, "PERFORMANCE UNDER PRESSURE", "Prepare   ·   Perform   ·   Recover", "2   ENABLING CAPABILITY", tag_fill=SWAMP, head_size=16) + 28
    y = block(pg, y, 56, OLIVE, "COMBAT MINDSET FRAMEWORK", "Governs, develops, delivers and assures Performance Under Pressure and Combat Mindset.", "3   ORGANISING SYSTEM", tag_fill=OLIVE, head_size=16) + 30

    # 4 developmental architecture: five steps across
    pg.box(M, y, W - 2 * M, 92, fill=FAINT, stroke=None, radius=4)
    label_pill(pg, W / 2, y - 6, "4   DEVELOPMENTAL ARCHITECTURE", fill=BLACK)
    n = len(STEPS)
    gap = 6
    sw = (W - 2 * M - 16 - gap * (n - 1)) / n
    for k, (num, name, what, _, _, _) in enumerate(STEPS):
        x = M + 8 + k * (sw + gap)
        last = k == n - 1
        pg.box(x, y + 12, sw, 66, fill=BLACK if last else WHITE, stroke=BLACK if last else GRID, radius=3)
        pg.text(x + 8, y + 26, num, 9, GOLD, bold=True)
        pg.textbox(x + 5, y + 31, sw - 10, 26, name, 6.6, WHITE if last else BLACK, bold=True, align=1, lh=1.15)
        pg.textbox(x + 5, y + 52, sw - 10, 26, what, 5.4, MOAWHANGO if last else MID, align=1, lh=1.15)
        if k < n - 1:
            pg.text(x + sw + gap / 2, y + 48, "›", 9, MID, align=1)
    pg.text(M + 8, y + 88, "Steps 1 to 4 build the enabling capability. Step 5 is its combat-specific expression: threat, consequence and ethical load.", 5.8, MID)
    y += 92 + 30

    # 5 delivery pathways
    pg.box(M, y, W - 2 * M, 74, fill=FAINT, stroke=None, radius=4)
    label_pill(pg, W / 2, y - 6, "5   DELIVERY PATHWAYS   ·   EMBEDDED, NOT STANDALONE", fill=BLACK)
    cols = [("PHYSICAL TRAINING", "Daily and weekly practice of self-regulation under genuine physical interference", "Steps 1 to 2"),
            ("LEADERSHIP TRAINING", "Perform and lead under interpersonal and decision pressure through LDS and ELDA", "Steps 3 to 4"),
            ("FIELD AND TACTICAL TRAINING", "Apply the capability under combat-representative demands", "Step 5")]
    cw = (W - 2 * M - 16 - 12) / 3
    for k, (head, body, steps) in enumerate(cols):
        x = M + 8 + k * (cw + 6)
        pg.box(x, y + 10, cw, 56, fill=WHITE, stroke=GRID, radius=3)
        pg.spaced(x + cw / 2, y + 23, head, 6.2, SWAMP, bold=True, spacing=1.0, align=1)
        pg.textbox(x + 6, y + 27, cw - 12, 30, body, 6, INK, align=1, lh=1.2)
        pg.text(x + cw / 2, y + 61, steps, 5.8, GOLD, bold=True, align=1)
    y += 74 + 30

    # 6 governance
    pg.box(M, y, W - 2 * M, 58, fill=FAINT, stroke=None, radius=4)
    label_pill(pg, W / 2, y - 6, "6   GOVERNANCE   ·   PROPOSED", fill=BLACK)
    chain = [("G7", "doctrine and policy"), ("ATG", "training governance"), ("ACS", "learning provider"), ("NZALC", "development and delivery")]
    bw = 84
    gx = M + 8
    for k, (a, b) in enumerate(chain):
        x = gx + k * (bw + 14)
        pg.box(x, y + 10, bw, 34, fill=WHITE, stroke=GRID, radius=3)
        pg.text(x + bw / 2, y + 25, a, 8.5, BLACK, bold=True, align=1)
        pg.text(x + bw / 2, y + 36, b, 5.6, MID, align=1)
        if k < len(chain) - 1:
            pg.text(x + bw + 7, y + 30, "›", 9, MID, align=1)
    ax = gx + 4 * (bw + 14) - 6
    pg.box(ax, y + 10, W - M - 8 - ax, 34, fill=WHITE, stroke=GOLD, radius=3)
    pg.text(ax + (W - M - 8 - ax) / 2, y + 22, "TECHNICAL ADVISERS", 6.2, SWAMP, bold=True, align=1)
    pg.text(ax + (W - M - 8 - ax) / 2, y + 32, "APS  ·  HPC  ·  ILD  ·  SMEs", 6, INK, align=1)
    pg.text(ax + (W - M - 8 - ax) / 2, y + 40, "advise and enable; do not own", 5.4, MID, align=1)


def page2(d):
    pg = d.page("Definitions and Principles", "The drafting baseline endorsed on 10 September, and the principles that now shape the design.")
    y = 122
    defs = [
        ("COMBAT MINDSET", BLACK,
         "The individual and collective readiness and disposition to remain effective and act decisively and ethically under the threat, adversity and uncertainty of combat in order to achieve the mission. It is the combat-specific expression of Performance Under Pressure."),
        ("PERFORMANCE UNDER PRESSURE", SWAMP,
         "The trainable individual and collective human-performance capability to prepare for, maintain effective performance through, adapt within and recover from conditions that create significant physiological, cognitive, emotional or social interference."),
        ("COMBAT MINDSET FRAMEWORK", OLIVE,
         "The framework through which Army governs, develops, delivers and assures Performance Under Pressure and its combat-specific expression, Combat Mindset."),
    ]
    for head, col, body in defs:
        pg.box(M, y, W - 2 * M, 58, fill=FAINT, stroke=None, radius=4)
        pg.spaced(M + 12, y + 15, head, 7.5, col, bold=True, spacing=1.4)
        pg.textbox(M + 12, y + 20, W - 2 * M - 24, 38, body, 8, INK, lh=1.3)
        y += 66
    y += 4
    pg.spaced(M, y + 8, "THE COMBAT-SPECIFICITY TEST", 7.5, SWAMP, bold=True, spacing=1.4)
    pg.textbox(M, y + 14, W - 2 * M, 44, "A product, method or activity is combat-specific where it develops or applies Performance Under Pressure in a context that represents or deliberately simulates the defining demands of combat. Products that do not represent these demands contribute to the enabling capability rather than its combat-specific expression.", 8, INK, lh=1.3)
    y += 58
    tests = [("OPPOSITION OR THREAT", "An adversary, or a credible representation of one"),
             ("MISSION OR HUMAN CONSEQUENCE", "Significant consequence attached to the outcome"),
             ("ETHICAL LOAD", "Decisions that carry moral weight under pressure")]
    cw = (W - 2 * M - 12) / 3
    for k, (h, b) in enumerate(tests):
        x = M + k * (cw + 6)
        pg.box(x, y, cw, 44, fill=WHITE, stroke=GRID, radius=3)
        pg.spaced(x + cw / 2, y + 15, h, 6, BLACK, bold=True, spacing=0.8, align=1)
        pg.textbox(x + 6, y + 20, cw - 12, 22, b, 6.5, MID, align=1, lh=1.2)
    y += 60

    pg.spaced(M, y + 8, "DESIGN PRINCIPLES", 7.5, SWAMP, bold=True, spacing=1.4)
    principles = [
        ("Organise and integrate before creating.", "The framework organises, standardises and connects what already exists. It is not another course or another piece of intellectual property."),
        ("Capability and outcomes first; products and organisations mapped beneath.", "The framework defines what Army develops and to what standard. Products, methods and organisations are then mapped against it, rather than the framework being built around any one of them."),
        ("Embedded delivery through existing pathways.", "Outcomes are carried in physical training, leadership training and field training, and in the course data sheets that already govern them."),
        ("Combat specificity by the defining demands.", "Performance Under Pressure techniques become Combat Mindset only when developed or applied against threat, consequence and ethical load."),
        ("Evidence and assurance built in.", "Progression, transfer to performance, product quality and organisational adoption are assessed at individual, product and system level."),
    ]
    yy = y + 16
    for k, (h, b) in enumerate(principles):
        pg.box(M, yy, 16, 16, fill=BLACK, stroke=None, radius=8)
        pg.text(M + 8, yy + 11.5, str(k + 1), 8, WHITE, bold=True, align=1)
        pg.text(M + 24, yy + 8, h, 8.5, BLACK, bold=True)
        pg.textbox(M + 24, yy + 11, W - 2 * M - 24, 26, b, 7.5, INK, lh=1.25)
        yy += 36
    y = yy + 4
    pg.box(M, y, W - 2 * M, 112, fill=PALE, stroke=None, radius=4)
    pg.spaced(M + 12, y + 14, "WHAT HAS CHANGED SINCE V1.0", 6.5, SWAMP, bold=True, spacing=1.4)
    changes = [
        "The construct is endorsed: Combat Mindset as the combat-specific expression of Performance Under Pressure (Option 1).",
        "Direction not to create a standalone course: organise, standardise and connect what exists, then embed it through existing training pathways.",
        "A proposed governance chain, G7 to ATG to ACS to NZALC, with APS, HPC and ILD as technical advisers rather than owners.",
        "A five-step developmental architecture in place of a product-by-product organisation.",
        "Physical training identified as the routine environment for practising self-regulation.",
        "A nearer decision point: AITC on or about 14 October 2026.",
    ]
    yy = y + 32
    for c in changes:
        pg.text(M + 14, yy, "•", 7.5, SWAMP)
        pg.textbox(M + 22, yy - 7, W - 2 * M - 34, 14, c, 7, INK, lh=1.2)
        yy += 12


def page3(d):
    pg = d.page("Developmental Architecture", "Five steps from understanding the pressure response to performing in combat conditions. The framework's backbone.")
    y = 120
    heads = ["STEP", "WHAT IT MEANS", "INDICATIVE CONTENT", "WHERE IT IS DEVELOPED", "LDF"]
    widths = [96, 108, 165, 100, 46]
    xs = [M]
    for w in widths[:-1]:
        xs.append(xs[-1] + w)
    for h, x, w in zip(heads, xs, widths):
        pg.box(x, y, w, 16, fill=SWAMP, stroke=WHITE)
        pg.spaced(x + 5, y + 11, h, 5.6, WHITE, bold=True, spacing=0.9)
    y += 16
    rh = 96
    for k, (num, name, what, content, where, ldf) in enumerate(STEPS):
        last = k == len(STEPS) - 1
        fill = rgb("F3F3EF") if k % 2 else WHITE
        pg.box(M, y, sum(widths), rh, fill=fill, stroke=GRID)
        pg.box(xs[0], y, widths[0], rh, fill=BLACK if last else SWAMP, stroke=WHITE)
        pg.text(xs[0] + 8, y + 22, num, 16, GOLD, bold=True)
        pg.textbox(xs[0] + 6, y + 30, widths[0] - 10, 50, name, 8, WHITE, bold=True, lh=1.2)
        pg.textbox(xs[1] + 6, y + 8, widths[1] - 12, rh - 12, what, 7.5, BLACK, bold=True, lh=1.25)
        pg.textbox(xs[2] + 6, y + 8, widths[2] - 12, rh - 12, content, 7, INK, lh=1.25)
        pg.textbox(xs[3] + 6, y + 8, widths[3] - 12, rh - 12, where, 7, INK, lh=1.25)
        pg.textbox(xs[4] + 4, y + 8, widths[4] - 8, rh - 12, ldf, 6.5, MID, lh=1.25)
        if k == 3:
            # the combat-specific boundary
            pg.line(M, y + rh, M + sum(widths), y + rh, ARMY_RED, width=1.6)
        y += rh
    y += 10
    pg.box(M, y, W - 2 * M, 44, fill=PALE, stroke=None, radius=4)
    pg.textbox(M + 12, y + 8, W - 2 * M - 24, 34,
               "Steps 1 to 4 build Performance Under Pressure and apply wherever significant pressure exists, with or without an enemy. "
               "The red line marks the combat-specificity test: step 5 is where the capability is developed or applied against opposition or threat, "
               "significant consequence and ethical load, and becomes Combat Mindset. The developmental steps are cumulative; a soldier at step 5 keeps practising steps 1 to 4.",
               7.5, INK, lh=1.3)
    y += 56
    pg.text(M, y + 8, "Content, pathways and LDF alignment are indicative and will be confirmed through the Phase 2 assessment and Phase 4 validation.", 6.5, MID)


def page4(d):
    pg = d.page("Training Integration Map", "Where the existing pathways contribute to each step. Indicative; confirmed in the Phase 2 assessment.")
    y = 122
    lw, dw = 170, 72
    cw = (W - 2 * M - lw - dw) / 5
    pg.box(M, y, lw + dw, 38, fill=SWAMP, stroke=WHITE)
    pg.spaced(M + 6, y + 23, "PATHWAY", 6, WHITE, bold=True, spacing=1.0)
    for k, (num, name, _, _, _, _) in enumerate(STEPS):
        x = M + lw + dw + k * cw
        pg.box(x, y, cw, 38, fill=BLACK if k == 4 else SWAMP, stroke=WHITE)
        pg.text(x + cw / 2, y + 12, num, 8, GOLD, bold=True, align=1)
        pg.textbox(x + 2, y + 15, cw - 4, 24, name, 5, WHITE, bold=True, align=1, lh=1.1)
    y += 38
    rh = 46
    for r, (name, note, marks) in enumerate(PATHWAYS):
        fill = rgb("F3F3EF") if r % 2 else WHITE
        pg.box(M, y, W - 2 * M, rh, fill=fill, stroke=GRID)
        pg.textbox(M + 6, y + 8, lw - 10, 16, name, 7.5, BLACK, bold=True, lh=1.2)
        pg.textbox(M + 6, y + 21, lw + dw - 14, rh - 22, note, 6.2, MID, lh=1.2)
        for k, m in enumerate(marks):
            cx = M + lw + dw + k * cw + cw / 2
            cy = y + rh / 2
            if m == 2:
                sh = pg.p.new_shape(); sh.draw_circle((cx, cy), 6); sh.finish(color=None, fill=SWAMP); sh.commit()
            elif m == 1:
                sh = pg.p.new_shape(); sh.draw_circle((cx, cy), 6); sh.finish(color=SWAMP, fill=WHITE, width=1.2); sh.commit()
        y += rh
    y += 12
    sh = pg.p.new_shape(); sh.draw_circle((M + 8, y + 5), 5); sh.finish(color=None, fill=SWAMP); sh.commit()
    pg.text(M + 18, y + 8, "Primary contribution", 7, INK)
    sh = pg.p.new_shape(); sh.draw_circle((M + 130, y + 5), 5); sh.finish(color=SWAMP, fill=WHITE, width=1.2); sh.commit()
    pg.text(M + 140, y + 8, "Contributes", 7, INK)
    y += 24
    pg.box(M, y, W - 2 * M, 70, fill=PALE, stroke=None, radius=4)
    pg.spaced(M + 12, y + 14, "HOW TO READ THE MAP", 6.5, SWAMP, bold=True, spacing=1.4)
    pg.textbox(M + 12, y + 20, W - 2 * M - 24, 48,
               "Read down a column to see which pathways develop a step; read across a row to see how far a pathway reaches. "
               "No single pathway carries the whole capability, and no pathway is the framework. Performance cognition and mental skills sit inside "
               "Performance Under Pressure as complementary components, psychological and cognitive skill alongside physiological self-regulation, "
               "trained progressively and then applied under increasingly representative pressure. The map is not an organisational turf chart.",
               7.5, INK, lh=1.3)


def page5(d):
    pg = d.page("Governance and Delivery Model", "Proposed on the basis of COMDT ACS direction of 10 September. Enduring arrangements are confirmed through ATG.")
    y = 124
    bw, bh = 300, 60
    x = M
    for k, (org, role, what) in enumerate(GOVERNANCE):
        fill = [BLACK, SWAMP, OLIVE, SWAMP][k] if k < 3 else OLIVE
        fill = [BLACK, CHARCOAL, SWAMP, OLIVE][k]
        pg.box(x, y, bw, bh, fill=fill, stroke=None, radius=4)
        pg.spaced(x + 14, y + 20, org, 8, WHITE, bold=True, spacing=1.2)
        pg.text(x + 14, y + 34, role, 7.5, GOLD, bold=True)
        pg.textbox(x + 14, y + 38, bw - 28, 24, what, 6.8, MOAWHANGO, lh=1.2)
        if k < len(GOVERNANCE) - 1:
            pg.line(x + bw / 2, y + bh, x + bw / 2, y + bh + 16, BLACK, width=1.2)
            pg.text(x + bw / 2, y + bh + 15, "▼", 6, BLACK, align=1)
        y += bh + 16
    # advisers beside the chain
    ax = M + bw + 20
    aw = W - M - ax
    ay = 124
    pg.box(ax, ay, aw, 4 * 76 - 16, fill=FAINT, stroke=GOLD, radius=4)
    pg.spaced(ax + 12, ay + 18, "TECHNICAL ADVISERS", 7, SWAMP, bold=True, spacing=1.4)
    pg.textbox(ax + 12, ay + 24, aw - 24, 30, "Advise, contribute and enable. They do not own Combat Mindset.", 7, MID, lh=1.25)
    yy = ay + 58
    for org, what in ADVISERS:
        pg.box(ax + 12, yy, aw - 24, 44, fill=WHITE, stroke=GRID, radius=3)
        pg.spaced(ax + 20, yy + 14, org, 6.2, BLACK, bold=True, spacing=1.0)
        pg.textbox(ax + 20, yy + 19, aw - 40, 24, what, 6.5, INK, lh=1.2)
        yy += 52
    pg.textbox(ax + 12, yy + 4, aw - 24, 60, "Units validate operational sense; professional and technical stakeholders validate evidence and supportability. Both are needed.", 6.5, MID, lh=1.25)

    y += 10
    pg.spaced(M, y + 8, "DELIVERY MODEL", 7.5, SWAMP, bold=True, spacing=1.4)
    rows = [
        ("Embedded, not standalone", "Combat Mindset outcomes are carried in the pathways soldiers and officers already pass through: physical training, recruit and promotion courses, ELDA, commissioning, and field training. No standalone Combat Mindset course is created."),
        ("One language across pathways", "Common terminology, the developmental steps and the combat-specificity test are used by every pathway, whoever delivers it."),
        ("Owned through existing course governance", "Outcomes enter course data sheets and are approved through the ATRB; PT and field application are directed through policy and guidance rather than new courses."),
        ("Assured at three levels", "Individual and team: can people perform better under pressure? Product: does the intervention produce the outcome it claims? System: is Army consistently developing, delivering and assuring the capability?"),
    ]
    yy = y + 16
    for h, b in rows:
        pg.box(M, yy, W - 2 * M, 44, fill=FAINT, stroke=None, radius=3)
        pg.text(M + 12, yy + 14, h, 8, BLACK, bold=True)
        pg.textbox(M + 12, yy + 18, W - 2 * M - 24, 26, b, 7, INK, lh=1.25)
        yy += 50


def page6(d):
    pg = d.page("Syllabus and CDS Architecture", "What AITC would be approving: outcome statements carried into existing course data sheets, and where.")
    y = 122
    pg.spaced(M, y + 8, "DRAFT DEVELOPMENTAL OUTCOMES", 7.5, SWAMP, bold=True, spacing=1.4)
    outcomes = [
        "Recognises own physiological and cognitive responses to pressure and their effect on performance.",
        "Regulates arousal, attention and cognitive load using trained techniques while under genuine interference.",
        "Performs assigned tasks and makes sound decisions while fatigued, overloaded and stressed.",
        "Leads others under pressure, maintaining command presence, judgement, communication and influence.",
        "Applies the capability under threat, uncertainty, consequence and ethical load to achieve the mission.",
    ]
    yy = y + 16
    for k, o in enumerate(outcomes):
        pg.box(M, yy, 16, 16, fill=BLACK if k == 4 else SWAMP, stroke=None, radius=8)
        pg.text(M + 8, yy + 11.5, str(k + 1), 8, WHITE, bold=True, align=1)
        pg.textbox(M + 24, yy + 3, W - 2 * M - 24, 16, o, 7.8, INK, lh=1.2)
        yy += 22
    y = yy + 8
    pg.spaced(M, y + 8, "WHERE THE OUTCOMES ARE CARRIED", 7.5, SWAMP, bold=True, spacing=1.4)
    y += 16
    heads = ["PATHWAY OR COURSE", "LEVEL", "OUTCOMES", "CDS ACTION"]
    widths = [190, 90, 60, 175]
    xs = [M]
    for w in widths[:-1]:
        xs.append(xs[-1] + w)
    for h, x, w in zip(heads, xs, widths):
        pg.box(x, y, w, 16, fill=SWAMP, stroke=WHITE)
        pg.spaced(x + 5, y + 11, h, 5.6, WHITE, bold=True, spacing=0.9)
    y += 16
    rh = 30
    for r, (course, level, outs, action) in enumerate(CDS_ROWS):
        fill = rgb("F3F3EF") if r % 2 else WHITE
        pg.box(M, y, sum(widths), rh, fill=fill, stroke=GRID)
        pg.textbox(xs[0] + 5, y + 5, widths[0] - 10, rh - 6, course, 7, BLACK, bold=True, lh=1.2)
        pg.textbox(xs[1] + 5, y + 5, widths[1] - 10, rh - 6, level, 6.8, INK, lh=1.2)
        pg.text(xs[2] + widths[2] / 2, y + rh / 2 + 3, outs, 7.5, SWAMP, bold=True, align=1)
        pg.textbox(xs[3] + 5, y + 5, widths[3] - 10, rh - 6, action, 6.6, INK, lh=1.2)
        y += rh
    y += 12
    pg.box(M, y, W - 2 * M, 64, fill=PALE, stroke=None, radius=4)
    pg.spaced(M + 12, y + 14, "WHAT AITC IS ASKED TO APPROVE", 6.5, SWAMP, bold=True, spacing=1.4)
    pg.textbox(M + 12, y + 20, W - 2 * M - 24, 44,
               "The outcome statements and the principle that they are carried in existing course data sheets rather than in a new course. "
               "Individual CDS amendments follow through the ATRB once Framework v1.0 is approved. Course codes, levels and the outcome allocation "
               "are indicative and rest on the Phase 2 assessment; the COGCON row is held pending that assessment.",
               7.5, INK, lh=1.3)


def page7(d):
    pg = d.page("Implementation and Validation", "A compressed Define, Understand and initial Design sprint to AITC, then validation to Framework v1.0.")
    y = 126
    n = len(TIMELINE)
    cw = (W - 2 * M) / n
    pg.line(M, y + 14, W - M, y + 14, GRID, width=1.2)
    for k, (when, head, body) in enumerate(TIMELINE):
        cx = M + k * cw + cw / 2
        key = when in ("14 OCT", "LATE NOV")
        sh = pg.p.new_shape(); sh.draw_circle((cx, y + 14), 6 if key else 4.5)
        sh.finish(color=None, fill=ARMY_RED if key else SWAMP); sh.commit()
        pg.text(cx, y + 5, when, 7, BLACK, bold=True, align=1)
        pg.textbox(cx - cw / 2 + 3, y + 26, cw - 6, 24, head, 7, SWAMP, bold=True, align=1, lh=1.15)
        pg.textbox(cx - cw / 2 + 3, y + 46, cw - 6, 70, body, 6.2, INK, align=1, lh=1.2)
    y += 128
    pg.box(M, y, W - 2 * M, 118, fill=BLACK, stroke=None, radius=4)
    pg.spaced(M + 14, y + 18, "DECISIONS SOUGHT FROM AITC, 14 OCTOBER 2026", 7, GOLD, bold=True, spacing=1.4)
    yy = y + 32
    for k, dcn in enumerate(AITC_DECISIONS):
        pg.text(M + 14, yy + 6, f"{k + 1}.", 8, WHITE, bold=True)
        pg.textbox(M + 30, yy - 1, W - 2 * M - 44, 18, dcn, 7.8, WHITE, lh=1.2)
        yy += 16
    y += 130
    pg.spaced(M, y + 8, "VALIDATION", 7.5, SWAMP, bold=True, spacing=1.4)
    cols = [("INDIVIDUAL AND TEAM", "Can people perform better under pressure? Observed performance in bounded pilots against the outcome statements."),
            ("PRODUCT", "Does each intervention produce the outcome it claims? Evidence maturity, transfer and scalability assessed in Phase 2 and tested in pilots."),
            ("SYSTEM", "Is Army consistently developing, delivering and assuring the capability? Outcomes present in CDS, delivered as designed, and reported.")]
    cw = (W - 2 * M - 12) / 3
    yy = y + 16
    for k, (h, b) in enumerate(cols):
        x = M + k * (cw + 6)
        pg.box(x, yy, cw, 74, fill=FAINT, stroke=None, radius=3)
        pg.spaced(x + 10, yy + 15, h, 6.2, SWAMP, bold=True, spacing=1.0)
        pg.textbox(x + 10, yy + 21, cw - 20, 52, b, 6.8, INK, lh=1.25)
    y = yy + 86
    pg.spaced(M, y + 8, "BOUNDED PILOTS, OCTOBER TO NOVEMBER", 7.5, SWAMP, bold=True, spacing=1.4)
    pilots = ["PT-embedded self-regulation practice in one unit programme, with the PTI cadre.",
              "One JNCO Course or ELDA Lead Teams serial carrying outcomes 2 and 3 explicitly.",
              "Stakeholder validation of the map, governance and CDS architecture with ACS, NZALC, HPC, APS, ILD and selected units."]
    yy = y + 20
    for p in pilots:
        pg.text(M + 2, yy, "•", 8, SWAMP)
        pg.textbox(M + 12, yy - 7, W - 2 * M - 12, 16, p, 7.5, INK, lh=1.2)
        yy += 14
    y = yy + 8
    pg.box(M, y, W - 2 * M, 54, fill=PALE, stroke=None, radius=4)
    pg.spaced(M + 12, y + 14, "SEPARATE WORKSTREAM: LCFT CURRENCY", 6.5, SWAMP, bold=True, spacing=1.4)
    pg.textbox(M + 12, y + 20, W - 2 * M - 24, 34,
               "The 10 September discussion also produced a command decision on physical currency before promotion training: units certify LCFT currency, "
               "NCO School enforces it, and ELDA remains a developmental environment rather than an informal fitness assessment. That is progressed as its own "
               "workstream and is not part of the Combat Mindset Framework.",
               7.2, INK, lh=1.3)


def build():
    d = Doc()
    for fn in (page1, page2, page3, page4, page5, page6, page7):
        fn(d)
    d.doc.set_metadata({"title": "Combat Mindset Framework v0.2, AITC Discussion Draft", "author": "Army Command School"})
    d.doc.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
