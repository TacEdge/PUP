// The rater journey: landing → one statement at a time → short prompts →
// submit → done. Also reused for the participant's self-assessment.
import { esc } from "../lib/html.js";
import * as db from "../lib/store.js";
import { instrument, allStatements, relationships } from "../data/instrument.js";
import { go } from "../lib/ui.js";
import { LOGO } from "./shared.js";

const statements = allStatements();
const dimOf = (id) => instrument.dimensions.find((d) => d.id === id);

// In-progress sessions live in memory only; nothing is stored until submit.
const sessions = new Map();
function session(key) {
  if (!sessions.has(key)) sessions.set(key, { step: "landing", qi: 0, pi: 0, ratings: {}, comments: {} });
  return sessions.get(key);
}

function shell(inner, who) {
  return `
  <div class="rater">
    <div class="rater-top">
      <img src="${LOGO}" alt="New Zealand Army">
      <span>360 Feedback</span>
      ${who ? `<span class="who">${esc(who)}</span>` : ""}
    </div>
    <main id="main" class="rater-body" tabindex="-1">${inner}</main>
  </div>`;
}

function confidentialityLine(relationship, first) {
  const rel = relationships.find((r) => r.key === relationship);
  if (relationship === "self") return `Your self-assessment is compared with the aggregated view of your raters in your report.`;
  if (rel?.anonymised) return `Your answers are combined with those of other ${rel.plural.toLowerCase()} before ${first} sees them. Your name is never shown against a rating or comment.`;
  return `${rel.label} feedback is reported as a group. Your name is never shown against a rating or comment, but with few ${rel.plural.toLowerCase()} your feedback may be recognisable.`;
}

// ---- resolve the token into a context ----------------------------------
export function raterContext(token) {
  const hit = db.raterByToken(token);
  if (!hit) return null;
  const p = db.participant(hit.assessment.participantId);
  return { key: token, assessment: hit.assessment, rater: hit.rater, participant: p, relationship: hit.rater.relationship };
}
export function selfContext(participantId) {
  const a = db.assessmentForParticipant(participantId);
  if (!a) return null;
  return { key: `self:${a.id}`, assessment: a, rater: null, participant: db.participant(participantId), relationship: "self" };
}

export function renderRater(ctx) {
  if (!ctx) {
    return { title: "Link not recognised", html: shell(`<div class="rater-landing"><p class="eyebrow">360 Feedback</p><h1 class="h1">This link isn't valid</h1><p class="lead">Check the link you were sent, or contact NZALC staff.</p></div>`) };
  }
  const { participant: p, assessment: a, relationship } = ctx;
  const first = p.firstName;
  const isSelf = relationship === "self";
  const who = isSelf ? "Self-assessment" : `About ${first}`;
  const s = session(ctx.key);

  const alreadyDone = isSelf ? a.selfCompleted : ctx.rater.status === "completed";
  if (alreadyDone && s.step !== "done") {
    return { title: "Already submitted", html: shell(`<div class="rater-landing"><p class="eyebrow">360 Feedback</p><h1 class="h1">Already submitted</h1><p class="lead">${isSelf ? "Your self-assessment has been recorded." : `Your feedback for ${esc(first)} has been recorded. Thank you.`}</p>${isSelf ? `<p><a class="btn" href="#/me">Back to My 360</a></p>` : ""}</div>`, who) };
  }
  if (a.status === "closed") {
    return { title: "360 closed", html: shell(`<div class="rater-landing"><p class="eyebrow">360 Feedback</p><h1 class="h1">This 360 has closed</h1><p class="lead">Feedback for ${esc(first)} is no longer being collected.</p></div>`, who) };
  }

  const total = statements.length;
  let inner = "";
  let title = `360 Feedback — ${first}`;

  if (s.step === "landing") {
    const relText = relationships.find((r) => r.key === relationship)?.label.toLowerCase();
    inner = `
    <div class="rater-landing q-enter">
      <p class="eyebrow">360 Feedback</p>
      <h1 class="h1">${isSelf ? "Your self-assessment" : esc(`${p.firstName} ${p.lastName}`)}</h1>
      ${isSelf
        ? `<p class="lead">Rate yourself on the same statements your raters see. Your report compares the two.</p>`
        : `<p class="lead">You have been asked to provide feedback as a <b>${esc(relText)}</b>.</p>
           <p class="lead muted">Your feedback contributes to ${esc(first)}'s leadership development.</p>`}
      <p class="time">Approx. <b>${instrument.estimatedMinutes} minutes</b> · ${total} short statements and ${isSelf ? "2" : instrument.prompts.length} short questions</p>
      <button class="btn btn-primary btn-lg btn-block" data-act="begin">${isSelf ? "Begin self-assessment" : "Begin feedback"}</button>
      <p class="fine">${confidentialityLine(relationship, first)}</p>
    </div>`;
  } else if (s.step === "q") {
    const st = statements[s.qi];
    const dim = dimOf(st.dimensionId);
    const chosen = s.ratings[st.id];
    const pct = Math.round((s.qi / total) * 100);
    title = `${s.qi + 1} of ${total} — 360 Feedback`;
    inner = `
    <div class="progress"><span class="num">${s.qi + 1} of ${total}</span><div class="bar thin"><i style="width:${pct}%"></i></div></div>
    <div class="q q-enter" data-q="${st.id}">
      <p class="eyebrow">${esc(dim.name)}</p>
      <h1 class="statement" id="stmt">${esc(st.text)}</h1>
      <div class="scale" role="group" aria-labelledby="stmt">
        ${instrument.scale.map((o) => `
          <button class="rate" data-act="rate" data-value="${o.value}" aria-pressed="${chosen === o.value}">
            ${esc(o.label)} <span class="key" aria-hidden="true">${o.hotkey}</span>
          </button>`).join("")}
      </div>
      <div class="scale-foot">
        <button class="rate-no" data-act="rate" data-value="null" aria-pressed="${chosen === null}">${esc(instrument.notObserved.label)}</button>
        <span class="tiny muted">${isSelf ? "How often is this true of you?" : `How often is this true of ${esc(first)}?`}</span>
      </div>
      <div class="q-nav">
        <button class="btn btn-ghost" data-act="back">← Back</button>
        ${chosen !== undefined ? `<button class="btn" data-act="next">Next</button>` : ""}
      </div>
    </div>`;
  } else if (s.step === "prompt") {
    const prompts = isSelf ? instrument.prompts.filter((x) => !x.optional) : instrument.prompts;
    const pr = prompts[s.pi];
    const q = isSelf
      ? pr.question.replace("{first}'s", "your").replace("{first} should", "you should").replace("{first}", "you")
      : pr.question.replace(/\{first\}/g, first);
    const val = s.comments[pr.id] || "";
    title = `${pr.heading} — 360 Feedback`;
    inner = `
    <div class="progress"><span class="num">${s.pi + 1} of ${prompts.length}</span><div class="bar thin"><i style="width:${Math.round((total + s.pi) / (total + prompts.length) * 100)}%"></i></div></div>
    <div class="q q-enter">
      <p class="eyebrow">${esc(pr.heading)}${pr.optional ? " · optional" : ""}</p>
      <label class="prompt" for="comment">${esc(q)}</label>
      <p class="prompt-hint">${esc(pr.hint)}</p>
      <textarea id="comment" class="textarea" rows="4" maxlength="600" placeholder="${pr.optional ? "" : "A sentence or two…"}">${esc(val)}</textarea>
      <div class="q-nav">
        <button class="btn btn-ghost" data-act="back">← Back</button>
        <div class="actions">
          ${pr.optional || !val.trim() ? `<button class="btn btn-ghost" data-act="skip">Skip</button>` : ""}
          <button class="btn btn-primary" data-act="next">Continue</button>
        </div>
      </div>
    </div>`;
  } else if (s.step === "submit") {
    const rated = Object.values(s.ratings).filter((v) => typeof v === "number").length;
    const notObs = Object.values(s.ratings).filter((v) => v === null).length;
    const comments = Object.values(s.comments).filter((v) => v && v.trim()).length;
    title = "Ready to submit — 360 Feedback";
    inner = `
    <div class="q q-enter">
      <p class="eyebrow">Ready to submit</p>
      <h1 class="prompt">${isSelf ? "Submit your self-assessment?" : `Submit your feedback for ${esc(first)}?`}</h1>
      <ul class="submit-summary">
        <li><span>Statements rated</span><span class="num">${rated}${notObs ? ` <span class="muted">(${notObs} not observed)</span>` : ""}</span></li>
        <li><span>Written answers</span><span class="num">${comments}</span></li>
      </ul>
      <p class="small muted">${confidentialityLine(relationship, first)} Once submitted, answers can't be changed.</p>
      <div class="q-nav">
        <button class="btn btn-ghost" data-act="back">← Back</button>
        <button class="btn btn-primary btn-lg" data-act="submit">${isSelf ? "Submit self-assessment" : "Submit feedback"}</button>
      </div>
    </div>`;
  } else if (s.step === "done") {
    title = "Feedback submitted — 360 Feedback";
    inner = `
    <div class="done q-enter">
      <div class="tick" aria-hidden="true">✓</div>
      <h1 class="h1">${isSelf ? "Self-assessment submitted" : "Feedback submitted"}</h1>
      <p class="lead">${isSelf
        ? `Thank you. Your self-assessment will be compared with your raters' feedback in your report.`
        : `Thank you. Your feedback has been recorded and will contribute to ${esc(first)}'s leadership development.`}</p>
      ${isSelf ? `<p><a class="btn btn-primary" href="#/me">Back to My 360</a></p>` : `<p class="muted small">You can close this page.</p>`}
    </div>`;
  }

  return {
    title,
    html: shell(inner, who),
    mount(root, rerender) {
      const total = statements.length;
      const prompts = isSelf ? instrument.prompts.filter((x) => !x.optional) : instrument.prompts;
      let advancing = false;

      const next = () => {
        if (s.step === "landing") s.step = "q";
        else if (s.step === "q") { if (s.qi < total - 1) s.qi += 1; else { s.step = "prompt"; s.pi = 0; } }
        else if (s.step === "prompt") { if (s.pi < prompts.length - 1) s.pi += 1; else s.step = "submit"; }
        rerender();
      };
      const back = () => {
        if (s.step === "q") { if (s.qi > 0) s.qi -= 1; else s.step = "landing"; }
        else if (s.step === "prompt") { if (s.pi > 0) s.pi -= 1; else { s.step = "q"; s.qi = total - 1; } }
        else if (s.step === "submit") { s.step = "prompt"; s.pi = prompts.length - 1; }
        rerender();
      };
      const saveComment = () => {
        const ta = root.querySelector("#comment");
        if (ta && s.step === "prompt") s.comments[prompts[s.pi].id] = ta.value;
      };
      const rate = (value) => {
        if (advancing) return;
        const st = statements[s.qi];
        s.ratings[st.id] = value;
        root.querySelectorAll("[data-act=rate]").forEach((b) => b.setAttribute("aria-pressed", String(String(value) === b.dataset.value)));
        advancing = true;
        const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        setTimeout(() => { advancing = false; next(); }, reduced ? 80 : 320);
      };

      root.addEventListener("click", (e) => {
        const btn = e.target.closest("[data-act]");
        if (!btn) return;
        const act = btn.dataset.act;
        if (act === "begin") next();
        else if (act === "rate") rate(btn.dataset.value === "null" ? null : Number(btn.dataset.value));
        else if (act === "next") { saveComment(); next(); }
        else if (act === "skip") { if (s.step === "prompt") s.comments[prompts[s.pi].id] = ""; next(); }
        else if (act === "back") { saveComment(); back(); }
        else if (act === "submit") {
          const ratings = {};
          for (const st of statements) ratings[st.id] = s.ratings[st.id] === undefined ? null : s.ratings[st.id];
          const comments = {};
          for (const [k, v] of Object.entries(s.comments)) if (v && v.trim()) comments[k] = v.trim();
          db.submitResponse({ assessmentId: a.id, raterId: ctx.rater?.id ?? null, relationship, ratings, comments });
          s.step = "done";
          rerender();
        }
      });

      if (s.step === "q") {
        root.querySelector("main").focus({ preventScroll: true });
        const onKey = (e) => {
          if (e.target.matches("input, textarea")) return;
          const opt = instrument.scale.find((o) => o.hotkey === e.key);
          if (opt) { e.preventDefault(); rate(opt.value); }
          else if (e.key.toLowerCase() === instrument.notObserved.hotkey) { e.preventDefault(); rate(null); }
          else if (e.key === "ArrowLeft" || e.key === "Backspace") { e.preventDefault(); back(); }
          else if ((e.key === "ArrowRight" || e.key === "Enter") && s.ratings[statements[s.qi].id] !== undefined) { e.preventDefault(); next(); }
        };
        document.addEventListener("keydown", onKey);
        return () => document.removeEventListener("keydown", onKey);
      }
      if (s.step === "prompt") {
        const ta = root.querySelector("#comment");
        if (ta && window.matchMedia("(min-width: 40rem)").matches) ta.focus();
      }
      return () => {};
    },
  };
}
