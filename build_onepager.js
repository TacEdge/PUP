// COMBAT MINDSET — THE WAY FORWARD : one-page briefing slide (16:9)
// Synthesises "Combat Mindset — Proposed Way Forward" Draft v0.3 on the
// NZ Army brand system (NZDF Visual Identity Standards palette).

const pptxgen = require("pptxgenjs");

const RED = "C62026";        // Army Red
const BLACK = "000000";      // Darkest Hour
const WHITE = "FFFFFF";      // Ruapehu White
const SWAMP = "002516";      // Swamp Green
const KAWAKAWA = "3A4B00";   // Kawakawa Leaf
const WAIOURU = "A89662";    // Waiouru Hills
const MOAWHANGO = "CDD2B7";  // Moawhango Green

const F = "Arial";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
const slide = pres.addSlide();
slide.background = { color: WHITE };

const L = 0.45;              // left margin
const W = 12.44;             // content width
const MAINW = 7.6;           // main hierarchy column width
const RX = L + MAINW + 0.25; // right column x = 8.30
const RW = L + W - RX;       // right column width = 4.59

// ---------------------------------------------------------------- markings
slide.addShape("rect", { x: 0, y: 0, w: 13.333, h: 0.18, fill: { color: BLACK } });
slide.addText("UNCLASSIFIED", {
  x: 0, y: 0, w: 13.333, h: 0.18, align: "center", valign: "middle",
  fontFace: F, fontSize: 8, bold: true, color: WHITE, charSpacing: 4, margin: 0,
});
slide.addShape("rect", { x: 0, y: 7.32, w: 13.333, h: 0.18, fill: { color: BLACK } });
slide.addText("UNCLASSIFIED", {
  x: 0, y: 7.32, w: 13.333, h: 0.18, align: "center", valign: "middle",
  fontFace: F, fontSize: 8, bold: true, color: WHITE, charSpacing: 4, margin: 0,
});
slide.addText("NZALC / Human Performance Cell   ·   NZALC/HPC 2026   ·   Draft v0.3   ·   July 2026", {
  x: L, y: 7.32, w: 6.4, h: 0.18, align: "left", valign: "middle",
  fontFace: F, fontSize: 6.5, color: MOAWHANGO, margin: 0,
});
slide.addText("Distribution: COMDT ACS", {
  x: 10.3, y: 7.32, w: 2.59, h: 0.18, align: "right", valign: "middle",
  fontFace: F, fontSize: 6.5, color: MOAWHANGO, margin: 0,
});

// ------------------------------------------------------------------ header
slide.addImage({ path: LOGO, x: L, y: 0.33, w: 1.32, h: 0.319 });
slide.addText("COMBAT MINDSET — THE WAY FORWARD", {
  x: 2.02, y: 0.26, w: 7.4, h: 0.4, fontFace: F, fontSize: 22, bold: true,
  color: BLACK, align: "left", valign: "middle", margin: 0,
});
slide.addText(
  "Defining, developing and assuring the human-performance capability Army requires to remain effective in combat.",
  { x: 2.02, y: 0.66, w: 7.6, h: 0.22, fontFace: F, fontSize: 9.5, italic: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
slide.addText("HARDER TO KILL", {
  x: 9.8, y: 0.28, w: 3.09, h: 0.28, fontFace: F, fontSize: 15, bold: true,
  color: RED, charSpacing: 3, align: "right", valign: "middle", margin: 0,
});
slide.addText("Proposed Warfighter Focus line — subject to sponsor endorsement", {
  x: 9.0, y: 0.57, w: 3.89, h: 0.18, fontFace: F, fontSize: 7.5,
  color: BLACK, align: "right", valign: "middle", margin: 0,
});

// -------------------------------------------------- main hierarchy helpers
function band(y, h, fill, label, chip, defText, defSize) {
  slide.addShape("rect", { x: L, y, w: MAINW, h, fill: { color: fill } });
  slide.addText(label, {
    x: L + 0.18, y: y + 0.05, w: MAINW - 4.0, h: 0.24, fontFace: F,
    fontSize: 12.5, bold: true, color: WHITE, align: "left", valign: "middle", margin: 0,
  });
  slide.addText(chip, {
    x: L + MAINW - 3.85, y: y + 0.07, w: 3.7, h: 0.2, fontFace: F, fontSize: 7.5,
    bold: true, color: MOAWHANGO, charSpacing: 1.5, align: "right", valign: "middle", margin: 0,
  });
  slide.addText(defText, {
    x: L + 0.18, y: y + 0.3, w: MAINW - 0.36, h: h - 0.34, fontFace: F,
    fontSize: defSize, color: WHITE, align: "left", valign: "top", margin: 0,
  });
}
function connector(y, text, color) {
  slide.addShape("triangle", {
    x: L + MAINW / 2 - 0.07, y: y + 0.03, w: 0.14, h: 0.1,
    fill: { color }, rotate: 180,
  });
  if (text) {
    slide.addText(text, {
      x: L + MAINW / 2 + 0.14, y, w: 2.9, h: 0.16, fontFace: F, fontSize: 8.5,
      italic: true, color: BLACK, align: "left", valign: "middle", margin: 0,
    });
  }
}

// 1 — warfighting imperative
slide.addShape("rect", { x: L, y: 1.02, w: MAINW, h: 0.62, fill: { color: BLACK } });
slide.addText("WARFIGHTING IMPERATIVE", {
  x: L + 0.18, y: 1.07, w: MAINW - 0.36, h: 0.2, fontFace: F, fontSize: 12.5,
  bold: true, color: WHITE, align: "left", valign: "middle", margin: 0,
});
slide.addText(
  "Army requires individuals, teams and leaders who remain effective and act decisively, persistently, adaptively and ethically under the threat, adversity and uncertainty of combat.",
  { x: L + 0.18, y: 1.28, w: MAINW - 0.36, h: 0.32, fontFace: F, fontSize: 9,
    color: WHITE, align: "left", valign: "top", margin: 0 });
connector(1.66, null, RED);

// 2 — Combat Mindset
band(1.84, 0.78, RED, "COMBAT MINDSET", "COMBAT-SPECIFIC EXPRESSION",
  "The individual and collective readiness and disposition to remain effective and act decisively, persistently, adaptively and ethically under the threat, adversity and uncertainty of combat in order to achieve the mission.",
  9);
connector(2.66, "enabled by", SWAMP);

// 3 — Performance Under Pressure
band(2.86, 1.18, SWAMP, "PERFORMANCE UNDER PRESSURE", "ENABLING HUMAN-PERFORMANCE CAPABILITY",
  "The trainable individual and collective human-performance capability to prepare for, maintain effective performance through, adapt within and recover from pressure.",
  9);
const chipW = 1.18, chipGap = 0.12;
["PREPARE", "PERFORM", "ADAPT", "RECOVER"].forEach((t, i) => {
  const cx = L + 0.18 + i * (chipW + chipGap);
  slide.addShape("rect", { x: cx, y: 3.55, w: chipW, h: 0.21, fill: { color: MOAWHANGO } });
  slide.addText(t, {
    x: cx, y: 3.55, w: chipW, h: 0.21, fontFace: F, fontSize: 8, bold: true,
    color: SWAMP, charSpacing: 1.5, align: "center", valign: "middle", margin: 0,
  });
});
slide.addText(
  "Applicable across combat, command, crisis response, training, garrison leadership and high-risk technical activity.",
  { x: L + 0.18, y: 3.8, w: MAINW - 0.36, h: 0.18, fontFace: F, fontSize: 7.5,
    italic: true, color: MOAWHANGO, align: "left", valign: "middle", margin: 0 });
connector(4.08, "developed and organised through", KAWAKAWA);

// 4 — Framework
band(4.28, 1.07, KAWAKAWA, "ARMY COMBAT MINDSET FRAMEWORK", "ORGANISING MODEL",
  "The organising model through which Army defines, develops, integrates and assures the capabilities, products and governance arrangements that enable Combat Mindset.",
  9);
slide.addText(
  "Organises:  definitions  ·  desired outcomes  ·  capability strands  ·  developmental progression  ·  products and methods  ·  delivery  ·  governance  ·  evidence  ·  assurance",
  { x: L + 0.18, y: 5.06, w: MAINW - 0.36, h: 0.24, fontFace: F, fontSize: 7.5,
    italic: true, color: MOAWHANGO, align: "left", valign: "top", margin: 0 });
connector(5.39, "delivered through", SWAMP);

// ------------------------------------------------------------ right column
// governance panel
slide.addShape("rect", { x: RX, y: 1.02, w: RW, h: 0.24, fill: { color: SWAMP } });
slide.addText("GOVERNANCE AND ASSURANCE — INTERIM MODEL", {
  x: RX + 0.12, y: 1.02, w: RW - 0.24, h: 0.24, fontFace: F, fontSize: 9,
  bold: true, color: WHITE, align: "left", valign: "middle", margin: 0,
});
slide.addShape("rect", {
  x: RX, y: 1.26, w: RW, h: 2.13, fill: { color: WHITE },
  line: { color: WAIOURU, width: 0.75 },
});
const govRows = [
  ["Army Sponsor", "Strategic sponsorship and policy direction"],
  ["COMDT ACS", "Interim capability integrator"],
  ["ACS", "Framework development and delivery coordination"],
  ["Human Performance Cell", "COGCON product steward; performance-cognition adviser"],
  ["Domain advisers", "NZDF Psychology, ILD, doctrine, physical performance"],
  ["Delivery", "Training establishments, units, existing instructors"],
  ["Assurance", "Layered: doctrine, evidence, professional, learning, delivery, operational"],
];
govRows.forEach((r, i) => {
  slide.addText(
    [
      { text: r[0], options: { bold: true, color: SWAMP } },
      { text: "  —  " + r[1], options: { color: BLACK } },
    ],
    { x: RX + 0.12, y: 1.32 + i * 0.295, w: RW - 0.24, h: 0.29, fontFace: F,
      fontSize: 8, align: "left", valign: "middle", margin: 0 });
});

// programme of work
slide.addShape("rect", { x: RX, y: 3.56, w: RW, h: 0.24, fill: { color: SWAMP } });
slide.addText("PROGRAMME OF WORK — 2026", {
  x: RX + 0.12, y: 3.56, w: RW - 0.24, h: 0.24, fontFace: F, fontSize: 9,
  bold: true, color: WHITE, align: "left", valign: "middle", margin: 0,
});
slide.addShape("rect", {
  x: RX, y: 3.8, w: RW, h: 0.72, fill: { color: WHITE },
  line: { color: WAIOURU, width: 0.75 },
});
const steps = ["DEFINE", "MAP", "DEVELOP", "VALIDATE", "TRIAL", "REPORT"];
const stepW = (RW - 0.24 - 0.05 * 5) / 6;
steps.forEach((t, i) => {
  const sx = RX + 0.12 + i * (stepW + 0.05);
  if (i === 4) {
    slide.addShape("chevron", { x: sx, y: 3.9, w: stepW, h: 0.24,
      fill: { color: WHITE }, line: { color: KAWAKAWA, width: 1 } });
  } else {
    slide.addShape("chevron", { x: sx, y: 3.9, w: stepW, h: 0.24, fill: { color: KAWAKAWA } });
  }
  slide.addText(t, {
    x: sx, y: 3.9, w: stepW, h: 0.24, fontFace: F, fontSize: 6.8, bold: true,
    color: i === 4 ? KAWAKAWA : WHITE, align: "center", valign: "middle", margin: 0,
  });
});
slide.addText(
  "Phase 4 is a limited COGCON MVP integration trial, subject to capacity. Report back November 2026: Framework v1.0, capability and product map, implementation plan.",
  { x: RX + 0.12, y: 4.17, w: RW - 0.24, h: 0.32, fontFace: F, fontSize: 7.3,
    italic: true, color: BLACK, align: "left", valign: "top", margin: 0 });

// outcome
slide.addShape("rect", { x: RX, y: 4.63, w: RW, h: 0.92, fill: { color: SWAMP } });
slide.addText("THE OUTCOME", {
  x: RX + 0.12, y: 4.68, w: RW - 0.24, h: 0.18, fontFace: F, fontSize: 9,
  bold: true, color: MOAWHANGO, charSpacing: 2, align: "left", valign: "middle", margin: 0,
});
slide.addText(
  "A coherent, joined-up and assured Army approach that deliberately develops individuals, teams and leaders who remain effective under pressure and are prepared to act decisively, persistently, adaptively and ethically in combat.",
  { x: RX + 0.12, y: 4.87, w: RW - 0.24, h: 0.64, fontFace: F, fontSize: 8.2,
    color: WHITE, align: "left", valign: "top", margin: 0 });

// ------------------------------------------------- strands + products rows
const cells = 7;
const cw = (W - 0.06 * (cells - 1)) / cells;

slide.addShape("rect", { x: L, y: 5.62, w: W, h: 0.2, fill: { color: SWAMP } });
slide.addText("CAPABILITY STRANDS — WHAT WE BUILD", {
  x: L + 0.12, y: 5.62, w: W - 0.24, h: 0.2, fontFace: F, fontSize: 8.5,
  bold: true, color: WHITE, align: "left", valign: "middle", margin: 0,
});
const strands = [
  "Leadership", "Mental skills", "Performance cognition", "Resilience & recovery",
  "Physical performance", "Professional identity & values", "Individual & collective exposure to pressure",
];
strands.forEach((t, i) => {
  const cx = L + i * (cw + 0.06);
  slide.addShape("rect", {
    x: cx, y: 5.86, w: cw, h: 0.44, fill: { color: MOAWHANGO },
  });
  slide.addText(t, {
    x: cx + 0.03, y: 5.86, w: cw - 0.06, h: 0.44, fontFace: F, fontSize: 7.6,
    bold: true, color: SWAMP, align: "center", valign: "middle", margin: 0,
  });
});

slide.addShape("rect", { x: L, y: 6.4, w: W, h: 0.2, fill: { color: SWAMP } });
slide.addText("TRAINING PRODUCTS AND METHODS — HOW WE BUILD IT", {
  x: L + 0.12, y: 6.4, w: 6.0, h: 0.2, fontFace: F, fontSize: 8.5,
  bold: true, color: WHITE, align: "left", valign: "middle", margin: 0,
});
slide.addText("each product contributes across multiple strands — columns do not pair one-to-one", {
  x: L + 6.1, y: 6.4, w: W - 6.22, h: 0.2, fontFace: F, fontSize: 7.2,
  italic: true, color: MOAWHANGO, align: "right", valign: "middle", margin: 0,
});
const products = [
  ["NZALC Performance Under Pressure package", null],
  ["NZDF Psychology products", null],
  ["COGCON MVP", "Developmental product — performance-cognition strand"],
  ["Scenario & experiential training", null],
  ["Physical conditioning", null],
  ["Structured reflection & recovery", null],
  ["Other products identified in Phase 1 mapping", null],
];
products.forEach((p, i) => {
  const cx = L + i * (cw + 0.06);
  slide.addShape("rect", {
    x: cx, y: 6.64, w: cw, h: 0.46, fill: { color: WHITE },
    line: { color: WAIOURU, width: 0.75 },
  });
  if (p[1]) {
    slide.addText(
      [
        { text: p[0], options: { bold: true, fontSize: 7.4, color: BLACK, breakLine: true } },
        { text: p[1], options: { fontSize: 6, italic: true, color: BLACK } },
      ],
      { x: cx + 0.04, y: 6.64, w: cw - 0.08, h: 0.46, fontFace: F,
        align: "center", valign: "middle", margin: 0 });
  } else {
    slide.addText(p[0], {
      x: cx + 0.04, y: 6.64, w: cw - 0.08, h: 0.46, fontFace: F, fontSize: 7.4,
      bold: true, color: BLACK, align: "center", valign: "middle", margin: 0,
    });
  }
});
// dashed link: COGCON MVP (cell 3) contributes to Performance cognition strand
slide.addShape("line", {
  x: L + 2 * (cw + 0.06) + cw / 2, y: 6.31, w: 0, h: 0.32,
  line: { color: RED, width: 1.25, dashType: "dash", beginArrowType: "triangle" },
});

// caption row
slide.addText(
  "COGCON MVP is nested within the performance-cognition strand (dashed link). It develops selected elements of Performance Under Pressure — not a complete Combat Mindset programme or a validated operational-readiness measure.",
  { x: L, y: 7.13, w: 7.7, h: 0.15, fontFace: F, fontSize: 6.8, italic: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
slide.addText(
  "Prepare → Perform → Recover   ·   Lead Self → Lead Teams → Lead Leaders → Lead Systems",
  { x: 8.2, y: 7.13, w: 4.69, h: 0.15, fontFace: F, fontSize: 6.8, bold: true,
    color: SWAMP, align: "right", valign: "middle", margin: 0 });

pres.writeFile({ fileName: "output/combat-mindset-onepager.pptx" }).then(() => {
  console.log("written output/combat-mindset-onepager.pptx");
});
