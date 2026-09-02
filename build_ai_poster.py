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
# No draft or version furniture on the wall product: that belongs to the paper.
REFERENCE_LINE  = "AI and Army Operational Effectiveness"

# Poster copy that compresses the paper rather than quoting it.
PUNCHLINE = ("A small army that cannot fight when the tools are denied has not "
             "gained effectiveness. It has moved its dependence.")
FRAMEWORK_TEST = ("If you cannot say what is limiting the task, and how AI would "
                  "help, stop.")
# the three tests behind the assurance rule, in the order a person asks them
ASSURANCE_TESTS = "How bad if it is wrong? &nbsp;&middot;&nbsp; Can we undo it? &nbsp;&middot;&nbsp; Can a person check it?"
# The framework above would suit any new technology. This is what makes AI
# need it: the four properties that generate the risk.
AI_IS_DIFFERENT = ("AI is different: it can be confidently wrong, it depends on "
                   "the data behind it, it changes fast, and anyone can use it "
                   "without asking.")

# The poster trusts the thinking: headlines and one line each, no prose.
# Everything here compresses the paper; the paper keeps its full wording.
STAGES = {   # source stage -> (chevron label, the question beneath it)
    "Output":                    ("Output",       "What must we achieve?"),
    "Task":                      ("Task",         "What limits it?"),
    "Constraint":                ("Constraint",   "Why?"),
    "AI":                        ("AI",           "How would AI help?"),
    "Human Role":                ("Human Role",   "What stays human?"),
    "Assurance":                 ("Assurance",    "What control is needed?"),
    "Competence":                ("Competence",   "Who must be able to do what?"),
    "Effect":                    ("Effect",       "Did it improve the output?"),
}
# What each area actually delivers, and who stays responsible. Scannable in
# seconds; the paper's table keeps the analytical wording.
POSTER_AREAS = {
    "Planning and staff work":
        ("Faster plans, more options properly considered",
         "Commander decides and accepts risk"),
    "Intelligence and readiness":
        ("See more, sooner, from more sources", "People judge what it means"),
    "Generating trained people":
        ("Train more people, more ways, to one standard",
         "Instructors coach and assure the standard"),
    "Learning and adaptation":
        ("Turn experience into changed training faster",
         "Commanders decide what changes"),
    "Administrative load":
        ("Less time on paperwork", "You own what you sign"),
}
POSTER_COPY = {
    "Effect first":                 "Measure Army output, not AI use.",
    "Task before tool":             "Start with the constraint, not the technology.",
    "The commander owns it":        "AI advises. The commander decides and signs.",
    "Assurance by consequence":     "More human control where getting it wrong matters more.",
    "Competence before dependence": "Practise the skill. Never depend on AI for what Army must do without it.",
    "Own it":                       "Put someone in charge. Say what needs approval and what does not.",
    "Prove effect in three places": "Planning, training design, readiness data. Stop what does not work.",
    "Train it through the approach":"Train on real tasks. Test core skills without the tool. Instructors first.",
    "Improve the data":             "Readiness and training data may be the limit. Test that first.",
    "Compress the lessons cycle":   "Get lessons into training faster than the threat changes.",
}
PEOPLE = [   # the competence model as four blocks, not a divider
    ("Everyone", "understands it"), ("Many", "employ it"),
    ("Leaders", "govern it"),       ("A few", "specialise in it"),
]

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
    out = []
    for stage in (x.strip() for x in band.split("→")):
        label, _ = STAGES.get(stage, (stage, ""))
        out.append(f'    <div class="chev">{esc(label)}</div>')
    return "\n".join(out)


def step_questions(band):
    out = []
    for stage in (x.strip() for x in band.split("→")):
        _, q = STAGES.get(stage, (stage, ""))
        out.append(f'    <div class="q">{esc(q)}</div>')
    return "\n".join(out)


def pill(mode):
    mode = mode.replace("; enable for readiness", " / Enable").replace(" and ", " / ")
    return esc(mode)


def area_tiles(rows):
    out = []
    for area, mechanism, mode, _consequence, human in rows[1:]:
        gain, role = POSTER_AREAS.get(area, (mechanism, human))
        out.append(
            f'    <div class="tile"><h4>{esc(area)}</h4>'
            f'<p>{esc(gain)}</p>'
            f'<div class="pill">{pill(mode)}</div>'
            f'<p class="human">{esc(role)}</p></div>')
    return "\n".join(out)


def people_blocks():
    return "\n".join(
        f'    <div class="block"><div class="who display">{esc(who)}</div>'
        f'<div class="what">{esc(what)}</div></div>'
        for who, what in PEOPLE)


def numbered(items):
    out = []
    for i, (head, body) in enumerate(items, 1):
        body = POSTER_COPY.get(head, body)
        out.append(
            f'    <div class="item"><div class="n display">{i}</div>'
            f'<div><h4>{esc(head)}</h4><p>{esc(body)}</p></div></div>')
    return "\n".join(out)


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

    if not framework["bands"]:
        sys.exit("framework band missing from section 2")
    if len(advantage["rows"]) != 6:
        sys.exit("expected a header row and five areas")
    if not human["bands"]:
        sys.exit("assurance test band missing from section 4")

    html = TEMPLATE.format(
        title=esc(POSTER_TITLE),
        logo=logo_data_uri(LOGO_FILE),
        question=esc(question[0]),
        answer=esc(answer[0]),
        punch=esc(PUNCHLINE),
        chevrons=chevrons(framework["bands"][0]),
        questions=step_questions(framework["bands"][0]),
        test=esc(FRAMEWORK_TEST),
        assurance=esc(human["bands"][0]), tests=ASSURANCE_TESTS,
        different=esc(AI_IS_DIFFERENT),
        tiles=area_tiles(advantage["rows"]),
        people=people_blocks(),
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
  /* Three levels: the answer, the model, the implications. Red carries one
     meaning only: effect, decision, command accountability. */
  :root {{
    --red: {red}; --black: {black}; --swamp: {swamp}; --kawa: {kawa};
    --hills: {hills}; --moa: {moa}; --white: {white};
    --ink: #14100C; --muted: #5A5449; --hair: #D9D2BC; --card: #F7F4E8;
    --r: 1.6mm;
  }}
  @page {{ size: A3 portrait; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  html, body {{ width: 297mm; }}
  body {{ font-family: Carlito, Calibri, sans-serif; background: var(--white);
          color: var(--ink); font-size: 11pt; line-height: 1.28; }}
  .sheet {{ width: 297mm; height: 420mm; padding: 12mm 16mm 9mm;
            display: flex; flex-direction: column; }}
  .display {{ font-family: "Archivo Black", "Arial Black", sans-serif;
              font-weight: 400; letter-spacing: -0.01em; }}
  .lab {{ font-size: 9pt; letter-spacing: 0.16em; text-transform: uppercase;
          color: var(--muted); }}
  .todo {{ color: var(--red); }}

  /* ---- level 1: the answer ---------------------------------------------- */
  .masthead {{ display: flex; align-items: center;
               justify-content: space-between; gap: 12mm; padding-bottom: 3.5mm;
               border-bottom: 1mm solid var(--red); }}
  .masthead img {{ height: 12mm; }}
  .titles h1 {{ font-size: 26pt; line-height: 0.95; color: var(--black);
                white-space: nowrap; }}

  .question {{ margin-top: 5mm; display: flex; align-items: baseline; gap: 5mm; }}
  .question .q {{ font-size: 12.5pt; color: var(--muted); }}

  .answer {{ margin-top: 4mm; border-left: 3.4mm solid var(--red);
             background: var(--moa); padding: 8mm 10mm 8.5mm;
             border-radius: var(--r); }}
  .answer p {{ font-size: 19pt; line-height: 1.3; color: var(--swamp);
               font-weight: 700; }}
  .answer .punch {{ display: block; margin-top: 6mm; font-size: 16.5pt;
                    line-height: 1.28; color: var(--red); }}

  /* ---- level 2: the model ----------------------------------------------- */
  h2.display {{ font-size: 17pt; color: var(--black); margin: 6mm 0 3.5mm; }}
  h2.display .lab {{ display: block; margin-bottom: 1.4mm; }}

  .chevrons {{ display: flex; gap: 1.4mm; }}
  .chev {{ flex: 1; padding: 4mm 3mm 4mm 7.5mm; font-size: 13.5pt;
           font-weight: 700; min-height: 23mm; display: flex;
           align-items: center; line-height: 1.12;
           background: var(--swamp); color: var(--white);
           clip-path: polygon(0 0, calc(100% - 5mm) 0, 100% 50%,
                              calc(100% - 5mm) 100%, 0 100%, 5mm 50%); }}
  .chev:first-child {{ padding-left: 4.5mm;
    clip-path: polygon(0 0, calc(100% - 5mm) 0, 100% 50%,
                       calc(100% - 5mm) 100%, 0 100%); }}
  .chev:last-child {{ background: var(--red);
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 5mm 50%); }}
  .questions {{ display: grid; grid-template-columns: repeat(8, 1fr);
                gap: 1.4mm; margin-top: 3mm; }}
  .questions .q {{ font-size: 11pt; font-weight: 700; line-height: 1.2;
                   color: var(--swamp); padding: 0 2mm 0 1.5mm; }}
  .test {{ margin-top: 5mm; text-align: center; font-size: 11.6pt;
           color: var(--muted); }}

  .band {{ margin-top: 5mm; background: var(--swamp); color: var(--white);
           padding: 4.5mm 8mm 5mm; text-align: center; border-radius: var(--r); }}
  .band .lab {{ color: var(--hills); }}
  .band .expr {{ font-size: 15.5pt; margin-top: 2.4mm; line-height: 1.2; }}
  .band .tests {{ font-size: 10.6pt; color: var(--hills); margin-top: 3mm; }}
  .different {{ margin-top: 3mm; text-align: center; font-size: 10.6pt;
                color: var(--muted); }}

  .tiles-lab {{ margin-top: 4.5mm; }}
  .tiles {{ margin-top: 3mm; display: grid; grid-template-columns: repeat(5, 1fr);
            gap: 4mm; }}
  .tile {{ background: var(--card); border-radius: var(--r);
           padding: 3.6mm 4.5mm 4mm; display: flex; flex-direction: column; }}
  .tile h4 {{ font-size: 12.5pt; color: var(--swamp); line-height: 1.15;
              margin-bottom: 2.6mm; }}
  .tile p {{ font-size: 10.4pt; line-height: 1.26; color: var(--ink); }}
  .tile .pill {{ align-self: flex-start; margin: 3mm 0 3mm; padding: 0.9mm 2.4mm;
                 background: var(--swamp); color: var(--white); border-radius: 1mm;
                 font-size: 8.6pt; letter-spacing: 0.1em; text-transform: uppercase; }}
  .tile .human {{ color: var(--muted); margin-top: auto; }}

  /* ---- level 3: the implications ---------------------------------------- */
  .people {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; }}
  .block {{ border: 0.5mm solid var(--hills); border-radius: var(--r);
            padding: 4mm 4mm 4.4mm; text-align: center; }}
  .block .who {{ font-size: 18pt; color: var(--swamp); line-height: 1; }}
  .block .what {{ font-size: 11.5pt; color: var(--muted); margin-top: 2.4mm; }}

  .two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14mm;
          margin-top: 5mm; }}
  .two h3 {{ font-size: 13pt; color: var(--black); margin-bottom: 4mm;
             font-family: "Archivo Black", "Arial Black", sans-serif;
             font-weight: 400; }}
  .item {{ display: flex; gap: 4mm; margin-bottom: 2.9mm; align-items: baseline; }}
  .item .n {{ font-size: 15pt; color: var(--swamp); width: 8mm; flex: none;
              line-height: 1; }}
  .item h4 {{ font-size: 12.5pt; color: var(--swamp); line-height: 1.15; }}
  .item p {{ font-size: 10.6pt; line-height: 1.26; color: var(--muted);
             margin-top: 0.8mm; }}

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
    </div>
    <img src="{logo}" alt="NZ Army">
  </header>

  <div class="question">
    <div class="lab">The Question</div>
    <div class="q">{question}</div>
  </div>

  <section class="answer">
    <p>{answer}<span class="punch display">{punch}</span></p>
  </section>

  <h2 class="display"><span class="lab">The Model</span>How to decide where to use AI</h2>
  <div class="chevrons">
{chevrons}
  </div>
  <div class="questions">
{questions}
  </div>
  <div class="test">{test}</div>

  <div class="band">
    <div class="lab">How much human control</div>
    <div class="expr display">{assurance}</div>
    <div class="tests">{tests}</div>
  </div>
  <div class="different">{different}</div>

  <div class="tiles-lab lab">Priority areas to test</div>
  <div class="tiles">
{tiles}
  </div>

  <h2 class="display"><span class="lab">The Implications</span>Army People</h2>
  <div class="people">
{people}
  </div>

  <div class="two">
    <div>
      <h3>The Principles</h3>
{principles}
    </div>
    <div>
      <h3>Priority Actions</h3>
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
