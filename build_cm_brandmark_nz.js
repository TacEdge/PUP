// COMBAT MINDSET : brandmark exploration, NZ-referencing options.
// Each option is shown three ways: brandmark (symbol alone), wordmark
// (type alone) and lockup (the two combined for document use).

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const GREY = "7F7F7F";
const F = "Arial";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function svgPng(body, px = 640) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">${body}</svg>`;
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---- primitives -----------------------------------------------------------
function star5(cx, cy, r, fill) {
  const pts = [];
  for (let i = 0; i < 10; i++) {
    const rad = i % 2 === 0 ? r : r * 0.42;
    const a = (Math.PI / 5) * i - Math.PI / 2;
    pts.push(`${(cx + rad * Math.cos(a)).toFixed(1)},${(cy + rad * Math.sin(a)).toFixed(1)}`);
  }
  return `<polygon points="${pts.join(" ")}" fill="#${fill}"/>`;
}

// Southern Cross in the flag arrangement, scaled about (128,128).
function southernCross(ink, accent, s = 1, dx = 0, dy = 0) {
  const P = (x, y, r, c) => star5(128 + (x - 128) * s + dx, 128 + (y - 128) * s + dy, r * s, c);
  return [
    P(128, 50, 20, ink),    // Gamma, top
    P(186, 112, 16, ink),   // Delta, right
    P(68, 136, 19, ink),    // Beta, left
    P(128, 204, 24, accent) // Alpha, bottom
  ].join("");
}

const shieldPath = (ink, w = 11) => `
  <path d="M128,30 L206,56 V128 C206,178 174,210 128,228 C82,210 50,178 50,128 V56 Z"
    fill="none" stroke="#${ink}" stroke-width="${w}" stroke-linejoin="round"/>`;

function fernFrond(ink, accent) {
  const N = 11;
  let s = `<path d="M128,222 C121,168 126,102 128,44" stroke="#${ink}"
    stroke-width="8" fill="none" stroke-linecap="round"/>`;
  for (let i = 0; i < N; i++) {
    const t = i / (N - 1);
    const y = 206 - t * 152;
    const x = 128 - 5 * Math.sin(t * Math.PI);
    const len = 62 * Math.pow(1 - t, 0.75) + 7;
    const rise = len * 0.66;
    const w = (7.5 - t * 3.4).toFixed(1);
    const c = t > 0.92 ? accent : ink;
    const P = (sx) => `<path d="M${x.toFixed(0)},${y.toFixed(0)}
      Q${(x + sx * len * 0.5).toFixed(0)},${(y - rise * 0.18).toFixed(0)}
      ${(x + sx * len).toFixed(0)},${(y - rise).toFixed(0)}"
      stroke="#${c}" stroke-width="${w}" fill="none" stroke-linecap="round"/>`;
    s += P(-1) + P(1);
  }
  return s;
}

function reticle(ink, r = 98, w = 7) {
  const tick = (a) => {
    const rad = (a * Math.PI) / 180;
    const x1 = 128 + (r - 16) * Math.sin(rad), y1 = 128 - (r - 16) * Math.cos(rad);
    const x2 = 128 + (r + 14) * Math.sin(rad), y2 = 128 - (r + 14) * Math.cos(rad);
    return `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}"
      stroke="#${ink}" stroke-width="${w}" stroke-linecap="round"/>`;
  };
  return `<circle cx="128" cy="128" r="${r}" fill="none" stroke="#${ink}" stroke-width="${w}"/>
    ${[0, 90, 180, 270].map(tick).join("")}`;
}

// ---- the four options -----------------------------------------------------
const OPTIONS = [
  {
    key: "A",
    name: "SOUTHERN CROSS",
    why: "Secular, already on the flag and NZDF insignia, and legible at badge size.",
    mark: (ink, accent) => `
      <circle cx="128" cy="128" r="104" fill="none" stroke="#${ink}" stroke-width="8"/>
      ${southernCross(ink, accent, 0.84)}`,
  },
  {
    key: "B",
    name: "CROSS AND SHIELD",
    why: "Keeps the shield's protection and adds the national reference inside it.",
    mark: (ink, accent) => `
      ${shieldPath(ink, 11)}
      ${southernCross(ink, accent, 0.58, 0, 6)}`,
  },
  {
    key: "C",
    name: "FERN",
    why: "Read as New Zealand anywhere. The red tip keeps the mark directional.",
    mark: (ink, accent) => `
      <circle cx="128" cy="128" r="104" fill="none" stroke="#${ink}" stroke-width="8"/>
      <g transform="translate(128 128) scale(0.82) translate(-128 -128)">${fernFrond(ink, accent)}</g>`,
  },
  {
    key: "D",
    name: "CROSS PATCH",
    why: "The reticle patch language, with the Southern Cross at the aim point.",
    mark: (ink, accent) => `
      ${reticle(ink, 98, 7)}
      ${southernCross(ink, accent, 0.64)}`,
  },
];

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "Combat Mindset Brandmark Options";
  pres.company = "Army Command School";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W;

  // ---- header -------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.36, w: 1.72, h: 0.416 });
  s.addText("COMBAT MINDSET BRANDMARK", {
    x: L, y: 0.88, w: W, h: 0.4, fontFace: F, fontSize: 22, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("New Zealand referencing options", {
    x: L, y: 1.26, w: W, h: 0.22, fontFace: F, fontSize: 11,
    color: SWAMP, align: "left", valign: "middle", margin: 0 });
  s.addText("Army Command School", {
    x: L, y: 1.48, w: W - 1.6, h: 0.2, fontFace: F, fontSize: 8.5, italic: true,
    color: GREY, align: "left", valign: "middle", margin: 0 });
  s.addText("August 2026", { x: R - 1.6, y: 1.48, w: 1.6, h: 0.2, fontFace: F,
    fontSize: 8.5, color: GREY, align: "right", valign: "middle", margin: 0 });
  s.addShape("rect", { x: L, y: 1.74, w: W, h: 0.028, fill: { color: RED } });

  s.addText(
    "Each option is drawn three ways. The brandmark is the symbol alone, for patches, favicons and small applications. " +
    "The wordmark is the type alone, where a symbol would compete with the NZ Army logo. The lockup is the pair set " +
    "together, and is what would sit in document headers and on slides.",
    { x: L, y: 1.9, w: W, h: 0.52, fontFace: F, fontSize: 9, color: BLACK,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });

  // ---- column headings ----------------------------------------------------
  const GAP = 0.14, CW = (W - 2 * GAP) / 3;
  ["BRANDMARK", "WORDMARK", "LOCKUP"].forEach((t, i) => {
    s.addText(t, { x: L + i * (CW + GAP), y: 2.5, w: CW, h: 0.18, fontFace: F,
      fontSize: 7.6, bold: true, color: SWAMP, charSpacing: 1.4,
      align: "center", valign: "middle", margin: 0 });
  });

  // ---- wordmark drawn with type ------------------------------------------
  function wordmark(x, y, w, h, ink, rule, scale = 1) {
    s.addText("COMBAT", { x, y: y + h / 2 - 0.30 * scale, w, h: 0.24 * scale,
      fontFace: F, fontSize: 17 * scale, bold: true, color: ink,
      charSpacing: 3.4 * scale, align: "center", valign: "middle", margin: 0 });
    s.addText("MINDSET", { x, y: y + h / 2 - 0.06 * scale, w, h: 0.24 * scale,
      fontFace: F, fontSize: 17 * scale, bold: true, color: ink,
      charSpacing: 3.4 * scale, align: "center", valign: "middle", margin: 0 });
    s.addShape("rect", { x: x + w / 2 - 0.42 * scale, y: y + h / 2 + 0.25 * scale,
      w: 0.84 * scale, h: 0.026 * scale, fill: { color: rule } });
  }

  // ---- option rows --------------------------------------------------------
  let y = 2.72;
  for (const opt of OPTIONS) {
    const inkMark = await svgPng(opt.mark(WHITE, RED));
    const inkDark = await svgPng(opt.mark(SWAMP, RED));

    s.addText([
      { text: `${opt.key}    ${opt.name}`, options: { bold: true, color: SWAMP, charSpacing: 1.6 } },
      { text: `    ${opt.why}`, options: { italic: true, color: BLACK, fontSize: 7.6 } },
    ], { x: L, y, w: W, h: 0.3, fontFace: F, fontSize: 9.4, align: "left",
      valign: "middle", margin: 0 });

    const ty = y + 0.3, TH = 1.44;

    // brandmark, reversed out of black
    s.addShape("rect", { x: L, y: ty, w: CW, h: TH, fill: { color: BLACK } });
    s.addImage({ data: inkMark, x: L + CW / 2 - 0.5, y: ty + 0.22, w: 1.0, h: 1.0 });

    // wordmark on white
    const wx = L + CW + GAP;
    s.addShape("rect", { x: wx, y: ty, w: CW, h: TH, fill: { color: WHITE },
      line: { color: MOAWHANGO, width: 1 } });
    wordmark(wx, ty, CW, TH, SWAMP, RED, 1);

    // lockup on swamp
    const lx = L + 2 * (CW + GAP);
    s.addShape("rect", { x: lx, y: ty, w: CW, h: TH, fill: { color: SWAMP } });
    s.addImage({ data: inkMark, x: lx + 0.2, y: ty + TH / 2 - 0.34, w: 0.68, h: 0.68 });
    s.addText("COMBAT", { x: lx + 0.94, y: ty + TH / 2 - 0.24, w: CW - 1.06, h: 0.2,
      fontFace: F, fontSize: 11.5, bold: true, color: WHITE, charSpacing: 2.2,
      align: "left", valign: "middle", margin: 0 });
    s.addText("MINDSET", { x: lx + 0.94, y: ty + TH / 2 - 0.04, w: CW - 1.06, h: 0.2,
      fontFace: F, fontSize: 11.5, bold: true, color: WHITE, charSpacing: 2.2,
      align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: lx + 0.94, y: ty + TH / 2 + 0.19, w: 0.5, h: 0.022,
      fill: { color: RED } });

    y += 0.3 + TH + 0.22;
  }

  // ---- note ---------------------------------------------------------------
  s.addText([
    { text: "Note.  ", options: { bold: true, color: SWAMP } },
    { text: "All four use national rather than iwi-specific imagery, so none carries a cultural-consultation " +
            "requirement of itself. Any final mark should still be cleared through NZDF visual identity, and any " +
            "later introduction of Māori design elements would require appropriate cultural consultation.",
      options: { color: BLACK } },
  ], { x: L, y: y + 0.04, w: W, h: 0.44, fontFace: F, fontSize: 8, align: "left",
       valign: "top", margin: 0, lineSpacingMultiple: 1.1 });

  await pres.writeFile({ fileName: "output/combat-mindset-brandmark-nz.pptx" });
  console.log("written output/combat-mindset-brandmark-nz.pptx");
})();
