#!/usr/bin/env python3
"""
NZALC HQ Co-ord action-item register in the shared house style.

    python3 build_nzalc_hq_coord_actions.py
    /usr/bin/python3 convert_to_pdf.py output/nzalc-hq-coord-action-items.docx \
        output/nzalc-hq-coord-action-items.pdf
"""

from docx.shared import Cm

import build_elda_data_sheet as cds

SOURCE = "./nzalc-hq-coord-action-items.md"
OUTPUT_DOCX = "./output/nzalc-hq-coord-action-items.docx"
TITLE = "Action Items"
KICKER = "NZALC HQ Co-ord"
TAG = None
REFERENCE = "NZALC HQ Co-ord meeting, September 2026"
STATUS = None
FOOTER_LEFT = "NZALC | HQ Co-ord Action Items"
COLUMN_WIDTHS_CM = (3.2, 10.6, 2.6)


def build():
    doc = cds.new_document()
    cds.add_header_footer(doc.sections[0], FOOTER_LEFT)
    cds.add_title_block(KICKER, TITLE, TAG, reference=REFERENCE, status=STATUS)
    with open(SOURCE, encoding="utf-8") as fh:
        cds.render_markdown(fh.read().splitlines())
    # widen the action column: owner | action | by
    for table in doc.tables:
        if len(table.columns) != len(COLUMN_WIDTHS_CM):
            continue
        for col, width in zip(table.columns, COLUMN_WIDTHS_CM):
            col.width = Cm(width)
            for cell in col.cells:
                cell.width = Cm(width)
        # keep the header row with the first body row
        for cell in table.rows[0].cells:
            for para in cell.paragraphs:
                para.paragraph_format.keep_with_next = True
    cds.finish(TITLE)
    doc.save(OUTPUT_DOCX)
    print(f"Saved {OUTPUT_DOCX}")


if __name__ == "__main__":
    build()
