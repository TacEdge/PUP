// COMBAT MINDSET — brandmark concept board (A4 portrait)
// Six candidate marks with lockups and rationale. Concept exploration only;
// the NZ Army wordmark remains the sole official logo.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const F = "Arial";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function svgPng(svg) {
  const buf = await sharp(Buffer.from(svg)).resize(512, 512).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---- mark generators (ink = main colour, accent = Army Red) --------------
const marks = {
  reticle: (ink, accent) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <circle cx="128" cy="128" r="80" fill="none" stroke="#${ink}" stroke-width="14"/>
    <line x1="128" y1="18" x2="128" y2="70" stroke="#${ink}" stroke-width="14" stroke-linecap="round"/>
    <line x1="128" y1="186" x2="128" y2="238" stroke="#${ink}" stroke-width="14" stroke-linecap="round"/>
    <line x1="18" y1="128" x2="70" y2="128" stroke="#${ink}" stroke-width="14" stroke-linecap="round"/>
    <line x1="186" y1="128" x2="238" y2="128" stroke="#${ink}" stroke-width="14" stroke-linecap="round"/>
    <circle cx="128" cy="128" r="24" fill="#${accent}"/>
  </svg>`,
  twoStates: (ink, accent) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <path d="M119,30 A100,100 0 0,0 119,226 Z" fill="#${accent}"/>
    <path d="M137,30 A100,100 0 0,1 137,226 Z" fill="#${ink}"/>
    <circle cx="128" cy="128" r="7" fill="#${ink}"/>
  </svg>`,
  coreHolds: (ink, accent) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <polyline points="40,34 128,86 216,34" fill="none" stroke="#${ink}" stroke-width="17" stroke-opacity="0.35" stroke-linecap="round" stroke-linejoin="round"/>
    <polyline points="40,78 128,130 216,78" fill="none" stroke="#${ink}" stroke-width="17" stroke-opacity="0.65" stroke-linecap="round" stroke-linejoin="round"/>
    <polyline points="40,122 128,174 216,122" fill="none" stroke="#${ink}" stroke-width="17" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="106" y="196" width="44" height="44" fill="#${accent}"/>
  </svg>`,
  steadyPulse: (ink, accent) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <polyline points="14,128 36,128 48,92 62,170 76,58 90,198 104,128" fill="none" stroke="#${accent}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
    <line x1="104" y1="128" x2="218" y2="128" stroke="#${ink}" stroke-width="13" stroke-linecap="round"/>
    <polygon points="212,112 244,128 212,144" fill="#${ink}"/>
  </svg>`,
  koruCoil: (ink, accent) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <path d="M223,140 A95,95 0 1,0 33,140 A76,76 0 0,0 185,140 A57,57 0 1,0 71,140 A38,38 0 0,0 147,140 A19,19 0 1,0 109,140"
      fill="none" stroke="#${ink}" stroke-width="15" stroke-linecap="round"/>
    <circle cx="128" cy="140" r="13" fill="#${accent}"/>
  </svg>`,
  stencil: (ink, accent) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <circle cx="128" cy="128" r="100" fill="#000000" stroke="#${MOAWHANGO}" stroke-width="8"/>
    <rect x="48" y="114" width="160" height="24" fill="#${accent}" transform="rotate(-12 128 128)"/>
    <text x="128" y="163" text-anchor="middle" font-family="Arial, Liberation Sans, sans-serif"
      font-weight="bold" font-size="98" letter-spacing="2" fill="#${WHITE}">CM</text>
  </svg>`,
};

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W;

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
  s.addText("Concept board  ·  July 2026", { x: 5.7, y: 11.51, w: 2.07, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6, color: MOAWHANGO, margin: 0 });

  // header
  s.addImage({ path: LOGO, x: L, y: 0.34, w: 1.1, h: 0.266 });
  s.addText("COMBAT MINDSET — BRANDMARK CONCEPTS", {
    x: 1.85, y: 0.3, w: 5.92, h: 0.28, fontFace: F, fontSize: 15.5, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Exploration board for discussion. No mark is endorsed; the NZ Army wordmark remains the sole official logo.", {
    x: 1.85, y: 0.58, w: 5.92, h: 0.18, fontFace: F, fontSize: 8, italic: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addShape("line", { x: L, y: 0.9, w: W, h: 0, line: { color: BLACK, width: 1 } });

  // tiles: 2 cols x 3 rows
  const tiles = [
    { key: "reticle", dark: false, name: "01  THE RETICLE",
      why: "Focus under threat. Extends the crosshair motif already used across the Way Forward suite.",
      ink: BLACK, accent: RED },
    { key: "twoStates", dark: true, name: "02  TWO STATES, ONE MIND",
      why: "Red head–blue head heritage: arousal mastered, not suppressed. One mind holding both states.",
      ink: MOAWHANGO, accent: RED },
    { key: "coreHolds", dark: false, name: "03  THE CORE HOLDS",
      why: "Pressure bears down in waves; the core remains intact. Direct read of Performance Under Pressure.",
      ink: SWAMP, accent: RED },
    { key: "steadyPulse", dark: false, name: "04  STEADY UNDER FIRE",
      why: "Interference settles into effective action: performance = potential − interference, drawn as a line.",
      ink: BLACK, accent: RED },
    { key: "koruCoil", dark: false, name: "05  THE KORU COIL",
      why: "NZ identity: a koru wound like a spring under load — strength and growth through pressure.",
      ink: KAWAKAWA, accent: RED },
    { key: "stencil", dark: true, name: "06  CM STENCIL ROUNDEL",
      why: "Utilitarian military stencil for patches, course materials and slides. Reads at any size.",
      ink: BLACK, accent: RED, tileFill: BLACK },
  ];

  const GAP = 0.17, colW = (W - GAP) / 2, rowH = 3.22, rowGap = 0.17;
  const Y0 = 1.08;

  for (let i = 0; i < tiles.length; i++) {
    const t = tiles[i];
    const cx = L + (i % 2) * (colW + GAP);
    const cy = Y0 + Math.floor(i / 2) * (rowH + rowGap);
    const darkFill = t.tileFill || SWAMP;
    const bg = t.dark ? darkFill : WHITE;
    const fg = t.dark ? WHITE : BLACK;

    s.addShape("rect", { x: cx, y: cy, w: colW, h: rowH,
      fill: { color: bg },
      line: { color: t.dark ? bg : WAIOURU, width: 0.75 } });

    const png = await svgPng(marks[t.key](t.ink, t.accent));
    s.addImage({ data: png, x: cx + colW / 2 - 0.62, y: cy + 0.22, w: 1.24, h: 1.24 });

    s.addText(t.name, { x: cx + 0.15, y: cy + 1.56, w: colW - 0.3, h: 0.2,
      fontFace: F, fontSize: 9.5, bold: true, color: t.dark ? MOAWHANGO : SWAMP,
      charSpacing: 1.5, align: "center", valign: "middle", margin: 0 });

    // lockup
    const small = await svgPng(marks[t.key](t.dark ? WHITE : t.ink, t.accent));
    s.addImage({ data: small, x: cx + colW / 2 - 1.28, y: cy + 1.86, w: 0.42, h: 0.42 });
    s.addText([
      { text: "COMBAT MINDSET", options: { fontSize: 13, bold: true, color: fg, breakLine: true } },
      { text: "Remain effective. Act decisively.", options: { fontSize: 6.4, italic: true, color: t.dark ? MOAWHANGO : BLACK } },
    ], { x: cx + colW / 2 - 0.76, y: cy + 1.84, w: 2.1, h: 0.48, fontFace: F,
      align: "left", valign: "middle", margin: 0 });

    s.addText(t.why, { x: cx + 0.18, y: cy + 2.44, w: colW - 0.36, h: 0.62,
      fontFace: F, fontSize: 7.4, italic: true, color: t.dark ? WHITE : BLACK,
      align: "center", valign: "top", margin: 0 });
  }

  // footer note
  s.addText(
    "Selection criteria: reads at patch size · monochrome-safe · consistent with NZDF Visual Identity Standards palette · distinct from existing NZDF unit insignia [verify against Defence heraldry before adoption].",
    { x: L, y: Y0 + 3 * rowH + 2 * rowGap + 0.06, w: W, h: 0.3, fontFace: F,
      fontSize: 7, italic: true, color: BLACK, align: "center", valign: "middle", margin: 0 });

  await pres.writeFile({ fileName: "output/combat-mindset-brandmarks.pptx" });
  console.log("written output/combat-mindset-brandmarks.pptx");
})();
