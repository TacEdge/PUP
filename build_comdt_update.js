// NZALC 43311 : FY26/27 month 1 financial position, one page for COMDT ACS.
//
// Copy is the CO's, tightened so each section says one thing once. The
// Outlook section is deliberately absent: it repeated the command
// assessment, which now stands alone as the conclusion.

const pptxgen = require("pptxgenjs");

const RED = "D31145", WHITE = "FFFFFF";
const AMBER = "B3A650";
const INK = "1A1A1A", GREY = "6E6E6E", RULE = "C8C8C8", PAPER = "F5F5F3";
const F = "Arial";
const LOGO = "assets/nz-army-logo.png";
const AR = 4.380;

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "NZALC FY26/27 Month 1 Financial Position";
  pres.subject = "Month 1 financial position for COMDT ACS";
  pres.company = "NZ Army Leadership Centre";

  const s = pres.addSlide();
  s.background = { color: WHITE };
  const L = 0.62, W = 7.03, R = L + W;

  const head = (y, t) => {
    s.addText(t, { x: L, y, w: W, h: 0.18, fontFace: F, fontSize: 7.6, bold: true,
      color: INK, charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L, y: y + 0.19, w: W, h: 0.008, fill: { color: RULE } });
    return y + 0.36;
  };
  const para = (y, t, h, x = L, w = W, size = 9.6) =>
    s.addText(t, { x, y, w, h, fontFace: F, fontSize: size, color: INK, align: "left",
      valign: "top", margin: 0, lineSpacingMultiple: 1.26 });

  // ---- header -------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.4, w: 1.5, h: 1.5 / AR });
  s.addText("NZ Army Leadership Centre", { x: R - 3, y: 0.4, w: 3, h: 0.22, fontFace: F,
    fontSize: 9, bold: true, color: INK, align: "right", valign: "middle", margin: 0 });
  s.addText("For COMDT ACS", { x: R - 3, y: 0.6, w: 3, h: 0.18, fontFace: F, fontSize: 7.6,
    color: GREY, align: "right", valign: "middle", margin: 0 });

  s.addText("FY26/27 Month 1 Financial Position", { x: L, y: 0.94, w: W - 1.7, h: 0.36,
    fontFace: F, fontSize: 20, bold: true, color: INK, align: "left", valign: "middle", margin: 0 });
  s.addText("Reporting period July 2026   ·   Cost centre 43311", { x: L, y: 1.3, w: W - 1.7,
    h: 0.2, fontFace: F, fontSize: 9, color: GREY, align: "left", valign: "middle", margin: 0 });

  s.addShape("rect", { x: R - 1.55, y: 0.98, w: 1.55, h: 0.46, fill: { color: AMBER } });
  s.addText("STATUS", { x: R - 1.55, y: 1.02, w: 1.55, h: 0.15, fontFace: F, fontSize: 6,
    bold: true, color: INK, charSpacing: 1, align: "center", valign: "middle", margin: 0 });
  s.addText("GREEN–AMBER", { x: R - 1.55, y: 1.17, w: 1.55, h: 0.23, fontFace: F,
    fontSize: 11.5, bold: true, color: INK, align: "center", valign: "middle", margin: 0 });

  s.addShape("rect", { x: L, y: 1.58, w: W, h: 0.018, fill: { color: INK } });

  // ---- headline figures ---------------------------------------------------
  const TY = 2.0, TH = 1.24;
  const TILES = [
    ["FY BUDGET", "$811.6k", "SAP full-year plan, includes $50k Winsborough"],
    ["JULY ACTUAL", "$40.5k", "against $23.0k profile"],
    ["BUDGET CONSUMED", "5.0%", "of the annual plan"],
    ["JULY VARIANCE", "$17.5k", "ahead of profile"],
  ];
  const TW = (W - 3 * 0.14) / 4;
  TILES.forEach(([k, v, note], i) => {
    const x = L + i * (TW + 0.14);
    s.addShape("rect", { x, y: TY, w: TW, h: TH, fill: { color: PAPER } });
    s.addShape("rect", { x, y: TY, w: TW, h: 0.03, fill: { color: i === 3 ? AMBER : INK } });
    s.addText(k, { x: x + 0.15, y: TY + 0.14, w: TW - 0.3, h: 0.16, fontFace: F, fontSize: 6.4,
      bold: true, color: GREY, charSpacing: 0.8, align: "left", valign: "middle", margin: 0 });
    s.addText(v, { x: x + 0.15, y: TY + 0.38, w: TW - 0.3, h: 0.38, fontFace: F, fontSize: 20,
      bold: true, color: INK, align: "left", valign: "middle", margin: 0 });
    s.addText(note, { x: x + 0.15, y: TY + 0.82, w: TW - 0.3, h: 0.36, fontFace: F,
      fontSize: 7, color: GREY, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });
  });

  // ---- position -----------------------------------------------------------
  let y = head(3.76, "POSITION AT 31 JULY 2026");
  const COLS = [3.0, 1.35, 1.35, 1.33];
  const ROWS = [
    ["", "July Budget", "July Actual", "Variance", true],
    ["Personnel", "$300", "$6,031", "($5,731)", false],
    ["Operating", "$22,715", "$34,504", "($11,789)", false],
    ["TOTAL", "$23,015", "$40,535", "($17,520)", false],
  ];
  ROWS.forEach(([a, b, c, d, isHead], i) => {
    const isTotal = i === ROWS.length - 1, rh = 0.44;
    if (isTotal) s.addShape("rect", { x: L, y, w: W, h: rh, fill: { color: PAPER } });
    let x = L;
    [a, b, c, d].forEach((t, j) => {
      s.addText(t, { x: x + (j ? 0 : 0.1), y, w: COLS[j] - (j ? 0.1 : 0), h: rh, fontFace: F,
        fontSize: isHead ? 7.6 : 9.8, bold: isHead || isTotal,
        color: isHead ? GREY : (j === 3 ? RED : INK), charSpacing: isHead ? 0.8 : 0,
        align: j ? "right" : "left", valign: "middle", margin: 0 });
      x += COLS[j];
    });
    s.addShape("rect", { x: L, y: y + rh, w: W, h: isHead || isTotal ? 0.012 : 0.006,
      fill: { color: isHead || isTotal ? INK : RULE } });
    y += rh + 0.04;
  });

  // ---- under watch --------------------------------------------------------
  y = head(6.34, "UNDER WATCH");
  const WATCH = [
    ["Nil-budget cost lines", "$6.1k", 0.6,
     "Civilian overtime and sundry expenses require coding and budget-line confirmation with the Financial Adviser."],
    ["Civilian allowances", "53% consumed", 0.48,
     "Run rate to be confirmed before Month 2."],
  ];
  WATCH.forEach(([t, v, rh, d]) => {
    s.addShape("rect", { x: L, y, w: 0.04, h: rh, fill: { color: AMBER } });
    s.addText(t, { x: L + 0.18, y, w: W - 1.6, h: 0.22, fontFace: F, fontSize: 9.6, bold: true,
      color: INK, align: "left", valign: "middle", margin: 0 });
    s.addText(v, { x: R - 1.5, y, w: 1.5, h: 0.22, fontFace: F, fontSize: 9.8, bold: true,
      color: INK, align: "right", valign: "middle", margin: 0 });
    para(y + 0.24, d, 0.3, L + 0.18, W - 0.36, 9);
    y += rh + 0.22;
  });

  // ---- command assessment -------------------------------------------------
  y = head(8.66, "MONTH 1 COMMAND ASSESSMENT");
  s.addShape("rect", { x: L, y, w: W, h: 1.34, fill: { color: INK } });
  s.addShape("rect", { x: L, y, w: 0.055, h: 1.34, fill: { color: AMBER } });
  s.addText("FY26/27 remains on track. July's $17.5k adverse variance is assessed predominantly as front-loaded expenditure supporting the August course programme, rather than an emerging budget pressure. No corrective action is required at this stage beyond monitoring the combined July and August position.", {
    x: L + 0.34, y: y + 0.24, w: W - 0.68, h: 0.9, fontFace: F, fontSize: 10.4, color: WHITE,
    align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.28 });

  // ---- footer -------------------------------------------------------------
  s.addShape("rect", { x: L, y: 11.08, w: W, h: 0.008, fill: { color: RULE } });
  s.addText("NZ ARMY LEADERSHIP CENTRE   ·   COST CENTRE 43311", { x: L, y: 11.16, w: 4.5,
    h: 0.16, fontFace: F, fontSize: 6, color: GREY, charSpacing: 0.6, align: "left",
    valign: "middle", margin: 0 });
  s.addText("SOURCE: SAP FINANCIAL MANAGEMENT REPORT, JULY 26", { x: R - 4, y: 11.16, w: 4,
    h: 0.16, fontFace: F, fontSize: 6, color: GREY, charSpacing: 0.6, align: "right",
    valign: "middle", margin: 0 });

  await pres.writeFile({ fileName: "output/nzalc-month1-comdt-update.pptx" });
  console.log("written output/nzalc-month1-comdt-update.pptx");
})();
