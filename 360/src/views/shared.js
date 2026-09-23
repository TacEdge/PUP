import { esc, fmtDate, daysBetween } from "../lib/html.js";
import * as db from "../lib/store.js";
import { relationships } from "../data/instrument.js";

export const LOGO = "../assets/nz-army-logo.png";

export function topbar({ role, nav = [], current = "" }) {
  const links = nav.map((n) => `<a href="${n.href}" ${n.href === current ? 'aria-current="page"' : ""}>${esc(n.label)}</a>`).join("");
  return `
  <div class="brandline"></div>
  <header class="topbar">
    <div class="wrap topbar-inner">
      <img src="${LOGO}" alt="New Zealand Army">
      <span class="sep" aria-hidden="true"></span>
      <span class="app">360 Feedback</span>
      ${links ? `<nav aria-label="Primary">${links}</nav>` : `<span class="role">${esc(role || "")}</span>`}
    </div>
  </header>`;
}

export const relLabel = (key, plural = false) => {
  const r = relationships.find((x) => x.key === key);
  return r ? (plural ? r.plural : r.label) : key;
};

export function statusOf(a) {
  if (a.status === "closed") return { key: "closed", label: "Closed" };
  if (a.status === "draft") return { key: "draft", label: "Nominating raters" };
  if (a.closeDate < db.todayISO()) return { key: "overdue", label: "Overdue" };
  return { key: "open", label: "In progress" };
}

export function statusPill(a) {
  const s = statusOf(a);
  return `<span class="status ${s.key}">${s.label}</span>`;
}

export function dueText(a) {
  if (a.status === "closed") return `Closed ${fmtDate(a.closedAt || a.closeDate)}`;
  const d = daysBetween(db.todayISO(), a.closeDate);
  if (d < 0) return `${Math.abs(d)} day${Math.abs(d) === 1 ? "" : "s"} overdue`;
  if (d === 0) return "Closes today";
  return `Closes in ${d} day${d === 1 ? "" : "s"}`;
}

export function bar(done, total, thin = false) {
  const pct = total ? Math.round((done / total) * 100) : 0;
  return `<div class="bar${thin ? " thin" : ""}" role="img" aria-label="${done} of ${total} complete"><i style="width:${pct}%"></i></div>`;
}

// Completion by rater group, shown to participants and staff alike. Counts
// only; never who.
export function groupBars(a) {
  const groups = db.groupCompletion(a);
  const order = ["superior", "peer", "subordinate", "other"];
  const items = order.filter((k) => groups[k]).map((k) => `
    <div class="group">
      <div class="label"><b>${relLabel(k, true)}</b><span class="num">${groups[k].done} / ${groups[k].total}</span></div>
      ${bar(groups[k].done, groups[k].total)}
    </div>`).join("");
  return items ? `<div class="groups">${items}</div>` : `<p class="muted">No raters yet.</p>`;
}

export const relOptions = (selected = "peer") =>
  relationships.filter((r) => r.key !== "self").map((r) => `<option value="${r.key}" ${r.key === selected ? "selected" : ""}>${r.label}</option>`).join("");
