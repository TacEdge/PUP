#!/usr/bin/env python3
"""
Build the web version of the NZ Army 'Performance Under Pressure and Combat
Mindset' capability note: one self-contained, GitHub Pages-ready HTML page.

Layout/typesetting only — the source text in SOURCE_FILE is reproduced
verbatim. The single permitted editorial change: inline filename citations
are replaced with sequential superscript markers linking to a 'Source
Documents' list at the end (with back-links).
"""

import base64
import html
import re

# ----------------------------------------------------------------- CONFIG ---
SOURCE_FILE        = "./capability-note.md"
LOGO_FILE          = "./assets/nz-army-logo.png"
LOGO_REVERSED_FILE = ""                       # not supplied — use white plate
OUTPUT_FILE        = "./index.html"
BRAND_PAGE_LINK    = ""                       # nz-army-brand-components.html not in repo
PDF_DOWNLOAD_PATH  = "./output/capability-note.pdf"
SITE_TITLE         = "Performance Under Pressure & Combat Mindset"
PROTECTIVE_MARKING = "UNCLASSIFIED"
DOCUMENT_REFERENCE = "NZALC 2026"
DATE               = "____ 2026"
ORIGINATOR         = "Major M Coom, Chief Instructor, New Zealand Army Leadership Centre"
VERSION            = "Draft v0.2"
SUBTITLE           = "Draft Capability Note"

# Brand palette (NZDF Visual Identity Standards — NZ Army)
ARMY_RED      = "#C62026"
DARKEST_HOUR  = "#000000"
RUAPEHU_WHITE = "#FFFFFF"
SWAMP_GREEN   = "#002516"
KAWAKAWA_LEAF = "#3A4B00"
WAIOURU_HILLS = "#A89662"
MOAWHANGO     = "#CDD2B7"

CITATION_FILES = [
    "PUP Workbook.pdf",
    "LSYS (Officers) Workbook_May 26.pdf",
    "ELDA Lead Leaders Workbook (LPR).pdf",
    "Lead Self Workbook (TAD) 2026.pdf",
    "Lead Teams Workbook.pdf",
    "LDS LEAD LEADERS WORKBOOK.pdf",
]
CITATION_RE = re.compile(
    r"\s*(" + "|".join(re.escape(f) for f in CITATION_FILES) + r")")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")

SECTION_IDS = {
    "Purpose": "purpose",
    "1. Context": "context",
    "2. The problem Army is attempting to solve": "problem",
    "3. Proposed terminology": "terminology",
    "4. Desired Army effect": "desired-effect",
    "5. Current NZALC capability": "current-capability",
    "6. Current assessment": "assessment",
    "7. Proposed future-state vision": "vision",
    "8. Proposed ownership and stakeholder framework": "ownership",
    "9. Capability lifecycle": "lifecycle",
    "10. Recommendation": "recommendation",
    "11. Proposed immediate outputs": "outputs",
    "12. Conclusion": "conclusion",
}

# ------------------------------------------------------------- references ---

footnote_order = []           # unique filenames, order of first appearance
occurrences = {}              # filename -> list of marker anchor ids


def esc(s):
    return html.escape(s, quote=False)


def render_inline(text):
    """Escape text, convert **bold** spans and citation filenames."""
    out = []
    pos = 0
    for m in CITATION_RE.finditer(text):
        out.append(_bold(esc(text[pos:m.start()])))
        fname = m.group(1)
        if fname not in footnote_order:
            footnote_order.append(fname)
            occurrences[fname] = []
        n = footnote_order.index(fname) + 1
        letter = chr(ord("a") + len(occurrences[fname]))
        anchor = f"ref-{n}-{letter}"
        occurrences[fname].append(anchor)
        out.append(
            f'<sup class="ref"><a id="{anchor}" href="#src-{n}" '
            f'aria-label="Source document {n}">{n}</a></sup>')
        pos = m.end()
    out.append(_bold(esc(text[pos:])))
    return "".join(out)


def _bold(escaped):
    return BOLD_RE.sub(r"<strong>\1</strong>", escaped)


# ------------------------------------------------------------------ parse ---

with open(SOURCE_FILE, encoding="utf-8") as fh:
    lines = fh.read().splitlines()

body = []          # html fragments
nav = []           # (id, label)
section_open = False
i = 0


def close_section():
    global section_open
    if section_open:
        body.append("</section>")
        section_open = False


while i < len(lines):
    line = lines[i]
    s = line.strip()

    if not s:
        i += 1
        continue

    if line.startswith("# ") or s == "*Draft Capability Note*":
        i += 1
        continue

    if s == "---":
        body.append('<hr>')
        i += 1
        continue

    if line.startswith("## "):
        text = line[3:].strip()
        close_section()
        sid = SECTION_IDS[text]
        nav.append((sid, text))
        m = re.match(r"^(\d+)\.\s+(.*)$", text)
        if m:
            heading = (f'<span class="num">{m.group(1)}</span>'
                       f'<span>{esc(m.group(2))}</span>')
            body.append(f'<section id="{sid}" class="doc-section">'
                        f'<h2 class="numbered">{heading}</h2>')
        else:
            body.append(f'<section id="{sid}" class="doc-section">'
                        f'<h2>{esc(text)}</h2>')
        section_open = True
        i += 1
        continue

    if line.startswith("### "):
        body.append(f"<h3>{render_inline(line[4:].strip())}</h3>")
        i += 1
        continue

    if line.startswith(">! "):
        block = []
        while i < len(lines) and lines[i].startswith(">! "):
            block.append(render_inline(lines[i][3:].strip()))
            i += 1
        cls = "callout arrows" if "→" in "".join(block) else "callout"
        body.append(f'<p class="{cls}">' + "<br>".join(block) + "</p>")
        continue

    if line.startswith("> "):
        block = []
        while i < len(lines) and lines[i].startswith("> "):
            block.append(render_inline(lines[i][2:].strip()))
            i += 1
        body.append('<p class="display">' + "<br>".join(block) + "</p>")
        continue

    if line.startswith("* "):
        items = []
        while i < len(lines) and lines[i].startswith("* "):
            items.append(f"<li>{render_inline(lines[i][2:].strip())}</li>")
            i += 1
        body.append('<ul class="marked">' + "".join(items) + "</ul>")
        continue

    m = re.match(r"^(\d+)\. (.*)$", line)
    if m:
        items = []
        while i < len(lines):
            m = re.match(r"^(\d+)\. (.*)$", lines[i])
            if not m:
                break
            lead = render_inline(m.group(2).strip())
            i += 1
            cont = ""
            if i < len(lines) and lines[i].startswith("   ") and lines[i].strip():
                cont = f"<p>{render_inline(lines[i].strip())}</p>"
                i += 1
            items.append(f'<li><p class="lead">{lead}</p>{cont}</li>')
        body.append('<ol class="rec">' + "".join(items) + "</ol>")
        continue

    body.append(f"<p>{render_inline(s)}</p>")
    i += 1

close_section()

# Source Documents section
src_items = []
for n, fname in enumerate(footnote_order, start=1):
    backs = " ".join(
        f'<a class="backref" href="#{a}" aria-label="Back to reference '
        f'{n}{a.rsplit("-", 1)[1]}">↩<span class="bl">{a.rsplit("-", 1)[1]}</span></a>'
        for a in occurrences[fname])
    src_items.append(
        f'<li id="src-{n}"><code>{esc(fname)}</code> — internal NZALC '
        f'workbook. {backs}</li>')

nav.append(("sources", "Source Documents"))
download_html = ""
if PDF_DOWNLOAD_PATH:
    download_html = (
        f'<p class="download"><a class="btn" href="{PDF_DOWNLOAD_PATH}" '
        f'download>Download the paper (PDF)</a></p>')

body.append(
    '<hr><section id="sources" class="doc-section"><h2>Source Documents</h2>'
    '<ol class="sources">' + "".join(src_items) + "</ol>"
    + download_html + "</section>")

body_html = "\n".join(body)
nav_html = "".join(
    f'<li><a href="#{sid}">{esc(label)}</a></li>' for sid, label in nav)

# Trim the logo's transparent margins so its visible ink left-aligns with
# the text column, then embed it.
import io
from PIL import Image
_logo = Image.open(LOGO_FILE).convert("RGBA")
_logo = _logo.crop(_logo.getchannel("A").getbbox())
LOGO_W, LOGO_H = _logo.size
_buf = io.BytesIO()
_logo.save(_buf, "PNG")
logo_b64 = base64.b64encode(_buf.getvalue()).decode()

meta_line = " · ".join([DOCUMENT_REFERENCE, ORIGINATOR, VERSION])

brand_link_html = ""
if BRAND_PAGE_LINK:
    brand_link_html = (f'<p><a class="footer-link" href="{BRAND_PAGE_LINK}">'
                       f"NZ Army brand components</a></p>")

# ------------------------------------------------------------------- page ---

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(SITE_TITLE)} — {esc(SUBTITLE)}</title>
<link rel="manifest" href="./manifest.webmanifest">
<meta name="theme-color" content="{SWAMP_GREEN}">
<link rel="icon" href="./icons/icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="./icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="NZ Army PUP">
<style>
:root {{
  --red: {ARMY_RED};
  --black: {DARKEST_HOUR};
  --white: {RUAPEHU_WHITE};
  --swamp: {SWAMP_GREEN};
  --kawakawa: {KAWAKAWA_LEAF};
  --waiouru: {WAIOURU_HILLS};
  --moawhango: {MOAWHANGO};
  --sans: "Helvetica Neue", Helvetica, Arial, "Segoe UI", Roboto, system-ui, sans-serif;
  --serif: "Book Antiqua", "Palatino Linotype", Palatino, Georgia, serif;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}}
* {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; }}
@media (prefers-reduced-motion: no-preference) {{
  html {{ scroll-behavior: smooth; }}
}}
body {{
  margin: 0;
  background: var(--white);
  color: var(--black);
  font-family: var(--serif);
  font-size: 1.0625rem;
  line-height: 1.7;
}}
.skip {{
  position: absolute; left: -9999px; top: 0;
  background: var(--red); color: var(--white);
  font-family: var(--sans); font-weight: 700;
  padding: .6rem 1rem; z-index: 10;
}}
.skip:focus {{ left: 0; }}
:focus-visible {{ outline: 3px solid var(--red); outline-offset: 2px; }}

.marking {{
  background: var(--black); color: var(--white);
  font-family: var(--sans); font-weight: 700;
  font-size: .72rem; letter-spacing: .32em; text-transform: uppercase;
  text-align: center; padding: .35rem .5rem .35rem .82em;
}}

/* --------------------------------------------------------- masthead ---- */
.logo-band {{
  background: var(--white);
  padding: 1.3rem 0 1.1rem;
}}
.logo-band img {{ display: block; width: 13.5rem; max-width: 60%; height: auto; }}
.masthead {{
  background: var(--swamp); color: var(--white);
  border-bottom: 6px solid var(--red);
  padding: 2rem 0 2.4rem;
}}
.wrap {{ max-width: 72rem; margin: 0 auto; padding: 0 1.25rem; }}
.eyebrow {{
  font-family: var(--mono); font-size: .8rem; letter-spacing: .18em;
  text-transform: uppercase; color: var(--moawhango); margin: 0 0 1.4rem;
}}
.masthead h1 {{
  font-family: var(--sans); font-weight: 800;
  font-size: clamp(1.7rem, 4.5vw, 3rem); line-height: 1.12;
  letter-spacing: -.01em; margin: 0 0 .6rem; color: var(--white);
}}
.subtitle {{
  font-family: var(--sans); font-size: 1.05rem;
  color: var(--moawhango); margin: 0 0 1.3rem;
}}
.meta {{
  font-family: var(--mono); font-size: .78rem; line-height: 1.7;
  color: var(--moawhango); margin: 0; max-width: 60ch;
}}

/* ----------------------------------------------------------- layout ---- */
.layout {{ display: block; padding-top: 2rem; padding-bottom: 3rem; }}
.toc {{ margin-bottom: 2rem; }}
.toc summary {{
  font-family: var(--sans); font-weight: 700; font-size: .95rem;
  cursor: pointer; color: var(--swamp);
  border-left: 5px solid var(--red); padding-left: .7rem;
}}
.toc ol {{
  list-style: none; margin: .9rem 0 0; padding: 0 0 0 1.2rem;
  border-left: 1px solid var(--waiouru);
}}
.toc li {{ margin: 0 0 .1rem; }}
.toc a {{
  display: block; font-family: var(--sans); font-size: .84rem;
  line-height: 1.45; text-decoration: none; color: var(--black);
  padding: .22rem .5rem; border-left: 3px solid transparent;
  margin-left: -1.25rem; padding-left: 1.2rem;
}}
.toc a:hover {{ color: var(--red); }}
.toc a.active {{ border-left-color: var(--red); color: var(--red); font-weight: 700; }}
main {{ min-width: 0; }}
article {{ max-width: 70ch; }}

@media (min-width: 68rem) {{
  .layout {{
    display: grid; grid-template-columns: 16.5rem minmax(0, 1fr);
    gap: 3.2rem; align-items: start;
  }}
  .toc {{ position: sticky; top: 1.4rem; margin-bottom: 0; }}
  .toc summary {{ pointer-events: none; }}
  .toc summary::-webkit-details-marker, .toc summary::marker {{ content: ""; display: none; }}
}}

/* ------------------------------------------------------------- body ---- */
h2 {{
  font-family: var(--sans); font-weight: 800; font-size: 1.45rem;
  line-height: 1.25; color: var(--swamp);
  margin: 2.6rem 0 1rem; scroll-margin-top: 1.2rem;
  display: flex; align-items: baseline; gap: .7rem;
}}
h2 .num {{
  flex: none; align-self: center;
  font-family: var(--mono); font-weight: 700; font-size: .95rem;
  background: var(--red); color: var(--white);
  min-width: 2rem; text-align: center; padding: .25rem .35rem;
}}
h2.numbered > span:last-child {{ display: block; }}
section > h2:first-child {{ margin-top: 1rem; }}
h3 {{
  font-family: var(--sans); font-weight: 700; font-size: 1.02rem;
  color: var(--black); margin: 1.9rem 0 .5rem;
}}
p {{ margin: 0 0 1rem; }}
hr {{
  border: 0; border-top: 1px solid var(--waiouru);
  margin: 2.6rem 0;
}}
.display {{
  font-style: italic; margin: 1.2rem 0 1.2rem;
  padding-left: 1.4rem; border-left: 1px solid var(--waiouru);
}}
.callout {{
  background: var(--moawhango); border-left: 6px solid var(--red);
  font-weight: 700; padding: .95rem 1.2rem; margin: 1.4rem 0;
}}
.callout.arrows {{ font-family: var(--sans); letter-spacing: .02em; }}
ul.marked {{ margin: 0 0 1.2rem; padding-left: 1.5rem; }}
ul.marked li {{ margin: 0 0 .35rem; padding-left: .3rem; }}
ul.marked li::marker {{ color: var(--red); }}
ol.rec {{ margin: 0 0 1.2rem; padding-left: 1.7rem; }}
ol.rec li {{ margin: 0 0 1rem; padding-left: .4rem; }}
ol.rec li::marker {{ color: var(--red); font-family: var(--sans); font-weight: 700; }}
ol.rec .lead {{ margin-bottom: .25rem; }}
ol.rec p {{ margin-bottom: .25rem; }}
sup.ref {{ line-height: 0; }}
sup.ref a {{
  font-family: var(--sans); font-size: .72em; font-weight: 700;
  color: var(--red); text-decoration: none; padding: 0 .1em;
}}
sup.ref a:hover {{ text-decoration: underline; }}
ol.sources {{ margin: 0 0 1.6rem; padding-left: 1.7rem; }}
ol.sources li {{ margin: 0 0 .6rem; padding-left: .4rem; scroll-margin-top: 1.2rem; }}
ol.sources li::marker {{ color: var(--red); font-family: var(--sans); font-weight: 700; }}
ol.sources code {{ font-family: var(--mono); font-size: .88em; }}
.backref {{
  font-family: var(--sans); font-size: .8em; color: var(--red);
  text-decoration: none; margin-left: .25rem;
}}
.backref .bl {{ font-size: .78em; vertical-align: super; }}
.backref:hover {{ text-decoration: underline; }}
a {{ color: var(--red); }}
.download {{ margin-top: 2rem; }}
.btn {{
  display: inline-block; background: var(--red); color: var(--white);
  font-family: var(--sans); font-weight: 700; font-size: .95rem;
  text-decoration: none; padding: .75rem 1.3rem;
}}
.btn:hover {{ background: var(--black); }}

/* ----------------------------------------------------------- footer ---- */
footer {{
  background: var(--swamp); color: var(--moawhango);
  border-top: 6px solid var(--red);
  font-family: var(--sans); padding: 2rem 0 2.4rem; margin-top: 2rem;
}}
footer .marking-line {{
  font-weight: 700; font-size: .72rem; letter-spacing: .32em;
  text-transform: uppercase; color: var(--white); margin: 0 0 .8rem;
}}
footer .ref-line {{
  font-family: var(--mono); font-size: .78rem; margin: 0 0 1.4rem;
}}
footer .force {{
  font-weight: 800; font-size: .95rem; letter-spacing: .14em;
  text-transform: uppercase; color: var(--white); margin: 0;
}}
footer .force span {{ display: block; color: var(--moawhango); }}
.footer-link {{ color: var(--moawhango); }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="marking" role="note" aria-label="Protective marking">{esc(PROTECTIVE_MARKING)}</div>

<header>
  <div class="logo-band">
    <div class="wrap">
      <img src="data:image/png;base64,{logo_b64}"
           alt="Ngāti Tūmatauenga — New Zealand Army" width="{LOGO_W}" height="{LOGO_H}">
    </div>
  </div>
  <div class="masthead">
    <div class="wrap">
      <h1>{esc(SITE_TITLE)}</h1>
      <p class="subtitle">{esc(SUBTITLE)}</p>
      <p class="meta">{esc(meta_line)}</p>
    </div>
  </div>
</header>

<div class="layout wrap">
  <nav class="toc" aria-label="Contents">
    <details id="tocD">
      <summary>Contents</summary>
      <ol>{nav_html}</ol>
    </details>
  </nav>
  <main id="main">
    <article>
{body_html}
    </article>
  </main>
</div>

<footer>
  <div class="wrap">
    <p class="marking-line">{esc(PROTECTIVE_MARKING)}</p>
    <p class="ref-line">{esc(DOCUMENT_REFERENCE)}</p>
    <p class="force"><span lang="mi">Hei Mana mō Aotearoa</span>A Force for New Zealand</p>
    {brand_link_html}
  </div>
</footer>

<script>
(function () {{
  var toc = document.getElementById('tocD');
  var mq = window.matchMedia('(min-width: 68rem)');
  function sync() {{ toc.open = mq.matches; }}
  sync();
  if (mq.addEventListener) {{ mq.addEventListener('change', sync); }}

  if ('IntersectionObserver' in window) {{
    var links = {{}};
    document.querySelectorAll('.toc a[href^="#"]').forEach(function (a) {{
      links[a.getAttribute('href').slice(1)] = a;
    }});
    var current = null;
    var io = new IntersectionObserver(function (entries) {{
      entries.forEach(function (e) {{
        if (e.isIntersecting) {{
          if (current) {{ current.classList.remove('active'); }}
          current = links[e.target.id];
          if (current) {{ current.classList.add('active'); }}
        }}
      }});
    }}, {{ rootMargin: '0px 0px -70% 0px', threshold: 0 }});
    document.querySelectorAll('section.doc-section').forEach(function (s) {{
      io.observe(s);
    }});
  }}

  if ('serviceWorker' in navigator && location.protocol !== 'file:') {{
    navigator.serviceWorker.register('./sw.js');
  }}
}})();
</script>
</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
    fh.write(page)

print(f"Saved {OUTPUT_FILE}")
print(f"Sections in nav: {len(nav)} (incl. Purpose and Source Documents)")
print(f"References: {len(footnote_order)} unique source documents, "
      f"{sum(len(v) for v in occurrences.values())} markers")
