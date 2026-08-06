// COMBAT MINDSET : visual identity proposal.
//
// Built against the NZDF and NZ Army Visual Identity Guidelines v1.0 (April
// 2018). The guidelines prohibit programmes from creating their own logos, so
// this is a typographic identity: a wordmark, a lockup with the Army logo, and
// the Army's own sanctioned graphic elements. No new symbol is invented.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

// ---- Army palette, taken from the guidelines (p58) -------------------------
const BLACK = "000000";        // Process Black C
const RED = "D31145";          // Pantone 200 C, rgb 211 17 69
const WHITE = "FFFFFF";
const G_LIGHT = "DFD8AD";      // Pantone 5855 C
const G_MID = "B3A650";        // Pantone 5853 C
const G_OLIVE = "444D06";      // Pantone 5747 C
const G_DARK = "00261B";       // Pantone 5605 C
const GREY = "7F7F7F";

// Production face is Neue Haas Grotesk; Arial Black is the sanctioned PC
// substitute for bold, Calibri for body. The board is set in Arial so the
// preview renders faithfully on any machine.
const F = "Arial";
const F_HEAVY = "Arial";

const LOGO = "assets/nz-army-logo.png";

async function svgPng(body, w, h, px) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}">${body}</svg>`;
  const buf = await sharp(Buffer.from(svg)).resize(px, Math.round((px * h) / w)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---- the sanctioned Army elements (guidelines p61) -------------------------

// Pennant: flat-topped block whose lower edge breaks into two chevrons, with
// echoing chevron lines beneath. Reproduced, not redrawn.
function pennant(colour) {
  const w = 200, top = 0, base = 110, tip = 150;
  const edge = `L${w},${base} L${w * 0.75},${tip} L${w * 0.5},${base} L${w * 0.25},${tip} L0,${base}`;
  let echoes = "";
  for (let i = 1; i <= 3; i++) {
    const o = i * 20;
    echoes += `<path d="M0,${base + o} L${w * 0.25},${tip + o} L${w * 0.5},${base + o} ` +
              `L${w * 0.75},${tip + o} L${w},${base + o}" fill="none" ` +
              `stroke="#${colour}" stroke-width="7"/>`;
  }
  return {
    body: `<path d="M0,${top} L${w},${top} ${edge} Z" fill="#${colour}"/>${echoes}`,
    w, h: 220,
  };
}

// Graduated dot rule closing on a triangle.
function dotRule(colour) {
  const w = 400, h = 30, n = 18;
  let dots = "";
  for (let i = 0; i < n; i++) {
    const t = i / (n - 1);
    const r = 7 - 5.4 * t;
    dots += `<circle cx="${10 + t * 330}" cy="15" r="${r.toFixed(2)}" fill="#${colour}"/>`;
  }
  return { body: `${dots}<path d="M358,4 L392,15 L358,26 Z" fill="none" stroke="#${colour}" stroke-width="3"/>`, w, h };
}

// The chevron rule proposed as the recurring Combat Mindset signal. It is the
// Army element at p61, not a new device.
function chevronRule(colour, weight = 9) {
  const w = 400, h = 40, span = 50;
  let d = "M0,30";
  for (let x = 0; x < w; x += span) d += ` L${x + span / 2},10 L${x + span},30`;
  return { body: `<path d="${d}" fill="none" stroke="#${colour}" stroke-width="${weight}" stroke-linejoin="miter"/>`, w, h };
}

// Halftone chevron pattern (guidelines p62), used as a background tint.
function halftone(colour, opacity = 1) {
  const w = 300, h = 300, step = 11;
  let dots = "";
  for (let y = 0; y < h; y += step) {
    for (let x = 0; x < w; x += step) {
      const phase = Math.abs(((x + y) % 120) - 60) / 60;
      const r = 1.0 + 2.2 * Math.pow(phase, 2.2);
      dots += `<circle cx="${x}" cy="${y}" r="${r.toFixed(2)}" fill="#${colour}" opacity="${opacity}"/>`;
    }
  }
  return { body: dots, w, h };
}

// A crossed-out box, matching how the guidelines mark incorrect use.
function crossBox() {
  return { body: `<path d="M4,4 L196,116 M196,4 L4,116" stroke="#231F20" stroke-width="2.4" fill="none"/>`, w: 200, h: 120 };
}

// Shield outline, standing in for any invented symbol.
function shieldGhost() {
  return { body: `<path d="M100,14 L168,38 V78 C168,108 138,128 100,140 C62,128 32,108 32,78 V38 Z" ` +
                 `fill="none" stroke="#9C9C9C" stroke-width="6"/>` +
                 `<path d="M100,52 L112,78 H88 Z" fill="#9C9C9C"/>`, w: 200, h: 154 };
}

// Unit patch, standing in for badge and patch use.
function patchGhost() {
  return { body: `<rect x="26" y="14" width="148" height="126" rx="26" fill="none" ` +
                 `stroke="#9C9C9C" stroke-width="6"/>` +
                 `<circle cx="100" cy="77" r="30" fill="none" stroke="#9C9C9C" stroke-width="6"/>`, w: 200, h: 154 };
}

(async () => {
  const P = {
    pennantRed: await svgPng(...Object.values(pennant(RED)).slice(0, 1), 200, 220, 400),
  };
  const img = async (o, px) => svgPng(o.body, o.w, o.h, px);

  const I = {
    pennant: await img(pennant(RED), 420),
    pennantWhite: await img(pennant(WHITE), 420),
    dots: await img(dotRule(RED), 800),
    chev: await img(chevronRule(RED), 800),
    chevWhite: await img(chevronRule(WHITE), 800),
    tint: await img(halftone(BLACK, 0.07), 700),
    tintOnRed: await img(halftone(BLACK, 0.18), 700),
    tintOnDark: await img(halftone(WHITE, 0.30), 700),
    cross: await img(crossBox(), 520),
    shieldGhost: await img(shieldGhost(), 300),
    patchGhost: await img(patchGhost(), 300),
  };

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "NZ Army Combat Mindset Visual Identity";
  pres.subject = "Visual identity proposal, reviewed against NZDF and NZ Army Visual Identity Guidelines v1.0";
  pres.company = "Army Command School";

  const L = 0.5, W = 7.27, R = L + W;

  // ---- shared furniture ---------------------------------------------------
  function page(n, title, strap) {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addImage({ path: LOGO, x: L, y: 0.38, w: 1.62, h: 0.370 });
    s.addText(title, { x: L, y: 0.9, w: W - 0.8, h: 0.3, fontFace: F_HEAVY, fontSize: 15,
      bold: true, color: BLACK, align: "left", valign: "middle", margin: 0, charSpacing: 0.4 });
    s.addText(strap, { x: L, y: 1.2, w: W - 0.8, h: 0.2, fontFace: F, fontSize: 8.5,
      color: GREY, align: "left", valign: "middle", margin: 0 });
    s.addText(`${n} / 3`, { x: R - 0.8, y: 0.9, w: 0.8, h: 0.3, fontFace: F, fontSize: 9,
      bold: true, color: RED, align: "right", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L, y: 1.48, w: W, h: 0.035, fill: { color: RED } });
    s.addText("A FORCE FOR NEW ZEALAND", { x: L, y: 11.24, w: 3, h: 0.18, fontFace: F_HEAVY,
      fontSize: 6.5, bold: true, color: BLACK, charSpacing: 0.8, align: "left", valign: "middle", margin: 0 });
    s.addText("Army Command School   |   August 2026", { x: R - 3.4, y: 11.24, w: 3.4, h: 0.18,
      fontFace: F, fontSize: 6.5, color: GREY, align: "right", valign: "middle", margin: 0 });
    return s;
  }

  function label(s, y, text) {
    s.addText(text, { x: L, y, w: W, h: 0.2, fontFace: F_HEAVY, fontSize: 8, bold: true,
      color: BLACK, charSpacing: 1.6, align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L, y: y + 0.2, w: W, h: 0.008, fill: { color: "D8D8D8" } });
  }

  // =========================================================================
  // PAGE 1 : the governing rule
  // =========================================================================
  {
    const s = page(1, "COMBAT MINDSET VISUAL IDENTITY", "Reviewed against the NZDF and NZ Army Visual Identity Guidelines, version 1.0, April 2018");

    label(s, 1.72, "THE GOVERNING RULE");

    s.addShape("rect", { x: L, y: 2.06, w: W, h: 1.62, fill: { color: BLACK } });
    s.addImage({ data: I.tintOnDark, x: L, y: 2.06, w: W, h: 1.62, transparency: 88 });
    s.addText("Programmes and projects should not create new logos.", {
      x: L + 0.34, y: 2.24, w: W - 0.68, h: 0.34, fontFace: F_HEAVY, fontSize: 15, bold: true,
      color: WHITE, align: "left", valign: "middle", margin: 0 });
    s.addText("The official NZDF logo should be used alongside the name of the programme or project in plain text.", {
      x: L + 0.34, y: 2.60, w: W - 0.68, h: 0.46, fontFace: F, fontSize: 11.5,
      color: WHITE, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });
    s.addShape("rect", { x: L + 0.34, y: 3.14, w: 0.6, h: 0.022, fill: { color: RED } });
    s.addText("NZDF Visual Identity Guidelines v1.0, page 34", {
      x: L + 0.34, y: 3.24, w: W - 0.68, h: 0.2, fontFace: F, fontSize: 8, italic: true,
      color: "BFBFBF", align: "left", valign: "middle", margin: 0 });
    s.addText("Supporting: unit and trade patches “should not be used as a logo in any form of internal or external communication” (p9, p33). Portfolios, Commands and Units “use their name in plain text alongside the NZDF logo” (p9).", {
      x: L + 0.34, y: 3.42, w: W - 0.68, h: 0.24, fontFace: F, fontSize: 7.6,
      color: "9C9C9C", align: "left", valign: "middle", margin: 0 });

    label(s, 3.94, "WHAT THIS MEANS");

    const findings = [
      ["Combat Mindset is a programme of work.",
       "It does not get a brandmark, a badge or a patch. The earlier symbol explorations cannot be used, however well drawn."],
      ["The identity is therefore typographic.",
       "A wordmark, a lockup with the Army logo, and the Army’s own graphic elements. Everything below is drawn from the sanctioned system."],
      ["A bespoke mark is not impossible, but it is not ours to make.",
       "It would require the Head of Visual Identity and Design, Defence Public Affairs. A badge would require the Chief of Army."],
    ];
    let fy = 4.3;
    findings.forEach(([h, b], i) => {
      s.addShape("rect", { x: L, y: fy, w: 0.028, h: 0.56, fill: { color: RED } });
      s.addText(h, { x: L + 0.2, y: fy, w: W - 0.2, h: 0.22, fontFace: F_HEAVY, fontSize: 10,
        bold: true, color: BLACK, align: "left", valign: "middle", margin: 0 });
      s.addText(b, { x: L + 0.2, y: fy + 0.21, w: W - 0.4, h: 0.34, fontFace: F, fontSize: 8.8,
        color: "3F3F3F", align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.12 });
      fy += 0.68;
    });

    label(s, 6.44, "THE THREE COMPONENTS");

    const comps = [
      ["01", "WORDMARK", "COMBAT MINDSET set in the Army’s own typeface, with the red rule. Used where the programme names itself."],
      ["02", "LOCKUP", "The Army logo with the programme name in plain text. The form required by the guidelines for all collateral."],
      ["03", "ELEMENT", "The Army chevron, used as the recurring signal across Combat Mindset material in place of a symbol."],
    ];
    const CW = (W - 0.28) / 3;
    comps.forEach(([n, t, d], i) => {
      const x = L + i * (CW + 0.14);
      s.addShape("rect", { x, y: 6.78, w: CW, h: 1.34, fill: { color: "F4F4F2" } });
      s.addShape("rect", { x, y: 6.78, w: CW, h: 0.03, fill: { color: RED } });
      s.addText(n, { x: x + 0.18, y: 6.9, w: CW - 0.36, h: 0.22, fontFace: F_HEAVY, fontSize: 9,
        bold: true, color: RED, align: "left", valign: "middle", margin: 0 });
      s.addText(t, { x: x + 0.18, y: 7.12, w: CW - 0.36, h: 0.26, fontFace: F_HEAVY, fontSize: 12,
        bold: true, color: BLACK, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
      s.addText(d, { x: x + 0.18, y: 7.42, w: CW - 0.36, h: 0.6, fontFace: F, fontSize: 8,
        color: "3F3F3F", align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.12 });
    });

    label(s, 8.36, "THE PROPOSED WORDMARK");

    // hero specimen, reversed out of black with the halftone chevron tint
    s.addShape("rect", { x: L, y: 8.7, w: W, h: 2.2, fill: { color: BLACK } });
    s.addImage({ data: I.tintOnDark, x: L, y: 8.7, w: W, h: 2.2, transparency: 86 });
    s.addText("COMBAT", { x: L + 0.5, y: 9.06, w: W - 1, h: 0.52, fontFace: F_HEAVY, fontSize: 40,
      bold: true, color: WHITE, charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
    s.addText("MINDSET", { x: L + 0.5, y: 9.56, w: W - 1, h: 0.52, fontFace: F_HEAVY, fontSize: 40,
      bold: true, color: WHITE, charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L + 0.5, y: 10.18, w: 1.5, h: 0.045, fill: { color: RED } });
    s.addText("Remain effective. Act decisively. Harder to kill.", {
      x: L + 0.5, y: 10.28, w: W - 1, h: 0.24, fontFace: F, fontSize: 11,
      color: WHITE, align: "left", valign: "middle", margin: 0 });
  }

  // =========================================================================
  // PAGE 2 : the system
  // =========================================================================
  {
    const s = page(2, "THE SYSTEM", "Wordmark, lockup, element, colour and type");

    // ---- wordmark variants ----
    label(s, 1.72, "WORDMARK  —  THREE PERMITTED RENDERINGS");

    const wmW = (W - 0.28) / 3, wmY = 2.06, wmH = 1.5;
    const variants = [
      ["Primary", WHITE, BLACK, RED, "F4F4F2"],
      ["Reverse", BLACK, WHITE, RED, null],
      ["One colour", WHITE, BLACK, BLACK, "F4F4F2"],
    ];
    variants.forEach(([name, bg, ink, rule, border], i) => {
      const x = L + i * (wmW + 0.14);
      s.addShape("rect", { x, y: wmY, w: wmW, h: wmH, fill: { color: bg },
        line: border ? { color: "D8D8D8", width: 1 } : undefined });
      s.addText("COMBAT", { x: x + 0.22, y: wmY + 0.36, w: wmW - 0.44, h: 0.28, fontFace: F_HEAVY,
        fontSize: 17, bold: true, color: ink, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
      s.addText("MINDSET", { x: x + 0.22, y: wmY + 0.62, w: wmW - 0.44, h: 0.28, fontFace: F_HEAVY,
        fontSize: 17, bold: true, color: ink, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
      s.addShape("rect", { x: x + 0.22, y: wmY + 0.94, w: 0.62, h: 0.028, fill: { color: rule } });
      s.addText(name, { x: x + 0.22, y: wmY + 1.08, w: wmW - 0.44, h: 0.2, fontFace: F, fontSize: 7.6,
        italic: true, color: ink === WHITE ? "BFBFBF" : GREY, align: "left", valign: "middle", margin: 0 });
    });
    s.addText("The rule is set to the cap height of the M and always sits beneath the second line. Red on light and dark grounds; black in one-colour work. Never coloured type, never outlined, never set in any face other than the Army’s.", {
      x: L, y: 3.62, w: W, h: 0.3, fontFace: F, fontSize: 7.8, color: "3F3F3F",
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.12 });

    // ---- lockup ----
    label(s, 4.0, "LOCKUP  —  THE REQUIRED FORM ON ALL COLLATERAL");

    s.addShape("rect", { x: L, y: 4.34, w: W, h: 1.66, fill: { color: "F4F4F2" } });

    // horizontal
    s.addImage({ path: LOGO, x: L + 0.3, y: 4.66, w: 1.62, h: 0.370 });
    s.addShape("rect", { x: L + 2.12, y: 4.6, w: 0.014, h: 0.52, fill: { color: "C8C8C8" } });
    s.addText("Combat Mindset", { x: L + 2.34, y: 4.6, w: 3.2, h: 0.26, fontFace: F_HEAVY,
      fontSize: 13, bold: true, color: BLACK, align: "left", valign: "middle", margin: 0 });
    s.addText("Framework Proposal", { x: L + 2.34, y: 4.86, w: 3.2, h: 0.26, fontFace: F_HEAVY,
      fontSize: 13, bold: true, color: BLACK, align: "left", valign: "middle", margin: 0 });
    s.addText("Horizontal", { x: L + 0.3, y: 5.16, w: 2, h: 0.18, fontFace: F, fontSize: 7.6,
      italic: true, color: GREY, align: "left", valign: "middle", margin: 0 });

    // stacked
    s.addImage({ path: LOGO, x: L + 4.7, y: 4.56, w: 1.34, h: 0.306 });
    s.addShape("rect", { x: L + 4.7, y: 4.96, w: 0.5, h: 0.022, fill: { color: RED } });
    s.addText("Combat Mindset", { x: L + 4.7, y: 5.04, w: 2.3, h: 0.24, fontFace: F_HEAVY,
      fontSize: 12, bold: true, color: BLACK, align: "left", valign: "middle", margin: 0 });
    s.addText("Stacked", { x: L + 4.7, y: 5.3, w: 2, h: 0.18, fontFace: F, fontSize: 7.6,
      italic: true, color: GREY, align: "left", valign: "middle", margin: 0 });

    s.addText("Name in plain text, title case, Neue Haas Grotesk Bold (Arial Bold substitute), never inside a shape and never set as a device. Clear space each side is the height of the N in NZ. Minimum logo width 35 mm.", {
      x: L + 0.3, y: 5.56, w: W - 0.6, h: 0.34, fontFace: F, fontSize: 7.8, color: "3F3F3F",
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.12 });

    // ---- element ----
    label(s, 6.1, "ELEMENT  —  THE ARMY CHEVRON, IN PLACE OF A SYMBOL");

    s.addShape("rect", { x: L, y: 6.44, w: 2.3, h: 1.5, fill: { color: WHITE }, line: { color: "D8D8D8", width: 1 } });
    s.addImage({ data: I.pennant, x: L + 0.72, y: 6.6, w: 0.86, h: 0.946 });
    s.addText("Pennant", { x: L, y: 7.62, w: 2.3, h: 0.18, fontFace: F, fontSize: 7.6, italic: true,
      color: GREY, align: "center", valign: "middle", margin: 0 });

    s.addShape("rect", { x: L + 2.44, y: 6.44, w: W - 2.44, h: 1.5, fill: { color: WHITE }, line: { color: "D8D8D8", width: 1 } });
    s.addImage({ data: I.chev, x: L + 2.66, y: 6.62, w: 4.4, h: 0.44 });
    s.addImage({ data: I.dots, x: L + 2.66, y: 7.12, w: 4.4, h: 0.33 });
    s.addText("Chevron rule and graduated dot rule, both from the Army element set (guidelines p61).", {
      x: L + 2.66, y: 7.56, w: W - 2.88, h: 0.28, fontFace: F, fontSize: 7.6, color: "3F3F3F",
      align: "left", valign: "top", margin: 0 });

    // ---- colour ----
    label(s, 8.06, "COLOUR  —  AS PUBLISHED, NOT AS PREVIOUSLY USED");

    const sw = [
      ["Black", BLACK, "Process Black C", "0 0 0", WHITE],
      ["Army Red", RED, "Pantone 200 C", "211 17 69", WHITE],
      ["White", WHITE, "White", "255 255 255", BLACK],
      ["5855 C", G_LIGHT, "Secondary", "223 216 173", BLACK],
      ["5853 C", G_MID, "Secondary", "179 166 80", BLACK],
      ["5747 C", G_OLIVE, "Secondary", "68 77 6", WHITE],
      ["5605 C", G_DARK, "Secondary", "0 38 27", WHITE],
    ];
    const SW = (W - 6 * 0.08) / 7;
    sw.forEach(([n, hex, pan, rgb, ink], i) => {
      const x = L + i * (SW + 0.08);
      s.addShape("rect", { x, y: 8.4, w: SW, h: 0.86, fill: { color: hex },
        line: hex === WHITE ? { color: "D8D8D8", width: 1 } : undefined });
      s.addText(n, { x: x + 0.06, y: 8.46, w: SW - 0.12, h: 0.18, fontFace: F_HEAVY, fontSize: 7,
        bold: true, color: ink, align: "left", valign: "middle", margin: 0 });
      s.addText(`#${hex}`, { x: x + 0.06, y: 9.0, w: SW - 0.12, h: 0.18, fontFace: F, fontSize: 6,
        color: ink, align: "left", valign: "middle", margin: 0 });
      s.addText(rgb, { x, y: 9.28, w: SW, h: 0.16, fontFace: F, fontSize: 5.8,
        color: GREY, align: "left", valign: "middle", margin: 0 });
    });
    s.addText("Correction. Earlier Combat Mindset material used red C62026 and four approximated greens. The published Army values are above; the red in particular is materially different and should be replaced everywhere.", {
      x: L, y: 9.5, w: W, h: 0.3, fontFace: F, fontSize: 7.8, color: "3F3F3F",
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.12 });

    // ---- type ----
    label(s, 9.9, "TYPE");

    s.addShape("rect", { x: L, y: 10.24, w: W, h: 0.86, fill: { color: "F4F4F2" } });
    s.addText([
      { text: "Neue Haas Grotesk", options: { bold: true, fontSize: 12, color: BLACK } },
      { text: "   primary, all headings and the wordmark", options: { fontSize: 8.5, color: "3F3F3F" } },
    ], { x: L + 0.24, y: 10.34, w: W - 0.48, h: 0.24, fontFace: F, align: "left", valign: "middle", margin: 0 });
    s.addText([
      { text: "Publico", options: { bold: true, fontSize: 12, color: BLACK } },
      { text: "   secondary, used sparingly for pull quotes and captions", options: { fontSize: 8.5, color: "3F3F3F" } },
    ], { x: L + 0.24, y: 10.58, w: W - 0.48, h: 0.24, fontFace: F, align: "left", valign: "middle", margin: 0 });
    s.addText("Everyday PC substitutes, per the guidelines: Arial Black for bold headings, Calibri for body copy, Book Antiqua for Publico. The guidelines state no other fonts are acceptable.", {
      x: L + 0.24, y: 10.82, w: W - 0.48, h: 0.22, fontFace: F, fontSize: 7.6, italic: true,
      color: GREY, align: "left", valign: "middle", margin: 0 });
  }

  // =========================================================================
  // PAGE 3 : applied, and what not to do
  // =========================================================================
  {
    const s = page(3, "APPLIED", "The identity in use, and the uses the guidelines rule out");

    label(s, 1.72, "DOCUMENT COVER");

    // --- cover mock, following the Army report template (p64) ---
    const cx = L, cy = 2.06, cw = 2.5, ch = 3.54;
    s.addShape("rect", { x: cx, y: cy, w: cw, h: ch, fill: { color: WHITE }, line: { color: "D8D8D8", width: 1 } });
    s.addImage({ path: LOGO, x: cx + 0.2, y: cy + 0.22, w: 0.94, h: 0.215 });
    s.addText("COMBAT\nMINDSET", { x: cx + 0.2, y: cy + 1.2, w: cw - 0.4, h: 0.62, fontFace: F_HEAVY,
      fontSize: 15, bold: true, color: BLACK, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 0.95 });
    s.addShape("rect", { x: cx + 0.2, y: cy + 1.86, w: 0.5, h: 0.024, fill: { color: RED } });
    s.addText("Framework Proposal", { x: cx + 0.2, y: cy + 1.94, w: cw - 0.4, h: 0.2, fontFace: F,
      fontSize: 7.5, color: "3F3F3F", align: "left", valign: "middle", margin: 0 });
    s.addImage({ data: I.tint, x: cx, y: cy + 2.3, w: cw, h: 1.24, transparency: 25 });
    s.addText("A FORCE FOR NEW ZEALAND", { x: cx + 0.2, y: cy + ch - 0.3, w: cw - 0.4, h: 0.16,
      fontFace: F_HEAVY, fontSize: 5, bold: true, color: BLACK, charSpacing: 0.5, align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: cx, y: cy + ch - 0.06, w: cw, h: 0.045, fill: { color: RED } });

    // --- slide mock ---
    const sx = L + 2.66, sw2 = W - 2.66, sy = 2.06, sh = 2.0;
    s.addShape("rect", { x: sx, y: sy, w: sw2, h: sh, fill: { color: RED } });
    s.addImage({ data: I.tintOnRed, x: sx, y: sy, w: sw2, h: sh, transparency: 40 });
    s.addImage({ path: LOGO, x: sx + 0.24, y: sy + 0.2, w: 1.06, h: 0.242 });
    s.addText("COMBAT MINDSET", { x: sx + 0.24, y: sy + 0.74, w: sw2 - 0.48, h: 0.36, fontFace: F_HEAVY,
      fontSize: 20, bold: true, color: WHITE, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
    s.addText("Remain effective. Act decisively. Harder to kill.", { x: sx + 0.24, y: sy + 1.12, w: sw2 - 0.48,
      h: 0.22, fontFace: F, fontSize: 9, color: WHITE, align: "left", valign: "middle", margin: 0 });
    s.addText("A FORCE FOR NEW ZEALAND", { x: sx + 0.24, y: sy + sh - 0.34, w: 2, h: 0.16,
      fontFace: F_HEAVY, fontSize: 5.5, bold: true, color: WHITE, charSpacing: 0.5, align: "left", valign: "middle", margin: 0 });

    // --- section divider mock ---
    const dy = sy + sh + 0.16, dh = ch - sh - 0.16;
    s.addShape("rect", { x: sx, y: dy, w: sw2, h: dh, fill: { color: G_DARK } });
    s.addImage({ data: I.chevWhite, x: sx + 0.24, y: dy + 0.24, w: 1.6, h: 0.16 });
    s.addText("PERFORMANCE\nUNDER PRESSURE", { x: sx + 0.24, y: dy + 0.5, w: sw2 - 0.48, h: 0.5,
      fontFace: F_HEAVY, fontSize: 13, bold: true, color: WHITE, align: "left", valign: "top",
      margin: 0, lineSpacingMultiple: 0.98 });
    s.addText("The enabling capability", { x: sx + 0.24, y: dy + 1.02, w: sw2 - 0.48, h: 0.2,
      fontFace: F, fontSize: 8, color: G_LIGHT, align: "left", valign: "middle", margin: 0 });

    label(s, 5.86, "INCORRECT USE  —  RULED OUT BY THE GUIDELINES");

    const BW = (W - 3 * 0.12) / 4, BH = 1.06;
    const bad = [
      ["A bespoke symbol", "Any invented mark, however well drawn. Programmes do not create logos.",
        (x, y) => s.addImage({ data: I.shieldGhost, x: x + BW / 2 - 0.32, y: y + 0.14, w: 0.64, h: 0.49 })],
      ["A badge or patch", "Patches are heritage items for uniforms. They are not communication assets.",
        (x, y) => s.addImage({ data: I.patchGhost, x: x + BW / 2 - 0.32, y: y + 0.14, w: 0.64, h: 0.49 })],
      ["An altered Army logo", "The logo’s colours, proportions and background are fixed.",
        (x, y) => {
          s.addShape("rect", { x: x + BW / 2 - 0.56, y: y + 0.2, w: 1.12, h: 0.38, fill: { color: G_MID } });
          s.addImage({ path: LOGO, x: x + BW / 2 - 0.44, y: y + 0.27, w: 0.88, h: 0.201 });
        }],
      ["A coloured wordmark", "The wordmark is black, white or reversed. Red is the rule, not the type.",
        (x, y) => {
          s.addText("COMBAT", { x, y: y + 0.18, w: BW, h: 0.22, fontFace: F_HEAVY, fontSize: 11,
            bold: true, color: RED, align: "center", valign: "middle", margin: 0 });
          s.addText("MINDSET", { x, y: y + 0.38, w: BW, h: 0.22, fontFace: F_HEAVY, fontSize: 11,
            bold: true, color: RED, align: "center", valign: "middle", margin: 0 });
        }],
    ];
    bad.forEach(([t, d, draw], i) => {
      const x = L + i * (BW + 0.12);
      s.addShape("rect", { x, y: 6.2, w: BW, h: BH, fill: { color: "F4F4F2" } });
      draw(x, 6.2);
      s.addImage({ data: I.cross, x: x + 0.1, y: 6.28, w: BW - 0.2, h: (BW - 0.2) * 0.6 });
      s.addText(t, { x: x + 0.02, y: 7.3, w: BW - 0.04, h: 0.2, fontFace: F_HEAVY, fontSize: 8,
        bold: true, color: BLACK, align: "left", valign: "middle", margin: 0 });
      s.addText(d, { x: x + 0.02, y: 7.48, w: BW - 0.04, h: 0.5, fontFace: F, fontSize: 7,
        color: "3F3F3F", align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });
    });

    label(s, 8.14, "WHAT TO DO NEXT");

    const steps = [
      ["Adopt the typographic identity now.", "It is compliant, it needs no approval, and it can be applied to the framework proposal and the ELDA one pager immediately."],
      ["Correct the colour across existing material.", "Replace C62026 with D31145 and the four approximated greens with the published values."],
      ["If a mark is genuinely wanted, ask properly.", "Head of Visual Identity and Design, Defence Public Affairs, 04 496 0297. Expect the answer to be no, and expect that to be the right answer."],
    ];
    let sy2 = 8.48;
    steps.forEach(([h, b], i) => {
      s.addShape("ellipse", { x: L, y: sy2 + 0.02, w: 0.28, h: 0.28, fill: { color: RED } });
      s.addText(String(i + 1), { x: L, y: sy2 + 0.02, w: 0.28, h: 0.28, fontFace: F_HEAVY, fontSize: 9,
        bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
      s.addText(h, { x: L + 0.42, y: sy2, w: W - 0.42, h: 0.22, fontFace: F_HEAVY, fontSize: 9.6,
        bold: true, color: BLACK, align: "left", valign: "middle", margin: 0 });
      s.addText(b, { x: L + 0.42, y: sy2 + 0.21, w: W - 0.62, h: 0.36, fontFace: F, fontSize: 8.4,
        color: "3F3F3F", align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.12 });
      sy2 += 0.66;
    });

    s.addShape("rect", { x: L, y: 10.62, w: W, h: 0.42, fill: { color: "F4F4F2" } });
    s.addText("Note. This board is set in Arial so it renders identically on any machine. Production artwork should be set in Neue Haas Grotesk, or Arial Black where that face is not held.", {
      x: L + 0.2, y: 10.62, w: W - 0.4, h: 0.42, fontFace: F, fontSize: 7.6, italic: true,
      color: GREY, align: "left", valign: "middle", margin: 0 });
  }

  await pres.writeFile({ fileName: "output/combat-mindset-identity.pptx" });
  console.log("written output/combat-mindset-identity.pptx");
})();
