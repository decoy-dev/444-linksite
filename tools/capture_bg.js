// Capture a still frame of the WebGL backdrop (relic + gradient), no HUD.
// Software WebGL so it renders without a GPU (see HANDOFF gotchas).
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    args: [
      '--use-gl=angle',
      '--use-angle=swiftshader',
      '--enable-unsafe-swiftshader',
      '--ignore-gpu-blocklist',
      '--enable-webgl',
    ],
  });
  const page = await browser.newPage({
    viewport: { width: 1200, height: 630 },
    deviceScaleFactor: 1,
  });
  page.on('console', m => console.log('[page]', m.text()));
  page.on('pageerror', e => console.log('[pageerror]', e.message));

  await page.goto('http://localhost:8779/', { waitUntil: 'load' });

  // Let the GLTF load + boot run, then force the final chrome backdrop.
  await page.waitForTimeout(12000);
  await page.evaluate(() => {
    if (window.__relicMode) window.__relicMode('solid');
    // strip every overlay/UI so only the backdrop remains
    for (const id of ['stage', 'boot', 'boot-fx', 'boot-flash', 'vignette', 'grain']) {
      const el = document.getElementById(id);
      if (el) el.style.display = 'none';
    }
    document.body.style.overflow = 'hidden';
  });
  // give the composer (bloom/DoF) several frames to settle
  await page.waitForTimeout(4000);

  await page.screenshot({ path: 'C:/Users/Chris/444-linksite/tools/bg-frame.png', animations: 'disabled', timeout: 120000 });
  console.log('captured bg-frame.png');
  await browser.close();
})();
