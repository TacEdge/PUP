// COMBAT MINDSET — emblem family options, round 2 (compass retired)
// Same family grammar (core / core within Prepare-Perform-Recover arcs /
// core on the organising grid) with three alternative core symbols:
// chevron, Southern Cross, shield. Concept only.

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

function arc(r, a0, a1, ink, w) {
  const rad = (d) => (d * Math.PI) / 180;
  const x0 = 128 + r * Math.sin(rad(a0)), y0 = 128 - r * Math.cos(rad(a0));
  const x1 = 128 + r * Math.sin(rad(a1)), y1 = 128 - r * Math.cos(rad(a1));
  const large = a1 - a0 > 180 ? 1 : 0;
  return `<path d="M ${x0.toFixed(1)},${y0.toFixed(1)} A ${r},${r} 0 ${large},1 ${x1.toFixed(1)},${y1.toFixed(1)}"
    fill="none" stroke="#${ink}" stroke-width="${w}" stroke-linecap="round"/>`;
}

// four-pointed star (NZ flag style)
function star4(cx, cy, r, fill) {
  const w = r * 0.36;
  const pts = [
    [cx, cy - r], [cx + w, cy - w], [cx + r, cy], [cx + w, cy + w],
    [cx, cy + r], [cx - w, cy + w], [cx - r, cy], [cx - w, cy - w],
  ].map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(" ");
  return `<polygon points="${pts}" fill="#${fill}"/>`;
}

const svg = (body) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">${body}</svg>`;

// ---- cores ----------------------------------------------------------------
const chevronCore = (ink, accent) => `
  <polyline points="66,150 128,74 190,150" fill="none" stroke="#${ink}"
    stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>
  <polyline points="90,196 128,150 166,196" fill="none" stroke="#${accent}"
    stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>`;

const crossCore = (ink, accent) => `
  ${star4(128, 62, 22, ink)}
  ${star4(70, 126, 18, ink)}
  ${star4(178, 100, 20, ink)}
  ${star4(128, 194, 26, accent)}`;

const shieldCore = (ink, accent) => `
  <g transform="translate(128 128) scale(0.78) translate(-128 -128)">
    <path d="M128,26 L210,52 V128 C210,180 176,214 128,232 C80,214 46,180 46,128 V52 Z"
      fill="none" stroke="#${ink}" stroke-width="12" stroke-linejoin="round"/>
    <polyline points="86,150 128,102 170,150" fill="none" stroke="#${accent}"
      stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
  </g>`;

// ---- family builders ------------------------------------------------------
function family(core) {
  return {
    cm: (ink, accent) => svg(`
      <circle cx="128" cy="128" r="96" fill="none" stroke="#${ink}" stroke-width="8"/>
      <g transform="translate(128 128) scale(0.74) translate(-128 -128)">${core(ink, accent)}</g>`),
    pup: (ink, accent) => svg(`
      ${arc(94, 15, 105, ink, 11)}
      ${arc(94, 135, 225, ink, 11)}
      ${arc(94, 255, 345, ink, 11)}
      <g transform="translate(128 128) scale(0.6) translate(-128 -128)">${core(ink, accent)}</g>`),
    fw: (ink, accent) => svg(`
      <circle cx="128" cy="128" r="96" fill="none" stroke="#${ink}" stroke-width="8"/>
      <g opacity="0.35">
        <line x1="84" y1="42" x2="84" y2="214" stroke="#${ink}" stroke-width="4"/>
        <line x1="172" y1="42" x2="172" y2="214" stroke="#${ink}" stroke-width="4"/>
        <line x1="42" y1="84" x2="214" y2="84" stroke="#${ink}" stroke-width="4"/>
        <line x1="42" y1="172" x2="214" y2="172" stroke="#${ink}" stroke-width="4"/>
      </g>
      <g transform="translate(128 128) scale(0.66) translate(-128 -128)">${core(ink, accent)}</g>`),
  };
}

(async () => {
  const families = [
    { name: "A  CHEVRON", core: chevronCore,
      why: "Advance under pressure. Rank language every soldier reads; the red echo chevron is the follow-through." },
    { name: "B  SOUTHERN CROSS", core: crossCore,
      why: "Orientation the New Zealand way. Navigation, identity and service under southern skies." },
    { name: "C  SHIELD", core: shieldCore,
      why: "Protection, resilience and professionalism. The most formal; strongest for official documents." },
  ];

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "Combat Mindset Emblem Families 2";
  pres.company = "Army Command School";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27;

  // header / footer
  s.addImage({ path: LOGO, x: L, y: 0.36, w: 1.72, h: 0.416 });
  s.addText("EMBLEM FAMILY OPTIONS  2", {
    x: L, y: 0.9, w: W, h: 0.34, fontFace: F, fontSize: 17, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Army Command School", {
    x: L, y: 1.24, w: W, h: 0.18, fontFace: F, fontSize: 9, italic: true,
    color: SWAMP, align: "left", valign: "middle", margin: 0 });
  s.addText("August 2026", { x: 4.77, y: 11.42, w: 3.0, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6.5, color: BLACK, margin: 0 });

  const GAP = 0.16, colW = (W - 2 * GAP) / 3;
  const labels = ["COMBAT MINDSET", "PERFORMANCE UNDER PRESSURE", "NZ ARMY COMBAT MINDSET FRAMEWORK"];
  const fills = [BLACK, SWAMP, KAWAKAWA];

  let y = 1.62;
  for (const fam of families) {
    s.addText([
      { text: `FAMILY ${fam.name}    `, options: { bold: true, color: SWAMP, charSpacing: 2 } },
      { text: fam.why, options: { italic: true, color: BLACK, fontSize: 7.8 } },
    ], { x: L, y, w: W, h: 0.34, fontFace: F, fontSize: 10, align: "left",
      valign: "middle", margin: 0 });
    y += 0.4;

    const f = family(fam.core);
    const imgs = [
      await svgPng(f.cm(WHITE, RED)),
      await svgPng(f.pup(WHITE, RED)),
      await svgPng(f.fw(WHITE, RED)),
    ];
    imgs.forEach((img, i) => {
      const x = L + i * (colW + GAP);
      s.addShape("rect", { x, y, w: colW, h: 2.16, fill: { color: fills[i] } });
      s.addImage({ data: img, x: x + colW / 2 - 0.58, y: y + 0.16, w: 1.16, h: 1.16 });
      s.addText(labels[i], { x: x + 0.08, y: y + 1.44, w: colW - 0.16, h: 0.34,
        fontFace: F, fontSize: 7.8, bold: true, color: WHITE, charSpacing: 0.5,
        align: "center", valign: "middle", margin: 0 });
      s.addText(["the core symbol", "within the Prepare, Perform, Recover arcs",
        "on the organising grid"][i], {
        x: x + 0.08, y: y + 1.78, w: colW - 0.16, h: 0.3, fontFace: F,
        fontSize: 6.6, italic: true, color: MOAWHANGO, align: "center",
        valign: "top", margin: 0 });
    });
    y += 2.16 + 0.34;
  }

  s.addText(
    "Family grammar unchanged from round 1: one core symbol; the arcs add the enabling cycle; the grid adds the organising system. Any family can be dropped into the proposal banners for review.",
    { x: L, y: y + 0.05, w: W, h: 0.4, fontFace: F, fontSize: 7.5, italic: true,
      color: BLACK, align: "center", valign: "top", margin: 0 });

  await pres.writeFile({ fileName: "output/combat-mindset-emblems-2.pptx" });
  console.log("written output/combat-mindset-emblems-2.pptx");
})();
