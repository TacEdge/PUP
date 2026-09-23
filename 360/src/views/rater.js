// The rater journey, phone first:
//   SMS → tap link → confirm mobile number → verification code → context →
//   one statement at a time → two short prompts → submit → done.
// A verified number is remembered on the device, so later links skip straight
// to the context screen. Progress is saved as a draft so an interrupted rater
// can pick up where they left off. Also reused for the participant's
// self-assessment (which skips identification in the prototype).
import { esc } from "../lib/html.js";
import * as db from "../lib/store.js";
import { instrument, allStatements, relationships } from "../data/instrument.js";
import { identity, normaliseMobile, maskMobile, formatMobile } from "../lib/auth.js";
import { LOGO } from "./shared.js";

const statements = allStatements();
const dimOf = (id) => instrument.dimensions.find((d) => d.id === id);
const TOUCH = () => window.matchMedia("(pointer: coarse)").matches;

// In-progress sessions: memory first, hydrated from the saved draft.
const sessions = new Map();
function session(key) {
  if (!sessions.has(key)) {
    const saved = db.draft(key);
    sessions.set(key, saved
      ? { ...saved, step: "landing", resumeStep: saved.step, otp: null, error: "" }
      : { step: "landing", resumeStep: null, qi: 0, pi: 0, ratings: {}, comments: {}, otp: null, error: "" });
  }
  return sessions.get(key);
}
function persistDraft(key, s) {
  if (["q", "prompt", "submit"].includes(s.step)) db.saveDraft(key, { step: s.step, qi: s.qi, pi: s.pi, ratings: s.ratings, comments: s.comments });
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

// ---- identify / verify screens (shared by the link flow and #/start) ------
function identifyScreen({ hint, error }) {
  return `
  <div class="auth q-enter">
    <p class="eyebrow">NZALC 360</p>
    <h1 class="h1">Enter your mobile number</h1>
    ${hint ? `<p class="muted">${hint}</p>` : `<p class="muted">We'll text you a code to confirm it's you.</p>`}
    <form id="identify-form" novalidate>
      <label class="sr-only" for="mobile">Mobile number</label>
      <input id="mobile" class="input input-xl" type="tel" inputmode="tel" autocomplete="tel" placeholder="021 123 4567" autofocus>
      ${error ? `<p class="error" role="alert">${esc(error)}</p>` : ""}
      <button class="btn btn-primary btn-lg btn-block" type="submit">Continue</button>
    </form>
    <p class="fine">Prototype only. Mobile-number sign-in stands in for an approved identity service.</p>
  </div>`;
}
function verifyScreen({ masked, devCode, error }) {
  return `
  <div class="auth q-enter">
    <p class="eyebrow">NZALC 360</p>
    <h1 class="h1">Verify your number</h1>
    <p class="muted">We've sent a verification code to<br><b class="num">${esc(masked)}</b></p>
    <form id="verify-form" novalidate>
      <label class="sr-only" for="code">Verification code</label>
      <input id="code" class="input input-otp num" inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]*" maxlength="6" placeholder="••••••" autofocus>
      ${error ? `<p class="error" role="alert">${esc(error)}</p>` : ""}
      <button class="btn btn-primary btn-lg btn-block" type="submit">Continue</button>
    </form>
    <p class="fine"><button class="link muted" type="button" data-act="change-number">Use a different number</button></p>
    <div class="devnote">
      <span class="tag">Prototype</span> No SMS is sent. Your code is <b class="num">${esc(devCode)}</b>. <button class="link" type="button" data-act="use-code" data-code="${esc(devCode)}">Use it</button>
    </div>
  </div>`;
}
function bindAuth(root, s, { expectedMobile, onVerified, rerender }) {
  const idForm = root.querySelector("#identify-form");
  if (idForm) idForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const raw = root.querySelector("#mobile").value;
    const m = normaliseMobile(raw);
    if (!m) { s.error = "That doesn't look like a NZ mobile number."; rerender(); return; }
    if (expectedMobile && m !== expectedMobile) { s.error = "That number doesn't match this request. Check the number, or ask NZALC staff to update it."; rerender(); return; }
    s.error = "";
    s.otp = await identity.requestCode(m);
    s.step = "verify";
    rerender();
  });
  const vForm = root.querySelector("#verify-form");
  if (vForm) {
    const input = root.querySelector("#code");
    const submit = async () => {
      const code = input.value.replace(/\D/g, "");
      if (code.length < 6) { s.error = "Enter the 6-digit code."; rerender(); return; }
      const ok = await identity.verify(s.otp.mobile, code);
      if (!ok) { s.error = "That code isn't right. Try again."; rerender(); return; }
      s.error = "";
      onVerified();
    };
    vForm.addEventListener("submit", (e) => { e.preventDefault(); submit(); });
    input.addEventListener("input", () => { if (input.value.replace(/\D/g, "").length === 6) submit(); });
    root.querySelector("[data-act=use-code]")?.addEventListener("click", (e) => { input.value = e.currentTarget.dataset.code; submit(); });
    root.querySelector("[data-act=change-number]")?.addEventListener("click", () => { s.step = "identify"; s.error = ""; rerender(); });
  }
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
    return { title: "Link not recognised", html: shell(`<div class="rater-landing"><p class="eyebrow">360 Feedback</p><h1 class="h1">This link isn't valid</h1><p class="lead">Check the link you were sent, or contact NZALC staff.</p><p><a class="link muted" href="#/start">Sign in with your mobile number instead</a></p></div>`) };
  }
  const { participant: p, assessment: a, relationship } = ctx;
  const first = p.firstName;
  const isSelf = relationship === "self";
  const who = isSelf ? "Self-assessment" : `About ${first}`;
  const s = session(ctx.key);

  // Identity: a link is bound to a rater's mobile number. A verified session
  // for that number skips identification.
  const authed = isSelf || identity.session()?.mobile === ctx.rater.mobile;
  if (!authed && !["identify", "verify"].includes(s.step)) { s.step = "identify"; }
  if (authed && ["identify", "verify"].includes(s.step)) { s.step = "landing"; }

  const alreadyDone = isSelf ? a.selfCompleted : ctx.rater.status === "completed";
  if (alreadyDone && s.step !== "done" && authed) {
    return { title: "Already submitted", html: shell(`<div class="rater-landing"><p class="eyebrow">360 Feedback</p><h1 class="h1">Already submitted</h1><p class="lead">${isSelf ? "Your self-assessment has been recorded." : `Your feedback for ${esc(first)} has been recorded. Thanks — you're done.`}</p>${isSelf ? `<p><a class="btn" href="#/me">Back to My 360</a></p>` : ""}</div>`, who) };
  }
  if (a.status === "closed" && authed) {
    return { title: "360 closed", html: shell(`<div class="rater-landing"><p class="eyebrow">360 Feedback</p><h1 class="h1">This 360 has closed</h1><p class="lead">Feedback for ${esc(first)} is no longer being collected.</p></div>`, who) };
  }

  const total = statements.length;
  const prompts = instrument.prompts;
  const answered = Object.keys(s.ratings).length;
  let inner = "";
  let title = `360 Feedback — ${first}`;

  if (s.step === "identify") {
    title = "Enter your mobile number";
    inner = identifyScreen({ hint: `This request was sent to <b class="num">${esc(maskMobile(ctx.rater.mobile))}</b>. Enter that number to continue.`, error: s.error });
  } else if (s.step === "verify") {
    title = "Verify your number";
    inner = verifyScreen({ masked: s.otp.masked, devCode: s.otp.devCode, error: s.error });
  } else if (s.step === "landing") {
    const relText = relationships.find((r) => r.key === relationship)?.label.toLowerCase();
    const resuming = !isSelf && answered > 0;
    inner = `
    <div class="rater-landing q-enter">
      <p class="eyebrow">360 Feedback</p>
      <h1 class="h1">${isSelf ? "Your self-assessment" : esc(`${p.firstName} ${p.lastName}`)}</h1>
      ${isSelf
        ? `<p class="lead">Rate yourself on the same statements your raters see. Your report compares the two.</p>`
        : `<p class="lead">You've been asked to provide feedback as a <b>${esc(relText)}</b>.</p>
           <p class="lead muted">Your feedback is confidential and contributes to ${esc(first)}'s leadership development.</p>`}
      <p class="time">${resuming ? `You're ${answered} of ${total} statements in.` : `About <b>${instrument.estimatedMinutes} minutes</b>`}</p>
      <button class="btn btn-primary btn-lg btn-block" data-act="begin">${resuming ? "Continue" : "Start"}</button>
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
      <p class="tiny muted ask">${isSelf ? "How often is this true of you?" : `How often is this true of ${esc(first)}?`}</p>
      <div class="scale" role="group" aria-labelledby="stmt">
        ${instrument.scale.map((o) => `
          <button class="rate" data-act="rate" data-value="${o.value}" aria-pressed="${chosen === o.value}">
            ${esc(o.label)} <span class="key" aria-hidden="true">${o.hotkey}</span>
          </button>`).join("")}
      </div>
      <div class="scale-foot">
        <button class="btn btn-ghost back-btn" data-act="back" aria-label="Back">←</button>
        <button class="rate-no" data-act="rate" data-value="null" aria-pressed="${chosen === null}">${esc(instrument.notObserved.label)}</button>
        ${chosen !== undefined ? `<button class="btn btn-ghost" data-act="next" aria-label="Next">→</button>` : `<span class="back-spacer"></span>`}
      </div>
    </div>`;
  } else if (s.step === "prompt") {
    const pr = prompts[s.pi];
    const q = isSelf ? pr.question.replace(/\{first\}/g, "you") : pr.question.replace(/\{first\}/g, first);
    const val = s.comments[pr.id] || "";
    title = `${pr.heading} — 360 Feedback`;
    inner = `
    <div class="progress"><span class="num">${s.pi + 1} of ${prompts.length}</span><div class="bar thin"><i style="width:${Math.round((total + s.pi) / (total + prompts.length) * 100)}%"></i></div></div>
    <div class="q q-enter">
      <p class="eyebrow">${esc(pr.heading)}</p>
      <label class="prompt" for="comment">${esc(q)}</label>
      <p class="prompt-hint">${esc(pr.hint)}${TOUCH() ? " Tap the microphone on your keyboard to dictate." : ""}</p>
      <textarea id="comment" class="textarea" rows="4" maxlength="600" autocapitalize="sentences" enterkeyhint="done">${esc(val)}</textarea>
      <div class="q-nav">
        <button class="btn btn-ghost" data-act="back">← Back</button>
        <div class="actions">
          <button class="btn btn-ghost" data-act="skip">Skip</button>
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
        <button class="btn btn-primary btn-lg" data-act="submit">${isSelf ? "Submit" : "Submit feedback"}</button>
      </div>
    </div>`;
  } else if (s.step === "done") {
    title = "Feedback submitted — 360 Feedback";
    inner = `
    <div class="done q-enter">
      <div class="tick" aria-hidden="true">✓</div>
      <h1 class="h1">${isSelf ? "Self-assessment submitted" : "Feedback submitted"}</h1>
      <p class="lead">${isSelf ? `Thanks — you're done. Your report compares this with your raters' feedback.` : `Thanks — you're done.`}</p>
      ${isSelf ? `<p><a class="btn btn-primary" href="#/me">Back to My 360</a></p>` : `<p class="muted small">Your feedback will contribute to ${esc(first)}'s leadership development. You can close this page.</p>`}
    </div>`;
  }

  return {
    title,
    html: shell(inner, s.step === "identify" || s.step === "verify" ? "" : who),
    mount(root, rerender) {
      let advancing = false;
      const save = () => persistDraft(ctx.key, s);

      const next = () => {
        if (s.step === "landing") s.step = "q";
        else if (s.step === "q") { if (s.qi < total - 1) s.qi += 1; else { s.step = "prompt"; s.pi = 0; } }
        else if (s.step === "prompt") { if (s.pi < prompts.length - 1) s.pi += 1; else s.step = "submit"; }
        save(); rerender();
      };
      const back = () => {
        if (s.step === "q") { if (s.qi > 0) s.qi -= 1; else s.step = "landing"; }
        else if (s.step === "prompt") { if (s.pi > 0) s.pi -= 1; else { s.step = "q"; s.qi = total - 1; } }
        else if (s.step === "submit") { s.step = "prompt"; s.pi = prompts.length - 1; }
        save(); rerender();
      };
      const saveComment = () => {
        const ta = root.querySelector("#comment");
        if (ta && s.step === "prompt") s.comments[prompts[s.pi].id] = ta.value;
      };
      const rate = (value) => {
        if (advancing) return;
        const st = statements[s.qi];
        s.ratings[st.id] = value;
        save();
        root.querySelectorAll("[data-act=rate]").forEach((b) => b.setAttribute("aria-pressed", String(String(value) === b.dataset.value)));
        advancing = true;
        const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        setTimeout(() => { advancing = false; next(); }, reduced ? 80 : 300);
      };

      if (s.step === "identify" || s.step === "verify") {
        bindAuth(root, s, { expectedMobile: ctx.rater?.mobile, rerender, onVerified: () => { s.step = "landing"; rerender(); } });
        return () => {};
      }

      root.addEventListener("click", (e) => {
        const btn = e.target.closest("[data-act]");
        if (!btn) return;
        const act = btn.dataset.act;
        if (act === "begin") { s.step = s.resumeStep || "q"; s.resumeStep = null; save(); rerender(); }
        else if (act === "rate") rate(btn.dataset.value === "null" ? null : Number(btn.dataset.value));
        else if (act === "next") { saveComment(); next(); }
        else if (act === "skip") { if (s.step === "prompt") s.comments[prompts[s.pi].id] = ""; next(); }
        else if (act === "back") { saveComment(); back(); }
        else if (act === "submit") {
          const ratings = {};
          for (const st of statements) ratings[st.id] = s.ratings[st.id] === undefined ? null : s.ratings[st.id];
          const comments = {};
          for (const [k, v] of Object.entries(s.comments)) if (v && v.trim()) comments[k] = v.trim();
          db.clearDraft(ctx.key);
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
        if (ta && !TOUCH()) ta.focus();
      }
      return () => {};
    },
  };
}

// ---- #/start: opened without a link ------------------------------------
const startState = { step: "identify", otp: null, error: "" };
export function renderStart() {
  const sess = identity.session();
  let inner = "";
  let title = "NZALC 360";
  if (sess && startState.step !== "verify") startState.step = "list";
  if (startState.step === "identify") {
    title = "Enter your mobile number";
    inner = identifyScreen({ error: startState.error });
  } else if (startState.step === "verify") {
    title = "Verify your number";
    inner = verifyScreen({ masked: startState.otp.masked, devCode: startState.otp.devCode, error: startState.error });
  } else {
    const reqs = db.requestsForMobile(sess.mobile).filter((r) => r.assessment.status === "open");
    const pending = reqs.filter((r) => r.rater.status !== "completed");
    const done = reqs.filter((r) => r.rater.status === "completed");
    inner = `
    <div class="rater-landing q-enter">
      <p class="eyebrow">NZALC 360 · ${esc(formatMobile(sess.mobile))}</p>
      <h1 class="h1">Your feedback requests</h1>
      ${pending.length ? `<ul class="requests">${pending.map(({ assessment: a, rater: r }) => { const p = db.participant(a.participantId); return `
        <li><a class="req" href="#/r/${r.token}">
          <span class="grow"><b>${esc(`${p.firstName} ${p.lastName}`)}</b><small>As a ${esc(relationships.find((x) => x.key === r.relationship)?.label.toLowerCase())} · about ${instrument.estimatedMinutes} minutes</small></span><span aria-hidden="true">→</span></a></li>`; }).join("")}</ul>`
        : `<p class="lead muted">Nothing waiting for you right now.</p>`}
      ${done.length ? `<p class="small muted" style="margin-top:1.5rem">Completed: ${done.map(({ assessment: a }) => esc(db.participant(a.participantId).firstName)).join(", ")}.</p>` : ""}
      <p class="fine"><button class="link muted" data-act="signout">Not you? Sign out</button></p>
    </div>`;
  }
  return {
    title,
    html: shell(inner),
    mount(root, rerender) {
      bindAuth(root, startState, { rerender, onVerified: () => { startState.step = "list"; rerender(); } });
      root.querySelector("[data-act=signout]")?.addEventListener("click", () => { identity.signOut(); startState.step = "identify"; rerender(); });
    },
  };
}
