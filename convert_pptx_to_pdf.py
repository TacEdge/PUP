#!/usr/bin/env python3
"""
Convert a .pptx to PDF via LibreOffice UNO (the plain CLI converter does not
load presentations in this environment).

    /usr/bin/python3 convert_pptx_to_pdf.py output/deck.pptx output/deck.pdf
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
    src = os.path.abspath(sys.argv[1])
    pdf = os.path.abspath(sys.argv[2])
    soffice = subprocess.Popen([
        "soffice", "--headless", "--invisible", "--norestore", "--nologo",
        "--accept=socket,host=127.0.0.1,port=2003;urp;",
    ])
    try:
        local_ctx = uno.getComponentContext()
        resolver = local_ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_ctx)
        ctx = None
        for _ in range(60):
            try:
                ctx = resolver.resolve("uno:socket,host=127.0.0.1,port=2003;urp;StarOffice.ComponentContext")
                break
            except Exception:
                time.sleep(1)
        if ctx is None:
            raise RuntimeError("could not connect to LibreOffice")
        desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(src), "_blank", 0, (prop("Hidden", True),))
        doc.storeToURL(uno.systemPathToFileUrl(pdf), (prop("FilterName", "impress_pdf_Export"),))
        doc.close(True)
        print(f"Wrote {pdf}")
    finally:
        try:
            desktop.terminate()
        except Exception:
            pass
        soffice.wait(timeout=30)


if __name__ == "__main__":
    main()
