// COMBAT MINDSET — 6D reticle roundel: lockup system board (A4 portrait)
// Brandmark + wordmark + tagline lockups, crest, compact applications and
// in-situ mocks. Concept exploration only.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const F = "Arial";
const FSTACK = "Arial, Liberation Sans, sans-serif";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";
const TAG = "REMAIN EFFECTIVE.  ACT DECISIVE.";

async function svgPng(svg, px = 512) {
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

const reticle = (ring, ticks, letters, disc) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <circle cx="128" cy="128" r="98" fill="${disc ? "#" + disc : "none"}" stroke="#${ring}" stroke-width="8"/>
  <line x1="128" y1="8" x2="128" y2="46" stroke="#${ticks}" stroke-width="13" stroke-linecap="round"/>
  <line x1="128" y1="210" x2="128" y2="248" stroke="#${ticks}" stroke-width="13" stroke-linecap="round"/>
  <line x1="8" y1="128" x2="46" y2="128" stroke="#${ticks}" stroke-width="13" stroke-linecap="round"/>
  <line x1="210" y1="128" x2="248" y2="128" stroke="#${ticks}" stroke-width="13" stroke-linecap="round"/>
  <text x="128" y="160" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
    font-size="90" letter-spacing="2" fill="#${letters}">CM</text>
</svg>`;

// librsvg has no textPath support, so circular text is placed glyph by glyph.
function arcGlyphs(text, radius, startDeg, endDeg, fontSize, fill, bottom) {
  const chars = [...text];
  const n = chars.length;
  let out = "";
  for (let i = 0; i < n; i++) {
    const t = n === 1 ? 0.5 : i / (n - 1);
    const deg = bottom
      ? startDeg - t * (startDeg - endDeg)   // traverse lower-left → lower-right
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

const crest = () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <circle cx="128" cy="128" r="124" fill="#000000" stroke="#${MOAWHANGO}" stroke-width="4"/>
  <circle cx="128" cy="128" r="88" fill="none" stroke="#${MOAWHANGO}" stroke-width="2.5"/>
  ${arcGlyphs("COMBAT MINDSET", 102, -62, 62, 25, WHITE, false)}
  ${arcGlyphs("REMAIN EFFECTIVE · ACT DECISIVE", 103, 180 + 66, 180 - 66, 13, MOAWHANGO, true)}
  <line x1="128" y1="34" x2="128" y2="58" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
  <line x1="128" y1="198" x2="128" y2="222" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
  <line x1="34" y1="128" x2="58" y2="128" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
  <line x1="198" y1="128" x2="222" y2="128" stroke="#${RED}" stroke-width="10" stroke-linecap="round"/>
  <text x="128" y="152" text-anchor="middle" font-family="${FSTACK}" font-weight="bold"
    font-size="66" letter-spacing="1" fill="#${WHITE}">CM</text>
</svg>`;

(async () => {
  const mark = await svgPng(reticle(MOAWHANGO, RED, WHITE, BLACK));
  const markOnWhite = await svgPng(reticle(BLACK, RED, BLACK, null));
  const markReversed = await svgPng(reticle(WHITE, RED, WHITE, null));
  const crestPng = await svgPng(crest(), 700);

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
  s.addText("Concept board 3  ·  July 2026", { x: 5.7, y: 11.51, w: 2.07, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6, color: MOAWHANGO, margin: 0 });

  // header
  s.addImage({ path: LOGO, x: L, y: 0.34, w: 1.1, h: 0.266 });
  s.addText("CM RETICLE ROUNDEL — LOCKUP SYSTEM", {
    x: 1.85, y: 0.3, w: 5.92, h: 0.28, fontFace: F, fontSize: 15.5, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Brandmark, wordmark and tagline. Exploration only; no mark is endorsed. NZ Army wordmark remains the sole official logo.", {
    x: 1.85, y: 0.58, w: 5.92, h: 0.18, fontFace: F, fontSize: 8, italic: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addShape("line", { x: L, y: 0.9, w: W, h: 0, line: { color: BLACK, width: 1 } });

  function tileLabel(x, y, w, text, dark) {
    s.addText(text, { x, y, w, h: 0.18, fontFace: F, fontSize: 8, bold: true,
      color: dark ? MOAWHANGO : SWAMP, charSpacing: 1.5, align: "center",
      valign: "middle", margin: 0 });
  }

  // ---- row 1: primary horizontal lockup ----------------------------------
  s.addShape("rect", { x: L, y: 1.06, w: W, h: 2.0,
    fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
  s.addImage({ data: markOnWhite, x: 1.05, y: 1.4, w: 1.1, h: 1.1 });
  s.addText("COMBAT MINDSET", { x: 2.4, y: 1.44, w: 4.6, h: 0.5, fontFace: F,
    fontSize: 29, bold: true, color: BLACK, align: "left", valign: "middle",
    charSpacing: 0.5, margin: 0 });
  s.addShape("line", { x: 2.46, y: 2.02, w: 4.15, h: 0,
    line: { color: WAIOURU, width: 1 } });
  s.addText(TAG, { x: 2.4, y: 2.1, w: 4.6, h: 0.24, fontFace: F, fontSize: 10.5,
    bold: true, color: RED, charSpacing: 2, align: "left", valign: "middle", margin: 0 });
  tileLabel(L, 2.76, W, "PRIMARY LOCKUP — HORIZONTAL", false);

  // ---- row 2: stacked + reversed -----------------------------------------
  const GAP = 0.17, colW = (W - GAP) / 2;
  const R2 = 3.2, R2H = 2.5;
  // stacked
  s.addShape("rect", { x: L, y: R2, w: colW, h: R2H,
    fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
  s.addImage({ data: markOnWhite, x: L + colW / 2 - 0.55, y: R2 + 0.22, w: 1.1, h: 1.1 });
  s.addText("COMBAT MINDSET", { x: L + 0.1, y: R2 + 1.42, w: colW - 0.2, h: 0.32,
    fontFace: F, fontSize: 17.5, bold: true, color: BLACK, align: "center",
    valign: "middle", charSpacing: 0.5, margin: 0 });
  s.addText(TAG, { x: L + 0.1, y: R2 + 1.76, w: colW - 0.2, h: 0.2, fontFace: F,
    fontSize: 7.6, bold: true, color: RED, charSpacing: 1.5, align: "center",
    valign: "middle", margin: 0 });
  tileLabel(L, R2 + R2H - 0.28, colW, "STACKED — CENTRED", false);
  // reversed
  const RX = L + colW + GAP;
  s.addShape("rect", { x: RX, y: R2, w: colW, h: R2H, fill: { color: BLACK } });
  s.addImage({ data: markReversed, x: RX + colW / 2 - 0.55, y: R2 + 0.22, w: 1.1, h: 1.1 });
  s.addText("COMBAT MINDSET", { x: RX + 0.1, y: R2 + 1.42, w: colW - 0.2, h: 0.32,
    fontFace: F, fontSize: 17.5, bold: true, color: WHITE, align: "center",
    valign: "middle", charSpacing: 0.5, margin: 0 });
  s.addText(TAG, { x: RX + 0.1, y: R2 + 1.76, w: colW - 0.2, h: 0.2, fontFace: F,
    fontSize: 7.6, bold: true, color: RED, charSpacing: 1.5, align: "center",
    valign: "middle", margin: 0 });
  tileLabel(RX, R2 + R2H - 0.28, colW, "REVERSED", true);

  // ---- row 3: crest + compact in-line ------------------------------------
  const R3 = R2 + R2H + 0.17, R3H = 2.5;
  s.addShape("rect", { x: L, y: R3, w: colW, h: R3H,
    fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
  s.addImage({ data: crestPng, x: L + colW / 2 - 0.95, y: R3 + 0.18, w: 1.9, h: 1.9 });
  tileLabel(L, R3 + R3H - 0.28, colW, "CREST — PATCH AND COLOURS", false);

  s.addShape("rect", { x: RX, y: R3, w: colW, h: R3H,
    fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
  // footer-bar demo
  s.addShape("rect", { x: RX + 0.2, y: R3 + 0.35, w: colW - 0.4, h: 0.34,
    fill: { color: SWAMP } });
  s.addImage({ data: markReversed, x: RX + 0.3, y: R3 + 0.39, w: 0.26, h: 0.26 });
  s.addText([
    { text: "COMBAT MINDSET", options: { bold: true, color: WHITE, fontSize: 8 } },
    { text: "  ·  REMAIN EFFECTIVE. ACT DECISIVE.", options: { bold: true, color: MOAWHANGO, fontSize: 5.8, charSpacing: 0.5 } },
  ], { x: RX + 0.62, y: R3 + 0.35, w: colW - 0.9, h: 0.34, fontFace: F,
    align: "left", valign: "middle", margin: 0 });
  // document header demo
  s.addShape("rect", { x: RX + 0.2, y: R3 + 0.92, w: colW - 0.4, h: 0.34,
    fill: { color: WHITE }, line: { color: WAIOURU, width: 0.5 } });
  s.addImage({ data: markOnWhite, x: RX + 0.3, y: R3 + 0.96, w: 0.26, h: 0.26 });
  s.addText("COMBAT MINDSET", { x: RX + 0.62, y: R3 + 0.92, w: 2.2, h: 0.34,
    fontFace: F, fontSize: 9, bold: true, color: BLACK, align: "left",
    valign: "middle", margin: 0 });
  s.addText("course handbook", { x: RX + 0.62, y: R3 + 0.92, w: colW - 0.92, h: 0.34,
    fontFace: F, fontSize: 6.5, italic: true, color: BLACK, align: "right",
    valign: "middle", margin: 0 });
  // roundel-only demo
  s.addImage({ data: markOnWhite, x: RX + 0.2, y: R3 + 1.5, w: 0.55, h: 0.55 });
  s.addText("Roundel stands alone once the association is established — slide corners, coins, signage.", {
    x: RX + 0.9, y: R3 + 1.5, w: colW - 1.15, h: 0.55, fontFace: F, fontSize: 7.2,
    italic: true, color: BLACK, align: "left", valign: "middle", margin: 0 });
  tileLabel(RX, R3 + R3H - 0.28, colW, "COMPACT IN-LINE", false);

  // ---- row 4: in-situ mocks + usage notes --------------------------------
  const R4 = R3 + R3H + 0.17; // ≈ 8.54
  // cover mock
  s.addShape("rect", { x: L, y: R4, w: 1.5, h: 2.12,
    fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
  s.addImage({ path: LOGO, x: L + 0.12, y: R4 + 0.12, w: 0.45, h: 0.109 });
  s.addImage({ data: markOnWhite, x: L + 0.12, y: R4 + 0.5, w: 0.4, h: 0.4 });
  s.addText("COMBAT\nMINDSET", { x: L + 0.12, y: R4 + 0.94, w: 1.26, h: 0.4,
    fontFace: F, fontSize: 10.5, bold: true, color: BLACK, align: "left",
    valign: "top", margin: 0 });
  s.addText(TAG, { x: L + 0.12, y: R4 + 1.36, w: 1.3, h: 0.24, fontFace: F,
    fontSize: 4.6, bold: true, color: RED, charSpacing: 0.5, align: "left",
    valign: "top", margin: 0 });
  s.addShape("line", { x: L + 0.12, y: R4 + 1.72, w: 0.9, h: 0, line: { color: WAIOURU, width: 0.75 } });
  s.addShape("line", { x: L + 0.12, y: R4 + 1.84, w: 1.1, h: 0, line: { color: WAIOURU, width: 0.75 } });
  s.addText("cover", { x: L, y: R4 + 2.14, w: 1.5, h: 0.16, fontFace: F,
    fontSize: 6.8, italic: true, color: BLACK, align: "center", valign: "middle", margin: 0 });

  // slide mock
  s.addShape("rect", { x: 2.2, y: R4 + 0.3, w: 2.3, h: 1.3, fill: { color: SWAMP } });
  s.addImage({ data: markReversed, x: 2.35, y: R4 + 0.45, w: 0.34, h: 0.34 });
  s.addText("COMBAT MINDSET", { x: 2.78, y: R4 + 0.45, w: 1.7, h: 0.34,
    fontFace: F, fontSize: 9.5, bold: true, color: WHITE, align: "left",
    valign: "middle", margin: 0 });
  s.addShape("line", { x: 2.35, y: R4 + 0.92, w: 2.0, h: 0, line: { color: WAIOURU, width: 0.5 } });
  s.addShape("line", { x: 2.35, y: R4 + 1.08, w: 1.7, h: 0, line: { color: WAIOURU, width: 0.5 } });
  s.addShape("line", { x: 2.35, y: R4 + 1.24, w: 1.85, h: 0, line: { color: WAIOURU, width: 0.5 } });
  s.addText("slide master", { x: 2.2, y: R4 + 1.66, w: 2.3, h: 0.16, fontFace: F,
    fontSize: 6.8, italic: true, color: BLACK, align: "center", valign: "middle", margin: 0 });

  // usage notes
  const notes = [
    "Minimum sizes: roundel alone 8 mm; horizontal lockup 40 mm wide; crest 25 mm.",
    "Clear space around the mark equals one tick length on all sides.",
    "Tagline always set in Army Red, capitals, letterspaced; never reworded or split.",
    "Tagline as directed: “Remain Effective. Act Decisive.” The Way Forward suite currently uses “Act decisively” — confirm final form before rollout.",
    "Mark, wordmark and tagline remain subject to sponsor endorsement and Defence heraldry check.",
  ];
  s.addText(notes.map((t, i) => ({
    text: t, options: { bullet: { characterCode: "2022", indent: 8 },
      breakLine: i < notes.length - 1 },
  })), { x: 4.75, y: R4 + 0.05, w: 3.0, h: 2.2, fontFace: F, fontSize: 7.2,
    color: BLACK, align: "left", valign: "top", margin: 0, paraSpaceAfter: 5 });

  await pres.writeFile({ fileName: "output/combat-mindset-brandmark-6d.pptx" });
  console.log("written output/combat-mindset-brandmark-6d.pptx");
})();
