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
VERSION         = "Working draft v0.6"

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

CHEV_CLASSES = ["c1", "c2", "c3", "c4", "c5"]


def chevrons(band):
    stages = [s.strip() for s in band.split("→")]
    if len(stages) != len(CHEV_CLASSES):
        sys.exit(f"progression needs {len(CHEV_CLASSES)} stages, got {len(stages)}")
    return "\n".join(
        f'    <div class="chev {cls}">{esc(s)}</div>'
        for cls, s in zip(CHEV_CLASSES, stages))


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
     Calibri body copy. */
  :root {{
    --red: {red}; --black: {black}; --swamp: {swamp}; --kawa: {kawa};
    --hills: {hills}; --moa: {moa}; --white: {white};
    --ink: #14100C; --muted: #5A5449; --card: #FBF9F1;
  }}
  @page {{ size: A3 portrait; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  html, body {{ width: 297mm; }}
  body {{ font-family: Carlito, Calibri, sans-serif; background: var(--white);
          color: var(--ink); font-size: 12.4pt; line-height: 1.32; }}
  .sheet {{ width: 297mm; height: 420mm; padding: 15mm 15mm 11mm;
            display: flex; flex-direction: column; }}
  .display {{ font-family: "Archivo Black", "Arial Black", sans-serif;
              font-weight: 400; letter-spacing: -0.01em; }}
  .lab {{ font-size: 9.4pt; letter-spacing: 0.16em; text-transform: uppercase; }}

  /* masthead */
  .masthead {{ display: flex; align-items: flex-end;
               justify-content: space-between; gap: 12mm; padding-bottom: 4.5mm; }}
  .masthead img {{ height: 16mm; }}
  .titles h1 {{ font-size: 43pt; line-height: 0.95; color: var(--black); }}
  .titles p {{ font-size: 14pt; font-weight: 700; color: var(--swamp);
               margin-top: 2.4mm; }}
  .rule-red {{ height: 1.8mm; background: var(--red); }}

  /* question */
  .question {{ background: var(--swamp); color: var(--white);
               padding: 6mm 7.5mm; display: flex; align-items: baseline;
               gap: 6mm; margin-top: 5mm; }}
  .question .lab {{ color: var(--hills); white-space: nowrap; }}
  .question .q {{ font-size: 21pt; }}

  /* the answer, given prominence: a poster is read answer first */
  .answer {{ margin-top: 5mm; border-left: 3.4mm solid var(--red);
             background: var(--moa); padding: 7mm 8mm 7.5mm; }}
  .answer .lab {{ color: var(--kawa); margin-bottom: 3.4mm; }}
  .answer p {{ font-size: 17.5pt; line-height: 1.29; color: var(--swamp);
               font-weight: 700; }}
  .answer .punch {{ display: block; margin-top: 4mm; font-size: 19pt;
                    color: var(--red); }}

  /* section rules */
  .band-title {{ display: flex; align-items: center; gap: 5mm;
                 margin: 9mm 0 5mm; }}
  .band-title h2 {{ font-size: 20pt; color: var(--black); white-space: nowrap; }}
  .band-title .line {{ flex: 1; height: 0.7mm; background: var(--black); }}

  /* progression */
  .chevrons {{ display: flex; gap: 1.4mm; }}
  .chev {{ flex: 1; padding: 5mm 4mm 5mm 9mm; font-size: 12.2pt;
           font-weight: 700; min-height: 19mm; display: flex;
           align-items: center; line-height: 1.18;
           clip-path: polygon(0 0, calc(100% - 5.5mm) 0, 100% 50%,
                              calc(100% - 5.5mm) 100%, 0 100%, 5.5mm 50%); }}
  .chev:first-child {{ padding-left: 5mm;
    clip-path: polygon(0 0, calc(100% - 5.5mm) 0, 100% 50%,
                       calc(100% - 5.5mm) 100%, 0 100%); }}
  .chev:last-child {{ clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%,
                                         5.5mm 50%); }}
  .c1 {{ background: var(--moa);   color: var(--swamp); }}
  .c2 {{ background: var(--hills); color: var(--swamp); }}
  .c3 {{ background: var(--kawa);  color: var(--white); }}
  .c4 {{ background: var(--swamp); color: var(--white); }}
  .c5 {{ background: var(--red);   color: var(--white); }}

  /* what actually changes across the progression */
  .wedges {{ margin-top: 4mm; display: flex; flex-direction: column; gap: 3mm; }}
  .wedge-row {{ display: flex; align-items: center; gap: 5mm; }}
  .wedge-lab {{ font-size: 10.8pt; width: 80mm; line-height: 1.24; }}
  .wedge-lab b {{ color: var(--swamp); }}
  .wedge {{ flex: 1; height: 10mm; }}
  .w-down {{ background: var(--swamp);
             clip-path: polygon(0 0, 100% 42%, 100% 58%, 0 100%); }}
  .w-up {{ background: var(--red);
           clip-path: polygon(0 42%, 100% 0, 100% 100%, 0 58%); }}
  .wedge-end {{ font-size: 9pt; letter-spacing: 0.12em; text-transform: uppercase;
                color: var(--muted); width: 22mm; text-align: right; }}

  /* decision rule: full width so the expression sits on one line */
  .rule-box {{ margin-top: 6mm; background: var(--swamp); color: var(--white);
               padding: 5mm 6mm 5.6mm; text-align: center; }}
  .rule-box .lab {{ color: var(--hills); }}
  .rule-box .expr {{ font-size: 16pt; margin-top: 3mm; line-height: 1.2; }}
  .rule-box .expr span {{ color: var(--hills); padding: 0 2.5mm; }}

  /* career cycle */
  .cycle-lab {{ margin-top: 7mm; font-size: 10.8pt; color: var(--muted); }}
  .cycle {{ margin-top: 3mm; display: flex; align-items: stretch; }}
  .step {{ flex: 1; text-align: center; font-size: 11.4pt; font-weight: 700;
           color: var(--swamp); border: 0.5mm solid var(--hills);
           background: var(--card); padding: 4.2mm 1mm;
           display: flex; align-items: center; justify-content: center; }}
  .arrow {{ width: 5mm; flex: none; display: flex; align-items: center;
            justify-content: center; color: var(--hills); font-size: 12pt; }}
  .loopback {{ display: flex; align-items: center; gap: 4mm; margin-top: 2.4mm; }}
  .loopback .track {{ flex: 1; height: 0.5mm; background: var(--hills); }}
  .loopback .txt {{ font-size: 9.2pt; letter-spacing: 0.12em;
                    text-transform: uppercase; color: var(--muted); }}

  /* supporting takeaways */
  .grid {{ margin-top: 5mm; display: grid; grid-template-columns: repeat(3, 1fr);
           gap: 5mm; }}
  .card {{ border-top: 1.2mm solid var(--red); padding-top: 3.4mm; }}
  .card .n {{ font-family: "Archivo Black", "Arial Black", sans-serif;
              font-size: 17pt; color: var(--red); line-height: 1; }}
  .card h3 {{ font-size: 12.2pt; color: var(--swamp); margin: 2mm 0;
              line-height: 1.22; }}
  .card p {{ font-size: 10.8pt; line-height: 1.3; }}

  /* footer */
  .foot {{ margin-top: auto; padding-top: 6mm; display: flex;
           justify-content: space-between; align-items: flex-end;
           gap: 8mm; border-top: 0.5mm solid var(--hills);
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
  <div class="rule-red"></div>

  <section class="question">
    <div class="lab">Commander's Question</div>
    <div class="q display">{question}</div>
  </section>

  <section class="answer">
    <div class="lab">Emerging Proposition</div>
    {proposition}
  </section>

  <div class="band-title"><h2 class="display">The Emerging Model</h2>
    <div class="line"></div></div>

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
  <div class="loopback">
    <div class="txt">Repeats</div><div class="track"></div>
    <div class="txt">Across a career</div>
  </div>

  <div class="band-title"><h2 class="display">Emerging Takeaways</h2>
    <div class="line"></div></div>

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
