#!/usr/bin/env python3
"""
2 ER Command Week initiating one-pager as an editable Word document in the
shared house style.  The PDF is drawn separately by build_2er_command_week.py.

    python3 build_2er_command_week_docx.py
"""

import build_elda_data_sheet as cds

SOURCE = "./2er-command-week.md"
OUTPUT_DOCX = "./output/2er-command-week-nzalc-support.docx"
TITLE = "2 ER Command Off-site"
KICKER = None
TAG = None
REFERENCE = None
FOOTER_LEFT = "NZALC | 2 ER Command Off-site"


def build():
    doc = cds.new_document()
    cds.add_header_footer(doc.sections[0], FOOTER_LEFT)
    cds.add_title_block(KICKER, TITLE, TAG, reference=REFERENCE, status=None, date_only=True)
    with open(SOURCE, encoding="utf-8") as fh:
        cds.render_markdown(fh.read().splitlines())
    # tighten to one page: drop the empty spacer after the table and the
    # blank gap paragraph under the title block
    from docx.shared import Pt
    for para in doc.paragraphs:
        if not para.text.strip() and para.runs == []:
            para.paragraph_format.space_after = Pt(0)
            para.paragraph_format.space_before = Pt(0)
            para.paragraph_format.line_spacing = Pt(4)
    cds.finish(TITLE)
    doc.save(OUTPUT_DOCX)
    print(f"Saved {OUTPUT_DOCX}")


if __name__ == "__main__":
    build()
