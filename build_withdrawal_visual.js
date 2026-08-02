// ELDA LEAD SYSTEMS STUDENT WITHDRAWAL SOP — 1-page visual model
// NZ Army design language (brand palette, Arial, UNCLASSIFIED markings).

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
    cross: ["LuCross", WHITE], activity: ["LuActivity", WHITE], brain: ["LuBrain", WHITE],
    alert: ["LuTriangleAlert", WHITE], heart: ["LuHeartPulse", WHITE],
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

  // ---- markings (plain text, no banner) -----------------------------------
  s.addText("UNCLASSIFIED", { x: 0, y: 0.02, w: 8.27, h: 0.18, align: "center",
    valign: "middle", fontFace: F, fontSize: 7.5, bold: true, color: BLACK,
    charSpacing: 4, margin: 0 });
  s.addText("UNCLASSIFIED", { x: 0, y: 11.49, w: 8.27, h: 0.18, align: "center",
    valign: "middle", fontFace: F, fontSize: 7.5, bold: true, color: BLACK,
    charSpacing: 4, margin: 0 });
  s.addText("Army Command School  ·  ACS 2026", {
    x: L, y: 11.49, w: 2.6, h: 0.18, align: "left", valign: "middle",
    fontFace: F, fontSize: 6, color: BLACK, margin: 0 });
  s.addText("Draft v0.1  ·  July 2026", { x: 5.7, y: 11.49, w: 2.07, h: 0.18,
    align: "right", valign: "middle", fontFace: F, fontSize: 6, color: BLACK, margin: 0 });

  // ---- header ------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.32, w: 1.05, h: 0.254 });
  s.addText("ELDA LEAD SYSTEMS STUDENT WITHDRAWAL SOP", {
    x: 1.72, y: 0.26, w: 6.05, h: 0.26, fontFace: F, fontSize: 14, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText([
    { text: "1-Page Visual Model", options: { bold: true, italic: true, color: KAWAKAWA } },
    { text: "   ·   Warrant Officers Adventure Race   ·   NZ Army Leadership Centre | Army Command School",
      options: { italic: true, color: BLACK } },
  ], { x: 1.72, y: 0.53, w: 6.05, h: 0.18, fontFace: F, fontSize: 7.6,
    align: "left", valign: "middle", margin: 0 });
  s.addShape("line", { x: L, y: 0.84, w: W, h: 0, line: { color: BLACK, width: 1 } });

  function bar(x, y, w, text, h = 0.26, fill = SWAMP, size = 8.6) {
    s.addShape("rect", { x, y, w, h, fill: { color: fill } });
    s.addText(text, { x, y, w, h, fontFace: F, fontSize: size, bold: true,
      color: WHITE, charSpacing: 1.5, align: "center", valign: "middle", margin: 0 });
  }

  // ---- row A: purpose + governing principle | not grounds ----------------
  const LW = 4.55, RXc = L + LW + 0.17, RW = R - RXc; // right col 2.55
  // purpose
  s.addImage({ data: I.target, x: L, y: 0.98, w: 0.3, h: 0.3 });
  s.addText("1. PURPOSE", { x: L + 0.4, y: 0.98, w: LW - 0.4, h: 0.2, fontFace: F,
    fontSize: 9.5, bold: true, color: SWAMP, charSpacing: 1.5, align: "left",
    valign: "middle", margin: 0 });
  s.addText(
    "Provide a consistent, fair and defensible process for deciding whether a participant is withdrawn from the Adventure Race for safety, medical, conduct or performance reasons.",
    { x: L + 0.4, y: 1.18, w: LW - 0.45, h: 0.62, fontFace: F, fontSize: 7.8,
      color: BLACK, align: "left", valign: "top", margin: 0 });

  // governing principle
  bar(L, 1.92, LW, "2. GOVERNING PRINCIPLE");
  s.addShape("rect", { x: L, y: 2.18, w: LW, h: 1.98,
    fill: { color: MOAWHANGO, transparency: 72 } });
  s.addText(
    "The Adventure Race deliberately exposes participants and teams to pressure, fatigue, adversity, uncertainty and interpersonal friction in support of approved learning objectives. Withdrawal is justified only where a participant's condition, capability or conduct materially prevents:",
    { x: L + 0.14, y: 2.28, w: LW - 0.28, h: 0.72, fontFace: F, fontSize: 7.7,
      color: BLACK, align: "left", valign: "top", margin: 0 });
  const circles = [
    ["shield", "Safe participation"],
    ["book", "The intended learning and assessment conditions"],
    ["users", "The safe and effective conduct of the activity"],
  ];
  const cw = LW / 3;
  circles.forEach(([ic, label], i) => {
    const cx = L + i * cw + cw / 2;
    if (i) s.addShape("line", { x: L + i * cw - 0.25, y: 3.36, w: 0.5, h: 0,
      line: { color: SWAMP, width: 1 } });
    s.addShape("ellipse", { x: cx - 0.26, y: 3.1, w: 0.52, h: 0.52,
      fill: { color: WHITE }, line: { color: SWAMP, width: 1.25 } });
    s.addImage({ data: I[ic], x: cx - 0.14, y: 3.22, w: 0.28, h: 0.28 });
    s.addText(label, { x: L + i * cw + 0.05, y: 3.66, w: cw - 0.1, h: 0.44,
      fontFace: F, fontSize: 6.6, bold: true, color: SWAMP, align: "center",
      valign: "top", margin: 0 });
  });

  // not grounds sidebar
  bar(RXc, 0.98, RW, "NOT GROUNDS BY THEMSELVES", 0.26, KAWAKAWA, 7.6);
  s.addShape("rect", { x: RXc, y: 1.24, w: RW, h: 2.92, fill: { color: WHITE },
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
    const gy = 1.36 + i * 0.4;
    s.addImage({ data: I[ic], x: RXc + 0.12, y: gy, w: 0.22, h: 0.22 });
    s.addText(label, { x: RXc + 0.42, y: gy - 0.04, w: RW - 0.52, h: 0.32,
      fontFace: F, fontSize: 7.2, color: BLACK, align: "left", valign: "middle", margin: 0 });
    if (i < 5) s.addShape("line", { x: RXc + 0.12, y: gy + 0.31, w: RW - 0.24, h: 0,
      line: { color: WAIOURU, width: 0.4 } });
  });
  s.addShape("rect", { x: RXc + 0.1, y: 3.78, w: RW - 0.2, h: 0.28,
    fill: { color: MOAWHANGO, transparency: 55 } });
  s.addText("These are normal developmental effects.", { x: RXc + 0.1, y: 3.78,
    w: RW - 0.2, h: 0.28, fontFace: F, fontSize: 6.8, italic: true, bold: true,
    color: SWAMP, align: "center", valign: "middle", margin: 0 });

  // ---- row B: grounds -----------------------------------------------------
  const GY = 4.32;
  bar(L, GY, W, "3. GROUNDS FOR WITHDRAWAL", 0.28);
  const grounds = [
    ["cross", "Medical and safety", "Protects the individual",
      "The participant cannot continue safely because of a medical condition or safety risk."],
    ["brain", "Learning and assessment", "Protects the learning environment",
      "Continued participation by the participant prevents the activity from providing the intended learning and assessment conditions."],
    ["alert", "Conduct", "Protects the activity",
      "The participant refuses to follow lawful instructions or behaves in a way that prevents the safe and effective conduct of the activity."],
  ];
  const gw = (W - 2 * 0.12) / 3;
  grounds.forEach(([ic, name, protects, desc], i) => {
    const gx = L + i * (gw + 0.12);
    s.addShape("rect", { x: gx, y: GY + 0.36, w: gw, h: 1.62, fill: { color: WHITE },
      line: { color: WAIOURU, width: 0.75 } });
    s.addShape("rect", { x: gx + 0.08, y: GY + 0.44, w: 0.19, h: 0.19,
      fill: { color: KAWAKAWA } });
    s.addText(String(i + 1), { x: gx + 0.08, y: GY + 0.44, w: 0.19, h: 0.19,
      fontFace: F, fontSize: 8, bold: true, color: WHITE, align: "center",
      valign: "middle", margin: 0 });
    s.addShape("ellipse", { x: gx + gw / 2 - 0.21, y: GY + 0.44, w: 0.42, h: 0.42,
      fill: { color: SWAMP } });
    s.addImage({ data: I[ic], x: gx + gw / 2 - 0.115, y: GY + 0.535, w: 0.23, h: 0.23 });
    s.addText(name, { x: gx + 0.06, y: GY + 0.9, w: gw - 0.12, h: 0.2,
      fontFace: F, fontSize: 8.2, bold: true, color: SWAMP, align: "center",
      valign: "middle", margin: 0 });
    s.addText(protects, { x: gx + 0.06, y: GY + 1.1, w: gw - 0.12, h: 0.16,
      fontFace: F, fontSize: 6.6, italic: true, color: RED, align: "center",
      valign: "middle", margin: 0 });
    s.addText(desc, { x: gx + 0.12, y: GY + 1.3, w: gw - 0.24, h: 0.64,
      fontFace: F, fontSize: 6.8, color: BLACK, align: "center", valign: "top", margin: 0 });
  });

  // ---- row C: withdrawal test ---------------------------------------------
  const TY = GY + 2.1;
  s.addShape("rect", { x: L, y: TY, w: W, h: 1.0, fill: { color: KAWAKAWA } });
  s.addText("4. THE WITHDRAWAL TEST", { x: L, y: TY + 0.05, w: W, h: 0.18,
    fontFace: F, fontSize: 8.6, bold: true, color: MOAWHANGO, charSpacing: 2,
    align: "center", valign: "middle", margin: 0 });
  s.addText(
    "What specific safety requirement, required activity, or approved learning or assessment objective can no longer be safely or meaningfully achieved, and what evidence shows that reasonable coaching, team adaptation or authorised adjustment will not restore the necessary conditions?",
    { x: L + 0.35, y: TY + 0.24, w: W - 0.7, h: 0.52, fontFace: F, fontSize: 8,
      bold: true, italic: true, color: WHITE, align: "center", valign: "top", margin: 0 });
  s.addText("A slower team, greater workload or frustration alone will not normally meet this threshold.",
    { x: L + 0.35, y: TY + 0.76, w: W - 0.7, h: 0.18, fontFace: F, fontSize: 7,
      italic: true, color: MOAWHANGO, align: "center", valign: "middle", margin: 0 });

  // ---- row D: decision process --------------------------------------------
  const DY = TY + 1.12;
  bar(L, DY, W, "5. DECISION PROCESS", 0.28);
  const steps = [
    ["eye", "Observe and enable",
      "Identify the issue; allow the team a reasonable opportunity to recognise, respond and manage it."],
    ["message", "Intervene and reassess",
      "Provide clear feedback; apply authorised adjustments; reassess whether safe and meaningful participation remains achievable."],
    ["clipboard", "Decide and record",
      "If withdrawal remains necessary, staff provide observations and a recommendation to the designated uniformed authority."],
  ];
  const sw = 2.25, sgap = (W - 3 * sw) / 2;
  steps.forEach(([ic, name, desc], i) => {
    const sx = L + i * (sw + sgap);
    s.addShape("ellipse", { x: sx, y: DY + 0.4, w: 0.34, h: 0.34,
      fill: { color: WHITE }, line: { color: SWAMP, width: 1.25 } });
    s.addImage({ data: I[ic], x: sx + 0.07, y: DY + 0.47, w: 0.2, h: 0.2 });
    s.addText([
      { text: `${i + 1}.  `, options: { color: RED, bold: true } },
      { text: name, options: { color: SWAMP, bold: true } },
    ], { x: sx + 0.4, y: DY + 0.38, w: sw - 0.4, h: 0.18, fontFace: F,
      fontSize: 7.8, align: "left", valign: "middle", margin: 0 });
    s.addText(desc, { x: sx + 0.4, y: DY + 0.56, w: sw - 0.42, h: 0.66,
      fontFace: F, fontSize: 6.3, color: BLACK, align: "left", valign: "top", margin: 0 });
    if (i < 2) s.addText("►", { x: sx + sw - 0.04, y: DY + 0.44, w: sgap + 0.08,
      h: 0.24, fontFace: F, fontSize: 10, bold: true, color: RED, align: "center",
      valign: "middle", margin: 0 });
  });
  s.addShape("rect", { x: L, y: DY + 1.28, w: W, h: 0.32,
    fill: { color: MOAWHANGO, transparency: 55 } });
  s.addText([
    { text: "Non-immediate withdrawal:  ", options: { bold: true, color: SWAMP } },
    { text: "CI NZALC and CI NCO School discuss the case; CI NZALC recommends withdrawal to COMDT ACS for confirmation.",
      options: { color: BLACK } },
  ], { x: L + 0.15, y: DY + 1.28, w: W - 0.3, h: 0.32, fontFace: F, fontSize: 7.4,
    align: "left", valign: "middle", margin: 0 });

  // ---- row E: immediate withdrawal | record of decision -------------------
  const EY = DY + 1.74, EH = 1.72;
  const LW2 = 3.3, RX2 = L + LW2 + 0.17, RW2 = R - RX2;
  bar(L, EY, LW2, "6. IMMEDIATE WITHDRAWAL", 0.26, SWAMP, 7.8);
  s.addShape("rect", { x: L, y: EY + 0.26, w: LW2, h: EH - 0.26,
    fill: { color: MOAWHANGO, transparency: 72 } });
  s.addImage({ data: I.shieldAlert, x: L + 0.14, y: EY + 0.42, w: 0.34, h: 0.34 });
  s.addText(
    "An instructor, safety staff member or medical practitioner may immediately stop or withdraw a participant to manage an immediate safety or medical risk, informing CI NZALC and CI NCO School as soon as practicable.",
    { x: L + 0.6, y: EY + 0.38, w: LW2 - 0.75, h: EH - 0.5, fontFace: F,
      fontSize: 7.3, color: BLACK, align: "left", valign: "top", margin: 0 });

  bar(RX2, EY, RW2, "7. RECORD OF DECISION", 0.26, SWAMP, 7.8);
  s.addShape("rect", { x: RX2, y: EY + 0.26, w: RW2, h: EH - 0.26,
    fill: { color: WHITE }, line: { color: WAIOURU, width: 0.75 } });
  const rec = [
    "Ground for withdrawal and relevant requirement or objective",
    "Observed evidence and any medical restriction",
    "Coaching, adaptations or authorised adjustments attempted",
    "Why the issue exceeded normal developmental friction",
    "Who recommended and who confirmed the withdrawal",
    "Effect on assessment and continued course participation",
  ];
  rec.forEach((t, i) => {
    const ry = EY + 0.33 + i * 0.225;
    s.addText("✓", { x: RX2 + 0.1, y: ry, w: 0.18, h: 0.2, fontFace: F,
      fontSize: 8, bold: true, color: RED, align: "left", valign: "middle", margin: 0 });
    s.addText(t, { x: RX2 + 0.3, y: ry, w: RW2 - 0.42, h: 0.2, fontFace: F,
      fontSize: 6.7, color: BLACK, align: "left", valign: "middle", margin: 0 });
  });

  await pres.writeFile({ fileName: "output/withdrawal-sop-visual.pptx" });
  console.log("written output/withdrawal-sop-visual.pptx");
})();
