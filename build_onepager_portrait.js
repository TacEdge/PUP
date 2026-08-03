// COMBAT MINDSET THE WAY FORWARD : portrait A4, design iteration 4
// Page 1: the core idea. Combat Mindset (warfighting imperative), Performance
// Under Pressure (Prepare, Perform, Recover), the Army Combat Mindset
// Framework (organising system) and a full-width five-phase Framework
// Development Programme.
// Page 2: Current System, Governance and Delivery (supporting detail).

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
  const cmp = lu[name] || lu.LuCircle;
  const el = React.createElement(cmp, { color: "#" + hex, size: 256, strokeWidth });
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
    chevronsG: ["LuChevronsUp", SWAMP], brainG: ["LuBrain", SWAMP],
    landmarkG: ["LuLandmark", SWAMP], usersG: ["LuUsers", SWAMP],
  };
  for (const [k, [n, c]] of Object.entries(need)) I[k] = await icon(n, c);

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";

  const L = 0.5, W = 7.27, R = L + W, MID = L + W / 2;

  function pageChrome(s, title) {
    s.background = { color: WHITE };
    s.addImage({ path: LOGO, x: L, y: 0.5, w: 1.1, h: 0.266 });
    s.addText(title, {
      x: 1.85, y: 0.47, w: 5.92, h: 0.32, fontFace: F, fontSize: 15.5, bold: true,
      color: BLACK, align: "left", valign: "middle", margin: 0 });
    s.addText("Army Command School  ·  ACS 2026", {
      x: L, y: 11.45, w: 2.6, h: 0.18, align: "left", valign: "middle",
      fontFace: F, fontSize: 6, color: BLACK, margin: 0 });
    s.addText("Draft v0.8  ·  July 2026", { x: 5.7, y: 11.45, w: 2.07, h: 0.18,
      align: "right", valign: "middle", fontFace: F, fontSize: 6, color: BLACK, margin: 0 });
  }

  function pill(s, y, w, text, fill) {
    const x = MID - w / 2;
    s.addShape("roundRect", { x, y, w, h: 0.24, fill: { color: fill },
      rectRadius: 0.12, line: { color: WHITE, width: 1 } });
    s.addText(text, { x, y, w, h: 0.24, fontFace: F, fontSize: 7.8, bold: true,
      color: WHITE, charSpacing: 1.2, align: "center", valign: "middle", margin: 0 });
  }

  function midConnector(s, y, label) {
    s.addShape("triangle", { x: MID - 0.07, y, w: 0.14, h: 0.11,
      fill: { color: SWAMP }, rotate: 180 });
    s.addText(label, { x: MID - 1.9, y: y + 0.13, w: 3.8, h: 0.16, fontFace: F,
      fontSize: 8.5, italic: true, color: BLACK, align: "center",
      valign: "middle", margin: 0 });
  }

  // ======================================================== page 1: the idea
  const s1 = pres.addSlide();
  pageChrome(s1, "COMBAT MINDSET THE WAY FORWARD");

  // section 1: Combat Mindset
  s1.addShape("rect", { x: L, y: 1.14, w: W, h: 1.56, fill: { color: BLACK } });
  pill(s1, 1.02, 2.4, "1)  WARFIGHTING IMPERATIVE", RED);
  s1.addImage({ data: I.crosshairHero, x: L + 0.3, y: 1.52, w: 0.8, h: 0.8, transparency: 40 });
  s1.addText("COMBAT MINDSET", {
    x: L, y: 1.52, w: W, h: 0.62, fontFace: F, fontSize: 37, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s1.addText("Remain effective. Act decisively. Harder to kill.", {
    x: L, y: 2.2, w: W, h: 0.3, fontFace: F, fontSize: 14, bold: true,
    color: RED, align: "center", valign: "middle", margin: 0 });

  midConnector(s1, 2.84, "enabled by");

  // section 2: Performance Under Pressure
  s1.addShape("rect", { x: L, y: 3.42, w: W, h: 1.24, fill: { color: SWAMP } });
  pill(s1, 3.3, 4.0, "2)  ENABLING HUMAN-PERFORMANCE CAPABILITY", SWAMP);
  s1.addImage({ data: I.brainW, x: L + 0.22, y: 3.8, w: 0.48, h: 0.48 });
  s1.addText("PERFORMANCE UNDER PRESSURE", {
    x: L, y: 3.7, w: W, h: 0.46, fontFace: F, fontSize: 22.5, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s1.addText("Prepare   •   Perform   •   Recover", {
    x: L, y: 4.2, w: W, h: 0.26, fontFace: F, fontSize: 12, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });

  midConnector(s1, 4.8, "developed, organised and assured through");

  // section 3: the framework
  s1.addShape("rect", { x: L, y: 5.38, w: W, h: 1.14, fill: { color: KAWAKAWA } });
  pill(s1, 5.26, 2.1, "3)  ORGANISING SYSTEM", KAWAKAWA);
  s1.addImage({ data: I.puzzleW, x: L + 0.22, y: 5.72, w: 0.44, h: 0.44 });
  s1.addText("THE ARMY COMBAT MINDSET FRAMEWORK", {
    x: L, y: 5.6, w: W, h: 0.4, fontFace: F, fontSize: 17.5, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s1.addText("The Army system through which Combat Mindset is governed, developed, delivered and assured.", {
    x: L, y: 6.04, w: W, h: 0.24, fontFace: F, fontSize: 9.5,
    color: WHITE, align: "center", valign: "middle", margin: 0 });

  midConnector(s1, 6.66, "achieved through");

  // section 4: framework development programme (full width)
  s1.addShape("rect", { x: L, y: 7.36, w: W, h: 2.85,
    fill: { color: MOAWHANGO, transparency: 72 } });
  pill(s1, 7.24, 3.7, "4)  FRAMEWORK DEVELOPMENT PROGRAMME", SWAMP);

  const phases = [
    ["0", "Define and govern",
      "Confirm terminology, sponsorship, ownership and interim governance."],
    ["1", "Understand",
      "Stocktake existing doctrine, products, delivery, evidence, ownership and assurance."],
    ["2", "Design",
      "Develop the framework, delivery architecture, outcomes and product-recognition criteria."],
    ["3", "Validate",
      "Refine the framework with stakeholders, training establishments and units."],
    ["4", "Endorse and implement",
      "Deliver Framework v1.0 and a prioritised implementation plan."],
  ];
  const pw = W / 5, CY = 8.16, CD = 0.52;
  s1.addShape("line", { x: L + pw / 2, y: CY + CD / 2, w: W - pw, h: 0,
    line: { color: SWAMP, width: 1.5 } });
  phases.forEach(([n, title, desc], i) => {
    const cx = L + i * pw + pw / 2;
    if (i < 4) s1.addText("►", { x: L + (i + 1) * pw - 0.24, y: CY + 0.1,
      w: 0.48, h: 0.32, fontFace: F, fontSize: 11, bold: true, color: RED,
      align: "center", valign: "middle", margin: 0 });
    s1.addShape("ellipse", { x: cx - CD / 2, y: CY, w: CD, h: CD,
      fill: { color: SWAMP }, line: { color: WHITE, width: 1.5 } });
    s1.addText(n, { x: cx - CD / 2, y: CY, w: CD, h: CD, fontFace: F,
      fontSize: 15, bold: true, color: WHITE, align: "center",
      valign: "middle", margin: 0 });
    s1.addText(title, { x: L + i * pw + 0.06, y: CY + 0.66, w: pw - 0.12, h: 0.42,
      fontFace: F, fontSize: 9.5, bold: true, color: SWAMP, align: "center",
      valign: "top", margin: 0 });
    s1.addText(desc, { x: L + i * pw + 0.1, y: CY + 1.12, w: pw - 0.2, h: 1.4,
      fontFace: F, fontSize: 7.6, color: BLACK, align: "center", valign: "top",
      margin: 0 });
  });

  // ================================== page 2: current system and governance
  const s2 = pres.addSlide();
  pageChrome(s2, "CURRENT SYSTEM, GOVERNANCE AND DELIVERY");

  const GAP = 0.2, colW = (W - GAP) / 2;
  const HY = 1.14, CARD_Y = HY + 0.4, CARD_H = 7.3;

  function colHeader(s, x, ic, title) {
    s.addShape("rect", { x, y: HY, w: colW, h: 0.4, fill: { color: SWAMP } });
    s.addImage({ data: I[ic], x: x + 0.12, y: HY + 0.09, w: 0.22, h: 0.22 });
    s.addText(title, { x: x + 0.42, y: HY, w: colW - 0.5, h: 0.4,
      fontFace: F, fontSize: 9.5, bold: true, color: WHITE, charSpacing: 1,
      align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x, y: CARD_Y, w: colW, h: CARD_H,
      fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
  }

  // governance & assurance
  colHeader(s2, L, "shieldW", "GOVERNANCE & ASSURANCE");
  const gov = [
    "Strategic sponsorship and policy direction",
    "Capability integration",
    "Technical and professional authorities",
    "Product recognition and evidence requirements",
    "Delivery standards",
    "Evaluation and assurance",
  ];
  s2.addText(gov.map((t, i) => ({
    text: t, options: { bullet: { characterCode: "2022", indent: 12 },
      breakLine: i < gov.length - 1 },
  })), { x: L + 0.2, y: CARD_Y + 0.3, w: colW - 0.4, h: CARD_H - 0.6,
    fontFace: F, fontSize: 9.5, color: BLACK, align: "left", valign: "top",
    margin: 0, paraSpaceAfter: 24 });

  // current delivery system
  const RX = L + colW + GAP;
  colHeader(s2, RX, "usersW", "CURRENT DELIVERY SYSTEM");
  function deliveryGroup(iconKey, title, items, y) {
    s2.addImage({ data: I[iconKey], x: RX + 0.16, y: y + 0.01, w: 0.28, h: 0.28 });
    s2.addText(title, { x: RX + 0.54, y: y, w: colW - 0.7, h: 0.3, fontFace: F,
      fontSize: 9.5, bold: true, color: SWAMP, align: "left", valign: "middle",
      margin: 0 });
    s2.addText(items.map((t, i) => ({
      text: t, options: { bullet: { characterCode: "2022", indent: 10 },
        breakLine: i < items.length - 1 },
    })), { x: RX + 0.54, y: y + 0.34, w: colW - 0.7, h: 1.6, fontFace: F,
      fontSize: 8.5, color: BLACK, align: "left", valign: "top", margin: 0,
      paraSpaceAfter: 5 });
  }
  deliveryGroup("chevronsG", "NZALC", [
    "ELDA Lead Leaders",
    "ELDA Lead Systems",
    "ELDA Resilience",
    "Performance Under Pressure (Lead Self)",
    "Performance Under Pressure (Lead Teams)",
  ], CARD_Y + 0.3);
  s2.addShape("line", { x: RX + 0.16, y: CARD_Y + 2.5, w: colW - 0.32, h: 0,
    line: { color: WAIOURU, width: 0.5 } });
  deliveryGroup("brainG", "HUMAN PERFORMANCE CELL", [
    "COGCON",
    "Performance conditioning",
  ], CARD_Y + 2.7);
  s2.addShape("line", { x: RX + 0.16, y: CARD_Y + 3.9, w: colW - 0.32, h: 0,
    line: { color: WAIOURU, width: 0.5 } });
  deliveryGroup("landmarkG", "UNITS AND TRAINING ESTABLISHMENTS", [
    "Training",
    "Exercises",
    "Mission rehearsal",
    "Field activity",
  ], CARD_Y + 4.1);
  s2.addShape("rect", { x: RX + 0.16, y: CARD_Y + 5.9, w: colW - 0.32, h: 0.9,
    fill: { color: WHITE }, line: { color: SWAMP, width: 1, dashType: "dash" } });
  s2.addImage({ data: I.usersG, x: RX + 0.28, y: CARD_Y + 6.2, w: 0.3, h: 0.3 });
  s2.addText("Units contextualise and express Combat Mindset under realistic warfighting conditions.", {
    x: RX + 0.68, y: CARD_Y + 5.96, w: colW - 0.94, h: 0.78, fontFace: F,
    fontSize: 8.5, italic: true, color: BLACK, align: "left", valign: "middle",
    margin: 0 });

  await pres.writeFile({ fileName: "output/combat-mindset-onepager-portrait.pptx" });
  console.log("written output/combat-mindset-onepager-portrait.pptx");
})();
