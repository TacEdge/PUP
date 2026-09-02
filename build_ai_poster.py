#!/usr/bin/env python3
"""
Build the 'AI and Operational Effectiveness' A3 poster from the paper's own
markdown, so the wall product and the paper cannot disagree.

Same design system as the individual training poster: one filled panel, Army
Red only for the punchline, the end stage and numbering, plain type elsewhere.

    python3 build_ai_poster.py
"""

import base64
import io
import os
import re
import subprocess
import sys

from PIL import Image

# ----------------------------------------------------------------- CONFIG ---
SOURCE_FILE   = "./ai-army-operational-effectiveness.md"
LOGO_FILE     = "./assets/nz-army-logo.png"
OUTPUT_HTML   = "./ai-army-operational-effectiveness-poster.html"
OUTPUT_PDF    = "./output/ai-army-operational-effectiveness-poster.pdf"
CHROME        = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

PROTECTIVE_MARKING = "UNCLASSIFIED"
POSTER_TITLE    = "AI and Operational Effectiveness"
POSTER_STRAP    = "How Army uses AI to increase operational effectiveness"
CONTROL_LINE    = "A first-principles analysis for senior Army leadership &nbsp;&middot;&nbsp; Draft v0.1"
REFERENCE_LINE  = "AI and Army Operational Effectiveness &nbsp;&middot;&nbsp; Draft v0.1"

# Poster copy that compresses the paper rather than quoting it.
PUNCHLINE = ("A small army that cannot fight when the tools are denied has not "
             "gained effectiveness. It has moved its dependence.")
FRAMEWORK_TEST = ("An application that cannot answer Constraint and Mechanism is "
                  "novelty. Measure the effect on the output, not the use of the tool.")
NOT_PRIORITISED = ("Deliberately not prioritised: autonomous targeting, and "
                   "personnel analytics ahead of the data to support them.")

# Below the people line the poster has to be read from a wall, not at arm's
# length. These compress the paper's principles and actions; the paper keeps
# its full wording. Keyed by heading; anything unlisted uses the paper's text.
POSTER_COPY = {
    "Effect first":
        "Adopted where it improves an Army output, and measured against it.",
    "Task before tool":
        "From the output and its constraint to the application, never the reverse.",
    "The commander owns it":
        "AI advises; it does not decide where consequence is high. "
        "Verify what you use. You own what you sign.",
    "Assurance by consequence":
        "More control where error costs more, lasts longer or is harder to check.",
    "Competence before dependence":
        "No one relies on a tool for a skill they must perform without it. "
        "Competence comes from practice against real tasks.",
    "Own it":
        "Assign accountability for AI in Army; set risk appetite by consequence, "
        "so low-consequence use is enabled by default.",
    "Prove effect in three places":
        "Bounded, measured trials: planning and orders in a headquarters; training "
        "design in Army Training Group; readiness data. Stop what does not work.",
    "Train it through the approach":
        "AI competence built into individual training against real tasks, with "
        "tool-denied assurance of core skills. Instructors first.",
    "Improve the data":
        "Readiness and training data are likely to constrain the highest-value "
        "applications Army controls directly.",
    "Compress the lessons cycle":
        "From observation to updated training and tactics at a pace the force "
        "can act on.",
}

PALETTE = {
    "red": "#D31145", "black": "#000000", "swamp": "#00261B",
    "kawa": "#444D06", "hills": "#B3A650", "moa": "#DFD8AD",
    "white": "#FFFFFF",
}

# --------------------------------------------------------- source parsing ---

BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
PLACEHOLDER_RE = re.compile(r"\[[^\]]+\]")


def parse(path):
    """Everything the poster needs, keyed by the paper's section headings."""
    lines = open(path, encoding="utf-8").read().splitlines()
    sections = {}
    section = None
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("## "):
            section = s[3:].strip()
            sections[section] = {"callouts": [], "bands": [], "items": [],
                                 "rows": [], "paras": []}
            continue
        if section is None:
            continue
        sec = sections[section]
        if s.startswith(">> "):
            sec["bands"].append(s[3:].strip())
        elif s.startswith("> "):
            sec["callouts"].append(s[2:].strip())
        elif s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not all(c and set(c) <= set("- ") for c in cells):
                sec["rows"].append(cells)
        else:
            m = re.match(r"^([a-z])\. (.*)$", s)
            if m:
                body = m.group(2)
                head = BOLD_RE.search(body)
                sec["items"].append((
                    head.group(1).rstrip(".") if head else "",
                    BOLD_RE.sub("", body).strip(),
                ))
            else:
                m = re.match(r"^\d+\. (.*)$", s)
                if m:
                    sec["paras"].append(m.group(1))
    return sections


def find(sections, prefix):
    for name, sec in sections.items():
        if name.startswith(prefix):
            return sec
    sys.exit(f"section not found: {prefix}")


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;"))


def mark(text):
    return PLACEHOLDER_RE.sub(
        lambda m: f'<span class="todo">{m.group(0)}</span>', text)


def logo_data_uri(path):
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


# ------------------------------------------------------------- components ---

def chevrons(band):
    stages = [s.strip() for s in band.split("→")]
    return "\n".join(f'    <div class="chev">{esc(s)}</div>' for s in stages)


def step_questions(items):
    return "\n".join(f'    <div class="q">{esc(body)}</div>' for _, body in items)


def area_cards(rows):
    out = []
    for area, mechanism, mode, _consequence, human in rows[1:]:
        out.append(
            f'    <div class="area"><h4>{esc(area)}</h4>'
            f'<p>{esc(mechanism)}</p>'
            f'<div class="mode">{esc(mode)}</div>'
            f'<p class="human">{esc(human)}</p></div>')
    return "\n".join(out)


def numbered(items):
    out = []
    for i, (head, body) in enumerate(items, 1):
        body = POSTER_COPY.get(head, body)
        out.append(
            f'    <div class="item"><div class="n">{i}</div>'
            f'<div><h4>{esc(head)}</h4><p>{esc(body)}</p></div></div>')
    return "\n".join(out)


def people_line(sections):
    sec = find(sections, "5.")
    for p in sec["paras"]:
        if "Everyone understands it" in p:
            sentence = p.split("Everyone understands it", 1)[1]
            parts = ["Everyone understands it" + sentence.split(";")[0]]
            parts += [s.strip().rstrip(".") for s in sentence.split(";")[1:]]
            return ' <span class="dot">&bull;</span> '.join(
                esc(x[0].upper() + x[1:]) for x in parts)
    sys.exit("people line not found in section 5")


# ------------------------------------------------------------------ build ---

def main():
    sections = parse(SOURCE_FILE)
    question = find(sections, "The Question")["callouts"]
    answer = find(sections, "1.")["callouts"]
    framework = find(sections, "2.")
    advantage = find(sections, "3.")
    human = find(sections, "4.")
    principles = find(sections, "8.")["items"]
    actions = find(sections, "9.")["items"]

    if len(framework["items"]) != 8 or not framework["bands"]:
        sys.exit("framework needs one band and eight steps")
    if len(advantage["rows"]) != 6:
        sys.exit("expected a header row and five areas")
    if not human["bands"]:
        sys.exit("assurance test band missing from section 4")

    html = TEMPLATE.format(
        title=esc(POSTER_TITLE), strap=esc(POSTER_STRAP),
        logo=logo_data_uri(LOGO_FILE),
        control=mark(CONTROL_LINE),
        question=esc(question[0]),
        answer=esc(answer[0]),
        punch=esc(PUNCHLINE),
        chevrons=chevrons(framework["bands"][0]),
        questions=step_questions(framework["items"]),
        test=esc(FRAMEWORK_TEST),
        assurance=esc(human["bands"][0]),
        areas=area_cards(advantage["rows"]),
        not_prioritised=esc(NOT_PRIORITISED),
        people=people_line(sections),
        principles=numbered(principles),
        actions=numbered(actions),
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
<title>AI and Operational Effectiveness</title>
<style>
  :root {{
    --red: {red}; --black: {black}; --swamp: {swamp}; --kawa: {kawa};
    --hills: {hills}; --moa: {moa}; --white: {white};
    --ink: #14100C; --muted: #5A5449; --hair: #D9D2BC; --r: 1.6mm;
  }}
  @page {{ size: A3 portrait; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  html, body {{ width: 297mm; }}
  body {{ font-family: Carlito, Calibri, sans-serif; background: var(--white);
          color: var(--ink); font-size: 11pt; line-height: 1.28; }}
  .sheet {{ width: 297mm; height: 420mm; padding: 13mm 17mm 10mm;
            display: flex; flex-direction: column; }}
  .display {{ font-family: "Archivo Black", "Arial Black", sans-serif;
              font-weight: 400; letter-spacing: -0.01em; }}
  .lab {{ font-size: 9pt; letter-spacing: 0.16em; text-transform: uppercase;
          color: var(--muted); }}
  .todo {{ color: var(--red); }}

  .masthead {{ display: flex; align-items: flex-start;
               justify-content: space-between; gap: 12mm; padding-bottom: 4mm;
               border-bottom: 1.2mm solid var(--red); }}
  .masthead img {{ height: 15mm; margin-top: 1mm; }}
  .titles h1 {{ font-size: 28pt; line-height: 0.95; color: var(--black);
               white-space: nowrap; }}
  .titles p {{ font-size: 12.5pt; font-weight: 700; color: var(--swamp);
               margin-top: 2mm; }}
  .control {{ margin-top: 4mm; padding-bottom: 3.4mm;
              border-bottom: 0.4mm solid var(--hair);
              font-size: 10pt; letter-spacing: 0.06em;
              text-transform: uppercase; color: var(--muted); }}

  .question {{ margin-top: 5mm; }}
  .question .q {{ font-size: 18pt; color: var(--black); margin-top: 2mm;
                  line-height: 1.12; }}

  .answer {{ margin-top: 4.5mm; border-left: 3.4mm solid var(--red);
             background: var(--moa); padding: 5mm 8mm 5.5mm;
             border-radius: var(--r); }}
  .answer .lab {{ color: var(--kawa); margin-bottom: 2.6mm; }}
  .answer p {{ font-size: 15pt; line-height: 1.3; color: var(--swamp);
               font-weight: 700; }}
  .answer .punch {{ display: block; margin-top: 3mm; font-size: 14.5pt;
                    color: var(--red); }}

  h2.display {{ font-size: 16pt; color: var(--black); margin: 7mm 0 1.2mm; }}
  .cap {{ font-size: 10pt; color: var(--muted); margin-bottom: 3.6mm; }}

  /* the framework: eight stages, each with its question beneath */
  .chevrons {{ display: flex; gap: 1.2mm; }}
  .chev {{ flex: 1; padding: 3.5mm 2.5mm 3.5mm 6.5mm; font-size: 10.8pt;
           font-weight: 700; min-height: 17mm; display: flex;
           align-items: center; line-height: 1.14;
           background: var(--swamp); color: var(--white);
           clip-path: polygon(0 0, calc(100% - 4.5mm) 0, 100% 50%,
                              calc(100% - 4.5mm) 100%, 0 100%, 4.5mm 50%); }}
  .chev:first-child {{ padding-left: 4mm;
    clip-path: polygon(0 0, calc(100% - 4.5mm) 0, 100% 50%,
                       calc(100% - 4.5mm) 100%, 0 100%); }}
  .chev:last-child {{ background: var(--red);
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 4.5mm 50%); }}
  .questions {{ display: grid; grid-template-columns: repeat(8, 1fr);
                gap: 1.2mm; margin-top: 2.6mm; }}
  .questions .q {{ font-size: 8.6pt; line-height: 1.22; color: var(--muted);
                   padding: 0 2mm 0 1mm; }}
  .test {{ margin-top: 3.6mm; text-align: center; font-size: 11.6pt;
           font-weight: 700; color: var(--swamp); }}

  .rule-box {{ margin-top: 6mm; padding: 4mm 0 4.5mm; text-align: center;
               border-top: 0.4mm solid var(--hair);
               border-bottom: 0.4mm solid var(--hair); }}
  .rule-box .expr {{ font-size: 14pt; margin-top: 2.2mm; line-height: 1.2;
                     color: var(--swamp); }}

  /* five areas of advantage */
  .areas {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 6mm; }}
  .area h4 {{ font-size: 11.4pt; color: var(--swamp); line-height: 1.18;
              margin-bottom: 1.6mm; }}
  .area p {{ font-size: 9.6pt; line-height: 1.28; color: var(--muted); }}
  .area .mode {{ display: inline-block; margin: 2mm 0 1.6mm; padding: 0.6mm 2mm;
                 border: 0.35mm solid var(--hills); border-radius: 1mm;
                 font-size: 8.6pt; letter-spacing: 0.08em;
                 text-transform: uppercase; color: var(--kawa); }}
  .area .human {{ color: var(--ink); }}
  .note {{ margin-top: 3mm; font-size: 9.6pt; color: var(--muted); }}

  .people {{ margin-top: 6mm; padding: 3.4mm 0; text-align: center;
             border-top: 0.4mm solid var(--hair);
             border-bottom: 0.4mm solid var(--hair); }}
  .people .line {{ font-size: 12.5pt; font-weight: 700; color: var(--swamp);
                   margin-top: 2mm; }}
  .people .dot {{ color: var(--hills); padding: 0 1.6mm; }}

  /* principles and actions side by side */
  .two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12mm; }}
  .two h2.display {{ margin-top: 6mm; }}
  .item {{ display: flex; gap: 3.5mm; margin-bottom: 2.6mm; }}
  .item .n {{ font-family: "Archivo Black", "Arial Black", sans-serif;
              font-size: 12.5pt; color: var(--red); line-height: 1.1;
              width: 7mm; flex: none; }}
  .item h4 {{ font-size: 11pt; color: var(--swamp); line-height: 1.2;
              margin-bottom: 0.8mm; }}
  .item p {{ font-size: 9.6pt; line-height: 1.26; color: var(--muted); }}

  .foot {{ margin-top: auto; padding-top: 4mm; display: flex;
           justify-content: space-between; align-items: flex-end; gap: 8mm;
           border-top: 0.4mm solid var(--hair); font-size: 9.4pt;
           color: var(--muted); }}
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

  <section class="question">
    <div class="lab">The Question</div>
    <div class="q display">{question}</div>
  </section>

  <section class="answer">
    <div class="lab">The Answer</div>
    <p>{answer}<span class="punch display">{punch}</span></p>
  </section>

  <h2 class="display">The Framework</h2>
  <div class="cap">Reason from the output to the tool. Close on measured effect.</div>
  <div class="chevrons">
{chevrons}
  </div>
  <div class="questions">
{questions}
  </div>
  <div class="test">{test}</div>

  <div class="rule-box">
    <div class="lab">Consequence and assurance are settled by a single test</div>
    <div class="expr display">{assurance}</div>
  </div>

  <h2 class="display">Where AI Creates Advantage</h2>
  <div class="cap">Five areas survive the test, ordered by the strength of the mechanism and how much of it Army controls.</div>
  <div class="areas">
{areas}
  </div>
  <div class="note">{not_prioritised}</div>

  <div class="people">
    <div class="lab">Army people</div>
    <div class="line">{people}</div>
  </div>

  <div class="two">
    <div>
      <h2 class="display">The Principles</h2>
{principles}
    </div>
    <div>
      <h2 class="display">Priority Actions</h2>
{actions}
    </div>
  </div>

  <footer class="foot">
    <div class="mark">{marking}</div>
    <div>{subtitle}</div>
  </footer>

</div>
"""


if __name__ == "__main__":
    main()
