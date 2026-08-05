// ELDA COMMAND : one-page capability brief for an external unit enquiry.
// Content drawn from the 1RNZIR ELDA Command participant workbook
// (NZ Army Leadership Centre, version Jan 26).
//
// Each section does one job: the opening states the outcome, the aim states
// the effect, the outcome cards signpost, the cycle explains the method, the
// content list evidences it, and the closing panels answer why NZALC and
// what next. Space freed by the brevity pass is left as white space.

const pptxgen = require("pptxgenjs");

const RED = "C62026", BLACK = "000000", WHITE = "FFFFFF";
const SWAMP = "002516", KAWAKAWA = "3A4B00", WAIOURU = "A89662", MOAWHANGO = "CDD2B7";
const GREY = "7F7F7F";
const F = "Arial";
const LOGO = "/tmp/claude-0/-home-user-PUP/2d4cec0e-a52e-5368-bb54-803c6f37698d/scratchpad/logo-trimmed.png";

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: "A4P", width: 8.27, height: 11.69 });
  pres.layout = "A4P";
  pres.title = "ELDA Command";
  pres.company = "NZ Army Leadership Centre";
  pres.subject = "Experiential Leadership Development Activity";
  const s = pres.addSlide();
  s.background = { color: WHITE };

  const L = 0.5, W = 7.27, R = L + W;

  // ---- header -------------------------------------------------------------
  s.addImage({ path: LOGO, x: L, y: 0.36, w: 1.72, h: 0.416 });
  s.addText("ELDA COMMAND", {
    x: L, y: 0.88, w: W, h: 0.42, fontFace: F, fontSize: 25, bold: true,
    color: BLACK, align: "left", valign: "middle", margin: 0 });
  s.addText("Experiential Leadership Development Activity", {
    x: L, y: 1.28, w: W, h: 0.22, fontFace: F, fontSize: 11.5,
    color: SWAMP, align: "left", valign: "middle", margin: 0 });
  s.addText("NZ Army Leadership Centre  |  Army Command School", {
    x: L, y: 1.5, w: W - 1.6, h: 0.2, fontFace: F, fontSize: 8.5, italic: true,
    color: GREY, align: "left", valign: "middle", margin: 0 });
  s.addText("August 2026", { x: R - 1.6, y: 1.5, w: 1.6, h: 0.2, fontFace: F,
    fontSize: 8.5, color: GREY, align: "right", valign: "middle", margin: 0 });
  s.addShape("rect", { x: L, y: 1.76, w: W, h: 0.028, fill: { color: RED } });

  // ---- operational outcome ------------------------------------------------
  s.addText(
    "ELDA Command develops leaders to perform, adapt and influence under operational pressure. Participants lead and " +
    "follow through a demanding physical, mental and interpersonal activity. Observed behaviour, peer feedback and " +
    "structured reflection are converted into a written Leadership Development Plan.",
    { x: L, y: 1.96, w: W, h: 0.56, fontFace: F, fontSize: 10, color: BLACK,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });

  // ---- aim ----------------------------------------------------------------
  s.addShape("roundRect", { x: L, y: 2.72, w: W, h: 0.44, rectRadius: 0.06, fill: { color: SWAMP } });
  s.addText("AIM", { x: L + 0.22, y: 2.72, w: 0.6, h: 0.44, fontFace: F, fontSize: 8,
    bold: true, color: MOAWHANGO, charSpacing: 1.6, align: "left", valign: "middle", margin: 0 });
  s.addText(
    "Strengthen individual command effectiveness and collective team performance under pressure.",
    { x: L + 0.86, y: 2.72, w: W - 1.08, h: 0.44, fontFace: F, fontSize: 9.6,
      color: WHITE, align: "left", valign: "middle", margin: 0 });

  // ---- learning outcomes --------------------------------------------------
  s.addText("LEARNING OUTCOMES", { x: L, y: 3.4, w: W, h: 0.2, fontFace: F,
    fontSize: 8.5, bold: true, color: SWAMP, charSpacing: 1.4, align: "left",
    valign: "middle", margin: 0 });

  const outcomes = [
    ["1", "PERFORM UNDER PRESSURE"],
    ["2", "LEAD UNDER LOAD"],
    ["3", "ADAPT BEHAVIOUR"],
  ];
  const oGap = 0.14, oW = (W - 2 * oGap) / 3;
  outcomes.forEach(([n, t], i) => {
    const x = L + i * (oW + oGap);
    s.addShape("roundRect", { x, y: 3.62, w: oW, h: 0.46, rectRadius: 0.06,
      fill: { color: MOAWHANGO, transparency: 55 },
      line: { color: MOAWHANGO, width: 1 } });
    s.addShape("ellipse", { x: x + 0.14, y: 3.74, w: 0.22, h: 0.22, fill: { color: SWAMP } });
    s.addText(n, { x: x + 0.14, y: 3.74, w: 0.22, h: 0.22, fontFace: F, fontSize: 8,
      bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(t, { x: x + 0.4, y: 3.62, w: oW - 0.48, h: 0.46, fontFace: F,
      fontSize: 8.8, bold: true, color: SWAMP, align: "left", valign: "middle", margin: 0 });
  });

  // ---- the performance cycle ---------------------------------------------
  s.addText("THE PERFORMANCE CYCLE", { x: L, y: 4.36, w: W, h: 0.2,
    fontFace: F, fontSize: 8.5, bold: true, color: SWAMP, charSpacing: 1.4,
    align: "left", valign: "middle", margin: 0 });

  const cycle = [
    ["PREPARE", SWAMP,
     ["Profile everyday and under-pressure behaviour and personal drivers.",
      "Identify behaviours that will help or hinder performance.",
      "Select mental skills for the activity."]],
    ["PERFORM", KAWAKAWA,
     ["Lead and follow as a team under sustained physical and mental load.",
      "Apply selected behaviours and mental skills in real time.",
      "Observe peer leadership behaviour in context."]],
    ["RECOVER", WAIOURU,
     ["Give and receive structured face-to-face feedback.",
      "Reflect on critical moments during the activity.",
      "Build a Leadership Development Plan and keep, stop, start Game Plan."]],
  ];
  const cGap = 0.14, cW = (W - 2 * cGap) / 3;
  cycle.forEach(([title, colour, items], i) => {
    const x = L + i * (cW + cGap);
    s.addShape("rect", { x, y: 4.58, w: cW, h: 0.28, fill: { color: colour } });
    s.addText(title, { x, y: 4.58, w: cW, h: 0.28, fontFace: F, fontSize: 9.5,
      bold: true, color: WHITE, charSpacing: 1.6, align: "center", valign: "middle", margin: 0 });
    s.addText(items.map((t) => ({ text: t, options: { bullet: { characterCode: "2022", indent: 10 }, breakLine: true } })), {
      x: x + 0.02, y: 4.94, w: cW - 0.04, h: 1.06, fontFace: F, fontSize: 8.2,
      color: BLACK, align: "left", valign: "top", margin: 0, paraSpaceAfter: 5,
      lineSpacingMultiple: 1.1 });
  });

  // ---- what is covered ----------------------------------------------------
  s.addText("WHAT IS COVERED", { x: L, y: 6.3, w: W, h: 0.2, fontFace: F,
    fontSize: 8.5, bold: true, color: SWAMP, charSpacing: 1.4, align: "left",
    valign: "middle", margin: 0 });

  const modules = [
    ["Leadership fundamentals",
     "Command, management and leadership; trust; identity and reputation; and the four competency domains."],
    ["Leadership Personality Report",
     "A validated Five Factor profile of everyday behaviour, behaviour under pressure, and underlying needs and drivers."],
    ["Self and peer feedback",
     "One strength to sustain and one behaviour to adapt, supported by evidence observed during the activity."],
    ["Performance under pressure",
     "Red head and blue head, performance as potential less interference, and practical mental skills including tactical breathing, self-talk, visualisation, chunking and recovery."],
    ["Leadership Development Plan",
     "Three behaviours to sustain and three to adapt, converted into observable keep, stop and start actions."],
  ];
  let my = 6.56;
  modules.forEach(([t, d]) => {
    s.addShape("rect", { x: L, y: my + 0.04, w: 0.045, h: 0.14, fill: { color: RED } });
    s.addText(t, { x: L + 0.14, y: my, w: 2.05, h: 0.22, fontFace: F, fontSize: 8.8,
      bold: true, color: SWAMP, align: "left", valign: "top", margin: 0 });
    s.addText(d, { x: L + 2.24, y: my, w: R - L - 2.24, h: 0.42, fontFace: F,
      fontSize: 8.4, color: BLACK, align: "left", valign: "top", margin: 0,
      lineSpacingMultiple: 1.1 });
    my += 0.46;
  });

  // ---- what a unit gets back ----------------------------------------------
  s.addShape("roundRect", { x: L, y: 9.06, w: W, h: 0.8, rectRadius: 0.06,
    fill: { color: MOAWHANGO, transparency: 62 } });
  s.addText("WHAT A UNIT GETS BACK", { x: L + 0.22, y: 9.15, w: W - 0.44, h: 0.2,
    fontFace: F, fontSize: 8.5, bold: true, color: SWAMP, charSpacing: 1.4,
    align: "left", valign: "middle", margin: 0 });
  const gets = [
    "Leadership behaviour evidenced under real load.",
    "Peer feedback on how each leader affects others.",
    "A written plan for behavioural adaptation.",
    "Alignment with the NZDF Leadership Framework.",
  ];
  const gGap = 0.2, gW = (W - 0.44 - gGap) / 2;
  gets.forEach((t, i) => {
    const x = L + 0.22 + (i % 2) * (gW + gGap);
    const y = 9.4 + Math.floor(i / 2) * 0.24;
    s.addText([{ text: t, options: { bullet: { characterCode: "2022", indent: 10 } } }], {
      x, y, w: gW, h: 0.22, fontFace: F, fontSize: 8.4, color: BLACK,
      align: "left", valign: "top", margin: 0 });
  });

  // ---- credibility --------------------------------------------------------
  s.addShape("rect", { x: L, y: 10.24, w: W, h: 0.42, fill: { color: WHITE },
    line: { color: SWAMP, width: 0.75 } });
  s.addText([
    { text: "DELIVERED BY NZALC.  ", options: { bold: true, color: SWAMP, charSpacing: 0.6 } },
    { text: "ELDA Command is delivered by the NZ Army Leadership Centre as part of the Army Command " +
            "School, integrating validated psychometrics, performance psychology and experiential leadership development.",
      options: { color: BLACK } },
  ], { x: L + 0.18, y: 10.24, w: W - 0.36, h: 0.42, fontFace: F, fontSize: 8.4,
       align: "left", valign: "middle", margin: 0, lineSpacingMultiple: 1.1 });

  // ---- next step ----------------------------------------------------------
  s.addText("NEXT STEP", { x: L, y: 10.86, w: W, h: 0.2, fontFace: F,
    fontSize: 8.5, bold: true, color: SWAMP, charSpacing: 1.4, align: "left",
    valign: "middle", margin: 0 });
  s.addText(
    "Scope a tailored 2027 ELDA Command serial for 2nd Commando Regiment, confirming participant profile, activity " +
    "design, delivery model and support requirements.",
    { x: L, y: 11.08, w: W, h: 0.32, fontFace: F, fontSize: 8.8, color: BLACK,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });

  await pres.writeFile({ fileName: "output/elda-command-onepager.pptx" });
  console.log("written output/elda-command-onepager.pptx");
})();
