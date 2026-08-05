// COMBAT MINDSET : brandmark exploration, round 2.
// Solid forms with the symbol knocked out, rather than outline drawing.
// The knockouts are genuine holes (evenodd fill), so the mark carries its
// weight on any background. Shown at three sizes to prove it holds.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const GREY = "7F7F7F";
const F = "Arial";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function svgPng(body, px = 720) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">${body}</svg>`;
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---- geometry as path data (so it can be combined for knockouts) ----------
function starPath(cx, cy, r) {
  const pts = [];
  for (let i = 0; i < 10; i++) {
    const rad = i % 2 === 0 ? r : r * 0.44;
    const a = (Math.PI / 5) * i - Math.PI / 2;
    pts.push(`${(cx + rad * Math.cos(a)).toFixed(1)},${(cy + rad * Math.sin(a)).toFixed(1)}`);
  }
  return "M" + pts.join("L") + "Z";
}

// Southern Cross, flag arrangement. Returns the three white stars and the
// leading star separately so the latter can be struck in red.
function crossParts(s = 1, dy = 0) {
  const P = (x, y, r) => starPath(128 + (x - 128) * s, 128 + (y - 128) * s + dy, r * s);
  return {
    field: [P(128, 48, 21), P(188, 112, 16), P(66, 138, 19)].join(" "),
    lead: P(128, 206, 25),
  };
}

const discPath = (r = 112) =>
  `M${128 - r},128 A${r},${r} 0 1,0 ${128 + r},128 A${r},${r} 0 1,0 ${128 - r},128 Z`;

const shieldSolid =
  "M128,20 L214,50 V126 C214,180 179,216 128,236 C77,216 42,180 42,126 V50 Z";

const patchSolid =
  "M62,26 H194 A36,36 0 0 1 230,62 V194 A36,36 0 0 1 194,230 H62 " +
  "A36,36 0 0 1 26,194 V62 A36,36 0 0 1 62,26 Z";

// Filled frond silhouette: serrated outline built from leaflet tips.
function fernPath() {
  const N = 13;
  const left = [], right = [];
  const lean = (u) => 128 + 9 * Math.sin(u * Math.PI * 0.9);   // frond curves, not a tree
  for (let i = 0; i < N; i++) {
    const t = i / (N - 1);
    const y = 208 - t * 156;
    const cx = lean(t);
    const len = 42 * Math.pow(1 - t, 0.62) + 4;
    const rise = len * 0.72;
    left.push([cx - len, y - rise]);
    right.push([cx + len, y - rise]);
    if (i < N - 1) {
      const t2 = (i + 0.5) / (N - 1);
      const y2 = 208 - t2 * 156;
      left.push([lean(t2) - 7, y2]);
      right.push([lean(t2) + 7, y2]);
    }
  }
  const fmt = (p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`;
  return `M${lean(0).toFixed(1)},214 L` + left.map(fmt).join("L") +
    ` L${lean(1).toFixed(1)},44 L` + right.reverse().map(fmt).join("L") + " Z";
}

// ---- the four options -----------------------------------------------------
const OPTIONS = [
  {
    key: "A",
    name: "ROUNDEL",
    why: "The disc carries the weight; the cross is cut out of it. Holds at any size.",
    mark: (ink) => {
      const c = crossParts(0.8);
      return `<path d="${discPath(112)} ${c.field} ${c.lead}" fill="#${ink}" fill-rule="evenodd"/>
        <path d="${c.lead}" fill="#${RED}"/>`;
    },
  },
  {
    key: "B",
    name: "SHIELD",
    why: "Keeps the protection of the shield, with the national reference cut into it.",
    mark: (ink) => {
      const c = crossParts(0.55, 10);
      return `<path d="${shieldSolid} ${c.field} ${c.lead}" fill="#${ink}" fill-rule="evenodd"/>
        <path d="${c.lead}" fill="#${RED}"/>`;
    },
  },
  {
    key: "C",
    name: "FERN",
    why: "A solid frond, and the only option carrying no red. The quietest of the four.",
    mark: (ink) =>
      `<path d="${discPath(112)} ${fernPath()}" fill="#${ink}" fill-rule="evenodd"/>`,
  },
  {
    key: "D",
    name: "PATCH",
    why: "Unit-patch geometry. The heaviest of the four and the most at home on cloth.",
    mark: (ink) => {
      const c = crossParts(0.72);
      return `<path d="${patchSolid} ${c.field} ${c.lead}" fill="#${ink}" fill-rule="evenodd"/>
        <path d="${c.lead}" fill="#${RED}"/>`;
    },
  },
];

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "Combat Mindset Brandmark Options 2";
  pres.company = "Army Command School";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W;

  // ---- header -------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.36, w: 1.72, h: 0.416 });
  s.addText("COMBAT MINDSET BRANDMARK", {
    x: L, y: 0.88, w: W, h: 0.4, fontFace: F, fontSize: 22, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Solid forms, round 2", {
    x: L, y: 1.26, w: W, h: 0.22, fontFace: F, fontSize: 11,
    color: SWAMP, align: "left", valign: "middle", margin: 0 });
  s.addText("Army Command School", {
    x: L, y: 1.48, w: W - 1.6, h: 0.2, fontFace: F, fontSize: 8.5, italic: true,
    color: GREY, align: "left", valign: "middle", margin: 0 });
  s.addText("August 2026", { x: R - 1.6, y: 1.48, w: 1.6, h: 0.2, fontFace: F,
    fontSize: 8.5, color: GREY, align: "right", valign: "middle", margin: 0 });
  s.addShape("rect", { x: L, y: 1.74, w: W, h: 0.028, fill: { color: RED } });

  s.addText(
    "Round one drew the marks as outlines, which read thin. These are solid forms with the symbol cut out of them, " +
    "so the mass carries the weight and the detail is subtractive. The centre column shows each mark at document, " +
    "slide and favicon size; a mark that survives the smallest of these is the one worth building.",
    { x: L, y: 1.9, w: W, h: 0.52, fontFace: F, fontSize: 9, color: BLACK,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });

  const GAP = 0.14, CW = (W - 2 * GAP) / 3;
  ["BRANDMARK", "AT SIZE", "LOCKUP"].forEach((t, i) => {
    s.addText(t, { x: L + i * (CW + GAP), y: 2.5, w: CW, h: 0.18, fontFace: F,
      fontSize: 7.6, bold: true, color: SWAMP, charSpacing: 1.4,
      align: "center", valign: "middle", margin: 0 });
  });

  let y = 2.72;
  for (const opt of OPTIONS) {
    const white = await svgPng(opt.mark(WHITE));
    const swamp = await svgPng(opt.mark(SWAMP));

    s.addText([
      { text: `${opt.key}    ${opt.name}`, options: { bold: true, color: SWAMP, charSpacing: 1.6 } },
      { text: `    ${opt.why}`, options: { italic: true, color: BLACK, fontSize: 7.6 } },
    ], { x: L, y, w: W, h: 0.3, fontFace: F, fontSize: 9.4, align: "left",
      valign: "middle", margin: 0 });

    const ty = y + 0.3, TH = 1.44;

    // brandmark, reversed out of black
    s.addShape("rect", { x: L, y: ty, w: CW, h: TH, fill: { color: BLACK } });
    s.addImage({ data: white, x: L + CW / 2 - 0.52, y: ty + 0.2, w: 1.04, h: 1.04 });

    // size ladder on white
    const mx = L + CW + GAP;
    s.addShape("rect", { x: mx, y: ty, w: CW, h: TH, fill: { color: WHITE },
      line: { color: MOAWHANGO, width: 1 } });
    const sizes = [0.74, 0.42, 0.22];
    let sx = mx + 0.26;
    sizes.forEach((sz) => {
      s.addImage({ data: swamp, x: sx, y: ty + TH / 2 - sz / 2 - 0.06, w: sz, h: sz });
      sx += sz + 0.2;
    });
    s.addText("24 mm        14 mm        7 mm", { x: mx, y: ty + TH - 0.28, w: CW, h: 0.18,
      fontFace: F, fontSize: 6.4, color: GREY, align: "center", valign: "middle", margin: 0 });

    // lockup on swamp
    const lx = L + 2 * (CW + GAP);
    s.addShape("rect", { x: lx, y: ty, w: CW, h: TH, fill: { color: SWAMP } });
    s.addImage({ data: white, x: lx + 0.2, y: ty + TH / 2 - 0.35, w: 0.7, h: 0.7 });
    s.addText("COMBAT", { x: lx + 0.98, y: ty + TH / 2 - 0.25, w: CW - 1.1, h: 0.2,
      fontFace: F, fontSize: 11.5, bold: true, color: WHITE, charSpacing: 2.2,
      align: "left", valign: "middle", margin: 0 });
    s.addText("MINDSET", { x: lx + 0.98, y: ty + TH / 2 - 0.05, w: CW - 1.1, h: 0.2,
      fontFace: F, fontSize: 11.5, bold: true, color: WHITE, charSpacing: 2.2,
      align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: lx + 0.98, y: ty + TH / 2 + 0.19, w: 0.5, h: 0.022,
      fill: { color: RED } });

    y += 0.3 + TH + 0.22;
  }

  s.addText([
    { text: "Note.  ", options: { bold: true, color: SWAMP } },
    { text: "In the three cross options the leading star is struck in red. It is the only colour in the mark, it sits at " +
            "the point of the cross, and it carries the accent through to the tagline.",
      options: { color: BLACK } },
  ], { x: L, y: y + 0.04, w: W, h: 0.4, fontFace: F, fontSize: 8, align: "left",
       valign: "top", margin: 0, lineSpacingMultiple: 1.1 });

  await pres.writeFile({ fileName: "output/combat-mindset-brandmark-solid.pptx" });
  console.log("written output/combat-mindset-brandmark-solid.pptx");
})();
