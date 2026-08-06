// COMBAT MINDSET : notation family, issued as assets.
//
// The identity system holds the notation as one source consumed by every
// surface. This emits the pilot set as PNGs so the Word and PowerPoint
// builders draw from the same geometry rather than redrawing it.
//
// Every mark: 24 unit grid, 2 unit stroke, datum at y=17.

const sharp = require("sharp");
const fs = require("fs");
const path = require("path");

const BLACK = "000000";
const RED = "D31145";
const G_DARK = "00261B";
const G_OLIVE = "444D06";

// Pilot set only. Candidate extensions are not issued as assets until the
// pilot shows the distinction is needed.
const MARKS = {
  framework: [`<path d="M2,17 H22"/><path d="M2,7 H22"/><path d="M7,7 V17"/><path d="M12,7 V17"/><path d="M17,7 V17"/>`, BLACK],
  governance: [`<path d="M2,17 H22"/><path d="M6,4 H2 V13 H6"/><path d="M18,4 H22 V13 H18"/><rect x="9" y="7" width="6" height="4" fill="currentColor" stroke="none"/>`, BLACK],
  evidence: [`<path d="M2,17 H22"/><path d="M6,17 V13"/><path d="M11,17 V10"/><path d="M16,17 V7"/><path d="M21,17 V4"/>`, G_DARK],
  assessment: [`<path d="M2,17 H22"/><rect x="2" y="8" width="8" height="4" fill="currentColor" stroke="none"/><rect x="14" y="8" width="8" height="4" fill="currentColor" stroke="none"/><path d="M12,5 V15"/>`, G_DARK],
  product: [`<path d="M2,17 H22"/><rect x="8" y="8" width="9" height="9" fill="currentColor" stroke="none"/>`, G_OLIVE],
  decision: [`<path d="M2,17 H22"/><path d="M12,17 L20,6"/><circle cx="12" cy="17" r="3.2" fill="#FFFFFF"/>`, RED],
};

const OUT = "assets/marks";

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  for (const [key, [body, colour]] of Object.entries(MARKS)) {
    for (const [suffix, ink] of [["", colour], ["-mono", BLACK]]) {
      const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">` +
        `<g fill="none" stroke="#${ink}" stroke-width="2" stroke-linecap="square" ` +
        `color="#${ink}">${body}</g></svg>`;
      const file = path.join(OUT, `${key}${suffix}.png`);
      await sharp(Buffer.from(svg)).resize(400, 400).png().toFile(file);
    }
  }
  console.log(`written ${Object.keys(MARKS).length} pilot marks to ${OUT}/ (classification and mono)`);
})();
