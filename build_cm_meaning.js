// COMBAT MINDSET : brandmark exploration, round 3 — meaning led.
// Control, readiness, resilience and decisive action, rather than aggression.
// Every mark is built from solid mass with the detail cut out of it.

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

// Filled annulus sector: the arcs carry weight instead of being stroked.
function ringSeg(a0, a1, R, r) {
  const large = a1 - a0 > 180 ? 1 : 0;
  return `M${fmt(P(a0, R))} A${R},${R} 0 ${large},1 ${fmt(P(a1, R))} ` +
    `L${fmt(P(a1, r))} A${r},${r} 0 ${large},0 ${fmt(P(a0, r))} Z`;
}

// Three arcs: the surrounding pressure, and the Prepare, Perform, Recover cycle.
function arcs(R = 112, r = 92, gap = 22) {
  const span = 120 - gap;
  return [0, 120, 240].map((s) => ringSeg(s + gap / 2, s + gap / 2 + span, R, r)).join(" ");
}

const disc = (r, cx = 128, cy = 128) =>
  `M${(cx - r).toFixed(1)},${cy} A${r},${r} 0 1,0 ${(cx + r).toFixed(1)},${cy} ` +
  `A${r},${r} 0 1,0 ${(cx - r).toFixed(1)},${cy} Z`;

// A restrained spearhead: apex, shoulders, concave base. No weapon detail.
function spearhead(scale = 1, cy = 128) {
  const S = (x, y) => `${(128 + (x - 128) * scale).toFixed(1)},${(cy + (y - 128) * scale).toFixed(1)}`;
  return `M${S(128, 62)} L${S(166, 156)} L${S(128, 134)} L${S(90, 156)} Z`;
}

// An eye as a vesica with a solid pupil: awareness, not surveillance.
function eye(scale = 1) {
  const S = (x, y) => `${(128 + (x - 128) * scale).toFixed(1)},${(128 + (y - 128) * scale).toFixed(1)}`;
  return `M${S(56, 128)} Q${S(128, 66)} ${S(200, 128)} Q${S(128, 190)} ${S(56, 128)} Z`;
}

// A heavy bar that breaks and steps forward: disruption, reset, continuation.
function brokenLine() {
  const seg = (x0, x1, y, h) => `M${x0},${y} H${x1} V${y + h} H${x0} Z`;
  return [seg(30, 104, 158, 30), seg(112, 186, 118, 30), seg(194, 228, 78, 30)].join(" ");
}

const patchSolid =
  "M62,26 H194 A36,36 0 0 1 230,62 V194 A36,36 0 0 1 194,230 H62 " +
  "A36,36 0 0 1 26,194 V62 A36,36 0 0 1 62,26 Z";

const shieldSolid =
  "M128,20 L214,50 V126 C214,180 179,216 128,236 C77,216 42,180 42,126 V50 Z";

// ---- the marks ------------------------------------------------------------
// Hero: arcs of pressure, a controlled core, a spearhead cut forward out of it.
const heroMark = (ink, accent = true) => `
  <path d="${arcs()}" fill="#${ink}"/>
  <path d="${disc(66)} ${spearhead(1.02, 132)}" fill="#${ink}" fill-rule="evenodd"/>
  ${accent ? `<path d="${spearhead(1.02, 132)}" fill="#${RED}"/>` : ""}`;

const ALTERNATIVES = [
  {
    name: "CORE",
    why: "Arcs and a solid centre. Self-command while the environment turns chaotic.",
    mark: (ink) => `<path d="${arcs()}" fill="#${ink}"/><path d="${disc(58)}" fill="#${ink}"/>`,
  },
  {
    name: "FOCUS",
    why: "The eye as awareness and threat recognition. Mindset begins with seeing clearly.",
    mark: (ink) => `
      <path d="${arcs()}" fill="#${ink}"/>
      <path d="${eye(0.82)} ${disc(20)}" fill="#${ink}" fill-rule="evenodd"/>`,
  },
  {
    name: "REFORM",
    why: "A line broken by adversity that resets and continues forward, higher each time.",
    mark: (ink) => `<path d="${brokenLine()}" fill="#${ink}"/>`,
  },
  {
    name: "GUARD",
    why: "The shield of restraint with the spearhead of decision cut through it.",
    mark: (ink) => `
      <path d="${shieldSolid} ${spearhead(1.12, 136)}" fill="#${ink}" fill-rule="evenodd"/>`,
  },
];

(async () => {
  const I = {
    heroW: await svgPng(heroMark(WHITE)),
    heroS: await svgPng(heroMark(SWAMP)),
    heroMono: await svgPng(heroMark(WHITE, false)),
    patchHero: await svgPng(
      `<path d="${patchSolid}" fill="#${WHITE}"/>
       <g transform="translate(128,128) scale(0.62) translate(-128,-128)">${heroMark(SWAMP)}</g>`),
  };
  for (const a of ALTERNATIVES) {
    a.imgW = await svgPng(a.mark(WHITE));
    a.imgS = await svgPng(a.mark(SWAMP));
  }

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "Combat Mindset Brandmark 3";
  pres.company = "Army Command School";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W, MID = L + W / 2;

  s.addImage({ path: LOGO, x: L, y: 0.36, w: 1.72, h: 0.416 });
  s.addText("COMBAT MINDSET BRANDMARK", {
    x: L, y: 0.88, w: W, h: 0.4, fontFace: F, fontSize: 22, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Meaning led: control, readiness, resilience, decisive action", {
    x: L, y: 1.26, w: W, h: 0.22, fontFace: F, fontSize: 11,
    color: SWAMP, align: "left", valign: "middle", margin: 0 });
  s.addText("Army Command School", {
    x: L, y: 1.48, w: W - 1.6, h: 0.2, fontFace: F, fontSize: 8.5, italic: true,
    color: GREY, align: "left", valign: "middle", margin: 0 });
  s.addText("August 2026", { x: R - 1.6, y: 1.48, w: 1.6, h: 0.2, fontFace: F,
    fontSize: 8.5, color: GREY, align: "right", valign: "middle", margin: 0 });
  s.addShape("rect", { x: L, y: 1.74, w: W, h: 0.028, fill: { color: RED } });

  s.addText(
    "The mark should say controlled capability under pressure, not rage. Nothing here uses skulls, weapons or " +
    "snarling imagery. Each option is built from three ideas: what surrounds the soldier, what holds at the centre, " +
    "and what the soldier does about it.",
    { x: L, y: 1.9, w: W, h: 0.5, fontFace: F, fontSize: 9, color: BLACK,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });

  // ---- hero ---------------------------------------------------------------
  s.addText("RECOMMENDED", { x: L, y: 2.44, w: W, h: 0.2, fontFace: F,
    fontSize: 7.6, bold: true, color: RED, charSpacing: 1.4, align: "left",
    valign: "middle", margin: 0 });

  s.addShape("rect", { x: L, y: 2.66, w: W, h: 2.72, fill: { color: BLACK } });
  s.addImage({ data: I.heroW, x: L + 0.42, y: 2.9, w: 2.24, h: 2.24 });

  const story = [
    ["Three arcs", "The pressure that surrounds, and the Prepare, Perform, Recover cycle."],
    ["A solid core", "Self-command. The centre holds while the environment does not."],
    ["A forward spearhead", "Decisive action, struck in red. The only colour in the mark."],
  ];
  let sy = 3.06;
  story.forEach(([t, d]) => {
    s.addShape("rect", { x: L + 3.0, y: sy + 0.03, w: 0.05, h: 0.15, fill: { color: RED } });
    s.addText(t, { x: L + 3.16, y: sy, w: 1.5, h: 0.2, fontFace: F, fontSize: 9.4,
      bold: true, color: WHITE, align: "left", valign: "middle", margin: 0 });
    s.addText(d, { x: L + 3.16, y: sy + 0.2, w: W - 3.4, h: 0.38, fontFace: F,
      fontSize: 8.4, color: MOAWHANGO, align: "left", valign: "top", margin: 0,
      lineSpacingMultiple: 1.1 });
    sy += 0.66;
  });
  s.addText("See clearly.   Remain controlled.   Act decisively.", {
    x: L + 3.0, y: 5.02, w: W - 3.2, h: 0.22, fontFace: F, fontSize: 9.6,
    italic: true, color: WHITE, align: "left", valign: "middle", margin: 0 });

  // ---- hero applications --------------------------------------------------
  const AG = 0.14, AW = (W - 3 * AG) / 4, AH = 1.16;
  const apps = [
    [I.heroS, WHITE, "On white"],
    [I.heroMono, BLACK, "Single colour"],
    [I.patchHero, SWAMP, "In the patch"],
    [I.heroS, WHITE, "Small"],
  ];
  apps.forEach(([img, bg, cap], i) => {
    const x = L + i * (AW + AG);
    s.addShape("rect", { x, y: 5.52, w: AW, h: AH, fill: { color: bg },
      line: bg === WHITE ? { color: MOAWHANGO, width: 1 } : undefined });
    const sz = i === 3 ? 0.4 : 0.76;
    s.addImage({ data: img, x: x + AW / 2 - sz / 2, y: 5.52 + 0.42 - sz / 2 + 0.1, w: sz, h: sz });
    s.addText(cap, { x, y: 5.52 + AH - 0.26, w: AW, h: 0.18, fontFace: F,
      fontSize: 6.6, color: bg === WHITE ? GREY : MOAWHANGO,
      align: "center", valign: "middle", margin: 0 });
  });

  // ---- alternatives -------------------------------------------------------
  s.addText("ALTERNATIVES", { x: L, y: 6.92, w: W, h: 0.2, fontFace: F,
    fontSize: 7.6, bold: true, color: SWAMP, charSpacing: 1.4, align: "left",
    valign: "middle", margin: 0 });

  let ay = 7.14;
  ALTERNATIVES.forEach((a) => {
    s.addShape("rect", { x: L, y: ay, w: 1.34, h: 0.86, fill: { color: BLACK } });
    s.addImage({ data: a.imgW, x: L + 0.24, y: ay + 0.07, w: 0.72, h: 0.72 });
    s.addText(a.name, { x: L + 1.5, y: ay + 0.14, w: 1.2, h: 0.22, fontFace: F,
      fontSize: 10, bold: true, color: SWAMP, charSpacing: 1.6,
      align: "left", valign: "middle", margin: 0 });
    s.addText(a.why, { x: L + 2.74, y: ay + 0.12, w: R - L - 2.74, h: 0.46,
      fontFace: F, fontSize: 8.4, color: BLACK, align: "left", valign: "top",
      margin: 0, lineSpacingMultiple: 1.1 });
    ay += 0.98;
  });

  s.addText([
    { text: "Note.  ", options: { bold: true, color: SWAMP } },
    { text: "The recommended mark carries the three-part story without writing it down, and the arcs give it a quiet " +
            "link to Prepare, Perform and Recover. It is the only option here that says all three things at once.",
      options: { color: BLACK } },
  ], { x: L, y: ay + 0.08, w: W, h: 0.4, fontFace: F, fontSize: 8, align: "left",
       valign: "top", margin: 0, lineSpacingMultiple: 1.1 });

  await pres.writeFile({ fileName: "output/combat-mindset-brandmark-meaning.pptx" });
  console.log("written output/combat-mindset-brandmark-meaning.pptx");
})();
