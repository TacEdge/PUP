#!/usr/bin/env python3
"""
Direction to ELDA Wing on physical preparedness: a one-page direction in
the shared house style.

    python3 build_elda_direction.py
    python3 convert_to_pdf.py output/elda-physical-preparedness-direction.docx \\
                              output/elda-physical-preparedness-direction.pdf
"""

import build_elda_data_sheet as cds

SOURCE = "./elda-physical-preparedness-direction.md"
OUTPUT_DOCX = "./output/elda-physical-preparedness-direction.docx"
TITLE = "Physical Preparedness"
KICKER = "Direction to ELDA Wing"
TAG = "COMDT ACS direction of 10 September 2026 applied to ELDA delivery"
REFERENCE = "COMDT ACS discussion, 10 September 2026"
STATUS = "For action"
FOOTER_LEFT = "NZALC | Direction to ELDA Wing"


def build():
    doc = cds.new_document()
    cds.add_header_footer(doc.sections[0], FOOTER_LEFT)
    cds.add_title_block(KICKER, TITLE, TAG, reference=REFERENCE, status=STATUS)
    with open(SOURCE, encoding="utf-8") as fh:
        cds.render_markdown(fh.read().splitlines())
    cds.finish(TITLE)
    doc.save(OUTPUT_DOCX)
    print(f"Saved {OUTPUT_DOCX}")


if __name__ == "__main__":
    build()
