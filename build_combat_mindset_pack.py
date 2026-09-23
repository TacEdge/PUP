#!/usr/bin/env python3
"""
Combat Mindset pack: the three products bound as one PDF with continuous
page numbering.

    python3 build_combat_mindset_pack.py
        -> output/combat-mindset-pack.pdf

  1  Cover
  2  Army Combat Mindset System (one-page system map)
  3  Combat Mindset Conditioning: the product in one picture

The staff document (build_cmc_staff_document.py) is kept as a standalone
design and development document and is not bound into the pack.
"""

import os
import tempfile

import pymupdf

import build_army_combat_mindset_development_system as acms
import build_cmc_one_pager as model
import build_combat_mindset_cover as cover

OUT = "./output/combat-mindset-pack.pdf"
ORDER = [cover, acms, model]


def build():
    tmp = tempfile.mkdtemp()
    # first pass: build each to learn its page count
    counts = []
    for i, mod in enumerate(ORDER):
        mod.OUT = os.path.join(tmp, f"part{i}.pdf")
        mod.PNG = os.path.join(tmp, f"part{i}.png")
        mod.build()
        counts.append(len(pymupdf.open(mod.OUT)))
    total = sum(counts)
    # second pass: rebuild with continuous numbering
    offset = 0
    for mod, n in zip(ORDER, counts):
        mod.PAGE_OFFSET = offset
        mod.PAGE_TOTAL = total
        mod.build()
        offset += n
    pack = pymupdf.open()
    for mod in ORDER:
        pack.insert_pdf(pymupdf.open(mod.OUT))
    pack.set_metadata({"title": "Army Combat Mindset System and Combat Mindset Conditioning",
                       "author": "Army Command School"})
    pack.save(OUT, garbage=3, deflate=True)
    print(f"Saved {OUT}: {total} pages ({', '.join(str(c) for c in counts)})")


if __name__ == "__main__":
    build()
