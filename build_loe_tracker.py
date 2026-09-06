#!/usr/bin/env python3
"""Build the macro-enabled Lines of Effort tracker.

Reads assets/lines-of-effort-tracker.xlsx and writes
output/lines-of-effort-tracker.xlsm.  The output is the same workbook with:

* the tblLoE rows pre-sorted Critical -> Important -> Routine,
* a "Complete" tick-box column on the right of the table,
* an Archive tab (table tblArchive) that completed lines move to, and
* a VBA project that keeps the table grouped by priority whenever a
  Priority cell changes, moves a line to the Archive tab when its tick
  box is clicked (and back again when the tick is clicked on the Archive
  tab), and stamps today's date when a Last Updated cell is double-clicked.

Excel stores VBA as an OLE compound file (xl/vbaProject.bin) laid out per
[MS-OVBA].  No library on the build box writes that format, so this script
contains a minimal writer for the two binary formats involved:
[MS-CFB] (the OLE container) and [MS-OVBA] (the VBA project streams and
their RLE/LZ77 compression).  Everything else in the workbook is copied
byte-for-byte from the source file.

Usage:  python3 build_loe_tracker.py [source.xlsx] [output.xlsm]
"""
from __future__ import annotations

import re
import struct
import sys
import zipfile
from dataclasses import dataclass, field

SRC = "assets/lines-of-effort-tracker.xlsx"
DST = "output/lines-of-effort-tracker.xlsm"

TABLE_NAME = "tblLoE"
FIRST_DATA_ROW = 8
PRIORITY_ORDER = ["Critical", "Important", "Routine"]

# Fixed so rebuilding the file gives identical output.  The protection
# fields in the PROJECT stream are encrypted against this ID (see
# _project_encrypt), so it must stay in step with them.
PROJECT_ID = "{7C4A1E2B-9D53-4F1A-8B6E-2A5C0F3D9E71}"
ENCRYPTION_SEED = 0x5A

# --------------------------------------------------------------------------
# VBA source.  Document modules (ThisWorkbook / Sheet1) are bound to the
# workbook via the codeName attributes patched into the XML further down.
# --------------------------------------------------------------------------

VBA_THISWORKBOOK = '''\
Attribute VB_Name = "ThisWorkbook"
Attribute VB_Base = "0{00020819-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
Option Explicit

' Tidy the tracker on open, in case it was edited somewhere macros do not
' run (for example Excel on iPad or iPhone).
Private Sub Workbook_Open()
    FillTickBoxes
    EnsureGroupedByPriority
End Sub
'''

VBA_SHEET1 = '''\
Attribute VB_Name = "Sheet1"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
Option Explicit

' The active Lines of Effort table on this sheet.
Private Function Tracker() As ListObject
    On Error Resume Next
    Set Tracker = Me.ListObjects("tblLoE")
    On Error GoTo 0
End Function

' Fires after any cell on this sheet changes.  Keeps every active line
' showing a tick box and, when a Priority cell changed, re-groups the
' table by priority.
Private Sub Worksheet_Change(ByVal Target As Range)
    Dim lo As ListObject

    Set lo = Tracker()
    If lo Is Nothing Then Exit Sub
    If lo.DataBodyRange Is Nothing Then Exit Sub
    If Intersect(Target, lo.DataBodyRange) Is Nothing Then Exit Sub

    FillTickBoxes
    If Not Intersect(Target, lo.ListColumns("Priority").DataBodyRange) Is Nothing Then
        EnsureGroupedByPriority
    End If
End Sub

' A single click on a line's tick box marks it complete and moves it to
' the Archive tab.
Private Sub Worksheet_SelectionChange(ByVal Target As Range)
    Dim lo As ListObject

    Set lo = Tracker()
    If Not IsInColumn(lo, "Complete", Target) Then Exit Sub

    ArchiveLine ListRowIndex(lo, Target)
    SelectLineCell Me, Target.Row
End Sub

' Double-clicking a Last Updated cell stamps today's date into it.
Private Sub Worksheet_BeforeDoubleClick(ByVal Target As Range, Cancel As Boolean)
    If IsInColumn(Tracker(), "Last Updated", Target) Then
        StampToday Target
        Cancel = True
    End If
End Sub
'''

VBA_SHEET2 = '''\
Attribute VB_Name = "Sheet2"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
Option Explicit

' The archive table on this sheet.
Private Function Archive() As ListObject
    On Error Resume Next
    Set Archive = Me.ListObjects("tblArchive")
    On Error GoTo 0
End Function

' A single click on an archived line's tick box sends it back to the
' active tracker, where it is slotted into its priority group.
Private Sub Worksheet_SelectionChange(ByVal Target As Range)
    Dim lo As ListObject

    Set lo = Archive()
    If Not IsInColumn(lo, "Complete", Target) Then Exit Sub

    RestoreLine ListRowIndex(lo, Target)
    SelectLineCell Me, Target.Row
End Sub
'''

VBA_MODULE = '''\
Attribute VB_Name = "modLoE"
Option Explicit

' Order in which priorities are grouped, top to bottom.
Private Const PRIORITY_ORDER As String = "Critical,Important,Routine"

' Rows are never shrunk below this height after a sort or move (the
' tables' standard row height).
Private Const MIN_ROW_HEIGHT As Double = 30

' Column headers the code relies on.
Private Const COL_PRIORITY As String = "Priority"
Private Const COL_LINE As String = "Line of Effort"
Private Const COL_COMPLETE As String = "Complete"
Private Const COL_COMPLETED_ON As String = "Completed"

Private mBusy As Boolean

' ---------------------------------------------------------------------
' Tables and tick-box glyphs
' ---------------------------------------------------------------------

' Returns the active Lines of Effort table, or Nothing if it cannot be found.
Private Function LoETable() As ListObject
    On Error Resume Next
    Set LoETable = Sheet1.ListObjects("tblLoE")
    On Error GoTo 0
End Function

' Returns the archive table, or Nothing if it cannot be found.
Private Function ArchiveTable() As ListObject
    On Error Resume Next
    Set ArchiveTable = Sheet2.ListObjects("tblArchive")
    On Error GoTo 0
End Function

' Empty tick box (Unicode ballot box).
Public Function TickEmpty() As String
    TickEmpty = ChrW(&H2610)
End Function

' Ticked box (Unicode ballot box with check).
Public Function TickDone() As String
    TickDone = ChrW(&H2611)
End Function

' ---------------------------------------------------------------------
' Helpers shared by the sheet event handlers
' ---------------------------------------------------------------------

' True when cell is one cell inside the named column of the table's body.
Public Function IsInColumn(ByVal lo As ListObject, ByVal colName As String, _
                           ByVal cell As Range) As Boolean
    IsInColumn = False
    If lo Is Nothing Then Exit Function
    If lo.DataBodyRange Is Nothing Then Exit Function
    If cell.Cells.CountLarge <> 1 Then Exit Function
    IsInColumn = Not Intersect(cell, lo.ListColumns(colName).DataBodyRange) Is Nothing
End Function

' 1-based index of the table row that cell sits in (0 if outside the body).
Public Function ListRowIndex(ByVal lo As ListObject, ByVal cell As Range) As Long
    ListRowIndex = 0
    If lo Is Nothing Then Exit Function
    If lo.DataBodyRange Is Nothing Then Exit Function
    If Intersect(cell, lo.DataBodyRange) Is Nothing Then Exit Function
    ListRowIndex = cell.Row - lo.DataBodyRange.Row + 1
End Function

' Moves the selection to the Line of Effort cell of the given sheet row,
' so keyboard navigation does not land on a tick box and fire it again.
Public Sub SelectLineCell(ByVal ws As Worksheet, ByVal sheetRow As Long)
    Dim lo As ListObject
    Dim eventsWereOn As Boolean

    Set lo = ws.ListObjects(1)
    eventsWereOn = Application.EnableEvents
    Application.EnableEvents = False
    On Error Resume Next
    ws.Cells(sheetRow, lo.ListColumns(COL_LINE).Range.Column).Select
    On Error GoTo 0
    Application.EnableEvents = eventsWereOn
End Sub

' Writes today's date into a cell without triggering other handlers.
Public Sub StampToday(ByVal cell As Range)
    Dim eventsWereOn As Boolean

    eventsWereOn = Application.EnableEvents
    Application.EnableEvents = False
    cell.Value = Date
    Application.EnableEvents = eventsWereOn
End Sub

' ---------------------------------------------------------------------
' Priority grouping
' ---------------------------------------------------------------------

' Re-groups the active table only when a row is out of priority order.
Public Sub EnsureGroupedByPriority()
    If Not IsGroupedByPriority() Then SortLinesOfEffort
End Sub

' Sorts the active table Critical, Important, Routine.  Rows with the
' same priority keep their existing relative order.  Can also be run by
' hand from Alt+F8.
Public Sub SortLinesOfEffort()
    Dim lo As ListObject
    Dim eventsWereOn As Boolean

    Set lo = LoETable()
    If lo Is Nothing Then Exit Sub
    If lo.DataBodyRange Is Nothing Then Exit Sub
    If mBusy Then Exit Sub

    mBusy = True
    eventsWereOn = Application.EnableEvents
    Application.EnableEvents = False
    Application.ScreenUpdating = False
    On Error GoTo CleanUp

    With lo.Sort
        .SortFields.Clear
        .SortFields.Add Key:=lo.ListColumns(COL_PRIORITY).DataBodyRange, _
            SortOn:=xlSortOnValues, Order:=xlAscending, _
            CustomOrder:=PRIORITY_ORDER, DataOption:=xlSortNormal
        .Header = xlYes
        .MatchCase = False
        .Orientation = xlTopToBottom
        .Apply
    End With

    FixRowHeights lo

CleanUp:
    Application.ScreenUpdating = True
    Application.EnableEvents = eventsWereOn
    mBusy = False
End Sub

' True when the Priority column is already in Critical / Important /
' Routine order (blank or unrecognised values count as last).
Public Function IsGroupedByPriority() As Boolean
    Dim lo As ListObject
    Dim cell As Range
    Dim lastRank As Long
    Dim thisRank As Long

    IsGroupedByPriority = True
    Set lo = LoETable()
    If lo Is Nothing Then Exit Function
    If lo.DataBodyRange Is Nothing Then Exit Function

    lastRank = 0
    For Each cell In lo.ListColumns(COL_PRIORITY).DataBodyRange.Cells
        thisRank = PriorityRank(cell.Value)
        If thisRank < lastRank Then
            IsGroupedByPriority = False
            Exit Function
        End If
        lastRank = thisRank
    Next cell
End Function

' 1 = Critical, 2 = Important, 3 = Routine, 4 = anything else.
Private Function PriorityRank(ByVal priority As Variant) As Long
    Dim parts() As String
    Dim i As Long

    parts = Split(PRIORITY_ORDER, ",")
    PriorityRank = UBound(parts) + 2
    If IsError(priority) Then Exit Function

    For i = LBound(parts) To UBound(parts)
        If StrComp(Trim$(CStr(priority)), parts(i), vbTextCompare) = 0 Then
            PriorityRank = i + 1
            Exit Function
        End If
    Next i
End Function

' ---------------------------------------------------------------------
' Tick boxes, archiving and restoring
' ---------------------------------------------------------------------

' Puts an empty tick box in the Complete column of every active line
' that has a Line of Effort but no box yet.
Public Sub FillTickBoxes()
    Dim lo As ListObject
    Dim r As ListRow
    Dim box As Range
    Dim eventsWereOn As Boolean

    Set lo = LoETable()
    If lo Is Nothing Then Exit Sub
    If lo.DataBodyRange Is Nothing Then Exit Sub

    eventsWereOn = Application.EnableEvents
    Application.EnableEvents = False
    On Error GoTo CleanUp

    For Each r In lo.ListRows
        Set box = r.Range.Cells(1, lo.ListColumns(COL_COMPLETE).Index)
        If LineIsBlank(lo, r) Then
            If box.Value = TickEmpty() Then box.ClearContents
        ElseIf Len(CStr(box.Value)) = 0 Then
            box.Value = TickEmpty()
        End If
    Next r

CleanUp:
    Application.EnableEvents = eventsWereOn
End Sub

' Marks the given active line complete and moves it to the Archive tab.
Public Sub ArchiveLine(ByVal rowIndex As Long)
    Dim src As ListObject
    Dim dst As ListObject
    Dim srcRow As ListRow
    Dim dstRow As ListRow
    Dim eventsWereOn As Boolean

    Set src = LoETable()
    Set dst = ArchiveTable()
    If src Is Nothing Or dst Is Nothing Then Exit Sub
    If rowIndex < 1 Or rowIndex > src.ListRows.Count Then Exit Sub
    If mBusy Then Exit Sub

    Set srcRow = src.ListRows(rowIndex)
    If LineIsBlank(src, srcRow) Then Exit Sub

    mBusy = True
    eventsWereOn = Application.EnableEvents
    Application.EnableEvents = False
    Application.ScreenUpdating = False
    On Error GoTo CleanUp

    Set dstRow = NextFreeRow(dst)
    CopyLine src, srcRow, dst, dstRow
    dstRow.Range.Cells(1, dst.ListColumns(COL_COMPLETE).Index).Value = TickDone()
    dstRow.Range.Cells(1, dst.ListColumns(COL_COMPLETED_ON).Index).Value = Date
    DeleteLine src, srcRow
    FixRowHeights dst

CleanUp:
    Application.ScreenUpdating = True
    Application.EnableEvents = eventsWereOn
    mBusy = False
End Sub

' Sends an archived line back to the active tracker and re-groups it.
Public Sub RestoreLine(ByVal rowIndex As Long)
    Dim src As ListObject
    Dim dst As ListObject
    Dim srcRow As ListRow
    Dim dstRow As ListRow
    Dim eventsWereOn As Boolean

    Set src = ArchiveTable()
    Set dst = LoETable()
    If src Is Nothing Or dst Is Nothing Then Exit Sub
    If rowIndex < 1 Or rowIndex > src.ListRows.Count Then Exit Sub
    If mBusy Then Exit Sub

    Set srcRow = src.ListRows(rowIndex)
    If LineIsBlank(src, srcRow) Then Exit Sub

    mBusy = True
    eventsWereOn = Application.EnableEvents
    Application.EnableEvents = False
    Application.ScreenUpdating = False
    On Error GoTo CleanUp

    Set dstRow = NextFreeRow(dst)
    CopyLine src, srcRow, dst, dstRow
    dstRow.Range.Cells(1, dst.ListColumns(COL_COMPLETE).Index).Value = TickEmpty()
    DeleteLine src, srcRow
    mBusy = False
    SortLinesOfEffort

CleanUp:
    Application.ScreenUpdating = True
    Application.EnableEvents = eventsWereOn
    mBusy = False
End Sub

' Copies every column the two tables share, matched by header name.
Private Sub CopyLine(ByVal src As ListObject, ByVal srcRow As ListRow, _
                     ByVal dst As ListObject, ByVal dstRow As ListRow)
    Dim col As ListColumn
    Dim dstCol As ListColumn

    For Each col In src.ListColumns
        Set dstCol = Nothing
        On Error Resume Next
        Set dstCol = dst.ListColumns(col.Name)
        On Error GoTo 0
        If Not dstCol Is Nothing Then
            If col.Name <> COL_COMPLETE And col.Name <> COL_COMPLETED_ON Then
                dstRow.Range.Cells(1, dstCol.Index).Value = srcRow.Range.Cells(1, col.Index).Value
            End If
        End If
    Next col
End Sub

' The table's last row if it is blank, otherwise a newly added row.
Private Function NextFreeRow(ByVal lo As ListObject) As ListRow
    If lo.ListRows.Count > 0 Then
        If LineIsBlank(lo, lo.ListRows(lo.ListRows.Count)) Then
            Set NextFreeRow = lo.ListRows(lo.ListRows.Count)
            Exit Function
        End If
    End If
    Set NextFreeRow = lo.ListRows.Add
End Function

' Deletes a row, or clears it when it is the only row (a table keeps one).
Private Sub DeleteLine(ByVal lo As ListObject, ByVal r As ListRow)
    If lo.ListRows.Count > 1 Then
        r.Delete
    Else
        r.Range.ClearContents
    End If
End Sub

' True when the row has nothing in its Line of Effort cell.
Private Function LineIsBlank(ByVal lo As ListObject, ByVal r As ListRow) As Boolean
    Dim v As Variant
    v = r.Range.Cells(1, lo.ListColumns(COL_LINE).Index).Value
    If IsError(v) Then
        LineIsBlank = False
    Else
        LineIsBlank = (Len(Trim$(CStr(v))) = 0)
    End If
End Function

' Excel's sort moves cell contents but not row heights, so re-fit the rows
' and keep them at least the standard height.
Private Sub FixRowHeights(ByVal lo As ListObject)
    Dim r As Range

    If lo.DataBodyRange Is Nothing Then Exit Sub
    lo.DataBodyRange.Rows.AutoFit
    For Each r In lo.DataBodyRange.Rows
        If r.RowHeight < MIN_ROW_HEIGHT Then r.RowHeight = MIN_ROW_HEIGHT
    Next r
End Sub
'''

MODULE_TYPE_STANDARD = 0x21
MODULE_TYPE_DOCUMENT = 0x22

# (module name, source, module type)
MODULES = [
    ("ThisWorkbook", VBA_THISWORKBOOK, MODULE_TYPE_DOCUMENT),
    ("Sheet1", VBA_SHEET1, MODULE_TYPE_DOCUMENT),
    ("Sheet2", VBA_SHEET2, MODULE_TYPE_DOCUMENT),
    ("modLoE", VBA_MODULE, MODULE_TYPE_STANDARD),
]


# --------------------------------------------------------------------------
# [MS-OVBA] 2.4.1  Compression
# --------------------------------------------------------------------------

def _compress_chunk(chunk: bytes) -> bytes:
    """Token stream for one decompressed chunk of at most 4096 bytes."""
    out = bytearray()
    pos = 0
    n = len(chunk)
    while pos < n:
        flag_index = len(out)
        out.append(0)
        flags = 0
        for bit in range(8):
            if pos >= n:
                break
            best_len = 0
            best_off = 0
            bit_count = max(4, (pos - 1).bit_length()) if pos > 0 else 4
            if pos > 0:
                max_len = (0xFFFF >> bit_count) + 3
                max_off = min(pos, 1 << bit_count)
                for off in range(1, max_off + 1):
                    length = 0
                    while (length < max_len and pos + length < n
                           and chunk[pos + length - off] == chunk[pos + length]):
                        length += 1
                    if length > best_len:
                        best_len, best_off = length, off
            if best_len >= 3:
                token = ((best_off - 1) << (16 - bit_count)) | (best_len - 3)
                out += struct.pack("<H", token)
                flags |= 1 << bit
                pos += best_len
            else:
                out.append(chunk[pos])
                pos += 1
        out[flag_index] = flags
    return bytes(out)


def ovba_compress(data: bytes) -> bytes:
    """Compress a stream as a CompressedContainer (signature byte + chunks)."""
    out = bytearray(b"\x01")
    for start in range(0, len(data), 4096):
        chunk = data[start:start + 4096]
        tokens = _compress_chunk(chunk)
        if len(tokens) <= 4096:
            header = 0xB000 | (len(tokens) + 2 - 3)   # compressed, sig 0b011
            out += struct.pack("<H", header) + tokens
        else:                                       # store raw, padded
            out += struct.pack("<H", 0x3FFF) + chunk.ljust(4096, b"\x00")
    return bytes(out)


def ovba_decompress(data: bytes) -> bytes:
    """Reference decompressor, used to self-check the compressor."""
    if data[:1] != b"\x01":
        raise ValueError("bad container signature")
    out = bytearray()
    i = 1
    while i < len(data):
        header = struct.unpack_from("<H", data, i)[0]
        i += 2
        end = i + (header & 0x0FFF) + 3 - 2
        chunk_start = len(out)
        if not header & 0x8000:
            out += data[i:i + 4096]
            i += 4096
            continue
        while i < end:
            flags = data[i]
            i += 1
            for bit in range(8):
                if i >= end:
                    break
                if flags & (1 << bit):
                    token = struct.unpack_from("<H", data, i)[0]
                    i += 2
                    diff = len(out) - chunk_start
                    bit_count = max(4, (diff - 1).bit_length())
                    length = (token & (0xFFFF >> bit_count)) + 3
                    offset = (token >> (16 - bit_count)) + 1
                    for _ in range(length):
                        out.append(out[-offset])
                else:
                    out.append(data[i])
                    i += 1
    return bytes(out)


# --------------------------------------------------------------------------
# [MS-OVBA] 2.3  Project streams
# --------------------------------------------------------------------------

def _rec(rec_id: int, payload: bytes) -> bytes:
    return struct.pack("<HI", rec_id, len(payload)) + payload


def _rec_text(rec_id: int, text: str, unicode_id: int) -> bytes:
    """A MBCS record followed by its Unicode twin record."""
    return (_rec(rec_id, text.encode("cp1252"))
            + _rec(unicode_id, text.encode("utf-16-le")))


def build_dir_stream() -> bytes:
    """Decompressed 'dir' stream: project info, references, modules."""
    out = bytearray()
    # PROJECTINFORMATION
    out += _rec(0x0001, struct.pack("<I", 3))          # SysKind: 64-bit Windows
    out += _rec(0x0002, struct.pack("<I", 0x0409))     # LCID
    out += _rec(0x0014, struct.pack("<I", 0x0409))     # LCIDINVOKE
    out += _rec(0x0003, struct.pack("<H", 1252))       # CodePage
    out += _rec(0x0004, b"VBAProject")                 # Name
    out += _rec(0x0005, b"") + _rec(0x0040, b"")       # DocString (+unicode)
    out += _rec(0x0006, b"") + _rec(0x003D, b"")       # HelpFilePath 1 & 2
    out += _rec(0x0007, struct.pack("<I", 0))          # HelpContext
    out += _rec(0x0008, struct.pack("<I", 0))          # LibFlags
    out += struct.pack("<HIIH", 0x0009, 4, 1, 0)       # Version (major 1, minor 0)
    out += _rec(0x000C, b"") + _rec(0x003C, b"")       # Constants (+unicode)
    # PROJECTREFERENCES: none.  The VBA and Excel libraries are implicit.
    # PROJECTMODULES
    out += _rec(0x000F, struct.pack("<H", len(MODULES)))
    out += _rec(0x0013, struct.pack("<H", 0xFFFF))     # Cookie
    for name, _source, module_type in MODULES:
        out += _rec_text(0x0019, name, 0x0047)         # MODULENAME (+unicode)
        out += _rec_text(0x001A, name, 0x0032)         # MODULESTREAMNAME (+unicode)
        out += _rec(0x001C, b"") + _rec(0x0048, b"")   # MODULEDOCSTRING (+unicode)
        out += _rec(0x0031, struct.pack("<I", 0))      # MODULEOFFSET: no perf cache
        out += _rec(0x001E, struct.pack("<I", 0))      # MODULEHELPCONTEXT
        out += _rec(0x002C, struct.pack("<H", 0xFFFF)) # MODULECOOKIE
        out += struct.pack("<HI", module_type, 0)      # MODULETYPE
        out += struct.pack("<HI", 0x002B, 0)           # module terminator
    out += struct.pack("<HI", 0x0010, 0)               # dir terminator
    return bytes(out)


def _project_encrypt(data: bytes, seed: int) -> str:
    """[MS-OVBA] 2.4.3.2 Data Encryption, keyed on PROJECT_ID."""
    project_key = 0
    for b in PROJECT_ID.encode("ascii"):
        project_key ^= b
    version_enc = seed ^ 2
    proj_key_enc = seed ^ project_key
    ignored_length = (seed & 6) >> 1

    out = bytearray([seed, version_enc, proj_key_enc])
    state = {"unenc1": project_key, "enc1": proj_key_enc, "enc2": version_enc}

    def step(value: int) -> None:
        enc = value ^ ((state["enc2"] + state["unenc1"]) & 0xFF)
        out.append(enc)
        state["enc2"] = state["enc1"]
        state["enc1"] = enc
        state["unenc1"] = value

    for _ in range(ignored_length):
        step(0)
    for b in struct.pack("<I", len(data)):
        step(b)
    for b in data:
        step(b)
    return out.hex().upper()


def _project_decrypt(hex_text: str) -> bytes:
    """Inverse of _project_encrypt, used for self-checking."""
    raw = bytes.fromhex(hex_text)
    seed, version_enc, proj_key_enc = raw[:3]
    project_key = seed ^ proj_key_enc
    if seed ^ version_enc != 2:
        raise ValueError("bad version")
    ignored_length = (seed & 6) >> 1
    unenc1, enc1, enc2 = project_key, proj_key_enc, version_enc
    plain = bytearray()
    for enc in raw[3:]:
        value = enc ^ ((enc2 + unenc1) & 0xFF)
        plain.append(value)
        enc2, enc1, unenc1 = enc1, enc, value
    plain = plain[ignored_length:]
    length = struct.unpack("<I", plain[:4])[0]
    return bytes(plain[4:4 + length])


def build_project_stream() -> bytes:
    lines = [f'ID="{PROJECT_ID}"']
    for name, _source, module_type in MODULES:
        if module_type == MODULE_TYPE_DOCUMENT:
            lines.append(f"Document={name}/&H00000000")
        else:
            lines.append(f"Module={name}")
    lines += [
        'Name="VBAProject"',
        'HelpContextID="0"',
        'VersionCompatible32="393222000"',
        # Unprotected, no password, project visible.
        'CMG="' + _project_encrypt(b"\x00\x00\x00\x00", ENCRYPTION_SEED) + '"',
        'DPB="' + _project_encrypt(b"\x00", ENCRYPTION_SEED) + '"',
        'GC="' + _project_encrypt(b"\xff", ENCRYPTION_SEED) + '"',
        "",
        "[Host Extender Info]",
        "&H00000001={3832D640-CF90-11CF-8E43-00A0C911005A};VBE;&H00000000",
        "",
        "[Workspace]",
    ]
    lines += [f"{name}=0, 0, 0, 0, C" for name, _s, _t in MODULES]
    return ("\r\n".join(lines) + "\r\n").encode("cp1252")


def build_projectwm_stream() -> bytes:
    out = bytearray()
    for name, _source, _type in MODULES:
        out += name.encode("cp1252") + b"\x00" + name.encode("utf-16-le") + b"\x00\x00"
    out += b"\x00\x00"
    return bytes(out)


def build_vba_project_bin() -> bytes:
    """Assemble every VBA stream and wrap it in an OLE compound file."""
    vba_storage = CfbStorage("VBA")
    vba_storage.add_stream("_VBA_PROJECT", b"\xCC\x61\xFF\xFF\x00\x00\x00")
    vba_storage.add_stream("dir", ovba_compress(build_dir_stream()))
    for name, source, _type in MODULES:
        code = source.replace("\n", "\r\n").encode("cp1252")
        vba_storage.add_stream(name, ovba_compress(code))

    root = CfbStorage("Root Entry")
    root.children.append(vba_storage)
    root.add_stream("PROJECT", build_project_stream())
    root.add_stream("PROJECTwm", build_projectwm_stream())
    return write_cfb(root)


# --------------------------------------------------------------------------
# [MS-CFB]  Minimal compound file writer (version 3, 512-byte sectors)
# --------------------------------------------------------------------------

SECTOR = 512
MINI_SECTOR = 64
MINI_CUTOFF = 4096
ENDOFCHAIN = 0xFFFFFFFE
FREESECT = 0xFFFFFFFF
FATSECT = 0xFFFFFFFD
NOSTREAM = 0xFFFFFFFF


@dataclass
class CfbNode:
    name: str
    data: bytes | None = None                     # None for storages
    children: list["CfbNode"] = field(default_factory=list)
    sid: int = -1
    left: int = NOSTREAM
    right: int = NOSTREAM
    child: int = NOSTREAM
    start: int = ENDOFCHAIN
    size: int = 0

    @property
    def is_stream(self) -> bool:
        return self.data is not None


class CfbStorage(CfbNode):
    def add_stream(self, name: str, data: bytes) -> None:
        self.children.append(CfbNode(name, data))


def _sort_key(node: CfbNode):
    # [MS-CFB] 2.6.4: shorter names first, then case-insensitive compare.
    return (len(node.name), node.name.upper())


def _build_tree(nodes: list[CfbNode]) -> int:
    """Arrange siblings into a balanced binary search tree; return root sid."""
    if not nodes:
        return NOSTREAM
    nodes = sorted(nodes, key=_sort_key)
    mid = len(nodes) // 2
    nodes[mid].left = _build_tree(nodes[:mid])
    nodes[mid].right = _build_tree(nodes[mid + 1:])
    return nodes[mid].sid


def _pack_dir_entry(node: CfbNode | None) -> bytes:
    if node is None:
        return (b"\x00" * 64 + struct.pack("<HBB", 0, 0, 0)
                + struct.pack("<III", NOSTREAM, NOSTREAM, NOSTREAM)
                + b"\x00" * 16 + struct.pack("<IQQIQ", 0, 0, 0, 0, 0))
    name = node.name.encode("utf-16-le") + b"\x00\x00"
    if node.sid == 0:
        obj_type = 5
    elif node.is_stream:
        obj_type = 2
    else:
        obj_type = 1
    return (name.ljust(64, b"\x00")
            + struct.pack("<HBB", len(name), obj_type, 1)          # 1 = black
            + struct.pack("<III", node.left, node.right, node.child)
            + b"\x00" * 16                                           # CLSID
            + struct.pack("<IQQ", 0, 0, 0)                           # state, times
            + struct.pack("<IQ", node.start, node.size))


def write_cfb(root: CfbStorage) -> bytes:
    # Assign stream ids depth-first with the root as sid 0.
    nodes: list[CfbNode] = []

    def visit(node: CfbNode) -> None:
        node.sid = len(nodes)
        nodes.append(node)
        for child in node.children:
            visit(child)

    visit(root)
    for node in nodes:
        if not node.is_stream:
            node.child = _build_tree(node.children)

    streams = [n for n in nodes if n.is_stream]
    small = [n for n in streams if len(n.data) < MINI_CUTOFF]
    large = [n for n in streams if len(n.data) >= MINI_CUTOFF]

    # Mini stream: every small stream, each padded to a 64-byte mini sector.
    mini = bytearray()
    mini_fat: list[int] = []
    for node in small:
        node.size = len(node.data)
        node.start = len(mini_fat)
        count = -(-len(node.data) // MINI_SECTOR)
        mini_fat += list(range(node.start + 1, node.start + count)) + [ENDOFCHAIN]
        mini += node.data.ljust(count * MINI_SECTOR, b"\x00")

    def sectors_for(n_bytes: int) -> int:
        return -(-n_bytes // SECTOR)

    n_dir_entries = -(-len(nodes) // 4) * 4
    n_dir = sectors_for(n_dir_entries * 128)
    n_minifat = sectors_for(len(mini_fat) * 4) if mini_fat else 0
    n_mini = sectors_for(len(mini))
    n_large = [sectors_for(len(n.data)) for n in large]

    n_fat = 1
    while n_fat + n_dir + n_minifat + n_mini + sum(n_large) > n_fat * (SECTOR // 4):
        n_fat += 1
    if n_fat > 109:
        raise ValueError("compound file too large for header DIFAT")

    fat = [FREESECT] * (n_fat * (SECTOR // 4))
    next_sector = 0

    def allocate(count: int, mark: int | None = None) -> int:
        nonlocal next_sector
        first = next_sector
        for i in range(count):
            s = first + i
            if mark is not None:
                fat[s] = mark
            else:
                fat[s] = s + 1 if i < count - 1 else ENDOFCHAIN
        next_sector += count
        return first

    fat_first = allocate(n_fat, FATSECT)
    dir_first = allocate(n_dir)
    minifat_first = allocate(n_minifat) if n_minifat else ENDOFCHAIN
    mini_first = allocate(n_mini) if n_mini else ENDOFCHAIN
    for node, count in zip(large, n_large):
        node.size = len(node.data)
        node.start = allocate(count)

    root.start = mini_first
    root.size = len(mini)

    header = bytearray()
    header += b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"
    header += b"\x00" * 16                            # CLSID
    header += struct.pack("<HHHHH", 0x003E, 0x0003, 0xFFFE, 9, 6)
    header += b"\x00" * 6                             # reserved
    header += struct.pack("<IIII", 0, n_fat, dir_first, 0)
    header += struct.pack("<IIII", MINI_CUTOFF, minifat_first, n_minifat, ENDOFCHAIN)
    header += struct.pack("<I", 0)                    # DIFAT sector count
    difat = [fat_first + i for i in range(n_fat)]
    difat += [FREESECT] * (109 - len(difat))
    header += struct.pack("<109I", *difat)
    assert len(header) == SECTOR

    body = bytearray()
    body += struct.pack(f"<{len(fat)}I", *fat)
    dir_entries = [_pack_dir_entry(n) for n in nodes]
    dir_entries += [_pack_dir_entry(None)] * (n_dir_entries - len(nodes))
    body += b"".join(dir_entries).ljust(n_dir * SECTOR, b"\x00")
    if n_minifat:
        mf = mini_fat + [FREESECT] * (n_minifat * (SECTOR // 4) - len(mini_fat))
        body += struct.pack(f"<{len(mf)}I", *mf)
    body += bytes(mini).ljust(n_mini * SECTOR, b"\x00")
    for node, count in zip(large, n_large):
        body += node.data.ljust(count * SECTOR, b"\x00")
    assert len(body) == next_sector * SECTOR
    return bytes(header + body)


# --------------------------------------------------------------------------
# Workbook package patching
# --------------------------------------------------------------------------

def shared_strings(xml: str) -> list[str]:
    items = re.findall(r"<si>(.*?)</si>", xml, re.S)
    return ["".join(re.findall(r"<t[^>]*>(.*?)</t>", item, re.S)) for item in items]


def sort_table_rows(sheet_xml: str, strings: list[str], first_row: int, last_row: int) -> str:
    """Reorder rows first_row..last_row by priority (stable), renumbering refs."""
    row_re = re.compile(r'<row r="(\d+)"[^>]*?(?:/>|>.*?</row>)', re.S)
    rows = [(int(m.group(1)), m) for m in row_re.finditer(sheet_xml)]
    table_rows = [(r, m) for r, m in rows if first_row <= r <= last_row]
    if not table_rows:
        raise ValueError("no table rows found")

    def rank(row_xml: str) -> int:
        m = re.search(r'<c r="A\d+"[^>]*t="s"[^>]*><v>(\d+)</v></c>', row_xml)
        value = strings[int(m.group(1))].strip() if m else ""
        return PRIORITY_ORDER.index(value) if value in PRIORITY_ORDER else len(PRIORITY_ORDER)

    ordered = sorted(table_rows, key=lambda rm: rank(rm[1].group(0)))  # stable
    new_rows = []
    for new_number, (_old, m) in zip(range(first_row, last_row + 1), ordered):
        xml = m.group(0)
        xml = re.sub(r'^<row r="\d+"', f'<row r="{new_number}"', xml)
        xml = re.sub(r'<c r="([A-Z]+)\d+"', lambda c: f'<c r="{c.group(1)}{new_number}"', xml)
        new_rows.append(xml)

    start = table_rows[0][1].start()
    end = table_rows[-1][1].end()
    return sheet_xml[:start] + "".join(new_rows) + sheet_xml[end:]


SHEET_NS = ('xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
X14_NS = 'xmlns:x14="http://schemas.microsoft.com/office/spreadsheetml/2009/9/main"'
ARCHIVE_HEADER_ROW = 6
ARCHIVE_DATABAR_ID = "{5B2E7D31-8C4A-4F0E-9A17-3D6C2B1E8F42}"

# Column header -> (header style, data style) as used by the source sheet.
HEADER_LEFT, HEADER_CENTRE = 3, 4
STYLE_PRIORITY, STYLE_TEXT, STYLE_PERCENT, STYLE_DATE = 5, 6, 7, 8
STYLE_TITLE, STYLE_BAND, STYLE_BAND_VALUE = 13, 14, 15
STYLE_TICK = 16   # appended to styles.xml by add_tick_style()


def add_tick_style(styles_xml: str) -> str:
    """Append a centred 14pt cell style for the tick boxes (cellXfs index 16)."""
    fonts = re.search(r'<fonts count="(\d+)"', styles_xml)
    n_fonts = int(fonts.group(1))
    styles_xml = styles_xml.replace(fonts.group(0), f'<fonts count="{n_fonts + 1}"', 1)
    styles_xml = styles_xml.replace(
        "</fonts>",
        '<font><sz val="14"/><color rgb="FF222222"/><name val="Arial"/><family val="2"/></font></fonts>', 1)

    xfs = re.search(r'<cellXfs count="(\d+)"', styles_xml)
    assert int(xfs.group(1)) == STYLE_TICK, "unexpected cellXfs count"
    styles_xml = styles_xml.replace(xfs.group(0), f'<cellXfs count="{STYLE_TICK + 1}"', 1)
    styles_xml = styles_xml.replace(
        "</cellXfs>",
        f'<xf numFmtId="0" fontId="{n_fonts}" fillId="0" borderId="1" xfId="0" '
        'applyFont="1" applyBorder="1" applyAlignment="1">'
        '<alignment horizontal="center" vertical="center"/></xf></cellXfs>', 1)
    return styles_xml


def add_shared_strings(sst_xml: str, texts: list[str]) -> tuple[str, dict[str, int]]:
    """Append texts to the shared string table; return their indexes."""
    existing = shared_strings(sst_xml)
    indexes = {}
    new = []
    for text in texts:
        if text in existing:
            indexes[text] = existing.index(text)
        else:
            indexes[text] = len(existing) + len(new)
            new.append(text)
    m = re.search(r'<sst [^>]*count="(\d+)" uniqueCount="(\d+)"', sst_xml)
    count, unique = int(m.group(1)), int(m.group(2))
    sst_xml = sst_xml.replace(m.group(0), m.group(0)
                              .replace(f'count="{count}"', f'count="{count + len(new)}"')
                              .replace(f'uniqueCount="{unique}"', f'uniqueCount="{unique + len(new)}"'), 1)
    sst_xml = sst_xml.replace("</sst>", "".join(f"<si><t>{t}</t></si>" for t in new) + "</sst>")
    return sst_xml, indexes


def cell(ref: str, style: int, shared: int | None = None) -> str:
    if shared is None:
        return f'<c r="{ref}" s="{style}"/>'
    return f'<c r="{ref}" s="{style}" t="s"><v>{shared}</v></c>'


def add_complete_column(sheet_xml: str, ss: dict[str, int], last_row: int) -> str:
    """Add column H (Complete) to the main sheet: header, tick boxes, widths."""
    sheet_xml = sheet_xml.replace('<dimension ref="A1:G31"/>', f'<dimension ref="A1:H{last_row}"/>', 1)
    sheet_xml = sheet_xml.replace(
        "</cols>", '<col min="8" max="8" width="11.5" customWidth="1"/></cols>', 1)
    sheet_xml = sheet_xml.replace('spans="1:7"', 'spans="1:8"')
    sheet_xml = sheet_xml.replace('<mergeCell ref="A2:G2"/>', '<mergeCell ref="A2:H2"/>', 1)

    extras = {2: cell("H2", STYLE_TITLE), 4: cell("H4", STYLE_BAND), 5: cell("H5", STYLE_BAND_VALUE),
              7: cell("H7", HEADER_CENTRE, ss["Complete"])}
    for r in range(FIRST_DATA_ROW, last_row + 1):
        extras[r] = cell(f"H{r}", STYLE_TICK, ss[TICK_EMPTY])

    def append_cell(m: re.Match) -> str:
        row_number = int(m.group(1))
        if row_number not in extras or not m.group(0).endswith("</row>"):
            return m.group(0)
        return m.group(0)[:-len("</row>")] + extras[row_number] + "</row>"

    sheet_xml, n = re.subn(r'<row r="(\d+)"[^>]*?(?:/>|>.*?</row>)', append_cell, sheet_xml, flags=re.S)
    assert n >= last_row, "rows not found"

    # Prompt on Last Updated cells so the double-click shortcut is discoverable.
    sheet_xml = sheet_xml.replace('<dataValidations count="2">', '<dataValidations count="3">', 1)
    sheet_xml = sheet_xml.replace(
        "</dataValidations>",
        '<dataValidation type="none" allowBlank="1" showInputMessage="1" '
        'promptTitle="Last Updated" prompt="Double-click to stamp today\'s date." '
        'sqref="G8:G38"/></dataValidations>', 1)
    return sheet_xml


def widen_table(table_xml: str, last_row: int) -> str:
    """Extend tblLoE from A:G to A:H with a Complete column."""
    table_xml = table_xml.replace(f'ref="A7:G{last_row}"', f'ref="A7:H{last_row}"')
    table_xml = table_xml.replace('<tableColumns count="7">', '<tableColumns count="8">', 1)
    table_xml = table_xml.replace(
        "</tableColumns>", '<tableColumn id="8" name="Complete"/></tableColumns>', 1)
    return table_xml


def build_archive_sheet(ss: dict[str, int], source_sheet_xml: str) -> str:
    """The Archive tab: title, hint band, and an empty tblArchive."""
    cols = "".join(re.findall(r'<col [^>]*/>', source_sheet_xml))
    cols += '<col min="8" max="8" width="11.5" customWidth="1"/>'
    cols += '<col min="9" max="9" width="13.98828125" customWidth="1"/>'
    header = ARCHIVE_HEADER_ROW
    data = header + 1
    columns = "ABCDEFGHI"

    headers = [("Priority", HEADER_LEFT), ("Line of Effort", HEADER_LEFT),
               ("End State / Output", HEADER_LEFT), ("Progress %", HEADER_CENTRE),
               ("Next Action", HEADER_LEFT), ("Notes", HEADER_LEFT),
               ("Last Updated", HEADER_CENTRE), ("Complete", HEADER_CENTRE),
               ("Completed", HEADER_CENTRE)]
    data_styles = [STYLE_PRIORITY, STYLE_TEXT, STYLE_TEXT, STYLE_PERCENT, STYLE_TEXT,
                   STYLE_TEXT, STYLE_DATE, STYLE_TICK, STYLE_DATE]

    rows = [
        '<row r="1" spans="1:9" ht="6" customHeight="1"/>',
        '<row r="2" spans="1:9" ht="31.5" customHeight="1">'
        + cell("A2", STYLE_TITLE, ss[ARCHIVE_TITLE])
        + "".join(cell(f"{c}2", STYLE_TITLE) for c in columns[1:]) + "</row>",
        '<row r="3" spans="1:9" ht="6" customHeight="1"/>',
        '<row r="4" spans="1:9" ht="15" customHeight="1">'
        + cell("A4", STYLE_BAND, ss[ARCHIVE_HINT])
        + "".join(cell(f"{c}4", STYLE_BAND) for c in columns[1:]) + "</row>",
        '<row r="5" spans="1:9" ht="6" customHeight="1"/>',
        f'<row r="{header}" spans="1:9" ht="24" customHeight="1">'
        + "".join(cell(f"{c}{header}", style, ss[name]) for c, (name, style) in zip(columns, headers))
        + "</row>",
        f'<row r="{data}" spans="1:9" ht="30" customHeight="1">'
        + "".join(cell(f"{c}{data}", style) for c, style in zip(columns, data_styles)) + "</row>",
    ]

    page = re.search(r"<pageMargins .*?</headerFooter>", source_sheet_xml, re.S).group(0)
    page = re.sub(r' r:id="[^"]*"', "", page)

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<worksheet {SHEET_NS}>'
        '<sheetPr codeName="Sheet2"><pageSetUpPr fitToPage="1"/></sheetPr>'
        f'<dimension ref="A1:I{data}"/>'
        '<sheetViews><sheetView showGridLines="0" zoomScaleNormal="100" workbookViewId="0">'
        f'<pane ySplit="{header}" topLeftCell="A{data}" activePane="bottomLeft" state="frozen"/>'
        f'<selection pane="bottomLeft" activeCell="B{data}" sqref="B{data}"/>'
        '</sheetView></sheetViews>'
        '<sheetFormatPr defaultColWidth="8.609375" defaultRowHeight="15"/>'
        f'<cols>{cols}</cols>'
        f'<sheetData>{"".join(rows)}</sheetData>'
        '<mergeCells count="2"><mergeCell ref="A2:I2"/><mergeCell ref="A4:I4"/></mergeCells>'
        f'<conditionalFormatting sqref="A{data}:A200">'
        '<cfRule type="expression" dxfId="4" priority="1"><formula>$A7="Critical"</formula></cfRule>'
        '<cfRule type="expression" dxfId="3" priority="2"><formula>$A7="Important"</formula></cfRule>'
        '<cfRule type="expression" dxfId="2" priority="3"><formula>$A7="Routine"</formula></cfRule>'
        '</conditionalFormatting>'
        f'<conditionalFormatting sqref="D{data}:D200"><cfRule type="dataBar" priority="4">'
        '<dataBar><cfvo type="num" val="0"/><cfvo type="num" val="1"/><color rgb="FF9DBE85"/></dataBar>'
        f'<extLst><ext uri="{{B025F937-C7B1-47D3-B67F-A62EFF666E3E}}" {X14_NS}>'
        f'<x14:id>{ARCHIVE_DATABAR_ID}</x14:id></ext></extLst></cfRule></conditionalFormatting>'
        + page +
        '<tableParts count="1"><tablePart r:id="rId1"/></tableParts>'
        f'<extLst><ext uri="{{78C0D931-6437-407d-A8EE-F0AAD7539E65}}" {X14_NS}>'
        '<x14:conditionalFormattings>'
        '<x14:conditionalFormatting xmlns:xm="http://schemas.microsoft.com/office/excel/2006/main">'
        f'<x14:cfRule type="dataBar" id="{ARCHIVE_DATABAR_ID}">'
        '<x14:dataBar minLength="0" maxLength="100" gradient="0" axisPosition="none">'
        '<x14:cfvo type="num"><xm:f>0</xm:f></x14:cfvo><x14:cfvo type="num"><xm:f>1</xm:f></x14:cfvo>'
        '<x14:negativeFillColor rgb="FF9DBE85"/></x14:dataBar></x14:cfRule>'
        f'<xm:sqref>D{data}:D200</xm:sqref></x14:conditionalFormatting>'
        '</x14:conditionalFormattings></ext></extLst>'
        '</worksheet>'
    )


def build_archive_table() -> str:
    names = ["Priority", "Line of Effort", "End State / Output", "Progress %", "Next Action",
             "Notes", "Last Updated", "Complete", "Completed"]
    ref = f"A{ARCHIVE_HEADER_ROW}:I{ARCHIVE_HEADER_ROW + 1}"
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<table xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        f'id="2" name="tblArchive" displayName="tblArchive" ref="{ref}" totalsRowShown="0">'
        f'<autoFilter ref="{ref}"/>'
        f'<tableColumns count="{len(names)}">'
        + "".join(f'<tableColumn id="{i + 1}" name="{n}"/>' for i, n in enumerate(names))
        + '</tableColumns>'
        '<tableStyleInfo showFirstColumn="0" showLastColumn="0" showRowStripes="1" showColumnStripes="0"/>'
        '</table>'
    )


TICK_EMPTY = "☐"
ARCHIVE_TITLE = "NZALC HQ - ARCHIVED LINES OF EFFORT"
ARCHIVE_HINT = ("COMPLETED LINES LAND HERE AUTOMATICALLY - CLICK A LINE'S TICK BOX "
                "TO SEND IT BACK TO THE ACTIVE TRACKER")


def build(src: str, dst: str) -> None:
    vba_bin = build_vba_project_bin()

    with zipfile.ZipFile(src) as zin:
        parts = {info.filename: zin.read(info.filename) for info in zin.infolist()}
        order = [info.filename for info in zin.infolist()]

    table_xml = parts["xl/tables/table1.xml"].decode("utf-8")
    ref = re.search(r'<table [^>]*\bref="([A-Z]+)(\d+):([A-Z]+)(\d+)"', table_xml)
    header_row, last_row = int(ref.group(2)), int(ref.group(4))
    assert header_row + 1 == FIRST_DATA_ROW, "table header row moved"
    assert f'name="{TABLE_NAME}"' in table_xml and ref.group(3) == "G"
    parts["xl/tables/table1.xml"] = widen_table(table_xml, last_row).encode("utf-8")

    sst_xml, ss = add_shared_strings(
        parts["xl/sharedStrings.xml"].decode("utf-8"),
        ["Complete", "Completed", TICK_EMPTY, ARCHIVE_TITLE, ARCHIVE_HINT, "Priority",
         "Line of Effort", "End State / Output", "Progress %", "Next Action", "Notes",
         "Last Updated"])
    parts["xl/sharedStrings.xml"] = sst_xml.encode("utf-8")
    strings = shared_strings(sst_xml)

    parts["xl/styles.xml"] = add_tick_style(parts["xl/styles.xml"].decode("utf-8")).encode("utf-8")

    sheet = parts["xl/worksheets/sheet1.xml"].decode("utf-8")
    sheet = sort_table_rows(sheet, strings, FIRST_DATA_ROW, last_row)
    sheet, n = re.subn(r"<sheetPr>", '<sheetPr codeName="Sheet1">', sheet, count=1)
    assert n == 1, "sheetPr not found"
    sheet = add_complete_column(sheet, ss, last_row)
    parts["xl/worksheets/sheet1.xml"] = sheet.encode("utf-8")

    parts["xl/worksheets/sheet2.xml"] = build_archive_sheet(ss, sheet).encode("utf-8")
    parts["xl/worksheets/_rels/sheet2.xml.rels"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/table" '
        'Target="../tables/table2.xml"/></Relationships>').encode("utf-8")
    parts["xl/tables/table2.xml"] = build_archive_table().encode("utf-8")

    workbook = parts["xl/workbook.xml"].decode("utf-8")
    workbook, n = re.subn(r"<workbookPr/>", '<workbookPr codeName="ThisWorkbook"/>', workbook, count=1)
    assert n == 1, "workbookPr not found"
    workbook = workbook.replace("</sheets>", '<sheet name="Archive" sheetId="2" r:id="rIdArchive"/></sheets>', 1)
    workbook = workbook.replace("'Lines of Effort Tracker'!$A$1:$G$38", "'Lines of Effort Tracker'!$A$1:$H$38", 1)
    parts["xl/workbook.xml"] = workbook.encode("utf-8")

    rels = parts["xl/_rels/workbook.xml.rels"].decode("utf-8")
    rels = rels.replace(
        "</Relationships>",
        '<Relationship Id="rIdArchive" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        'Target="worksheets/sheet2.xml"/>'
        '<Relationship Id="rIdVBA" '
        'Type="http://schemas.microsoft.com/office/2006/relationships/vbaProject" '
        'Target="vbaProject.bin"/></Relationships>')
    parts["xl/_rels/workbook.xml.rels"] = rels.encode("utf-8")

    types = parts["[Content_Types].xml"].decode("utf-8")
    types, n = re.subn(
        r'(<Override PartName="/xl/workbook.xml" ContentType=")[^"]+(")',
        r"\1application/vnd.ms-excel.sheet.macroEnabled.main+xml\2", types, count=1)
    assert n == 1, "workbook content type not found"
    types = types.replace(
        "</Types>",
        '<Override PartName="/xl/worksheets/sheet2.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '<Override PartName="/xl/tables/table2.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml"/>'
        '<Override PartName="/xl/vbaProject.bin" '
        'ContentType="application/vnd.ms-office.vbaProject"/></Types>')
    parts["[Content_Types].xml"] = types.encode("utf-8")

    parts["xl/vbaProject.bin"] = vba_bin
    order.insert(order.index("xl/workbook.xml") + 1, "xl/vbaProject.bin")
    at = order.index("xl/worksheets/sheet1.xml") + 1
    order[at:at] = ["xl/worksheets/sheet2.xml"]
    order.insert(order.index("xl/worksheets/_rels/sheet1.xml.rels") + 1, "xl/worksheets/_rels/sheet2.xml.rels")
    order.insert(order.index("xl/tables/table1.xml") + 1, "xl/tables/table2.xml")

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in order:
            zout.writestr(name, parts[name])


def self_check() -> None:
    for _name, source, _type in MODULES:
        code = source.replace("\n", "\r\n").encode("cp1252")
        assert ovba_decompress(ovba_compress(code)) == code, "compression round trip"
    assert ovba_decompress(ovba_compress(build_dir_stream())) == build_dir_stream()
    for payload in (b"\x00\x00\x00\x00", b"\x00", b"\xff"):
        assert _project_decrypt(_project_encrypt(payload, ENCRYPTION_SEED)) == payload


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else SRC
    dst = sys.argv[2] if len(sys.argv) > 2 else DST
    self_check()
    build(src, dst)
    print(f"wrote {dst}")
