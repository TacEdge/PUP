// Turns raw responses into the participant-facing report model.
//
// Privacy rules live here, not in the views:
//  - individual responses are never exposed; only group aggregates leave this module;
//  - anonymised groups below `privacy.minGroupSize` fold into a pooled group,
//    and a pooled group that is still too small is withheld;
//  - comments are pooled across all raters and shuffled, with no relationship.
import { instrument, relationships, privacy, allStatements } from "../data/instrument.js";
import * as db from "./store.js";

const GAP_THRESHOLD = 0.75;   // difference on the 1–4 scale worth a conversation
const STRENGTH_FLOOR = 3.4;   // "Usually" to "Consistently"
const DEVELOP_CEILING = 2.9;  // below "Usually"

const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);
const round1 = (x) => (x == null ? null : Math.round(x * 10) / 10);

function seededShuffle(items, seedStr) {
  let h = 2166136261;
  for (const ch of seedStr) h = Math.imul(h ^ ch.charCodeAt(0), 16777619);
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) {
    h = Math.imul(h ^ (h >>> 13), 1274126177) >>> 0;
    const j = h % (i + 1);
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

// Decide which groups can be displayed and how responses map onto them.
function displayGroups(responses) {
  const counts = {};
  for (const r of responses) counts[r.relationship] = (counts[r.relationship] || 0) + 1;

  const groups = [];
  const map = {}; // relationship -> display group key
  let pooledN = 0;
  const pooledFrom = [];

  for (const rel of relationships) {
    if (rel.key === "self") continue;
    const n = counts[rel.key] || 0;
    if (n === 0) continue;
    if (!rel.anonymised || n >= privacy.minGroupSize) {
      groups.push({ key: rel.key, label: rel.plural, n, anonymised: rel.anonymised });
      map[rel.key] = rel.key;
    } else {
      pooledN += n;
      pooledFrom.push(rel.key);
    }
  }
  const withheld = [];
  if (pooledN >= privacy.minGroupSize) {
    groups.push({ key: "pooled", label: privacy.pooledGroupLabel, n: pooledN, anonymised: true, pooledFrom });
    pooledFrom.forEach((k) => { map[k] = "pooled"; });
  } else {
    pooledFrom.forEach((k) => withheld.push({ key: k, n: counts[k] }));
  }
  return { groups, map, withheld };
}

export function buildReport(assessmentId) {
  const a = db.assessment(assessmentId);
  const p = db.participant(a.participantId);
  const c = db.course(a.courseId);
  const all = db.responsesFor(assessmentId);
  const selfResp = all.find((r) => r.relationship === "self") || null;
  const others = all.filter((r) => r.relationship !== "self");
  const { groups, map, withheld } = displayGroups(others);

  const statAgg = (statementId, rs) => {
    const vals = rs.map((r) => r.ratings[statementId]).filter((v) => typeof v === "number");
    return { mean: round1(mean(vals)), n: vals.length };
  };

  const statements = allStatements().map((s) => {
    const byGroup = {};
    for (const g of groups) {
      const rs = others.filter((r) => map[r.relationship] === g.key);
      byGroup[g.key] = statAgg(s.id, rs);
    }
    const othersAgg = statAgg(s.id, others);
    const selfVal = selfResp ? selfResp.ratings[s.id] : null;
    const gap = selfVal != null && othersAgg.mean != null ? round1(selfVal - othersAgg.mean) : null;
    return { ...s, byGroup, others: othersAgg, self: selfVal, gap };
  });

  const dimensions = instrument.dimensions.map((d) => {
    const sts = statements.filter((s) => s.dimensionId === d.id);
    const dimAgg = (pick) => {
      const vals = sts.map(pick).filter((v) => v != null);
      return round1(mean(vals));
    };
    const byGroup = {};
    for (const g of groups) byGroup[g.key] = { mean: dimAgg((s) => s.byGroup[g.key].mean), n: g.n };
    return {
      id: d.id, name: d.name, short: d.short, statements: sts, byGroup,
      others: dimAgg((s) => s.others.mean),
      self: dimAgg((s) => s.self),
    };
  });

  const rated = statements.filter((s) => s.others.mean != null);
  const strengths = [...rated].sort((x, y) => y.others.mean - x.others.mean).filter((s) => s.others.mean >= STRENGTH_FLOOR).slice(0, 4);
  const development = [...rated].sort((x, y) => x.others.mean - y.others.mean).filter((s) => s.others.mean <= DEVELOP_CEILING).slice(0, 4);
  const gaps = rated
    .filter((s) => s.gap != null && Math.abs(s.gap) >= GAP_THRESHOLD)
    .sort((x, y) => Math.abs(y.gap) - Math.abs(x.gap))
    .map((s) => ({ ...s, direction: s.gap > 0 ? "self-higher" : "others-higher" }))
    .slice(0, 5);

  // Written feedback: pooled, shuffled, unattributed.
  const comments = {};
  for (const pr of instrument.prompts) {
    const texts = others.map((r) => (r.comments?.[pr.id] || "").trim()).filter(Boolean);
    comments[pr.id] = seededShuffle(texts, assessmentId + pr.id);
  }

  const dimsByOthers = dimensions.filter((d) => d.others != null).sort((x, y) => y.others - x.others);
  const atAGlance = {
    raters: others.length,
    groupCount: groups.length,
    strongest: dimsByOthers[0] || null,
    weakest: dimsByOthers.length > 1 ? dimsByOthers[dimsByOthers.length - 1] : null,
    gapCount: gaps.length,
    commentCount: Object.values(comments).reduce((n, xs) => n + xs.length, 0),
    hasSelf: Boolean(selfResp),
  };

  return {
    assessment: a, participant: p, course: c,
    groups, withheld, hasSelf: Boolean(selfResp),
    dimensions, statements, strengths, development, gaps, comments, atAGlance,
    scale: instrument.scale,
    sufficient: others.length >= privacy.minGroupSize,
  };
}

export const scaleLabel = (value) => {
  if (value == null) return "";
  const nearest = instrument.scale.reduce((best, s) => (Math.abs(s.value - value) < Math.abs(best.value - value) ? s : best));
  return nearest.label;
};
