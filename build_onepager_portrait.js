// COMBAT MINDSET FRAMEWORK PROPOSAL : portrait A4, design iteration 6
// Executive presentation: larger brand mark, clean header (logo / title /
// originator), version control in document properties rather than on the
// page, and a roomier five-phase vertical pathway.

const pptxgen = require("pptxgenjs");
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const sharp = require("sharp");
const lu = require("react-icons/lu");

// NZ Army palette, as published in the Visual Identity Guidelines p58.
const RED = "D31145", BLACK = "000000", WHITE = "FFFFFF";   // 200 C, Process Black C
const SWAMP = "00261B", KAWAKAWA = "444D06", WAIOURU = "B3A650", MOAWHANGO = "DFD8AD";
const F = "Arial";          // Neue Haas Grotesk in production
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function svgPng(body, px = 600) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">${body}</svg>`;
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---- shield emblem family (family C) --------------------------------------
function famArc(r, a0, a1, ink, w) {
  const rad = (d) => (d * Math.PI) / 180;
  const x0 = 128 + r * Math.sin(rad(a0)), y0 = 128 - r * Math.cos(rad(a0));
  const x1 = 128 + r * Math.sin(rad(a1)), y1 = 128 - r * Math.cos(rad(a1));
  return `<path d="M ${x0.toFixed(1)},${y0.toFixed(1)} A ${r},${r} 0 0,1 ${x1.toFixed(1)},${y1.toFixed(1)}"
    fill="none" stroke="#${ink}" stroke-width="${w}" stroke-linecap="round"/>`;
}

const shieldCore = (ink, accent) => `
  <g transform="translate(128 128) scale(0.78) translate(-128 -128)">
    <path d="M128,26 L210,52 V128 C210,180 176,214 128,232 C80,214 46,180 46,128 V52 Z"
      fill="none" stroke="#${ink}" stroke-width="12" stroke-linejoin="round"/>
    <polyline points="86,150 128,102 170,150" fill="none" stroke="#${accent}"
      stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
  </g>`;

const emblemCM = (ink, accent) => `
  <circle cx="128" cy="128" r="96" fill="none" stroke="#${ink}" stroke-width="8"/>
  <g transform="translate(128 128) scale(0.74) translate(-128 -128)">${shieldCore(ink, accent)}</g>`;

const emblemPUP = (ink, accent) => `
  ${famArc(94, 15, 105, ink, 11)}
  ${famArc(94, 135, 225, ink, 11)}
  ${famArc(94, 255, 345, ink, 11)}
  <g transform="translate(128 128) scale(0.6) translate(-128 -128)">${shieldCore(ink, accent)}</g>`;

const emblemFW = (ink, accent) => `
  <circle cx="128" cy="128" r="96" fill="none" stroke="#${ink}" stroke-width="8"/>
  <g opacity="0.35">
    <line x1="84" y1="42" x2="84" y2="214" stroke="#${ink}" stroke-width="4"/>
    <line x1="172" y1="42" x2="172" y2="214" stroke="#${ink}" stroke-width="4"/>
    <line x1="42" y1="84" x2="214" y2="84" stroke="#${ink}" stroke-width="4"/>
    <line x1="42" y1="172" x2="214" y2="172" stroke="#${ink}" stroke-width="4"/>
  </g>
  <g transform="translate(128 128) scale(0.66) translate(-128 -128)">${shieldCore(ink, accent)}</g>`;

(async () => {
  const I = {
    // No red accent: red is reserved for decision, action notation and
    // defined threshold states. None of the four cards is a decision.
    cm: await svgPng(emblemCM(WHITE, WHITE)),
    pup: await svgPng(emblemPUP(WHITE, WHITE)),
    fw: await svgPng(emblemFW(WHITE, WHITE)),
  };

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
  s.addImage({ data: I.cm, x: L + 0.24, y: 1.94, w: 0.82, h: 0.82 });
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
  s.addImage({ data: I.pup, x: L + 0.26, y: 3.84, w: 0.6, h: 0.6 });
  s.addText("PERFORMANCE UNDER PRESSURE", {
    x: L, y: 3.80, w: W, h: 0.46, fontFace: F, fontSize: 22.5, bold: true,
    color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Prepare   •   Perform   •   Recover", {
    x: L, y: 4.30, w: W, h: 0.26, fontFace: F, fontSize: 9.5,
    color: WHITE, align: "center", valign: "middle", margin: 0 });

  // ---- section 3: the framework ------------------------------------------
  s.addShape("roundRect", { x: L, y: 5.16, w: W, h: 1.12, rectRadius: 0.08, fill: { color: KAWAKAWA } });
  pill(5.04, 2.1, "3)  ORGANISING SYSTEM", KAWAKAWA);
  s.addImage({ data: I.fw, x: L + 0.26, y: 5.42, w: 0.58, h: 0.58 });
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
