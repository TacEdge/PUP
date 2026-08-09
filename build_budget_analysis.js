// NZALC 43311 : FY26/27 month 1 budget analysis.
//
// July 26 actuals against the SAP phased budget, and the SAP full year plan
// reconciled to the NZALC FY26/27 Budget Summary.
//
// Charts: polarity is carried by POSITION against a zero datum and by signed
// direct labels on every bar. Colour is tertiary. The Army red/olive pair
// clears the normal-vision and contrast checks but sits in the 6-8 CVD band,
// which is legal only with that secondary encoding, so it is always present.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RED = "D31145", BLACK = "000000", WHITE = "FFFFFF";
const OLIVE = "444D06", G_DARK = "00261B", G_LIGHT = "DFD8AD";
const INK = "1A1A1A", GREY = "6E6E6E", RULE = "C8C8C8", PAPER = "F5F5F3";
const F = "Arial";
const LOGO = "assets/nz-army-logo.png";
const AR = 4.380;

const money = (n, dp = 0) =>
  (n < 0 ? "-$" : "$") + Math.abs(n).toLocaleString("en-NZ",
    { minimumFractionDigits: dp, maximumFractionDigits: dp });
const signed = (n) => (n >= 0 ? "+" : "-") + "$" +
  Math.abs(n).toLocaleString("en-NZ", { maximumFractionDigits: 0 });

async function svg(body, w, h, px) {
  const s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}">` +
    `<rect width="${w}" height="${h}" fill="#${WHITE}"/>${body}</svg>`;
  const buf = await sharp(Buffer.from(s)).resize(px, Math.round((px * h) / w)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
// SVG is XML: ampersands in cost element names must be escaped.
const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const txt = (x, y, t, size, o = {}) =>
  `<text x="${x}" y="${y}" font-family="Arial" font-size="${size}" fill="#${o.fill || INK}"` +
  (o.bold ? ' font-weight="bold"' : "") + (o.anchor ? ` text-anchor="${o.anchor}"` : "") +
  (o.track ? ` letter-spacing="${o.track}"` : "") + `>${esc(t)}</text>`;

// ---- the data --------------------------------------------------------------
const JUL_BUDGET = 23015, JUL_ACTUAL = 40534.98;
const FY_PLAN = 811626, NZALC_BUDGET = 761477, WINSBOROUGH = 50000;
const FORECAST = 829147.17;

// July variance by cost element, budget less actual. Negative is overspend.
// ce, name, July phased budget, July actual, SAP full year plan
const VAR = [
  ["6520", "Travel", 2688, 8738.90, 198815],
  ["7395", "Sundry expenses", 0, 3217.28, 0],
  ["7191", "Computer hardware", 0, 3133.46, 5376],
  ["6020", "Civilian overtime", 0, 2847.27, 0],
  ["7120", "Food", 607, 3426.59, 112102],
  ["6010", "Civilian allowances", 300, 2808.94, 5260],
  ["7370", "Rental of equipment", 353, 2660.76, 53124],
  ["7100", "Fuel", 213, 1290.63, 16284],
  ["7345", "Vehicle licences", 0, 1006.92, 2450],
  ["7140", "Publications & stationery", 600, 1161.43, 17318],
  ["6252", "RF activity allowances", 0, 375.01, 113250],
  ["7290", "Professional fees", 113, 0, 56551],
  ["7040", "Medical supplies", 200, 0.06, 800],
  ["6950", "Rentals & licences", 1448, 779.59, 17376],
  ["7065", "Clothing", 2400, 1684.56, 26400],
  ["7010", "Equipment & spares", 9174, 2509.23, 36699],
].map(([ce, name, b, a, fy]) => ({ ce, name, b, a, fy, v: b - a, share: fy ? a / fy : null }));

// ---- variance chart --------------------------------------------------------
function varianceChart() {
  const W = 1500, rowH = 46, top = 92, H = top + VAR.length * rowH + 66;
  const zero = 800, span = 380, scale = span / 7000;   // px per dollar
  const rows = [...VAR].sort((p, q) => p.v - q.v);
  const bot = top + rows.length * rowH - 8;

  let body =
      txt(zero - 16, 44, "OVER BUDGET", 19, { anchor: "end", fill: RED, bold: true, track: 2 })
    + txt(zero + 16, 44, "UNDER BUDGET", 19, { fill: OLIVE, bold: true, track: 2 })
    + txt(1352, 44, "ANNUAL PLAN", 16, { anchor: "end", fill: GREY, track: 1.4 })
    + txt(1478, 44, "SPENT", 16, { anchor: "end", fill: GREY, track: 1.4 });

  for (let g = -6000; g <= 6000; g += 2000) {
    if (g === 0) continue;
    const x = zero + g * scale;
    body += `<line x1="${x}" y1="${top - 16}" x2="${x}" y2="${bot}" stroke="#EAEAEA" stroke-width="2"/>`
      + txt(x, bot + 30, `${g > 0 ? "" : "-"}$${Math.abs(g) / 1000}k`, 17, { anchor: "middle", fill: GREY });
  }

  rows.forEach((r, i) => {
    const cy = top + i * rowH + rowH / 2 - 6;
    const w = Math.max(Math.abs(r.v) * scale, 2), adverse = r.v < 0;
    const x = adverse ? zero - w : zero;
    body += txt(24, cy + 6, r.ce, 17, { fill: GREY })
      + txt(100, cy + 6, r.name, 19)
      + `<rect x="${x}" y="${cy - 12}" width="${w}" height="24" rx="5" fill="#${adverse ? RED : OLIVE}"/>`
      + txt(adverse ? x - 14 : x + w + 14, cy + 6, signed(r.v), 18,
            { anchor: adverse ? "end" : "start", bold: true })
      + txt(1352, cy + 6, r.fy ? money(r.fy) : "no budget", 17,
            { anchor: "end", fill: r.fy ? GREY : RED, bold: !r.fy })
      + txt(1478, cy + 6, r.share === null ? "\u2014" : `${(r.share * 100).toFixed(0)}%`, 17,
            { anchor: "end", fill: r.share > 0.25 ? RED : GREY, bold: r.share > 0.25 });
  });

  body += `<line x1="${zero}" y1="${top - 22}" x2="${zero}" y2="${bot + 6}" stroke="#${INK}" stroke-width="4"/>`;
  return { body, w: W, h: H };
}

// ---- reconciliation bridge -------------------------------------------------
function bridgeChart() {
  const W = 1500, H = 300, base = 208, top = 44;
  const scale = (base - top) / FY_PLAN;
  const steps = [
    ["NZALC budget\nFY26/27", NZALC_BUDGET, G_DARK, "total"],
    ["Winsborough\nuplift", WINSBOROUGH, OLIVE, "step"],
    ["Line\nreallocation", 151, GREY, "step"],
    ["SAP full year\nplan", FY_PLAN, BLACK, "total"],
  ];
  const BW = 210, GAP = (W - 120 - steps.length * BW) / (steps.length - 1);
  let body = "", x = 60, run = 0;
  steps.forEach(([label, v, c, kind]) => {
    const isTotal = kind === "total";
    const h = isTotal ? v * scale : Math.max(v * scale, 4);
    const y = isTotal ? base - h : base - run * scale - h;
    body += `<rect x="${x}" y="${y}" width="${BW}" height="${h}" rx="4" fill="#${c}"/>`
      + txt(x + BW / 2, y - 14, isTotal ? money(v) : signed(v), 21, { anchor: "middle", bold: true })
      + label.split("\n").map((l, j) =>
          txt(x + BW / 2, base + 34 + j * 26, l, 19, { anchor: "middle", fill: GREY })).join("");
    run = isTotal ? v : run + v;
    x += BW + GAP;
  });
  body += `<line x1="40" y1="${base}" x2="${W - 40}" y2="${base}" stroke="#${INK}" stroke-width="4"/>`;
  return { body, w: W, h: H };
}

// ---------------------------------------------------------------------------
(async () => {
  const mk = async (o, px) => svg(o.body, o.w, o.h, px);
  const I = { variance: await mk(varianceChart(), 1700), bridge: await mk(bridgeChart(), 1700) };

  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "NZALC FY26/27 Month 1 Budget Analysis";
  pres.company = "NZ Army Leadership Centre";

  const L = 0.62, W = 7.03, R = L + W;
  let PAGE = 0;

  function page(title, strap) {
    PAGE += 1;
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addImage({ path: LOGO, x: L, y: 0.4, w: 1.5, h: 1.5 / AR });
    s.addText("NZ Army Leadership Centre", { x: R - 3, y: 0.42, w: 3, h: 0.22, fontFace: F,
      fontSize: 9, bold: true, color: INK, align: "right", valign: "middle", margin: 0 });
    s.addText("Cost centre 43311", { x: R - 3, y: 0.62, w: 3, h: 0.18, fontFace: F,
      fontSize: 7.6, color: GREY, align: "right", valign: "middle", margin: 0 });
    s.addText(title, { x: L, y: 0.92, w: W, h: 0.32, fontFace: F, fontSize: 18, bold: true,
      color: INK, align: "left", valign: "middle", margin: 0 });
    s.addText(strap, { x: L, y: 1.24, w: W - 0.3, h: 0.42, fontFace: F, fontSize: 9.2,
      color: GREY, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.2 });
    s.addShape("rect", { x: L, y: 1.72, w: W, h: 0.018, fill: { color: INK } });
    s.addText("FY26/27 MONTH 1 BUDGET ANALYSIS", { x: L, y: 11.16, w: 4, h: 0.16, fontFace: F,
      fontSize: 6, color: GREY, charSpacing: 0.6, align: "left", valign: "middle", margin: 0 });
    s.addText(`JULY 2026   |   PAGE ${PAGE} OF 2`, { x: R - 3, y: 11.16, w: 3, h: 0.16,
      fontFace: F, fontSize: 6, color: GREY, charSpacing: 0.6, align: "right", valign: "middle", margin: 0 });
    return s;
  }
  const head = (s, y, t) => {
    s.addText(t, { x: L, y, w: W, h: 0.18, fontFace: F, fontSize: 7.4, bold: true, color: INK,
      charSpacing: 1.2, align: "left", valign: "middle", margin: 0 });
    s.addShape("rect", { x: L, y: y + 0.19, w: W, h: 0.008, fill: { color: RULE } });
    return y + 0.32;
  };
  const body = (s, x, y, w, t, size = 8.8, colour = "3E3E3E", h = 0.6) =>
    s.addText(t, { x, y, w, h, fontFace: F, fontSize: size, color: colour, align: "left",
      valign: "top", margin: 0, lineSpacingMultiple: 1.22 });

  // =========================================================================
  // PAGE 1 : the month
  // =========================================================================
  {
    const s = page("July 2026 against budget",
      "Month 1 of FY26/27. Source: SAP financial management report 43311, July 26, and the NZALC FY26/27 Budget Summary.");

    let y = 1.94;
    const TILES = [
      ["SAP JULY BUDGET", money(JUL_BUDGET), "phased, no courses in July", INK],
      ["JULY ACTUAL", money(JUL_ACTUAL), "176% of the phased budget", RED],
      ["VARIANCE", signed(JUL_BUDGET - JUL_ACTUAL), "adverse", RED],
      ["OF THE ANNUAL PLAN", "5.0%", "a straight twelfth is 8.3%", INK],
    ];
    const TW = (W - 3 * 0.14) / 4;
    TILES.forEach(([k, v, note, c], i) => {
      const x = L + i * (TW + 0.14);
      s.addShape("rect", { x, y, w: TW, h: 1.08, fill: { color: PAPER } });
      s.addShape("rect", { x, y, w: TW, h: 0.03, fill: { color: c } });
      s.addText(k, { x: x + 0.14, y: y + 0.12, w: TW - 0.28, h: 0.16, fontFace: F, fontSize: 6.4,
        bold: true, color: GREY, charSpacing: 0.8, align: "left", valign: "middle", margin: 0 });
      s.addText(v, { x: x + 0.14, y: y + 0.34, w: TW - 0.28, h: 0.34, fontFace: F, fontSize: 17,
        bold: true, color: c, align: "left", valign: "middle", margin: 0 });
      s.addText(note, { x: x + 0.14, y: y + 0.7, w: TW - 0.28, h: 0.3, fontFace: F, fontSize: 6.8,
        color: GREY, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });
    });
    y += 1.3;

    y = head(s, y, "THE FINDING");
    body(s, L, y, W,
      "July delivered no training. The first activity of the year, Ser 01 LSYS NCO Advanced, begins in August. The phased budget recognises this: July carries 2.8 per cent of the annual plan, well under a straight twelfth. Actual spend was 5.0 per cent of the annual plan, so the centre consumed roughly two months of budget in a month with no course output.",
      9.2, INK, 0.6);
    y += 0.66;

    y = head(s, y, "JULY VARIANCE BY COST ELEMENT");
    const ch = varianceChart();
    s.addImage({ data: I.variance, x: L, y, w: W, h: W * ch.h / ch.w });
    y += W * ch.h / ch.w + 0.16;
    body(s, L, y, W,
      "Budget less actual. Bars left of the datum are overspends. The right-hand columns show the full year plan and the share of it already spent in month one; a straight twelfth would be 8 per cent.",
      7.8, GREY, 0.3);
  }

  // =========================================================================
  // PAGE 2 : the year
  // =========================================================================
  {
    const s = page("The year, and what July implies",
      "Reconciliation of the SAP full year plan to the NZALC budget, the exposures July has surfaced, and what needs a decision.");

    let y = head(s, 1.94, "RECONCILIATION  —  THE TWO PLANS AGREE");
    const bc = bridgeChart();
    s.addImage({ data: I.bridge, x: L, y, w: W, h: W * bc.h / bc.w });
    y += W * bc.h / bc.w + 0.1;
    body(s, L, y, W,
      "The two plans differ by $50,151. The $50,000 Winsborough uplift accounts for almost all of it, loaded correctly to CE 7290 Professional Fees, which carries $56,551 in SAP against $6,350 in the budget. The rest is line reallocation, chiefly travel down $3,770 offset by training fees up $3,414. Note that the budget summary is internally inconsistent by $150: its cover states variable costs of $502,584, its cost element table $502,434. Against the cover figure the two plans reconcile to $1.",
      8.8, INK, 0.8);
    y += 0.92;

    y = head(s, y, "THREE EXPOSURES JULY HAS SURFACED");
    const EXP = [
      ["Spending against cost elements with no budget", money(6064.55),
        "Civilian overtime $2,847 and sundry expenses $3,217 were incurred against lines that carry zero for the year. These are not phasing differences; there is no budget behind them at any point in FY26/27. If they continue at anything like July's rate the annual exposure is material.", RED],
      ["Annual lines largely consumed in month 1", money(6949.32),
        "Civilian allowances at 53 per cent of the annual line, computer hardware at 58 per cent and vehicle licences at 41 per cent. Some of this is legitimately front-loaded, licences and hardware are typically annual purchases, but civilian allowances at over half the year in month one is a run-rate question, not a timing one.", RED],
      ["The forecast is arithmetic, not judgement", money(FORECAST - FY_PLAN),
        "The full year forecast outturn of $829,147 is simply the July variance added to the remaining phased budget. It assumes every future month lands exactly on plan. It is not a re-forecast and should not be read as one.", INK],
    ];
    EXP.forEach(([t, v, d, c]) => {
      s.addShape("rect", { x: L, y, w: 0.04, h: 0.88, fill: { color: c } });
      s.addText(t, { x: L + 0.18, y, w: W - 1.6, h: 0.22, fontFace: F, fontSize: 9.6, bold: true,
        color: INK, align: "left", valign: "middle", margin: 0 });
      s.addText(v, { x: R - 1.5, y, w: 1.5, h: 0.22, fontFace: F, fontSize: 10.4, bold: true,
        color: c, align: "right", valign: "middle", margin: 0 });
      body(s, L + 0.18, y + 0.24, W - 0.28, d, 8.4, "3E3E3E", 0.64);
      y += 0.97;
    });

    y = head(s, y, "WHAT NEEDS A DECISION");
    const ASKS = [
      ["Establish where overtime and sundry spend belongs", "Either a budget line is created for CE 6020 and CE 7395, or the spend is reallocated to the cost elements that should carry it. Running a year against zero-budget lines will distort every month's variance from here."],
      ["Confirm whether the civilian allowance rate is correct", "At July's rate the $5,260 annual line is exhausted by September. Either the rate is wrong or the budget is."],
      ["Populate the report narrative", "The activities conducted, risks, reprioritisation account and CO's comment fields are all blank, and there is no commentary against any variance. A month 1 report with a 76 per cent overspend and no explanation invites the wrong questions."],
      ["Re-forecast after the first courses complete", "August and September carry seven activities. Actual course costs against the per-course budget will be the first real test of the variable-cost assumptions, and the point at which a genuine re-forecast becomes possible."],
    ];
    ASKS.forEach(([t, d], i) => {
      s.addShape("ellipse", { x: L, y: y + 0.02, w: 0.26, h: 0.26, fill: { color: RED } });
      s.addText(String(i + 1), { x: L, y: y + 0.02, w: 0.26, h: 0.26, fontFace: F, fontSize: 7.6,
        bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
      s.addText(t, { x: L + 0.4, y, w: W - 0.4, h: 0.2, fontFace: F, fontSize: 9, bold: true,
        color: INK, align: "left", valign: "middle", margin: 0 });
      body(s, L + 0.4, y + 0.2, W - 0.5, d, 8.2, "3E3E3E", 0.4);
      y += 0.63;
    });
  }

  await pres.writeFile({ fileName: "output/nzalc-fy2627-month1-analysis.pptx" });
  console.log("written output/nzalc-fy2627-month1-analysis.pptx");
})();
