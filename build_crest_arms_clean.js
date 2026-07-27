// COMBAT MINDSET — sword and taiaha in the clean brandmark language
// (dark green on white, single red accent). Three ring treatments from the
// clean exploration board, with application examples. Concept only.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const F = "Arial";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";
const TAG = "REMAIN EFFECTIVE. ACT DECISIVELY.";

async function svgPng(svg, px = 900) {
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Crossed sword and taiaha as flat silhouettes: ink for weapons, accent
// for the tauri feather collar — the mark's single red element.
function arms(ink, accent) {
  return `
  <polygon points="57,47 161,151 151,161 47,57" fill="#${ink}"/>
  <ellipse cx="169" cy="169" rx="9" ry="17" transform="rotate(45 169 169)" fill="#${accent}"/>
  <polygon points="184,174 211,211 174,184" fill="#${ink}"/>
  <polygon points="106,166 90,150 210,46" fill="#${ink}"/>
  <line x1="83" y1="151" x2="105" y2="173" stroke="#${ink}" stroke-width="9" stroke-linecap="round"/>
  <line x1="94" y1="162" x2="72" y2="184" stroke="#${ink}" stroke-width="10" stroke-linecap="butt"/>
  <circle cx="65" cy="191" r="9" fill="#${ink}"/>`;
}

function armsGroup(scale, ink, accent) {
  return `<g transform="translate(128 128) scale(${scale}) translate(-128 -128)">${arms(ink, accent)}</g>`;
}

// arc helper for the broken ring (focus point)
function ringArc(r, a0, a1, ink, w) {
  const rad = (d) => (d * Math.PI) / 180;
  const x0 = 128 + r * Math.sin(rad(a0)), y0 = 128 - r * Math.cos(rad(a0));
  const x1 = 128 + r * Math.sin(rad(a1)), y1 = 128 - r * Math.cos(rad(a1));
  const large = a1 - a0 > 180 ? 1 : 0;
  return `<path d="M ${x0.toFixed(1)},${y0.toFixed(1)} A ${r},${r} 0 ${large},1 ${x1.toFixed(1)},${y1.toFixed(1)}"
    fill="none" stroke="#${ink}" stroke-width="${w}" stroke-linecap="round"/>`;
}

const marks = {
  focusPoint: (ink, accent) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    ${ringArc(92, 20, 70, ink, 13)}${ringArc(92, 110, 160, ink, 13)}
    ${ringArc(92, 200, 250, ink, 13)}${ringArc(92, 290, 340, ink, 13)}
    ${armsGroup(0.56, ink, accent)}
  </svg>`,
  objective: (ink, accent) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <circle cx="128" cy="128" r="86" fill="none" stroke="#${ink}" stroke-width="13"/>
    <line x1="128" y1="18" x2="128" y2="64" stroke="#${ink}" stroke-width="13" stroke-linecap="round"/>
    <line x1="128" y1="192" x2="128" y2="238" stroke="#${ink}" stroke-width="13" stroke-linecap="round"/>
    <line x1="18" y1="128" x2="64" y2="128" stroke="#${ink}" stroke-width="13" stroke-linecap="round"/>
    <line x1="192" y1="128" x2="238" y2="128" stroke="#${ink}" stroke-width="13" stroke-linecap="round"/>
    ${armsGroup(0.5, ink, accent)}
  </svg>`,
  enduringCentre: (ink, accent) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <circle cx="128" cy="128" r="96" fill="none" stroke="#${ink}" stroke-width="17"/>
    ${armsGroup(0.56, ink, accent)}
  </svg>`,
};

(async () => {
  const m = {
    focusPoint: await svgPng(marks.focusPoint(SWAMP, RED)),
    objective: await svgPng(marks.objective(SWAMP, RED)),
    enduringCentre: await svgPng(marks.enduringCentre(SWAMP, RED)),
    objectiveRev: await svgPng(marks.objective(WHITE, RED)),
    objectiveSmall: await svgPng(marks.objective(SWAMP, RED), 400),
  };

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27;

  // markings + credits
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
  s.addText("Concept board 6  ·  July 2026", { x: 5.7, y: 11.51, w: 2.07, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6, color: MOAWHANGO, margin: 0 });

  // header
  s.addImage({ path: LOGO, x: L, y: 0.34, w: 1.1, h: 0.266 });
  s.addText("SWORD AND TAIAHA — CLEAN MARKS", {
    x: 1.85, y: 0.3, w: 5.92, h: 0.28, fontFace: F, fontSize: 15.5, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("The crossed arms rendered in the clean brandmark language: dark green on white, red reserved for the tauri. Exploration only.", {
    x: 1.85, y: 0.58, w: 5.92, h: 0.18, fontFace: F, fontSize: 8, italic: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addShape("line", { x: L, y: 0.9, w: W, h: 0, line: { color: BLACK, width: 1 } });

  // three marks
  const tiles = [
    { key: "focusPoint", name: "8A  FOCUS POINT",
      why: "The broken ring holds the arms loosely — focus gathering around the profession of arms." },
    { key: "objective", name: "8B  OBJECTIVE",
      why: "Sight ticks cross the ring: the crossed arms as the objective. Strongest reticle read." },
    { key: "enduringCentre", name: "8C  ENDURING CENTRE",
      why: "A heavy unbroken ring: pressure surrounds, the arms remain. Simplest and boldest." },
  ];
  const GAP = 0.17, colW = (W - 2 * GAP) / 3, Y0 = 1.1, TH = 3.35;
  tiles.forEach((t, i) => {
    const cx = L + i * (colW + GAP);
    s.addShape("rect", { x: cx, y: Y0, w: colW, h: TH,
      fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
    s.addImage({ data: m[t.key], x: cx + colW / 2 - 0.95, y: Y0 + 0.22, w: 1.9, h: 1.9 });
    s.addShape("line", { x: cx + 0.55, y: Y0 + 2.28, w: colW - 1.1, h: 0,
      line: { color: WAIOURU, width: 1 } });
    s.addText(t.name, { x: cx + 0.1, y: Y0 + 2.38, w: colW - 0.2, h: 0.2,
      fontFace: F, fontSize: 9, bold: true, color: SWAMP, charSpacing: 1.5,
      align: "center", valign: "middle", margin: 0 });
    s.addText(t.why, { x: cx + 0.15, y: Y0 + 2.62, w: colW - 0.3, h: 0.68,
      fontFace: F, fontSize: 7.2, italic: true, color: BLACK,
      align: "center", valign: "top", margin: 0 });
  });

  // promise band (echoes the clean board)
  const PY = Y0 + TH + 0.22;
  s.addShape("rect", { x: L, y: PY, w: W, h: 0.34, fill: { color: WHITE },
    line: { color: WAIOURU, width: 1 } });
  s.addText([
    { text: "OUR PROMISE:  ", options: { bold: true, color: BLACK, charSpacing: 1.5 } },
    { text: "REMAIN EFFECTIVE IN COMBAT.", options: { bold: true, color: RED, charSpacing: 1.5 } },
    { text: "  ACT DECISIVELY.", options: { bold: true, color: BLACK, charSpacing: 1.5 } },
  ], { x: L, y: PY, w: W, h: 0.34, fontFace: F, fontSize: 10,
    align: "center", valign: "middle", margin: 0 });

  // application examples
  const AY = PY + 0.56, AH = 2.75;
  s.addText("APPLICATION EXAMPLES", { x: L, y: AY - 0.06, w: W, h: 0.2,
    fontFace: F, fontSize: 8.5, bold: true, color: SWAMP, charSpacing: 2,
    align: "center", valign: "middle", margin: 0 });

  const half = (W - GAP) / 2;
  // left: slide header + compact lockup
  s.addShape("rect", { x: L, y: AY + 0.2, w: half, h: AH,
    fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
  // slide master header demo
  s.addShape("rect", { x: L + 0.2, y: AY + 0.45, w: half - 0.4, h: 0.62,
    fill: { color: WHITE }, line: { color: WAIOURU, width: 0.5 } });
  s.addImage({ path: LOGO, x: L + 0.32, y: AY + 0.66, w: 0.72, h: 0.174 });
  s.addShape("line", { x: L + 1.18, y: AY + 0.55, w: 0, h: 0.42,
    line: { color: WAIOURU, width: 0.75 } });
  s.addImage({ data: m.objectiveSmall, x: L + 1.3, y: AY + 0.56, w: 0.4, h: 0.4 });
  s.addText([
    { text: "COMBAT MINDSET", options: { bold: true, fontSize: 9.5, color: BLACK, breakLine: true } },
    { text: TAG, options: { fontSize: 5.6, color: BLACK } },
  ], { x: L + 1.8, y: AY + 0.45, w: half - 2.1, h: 0.62, fontFace: F,
    align: "left", valign: "middle", margin: 0 });
  s.addText("slide master header", { x: L + 0.2, y: AY + 1.12, w: half - 0.4, h: 0.16,
    fontFace: F, fontSize: 6.5, italic: true, color: BLACK, align: "center",
    valign: "middle", margin: 0 });
  // compact horizontal lockup
  s.addImage({ data: m.objectiveSmall, x: L + 0.45, y: AY + 1.6, w: 0.66, h: 0.66 });
  s.addShape("line", { x: L + 1.28, y: AY + 1.62, w: 0, h: 0.62,
    line: { color: WAIOURU, width: 1 } });
  s.addText([
    { text: "COMBAT MINDSET", options: { bold: true, fontSize: 14, color: BLACK, breakLine: true } },
    { text: TAG, options: { fontSize: 6.8, color: BLACK } },
  ], { x: L + 1.42, y: AY + 1.58, w: half - 1.7, h: 0.7, fontFace: F,
    align: "left", valign: "middle", margin: 0 });
  s.addText("compact horizontal lockup", { x: L + 0.2, y: AY + 2.42, w: half - 0.4, h: 0.16,
    fontFace: F, fontSize: 6.5, italic: true, color: BLACK, align: "center",
    valign: "middle", margin: 0 });

  // right: course handbook cover (reversed)
  const RXa = L + half + GAP;
  s.addShape("rect", { x: RXa, y: AY + 0.2, w: half, h: AH,
    fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
  const CVw = 1.85, CVx = RXa + half / 2 - CVw / 2;
  s.addShape("rect", { x: CVx, y: AY + 0.38, w: CVw, h: 2.2, fill: { color: SWAMP } });
  s.addImage({ data: m.objectiveRev, x: CVx + CVw / 2 - 0.42, y: AY + 0.56, w: 0.84, h: 0.84 });
  s.addText("COMBAT MINDSET", { x: CVx, y: AY + 1.48, w: CVw, h: 0.2, fontFace: F,
    fontSize: 10.5, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("REMAIN EFFECTIVE.\nACT DECISIVELY.", { x: CVx, y: AY + 1.68, w: CVw, h: 0.3,
    fontFace: F, fontSize: 6.6, bold: true, color: RED, align: "center",
    valign: "middle", margin: 0 });
  s.addShape("line", { x: CVx + 0.4, y: AY + 2.08, w: CVw - 0.8, h: 0,
    line: { color: WAIOURU, width: 0.75 } });
  s.addText("COURSE HANDBOOK", { x: CVx, y: AY + 2.16, w: CVw, h: 0.18, fontFace: F,
    fontSize: 6.5, bold: true, color: MOAWHANGO, charSpacing: 2, align: "center",
    valign: "middle", margin: 0 });
  s.addText("course handbook cover", { x: RXa + 0.2, y: AY + 2.66, w: half - 0.4, h: 0.16,
    fontFace: F, fontSize: 6.5, italic: true, color: BLACK, align: "center",
    valign: "middle", margin: 0 });

  // notes
  const notes = [
    "The NZ Army wordmark remains the sole official logo; these marks are exploration only.",
    "Weapons are simplified redrawings from the Badge of the New Zealand Army — Defence heraldry approval and cultural consultation (taiaha) required before adoption.",
    "This option's tagline reads “Act decisively” (per the clean exploration board) — final wording still to be confirmed.",
  ];
  s.addText(notes.map((t, i) => ({
    text: t, options: { bullet: { characterCode: "2022", indent: 8 },
      breakLine: i < notes.length - 1 },
  })), { x: 1.0, y: AY + AH + 0.42, w: 6.27, h: 0.95, fontFace: F, fontSize: 7.2,
    color: BLACK, align: "left", valign: "top", margin: 0, paraSpaceAfter: 4 });

  await pres.writeFile({ fileName: "output/combat-mindset-arms-clean.pptx" });
  console.log("written output/combat-mindset-arms-clean.pptx");
})();
