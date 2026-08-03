// COMBAT MINDSET FRAMEWORK PROPOSAL : portrait A4, design iteration 6
// Executive presentation: larger brand mark, clean header (logo / title /
// originator), version control in document properties rather than on the
// page, and a roomier five-phase vertical pathway.

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
  };
  for (const [k, [n, c]] of Object.entries(need)) I[k] = await icon(n, c);

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "Combat Mindset Framework Proposal";
  pres.company = "Army Command School";
  pres.revision = "9";
  pres.subject = "Combat Mindset Framework Proposal";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W, MID = L + W / 2;

  // ---- header ------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.4, w: 1.38, h: 0.334 });
  s.addText("COMBAT MINDSET FRAMEWORK PROPOSAL", {
    x: L, y: 0.86, w: W, h: 0.34, fontFace: F, fontSize: 17, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Army Command School", {
    x: L, y: 1.2, w: W, h: 0.2, fontFace: F, fontSize: 9, italic: true,
    color: SWAMP, align: "left", valign: "middle", margin: 0 });

  // ---- footer ------------------------------------------------------------
  s.addText("Army Command School", {
    x: L, y: 11.42, w: 3.0, h: 0.18, align: "left", valign: "middle",
    fontFace: F, fontSize: 6.5, color: BLACK, margin: 0 });
  s.addText("August 2026", { x: 4.77, y: 11.42, w: 3.0, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6.5, color: BLACK, margin: 0 });

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

  // ---- section 1: Combat Mindset -----------------------------------------
  s.addShape("rect", { x: L, y: 1.62, w: W, h: 1.5, fill: { color: BLACK } });
  pill(1.5, 2.4, "1)  WARFIGHTING IMPERATIVE", RED);
  s.addImage({ data: I.crosshairHero, x: L + 0.3, y: 1.98, w: 0.78, h: 0.78, transparency: 40 });
  s.addText("COMBAT MINDSET", {
    x: L, y: 1.98, w: W, h: 0.6, fontFace: F, fontSize: 36, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Remain effective. Act decisively. Harder to kill.", {
    x: L, y: 2.62, w: W, h: 0.3, fontFace: F, fontSize: 14, bold: true,
    color: RED, align: "center", valign: "middle", margin: 0 });

  midConnector(3.24, "enabled by");

  // ---- section 2: Performance Under Pressure -----------------------------
  s.addShape("rect", { x: L, y: 3.8, w: W, h: 1.2, fill: { color: SWAMP } });
  pill(3.68, 4.0, "2)  ENABLING HUMAN-PERFORMANCE CAPABILITY", SWAMP);
  s.addImage({ data: I.brainW, x: L + 0.22, y: 4.16, w: 0.48, h: 0.48 });
  s.addText("PERFORMANCE UNDER PRESSURE", {
    x: L, y: 4.06, w: W, h: 0.46, fontFace: F, fontSize: 22.5, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Prepare   •   Perform   •   Recover", {
    x: L, y: 4.56, w: W, h: 0.26, fontFace: F, fontSize: 12, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });

  midConnector(5.12, "developed, organised and assured through");

  // ---- section 3: the framework ------------------------------------------
  s.addShape("rect", { x: L, y: 5.68, w: W, h: 1.12, fill: { color: KAWAKAWA } });
  pill(5.56, 2.1, "3)  ORGANISING SYSTEM", KAWAKAWA);
  s.addImage({ data: I.puzzleW, x: L + 0.22, y: 6.0, w: 0.44, h: 0.44 });
  s.addText("THE ARMY COMBAT MINDSET FRAMEWORK", {
    x: L, y: 5.9, w: W, h: 0.4, fontFace: F, fontSize: 17.5, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("The Army system through which Combat Mindset is governed, developed, delivered and assured.", {
    x: L, y: 6.33, w: W, h: 0.24, fontFace: F, fontSize: 9.5,
    color: WHITE, align: "center", valign: "middle", margin: 0 });

  midConnector(6.92, "achieved through");

  // ---- section 4: framework development programme (vertical pathway) -----
  s.addShape("rect", { x: L, y: 7.48, w: W, h: 3.76,
    fill: { color: MOAWHANGO, transparency: 72 } });
  pill(7.36, 3.7, "4)  FRAMEWORK DEVELOPMENT PROGRAMME", SWAMP);

  const phases = [
    ["1", "DEFINE",
      "Confirm terminology, governance, roles and responsibilities."],
    ["2", "UNDERSTAND",
      "Assess existing doctrine, products, delivery and governance."],
    ["3", "DESIGN",
      "Develop the Combat Mindset Framework, delivery architecture and outcomes."],
    ["4", "VALIDATE",
      "Refine the framework with key stakeholders and conduct bounded pilots."],
    ["5", "IMPLEMENT",
      "Deliver the framework for approval and implementation."],
  ];
  const LN = L + 0.58;      // vertical line x
  const CY0 = 8.1, PITCH = 0.71, CD = 0.42;
  s.addShape("line", { x: LN, y: CY0, w: 0, h: PITCH * 4,
    line: { color: SWAMP, width: 1.5 } });
  phases.forEach(([n, title, desc], i) => {
    const cy = CY0 + i * PITCH;
    s.addShape("ellipse", { x: LN - CD / 2, y: cy - CD / 2, w: CD, h: CD,
      fill: { color: SWAMP }, line: { color: WHITE, width: 1.5 } });
    s.addText(n, { x: LN - CD / 2, y: cy - CD / 2, w: CD, h: CD, fontFace: F,
      fontSize: 13, bold: true, color: WHITE, align: "center",
      valign: "middle", margin: 0 });
    s.addText(title, { x: LN + 0.4, y: cy - 0.2, w: 1.95, h: 0.4,
      fontFace: F, fontSize: 11.5, bold: true, color: SWAMP, charSpacing: 1.2,
      align: "left", valign: "middle", margin: 0 });
    s.addText(desc, { x: LN + 2.4, y: cy - 0.24, w: R - LN - 2.58, h: 0.48,
      fontFace: F, fontSize: 8.6, color: BLACK, align: "left",
      valign: "middle", margin: 0 });
  });

  await pres.writeFile({ fileName: "output/combat-mindset-onepager-portrait.pptx" });
  console.log("written output/combat-mindset-onepager-portrait.pptx");
})();
