// NZALC MONTHLY OUTCOMES — OCTOBER 2026
// A4 portrait poster: a monthly vision board, editable in PowerPoint.
//   node build_nzalc_monthly_outcomes.js
//   -> output/nzalc-monthly-outcomes-october-2026.pptx (then PDF via LibreOffice)

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const OUT = "output/nzalc-monthly-outcomes-october-2026.pptx";
const LOGO = "assets/nz-army-logo.png";

// NZ Army palette
const RED = "C62026", GOLD = "A89662", SWAMP = "002516", CHARCOAL = "222222";
const MOAWHANGO = "CDD2B7", PALE = "EEF1E5", FAINT = "F6F6F3", MID = "8A8A8A", WHITE = "FFFFFF";
const F = "Arial";

// ---- content -------------------------------------------------------------
const TITLE = "NZALC MONTHLY OUTCOMES";
const MONTH = "OCTOBER 2026";
const PURPOSE = "To align the Centre around the outcomes that matter most this month: delivering our immediate commitments while deliberately improving how NZALC operates.";
const END_STATE = "By 31 October, NZALC will have delivered its priority training outputs to the required standard and made tangible progress toward stronger, more effective future delivery.";
const DELIVER = {
  title: "DELIVER THE BUSINESS",
  sub: "Deliver the Centre's core outputs.",
  items: [
    ["Lead Leaders delivered", "The Lead Leaders course is delivered to the required standard, with all associated administration and reporting completed."],
    ["Lead Integrated Capability delivered", "The Lead Integrated Capability course is delivered to the required standard, with lessons and follow-up actions captured."],
  ],
};
const IMPROVE = {
  title: "IMPROVE THE BUSINESS",
  sub: "Leave the Centre stronger than it began the month.",
  items: [
    ["Course data sheets redrafted", "A complete draft set of NZALC course data sheets has been reviewed, updated and prepared for endorsement."],
    ["Amendment pathway confirmed", "Required changes have been confirmed with the relevant stakeholders, with responsibilities and approval pathways clearly established."],
  ],
};
const PRINCIPLE = "CONTINUOUS IMPROVEMENT";
const TEST = "We delivered what was required, and NZALC finishes the month stronger than it started.";

// ---- line icons (SVG -> PNG) ---------------------------------------------
const ICONS = {
  deliver: (ink) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <circle cx="128" cy="128" r="96" fill="none" stroke="#${ink}" stroke-width="14"/>
    <polyline points="78,132 114,168 182,96" fill="none" stroke="#${ink}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`,
  improve: (ink) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
    <polyline points="34,196 96,134 140,170 222,72" fill="none" stroke="#${ink}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
    <polyline points="166,66 226,66 226,126" fill="none" stroke="#${ink}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`,
};
async function svgPng(svg, px = 512) {
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
async function logoData() {
  const buf = await sharp(LOGO).trim().png().toBuffer();
  const meta = await sharp(buf).metadata();
  return { data: "image/png;base64," + buf.toString("base64"), ratio: meta.width / meta.height };
}

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "NZALC Monthly Outcomes, October 2026";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.6, W = 7.07, R = L + W;
  const t = (text, o) => s.addText(text, Object.assign({ fontFace: F, margin: 0 }, o));

  // markings, quiet
  t("UNCLASSIFIED", { x: 0, y: 0.16, w: 8.27, h: 0.16, align: "center", fontSize: 6.5, bold: true, color: MID });
  t("UNCLASSIFIED", { x: 0, y: 11.36, w: 8.27, h: 0.16, align: "center", fontSize: 6.5, bold: true, color: MID });

  // header
  const logo = await logoData();
  const lh = 0.28;
  s.addImage({ data: logo.data, x: L, y: 0.5, w: lh * logo.ratio, h: lh });
  t("NEW ZEALAND ARMY LEADERSHIP CENTRE", { x: L, y: 1.0, w: W, h: 0.2, fontSize: 8, bold: true, color: SWAMP, charSpacing: 3 });
  t(TITLE, { x: L, y: 1.22, w: W, h: 0.5, fontSize: 27, bold: true, color: CHARCOAL, charSpacing: 1 });
  t(MONTH, { x: L, y: 1.7, w: W, h: 0.5, fontSize: 27, bold: true, color: SWAMP, charSpacing: 1 });
  s.addShape("rect", { x: L, y: 2.3, w: W, h: 0.045, fill: { color: RED }, line: { color: RED, width: 0 } });

  // purpose and end state, side by side
  const colW = (W - 0.4) / 2;
  t("PURPOSE", { x: L, y: 2.5, w: colW, h: 0.18, fontSize: 7, bold: true, color: GOLD, charSpacing: 2.5 });
  t(PURPOSE, { x: L, y: 2.7, w: colW, h: 0.75, fontSize: 9.5, color: CHARCOAL, valign: "top", lineSpacingMultiple: 1.15 });
  t("OCTOBER END STATE", { x: L + colW + 0.4, y: 2.5, w: colW, h: 0.18, fontSize: 7, bold: true, color: GOLD, charSpacing: 2.5 });
  t(END_STATE, { x: L + colW + 0.4, y: 2.7, w: colW, h: 0.75, fontSize: 9.5, bold: true, color: SWAMP, valign: "top", lineSpacingMultiple: 1.15 });

  // the two fields
  const PY = 3.7, PH = 4.95, GAP = 0.24, PW = (W - GAP) / 2;
  const panel = async (x, spec, dark) => {
    const bg = dark ? SWAMP : PALE;
    const fg = dark ? WHITE : CHARCOAL;
    const sub = dark ? MOAWHANGO : SWAMP;
    const body = dark ? PALE : CHARCOAL;
    s.addShape("roundRect", { x, y: PY, w: PW, h: PH, fill: { color: bg }, line: { color: bg, width: 0 }, rectRadius: 0.08 });
    const icon = await svgPng(spec === DELIVER ? ICONS.deliver(dark ? GOLD : SWAMP) : ICONS.improve(dark ? GOLD : SWAMP));
    s.addImage({ data: icon, x: x + 0.28, y: PY + 0.3, w: 0.5, h: 0.5 });
    t(spec.title, { x: x + 0.28, y: PY + 0.92, w: PW - 0.56, h: 0.34, fontSize: 15, bold: true, color: fg, charSpacing: 1 });
    t(spec.sub, { x: x + 0.28, y: PY + 1.26, w: PW - 0.56, h: 0.24, fontSize: 8.5, italic: true, color: sub });
    // hairline under the header
    const rule = dark ? GOLD : MOAWHANGO;
    s.addShape("rect", { x: x + 0.28, y: PY + 1.62, w: PW - 0.56, h: 0.012, fill: { color: rule }, line: { color: rule, width: 0 } });
    let y = PY + 1.78;
    spec.items.forEach(([head, text], i) => {
      t(`0${i + 1}`, { x: x + 0.28, y, w: 0.6, h: 0.4, fontSize: 24, bold: true, color: GOLD });
      t(head, { x: x + 0.28, y: y + 0.42, w: PW - 0.56, h: 0.46, fontSize: 12.5, bold: true, color: fg, valign: "top", lineSpacingMultiple: 1.05 });
      t(text, { x: x + 0.28, y: y + 0.9, w: PW - 0.56, h: 0.55, fontSize: 8.5, color: body, valign: "top", lineSpacingMultiple: 1.2 });
      y += 1.5;
    });
  };
  await panel(L, DELIVER, true);
  await panel(L + PW + GAP, IMPROVE, false);

  // the connecting principle: forward movement across both fields
  const BY = PY + PH + 0.28;
  s.addShape("line", { x: L, y: BY + 0.16, w: W, h: 0, line: { color: GOLD, width: 1.25 } });
  for (let i = 0; i < 3; i++) {
    const cx = L + 0.95 + i * 0.28;
    s.addShape("chevron", { x: cx, y: BY + 0.06, w: 0.14, h: 0.2, fill: { color: GOLD }, line: { color: GOLD, width: 0 } });
    const cx2 = R - 0.95 - 0.14 - i * 0.28;
    s.addShape("chevron", { x: cx2, y: BY + 0.06, w: 0.14, h: 0.2, fill: { color: GOLD }, line: { color: GOLD, width: 0 } });
  }
  const labelW = 3.1;
  s.addShape("rect", { x: L + W / 2 - labelW / 2, y: BY, w: labelW, h: 0.32, fill: { color: WHITE }, line: { color: WHITE, width: 0 } });
  t(PRINCIPLE, { x: L + W / 2 - labelW / 2, y: BY, w: labelW, h: 0.32, align: "center", valign: "middle", fontSize: 9.5, bold: true, color: SWAMP, charSpacing: 3 });

  // month-end test
  const TY = BY + 0.7, TH = 1.05;
  s.addShape("roundRect", { x: L, y: TY, w: W, h: TH, fill: { color: CHARCOAL }, line: { color: CHARCOAL, width: 0 }, rectRadius: 0.06 });
  t("MONTH-END TEST", { x: L + 0.32, y: TY + 0.18, w: W - 0.64, h: 0.18, fontSize: 7, bold: true, color: GOLD, charSpacing: 2.5 });
  t(TEST, { x: L + 0.32, y: TY + 0.4, w: W - 0.64, h: 0.55, fontSize: 14.5, bold: true, color: WHITE, valign: "top", lineSpacingMultiple: 1.1 });

  // footer
  t("New Zealand Army Leadership Centre  ·  Army Command School", { x: L, y: 11.12, w: 4.5, h: 0.16, fontSize: 6.5, color: MID });
  t("Monthly outcomes  ·  October 2026", { x: R - 3, y: 11.12, w: 3, h: 0.16, align: "right", fontSize: 6.5, color: MID });

  await pres.writeFile({ fileName: OUT });
  console.log("Saved " + OUT);
})();
