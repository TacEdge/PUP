// COMBAT MINDSET : the patch, with the NZ Army fern.
// The interior is the fern device from the NZ Army logo, traced as a fan of
// tapering pinnae along a curving frond, and cut out of the solid patch.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const GREY = "7F7F7F";
const F = "Arial";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function svgPng(body, px = 800) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">${body}</svg>`;
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---- the NZ Army fern, traced from the logo -------------------------------
const AXIS = { P0: [62, 212], P1: [126, 156], P2: [188, 124], P3: [180, 44] };

function bez(t) {
  const { P0, P1, P2, P3 } = AXIS, u = 1 - t;
  return [
    u*u*u*P0[0] + 3*u*u*t*P1[0] + 3*u*t*t*P2[0] + t*t*t*P3[0],
    u*u*u*P0[1] + 3*u*u*t*P1[1] + 3*u*t*t*P2[1] + t*t*t*P3[1],
  ];
}
function dbez(t) {
  const { P0, P1, P2, P3 } = AXIS, u = 1 - t;
  return [
    3*u*u*(P1[0]-P0[0]) + 6*u*t*(P2[0]-P1[0]) + 3*t*t*(P3[0]-P2[0]),
    3*u*u*(P1[1]-P0[1]) + 6*u*t*(P2[1]-P1[1]) + 3*t*t*(P3[1]-P2[1]),
  ];
}

// Each pinna as a closed quad, so it can serve as a knockout.
function pinnae({ N = 15, L0 = 54, LP = 0.68, W0 = 8, WP = 0.5 } = {}) {
  const out = [];
  for (let i = 0; i < N; i++) {
    const t = i / (N - 1);
    const a = bez(t);
    let [tx, ty] = dbez(t);
    const m = Math.hypot(tx, ty); tx /= m; ty /= m;
    const nx = ty, ny = -tx;                       // outward, up and left
    const L = L0 * Math.pow(1 - t, LP) + 7;
    const w = (W0 * Math.pow(1 - t, WP) + 2.6) / 2;
    const b = [a[0] + nx * L, a[1] + ny * L];
    const px = -ny * w, py = nx * w;               // half-width across the pinna
    const P = (p, sx) => `${(p[0] + sx * px).toFixed(1)},${(p[1] + sx * py).toFixed(1)}`;
    out.push(`M${P(a, 1)}L${P(b, 1)}L${P(b, -1)}L${P(a, -1)}Z`);
  }
  return out;
}

// Fern centred and scaled into the 256 box.
function fernGroup(inner, scale = 0.68) {
  return `<g transform="translate(128,128) scale(${scale}) translate(-112,-128)">${inner}</g>`;
}

const patchSolid =
  "M62,26 H194 A36,36 0 0 1 230,62 V194 A36,36 0 0 1 194,230 H62 " +
  "A36,36 0 0 1 26,194 V62 A36,36 0 0 1 62,26 Z";

const discPath = (r = 112) =>
  `M${128 - r},128 A${r},${r} 0 1,0 ${128 + r},128 A${r},${r} 0 1,0 ${128 - r},128 Z`;

// leading pinnae struck in red
const LEAD = 2;

function markPatch(ink, { accent = true, container = patchSolid } = {}) {
  const q = pinnae();
  const lead = q.slice(-LEAD).join(" ");
  const rest = q.slice(0, -LEAD).join(" ");
  const holes = fernGroup(rest + " " + lead);
  return `<path d="${container}" fill="#${ink}"/>
    <mask id="m"><rect width="256" height="256" fill="#fff"/>
      ${fernGroup(`<path d="${rest} ${lead}" fill="#000"/>`)}</mask>
    <path d="${container}" fill="#${ink}" mask="url(#m)"/>
    ${accent ? fernGroup(`<path d="${lead}" fill="#${RED}"/>`) : ""}`;
}

// Knockout version: genuine holes so the background reads through.
function markKnockout(ink, { accent = true, container = patchSolid } = {}) {
  const q = pinnae();
  const lead = q.slice(-LEAD);
  const rest = q.slice(0, -LEAD);
  const all = [...rest, ...lead].join(" ");
  const scaled = (d) =>
    `<g transform="translate(128,128) scale(0.68) translate(-112,-128)">${d}</g>`;
  return `
    <defs><clipPath id="c"><path d="${container}"/></clipPath></defs>
    <path d="${container}" fill="#${ink}"/>
    <g clip-path="url(#c)">
      ${scaled(`<path d="${all}" fill="#000" fill-opacity="0"/>`)}
    </g>
    ${scaled(`<path d="${rest.join(" ")}" fill="none"/>`)}`;
}

(async () => {
  // solid patch with the fern cut out, as a single evenodd path
  const q = pinnae();
  const leadD = q.slice(-LEAD).join(" ");
  const restD = q.slice(0, -LEAD).join(" ");

  // pre-transform the pinnae: centre on their own bounding box and scale to fill
  const nums = (d) => {
    const out = [];
    d.replace(/(-?\d+\.?\d*),(-?\d+\.?\d*)/g, (_, x, y) => {
      out.push([parseFloat(x), parseFloat(y)]); return _;
    });
    return out;
  };
  const allPts = nums(q.join(" "));
  const xs = allPts.map((p) => p[0]), ys = allPts.map((p) => p[1]);
  const bb = { x0: Math.min(...xs), x1: Math.max(...xs), y0: Math.min(...ys), y1: Math.max(...ys) };
  const cx = (bb.x0 + bb.x1) / 2, cy = (bb.y0 + bb.y1) / 2;
  const TARGET = 156;                       // across the patch interior
  const sc = TARGET / Math.max(bb.x1 - bb.x0, bb.y1 - bb.y0);

  function xf(d) {
    return d.replace(/(-?\d+\.?\d*),(-?\d+\.?\d*)/g, (_, x, y) =>
      `${(128 + (parseFloat(x) - cx) * sc).toFixed(1)},${(128 + (parseFloat(y) - cy) * sc).toFixed(1)}`);
  }
  const restX = xf(restD), leadX = xf(leadD);

  const mark = (ink, container, accent = true) =>
    `<path d="${container} ${restX} ${leadX}" fill="#${ink}" fill-rule="evenodd"/>` +
    (accent ? `<path d="${leadX}" fill="#${RED}"/>` : "");

  const I = {
    patchW: await svgPng(mark(WHITE, patchSolid)),
    patchS: await svgPng(mark(SWAMP, patchSolid)),
    patchMono: await svgPng(mark(WHITE, patchSolid, false)),
    patchRed: await svgPng(mark(RED, patchSolid, false)),
    discW: await svgPng(mark(WHITE, discPath(112))),
  };

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "Combat Mindset Patch";
  pres.company = "Army Command School";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W, MID = L + W / 2;

  s.addImage({ path: LOGO, x: L, y: 0.36, w: 1.72, h: 0.416 });
  s.addText("COMBAT MINDSET PATCH", {
    x: L, y: 0.88, w: W, h: 0.4, fontFace: F, fontSize: 22, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("The NZ Army fern, cut into the patch", {
    x: L, y: 1.26, w: W, h: 0.22, fontFace: F, fontSize: 11,
    color: SWAMP, align: "left", valign: "middle", margin: 0 });
  s.addText("Army Command School", {
    x: L, y: 1.48, w: W - 1.6, h: 0.2, fontFace: F, fontSize: 8.5, italic: true,
    color: GREY, align: "left", valign: "middle", margin: 0 });
  s.addText("August 2026", { x: R - 1.6, y: 1.48, w: 1.6, h: 0.2, fontFace: F,
    fontSize: 8.5, color: GREY, align: "right", valign: "middle", margin: 0 });
  s.addShape("rect", { x: L, y: 1.74, w: W, h: 0.028, fill: { color: RED } });

  s.addText(
    "The interior is the fern from the NZ Army logo, traced as a fan of tapering pinnae along a curving frond and " +
    "cut out of the solid patch. Nothing is invented: the mark borrows the Army's own device and gives it the patch " +
    "geometry. The leading pinnae are struck in red, the single accent in the mark.",
    { x: L, y: 1.9, w: W, h: 0.52, fontFace: F, fontSize: 9, color: BLACK,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });

  // ---- hero ---------------------------------------------------------------
  s.addShape("rect", { x: L, y: 2.5, w: W, h: 2.5, fill: { color: BLACK } });
  s.addImage({ data: I.patchW, x: MID - 1.05, y: 2.72, w: 2.1, h: 2.1 });

  // ---- treatments ---------------------------------------------------------
  s.addText("TREATMENTS", { x: L, y: 5.14, w: W, h: 0.2, fontFace: F,
    fontSize: 7.6, bold: true, color: SWAMP, charSpacing: 1.4,
    align: "left", valign: "middle", margin: 0 });

  const TG = 0.14, TW = (W - 3 * TG) / 4, TH = 1.26;
  const treatments = [
    [I.patchS, WHITE, "On white"],
    [I.patchW, SWAMP, "On Swamp Green"],
    [I.patchMono, BLACK, "Single colour"],
    [I.patchRed, WHITE, "Army Red"],
  ];
  treatments.forEach(([img, bg, cap], i) => {
    const x = L + i * (TW + TG);
    s.addShape("rect", { x, y: 5.36, w: TW, h: TH, fill: { color: bg },
      line: bg === WHITE ? { color: MOAWHANGO, width: 1 } : undefined });
    s.addImage({ data: img, x: x + TW / 2 - 0.42, y: 5.5, w: 0.84, h: 0.84 });
    s.addText(cap, { x, y: 5.36 + TH - 0.28, w: TW, h: 0.18, fontFace: F,
      fontSize: 6.6, color: bg === WHITE ? GREY : MOAWHANGO,
      align: "center", valign: "middle", margin: 0 });
  });

  // ---- at size ------------------------------------------------------------
  s.addText("AT SIZE", { x: L, y: 6.84, w: W, h: 0.2, fontFace: F,
    fontSize: 7.6, bold: true, color: SWAMP, charSpacing: 1.4,
    align: "left", valign: "middle", margin: 0 });
  s.addShape("rect", { x: L, y: 7.06, w: W, h: 1.26, fill: { color: WHITE },
    line: { color: MOAWHANGO, width: 1 } });
  const sizes = [[0.9, "30 mm"], [0.6, "20 mm"], [0.36, "12 mm"], [0.21, "7 mm"]];
  let sx = L + 1.05;
  sizes.forEach(([sz, cap]) => {
    s.addImage({ data: I.patchS, x: sx, y: 7.06 + 0.58 - sz / 2, w: sz, h: sz });
    s.addText(cap, { x: sx + sz / 2 - 0.35, y: 8.02, w: 0.7, h: 0.18, fontFace: F,
      fontSize: 6.6, color: GREY, align: "center", valign: "middle", margin: 0 });
    sx += sz + 0.52;
  });

  // ---- lockups ------------------------------------------------------------
  s.addText("LOCKUP", { x: L, y: 8.5, w: W, h: 0.2, fontFace: F,
    fontSize: 7.6, bold: true, color: SWAMP, charSpacing: 1.4,
    align: "left", valign: "middle", margin: 0 });

  const LG = 0.16, LW = (W - LG) / 2, LH = 1.5;
  // horizontal
  s.addShape("rect", { x: L, y: 8.72, w: LW, h: LH, fill: { color: SWAMP } });
  s.addImage({ data: I.patchW, x: L + 0.3, y: 8.72 + LH / 2 - 0.42, w: 0.84, h: 0.84 });
  s.addText("COMBAT", { x: L + 1.26, y: 8.72 + LH / 2 - 0.3, w: LW - 1.4, h: 0.24,
    fontFace: F, fontSize: 14, bold: true, color: WHITE, charSpacing: 2.6,
    align: "left", valign: "middle", margin: 0 });
  s.addText("MINDSET", { x: L + 1.26, y: 8.72 + LH / 2 - 0.06, w: LW - 1.4, h: 0.24,
    fontFace: F, fontSize: 14, bold: true, color: WHITE, charSpacing: 2.6,
    align: "left", valign: "middle", margin: 0 });
  s.addShape("rect", { x: L + 1.26, y: 8.72 + LH / 2 + 0.22, w: 0.6, h: 0.024,
    fill: { color: RED } });
  s.addText("Horizontal, for document headers", { x: L, y: 8.72 + LH - 0.26, w: LW,
    h: 0.18, fontFace: F, fontSize: 6.6, color: MOAWHANGO, align: "center",
    valign: "middle", margin: 0 });

  // stacked
  const bx = L + LW + LG;
  s.addShape("rect", { x: bx, y: 8.72, w: LW, h: LH, fill: { color: BLACK } });
  s.addImage({ data: I.patchW, x: bx + LW / 2 - 0.36, y: 8.86, w: 0.72, h: 0.72 });
  s.addText("COMBAT  MINDSET", { x: bx, y: 9.64, w: LW, h: 0.24, fontFace: F,
    fontSize: 11.5, bold: true, color: WHITE, charSpacing: 2.6,
    align: "center", valign: "middle", margin: 0 });
  s.addShape("rect", { x: bx + LW / 2 - 0.3, y: 9.9, w: 0.6, h: 0.024, fill: { color: RED } });
  s.addText("Stacked, for covers and slides", { x: bx, y: 8.72 + LH - 0.26, w: LW,
    h: 0.18, fontFace: F, fontSize: 6.6, color: MOAWHANGO, align: "center",
    valign: "middle", margin: 0 });

  s.addText([
    { text: "Note.  ", options: { bold: true, color: SWAMP } },
    { text: "The fern here is a trace, close enough to judge the direction. If this is the mark, the final artwork " +
            "should take the fern outline from the NZ Army master files rather than a redraw, so the two devices " +
            "match exactly wherever they appear together.",
      options: { color: BLACK } },
  ], { x: L, y: 10.36, w: W, h: 0.44, fontFace: F, fontSize: 8, align: "left",
       valign: "top", margin: 0, lineSpacingMultiple: 1.1 });

  await pres.writeFile({ fileName: "output/combat-mindset-patch-fern.pptx" });
  console.log("written output/combat-mindset-patch-fern.pptx");
})();
