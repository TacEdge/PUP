// ARMY TRAINING GROUP STORYBOARD — redesigned template
// 16:9 PowerPoint template in the NZ Army house style, with a worked example
// and a submission-guidance slide.
//
//   node build_atg_storyboard.js && python3 build_atg_storyboard_finish.py
//   -> output/atg-storyboard-template.pptx (then PDF via convert_pptx_to_pdf.py)
//
// Slide 1 (blank template) is added by the finishing script from the layout,
// so its placeholders show PowerPoint's click-to-add prompts.

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const OUT = "output/atg-storyboard-template.pptx";
const A = "assets/atg-storyboard";
const LOGO = "assets/nz-army-logo-mono.png";

// NZ Army palette
const RED = "C62026", GOLD = "A89662", SWAMP = "002516", BLACK = "000000", INK = "222222";
const MOAWHANGO = "CDD2B7", PALE = "EEF1E5", FAINT = "F6F6F3", GRID = "D9D9D2", MID = "8A8A8A";
const GREY = "5F5F5A", WHITE = "FFFFFF";
const F = "Arial";

// ---- geometry (inches, 10 x 5.625) ---------------------------------------
const W = 10, H = 5.625, M = 0.35;
const HEAD = { x: M, y: 0.22, w: W - 2 * M, h: 0.86 };
const LEFT = { x: M, w: 3.55 };
const GRID_BOX = { x: 4.15, y: 1.3, w: 5.5, h: 3.25, gap: 0.1 };
const PH_W = (GRID_BOX.w - GRID_BOX.gap) / 2;
const PH_H = (GRID_BOX.h - GRID_BOX.gap) / 2;
const PHOTOS = [0, 1, 2, 3].map((i) => ({
  x: GRID_BOX.x + (i % 2) * (PH_W + GRID_BOX.gap),
  y: GRID_BOX.y + Math.floor(i / 2) * (PH_H + GRID_BOX.gap),
  w: PH_W, h: PH_H,
}));
const CAPTION = { x: GRID_BOX.x, y: GRID_BOX.y + GRID_BOX.h + 0.1, w: GRID_BOX.w, h: 0.42 };
// left column: label 0.17, then body; sections separated by 0.1
const SECTIONS = [
  ["01", "INTRODUCTION", "intro", 0.58],
  ["02", "PURPOSE", "purpose", 0.62],
  ["03", "METHOD", "method", 1.02],
  ["04", "END STATE", "endstate", 0.58],
];
const FOOT_Y = 5.28;

// ---- assets ---------------------------------------------------------------
async function png(path, opts = {}) {
  let img = sharp(path);
  if (opts.trim) img = img.trim();
  const buf = await img.png().toBuffer();
  const meta = await sharp(buf).metadata();
  return { data: "image/png;base64," + buf.toString("base64"), ratio: meta.width / meta.height };
}
async function cover(path, w, h) {
  // crop to the placeholder aspect so the photo is never stretched
  const px = 1400;
  const buf = await sharp(path).resize(px, Math.round((px * h) / w), { fit: "cover" }).jpeg({ quality: 82 }).toBuffer();
  return "image/jpeg;base64," + buf.toString("base64");
}
function fitBox(ratio, box) {
  // largest w,h with the given aspect inside box, centred
  let w = box.w, h = w / ratio;
  if (h > box.h) { h = box.h; w = h * ratio; }
  return { x: box.x + (box.w - w) / 2, y: box.y + (box.h - h) / 2, w, h };
}

// ---- shared drawing -------------------------------------------------------
function marker(slide, p, n) {
  const d = 0.26;
  slide.addShape("ellipse", { x: p.x + 0.09, y: p.y + 0.09, w: d, h: d, fill: { color: BLACK }, line: { color: BLACK, width: 0 } });
  slide.addText(String(n), { x: p.x + 0.09, y: p.y + 0.09, w: d, h: d, fontFace: F, fontSize: 8, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
function markers(slide) { PHOTOS.forEach((p, i) => marker(slide, p, i + 1)); }
function section(slide, x, y, num, text, desc) {
  slide.addText([
    { text: num + "  ", options: { color: GOLD, bold: true, fontSize: 10 } },
    { text, options: { color: SWAMP, bold: true, fontSize: 8.5, charSpacing: 2.5 } },
  ], { x, y, w: 6, h: 0.22, fontFace: F, margin: 0, valign: "top", isTextBox: true });
  if (desc) slide.addText(desc, { x: x + 0.28, y: y + 0.2, w: 8, h: 0.2, fontFace: F, fontSize: 8, color: GREY, margin: 0, isTextBox: true });
}

async function build() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "Army Training Group";
  pres.title = "ATG Storyboard";

  const crest = await png(`${A}/atg-crest.png`, { trim: true });
  const logo = await png(LOGO, { trim: true });

  // ---- master: everything a unit must not move lives here ---------------
  const crestBox = fitBox(crest.ratio, { x: HEAD.x + 0.12, y: HEAD.y + 0.09, w: 0.7, h: HEAD.h - 0.18 });
  const tx = HEAD.x + 1.0;
  const tw = HEAD.w - 1.0 - 1.05;
  const objects = [
    { text: { text: "UNCLASSIFIED", options: { x: 0, y: 0.03, w: W, h: 0.16, fontFace: F, fontSize: 7, bold: true, color: BLACK, align: "center", margin: 0 } } },
    { rect: { x: HEAD.x, y: HEAD.y, w: HEAD.w, h: HEAD.h, fill: { color: FAINT }, line: { color: FAINT, width: 0 }, rectRadius: 0.06 } },
    { image: { x: crestBox.x, y: crestBox.y, w: crestBox.w, h: crestBox.h, data: crest.data } },
    { text: { text: "ARMY TRAINING GROUP", options: { x: tx, y: HEAD.y + 0.09, w: tw, h: 0.16, fontFace: F, fontSize: 6.5, bold: true, color: SWAMP, charSpacing: 2.5, margin: 0 } } },
    { placeholder: { options: { name: "unit", type: "title", x: tx, y: HEAD.y + 0.25, w: tw, h: 0.32, fontFace: F, fontSize: 16, bold: true, color: BLACK, align: "left", margin: 0, valign: "middle", fit: "shrink" }, text: "Unit and sub-unit" } },
    { placeholder: { options: { name: "activity", type: "body", x: tx, y: HEAD.y + 0.57, w: tw, h: 0.22, fontFace: F, fontSize: 9, color: GREY, margin: 0, valign: "middle", fit: "shrink" }, text: "Activity name  ·  01 Jan – 31 Jan 20XX" } },
    { placeholder: { options: { name: "badge", type: "pic", x: HEAD.x + HEAD.w - 0.86, y: HEAD.y + 0.08, w: 0.7, h: 0.7 }, text: "Unit badge" } },
    { text: { text: "ATG Storyboard", options: { x: M, y: FOOT_Y, w: 3, h: 0.16, fontFace: F, fontSize: 7, color: GREY, margin: 0 } } },
    { text: { text: "UNCLASSIFIED", options: { x: 0, y: FOOT_Y, w: W, h: 0.16, fontFace: F, fontSize: 7, bold: true, color: BLACK, align: "center", margin: 0 } } },
  ];
  const logoBox = fitBox(logo.ratio, { x: W - M - 1.1, y: FOOT_Y - 0.06, w: 1.1, h: 0.26 });
  objects.push({ image: { x: logoBox.x, y: logoBox.y, w: logoBox.w, h: logoBox.h, data: logo.data } });

  // left column labels and body placeholders
  let y = GRID_BOX.y;
  for (const [num, text, name, h] of SECTIONS) {
    objects.push({ text: { text: num, options: { x: LEFT.x, y, w: 0.25, h: 0.17, fontFace: F, fontSize: 8, bold: true, color: GOLD, margin: 0, valign: "top" } } });
    objects.push({ text: { text, options: { x: LEFT.x + 0.25, y, w: LEFT.w - 0.25, h: 0.17, fontFace: F, fontSize: 7, bold: true, color: SWAMP, charSpacing: 2, margin: 0, valign: "top" } } });
    y += 0.18;
    objects.push({ placeholder: { options: { name, type: "body", x: LEFT.x, y, w: LEFT.w, h, fontFace: F, fontSize: 8.5, color: INK, margin: 0, valign: "top", fit: "shrink", paraSpaceAfter: 3 }, text: `${text.charAt(0)}${text.slice(1).toLowerCase()} text` } });
    y += h + 0.1;
  }
  // photo placeholders and caption line
  PHOTOS.forEach((p, i) => objects.push({ placeholder: { options: { name: `photo${i + 1}`, type: "pic", x: p.x, y: p.y, w: p.w, h: p.h }, text: `Photo ${i + 1}` } }));
  objects.push({ placeholder: { options: { name: "captions", type: "body", x: CAPTION.x, y: CAPTION.y, w: CAPTION.w, h: CAPTION.h, fontFace: F, fontSize: 7.5, color: GREY, margin: 0, valign: "top", fit: "shrink" }, text: "1  Caption   ·   2  Caption   ·   3  Caption   ·   4  Caption" } });

  pres.defineSlideMaster({ title: "ATG_STORYBOARD", background: { color: WHITE }, objects });
  pres.defineSlideMaster({ title: "ATG_PLAIN", background: { color: WHITE }, objects: [
    { text: { text: "UNCLASSIFIED", options: { x: 0, y: 0.03, w: W, h: 0.16, fontFace: F, fontSize: 7, bold: true, color: BLACK, align: "center", margin: 0 } } },
    { text: { text: "ATG Storyboard", options: { x: M, y: FOOT_Y, w: 3, h: 0.16, fontFace: F, fontSize: 7, color: GREY, margin: 0 } } },
    { text: { text: "UNCLASSIFIED", options: { x: 0, y: FOOT_Y, w: W, h: 0.16, fontFace: F, fontSize: 7, bold: true, color: BLACK, align: "center", margin: 0 } } },
    { image: { x: logoBox.x, y: logoBox.y, w: logoBox.w, h: logoBox.h, data: logo.data } },
  ] });

  // ---- slide: worked example (NZALC ELDA Lead Systems) -------------------
  const ex = pres.addSlide({ masterName: "ATG_STORYBOARD" });
  ex.addText("Army Command School  ·  NZ Army Leadership Centre", { placeholder: "unit" });
  ex.addText("ELDA Lead Systems NCO Course  ·  7 – 14 Aug 26", { placeholder: "activity" });
  const badge = await png(`${A}/badge-nz-onward.png`, { trim: true });
  const bb = fitBox(badge.ratio, { x: HEAD.x + HEAD.w - 0.86, y: HEAD.y + 0.08, w: 0.7, h: 0.7 });
  ex.addImage({ data: badge.data, x: bb.x, y: bb.y, w: bb.w, h: bb.h });
  ex.addText("NZALC delivered ELDA Lead Systems to 27 NZ Army and Australian Defence Force personnel from 7 to 14 August 2026. The activity was a three-day rogaine culminating in a whitewater rafting descent.", { placeholder: "intro" });
  ex.addText("To enhance leadership and warrior ethos through the conduct of a challenging multisport activity, supported by leadership tools, psychometrics, reflection and behaviour selection.", { placeholder: "purpose" });
  ex.addText([
    { text: "The rogaine forced planning and execution against incomplete information, giving direct evidence of resilience, judgement and teamwork under pressure.", options: { breakLine: true } },
    { text: "Leadership diagnostics, structured debriefs and individual Leadership Development Plans converted reflection into readiness, building the combat mindset required at lead systems level. Training alongside ADF personnel strengthened joint leadership development ties." },
  ], { placeholder: "method" });
  ex.addText([
    { text: "All personnel completed ELDA Lead Systems. Student evaluations indicate a well-conducted course. ", options: {} },
    { text: "“An excellent course that required a high level of personal drive and commitment, whilst also reinforcing the importance of working as a team towards a common goal.”", options: { italic: true, color: SWAMP } },
  ], { placeholder: "endstate" });
  for (let i = 0; i < 4; i++) {
    const p = PHOTOS[i];
    ex.addImage({ data: await cover(`${A}/example-photo-${i + 1}.jpg`, p.w, p.h), x: p.x, y: p.y, w: p.w, h: p.h });
  }
  markers(ex);
  ex.addText([
    { text: "1  ", options: { bold: true, color: BLACK } }, { text: "Whitewater descent, day three   ·   " },
    { text: "2  ", options: { bold: true, color: BLACK } }, { text: "Lake leg of the rogaine   ·   " },
    { text: "3  ", options: { bold: true, color: BLACK } }, { text: "Night navigation planning   ·   " },
    { text: "4  ", options: { bold: true, color: BLACK } }, { text: "Course group with ADF personnel" },
  ], { placeholder: "captions" });
  // example tag
  ex.addText("EXAMPLE", { x: M + 0.95, y: FOOT_Y - 0.05, w: 0.8, h: 0.24, fontFace: F, fontSize: 7, bold: true, color: GOLD, charSpacing: 2, align: "center", valign: "middle", margin: 0, isTextBox: true, line: { color: GOLD, width: 0.75 }, rectRadius: 0.12 });
  ex.addNotes("Worked example of the ATG storyboard. Content and photographs from the NZALC ELDA Lead Systems NCO Course storyboard; photo captions are illustrative.");

  // ---- slide: how to use it ------------------------------------------------
  const g = pres.addSlide({ masterName: "ATG_PLAIN" });
  g.addText("ATG Storyboard", { x: M, y: 0.32, w: 6, h: 0.42, fontFace: F, fontSize: 20, bold: true, color: BLACK, margin: 0, isTextBox: true });
  g.addText("How to complete and submit the board  ·  template in use from 15 Oct 25", { x: M, y: 0.74, w: 7, h: 0.2, fontFace: F, fontSize: 8, color: GREY, margin: 0, isTextBox: true });

  // submission flow
  section(g, M, 1.18, "01", "SUBMISSION", "The board moves from the unit to ATG Registry, is checked, and is released once approved.");
  const steps = ["Unit", "ATG Registry", "ATG S75 check", "CoS", "Approved", "ATG Registry releases to OLCC"];
  const sy = 1.62, sh = 0.5, sgap = 0.32;
  const sw = (W - 2 * M - sgap * (steps.length - 1)) / steps.length;
  steps.forEach((s, i) => {
    const x = M + i * (sw + sgap);
    const dark = i === steps.length - 1;
    g.addShape("roundRect", { x, y: sy, w: sw, h: sh, fill: { color: dark ? BLACK : FAINT }, line: { color: dark ? BLACK : FAINT, width: 0 }, rectRadius: 0.06 });
    g.addText(s, { x: x + 0.08, y: sy, w: sw - 0.16, h: sh, fontFace: F, fontSize: 8.5, bold: true, color: dark ? WHITE : BLACK, align: "center", valign: "middle", margin: 0, isTextBox: true, fit: "shrink" });
    if (i < steps.length - 1) {
      const ax = x + sw + 0.06;
      g.addShape("line", { x: ax, y: sy + sh / 2, w: sgap - 0.12, h: 0, line: { color: GOLD, width: 1.25, endArrowType: "triangle" } });
    }
  });
  // not-approved branch: CoS -> Not approved -> back to the unit
  const cosX = M + 3 * (sw + sgap);
  const by = sy + sh + 0.3;
  const ux = M + sw / 2;
  g.addShape("line", { x: cosX + sw / 2, y: sy + sh, w: 0, h: by - (sy + sh), line: { color: GOLD, width: 1, dashType: "dash" } });
  g.addShape("roundRect", { x: cosX, y: by, w: sw, h: 0.36, fill: { color: WHITE }, line: { color: GRID, width: 0.75 }, rectRadius: 0.06 });
  g.addText("Not approved", { x: cosX, y: by, w: sw, h: 0.36, fontFace: F, fontSize: 8, color: GREY, align: "center", valign: "middle", margin: 0, isTextBox: true });
  g.addShape("line", { x: ux, y: by + 0.18, w: cosX - ux, h: 0, line: { color: GOLD, width: 1, dashType: "dash" } });
  g.addShape("line", { x: ux, y: sy + sh + 0.04, w: 0, h: by + 0.18 - (sy + sh + 0.04), line: { color: GOLD, width: 1, dashType: "dash", endArrowType: "triangle" }, flipV: true });
  g.addText("Returned to the unit for resubmission", { x: ux + 0.12, y: by + 0.22, w: cosX - ux - 0.2, h: 0.2, fontFace: F, fontSize: 7.5, color: GREY, margin: 0, isTextBox: true });

  // completing the board
  const cy = 3.14;
  section(g, M, cy, "02", "COMPLETING THE BOARD", "Fill each field on the template slide; the frame itself is locked in the layout.");
  const tips = [
    ["Header", "Unit and sub-unit, activity name and dates. Insert your unit badge from the set at right."],
    ["Text", "Introduction, purpose, method and end state. Each field shrinks to fit; keep the board to one page."],
    ["Photos", "Four landscape photos, numbered 1 to 4. Click a frame to insert; PowerPoint crops to fit."],
    ["Captions", "One line beneath the photos, numbered to match. Name the activity, place and date where useful."],
  ];
  const tw2 = 1.35, tgap = 0.12, tipY = cy + 0.5;
  tips.forEach(([h, d], i) => {
    const x = M + i * (tw2 + tgap);
    g.addShape("roundRect", { x, y: tipY, w: tw2, h: 1.32, fill: { color: FAINT }, line: { color: FAINT, width: 0 }, rectRadius: 0.06 });
    g.addText(h, { x: x + 0.12, y: tipY + 0.1, w: tw2 - 0.24, h: 0.2, fontFace: F, fontSize: 9, bold: true, color: BLACK, margin: 0, isTextBox: true });
    g.addText(d, { x: x + 0.12, y: tipY + 0.33, w: tw2 - 0.24, h: 0.95, fontFace: F, fontSize: 7.5, color: INK, margin: 0, valign: "top", isTextBox: true });
  });

  // unit badges
  const bx0 = M + 4 * (tw2 + tgap) + 0.15;
  section(g, bx0, cy, "03", "UNIT BADGES", "Copy your unit's badge into the header.");
  const badges = [["badge-ocs-nz.png", "OCS (NZ)"], ["badge-army-depot.png", "The Army Depot"], ["badge-mctc.png", "MCTC"], ["badge-atg.png", "ATG"], ["badge-lotc.jpg", "LOTC"]];
  const bw = (W - M - bx0 - 0.1 * 4) / 5;
  for (let i = 0; i < badges.length; i++) {
    const [file, name] = badges[i];
    const x = bx0 + i * (bw + 0.1);
    const im = await png(`${A}/${file}`, { trim: true });
    const box = fitBox(im.ratio, { x: x + 0.06, y: tipY + 0.08, w: bw - 0.12, h: 0.72 });
    g.addShape("roundRect", { x, y: tipY, w: bw, h: 1.32, fill: { color: WHITE }, line: { color: GRID, width: 0.75 }, rectRadius: 0.06 });
    g.addImage({ data: im.data, x: box.x, y: box.y, w: box.w, h: box.h });
    g.addText(name, { x, y: tipY + 0.9, w: bw, h: 0.34, fontFace: F, fontSize: 7, color: INK, align: "center", valign: "top", margin: 0, isTextBox: true });
  }
  g.addNotes("Submission flow as issued by ATG on 13 Oct 25. Unit badges carried over from the previous template.");

  await pres.writeFile({ fileName: OUT });
  console.log("wrote", OUT);
}

build().catch((e) => { console.error(e); process.exit(1); });
