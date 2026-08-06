// COMBAT MINDSET FRAMEWORK PROPOSAL : the model on a page, portrait A4.
// No emblem, badge or symbol: under the identity system the page carries its
// meaning through structure, hierarchy and the published Army palette alone.

const pptxgen = require("pptxgenjs");

// NZ Army palette, as published in the Visual Identity Guidelines p58.
const RED = "D31145", BLACK = "000000", WHITE = "FFFFFF";   // 200 C, Process Black C
const SWAMP = "00261B", KAWAKAWA = "444D06", WAIOURU = "B3A650", MOAWHANGO = "DFD8AD";
const F = "Arial";          // Neue Haas Grotesk in production
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "NZ Army Combat Mindset Framework Proposal";
  pres.company = "Army Command School";
  pres.revision = "9";
  pres.subject = "NZ Army Combat Mindset Framework Proposal";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W, MID = L + W / 2;

  // ---- header ------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.36, w: 1.72, h: 0.393 });
  s.addText("NZ ARMY COMBAT MINDSET FRAMEWORK PROPOSAL", {
    x: L, y: 0.9, w: W, h: 0.34, fontFace: F, fontSize: 16, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Army Command School", {
    x: L, y: 1.24, w: W, h: 0.18, fontFace: F, fontSize: 9, italic: true,
    color: SWAMP, align: "left", valign: "middle", margin: 0 });

  // ---- footer ------------------------------------------------------------
  s.addText("August 2026", { x: 4.77, y: 11.42, w: 3.0, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6.5, color: BLACK, margin: 0 });

  function pill(y, w, text, fill) {
    const x = MID - w / 2;
    s.addShape("roundRect", { x, y, w, h: 0.24, fill: { color: fill },
      rectRadius: 0.12, line: { color: WHITE, width: 1 } });
    s.addText(text, { x, y, w, h: 0.24, fontFace: F, fontSize: 7.8, bold: true,
      color: WHITE, charSpacing: 1.2, align: "center", valign: "middle", margin: 0 });
  }

  // ---- section 1: Combat Mindset -----------------------------------------
  s.addShape("roundRect", { x: L, y: 1.62, w: W, h: 1.5, rectRadius: 0.08, fill: { color: BLACK } });
  pill(1.5, 2.4, "1)  WARFIGHTING IMPERATIVE", BLACK);
  s.addText("COMBAT MINDSET", {
    x: L, y: 1.92, w: W, h: 0.58, fontFace: F, fontSize: 36, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Remain effective. Act decisively.", {
    x: L, y: 2.52, w: W, h: 0.24, fontFace: F, fontSize: 13.5,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Harder to kill.", {
    x: L, y: 2.76, w: W, h: 0.28, fontFace: F, fontSize: 13.5, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });

  // ---- section 2: Performance Under Pressure -----------------------------
  s.addShape("roundRect", { x: L, y: 3.54, w: W, h: 1.2, rectRadius: 0.08, fill: { color: SWAMP } });
  pill(3.42, 2.35, "2)  ENABLING CAPABILITY", SWAMP);
  s.addText("PERFORMANCE UNDER PRESSURE", {
    x: L, y: 3.80, w: W, h: 0.46, fontFace: F, fontSize: 22.5, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Prepare   •   Perform   •   Recover", {
    x: L, y: 4.30, w: W, h: 0.26, fontFace: F, fontSize: 9.5,
    color: WHITE, align: "center", valign: "middle", margin: 0 });

  // ---- section 3: the framework ------------------------------------------
  s.addShape("roundRect", { x: L, y: 5.16, w: W, h: 1.12, rectRadius: 0.08, fill: { color: KAWAKAWA } });
  pill(5.04, 2.1, "3)  ORGANISING SYSTEM", KAWAKAWA);
  s.addText("COMBAT MINDSET FRAMEWORK", {
    x: L, y: 5.34, w: W, h: 0.44, fontFace: F, fontSize: 22.5, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Governs, develops, delivers and assures Performance Under Pressure and Combat Mindset.", {
    x: L, y: 5.81, w: W, h: 0.24, fontFace: F, fontSize: 9.5,
    color: WHITE, align: "center", valign: "middle", margin: 0 });

  // ---- section 4: framework development programme (vertical pathway) -----
  s.addShape("roundRect", { x: L, y: 6.70, w: W, h: 4.54, rectRadius: 0.08,
    fill: { color: MOAWHANGO, transparency: 72 } });
  pill(6.58, 3.7, "4)  FRAMEWORK DEVELOPMENT PROGRAMME", SWAMP);

  const phases = [
    ["1", "DEFINE",
      "Confirm terminology, governance, roles and responsibilities."],
    ["2", "UNDERSTAND",
      "Assess existing doctrine, products and delivery."],
    ["3", "DESIGN",
      "Develop the Combat Mindset Framework, delivery system and outcomes."],
    ["4", "VALIDATE",
      "Refine the framework with key stakeholders and conduct bounded pilots."],
    ["5", "IMPLEMENT",
      "Deliver the framework for approval and implementation."],
  ];
  const LN = L + 0.58;      // vertical line x
  const CY0 = 7.40, PITCH = 0.81, CD = 0.42;
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
