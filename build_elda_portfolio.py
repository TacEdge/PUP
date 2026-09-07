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
TITLE = "Proposed Revised ELDA Course Portfolio"
SUBTITLE = ("NZALC Experiential Leadership Development Activities: "
            "Pathway Overview and Course Data Sheets")
REFERENCE = "Course Data Sheets A18011, A18008, A18010, A18009"
STATUS = "Draft for Validation"
FOOTER_LEFT = "Proposed Revised ELDA Course Portfolio"

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
    title = doc.add_paragraph(style="Heading 1")
    cds.add_text_runs(title, "Points for Validation", base_font=cds.FONT_HEAD,
                      size=Pt(20), bold=True)
    sub = doc.add_paragraph()
    sub.paragraph_format.space_after = Pt(4)
    cds.set_border(sub, "bottom", cds.ARMY_RED, 18, space=8)
    cds.add_text_runs(sub, "Administrative entries to confirm before publication",
                      base_font=cds.FONT_HEAD, size=Pt(12), bold=True,
                      color=cds.SWAMP_GREEN)
    intro = doc.add_paragraph()
    intro.paragraph_format.space_before = Pt(8)
    cds.add_text_runs(intro, (
        "The learning outcomes, aims and notes in this portfolio are the "
        "proposed redraft. The entries below were carried over from the "
        "current data sheets and are marked in the sheets as retained, "
        "subject to confirmation or subject to review. Each is to be "
        "validated and the placeholder wording replaced before the package "
        "is submitted as the authoritative revision."))
    for heading, items in VALIDATION:
        cds.add_sub_heading(heading, 3)
        for n, item in enumerate(items, 1):
            lead, _, rest = item.partition(". ")
            cds.add_numbered(n, f"**{lead}.** {rest}")


def build():
    doc = cds.new_document()
    cds.SECTION_HEADING_STYLE = "Heading 2"   # data-sheet sections nest under each sheet
    cds.add_header_footer(doc.sections[0], FOOTER_LEFT)

    # ---- 1. cover -------------------------------------------------------
    cds.add_logo(width_mm=48, space_after=60)
    t = doc.add_paragraph()
    t.paragraph_format.space_after = Pt(4)
    cds.add_text_runs(t, TITLE, base_font=cds.FONT_HEAD, size=Pt(28), bold=True)
    s = doc.add_paragraph()
    s.paragraph_format.space_after = Pt(6)
    cds.set_border(s, "bottom", cds.ARMY_RED, 24, space=10)
    cds.add_text_runs(s, SUBTITLE, base_font=cds.FONT_HEAD, size=Pt(13),
                      bold=True, color=cds.SWAMP_GREEN)
    o = doc.add_paragraph()
    o.paragraph_format.space_before = Pt(10)
    cds.add_text_runs(o, cds.ORIGINATOR, base_font=cds.FONT_HEAD, size=Pt(11),
                      color=cds.SWAMP_GREEN)
    for pairs in ([("Reference", REFERENCE), ("Date", cds.DATE)],
                  [("Status", STATUS)]):
        m = doc.add_paragraph()
        m.paragraph_format.space_after = Pt(2)
        for i, (label, value) in enumerate(pairs):
            if i:
                cds.add_text_runs(m, "      ", base_font=cds.FONT_HEAD)
            cds.add_text_runs(m, f"{label}  ", base_font=cds.FONT_HEAD, size=Pt(9.5),
                              bold=True, color=cds.SWAMP_GREEN)
            cds.add_text_runs(m, value, base_font=cds.FONT_HEAD, size=Pt(9.5),
                              bold=(label == "Status"))

    intro = doc.add_paragraph()
    intro.paragraph_format.space_before = Pt(36)
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
        title = cds.add_letterhead(sheet["title"], cds.SUBTITLE_LINE,
                                   sheet["reference"], with_logo=False,
                                   title_style="Heading 1")
        title.paragraph_format.page_break_before = True
        with open(sheet["source"], encoding="utf-8") as fh:
            cds.render_markdown(fh.read().splitlines())

    cds.finish(TITLE)
    doc.save(OUTPUT_DOCX)
    print(f"Saved {OUTPUT_DOCX}")


if __name__ == "__main__":
    build()
