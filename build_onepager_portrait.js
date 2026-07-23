// COMBAT MINDSET — THE WAY FORWARD : portrait A4 one-pager, design iteration 2
// Hero treatment of the warfighting imperative, soft-tint panels, line icons.

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
    swords: ["LuSwords", WHITE], brain: ["LuBrain", WHITE], puzzle: ["LuPuzzle", WHITE],
    users: ["LuUsers", SWAMP], mskills: ["LuBrain", SWAMP], target: ["LuCrosshair", WHITE],
    heart: ["LuHeartPulse", SWAMP], dumbbell: ["LuDumbbell", SWAMP], medal: ["LuMedal", SWAMP],
    compass: ["LuCompass", SWAMP], landmark: ["LuLandmark", SWAMP], clipboard: ["LuClipboardList", SWAMP],
    star: ["LuStar", RED], crosshairHero: ["LuCrosshair", MOAWHANGO],
  };
  for (const [k, [n, c]] of Object.entries(need)) I[k] = await icon(n, c);

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W; // 7.77

  // ---- markings ----------------------------------------------------------
  s.addShape("rect", { x: 0, y: 0, w: 8.27, h: 0.18, fill: { color: BLACK } });
  s.addText("UNCLASSIFIED", { x: 0, y: 0, w: 8.27, h: 0.18, align: "center",
    valign: "middle", fontFace: F, fontSize: 7.5, bold: true, color: WHITE,
    charSpacing: 4, margin: 0 });
  s.addShape("rect", { x: 0, y: 11.51, w: 8.27, h: 0.18, fill: { color: BLACK } });
  s.addText("UNCLASSIFIED", { x: 0, y: 11.51, w: 8.27, h: 0.18, align: "center",
    valign: "middle", fontFace: F, fontSize: 7.5, bold: true, color: WHITE,
    charSpacing: 4, margin: 0 });
  s.addText("Army Command School  ·  ACS 2026", {
    x: L, y: 11.51, w: 2.6, h: 0.18, align: "left", valign: "middle",
    fontFace: F, fontSize: 6, color: MOAWHANGO, margin: 0 });
  s.addText("Draft v0.7  ·  July 2026", { x: 5.7, y: 11.51, w: 2.07, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6, color: MOAWHANGO, margin: 0 });

  // ---- header ------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.34, w: 1.1, h: 0.266 });
  s.addText("COMBAT MINDSET — THE WAY FORWARD", {
    x: 1.85, y: 0.3, w: 5.92, h: 0.28, fontFace: F, fontSize: 15.5, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Defining, developing and assuring the human-performance capability Army requires to remain effective in combat.", {
    x: 1.85, y: 0.58, w: 5.92, h: 0.18, fontFace: F, fontSize: 8, italic: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });

  // ---- hero --------------------------------------------------------------
  s.addShape("rect", { x: L, y: 0.95, w: W, h: 1.35, fill: { color: BLACK } });
  s.addImage({ data: I.crosshairHero, x: 6.62, y: 1.18, w: 0.88, h: 0.88, transparency: 45 });
  s.addText("WARFIGHTING IMPERATIVE", { x: 0.78, y: 1.08, w: 4.5, h: 0.18,
    fontFace: F, fontSize: 8.5, bold: true, color: MOAWHANGO, charSpacing: 3, margin: 0 });
  s.addText([
    { text: "REMAIN EFFECTIVE. ", options: { color: WHITE } },
    { text: "ACT DECISIVELY.", options: { color: RED } },
  ], { x: 0.78, y: 1.27, w: 5.6, h: 0.42, fontFace: F, fontSize: 21, bold: true,
    align: "left", valign: "middle", margin: 0 });
  s.addText(
    "Army requires individuals, teams and leaders who remain effective and act decisively, persistently, adaptively and ethically under the threat, adversity and uncertainty of combat.",
    { x: 0.78, y: 1.74, w: 5.7, h: 0.44, fontFace: F, fontSize: 8.5,
      color: WHITE, align: "left", valign: "top", margin: 0 });

  // ---- relationship rows -------------------------------------------------
  const LB = 2.05, PX = 2.72, PW = R - PX; // left block width, panel x/w
  function leftBlock(y, h, fill, iconKey, label, descriptor) {
    s.addShape("rect", { x: L, y, w: LB, h, fill: { color: fill } });
    s.addImage({ data: I[iconKey], x: L + 0.16, y: y + 0.14, w: 0.34, h: 0.34 });
    s.addText(label, { x: L + 0.6, y: y + 0.1, w: LB - 0.72, h: 0.46, fontFace: F,
      fontSize: 10.5, bold: true, color: WHITE, align: "left", valign: "middle", margin: 0 });
    s.addText(descriptor, { x: L + 0.16, y: y + h - 0.3, w: LB - 0.32, h: 0.24,
      fontFace: F, fontSize: 7.5, italic: true, color: MOAWHANGO,
      align: "left", valign: "middle", margin: 0 });
  }
  function panel(y, h) {
    s.addShape("rect", { x: PX, y, w: PW, h, fill: { color: MOAWHANGO, transparency: 72 } });
  }
  function flowArrow(y, color, label) {
    s.addShape("triangle", { x: L + LB / 2 - 0.08, y, w: 0.16, h: 0.12,
      fill: { color }, rotate: 180 });
    s.addText(label, { x: L + LB / 2 + 0.16, y: y - 0.02, w: 3.2, h: 0.16,
      fontFace: F, fontSize: 7.5, italic: true, color: BLACK,
      align: "left", valign: "middle", margin: 0 });
  }

  // Combat Mindset
  leftBlock(2.48, 0.88, RED, "swords", "COMBAT MINDSET", "Combat-specific expression");
  panel(2.48, 0.88);
  s.addText(
    "Combat Mindset is the individual and collective readiness and disposition to remain effective and act decisively, persistently, adaptively and ethically under the threat, adversity and uncertainty of combat in order to achieve the mission.",
    { x: PX + 0.16, y: 2.55, w: PW - 0.32, h: 0.5, fontFace: F, fontSize: 8.4,
      bold: true, color: SWAMP, align: "left", valign: "top", margin: 0 });
  s.addText(
    "It is the combat-specific expression of Performance Under Pressure.",
    { x: PX + 0.16, y: 3.08, w: PW - 0.32, h: 0.2, fontFace: F, fontSize: 8.2,
      italic: true, color: BLACK, align: "left", valign: "top", margin: 0 });
  flowArrow(3.44, SWAMP, "enabled by");

  // Performance Under Pressure
  leftBlock(3.66, 1.26, SWAMP, "brain", "PERFORMANCE UNDER PRESSURE", "Enabling human-performance capability");
  panel(3.66, 1.26);
  s.addText("Performance Under Pressure is the trainable individual and collective human-performance capability to:",
    { x: PX + 0.16, y: 3.74, w: PW - 0.32, h: 0.34, fontFace: F, fontSize: 8.7,
      bold: true, color: SWAMP, align: "left", valign: "top", margin: 0 });
  const checks = [
    ["Prepare for pressure", "Adapt within pressure"],
    ["Maintain performance through pressure", "Recover from pressure"],
  ];
  checks.forEach((row, r) => {
    row.forEach((t, c) => {
      s.addText([
        { text: "✓ ", options: { bold: true, color: KAWAKAWA } },
        { text: t, options: { color: BLACK } },
      ], { x: PX + 0.16 + c * 2.55, y: 4.12 + r * 0.2, w: 2.5, h: 0.2,
        fontFace: F, fontSize: 8.2, align: "left", valign: "middle", margin: 0 });
    });
  });
  s.addText(
    "Applicable across combat, command, crisis response, training, garrison leadership and high-risk technical activity.",
    { x: PX + 0.16, y: 4.58, w: PW - 0.32, h: 0.3, fontFace: F, fontSize: 7.5,
      italic: true, color: BLACK, align: "left", valign: "top", margin: 0 });
  flowArrow(5.0, KAWAKAWA, "developed and organised through");

  // Framework
  leftBlock(5.22, 1.18, KAWAKAWA, "puzzle", "ARMY COMBAT MINDSET FRAMEWORK", "Organising model");
  panel(5.22, 1.18);
  s.addText(
    "The Army Combat Mindset Framework is the organising model through which Army defines, develops, integrates and assures the capabilities, products and governance arrangements that enable Combat Mindset.",
    { x: PX + 0.16, y: 5.3, w: PW - 0.32, h: 0.52, fontFace: F, fontSize: 8.7,
      bold: true, color: SWAMP, align: "left", valign: "top", margin: 0 });
  s.addText("It organises:", { x: PX + 0.16, y: 5.84, w: 1.2, h: 0.16, fontFace: F,
    fontSize: 7.6, italic: true, color: BLACK, align: "left", valign: "middle", margin: 0 });
  const org = [
    ["Doctrinal definitions", "Desired outcomes", "Provisional pillars"],
    ["Developmental progression", "Products and methods", "Delivery responsibilities"],
    ["Governance", "Evidence", "Assurance"],
  ];
  org.forEach((col, c) => {
    s.addText(col.map((t, i) => ({
      text: "·  " + t, options: { breakLine: i < col.length - 1 },
    })), { x: PX + 0.16 + c * 1.72, y: 6.02, w: 1.7, h: 0.34, fontFace: F,
      fontSize: 7.2, color: BLACK, align: "left", valign: "top", margin: 0 });
  });
  flowArrow(6.52, SWAMP, "delivered through");

  // ---- capability strands ------------------------------------------------
  s.addShape("rect", { x: L, y: 6.74, w: W, h: 1.24, fill: { color: MOAWHANGO, transparency: 72 } });
  s.addText("PROVISIONAL CAPABILITY PILLARS", { x: L, y: 6.79, w: W, h: 0.18, fontFace: F,
    fontSize: 10, bold: true, color: SWAMP, charSpacing: 2, align: "center",
    valign: "middle", margin: 0 });
  s.addText("Provisional working pillars — subject to Phase 1 validation", {
    x: L, y: 6.96, w: W, h: 0.13, fontFace: F, fontSize: 6.5, italic: true,
    color: BLACK, align: "center", valign: "middle", margin: 0 });
  const strands = [
    ["compass", "Leadership"], ["mskills", "Self-regulation"], ["target", "Performance cognition"],
    ["heart", "Resilience & recovery"], ["dumbbell", "Physical performance"],
    ["medal", "Identity, values & will"], ["users", "Collective performance"],
  ];
  const cellW = W / 7;
  strands.forEach(([ic, label], i) => {
    const cx = L + i * cellW + cellW / 2;
    const filled = ic === "target";
    s.addShape("ellipse", { x: cx - 0.19, y: 7.12, w: 0.38, h: 0.38,
      fill: { color: filled ? SWAMP : WHITE },
      line: { color: SWAMP, width: 1.25 } });
    s.addImage({ data: filled ? I.target : I[ic], x: cx - 0.11, y: 7.2, w: 0.22, h: 0.22 });
    s.addText(label, { x: L + i * cellW + 0.03, y: 7.54, w: cellW - 0.06, h: 0.42,
      fontFace: F, fontSize: 6.8, bold: true, color: SWAMP, align: "center",
      valign: "top", margin: 0 });
  });

  // connector + clarifier
  s.addShape("triangle", { x: L + W / 2 - 0.08, y: 8.06, w: 0.16, h: 0.12,
    fill: { color: SWAMP }, rotate: 180 });
  s.addText("each product contributes across multiple pillars", {
    x: L + W / 2 + 0.16, y: 8.04, w: 3.2, h: 0.16, fontFace: F, fontSize: 7.5,
    italic: true, color: BLACK, align: "left", valign: "middle", margin: 0 });

  // ---- products ----------------------------------------------------------
  s.addText("TRAINING PRODUCTS AND METHODS", { x: L, y: 8.26, w: W, h: 0.2,
    fontFace: F, fontSize: 10.5, bold: true, color: SWAMP, charSpacing: 2,
    align: "center", valign: "middle", margin: 0 });
  const prods = [
    ["NZALC Performance Under Pressure package", false],
    ["NZDF Psychology products", false],
    ["COGCON", true],
    ["Scenario, experiential & progressive pressure training", false],
    ["Physical & cognitive conditioning", false],
    ["Structured reflection & recovery", false],
    ["Other products identified in Phase 1 stocktake", false],
  ];
  const pw = (W - 0.06 * 6) / 7;
  prods.forEach(([label, isCogcon], i) => {
    const px = L + i * (pw + 0.06);
    s.addShape("rect", { x: px, y: 8.52, w: pw, h: 0.78, fill: { color: WHITE },
      line: isCogcon ? { color: SWAMP, width: 1.5, dashType: "dash" }
                     : { color: WAIOURU, width: 0.75 } });
    if (isCogcon) {
      s.addText([
        { text: "COGCON", options: { bold: true, fontSize: 7.2, breakLine: true } },
        { text: "Developmental performance-cognition product", options: { fontSize: 6.2, italic: true } },
      ], { x: px + 0.03, y: 8.52, w: pw - 0.06, h: 0.78, fontFace: F, color: BLACK,
        align: "center", valign: "middle", margin: 0 });
    } else {
      s.addText(label, { x: px + 0.04, y: 8.52, w: pw - 0.08, h: 0.78, fontFace: F,
        fontSize: 7.2, bold: true, color: BLACK, align: "center", valign: "middle", margin: 0 });
    }
  });

  // ---- delivery ribbon ---------------------------------------------------
  s.addText("Dashed outline indicates developmental status pending the Phase 1 stocktake", {
    x: L, y: 9.31, w: W, h: 0.1, fontFace: F, fontSize: 6, italic: true,
    color: BLACK, align: "center", valign: "middle", margin: 0 });
  const rib = [];
  rib.push({ text: "Developed across the Prepare – Perform – Recover cycle   ·   Lead Self", options: { color: SWAMP } });
  ["Lead Teams", "Lead Leaders", "Lead Systems"].forEach((t) => {
    rib.push({ text: "  \u25BA  ", options: { color: RED, fontSize: 6.2 } });
    rib.push({ text: t, options: { color: SWAMP } });
  });
  s.addText(rib, { x: L, y: 9.4, w: W, h: 0.18, fontFace: F, fontSize: 8,
    bold: true, align: "center", valign: "middle", margin: 0 });
  s.addText(
    "Delivered by approved training establishments, units and existing instructor workforces across Army",
    { x: L, y: 9.59, w: W, h: 0.15, fontFace: F, fontSize: 7, italic: true,
      color: BLACK, align: "center", valign: "middle", margin: 0 });

  // ---- governance / programme -------------------------------------------
  const colW = 3.55, gx = L, px2 = 4.22;
  s.addShape("rect", { x: gx, y: 9.84, w: colW, h: 1.18, fill: { color: MOAWHANGO, transparency: 72 } });
  s.addImage({ data: I.landmark, x: gx + 0.14, y: 9.94, w: 0.22, h: 0.22 });
  s.addText("GOVERNANCE AND ASSURANCE", { x: gx + 0.44, y: 9.93, w: colW - 0.52,
    h: 0.22, fontFace: F, fontSize: 8.8, bold: true, color: SWAMP,
    align: "left", valign: "middle", margin: 0 });
  const gov = [
    "Army Sponsor — strategic sponsorship and policy direction",
    "COMDT ACS — interim capability integrator",
    "ACS — framework development and capability-integration lead",
    "HPC — COGCON product steward; performance-cognition adviser",
    "Layered doctrine, evidence, professional and delivery assurance",
  ];
  s.addText(gov.map((t, i) => ({
    text: t, options: { bullet: { characterCode: "2022", indent: 8 }, breakLine: i < gov.length - 1 },
  })), { x: gx + 0.18, y: 10.2, w: colW - 0.3, h: 0.78, fontFace: F, fontSize: 7,
    color: BLACK, align: "left", valign: "top", margin: 0, paraSpaceAfter: 2 });

  s.addShape("rect", { x: px2, y: 9.84, w: colW, h: 1.18, fill: { color: MOAWHANGO, transparency: 72 } });
  s.addImage({ data: I.clipboard, x: px2 + 0.14, y: 9.94, w: 0.22, h: 0.22 });
  s.addText("PROGRAMME OF WORK — PHASES 0–4", { x: px2 + 0.44, y: 9.93, w: colW - 0.52,
    h: 0.22, fontFace: F, fontSize: 8.8, bold: true, color: SWAMP,
    align: "left", valign: "middle", margin: 0 });
  const prog = [
    "0.  Define terms, sponsorship and relationship",
    "1.  Stocktake current capabilities, products and evidence",
    "2.  Draft the Army Combat Mindset Framework",
    "3.  Validate with stakeholders and units",
    "4.  Report back — Framework v1.0, November 2026",
  ];
  s.addText(prog.map((t, i) => ({
    text: t, options: { breakLine: i < prog.length - 1 },
  })), { x: px2 + 0.18, y: 10.2, w: colW - 0.3, h: 0.78, fontFace: F, fontSize: 7,
    color: BLACK, align: "left", valign: "top", margin: 0, paraSpaceAfter: 2 });

  // ---- footer: harder to kill + key point --------------------------------
  s.addShape("rect", { x: L, y: 11.16, w: W, h: 0.3, fill: { color: BLACK } });
  s.addImage({ data: I.star, x: L + 0.14, y: 11.21, w: 0.2, h: 0.2 });
  s.addText([
    { text: "HARDER TO KILL", options: { bold: true, fontSize: 10, color: RED, charSpacing: 2.5 } },
    { text: "      Proposed Warfighter Focus tagline — subject to sponsor endorsement",
      options: { fontSize: 7, color: WHITE } },
  ], { x: L + 0.46, y: 11.16, w: W - 0.56, h: 0.3, fontFace: F,
    align: "left", valign: "middle", margin: 0 });

  await pres.writeFile({ fileName: "output/combat-mindset-onepager-portrait.pptx" });
  console.log("written output/combat-mindset-onepager-portrait.pptx");
})();
