#!/usr/bin/env python3
"""
Restyle the Lines of Effort tracker source workbook in the house design
language: split masthead (red brand block with the reversed logo, pale title
field), pale stat band, black header row, priority chips in black /
moawhango / pale, moawhango progress bars, grid-grey rules, red only for the
stale warnings.

    python3 restyle_loe_tracker.py            # rewrites assets/lines-of-effort-tracker.xlsx
    python3 build_loe_tracker.py              # then rebuilds the macro-enabled tracker

Data, formulas, validation, the table and the macros' expectations (cell
style indexes, dxf indexes, sheet structure) are all preserved: only the
look changes.  Safe to run more than once.
"""

import io
import re
import sys
import zipfile

from PIL import Image, ImageDraw

SRC = "assets/lines-of-effort-tracker.xlsx"
LOGO = "assets/nz-army-logo-white.png"

ARMY_RED, BLACK, WHITE = "FFC62026", "FF000000", "FFFFFFFF"
SWAMP, GOLD, MOAWHANGO = "FF002516", "FFA89662", "FFCDD2B7"
PALE, FAINT, GRID, MID, INK = "FFEEF1E5", "FFF6F6F3", "FFD9D9D2", "FF8A8A8A", "FF222222"

TITLE = "NZALC HQ Lines of Effort Tracker"
BLOCK_W_PT, BLOCK_H_PT = 96, 32          # the brand block, sized to sit in A2
EMU = 12700


def brand_block_png() -> bytes:
    """Red rounded block carrying the reversed logo, drawn at 4x for print."""
    s = 4
    w, h = BLOCK_W_PT * s, BLOCK_H_PT * s
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=6 * s, fill=(198, 32, 38, 255))
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.crop(logo.getchannel("A").getbbox())
    lh = int(h * 0.58)
    lw = int(lh * logo.width / logo.height)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    im.alpha_composite(logo, ((w - lw) // 2, (h - lh) // 2))
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue()


def restyle_styles(x: str) -> str:
    # fonts: title black on the pale field; labels swamp; big numbers black;
    # header white; body ink; completed lines mid grey
    fonts = [
        '<font><sz val="11"/><color theme="1"/><name val="Calibri"/><family val="2"/><charset val="1"/></font>',
        f'<font><b/><sz val="16"/><color rgb="{BLACK}"/><name val="Arial"/><family val="2"/></font>',
        f'<font><b/><sz val="7"/><color rgb="{SWAMP}"/><name val="Arial"/><family val="2"/></font>',
        f'<font><b/><sz val="22"/><color rgb="{BLACK}"/><name val="Arial"/><family val="2"/></font>',
        f'<font><b/><sz val="8.5"/><color rgb="{WHITE}"/><name val="Arial"/><family val="2"/></font>',
        f'<font><sz val="10"/><color rgb="{INK}"/><name val="Arial"/><family val="2"/></font>',
        f'<font><sz val="10"/><color rgb="{MID}"/><name val="Arial"/><family val="2"/></font>',
        f'<font><sz val="10"/><color rgb="{INK}"/><name val="Arial"/><family val="2"/></font>',
        f'<font><sz val="10"/><color rgb="{INK}"/><name val="Arial"/><family val="2"/><charset val="1"/></font>',
    ]
    x = re.sub(r"<fonts [^>]*>.*?</fonts>",
               '<fonts count="9" x14ac:knownFonts="1">' + "".join(fonts) + "</fonts>", x, count=1, flags=re.S)
    # fills: 2 stays black (header row); 3 becomes the pale field
    x = re.sub(r"<fills count=\"4\">.*?</fills>",
               '<fills count="4"><fill><patternFill patternType="none"/></fill>'
               '<fill><patternFill patternType="gray125"/></fill>'
               f'<fill><patternFill patternType="solid"><fgColor rgb="{BLACK}"/><bgColor rgb="{INK}"/></patternFill></fill>'
               f'<fill><patternFill patternType="solid"><fgColor rgb="{FAINT}"/><bgColor rgb="{WHITE}"/></patternFill></fill></fills>',
               x, count=1, flags=re.S)
    # rules in grid grey
    x = x.replace('<color rgb="FFD9D9D9"/>', f'<color rgb="{GRID}"/>')
    # the title style (cellXfs 13) moves from the black fill to the pale field
    x = x.replace('<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment horizontal="left" vertical="center" indent="1"/></xf>',
                  '<xf numFmtId="0" fontId="1" fillId="3" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment horizontal="left" vertical="center" indent="1"/></xf>')
    # conditional formats: stale in Army red; priority chips black / moawhango / pale
    dxfs = [
        f'<dxf><font><b/><sz val="10"/><color rgb="{ARMY_RED}"/><name val="Arial"/><charset val="1"/></font></dxf>',
        f'<dxf><font><b/><sz val="22"/><color rgb="{ARMY_RED}"/><name val="Arial"/><charset val="1"/></font></dxf>',
        f'<dxf><font><b/><sz val="10"/><color rgb="{INK}"/><name val="Arial"/><charset val="1"/></font><fill><patternFill><bgColor rgb="{PALE}"/></patternFill></fill></dxf>',
        f'<dxf><font><b/><sz val="10"/><color rgb="{SWAMP}"/><name val="Arial"/><charset val="1"/></font><fill><patternFill><bgColor rgb="{MOAWHANGO}"/></patternFill></fill></dxf>',
        f'<dxf><font><b/><sz val="10"/><color rgb="{WHITE}"/><name val="Arial"/><charset val="1"/></font><fill><patternFill><bgColor rgb="{BLACK}"/></patternFill></fill></dxf>',
    ]
    x = re.sub(r"<dxfs count=\"5\">.*?</dxfs>", '<dxfs count="5">' + "".join(dxfs) + "</dxfs>", x, count=1, flags=re.S)
    return x


def restyle_sheet(x: str) -> str:
    # masthead: A2 holds the brand block image; the title field runs B2:G2
    x = x.replace('<row r="2" spans="1:7" ht="31.5" customHeight="1"', '<row r="2" spans="1:7" ht="40" customHeight="1"', 1)
    x = x.replace('<mergeCell ref="A2:G2"/>', '<mergeCell ref="B2:G2"/>', 1)
    x = re.sub(r'<c r="A2" s="13" t="s"><v>(\d+)</v></c><c r="B2" s="13"/>',
               r'<c r="A2" s="13"/><c r="B2" s="13" t="s"><v>\1</v></c>', x, count=1)
    # priority column a little wider for the chips and the block
    x = re.sub(r'<col min="1" max="1" width="[\d.]+" customWidth="1"/>',
               '<col min="1" max="1" width="18.5" customWidth="1"/>', x, count=1)
    # progress bars in moawhango: quiet, the same tone as the Reinforces chip
    x = re.sub(r'(<dataBar>.*?<color rgb=")[0-9A-F]{8}(")', rf'\g<1>{MOAWHANGO}\2', x, flags=re.S)
    x = re.sub(r'(<x14:negativeFillColor rgb=")[0-9A-F]{8}(")', rf'\g<1>{MOAWHANGO}\2', x)
    # the drawing, placed where the schema wants it
    if "<drawing " not in x:
        x = x.replace("</headerFooter>", '</headerFooter><drawing r:id="rIdDrawing"/>', 1)
    return x


def drawing_xml() -> str:
    cx, cy = BLOCK_W_PT * EMU, BLOCK_H_PT * EMU
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<xdr:oneCellAnchor><xdr:from><xdr:col>0</xdr:col><xdr:colOff>0</xdr:colOff>'
        f'<xdr:row>1</xdr:row><xdr:rowOff>{4 * EMU}</xdr:rowOff></xdr:from>'
        f'<xdr:ext cx="{cx}" cy="{cy}"/>'
        '<xdr:pic><xdr:nvPicPr><xdr:cNvPr id="2" name="NZ Army"/><xdr:cNvPicPr><a:picLocks noChangeAspect="1"/></xdr:cNvPicPr></xdr:nvPicPr>'
        '<xdr:blipFill><a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rId1"/>'
        '<a:stretch><a:fillRect/></a:stretch></xdr:blipFill>'
        f'<xdr:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></xdr:spPr>'
        '</xdr:pic><xdr:clientData/></xdr:oneCellAnchor></xdr:wsDr>'
    )


def restyle(path: str) -> None:
    with zipfile.ZipFile(path) as zin:
        parts = {i.filename: zin.read(i.filename) for i in zin.infolist()}
        order = [i.filename for i in zin.infolist()]

    parts["xl/styles.xml"] = restyle_styles(parts["xl/styles.xml"].decode("utf-8")).encode("utf-8")
    parts["xl/worksheets/sheet1.xml"] = restyle_sheet(parts["xl/worksheets/sheet1.xml"].decode("utf-8")).encode("utf-8")

    sst = parts["xl/sharedStrings.xml"].decode("utf-8")
    sst = re.sub(r"<si><t>NZALC HQ - LINES OF EFFORT TRACKER</t></si>", f"<si><t>{TITLE}</t></si>", sst, count=1)
    parts["xl/sharedStrings.xml"] = sst.encode("utf-8")

    rels = parts["xl/worksheets/_rels/sheet1.xml.rels"].decode("utf-8")
    if "rIdDrawing" not in rels:
        rels = rels.replace("</Relationships>",
                            '<Relationship Id="rIdDrawing" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing" '
                            'Target="../drawings/drawing1.xml"/></Relationships>')
    parts["xl/worksheets/_rels/sheet1.xml.rels"] = rels.encode("utf-8")

    parts["xl/drawings/drawing1.xml"] = drawing_xml().encode("utf-8")
    parts["xl/drawings/_rels/drawing1.xml.rels"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
        'Target="../media/image1.png"/></Relationships>').encode("utf-8")
    parts["xl/media/image1.png"] = brand_block_png()
    for name in ("xl/drawings/drawing1.xml", "xl/drawings/_rels/drawing1.xml.rels", "xl/media/image1.png"):
        if name not in order:
            order.insert(order.index("xl/worksheets/sheet1.xml") + 1, name)

    types = parts["[Content_Types].xml"].decode("utf-8")
    if 'Extension="png"' not in types:
        types = types.replace('<Default Extension="rels"', '<Default Extension="png" ContentType="image/png"/><Default Extension="rels"', 1)
    if "drawing1.xml" not in types:
        types = types.replace("</Types>",
                              '<Override PartName="/xl/drawings/drawing1.xml" '
                              'ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/></Types>')
    parts["[Content_Types].xml"] = types.encode("utf-8")

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in order:
            zout.writestr(name, parts[name])
    print(f"restyled {path}")


if __name__ == "__main__":
    restyle(sys.argv[1] if len(sys.argv) > 1 else SRC)
