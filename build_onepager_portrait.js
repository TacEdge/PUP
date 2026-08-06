// COMBAT MINDSET FRAMEWORK PROPOSAL : the model on a page, portrait A4.
//
// Built on the datum, the governing device adopted in the identity system.
// No emblem, badge or symbol. The relationships are drawn rather than
// asserted: Performance Under Pressure is the full measure of the datum,
// Combat Mindset is the segment of it under combat load, and the framework
// is the bracket holding both.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

// NZ Army palette, as published in the Visual Identity Guidelines p58.
const RED = "D31145", BLACK = "000000", WHITE = "FFFFFF";
const GREY = "6E6E6E", RULE = "C8C8C8";
const F = "Arial";          // Neue Haas Grotesk in production
const LOGO = "assets/nz-army-logo.png";
const LOGO_AR = 4.38;

async function svg(body, w, h, px) {
  const s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}">` +
    `<rect width="${w}" height="${h}" fill="#${WHITE}"/>${body}</svg>`;
  const buf = await sharp(Buffer.from(s)).resize(px, Math.round((px * h) / w)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

const txt = (x, y, t, size, o = {}) =>
  `<text x="${x}" y="${y}" font-family="Arial" font-size="${size}"` +
  ` fill="#${o.fill || BLACK}"` +
  (o.bold ? ' font-weight="bold"' : "") +
  (o.anchor ? ` text-anchor="${o.anchor}"` : "") +
  (o.track ? ` letter-spacing="${o.track}"` : "") + `>${t}</text>`;

// A measure bar: a span with end serifs. States the extent of something.
const measure = (x0, x1, y) =>
  `<path d="M${x0},${y - 9} V${y + 9} M${x0},${y} H${x1} M${x1},${y - 9} V${y + 9}"` +
  ` stroke="#${BLACK}" stroke-width="4" fill="none"/>`;

// ---------------------------------------------------------------------------
// FIGURE 1 : the model.
// ---------------------------------------------------------------------------
function modelFigure() {
  const W = 1400, H = 850;
  const dY = 470, x0 = 150, x1 = 1250;   // the datum
  const cA = 600, cB = 1060;             // the combat-specific segment

  let ticks = "";
  for (let x = x0; x <= x1; x += 50) {
    const major = (x - x0) % 200 === 0;
    ticks += `<line x1="${x}" y1="${dY}" x2="${x}" y2="${dY + (major ? 20 : 11)}"` +
      ` stroke="#${RULE}" stroke-width="3"/>`;
  }

  // density above the datum: accumulated pressure, heaviest nearest the line
  let field = "";
  for (let y = 226; y < dY - 10; y += 14)
    for (let x = cA; x <= cB; x += 14) {
      const t = (y - 226) / (dY - 236);
      field += `<circle cx="${x}" cy="${y}" r="${(0.7 + 2.9 * Math.pow(t, 1.5)).toFixed(2)}" fill="#${BLACK}"/>`;
    }

  // the displacement trace: load displaces the standard, and it returns to true
  let d = `M${x0},${dY}`;
  for (let x = x0; x <= x1; x += 4) {
    const t = (x - 830) / 155;
    const load = x > cA && x < cB ? Math.exp(-t * t * 1.1) : 0;
    d += ` L${x},${(dY - load * 78 + load * 34 * Math.sin((x - cA) / 17)).toFixed(1)}`;
  }

  return {
    body: `
      ${txt(700, 52, "ORGANISING SYSTEM", 19, { anchor: "middle", fill: GREY, track: 3 })}
      ${txt(700, 94, "COMBAT MINDSET FRAMEWORK", 36, { anchor: "middle", bold: true })}
      ${txt(700, 126, "Governs, develops, delivers and assures both.", 21, { anchor: "middle", fill: GREY })}

      <path d="M110,164 H32 V812 H110" fill="none" stroke="#${BLACK}" stroke-width="6"/>
      <path d="M1290,164 H1368 V812 H1290" fill="none" stroke="#${BLACK}" stroke-width="6"/>

      ${field}
      <line x1="${cA}" y1="212" x2="${cA}" y2="${dY}" stroke="#${GREY}" stroke-width="3" stroke-dasharray="9 7"/>
      <line x1="${cB}" y1="212" x2="${cB}" y2="${dY}" stroke="#${GREY}" stroke-width="3" stroke-dasharray="9 7"/>
      ${txt((cA + cB) / 2, 200, "OPERATIONAL PRESSURE", 19, { anchor: "middle", fill: GREY, track: 3 })}

      ${ticks}
      <line x1="${x0}" y1="${dY}" x2="${x1}" y2="${dY}" stroke="#${BLACK}" stroke-width="5"/>
      <path d="${d}" fill="none" stroke="#${BLACK}" stroke-width="5"/>

      ${measure(x0, x1, 552)}
      ${txt(x0, 594, "ENABLING CAPABILITY", 18, { fill: GREY, track: 3 })}
      ${txt(x0, 628, "PERFORMANCE UNDER PRESSURE", 28, { bold: true })}
      ${txt(x0, 658, "The trainable capability, wherever significant pressure exists.", 20, { fill: GREY })}

      ${measure(cA, cB, 712)}
      ${txt(cA, 754, "WARFIGHTING IMPERATIVE", 18, { fill: GREY, track: 3 })}
      ${txt(cA, 788, "COMBAT MINDSET", 28, { bold: true })}
      ${txt(cA, 818, "Its combat-specific expression.", 20, { fill: GREY })}`,
    w: W, h: H,
  };
}

// ---------------------------------------------------------------------------
// FIGURE 2 : the programme. Sequence along the datum, with a node at each
// point where a phase output is committed.
// ---------------------------------------------------------------------------
function programmeFigure() {
  const W = 1400, H = 440, dY = 175, x0 = 60, x1 = 1340;
  const PHASES = [
    ["SEPT 2026", "DEFINE", ["Terminology, governance,", "roles and responsibilities"]],
    ["SEPT 2026", "UNDERSTAND", ["Assess existing doctrine,", "products and delivery"]],
    ["OCT 2026", "DESIGN", ["Framework, delivery system", "and outcomes"]],
    ["NOV 2026", "VALIDATE", ["Refine with stakeholders,", "bounded pilots"]],
    ["LATE NOV 2026", "IMPLEMENT", ["Deliver for approval", "and implementation"]],
  ];
  let ticks = "";
  for (let x = x0; x <= x1; x += 40)
    ticks += `<line x1="${x}" y1="${dY}" x2="${x}" y2="${dY + ((x - x0) % 160 === 0 ? 16 : 9)}"` +
      ` stroke="#${RULE}" stroke-width="3"/>`;

  const body = PHASES.map(([date, name, lines], i) => {
    const x = 190 + i * 255;
    return `
      ${txt(x, 84, date, 19, { anchor: "middle", fill: GREY, track: 2 })}
      <circle cx="${x}" cy="${dY}" r="26" fill="#${WHITE}" stroke="#${RED}" stroke-width="10"/>
      ${txt(x, 272, name, 30, { anchor: "middle", bold: true, track: 1.4 })}
      ${lines.map((l, j) => txt(x, 314 + j * 28, l, 20, { anchor: "middle", fill: GREY })).join("")}`;
  }).join("");

  return {
    body: `${ticks}<line x1="${x0}" y1="${dY}" x2="${x1}" y2="${dY}" stroke="#${BLACK}" stroke-width="5"/>${body}`,
    w: W, h: H,
  };
}

// Rationed density for the outcome band. Divider surfaces only.
function bandField() {
  const W = 900, H = 200;
  let dots = "";
  for (let y = 0; y < H; y += 11)
    for (let x = 0; x < W; x += 11) {
      const t = x / W;
      dots += `<circle cx="${x}" cy="${y}" r="${(0.5 + 2.4 * t * t).toFixed(2)}" fill="#${WHITE}"/>`;
    }
  return { body: `<rect width="${W}" height="${H}" fill="#${BLACK}"/>${dots}`, w: W, h: H };
}

// ---------------------------------------------------------------------------
(async () => {
  const mk = async (o, px) => svg(o.body, o.w, o.h, px);
  const I = {
    model: await mk(modelFigure(), 1600),
    programme: await mk(programmeFigure(), 1600),
    band: await mk(bandField(), 900),
  };

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "NZ Army Combat Mindset Framework Proposal";
  pres.subject = "NZ Army Combat Mindset Framework Proposal";
  pres.company = "Army Command School";
  pres.revision = "10";

  const s = pres.addSlide();
  s.background = { color: WHITE };
  const L = 0.62, W = 7.03, R = L + W;

  const label = (y, t) => {
    s.addText(t, { x: L, y, w: W, h: 0.18, fontFace: F, fontSize: 7.4, bold: true,
      color: BLACK, charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L, y: y + 0.19, w: W, h: 0.008, fill: { color: RULE } });
  };

  // ---- header -------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.4, w: 1.62, h: 1.62 / LOGO_AR });
  s.addText("NZ ARMY COMBAT MINDSET FRAMEWORK PROPOSAL", {
    x: L, y: 0.92, w: W, h: 0.28, fontFace: F, fontSize: 15, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("The model on a page", {
    x: L, y: 1.2, w: W - 2, h: 0.2, fontFace: F, fontSize: 9, color: GREY,
    align: "left", valign: "middle", margin: 0 });
  s.addText("Army Command School", {
    x: R - 2, y: 1.2, w: 2, h: 0.2, fontFace: F, fontSize: 8, italic: true,
    color: GREY, align: "right", valign: "middle", margin: 0 });
  s.addShape("rect", { x: L, y: 1.46, w: W, h: 0.018, fill: { color: BLACK } });

  // ---- the model ----------------------------------------------------------
  label(1.72, "THE MODEL");
  const mH = W * 850 / 1400;
  s.addImage({ data: I.model, x: L, y: 2.0, w: W, h: mH });

  // ---- the outcome --------------------------------------------------------
  const bY = 2.0 + mH + 0.42;
  label(bY - 0.32, "THE OUTCOME");
  s.addShape("rect", { x: L, y: bY, w: W, h: 1.02, fill: { color: BLACK } });
  s.addImage({ data: I.band, x: L, y: bY, w: W, h: 1.02, transparency: 90 });
  s.addText("Remain effective. Act decisively.", {
    x: L + 0.32, y: bY + 0.22, w: W - 0.64, h: 0.28, fontFace: F, fontSize: 15,
    color: WHITE, align: "left", valign: "middle", margin: 0 });
  s.addText("Harder to kill.", {
    x: L + 0.32, y: bY + 0.52, w: W - 0.64, h: 0.28, fontFace: F, fontSize: 15,
    bold: true, color: WHITE, align: "left", valign: "middle", margin: 0 });

  // ---- the programme ------------------------------------------------------
  const pY = bY + 1.02 + 0.56;
  label(pY - 0.32, "THE FRAMEWORK DEVELOPMENT PROGRAMME");
  s.addImage({ data: I.programme, x: L, y: pY, w: W, h: W * 440 / 1400 });
  s.addText("Each node marks the point at which a phase output is committed. Phases may overlap, but each depends on the endorsed outputs of the one before it.", {
    x: L, y: pY + W * 440 / 1400 + 0.14, w: W, h: 0.3, fontFace: F, fontSize: 7.8,
    italic: true, color: GREY, align: "left", valign: "top", margin: 0 });

  // ---- footer -------------------------------------------------------------
  s.addShape("rect", { x: L, y: 11.1, w: W, h: 0.012, fill: { color: RULE } });
  s.addText("FRAMEWORK", { x: L, y: 11.16, w: 3, h: 0.18, fontFace: F, fontSize: 6.4,
    bold: true, color: BLACK, charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
  s.addText("August 2026", { x: R - 2, y: 11.16, w: 2, h: 0.18, fontFace: F, fontSize: 6.4,
    color: GREY, align: "right", valign: "middle", margin: 0 });

  await pres.writeFile({ fileName: "output/combat-mindset-onepager-portrait.pptx" });
  console.log("written output/combat-mindset-onepager-portrait.pptx");
})();
