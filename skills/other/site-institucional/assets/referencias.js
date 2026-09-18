#!/usr/bin/env node
/**
 * referencias.js — screenshot SEVERAL live reference websites in one browser launch,
 * so the skill can actually SEE current, real designs and design from them (Vision).
 * Zero-dependency: drives installed Chrome/Edge via DevTools Protocol. Node 21+.
 *
 * Usage:
 *   node referencias.js <outDir> <bandHeight> <url1> <url2> ...
 * Example:
 *   node referencias.js ./_refs 1600 https://noma.dk/ https://www.ateliercrenn.com/ ...
 *
 * Writes <outDir>/ref-1.png, ref-2.png, ... and prints one status line per URL:
 *   "ref-1.png  OK      textlen=2143  https://..."   ← worth reading (real design)
 *   "ref-3.png  BLOCKED textlen=42    https://..."   ← bot-wall / SPA loader — SKIP it
 * Read the OK ones with Vision; skip BLANK/BLOCKED. Aim to pass enough URLs to net >=5 OK.
 */
const { spawn } = require('child_process');
const fs = require('fs'), os = require('os'), path = require('path');

function findBrowser() {
  if (process.env.CHROME && fs.existsSync(process.env.CHROME)) return process.env.CHROME;
  const PF = process.env['ProgramFiles'] || 'C:/Program Files';
  const PF86 = process.env['ProgramFiles(x86)'] || 'C:/Program Files (x86)';
  const LOCAL = process.env['LOCALAPPDATA'] || '';
  const c = [
    `${PF}/Google/Chrome/Application/chrome.exe`, `${PF86}/Google/Chrome/Application/chrome.exe`,
    `${LOCAL}/Google/Chrome/Application/chrome.exe`, `${PF86}/Microsoft/Edge/Application/msedge.exe`,
    `${PF}/Microsoft/Edge/Application/msedge.exe`,
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser',
  ];
  for (const p of c) { try { if (fs.existsSync(p)) return p; } catch (e) {} }
  return null;
}
const BROWSER = findBrowser();
if (!BROWSER) { console.error('ERR no Chrome/Edge found. Set CHROME=/path and retry.'); process.exit(1); }
if (typeof WebSocket === 'undefined') { console.error('ERR Node 21+ required (global WebSocket).'); process.exit(1); }

const outDir = process.argv[2];
const band = parseInt(process.argv[3] || '1600', 10);
const urls = process.argv.slice(4);
if (!outDir || !urls.length) { console.error('ERR usage: node referencias.js <outDir> <bandHeight> <url1> <url2> ...'); process.exit(1); }
fs.mkdirSync(outDir, { recursive: true });

const PORT = 9000 + Math.floor(Math.random() * 900);
const udd = fs.mkdtempSync(path.join(os.tmpdir(), 'refs-'));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const browser = spawn(BROWSER, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${udd}`,
  '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', '--disable-sync',
  '--disable-extensions', '--mute-audio', '--force-color-profile=srgb', '--disable-features=Translate',
  '--window-size=1440,900', 'about:blank'], { stdio: 'ignore' });

const WATCHDOG = setTimeout(() => { console.error('ERR overall timeout'); cleanup(1); }, 25000 + urls.length * 26000);
function cleanup(code) { clearTimeout(WATCHDOG); try { browser.kill(); } catch (e) {} try { fs.rmSync(udd, { recursive: true, force: true }); } catch (e) {} process.exit(code); }

async function pageWS() {
  for (let i = 0; i < 100; i++) { try { const r = await fetch(`http://127.0.0.1:${PORT}/json/list`); const l = await r.json();
    const p = l.find(t => t.type === 'page' && t.webSocketDebuggerUrl); if (p) return p.webSocketDebuggerUrl; } catch (e) {} await sleep(150); }
  throw new Error('CDP not ready');
}
function rpc(ws) { let id = 0; const pend = new Map(), evt = [];
  ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } else evt.push(m); });
  const send = (method, params = {}) => new Promise((res, rej) => { const _id = ++id; pend.set(_id, m => m.error ? rej(new Error(method + ' ' + JSON.stringify(m.error))) : res(m.result)); ws.send(JSON.stringify({ id: _id, method, params })); });
  return { send, evt };
}

const BOT = /(checking your browser|just a moment|verificando|aguarde enquanto|enable javascript|please enable js|are you a robot|cf-browser-verification|attention required|you have been blocked|access denied|unable to access|cloudflare ray id|security service to protect|ddos protection|captcha)/i;

(async () => {
  const ws = new WebSocket(await pageWS());
  await new Promise((r, j) => { ws.addEventListener('open', r, { once: true }); ws.addEventListener('error', j, { once: true }); });
  const { send, evt } = rpc(ws);
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });

  let n = 0, ok = 0;
  for (const url of urls) {
    n++; const out = path.join(outDir, 'ref-' + n + '.png');
    let status = 'OK', textlen = 0;
    try {
      let loaded = false; const onLoad = m => { if (m.method === 'Page.loadEventFired') loaded = true; };
      evt.length = 0; evt.push(onLoad);
      await send('Page.navigate', { url });
      for (let i = 0; i < 80 && !loaded; i++) await sleep(100);  // up to 8s for load
      // settle: fonts, images, reveals, dismiss obvious overlays; report body text length
      const r = await send('Runtime.evaluate', { awaitPromise: true, returnByValue: true, expression: `(async()=>{
        try{await document.fonts.ready;}catch(e){}
        const s=document.createElement('style'); s.textContent='html{scroll-behavior:auto!important}.reveal,[data-reveal]{opacity:1!important;transform:none!important}'; document.head.appendChild(s);
        document.querySelectorAll('.reveal,[data-reveal]').forEach(e=>e.classList.add('is-visible'));
        document.querySelectorAll('img').forEach(i=>{i.loading='eager';i.decoding='sync';});
        window.scrollTo(0,600); await new Promise(r=>setTimeout(r,250)); window.scrollTo(0,0);
        await Promise.race([Promise.all([...document.images].slice(0,24).map(i=> i.complete&&i.naturalWidth>0?0:new Promise(r=>{i.addEventListener('load',r,{once:true});i.addEventListener('error',r,{once:true});}))), new Promise(r=>setTimeout(r,5000))]);
        await Promise.all([...document.images].slice(0,24).map(i=> i.naturalWidth>0 ? i.decode().catch(()=>{}) : 0));
        return (document.body&&document.body.innerText||'').slice(0,5000); })()` });
      const txt = r.result.value || ''; textlen = txt.length;
      if (BOT.test(txt)) status = 'BLOCKED';
      else if (textlen < 60) status = 'BLANK';
      await sleep(300);
      const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: 1440, height: band, scale: 1 } });
      fs.writeFileSync(out, Buffer.from(shot.data, 'base64'));
      if (status === 'OK') ok++;
    } catch (e) { status = 'ERR'; }
    console.log('ref-' + n + '.png\t' + status + '\ttextlen=' + textlen + '\t' + url);
  }
  console.log('# ' + ok + '/' + n + ' usable (OK)');
  ws.close(); cleanup(0);
})().catch(e => { console.error('ERR ' + e.message); cleanup(1); });
