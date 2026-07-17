#!/usr/bin/env python3
"""
Convert the built .docx to PDF via LibreOffice UNO, updating all fields and
the table of contents first, and re-saving the .docx with fields resolved.

Run with the system python (which has the 'uno' module):
    /usr/bin/python3 convert_to_pdf.py output/capability-note.docx output/capability-note.pdf
"""

import os
import subprocess
import sys
import time

import uno
from com.sun.star.beans import PropertyValue


def prop(name, value):
    p = PropertyValue()
    p.Name = name
    p.Value = value
    return p


def main():
    docx_path = os.path.abspath(sys.argv[1])
    pdf_path = os.path.abspath(sys.argv[2])

    soffice = subprocess.Popen([
        "soffice", "--headless", "--invisible", "--norestore", "--nologo",
        "--accept=socket,host=127.0.0.1,port=2002;urp;",
    ])
    try:
        local_ctx = uno.getComponentContext()
        resolver = local_ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_ctx)
        ctx = None
        for _ in range(60):
            try:
                ctx = resolver.resolve(
                    "uno:socket,host=127.0.0.1,port=2002;urp;"
                    "StarOffice.ComponentContext")
                break
            except Exception:
                time.sleep(1)
        if ctx is None:
            raise RuntimeError("could not connect to LibreOffice")

        desktop = ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", ctx)
        doc = desktop.loadComponentFromURL(
            uno.systemPathToFileUrl(docx_path), "_blank", 0,
            (prop("Hidden", True),))

        # Update fields and indexes; repeat so pagination settles after the
        # TOC changes page flow.
        for _ in range(3):
            try:
                doc.getTextFields().refresh()
            except Exception:
                pass
            doc.refresh()
            indexes = doc.getDocumentIndexes()
            for i in range(indexes.getCount()):
                indexes.getByIndex(i).update()

        # Re-save the docx with fields/TOC resolved, then export the PDF.
        doc.storeToURL(uno.systemPathToFileUrl(docx_path),
                       (prop("FilterName", "MS Word 2007 XML"),
                        prop("Overwrite", True)))
        doc.storeToURL(uno.systemPathToFileUrl(pdf_path),
                       (prop("FilterName", "writer_pdf_Export"),
                        prop("Overwrite", True)))
        doc.close(False)
        print(f"Wrote {pdf_path}")
    finally:
        soffice.terminate()
        try:
            soffice.wait(timeout=15)
        except subprocess.TimeoutExpired:
            soffice.kill()


if __name__ == "__main__":
    main()
