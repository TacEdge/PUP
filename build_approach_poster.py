#!/usr/bin/env python3
"""
Build the 'Individual Training' A3 poster from the authoritative approach
document, so the wall product and the authority cannot say different things.

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
SOURCE_FILE   = "./individual-training-approach.md"
LOGO_FILE     = "./assets/nz-army-logo.png"
OUTPUT_HTML   = "./individual-training-poster.html"
OUTPUT_PDF    = "./output/individual-training-poster.pdf"
CHROME        = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

PROTECTIVE_MARKING = "UNCLASSIFIED"
POSTER_TITLE    = "Individual Training"
POSTER_STRAP    = "The Army Approach"
# Scope only. Version, effective date, issuing authority and reference belong
# to the controlled document; on a wall product they read as unfinished draft
# furniture, so the poster states who it applies to and nothing more.
CONTROL_LINE    = "Applies to all Army individual training"
REFERENCE_LINE  = "The Army Approach to Individual Training"

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
    doc = {"takeaways": [], "bands": [], "proposition": []}
    items = {}          # numbered items, keyed by the section they sit in
    section = None
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("## "):
            section = s[3:].strip()
        elif s.startswith(">> "):
            doc["bands"].append(s[3:].strip())
        elif s.startswith("> "):
            doc["proposition"].append(s[2:].strip())
        else:
            m = re.match(r"^(\d+)\. (.*)$", s)
            if m:
                body = m.group(2)
                head = BOLD_RE.search(body)
                items.setdefault(section, []).append((
                    m.group(1),
                    head.group(1) if head else "",
                    BOLD_RE.sub("", body).strip(),
                ))
    # The poster carries the condensed principles; the full wording stays in
    # the document, where it will actually be read.
    doc["takeaways"] = (items.get("Poster Principles")
                        or items.get("The Principles") or [])
    missing = [k for k, v in doc.items() if not v]
    if missing:
        sys.exit(f"source is missing: {', '.join(missing)}")
    if len(doc["bands"]) != 3:
        sys.exit(f"expected 3 display bands, found {len(doc['bands'])}")
    return doc


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;"))


PLACEHOLDER_RE = re.compile(r"\[[^\]]+\]")


def mark(text):
    """Flag [gaps for the issuing staff] so they cannot be missed."""
    return PLACEHOLDER_RE.sub(
        lambda m: f'<span class="todo">{m.group(0)}</span>', text)


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
        control=mark(CONTROL_LINE),
        proposition=proposition(doc["proposition"]),
        chevrons=chevrons(doc["bands"][0]),
        rule=decision_rule(doc["bands"][1]),
        cycle=cycle(doc["bands"][2]),
        cards=cards(doc["takeaways"]),
        marking=PROTECTIVE_MARKING,
        subtitle=mark(REFERENCE_LINE),
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

     Deliberately restrained: one filled panel (the answer), Army Red only
     for the punchline, the final stage and the numbering, and plain type
     everywhere else. Three levels: the answer, the model, the principles. */
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
  /* the mark sits with the hero heading, not with the strapline below it */
  .masthead {{ display: flex; align-items: flex-start;
               justify-content: space-between; gap: 12mm; padding-bottom: 4mm;
               border-bottom: 1.2mm solid var(--red); }}
  /* the 0.95 line-height on the heading sets its glyphs ~1mm below the top
     of their line box, so the mark is nudged to match the cap line */
  .masthead img {{ height: 15mm; margin-top: 1mm; }}
  .titles h1 {{ font-size: 42pt; line-height: 0.95; color: var(--black); }}
  .titles p {{ font-size: 14pt; font-weight: 700; color: var(--swamp);
               margin-top: 2.4mm; }}

  /* document control, where an emerging product asked a question */
  .control {{ margin-top: 7mm; padding-bottom: 5mm;
              border-bottom: 0.4mm solid var(--hair);
              font-size: 10.4pt; letter-spacing: 0.06em;
              text-transform: uppercase; color: var(--muted); }}
  .todo {{ color: var(--red); }}

  /* the answer: the single filled panel on the sheet */
  .answer {{ margin-top: 7mm; border-left: 3.4mm solid var(--red);
             background: var(--moa); padding: 6.5mm 8mm 7mm;
             border-radius: var(--r); }}
  .answer .lab {{ color: var(--kawa); margin-bottom: 3.4mm; }}
  .answer p {{ font-size: 17pt; line-height: 1.3; color: var(--swamp);
               font-weight: 700; }}
  .answer .punch {{ display: block; margin-top: 4mm; font-size: 17pt;
                    color: var(--red); }}

  /* section headings: type alone, no rules */
  h2.display {{ font-size: 19pt; color: var(--black); margin: 12mm 0 1.6mm; }}
  .cap {{ font-size: 11pt; color: var(--muted); margin-bottom: 6mm; }}

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

  /* what changes across it: said once, in type */
  .axis {{ margin-top: 5mm; display: flex; justify-content: center; gap: 16mm;
           font-size: 13pt; font-weight: 700; color: var(--swamp); }}
  .axis .dot {{ color: var(--hills); padding: 0 1.4mm; }}
  .axis .arr {{ color: var(--red); padding-left: 1.4mm; }}

  /* decision rule: large type between two hairlines */
  .rule-box {{ margin-top: 11mm; padding: 7mm 0 7.5mm; text-align: center;
               border-top: 0.4mm solid var(--hair);
               border-bottom: 0.4mm solid var(--hair); }}
  .rule-box .expr {{ font-size: 16.5pt; margin-top: 3.6mm; line-height: 1.2;
                     color: var(--swamp); }}
  .rule-box .expr span {{ color: var(--red); padding: 0 2.5mm; }}

  /* career cycle: words and arrows, no boxes */
  .cycle-lab {{ margin-top: 11mm; font-size: 11pt; color: var(--muted); }}
  .cycle {{ margin-top: 4mm; display: flex; align-items: center; }}
  .step {{ flex: 1 1 auto; white-space: nowrap; text-align: center;
           font-size: 12.6pt; font-weight: 700; color: var(--swamp);
           padding: 2mm 1mm; }}
  .arrow {{ width: 5mm; flex: none; text-align: center; color: var(--hills);
            font-size: 12pt; }}
  .repeat {{ width: 9mm; flex: none; text-align: right; color: var(--hills);
             font-size: 17pt; line-height: 1; }}

  /* the principles: number, short title, one line */
  .grid {{ display: grid; grid-template-columns: repeat(3, 1fr);
           gap: 10mm 10mm; }}
  .card .n {{ font-family: "Archivo Black", "Arial Black", sans-serif;
              font-size: 19pt; color: var(--red); line-height: 1; }}
  .card h3 {{ font-size: 15pt; color: var(--swamp); margin: 2.6mm 0 2mm;
              line-height: 1.18; }}
  .card p {{ font-size: 12.4pt; line-height: 1.3; color: var(--muted); }}

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

  <div class="control">{control}</div>

  <section class="answer">
    <div class="lab">The Approach</div>
    {proposition}
  </section>

  <h2 class="display">The Model</h2>
  <div class="cap">How Army develops the individual.</div>

  <div class="chevrons">
{chevrons}
  </div>

  <div class="axis">
    <span>Instructor direction<span class="arr">&darr;</span></span>
    <span>Learner autonomy<span class="dot">&bull;</span>complexity<span class="dot">&bull;</span>pressure<span class="arr">&uarr;</span></span>
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
    <div class="repeat">&#8635;</div>
  </div>

  <h2 class="display">The Principles</h2>
  <div class="cap">What the approach means in practice.</div>

  <div class="grid">
{cards}
  </div>

  <footer class="foot">
    <div class="mark">{marking}</div>
    <div>{subtitle}</div>
  </footer>

</div>
"""


if __name__ == "__main__":
    main()
