// COMBAT MINDSET — emblem concepts (A4 portrait)
// Five candidate emblems, the compass family (option 1 developed across
// Combat Mindset, Performance Under Pressure and the Framework), and the
// family shown in situ on the three banners. Concept only.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const F = "Arial";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function svgPng(svg, px = 600) {
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// kite-shaped compass point
function kite(angleDeg, tipR, shoulderR, halfW, fill) {
  const a = (angleDeg * Math.PI) / 180;
  const dx = Math.sin(a), dy = -Math.cos(a);
  const px = -dy, py = dx;
  const cx = 128, cy = 128;
  const tip = `${(cx + tipR * dx).toFixed(1)},${(cy + tipR * dy).toFixed(1)}`;
  const s1 = `${(cx + shoulderR * dx + halfW * px).toFixed(1)},${(cy + shoulderR * dy + halfW * py).toFixed(1)}`;
  const s2 = `${(cx + shoulderR * dx - halfW * px).toFixed(1)},${(cy + shoulderR * dy - halfW * py).toFixed(1)}`;
  return `<polygon points="${tip} ${s1} ${cx},${cy} ${s2}" fill="#${fill}"/>`;
}

function arc(r, a0, a1, ink, w) {
  const rad = (d) => (d * Math.PI) / 180;
  const x0 = 128 + r * Math.sin(rad(a0)), y0 = 128 - r * Math.cos(rad(a0));
  const x1 = 128 + r * Math.sin(rad(a1)), y1 = 128 - r * Math.cos(rad(a1));
  const large = a1 - a0 > 180 ? 1 : 0;
  return `<path d="M ${x0.toFixed(1)},${y0.toFixed(1)} A ${r},${r} 0 ${large},1 ${x1.toFixed(1)},${y1.toFixed(1)}"
    fill="none" stroke="#${ink}" stroke-width="${w}" stroke-linecap="round"/>`;
}

// compass star core (no ring)
function compassCore(ink, accent) {
  let out = "";
  [45, 135, 225, 315].forEach((a) => { out += kite(a, 52, 18, 9, ink); });
  [90, 180, 270].forEach((a) => { out += kite(a, 80, 26, 13, ink); });
  out += kite(0, 80, 26, 13, accent); // north in accent
  out += `<circle cx="128" cy="128" r="9" fill="#${ink}"/>`;
  return out;
}

const svg = (body) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">${body}</svg>`;

const marks = {
  compassRose: (ink, accent) => svg(`
    <circle cx="128" cy="128" r="96" fill="none" stroke="#${ink}" stroke-width="8"/>
    ${compassCore(ink, accent)}`),
  shieldChevron: (ink, accent) => svg(`
    <path d="M128,26 L210,52 V128 C210,180 176,214 128,232 C80,214 46,180 46,128 V52 Z"
      fill="none" stroke="#${ink}" stroke-width="10" stroke-linejoin="round"/>
    <polyline points="86,150 128,102 170,150" fill="none" stroke="#${accent}"
      stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>`),
  helmet: (ink, accent) => svg(`
    <circle cx="128" cy="128" r="96" fill="none" stroke="#${ink}" stroke-width="8"/>
    <path d="M62,146 a66,60 0 0 1 132,0 z" fill="#${ink}"/>
    <rect x="52" y="146" width="152" height="14" rx="7" fill="#${ink}"/>
    <rect x="120" y="160" width="16" height="22" rx="6" fill="#${accent}"/>`),
  threePart: (ink, accent) => svg(`
    ${arc(88, 8, 112, ink, 16)}
    ${arc(88, 128, 232, ink, 16)}
    ${arc(88, 248, 352, ink, 16)}
    <circle cx="128" cy="128" r="26" fill="#${accent}"/>`),
  mountain: (ink, accent) => svg(`
    <circle cx="128" cy="128" r="96" fill="none" stroke="#${ink}" stroke-width="8"/>
    <polyline points="52,178 104,92 132,136 160,74 204,178" fill="none"
      stroke="#${ink}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="160" cy="74" r="10" fill="#${accent}"/>`),
  pupFamily: (ink, accent) => svg(`
    ${arc(94, 15, 105, ink, 11)}
    ${arc(94, 135, 225, ink, 11)}
    ${arc(94, 255, 345, ink, 11)}
    <g transform="translate(128 128) scale(0.66) translate(-128 -128)">
      ${compassCore(ink, accent)}
    </g>`),
  frameworkFamily: (ink, accent) => svg(`
    <circle cx="128" cy="128" r="96" fill="none" stroke="#${ink}" stroke-width="8"/>
    <g opacity="0.35">
      <line x1="84" y1="42" x2="84" y2="214" stroke="#${ink}" stroke-width="4"/>
      <line x1="172" y1="42" x2="172" y2="214" stroke="#${ink}" stroke-width="4"/>
      <line x1="42" y1="84" x2="214" y2="84" stroke="#${ink}" stroke-width="4"/>
      <line x1="42" y1="172" x2="214" y2="172" stroke="#${ink}" stroke-width="4"/>
    </g>
    <g transform="translate(128 128) scale(0.72) translate(-128 -128)">
      ${compassCore(ink, accent)}
    </g>`),
};

(async () => {
  const tiles5 = [
    { key: "compassRose", name: "1  COMPASS ROSE", pref: true,
      why: "Direction, judgement and orientation held under uncertainty. Military without aggression." },
    { key: "shieldChevron", name: "2  SHIELD AND CHEVRON",
      why: "Protection, resilience and professional Army identity. Clean for official documents." },
    { key: "helmet", name: "3  HELMET",
      why: "The soldier, not the organisation. Minimal profile inside a circular badge." },
    { key: "threePart", name: "4  THREE-PART DEVICE",
      why: "Prepare, Perform and Recover around a Combat Mindset core." },
    { key: "mountain", name: "5  MOUNTAIN PEAK",
      why: "Challenge, perseverance and continual development. Least distinctively military." },
  ];

  const imgs = {};
  for (const t of tiles5) imgs[t.key] = await svgPng(marks[t.key](WHITE, RED));
  imgs.pupFamily = await svgPng(marks.pupFamily(WHITE, RED));
  imgs.frameworkFamily = await svgPng(marks.frameworkFamily(WHITE, RED));
  imgs.compassSmall = imgs.compassRose;

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "Combat Mindset Emblem Concepts";
  pres.company = "Army Command School";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27;

  // header / footer
  s.addImage({ path: LOGO, x: L, y: 0.36, w: 1.72, h: 0.416 });
  s.addText("COMBAT MINDSET EMBLEM CONCEPTS", {
    x: L, y: 0.9, w: W, h: 0.34, fontFace: F, fontSize: 17, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Army Command School", {
    x: L, y: 1.24, w: W, h: 0.18, fontFace: F, fontSize: 9, italic: true,
    color: SWAMP, align: "left", valign: "middle", margin: 0 });
  s.addText("August 2026", { x: 4.77, y: 11.42, w: 3.0, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6.5, color: BLACK, margin: 0 });

  function sectionTitle(y, text) {
    s.addText(text, { x: L, y, w: W, h: 0.22, fontFace: F, fontSize: 10, bold: true,
      color: SWAMP, charSpacing: 2, align: "left", valign: "middle", margin: 0 });
  }

  // ---- section A: candidates (3 + 2) -------------------------------------
  sectionTitle(1.56, "CANDIDATE EMBLEMS");
  const GAP = 0.16, colW3 = (W - 2 * GAP) / 3, TH = 2.06;
  tiles5.forEach((t, i) => {
    const row = i < 3 ? 0 : 1;
    const idx = i < 3 ? i : i - 3;
    const rowW = row === 0 ? colW3 : colW3;
    const x0 = row === 0 ? L : L + (W - (2 * colW3 + GAP)) / 2;
    const cx = x0 + idx * (rowW + GAP);
    const cy = 1.86 + row * (TH + 0.16);
    s.addShape("rect", { x: cx, y: cy, w: rowW, h: TH, fill: { color: BLACK } });
    if (t.pref) s.addShape("rect", { x: cx, y: cy, w: rowW, h: TH,
      fill: { color: BLACK }, line: { color: RED, width: 1.5 } });
    s.addImage({ data: imgs[t.key], x: cx + rowW / 2 - 0.52, y: cy + 0.14, w: 1.04, h: 1.04 });
    s.addText(t.name + (t.pref ? "   (PREFERRED)" : ""), {
      x: cx + 0.08, y: cy + 1.24, w: rowW - 0.16, h: 0.18, fontFace: F,
      fontSize: 7.6, bold: true, color: t.pref ? RED : MOAWHANGO, charSpacing: 1,
      align: "center", valign: "middle", margin: 0 });
    s.addText(t.why, { x: cx + 0.1, y: cy + 1.44, w: rowW - 0.2, h: 0.56,
      fontFace: F, fontSize: 6.8, italic: true, color: WHITE, align: "center",
      valign: "top", margin: 0 });
  });

  // ---- section B: the family ---------------------------------------------
  const BY = 1.86 + 2 * TH + 0.16 + 0.3; // ≈ 6.44
  sectionTitle(BY, "THE COMPASS FAMILY  (OPTION 1 DEVELOPED)");
  const fam = [
    ["compassSmall", BLACK, "COMBAT MINDSET", "The compass: judgement and direction under pressure."],
    ["pupFamily", SWAMP, "PERFORMANCE UNDER PRESSURE", "The compass within three arcs: Prepare, Perform, Recover."],
    ["frameworkFamily", KAWAKAWA, "NZ ARMY COMBAT MINDSET FRAMEWORK", "The compass on the organising grid: the system around the soldier."],
  ];
  fam.forEach(([key, fill, name, why], i) => {
    const cx = L + i * (colW3 + GAP);
    const cy = BY + 0.3;
    s.addShape("rect", { x: cx, y: cy, w: colW3, h: 2.16, fill: { color: fill } });
    s.addImage({ data: imgs[key], x: cx + colW3 / 2 - 0.52, y: cy + 0.14, w: 1.04, h: 1.04 });
    s.addText(name, { x: cx + 0.08, y: cy + 1.26, w: colW3 - 0.16, h: 0.32,
      fontFace: F, fontSize: 7.8, bold: true, color: WHITE, charSpacing: 0.5,
      align: "center", valign: "middle", margin: 0 });
    s.addText(why, { x: cx + 0.1, y: cy + 1.6, w: colW3 - 0.2, h: 0.5,
      fontFace: F, fontSize: 6.8, italic: true, color: MOAWHANGO, align: "center",
      valign: "top", margin: 0 });
  });

  // ---- section C: in situ -------------------------------------------------
  const CYs = BY + 0.3 + 2.16 + 0.3; // ≈ 9.5
  sectionTitle(CYs, "IN SITU");
  const insitu = [
    [BLACK, "compassSmall", "COMBAT MINDSET", 15],
    [SWAMP, "pupFamily", "PERFORMANCE UNDER PRESSURE", 12],
    [KAWAKAWA, "frameworkFamily", "NZ ARMY COMBAT MINDSET FRAMEWORK", 10.5],
  ];
  insitu.forEach(([fill, key, title, size], i) => {
    const by = CYs + 0.3 + i * 0.56;
    s.addShape("rect", { x: L, y: by, w: W, h: 0.48, fill: { color: fill } });
    s.addImage({ data: imgs[key], x: L + 0.16, y: by + 0.07, w: 0.34, h: 0.34 });
    s.addText(title, { x: L, y: by, w: W, h: 0.48, fontFace: F, fontSize: size,
      bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
  });

  await pres.writeFile({ fileName: "output/combat-mindset-emblems.pptx" });
  console.log("written output/combat-mindset-emblems.pptx");
})();
