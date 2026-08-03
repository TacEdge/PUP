// ELDA LEAD SYSTEMS STUDENT WITHDRAWAL SOP — 1-page visual model
// NZ Army design language. Brevity pass: readable in 30 seconds in the field.

const pptxgen = require("pptxgenjs");
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const sharp = require("sharp");
const lu = require("react-icons/lu");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const F = "Arial";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

async function icon(name, hex, strokeWidth = 1.7) {
  const cmp = lu[name] || lu.LuCircle;
  const el = React.createElement(cmp, { color: "#" + hex, size: 256, strokeWidth });
  let svg = renderToStaticMarkup(el);
  if (!svg.includes("xmlns")) svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ');
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

(async () => {
  const I = {};
  const need = {
    target: ["LuTarget", SWAMP],
    shield: ["LuShieldCheck", SWAMP], users: ["LuUsers", SWAMP], book: ["LuBookOpen", SWAMP],
    timer: ["LuTimer", SWAMP], handshake: ["LuHandshake", SWAMP], backpack: ["LuBackpack", SWAMP],
    usersRow: ["LuUsers", SWAMP], storm: ["LuCloudLightning", SWAMP], route: ["LuRoute", SWAMP],
    cross: ["LuCross", WHITE], brain: ["LuBrain", WHITE], alert: ["LuTriangleAlert", WHITE],
    eye: ["LuEye", SWAMP], message: ["LuMessageSquare", SWAMP], clipboard: ["LuClipboardList", SWAMP],
    shieldAlert: ["LuShieldAlert", SWAMP],
  };
  for (const [k, [n, c]] of Object.entries(need)) I[k] = await icon(n, c);

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W;

  // ---- header ------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.42, w: 1.05, h: 0.254 });
  s.addText("ELDA LEAD SYSTEMS STUDENT WITHDRAWAL SOP", {
    x: 1.72, y: 0.32, w: 6.05, h: 0.26, fontFace: F, fontSize: 14, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Warrant Officers Adventure Race", {
    x: 1.72, y: 0.59, w: 6.05, h: 0.17, fontFace: F, fontSize: 8.6, bold: true,
    italic: true, color: KAWAKAWA, align: "left", valign: "middle", margin: 0 });
  s.addText("NZ Army Leadership Centre | Army Command School", {
    x: 1.72, y: 0.76, w: 6.05, h: 0.16, fontFace: F, fontSize: 7.6, italic: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addShape("line", { x: L, y: 1.02, w: W, h: 0, line: { color: BLACK, width: 1 } });

  function bar(x, y, w, text, h = 0.3, fill = SWAMP, size = 9) {
    s.addShape("rect", { x, y, w, h, fill: { color: fill } });
    s.addText(text, { x, y, w, h, fontFace: F, fontSize: size, bold: true,
      color: WHITE, charSpacing: 1.5, align: "center", valign: "middle", margin: 0 });
  }

  // ---- row A: purpose + governing principle | not grounds ----------------
  const LW = 4.55, RXc = L + LW + 0.17, RW = R - RXc;
  s.addImage({ data: I.target, x: L, y: 1.22, w: 0.3, h: 0.3 });
  s.addText("1. PURPOSE", { x: L + 0.42, y: 1.2, w: LW - 0.42, h: 0.2, fontFace: F,
    fontSize: 10, bold: true, color: SWAMP, charSpacing: 1.5, align: "left",
    valign: "middle", margin: 0 });
  s.addText(
    "The Adventure Race creates a race environment that exposes participants and teams to physical, mental and interpersonal pressure to enable leadership development. This SOP provides a fair, consistent and defensible process for participant withdrawal.",
    { x: L + 0.42, y: 1.4, w: LW - 0.47, h: 0.6, fontFace: F, fontSize: 8.6,
      color: BLACK, align: "left", valign: "top", margin: 0 });

  bar(L, 2.06, LW, "2. GOVERNING PRINCIPLE");
  s.addShape("rect", { x: L, y: 2.36, w: LW, h: 1.86,
    fill: { color: MOAWHANGO, transparency: 72 } });
  s.addText(
    "The Adventure Race deliberately creates pressure, fatigue, uncertainty and adversity to achieve approved learning objectives. Withdrawal is justified only where a participant's condition or conduct materially prevents:",
    { x: L + 0.16, y: 2.48, w: LW - 0.32, h: 0.66, fontFace: F, fontSize: 8.2,
      color: BLACK, align: "left", valign: "top", margin: 0 });
  const circles = [
    ["shield", "Safe participation"],
    ["book", "The intended learning and assessment conditions"],
    ["users", "The safe and effective conduct of the activity"],
  ];
  const cw = LW / 3;
  circles.forEach(([ic, label], i) => {
    const cx = L + i * cw + cw / 2;
    if (i) s.addShape("line", { x: L + i * cw - 0.25, y: 3.43, w: 0.5, h: 0,
      line: { color: SWAMP, width: 1 } });
    s.addShape("ellipse", { x: cx - 0.27, y: 3.16, w: 0.54, h: 0.54,
      fill: { color: WHITE }, line: { color: SWAMP, width: 1.25 } });
    s.addImage({ data: I[ic], x: cx - 0.145, y: 3.285, w: 0.29, h: 0.29 });
    s.addText(label, { x: L + i * cw + 0.05, y: 3.74, w: cw - 0.1, h: 0.44,
      fontFace: F, fontSize: 6.9, bold: true, color: SWAMP, align: "center",
      valign: "top", margin: 0 });
  });

  bar(RXc, 1.2, RW, "NOT GROUNDS BY THEMSELVES", 0.3, KAWAKAWA, 7.8);
  s.addShape("rect", { x: RXc, y: 1.5, w: RW, h: 2.72, fill: { color: WHITE },
    line: { color: WAIOURU, width: 0.75 } });
  const ng = [
    ["timer", "Slower pace than peers"],
    ["handshake", "Need for reasonable assistance"],
    ["backpack", "Redistribution of equipment"],
    ["usersRow", "Increased workload on others"],
    ["storm", "Frustration or interpersonal friction"],
    ["route", "Need to adjust pace, roles or plan"],
  ];
  ng.forEach(([ic, label], i) => {
    const gy = 1.64 + i * 0.37;
    s.addImage({ data: I[ic], x: RXc + 0.12, y: gy, w: 0.22, h: 0.22 });
    s.addText(label, { x: RXc + 0.42, y: gy - 0.04, w: RW - 0.52, h: 0.3,
      fontFace: F, fontSize: 7.4, color: BLACK, align: "left", valign: "middle", margin: 0 });
    if (i < 5) s.addShape("line", { x: RXc + 0.12, y: gy + 0.29, w: RW - 0.24, h: 0,
      line: { color: WAIOURU, width: 0.4 } });
  });
  s.addShape("rect", { x: RXc + 0.1, y: 3.86, w: RW - 0.2, h: 0.26,
    fill: { color: MOAWHANGO, transparency: 55 } });
  s.addText("Normal developmental effects.", { x: RXc + 0.1, y: 3.86,
    w: RW - 0.2, h: 0.26, fontFace: F, fontSize: 7.2, italic: true, bold: true,
    color: SWAMP, align: "center", valign: "middle", margin: 0 });

  // ---- grounds ------------------------------------------------------------
  const GY = 4.48;
  bar(L, GY, W, "3. GROUNDS FOR WITHDRAWAL");
  const grounds = [
    ["cross", "Medical & Safety",
      "The participant cannot continue safely because of a medical condition or safety risk."],
    ["brain", "Learning & Assessment",
      "Continued participation prevents the intended learning and assessment conditions."],
    ["alert", "Conduct",
      "The participant refuses lawful instructions or prevents the safe and effective conduct of the activity."],
  ];
  const gw = (W - 2 * 0.12) / 3;
  grounds.forEach(([ic, name, desc], i) => {
    const gx = L + i * (gw + 0.12);
    s.addShape("rect", { x: gx, y: GY + 0.38, w: gw, h: 1.34, fill: { color: WHITE },
      line: { color: WAIOURU, width: 0.75 } });
    s.addShape("rect", { x: gx + 0.08, y: GY + 0.46, w: 0.19, h: 0.19,
      fill: { color: KAWAKAWA } });
    s.addText(String(i + 1), { x: gx + 0.08, y: GY + 0.46, w: 0.19, h: 0.19,
      fontFace: F, fontSize: 8, bold: true, color: WHITE, align: "center",
      valign: "middle", margin: 0 });
    s.addShape("ellipse", { x: gx + gw / 2 - 0.21, y: GY + 0.46, w: 0.42, h: 0.42,
      fill: { color: SWAMP } });
    s.addImage({ data: I[ic], x: gx + gw / 2 - 0.115, y: GY + 0.555, w: 0.23, h: 0.23 });
    s.addText(name, { x: gx + 0.06, y: GY + 0.92, w: gw - 0.12, h: 0.2,
      fontFace: F, fontSize: 8.8, bold: true, color: SWAMP, align: "center",
      valign: "middle", margin: 0 });
    s.addText(desc, { x: gx + 0.14, y: GY + 1.14, w: gw - 0.28, h: 0.52,
      fontFace: F, fontSize: 7.4, color: BLACK, align: "center", valign: "top", margin: 0 });
  });

  // ---- withdrawal test ----------------------------------------------------
  const TY = GY + 1.94;
  s.addShape("rect", { x: L, y: TY, w: W, h: 0.94, fill: { color: KAWAKAWA } });
  s.addText("4. THE WITHDRAWAL TEST", { x: L, y: TY + 0.06, w: W, h: 0.18,
    fontFace: F, fontSize: 9, bold: true, color: MOAWHANGO, charSpacing: 2,
    align: "center", valign: "middle", margin: 0 });
  s.addText(
    "What specific requirement or learning objective can no longer be safely or meaningfully achieved, and why will coaching or authorised adjustment not restore it?",
    { x: L + 0.45, y: TY + 0.26, w: W - 0.9, h: 0.4, fontFace: F, fontSize: 8.8,
      bold: true, italic: true, color: WHITE, align: "center", valign: "top", margin: 0 });
  s.addText("A slower team, greater workload or frustration alone do not meet this threshold.",
    { x: L + 0.45, y: TY + 0.68, w: W - 0.9, h: 0.18, fontFace: F, fontSize: 7.4,
      italic: true, color: MOAWHANGO, align: "center", valign: "middle", margin: 0 });

  // ---- decision process ---------------------------------------------------
  const DY = TY + 1.12;
  bar(L, DY, W, "5. DECISION PROCESS");
  const steps = [
    ["eye", "Observe", "Identify the issue and allow the team to respond."],
    ["message", "Intervene", "Coach, apply authorised adjustments and reassess."],
    ["clipboard", "Decide", "Recommend withdrawal to the designated authority."],
  ];
  const sw = 2.25, sgap = (W - 3 * sw) / 2;
  steps.forEach(([ic, name, desc], i) => {
    const sx = L + i * (sw + sgap);
    s.addShape("ellipse", { x: sx, y: DY + 0.44, w: 0.38, h: 0.38,
      fill: { color: WHITE }, line: { color: SWAMP, width: 1.25 } });
    s.addImage({ data: I[ic], x: sx + 0.085, y: DY + 0.525, w: 0.21, h: 0.21 });
    s.addText([
      { text: `${i + 1}.  `, options: { color: RED, bold: true } },
      { text: name, options: { color: SWAMP, bold: true } },
    ], { x: sx + 0.46, y: DY + 0.42, w: sw - 0.46, h: 0.2, fontFace: F,
      fontSize: 9, align: "left", valign: "middle", margin: 0 });
    s.addText(desc, { x: sx + 0.46, y: DY + 0.63, w: sw - 0.48, h: 0.44,
      fontFace: F, fontSize: 7.2, color: BLACK, align: "left", valign: "top", margin: 0 });
    if (i < 2) s.addText("►", { x: sx + sw - 0.04, y: DY + 0.5, w: sgap + 0.08,
      h: 0.24, fontFace: F, fontSize: 10, bold: true, color: RED, align: "center",
      valign: "middle", margin: 0 });
  });
  s.addShape("rect", { x: L, y: DY + 1.16, w: W, h: 0.34,
    fill: { color: MOAWHANGO, transparency: 55 } });
  s.addText([
    { text: "Non-immediate withdrawal:  ", options: { bold: true, color: SWAMP } },
    { text: "CI NZALC and CI NCO School discuss the case; CI NZALC recommends withdrawal to COMDT ACS for confirmation.",
      options: { color: BLACK } },
  ], { x: L + 0.15, y: DY + 1.16, w: W - 0.3, h: 0.34, fontFace: F, fontSize: 7.6,
    align: "left", valign: "middle", margin: 0 });

  // ---- immediate withdrawal | record of decision --------------------------
  const EY = DY + 1.72, EH = 1.66;
  const LW2 = 3.3, RX2 = L + LW2 + 0.17, RW2 = R - RX2;
  bar(L, EY, LW2, "6. IMMEDIATE WITHDRAWAL", 0.28, SWAMP, 8);
  s.addShape("rect", { x: L, y: EY + 0.28, w: LW2, h: EH - 0.28,
    fill: { color: MOAWHANGO, transparency: 72 } });
  s.addImage({ data: I.shieldAlert, x: L + 0.14, y: EY + 0.46, w: 0.34, h: 0.34 });
  s.addText(
    "An instructor, safety staff member or medical practitioner may immediately withdraw a participant to manage an immediate safety or medical risk. Notify CI NZALC and CI NCO School as soon as practicable.",
    { x: L + 0.6, y: EY + 0.42, w: LW2 - 0.75, h: EH - 0.56, fontFace: F,
      fontSize: 7.8, color: BLACK, align: "left", valign: "top", margin: 0 });

  bar(RX2, EY, RW2, "7. RECORD OF DECISION", 0.28, SWAMP, 8);
  s.addShape("rect", { x: RX2, y: EY + 0.28, w: RW2, h: EH - 0.28,
    fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
  const rec = [
    "Ground for withdrawal",
    "Supporting evidence",
    "Coaching or adjustments attempted",
    "Why the threshold was met",
    "Recommending and approving authority",
    "Assessment/course outcome",
  ];
  rec.forEach((t, i) => {
    const ry = EY + 0.36 + i * 0.21;
    s.addText("✓", { x: RX2 + 0.12, y: ry, w: 0.18, h: 0.2, fontFace: F,
      fontSize: 8.5, bold: true, color: RED, align: "left", valign: "middle", margin: 0 });
    s.addText(t, { x: RX2 + 0.34, y: ry, w: RW2 - 0.46, h: 0.2, fontFace: F,
      fontSize: 7.6, color: BLACK, align: "left", valign: "middle", margin: 0 });
  });

  await pres.writeFile({ fileName: "output/withdrawal-sop-visual.pptx" });
  console.log("written output/withdrawal-sop-visual.pptx");
})();
