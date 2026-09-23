// Prototype persistence: the whole domain lives in one object in localStorage.
// Mutations are plain functions that return the new state and notify listeners.
import { buildSeed } from "../data/seed.js";

const KEY = "nzalc-360-proto-v1";
const listeners = new Set();
let state = load();

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && parsed.version === 1) return parsed;
    }
  } catch (_) { /* fall through to seed */ }
  return buildSeed();
}

function persist() {
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (_) { /* private mode etc. */ }
  listeners.forEach((fn) => fn(state));
}

export const getState = () => state;
export const subscribe = (fn) => { listeners.add(fn); return () => listeners.delete(fn); };
export function resetDemo() { state = buildSeed(); persist(); }

// ---- lookups ---------------------------------------------------------------
export const todayISO = () => state.today;
export const participant = (id) => state.participants.find((p) => p.id === id);
export const course = (id) => state.courses.find((c) => c.id === id);
export const assessment = (id) => state.assessments.find((a) => a.id === id);
export const assessmentForParticipant = (pid) =>
  [...state.assessments].filter((a) => a.participantId === pid).sort((a, b) => (a.createdAt < b.createdAt ? 1 : -1))[0];
export const responsesFor = (assessmentId) => state.responses.filter((r) => r.assessmentId === assessmentId);
export const raterByToken = (token) => {
  for (const a of state.assessments) {
    const r = a.raters.find((x) => x.token === token);
    if (r) return { assessment: a, rater: r };
  }
  return null;
};

export function fullName(p) { return `${p.rank} ${p.firstName} ${p.lastName}`; }
export function shortName(p) { return `${p.firstName} ${p.lastName}`; }

export function completion(a) {
  const done = a.raters.filter((r) => r.status === "completed").length;
  return { done, total: a.raters.length };
}
export function groupCompletion(a) {
  const groups = {};
  for (const r of a.raters) {
    groups[r.relationship] ||= { done: 0, total: 0 };
    groups[r.relationship].total += 1;
    if (r.status === "completed") groups[r.relationship].done += 1;
  }
  return groups;
}

// ---- mutations -------------------------------------------------------------
function log(a, text) { a.log.push({ at: state.today, text }); }
const newId = (prefix) => `${prefix}-${Math.random().toString(36).slice(2, 8)}`;

export function createAssessment({ rank, firstName, lastName, unit, courseId, closeDate }) {
  const p = { id: newId("p"), rank, firstName, lastName, unit };
  state.participants.push(p);
  const a = {
    id: newId("a"), participantId: p.id, courseId, status: "draft",
    createdAt: state.today, closeDate, selfCompleted: false, raters: [],
    log: [{ at: state.today, text: "360 created by NZALC staff. Awaiting rater nominations." }],
  };
  state.assessments.push(a);
  persist();
  return a;
}

export function addRater(assessmentId, { name, relationship, by = "NZALC staff" }) {
  const a = assessment(assessmentId);
  const rater = { id: newId("r"), name, relationship, status: "invited", token: newId("t") };
  a.raters.push(rater);
  log(a, `${by} added ${name} (${relationship}). Invitation sent (simulated).`);
  persist();
  return rater;
}

export function removeRater(assessmentId, raterId) {
  const a = assessment(assessmentId);
  const r = a.raters.find((x) => x.id === raterId);
  if (!r || r.status === "completed") return;
  a.raters = a.raters.filter((x) => x.id !== raterId);
  log(a, `Removed ${r.name} (${r.relationship}).`);
  persist();
}

export function remind(assessmentId, raterIds) {
  const a = assessment(assessmentId);
  const targets = a.raters.filter((r) => raterIds.includes(r.id) && r.status !== "completed");
  targets.forEach((r) => { r.lastReminded = state.today; });
  if (targets.length) log(a, `Reminder sent to ${targets.length} outstanding rater${targets.length === 1 ? "" : "s"} (simulated).`);
  persist();
  return targets.length;
}

export function openAssessment(assessmentId) {
  const a = assessment(assessmentId);
  a.status = "open";
  log(a, `Invitations sent to ${a.raters.length} raters (simulated). 360 is open.`);
  persist();
}

export function closeAssessment(assessmentId) {
  const a = assessment(assessmentId);
  a.status = "closed";
  a.closedAt = state.today;
  const p = participant(a.participantId);
  log(a, `360 closed. Report released to ${p.firstName}.`);
  persist();
}

export function reopenAssessment(assessmentId) {
  const a = assessment(assessmentId);
  a.status = "open";
  delete a.closedAt;
  log(a, "360 reopened.");
  persist();
}

export function submitResponse({ assessmentId, raterId, relationship, ratings, comments }) {
  const a = assessment(assessmentId);
  state.responses.push({
    id: newId("resp"), assessmentId, raterId, relationship,
    submittedAt: state.today, ratings, comments,
  });
  if (relationship === "self") {
    a.selfCompleted = true;
  } else {
    const r = a.raters.find((x) => x.id === raterId);
    if (r) r.status = "completed";
  }
  persist();
}

export function setView(patch) {
  state.view = { ...state.view, ...patch };
  persist();
}
