#!/usr/bin/env node
/**
 * render.js — zero-dependency full-page screenshot of a local HTML file.
 *
 * Drives an already-installed Chrome or Edge via the DevTools Protocol (no npm,
 * no Puppeteer). Node 18+ (uses global fetch); Node 21+ for global WebSocket.
 * Lets the skill SEE what it built and fix it before delivering.
 *
 * Usage:
 *   node render.js <fileUrlOrPath> <out.png> [width=1440] [mobile=0] [clipY] [clipH]
 * Examples:
 *   node render.js site-cliente/index.html shot-full.png 1440        # full desktop page
 *   node render.js site-cliente/index.html shot-mobile.png 390 1     # full mobile page
 *   node render.js site-cliente/index.html shot-hero.png 1440 0 0 900 # crop a region
 *
 * Exit 0 on success (prints "WROTE <out> WxH"); exit 1 on failure (prints "ERR ...").
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
if (!BROWSER) { console.error('ERR no Chrome/Edge found. Set CHROME=/path/to/chrome and retry.'); process.exit(1); }
if (typeof WebSocket === 'undefined') { console.error('ERR Node 21+ required (global WebSocket missing). Run `node -v`.'); process.exit(1); }

let url = process.argv[2], out = process.argv[3];
if (!url || !out) { console.error('ERR usage: node render.js <fileUrlOrPath> <out.png> [width] [mobile] [clipY] [clipH]'); process.exit(1); }
if (!/^file:|^https?:/.test(url)) url = 'file:///' + path.resolve(url).replace(/\\/g, '/');
const width = parseInt(process.argv[4] || '1440', 10);
const mobile = process.argv[5] === '1';
const CLIPY = process.argv[6] !== undefined ? parseInt(process.argv[6], 10) : null;
const CLIPH = process.argv[7] !== undefined ? parseInt(process.argv[7], 10) : null;
const PORT = 9000 + Math.floor(Math.random() * 900);
const udd = fs.mkdtempSync(path.join(os.tmpdir(), 'render-'));
const sleep = ms => new Promise(r => setTimeout(r, ms));

const browser = spawn(BROWSER, [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${udd}`,
  '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check',
  '--disable-sync', '--disable-extensions', '--mute-audio', '--force-color-profile=srgb',
  '--disable-background-networking', '--disable-features=Translate', 'about:blank'
], { stdio: 'ignore' });

// Watchdog: never hang and never leave a zombie browser. Capturing a VERY long full page
// can stall; if so, kill everything and tell the caller to use region crops (clipY clipH).
const WATCHDOG = setTimeout(() => {
  console.error('ERR timeout — page likely too long to capture whole. Re-run with region crops: '
    + 'node render.js <site>/index.html out.png 1440 0 <clipY> <clipH>  (e.g. 0 1600 for the hero band).');
  try { browser.kill(); } catch (e) {}
  try { fs.rmSync(udd, { recursive: true, force: true }); } catch (e) {}
  process.exit(1);
}, 55000);
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
  let id = 0; const pend = new Map(), evt = [];
  ws.addEventListener('message', e => { const m = JSON.parse(e.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } else evt.push(m); });
  const send = (method, params = {}) => new Promise((res, rej) => { const _id = ++id;
    pend.set(_id, m => m.error ? rej(new Error(method + ' ' + JSON.stringify(m.error))) : res(m.result));
    ws.send(JSON.stringify({ id: _id, method, params })); });
  return { send, evt };
}
(async () => {
  const ws = new WebSocket(await pageWS());
  await new Promise((r, j) => { ws.addEventListener('open', r, { once: true }); ws.addEventListener('error', j, { once: true }); });
  const { send, evt } = rpc(ws);
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width, height: mobile ? 844 : 900, deviceScaleFactor: 1, mobile, screenWidth: width, screenHeight: mobile ? 844 : 900 });
  let loaded = false; evt.push(m => { if (m.method === 'Page.loadEventFired') loaded = true; });
  await send('Page.navigate', { url });
  for (let i = 0; i < 80 && !loaded; i++) await sleep(100);
  // settle: fonts ready, reveal-classes shown, every image downloaded AND decoded (so async images paint)
  await send('Runtime.evaluate', { awaitPromise: true, expression: `(async()=>{
    try{await document.fonts.ready;}catch(e){}
    const s=document.createElement('style');
    s.textContent='html{scroll-behavior:auto!important}.reveal,[data-reveal]{opacity:1!important;transform:none!important}';
    document.head.appendChild(s);
    document.querySelectorAll('.reveal,[data-reveal]').forEach(e=>e.classList.add('is-visible'));
    document.querySelectorAll('img').forEach(i=>{i.loading='eager';i.decoding='sync';});
    window.scrollTo(0,document.body.scrollHeight); await new Promise(r=>setTimeout(r,400)); window.scrollTo(0,0);
    await Promise.race([
      Promise.all([...document.images].map(i=> i.complete&&i.naturalWidth>0?0:new Promise(r=>{i.addEventListener('load',r,{once:true});i.addEventListener('error',r,{once:true});}))),
      new Promise(r=>setTimeout(r,15000))
    ]);
    await Promise.all([...document.images].map(i=> i.naturalWidth>0 ? i.decode().catch(()=>{}) : 0));
    return 1; })()` });
  await sleep(400);
  const lm = await send('Page.getLayoutMetrics');
  const cs = lm.cssContentSize || lm.contentSize;
  const clipY = CLIPY !== null ? CLIPY : 0;
  // Capturing a giant page in one shot can stall — cap height and hint to use crops past the cap.
  const CAP = 6000;
  const full = Math.ceil(cs.height);
  const clipH = CLIPH !== null ? CLIPH : Math.min(full, CAP);
  if (CLIPH === null && full > CAP)
    console.error('NOTE page is ' + full + 'px tall; captured top ' + CAP + 'px. Use crops (clipY clipH) for lower sections.');
  const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: 0, y: clipY, width: Math.ceil(cs.width), height: clipH, scale: 1 } });
  fs.writeFileSync(out, Buffer.from(shot.data, 'base64'));
  console.log('WROTE ' + out + ' ' + Math.ceil(cs.width) + 'x' + clipH);
  ws.close(); done(0);
})().catch(e => { console.error('ERR ' + e.message); done(1); });
