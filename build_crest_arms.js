// COMBAT MINDSET — crest with the crossed sword and taiaha of the NZ Army
// badge (Ngāti Tūmatauenga) as the centre symbol. Weapons redrawn as
// simplified vector forms; crown, lion, NZ cypher and scroll deliberately
// omitted. Concept only — requires Defence heraldry approval and cultural
// consultation before any use.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const BLADE = "E8E8E8", GOLD = "A89662", SHAFT = "8A6A4F", TIPBROWN = "6E4F35";
const F = "Arial";
const FSTACK = "Arial, Liberation Sans, sans-serif";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function svgPng(svg, px = 900) {
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

// Crossed sword and taiaha, 256 viewBox. mono=true renders single-ink.
function arms(mono, ink = WHITE) {
  const blade = mono ? ink : BLADE, gold = mono ? ink : GOLD;
  const shaft = mono ? ink : SHAFT, tip = mono ? ink : TIPBROWN;
  const feather = mono ? ink : RED;
  return `
  <!-- taiaha: rau (upper left) through centre to arero point (lower right) -->
  <polygon points="57,47 161,151 151,161 47,57" fill="#${shaft}"/>
  <ellipse cx="169" cy="169" rx="9" ry="17" transform="rotate(45 169 169)" fill="#${feather}"/>
  <polygon points="184,174 211,211 174,184" fill="#${tip}"/>
  <!-- sword: pommel lower left through centre to blade tip (upper right) -->
  <polygon points="106,166 90,150 210,46" fill="#${blade}"/>
  <line x1="83" y1="151" x2="105" y2="173" stroke="#${gold}" stroke-width="9" stroke-linecap="round"/>
  <line x1="94" y1="162" x2="72" y2="184" stroke="#${gold}" stroke-width="10" stroke-linecap="butt"/>
  <line x1="86" y1="164" x2="93" y2="171" stroke="#${mono ? ink : "8F7A47"}" stroke-width="3"/>
  <line x1="79" y1="171" x2="86" y2="178" stroke="#${mono ? ink : "8F7A47"}" stroke-width="3"/>
  <circle cx="65" cy="191" r="9" fill="#${gold}"/>`;
}

const crest = (mono) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <circle cx="128" cy="128" r="124" fill="#000000" stroke="#${MOAWHANGO}" stroke-width="4"/>
  <circle cx="128" cy="128" r="88" fill="none" stroke="#${MOAWHANGO}" stroke-width="2.5"/>
  ${arcGlyphs("COMBAT MINDSET", 102, -62, 62, 25, WHITE, false)}
  ${arcGlyphs("REMAIN EFFECTIVE · ACT DECISIVE", 112, 180 + 66, 180 - 66, 13, MOAWHANGO, true)}
  <line x1="128" y1="34" x2="128" y2="58" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
  <line x1="128" y1="198" x2="128" y2="222" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
  <line x1="34" y1="128" x2="58" y2="128" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
  <line x1="198" y1="128" x2="222" y2="128" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
  <g transform="translate(128 128) scale(0.6) translate(-128 -128)">
    ${arms(mono)}
  </g>
</svg>`;

(async () => {
  const hero = await svgPng(crest(false), 1200);
  const mono = await svgPng(crest(true), 700);
  const armsOnly = await svgPng(
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">${arms(false)}</svg>`, 500);

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
  s.addText("Concept board 5  ·  July 2026", { x: 5.7, y: 11.51, w: 2.07, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6, color: MOAWHANGO, margin: 0 });

  // header
  s.addImage({ path: LOGO, x: L, y: 0.34, w: 1.1, h: 0.266 });
  s.addText("CREST — SWORD AND TAIAHA", {
    x: 1.85, y: 0.3, w: 5.92, h: 0.28, fontFace: F, fontSize: 15.5, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Centre symbol drawn from the crossed sword and taiaha of the Badge of the New Zealand Army. Exploration only; no mark is endorsed.", {
    x: 1.85, y: 0.58, w: 5.92, h: 0.18, fontFace: F, fontSize: 8, italic: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addShape("line", { x: L, y: 0.9, w: W, h: 0, line: { color: BLACK, width: 1 } });

  // hero
  s.addImage({ data: hero, x: 8.27 / 2 - 2.0, y: 1.25, w: 4.0, h: 4.0 });
  s.addText("7G  NGĀTI TŪMATAUENGA ARMS", { x: L, y: 5.4, w: W, h: 0.22,
    fontFace: F, fontSize: 11, bold: true, color: SWAMP, charSpacing: 2,
    align: "center", valign: "middle", margin: 0 });
  s.addText(
    "The sword and taiaha carried together — the two traditions of the profession of arms in Aotearoa, crossed at the point of focus. Crown, lion, cypher and scroll deliberately omitted: this is a training-culture mark, not a replacement badge.",
    { x: 1.2, y: 5.68, w: 5.87, h: 0.5, fontFace: F, fontSize: 8, italic: true,
      color: BLACK, align: "center", valign: "top", margin: 0 });

  // supporting row: arms alone, mono, small sizes
  const RY = 6.55;
  s.addShape("rect", { x: L, y: RY, w: W, h: 2.6, fill: { color: WHITE },
    line: { color: WAIOURU, width: 0.75 } });
  // arms only
  s.addImage({ data: armsOnly, x: 1.0, y: RY + 0.3, w: 1.5, h: 1.5 });
  s.addText("centre symbol alone", { x: 0.7, y: RY + 1.9, w: 2.1, h: 0.16,
    fontFace: F, fontSize: 6.8, italic: true, color: BLACK, align: "center",
    valign: "middle", margin: 0 });
  // mono
  s.addShape("rect", { x: 3.3, y: RY + 0.3, w: 1.5, h: 1.5, fill: { color: BLACK } });
  s.addImage({ data: mono, x: 3.35, y: RY + 0.35, w: 1.4, h: 1.4 });
  s.addText("single ink — embroidery", { x: 3.0, y: RY + 1.9, w: 2.1, h: 0.16,
    fontFace: F, fontSize: 6.8, italic: true, color: BLACK, align: "center",
    valign: "middle", margin: 0 });
  // size ladder
  s.addImage({ data: hero, x: 5.65, y: RY + 0.35, w: 0.95, h: 0.95 });
  s.addImage({ data: hero, x: 6.75, y: RY + 0.65, w: 0.62, h: 0.62 });
  s.addImage({ data: hero, x: 7.0, y: RY + 1.42, w: 0.38, h: 0.38 });
  s.addText("size ladder", { x: 5.55, y: RY + 1.9, w: 2.0, h: 0.16,
    fontFace: F, fontSize: 6.8, italic: true, color: BLACK, align: "center",
    valign: "middle", margin: 0 });

  // caveats
  const notes = [
    "Weapons are simplified redrawings of the sword and taiaha from the Badge of the New Zealand Army — not traced artwork.",
    "Use of elements derived from the Army badge requires Defence heraldry approval.",
    "Use of the taiaha and any Māori design element requires appropriate cultural consultation (Ngāti Tūmatauenga kaitiaki).",
    "Tagline wording (“Act Decisive” vs “Act decisively”) remains to be confirmed.",
  ];
  s.addText(notes.map((t, i) => ({
    text: t, options: { bullet: { characterCode: "2022", indent: 8 },
      breakLine: i < notes.length - 1 },
  })), { x: 1.0, y: 9.45, w: 6.27, h: 1.4, fontFace: F, fontSize: 7.4,
    color: BLACK, align: "left", valign: "top", margin: 0, paraSpaceAfter: 5 });

  await pres.writeFile({ fileName: "output/combat-mindset-crest-arms.pptx" });
  console.log("written output/combat-mindset-crest-arms.pptx");
})();
