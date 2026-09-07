#!/usr/bin/env python3
"""
Build the NZALC meeting record (priorities and consolidated action list)
as a branded .docx, reusing the data-sheet builder's styles and helpers.

    python3 build_meeting_record.py
    python3 convert_to_pdf.py output/nzalc-meeting-record.docx \\
                              output/nzalc-meeting-record.pdf
"""

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

import build_elda_data_sheet as cds

OUTPUT_DOCX = "./output/nzalc-meeting-record.docx"
TITLE = "Priorities and Actions"
KICKER = "Meeting Record"
TAG = "NZALC Command and Staff Meeting"
REFERENCE = "Meeting notes, September 2026"
FOOTER_LEFT = "NZALC | Meeting Record"

TAKEAWAY = (
    "The centre's problem is no longer primarily designing good training. "
    "The material and delivery architecture are increasingly mature. The "
    "next phase is about institutionalising it: instructor behaviours, "
    "induction, SOPs, assurance, administrative discipline, and ensuring "
    "programmes such as Nemesis genuinely deliver the outcomes they claim "
    "to deliver."
)

PRIORITIES = [
    ("Course delivery is in a strong position.",
     "Lead Teams and ELDA delivery is producing good outcomes and the updated "
     "packages, tools and workbooks are aligned. The key vulnerability is now "
     "instructor engagement and consistency, particularly ensuring "
     "instructors actually use the updated material as designed."),
    ("Contractor onboarding needs immediate tightening.",
     "The recent contractor experience exposed gaps in induction, safety "
     "briefing, role suitability and due diligence. The individual should "
     "not be re-engaged, but the larger lesson is to establish a clear, "
     "repeatable staff and contractor onboarding SOP rather than treating "
     "this as an isolated personnel issue."),
    ("Nemesis needs a deliberate curriculum decision.",
     "It currently appears closer to a challenging rite-of-passage "
     "experience than a genuine equivalent of Lead Teams. The missing "
     "elements are particularly the structured cognitive preparation, "
     "coaching and reflection, and recovery phases. This needs to be "
     "resolved with OCS and Army leadership: either clarify Nemesis's "
     "distinct purpose or redesign it to achieve the intended Lead Teams "
     "outcomes."),
    ("Administration and assurance need continued focus.",
     "H&S audit actions, visitor management, signage, security training, "
     "POs and invoices and contractor administration are progressing but "
     "require active tracking. Jim's field strengths are recognised; the "
     "answer is to provide more deliberate administrative support and "
     "prioritisation around him rather than allowing critical tasks to "
     "drift."),
    ("The unit is otherwise in a good operational position.",
     "Courses, November activities, leave, end-of-year events and "
     "leadership-development work are broadly on track. The recent push to "
     "close outstanding work appears to have materially improved the unit's "
     "position."),
]

# (priority, action, owner, timing)
ACTIONS = [
    ("High", "Chase remaining Lead Leaders officer nominations and confirm "
             "final attendance", "Mike", "Tomorrow"),
    ("High", "Follow up Lighthouse approval for Engineer Survival", "Mike",
     "ASAP"),
    ("High", "Review and tighten the staff and contractor onboarding and "
             "induction SOP, including safety induction, supervision, due "
             "diligence and documented completion", "Mike", "ASAP"),
    ("High", "Close out the contractor engagement and ensure no expectation "
             "of future work remains. Jim makes the formal close-out call; "
             "Mike is accountable for confirming closure", "Jim (call); Mike "
             "(closure)", "ASAP"),
    ("High", "Work with Army and OCS leadership to clarify Nemesis versus "
             "Lead Teams: intended outcomes, perform and recovery phases, "
             "coaching and appropriate positioning", "Mike", "Upcoming"),
    ("High", "Track outstanding H&S audit actions, including kayak audit "
             "follow-up", "Mike", "Ongoing"),
    ("Medium", "Coordinate with Jim and Dave Bertram on leadership journal "
               "use and briefing for current and upcoming courses", "Mike",
     "Current courses"),
    ("Medium", "Prepare the ATG submission presentation and have Dave review "
               "it", "Mike", "Wed to Thu"),
    ("Medium", "Develop the leadership-development programme for the 16 to "
               "17 Nov Linton team-building activity, including allocation "
               "of instructors and session responsibilities", "Mike",
     "Before Nov"),
    ("Medium", "Organise the end-of-year farewell event, investigating the "
               "week of 23 Nov as the preferred option", "Mike",
     "Confirm soon"),
    ("Medium", "Provide Jim targeted admin support, particularly safety "
               "assurance, contractor administration and PO tracking",
     "Mike", "Ongoing"),
]


def add_action_table(doc):
    widths = (Cm(1.8), Cm(9.2), Cm(2.9), Cm(2.5))
    headers = ("Priority", "Action", "Owner", "Timing")
    table = doc.add_table(rows=len(ACTIONS) + 1, cols=4)
    table.autofit = False
    cds._table_borders(table, cds.GRID_GREY, outer=cds.WAIOURU_HILLS)
    for col, w in zip(table.columns, widths):
        col.width = w
    for r_idx, row_values in enumerate([headers] + ACTIONS):
        row = table.rows[r_idx]
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for c_idx, text in enumerate(row_values):
            cell = row.cells[c_idx]
            cell.width = widths[c_idx]
            cds._cell_margins(cell, top=55, bottom=55, left=100, right=100)
            cds._cell_valign_top(cell)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            if r_idx == 0:
                cds._cell_shading(cell, cds.SWAMP_GREEN)
                cds.add_text_runs(p, text, base_font=cds.FONT_HEAD, size=Pt(9),
                                  bold=True, color=cds.RUAPEHU_WHITE)
            elif c_idx == 0:
                cds._cell_shading(cell, cds.MOAWHANGO if text == "High" else cds.PALE_GREEN)
                cds.add_text_runs(p, text, base_font=cds.FONT_HEAD, size=Pt(9),
                                  bold=True, color=cds.SWAMP_GREEN)
            else:
                cds.add_text_runs(p, text, size=Pt(9.5))
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(4)
    return table


def build():
    doc = cds.new_document()
    cds.add_header_footer(doc.sections[0], FOOTER_LEFT)
    cds.add_title_block(KICKER, TITLE, TAG, reference=REFERENCE, status=None)

    # Key takeaway first, as a key message panel.
    panel = doc.add_paragraph()
    panel.paragraph_format.left_indent = Cm(0.3)
    panel.paragraph_format.right_indent = Cm(0.3)
    panel.paragraph_format.space_before = Pt(4)
    panel.paragraph_format.space_after = Pt(6)
    cds.set_shading(panel, cds.SWAMP_GREEN)
    cds.set_border(panel, "left", cds.ARMY_RED, 28, space=10)
    r = cds._run(panel, "KEY TAKEAWAY", cds.FONT_HEAD, Pt(7.5), True, False,
                 cds.MOAWHANGO)
    cds.letterspace(r, 30)
    panel.add_run().add_break()
    cds._run(panel, TAKEAWAY, cds.FONT_HEAD, Pt(10), True, False,
             cds.RUAPEHU_WHITE)

    cds.add_section_heading("Five Priorities")
    for n, (lead, text) in enumerate(PRIORITIES, 1):
        cds.add_numbered(n, f"**{lead}** {text}")

    h = cds.add_section_heading("Consolidated Action List")
    h.paragraph_format.page_break_before = True
    cds.add_body("Actions for Mike unless otherwise stated. High-priority "
                 "actions are shaded.")
    add_action_table(doc)

    cds.add_section_heading("Ownership Note")
    cds.add_body(
        "The formal close-out call to the contractor belongs to Jim, who was "
        "tasked with it at the meeting. Mike remains accountable for ensuring "
        "the engagement is closed and that no expectation of future work "
        "remains, and for the wider fix: a repeatable onboarding SOP rather "
        "than a one-off personnel response.")

    cds.finish(TITLE)
    doc.save(OUTPUT_DOCX)
    print(f"Saved {OUTPUT_DOCX}")


if __name__ == "__main__":
    build()
