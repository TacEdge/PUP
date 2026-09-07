#!/usr/bin/env python3
"""
Build the NZALC ELDA Course Portfolio: one branded .docx that compiles

  1. a cover page,
  2. a contents page (Word TOC field, resolved by convert_to_pdf.py),
  3. the one-page landscape ELDA Pathway Overview, and
  4. a Points for Validation page listing every carried-over placeholder, and
  5. the four proposed revised Course Data Sheets in pathway order
     (Lead Teams, Lead Leaders, Lead Systems, Command).

Content and styling come from build_elda_data_sheet.py and
build_elda_pathway.py, so the portfolio always matches the standalone
documents.  Run after any change to a data-sheet source:

    python3 build_elda_portfolio.py
    python3 convert_to_pdf.py output/elda-course-portfolio.docx \\
                              output/elda-course-portfolio.pdf
"""

from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.shared import Cm, Mm, Pt

import build_elda_data_sheet as cds
import build_elda_pathway as pathway

OUTPUT_DOCX = "./output/elda-course-portfolio.docx"
TITLE = "NZALC ELDA Course Portfolio"
SUBTITLE_1 = "Experiential Leadership Development Activities"
SUBTITLE_2 = "Pathway Overview and Course Data Sheets"
REFERENCE = "Course Data Sheets A18011, A18008, A18010, A18009"
STATUS = "Proposed Revision: Draft for Validation"
FOOTER_LEFT = "NZALC | ELDA Course Portfolio"

# Pathway order, not course-code order.
SHEET_ORDER = ["lead-teams", "lead-leaders", "lead-systems", "command"]


def set_portrait(section):
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.3)
    section.right_margin = Cm(2.3)
    section.header_distance = Cm(1.0)
    section.footer_distance = Cm(1.0)



# Every "retain / confirm / subject to review" entry carried over from the
# current data sheets, so the reader can see exactly what is still open.
VALIDATION = [
    ("Across all courses", [
        "Qualifications / Certifications. Confirm whether AA18001 to AA18007 "
        "are formal qualifications or certifications awarded on completion, "
        "or activity result codes. The notes in each data sheet state that "
        "the adventure activity is the experiential vehicle, not the "
        "learning outcome; if the codes are result codes, relabel the field "
        "in the supporting documentation so it does not imply a substantive "
        "adventure qualification.",
        "Governance Body. Confirm that the Army Training Review Board (ATRB) "
        "remains the governance body for all four courses.",
        "Included Courses. Confirm the current SOLO administrative "
        "configuration for each course and record it explicitly.",
        "Staff qualifications. Confirm the NZALC Activity SOP references and "
        "instructor-to-learner ratios against the current NZALC Safety "
        "Management Plan and activity SOPs.",
    ]),
    ("A18011 ELDA Lead Teams", [
        "Course Entry Requirements. The existing A1530 entry requirements and "
        "prerequisite codes are carried forward by reference only. List them "
        "explicitly once verified in SOLO, so this sheet matches the "
        "specificity of the other three.",
        "Manual Checks. Confirm the medical fitness requirement for prolonged "
        "field activity carrying FSMO against the NZALC Safety Management "
        "Plan and applicable NZDF medical policy.",
        "Note 3. Confirm that delivery before D03020 LDS Lead Teams remains a "
        "current sequencing requirement.",
    ]),
    ("A18008 ELDA Lead Leaders", [
        "Course Entry Requirements. Confirm the DLMS medical classification, "
        "Service fitness requirement and prerequisite codes D03030 (Regular "
        "Force) and D03003 (OB) against current NZDF policy.",
        "Non-NZDF Personnel Suitability. The current administrative setting "
        "is carried forward subject to review; record the confirmed setting.",
    ]),
    ("A18010 ELDA Lead Systems", [
        "Course Entry Requirements. Confirm the medical classification "
        "(A4 G3 Z1 or higher) and fitness requirement (Pass or higher) "
        "against current NZDF policy.",
    ]),
    ("A18009 ELDA Command", [
        "Course Entry Requirements. Confirm the medical classification "
        "(A4 G3 Z1 or higher) and fitness requirement (Pass or higher) "
        "against current NZDF policy.",
        "Manual Checks. Confirm whether the current reference to HQ Joint "
        "Forces NZ SOP 10-75 remains current; retain it only if so.",
    ]),
]


def render_validation(doc):
    cds.add_title_block("Portfolio", "Points for Validation",
                        "Administrative entries to confirm before publication",
                        reference=None, with_logo=False, title_style="Heading 1")
    intro = doc.add_paragraph()
    cds.add_text_runs(intro, (
        "The learning outcomes, aims and notes in this portfolio are the "
        "proposed redraft. The entries below were carried over from the "
        "current data sheets and are marked in the sheets as retained, "
        "subject to confirmation or subject to review. Each is to be "
        "validated and the placeholder wording replaced before the package "
        "is submitted as the authoritative revision."))
    for heading, items in VALIDATION:
        cds.add_sub_heading(heading, 3)
        cds._context["notes"] = True   # supporting material: notes sizing
        for n, item in enumerate(items, 1):
            lead, _, rest = item.partition(". ")
            cds.add_numbered(n, f"**{lead}.** {rest}")


def build():
    doc = cds.new_document()
    cds.SECTION_HEADING_STYLE = "Heading 2"   # data-sheet sections nest under each sheet
    cds.add_header_footer(doc.sections[0], FOOTER_LEFT)

    # ---- 1. cover -------------------------------------------------------
    cds.add_logo(width_mm=46, space_after=54)

    # Hero block: a single dark-green cell carrying the title.
    hero = doc.add_table(rows=1, cols=1)
    hero.autofit = False
    hero.columns[0].width = Cm(cds.TEXT_WIDTH_CM)
    cell = hero.cell(0, 0)
    cell.width = Cm(cds.TEXT_WIDTH_CM)
    cds._cell_shading(cell, cds.SWAMP_GREEN)
    cds._cell_margins(cell, top=420, bottom=420, left=440, right=440)
    k = cell.paragraphs[0]
    k.paragraph_format.space_after = Pt(10)
    r = cds._run(k, "NEW ZEALAND ARMY LEADERSHIP CENTRE", cds.FONT_HEAD,
                 Pt(9.5), True, False, cds.MOAWHANGO)
    cds.letterspace(r, 50)
    t = cell.add_paragraph()
    t.paragraph_format.space_after = Pt(14)
    t.paragraph_format.line_spacing = 1.0
    cds._run(t, TITLE, cds.FONT_HEAD, Pt(34), True, False, cds.RUAPEHU_WHITE)
    s1 = cell.add_paragraph()
    s1.paragraph_format.space_after = Pt(2)
    cds._run(s1, SUBTITLE_1, cds.FONT_HEAD, Pt(14), True, False, cds.RUAPEHU_WHITE)
    s2 = cell.add_paragraph()
    s2.paragraph_format.space_after = Pt(0)
    cds._run(s2, SUBTITLE_2, cds.FONT_HEAD, Pt(12), False, False, cds.MOAWHANGO)

    rule = doc.add_paragraph()
    rule.paragraph_format.space_after = Pt(10)
    cds.set_border(rule, "bottom", cds.ARMY_RED, 24, space=1)

    o = doc.add_paragraph()
    o.paragraph_format.space_before = Pt(6)
    o.paragraph_format.space_after = Pt(2)
    cds._run(o, cds.ORIGINATOR_LONG, cds.FONT_HEAD, Pt(10.5), False, False,
             cds.SWAMP_GREEN)
    m = doc.add_paragraph()
    m.paragraph_format.space_after = Pt(0)
    for i, (label, value) in enumerate([("Reference", REFERENCE), ("Date", cds.DATE),
                                        ("Status", STATUS)]):
        if i:
            cds._run(m, "   ·   ", cds.FONT_HEAD, Pt(9), False, False, cds.WAIOURU_HILLS)
        cds._run(m, f"{label}: ", cds.FONT_HEAD, Pt(9), True, False, cds.SWAMP_GREEN)
        cds._run(m, value, cds.FONT_HEAD, Pt(9), label == "Status", False,
                 cds.ARMY_RED if label == "Status" else cds.DARKEST_HOUR)

    intro = doc.add_paragraph()
    intro.paragraph_format.space_before = Pt(48)
    cds.add_text_runs(intro, (
        "This portfolio brings together the proposed revised course data "
        "sheets for the four Experiential Leadership Development Activity "
        "(ELDA) courses delivered by the New Zealand Army Leadership Centre, "
        "together with a one-page overview of the pathway they form. The "
        "learning architecture is settled; a number of administrative "
        "entries carried over from the current data sheets remain to be "
        "validated against SOLO, DLMS and current NZDF policy before the "
        "package is published. Those entries are listed under Points for "
        "Validation."))
    for line in [
        "ELDA Pathway Overview",
        "Points for Validation",
        "A18011 ELDA Lead Teams",
        "A18008 ELDA Lead Leaders",
        "A18010 ELDA Lead Systems",
        "A18009 ELDA Command",
    ]:
        cds.add_bullet(line)

    # ---- 2. contents ----------------------------------------------------
    toc_head = doc.add_paragraph()
    toc_head.paragraph_format.page_break_before = True
    toc_head.paragraph_format.space_after = Pt(12)
    cds.add_text_runs(toc_head, "Contents", base_font=cds.FONT_HEAD,
                      size=Pt(16), bold=True)
    toc_p = doc.add_paragraph()
    cds.add_field(toc_p, r'TOC \o "1-2" \h \z \u',
                  "Right-click and choose Update Field to refresh the contents.")

    # ---- 3. pathway overview (landscape section) ------------------------
    land = doc.add_section(WD_SECTION.NEW_PAGE)
    pathway.set_landscape(land)
    # Landscape footer tabs need the wider text width.
    land.footer.is_linked_to_previous = False
    land.header.is_linked_to_previous = False
    cds.add_header_footer(land, FOOTER_LEFT, text_width_cm=pathway.TEXT_WIDTH_CM)

    pathway.add_letterhead(doc, with_logo=False, title_style="Heading 1")
    pathway.render_pathway_table(doc)
    pathway.render_closing(doc)

    # ---- 4. course data sheets (portrait section) -----------------------
    port = doc.add_section(WD_SECTION.NEW_PAGE)
    set_portrait(port)
    port.footer.is_linked_to_previous = False
    port.header.is_linked_to_previous = False
    cds.add_header_footer(port, FOOTER_LEFT)

    render_validation(doc)

    for key in SHEET_ORDER:
        sheet = cds.SHEETS[key]
        cds.add_letterhead(sheet["title"], cds.SUBTITLE_LINE,
                           sheet["reference"], with_logo=False,
                           title_style="Heading 1", sheet=sheet,
                           page_break=True)
        with open(sheet["source"], encoding="utf-8") as fh:
            cds.render_markdown(fh.read().splitlines())

    cds.finish(TITLE)
    doc.save(OUTPUT_DOCX)
    print(f"Saved {OUTPUT_DOCX}")


if __name__ == "__main__":
    build()
