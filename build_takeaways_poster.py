#!/usr/bin/env python3
"""
Build the 'Individual Training' A3 poster from the same source markdown as the
staff-paper one-pager, so the two never drift apart.

The poster is not the paper enlarged: it leads with the answer, gives the
emerging model a real diagram (progression chevrons, the opposing wedges that
show what actually changes across it, the decision rule, the career cycle),
and drops the takeaways to a supporting grid underneath.

    python3 build_takeaways_poster.py

Renders through the pre-installed Chromium; no Playwright needed.
"""

import base64
import io
import os
import re
import subprocess
import sys

from PIL import Image

# ----------------------------------------------------------------- CONFIG ---
SOURCE_FILE   = "./individual-training-key-takeaways.md"
LOGO_FILE     = "./assets/nz-army-logo.png"
OUTPUT_HTML   = "./individual-training-poster.html"
OUTPUT_PDF    = "./output/individual-training-poster.pdf"
CHROME        = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

PROTECTIVE_MARKING = "UNCLASSIFIED"
POSTER_TITLE    = "Individual Training"
POSTER_STRAP    = "The Army Approach: an emerging synthesis"
ORIGINATOR      = "Individual Training Review"
DATE            = "September 2026"
VERSION         = "Working draft v0.7"

# NZ Army palette, Visual Identity Guidelines v1.0 p58.
PALETTE = {
    "red": "#D31145", "black": "#000000", "swamp": "#00261B",
    "kawa": "#444D06", "hills": "#B3A650", "moa": "#DFD8AD",
    "white": "#FFFFFF",
}

# --------------------------------------------------------- source parsing ---

BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def parse(path):
    """Pull the poster's content out of the shared markdown."""
    lines = open(path, encoding="utf-8").read().splitlines()
    doc = {"subtitle": "", "question": "", "takeaways": [], "bands": [],
           "proposition": []}
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("**Adult Learning Principles"):
            doc["subtitle"] = s.strip("*")
        elif s == "**What is the Army approach to individual training?**":
            doc["question"] = s.strip("*")
        elif s.startswith(">> "):
            doc["bands"].append(s[3:].strip())
        elif s.startswith("> "):
            doc["proposition"].append(s[2:].strip())
        else:
            m = re.match(r"^(\d+)\. (.*)$", s)
            if m:
                body = m.group(2)
                head = BOLD_RE.search(body)
                doc["takeaways"].append((
                    m.group(1),
                    head.group(1) if head else "",
                    BOLD_RE.sub("", body).strip(),
                ))
    missing = [k for k, v in doc.items() if not v]
    if missing:
        sys.exit(f"source is missing: {', '.join(missing)}")
    if len(doc["bands"]) != 3:
        sys.exit(f"expected 3 display bands, found {len(doc['bands'])}")
    return doc


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;"))


def logo_data_uri(path):
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())   # trim the transparent margin
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


# ------------------------------------------------------------- components ---

STAGES = 5


def chevrons(band):
    stages = [s.strip() for s in band.split("→")]
    if len(stages) != STAGES:
        sys.exit(f"progression needs {STAGES} stages, got {len(stages)}")
    return "\n".join(f'    <div class="chev">{esc(s)}</div>' for s in stages)


def decision_rule(band):
    factors = [f.strip() for f in band.split("×")]
    joined = ' <span>&times;</span> '.join(esc(f) for f in factors)
    return f'<div class="expr display">{joined}</div>'


def cycle(band):
    steps = [s.strip() for s in band.split("→")]
    out = []
    for i, s in enumerate(steps):
        if i:
            out.append('    <div class="arrow">&#9656;</div>')
        out.append(f'    <div class="step">{esc(s)}</div>')
    return "\n".join(out)


# Chain geometry, in mm across the 267mm text measure: 7 steps separated by
# 5mm arrows. Used to land the return path under the right boxes.
CYCLE_W, ARROW_W = 263.0, 5.0


def loop(band):
    """Return path from the end of the cycle back into 'Learn'.

    A straight rule under the chain reads as an end-to-end process; the poster
    has to show feedback re-entering the cycle, which is the whole point of
    calling it one.
    """
    steps = [s.strip() for s in band.split("→")]
    step_w = (CYCLE_W - ARROW_W * (len(steps) - 1)) / len(steps)

    def centre(i):
        return i * (step_w + ARROW_W) + step_w / 2

    try:
        target = centre(steps.index("Learn"))
    except ValueError:
        target = centre(1)
    start = centre(len(steps) - 1)
    caption = "Feedback and reinforcement re-enter the cycle"
    mid = (start + target) / 2
    box_w = len(caption) * 2.06 + 6

    return f'''<svg viewBox="0 0 {CYCLE_W:.0f} 15" preserveAspectRatio="xMidYMid meet">
      <defs>
        <marker id="ah" viewBox="0 0 10 10" refX="6" refY="5"
                markerWidth="4" markerHeight="4" orient="auto">
          <path d="M0,0 L10,5 L0,10 z" fill="var(--hills)"/>
        </marker>
      </defs>
      <path d="M {start:.1f} 0 V 8 Q {start:.1f} 12 {start - 5:.1f} 12
               H {target + 5:.1f} Q {target:.1f} 12 {target:.1f} 8 V 1"
            fill="none" stroke="var(--hills)" stroke-width="0.6"
            marker-end="url(#ah)"/>
      <rect x="{mid - box_w / 2:.1f}" y="9.2" width="{box_w:.1f}" height="5.6"
            fill="var(--white)"/>
      <text x="{mid:.1f}" y="13.1" text-anchor="middle" fill="var(--muted)"
            font-family="Carlito, Calibri, sans-serif" font-size="3.1"
            letter-spacing="0.25">{caption.upper()}</text>
    </svg>'''


def cards(takeaways):
    out = []
    for num, head, body in takeaways:
        out.append(
            f'    <div class="card"><div class="n">{num}</div>\n'
            f'      <h3>{esc(head)}</h3>\n'
            f'      <p>{esc(body)}</p></div>')
    return "\n".join(out)


def proposition(lines):
    body = esc(lines[0])
    punch = "".join(
        f'<span class="punch display">{esc(l)}</span>' for l in lines[1:])
    return f"<p>{body}{punch}</p>"


# ------------------------------------------------------------------ build ---

def main():
    doc = parse(SOURCE_FILE)
    html = TEMPLATE.format(
        title=esc(POSTER_TITLE),
        strap=esc(POSTER_STRAP),
        logo=logo_data_uri(LOGO_FILE),
        question=esc(doc["question"]),
        proposition=proposition(doc["proposition"]),
        chevrons=chevrons(doc["bands"][0]),
        rule=decision_rule(doc["bands"][1]),
        cycle=cycle(doc["bands"][2]),
        loop=loop(doc["bands"][2]),
        cards=cards(doc["takeaways"]),
        marking=PROTECTIVE_MARKING,
        stamp=f"{esc(ORIGINATOR)} &nbsp;&middot;&nbsp; {esc(VERSION)}"
              f" &nbsp;&middot;&nbsp; {esc(DATE)}",
        subtitle=esc(doc["subtitle"]),
        **PALETTE,
    )
    with open(OUTPUT_HTML, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Saved {OUTPUT_HTML}")

    os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)
    result = subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", "--virtual-time-budget=6000",
        f"--print-to-pdf={os.path.abspath(OUTPUT_PDF)}",
        "file://" + os.path.abspath(OUTPUT_HTML),
    ], capture_output=True, text=True)
    if not os.path.exists(OUTPUT_PDF):
        sys.exit(result.stderr[-2000:] or "chromium produced no PDF")
    print(f"Saved {OUTPUT_PDF}")


TEMPLATE = """<!doctype html>
<meta charset="utf-8">
<title>Individual Training: The Army Approach</title>
<style>
  /* NZ Army palette, Visual Identity Guidelines v1.0 p58. Typography p59:
     Archivo Black stands in for the Arial Black display face, Carlito for
     Calibri body copy.

     Deliberately restrained: one filled panel (the proposition), Army Red
     only for the punchline, the final stage and the numbering, and plain
     type everywhere else. The content carries the hierarchy. */
  :root {{
    --red: {red}; --black: {black}; --swamp: {swamp}; --kawa: {kawa};
    --hills: {hills}; --moa: {moa}; --white: {white};
    --ink: #14100C; --muted: #5A5449; --hair: #D9D2BC;
    --r: 1.6mm;
  }}
  @page {{ size: A3 portrait; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  html, body {{ width: 297mm; }}
  body {{ font-family: Carlito, Calibri, sans-serif; background: var(--white);
          color: var(--ink); font-size: 12.4pt; line-height: 1.34; }}
  .sheet {{ width: 297mm; height: 420mm; padding: 16mm 17mm 11mm;
            display: flex; flex-direction: column; }}
  .display {{ font-family: "Archivo Black", "Arial Black", sans-serif;
              font-weight: 400; letter-spacing: -0.01em; }}
  .lab {{ font-size: 9.4pt; letter-spacing: 0.16em; text-transform: uppercase;
          color: var(--muted); }}

  /* masthead */
  .masthead {{ display: flex; align-items: flex-end;
               justify-content: space-between; gap: 12mm; padding-bottom: 4mm;
               border-bottom: 1.2mm solid var(--red); }}
  .masthead img {{ height: 15mm; }}
  .titles h1 {{ font-size: 42pt; line-height: 0.95; color: var(--black); }}
  .titles p {{ font-size: 14pt; font-weight: 700; color: var(--swamp);
               margin-top: 2.4mm; }}

  /* question: plain type, no band */
  .question {{ margin-top: 8mm; }}
  .question .q {{ font-size: 22pt; color: var(--black); margin-top: 2.2mm;
                  line-height: 1.12; }}

  /* the answer: the single filled panel on the sheet */
  .answer {{ margin-top: 6mm; border-left: 3.4mm solid var(--red);
             background: var(--moa); padding: 6.5mm 8mm 7mm;
             border-radius: var(--r); }}
  .answer .lab {{ color: var(--kawa); margin-bottom: 3.4mm; }}
  .answer p {{ font-size: 17pt; line-height: 1.3; color: var(--swamp);
               font-weight: 700; }}
  .answer .punch {{ display: block; margin-top: 4mm; font-size: 17pt;
                    color: var(--red); }}

  /* section headings: type alone, no rules */
  h2.display {{ font-size: 18pt; color: var(--black); margin: 10mm 0 5mm; }}
  h2.display.sub {{ font-size: 15pt; color: var(--swamp); margin-bottom: 1.6mm; }}
  .sub-cap {{ font-size: 10.4pt; color: var(--muted); margin-bottom: 4.5mm; }}

  /* progression: one colour, the end stage in red */
  .chevrons {{ display: flex; gap: 1.4mm; }}
  .chev {{ flex: 1; padding: 5mm 4mm 5mm 9mm; font-size: 13pt;
           font-weight: 700; min-height: 18mm; display: flex;
           align-items: center; line-height: 1.18;
           background: var(--swamp); color: var(--white);
           clip-path: polygon(0 0, calc(100% - 5.5mm) 0, 100% 50%,
                              calc(100% - 5.5mm) 100%, 0 100%, 5.5mm 50%); }}
  .chev:first-child {{ padding-left: 5mm;
    clip-path: polygon(0 0, calc(100% - 5.5mm) 0, 100% 50%,
                       calc(100% - 5.5mm) 100%, 0 100%); }}
  .chev:last-child {{ background: var(--red);
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 5.5mm 50%); }}

  /* what changes across it: two thin wedges in the quiet colours */
  .wedges {{ margin-top: 4mm; display: flex; flex-direction: column; gap: 2.5mm; }}
  .wedge-row {{ display: flex; align-items: center; gap: 5mm; }}
  .wedge-lab {{ font-size: 10.8pt; width: 80mm; line-height: 1.24; }}
  .wedge-lab b {{ color: var(--swamp); }}
  .wedge {{ flex: 1; height: 7mm; }}
  .w-down {{ background: var(--swamp);
             clip-path: polygon(0 0, 100% 44%, 100% 56%, 0 100%); }}
  .w-up {{ background: var(--hills);
           clip-path: polygon(0 44%, 100% 0, 100% 100%, 0 56%); }}
  .wedge-end {{ font-size: 9pt; letter-spacing: 0.12em; text-transform: uppercase;
                color: var(--muted); width: 22mm; text-align: right; }}

  /* decision rule: large type between two hairlines */
  .rule-box {{ margin-top: 7mm; padding: 4.5mm 0 5mm; text-align: center;
               border-top: 0.4mm solid var(--hair);
               border-bottom: 0.4mm solid var(--hair); }}
  .rule-box .expr {{ font-size: 16pt; margin-top: 3mm; line-height: 1.2;
                     color: var(--swamp); }}
  .rule-box .expr span {{ color: var(--red); padding: 0 2.5mm; }}

  /* career cycle: words and arrows, no boxes */
  .cycle-lab {{ margin-top: 7mm; font-size: 10.8pt; color: var(--muted); }}
  .cycle {{ margin-top: 3.4mm; display: flex; align-items: center; }}
  .step {{ flex: 1; text-align: center; font-size: 12pt; font-weight: 700;
           color: var(--swamp); padding: 2mm 1mm; }}
  .arrow {{ width: 5mm; flex: none; text-align: center; color: var(--hills);
            font-size: 12pt; }}
  .loopback {{ line-height: 0; }}
  .loopback svg {{ width: 100%; height: 15mm; display: block; }}

  /* supporting takeaways: number, heading, text */
  .grid {{ display: grid; grid-template-columns: repeat(3, 1fr);
           gap: 5.5mm 9mm; }}
  .card .n {{ font-family: "Archivo Black", "Arial Black", sans-serif;
              font-size: 15pt; color: var(--red); line-height: 1; }}
  .card h3 {{ font-size: 11.2pt; color: var(--swamp); margin: 2mm 0 1.8mm;
              line-height: 1.22; }}
  .card p {{ font-size: 10pt; line-height: 1.32; color: var(--muted); }}

  /* footer */
  .foot {{ margin-top: auto; padding-top: 5mm; display: flex;
           justify-content: space-between; align-items: flex-end;
           gap: 8mm; border-top: 0.4mm solid var(--hair);
           font-size: 9.4pt; color: var(--muted); }}
  .foot .mark {{ font-weight: 700; letter-spacing: 0.14em; color: var(--black);
                 white-space: nowrap; }}
</style>
<div class="sheet">

  <header class="masthead">
    <div class="titles">
      <h1 class="display">{title}</h1>
      <p>{strap}</p>
    </div>
    <img src="{logo}" alt="NZ Army">
  </header>

  <section class="question">
    <div class="lab">Commander's Question</div>
    <div class="q display">{question}</div>
  </section>

  <section class="answer">
    <div class="lab">Emerging Proposition</div>
    {proposition}
  </section>

  <h2 class="display">The Emerging Model</h2>

  <div class="chevrons">
{chevrons}
  </div>

  <div class="wedges">
    <div class="wedge-row">
      <div class="wedge-lab"><b>Instructor direction</b> decreases</div>
      <div class="wedge w-down"></div>
      <div class="wedge-end">Less</div>
    </div>
    <div class="wedge-row">
      <div class="wedge-lab"><b>Learner autonomy, complexity and pressure</b>
        increase</div>
      <div class="wedge w-up"></div>
      <div class="wedge-end">More</div>
    </div>
  </div>

  <div class="rule-box">
    <div class="lab">How far and how fast an individual progresses is
      determined by</div>
    {rule}
  </div>

  <div class="cycle-lab">Individual training continues across a career through
    a recurring cycle:</div>
  <div class="cycle">
{cycle}
  </div>
  <div class="loopback">{loop}</div>

  <h2 class="display sub">Emerging Takeaways</h2>
  <div class="sub-cap">The evidence underpinning the approach above.</div>

  <div class="grid">
{cards}
  </div>

  <footer class="foot">
    <div class="mark">{marking}</div>
    <div>{stamp}</div>
    <div>{subtitle}</div>
  </footer>

</div>
"""


if __name__ == "__main__":
    main()
