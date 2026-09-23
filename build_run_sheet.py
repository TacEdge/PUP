#!/usr/bin/env python3
"""
Daily run sheet: one portrait page in the house style.  Intended outputs,
the programme with a tick box per line, and the end-of-day check.

    python3 build_run_sheet.py
        -> output/run-sheet-2026-09-24.pdf (+ .png preview)

Edit the content block below for another day.
"""

import pymupdf

from army_onepager import ARMY_RED, BLACK, FAINT, GOLD, GRID, INK, MID, PALE, SWAMP, WHITE, Page, rgb
from build_army_combat_mindset_development_system import reversed_logo_png, wrapped

DAY = "2026-09-24"
OUT = f"./output/run-sheet-{DAY}.pdf"
PNG = f"./output/run-sheet-{DAY}.png"
W, H = 595, 842
M = 40
CW = W - 2 * M
R = 6
GREY = rgb("5F5F5A")

TITLE = "Run Sheet"
SUBTITLE = "Thursday 24 September 2026"
FOOTER_LEFT = "NZALC | Run Sheet"

OUTPUTS = [
    ("AITC submission foundation", "Understand the required format, sketch the submission structure, and identify the material or decisions still needed."),
    ("Admin loose ends cleared", "Deal with priority forms, updates, emails and follow-ups."),
    ("Call Ollie", "Call Ollie at Moore Construction."),
]

# (time, activity, tasks and outcome, kind)  kind: work | admin | routine
PROGRAMME = [
    ("8:15 - 9:00", "Drive to work", "", "routine"),
    ("9:00 - 9:15", "Catch up with staff", "Check priorities and pick up anything requiring action today.", "admin"),
    ("9:15 - 10:00", "Admin and calls", "Sign INE forms; update the lines of operation and effort matrix; ask Jono or call the clothing store about the outstanding issue; clear priority emails; quick call to Ollie at Moore Construction.", "admin"),
    ("10:00 - 10:30", "Smoko", "", "routine"),
    ("10:30 - 12:00", "Work bout 1: Combat Mindset and AITC", "Review the AITC submission format and requirements. Set out a rough structure for the Combat Mindset submission and note any gaps or decisions needed to develop it.", "work"),
    ("12:00 - 12:30", "Lunch", "", "routine"),
    ("12:30 - 1:00", "Admin", "Follow up on the morning's calls and clear short tasks.", "admin"),
    ("1:00 - 2:30", "Work bout 2: to be confirmed", "Choose the focus based on the morning's AITC work and any staff priorities.", "work"),
    ("2:30 - 3:00", "Admin", "Close out remaining loose ends and record follow-ups.", "admin"),
    ("3:00 - 4:30", "Work bout 3: to be confirmed", "Use for the next substantive priority.", "work"),
    ("4:30 - 5:00", "Commute home", "", "routine"),
]

CHECK = "You have an AITC submission outline, a clear list of what it still needs, an outcome from the call with Ollie, and any unfinished admin captured for follow-up."


def masthead(pg):
    pg.text(W / 2, 20, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(W / 2, H - 22, "UNCLASSIFIED", 8, BLACK, bold=True, align=1)
    pg.text(M, H - 11, FOOTER_LEFT, 7.5, BLACK)
    pg.text(W / 2, H - 11, "ACS 2026", 7.5, BLACK, align=1)
    pg.text(W - M, H - 11, "Page 1 of 1", 7.5, BLACK, align=2)
    top, hh = 30, 46
    brand_w = 118
    pg.box(M, top, CW, hh, fill=FAINT, stroke=None, radius=R)
    pg.box(M, top, brand_w + R, hh, fill=ARMY_RED, stroke=None, radius=R)
    pg.box(M + brand_w, top, R + 1, hh, fill=FAINT, stroke=None)
    png, (iw, ih) = reversed_logo_png()
    lh = 24
    lw = lh * iw / ih
    pg.p.insert_image(pymupdf.Rect(M + (brand_w - lw) / 2, top + (hh - lh) / 2,
                                   M + (brand_w + lw) / 2, top + (hh + lh) / 2), stream=png)
    tx = M + brand_w + 16
    pg.text(tx, top + 24, TITLE, 16, BLACK, bold=True)
    pg.text(tx, top + 36, SUBTITLE, 8, INK)
    return top + hh


def heading(pg, y, num, label, desc):
    pg.text(M, y, num, 9, GOLD, bold=True)
    pg.spaced(M + 17, y, label, 7.6, SWAMP, bold=True, spacing=1.8)
    pg.text(M + 17, y + 10.5, desc, 7, GREY)
    return y + 26


def tick_box(pg, x, y, s=9):
    pg.box(x, y, s, s, fill=WHITE, stroke=MID, width=0.8, radius=2)


def build():
    doc = pymupdf.open()
    pg = Page(doc, W, H)
    y = masthead(pg) + 24

    # ---- 01 intended outputs: three cards, each with a tick box ----
    y = heading(pg, y, "01", "TODAY'S INTENDED OUTPUTS", "What the day is for.")
    gap = 10
    cw = (CW - 2 * gap) / 3
    size, lh = 7.4, 9.6
    prepared = [(t, wrapped(pg, d, size, cw - 22)) for t, d in OUTPUTS]
    ch = max(30 + len(l) * lh for _, l in prepared)
    for i, (title, lines) in enumerate(prepared):
        x = M + i * (cw + gap)
        pg.box(x, y, cw, ch, fill=FAINT, stroke=None, radius=R)
        pg.text(x + 10, y + 17, str(i + 1), 11, GOLD, bold=True)
        pg.text(x + 24, y + 17, title, 8.2, BLACK, bold=True)
        tick_box(pg, x + cw - 19, y + 9)
        ty = y + 31
        for line in lines:
            pg.text(x + 10, ty, line, size, INK)
            ty += lh
    y += ch + 22

    # ---- 02 programme: one row per block, work bouts carry a black spine ----
    y = heading(pg, y, "02", "PROGRAMME", "The day in blocks. Tick each line as it closes.")
    time_w, act_w, box_w = 66, 128, 22
    text_w = CW - time_w - act_w - box_w - 20
    size, lh = 7.6, 9.8
    for time, activity, tasks, kind in PROGRAMME:
        lines = wrapped(pg, tasks, size, text_w) if tasks else []
        act_lines = wrapped(pg, activity, 7.8, act_w - 10, bold=True)
        h = max(22, 10 + max(len(lines), len(act_lines)) * lh)
        if kind == "routine":
            pg.box(M, y, CW, h, fill=WHITE, stroke=GRID, width=0.6, radius=4)
            pg.text(M + 8, y + h / 2 + 2.6, time, 7.2, GREY)
            pg.text(M + time_w, y + h / 2 + 2.6, activity, 7.6, GREY)
        else:
            pg.box(M, y, CW, h, fill=FAINT, stroke=None, radius=4)
            if kind == "work":
                pg.box(M, y, 4 + R, h, fill=BLACK, stroke=None, radius=4)
                pg.box(M + 4, y, R + 1, h, fill=FAINT, stroke=None)
            pg.text(M + 8, y + 14, time, 7.2, GREY)
            ty = y + 14
            for line in act_lines:
                pg.text(M + time_w, ty, line, 7.8, BLACK, bold=True)
                ty += lh
            ty = y + 14
            for line in lines:
                pg.text(M + time_w + act_w, ty, line, size, INK)
                ty += lh
            tick_box(pg, M + CW - 17, y + 7)
        y += h + 4
    y += 14

    # ---- 03 end-of-day check: black band ----
    y = heading(pg, y, "03", "END-OF-DAY CHECK", "Done means all of this is true.")
    lines = wrapped(pg, CHECK, 8.4, CW - 90)
    h = 18 + len(lines) * 11
    pg.box(M, y, CW, h, fill=BLACK, stroke=None, radius=R)
    pg.text(M + 30, y + h / 2 + 3.5, "CHECK", 9.5, GOLD, bold=True, align=1)
    pg.line(M + 60, y + 8, M + 60, y + h - 8, GOLD, width=0.8)
    ty = y + 15
    for line in lines:
        pg.text(M + 72, ty, line, 8.4, WHITE)
        ty += 11
    y += h + 22

    # ---- 04 follow-ups: ruled lines to capture what carries over ----
    y = heading(pg, y, "04", "FOLLOW-UPS", "Unfinished admin and anything to carry to tomorrow.")
    bottom = H - 48
    line_gap = 20
    n = int((bottom - y) // line_gap)
    for i in range(n):
        ly = y + (i + 1) * line_gap
        tick_box(pg, M + 2, ly - 9)
        pg.line(M + 18, ly, M + CW, ly, GRID, width=0.6)
    end = y + n * line_gap
    print(f"content ends {end:.0f}, footer marking at {H - 30}")

    doc.set_metadata({"title": f"Run Sheet {SUBTITLE}", "author": "NZALC"})
    doc.save(OUT, garbage=3, deflate=True)
    pymupdf.open(OUT)[0].get_pixmap(dpi=200).save(PNG)
    print(f"Saved {OUT} and {PNG}")


if __name__ == "__main__":
    build()
