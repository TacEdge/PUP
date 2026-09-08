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
    ("Mandate",
     "Is that development a prerequisite for promotion, embedded in the promotion course, expected but not mandatory, or unconnected?",
     "SOLO prerequisites; promotion course CDS; Army promotion policy"),
]

# Items already in hand from the four sources or this project's session documents.
KNOWN = {
    ("T1", "Officer", "Promotion point"): ("Leadership Levels poster: OCDT (Lead Self) to Junior Officer (Lead Teams). Poster states rank alignment is 'only an estimation'.", "TO CONFIRM"),
    ("T1", "Soldier", "Promotion point"): ("Leadership Levels poster: PTE to LCPL / CPL. 'Only an estimation'.", "TO CONFIRM"),
    ("T2", "Officer", "Promotion point"): ("Leadership Levels poster: Junior Officer spans Transition One and Two.", "TO CONFIRM"),
    ("T2", "Soldier", "Promotion point"): ("Leadership Levels poster: SGT / SSGT / WO band.", "TO CONFIRM"),
    ("T3", "Officer", "Promotion point"): ("Leadership Levels poster: MAJ (Transition Three).", "TO CONFIRM"),
    ("T3", "Soldier", "Promotion point"): ("Leadership Levels poster: WO band; Tier 5 WO at Transition Four.", "TO CONFIRM"),
    ("T4", "Officer", "Promotion point"): ("Leadership Levels poster: LTCOL (Transition Four).", "TO CONFIRM"),
    ("T4", "Soldier", "Promotion point"): ("Leadership Levels poster: Tier 5 WO.", "TO CONFIRM"),
    ("T5", "Officer", "Promotion point"): ("Leadership Levels poster: COL (Transition Five).", "TO CONFIRM"),
    ("T5", "Soldier", "Promotion point"): ("Leadership Levels poster: Tier 4 WO.", "TO CONFIRM"),
    ("T6", "Officer", "Promotion point"): ("Leadership Levels poster: BRIG and above (Transition Six).", "TO CONFIRM"),
    ("T6", "Soldier", "Promotion point"): ("Leadership Levels poster: Tier 3 WO and above.", "TO CONFIRM"),
    ("T1", "Officer", "Development intervention"): ("LDS poster: LDS Lead Teams course embedded in single-Service development courses.", "TO CONFIRM"),
    ("T1", "Soldier", "Development intervention"): ("LDS poster: LDS Lead Teams course embedded in single-Service development courses. Session documents: ELDA Lead Teams (A18011) is an included course within A1530 JNCO Course; D03020 LDS Lead Teams sequencing referenced.", "TO CONFIRM"),
    ("T2", "Officer", "Development intervention"): ("LDS poster: LDS Lead Leaders course delivered by single-Service learning providers. Session documents: ELDA Lead Leaders (A18008) targets 2LT and LT; prerequisite D03030 / D03003 LDS Lead Leaders referenced.", "TO CONFIRM"),
    ("T2", "Soldier", "Development intervention"): ("LDS poster: as for Officer. Session documents: ELDA Lead Leaders targets NCOs accepted onto A1531 SNCO Promotion Course.", "TO CONFIRM"),
    ("T3", "Officer", "Development intervention"): ("LDS poster: LDS Lead Systems course delivered by ILD. Session documents: ELDA Lead Systems (A18010) targets Captains preparing for promotion to Major; A1302 Staff and Tactics Grade Two referenced.", "TO CONFIRM"),
    ("T3", "Soldier", "Development intervention"): ("LDS poster: as for Officer. Session documents: ELDA Lead Systems targets SNCOs and WOs accepted onto A1532 WO Course.", "TO CONFIRM"),
    ("T4", "Officer", "Development intervention"): ("LDS poster: LDS Lead Capability course delivered by ILD.", "TO CONFIRM"),
    ("T4", "Soldier", "Development intervention"): ("LDS poster: LDS Lead Capability course delivered by ILD.", "TO CONFIRM"),
    ("T5", "Officer", "Development intervention"): ("LDS poster: LDS Lead Integrated course delivered by ILD.", "TO CONFIRM"),
    ("T5", "Soldier", "Development intervention"): ("LDS poster: LDS Lead Integrated course delivered by ILD.", "TO CONFIRM"),
    ("T6", "Officer", "Development intervention"): ("LDS poster: LDS Lead Organisation course delivered by ILD.", "TO CONFIRM"),
    ("T6", "Soldier", "Development intervention"): ("LDS poster: LDS Lead Organisation course delivered by ILD.", "TO CONFIRM"),
}
KNOWN[("T2", "Officer", "Mandate")] = ("The trigger for the tasking: a request to link Lead Leaders to promotion to substantive Captain, implying no current mandate. The single most important cell.", "DATA REQUIRED")
KNOWN[("T1", "Soldier", "Mandate")] = ("Session documents: ELDA Lead Teams is an included course within the A1530 JNCO Course.", "TO CONFIRM")
KNOWN[("T2", "Soldier", "Mandate")] = ("Session documents: D03030 LDS Lead Leaders listed as a prerequisite; ELDA Lead Leaders targets NCOs accepted onto A1531.", "TO CONFIRM")

CROSS_CUTTING = [
    ("X1", "Policy", "Army promotion policy: the authoritative statement of promotion prerequisites for each rank, Officer and Soldier.", "Army orders; Army Career Management"),
    ("X2", "Courses", "Complete list of Army promotion courses with codes, target ranks and the LDS or ELDA content each includes or requires.", "SOLO"),
    ("X3", "Courses", "ILD delivery data for Lead Capability and above: which Army ranks attend, when, and whether attendance is mandated.", "ILD; Army Career Management"),
    ("X4", "Scope", "The authoritative Army view of which rank corresponds to each LDF transition, replacing the LDS poster estimate.", "AITC / Army Leadership Centre"),
    ("X5", "Scope", "The substantive Captain request: its current status and any rationale already recorded for not linking Lead Leaders to promotion.", "COMDT ACS; Army Career Management"),
]

STATUSES = ["DATA REQUIRED", "TO CONFIRM", "KNOWN", "NOT APPLICABLE"]

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
                ws.append([f"{code}-{'O' if cont == 'Officer' else 'R'}-{cat.split(' ')[0][:4].upper()}",
                           code, frm, to, cont, cat, question, source, known, status, "", "", ""])
    for cid, area, item, source in CROSS_CUTTING:
        ws.append([cid, "All", "", "", "Both", area, item, source, "", "DATA REQUIRED", "", "", ""])

    widths = [11, 9, 16, 22, 11, 20, 46, 30, 46, 15, 36, 24, 24]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for cell in row:
            cell.font = Font(name="Arial", size=9)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = border
        status = row[9].value
        fill = {"DATA REQUIRED": "F2F2F2", "TO CONFIRM": BAND, "KNOWN": PALE, "NOT APPLICABLE": "FFFFFF"}.get(status, "FFFFFF")
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
        ("One row per transition (T1 to T6), per continuum (Officer, Soldier), per fact (promotion point, development intervention, mandate), plus cross-cutting items X1 to X5.", False),
        ("Populate the three cream columns: Answer, Source cited, Notes. Set Status when done.", False),
        ("", False),
        ("STATUS VALUES", True),
        ("DATA REQUIRED: nothing in hand.", False),
        ("TO CONFIRM: something in hand but from an estimate (the Leadership Levels poster) or a session document, not authoritative policy.", False),
        ("KNOWN: confirmed against an authoritative source.", False),
        ("NOT APPLICABLE: the category does not apply to this transition for this continuum (state why in Notes).", False),
        ("", False),
        ("CATEGORY MEANINGS", True),
    ]
    for cat, q, _ in CATEGORIES:
        lines.append((f"{cat}: {q}", False))
    lines += [("", False), ("PRIORITY", True),
              ("The Officer Mandate rows at T2 and T3 decide the piece. Populate those first.", False)]
    for i, (text, bold) in enumerate(lines, 1):
        c = lg.cell(row=i, column=1, value=text)
        c.font = Font(name="Arial", size=10, bold=bold, color=GREEN if bold else "000000")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    lg.column_dimensions["A"].width = 120

    wb.save(OUT)
    print(f"Saved {OUT}: {n} matrix rows + {len(CROSS_CUTTING)} cross-cutting items")


if __name__ == "__main__":
    build()
