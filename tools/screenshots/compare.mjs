// compare.mjs — capture side-by-side screenshots of LINZ vs accessible styles at
// real NZ locations, under each vision/lighting simulation.
//
//   npm i --no-save playwright@1 && npx playwright install chromium
//   python3 -m http.server 8000 &          # from repo root
//   LINZ_API_KEY=... node tools/screenshots/compare.mjs [scenario-id ...]
//
// Writes docs/visuals/real/<scenario>/<sim>.png. Commit the ones worth keeping
// with a research-log entry describing what they show.
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

const key = process.env.LINZ_API_KEY;
if (!key) { console.error("Set LINZ_API_KEY"); process.exit(1); }
const base = process.env.PREVIEW_URL || "http://localhost:8000/preview/";
const variant = process.env.VARIANT || "accessible-v0";
const sims = (process.env.SIMS || "none,deutan,protan,tritan,grey,red").split(",");
const all = JSON.parse(fs.readFileSync(new URL("./scenarios.json", import.meta.url)));
const wanted = process.argv.slice(2);
const scenarios = wanted.length ? all.filter(s => wanted.includes(s.id)) : all;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1400, height: 700 }, deviceScaleFactor: 2 });
for (const s of scenarios) {
  for (const sim of sims) {
    const url = `${base}?key=${encodeURIComponent(key)}&variant=${variant}&sim=${sim}#${s.zoom}/${s.lat}/${s.lon}`;
    await page.goto(url);
    await page.waitForFunction(() => window.__mapsIdle >= 2, null, { timeout: 60000 });
    await page.waitForTimeout(500); // let label fade-in finish
    const out = path.join("docs/visuals/real", s.id, `${sim}.png`);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await page.locator("main").screenshot({ path: out });
    console.log("wrote", out);
  }
}
await browser.close();
