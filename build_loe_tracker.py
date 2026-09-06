#!/usr/bin/env python3
"""Build the macro-enabled Lines of Effort tracker.

Reads assets/lines-of-effort-tracker.xlsx and writes
output/lines-of-effort-tracker.xlsm.  The output is the same workbook with:

* the tblLoE rows pre-sorted Critical -> Important -> Routine, and
* a VBA project whose Worksheet_Change handler re-sorts the table every
  time a Priority cell changes, so rows always stay grouped by priority.

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

' Tidy the table on open, in case it was edited somewhere macros do not
' run (for example Excel on iPad or iPhone).
Private Sub Workbook_Open()
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

' Fires after any cell on this sheet changes.  When the change touches the
' Priority column of tblLoE the table is re-grouped by priority.
Private Sub Worksheet_Change(ByVal Target As Range)
    Dim lo As ListObject

    On Error Resume Next
    Set lo = Me.ListObjects("tblLoE")
    On Error GoTo 0
    If lo Is Nothing Then Exit Sub
    If lo.DataBodyRange Is Nothing Then Exit Sub

    If Intersect(Target, lo.ListColumns("Priority").DataBodyRange) Is Nothing Then Exit Sub

    EnsureGroupedByPriority
End Sub
'''

VBA_MODULE = '''\
Attribute VB_Name = "modLoE"
Option Explicit

' Order in which priorities are grouped, top to bottom.
Private Const PRIORITY_ORDER As String = "Critical,Important,Routine"

' Rows are never shrunk below this height after a sort (the table's
' standard row height).
Private Const MIN_ROW_HEIGHT As Double = 30

Private mSorting As Boolean

' Returns the Lines of Effort table, or Nothing if it cannot be found.
Private Function LoETable() As ListObject
    On Error Resume Next
    Set LoETable = Sheet1.ListObjects("tblLoE")
    On Error GoTo 0
End Function

' Re-groups the table only when a row is out of priority order.
Public Sub EnsureGroupedByPriority()
    If Not IsGroupedByPriority() Then SortLinesOfEffort
End Sub

' Sorts the table Critical, Important, Routine.  Rows with the same
' priority keep their existing relative order.  Can also be run by hand
' from Alt+F8.
Public Sub SortLinesOfEffort()
    Dim lo As ListObject
    Dim eventsWereOn As Boolean

    Set lo = LoETable()
    If lo Is Nothing Then Exit Sub
    If lo.DataBodyRange Is Nothing Then Exit Sub
    If mSorting Then Exit Sub

    mSorting = True
    eventsWereOn = Application.EnableEvents
    Application.EnableEvents = False
    Application.ScreenUpdating = False
    On Error GoTo CleanUp

    With lo.Sort
        .SortFields.Clear
        .SortFields.Add Key:=lo.ListColumns("Priority").DataBodyRange, _
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
    mSorting = False
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
    For Each cell In lo.ListColumns("Priority").DataBodyRange.Cells
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

' Excel's sort moves cell contents but not row heights, so re-fit the rows
' and keep them at least the table's standard height.
Private Sub FixRowHeights(ByVal lo As ListObject)
    Dim r As Range

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


def build(src: str, dst: str) -> None:
    vba_bin = build_vba_project_bin()

    with zipfile.ZipFile(src) as zin:
        parts = {info.filename: zin.read(info.filename) for info in zin.infolist()}
        order = [info.filename for info in zin.infolist()]

    table_xml = parts["xl/tables/table1.xml"].decode("utf-8")
    ref = re.search(r'<table [^>]*\bref="([A-Z]+)(\d+):([A-Z]+)(\d+)"', table_xml)
    header_row, last_row = int(ref.group(2)), int(ref.group(4))
    assert header_row + 1 == FIRST_DATA_ROW, "table header row moved"
    assert f'name="{TABLE_NAME}"' in table_xml

    strings = shared_strings(parts["xl/sharedStrings.xml"].decode("utf-8"))

    sheet = parts["xl/worksheets/sheet1.xml"].decode("utf-8")
    sheet = sort_table_rows(sheet, strings, FIRST_DATA_ROW, last_row)
    sheet, n = re.subn(r"<sheetPr>", '<sheetPr codeName="Sheet1">', sheet, count=1)
    assert n == 1, "sheetPr not found"
    parts["xl/worksheets/sheet1.xml"] = sheet.encode("utf-8")

    workbook = parts["xl/workbook.xml"].decode("utf-8")
    workbook, n = re.subn(r"<workbookPr/>", '<workbookPr codeName="ThisWorkbook"/>', workbook, count=1)
    assert n == 1, "workbookPr not found"
    parts["xl/workbook.xml"] = workbook.encode("utf-8")

    rels = parts["xl/_rels/workbook.xml.rels"].decode("utf-8")
    rels = rels.replace(
        "</Relationships>",
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
        '<Override PartName="/xl/vbaProject.bin" '
        'ContentType="application/vnd.ms-office.vbaProject"/></Types>')
    parts["[Content_Types].xml"] = types.encode("utf-8")

    parts["xl/vbaProject.bin"] = vba_bin
    order.insert(order.index("xl/workbook.xml") + 1, "xl/vbaProject.bin")

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
