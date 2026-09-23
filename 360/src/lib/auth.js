// Mobile-number identity for the prototype.
//
// The app talks only to the `identity` interface below:
//   requestCode(mobile)  -> Promise<{ masked }>   send a one-time code
//   verify(mobile, code) -> Promise<boolean>      check the code, start a session
//   session()            -> { mobile, verifiedAt } | null
//   signOut()
//
// `MockSmsIdentity` generates codes locally and drops them into the simulated
// SMS inbox in the store. A production build would swap in a provider backed
// by an approved identity and SMS service with the same interface. Nothing
// here is suitable for operational Defence use as it stands.
import * as db from "./store.js";

const SESSION_KEY = "nzalc-360-auth";
export const DEV_CODE = "000000"; // accepted by the mock provider only

// ---- NZ mobile number helpers ------------------------------------------
export function normaliseMobile(input) {
  let d = String(input || "").replace(/[^\d+]/g, "");
  if (d.startsWith("+64")) d = "0" + d.slice(3);
  else if (d.startsWith("64") && d.length >= 11) d = "0" + d.slice(2);
  if (!/^02\d{7,9}$/.test(d)) return null;
  return d;
}
export function formatMobile(m) {
  const d = normaliseMobile(m);
  if (!d) return m;
  return `${d.slice(0, 3)} ${d.slice(3, 6)} ${d.slice(6)}`;
}
export function maskMobile(m) {
  const d = normaliseMobile(m);
  if (!d) return "";
  return `${d.slice(0, 3)} ••• ••${d.slice(-2)}`;
}

// ---- mock provider ------------------------------------------------------
class MockSmsIdentity {
  constructor() { this.pending = new Map(); }

  async requestCode(mobile) {
    const m = normaliseMobile(mobile);
    if (!m) throw new Error("Enter a valid NZ mobile number.");
    const code = String(Math.floor(100000 + Math.random() * 900000));
    this.pending.set(m, { code, at: Date.now() });
    db.sendSms({ to: m, kind: "code", text: `${code} is your NZALC 360 verification code. It expires in 10 minutes.` });
    return { masked: maskMobile(m), mobile: m, devCode: code };
  }

  async verify(mobile, code) {
    const m = normaliseMobile(mobile);
    const p = this.pending.get(m);
    const ok = Boolean(m) && (code === DEV_CODE || (p && p.code === code && Date.now() - p.at < 10 * 60 * 1000));
    if (!ok) return false;
    this.pending.delete(m);
    try { localStorage.setItem(SESSION_KEY, JSON.stringify({ mobile: m, verifiedAt: new Date().toISOString() })); } catch (_) {}
    return true;
  }

  session() {
    try { const raw = localStorage.getItem(SESSION_KEY); return raw ? JSON.parse(raw) : null; } catch (_) { return null; }
  }

  signOut() { try { localStorage.removeItem(SESSION_KEY); } catch (_) {} }
}

export const identity = new MockSmsIdentity();
