// COMBAT MINDSET — patch with the clean-board reticle at centre
// (sword and taiaha removed). Chassis retained from the 7G patch: black
// disc, Moawhango ring, arc wordmark and tagline. Concept only.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const F = "Arial";
const FSTACK = "Arial, Liberation Sans, sans-serif";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function svgPng(svg, px = 1000) {
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

function arcGlyphs(text, radius, startDeg, endDeg, fontSize, fill, bottom) {
  const chars = [...text];
  const n = chars.length;
  let out = "";
  for (let i = 0; i < n; i++) {
    const t = n === 1 ? 0.5 : i / (n - 1);
    const deg = bottom ? startDeg - t * (startDeg - endDeg)
                       : startDeg + t * (endDeg - startDeg);
    const rad = (deg * Math.PI) / 180;
    const x = 128 + radius * Math.sin(rad);
    const y = 128 - radius * Math.cos(rad);
    const rot = bottom ? deg + 180 : deg;
    if (chars[i] === " ") continue;
    out += `<text x="0" y="0" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
      font-size="${fontSize}" fill="#${fill}"
      transform="translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${rot.toFixed(1)})">${chars[i]}</text>`;
  }
  return out;
}

function ringArc(r, a0, a1, ink, w) {
  const rad = (d) => (d * Math.PI) / 180;
  const x0 = 128 + r * Math.sin(rad(a0)), y0 = 128 - r * Math.cos(rad(a0));
  const x1 = 128 + r * Math.sin(rad(a1)), y1 = 128 - r * Math.cos(rad(a1));
  const large = a1 - a0 > 180 ? 1 : 0;
  return `<path d="M ${x0.toFixed(1)},${y0.toFixed(1)} A ${r},${r} 0 ${large},1 ${x1.toFixed(1)},${y1.toFixed(1)}"
    fill="none" stroke="#${ink}" stroke-width="${w}" stroke-linecap="round"/>`;
}

function radialTick(deg, r0, r1, ink, w) {
  const rad = (deg * Math.PI) / 180;
  const x0 = 128 + r0 * Math.sin(rad), y0 = 128 - r0 * Math.cos(rad);
  const x1 = 128 + r1 * Math.sin(rad), y1 = 128 - r1 * Math.cos(rad);
  return `<line x1="${x0.toFixed(1)}" y1="${y0.toFixed(1)}" x2="${x1.toFixed(1)}" y2="${y1.toFixed(1)}"
    stroke="#${ink}" stroke-width="${w}" stroke-linecap="round"/>`;
}

// centre reticles (clean-board designs), drawn for a dark ground
const focusPointCentre = (ink, accent) => `
  ${ringArc(66, 17, 73, ink, 11)}${ringArc(66, 107, 163, ink, 11)}
  ${ringArc(66, 197, 253, ink, 11)}${ringArc(66, 287, 343, ink, 11)}
  ${radialTick(0, 54, 78, ink, 11)}${radialTick(90, 54, 78, ink, 11)}
  ${radialTick(180, 54, 78, ink, 11)}${radialTick(270, 54, 78, ink, 11)}
  <circle cx="128" cy="128" r="16" fill="#${accent}"/>`;

const objectiveCentre = (ink, accent) => `
  <circle cx="128" cy="128" r="62" fill="none" stroke="#${ink}" stroke-width="10"/>
  ${radialTick(0, 42, 86, ink, 10)}${radialTick(90, 42, 86, ink, 10)}
  ${radialTick(180, 42, 86, ink, 10)}${radialTick(270, 42, 86, ink, 10)}
  <circle cx="128" cy="128" r="14" fill="#${accent}"/>`;

const patch = (centre) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <circle cx="128" cy="128" r="124" fill="#000000" stroke="#${MOAWHANGO}" stroke-width="4"/>
  ${arcGlyphs("COMBAT MINDSET", 102, -62, 62, 25, WHITE, false)}
  ${arcGlyphs("REMAIN EFFECTIVE · ACT DECISIVE", 112, 180 + 66, 180 - 66, 13, MOAWHANGO, true)}
  ${centre}
</svg>`;

(async () => {
  const heroA = await svgPng(patch(focusPointCentre(WHITE, RED)), 1200);
  const altB = await svgPng(patch(objectiveCentre(WHITE, RED)));
  const monoA = await svgPng(patch(focusPointCentre(WHITE, WHITE)));
  const tonal = await svgPng(patch(focusPointCentre(MOAWHANGO, RED)));

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
  s.addText("Concept board 7  ·  July 2026", { x: 5.7, y: 11.51, w: 2.07, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6, color: MOAWHANGO, margin: 0 });

  // header
  s.addImage({ path: LOGO, x: L, y: 0.34, w: 1.1, h: 0.266 });
  s.addText("PATCH — CLEAN RETICLE CENTRE", {
    x: 1.85, y: 0.3, w: 5.92, h: 0.28, fontFace: F, fontSize: 15.5, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("The 7G patch chassis retained; sword and taiaha removed; centre replaced with the clean-board reticle. Exploration only.", {
    x: 1.85, y: 0.58, w: 5.92, h: 0.18, fontFace: F, fontSize: 8, italic: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addShape("line", { x: L, y: 0.9, w: W, h: 0, line: { color: BLACK, width: 1 } });

  // hero
  s.addImage({ data: heroA, x: 8.27 / 2 - 2.0, y: 1.25, w: 4.0, h: 4.0 });
  s.addText("9A  FOCUS POINT PATCH", { x: L, y: 5.4, w: W, h: 0.22,
    fontFace: F, fontSize: 11, bold: true, color: SWAMP, charSpacing: 2,
    align: "center", valign: "middle", margin: 0 });
  s.addText(
    "The clean focus-point reticle at the heart of the patch: a broken ring gathering on a single red centre — focus held under pressure. No weapons, no letters; one idea.",
    { x: 1.2, y: 5.68, w: 5.87, h: 0.4, fontFace: F, fontSize: 8, italic: true,
      color: BLACK, align: "center", valign: "top", margin: 0 });

  // supporting row
  const RY = 6.45;
  s.addShape("rect", { x: L, y: RY, w: W, h: 2.85, fill: { color: WHITE },
    line: { color: WAIOURU, width: 0.75 } });
  s.addImage({ data: altB, x: 0.95, y: RY + 0.35, w: 1.6, h: 1.6 });
  s.addText("alternative — objective centre", { x: 0.65, y: RY + 2.05, w: 2.2, h: 0.16,
    fontFace: F, fontSize: 6.8, italic: true, color: BLACK, align: "center",
    valign: "middle", margin: 0 });
  s.addImage({ data: tonal, x: 3.35, y: RY + 0.35, w: 1.6, h: 1.6 });
  s.addText("tonal — subdued field wear", { x: 3.05, y: RY + 2.05, w: 2.2, h: 0.16,
    fontFace: F, fontSize: 6.8, italic: true, color: BLACK, align: "center",
    valign: "middle", margin: 0 });
  s.addImage({ data: monoA, x: 5.75, y: RY + 0.35, w: 1.6, h: 1.6 });
  s.addText("single ink — embroidery", { x: 5.45, y: RY + 2.05, w: 2.2, h: 0.16,
    fontFace: F, fontSize: 6.8, italic: true, color: BLACK, align: "center",
    valign: "middle", margin: 0 });
  // size ladder along bottom of the row
  s.addImage({ data: heroA, x: 2.6, y: RY + 2.28, w: 0.52, h: 0.52 });
  s.addImage({ data: heroA, x: 3.3, y: RY + 2.4, w: 0.38, h: 0.38 });
  s.addImage({ data: heroA, x: 3.85, y: RY + 2.5, w: 0.26, h: 0.26 });
  s.addText("size ladder", { x: 4.35, y: RY + 2.45, w: 1.2, h: 0.16,
    fontFace: F, fontSize: 6.8, italic: true, color: BLACK, align: "left",
    valign: "middle", margin: 0 });

  // notes
  const notes = [
    "Chassis unchanged from 7G: black disc, Moawhango ring, arc wordmark and tagline.",
    "Centre reticle drawn from the clean brandmark exploration (focus point; objective offered as alternative).",
    "Tagline wording (“Act Decisive” vs “Act decisively”) remains to be confirmed.",
    "All marks remain subject to sponsor endorsement and Defence heraldry check.",
  ];
  s.addText(notes.map((t, i) => ({
    text: t, options: { bullet: { characterCode: "2022", indent: 8 },
      breakLine: i < notes.length - 1 },
  })), { x: 1.0, y: 9.55, w: 6.27, h: 1.2, fontFace: F, fontSize: 7.4,
    color: BLACK, align: "left", valign: "top", margin: 0, paraSpaceAfter: 4 });

  await pres.writeFile({ fileName: "output/combat-mindset-patch-reticle.pptx" });
  console.log("written output/combat-mindset-patch-reticle.pptx");
})();
