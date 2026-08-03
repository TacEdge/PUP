// COMBAT MINDSET — THE WAY FORWARD : portrait A4 one-pager, design iteration 3
// Top-down hierarchy: Combat Mindset (warfighting imperative) → Performance
// Under Pressure (enabling capability) → Army Combat Mindset Framework, with
// three balanced columns: governance & assurance, current delivery system,
// framework development programme.

const pptxgen = require("pptxgenjs");
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const sharp = require("sharp");
const lu = require("react-icons/lu");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const F = "Arial";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function icon(name, hex, strokeWidth = 1.6) {
  const el = React.createElement(lu[name], {
    color: "#" + hex, size: 256, strokeWidth,
  });
  let svg = renderToStaticMarkup(el);
  if (!svg.includes("xmlns")) svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ');
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

(async () => {
  const I = {};
  const need = {
    crosshairHero: ["LuCrosshair", MOAWHANGO],
    brainW: ["LuBrain", WHITE], puzzleW: ["LuPuzzle", WHITE],
    shieldW: ["LuShieldCheck", WHITE], usersW: ["LuUsers", WHITE],
    gearW: ["LuSettings", WHITE],
    chevronsG: ["LuChevronsUp", SWAMP], brainG: ["LuBrain", SWAMP],
    landmarkG: ["LuLandmark", SWAMP], usersG: ["LuUsers", SWAMP],
  };
  for (const [k, [n, c]] of Object.entries(need)) I[k] = await icon(n, c);

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W; // 7.77
  const MID = L + W / 2;

  // ---- footer credits (plain text, no banners) ---------------------------
  s.addText("Army Command School  ·  ACS 2026", {
    x: L, y: 11.45, w: 2.6, h: 0.18, align: "left", valign: "middle",
    fontFace: F, fontSize: 6, color: BLACK, margin: 0 });
  s.addText("Draft v0.8  ·  July 2026", { x: 5.7, y: 11.45, w: 2.07, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6, color: BLACK, margin: 0 });

  // ---- header ------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.5, w: 1.1, h: 0.266 });
  s.addText("COMBAT MINDSET THE WAY FORWARD", {
    x: 1.85, y: 0.47, w: 5.92, h: 0.32, fontFace: F, fontSize: 15.5, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });

  // ---- shared helpers ----------------------------------------------------
  function pill(y, w, text, fill) {
    const x = MID - w / 2;
    s.addShape("roundRect", { x, y, w, h: 0.24, fill: { color: fill },
      rectRadius: 0.12, line: { color: WHITE, width: 1 } });
    s.addText(text, { x, y, w, h: 0.24, fontFace: F, fontSize: 7.8, bold: true,
      color: WHITE, charSpacing: 1.2, align: "center", valign: "middle", margin: 0 });
  }
  function midConnector(y, label) {
    s.addShape("triangle", { x: MID - 0.07, y, w: 0.14, h: 0.11,
      fill: { color: SWAMP }, rotate: 180 });
    s.addText(label, { x: MID - 1.9, y: y + 0.13, w: 3.8, h: 0.16, fontFace: F,
      fontSize: 8.5, italic: true, color: BLACK, align: "center",
      valign: "middle", margin: 0 });
  }

  // ---- section 1: warfighting imperative — COMBAT MINDSET ----------------
  s.addShape("rect", { x: L, y: 1.12, w: W, h: 1.3, fill: { color: BLACK } });
  pill(1.0, 2.4, "1)  WARFIGHTING IMPERATIVE", RED);
  s.addImage({ data: I.crosshairHero, x: L + 0.28, y: 1.46, w: 0.66, h: 0.66, transparency: 40 });
  s.addText("COMBAT MINDSET", {
    x: L, y: 1.44, w: W, h: 0.55, fontFace: F, fontSize: 33, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Remain effective. Act decisively. Harder to kill.", {
    x: L, y: 2.02, w: W, h: 0.26, fontFace: F, fontSize: 13, bold: true,
    color: RED, align: "center", valign: "middle", margin: 0 });

  midConnector(2.5, "enabled by");

  // ---- section 2: enabling capability — PUP -------------------------------
  s.addShape("rect", { x: L, y: 3.1, w: W, h: 1.06, fill: { color: SWAMP } });
  pill(2.98, 4.0, "2)  ENABLING HUMAN-PERFORMANCE CAPABILITY", SWAMP);
  s.addImage({ data: I.brainW, x: L + 0.24, y: 3.42, w: 0.5, h: 0.5 });
  s.addText("PERFORMANCE UNDER PRESSURE", {
    x: L, y: 3.32, w: W, h: 0.42, fontFace: F, fontSize: 23,
    bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Prepare   •   Perform   •   Recover",
    { x: L, y: 3.79, w: W, h: 0.2, fontFace: F, fontSize: 10.5,
      bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });

  midConnector(4.24, "developed, organised and assured through");

  // ---- section 3: organising system — the framework ----------------------
  s.addShape("rect", { x: L, y: 4.84, w: W, h: 0.92, fill: { color: KAWAKAWA } });
  pill(4.72, 2.1, "3)  ORGANISING SYSTEM", KAWAKAWA);
  s.addImage({ data: I.puzzleW, x: L + 0.24, y: 5.06, w: 0.46, h: 0.46 });
  s.addText("THE ARMY COMBAT MINDSET FRAMEWORK", {
    x: L, y: 4.98, w: W, h: 0.36, fontFace: F, fontSize: 19,
    bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("The Army system through which Combat Mindset is governed, developed, delivered and assured.", {
    x: L, y: 5.37, w: W, h: 0.2, fontFace: F, fontSize: 9,
    color: WHITE, align: "center", valign: "middle", margin: 0 });

  // ---- three framework columns -------------------------------------------
  const GAP = 0.12, colW = (W - 2 * GAP) / 3;
  const CX = [L, L + colW + GAP, L + 2 * (colW + GAP)];
  const HY = 5.92, CARD_Y = HY + 0.36, CARD_H = 4.82;

  const heads = [
    ["shieldW", "1. GOVERNANCE & ASSURANCE"],
    ["usersW", "2. CURRENT DELIVERY SYSTEM"],
    ["gearW", "3. FRAMEWORK DEVELOPMENT PROGRAMME"],
  ];
  heads.forEach(([ic, title], i) => {
    s.addShape("rect", { x: CX[i], y: HY, w: colW, h: 0.36, fill: { color: SWAMP } });
    s.addImage({ data: I[ic], x: CX[i] + 0.08, y: HY + 0.08, w: 0.2, h: 0.2 });
    s.addText(title, { x: CX[i] + 0.34, y: HY, w: colW - 0.4, h: 0.36,
      fontFace: F, fontSize: 7.6, bold: true, color: WHITE, align: "left",
      valign: "middle", margin: 0 });
    s.addShape("rect", { x: CX[i], y: CARD_Y, w: colW, h: CARD_H,
      fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
  });

  // Column 1 — governance & assurance
  const gov = [
    "Strategic sponsorship and policy direction",
    "Capability integration",
    "Technical and professional authorities",
    "Product recognition and evidence requirements",
    "Delivery standards",
    "Evaluation and assurance",
  ];
  s.addText(gov.map((t, i) => ({
    text: t, options: { bullet: { characterCode: "2022", indent: 10 },
      breakLine: i < gov.length - 1 },
  })), { x: CX[0] + 0.14, y: CARD_Y + 0.18, w: colW - 0.26, h: CARD_H - 0.36,
    fontFace: F, fontSize: 8.2, color: BLACK, align: "left", valign: "top",
    margin: 0, paraSpaceAfter: 12 });

  // Column 2 — current delivery system
  function deliveryGroup(iconKey, title, items, y, itemSize) {
    s.addImage({ data: I[iconKey], x: CX[1] + 0.12, y: y + 0.01, w: 0.24, h: 0.24 });
    s.addText(title, { x: CX[1] + 0.44, y, w: colW - 0.56, h: 0.26, fontFace: F,
      fontSize: 8.3, bold: true, color: SWAMP, align: "left", valign: "middle",
      margin: 0 });
    s.addText(items.map((t, i) => ({
      text: t, options: { bullet: { characterCode: "2022", indent: 8 },
        breakLine: i < items.length - 1 },
    })), { x: CX[1] + 0.44, y: y + 0.27, w: colW - 0.56, h: 1.3, fontFace: F,
      fontSize: itemSize, color: BLACK, align: "left", valign: "top", margin: 0,
      paraSpaceAfter: 3 });
  }
  deliveryGroup("chevronsG", "NZALC", [
    "ELDA Lead Leaders",
    "ELDA Lead Systems",
    "ELDA Resilience",
    "Performance Under Pressure (Lead Self)",
    "Performance Under Pressure (Lead Teams)",
  ], CARD_Y + 0.14, 7.3);
  s.addShape("line", { x: CX[1] + 0.12, y: CARD_Y + 1.72, w: colW - 0.24, h: 0,
    line: { color: WAIOURU, width: 0.5 } });
  deliveryGroup("brainG", "HUMAN PERFORMANCE CELL", [
    "COGCON",
    "Performance conditioning",
  ], CARD_Y + 1.84, 7.3);
  s.addShape("line", { x: CX[1] + 0.12, y: CARD_Y + 2.62, w: colW - 0.24, h: 0,
    line: { color: WAIOURU, width: 0.5 } });
  s.addImage({ data: I.landmarkG, x: CX[1] + 0.12, y: CARD_Y + 2.75, w: 0.24, h: 0.24 });
  s.addText("UNITS AND TRAINING ESTABLISHMENTS", {
    x: CX[1] + 0.44, y: CARD_Y + 2.72, w: colW - 0.56, h: 0.34, fontFace: F,
    fontSize: 8.3, bold: true, color: SWAMP, align: "left", valign: "middle",
    margin: 0 });
  s.addText([
    "Training", "Exercises", "Mission rehearsal", "Field activity",
  ].map((t, i, a) => ({
    text: t, options: { bullet: { characterCode: "2022", indent: 8 },
      breakLine: i < a.length - 1 },
  })), { x: CX[1] + 0.44, y: CARD_Y + 3.08, w: colW - 0.56, h: 0.75, fontFace: F,
    fontSize: 7.3, color: BLACK, align: "left", valign: "top", margin: 0,
    paraSpaceAfter: 3 });
  s.addShape("rect", { x: CX[1] + 0.12, y: CARD_Y + 3.98, w: colW - 0.24, h: 0.72,
    fill: { color: WHITE }, line: { color: SWAMP, width: 1, dashType: "dash" } });
  s.addImage({ data: I.usersG, x: CX[1] + 0.2, y: CARD_Y + 4.22, w: 0.24, h: 0.24 });
  s.addText("Units contextualise and express Combat Mindset under realistic warfighting conditions.", {
    x: CX[1] + 0.5, y: CARD_Y + 4.02, w: colW - 0.72, h: 0.64, fontFace: F,
    fontSize: 7.2, italic: true, color: BLACK, align: "left", valign: "middle",
    margin: 0 });

  // Column 3 — framework development programme
  const phases = [
    ["0", "Phase 0: Define and govern",
      "Confirm terminology, sponsorship, ownership and interim governance."],
    ["1", "Phase 1: Understand",
      "Stocktake existing doctrine, products, delivery, evidence, ownership and assurance."],
    ["2", "Phase 2: Design",
      "Develop the framework, delivery architecture, outcomes and product-recognition criteria."],
    ["3", "Phase 3: Validate",
      "Refine the framework with stakeholders, training establishments and units."],
    ["4", "Phase 4: Endorse and implement",
      "Deliver Framework v1.0 and a prioritised implementation plan."],
  ];
  const P0 = CARD_Y + 0.18, PITCH = 0.92;
  s.addShape("line", { x: CX[2] + 0.29, y: P0 + 0.15,
    w: 0, h: PITCH * 4, line: { color: SWAMP, width: 1.25 } });
  phases.forEach(([n, title, desc], i) => {
    const py = P0 + i * PITCH;
    s.addShape("ellipse", { x: CX[2] + 0.14, y: py, w: 0.3, h: 0.3,
      fill: { color: SWAMP }, line: { color: WHITE, width: 1 } });
    s.addText(n, { x: CX[2] + 0.14, y: py, w: 0.3, h: 0.3, fontFace: F,
      fontSize: 10, bold: true, color: WHITE, align: "center",
      valign: "middle", margin: 0 });
    s.addText(title, { x: CX[2] + 0.54, y: py - 0.02, w: colW - 0.66, h: 0.34,
      fontFace: F, fontSize: 8.2, bold: true, color: SWAMP, align: "left",
      valign: "top", margin: 0 });
    s.addText(desc, { x: CX[2] + 0.54, y: py + 0.3, w: colW - 0.66, h: 0.56,
      fontFace: F, fontSize: 7.2, color: BLACK, align: "left", valign: "top",
      margin: 0 });
  });

  await pres.writeFile({ fileName: "output/combat-mindset-onepager-portrait.pptx" });
  console.log("written output/combat-mindset-onepager-portrait.pptx");
})();
