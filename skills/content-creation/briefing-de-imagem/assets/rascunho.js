#!/usr/bin/env node
/**
 * rascunho.js — render a fixed-size composition sketch (HTML/SVG) to a PNG.
 *
 * Zero-dependency: drives an already-installed Chrome or Edge via the DevTools
 * Protocol (no npm, no Puppeteer). Node 21+ (needs global fetch + WebSocket).
 * This is the "rascunho visual" the user attaches to their image generator as a
 * COMPOSITION reference — a clean, flat, LABEL-FREE blocking at the target ratio.
 *
 * Usage:
 *   node rascunho.js <in.html> <out.png> <cssWidth> <cssHeight> [scale=2]
 * Example (16:9 wallpaper sketch at 1280x720 CSS, output 2560x1440):
 *   node rascunho.js rascunho.html rascunho.png 1280 720
 *
 * Exit 0 on success (prints "WROTE <out> WxH"); exit 1 on failure (prints "ERR ...").
 * On failure the caller MUST fall back to the text planta (degraded mode) — never
 * pretend a PNG was produced.
 */
const { spawn } = require('child_process');
const fs = require('fs'), os = require('os'), path = require('path');

// ---- locate a Chromium-based browser (Chrome preferred, Edge fallback) ----
function findBrowser() {
  if (process.env.CHROME && fs.existsSync(process.env.CHROME)) return process.env.CHROME;
  const PF = process.env['ProgramFiles'] || 'C:/Program Files';
  const PF86 = process.env['ProgramFiles(x86)'] || 'C:/Program Files (x86)';
  const LOCAL = process.env['LOCALAPPDATA'] || '';
  const candidates = [
    // Windows
    `${PF}/Google/Chrome/Application/chrome.exe`,
    `${PF86}/Google/Chrome/Application/chrome.exe`,
    `${LOCAL}/Google/Chrome/Application/chrome.exe`,
    `${PF86}/Microsoft/Edge/Application/msedge.exe`,
    `${PF}/Microsoft/Edge/Application/msedge.exe`,
    // macOS
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    // Linux
    '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/microsoft-edge',
  ];
  for (const c of candidates) { try { if (fs.existsSync(c)) return c; } catch (e) {} }
  return null;
}

const BROWSER = findBrowser();
if (!BROWSER) { console.error('ERR no Chrome/Edge found. Set CHROME=/path/to/chrome and retry, or use the text planta.'); process.exit(1); }
if (typeof WebSocket === 'undefined') { console.error('ERR Node 21+ required (global WebSocket missing). Run `node -v`.'); process.exit(1); }

let src = process.argv[2], out = process.argv[3];
if (!src || !out) { console.error('ERR usage: node rascunho.js <in.html> <out.png> <cssWidth> <cssHeight> [scale]'); process.exit(1); }
// encodeURI so spaces in the project path (e.g. "my project") don't break navigation.
if (!/^file:|^https?:/.test(src)) src = 'file:///' + encodeURI(path.resolve(src).replace(/\\/g, '/'));
const width = parseInt(process.argv[4] || '1280', 10);
const height = parseInt(process.argv[5] || '720', 10);
const scale = parseInt(process.argv[6] || '2', 10); // 2x = crisp; references get downsampled anyway
const PORT = 9000 + Math.floor(Math.random() * 900);
const udd = fs.mkdtempSync(path.join(os.tmpdir(), 'rascunho-'));
const sleep = ms => new Promise(r => setTimeout(r, ms));

const browser = spawn(BROWSER, [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${udd}`,
  '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check',
  '--disable-sync', '--disable-extensions', '--mute-audio', '--force-color-profile=srgb',
  '--disable-background-networking', '--disable-features=Translate', 'about:blank'
], { stdio: 'ignore' });

// Watchdog: never hang, never leave a zombie browser.
const WATCHDOG = setTimeout(() => {
  console.error('ERR timeout rendering the sketch. Fall back to the text planta.');
  try { browser.kill(); } catch (e) {}
  try { fs.rmSync(udd, { recursive: true, force: true }); } catch (e) {}
  process.exit(1);
}, 30000);
function done(code) { clearTimeout(WATCHDOG); try { browser.kill(); } catch (e) {}
  try { fs.rmSync(udd, { recursive: true, force: true }); } catch (e) {} process.exit(code); }

async function pageWS() {
  for (let i = 0; i < 100; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}/json/list`); const l = await r.json();
      const p = l.find(t => t.type === 'page' && t.webSocketDebuggerUrl); if (p) return p.webSocketDebuggerUrl;
    } catch (e) {}
    await sleep(150);
  }
  throw new Error('browser CDP not ready');
}
function rpc(ws) {
  let id = 0; const pend = new Map();
  ws.addEventListener('message', e => { const m = JSON.parse(e.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } });
  const send = (method, params = {}) => new Promise((res, rej) => { const _id = ++id;
    pend.set(_id, m => m.error ? rej(new Error(method + ' ' + JSON.stringify(m.error))) : res(m.result));
    ws.send(JSON.stringify({ id: _id, method, params })); });
  return { send };
}
(async () => {
  const ws = new WebSocket(await pageWS());
  await new Promise((r, j) => { ws.addEventListener('open', r, { once: true }); ws.addEventListener('error', j, { once: true }); });
  const { send } = rpc(ws);
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false, screenWidth: width, screenHeight: height });
  let loaded = false; ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (m.method === 'Page.loadEventFired') loaded = true; });
  await send('Page.navigate', { url: src });
  for (let i = 0; i < 80 && !loaded; i++) await sleep(100);
  // settle: fonts + a paint tick (SVG paints synchronously, but be safe)
  await send('Runtime.evaluate', { awaitPromise: true, expression: `(async()=>{ try{await document.fonts.ready;}catch(e){} await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))); return 1; })()` });
  await sleep(150);
  const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: 0, y: 0, width, height, scale } });
  fs.writeFileSync(out, Buffer.from(shot.data, 'base64'));
  console.log('WROTE ' + out + ' ' + (width * scale) + 'x' + (height * scale));
  ws.close(); done(0);
})().catch(e => { console.error('ERR ' + e.message + ' — fall back to the text planta.'); done(1); });
