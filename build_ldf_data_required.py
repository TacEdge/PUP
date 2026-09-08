#!/usr/bin/env python3
"""
The DATA REQUIRED register for the LDF alignment analysis: one row per
(transition x continuum x category), plus cross-cutting policy items.
Written as a plain .xlsx to be populated by hand.

    python3 build_ldf_data_required.py -> output/ldf-alignment-data-required.xlsx
"""

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = "./output/ldf-alignment-data-required.xlsx"

TRANSITIONS = [
    ("T1", "Lead Self", "Lead Teams"),
    ("T2", "Lead Teams", "Lead Leaders"),
    ("T3", "Lead Leaders", "Lead Systems"),
    ("T4", "Lead Systems", "Lead Capability"),
    ("T5", "Lead Capability", "Lead Integrated Capability"),
    ("T6", "Lead Integrated Capability", "Lead Organisation"),
]
CONTINUUMS = ["Officer", "Soldier"]

# category -> (question to answer, likely source)
CATEGORIES = [
    ("Promotion point",
     "Which Army promotion or career point corresponds to this LDF transition?",
     "Army promotion policy; Army Career Management"),
    ("Development intervention",
     "Which course or programme develops the individual for this transition (SOLO code, LDS, ELDA, promotion course)?",
     "SOLO course catalogue; ILD course list; NZALC course data sheets"),
    ("Career linkage",
     "Where does the link between the development and the transition sit: 4 formally mandated (in policy or embedded in the qualifying course), 3 functionally required (policed, not in policy), 2 expected (self-selected, high uptake), 1 self-selected (uptake by inclination), 0 unconnected?",
     "SOLO prerequisites; promotion course CDS; Army promotion policy"),
]

# Items already in hand.  Source order: the four source documents, this
# project's session documents, then the NZALC meeting of 9 Sep 2026 (Mike
# and Dave), whose statements carry the status STATED 9 SEP until checked.
MEET = "Meeting 9 Sep: "
KNOWN = {
    # promotion points (ranks per the meeting; the LDS poster's own mapping is an estimate)
    ("T1", "Officer", "Promotion point"): (MEET + "OCDT to 2LT (commissioning on NZCC).", "STATED 9 SEP"),
    ("T1", "Soldier", "Promotion point"): (MEET + "PTE to LCPL (JNCO course).", "STATED 9 SEP"),
    ("T2", "Officer", "Promotion point"): (MEET + "2LT and LT to CAPT; the substantive CAPT request.", "STATED 9 SEP"),
    ("T2", "Soldier", "Promotion point"): (MEET + "CPL to SGT (SNCO course).", "STATED 9 SEP"),
    ("T3", "Officer", "Promotion point"): (MEET + "CAPT to MAJ; CAPT to OC is the largest jump in scope of influence.", "STATED 9 SEP"),
    ("T3", "Soldier", "Promotion point"): (MEET + "SSGT to WO2; WO2 is the Lead Systems tick.", "STATED 9 SEP"),
    ("T4", "Officer", "Promotion point"): (MEET + "MAJ to LTCOL.", "STATED 9 SEP"),
    ("T4", "Soldier", "Promotion point"): (MEET + "WO2 to WO1; WO1 is the Lead Capability tick.", "STATED 9 SEP"),
    ("T5", "Officer", "Promotion point"): (MEET + "LTCOL and COL attend Lead Integrated Capability; senior MAJ do not.", "STATED 9 SEP"),
    ("T5", "Soldier", "Promotion point"): (MEET + "WO1s attend Lead Integrated Capability alongside LTCOL and COL.", "STATED 9 SEP"),
    ("T6", "Officer", "Promotion point"): (MEET + "COL and BRIG considered for the senior appointments.", "STATED 9 SEP"),
    ("T6", "Soldier", "Promotion point"): (MEET + "Senior WO1s considered for the senior appointments (SMA level).", "STATED 9 SEP"),
    # development interventions
    ("T1", "Officer", "Development intervention"): (MEET + "NZCC includes ELDA Lead Teams (the former Nemesis, rebranded with the same learning outcomes) and LDS Lead Teams, delivered by ALC at OCS in March, two years running.", "STATED 9 SEP"),
    ("T1", "Soldier", "Development intervention"): (MEET + "ELDA Lead Teams (A18011) embedded in the JNCO course (A1530) as the performance-under-pressure module; LDS Lead Teams (D03020) sequenced alongside.", "STATED 9 SEP"),
    ("T2", "Officer", "Development intervention"): (MEET + "ELDA Lead Leaders (A18008) and LDS Lead Leaders, distributed and self-scheduled. Session documents: A18008 targets 2LT and LT; prerequisite D03030 / D03003 referenced.", "STATED 9 SEP"),
    ("T2", "Soldier", "Development intervention"): (MEET + "SNCO course (A1531) carries ELDA Lead Leaders (A18008) and LDS Lead Leaders (D03030).", "STATED 9 SEP"),
    ("T3", "Officer", "Development intervention"): (MEET + "ELDA Lead Systems (A18010, ALC) and LDS Lead Systems (ILD). Session documents: A18010 targets CAPT preparing for MAJ; A1302 referenced.", "STATED 9 SEP"),
    ("T3", "Soldier", "Development intervention"): (MEET + "ELDA Lead Systems (A18010) on the WO course (A1532); LDS Lead Systems delivered by ILD, routinely before or after the promotion course because Army cannot guarantee a seat.", "STATED 9 SEP"),
    ("T4", "Officer", "Development intervention"): (MEET + "LDS Lead Capability, ILD tri-service course.", "STATED 9 SEP"),
    ("T4", "Soldier", "Development intervention"): (MEET + "LDS Lead Capability, ILD tri-service course.", "STATED 9 SEP"),
    ("T5", "Officer", "Development intervention"): (MEET + "LDS Lead Integrated Capability: one ELDA week (ALC caving or Navy sailing as activity contractors) plus one LDS week in Wellington; ILD runs, facilitates and funds both. 12 to 16 students; ALC now runs one caving week a year.", "STATED 9 SEP"),
    ("T5", "Soldier", "Development intervention"): (MEET + "As for Officer.", "STATED 9 SEP"),
    ("T6", "Officer", "Development intervention"): (MEET + "LDS Lead Organisation with an ELDA component (retreat setting, equine behaviour, psychometric profiling, external facilitation such as Rob Holt). Timing of the LDS element to check.", "STATED 9 SEP"),
    ("T6", "Soldier", "Development intervention"): (MEET + "As for Officer.", "STATED 9 SEP"),
    # mandates
    ("T1", "Officer", "Career linkage"): (MEET + 'Level 4, formally mandated: embedded in NZCC; qualifying on NZCC qualifies both LDS and ELDA Lead Teams.', 'STATED 9 SEP'),
    ("T1", "Soldier", "Career linkage"): (MEET + 'Level 4, formally mandated: an included course within the JNCO course for PTE to LCPL.', 'STATED 9 SEP'),
    ("T2", "Officer", "Career linkage"): (MEET + 'Level 3, functionally required: not in promotion policy, but policed by OCS and COs so that no 2LT or LT promotes to CAPT without it in practice. The single most important cell: confirm the policy position.', 'TO CONFIRM'),
    ("T2", "Soldier", "Career linkage"): (MEET + "Level 4, formally mandated in promotion policy: CPL promoting to SGT must complete the SNCO course, which carries it. 'Very clear on the NCO front.'", 'STATED 9 SEP'),
    ("T3", "Officer", "Career linkage"): (MEET + 'Level 1, self-selected: neither ELDA Lead Systems nor ILD LDS Lead Systems is mandated or policed; uptake rests on inclination. The weakest point on either continuum.', 'STATED 9 SEP'),
    ("T3", "Soldier", "Career linkage"): (MEET + "Level 4 for ELDA Lead Systems (mandated on the WO course). ILD LDS Lead Systems as a WO2 prerequisite: 'understanding is yes', with a question mark. Dave to check the promotion-course CDS.", 'TO CONFIRM'),
    ("T4", "Officer", "Career linkage"): (MEET + 'Level 2, expected: not mandated; impression is that all MAJ to LTCOL complete it. Confirm against promotion policy.', 'TO CONFIRM'),
    ("T4", "Soldier", "Career linkage"): (MEET + "Level 2, expected: expected for promotion to WO1; 'pretty sure' not in policy; most attend subject to an ILD seat. Confirm against promotion policy.", 'TO CONFIRM'),
    ("T5", "Officer", "Career linkage"): (MEET + 'Level 2, expected: ILD pathway; attendance without exception (selected, scrutinised, ambitious). Mandate not stated.', 'STATED 9 SEP'),
    ("T5", "Soldier", "Career linkage"): (MEET + 'Level 2, expected: ILD pathway; attendance without exception. Mandate not stated.', 'STATED 9 SEP'),
    ("T6", "Officer", "Career linkage"): (MEET + 'Level 2, expected: senior selection pathway; all complete it well before required. Mandate not stated.', 'STATED 9 SEP'),
    ("T6", "Soldier", "Career linkage"): (MEET + 'Level 2, expected: senior selection pathway; all complete it well before required. Mandate not stated.', 'STATED 9 SEP'),
}

CROSS_CUTTING = [
    ("X1", "Policy", "Army promotion policy: the authoritative statement of promotion prerequisites for each rank, Officer and Soldier. The meeting's officer statements (T2 to T4) are checked here first.", "Army orders; Army Career Management", "DATA REQUIRED"),
    ("X2", "Courses", "Complete list of Army promotion courses with codes, target ranks and the LDS or ELDA content each includes or requires.", "SOLO", "DATA REQUIRED"),
    ("X3", "Courses", "ILD delivery data for Lead Systems and above: which Army ranks attend, when relative to the promotion course, seats available to Army, and whether attendance is mandated.", "ILD; Army Career Management", "DATA REQUIRED"),
    ("X4", "Scope", "The authoritative Army view of which rank corresponds to each LDF transition. " + MEET + "WO2 is the Lead Systems tick, WO1 the Lead Capability tick; LIC attended by LTCOL, COL and WO1; Lead Org by COL, BRIG and senior WO1.", "AITC / Army Leadership Centre", "STATED 9 SEP"),
    ("X5", "Scope", "The substantive Captain request: its current status and any rationale already recorded for not linking Lead Leaders to promotion.", "COMDT ACS; Army Career Management", "DATA REQUIRED"),
    ("X6", "History", "The officer mandate history. " + MEET + "two-year pilot attaching Lead Leaders to Grade 2 and 3 coursing withdrawn as untenable time away from units; distributed self-scheduled approach agreed; Post Commissioning Programme delivered Lead Leaders before unit experience; AITC agreed in principle, then parked in a headquarters restructure; ACS not at the table for later redesigns. Dates and the AITC record to confirm.", "AITC minutes; ACS records", "STATED 9 SEP"),
    ("X7", "Delivery", "The 2012 division of delivery: single-Service providers to Lead Leaders, ILD for Lead Systems and above, Army retaining the ELDA function. " + MEET + "as stated; source document to cite.", "ILD; NZDF leadership governance", "STATED 9 SEP"),
    ("X8", "Explanation", "The candidate explanation for the difference. " + MEET + "'a scheduling oversight in the face of tempo'; non-required training is bumped; senior leaders assume the training is universal. Test against X1, X5 and X6 before it is presented as more than a candidate.", "COMDT ACS; AITC", "STATED 9 SEP"),
]

CAT_CODE = {"Promotion point": "PROM", "Development intervention": "DEV", "Career linkage": "LINK"}

STATUSES = ["DATA REQUIRED", "TO CONFIRM", "STATED 9 SEP", "KNOWN", "NOT APPLICABLE"]

GREEN = "002516"
BAND = "CDD2B7"
PALE = "EEF1E5"
GOLD = "A89662"


def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(name="Arial", size=9, bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=GREEN)
        cell.alignment = Alignment(vertical="center", wrap_text=True)


def build():
    wb = Workbook()
    ws = wb.active
    ws.title = "Data Required"
    thin = Side(style="thin", color="D9D9D2")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    headers = ["ID", "Transition", "From", "To", "Continuum", "Category",
               "Question to answer", "Likely source", "Currently in hand",
               "Status", "Answer (populate)", "Source cited (populate)", "Notes"]
    ws.append(headers)
    style_header(ws, 1, len(headers))

    n = 0
    for code, frm, to in TRANSITIONS:
        for cont in CONTINUUMS:
            for cat, question, source in CATEGORIES:
                n += 1
                known, status = KNOWN.get((code, cont, cat), ("", "DATA REQUIRED"))
                ws.append([f"{code}-{'O' if cont == 'Officer' else 'R'}-{CAT_CODE[cat]}",
                           code, frm, to, cont, cat, question, source, known, status, "", "", ""])
    for cid, area, item, source, status in CROSS_CUTTING:
        ws.append([cid, "All", "", "", "Both", area, item, source, "", status, "", "", ""])

    widths = [11, 9, 16, 22, 11, 20, 46, 30, 46, 15, 36, 24, 24]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for cell in row:
            cell.font = Font(name="Arial", size=9)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = border
        status = row[9].value
        fill = {"DATA REQUIRED": "F2F2F2", "TO CONFIRM": BAND, "STATED 9 SEP": "F3E9D2", "KNOWN": PALE, "NOT APPLICABLE": "FFFFFF"}.get(status, "FFFFFF")
        row[9].fill = PatternFill("solid", fgColor=fill)
        row[9].font = Font(name="Arial", size=9, bold=True, color=GREEN)
        for c in (10, 11, 12):
            row[c].fill = PatternFill("solid", fgColor="FFFBEA")
    ws.freeze_panes = "G2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{ws.max_row}"
    dv = DataValidation(type="list", formula1='"' + ",".join(STATUSES) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"J2:J{ws.max_row}")
    ws.row_dimensions[1].height = 30

    # Legend sheet
    lg = wb.create_sheet("Read Me")
    lines = [
        ("LDF ALIGNMENT: DATA REQUIRED REGISTER", True),
        ("", False),
        ("One row per transition (T1 to T6), per continuum (Officer, Soldier), per fact (promotion point, development intervention, mandate), plus cross-cutting items X1 to X8.", False),
        ("Populate the three cream columns: Answer, Source cited, Notes. Set Status when done.", False),
        ("", False),
        ("STATUS VALUES", True),
        ("DATA REQUIRED: nothing in hand.", False),
        ("TO CONFIRM: something in hand but from an estimate (the Leadership Levels poster) or a session document, not authoritative policy.", False),
        ("STATED 9 SEP: stated at the NZALC meeting of 9 Sep 2026 (Mike and Dave); the transcript governs over the generated notes. Treated as the working position; still to be checked against an authoritative source.", False),
        ("TO CONFIRM also marks the career-linkage cells where the meeting itself left a question mark or where a policy check decides the state (officer T2 to T4, soldier T3 and T4).", False),
        ("KNOWN: confirmed against an authoritative source.", False),
        ("NOT APPLICABLE: the category does not apply to this transition for this continuum (state why in Notes).", False),
        ("", False),
        ("CATEGORY MEANINGS", True),
    ]
    for cat, q, _ in CATEGORIES:
        lines.append((f"{cat}: {q}", False))
    lines += [("", False), ("PRIORITY", True),
              ("The Officer Career linkage rows at T2 to T4 decide the piece: confirm the meeting's statements against promotion policy (X1) first.", False),
              ("Then the Soldier Career linkage row at T3 (Dave: is ILD LDS Lead Systems a prerequisite in the WO promotion-course CDS?).", False),
              ("", False), ("LINKAGE SCALE", True),
              ("4 formally mandated; 3 functionally required; 2 expected (high uptake); 1 self-selected (uptake by inclination); 0 unconnected. Record the level in the Answer column once confirmed.", False)]
    for i, (text, bold) in enumerate(lines, 1):
        c = lg.cell(row=i, column=1, value=text)
        c.font = Font(name="Arial", size=10, bold=bold, color=GREEN if bold else "000000")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    lg.column_dimensions["A"].width = 120

    wb.save(OUT)
    print(f"Saved {OUT}: {n} matrix rows + {len(CROSS_CUTTING)} cross-cutting items")


if __name__ == "__main__":
    build()
