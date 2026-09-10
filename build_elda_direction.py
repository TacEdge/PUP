#!/usr/bin/env python3
"""
Direction to ELDA Wing on physical preparedness: a one-page direction in
the shared house style.

    python3 build_elda_direction.py
    The PDF is drawn separately by build_elda_direction_pdf.py so the
    bottom-line card can carry rounded corners.
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
    # the bottom-line card: no red edge, larger type, more padding
    from docx.oxml.ns import qn
    from docx.shared import Pt
    for para in doc.paragraphs:
        pPr = para._p.pPr
        if pPr is not None and pPr.find(qn("w:shd")) is not None:
            bdr = pPr.find(qn("w:pBdr"))
            if bdr is not None:
                pPr.remove(bdr)
            para.paragraph_format.space_before = Pt(14)
            para.paragraph_format.space_after = Pt(14)
            for run in para.runs:
                run.font.size = Pt(11.5)
    cds.finish(TITLE)
    doc.save(OUTPUT_DOCX)
    print(f"Saved {OUTPUT_DOCX}")


if __name__ == "__main__":
    build()
