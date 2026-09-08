#!/usr/bin/env python3
"""
Build the LDF Alignment Design Note (analysis, information architecture,
visual logic, data required, assumptions not made) from its markdown
source, in the shared house style.

    python3 build_ldf_design_note.py
    python3 convert_to_pdf.py output/ldf-alignment-design-note.docx \\
                              output/ldf-alignment-design-note.pdf
"""

import build_elda_data_sheet as cds

SOURCE = "./ldf-alignment-design-note.md"
OUTPUT_DOCX = "./output/ldf-alignment-design-note.docx"
TITLE = "Officer and Soldier Leadership Development"
KICKER = "Design Note"
TAG = "AITC discussion piece, two pages plus a detachable future state: design draft"
REFERENCE = ("NZDF Leadership Framework v2 (Oct 2025); LDS, Leadership Levels "
             "and Leadership Framework posters")
STATUS = "Design draft for approval"
FOOTER_LEFT = "NZALC | Leadership Development Design Note"


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
