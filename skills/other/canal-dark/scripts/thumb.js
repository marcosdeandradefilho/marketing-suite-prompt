#!/usr/bin/env node
/**
 * thumb.js — render an HTML thumbnail to a PNG (1280x720 CSS -> 2560x1440 at scale 2).
 *
 * Zero-dependency: drives an already-installed Chrome or Edge via the DevTools Protocol
 * (no npm, no Puppeteer). Node 21+ (needs global fetch + WebSocket). Deterministic, no
 * image generator, no API key.
 *
 * Uso:
 *   node thumb.js <in.html> <out.png> [cssW=1280] [cssH=720] [scale=2]
 *   node thumb.js --multi <in1.html> <out1.png> <in2.html> <out2.png> ...
 *
 * MULTI: renderiza varias thumbs num UNICO navegador (um cold-start, nao N). E assim que a
 * skill gera as 3 variantes — no Windows, com o Chrome do usuario cheio de abas, abrir 3
 * navegadores headless em sequencia estoura o watchdog; abrir 1 e capturar 3 vezes nao.
 *
 * Exit 0 on success ("WROTE <out> WxH" por thumb); exit 1 on failure ("ERR ...") — caller must
 * fall back to telling the user to make the thumb by hand, never pretend a PNG exists.
 */
const { spawn } = require('child_process');
const fs = require('fs'), os = require('os'), path = require('path');

function findBrowser() {
  if (process.env.CHROME && fs.existsSync(process.env.CHROME)) return process.env.CHROME;
  const PF = process.env['ProgramFiles'] || 'C:/Program Files';
  const PF86 = process.env['ProgramFiles(x86)'] || 'C:/Program Files (x86)';
  const LOCAL = process.env['LOCALAPPDATA'] || '';
  const candidates = [
    `${PF}/Google/Chrome/Application/chrome.exe`,
    `${PF86}/Google/Chrome/Application/chrome.exe`,
    `${LOCAL}/Google/Chrome/Application/chrome.exe`,
    `${PF86}/Microsoft/Edge/Application/msedge.exe`,
    `${PF}/Microsoft/Edge/Application/msedge.exe`,
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/microsoft-edge',
  ];
  for (const c of candidates) { try { if (fs.existsSync(c)) return c; } catch (e) {} }
  return null;
}

const BROWSER = findBrowser();
if (!BROWSER) { console.error('ERR nenhum Chrome/Edge encontrado. Faca a thumb na mao ou instale o Edge.'); process.exit(1); }
if (typeof WebSocket === 'undefined') { console.error('ERR Node 21+ necessario (WebSocket global ausente).'); process.exit(1); }

// --- parse de argumentos: single (retrocompat) ou --multi ---------------------
const argv = process.argv.slice(2);
let pairs = [];
let width = 1280, height = 720, scale = 2;
if (argv[0] === '--multi') {
  const rest = argv.slice(1);
  for (let i = 0; i + 1 < rest.length; i += 2) pairs.push({ src: rest[i], out: rest[i + 1] });
} else {
  const src = argv[0], out = argv[1];
  if (!src || !out) {
    console.error('ERR uso: node thumb.js <in.html> <out.png> [cssW] [cssH] [scale]  |  node thumb.js --multi <in1> <out1> <in2> <out2> ...');
    process.exit(1);
  }
  width = parseInt(argv[2] || '1280', 10);
  height = parseInt(argv[3] || '720', 10);
  scale = parseInt(argv[4] || '2', 10);
  pairs.push({ src, out });
}
if (!pairs.length) { console.error('ERR nenhum par entrada/saida valido.'); process.exit(1); }
for (const p of pairs) {
  if (!/^file:|^https?:/.test(p.src)) p.src = 'file:///' + encodeURI(path.resolve(p.src).replace(/\\/g, '/'));
}

const PORT = 9000 + Math.floor(Math.random() * 900);
const udd = fs.mkdtempSync(path.join(os.tmpdir(), 'thumb-'));
const sleep = ms => new Promise(r => setTimeout(r, ms));

const browser = spawn(BROWSER, [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${udd}`,
  '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check',
  '--disable-sync', '--disable-extensions', '--mute-audio', '--force-color-profile=srgb',
  '--disable-background-networking', '--disable-features=Translate', 'about:blank'
], { stdio: 'ignore' });

// watchdog do processo inteiro: cresce com o nº de thumbs (cold-start unico + N capturas).
const WATCHDOG = setTimeout(() => {
  console.error('ERR timeout renderizando a thumb. Faca na mao.');
  try { browser.kill(); } catch (e) {}
  try { fs.rmSync(udd, { recursive: true, force: true }); } catch (e) {}
  process.exit(1);
}, 45000 + 25000 * pairs.length);  // no Windows o cold-start do Chrome (com Defender/abas) e lento.
function done(code) { clearTimeout(WATCHDOG); try { browser.kill(); } catch (e) {}
  try { fs.rmSync(udd, { recursive: true, force: true }); } catch (e) {} process.exit(code); }

async function pageWS() {
  for (let i = 0; i < 200; i++) {  // ate ~30s esperando a porta de debug subir (cold-start lento no Windows)
    try { const r = await fetch(`http://127.0.0.1:${PORT}/json/list`); const l = await r.json();
      const p = l.find(t => t.type === 'page' && t.webSocketDebuggerUrl); if (p) return p.webSocketDebuggerUrl;
    } catch (e) {}
    await sleep(150);
  }
  throw new Error('CDP do browser nao respondeu');
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
  let loaded = false;
  ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (m.method === 'Page.loadEventFired') loaded = true; });
  for (const p of pairs) {
    loaded = false;
    await send('Page.navigate', { url: p.src });
    for (let i = 0; i < 120 && !loaded; i++) await sleep(100);  // ate 12s por thumb esperando o load
    await send('Runtime.evaluate', { awaitPromise: true, expression: `(async()=>{ try{await document.fonts.ready;}catch(e){} await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))); return 1; })()` });
    await sleep(150);
    // captureBeyondViewport:false — o thumb cabe inteiro no viewport (1280x720, overflow hidden);
    // o modo "beyond" forcava o Chrome a compor a pagina toda e, com imagem grande + RAM sob pressao,
    // travava o screenshot. Com clip explicito + beyond:false, so o viewport e rasterizado.
    const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false,
      clip: { x: 0, y: 0, width, height, scale } });
    fs.writeFileSync(p.out, Buffer.from(shot.data, 'base64'));
    console.log('WROTE ' + p.out + ' ' + (width * scale) + 'x' + (height * scale));
  }
  ws.close(); done(0);
})().catch(e => { console.error('ERR ' + e.message + ' — faca a thumb na mao.'); done(1); });
