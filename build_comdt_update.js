// NZALC 43311 : FY26/27 month 1 financial position, one page for COMDT ACS.
//
// The command assessment and the outlook are the CO's, carried through as
// written. What is added is the two items that are structural rather than
// timing, held under a watch heading so the monitoring position stands.

const pptxgen = require("pptxgenjs");

const RED = "D31145", BLACK = "000000", WHITE = "FFFFFF";
const AMBER = "B3A650", G_DARK = "00261B";
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
    s.addText(t, { x: L, y, w: W, h: 0.18, fontFace: F, fontSize: 7.4, bold: true,
      color: INK, charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L, y: y + 0.19, w: W, h: 0.008, fill: { color: RULE } });
    return y + 0.34;
  };
  const para = (y, t, w = W, x = L, size = 9, h = 0.8) =>
    s.addText(t, { x, y, w, h, fontFace: F, fontSize: size, color: INK, align: "left",
      valign: "top", margin: 0, lineSpacingMultiple: 1.24 });

  // ---- header -------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.4, w: 1.5, h: 1.5 / AR });
  s.addText("NZ Army Leadership Centre", { x: R - 3, y: 0.4, w: 3, h: 0.22, fontFace: F,
    fontSize: 9, bold: true, color: INK, align: "right", valign: "middle", margin: 0 });
  s.addText("For COMDT ACS", { x: R - 3, y: 0.6, w: 3, h: 0.18, fontFace: F, fontSize: 7.6,
    color: GREY, align: "right", valign: "middle", margin: 0 });

  s.addText("FY26/27 Month 1 Financial Position", { x: L, y: 0.94, w: W - 1.6, h: 0.34,
    fontFace: F, fontSize: 19, bold: true, color: INK, align: "left", valign: "middle", margin: 0 });
  s.addText("Reporting period July 2026   ·   Cost centre 43311", { x: L, y: 1.28, w: W - 1.6,
    h: 0.2, fontFace: F, fontSize: 9, color: GREY, align: "left", valign: "middle", margin: 0 });

  // status
  s.addShape("rect", { x: R - 1.5, y: 0.98, w: 1.5, h: 0.44, fill: { color: AMBER } });
  s.addText("STATUS", { x: R - 1.5, y: 1.02, w: 1.5, h: 0.14, fontFace: F, fontSize: 6,
    bold: true, color: INK, charSpacing: 1, align: "center", valign: "middle", margin: 0 });
  s.addText("GREEN–AMBER", { x: R - 1.5, y: 1.16, w: 1.5, h: 0.22, fontFace: F,
    fontSize: 11, bold: true, color: INK, align: "center", valign: "middle", margin: 0 });

  s.addShape("rect", { x: L, y: 1.56, w: W, h: 0.018, fill: { color: INK } });

  // ---- headline figures ---------------------------------------------------
  let y = 1.78;
  const TILES = [
    ["FY BUDGET", "$811.6k", "SAP full year plan"],
    ["JULY ACTUAL", "$40.5k", "against a $23.0k profile"],
    ["BUDGET CONSUMED", "5.0%", "of the annual plan"],
    ["JULY VARIANCE", "$17.5k", "ahead of profile"],
  ];
  const TW = (W - 3 * 0.14) / 4;
  TILES.forEach(([k, v, note], i) => {
    const x = L + i * (TW + 0.14);
    s.addShape("rect", { x, y, w: TW, h: 1.02, fill: { color: PAPER } });
    s.addShape("rect", { x, y, w: TW, h: 0.028, fill: { color: i === 3 ? AMBER : INK } });
    s.addText(k, { x: x + 0.14, y: y + 0.12, w: TW - 0.28, h: 0.16, fontFace: F, fontSize: 6.2,
      bold: true, color: GREY, charSpacing: 0.8, align: "left", valign: "middle", margin: 0 });
    s.addText(v, { x: x + 0.14, y: y + 0.32, w: TW - 0.28, h: 0.34, fontFace: F, fontSize: 18,
      bold: true, color: INK, align: "left", valign: "middle", margin: 0 });
    s.addText(note, { x: x + 0.14, y: y + 0.68, w: TW - 0.28, h: 0.28, fontFace: F,
      fontSize: 6.8, color: GREY, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });
  });
  y += 1.26;

  // ---- position -----------------------------------------------------------
  y = head(y, "POSITION AT 31 JULY 2026");
  const COLS = [3.0, 1.35, 1.35, 1.33];
  const ROWS = [
    ["", "July budget", "July actual", "Variance", true],
    ["Personnel", "$300", "$6,031", "($5,731)", false],
    ["Operating", "$22,715", "$34,504", "($11,789)", false],
    ["TOTAL", "$23,015", "$40,535", "($17,520)", false],
  ];
  ROWS.forEach(([a, b, c, d, isHead], i) => {
    const isTotal = i === ROWS.length - 1;
    const rh = 0.32;
    if (isTotal) s.addShape("rect", { x: L, y, w: W, h: rh, fill: { color: PAPER } });
    let x = L;
    [a, b, c, d].forEach((t, j) => {
      s.addText(t, { x: x + (j ? 0 : 0.1), y, w: COLS[j] - (j ? 0.1 : 0), h: rh, fontFace: F,
        fontSize: isHead ? 7.4 : 9.2, bold: isHead || isTotal,
        color: isHead ? GREY : (j === 3 && !isHead ? RED : INK),
        charSpacing: isHead ? 0.8 : 0,
        align: j ? "right" : "left", valign: "middle", margin: 0 });
      x += COLS[j];
    });
    s.addShape("rect", { x: L, y: y + rh, w: W, h: isHead || isTotal ? 0.012 : 0.006,
      fill: { color: isHead || isTotal ? INK : RULE } });
    y += rh + 0.04;
  });
  y += 0.18;

  // ---- assessment ---------------------------------------------------------
  y = head(y, "MONTH 1 ASSESSMENT");
  para(y, "July expenditure was $17.5k ahead of the SAP monthly profile. This is assessed primarily as an expenditure timing and phasing variance rather than an emerging structural overspend. July was effectively a preparation period ahead of the FY26/27 delivery programme, with no programmed NZALC courses conducted during the month. The first three activities commence on 8, 24 and 31 August, and July expenditure is broadly consistent with the preparation, movement, procurement and enabling activity required ahead of them.", W, L, 9, 0.94);
  y += 0.98;
  para(y, "The FY26/27 budget has been increased by $50k for Winsborough support, bringing the SAP full year plan to $811.6k. That uplift is correctly reflected in SAP, and the full year plan otherwise reconciles to the NZALC budget.", W, L, 9, 0.5);
  y += 0.58;

  // ---- watch items --------------------------------------------------------
  y = head(y, "UNDER WATCH");
  const WATCH = [
    ["Cost elements carrying no budget", "$6.1k", 0.62,
     "Civilian overtime and sundry expenses were incurred against lines that hold nil for the year. This is a coding or budget-line question rather than a phasing one, and is to be resolved with the Financial Adviser."],
    ["Civilian allowance run rate", "53%", 0.44,
     "Just over half the $5.3k annual line was drawn in month 1. The rate is to be confirmed before the position compounds."],
  ];
  WATCH.forEach(([t, v, rh, d]) => {
    s.addShape("rect", { x: L, y, w: 0.035, h: rh, fill: { color: AMBER } });
    s.addText(t, { x: L + 0.16, y, w: W - 1.2, h: 0.2, fontFace: F, fontSize: 9.2, bold: true,
      color: INK, align: "left", valign: "middle", margin: 0 });
    s.addText(v, { x: R - 1.1, y, w: 1.1, h: 0.2, fontFace: F, fontSize: 9.6, bold: true,
      color: INK, align: "right", valign: "middle", margin: 0 });
    para(y + 0.21, d, W - 0.3, L + 0.16, 8.4, 0.42);
    y += rh + 0.1;
  });
  y += 0.06;

  // ---- outlook ------------------------------------------------------------
  y = head(y, "OUTLOOK");
  para(y, "At the completion of Month 1 there is no clear indication of underlying FY budget pressure. The July variance will be monitored through August, with the combined July and August position providing a more meaningful assessment of expenditure against the programmed delivery profile.", W, L, 9, 0.56);
  y += 0.64;

  // ---- command assessment -------------------------------------------------
  y = head(y, "COMMAND ASSESSMENT");
  s.addShape("rect", { x: L, y, w: W, h: 0.96, fill: { color: INK } });
  s.addShape("rect", { x: L, y, w: 0.05, h: 0.96, fill: { color: AMBER } });
  s.addText("FY26/27 budget remains on track. July expenditure is $17.5k ahead of the monthly profile; this is assessed predominantly as front-loaded expenditure associated with preparation for the August course programme rather than a structural overspend. Current expenditure represents approximately 5 per cent of the annual budget, with no immediate corrective action required beyond continued monitoring.", {
    x: L + 0.28, y: y + 0.14, w: W - 0.56, h: 0.7, fontFace: F, fontSize: 9.2, color: WHITE,
    align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.24 });

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
