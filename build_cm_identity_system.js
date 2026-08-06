// NZ ARMY COMBAT MINDSET : visual identity system.
//
// A subordinate identity system for an Army capability framework, developed
// against the NZDF and NZ Army Visual Identity Guidelines v1.0 (April 2018).
// No new logo is created. The system is typographic and structural: a
// wordmark, a graphic grammar, a notation family, and rules for their use.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

// ---- palette, as published (Army guidelines p58) ---------------------------
const BLACK = "000000";     // Process Black C
const RED = "D31145";       // Pantone 200 C
const WHITE = "FFFFFF";
const G_LIGHT = "DFD8AD";   // 5855 C
const G_MID = "B3A650";     // 5853 C
const G_OLIVE = "444D06";   // 5747 C
const G_DARK = "00261B";    // 5605 C
const INK = "1A1A1A";
const GREY = "6E6E6E";
const RULE = "D2D2D2";
const PAPER = "F5F5F3";

const F = "Arial";          // Neue Haas Grotesk in production
const LOGO = "assets/nz-army-logo.png";
const LOGO_AR = 4.38;

const svg = async (body, w, h, px) => {
  const s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}">${body}</svg>`;
  const buf = await sharp(Buffer.from(s)).resize(px, Math.round((px * h) / w)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
};

// =========================================================================
// GRAPHIC GRAMMAR : the drawings that carry the argument
// =========================================================================

// CONCEPT A, DATUM. A held reference line. Load displaces it; it returns to
// true. Every measurement in the system is taken against this line.
function datumFigure() {
  const w = 900, h = 220, y = 130;
  let ticks = "";
  for (let x = 40; x <= 860; x += 40) {
    const major = (x - 40) % 160 === 0;
    ticks += `<line x1="${x}" y1="${y}" x2="${x}" y2="${y + (major ? 16 : 8)}" stroke="#${RULE}" stroke-width="2"/>`;
  }
  // the trace: true, displaced under load, returned to true
  let d = `M40,${y}`;
  for (let x = 40; x <= 860; x += 4) {
    const t = (x - 300) / 200;
    const load = x > 300 && x < 700 ? Math.exp(-t * t * 1.1) : 0;
    const noise = load * 26 * Math.sin((x - 300) / 17);
    d += ` L${x},${(y - load * 34 + noise).toFixed(1)}`;
  }
  return {
    body: `<rect width="${w}" height="${h}" fill="#${WHITE}"/>
      ${ticks}
      <line x1="40" y1="${y}" x2="860" y2="${y}" stroke="#${INK}" stroke-width="2.5"/>
      <rect x="300" y="34" width="400" height="${y - 34}" fill="#${INK}" opacity="0.04"/>
      <line x1="300" y1="34" x2="300" y2="${y}" stroke="#${GREY}" stroke-width="1.6" stroke-dasharray="5 5"/>
      <line x1="700" y1="34" x2="700" y2="${y}" stroke="#${GREY}" stroke-width="1.6" stroke-dasharray="5 5"/>
      <path d="${d}" fill="none" stroke="#${INK}" stroke-width="3"/>`,
    w, h,
  };
}

// CONCEPT B, THRESHOLD. Pressure as an accumulating field that stops at a
// held edge. Drawn from the Army halftone chevron pattern.
function thresholdFigure() {
  const w = 900, h = 220, edge = 560, step = 13;
  let dots = "";
  for (let y = 24; y < h - 20; y += step) {
    for (let x = 40; x < edge; x += step) {
      const t = (x - 40) / (edge - 40);
      const r = 0.8 + 3.4 * Math.pow(t, 1.9);
      dots += `<circle cx="${x}" cy="${y}" r="${r.toFixed(2)}" fill="#${INK}"/>`;
    }
  }
  return {
    body: `<rect width="${w}" height="${h}" fill="#${WHITE}"/>${dots}
      <rect x="${edge}" y="24" width="6" height="${h - 44}" fill="#${RED}"/>
      <line x1="${edge + 40}" y1="${h / 2}" x2="840" y2="${h / 2}" stroke="#${INK}" stroke-width="2.5"/>`,
    w, h,
  };
}

// CONCEPT C, TRACE. One resolved path through a field of competing signal.
function traceFigure() {
  const w = 900, h = 220;
  let noise = "";
  for (let i = 0; i < 26; i++) {
    const y0 = 30 + (i * 37) % 160;
    let d = `M40,${y0}`;
    for (let x = 40; x <= 860; x += 30) {
      d += ` L${x},${(y0 + Math.sin((x + i * 90) / 46) * 26 + ((i * 13) % 17) - 8).toFixed(1)}`;
    }
    noise += `<path d="${d}" fill="none" stroke="#${INK}" stroke-width="1" opacity="0.13"/>`;
  }
  const nodes = [130, 330, 530, 730].map(
    (x) => `<circle cx="${x}" cy="110" r="7" fill="#${WHITE}" stroke="#${RED}" stroke-width="3"/>`
  ).join("");
  return {
    body: `<rect width="${w}" height="${h}" fill="#${WHITE}"/>${noise}
      <line x1="40" y1="110" x2="860" y2="110" stroke="#${INK}" stroke-width="3"/>${nodes}`,
    w, h,
  };
}

// The recommended system: datum as spine, trace nodes as the active element,
// threshold density reserved for texture only.
function systemFigure() {
  const w = 900, h = 260, y = 150;
  let ticks = "";
  for (let x = 40; x <= 860; x += 40)
    ticks += `<line x1="${x}" y1="${y}" x2="${x}" y2="${y + ((x - 40) % 160 === 0 ? 16 : 8)}" stroke="#${RULE}" stroke-width="2"/>`;
  let field = "";
  for (let yy = 40; yy < y - 14; yy += 13)
    for (let x = 620; x < 860; x += 13) {
      const t = (x - 620) / 240;
      field += `<circle cx="${x}" cy="${yy}" r="${(0.6 + 2.4 * t * t).toFixed(2)}" fill="#${INK}" opacity="0.5"/>`;
    }
  const labels = [
    [130, "DEFINE"], [310, "UNDERSTAND"], [490, "DESIGN"], [670, "VALIDATE"], [830, "IMPLEMENT"],
  ].map(([x, t]) =>
    `<circle cx="${x}" cy="${y}" r="8" fill="#${WHITE}" stroke="#${RED}" stroke-width="3.5"/>
     <text x="${x}" y="${y + 42}" font-family="Arial" font-size="15" fill="#${INK}"
       text-anchor="middle" letter-spacing="1.4">${t}</text>`).join("");
  return {
    body: `<rect width="${w}" height="${h}" fill="#${WHITE}"/>${field}${ticks}
      <line x1="40" y1="${y}" x2="860" y2="${y}" stroke="#${INK}" stroke-width="3"/>${labels}`,
    w, h,
  };
}

// ---- notation family -------------------------------------------------------
// Twelve marks, one grammar. Every mark is built on a common datum at y=17 on
// a 24 unit grid, stroke 2. They are notation, not pictures of things.
const MARKS = {
  framework: `<path d="M2,17 H22"/><path d="M2,7 H22"/><path d="M7,7 V17"/><path d="M12,7 V17"/><path d="M17,7 V17"/>`,
  doctrine: `<path d="M2,17 H22"/><rect x="2" y="8" width="20" height="4" fill="currentColor" stroke="none"/>`,
  policy: `<path d="M2,17 H22"/><path d="M2,4 H22"/><rect x="2" y="9" width="20" height="4" fill="currentColor" stroke="none"/>`,
  evidence: `<path d="M2,17 H22"/><path d="M6,17 V13"/><path d="M11,17 V10"/><path d="M16,17 V7"/><path d="M21,17 V4"/>`,
  research: `<path d="M2,17 H22"/><path d="M7,4 H3 V13 H7"/><path d="M11,8 H22" stroke-dasharray="3 3"/>`,
  product: `<path d="M2,17 H22"/><rect x="8" y="8" width="9" height="9" fill="currentColor" stroke="none"/>`,
  assessment: `<path d="M2,17 H22"/><rect x="2" y="8" width="8" height="4" fill="currentColor" stroke="none"/><rect x="14" y="8" width="8" height="4" fill="currentColor" stroke="none"/><path d="M12,5 V15"/>`,
  governance: `<path d="M2,17 H22"/><path d="M6,4 H2 V13 H6"/><path d="M18,4 H22 V13 H18"/><rect x="9" y="7" width="6" height="4" fill="currentColor" stroke="none"/>`,
  decision: `<path d="M2,17 H22"/><path d="M12,17 L20,6"/><circle cx="12" cy="17" r="3.2" fill="#FFFFFF"/>`,
  review: `<path d="M2,17 H22"/><path d="M20,14 C20,6 8,6 8,13"/><path d="M5,10 L8,14 L11,10"/>`,
  risk: `<path d="M2,17 H10"/><path d="M14,17 H22"/><path d="M12,5 V14"/><circle cx="12" cy="17.6" r="1.8" fill="currentColor" stroke="none"/>`,
  reference: `<path d="M2,17 H22"/><path d="M6,17 V9"/><rect x="15" y="12" width="5" height="5" fill="currentColor" stroke="none"/>`,
};

// Four families. The colour is the classification, not decoration.
const TYPES = [
  ["FRAMEWORK", "framework", BLACK, "Structure", "The governing architecture. Used once, at the top of a hierarchy."],
  ["DOCTRINE", "doctrine", BLACK, "Structure", "Endorsed and enduring. The bar is solid because doctrine does not qualify itself."],
  ["POLICY", "policy", BLACK, "Structure", "Bounded above and below: the convention for rules that carry limits."],
  ["GOVERNANCE", "governance", BLACK, "Structure", "Brackets on both sides. Something is being held, not merely described."],
  ["EVIDENCE", "evidence", G_DARK, "Analysis", "Rising measures. Evidence accumulates and is read against the datum."],
  ["RESEARCH", "research", G_DARK, "Analysis", "An open bracket and a dashed continuation. The question is not yet closed."],
  ["ASSESSMENT", "assessment", G_DARK, "Analysis", "A measured gap. Assessment is the act of reading the interval."],
  ["REVIEW", "review", G_DARK, "Analysis", "A return to a prior point. Review is deliberate, not repetition."],
  ["PRODUCT", "product", G_OLIVE, "Delivery", "A discrete block on the datum. Products are countable and can be held."],
  ["REFERENCE", "reference", G_OLIVE, "Delivery", "A single tick and a marker. Points elsewhere; carries no authority itself."],
  ["DECISION", "decision", RED, "Action", "A node and a departure. The only mark that leaves the datum."],
  ["RISK", "risk", RED, "Action", "A break in the datum identifies risk. A reading convention, not a definition."],
];

const markSvg = (key, colour, px = 96) =>
  svg(`<g fill="none" stroke="#${colour}" stroke-width="2" stroke-linecap="square"
        color="#${colour}">${MARKS[key]}</g>`, 24, 24, px);

// ---- supporting diagrams ---------------------------------------------------
function motionCurve() {
  const w = 420, h = 260;
  return {
    body: `<rect width="${w}" height="${h}" fill="#${WHITE}"/>
      <line x1="50" y1="220" x2="390" y2="220" stroke="#${RULE}" stroke-width="2"/>
      <line x1="50" y1="220" x2="50" y2="40" stroke="#${RULE}" stroke-width="2"/>
      <path d="M50,220 C118,220 118,60 390,60" fill="none" stroke="#${RED}" stroke-width="3.5"/>
      <path d="M50,220 C160,-20 280,300 390,60" fill="none" stroke="#${INK}" stroke-width="1.6"
        stroke-dasharray="5 5" opacity="0.45"/>
      <text x="60" y="34" font-family="Arial" font-size="15" fill="#${RED}">cubic-bezier(0.2, 0, 0, 1)</text>
      <text x="60" y="250" font-family="Arial" font-size="14" fill="#${GREY}">dashed: overshoot, rejected</text>`,
    w, h,
  };
}

function gridDiagram() {
  const w = 420, h = 260;
  let cols = "";
  for (let i = 0; i < 6; i++) {
    const x = 40 + i * 58;
    cols += `<rect x="${x}" y="30" width="42" height="200" fill="#${RED}" opacity="0.07"/>`;
  }
  return {
    body: `<rect width="${w}" height="${h}" fill="#${WHITE}"/>${cols}
      <line x1="40" y1="30" x2="380" y2="30" stroke="#${INK}" stroke-width="2.5"/>
      <line x1="40" y1="230" x2="380" y2="230" stroke="#${INK}" stroke-width="2.5"/>
      <line x1="40" y1="96" x2="380" y2="96" stroke="#${RULE}" stroke-width="1.6"/>
      <line x1="40" y1="163" x2="380" y2="163" stroke="#${RULE}" stroke-width="1.6"/>
      <text x="40" y="252" font-family="Arial" font-size="14" fill="#${GREY}">6 columns, 3 registers, one datum</text>`,
    w, h,
  };
}

function proportionBar() {
  const w = 900, h = 64;
  const seg = [[BLACK, 0.46, "STRUCTURE"], [WHITE, 0.34, "SPACE"], [G_DARK, 0.15, "CLASSIFICATION"], [RED, 0.05, "ACTION"]];
  let x = 0, out = "";
  seg.forEach(([c, f, t]) => {
    const ww = w * f;
    out += `<rect x="${x}" y="0" width="${ww}" height="34" fill="#${c}" ${c === WHITE ? `stroke="#${RULE}" stroke-width="2"` : ""}/>
      <text x="${x + 4}" y="54" font-family="Arial" font-size="14" fill="#${GREY}">${t} ${Math.round(f * 100)}%</text>`;
    x += ww;
  });
  return { body: `<rect width="${w}" height="${h}" fill="#${WHITE}"/>${out}`, w, h };
}

function horizons() {
  const w = 900, h = 250;
  const bands = [
    ["NOW  2026 to 2028", "Specification issued. Wordmark, grammar, notation, colour, templates.", 300, BLACK],
    ["NEXT  2029 to 2032", "Notation extended as new content types appear. No redesign.", 600, G_DARK],
    ["ENDURING  2033 to 2046", "Typeface and medium may change. The grammar does not.", 900, G_OLIVE],
  ];
  let out = `<line x1="0" y1="16" x2="${w}" y2="16" stroke="#${RULE}" stroke-width="2"/>`;
  bands.forEach(([t, d, len, c], i) => {
    const y = 40 + i * 70;
    out += `<text x="0" y="${y}" font-family="Arial" font-size="16" font-weight="bold"
        fill="#${INK}" letter-spacing="1.2">${t}</text>
      <text x="0" y="${y + 20}" font-family="Arial" font-size="13" fill="#5A5A5A">${d}</text>
      <rect x="0" y="${y + 30}" width="${len}" height="10" fill="#${c}"/>
      <rect x="${len}" y="${y + 30}" width="${w - len}" height="10" fill="#${c}" opacity="0.12"/>`;
  });
  return { body: `<rect width="${w}" height="${h}" fill="#${WHITE}"/>${out}`, w, h };
}

// =========================================================================
(async () => {
  const I = {
    datum: await svg(...Object.values(datumFigure()).slice(0, 1), 900, 220, 1400),
  };
  const mk = async (o, px) => svg(o.body, o.w, o.h, px);
  Object.assign(I, {
    datum: await mk(datumFigure(), 1500),
    threshold: await mk(thresholdFigure(), 1500),
    trace: await mk(traceFigure(), 1500),
    system: await mk(systemFigure(), 1500),
    motion: await mk(motionCurve(), 800),
    grid: await mk(gridDiagram(), 800),
    proportion: await mk(proportionBar(), 1500),
    horizons: await mk(horizons(), 1500),
  });
  const MARK_IMG = {}, MONO_IMG = {};
  for (const [, key, colour] of TYPES) {
    MARK_IMG[key] = await markSvg(key, colour, 120);
    MONO_IMG[key] = await markSvg(key, INK, 120);
  }

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "NZ Army Combat Mindset Visual Identity System";
  pres.subject = "Subordinate identity system for an Army capability framework";
  pres.company = "Army Command School";

  const L = 0.62, W = 7.03, R = L + W;
  let PAGE = 0;
  const SECTIONS = [];

  // ---- furniture ----------------------------------------------------------
  function page(section, title, strap) {
    PAGE += 1;
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText(section.toUpperCase(), { x: L, y: 0.42, w: W - 1.2, h: 0.18, fontFace: F,
      fontSize: 7, bold: true, color: RED, charSpacing: 1.8, align: "left", valign: "middle", margin: 0 });
    s.addText(String(PAGE).padStart(2, "0"), { x: R - 0.6, y: 0.42, w: 0.6, h: 0.18, fontFace: F,
      fontSize: 7, bold: true, color: GREY, align: "right", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L, y: 0.64, w: W, h: 0.012, fill: { color: INK } });
    if (title) {
      s.addText(title, { x: L, y: 0.8, w: W, h: 0.34, fontFace: F, fontSize: 19, bold: true,
        color: INK, align: "left", valign: "middle", margin: 0 });
    }
    if (strap) {
      s.addText(strap, { x: L, y: 1.16, w: W - 0.4, h: 0.42, fontFace: F, fontSize: 9.6,
        color: GREY, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.2 });
    }
    s.addText("COMBAT MINDSET   VISUAL IDENTITY", { x: L, y: 11.16, w: 5, h: 0.16,
      fontFace: F, fontSize: 6, color: GREY, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
    s.addText("DRAFT V0.3   |   AUGUST 2026", { x: R - 3, y: 11.16, w: 3, h: 0.16,
      fontFace: F, fontSize: 6, color: GREY, charSpacing: 0.9, align: "right", valign: "middle", margin: 0 });
    return s;
  }

  const rule = (s, y, colour = RULE, h = 0.008) =>
    s.addShape("rect", { x: L, y, w: W, h, fill: { color: colour } });

  function head(s, y, text) {
    s.addText(text, { x: L, y, w: W, h: 0.2, fontFace: F, fontSize: 7.4, bold: true,
      color: INK, charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
    rule(s, y + 0.2);
    return y + 0.32;
  }

  const body = (s, x, y, w, text, size = 9, colour = INK, h = 0.6) =>
    s.addText(text, { x, y, w, h, fontFace: F, fontSize: size, color: colour,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.22 });

  function bullets(s, x, y, w, items, size = 9, h = 2.0) {
    s.addText(items.map((t) => ({
      text: t,
      options: { breakLine: true, bullet: { characterCode: "2013", indent: 14 }, paraSpaceAfter: 5 },
    })), { x, y, w, h, fontFace: F, fontSize: size, color: INK, align: "left", valign: "top",
      margin: 0, lineSpacingMultiple: 1.22 });
  }

  // =======================================================================
  // 01  COVER
  // =======================================================================
  {
    PAGE += 1;
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addImage({ path: LOGO, x: L, y: 0.94, w: 1.7, h: 1.7 / LOGO_AR });
    s.addImage({ data: I.datum, x: 0, y: 3.2, w: 8.27, h: 8.27 * 220 / 900 });

    s.addText("COMBAT", { x: L, y: 5.5, w: W, h: 0.72, fontFace: F, fontSize: 50, bold: true,
      color: INK, charSpacing: 1.4, align: "left", valign: "middle", margin: 0 });
    s.addText("MINDSET", { x: L, y: 6.2, w: W, h: 0.72, fontFace: F, fontSize: 50, bold: true,
      color: INK, charSpacing: 1.4, align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L, y: 7.0, w: 1.9, h: 0.05, fill: { color: INK } });
    s.addText("Visual identity system", { x: L, y: 7.14, w: W, h: 0.3, fontFace: F, fontSize: 15,
      color: INK, align: "left", valign: "middle", margin: 0 });
    s.addText("A subordinate identity for an Army capability framework, developed against the\nNZDF and NZ Army Visual Identity Guidelines v1.0.", {
      x: L, y: 7.5, w: W - 1.2, h: 0.5, fontFace: F, fontSize: 9.6, color: GREY,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.2 });

    rule(s, 9.5, INK, 0.012);
    const meta = [
      ["Developed by", "Army Command School and NZ Army Leadership Centre,\nfor internal consideration"],
      ["Proposed reviewers", "COMDT ACS; HPC; Head of Visual Identity and Design, Defence Public Affairs"],
      ["Status", "Draft for review. Not an approved standard."],
      ["Version", "V0.3, August 2026"],
    ];
    let my = 9.68;
    meta.forEach(([k, v]) => {
      s.addText(k, { x: L, y: my, w: 1.62, h: 0.34, fontFace: F, fontSize: 8, bold: true,
        color: INK, align: "left", valign: "top", margin: 0 });
      s.addText(v, { x: L + 1.74, y: my, w: W - 1.74, h: 0.34, fontFace: F, fontSize: 8,
        color: GREY, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });
      my += v.includes("\n") ? 0.36 : 0.24;
    });
  }

  // =======================================================================
  // 02  CONTENTS AND THE ARGUMENT
  // =======================================================================
  {
    const s = page("Contents", "What this document argues",
      "Thirteen outputs were requested. They resolve into one argument, set out below, and a specification that follows from it.");

    let y = head(s, 1.78, "THE ARGUMENT IN FOUR STEPS");
    const steps = [
      ["01", "Combat Mindset is not a programme, so programme branding is the wrong precedent.",
        "The guidelines forbid programmes creating logos. Correct, but the more useful observation is that a capability framework is closer to doctrine than to a project. Doctrine has a visual system: format, hierarchy, notation, numbering. That is the precedent to follow."],
      ["02", "The identity must therefore be a grammar, not a mark.",
        "A mark is recognised. A grammar is trusted. Personnel should know a Combat Mindset product by how it is built, not by a badge in the corner."],
      ["03", "The organising idea is signal held under load.",
        "The framework exists because capability degrades under pressure. The visual system should say that, structurally, in every artefact: a datum that is measured, disturbed and returned to true."],
      ["04", "Longevity comes from structure, not style.",
        "Rules, grids, notation and typographic hierarchy survive decades. Gradients, fields and illustrative devices carry a date stamp. The recommendation is built on the first and rations the second."],
    ];
    steps.forEach(([n, h, d]) => {
      s.addText(n, { x: L, y, w: 0.4, h: 0.22, fontFace: F, fontSize: 9, bold: true,
        color: RED, align: "left", valign: "middle", margin: 0 });
      s.addText(h, { x: L + 0.44, y, w: W - 0.44, h: 0.24, fontFace: F, fontSize: 10.4, bold: true,
        color: INK, align: "left", valign: "middle", margin: 0 });
      body(s, L + 0.44, y + 0.24, W - 0.64, d, 8.8, "3E3E3E", 0.62);
      y += 0.94;
    });

    y = head(s, y + 0.16, "STRUCTURE OF THIS DOCUMENT");
    const toc = [
      ["03", "Position and compliance"], ["04", "Identity philosophy"],
      ["05", "Brand attributes"], ["06", "Visual principles"],
      ["07", "Concept A: Datum"], ["08", "Concept B: Threshold"],
      ["09", "Concept C: Trace"], ["10", "Evaluation and recommendation"],
      ["11", "Title treatment explorations"], ["12", "Title treatment specification"],
      ["13", "Graphic language"], ["14", "Notation family"],
      ["15", "Colour system"], ["16", "Information architecture"],
      ["17", "Photography direction"], ["18", "Motion language"],
      ["19", "Digital application"], ["20", "Brand voice"],
      ["21", "Identity evolution"], ["22", "Governance and next steps"],
    ];
    const CW = W / 2;
    toc.forEach(([n, t], i) => {
      const col = i % 2, row = Math.floor(i / 2);
      s.addText(`${n}    ${t}`, { x: L + col * CW, y: y + row * 0.212, w: CW - 0.2, h: 0.2,
        fontFace: F, fontSize: 8.6, color: INK, align: "left", valign: "middle", margin: 0 });
    });
  }

  // =======================================================================
  // 03  POSITION AND COMPLIANCE
  // =======================================================================
  {
    const s = page("Position", "What kind of thing is this?",
      "The single most consequential decision in this document is made here, because it determines what the identity is permitted to be.");

    let y = head(s, 1.86, "THREE POSSIBLE READINGS, AND THEIR CONSEQUENCES");
    const readings = [
      ["AS A PROGRAMME", "Guidelines p34", "No logo. Name in plain text beside the Army logo. Nothing more.",
        "Compliant but inert. Produces no system, and no reason for anyone to trust one product over another.", G_MID],
      ["AS AN ORGANISATION", "Guidelines p9, p54", "A badge or unit patch. Explicitly ruled out for communication use.",
        "Non-compliant, and wrong in substance. Combat Mindset commands nothing and has no establishment.", RED],
      ["DOCTRINE AS PRECEDENT", "The recommended position", "A publication system: format, hierarchy, notation, numbering, classification.",
        "Compliant, and it borrows doctrine's enduring qualities without claiming doctrinal status. What the framework becomes is decided through the programme, not by its identity.", G_DARK],
    ];
    readings.forEach(([t, ref, what, cons, c]) => {
      s.addShape("rect", { x: L, y, w: 0.04, h: 0.96, fill: { color: c } });
      s.addText(t, { x: L + 0.18, y, w: 2.2, h: 0.22, fontFace: F, fontSize: 9.6, bold: true,
        color: INK, charSpacing: 0.8, align: "left", valign: "middle", margin: 0 });
      s.addText(ref, { x: L + 0.18, y: y + 0.21, w: 2.2, h: 0.18, fontFace: F, fontSize: 7.4,
        italic: true, color: GREY, align: "left", valign: "middle", margin: 0 });
      body(s, L + 2.5, y, W - 2.5, what, 9, INK, 0.4);
      body(s, L + 2.5, y + 0.4, W - 2.5, cons, 8.6, "3E3E3E", 0.5);
      y += 1.06;
    });

    y = head(s, y + 0.1, "WHAT FOLLOWS FROM TAKING DOCTRINE AS THE PRECEDENT");
    bullets(s, L, y, W, [
      "No mark, no badge, no patch, no symbol. The identity is carried by typography and structure.",
      "The Army logo appears unaltered on every artefact. Combat Mindset never competes with it.",
      "Authority is signalled the way doctrine signals it: consistent format, visible hierarchy, explicit classification of content, and a reference number on everything.",
      "Every element is specifiable in a written standard, so it can be applied by people who are not designers. This is the practical test the system must pass inside a training establishment.",
    ], 9, 1.5);

    y += 1.6;
    y = head(s, y, "COMPLIANCE POSITION");
    s.addShape("rect", { x: L, y, w: W, h: 1.24, fill: { color: PAPER } });
    body(s, L + 0.22, y + 0.16, W - 0.44,
      "This system creates no new logo and modifies nothing in the NZDF or NZ Army identity. It uses the published Army palette, the published typefaces, and the published graphic elements. It is a subordinate application, in the same sense that a doctrine publication is a subordinate application.",
      8.8, INK, 0.62);
    body(s, L + 0.22, y + 0.76, W - 0.44,
      "It should nonetheless be put to the Head of Visual Identity and Design, Defence Public Affairs, before issue. Adopting a system without that endorsement would repeat the error this document exists to avoid.",
      8.8, GREY, 0.44);
    y += 1.4;

    y = head(s, y, "THE PRECEDENT BEING FOLLOWED");
    const PREC = [
      ["Doctrine publications", "Numbered, classified, formatted identically across decades, and recognisable at a glance without a logo."],
      ["Range cards and orders formats", "Authority carried entirely by structure. Nobody has ever needed to brand a set of orders."],
      ["Map and chart conventions", "A notation learned once and applied everywhere. The reader interprets symbols never seen before."],
    ];
    const PW2 = (W - 2 * 0.14) / 3;
    PREC.forEach(([t, d], i) => {
      const x = L + i * (PW2 + 0.14);
      s.addShape("rect", { x, y, w: PW2, h: 1.0, fill: { color: WHITE }, line: { color: RULE, width: 1 } });
      s.addShape("rect", { x, y, w: PW2, h: 0.028, fill: { color: INK } });
      s.addText(t, { x: x + 0.16, y: y + 0.12, w: PW2 - 0.32, h: 0.36, fontFace: F, fontSize: 8.8,
        bold: true, color: INK, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });
      body(s, x + 0.16, y + 0.5, PW2 - 0.32, d, 7.8, "3E3E3E", 0.44);
    });
    body(s, L, y + 1.14, W,
      "None of these is branded. All of them are instantly recognisable to the people who use them. That is the standard this system is aiming at.",
      8.8, INK, 0.4);
  }

  // =======================================================================
  // 04  IDENTITY PHILOSOPHY
  // =======================================================================
  {
    const s = page("Philosophy", "What Combat Mindset should feel like",
      "Not what it looks like. Feel is the harder specification and the one that determines whether the system is used or quietly abandoned.");

    let y = head(s, 1.86, "THE FEELING TO ACHIEVE");
    const feels = [
      ["It should feel like something that was already there.",
        "Not launched. Not campaigned. A soldier meeting a Combat Mindset product for the first time should assume it has existed for years and that they simply had not needed it until now. Visible novelty is a liability in an enduring capability framework."],
      ["It should feel like it has been checked.",
        "The strongest emotional response the system can produce is the quiet assumption that someone competent has been over this. That is what evidence-based means in practice: not citations on display, but the felt absence of guesswork."],
      ["It should feel calm at the moment the reader is not.",
        "These products will be opened by people under load: before a serial, after a poor performance, during a difficult command decision. The identity must lower the temperature of the page, not raise it."],
      ["It should feel like it respects the reader's time.",
        "Hierarchy that answers questions in the order they are asked. No persuasion, no preamble, no motivational framing. Get to the thing."],
      ["It should feel institutional rather than authored.",
        "No individual's taste should be visible in it. The system belongs to Army, and personal signature is what makes identity systems fragile when their author posts out."],
    ];
    feels.forEach(([h, d]) => {
      s.addText(h, { x: L, y, w: W, h: 0.24, fontFace: F, fontSize: 10.6, bold: true,
        color: INK, align: "left", valign: "middle", margin: 0 });
      body(s, L, y + 0.25, W - 0.3, d, 9, "3E3E3E", 0.66);
      y += 1.02;
    });

    y = head(s, y + 0.06, "WHAT IT MUST NOT FEEL LIKE");
    const nots = [
      ["Inspiring", "Motivation fades. Institutional systems endure."],
      ["Elite", "The framework is for the whole Army, not a selected minority."],
      ["Commercial", "Nothing is being sold. Nothing is being competed for."],
      ["Clever", "Wit in an institutional system reads as unseriousness on the second reading."],
    ];
    const NW = (W - 3 * 0.12) / 4;
    nots.forEach(([t, d], i) => {
      const x = L + i * (NW + 0.12);
      s.addShape("rect", { x, y, w: NW, h: 0.86, fill: { color: PAPER } });
      s.addShape("rect", { x, y, w: NW, h: 0.028, fill: { color: RED } });
      s.addText(t, { x: x + 0.14, y: y + 0.1, w: NW - 0.28, h: 0.22, fontFace: F, fontSize: 9.4,
        bold: true, color: INK, align: "left", valign: "middle", margin: 0 });
      body(s, x + 0.14, y + 0.34, NW - 0.28, d, 8, "3E3E3E", 0.44);
    });
  }

  // =======================================================================
  // 05  BRAND ATTRIBUTES
  // =======================================================================
  {
    const s = page("Attributes", "Brand attributes",
      "Thirteen adjectives. Each is paired with the adjective it is most often confused with, because the distinction is where the system is actually held.");

    let y = head(s, 1.86, "THE ATTRIBUTES, AND THEIR NEAR MISSES");
    const attrs = [
      ["Measured", "not cautious"], ["Precise", "not fussy"],
      ["Composed", "not detached"], ["Disciplined", "not rigid"],
      ["Credible", "not authoritative in tone"], ["Structured", "not bureaucratic"],
      ["Clear", "not simplified"], ["Enduring", "not old"],
      ["Technical", "not cold"], ["Operational", "not tactical in styling"],
      ["Adaptive", "not fashionable"], ["Human", "not warm"],
      ["Unshowy", "not plain"],
    ];
    const AW = (W - 2 * 0.14) / 3;
    attrs.forEach(([a, b], i) => {
      const col = i % 3, row = Math.floor(i / 3);
      const x = L + col * (AW + 0.14), yy = y + row * 0.72;
      s.addShape("rect", { x, y: yy, w: AW, h: 0.6, fill: { color: WHITE },
        line: { color: RULE, width: 1 } });
      s.addShape("rect", { x, y: yy, w: 0.03, h: 0.6, fill: { color: INK } });
      s.addText(a, { x: x + 0.16, y: yy + 0.08, w: AW - 0.3, h: 0.24, fontFace: F, fontSize: 11.4,
        bold: true, color: INK, align: "left", valign: "middle", margin: 0 });
      s.addText(b, { x: x + 0.16, y: yy + 0.32, w: AW - 0.3, h: 0.2, fontFace: F, fontSize: 8.2,
        italic: true, color: RED, align: "left", valign: "middle", margin: 0 });
    });

    y += 5 * 0.72 + 0.1;
    y = head(s, y, "THE TEST");
    s.addShape("rect", { x: L, y, w: W, h: 1.5, fill: { color: INK } });
    s.addText("If an artefact could be mistaken for recruitment material, fitness branding, or a\ncommercial resilience product, it has failed. If it could be mistaken for a well made\ndoctrine publication, it has succeeded.", {
      x: L + 0.3, y: y + 0.24, w: W - 0.6, h: 0.7, fontFace: F, fontSize: 13, bold: true,
      color: WHITE, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.25 });
    s.addText("This is a deliberately low ceiling on expressiveness. It is the correct ceiling for a system that has to survive twenty years and four changes of sponsor.", {
      x: L + 0.3, y: y + 1.06, w: W - 0.6, h: 0.34, fontFace: F, fontSize: 8.6,
      color: "B4B4B4", align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });
  }

  // =======================================================================
  // 06  VISUAL PRINCIPLES
  // =======================================================================
  {
    const s = page("Principles", "Visual principles",
      "Seven principles. Each is written so that a non-designer can apply it and a designer can be held to it.");

    let y = head(s, 1.86, "THE DESIGN LANGUAGE");
    const principles = [
      ["Everything is measured against a line.", "Datum",
        "A single horizontal reference governs each surface. Elements align to it, hang from it or sit on it. Nothing floats. This is the structural expression of the framework's own subject: a standard held under load."],
      ["Structure is visible.", "Legible construction",
        "Rules, columns and registers are shown rather than concealed. The reader can see how the page was built, which is the visual equivalent of showing method."],
      ["Contrast carries hierarchy, not colour.", "High contrast",
        "Black on white, at real weight differences. Colour classifies content; it never ranks it. A page printed on a unit's mono printer must lose nothing."],
      ["Space is a material, not a leftover.", "Measured",
        "Generous, consistent intervals. Density is reserved for texture and never applied to text. Crowding reads as haste, and haste is the opposite of what the framework teaches."],
      ["Direction is meaningful.", "Directional",
        "Movement along the datum means sequence. Departure from the datum means decision. A break in the datum means risk. Direction is never used decoratively."],
      ["Complexity resolves.", "Clarity from complexity",
        "Where a field of competing signal is shown, it must resolve into a single clear element. Unresolved complexity is a picture of the problem, not the framework."],
      ["Restraint is the house style.", "Unshowy",
        "If an element cannot be justified in one sentence in the specification, it is removed. The system should look under-designed to a designer and obvious to a soldier."],
    ];
    principles.forEach(([h, tag, d], i) => {
      s.addText(String(i + 1).padStart(2, "0"), { x: L, y, w: 0.36, h: 0.22, fontFace: F,
        fontSize: 8.6, bold: true, color: RED, align: "left", valign: "middle", margin: 0 });
      s.addText(h, { x: L + 0.4, y, w: W - 1.7, h: 0.22, fontFace: F, fontSize: 10.4, bold: true,
        color: INK, align: "left", valign: "middle", margin: 0 });
      s.addText(tag.toUpperCase(), { x: R - 1.5, y, w: 1.5, h: 0.22, fontFace: F, fontSize: 7,
        bold: true, color: GREY, charSpacing: 1.2, align: "right", valign: "middle", margin: 0 });
      body(s, L + 0.4, y + 0.23, W - 0.6, d, 8.8, "3E3E3E", 0.56);
      y += 0.96;
    });

    s.addImage({ data: I.grid, x: L, y: 9.3, w: 2.8, h: 2.8 * 260 / 420 });
    s.addText("The page is built from six columns and three registers, all hung from a single datum. Every surface in the system, printed or digital, is a variation on this construction.", {
      x: L + 3.0, y: 9.4, w: W - 3.0, h: 1.2, fontFace: F, fontSize: 8.8, color: "3E3E3E",
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.22 });
  }

  // =======================================================================
  // 07 to 09  THREE CONCEPTS
  // =======================================================================
  const CONCEPTS = [
    {
      key: "A", name: "DATUM", img: () => I.datum,
      line: "A standard is held. Load displaces it. It returns to true.",
      idea: "The page is governed by a single measured reference line. Content aligns to it. Where pressure is represented, the line deviates and then recovers. Ticks, registers and intervals come from the language of instruments, maps and range cards.",
      says: "This is what the framework is for. Capability is not lost under pressure; access to it is temporarily displaced, and the system exists to shorten the return.",
      strengths: [
        "Structural rather than illustrative, so it dates slowly. A ruled line with tick marks is as legible in 2046 as in 1946.",
        "Scales without loss from a favicon to a wall, because it is composed of rules rather than detail.",
        "Applies to non-designers. A datum and a tick interval can be specified in words and reproduced in Word, PowerPoint, HTML and print.",
        "Reads as instrumentation, which is the correct register for an evidence-based capability framework.",
      ],
      risks: [
        "Quiet to the point of invisibility if applied timidly. Requires real weight contrast to carry a cover.",
        "Adjacent to financial and engineering identities. Distinctiveness must come from typography and colour discipline, not from the line itself.",
      ],
      colour: G_DARK,
    },
    {
      key: "B", name: "THRESHOLD", img: () => I.threshold,
      line: "Pressure accumulates. The line holds. Beyond it, clarity.",
      idea: "Pressure is drawn as an accumulating density field, built from the Army halftone chevron pattern. The field intensifies towards a hard edge and stops. Beyond the edge the surface is clear and ordered.",
      says: "The framework is the threshold. It is what stands between accumulating load and the collapse of performance.",
      strengths: [
        "The most emotionally direct of the three. A reader grasps it without explanation.",
        "Uses an existing sanctioned Army element, so it is already inside the visual family.",
        "Produces striking covers and divider surfaces with very little effort.",
      ],
      risks: [
        "Density gradients are a period signature. They read as 2015 to 2025 and will date the system within a decade.",
        "Hard to apply consistently at small size or in mono. The field either disappears or blocks up.",
        "Tends toward the decorative. Once a texture exists, it gets used everywhere, and the discipline is lost within two years.",
      ],
      colour: G_OLIVE,
    },
    {
      key: "C", name: "TRACE", img: () => I.trace,
      line: "One resolved path through competing signal.",
      idea: "A field of weak, conflicting traces sits behind a single strong path. Nodes mark the points at which the path is committed. The eye is drawn to the resolved line, not to the noise.",
      says: "Decision under pressure is not the absence of competing information. It is the selection of one line through it, and the willingness to commit at nodes.",
      strengths: [
        "The only concept that directly represents decision, which is central to the framework and absent from the other two.",
        "Gives an immediately useful device for phase diagrams, decision support and pathway documentation.",
        "Nodes provide a natural interactive affordance in digital products.",
      ],
      risks: [
        "Closest of the three to contemporary technology branding. Without severe restraint it reads as a data-visualisation aesthetic.",
        "The noise field is easily overdone and becomes ornament.",
        "Weakest at very small size, where the field collapses into grey.",
      ],
      colour: G_MID,
    },
  ];

  CONCEPTS.forEach((c) => {
    const s = page(`Concept ${c.key}`, `Concept ${c.key}: ${c.name}`, c.line);
    s.addImage({ data: c.img(), x: L, y: 1.72, w: W, h: W * 220 / 900 });
    s.addShape("rect", { x: L, y: 1.72 + W * 220 / 900, w: W, h: 0.014, fill: { color: c.colour } });

    let y = 1.72 + W * 220 / 900 + 0.32;
    y = head(s, y, "THE IDEA");
    body(s, L, y, W, c.idea, 9.4, INK, 0.72);
    y += 0.82;
    y = head(s, y, "WHAT IT SAYS ABOUT THE FRAMEWORK");
    s.addShape("rect", { x: L, y, w: 0.04, h: 0.62, fill: { color: RED } });
    body(s, L + 0.2, y, W - 0.2, c.says, 10.2, INK, 0.62);
    y += 0.78;

    const HW = (W - 0.28) / 2;
    y = head(s, y, "STRENGTHS");
    s.addText("RISKS", { x: L + HW + 0.28, y: y - 0.32, w: HW, h: 0.2, fontFace: F, fontSize: 7.4,
      bold: true, color: INK, charSpacing: 1.6, align: "left", valign: "middle", margin: 0 });
    bullets(s, L, y, HW, c.strengths, 8.6, 2.6);
    bullets(s, L + HW + 0.28, y, HW, c.risks, 8.6, 2.6);

    // The scale test. Longevity and small-size behaviour are two of the six
    // evaluation criteria, so each concept is shown surviving reduction.
    let sy = 9.06;
    sy = head(s, sy, "TESTED AT SIZE");
    const widths = [3.0, 1.85, 1.0];
    const caps = ["Cover, 72 mm", "Slide, 44 mm", "Favicon, 24 mm"];
    let sx = L;
    widths.forEach((ww, i) => {
      const hh = ww * 220 / 900;
      s.addShape("rect", { x: sx, y: sy, w: ww, h: 0.92, fill: { color: WHITE },
        line: { color: RULE, width: 1 } });
      s.addImage({ data: c.img(), x: sx + 0.04, y: sy + 0.46 - hh / 2, w: ww - 0.08, h: hh });
      s.addText(caps[i], { x: sx, y: sy + 0.96, w: ww, h: 0.18, fontFace: F, fontSize: 7,
        color: GREY, align: "left", valign: "middle", margin: 0 });
      sx += ww + 0.14;
    });
    body(s, L, sy + 1.22, W,
      c.key === "A"
        ? "The datum survives reduction because it is composed of rules. At favicon size the tick interval is lost but the line and the displacement remain legible."
        : c.key === "B"
        ? "The field collapses at slide size and reads as a grey block at favicon size. The threshold edge survives, but the idea that produced it does not."
        : "The noise field is the first thing to go. At favicon size the concept reduces to a plain line with dots, which is indistinguishable from Concept A.",
      8.4, "3E3E3E", 0.46);
  });

  // =======================================================================
  // 10  EVALUATION AND RECOMMENDATION
  // =======================================================================
  {
    const s = page("Recommendation", "Evaluation and recommendation",
      "Scored against the criteria that matter for a system intended to last twenty years, not against which concept looks best on a cover.");

    let y = head(s, 1.86, "EVALUATION");
    const CRIT = ["Longevity", "Scalability", "Mono and small size", "Applied by non-designers", "Distinctiveness", "Says what the framework is"];
    const SCORES = { A: [5, 5, 5, 5, 3, 4], B: [2, 3, 2, 3, 4, 4], C: [3, 3, 2, 3, 3, 5] };
    const colW = 1.2, labW = W - 3 * colW;
    ["", "A  DATUM", "B  THRESHOLD", "C  TRACE"].forEach((t, i) => {
      s.addText(t, { x: i === 0 ? L : L + labW + (i - 1) * colW, y, w: i === 0 ? labW : colW, h: 0.24,
        fontFace: F, fontSize: 7.6, bold: true, color: INK, charSpacing: 0.8,
        align: i === 0 ? "left" : "center", valign: "middle", margin: 0 });
    });
    y += 0.26;
    rule(s, y, INK, 0.012); y += 0.08;
    CRIT.forEach((crit, r) => {
      s.addText(crit, { x: L, y, w: labW, h: 0.3, fontFace: F, fontSize: 8.8, color: INK,
        align: "left", valign: "middle", margin: 0 });
      ["A", "B", "C"].forEach((k, ci) => {
        const v = SCORES[k][r];
        for (let i = 0; i < 5; i++) {
          s.addShape("rect", {
            x: L + labW + ci * colW + 0.22 + i * 0.15, y: y + 0.1, w: 0.11, h: 0.11,
            fill: { color: i < v ? (v >= 4 ? INK : GREY) : "E4E4E4" } });
        }
      });
      rule(s, y + 0.3);
      y += 0.36;
    });

    y += 0.12;
    y = head(s, y, "RECOMMENDATION");
    s.addShape("rect", { x: L, y, w: W, h: 1.34, fill: { color: INK } });
    s.addText("Adopt Concept A, Datum, as the governing system.", {
      x: L + 0.3, y: y + 0.18, w: W - 0.6, h: 0.32, fontFace: F, fontSize: 15, bold: true,
      color: WHITE, align: "left", valign: "middle", margin: 0 });
    s.addText("Take the node and departure device from Concept C as its only dynamic element, used solely to mark decision. Retain the density field from Concept B as texture, rationed to divider surfaces and never behind text.", {
      x: L + 0.3, y: y + 0.54, w: W - 0.6, h: 0.66, fontFace: F, fontSize: 9.4, color: "D8D8D8",
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.22 });

    y += 1.5;
    y = head(s, y, "WHY, AND WHAT IS BEING GIVEN UP");
    body(s, L, y, W,
      "Datum wins on the criteria that decide whether a system survives. It is the only one of the three that a staff officer can reproduce correctly in PowerPoint at 2200 hours without a designer present, and that is the real durability test inside a training establishment.",
      9.2, INK, 0.6);
    body(s, L, y + 0.62, W,
      "What is given up is immediate emotional impact. Threshold is the stronger first impression and it is being deliberately declined, because the objective stated in the brief is trust rather than recognition, and trust is built by the twentieth artefact rather than the first. Trace is the sharpest expression of decision, which is why its node is retained rather than the whole concept: adopted wholesale it would pull the system toward a data-visualisation aesthetic that will age badly.",
      9.2, "3E3E3E", 1.0);

    s.addImage({ data: I.system, x: L, y: y + 1.78, w: W, h: W * 260 / 900 });
    s.addText("The recommended system: datum as spine, nodes for decision, density rationed to texture. Shown here carrying the five phase framework development programme.", {
      x: L, y: y + 1.78 + W * 260 / 900 + 0.06, w: W, h: 0.3, fontFace: F, fontSize: 7.8,
      italic: true, color: GREY, align: "left", valign: "top", margin: 0 });
  }

  // =======================================================================
  // 11  WORDMARK EXPLORATIONS
  // =======================================================================
  {
    const s = page("Title treatment", "Title treatment explorations",
      "Six typographic approaches to presenting the Combat Mindset title. None is a logo and none is a freestanding asset: these are repeatable heading constructions. Set in Arial; production is Neue Haas Grotesk.");

    const EX = [
      ["01", "STACKED MASS", "Bold, tight leading, datum rule beneath.",
        "Authority through mass. The rule anchors the mark to the system. Reads at any size and reverses cleanly.",
        (s, x, y, w) => {
          s.addText("COMBAT", { x, y: y + 0.1, w, h: 0.3, fontFace: F, fontSize: 21, bold: true, color: INK, charSpacing: 0.8, align: "left", valign: "middle", margin: 0 });
          s.addText("MINDSET", { x, y: y + 0.38, w, h: 0.3, fontFace: F, fontSize: 21, bold: true, color: INK, charSpacing: 0.8, align: "left", valign: "middle", margin: 0 });
          s.addShape("rect", { x, y: y + 0.72, w: 0.8, h: 0.035, fill: { color: RED } });
        }],
      ["02", "SINGLE LINE, LETTERSPACED", "Light weight, wide tracking, uppercase.",
        "Institutional and quiet. Excellent as a running header or a spine. Too weak to carry a cover alone.",
        (s, x, y, w) => {
          s.addText("C O M B A T   M I N D S E T", { x, y: y + 0.3, w, h: 0.3, fontFace: F, fontSize: 12, color: INK, charSpacing: 1.4, align: "left", valign: "middle", margin: 0 });
        }],
      ["03", "HUNG FROM THE DATUM", "Rule above, mark below, aligned left.",
        "Expresses the governing principle in the mark itself. The strongest structural fit with the system.",
        (s, x, y, w) => {
          s.addShape("rect", { x, y: y + 0.2, w: w - 0.2, h: 0.03, fill: { color: INK } });
          s.addText("COMBAT MINDSET", { x, y: y + 0.32, w, h: 0.3, fontFace: F, fontSize: 15, bold: true, color: INK, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
          s.addText("NZ ARMY COMBAT MINDSET FRAMEWORK", { x, y: y + 0.6, w, h: 0.2, fontFace: F, fontSize: 6.6, color: GREY, charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
        }],
      ["04", "WITH REFERENCE NUMBER", "Doctrine publication convention.",
        "Borrows the authority of the doctrine series directly. Recommended as the formal variant on covers and title pages.",
        (s, x, y, w) => {
          s.addText("CM", { x, y: y + 0.16, w: 0.6, h: 0.34, fontFace: F, fontSize: 20, bold: true, color: INK, align: "left", valign: "middle", margin: 0 });
          s.addText("COMBAT MINDSET", { x: x + 0.62, y: y + 0.18, w: w - 0.62, h: 0.24, fontFace: F, fontSize: 13, bold: true, color: INK, charSpacing: 0.5, align: "left", valign: "middle", margin: 0 });
          s.addText("CM-FWK-001  |  FRAMEWORK", { x: x + 0.62, y: y + 0.44, w: w - 0.62, h: 0.2, fontFace: F, fontSize: 7, color: GREY, charSpacing: 1, align: "left", valign: "middle", margin: 0 });
        }],
      ["05", "TWO WEIGHT RELATIONSHIP", "Combat bold, Mindset light.",
        "Attempts to show the capability relationship typographically. Rejected: it implies Mindset is subordinate to Combat, which inverts the actual hierarchy.",
        (s, x, y, w) => {
          s.addText([{ text: "COMBAT", options: { bold: true } }, { text: " MINDSET", options: { bold: false } }],
            { x, y: y + 0.3, w, h: 0.3, fontFace: F, fontSize: 17, color: INK, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
        }],
      ["06", "MONOGRAM", "CM in a bounded field.",
        "Rejected. However typographic its construction, a bounded monogram functions as a logo and would breach the guidelines and this document's own position.",
        (s, x, y, w) => {
          s.addShape("rect", { x, y: y + 0.16, w: 0.66, h: 0.66, fill: { color: INK } });
          s.addText("CM", { x, y: y + 0.16, w: 0.66, h: 0.66, fontFace: F, fontSize: 19, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
        }],
    ];

    let y = 1.9;
    const EH = 1.24;
    EX.forEach(([n, t, sub, note, draw], i) => {
      const rejected = i >= 4;
      s.addShape("rect", { x: L, y, w: W, h: EH, fill: { color: rejected ? "FAFAF8" : WHITE },
        line: { color: RULE, width: 1 } });
      s.addText(n, { x: L + 0.18, y: y + 0.12, w: 0.3, h: 0.18, fontFace: F, fontSize: 7.4,
        bold: true, color: rejected ? GREY : RED, align: "left", valign: "middle", margin: 0 });
      s.addText(t, { x: L + 0.5, y: y + 0.12, w: 2.4, h: 0.18, fontFace: F, fontSize: 8.4,
        bold: true, color: INK, charSpacing: 0.8, align: "left", valign: "middle", margin: 0 });
      s.addText(sub, { x: L + 0.5, y: y + 0.31, w: 2.4, h: 0.18, fontFace: F, fontSize: 7.2,
        italic: true, color: GREY, align: "left", valign: "middle", margin: 0 });
      body(s, L + 0.5, y + 0.54, 2.5, note, 7.6, rejected ? GREY : "3E3E3E", 0.6);
      draw(s, L + 3.3, y, W - 3.6);
      if (rejected) {
        s.addText("NOT RECOMMENDED", { x: R - 1.6, y: y + 0.12, w: 1.42, h: 0.18, fontFace: F,
          fontSize: 6.4, bold: true, color: RED, charSpacing: 0.8, align: "right", valign: "middle", margin: 0 });
      }
      y += EH + 0.12;
    });

    y = head(s, y + 0.06, "SELECTION");
    body(s, L, y, W,
      "Carry 03 as the primary title treatment and 04 as the formal variant on covers, title pages and formal framework publications. Retain 02 for running headers and spines. Options 05 and 06 are recorded so that the reasons for rejecting them survive the people who rejected them.",
      9, INK, 0.6);
  }

  // =======================================================================
  // 12  WORDMARK SPECIFICATION
  // =======================================================================
  {
    const s = page("Title treatment", "Title treatment specification",
      "Written so it can be applied without a designer, and audited without a debate. Deliberately not called a wordmark: this is a heading construction inside Army collateral, not a brand asset.");

    let y = head(s, 1.86, "PRIMARY TITLE TREATMENT");
    s.addShape("rect", { x: L, y, w: W, h: 1.9, fill: { color: PAPER } });
    s.addShape("rect", { x: L + 0.5, y: y + 0.62, w: 3.4, h: 0.035, fill: { color: INK } });
    s.addText("COMBAT MINDSET", { x: L + 0.5, y: y + 0.72, w: 5, h: 0.4, fontFace: F, fontSize: 24,
      bold: true, color: INK, charSpacing: 0.8, align: "left", valign: "middle", margin: 0 });
    s.addText("NZ ARMY COMBAT MINDSET FRAMEWORK", { x: L + 0.5, y: y + 1.14, w: 5, h: 0.22, fontFace: F,
      fontSize: 8, color: GREY, charSpacing: 1.6, align: "left", valign: "middle", margin: 0 });
    y += 2.04;

    y = head(s, y, "CONSTRUCTION RULES");
    const rules = [
      ["Datum rule", "Width equals the treatment measure. Weight equals one tenth of the cap height. Colour black, or white when reversed. Never red."],
      ["Clear space", "One cap height on all four sides. Nothing enters it, including the Army logo."],
      ["Minimum size", "28 mm measure in print. 180 px in digital. Below this, use the single line variant without the descriptor."],
      ["Descriptor", "One third of the title size, letterspaced 1.6. Wording settled at endorsement; until then, NZ Army Combat Mindset Framework. Omit where context establishes it; never reword locally."],
      ["Colour", "Black on light grounds, white on dark. One colour only. The treatment is never red, never tinted, never outlined and never set on a photograph without a solid panel behind it."],
      ["Relationship to the Army logo", "Appears on every complete formal artefact, at greater visual weight. It need not repeat inside every internal component or screen. The treatment stays outside the logo's clear space and off its baseline."],
    ];
    rules.forEach(([k, v]) => {
      s.addText(k, { x: L, y, w: 1.5, h: 0.4, fontFace: F, fontSize: 8.6, bold: true,
        color: INK, align: "left", valign: "top", margin: 0 });
      body(s, L + 1.6, y, W - 1.6, v, 8.6, "3E3E3E", 0.42);
      rule(s, y + 0.44);
      y += 0.54;
    });

    y = head(s, y + 0.06, "VARIANTS");
    const VW = (W - 2 * 0.14) / 3;
    const vars = [
      ["FORMAL", INK, WHITE, "Covers and title pages. Carries the reference number."],
      ["RUNNING", WHITE, INK, "Headers, spines and footers. Single line, no descriptor."],
      ["REVERSED", G_DARK, WHITE, "Divider surfaces and dark applications."],
    ];
    vars.forEach(([t, bg, fg, note], i) => {
      const x = L + i * (VW + 0.14);
      s.addShape("rect", { x, y, w: VW, h: 1.0, fill: { color: bg },
        line: bg === WHITE ? { color: RULE, width: 1 } : undefined });
      s.addShape("rect", { x: x + 0.18, y: y + 0.3, w: VW - 0.9, h: 0.024, fill: { color: fg } });
      s.addText("COMBAT MINDSET", { x: x + 0.18, y: y + 0.36, w: VW - 0.36, h: 0.24, fontFace: F,
        fontSize: 9.6, bold: true, color: fg, charSpacing: 0.4, align: "left", valign: "middle", margin: 0 });
      s.addText(t, { x: x + 0.18, y: y + 0.62, w: VW - 0.36, h: 0.18, fontFace: F, fontSize: 6.4,
        color: fg, charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
      body(s, x, y + 1.06, VW, note, 7.6, GREY, 0.4);
    });
  }

  // =======================================================================
  // 13  GRAPHIC LANGUAGE
  // =======================================================================
  {
    const s = page("Graphic language", "Graphic language",
      "Five elements. Nothing else is permitted, and each carries a fixed meaning so the language cannot drift into decoration.");

    const ELEMENTS = [
      ["THE DATUM", "A single black rule, weight 1.5 pt at A4.",
        "Governs the surface. Everything aligns to it. Its meaning is a standard being held. It is never dashed, never coloured and never curved."],
      ["TICKS AND REGISTERS", "Short marks at a fixed interval, major every fourth.",
        "Provide measure. Their presence signals that something is being assessed rather than asserted. Used on evidence, assessment and progress surfaces only."],
      ["THE NODE", "An open circle on the datum, red stroke.",
        "Marks a decision point. It is the only element permitted to interrupt the datum, and the only routine use of red. A surface with four nodes is making four claims about where commitment occurs."],
      ["THE DEPARTURE", "A single line leaving the datum at a node.",
        "Represents a decision taken and its consequence. Only one departure per node. Multiple departures would represent optionality, which is a different and rarer claim."],
      ["THE FIELD", "Halftone density drawn from the Army chevron pattern.",
        "Represents accumulated pressure. Permitted on covers and dividers, never behind text, never as a page background, and never at more than 18 per cent opacity."],
      ["THE DISPLACEMENT TRACE", "A curved deviation from the datum, black, at the datum's weight.",
        "Represents load, interference and recovery. The only curve in the system, defined so the Datum concept can be drawn without breaking its own rules. It always returns to the datum, is never red, and is never decorative."],
    ];
    let y = 1.86;
    y = head(s, y, "THE PERMITTED ELEMENTS");
    ELEMENTS.forEach(([t, spec, why], i) => {
      s.addShape("rect", { x: L, y, w: 0.03, h: 0.74, fill: { color: i === 2 || i === 3 ? RED : INK } });
      s.addText(t, { x: L + 0.18, y, w: 2.1, h: 0.22, fontFace: F, fontSize: 9.2, bold: true,
        color: INK, charSpacing: 0.8, align: "left", valign: "middle", margin: 0 });
      s.addText(spec, { x: L + 0.18, y: y + 0.22, w: 2.1, h: 0.4, fontFace: F, fontSize: 7.4,
        italic: true, color: GREY, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });
      body(s, L + 2.5, y, W - 2.5, why, 8.6, "3E3E3E", 0.72);
      y += 0.82;
    });

    y = head(s, y + 0.04, "THE GRAMMAR");
    s.addShape("rect", { x: L, y, w: W, h: 1.16, fill: { color: PAPER } });
    const grammar = [
      ["Along the datum", "sequence"],
      ["Away from the datum", "decision"],
      ["Break in the datum", "risk"],
      ["Return to the datum", "recovery"],
      ["Density above the datum", "pressure"],
    ];
    s.addText("Visual conventions for reading Combat Mindset surfaces, not definitions of the concepts they mark.", {
      x: L + 0.22, y: y + 0.9, w: W - 0.44, h: 0.2, fontFace: F, fontSize: 7.4, italic: true,
      color: GREY, align: "left", valign: "middle", margin: 0 });
    grammar.forEach(([a, b], i) => {
      const gx = L + 0.22 + i * ((W - 0.44) / 5);
      s.addText(a, { x: gx, y: y + 0.24, w: (W - 0.44) / 5 - 0.1, h: 0.36, fontFace: F,
        fontSize: 8.4, bold: true, color: INK, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });
      s.addText(b.toUpperCase(), { x: gx, y: y + 0.66, w: (W - 0.44) / 5 - 0.1, h: 0.22, fontFace: F,
        fontSize: 8, color: RED, charSpacing: 1, align: "left", valign: "middle", margin: 0 });
    });

    y += 1.3;
    y = head(s, y, "WHAT IS FORBIDDEN, AND WHY");
    bullets(s, L, y, W, [
      "Curves outside the displacement trace. The datum itself is always straight, and no other element bends.",
      "Gradients other than the sanctioned halftone field. Gradients carry a date.",
      "Drop shadows, glows, bevels and any depth effect. Depth implies a physical object; this is a notation, not an artefact.",
      "Red used as a surface, a heading colour or a fill. Red marks decision nodes and defined threshold states; risk is otherwise carried structurally by the broken datum. Spending it elsewhere destroys the only signal in the system that carries urgency.",
      "Any new element added without an accompanying sentence in the specification stating what it means.",
    ], 8.8, 1.8);
  }

  // =======================================================================
  // 14  NOTATION FAMILY
  // =======================================================================
  {
    const s = page("Notation", "Notation family",
      "Twelve marks, one grammar. These are not pictograms: nothing is a picture of a thing. Each mark is a statement about how a piece of content relates to the datum.");

    let y = head(s, 2.0, "THE CONSTRUCTION");
    body(s, L, y, W,
      "Every mark is drawn on a 24 unit grid at 2 unit stroke, and every mark contains the datum at y=17. What differs is what happens to that datum, and what sits on it. A reader who learns the grammar once can interpret a mark they have never seen, which is the property a pictogram set can never have. Six marks form the pilot set: Framework, Governance, Evidence, Assessment, Product and Decision, the minimum spread across the four families. Doctrine and the other marks are drafted to prove the grammar extends, and join when authority arrangements and repository content warrant them.",
      9, INK, 0.98);
    y += 1.1;

    const FAMS = [
      ["STRUCTURE", BLACK, "Content that carries authority. The datum is complete and unbroken."],
      ["ANALYSIS", G_DARK, "Content that examines. The datum carries measures, intervals or returns."],
      ["DELIVERY", G_OLIVE, "Content that is used. Discrete objects sit on the datum."],
      ["ACTION", RED, "Content that requires a person to do something. The datum is left or broken."],
    ];
    y = head(s, y, "FOUR FAMILIES");
    const FW = (W - 3 * 0.12) / 4;
    FAMS.forEach(([t, c, d], i) => {
      const x = L + i * (FW + 0.12);
      s.addShape("rect", { x, y, w: FW, h: 0.72, fill: { color: WHITE }, line: { color: RULE, width: 1 } });
      s.addShape("rect", { x, y, w: FW, h: 0.04, fill: { color: c } });
      s.addText(t, { x: x + 0.12, y: y + 0.08, w: FW - 0.24, h: 0.18, fontFace: F, fontSize: 7.6,
        bold: true, color: INK, charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
      body(s, x + 0.12, y + 0.28, FW - 0.24, d, 7.2, "3E3E3E", 0.4);
    });
    y += 0.86;

    y = head(s, y, "THE TWELVE MARKS");
    const MW = (W - 3 * 0.14) / 4, MH = 1.32;
    TYPES.forEach(([name, key, colour, fam, why], i) => {
      const col = i % 4, row = Math.floor(i / 4);
      const x = L + col * (MW + 0.14), yy = y + row * (MH + 0.14);
      s.addShape("rect", { x, y: yy, w: MW, h: MH, fill: { color: WHITE }, line: { color: RULE, width: 1 } });
      s.addImage({ data: MARK_IMG[key], x: x + 0.14, y: yy + 0.14, w: 0.44, h: 0.44 });
      s.addText(name, { x: x + 0.66, y: yy + 0.16, w: MW - 0.76, h: 0.2, fontFace: F, fontSize: 8,
        bold: true, color: INK, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
      if (["framework", "governance", "evidence", "assessment", "product", "decision"].includes(key)) {
        s.addText("PILOT", { x: x + MW - 0.6, y: yy + 0.08, w: 0.52, h: 0.14, fontFace: F,
          fontSize: 5.6, bold: true, color: GREY, charSpacing: 1, align: "right", valign: "middle", margin: 0 });
      }
      s.addText(fam.toUpperCase(), { x: x + 0.66, y: yy + 0.35, w: MW - 0.76, h: 0.16, fontFace: F,
        fontSize: 6, color: colour, charSpacing: 1, align: "left", valign: "middle", margin: 0 });
      body(s, x + 0.14, yy + 0.66, MW - 0.28, why, 6.9, "3E3E3E", 0.6);
    });

    let sy = y + 3 * (MH + 0.14) + 0.16;
    sy = head(s, sy, "AT SIZE, AND IN MONO");
    s.addShape("rect", { x: L, y: sy, w: W, h: 0.94, fill: { color: WHITE },
      line: { color: RULE, width: 1 } });
    const sizes = [0.46, 0.34, 0.26, 0.19];
    let sx = L + 0.24;
    sizes.forEach((z) => {
      s.addImage({ data: MARK_IMG["evidence"], x: sx, y: sy + 0.47 - z / 2, w: z, h: z });
      sx += z + 0.2;
    });
    s.addText("48  32  24  16 px", { x: L + 0.24, y: sy + 0.74, w: 2, h: 0.16, fontFace: F,
      fontSize: 6.4, color: GREY, align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L + 2.5, y: sy + 0.12, w: 0.014, h: 0.7, fill: { color: RULE } });
    ["framework", "evidence", "product", "decision"].forEach((k, i) => {
      s.addImage({ data: MARK_IMG[k], x: L + 2.76 + i * 0.5, y: sy + 0.24, w: 0.34, h: 0.34 });
    });
    s.addText("in classification colour", { x: L + 2.76, y: sy + 0.66, w: 2, h: 0.16, fontFace: F,
      fontSize: 6.4, color: GREY, align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L + 4.9, y: sy + 0.12, w: 0.014, h: 0.7, fill: { color: RULE } });
    ["framework", "evidence", "product", "decision"].forEach((k, i) => {
      s.addImage({ data: MONO_IMG[k], x: L + 5.16 + i * 0.5, y: sy + 0.24, w: 0.34, h: 0.34 });
    });
    s.addText("mono, meaning intact", { x: L + 5.16, y: sy + 0.66, w: 2, h: 0.16, fontFace: F,
      fontSize: 6.4, color: GREY, align: "left", valign: "middle", margin: 0 });
  }

  // =======================================================================
  // 15  COLOUR SYSTEM
  // =======================================================================
  {
    const s = page("Colour", "Colour system",
      "No colour is invented. Every value is published in the NZ Army Visual Identity Guidelines p58. What is added here is a set of rules about what each colour is allowed to mean.");

    let y = head(s, 1.94, "PRIMARY");
    const prim = [
      ["Black", BLACK, "Process Black C", "0 0 0", "Structure, type and the datum. The default. Carries all hierarchy.", WHITE],
      ["White", WHITE, "White", "255 255 255", "Space, and the reversed state. Space is a material and is budgeted, not filled.", INK],
      ["Army Red", RED, "Pantone 200 C", "211 17 69", "Decision nodes, the action notation, and defined threshold states. Otherwise risk is carried by the broken datum.", WHITE],
    ];
    const PW = (W - 2 * 0.14) / 3;
    prim.forEach(([n, hex, pan, rgb, use, ink], i) => {
      const x = L + i * (PW + 0.14);
      s.addShape("rect", { x, y, w: PW, h: 1.24, fill: { color: hex },
        line: hex === WHITE ? { color: RULE, width: 1 } : undefined });
      s.addText(n, { x: x + 0.16, y: y + 0.12, w: PW - 0.32, h: 0.22, fontFace: F, fontSize: 10.4,
        bold: true, color: ink, align: "left", valign: "middle", margin: 0 });
      s.addText(`#${hex}\n${pan}\nrgb ${rgb}`, { x: x + 0.16, y: y + 0.62, w: PW - 0.32, h: 0.56,
        fontFace: F, fontSize: 7, color: ink, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.2 });
      body(s, x, y + 1.3, PW, use, 7.8, "3E3E3E", 0.5);
    });
    y += 1.86;

    y = head(s, y, "SECONDARY: CLASSIFICATION, NOT DECORATION");
    const sec = [
      ["5605 C", G_DARK, "00261B", "Analysis", "Evidence, research, assessment, review."],
      ["5747 C", G_OLIVE, "444D06", "Delivery", "Products, references, training material."],
      ["5853 C", G_MID, "B3A650", "Layering", "Secondary surfaces, table banding, inactive states."],
      ["5855 C", G_LIGHT, "DFD8AD", "Ground", "Panels and callouts beneath text. Never text itself."],
    ];
    const SW2 = (W - 3 * 0.12) / 4;
    sec.forEach(([pan, hex, h, role, use], i) => {
      const x = L + i * (SW2 + 0.12);
      s.addShape("rect", { x, y, w: SW2, h: 0.64, fill: { color: hex } });
      s.addText(role.toUpperCase(), { x: x + 0.12, y: y + 0.1, w: SW2 - 0.24, h: 0.2, fontFace: F,
        fontSize: 7.6, bold: true, color: i < 2 ? WHITE : INK, charSpacing: 1, align: "left", valign: "middle", margin: 0 });
      s.addText(`${pan}   #${h}`, { x: x + 0.12, y: y + 0.4, w: SW2 - 0.24, h: 0.16, fontFace: F,
        fontSize: 6, color: i < 2 ? "D0D0D0" : "3E3E3E", align: "left", valign: "middle", margin: 0 });
      body(s, x, y + 0.7, SW2, use, 7.4, "3E3E3E", 0.44);
    });
    y += 1.3;

    y = head(s, y, "PROPORTION RULE");
    s.addImage({ data: I.proportion, x: L, y, w: W, h: W * 64 / 900 });
    y += W * 64 / 900 + 0.12;
    body(s, L, y, W,
      "Red never exceeds five per cent of any surface. This is the only hard numerical constraint in the colour system, and it is the one that keeps the signal working. A page where red marks four decision nodes tells the reader something. A page where red also carries headings, rules and callouts tells them nothing.",
      8.8, INK, 0.62);
    y += 0.74;

    y = head(s, y, "MONO AND ACCESSIBILITY");
    bullets(s, L, y, W, [
      "Every artefact must survive a mono print with no loss of meaning. Classification is therefore carried by the notation mark as well as by colour, never by colour alone.",
      "Body text is black on white or white on black. The greens are never used for running text.",
      "Army Red on white calculates at roughly 5.3 to 1, which passes AA for body text; Army Red on black fails and is not permitted for type. Every claim here is re-verified with accredited tooling at step 03, and the repository tests contrast, minimum sizes, mono output and reduced motion automatically.",
      "Colour blindness affects roughly one in twelve men. Red against the four greens is the least safe pairing in the palette, which is a further reason red is reserved for a marker shape rather than a fill.",
    ], 8.6, 1.8);
  }

  // =======================================================================
  // 16  INFORMATION ARCHITECTURE
  // =======================================================================
  {
    const s = page("Architecture", "Information architecture",
      "Twelve content types, each with a fixed treatment. A reader should be able to tell what kind of thing they are holding before they have read a word of it.");

    let y = head(s, 1.94, "THE COMPONENT");
    body(s, L, y, W,
      "Every piece of Combat Mindset content is presented in the same component: a notation mark, a type label, an identifier, a title, and a status line. The component is identical in print, in a slide, in a repository and on a phone; only its scale changes. Identifiers separate content type, item and version, because a number that means two things eventually means nothing. The scheme shown is illustrative: allocation authority, and its relationship to existing Army and NZDF reference series, is resolved at step 03 before any identifier is issued. The pilot also tests whether some types are better held as status or relationship metadata than as primary types.",
      9, INK, 1.0);
    y += 1.1;

    // the anatomy diagram
    s.addShape("rect", { x: L, y, w: W, h: 1.0, fill: { color: WHITE }, line: { color: RULE, width: 1 } });
    s.addShape("rect", { x: L, y, w: 0.05, h: 1.0, fill: { color: G_DARK } });
    s.addImage({ data: MARK_IMG["evidence"], x: L + 0.24, y: y + 0.22, w: 0.5, h: 0.5 });
    s.addText("EVIDENCE", { x: L + 0.88, y: y + 0.2, w: 2, h: 0.2, fontFace: F, fontSize: 7.4,
      bold: true, color: G_DARK, charSpacing: 1.4, align: "left", valign: "middle", margin: 0 });
    s.addText("CM-EVD-004  v0.3", { x: L + 0.88, y: y + 0.38, w: 2, h: 0.2, fontFace: F, fontSize: 7,
      color: GREY, charSpacing: 0.8, align: "left", valign: "middle", margin: 0 });
    s.addText("Cognitive load and decision quality under physical stress", {
      x: L + 3.0, y: y + 0.2, w: W - 3.4, h: 0.26, fontFace: F, fontSize: 10.4, bold: true,
      color: INK, align: "left", valign: "middle", margin: 0 });
    s.addText("Endorsed  |  Reviewed Aug 2026  |  Owner NZALC", { x: L + 3.0, y: y + 0.48,
      w: W - 3.4, h: 0.2, fontFace: F, fontSize: 7.6, color: GREY, align: "left", valign: "middle", margin: 0 });
    const anno = [
      [L + 0.24, "notation"], [L + 0.88, "type and reference"], [L + 3.0, "title and status"],
    ];
    anno.forEach(([x, t]) =>
      s.addText(t, { x, y: y + 1.02, w: 2, h: 0.16, fontFace: F, fontSize: 6.4, italic: true,
        color: RED, align: "left", valign: "middle", margin: 0 }));
    y += 1.26;

    y = head(s, y, "THE TWELVE TREATMENTS");
    const RH = 0.46;
    TYPES.forEach(([name, key, colour, fam], i) => {
      const yy = y + i * (RH + 0.04);
      s.addShape("rect", { x: L, y: yy, w: W, h: RH, fill: { color: i % 2 ? "FBFBFA" : WHITE } });
      s.addShape("rect", { x: L, y: yy, w: 0.04, h: RH, fill: { color: colour } });
      s.addImage({ data: MARK_IMG[key], x: L + 0.18, y: yy + 0.11, w: 0.28, h: 0.28 });
      s.addText(name, { x: L + 0.58, y: yy, w: 1.5, h: RH, fontFace: F, fontSize: 8.2, bold: true,
        color: INK, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
      s.addText(fam.toUpperCase(), { x: L + 2.06, y: yy, w: 1.0, h: RH, fontFace: F, fontSize: 6.4,
        color: colour, charSpacing: 1, align: "left", valign: "middle", margin: 0 });
      s.addText(["CM-FWK-001", "CM-DOC-001", "CM-POL-001", "CM-GOV-001", "CM-EVD-001", "CM-RES-001",
        "CM-ASM-001", "CM-REV-001", "CM-PRD-001", "CM-REF-001", "CM-DEC-001", "CM-RSK-001"][i],
        { x: L + 3.0, y: yy, w: 1.06, h: RH, fontFace: F, fontSize: 7,
        color: GREY, align: "left", valign: "middle", margin: 0 });
      s.addText([
        "Governing architecture", "Endorsed and enduring statements", "Rules with limits",
        "Who holds and assures what", "Findings and their strength", "Open questions and method",
        "Measurement against a standard", "Deliberate return to a prior position",
        "Material issued for use", "Pointers to work held elsewhere",
        "A point at which commitment is required", "A discontinuity to be managed",
      ][i], { x: L + 4.14, y: yy, w: W - 4.24, h: RH, fontFace: F, fontSize: 7.8,
        color: "3E3E3E", align: "left", valign: "middle", margin: 0 });
    });
  }

  // =======================================================================
  // 17  PHOTOGRAPHY
  // =======================================================================
  {
    const s = page("Photography", "Photography direction",
      "Photography is the element most likely to break this system, because it is the element most often chosen by someone in a hurry. The direction below is written to be enforceable.");

    let y = head(s, 1.94, "THE GOVERNING INSTRUCTION");
    s.addShape("rect", { x: L, y, w: W, h: 0.94, fill: { color: INK } });
    s.addText("Photograph the load, not the outcome.", { x: L + 0.3, y: y + 0.16, w: W - 0.6, h: 0.3,
      fontFace: F, fontSize: 15, bold: true, color: WHITE, align: "left", valign: "middle", margin: 0 });
    s.addText("The framework is about what happens to people under pressure. The imagery should show pressure being carried, not victory being celebrated.", {
      x: L + 0.3, y: y + 0.5, w: W - 0.6, h: 0.36, fontFace: F, fontSize: 9, color: "C8C8C8",
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.2 });
    y += 1.1;

    const DIRS = [
      ["LIGHTING", "Available light only. Overcast, dawn, dusk, interior fluorescent, vehicle interior. No fill, no flash, no colour grading beyond correction. If the light was poor, the photograph shows poor light."],
      ["COMPOSITION", "Eye level. The camera stands where another soldier would stand. High and low angles are permitted only where the operational reality requires it, never for drama."],
      ["FRAMING", "Wide enough to show the environment doing the work. The context is the pressure; a tight portrait removes the very thing being documented."],
      ["SUBJECT", "The whole Army. Ranks from private to colonel, all trades, all body types, both regular and reserve. If the imagery set skews young, male and infantry, the framework will be read as belonging to them."],
      ["EMOTION", "Concentration, fatigue, recovery, deliberation, the flat expression of someone thinking hard. Never aggression, never triumph, never the shouted moment."],
      ["MOMENT", "The moment before or the moment after. The moment itself is almost always the least informative frame and the most theatrical."],
      ["EYE CONTACT", "None, except in a named environmental portrait where a person is being quoted or credited. A soldier looking into the lens is performing."],
      ["POST", "Correction only. No vignettes, no crushed blacks, no teal and orange, no monochrome conversion to add gravity."],
    ];
    y = head(s, y, "DIRECTION");
    DIRS.forEach(([k, v]) => {
      s.addText(k, { x: L, y, w: 1.3, h: 0.5, fontFace: F, fontSize: 7.6, bold: true, color: INK,
        charSpacing: 1, align: "left", valign: "top", margin: 0 });
      body(s, L + 1.4, y, W - 1.4, v, 8.6, "3E3E3E", 0.52);
      rule(s, y + 0.54);
      y += 0.64;
    });

    y = head(s, y + 0.04, "AUTOMATIC REJECTIONS");
    const rej = ["Silhouettes against a sunset", "Gym and physical training as a stand-in for performance",
      "Weapon-forward hero framing", "Shouted faces", "Staged planning shots around a map",
      "Stock imagery of any kind", "Anything shot for recruitment", "Composites and montage"];
    const RW = (W - 3 * 0.1) / 4;
    rej.forEach((t, i) => {
      const x = L + (i % 4) * (RW + 0.1), yy = y + Math.floor(i / 4) * 0.46;
      s.addShape("rect", { x, y: yy, w: RW, h: 0.38, fill: { color: PAPER } });
      s.addShape("rect", { x, y: yy, w: 0.025, h: 0.38, fill: { color: RED } });
      s.addText(t, { x: x + 0.12, y: yy, w: RW - 0.2, h: 0.38, fontFace: F, fontSize: 7,
        color: INK, align: "left", valign: "middle", margin: 0 });
    });
  }

  // =======================================================================
  // 18  MOTION
  // =======================================================================
  {
    const s = page("Motion", "Motion language",
      "Motion is the newest part of the system and the part most likely to date it. The specification is therefore deliberately narrow.");

    let y = head(s, 1.94, "THE PRINCIPLE");
    s.addShape("rect", { x: L, y, w: W, h: 0.68, fill: { color: PAPER } });
    s.addText("Motion confirms. It does not perform.", { x: L + 0.3, y, w: W - 0.6, h: 0.68,
      fontFace: F, fontSize: 15, bold: true, color: INK, align: "left", valign: "middle", margin: 0 });
    y += 0.86;

    s.addImage({ data: I.motion, x: L, y, w: 3.0, h: 3.0 * 260 / 420 });
    const specs = [
      ["Easing", "cubic-bezier(0.2, 0, 0, 1). Decelerate into position. No overshoot, no bounce, no elastic."],
      ["Duration", "180 ms for state change. 240 ms for element entry. 320 ms for view transition. Nothing exceeds 400 ms."],
      ["Entry", "Elements arrive along the datum, by wipe or by translation on one axis. Nothing fades in from nowhere and nothing scales up."],
      ["Emphasis", "A node may draw its stroke once, in 240 ms, on first appearance only. It never pulses, never loops and never glows."],
      ["Reduced motion", "Honour the operating system preference. With reduced motion set, every transition becomes an instant state change with no substitute effect."],
    ];
    let sy = y + 0.04;
    specs.forEach(([k, v]) => {
      s.addText(k, { x: L + 3.24, y: sy, w: 1.0, h: 0.38, fontFace: F, fontSize: 8, bold: true,
        color: INK, align: "left", valign: "top", margin: 0 });
      body(s, L + 4.3, sy, W - 4.3, v, 8.2, "3E3E3E", 0.4);
      sy += 0.42;
    });
    y += 3.0 * 260 / 420 + 0.2;

    y = head(s, y, "WHY SO NARROW");
    body(s, L, y, W,
      "Every generation of interface has an animation signature, and it is always the first thing that makes an old product look old. Skeuomorphic easing dated in five years. Material motion dated in seven. A system intended to run for twenty must spend as little as possible on motion, so that when the signature of this decade becomes visible, there is almost nothing of it to remove.",
      9, INK, 0.62);
    y += 0.74;

    y = head(s, y, "FORBIDDEN");
    bullets(s, L, y, W, [
      "Parallax, particles, glow, blur transitions, and anything that draws attention to the transition itself.",
      "Looping animation of any kind. A loop is a demand for attention, and these products are read by people who have somewhere to be.",
      "Motion that conveys information not otherwise available. If a reader with reduced motion enabled loses meaning, the design has failed.",
      "Animated logos or title treatments. The title treatment is a fixed thing; animating it makes it a performance.",
    ], 8.8, 1.5);
  }

  // =======================================================================
  // 19  DIGITAL APPLICATION
  // =======================================================================
  {
    const s = page("Digital", "Digital application",
      "The system is digital-first, which means the specification must survive contact with markdown, a repository theme and a phone screen.");

    const APPS = [
      ["REPOSITORY AND GITHUB DOCUMENTATION",
        "Markdown is the constraint. The notation family is issued as inline SVG so a mark can precede a heading in a README without an image pipeline. The datum becomes a horizontal rule. The reference number goes in the front matter and the file name, so a document remains identifiable when detached from its interface."],
      ["FRAMEWORK BROWSER",
        "The twelve content types become the primary filter, not a search box. A user arrives asking what kind of thing they need before they know its title. Left rail carries the notation; content pane carries the component."],
      ["INTERACTIVE DOCTRINE",
        "Doctrine text at full measure, with evidence and assessment content collapsed beneath it and marked with their own notation. The reader can see that evidence exists without being made to read it, which is the behaviour the framework wants to encourage."],
      ["DECISION SUPPORT",
        "The only place the departure element is used interactively. A node expands to show what commitment at that point entails. No wizard, no scoring, no recommendation engine; the tool documents the decision, it does not make it."],
      ["DASHBOARDS",
        "Ticks and registers, black on white, no chart junk. Red marks only thresholds crossed. A dashboard where several things are red is reporting a genuine problem, not a styling choice."],
      ["PRESENTATIONS",
        "One template, three slide types: statement, component list, diagram. The datum runs across every slide at a fixed height so a deck reads as one continuous surface."],
      ["TRAINING PRODUCTS",
        "Printable at unit level on a mono printer. Every classification survives without colour because the notation carries it. This is the constraint that most often breaks identity systems in a training establishment, and it is designed for rather than discovered."],
      ["MOBILE",
        "Single column, datum at the top of the viewport, notation at 24 px. Content types collapse to the mark and the reference number. Offline first, because the reader is frequently somewhere without signal."],
    ];
    let y = 1.98;
    y = head(s, y, "APPLICATION BY SURFACE");
    APPS.forEach(([t, d], i) => {
      s.addText(String(i + 1).padStart(2, "0"), { x: L, y, w: 0.34, h: 0.2, fontFace: F,
        fontSize: 7.6, bold: true, color: RED, align: "left", valign: "middle", margin: 0 });
      s.addText(t, { x: L + 0.36, y, w: W - 0.36, h: 0.2, fontFace: F, fontSize: 8.6, bold: true,
        color: INK, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
      body(s, L + 0.36, y + 0.2, W - 0.5, d, 8.4, "3E3E3E", 0.62);
      y += 0.82;
    });

    y = head(s, y + 0.02, "THE SINGLE SOURCE");
    s.addShape("rect", { x: L, y, w: W, h: 0.9, fill: { color: PAPER } });
    body(s, L + 0.24, y + 0.16, W - 0.48,
      "The specification, the notation family, the colour tokens and the component markup are held in one repository and consumed by every surface. Nothing is redrawn per product. This is what makes the twenty year claim credible: the identity is maintained as code with a version number, not as a PDF that people copy from.",
      8.8, INK, 0.7);
  }

  // =======================================================================
  // 20  BRAND VOICE
  // =======================================================================
  {
    const s = page("Voice", "Brand voice",
      "The identity fails at the first sentence if the writing does not match it. Voice is specified here as pairs, because writers learn faster from contrast than from adjectives.");

    let y = head(s, 1.94, "HOW COMBAT MINDSET SPEAKS");
    const VOICE = [
      ["Confident", "It states. It does not argue with an imagined sceptic, and it does not hedge every claim into meaninglessness."],
      ["Measured", "Short sentences. One idea each. The register of a good set of orders, not a good speech."],
      ["Evidence-based", "Claims carry their strength. Where the evidence is thin, the text says so, because a framework that overclaims once is discounted permanently."],
      ["Operational", "Written for someone who will act on it. Every paragraph should survive the question: what does the reader do differently now."],
      ["Plain", "No jargon that a corporal would have to look up, and no psychology terminology used decoratively."],
      ["Never motivational", "It does not exhort, inspire, challenge or remind anyone what they are capable of. The moment it does, it becomes a poster, and posters are ignored."],
    ];
    VOICE.forEach(([k, v]) => {
      s.addText(k, { x: L, y, w: 1.5, h: 0.44, fontFace: F, fontSize: 9.6, bold: true,
        color: k === "Never motivational" ? RED : INK, align: "left", valign: "top", margin: 0 });
      body(s, L + 1.6, y, W - 1.6, v, 8.8, "3E3E3E", 0.46);
      rule(s, y + 0.5);
      y += 0.6;
    });

    y = head(s, y + 0.06, "WRITE THIS, NOT THAT");
    const PAIRS = [
      ["Under pressure, trained people lose access to capability they demonstrably hold.",
       "Unlock your true potential when it matters most."],
      ["The evidence for transfer to operational performance is currently limited.",
       "Proven to deliver results on operations."],
      ["Phase 2 assesses existing products against the endorsed outcomes.",
       "We are on an exciting journey to transform how Army thinks about performance."],
      ["Do this before the serial. Record what happened. Review it within 48 hours.",
       "Embrace the challenge and push through your limits."],
    ];
    const CW2 = (W - 0.24) / 2;
    s.addText("WRITE", { x: L, y, w: CW2, h: 0.2, fontFace: F, fontSize: 7, bold: true,
      color: G_DARK, charSpacing: 1.4, align: "left", valign: "middle", margin: 0 });
    s.addText("NOT", { x: L + CW2 + 0.24, y, w: CW2, h: 0.2, fontFace: F, fontSize: 7, bold: true,
      color: RED, charSpacing: 1.4, align: "left", valign: "middle", margin: 0 });
    y += 0.24;
    PAIRS.forEach(([good, bad]) => {
      s.addShape("rect", { x: L, y, w: CW2, h: 0.66, fill: { color: WHITE }, line: { color: RULE, width: 1 } });
      s.addShape("rect", { x: L, y, w: 0.03, h: 0.66, fill: { color: G_DARK } });
      body(s, L + 0.16, y + 0.1, CW2 - 0.3, good, 8.2, INK, 0.5);
      s.addShape("rect", { x: L + CW2 + 0.24, y, w: CW2, h: 0.66, fill: { color: "FBFBFA" }, line: { color: RULE, width: 1 } });
      s.addShape("rect", { x: L + CW2 + 0.24, y, w: 0.03, h: 0.66, fill: { color: RED } });
      body(s, L + CW2 + 0.4, y + 0.1, CW2 - 0.3, bad, 8.2, GREY, 0.5);
      y += 0.76;
    });

    y = head(s, y, "THE TAGLINE");
    body(s, L, y, W,
      "Remain effective. Act decisively. Harder to kill. It works because the first two lines are instructions and the third is a consequence, not a boast. It should be used sparingly, on covers and dividers, and never as a heading inside a document. Overused, it becomes the motivational register the rest of the voice is written to avoid.",
      8.8, INK, 0.6);
  }

  // =======================================================================
  // 21  IDENTITY EVOLUTION
  // =======================================================================
  {
    const s = page("Evolution", "Identity evolution",
      "How the system matures over ten years, and why it should never need a redesign.");

    let y = head(s, 1.94, "THE MECHANISM");
    body(s, L, y, W,
      "The system is a grammar, not a set of assets. New content types are added by extending the notation according to the existing rules, not by commissioning new marks. New surfaces are built from the datum, the grid and the component. Because meaning lives in the grammar rather than in any particular drawing, the drawings can be replaced without the identity changing.",
      9, INK, 0.6);
    y += 0.72;

    s.addImage({ data: I.horizons, x: L, y, w: W, h: W * 250 / 900 });
    y += W * 250 / 900 + 0.16;

    y = head(s, y, "WHAT IS ALLOWED TO CHANGE, AND WHAT IS NOT");
    const CH = [
      ["May change", G_DARK, [
        "The typeface, if NZDF changes its own. The system specifies weight relationships and measure, not a named font.",
        "The medium. Print, web, native application, whatever follows. The component survives the transport.",
        "The notation set, by extension. New marks are added when new content types genuinely appear.",
        "Photography, continuously. Imagery should always look like this year's Army.",
      ]],
      ["Must not change", RED, [
        "The meaning of the grammar. Away from the datum is decision, permanently.",
        "The reservation of red for decision and risk. This is the single constraint that keeps the system readable.",
        "The primacy of the Army logo, and the absence of a Combat Mindset logo.",
        "The requirement that every artefact survives a mono print.",
      ]],
    ];
    const HW2 = (W - 0.24) / 2;
    CH.forEach(([t, c, items], i) => {
      const x = L + i * (HW2 + 0.24);
      s.addText(t.toUpperCase(), { x, y, w: HW2, h: 0.2, fontFace: F, fontSize: 7.2, bold: true,
        color: c, charSpacing: 1.4, align: "left", valign: "middle", margin: 0 });
      s.addShape("rect", { x, y: y + 0.2, w: HW2, h: 0.02, fill: { color: c } });
      bullets(s, x, y + 0.3, HW2, items, 8.4, 2.0);
    });
    y += 2.3;

    y = head(s, y, "THE FAILURE MODE TO WATCH FOR");
    s.addShape("rect", { x: L, y, w: W, h: 0.92, fill: { color: PAPER } });
    body(s, L + 0.24, y + 0.14, W - 0.48,
      "Identity systems in defence do not usually die of obsolescence. They die when a capable person arrives, finds the system constraining, and improves it locally. Within three years there are four versions and the signal is gone. The defence against this is not enforcement, it is making the specification good enough, and available enough, that improvising is more work than complying.",
      8.8, INK, 0.66);
  }

  // =======================================================================
  // 22  GOVERNANCE AND NEXT STEPS
  // =======================================================================
  {
    const s = page("Governance", "Governance and next steps",
      "What this document is, what it is not, and what would have to happen for it to become a standard.");

    let y = head(s, 1.94, "STATUS OF THIS DOCUMENT");
    s.addShape("rect", { x: L, y, w: W, h: 1.0, fill: { color: INK } });
    s.addText("This is a proposal, not an approved standard.", { x: L + 0.3, y: y + 0.16, w: W - 0.6,
      h: 0.28, fontFace: F, fontSize: 13, bold: true, color: WHITE, align: "left", valign: "middle", margin: 0 });
    s.addText("It was developed inside ACS and NZALC against the published guidelines. It has not been reviewed by Defence Public Affairs, and no part of it should be issued as authoritative until it has been.", {
      x: L + 0.3, y: y + 0.48, w: W - 0.6, h: 0.44, fontFace: F, fontSize: 8.8, color: "C8C8C8",
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.2 });
    y += 1.18;

    y = head(s, y, "SEQUENCE");
    const STEPS = [
      ["01", "Internal agreement on position", "ACS, NZALC, HPC",
        "Agree that doctrine and controlled information systems are the visual precedent, without claiming doctrinal status for the framework itself. Everything else follows from this position and nothing should be built before it is settled."],
      ["02", "Review by Defence Public Affairs", "Head of Visual Identity and Design",
        "Put the position and the specification to DPA. Expect challenge on the title treatment, the notation family, and the derivation of the field from the Army chevron pattern. Obtain the vector Army logo at the same time."],
      ["03", "Specification written", "ACS with a design agency",
        "Convert this document into a written standard with measurable rules, plus the asset set: notation SVGs, colour tokens, component markup, templates."],
      ["04", "Pilot on real products", "The framework proposal and ELDA material",
        "Apply it to two live products before issuing it. A system that has never been used is a system that has never been tested."],
      ["05", "Issue and version", "NZALC as custodian",
        "Publish under a validated identifier with a version number and a named owner. Review annually, extend by amendment, and resist redesign."],
    ];
    STEPS.forEach(([n, t, who, d]) => {
      s.addShape("ellipse", { x: L, y: y + 0.02, w: 0.3, h: 0.3, fill: { color: RED } });
      s.addText(n, { x: L, y: y + 0.02, w: 0.3, h: 0.3, fontFace: F, fontSize: 8, bold: true,
        color: WHITE, align: "center", valign: "middle", margin: 0 });
      s.addText(t, { x: L + 0.44, y, w: W - 2.2, h: 0.22, fontFace: F, fontSize: 10, bold: true,
        color: INK, align: "left", valign: "middle", margin: 0 });
      s.addText(who, { x: R - 2.0, y, w: 2.0, h: 0.22, fontFace: F, fontSize: 7.4, italic: true,
        color: GREY, align: "right", valign: "middle", margin: 0 });
      body(s, L + 0.44, y + 0.23, W - 0.64, d, 8.6, "3E3E3E", 0.54);
      y += 0.9;
    });

    y = head(s, y - 0.04, "THE TEST TO APPLY IN TEN YEARS");
    s.addShape("rect", { x: L, y, w: W, h: 1.16, fill: { color: PAPER } });
    s.addShape("rect", { x: L, y, w: 0.05, h: 1.16, fill: { color: RED } });
    s.addText("Open two Combat Mindset products made a decade apart, by different people, in different\nmedia. If they are recognisably the same system, and neither looks like it is trying to\npersuade anyone of anything, the identity has done its work.", {
      x: L + 0.3, y: y + 0.18, w: W - 0.6, h: 0.8, fontFace: F, fontSize: 10.6, bold: true,
      color: INK, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.28 });
  }

  await pres.writeFile({ fileName: "output/combat-mindset-identity-system.pptx" });
  console.log(`written output/combat-mindset-identity-system.pptx  (${PAGE} pages)`);
})();
