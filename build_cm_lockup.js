// COMBAT MINDSET : lockup with the NZ Army logo.
//
// The guidelines fix the logo and leave the pairing open: "There is no fixed
// lockup with the NZDF logo, this is left flexible to allow for the
// appropriate placement given the specific context" (p33). What they do fix
// is that the name is set in plain text, title case, Neue Haas Grotesk Bold,
// and that the logo keeps its clear space of one N height on all sides.
//
// Measured from the artwork: the N is 0.531 of the logo height, so clear
// space is 0.1212 of the logo width. Nothing here is guessed.

const pptxgen = require("pptxgenjs");

const BLACK = "000000", RED = "D31145", WHITE = "FFFFFF";
const G_DARK = "00261B";
const INK = "1A1A1A", GREY = "6E6E6E", RULE = "D2D2D2", PAPER = "F5F5F3";
const F = "Arial";                    // Neue Haas Grotesk in production
const LOGO = "assets/nz-army-logo.png";
const LOGO_WHITE = "assets/nz-army-logo-white.png";
const AR = 4.380;                     // logo width : height
const NCAP = 0.1212;                  // clear space, as a fraction of logo width
const CAPH = 0.1212;                  // NZ ARMY cap height, same fraction

// Point size whose cap height is `k` times the logo's cap height.
const nameSize = (logoW, k) => (logoW * CAPH * k * 72) / 0.716;

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "Combat Mindset lockup";
  pres.subject = "Lockup of the Combat Mindset name with the NZ Army logo";
  pres.company = "Army Command School";

  const L = 0.62, W = 7.03, R = L + W;
  let PAGE = 0;

  function page(section, title, strap) {
    PAGE += 1;
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText(section.toUpperCase(), { x: L, y: 0.42, w: W - 1, h: 0.18, fontFace: F,
      fontSize: 7, bold: true, color: INK, charSpacing: 1.4, align: "left", valign: "middle", margin: 0 });
    s.addText(`0${PAGE}`, { x: R - 0.6, y: 0.42, w: 0.6, h: 0.18, fontFace: F, fontSize: 7,
      bold: true, color: GREY, align: "right", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L, y: 0.64, w: W, h: 0.012, fill: { color: INK } });
    s.addText(title, { x: L, y: 0.8, w: W, h: 0.34, fontFace: F, fontSize: 19, bold: true,
      color: INK, align: "left", valign: "middle", margin: 0 });
    s.addText(strap, { x: L, y: 1.16, w: W - 0.3, h: 0.44, fontFace: F, fontSize: 9.4,
      color: GREY, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.2 });
    s.addText("COMBAT MINDSET   LOCKUP", { x: L, y: 11.16, w: 4, h: 0.16, fontFace: F,
      fontSize: 6, color: GREY, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
    s.addText("DRAFT   |   AUGUST 2026", { x: R - 3, y: 11.16, w: 3, h: 0.16, fontFace: F,
      fontSize: 6, color: GREY, charSpacing: 0.6, align: "right", valign: "middle", margin: 0 });
    return s;
  }

  function head(s, y, text) {
    s.addText(text, { x: L, y, w: W, h: 0.2, fontFace: F, fontSize: 7.4, bold: true,
      color: INK, charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L, y: y + 0.2, w: W, h: 0.008, fill: { color: RULE } });
    return y + 0.34;
  }

  // ---- the lockups ---------------------------------------------------------
  // Each draws itself at a given origin and logo width, and returns its height.

  // Horizontal. Name set beside the logo, one clear space away, optically
  // centred on the logo. The sanctioned pattern at p33.
  function horizontal(s, x, y, lw, opts = {}) {
    const lh = lw / AR, gap = lw * NCAP;
    const ink = opts.ink || INK;
    const size = nameSize(lw, opts.k || 0.78);
    s.addImage({ path: opts.ink === WHITE ? LOGO_WHITE : LOGO, x, y, w: lw, h: lh });
    s.addText(opts.name || "Combat Mindset", {
      x: x + lw + gap, y, w: lw * 1.5, h: lh, fontFace: F, fontSize: size, bold: true,
      color: ink, align: "left", valign: "middle", margin: 0 });
    return lh;
  }

  // Stacked, hung from the datum. The rule is the adopted device: it separates
  // the two without introducing a new element, and it is always horizontal.
  function stacked(s, x, y, lw, opts = {}) {
    const lh = lw / AR, gap = lw * NCAP;
    const ink = opts.ink || INK;
    const size = nameSize(lw, opts.k || 0.86);
    s.addImage({ path: opts.ink === WHITE ? LOGO_WHITE : LOGO, x, y, w: lw, h: lh });
    const ry = y + lh + gap;
    s.addShape("rect", { x, y: ry, w: lw, h: lw * 0.012, fill: { color: ink } });
    s.addText(opts.name || "Combat Mindset", {
      x, y: ry + lw * 0.012 + gap * 0.35, w: lw * 1.6, h: size / 60, fontFace: F,
      fontSize: size, bold: true, color: ink, align: "left", valign: "top", margin: 0 });
    return lh + gap + lw * 0.012 + gap * 0.35 + size / 60;
  }

  // =========================================================================
  // PAGE 1 : options
  // =========================================================================
  {
    const s = page("Lockup", "Combat Mindset and the NZ Army logo",
      "Six pairings, all built only from the logo and plain text. The guidelines fix the logo, its clear space and its minimum size, and set the name in plain text, title case, in the Army's own face. They leave the arrangement open.");

    let y = head(s, 1.86, "SIX PAIRINGS");

    const BOX = 1.42, LW = 1.28;
    const OPTS = [
      ["A", "Horizontal", "Name beside the logo, one clear space away. The pattern the guidelines illustrate.",
        (s, x, yy) => horizontal(s, x + 0.24, yy + 0.52, LW)],
      ["B", "Horizontal, two line", "For where the full name of the framework is needed.",
        (s, x, yy) => horizontal(s, x + 0.24, yy + 0.52, LW, { name: "Combat Mindset\nFramework", k: 0.6 })],
      ["C", "Stacked, hung from the datum", "The adopted device separating the two. Compact footprint.",
        (s, x, yy) => stacked(s, x + 0.24, yy + 0.3, 1.55)],
      ["D", "Stacked, plain", "The same without the rule. Quieter, and the pairing is looser for it.",
        (s, x, yy) => {
          const lw = 1.55, lh = lw / AR, gap = lw * NCAP;
          s.addImage({ path: LOGO, x: x + 0.24, y: yy + 0.38, w: lw, h: lh });
          s.addText("Combat Mindset", { x: x + 0.24, y: yy + 0.38 + lh + gap, w: lw * 1.6,
            h: 0.34, fontFace: F, fontSize: nameSize(lw, 0.86), bold: true, color: INK,
            align: "left", valign: "top", margin: 0 });
        }],
      ["E", "Uppercase", "Reads harder, but the guidelines set unit and portfolio names in title case.",
        (s, x, yy) => stacked(s, x + 0.24, yy + 0.3, 1.55, { name: "COMBAT MINDSET", k: 0.7 })],
      ["F", "Running, single line", "For headers, footers and spines. The logo drops to minimum size.",
        (s, x, yy) => {
          const lw = 1.05, lh = lw / AR, gap = lw * NCAP;
          s.addImage({ path: LOGO, x: x + 0.24, y: yy + 0.62, w: lw, h: lh });
          s.addText("COMBAT MINDSET", { x: x + 0.24 + lw + gap, y: yy + 0.62, w: 1.8, h: lh,
            fontFace: F, fontSize: 7.2, bold: true, color: INK, charSpacing: 1,
            align: "left", valign: "middle", margin: 0 });
        }],
    ];

    const CW = (W - 0.16) / 2;
    OPTS.forEach(([k, name, note, draw], i) => {
      const col = i % 2, row = Math.floor(i / 2);
      const x = L + col * (CW + 0.16), yy = y + row * (BOX + 0.62);
      s.addShape("rect", { x, y: yy, w: CW, h: BOX, fill: { color: WHITE },
        line: { color: RULE, width: 1 } });
      s.addText(k, { x: x + 0.14, y: yy + 0.1, w: 0.3, h: 0.16, fontFace: F, fontSize: 7,
        bold: true, color: GREY, align: "left", valign: "middle", margin: 0 });
      draw(s, x, yy);
      s.addText(name, { x, y: yy + BOX + 0.06, w: CW, h: 0.18, fontFace: F, fontSize: 8.6,
        bold: true, color: INK, align: "left", valign: "middle", margin: 0 });
      s.addText(note, { x, y: yy + BOX + 0.24, w: CW - 0.1, h: 0.24, fontFace: F,
        fontSize: 7.6, color: "3E3E3E", align: "left", valign: "top", margin: 0,
        lineSpacingMultiple: 1.12 });
    });

    y += 3 * (BOX + 0.62) + 0.02;
    y = head(s, y, "WHAT THE GUIDELINES DECIDE FOR US");
    const facts = [
      ["Clear space", "One N height on all four sides, measured from the artwork at 0.531 of the logo height. Nothing enters it, including the name."],
      ["Minimum size", "35 mm logo width in print. Below that the descriptor stops being readable and the logo may not be used."],
      ["The name", "Plain text, title case, in the Army's own face. Never inside a shape, never on a rule of its own colour, never redrawn."],
      ["Hierarchy", "The logo carries more visual weight than the name in every pairing. The name is set at 78 to 86 per cent of the logo cap height."],
    ];
    facts.forEach(([k, v]) => {
      s.addText(k, { x: L, y, w: 1.4, h: 0.34, fontFace: F, fontSize: 8.4, bold: true,
        color: INK, align: "left", valign: "top", margin: 0 });
      s.addText(v, { x: L + 1.5, y, w: W - 1.5, h: 0.34, fontFace: F, fontSize: 8.4,
        color: "3E3E3E", align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });
      s.addShape("rect", { x: L, y: y + 0.38, w: W, h: 0.006, fill: { color: RULE } });
      y += 0.48;
    });
  }

  // =========================================================================
  // PAGE 2 : the recommended pair
  // =========================================================================
  {
    const s = page("Lockup", "The recommended pair",
      "One horizontal lockup for headers, slides and correspondence, and one stacked lockup for covers and anywhere the measure is narrow. Both are built from the same two parts and the same interval.");

    // --- primary, horizontal, with the clear space shown ---
    let y = head(s, 1.9, "PRIMARY  —  HORIZONTAL");
    const LW = 2.3, lh = LW / AR, gap = LW * NCAP;
    const boxH = lh + 2 * gap;
    s.addShape("rect", { x: L, y, w: W, h: boxH + 0.5, fill: { color: PAPER } });
    const ox = L + 0.55, oy = y + 0.25 + gap;
    // clear-space envelope
    s.addShape("rect", { x: ox - gap, y: oy - gap, w: LW + 2 * gap, h: lh + 2 * gap,
      fill: { color: WHITE }, line: { color: RED, width: 0.75, dashType: "dash" } });
    horizontal(s, ox, oy, LW);
    s.addText(`clear space = one N height = ${(LW * NCAP * 25.4).toFixed(1)} mm at this size`, {
      x: ox - gap, y: y + boxH + 0.24, w: 4, h: 0.18, fontFace: F, fontSize: 6.8,
      italic: true, color: RED, align: "left", valign: "middle", margin: 0 });
    y += boxH + 0.62;

    // --- alternate, stacked ---
    y = head(s, y, "ALTERNATE  —  STACKED");
    const SH = 1.5;
    s.addShape("rect", { x: L, y, w: (W - 0.16) / 2, h: SH, fill: { color: PAPER } });
    stacked(s, L + 0.45, y + 0.34, 1.9);
    s.addShape("rect", { x: L + (W - 0.16) / 2 + 0.16, y, w: (W - 0.16) / 2, h: SH,
      fill: { color: G_DARK } });
    stacked(s, L + (W - 0.16) / 2 + 0.61, y + 0.34, 1.9, { ink: WHITE });
    s.addText("On light grounds", { x: L, y: y + SH + 0.06, w: 2, h: 0.18, fontFace: F,
      fontSize: 7.4, italic: true, color: GREY, align: "left", valign: "middle", margin: 0 });
    s.addText("Reversed, one colour", { x: L + (W - 0.16) / 2 + 0.16, y: y + SH + 0.06, w: 2,
      h: 0.18, fontFace: F, fontSize: 7.4, italic: true, color: GREY, align: "left",
      valign: "middle", margin: 0 });
    y += SH + 0.42;

    // --- rules ---
    y = head(s, y, "RULES");
    const RULES = [
      ["Interval", "The gap between the logo and the name is exactly one clear space. It never closes up and never opens out."],
      ["Alignment", "Horizontal: the name is optically centred on the logo. Stacked: the name aligns to the left edge of the logo's ink."],
      ["The rule", "In the stacked lockup the rule spans the logo width exactly, at one hundredth of that width. Black, or white reversed. Never red."],
      ["Colour", "One colour throughout. The logo's own red is the only red in the lockup; the name is never red, never tinted, never outlined."],
      ["Backgrounds", "White, black, or a solid panel in the palette. Never a photograph, never a pattern, never a mid tone that flattens the logo."],
      ["Not a logo", "This is a pairing of an approved logo with plain text. It is not itself a mark, and it is not registered, drawn as artwork or used as a badge."],
    ];
    RULES.forEach(([k, v]) => {
      s.addText(k, { x: L, y, w: 1.15, h: 0.32, fontFace: F, fontSize: 8.2, bold: true,
        color: INK, align: "left", valign: "top", margin: 0 });
      s.addText(v, { x: L + 1.25, y, w: W - 1.25, h: 0.32, fontFace: F, fontSize: 8.2,
        color: "3E3E3E", align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });
      s.addShape("rect", { x: L, y: y + 0.36, w: W, h: 0.006, fill: { color: RULE } });
      y += 0.46;
    });

    // --- incorrect use ---
    y = head(s, y + 0.04, "INCORRECT USE");
    const BW = (W - 3 * 0.12) / 4, BH = 0.86;
    const BAD = [
      ["Name larger than the logo", 1.05],
      ["Clear space closed up", null],
      ["Name in red", null],
      ["Name set in another face", null],
    ];
    BAD.forEach(([t, k], i) => {
      const x = L + i * (BW + 0.12);
      s.addShape("rect", { x, y, w: BW, h: BH, fill: { color: PAPER } });
      const lw = 0.78, lhh = lw / AR;
      s.addImage({ path: LOGO, x: x + 0.12, y: y + 0.22, w: lw, h: lhh });
      const g = i === 1 ? 0.01 : lw * NCAP;
      s.addText("Combat Mindset", {
        x: x + 0.12 + lw + g, y: y + 0.22, w: BW - 0.9, h: lhh, fontFace: F,
        fontSize: i === 0 ? 8.4 : 5.6, bold: i !== 3,
        italic: i === 3, color: i === 2 ? RED : INK,
        align: "left", valign: "middle", margin: 0 });
      s.addShape("line", { x: x + 0.06, y: y + 0.1, w: BW - 0.12, h: BH - 0.2,
        line: { color: INK, width: 1 } });
      s.addShape("line", { x: x + 0.06, y: y + BH - 0.1, w: BW - 0.12, h: -(BH - 0.2),
        line: { color: INK, width: 1 } });
      s.addText(t, { x, y: y + BH + 0.06, w: BW, h: 0.3, fontFace: F, fontSize: 7.2,
        color: INK, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });
    });
  }

  await pres.writeFile({ fileName: "output/combat-mindset-lockup.pptx" });
  console.log("written output/combat-mindset-lockup.pptx");
})();
