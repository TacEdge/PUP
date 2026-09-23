// Tiny templating helpers. Views return HTML strings; `esc` protects any
// user-entered or seeded text.
export const esc = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

export const fmtDate = (iso) => {
  if (!iso) return "";
  const d = new Date(iso + "T00:00:00");
  return d.toLocaleDateString("en-NZ", { day: "numeric", month: "short", year: "numeric" });
};

export const daysBetween = (fromISO, toISO) =>
  Math.round((new Date(toISO + "T00:00:00") - new Date(fromISO + "T00:00:00")) / 86400000);

export const plural = (n, one, many = one + "s") => `${n} ${n === 1 ? one : many}`;
