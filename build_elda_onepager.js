// ELDA COMMAND : one-page capability brief for an external unit enquiry.
// Content drawn from the 1RNZIR ELDA Command participant workbook
// (NZ Army Leadership Centre, version Jan 26).

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
    "ELDA Command develops leaders who can perform, adapt and influence others under operational pressure. Rather " +
    "than teaching leadership in a classroom, it exposes leadership behaviour through demanding physical, mental and " +
    "interpersonal challenge, then converts that experience into lasting behavioural change. Every participant leaves " +
    "with a written Leadership Development Plan grounded in observed behaviour rather than self-perception.",
    { x: L, y: 1.9, w: W, h: 0.74, fontFace: F, fontSize: 10, color: BLACK,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });

  // ---- why it works -------------------------------------------------------
  s.addShape("rect", { x: L, y: 2.72, w: 0.05, h: 0.46, fill: { color: RED } });
  s.addText(
    "Leadership behaviour is most accurately revealed under sustained pressure, uncertainty and fatigue. ELDA " +
    "deliberately creates those conditions, then uses structured reflection and peer feedback to convert experience " +
    "into enduring behavioural change.",
    { x: L + 0.18, y: 2.7, w: W - 0.18, h: 0.52, fontFace: F, fontSize: 9.6,
      italic: true, color: SWAMP, align: "left", valign: "top", margin: 0,
      lineSpacingMultiple: 1.1 });

  // ---- aim ----------------------------------------------------------------
  s.addShape("roundRect", { x: L, y: 3.28, w: W, h: 0.66, rectRadius: 0.06, fill: { color: SWAMP } });
  s.addText("AIM", { x: L + 0.22, y: 3.35, w: 1.2, h: 0.18, fontFace: F, fontSize: 8,
    bold: true, color: MOAWHANGO, charSpacing: 1.6, align: "left", valign: "middle", margin: 0 });
  s.addText(
    "To develop leaders who can consistently perform, adapt and influence others under pressure, while strengthening " +
    "individual effectiveness and collective team performance.",
    { x: L + 0.22, y: 3.54, w: W - 0.44, h: 0.34, fontFace: F, fontSize: 9.6,
      color: WHITE, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });

  // ---- learning outcomes --------------------------------------------------
  s.addText("LEARNING OUTCOMES", { x: L, y: 4.02, w: W, h: 0.2, fontFace: F,
    fontSize: 8.5, bold: true, color: SWAMP, charSpacing: 1.4, align: "left",
    valign: "middle", margin: 0 });

  const outcomes = [
    ["1", "PERFORMANCE MINDSET", "Build the mental skills to perform and decide under pressure."],
    ["2", "THE ACTIVITY", "Lead and follow through a genuinely demanding serial."],
    ["3", "DEVELOPMENT PLAN", "Transfer observed behaviour into command effectiveness."],
  ];
  const oGap = 0.14, oW = (W - 2 * oGap) / 3;
  outcomes.forEach(([n, t, d], i) => {
    const x = L + i * (oW + oGap);
    s.addShape("roundRect", { x, y: 4.24, w: oW, h: 0.76, rectRadius: 0.06,
      fill: { color: MOAWHANGO, transparency: 55 },
      line: { color: MOAWHANGO, width: 1 } });
    s.addShape("ellipse", { x: x + 0.14, y: 4.34, w: 0.22, h: 0.22, fill: { color: SWAMP } });
    s.addText(n, { x: x + 0.14, y: 4.34, w: 0.22, h: 0.22, fontFace: F, fontSize: 8,
      bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(t, { x: x + 0.42, y: 4.34, w: oW - 0.56, h: 0.22, fontFace: F,
      fontSize: 8.6, bold: true, color: SWAMP, align: "left", valign: "middle", margin: 0 });
    s.addText(d, { x: x + 0.14, y: 4.58, w: oW - 0.28, h: 0.4, fontFace: F,
      fontSize: 8.4, color: BLACK, align: "left", valign: "top", margin: 0,
      lineSpacingMultiple: 1.1 });
  });

  // ---- the performance cycle ---------------------------------------------
  s.addText("HOW IT IS STRUCTURED: THE PERFORMANCE CYCLE", { x: L, y: 5.1, w: W, h: 0.2,
    fontFace: F, fontSize: 8.5, bold: true, color: SWAMP, charSpacing: 1.4,
    align: "left", valign: "middle", margin: 0 });

  const cycle = [
    ["PREPARE", SWAMP,
     ["Leadership Personality Report: a Five Factor profile of behaviour day to day, under pressure, and the drivers behind it.",
      "Identify the behaviours that will help and hinder performance.",
      "Select the mental skills to be used during the activity."]],
    ["PERFORM", KAWAKAWA,
     ["Execute the activity as a team under sustained physical and mental load.",
      "Apply the selected behaviours and mental skills in real time.",
      "Peers observe leadership behaviour continuously, in context."]],
    ["RECOVER", WAIOURU,
     ["Structured self and peer feedback, written then delivered face to face.",
      "Systematic self-reflection on the hardest moments of the activity.",
      "Build the Leadership Development Plan and keep, stop, start Game Plan."]],
  ];
  const cGap = 0.14, cW = (W - 2 * cGap) / 3;
  cycle.forEach(([title, colour, items], i) => {
    const x = L + i * (cW + cGap);
    s.addShape("rect", { x, y: 5.32, w: cW, h: 0.26, fill: { color: colour } });
    s.addText(title, { x, y: 5.32, w: cW, h: 0.26, fontFace: F, fontSize: 9.5,
      bold: true, color: WHITE, charSpacing: 1.6, align: "center", valign: "middle", margin: 0 });
    s.addText(items.map((t) => ({ text: t, options: { bullet: { characterCode: "2022", indent: 10 }, breakLine: true } })), {
      x: x + 0.02, y: 5.63, w: cW - 0.04, h: 1.22, fontFace: F, fontSize: 8.2,
      color: BLACK, align: "left", valign: "top", margin: 0, paraSpaceAfter: 4,
      lineSpacingMultiple: 1.1 });
  });

  // ---- what is covered ----------------------------------------------------
  s.addText("WHAT IS COVERED", { x: L, y: 7.0, w: W, h: 0.2, fontFace: F,
    fontSize: 8.5, bold: true, color: SWAMP, charSpacing: 1.4, align: "left",
    valign: "middle", margin: 0 });

  const modules = [
    ["Leadership fundamentals",
     "Command, management and leadership as distinct functions. The four pillars of trust: competence, predictability, benevolence and integrity. Identity against reputation, and the four competency domains."],
    ["Leadership Personality Report",
     "A validated Five Factor instrument reporting day to day behaviour, behaviour under pressure or with the guard down, and the needs and drivers behind it."],
    ["Self and peer feedback",
     "Every participant gives and receives specific behavioural feedback on one strength to sustain and one behaviour to adapt, evidenced by what was observed during the activity."],
    ["Performance under pressure",
     "Red head and blue head, performance as potential less interference, and a mental-skills set: noticing, grounding, tactical breathing, self-talk, visualisation, chunking and recovery habits."],
    ["Leadership Development Plan",
     "Three leadership behaviours to sustain and three to adapt, converted into keep, stop and start strategies that are effective, actionable and observable, then disclosed to the team."],
  ];
  let my = 7.22;
  modules.forEach(([t, d]) => {
    s.addShape("rect", { x: L, y: my + 0.04, w: 0.045, h: 0.14, fill: { color: RED } });
    s.addText(t, { x: L + 0.14, y: my, w: 2.05, h: 0.22, fontFace: F, fontSize: 8.8,
      bold: true, color: SWAMP, align: "left", valign: "top", margin: 0 });
    s.addText(d, { x: L + 2.24, y: my, w: R - L - 2.24, h: 0.44, fontFace: F,
      fontSize: 8.2, color: BLACK, align: "left", valign: "top", margin: 0,
      lineSpacingMultiple: 1.1 });
    my += 0.46;
  });

  // ---- what a unit gets back ----------------------------------------------
  s.addShape("roundRect", { x: L, y: 9.56, w: W, h: 0.9, rectRadius: 0.06,
    fill: { color: MOAWHANGO, transparency: 62 } });
  s.addText("WHAT A UNIT GETS BACK", { x: L + 0.22, y: 9.63, w: W - 0.44, h: 0.2,
    fontFace: F, fontSize: 8.5, bold: true, color: SWAMP, charSpacing: 1.4,
    align: "left", valign: "middle", margin: 0 });
  const gets = [
    "Leadership behaviour assessed under real load, not self-reported.",
    "Each leader holds peer evidence of how their behaviour actually lands.",
    "Every leader returns with a written plan for behavioural adaptation.",
    "Nested in the NZDF Leadership Framework, Lead Self to Lead Organisation.",
  ];
  const gGap = 0.2, gW = (W - 0.44 - gGap) / 2;
  gets.forEach((t, i) => {
    const x = L + 0.22 + (i % 2) * (gW + gGap);
    const y = 9.85 + Math.floor(i / 2) * 0.29;
    s.addText([{ text: t, options: { bullet: { characterCode: "2022", indent: 10 } } }], {
      x, y, w: gW, h: 0.27, fontFace: F, fontSize: 8.1, color: BLACK,
      align: "left", valign: "top", margin: 0 });
  });

  // ---- credibility --------------------------------------------------------
  s.addShape("rect", { x: L, y: 10.56, w: W, h: 0.54, fill: { color: WHITE },
    line: { color: SWAMP, width: 0.75 } });
  s.addText([
    { text: "DELIVERED BY THE NZ ARMY LEADERSHIP CENTRE.  ",
      options: { bold: true, color: SWAMP, charSpacing: 0.6 } },
    { text: "ELDA Command is developed and delivered by the NZ Army Leadership Centre as part of the " +
            "Army Command School. It integrates validated psychometrics, evidence-based performance psychology and " +
            "experiential leadership development within the NZDF Leadership Framework.",
      options: { color: BLACK } },
  ], { x: L + 0.18, y: 10.63, w: W - 0.36, h: 0.42, fontFace: F, fontSize: 8.2,
       align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });

  // ---- close --------------------------------------------------------------
  s.addText(
    "NZALC welcomes the opportunity to tailor an ELDA Command serial to 2nd Commando Regiment's operational context " +
    "and leadership priorities. Initial scoping would confirm participant profile, activity design, delivery model " +
    "and support requirements.",
    { x: L, y: 11.18, w: W, h: 0.34, fontFace: F, fontSize: 8.6, color: BLACK,
      align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });

  await pres.writeFile({ fileName: "output/elda-command-onepager.pptx" });
  console.log("written output/elda-command-onepager.pptx");
})();
