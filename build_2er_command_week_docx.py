#!/usr/bin/env python3
"""
2 ER Command Week initiating one-pager as an editable Word document in the
shared house style.  The PDF is drawn separately by build_2er_command_week.py.

    python3 build_2er_command_week_docx.py
"""

from docx.shared import Pt

import build_elda_data_sheet as cds

SOURCE = "./2er-command-week.md"
OUTPUT_DOCX = "./output/2er-command-week-nzalc-support.docx"
TITLE = "NZALC Support to 2 ER Command Week"
KICKER = None
TAG = None
REFERENCE = None
FOOTER_LEFT = "NZALC | 2 ER Command Week 2026"


def build():
    cds.DATE = "17 September 2026"
    cds.ORIGINATOR_LONG = "New Zealand Army Leadership Centre"
    doc = cds.new_document()
    doc.styles["Normal"].font.size = Pt(10)
    cds.add_header_footer(doc.sections[0], FOOTER_LEFT)
    cds.add_title_block(KICKER, TITLE, TAG, reference=REFERENCE, status=None, date_only=True)
    with open(SOURCE, encoding="utf-8") as fh:
        cds.render_markdown(fh.read().splitlines())
    # tighten to one page: drop the empty spacer after the table and the
    # blank gap paragraph under the title block
    for para in doc.paragraphs:
        if para.style is not None and para.style.name == cds.SECTION_HEADING_STYLE:
            para.paragraph_format.space_before = Pt(9)
            para.paragraph_format.space_after = Pt(4)
        elif para.text.strip() and para.paragraph_format.space_after is None:
            para.paragraph_format.space_after = Pt(4)
            para.paragraph_format.line_spacing = 1.1
        if not para.text.strip() and para.runs == []:
            para.paragraph_format.space_after = Pt(0)
            para.paragraph_format.space_before = Pt(0)
            para.paragraph_format.line_spacing = Pt(4)
    cds.finish(TITLE)
    doc.save(OUTPUT_DOCX)
    print(f"Saved {OUTPUT_DOCX}")


if __name__ == "__main__":
    build()
