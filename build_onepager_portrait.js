// COMBAT MINDSET THE WAY FORWARD : portrait A4, design iteration 5
// One page, one story: Combat Mindset, enabled by Performance Under Pressure,
// developed, organised and assured through the Army Combat Mindset Framework,
// achieved through a five-phase Framework Development Programme (vertical
// pathway, phases 1-5).

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
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W, MID = L + W / 2;

  // ---- chrome ------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.5, w: 1.1, h: 0.266 });
  s.addText("COMBAT MINDSET THE WAY FORWARD", {
    x: 1.85, y: 0.47, w: 5.92, h: 0.32, fontFace: F, fontSize: 15.5, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Army Command School  ·  ACS 2026", {
    x: L, y: 11.45, w: 2.6, h: 0.18, align: "left", valign: "middle",
    fontFace: F, fontSize: 6, color: BLACK, margin: 0 });
  s.addText("Draft v0.8  ·  July 2026", { x: 5.7, y: 11.45, w: 2.07, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6, color: BLACK, margin: 0 });

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
  s.addShape("rect", { x: L, y: 1.14, w: W, h: 1.56, fill: { color: BLACK } });
  pill(1.02, 2.4, "1)  WARFIGHTING IMPERATIVE", RED);
  s.addImage({ data: I.crosshairHero, x: L + 0.3, y: 1.52, w: 0.8, h: 0.8, transparency: 40 });
  s.addText("COMBAT MINDSET", {
    x: L, y: 1.52, w: W, h: 0.62, fontFace: F, fontSize: 37, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Remain effective. Act decisively. Harder to kill.", {
    x: L, y: 2.2, w: W, h: 0.3, fontFace: F, fontSize: 14, bold: true,
    color: RED, align: "center", valign: "middle", margin: 0 });

  midConnector(2.84, "enabled by");

  // ---- section 2: Performance Under Pressure -----------------------------
  s.addShape("rect", { x: L, y: 3.42, w: W, h: 1.24, fill: { color: SWAMP } });
  pill(3.3, 4.0, "2)  ENABLING HUMAN-PERFORMANCE CAPABILITY", SWAMP);
  s.addImage({ data: I.brainW, x: L + 0.22, y: 3.8, w: 0.48, h: 0.48 });
  s.addText("PERFORMANCE UNDER PRESSURE", {
    x: L, y: 3.7, w: W, h: 0.46, fontFace: F, fontSize: 22.5, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Prepare   •   Perform   •   Recover", {
    x: L, y: 4.2, w: W, h: 0.26, fontFace: F, fontSize: 12, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });

  midConnector(4.8, "developed, organised and assured through");

  // ---- section 3: the framework ------------------------------------------
  s.addShape("rect", { x: L, y: 5.38, w: W, h: 1.14, fill: { color: KAWAKAWA } });
  pill(5.26, 2.1, "3)  ORGANISING SYSTEM", KAWAKAWA);
  s.addImage({ data: I.puzzleW, x: L + 0.22, y: 5.72, w: 0.44, h: 0.44 });
  s.addText("THE ARMY COMBAT MINDSET FRAMEWORK", {
    x: L, y: 5.6, w: W, h: 0.4, fontFace: F, fontSize: 17.5, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("The Army system through which Combat Mindset is governed, developed, delivered and assured.", {
    x: L, y: 6.04, w: W, h: 0.24, fontFace: F, fontSize: 9.5,
    color: WHITE, align: "center", valign: "middle", margin: 0 });

  midConnector(6.66, "achieved through");

  // ---- section 4: framework development programme (vertical pathway) -----
  s.addShape("rect", { x: L, y: 7.36, w: W, h: 3.72,
    fill: { color: MOAWHANGO, transparency: 72 } });
  pill(7.24, 3.7, "4)  FRAMEWORK DEVELOPMENT PROGRAMME", SWAMP);

  const phases = [
    ["1", "Define and govern",
      "Confirm terminology, governance, roles and responsibilities."],
    ["2", "Understand",
      "Assess existing doctrine, products, delivery and governance."],
    ["3", "Design",
      "Develop the Combat Mindset Framework, delivery architecture and outcomes."],
    ["4", "Validate",
      "Refine the framework with key stakeholders and conduct bounded pilots."],
    ["5", "Endorse and implement",
      "Deliver the framework for approval and implementation."],
  ];
  const LN = L + 0.62;      // vertical line x
  const CY0 = 7.98, PITCH = 0.66, CD = 0.42;
  s.addShape("line", { x: LN, y: CY0, w: 0, h: PITCH * 4,
    line: { color: SWAMP, width: 1.5 } });
  phases.forEach(([n, title, desc], i) => {
    const cy = CY0 + i * PITCH;
    s.addShape("ellipse", { x: LN - CD / 2, y: cy - CD / 2, w: CD, h: CD,
      fill: { color: SWAMP }, line: { color: WHITE, width: 1.5 } });
    s.addText(n, { x: LN - CD / 2, y: cy - CD / 2, w: CD, h: CD, fontFace: F,
      fontSize: 13, bold: true, color: WHITE, align: "center",
      valign: "middle", margin: 0 });
    s.addText(title, { x: LN + 0.4, y: cy - 0.26, w: R - LN - 0.6, h: 0.24,
      fontFace: F, fontSize: 11, bold: true, color: SWAMP, align: "left",
      valign: "middle", margin: 0 });
    s.addText(desc, { x: LN + 0.4, y: cy - 0.01, w: R - LN - 0.6, h: 0.24,
      fontFace: F, fontSize: 8.5, color: BLACK, align: "left",
      valign: "middle", margin: 0 });
  });

  await pres.writeFile({ fileName: "output/combat-mindset-onepager-portrait.pptx" });
  console.log("written output/combat-mindset-onepager-portrait.pptx");
})();
