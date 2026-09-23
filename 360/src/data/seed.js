// Synthetic demonstration data. Every person here is fictional.
import { allStatements } from "./instrument.js";

// Small deterministic RNG so the seed is identical on every reset.
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const TODAY = "2026-09-23";

// Rating profile: for each statement, a base level per rater group (1–4).
// Deviations from this are jittered per rater to look like real data.
function makeRatings(profile, group, seed, notObservedIds = []) {
  const r = rng(seed);
  const out = {};
  for (const s of allStatements()) {
    if (notObservedIds.includes(s.id)) { out[s.id] = null; continue; }
    const base = (profile[s.id] && profile[s.id][group]) ?? profile[s.id]?.default ?? 3;
    const jitter = r() < 0.3 ? (r() < 0.5 ? -1 : 1) : 0;
    out[s.id] = Math.max(1, Math.min(4, Math.round(base + jitter)));
  }
  return out;
}

// Capt Alex Morgan: strong on teams and composure, softer on inviting
// challenge and seeking other perspectives, self-rates communication higher
// than others do and decisiveness lower than others do.
const alexProfile = {
  s1: { default: 4, self: 4 },
  s2: { default: 3, subordinate: 3, self: 3 },
  s3: { default: 3, self: 4 },
  s4: { default: 4, self: 4 },
  o1: { default: 3, subordinate: 2, self: 4 },
  o2: { default: 3, superior: 4, self: 3 },
  o3: { default: 3, self: 3 },
  o4: { default: 2, superior: 3, self: 3 },
  t1: { default: 4, self: 4 },
  t2: { default: 4, self: 3 },
  t3: { default: 3, superior: 4, self: 3 },
  t4: { default: 4, self: 4 },
  a1: { default: 3, self: 3 },
  a2: { default: 3, self: 3 },
  a3: { default: 2, superior: 3, self: 3 },
};

// WO2 Hana Rewiti: closed 360 with a released report.
const hanaProfile = {
  s1: { default: 3, self: 3 }, s2: { default: 4, self: 3 }, s3: { default: 4, self: 4 }, s4: { default: 4, self: 4 },
  o1: { default: 4, self: 4 }, o2: { default: 4, self: 4 }, o3: { default: 4, superior: 3, self: 3 }, o4: { default: 4, self: 3 },
  t1: { default: 3, self: 4 }, t2: { default: 3, subordinate: 2, self: 4 }, t3: { default: 4, self: 4 }, t4: { default: 3, self: 4 },
  a1: { default: 3, self: 3 }, a2: { default: 4, self: 3 }, a3: { default: 4, self: 3 },
};

const alexSelf = {
  s1: 4, s2: 3, s3: 4, s4: 4, o1: 4, o2: 3, o3: 3, o4: 3, t1: 4, t2: 3, t3: 3, t4: 4, a1: 3, a2: 3, a3: 3,
};
const hanaSelf = {
  s1: 3, s2: 3, s3: 4, s4: 4, o1: 4, o2: 4, o3: 3, o4: 3, t1: 4, t2: 4, t3: 4, t4: 4, a1: 3, a2: 3, a3: 3,
};

export function buildSeed() {
  const courses = [
    { id: "c-elda-ll", name: "ELDA Lead Leaders", startDate: "2026-10-12" },
    { id: "c-jolc", name: "Junior Officer Leadership Course", startDate: "2026-11-02" },
    { id: "c-snco", name: "Senior NCO Leadership Programme", startDate: "2026-08-17" },
  ];

  const participants = [
    { id: "p-alex", rank: "Capt", firstName: "Alex", lastName: "Morgan", unit: "2/1 RNZIR" },
    { id: "p-hana", rank: "WO2", firstName: "Hana", lastName: "Rewiti", unit: "1 NZSAS Regt (Trg)" },
    { id: "p-jordan", rank: "Lt", firstName: "Jordan", lastName: "Blake", unit: "16 Fd Regt" },
    { id: "p-priya", rank: "Sgt", firstName: "Priya", lastName: "Nathan", unit: "2 Engr Regt" },
  ];

  // Raters. `token` is the capability in the rater's link. `status` is
  // invited | completed. Names are fictional.
  const alexRaters = [
    { id: "r-a1", name: "Maj Tom Whitfield", relationship: "superior", status: "completed", token: "alx-sup-1" },
    { id: "r-a2", name: "Maj Sarah Ngata", relationship: "superior", status: "completed", token: "alx-sup-2" },
    { id: "r-a3", name: "Capt Ben Carter", relationship: "peer", status: "completed", token: "alx-peer-1" },
    { id: "r-a4", name: "Capt Mere Tane", relationship: "peer", status: "completed", token: "alx-peer-2" },
    { id: "r-a5", name: "Capt Liam O'Shea", relationship: "peer", status: "completed", token: "alx-peer-3" },
    { id: "r-a6", name: "Capt Ruth Davies", relationship: "peer", status: "invited", token: "alx-peer-4" },
    { id: "r-a7", name: "Sgt Nikau Paora", relationship: "subordinate", status: "completed", token: "alx-sub-1" },
    { id: "r-a8", name: "Cpl Jess Hartley", relationship: "subordinate", status: "completed", token: "alx-sub-2" },
    { id: "r-a9", name: "LCpl Dan Mistry", relationship: "subordinate", status: "completed", token: "alx-sub-3" },
    { id: "r-a10", name: "Sgt Ana Fifita", relationship: "subordinate", status: "invited", token: "alx-sub-4" },
  ];

  const hanaRaters = [
    { id: "r-h1", name: "Maj Kate Lindsay", relationship: "superior", status: "completed", token: "han-sup-1" },
    { id: "r-h2", name: "WO2 Pete Solomon", relationship: "peer", status: "completed", token: "han-peer-1" },
    { id: "r-h3", name: "WO2 Anaru Waititi", relationship: "peer", status: "completed", token: "han-peer-2" },
    { id: "r-h4", name: "SSgt Chloe Brennan", relationship: "peer", status: "completed", token: "han-peer-3" },
    { id: "r-h5", name: "Sgt Josh Palmer", relationship: "subordinate", status: "completed", token: "han-sub-1" },
    { id: "r-h6", name: "Cpl Aroha Mead", relationship: "subordinate", status: "completed", token: "han-sub-2" },
    { id: "r-h7", name: "Cpl Sam Reid", relationship: "subordinate", status: "completed", token: "han-sub-3" },
    { id: "r-h8", name: "Cpl Tui Henare", relationship: "subordinate", status: "completed", token: "han-sub-4" },
  ];

  const jordanRaters = [
    { id: "r-j1", name: "Maj Ian Crawford", relationship: "superior", status: "invited", token: "jor-sup-1" },
    { id: "r-j2", name: "Lt Emma Walsh", relationship: "peer", status: "invited", token: "jor-peer-1" },
  ];

  const priyaRaters = [
    { id: "r-p1", name: "Lt Zoe Marsh", relationship: "superior", status: "completed", token: "pri-sup-1" },
    { id: "r-p2", name: "Sgt Kane Roberts", relationship: "peer", status: "completed", token: "pri-peer-1" },
    { id: "r-p3", name: "Sgt Ella Tuhoe", relationship: "peer", status: "invited", token: "pri-peer-2" },
    { id: "r-p4", name: "Sgt Marcus Lee", relationship: "peer", status: "invited", token: "pri-peer-3" },
    { id: "r-p5", name: "Cpl Ben Foster", relationship: "subordinate", status: "completed", token: "pri-sub-1" },
    { id: "r-p6", name: "Cpl Rangi Ngatai", relationship: "subordinate", status: "invited", token: "pri-sub-2" },
    { id: "r-p7", name: "LCpl Sophie Grant", relationship: "subordinate", status: "completed", token: "pri-sub-3" },
    { id: "r-p8", name: "LCpl Wiremu Kahu", relationship: "subordinate", status: "invited", token: "pri-sub-4" },
    { id: "r-p9", name: "LCpl Mia Chen", relationship: "subordinate", status: "invited", token: "pri-sub-5" },
  ];

  const assessments = [
    {
      id: "a-alex", participantId: "p-alex", courseId: "c-elda-ll",
      status: "open", // draft | open | closed
      createdAt: "2026-09-08", closeDate: "2026-10-02",
      selfCompleted: true, raters: alexRaters,
      log: [
        { at: "2026-09-08", text: "360 created by NZALC staff." },
        { at: "2026-09-08", text: "Invitations sent to 8 raters (simulated)." },
        { at: "2026-09-10", text: "Alex added Capt Ruth Davies (Peer) and Sgt Ana Fifita (Subordinate)." },
        { at: "2026-09-10", text: "Invitations sent to 2 raters (simulated)." },
        { at: "2026-09-18", text: "Reminder sent to 4 outstanding raters (simulated)." },
      ],
    },
    {
      id: "a-hana", participantId: "p-hana", courseId: "c-snco",
      status: "closed", createdAt: "2026-07-20", closeDate: "2026-08-07", closedAt: "2026-08-08",
      selfCompleted: true, raters: hanaRaters,
      log: [
        { at: "2026-07-20", text: "360 created by NZALC staff." },
        { at: "2026-07-20", text: "Invitations sent to 8 raters (simulated)." },
        { at: "2026-08-08", text: "360 closed. Report released to Hana." },
      ],
    },
    {
      id: "a-jordan", participantId: "p-jordan", courseId: "c-jolc",
      status: "draft", createdAt: "2026-09-21", closeDate: "2026-10-16",
      selfCompleted: false, raters: jordanRaters,
      log: [{ at: "2026-09-21", text: "360 created by NZALC staff. Awaiting rater nominations." }],
    },
    {
      id: "a-priya", participantId: "p-priya", courseId: "c-elda-ll",
      status: "open", createdAt: "2026-08-25", closeDate: "2026-09-19",
      selfCompleted: false, raters: priyaRaters,
      log: [
        { at: "2026-08-25", text: "360 created by NZALC staff." },
        { at: "2026-08-25", text: "Invitations sent to 9 raters (simulated)." },
        { at: "2026-09-12", text: "Reminder sent to 6 outstanding raters (simulated)." },
      ],
    },
  ];

  // Responses: one per completed rater, plus the participant's self-assessment.
  // Comments are attached to responses but the report never links them to a
  // rater or a relationship.
  const responses = [];
  let seedN = 11;
  const addResponse = (assessmentId, raterId, relationship, profile, comments, notObserved = []) => {
    responses.push({
      id: `resp-${responses.length + 1}`,
      assessmentId, raterId, relationship,
      submittedAt: TODAY,
      ratings: makeRatings(profile, relationship, seedN++, notObserved),
      comments,
    });
  };

  responses.push({ id: "resp-self-alex", assessmentId: "a-alex", raterId: null, relationship: "self", submittedAt: "2026-09-09", ratings: alexSelf, comments: {} });
  responses.push({ id: "resp-self-hana", assessmentId: "a-hana", raterId: null, relationship: "self", submittedAt: "2026-07-22", ratings: hanaSelf, comments: {} });

  const alexComments = {
    "r-a1": { keep: "Keep backing your people in front of the Bn. It's noticed.", more: "Ask for the room's view before you give yours. You usually have the answer, and people have learned to wait for it." },
    "r-a2": { keep: "Calm on the net when things go sideways. Sets the tone for everyone.", more: "Delegate more of the planning detail; you carry too much of it yourself.", other: "Would benefit from a mentor outside the Regiment." },
    "r-a3": { keep: "Clear orders, no drama. Easy to work alongside.", more: "Be quicker to share the credit with other sub-units." },
    "r-a4": { keep: "Keep pushing the standards on the range. The platoon is better for it.", more: "Slow down in the first five minutes of a problem. First answer isn't always the best one.", other: "" },
    "r-a5": { keep: "Honest with peers, even when it's awkward.", more: "Check in on people after a hard week, not just during." },
    "r-a7": { keep: "Always has the platoon's back with the OC.", more: "Sometimes decisions are made before the section commanders have been asked. Ask us first.", other: "Junior soldiers find it hard to raise things directly. A regular five minutes with each section would help." },
    "r-a8": { keep: "Explains the why, not just the what.", more: "Would be good to see more of the boss around the lines outside of exercises." },
    "r-a9": { keep: "Fair. Treats everyone the same.", more: "Not sure. Maybe let people try things their way sometimes." },
  };
  for (const r of alexRaters.filter((x) => x.status === "completed")) {
    const notObs = r.relationship === "subordinate" ? ["o3"] : [];
    addResponse("a-alex", r.id, r.relationship, alexProfile, alexComments[r.id] || {}, r.id === "r-a9" ? notObs : []);
  }

  const hanaComments = {
    "r-h1": { keep: "The way you coach the young NCOs. Best in the unit.", more: "Push decisions down earlier. You hold on to them because you can do them well." },
    "r-h2": { keep: "Straight talking. You always know where you stand.", more: "Say no to a few more taskings. You're the default answer to everything." },
    "r-h3": { keep: "Keep bringing the wider view into planning.", more: "Give the plan earlier, even if it's rough." },
    "r-h4": { keep: "Looking after people quietly, without making a show of it.", more: "Let the section commanders run their own AARs." },
    "r-h5": { keep: "Always approachable.", more: "Decisions can take a while when it's a grey area." },
    "r-h6": { keep: "You teach rather than tell.", more: "Nothing major. Maybe trust us to run things more.", other: "Best boss I've had." },
    "r-h7": { keep: "Fair and consistent.", more: "Be quicker to make the call under time pressure." },
    "r-h8": { keep: "Explains things properly.", more: "Sometimes waits too long to decide." },
  };
  for (const r of hanaRaters) addResponse("a-hana", r.id, r.relationship, hanaProfile, hanaComments[r.id] || {});

  const priyaProfile = { s1: { default: 3 }, o4: { default: 3 }, t2: { default: 3 }, a3: { default: 3 } };
  const priyaComments = {
    "r-p1": { keep: "Thorough preparation.", more: "Speak up earlier in the O Group." },
    "r-p2": { keep: "Reliable.", more: "Share the workload." },
    "r-p5": { keep: "Looks after us.", more: "More feedback on how we're going." },
    "r-p7": { keep: "Patient when teaching.", more: "Not sure." },
  };
  for (const r of priyaRaters.filter((x) => x.status === "completed")) addResponse("a-priya", r.id, r.relationship, priyaProfile, priyaComments[r.id] || {});

  return {
    version: 1,
    today: TODAY,
    courses, participants, assessments, responses,
    // Development-only viewing state.
    view: { role: "admin", participantId: "p-alex" },
  };
}
