// COMBAT MINDSET — crest centre-symbol iterations (replacing the CM monogram)
// Same crest chassis; six combat-oriented centre symbols. Concept only.

const pptxgen = require("pptxgenjs");
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const sharp = require("sharp");
const lu = require("react-icons/lu");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const F = "Arial";
const FSTACK = "Arial, Liberation Sans, sans-serif";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function svgPng(svg, px = 700) {
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

async function luIcon(name, hex, strokeWidth = 1.8) {
  const el = React.createElement(lu[name], { color: "#" + hex, size: 256, strokeWidth });
  let svg = renderToStaticMarkup(el);
  if (!svg.includes("xmlns")) svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ');
  const buf = await sharp(Buffer.from(svg)).resize(300, 300).png().toBuffer();
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

// crest chassis without a centre symbol
const chassis = () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <circle cx="128" cy="128" r="124" fill="#000000" stroke="#${MOAWHANGO}" stroke-width="4"/>
  <circle cx="128" cy="128" r="88" fill="none" stroke="#${MOAWHANGO}" stroke-width="2.5"/>
  ${arcGlyphs("COMBAT MINDSET", 102, -62, 62, 25, WHITE, false)}
  ${arcGlyphs("REMAIN EFFECTIVE · ACT DECISIVE", 112, 180 + 66, 180 - 66, 13, MOAWHANGO, true)}
  <line x1="128" y1="34" x2="128" y2="58" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
  <line x1="128" y1="198" x2="128" y2="222" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
  <line x1="34" y1="128" x2="58" y2="128" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
  <line x1="198" y1="128" x2="222" y2="128" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
</svg>`;

// custom centre symbols (white on transparent, 256 viewBox)
const centres = {
  taiaha: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <line x1="70" y1="196" x2="186" y2="60" stroke="#${WHITE}" stroke-width="13" stroke-linecap="round"/>
    <polygon points="186,60 206,32 196,66" fill="#${WHITE}"/>
    <line x1="168" y1="64" x2="184" y2="78" stroke="#${RED}" stroke-width="7" stroke-linecap="round"/>
    <line x1="186" y1="196" x2="70" y2="60" stroke="#${WHITE}" stroke-width="13" stroke-linecap="round"/>
    <polygon points="70,60 50,32 60,66" fill="#${WHITE}"/>
    <line x1="88" y1="64" x2="72" y2="78" stroke="#${RED}" stroke-width="7" stroke-linecap="round"/>
  </svg>`,
  spearhead: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <polygon points="128,36 194,214 128,178 62,214" fill="#${WHITE}"/>
    <polygon points="128,80 158,196 128,178 98,196" fill="#${RED}"/>
  </svg>`,
  aimingPoint: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <circle cx="128" cy="128" r="58" fill="none" stroke="#${WHITE}" stroke-width="11"/>
    <circle cx="128" cy="128" r="26" fill="#${RED}"/>
  </svg>`,
};

(async () => {
  const chassisPng = await svgPng(chassis());
  const symbols = {
    swords: await luIcon("LuSwords", WHITE),
    taiaha: await svgPng(centres.taiaha, 300),
    spearhead: await svgPng(centres.spearhead, 300),
    aimingPoint: await svgPng(centres.aimingPoint, 300),
    flame: await luIcon("LuFlame", WHITE),
    bolt: await luIcon("LuZap", WHITE),
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
  s.addText("Concept board 4  ·  July 2026", { x: 5.7, y: 11.51, w: 2.07, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6, color: MOAWHANGO, margin: 0 });

  // header
  s.addImage({ path: LOGO, x: L, y: 0.34, w: 1.1, h: 0.266 });
  s.addText("CREST CENTRE SYMBOLS — ITERATIONS", {
    x: 1.85, y: 0.3, w: 5.92, h: 0.28, fontFace: F, fontSize: 15.5, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Replacing the CM monogram with a combat-oriented symbol. Exploration only; no mark is endorsed.", {
    x: 1.85, y: 0.58, w: 5.92, h: 0.18, fontFace: F, fontSize: 8, italic: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addShape("line", { x: L, y: 0.9, w: W, h: 0, line: { color: BLACK, width: 1 } });

  const tiles = [
    { key: "swords", name: "7A  CROSSED SWORDS",
      why: "The traditional combat symbol — already the Combat Mindset icon on the Way Forward model." },
    { key: "taiaha", name: "7B  CROSSED TAIAHA",
      why: "Ngāti Tūmatauenga — the Army's own weapon. Combat rooted in New Zealand warrior identity. [cultural consultation required]" },
    { key: "spearhead", name: "7C  SPEARHEAD",
      why: "The point of the spear — offensive spirit, momentum and the will to close with the enemy." },
    { key: "aimingPoint", name: "7D  AIMING POINT",
      why: "The pure reticle: one point of focus. Most minimal, most ownable, strongest tie to the roundel." },
    { key: "flame", name: "7E  INNER FIRE",
      why: "The warrior spirit that endures pressure — controlled, not extinguished." },
    { key: "bolt", name: "7F  DECISIVE STRIKE",
      why: "Speed and violence of action — act decisively, rendered literally." },
  ];

  const GAP = 0.17, colW = (W - GAP) / 2, rowH = 3.22, rowGap = 0.17, Y0 = 1.08;
  for (let i = 0; i < tiles.length; i++) {
    const t = tiles[i];
    const cx = L + (i % 2) * (colW + GAP);
    const cy = Y0 + Math.floor(i / 2) * (rowH + rowGap);
    s.addShape("rect", { x: cx, y: cy, w: colW, h: rowH,
      fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
    const CS = 1.95, ICON = 0.72;
    const mx = cx + colW / 2;
    s.addImage({ data: chassisPng, x: mx - CS / 2, y: cy + 0.22, w: CS, h: CS });
    s.addImage({ data: symbols[t.key], x: mx - ICON / 2, y: cy + 0.22 + CS / 2 - ICON / 2,
      w: ICON, h: ICON });
    s.addText(t.name, { x: cx + 0.15, y: cy + 2.28, w: colW - 0.3, h: 0.2,
      fontFace: F, fontSize: 9.5, bold: true, color: SWAMP, charSpacing: 1.5,
      align: "center", valign: "middle", margin: 0 });
    s.addText(t.why, { x: cx + 0.2, y: cy + 2.52, w: colW - 0.4, h: 0.62,
      fontFace: F, fontSize: 7.4, italic: true, color: BLACK,
      align: "center", valign: "top", margin: 0 });
  }

  s.addText(
    "Any centre symbol must clear Defence heraldry and, where Māori design elements are used, appropriate cultural consultation, before adoption.",
    { x: L, y: Y0 + 3 * rowH + 2 * rowGap + 0.05, w: W, h: 0.3, fontFace: F,
      fontSize: 7, italic: true, color: BLACK, align: "center", valign: "middle", margin: 0 });

  await pres.writeFile({ fileName: "output/combat-mindset-crest-symbols.pptx" });
  console.log("written output/combat-mindset-crest-symbols.pptx");
})();
