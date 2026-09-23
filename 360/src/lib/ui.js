// Small UI utilities shared by views.
let toastTimer = null;
export function toast(msg) {
  const el = document.getElementById("toast");
  el.innerHTML = `<div class="toast">${msg}</div>`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.innerHTML = ""; }, 2600);
}
export const go = (hash) => { location.hash = hash; };
export const ask = (msg) => window.confirm(msg);
export function copyText(text) {
  if (navigator.clipboard?.writeText) return navigator.clipboard.writeText(text).catch(() => false);
  return Promise.resolve(false);
}
export const raterLink = (token) => `${location.origin}${location.pathname}#/r/${token}`;
