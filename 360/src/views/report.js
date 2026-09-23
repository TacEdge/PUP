// The feedback report. Consumes only the aggregated model from report.js.
import { esc, fmtDate, plural } from "../lib/html.js";
import * as db from "../lib/store.js";
import { buildReport, scaleLabel } from "../lib/report.js";
import { instrument, privacy } from "../data/instrument.js";
import { topbar } from "./shared.js";

const MIN = instrument.scale[0].value, MAX = instrument.scale[instrument.scale.length - 1].value;
const pct = (v) => ((v - MIN) / (MAX - MIN)) * 100;

function axis() {
  return `<div class="axis"><span></span><div class="ticks">${instrument.scale.map((s) => `<span>${esc(s.label)}</span>`).join("")}</div><span></span></div>`;
}
const ticks = () => instrument.scale.map((s) => `<i class="t" style="left:${pct(s.value)}%"></i>`).join("");

function dotRow({ label, sub, value, self = false, withheld = false, gapFrom = null }) {
  const mark = value == null ? "" : `<i class="mark${self ? " self" : ""}" style="left:${pct(value)}%" title="${esc(label)}: ${value}"></i>`;
  const gap = gapFrom != null && value != null
    ? `<i class="gapline" style="left:${Math.min(pct(gapFrom), pct(value))}%;width:${Math.abs(pct(gapFrom) - pct(value))}%"></i>` : "";
  return `<div class="dot-row${self ? " self" : ""}${withheld ? " withheld" : ""}">
    <div class="lab">${esc(label)}${sub ? `<small>${esc(sub)}</small>` : ""}</div>
    <div class="track">${ticks()}${gap}${mark}</div>
    <div class="val">${value == null ? (withheld ? "—" : "") : `${value.toFixed(1)}`}</div>
  </div>`;
}

function dimensionBlock(d, r) {
  const rows = [];
  if (r.hasSelf) rows.push(dotRow({ label: "Self", value: d.self, self: true }));
  for (const g of r.groups) rows.push(dotRow({ label: g.label, sub: `n = ${g.n}`, value: d.byGroup[g.key].mean }));
  for (const w of r.withheld) rows.push(dotRow({ label: relPlural(w.key), sub: `n = ${w.n} · not shown`, value: null, withheld: true }));
  const stmts = `
  <details class="plain" style="margin-top:.75rem">
    <summary>Statements</summary>
    <table class="stmt-table">
      <thead><tr><th>Statement</th>${r.hasSelf ? "<th>Self</th>" : ""}${r.groups.map((g) => `<th>${esc(g.label)}</th>`).join("")}<th>All raters</th></tr></thead>
      <tbody>${d.statements.map((s) => `<tr><td>${esc(s.text)}</td>${r.hasSelf ? `<td class="self">${s.self ?? "—"}</td>` : ""}${r.groups.map((g) => `<td>${s.byGroup[g.key].mean?.toFixed(1) ?? "—"}</td>`).join("")}<td>${s.others.mean?.toFixed(1) ?? "—"}</td></tr>`).join("")}</tbody>
    </table>
  </details>`;
  return `<section class="dim" id="dim-${d.id}">
    <div class="dim-head"><h3>${esc(d.name)}</h3><span class="muted">All raters ${d.others?.toFixed(1) ?? "—"} · ${scaleLabel(d.others)}</span></div>
    <div class="dots">${axis()}${rows.join("")}</div>
    ${stmts}
  </section>`;
}

const relPlural = (k) => ({ peer: "Peers", subordinate: "Subordinates", other: "Others", superior: "Superiors" }[k] || k);

function glance(r) {
  const g = r.atAGlance;
  const dimText = (d) => (d ? `${d.name}` : "—");
  return `<div class="glance">
    <div class="tile"><div class="k">Feedback from</div><div class="v">${plural(g.raters, "rater")}</div><div class="d">${plural(g.groupCount, "group")} reported separately${r.withheld.length ? ", " + plural(r.withheld.length, "group") + " withheld" : ""}</div></div>
    <div class="tile"><div class="k">Rated highest</div><div class="v">${esc(dimText(g.strongest))}</div><div class="d">${g.strongest ? `${g.strongest.others.toFixed(1)} · ${scaleLabel(g.strongest.others)}` : ""}</div></div>
    <div class="tile"><div class="k">Most room to grow</div><div class="v">${esc(dimText(g.weakest))}</div><div class="d">${g.weakest ? `${g.weakest.others.toFixed(1)} · ${scaleLabel(g.weakest.others)}` : ""}</div></div>
    <div class="tile"><div class="k">Perception gaps</div><div class="v">${g.hasSelf ? g.gapCount : "—"}</div><div class="d">${g.hasSelf ? "statements where self and others differ" : "no self-assessment"}</div></div>
  </div>`;
}

function summarySentences(r) {
  const g = r.atAGlance; const p = r.participant.firstName;
  const out = [];
  if (g.strongest && g.weakest) out.push(`Across ${plural(g.raters, "rater")}, ${p} is rated most consistently on <b>${esc(g.strongest.name)}</b> and has most room to grow in <b>${esc(g.weakest.name)}</b>.`);
  if (r.strengths.length) out.push(`${r.strengths.length === 1 ? "One statement is" : `${r.strengths.length} statements are`} rated close to “Consistently” by raters overall.`);
  if (r.development.length) out.push(`${r.development.length === 1 ? "One statement sits" : `${r.development.length} statements sit`} below “Usually”, which is where reflection is likely to be most useful.`);
  if (g.hasSelf && g.gapCount) out.push(`Self-rating and others' ratings differ noticeably on ${plural(g.gapCount, "statement")}; these are worth exploring rather than resolving.`);
  if (g.hasSelf && !g.gapCount) out.push(`Self-rating and others' ratings are broadly aligned.`);
  return out.map((s) => `<p>${s}</p>`).join("");
}

function findings(items, empty, kind) {
  if (!items.length) return `<p class="muted">${empty}</p>`;
  return `<ul class="findings">${items.map((s) => `<li>
    <div><div class="t">${esc(s.text)}</div><div class="d">${esc(instrument.dimensions.find((d) => d.id === s.dimensionId).name)}</div></div>
    <div class="m">${s.others.mean.toFixed(1)}<small>${scaleLabel(s.others.mean)} · n = ${s.others.n}</small></div>
  </li>`).join("")}</ul>`;
}

function gaps(r) {
  if (!r.hasSelf) return `<p class="muted">No self-assessment was completed, so self-perception cannot be compared.</p>`;
  if (!r.gaps.length) return `<p class="muted">No statement differs by ${0.75} or more between self and others.</p>`;
  return r.gaps.map((s) => `<div class="gap-row">
    <div class="t">${esc(s.text)}</div>
    <div class="d">${s.direction === "self-higher" ? "You rated yourself higher than others rated you." : "Others rated you higher than you rated yourself."} Difference ${Math.abs(s.gap).toFixed(1)}.</div>
    <div class="dots">${dotRow({ label: "Self", value: s.self, self: true })}${dotRow({ label: "All raters", sub: `n = ${s.others.n}`, value: s.others.mean, gapFrom: s.self })}</div>
  </div>`).join("");
}

function quotes(list) {
  if (!list.length) return `<p class="muted">No written answers yet.</p>`;
  return `<ul class="quotes">${list.map((t) => `<li>${esc(t)}</li>`).join("")}</ul>`;
}

export function renderReport(assessmentId, { asStaff = false } = {}) {
  const a = db.assessment(assessmentId);
  const nav = asStaff ? [{ href: "#/admin", label: "360s" }] : [{ href: "#/me", label: "My 360" }, { href: `#/report/${assessmentId}`, label: "My report" }];
  const head = topbar({ nav, current: asStaff ? "" : `#/report/${assessmentId}` });
  if (!a) return { title: "Report", html: `${head}<main id="main" class="reading page" tabindex="-1"><p class="empty">Report not found.</p></main>` };

  if (!asStaff && a.status !== "closed") {
    return { title: "Report not yet available", html: `${head}<main id="main" class="reading page" tabindex="-1"><a class="back" href="#/me">← My 360</a><h1 class="h1">Not yet available</h1><p class="lead muted">Your report is released when NZALC closes the 360.</p></main>` };
  }

  const r = buildReport(assessmentId);
  const p = r.participant;
  const { done, total } = db.completion(a);
  const first = p.firstName;

  const banner = asStaff && a.status !== "closed"
    ? `<div class="note" style="margin-top:1.25rem"><p><b>Preview.</b> This 360 is still open (${done} of ${total} raters). ${first} cannot see this report until it is closed.</p></div>` : "";

  const insufficient = !r.sufficient
    ? `<div class="note" style="margin-top:1.25rem"><p><b>Not enough feedback yet.</b> At least ${privacy.minGroupSize} rater responses are needed before aggregated results are meaningful. Sections below show what is available.</p></div>` : "";

  const html = `${head}
  <main id="main" class="reading report" tabindex="-1">
    <div class="report-head">
      <a class="back" href="${asStaff ? `#/admin/a/${a.id}` : "#/me"}">← ${asStaff ? "Back to 360" : "My 360"}</a>
      <p class="eyebrow">360 Feedback report</p>
      <h1 class="h1">${esc(db.fullName(p))}</h1>
      <p class="muted">${esc(r.course.name)} · ${plural(r.atAGlance.raters, "rater")}${a.status === "closed" ? ` · closed ${fmtDate(a.closedAt || a.closeDate)}` : ""}</p>
      <nav class="report-nav" aria-label="Report sections">
        <a href="#glance">At a glance</a><a href="#dimensions">Dimensions</a><a href="#strengths">Strengths</a><a href="#development">Development</a><a href="#gaps">Perception gaps</a><a href="#written">Written feedback</a><a href="#next">What next</a>
      </nav>
      ${banner}${insufficient}
    </div>

    <h2 id="glance">At a glance</h2>
    <p>A summary of what your raters said, taken together.</p>
    ${glance(r)}
    ${summarySentences(r)}
    <p class="small muted">Ratings are on a four-point scale from Rarely (1) to Consistently (4). Averages are shown to one decimal place and are a guide to patterns, not precise measures.</p>

    <h2 id="dimensions">Leadership dimensions</h2>
    <p>How each rater group sees you, dimension by dimension. Your own rating is shown for comparison.</p>
    <div class="legend"><span><i class="self"></i>Self</span><span><i></i>Rater group average</span></div>
    ${r.dimensions.map((d) => dimensionBlock(d, r)).join("")}
    ${r.withheld.length ? `<p class="small muted">Groups with fewer than ${privacy.minGroupSize} responses are not shown separately, to protect the confidentiality of individual raters. Their responses are included in “All raters”.</p>` : ""}

    <h2 id="strengths">Strengths</h2>
    <p>Where feedback from all raters is consistently positive.</p>
    ${findings(r.strengths, "No statement is rated close to “Consistently” yet.")}

    <h2 id="development">Development opportunities</h2>
    <p>Where feedback suggests reflection, or a conversation, would be useful.</p>
    ${findings(r.development, "No statement is rated below “Usually” on average. Look at the perception gaps and written feedback for where to focus.")}

    <h2 id="gaps">Perception gaps</h2>
    <p>Where how you see yourself and how others see you differ most. A gap is evidence to explore, not a verdict.</p>
    <div class="legend"><span><i class="self"></i>Self</span><span><i></i>All raters</span><span><i class="gap"></i>Gap</span></div>
    ${gaps(r)}

    <h2 id="written">Written feedback</h2>
    <p>Comments from all raters, pooled and in random order. Rater group is not shown.</p>
    ${instrument.prompts.map((pr) => `<h3 class="h3">${esc(pr.heading)}</h3>${quotes(r.comments[pr.id])}`).join("")}

    <h2 id="next">What next</h2>
    <p>Suggested steps before your development conversation.</p>
    <ol class="next-steps">
      <li>Read the report once without responding to it. Come back to it a day later.</li>
      <li>Choose one strength to keep doing deliberately${r.strengths[0] ? `, for example “${esc(r.strengths[0].text)}”` : ""}.</li>
      <li>Choose one development opportunity or perception gap to explore. Ask: what would others be seeing that leads them here?</li>
      <li>Bring both to your conversation with NZALC staff and decide one concrete thing to try on course.</li>
    </ol>
    <p class="small muted" style="margin-top:2rem">This report is for ${first}'s leadership development. It is not a performance assessment. Prototype instrument: placeholder developmental content, not NZ Army doctrine.</p>
  </main>`;
  return { title: `${db.shortName(p)} — 360 report`, html };
}
