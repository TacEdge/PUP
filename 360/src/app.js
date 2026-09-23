// Router, re-render loop and the development-only role switcher.
import * as db from "./lib/store.js";
import { esc } from "./lib/html.js";
import { renderRater, raterContext, selfContext, renderStart } from "./views/rater.js";
import { raterLink } from "./lib/ui.js";
import { identity, formatMobile } from "./lib/auth.js";
import { renderParticipant } from "./views/participant.js";
import { renderAdminList, renderAdminNew, renderAdminDetail } from "./views/admin.js";
import { renderReport } from "./views/report.js";
import { relLabel } from "./views/shared.js";

const app = document.getElementById("app");
const devbar = document.getElementById("devbar");

const routes = [
  { re: /^#\/r\/([^/]+)$/, view: (m) => renderRater(raterContext(m[1])), role: "rater" },
  { re: /^#\/start$/, view: () => renderStart(), role: "rater" },
  { re: /^#\/me$/, view: () => renderParticipant(db.getState().view.participantId), role: "participant" },
  { re: /^#\/me\/self$/, view: () => renderRater(selfContext(db.getState().view.participantId)), role: "participant" },
  { re: /^#\/report\/([^/]+)$/, view: (m) => renderReport(m[1]), role: "participant" },
  { re: /^#\/admin$/, view: () => renderAdminList(), role: "admin" },
  { re: /^#\/admin\/new$/, view: () => renderAdminNew(), role: "admin" },
  { re: /^#\/admin\/a\/([^/]+)\/report$/, view: (m) => renderReport(m[1], { asStaff: true }), role: "admin" },
  { re: /^#\/admin\/a\/([^/]+)$/, view: (m) => renderAdminDetail(m[1]), role: "admin" },
];

let cleanup = () => {};
let lastHash = null;

function match() {
  for (const r of routes) {
    const m = location.hash.match(r.re);
    if (m) return { route: r, m };
  }
  return null;
}

function render() {
  const hit = match();
  if (!hit) {
    const role = db.getState().view.role;
    location.hash = role === "participant" ? "#/me" : role === "rater" ? "#/start" : "#/admin";
    return;
  }
  const routeChanged = lastHash !== location.hash;
  const scrollY = window.scrollY;
  cleanup();
  const out = hit.route.view(hit.m);
  document.title = `${out.title} · NZALC 360 (prototype)`;
  // Mount into a fresh element each render so view listeners never accumulate.
  const root = document.createElement("div");
  root.innerHTML = out.html;
  app.replaceChildren(root);
  cleanup = (out.mount && out.mount(root, render)) || (() => {});
  renderDevbar(hit.route.role);
  const isFlow = location.hash.startsWith("#/r/") || location.hash.startsWith("#/me/self");
  if (routeChanged || isFlow) {
    window.scrollTo(0, 0);
    if (!isFlow) app.querySelector("#main")?.focus({ preventScroll: true });
  } else {
    window.scrollTo(0, scrollY);
  }
  lastHash = location.hash;
}

// ---- development-only role switcher and simulated SMS inbox ----------------
let inboxOpen = false;
function renderInbox() {
  if (!inboxOpen) return "";
  const msgs = db.messages().slice(0, 30);
  const fmt = (iso) => new Date(iso).toLocaleString("en-NZ", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
  return `
  <div class="inbox" role="region" aria-label="Simulated SMS inbox">
    <h2>Simulated SMS</h2>
    <p class="muted">Messages the system would have sent. Nothing leaves this browser. Tap a link to follow it as the rater would.</p>
    ${msgs.length ? msgs.map((m) => `
      <div class="sms ${m.kind}">
        <div class="meta"><span>To ${esc(formatMobile(m.to))}</span><span>${fmt(m.at)}</span></div>
        <div class="bubble">${esc(m.text)}${m.token ? `<a href="#/r/${m.token}" data-inbox-link>${esc(raterLink(m.token).replace(/^https?:\/\//, ""))}</a>` : ""}</div>
      </div>`).join("") : `<p class="muted">No messages yet.</p>`}
  </div>`;
}

function renderDevbar(activeRole) {
  const s = db.getState();
  const participants = s.participants.filter((p) => s.assessments.some((a) => a.participantId === p.id));
  const raterOptions = s.assessments.flatMap((a) => {
    const p = db.participant(a.participantId);
    return a.raters.map((r) => ({ token: r.token, label: `${r.name} · ${relLabel(r.relationship)} of ${p.firstName}${r.status === "completed" ? " (done)" : ""}` }));
  });
  const currentToken = (location.hash.match(/^#\/r\/([^/]+)$/) || [])[1] || s.view.token || "";
  const mobileValue = activeRole === "admin" ? "admin" : activeRole === "participant" ? `p:${s.view.participantId}` : currentToken ? `r:${currentToken}` : "";
  devbar.innerHTML = `
  <div class="devbar" role="region" aria-label="Prototype controls">
    <span class="tag">Prototype</span>
    <span class="lbl">View as</span>
    <span class="desktop"><button data-role="admin" aria-pressed="${activeRole === "admin"}">NZALC staff</button></span>
    <span class="desktop"><button data-role="participant" aria-pressed="${activeRole === "participant"}">Participant</button></span>
    <span class="desktop"><select data-sel="participant" aria-label="Participant to view as">${participants.map((p) => `<option value="${p.id}" ${p.id === s.view.participantId ? "selected" : ""}>${esc(db.fullName(p))}</option>`).join("")}</select></span>
    <span class="desktop"><button data-role="rater" aria-pressed="${activeRole === "rater"}">Rater</button></span>
    <span class="desktop"><select data-sel="rater" aria-label="Rater link to open"><option value="">No link (open the app)</option>${raterOptions.map((o) => `<option value="${o.token}" ${o.token === currentToken ? "selected" : ""}>${esc(o.label)}</option>`).join("")}</select></span>
    <select class="mobile" data-sel="mobile" aria-label="View as">
      <option value="admin" ${mobileValue === "admin" ? "selected" : ""}>NZALC staff</option>
      <optgroup label="Participant">${participants.map((p) => `<option value="p:${p.id}" ${mobileValue === `p:${p.id}` ? "selected" : ""}>${esc(db.fullName(p))}</option>`).join("")}</optgroup>
      <optgroup label="Rater link">${raterOptions.map((o) => `<option value="r:${o.token}" ${mobileValue === `r:${o.token}` ? "selected" : ""}>${esc(o.label)}</option>`).join("")}</optgroup>
    </select>
    <span class="spacer"></span>
    <button data-inbox aria-pressed="${inboxOpen}" aria-label="Simulated SMS inbox">SMS ${db.messages().length ? `(${db.messages().length})` : ""}</button>
    <button class="reset" data-reset>Reset</button>
  </div>
  ${renderInbox()}`;
  devbar.querySelector("[data-inbox]").addEventListener("click", () => { inboxOpen = !inboxOpen; renderDevbar(activeRole); });
  devbar.querySelectorAll("[data-inbox-link]").forEach((a) => a.addEventListener("click", () => { inboxOpen = false; }));
  devbar.querySelectorAll("[data-role]").forEach((b) => b.addEventListener("click", () => {
    const role = b.dataset.role;
    db.setView({ role });
    if (role === "admin") location.hash = "#/admin";
    else if (role === "participant") location.hash = "#/me";
    else { const sel = devbar.querySelector("[data-sel=rater]"); if (sel.value) { db.setView({ token: sel.value }); location.hash = `#/r/${sel.value}`; } else location.hash = "#/start"; }
  }));
  devbar.querySelector("[data-sel=participant]").addEventListener("change", (e) => { db.setView({ participantId: e.target.value, role: "participant" }); location.hash = "#/me"; render(); });
  devbar.querySelector("[data-sel=rater]").addEventListener("change", (e) => { if (e.target.value) { db.setView({ token: e.target.value, role: "rater" }); location.hash = `#/r/${e.target.value}`; } });
  devbar.querySelector("[data-sel=mobile]").addEventListener("change", (e) => {
    const v = e.target.value;
    if (v === "admin") { db.setView({ role: "admin" }); location.hash = "#/admin"; }
    else if (v.startsWith("p:")) { db.setView({ role: "participant", participantId: v.slice(2) }); location.hash = "#/me"; render(); }
    else if (v.startsWith("r:")) { db.setView({ role: "rater", token: v.slice(2) }); location.hash = `#/r/${v.slice(2)}`; }
  });
  devbar.querySelector("[data-reset]").addEventListener("click", () => { if (confirm("Reset all demonstration data, including the remembered mobile sign-in?")) { db.resetDemo(); identity.signOut(); location.hash = "#/admin"; render(); } });
}

window.addEventListener("hashchange", render);
db.subscribe(() => render());
render();
