// Screenshot the preview pages written by src/preview.py.
//   node src/shoot.cjs [name ...]
const { chromium } = require("playwright");
const { readdirSync } = require("node:fs");
const { join, resolve } = require("node:path");

const dir = resolve(__dirname, "..", "assets", "previews");
const only = process.argv.slice(2);
const pages = readdirSync(dir).filter(
  (f) => f.endsWith(".html") && (!only.length || only.some((o) => f.startsWith(o))),
);

(async () => {
const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: 1280, height: 800 } });
for (const f of pages) {
  await page.goto("file://" + join(dir, f));
  await page.waitForLoadState("networkidle");
  const fullPage = f.startsWith("icons") || f.startsWith("banner") || f.startsWith("palettes");
  if (fullPage) await page.setViewportSize({ width: 1600, height: 800 });
  else await page.setViewportSize({ width: 1280, height: 800 });
  const target = fullPage ? page.locator("body") : page;
  await target.screenshot({ path: join(dir, f.replace(/\.html$/, ".png")) });
  console.log("shot", f);
}
await browser.close();
})();
