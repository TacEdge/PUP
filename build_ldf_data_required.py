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
CONTINUUMS = ["Officer", "Other Rank"]

# category -> (question to answer, likely source)
CATEGORIES = [
    ("Rank / career point",
     "Which Army promotion or career point corresponds to this transition?",
     "Army career management policy; DFO promotion regulations; Army Career Management"),
    ("Appointment / responsibility",
     "What appointment or increase in leadership responsibility is assumed at this point?",
     "Position descriptions; establishment; corps career profiles"),
    ("Formal development",
     "What course, programme or intervention exists for this transition (LDS course, promotion course, ELDA, other)?",
     "SOLO course catalogue; ILD course list; NZALC course data sheets"),
    ("Career linkage",
     "Is the intervention a prerequisite for promotion, embedded in a promotion course, a prerequisite for appointment, expected but not mandatory, or disconnected?",
     "SOLO prerequisites; promotion course CDS; DFO / Army promotion policy"),
    ("Timing",
     "Does the development occur before, at or after the transition (LDS intent: about six months prior, in the Orientation phase)?",
     "Course scheduling; nomination windows; career management practice"),
    ("Assurance",
     "How does Army know the individual is ready to lead at the new level (assessment, PDR mapping, board, competency sign-off)?",
     "PDR / performance system; promotion board criteria; course assessment"),
]

# Items already in hand from the four sources or this project's session documents.
KNOWN = {
    ("T1", "Officer", "Rank / career point"): ("Leadership Levels poster: OCDT (Lead Self) to Junior Officer (Lead Teams). Poster states rank alignment is 'only an estimation'.", "TO CONFIRM"),
    ("T1", "Other Rank", "Rank / career point"): ("Leadership Levels poster: PTE to LCPL / CPL. 'Only an estimation'.", "TO CONFIRM"),
    ("T2", "Officer", "Rank / career point"): ("Leadership Levels poster: Junior Officer spans Transition One and Two.", "TO CONFIRM"),
    ("T2", "Other Rank", "Rank / career point"): ("Leadership Levels poster: SGT / SSGT / WO band.", "TO CONFIRM"),
    ("T3", "Officer", "Rank / career point"): ("Leadership Levels poster: MAJ (Transition Three).", "TO CONFIRM"),
    ("T3", "Other Rank", "Rank / career point"): ("Leadership Levels poster: WO band; Tier 5 WO at Transition Four.", "TO CONFIRM"),
    ("T4", "Officer", "Rank / career point"): ("Leadership Levels poster: LTCOL (Transition Four).", "TO CONFIRM"),
    ("T4", "Other Rank", "Rank / career point"): ("Leadership Levels poster: Tier 5 WO.", "TO CONFIRM"),
    ("T5", "Officer", "Rank / career point"): ("Leadership Levels poster: COL (Transition Five).", "TO CONFIRM"),
    ("T5", "Other Rank", "Rank / career point"): ("Leadership Levels poster: Tier 4 WO.", "TO CONFIRM"),
    ("T6", "Officer", "Rank / career point"): ("Leadership Levels poster: BRIG and above (Transition Six).", "TO CONFIRM"),
    ("T6", "Other Rank", "Rank / career point"): ("Leadership Levels poster: Tier 3 WO and above.", "TO CONFIRM"),
    ("T1", "Officer", "Formal development"): ("LDS poster: LDS Lead Teams course embedded in single-Service development courses.", "TO CONFIRM"),
    ("T1", "Other Rank", "Formal development"): ("LDS poster: LDS Lead Teams course embedded in single-Service development courses. Session documents: ELDA Lead Teams (A18011) is an included course within A1530 JNCO Course; D03020 LDS Lead Teams sequencing referenced.", "TO CONFIRM"),
    ("T2", "Officer", "Formal development"): ("LDS poster: LDS Lead Leaders course delivered by single-Service learning providers. Session documents: ELDA Lead Leaders (A18008) targets 2LT and LT; prerequisite D03030 / D03003 LDS Lead Leaders referenced.", "TO CONFIRM"),
    ("T2", "Other Rank", "Formal development"): ("LDS poster: as for Officer. Session documents: ELDA Lead Leaders targets NCOs accepted onto A1531 SNCO Promotion Course.", "TO CONFIRM"),
    ("T3", "Officer", "Formal development"): ("LDS poster: LDS Lead Systems course delivered by ILD. Session documents: ELDA Lead Systems (A18010) targets Captains preparing for promotion to Major; A1302 Staff and Tactics Grade Two referenced.", "TO CONFIRM"),
    ("T3", "Other Rank", "Formal development"): ("LDS poster: as for Officer. Session documents: ELDA Lead Systems targets SNCOs and WOs accepted onto A1532 WO Course.", "TO CONFIRM"),
    ("T4", "Officer", "Formal development"): ("LDS poster: LDS Lead Capability course delivered by ILD.", "TO CONFIRM"),
    ("T4", "Other Rank", "Formal development"): ("LDS poster: LDS Lead Capability course delivered by ILD.", "TO CONFIRM"),
    ("T5", "Officer", "Formal development"): ("LDS poster: LDS Lead Integrated course delivered by ILD.", "TO CONFIRM"),
    ("T5", "Other Rank", "Formal development"): ("LDS poster: LDS Lead Integrated course delivered by ILD.", "TO CONFIRM"),
    ("T6", "Officer", "Formal development"): ("LDS poster: LDS Lead Organisation course delivered by ILD.", "TO CONFIRM"),
    ("T6", "Other Rank", "Formal development"): ("LDS poster: LDS Lead Organisation course delivered by ILD.", "TO CONFIRM"),
}
for t, _, _ in TRANSITIONS:
    for c in CONTINUUMS:
        KNOWN.setdefault((t, c, "Timing"), ("LDS poster intent only: LDS course 'ideally 6 months prior to transition to the new level'. Army practice not known.", "DATA REQUIRED"))

CROSS_CUTTING = [
    ("X1", "Policy", "Army promotion policy: the authoritative statement of promotion prerequisites for each rank, Officer and OR.", "DFO / Army orders; Army Career Management"),
    ("X2", "Policy", "Army career-development continuum documents (Officer and OR), including any published 'career pathway' diagrams.", "Army Career Management; Corps career profiles"),
    ("X3", "Courses", "Complete list of Army promotion and career courses with codes, target ranks and included or prerequisite LDS content.", "SOLO"),
    ("X4", "Courses", "ILD delivery data for Lead Systems and above: which Army ranks attend, when in career, and whether attendance is mandated.", "ILD; Army Career Management"),
    ("X5", "Assurance", "How the LDF Essential Tasks map to the Army PDR and whether PDR outcomes feed promotion boards.", "PDR policy; promotion board terms of reference"),
    ("X6", "Assurance", "Whether any readiness assessment exists at the point of first appointment to a new leadership level.", "Army Career Management; commanders"),
    ("X7", "Scope", "Treatment of Reserve Force, lateral entrants and civilian leaders: in or out of scope for this analysis.", "AITC direction"),
    ("X8", "Scope", "Which Army rank equates to each LDF level: the authoritative Army view, replacing the LDS poster estimate.", "AITC / Army Leadership Centre"),
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
        ("One row per transition (T1 to T6), per continuum (Officer, Other Rank), per analytical category, plus cross-cutting items X1 to X8.", False),
        ("Populate the three cream columns: Answer, Source cited, Notes. Set Status when done.", False),
        ("", False),
        ("STATUS VALUES", True),
        ("DATA REQUIRED: nothing in hand. Grey on the matrix.", False),
        ("TO CONFIRM: something in hand but from an estimate (the Leadership Levels poster) or a session document, not authoritative policy. Amber on the matrix.", False),
        ("KNOWN: confirmed against an authoritative source. Eligible for green or a named gap on the matrix.", False),
        ("NOT APPLICABLE: the category does not apply to this transition for this continuum (state why in Notes).", False),
        ("", False),
        ("CATEGORY MEANINGS", True),
    ]
    for cat, q, _ in CATEGORIES:
        lines.append((f"{cat}: {q}", False))
    lines += [("", False), ("GAP TYPES (assigned during analysis, not data entry)", True),
              ("DEVELOPMENT: no deliberate development identified for the transition.", False),
              ("ALIGNMENT: development exists but does not correspond cleanly with the LDF transition.", False),
              ("TIMING: development occurs after the individual has already transitioned.", False),
              ("CONSEQUENCE: appropriate development exists but has no formal relationship with promotion or appointment.", False),
              ("ASSURANCE: no clear mechanism establishes readiness for the next leadership level.", False),
              ("DATA: insufficient information currently available.", False)]
    for i, (text, bold) in enumerate(lines, 1):
        c = lg.cell(row=i, column=1, value=text)
        c.font = Font(name="Arial", size=10, bold=bold, color=GREEN if bold else "000000")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    lg.column_dimensions["A"].width = 120

    wb.save(OUT)
    print(f"Saved {OUT}: {n} matrix rows + {len(CROSS_CUTTING)} cross-cutting items")


if __name__ == "__main__":
    build()
