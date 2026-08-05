// COMBAT MINDSET : the mark, with a taiaha at the centre.
// Three arcs for the pressure that surrounds and the Prepare, Perform,
// Recover cycle; a solid core for self-command; a taiaha cut through it.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const GREY = "7F7F7F";
const F = "Arial";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function svgPng(body, px = 820) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">${body}</svg>`;
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

const P = (a, r) => [
  128 + r * Math.sin((a * Math.PI) / 180),
  128 - r * Math.cos((a * Math.PI) / 180),
];
const fmt = (p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`;

function ringSeg(a0, a1, R, r) {
  const large = a1 - a0 > 180 ? 1 : 0;
  return `M${fmt(P(a0, R))} A${R},${R} 0 ${large},1 ${fmt(P(a1, R))} ` +
    `L${fmt(P(a1, r))} A${r},${r} 0 ${large},0 ${fmt(P(a0, r))} Z`;
}
function arcs(R = 112, r = 92, gap = 22) {
  const span = 120 - gap;
  return [0, 120, 240].map((s) => ringSeg(s + gap / 2, s + gap / 2 + span, R, r)).join(" ");
}
const disc = (r, cx = 128, cy = 128) =>
  `M${(cx - r).toFixed(1)},${cy} A${r},${r} 0 1,0 ${(cx + r).toFixed(1)},${cy} ` +
  `A${r},${r} 0 1,0 ${(cx - r).toFixed(1)},${cy} Z`;

// ---- taiaha ---------------------------------------------------------------
// Right-hand profile, mirrored: arero (tongue), upoko (head), ate (shaft),
// rau (blade). Silhouette only, with no carving detail.
const TAIAHA_RIGHT = [
  [128, 22], [134, 46], [129, 58],
  [144, 72], [142, 92], [132, 104],
  [130.5, 112], [130.5, 150],
  [136, 176], [143, 204], [145, 222],
  [137, 238], [128, 246],
];
function taiaha(scale = 1, cy = 128) {
  const left = TAIAHA_RIGHT.slice(0, -1).reverse().map(([x, y]) => [256 - x, y]);
  const pts = [...TAIAHA_RIGHT, ...left].map(([x, y]) =>
    `${(128 + (x - 128) * scale).toFixed(1)},${(cy + (y - 134) * scale).toFixed(1)}`);
  return "M" + pts.join("L") + "Z";
}
// Just the head: arero and upoko, for the smallest applications.
function taiahaHead(scale = 1, cy = 128) {
  const head = TAIAHA_RIGHT.slice(0, 7).concat([[130.5, 112]]);
  const left = head.slice(0, -1).reverse().map(([x, y]) => [256 - x, y]);
  const pts = [...head, ...left].map(([x, y]) =>
    `${(128 + (x - 128) * scale).toFixed(1)},${(cy + (y - 66) * scale).toFixed(1)}`);
  return "M" + pts.join("L") + "Z";
}

const patchSolid =
  "M62,26 H194 A36,36 0 0 1 230,62 V194 A36,36 0 0 1 194,230 H62 " +
  "A36,36 0 0 1 26,194 V62 A36,36 0 0 1 62,26 Z";

const TS = 0.72, TCY = 122;

const heroMark = (ink, accent = true) => `
  <path d="${arcs()}" fill="#${ink}"/>
  <path d="${disc(66)} ${taiaha(TS, TCY)}" fill="#${ink}" fill-rule="evenodd"/>
  ${accent ? `<path d="${taiaha(TS, TCY)}" fill="#${RED}"/>` : ""}`;

const headMark = (ink, accent = true) => `
  <path d="${arcs()}" fill="#${ink}"/>
  <path d="${disc(66)} ${taiahaHead(1.34, 128)}" fill="#${ink}" fill-rule="evenodd"/>
  ${accent ? `<path d="${taiahaHead(1.34, 128)}" fill="#${RED}"/>` : ""}`;

(async () => {
  const I = {
    heroW: await svgPng(heroMark(WHITE)),
    heroS: await svgPng(heroMark(SWAMP)),
    heroMono: await svgPng(heroMark(WHITE, false)),
    headW: await svgPng(headMark(WHITE)),
    headS: await svgPng(headMark(SWAMP)),
    patch: await svgPng(
      `<path d="${patchSolid}" fill="#${WHITE}"/>
       <g transform="translate(128,128) scale(0.6) translate(-128,-128)">${heroMark(SWAMP)}</g>`),
  };

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "Combat Mindset Taiaha Mark";
  pres.company = "Army Command School";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W, MID = L + W / 2;

  s.addImage({ path: LOGO, x: L, y: 0.36, w: 1.72, h: 0.416 });
  s.addText("COMBAT MINDSET BRANDMARK", {
    x: L, y: 0.88, w: W, h: 0.4, fontFace: F, fontSize: 22, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("The taiaha at the centre", {
    x: L, y: 1.26, w: W, h: 0.22, fontFace: F, fontSize: 11,
    color: SWAMP, align: "left", valign: "middle", margin: 0 });
  s.addText("Army Command School", {
    x: L, y: 1.48, w: W - 1.6, h: 0.2, fontFace: F, fontSize: 8.5, italic: true,
    color: GREY, align: "left", valign: "middle", margin: 0 });
  s.addText("August 2026", { x: R - 1.6, y: 1.48, w: 1.6, h: 0.2, fontFace: F,
    fontSize: 8.5, color: GREY, align: "right", valign: "middle", margin: 0 });
  s.addShape("rect", { x: L, y: 1.74, w: W, h: 0.028, fill: { color: RED } });

  s.addText(
    "The taiaha is a stronger centre than a spearhead. It is a rangatira's weapon, carrying skill, discipline and " +
    "mana rather than force alone, and it already sits in NZ Army heraldry. It is drawn here in silhouette only: " +
    "arero, upoko, ate and rau, with no carving detail.",
    { x: L, y: 1.9, w: W, h: 0.5, fontFace: F, fontSize: 9, color: BLACK,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });

  // ---- hero ---------------------------------------------------------------
  s.addShape("rect", { x: L, y: 2.46, w: W, h: 2.8, fill: { color: BLACK } });
  s.addImage({ data: I.heroW, x: L + 0.42, y: 2.7, w: 2.32, h: 2.32 });

  const story = [
    ["Three arcs", "The pressure that surrounds, and the Prepare, Perform, Recover cycle."],
    ["A solid core", "Self-command. The centre holds while the environment does not."],
    ["The taiaha", "Trained, disciplined capability. Held ready, used decisively."],
  ];
  let sy = 2.94;
  story.forEach(([t, d]) => {
    s.addShape("rect", { x: L + 3.08, y: sy + 0.03, w: 0.05, h: 0.15, fill: { color: RED } });
    s.addText(t, { x: L + 3.24, y: sy, w: 2.2, h: 0.2, fontFace: F, fontSize: 9.4,
      bold: true, color: WHITE, align: "left", valign: "middle", margin: 0 });
    s.addText(d, { x: L + 3.24, y: sy + 0.2, w: W - 3.5, h: 0.4, fontFace: F,
      fontSize: 8.4, color: MOAWHANGO, align: "left", valign: "top", margin: 0,
      lineSpacingMultiple: 1.1 });
    sy += 0.7;
  });
  s.addText("See clearly.   Remain controlled.   Act decisively.", {
    x: L + 3.08, y: 4.94, w: W - 3.3, h: 0.22, fontFace: F, fontSize: 9.6,
    italic: true, color: WHITE, align: "left", valign: "middle", margin: 0 });

  // ---- applications -------------------------------------------------------
  s.addText("APPLICATIONS", { x: L, y: 5.4, w: W, h: 0.2, fontFace: F,
    fontSize: 7.6, bold: true, color: SWAMP, charSpacing: 1.4, align: "left",
    valign: "middle", margin: 0 });

  const AG = 0.14, AW = (W - 3 * AG) / 4, AH = 1.2;
  const apps = [
    [I.heroS, WHITE, "On white", 0.8],
    [I.heroMono, BLACK, "Single colour", 0.8],
    [I.patch, SWAMP, "In the patch", 0.8],
    [I.heroS, WHITE, "Reduced", 0.4],
  ];
  apps.forEach(([img, bg, cap, sz], i) => {
    const x = L + i * (AW + AG);
    s.addShape("rect", { x, y: 5.62, w: AW, h: AH, fill: { color: bg },
      line: bg === WHITE ? { color: MOAWHANGO, width: 1 } : undefined });
    s.addImage({ data: img, x: x + AW / 2 - sz / 2, y: 5.62 + 0.46 - sz / 2, w: sz, h: sz });
    s.addText(cap, { x, y: 5.62 + AH - 0.26, w: AW, h: 0.18, fontFace: F,
      fontSize: 6.6, color: bg === WHITE ? GREY : MOAWHANGO,
      align: "center", valign: "middle", margin: 0 });
  });

  // ---- size ladder --------------------------------------------------------
  s.addText("AT SIZE", { x: L, y: 6.96, w: W, h: 0.2, fontFace: F,
    fontSize: 7.6, bold: true, color: SWAMP, charSpacing: 1.4, align: "left",
    valign: "middle", margin: 0 });
  s.addShape("rect", { x: L, y: 7.18, w: W, h: 1.24, fill: { color: WHITE },
    line: { color: MOAWHANGO, width: 1 } });
  let sx = L + 1.0;
  [[0.88, "30 mm"], [0.58, "20 mm"], [0.35, "12 mm"], [0.2, "7 mm"]].forEach(([sz, cap]) => {
    s.addImage({ data: I.heroS, x: sx, y: 7.18 + 0.56 - sz / 2, w: sz, h: sz });
    s.addText(cap, { x: sx + sz / 2 - 0.35, y: 8.12, w: 0.7, h: 0.18, fontFace: F,
      fontSize: 6.6, color: GREY, align: "center", valign: "middle", margin: 0 });
    sx += sz + 0.54;
  });

  // ---- head variant -------------------------------------------------------
  s.addText("VARIANT: THE HEAD ALONE", { x: L, y: 8.6, w: W, h: 0.2, fontFace: F,
    fontSize: 7.6, bold: true, color: SWAMP, charSpacing: 1.4, align: "left",
    valign: "middle", margin: 0 });
  s.addShape("rect", { x: L, y: 8.82, w: 1.9, h: 1.28, fill: { color: BLACK } });
  s.addImage({ data: I.headW, x: L + 0.29, y: 8.98, w: 0.96, h: 0.96 });
  s.addShape("rect", { x: L + 2.04, y: 8.82, w: 1.9, h: 1.28, fill: { color: WHITE },
    line: { color: MOAWHANGO, width: 1 } });
  s.addImage({ data: I.headS, x: L + 2.62, y: 9.18, w: 0.74, h: 0.74 });
  s.addText(
    "The full taiaha carries more meaning, but its shaft is slim and the first thing to disappear when the mark is " +
    "reduced. Cutting the arero and upoko alone keeps the reference and gains weight. Worth holding as the small-size " +
    "variant if the full weapon proves too fine below about 12 mm.",
    { x: L + 4.1, y: 8.86, w: R - L - 4.1, h: 1.1, fontFace: F, fontSize: 8.4,
      color: BLACK, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });

  s.addText([
    { text: "Note.  ", options: { bold: true, color: SWAMP } },
    { text: "The taiaha already appears in NZ Army heraldry, so this draws on the Army's own device rather than " +
            "introducing new imagery. Even so, a mark that places a taiaha at its centre should be confirmed through " +
            "the appropriate cultural advice before it is adopted.",
      options: { color: BLACK } },
  ], { x: L, y: 10.26, w: W, h: 0.44, fontFace: F, fontSize: 8, align: "left",
       valign: "top", margin: 0, lineSpacingMultiple: 1.1 });

  await pres.writeFile({ fileName: "output/combat-mindset-brandmark-taiaha.pptx" });
  console.log("written output/combat-mindset-brandmark-taiaha.pptx");
})();
