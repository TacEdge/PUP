// COMBAT MINDSET — brandmark evolution board: option 06 (CM stencil roundel)
// Six evolutions of the stencil direction plus an application-test strip.
// Concept exploration only; the NZ Army wordmark remains the sole official logo.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const F = "Arial";
const FSTACK = "Arial, Liberation Sans, sans-serif";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function svgPng(svg) {
  const buf = await sharp(Buffer.from(svg)).resize(512, 512).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

const V = {
  // 6A — refined ring stencil (the baseline from the first board)
  ringStencil: () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <circle cx="128" cy="128" r="100" fill="#000000" stroke="#${MOAWHANGO}" stroke-width="8"/>
    <rect x="48" y="114" width="160" height="24" fill="#${RED}" transform="rotate(-12 128 128)"/>
    <text x="128" y="163" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
      font-size="98" letter-spacing="2" fill="#${WHITE}">CM</text>
  </svg>`,
  // 6B — cut stencil: sliced letterforms, red underline, no bar
  cutStencil: () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <circle cx="128" cy="128" r="100" fill="#000000" stroke="#${MOAWHANGO}" stroke-width="8"/>
    <text x="128" y="163" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
      font-size="98" letter-spacing="2" fill="#${WHITE}">CM</text>
    <rect x="50" y="116" width="156" height="9" fill="#000000"/>
    <rect x="50" y="140" width="156" height="9" fill="#000000"/>
    <rect x="104" y="186" width="48" height="10" fill="#${RED}"/>
  </svg>`,
  // 6C — chevron roundel: rank-style chevron beneath the monogram
  chevronRoundel: () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <circle cx="128" cy="128" r="100" fill="#000000" stroke="#${MOAWHANGO}" stroke-width="8"/>
    <text x="128" y="148" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
      font-size="88" letter-spacing="2" fill="#${WHITE}">CM</text>
    <polyline points="82,204 128,174 174,204" fill="none" stroke="#${RED}"
      stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`,
  // 6D — reticle roundel: red sight ticks crossing the ring
  reticleRoundel: () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <circle cx="128" cy="128" r="98" fill="#000000" stroke="#${MOAWHANGO}" stroke-width="8"/>
    <line x1="128" y1="8" x2="128" y2="46" stroke="#${RED}" stroke-width="13" stroke-linecap="round"/>
    <line x1="128" y1="210" x2="128" y2="248" stroke="#${RED}" stroke-width="13" stroke-linecap="round"/>
    <line x1="8" y1="128" x2="46" y2="128" stroke="#${RED}" stroke-width="13" stroke-linecap="round"/>
    <line x1="210" y1="128" x2="248" y2="128" stroke="#${RED}" stroke-width="13" stroke-linecap="round"/>
    <text x="128" y="160" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
      font-size="90" letter-spacing="2" fill="#${WHITE}">CM</text>
  </svg>`,
  // 6E — embroidered patch: olive field, stitched border, microtype
  patchSquare: () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <rect x="20" y="20" width="216" height="216" rx="26" fill="#${KAWAKAWA}"
      stroke="#${MOAWHANGO}" stroke-width="6" stroke-dasharray="9 6"/>
    <rect x="48" y="102" width="160" height="22" fill="#${RED}" transform="rotate(-12 128 118)"/>
    <text x="128" y="150" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
      font-size="86" letter-spacing="2" fill="#${WHITE}">CM</text>
    <text x="128" y="203" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
      font-size="16" letter-spacing="2" fill="#${MOAWHANGO}">COMBAT MINDSET</text>
  </svg>`,
  // 6F — flat wordstack: container-free lockup for slides and documents
  wordstack: () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <rect x="44" y="104" width="168" height="22" fill="#${RED}" transform="rotate(-12 128 115)"/>
    <text x="128" y="152" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
      font-size="112" letter-spacing="2" fill="#${BLACK}">CM</text>
    <text x="128" y="204" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
      font-size="21" letter-spacing="5" fill="#${BLACK}">COMBAT MINDSET</text>
  </svg>`,
  // single-ink variants for the application strip
  monoRing: (ink) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <circle cx="128" cy="128" r="98" fill="none" stroke="#${ink}" stroke-width="10"/>
    <line x1="128" y1="8" x2="128" y2="46" stroke="#${ink}" stroke-width="13" stroke-linecap="round"/>
    <line x1="128" y1="210" x2="128" y2="248" stroke="#${ink}" stroke-width="13" stroke-linecap="round"/>
    <line x1="8" y1="128" x2="46" y2="128" stroke="#${ink}" stroke-width="13" stroke-linecap="round"/>
    <line x1="210" y1="128" x2="248" y2="128" stroke="#${ink}" stroke-width="13" stroke-linecap="round"/>
    <text x="128" y="160" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
      font-size="90" letter-spacing="2" fill="#${ink}">CM</text>
  </svg>`,
};

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27;

  // markings
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
  s.addText("Concept board 2  ·  July 2026", { x: 5.7, y: 11.51, w: 2.07, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6, color: MOAWHANGO, margin: 0 });

  // header
  s.addImage({ path: LOGO, x: L, y: 0.34, w: 1.1, h: 0.266 });
  s.addText("CM STENCIL ROUNDEL — EVOLUTIONS", {
    x: 1.85, y: 0.3, w: 5.92, h: 0.28, fontFace: F, fontSize: 15.5, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Developing concept 06. Exploration only; no mark is endorsed. NZ Army wordmark remains the sole official logo.", {
    x: 1.85, y: 0.58, w: 5.92, h: 0.18, fontFace: F, fontSize: 8, italic: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addShape("line", { x: L, y: 0.9, w: W, h: 0, line: { color: BLACK, width: 1 } });

  const tiles = [
    { key: "ringStencil", dark: true, name: "6A  RING STENCIL",
      why: "The baseline: ringed roundel, stencil bar behind the monogram. Formal, badge-like." },
    { key: "cutStencil", dark: true, name: "6B  CUT STENCIL",
      why: "Sliced letterforms carry the stencil idea without the bar; red underline as the only accent." },
    { key: "chevronRoundel", dark: true, name: "6C  CHEVRON ROUNDEL",
      why: "Rank-style chevron beneath the monogram — soldierly, ties to the pressure chevrons of concept 03." },
    { key: "reticleRoundel", dark: true, name: "6D  RETICLE ROUNDEL",
      why: "Sight ticks cross the ring — merges the stencil with concept 01 and the Way Forward hero motif." },
    { key: "patchSquare", dark: false, name: "6E  EMBROIDERED PATCH",
      why: "Olive field with stitched border and microtype — ready for uniform patch or course badge." },
    { key: "wordstack", dark: false, name: "6F  FLAT WORDSTACK",
      why: "Container-free lockup for document covers, slide masters and letterheads." },
  ];

  const GAP = 0.17, colW = (W - GAP) / 2, rowH = 2.72, rowGap = 0.14, Y0 = 1.06;
  for (let i = 0; i < tiles.length; i++) {
    const t = tiles[i];
    const cx = L + (i % 2) * (colW + GAP);
    const cy = Y0 + Math.floor(i / 2) * (rowH + rowGap);
    s.addShape("rect", { x: cx, y: cy, w: colW, h: rowH,
      fill: { color: t.dark ? BLACK : WHITE },
      line: { color: t.dark ? BLACK : WAIOURU, width: 0.75 } });
    const png = await svgPng(V[t.key]());
    s.addImage({ data: png, x: cx + colW / 2 - 0.72, y: cy + 0.16, w: 1.44, h: 1.44 });
    s.addText(t.name, { x: cx + 0.15, y: cy + 1.7, w: colW - 0.3, h: 0.2,
      fontFace: F, fontSize: 9.5, bold: true, color: t.dark ? MOAWHANGO : SWAMP,
      charSpacing: 1.5, align: "center", valign: "middle", margin: 0 });
    s.addText(t.why, { x: cx + 0.2, y: cy + 1.96, w: colW - 0.4, h: 0.62,
      fontFace: F, fontSize: 7.4, italic: true, color: t.dark ? WHITE : BLACK,
      align: "center", valign: "top", margin: 0 });
  }

  // ---- application tests --------------------------------------------------
  const AY = Y0 + 3 * rowH + 2 * rowGap + 0.12; // ≈ 9.7
  s.addText("APPLICATION TESTS — 6D RETICLE ROUNDEL", { x: L, y: AY, w: W, h: 0.2,
    fontFace: F, fontSize: 8.5, bold: true, color: SWAMP, charSpacing: 2,
    align: "center", valign: "middle", margin: 0 });

  const full = await svgPng(V.reticleRoundel());
  const monoBlack = await svgPng(V.monoRing(BLACK));
  const monoWhite = await svgPng(V.monoRing(WHITE));
  const monoOlive = await svgPng(V.monoRing(KAWAKAWA));

  const iy = AY + 0.3;
  // size ladder
  s.addImage({ data: full, x: 0.95, y: iy, w: 0.85, h: 0.85 });
  s.addImage({ data: full, x: 1.95, y: iy + 0.28, w: 0.55, h: 0.55 });
  s.addImage({ data: full, x: 2.65, y: iy + 0.5, w: 0.32, h: 0.32 });
  s.addText("size ladder", { x: 0.85, y: iy + 0.92, w: 2.2, h: 0.16, fontFace: F,
    fontSize: 6.8, italic: true, color: BLACK, align: "center", valign: "middle", margin: 0 });
  // monochrome
  s.addImage({ data: monoBlack, x: 3.75, y: iy + 0.05, w: 0.75, h: 0.75 });
  s.addText("one colour", { x: 3.55, y: iy + 0.92, w: 1.15, h: 0.16, fontFace: F,
    fontSize: 6.8, italic: true, color: BLACK, align: "center", valign: "middle", margin: 0 });
  // reversed
  s.addShape("rect", { x: 5.0, y: iy, w: 0.85, h: 0.85, fill: { color: BLACK } });
  s.addImage({ data: monoWhite, x: 5.05, y: iy + 0.05, w: 0.75, h: 0.75 });
  s.addText("reversed", { x: 4.9, y: iy + 0.92, w: 1.05, h: 0.16, fontFace: F,
    fontSize: 6.8, italic: true, color: BLACK, align: "center", valign: "middle", margin: 0 });
  // subdued
  s.addShape("rect", { x: 6.35, y: iy, w: 0.85, h: 0.85, fill: { color: MOAWHANGO } });
  s.addImage({ data: monoOlive, x: 6.4, y: iy + 0.05, w: 0.75, h: 0.75 });
  s.addText("subdued", { x: 6.25, y: iy + 0.92, w: 1.05, h: 0.16, fontFace: F,
    fontSize: 6.8, italic: true, color: BLACK, align: "center", valign: "middle", margin: 0 });

  s.addText(
    "Check any preferred mark against Defence heraldry and existing unit insignia before adoption.",
    { x: L, y: iy + 1.12, w: W, h: 0.18, fontFace: F, fontSize: 7, italic: true,
      color: BLACK, align: "center", valign: "middle", margin: 0 });

  await pres.writeFile({ fileName: "output/combat-mindset-brandmarks-cm.pptx" });
  console.log("written output/combat-mindset-brandmarks-cm.pptx");
})();
