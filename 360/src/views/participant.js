// Participant view: My 360.
import { esc, fmtDate } from "../lib/html.js";
import * as db from "../lib/store.js";
import { toast } from "../lib/ui.js";
import { topbar, statusPill, statusOf, dueText, groupBars, relLabel, relOptions, bar } from "./shared.js";
import { normaliseMobile } from "../lib/auth.js";

export function renderParticipant(participantId) {
  const p = db.participant(participantId);
  const a = db.assessmentForParticipant(participantId);
  const nav = [{ href: "#/me", label: "My 360" }];
  if (a && a.status === "closed") nav.push({ href: `#/report/${a.id}`, label: "My report" });
  const head = topbar({ nav, current: "#/me" });

  if (!a) {
    return { title: "My 360", html: `${head}<main id="main" class="reading page" tabindex="-1"><p class="eyebrow">My 360</p><h1 class="h1">No 360 yet</h1><p class="lead muted">When NZALC sets one up for you it will appear here.</p></main>` };
  }

  const c = db.course(a.courseId);
  const { done, total } = db.completion(a);
  const st = statusOf(a);
  const canNominate = a.status !== "closed";

  const raterList = a.raters.length
    ? `<ul class="list">${a.raters.map((r) => `<li><div class="grow"><div class="name">${esc(r.name)}</div><div class="sub">${relLabel(r.relationship)}</div></div></li>`).join("")}</ul>`
    : `<p class="muted">No raters nominated yet.</p>`;

  const html = `${head}
  <main id="main" class="reading page" tabindex="-1">
    <p class="eyebrow">My 360</p>
    <div class="page-head">
      <div>
        <h1 class="h1">${esc(c.name)}</h1>
        <p class="muted">${esc(db.fullName(p))} · ${esc(p.unit)}</p>
      </div>
    </div>

    ${a.status === "closed" ? `
    <div class="callout">
      <p><b>Your report is ready.</b> Read it before your development conversation with NZALC staff.</p>
      <a class="btn btn-primary" href="#/report/${a.id}">Open my report</a>
    </div>` : ""}

    <div class="facts">
      <div class="fact"><div class="k">Status</div><div class="v">${st.label}</div></div>
      <div class="fact"><div class="k">Raters complete</div><div class="v num">${done} of ${total}</div></div>
      <div class="fact"><div class="k">${a.status === "closed" ? "Closed" : "Closes"}</div><div class="v">${fmtDate(a.status === "closed" ? (a.closedAt || a.closeDate) : a.closeDate)}</div><div class="tiny muted">${a.status === "closed" ? "" : dueText(a)}</div></div>
      <div class="fact"><div class="k">Self-assessment</div><div class="v">${a.selfCompleted ? "Complete" : `<a class="btn btn-sm btn-primary" href="#/me/self">Complete now</a>`}</div></div>
    </div>

    <p class="lead">This 360 gathers a rounded view of how you lead, from the people who see it most. It is for your development on ${esc(c.name)}, not for reporting or performance management.</p>
    <p class="muted small">You will see feedback aggregated by rater group, never who said what. Only you and NZALC staff see your report.</p>

    <h2 class="h2">Rater completion</h2>
    ${groupBars(a)}
    ${a.status === "draft" ? `<p class="muted small">Aim for 2 superiors, 3 to 4 peers and 3 to 4 subordinates. Groups with fewer than 3 responses cannot be shown separately in your report.</p>` : ""}

    <h2 class="h2">Your raters</h2>
    ${raterList}
    ${canNominate ? `
    <details class="plain" id="nominate" ${a.status === "draft" ? "open" : ""}>
      <summary>Nominate a rater</summary>
      <form class="inline-form" id="nominate-form">
        <div class="form-row">
          <div class="field"><label for="n-name">Rank and name</label><input class="input" id="n-name" required placeholder="e.g. Capt Sam Reid"></div>
          <div class="field"><label for="n-mobile">Mobile</label><input class="input" id="n-mobile" type="tel" inputmode="tel" required placeholder="021 123 4567"></div>
          <div class="field"><label for="n-rel">Relationship</label><select class="select" id="n-rel">${relOptions("peer")}</select></div>
          <div class="field"><button class="btn btn-primary" type="submit">Add rater</button></div>
        </div>
        <p class="hint">They will receive a text message with a link (simulated in this prototype). NZALC staff can see and adjust your nominations.</p>
      </form>
    </details>` : ""}
  </main>`;

  return {
    title: "My 360",
    html,
    mount(root) {
      const form = root.querySelector("#nominate-form");
      if (form) form.addEventListener("submit", (e) => {
        e.preventDefault();
        const name = root.querySelector("#n-name").value.trim();
        const mobile = normaliseMobile(root.querySelector("#n-mobile").value);
        const relationship = root.querySelector("#n-rel").value;
        if (!name) return;
        if (!mobile) { toast("Enter a valid NZ mobile number"); return; }
        db.addRater(a.id, { name, mobile, relationship, by: p.firstName });
        toast(`${name} added. ${a.status === "open" ? "Invitation sent by SMS (simulated)." : "Invited when the 360 opens."}`);
      });
    },
  };
}
