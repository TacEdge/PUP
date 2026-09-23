// NZALC staff views: the list of 360s, a new-360 form, and one 360's detail.
import { esc, fmtDate, plural } from "../lib/html.js";
import * as db from "../lib/store.js";
import { toast, go, ask, copyText, raterLink } from "../lib/ui.js";
import { topbar, statusPill, statusOf, dueText, bar, groupBars, relLabel, relOptions } from "./shared.js";
import { relationships } from "../data/instrument.js";
import { normaliseMobile, formatMobile } from "../lib/auth.js";

const NAV = [{ href: "#/admin", label: "360s" }];
const head = (current = "#/admin") => topbar({ nav: NAV, current });

let listTab = "active";

export function renderAdminList() {
  const all = db.getState().assessments;
  const rows = all
    .filter((a) => (listTab === "active" ? a.status !== "closed" : a.status === "closed"))
    .sort((x, y) => (x.closeDate < y.closeDate ? -1 : 1));

  const table = rows.length ? `
    <table class="table">
      <thead><tr><th>Participant</th><th>Course</th><th>Completion</th><th>Close date</th><th>Status</th></tr></thead>
      <tbody>${rows.map((a) => {
        const p = db.participant(a.participantId); const c = db.course(a.courseId); const { done, total } = db.completion(a);
        return `<tr>
          <td><a class="row-link" href="#/admin/a/${a.id}">${esc(db.fullName(p))}</a><div class="tiny muted">${esc(p.unit)}</div></td>
          <td>${esc(c.name)}</td>
          <td><div class="num small" style="margin-bottom:.3rem">${done} / ${total}${a.selfCompleted ? "" : ' <span class="tiny muted">· self outstanding</span>'}</div>${bar(done, total, true)}</td>
          <td><div>${fmtDate(a.closeDate)}</div><div class="tiny muted">${dueText(a)}</div></td>
          <td>${statusPill(a)}</td>
        </tr>`; }).join("")}</tbody>
    </table>` : `<p class="empty">Nothing here yet.</p>`;

  const html = `${head()}
  <main id="main" class="wrap page" tabindex="-1">
    <div class="page-head">
      <div><p class="eyebrow">NZ Army Leadership Centre</p><h1 class="h1">${listTab === "active" ? "Active 360s" : "Closed 360s"}</h1></div>
      <a class="btn btn-primary" href="#/admin/new">New 360</a>
    </div>
    <div class="tabs" role="tablist">
      <button role="tab" aria-selected="${listTab === "active"}" data-tab="active">Active</button>
      <button role="tab" aria-selected="${listTab === "closed"}" data-tab="closed">Closed</button>
    </div>
    ${table}
  </main>`;
  return {
    title: "Active 360s",
    html,
    mount(root, rerender) {
      root.querySelectorAll("[data-tab]").forEach((b) => b.addEventListener("click", () => { listTab = b.dataset.tab; rerender(); }));
    },
  };
}

export function renderAdminNew() {
  const courses = db.getState().courses;
  const html = `${head()}
  <main id="main" class="narrow page" tabindex="-1">
    <a class="back" href="#/admin">← Active 360s</a>
    <h1 class="h1">New 360</h1>
    <p class="muted">Set up the 360 and add the participant. Raters can be added by you or nominated by the participant.</p>
    <form id="new-form" class="section">
      <div class="form-row">
        <div class="field"><label for="f-rank">Rank</label><input class="input" id="f-rank" required placeholder="Capt"></div>
        <div class="field"><label for="f-first">First name</label><input class="input" id="f-first" required></div>
        <div class="field"><label for="f-last">Last name</label><input class="input" id="f-last" required></div>
      </div>
      <div class="field"><label for="f-unit">Unit</label><input class="input" id="f-unit" placeholder="e.g. 2/1 RNZIR"></div>
      <div class="form-row">
        <div class="field"><label for="f-course">Course</label><select class="select" id="f-course">${courses.map((c) => `<option value="${c.id}">${esc(c.name)}</option>`).join("")}</select></div>
        <div class="field"><label for="f-close">Close date</label><input class="input" id="f-close" type="date" required value="2026-10-16"></div>
      </div>
      <div class="actions"><button class="btn btn-primary" type="submit">Create 360</button><a class="btn btn-ghost" href="#/admin">Cancel</a></div>
    </form>
  </main>`;
  return {
    title: "New 360",
    html,
    mount(root) {
      root.querySelector("#new-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const v = (id) => root.querySelector(id).value.trim();
        const a = db.createAssessment({ rank: v("#f-rank"), firstName: v("#f-first"), lastName: v("#f-last"), unit: v("#f-unit") || "—", courseId: v("#f-course"), closeDate: v("#f-close") });
        toast("360 created");
        go(`#/admin/a/${a.id}`);
      });
    },
  };
}

export function renderAdminDetail(id) {
  const a = db.assessment(id);
  if (!a) return { title: "Not found", html: `${head()}<main id="main" class="wrap page" tabindex="-1"><p class="empty">360 not found.</p></main>` };
  const p = db.participant(a.participantId);
  const c = db.course(a.courseId);
  const { done, total } = db.completion(a);
  const outstanding = a.raters.filter((r) => r.status !== "completed");
  const st = statusOf(a);

  const submittedAt = (raterId) => db.responsesFor(a.id).find((x) => x.raterId === raterId)?.submittedAt || a.createdAt;
  const groupBlock = (key) => {
    const rs = a.raters.filter((r) => r.relationship === key);
    if (!rs.length) return "";
    const d = rs.filter((r) => r.status === "completed").length;
    return `
    <h3 class="h3">${relLabel(key, true)} <span class="muted num">${d} / ${rs.length}</span></h3>
    <ul class="list">${rs.map((r) => `
      <li>
        <div class="grow"><div class="name">${esc(r.name)}</div>
          <div class="sub">${esc(formatMobile(r.mobile))} · ${r.status === "completed" ? `submitted ${fmtDate(submittedAt(r.id))}` : `invited${r.lastReminded ? `, reminded ${fmtDate(r.lastReminded)}` : ""}`}</div></div>
        <span class="status ${r.status === "completed" ? "done" : "invited"}">${r.status === "completed" ? "Complete" : "Outstanding"}</span>
        ${a.status !== "closed" && r.status !== "completed" ? `<div class="rowbtns">
          <button class="btn btn-sm btn-ghost" data-act="remind" data-id="${r.id}">Remind</button>
          <button class="btn btn-sm btn-ghost" data-act="link" data-token="${r.token}" title="Copy the rater's link">Link</button>
          <button class="btn btn-sm btn-ghost" data-act="remove" data-id="${r.id}" data-name="${esc(r.name)}">Remove</button>
        </div>` : ""}
      </li>`).join("")}</ul>`;
  };

  const actions = a.status === "closed"
    ? `<a class="btn btn-primary" href="#/admin/a/${a.id}/report">View report</a><button class="btn btn-ghost" data-act="reopen">Reopen</button>`
    : `${a.status === "draft" ? `<button class="btn btn-primary" data-act="open" ${a.raters.length ? "" : "disabled"}>Open 360 and send invitations</button>` : ""}
       <button class="btn" data-act="add">Add rater</button>
       <button class="btn" data-act="remind-all" ${outstanding.length ? "" : "disabled"}>Send reminder${outstanding.length ? ` (${outstanding.length})` : ""}</button>
       <a class="btn" href="#/admin/a/${a.id}/report">Preview report</a>
       ${a.status === "open" ? `<button class="btn" data-act="close">Close 360</button>` : ""}`;

  const html = `${head()}
  <main id="main" class="wrap page" tabindex="-1">
    <a class="back" href="#/admin">← Active 360s</a>
    <div class="page-head">
      <div>
        <p class="eyebrow">${esc(c.name)}</p>
        <h1 class="h1">${esc(db.fullName(p))} <span class="muted" style="font-weight:400">— 360 Feedback</span></h1>
        <p class="muted">${esc(p.unit)} · ${statusPill(a)} · ${dueText(a)}</p>
      </div>
      <div class="actions">${actions}</div>
    </div>

    <div class="facts">
      <div class="fact"><div class="k">Overall completion</div><div class="v num">${done} / ${total}</div></div>
      <div class="fact"><div class="k">Self-assessment</div><div class="v">${a.selfCompleted ? "Complete" : "Outstanding"}</div></div>
      <div class="fact"><div class="k">Close date</div><div class="v">${fmtDate(a.closeDate)}</div></div>
      <div class="fact"><div class="k">Created</div><div class="v">${fmtDate(a.createdAt)}</div></div>
    </div>
    ${bar(done, total)}
    ${groupBars(a)}

    <div id="add-form-slot"></div>

    <h2 class="h2">Raters</h2>
    ${a.raters.length ? relationships.filter((r) => r.key !== "self").map((r) => groupBlock(r.key)).join("") : `<p class="muted">No raters yet. Add raters, or wait for ${esc(p.firstName)} to nominate.</p>`}

    <h2 class="h2">Activity</h2>
    <ul class="log">${[...a.log].reverse().map((l) => `<li><span>${fmtDate(l.at)}</span><span>${esc(l.text)}</span></li>`).join("")}</ul>
  </main>`;

  return {
    title: `${db.shortName(p)} — 360`,
    html,
    mount(root) {
      const slot = root.querySelector("#add-form-slot");
      const showAdd = () => {
        slot.innerHTML = `
        <form class="inline-form" id="add-form">
          <div class="form-row">
            <div class="field"><label for="a-name">Rank and name</label><input class="input" id="a-name" required placeholder="e.g. Capt Sam Reid"></div>
            <div class="field"><label for="a-mobile">Mobile</label><input class="input" id="a-mobile" type="tel" inputmode="tel" required placeholder="021 123 4567"></div>
            <div class="field"><label for="a-rel">Relationship</label><select class="select" id="a-rel">${relOptions("peer")}</select></div>
            <div class="field actions"><button class="btn btn-primary" type="submit">Add</button><button class="btn btn-ghost" type="button" data-act="cancel-add">Cancel</button></div>
          </div>
        </form>`;
        slot.querySelector("#a-name").focus();
        slot.querySelector("#add-form").addEventListener("submit", (e) => {
          e.preventDefault();
          const name = slot.querySelector("#a-name").value.trim();
          const mobile = normaliseMobile(slot.querySelector("#a-mobile").value);
          if (!name) return;
          if (!mobile) { toast("Enter a valid NZ mobile number"); return; }
          db.addRater(a.id, { name, mobile, relationship: slot.querySelector("#a-rel").value });
          toast(a.status === "open" ? `${name} added. Invitation sent by SMS (simulated).` : `${name} added. Invited when the 360 opens.`);
        });
      };
      root.addEventListener("click", async (e) => {
        const b = e.target.closest("[data-act]"); if (!b) return;
        const act = b.dataset.act;
        if (act === "add") showAdd();
        else if (act === "cancel-add") slot.innerHTML = "";
        else if (act === "remind") { db.remind(a.id, [b.dataset.id]); toast("Reminder sent (simulated)"); }
        else if (act === "remind-all") { const n = db.remind(a.id, outstanding.map((r) => r.id)); toast(`Reminder sent to ${plural(n, "rater")} (simulated)`); }
        else if (act === "remove") { if (ask(`Remove ${b.dataset.name} from this 360?`)) { db.removeRater(a.id, b.dataset.id); toast("Rater removed"); } }
        else if (act === "link") { const url = raterLink(b.dataset.token); await copyText(url); toast(`Rater link copied · <a href="${url}" style="color:#fff">open it</a>`); }
        else if (act === "open") { db.openAssessment(a.id); toast("360 opened. Invitations sent (simulated)."); }
        else if (act === "close") {
          if (ask(`Close this 360 with ${done} of ${total} responses? ${p.firstName} will be able to read the report.`)) { db.closeAssessment(a.id); toast("360 closed. Report released."); }
        }
        else if (act === "reopen") { db.reopenAssessment(a.id); toast("360 reopened"); }
      });
    },
  };
}
