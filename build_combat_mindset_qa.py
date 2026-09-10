#!/usr/bin/env python3
"""
Questions and Answers companion to the Combat Mindset Framework Proposal,
built from its markdown source in the shared house style.

    python3 build_combat_mindset_qa.py
    python3 convert_to_pdf.py output/combat-mindset-qa.docx output/combat-mindset-qa.pdf
"""

import build_elda_data_sheet as cds

SOURCE = "./combat-mindset-qa.md"
OUTPUT_DOCX = "./output/combat-mindset-qa.docx"
TITLE = "Combat Mindset Framework Proposal"
KICKER = "Questions and Answers"
TAG = "Preparation for the COMDT ACS discussion"
REFERENCE = "NZ Army Combat Mindset Framework Proposal, V1.0 (August 2026)"
STATUS = "Speaking notes: not for distribution"
FOOTER_LEFT = "NZALC | Combat Mindset Questions and Answers"


def build():
    doc = cds.new_document()
    cds.add_header_footer(doc.sections[0], FOOTER_LEFT)
    cds.add_title_block(KICKER, TITLE, TAG, reference=REFERENCE, status=STATUS)
    with open(SOURCE, encoding="utf-8") as fh:
        cds.render_markdown(fh.read().splitlines())
    # keep the reference table whole: section 5 starts a new page
    for para in doc.paragraphs:
        if para.text.strip().startswith("5. Facts to Have to Hand"):
            para.paragraph_format.page_break_before = True
    cds.finish(TITLE)
    doc.save(OUTPUT_DOCX)
    print(f"Saved {OUTPUT_DOCX}")


if __name__ == "__main__":
    build()
