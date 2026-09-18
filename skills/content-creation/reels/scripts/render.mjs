#!/usr/bin/env node
/*
 * render.mjs — Remotion render orchestrator for the reels skill.
 *
 * Why a script: the render path is deterministic and repeated every run. The skill only
 * generates the SCENE PLAN (props.json); this script does the rest the same way every time.
 *
 * It handles the verified Windows landmines:
 *  - spaces in the project path break Chromium ("Multiple targets are not supported")
 *      -> scaffold + render in a NO-SPACES temp dir, copy the MP4 back.
 *  - --props inline JSON breaks on Windows shell -> always a relative ./props.json FILE.
 *  - 150-300MB Chrome Headless Shell download dodged via --browser-executable <Edge/Chrome>.
 *
 * Usage:
 *   node render.mjs --props "<plan.json>" --out "<final.mp4>" [--assets "<assets/remotion dir>"]
 * Exit 0 on success (prints OUT=<path>), non-zero on failure so the skill can fall back to ffmpeg.
 */
import {execFileSync} from 'node:child_process';
import {existsSync, mkdirSync, cpSync, copyFileSync, rmSync, readFileSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const getArg = (k) => {
  const i = args.indexOf(k);
  return i >= 0 ? args[i + 1] : undefined;
};
const propsPath = getArg('--props');
const outPath = getArg('--out');
const assetsDir = getArg('--assets') || path.resolve(__dirname, '..', 'assets');

if (!propsPath || !outPath) {
  console.error('uso: node render.mjs --props <plan.json> --out <final.mp4>');
  process.exit(2);
}

const log = (m) => console.log(`[reels] ${m}`);

// --- 1. pick a NO-SPACES working dir ---
const base = tmpdir();
const safeBase = base.includes(' ') ? (process.platform === 'win32' ? 'C:\\reel-tmp' : '/tmp') : base;
const work = path.join(safeBase, `reel-${Date.now()}`);
mkdirSync(work, {recursive: true});

// --- 2. probe a system browser to skip the headless-shell download ---
const browserCandidates =
  process.platform === 'win32'
    ? [
        'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
        'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
      ]
    : process.platform === 'darwin'
    ? [
        '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium',
      ]
    : ['/usr/bin/microsoft-edge', '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'];
const browser = browserCandidates.find((p) => existsSync(p));

try {
  // --- 3. stage the engine + font + plan in the safe dir ---
  log(`preparando em ${work}`);
  cpSync(path.join(assetsDir, 'remotion'), work, {recursive: true});
  const pub = path.join(work, 'public');
  mkdirSync(pub, {recursive: true});
  copyFileSync(path.join(assetsDir, 'fonts', 'Anton-Regular.ttf'), path.join(pub, 'Anton-Regular.ttf'));
  copyFileSync(propsPath, path.join(work, 'props.json'));

  // sanity: plan must parse and have scenes
  const plan = JSON.parse(readFileSync(path.join(work, 'props.json'), 'utf8'));
  if (!plan.scenes || !plan.scenes.length) throw new Error('props.json sem cenas');

  // --- 3b. optional background audio: copy into public/, probe duration with ffprobe ---
  if (plan.audio) {
    const audioAbs = path.isAbsolute(plan.audio) ? plan.audio : path.resolve(path.dirname(propsPath), plan.audio);
    if (existsSync(audioAbs)) {
      const ext = path.extname(audioAbs) || '.mp3';
      copyFileSync(audioAbs, path.join(pub, `voz${ext}`));
      plan.audioSrc = `voz${ext}`;
      try {
        const out = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audioAbs], {encoding: 'utf8'}).trim();
        const secs = parseFloat(out);
        if (secs > 0) plan.audioDurationInFrames = Math.ceil(secs * 30);
        log(`áudio de fundo: ${secs.toFixed(1)}s — o vídeo vai durar isso.`);
      } catch {
        log('não consegui medir a duração do áudio (ffprobe); usando a duração das cenas.');
      }
      delete plan.audio;
      writeFileSync(path.join(work, 'props.json'), JSON.stringify(plan));
    } else {
      log(`áudio não encontrado em ${audioAbs}; seguindo sem som.`);
    }
  }

  // On Windows + Node 20+, spawning .cmd requires shell:true; under a shell, quote any
  // arg that may contain spaces (the Edge path lives in "Program Files").
  const win = process.platform === 'win32';
  const q = (s) => (win && s.includes(' ') ? `"${s}"` : s);

  // --- 4. install (first run only; pinned + exact) ---
  log('instalando ferramentas de vídeo (só na primeira vez, pode levar 1-2 min)...');
  execFileSync(win ? 'npm.cmd' : 'npm', ['install', '--no-audit', '--no-fund', '--silent'], {
    cwd: work,
    stdio: 'inherit',
    shell: win,
  });

  // --- 5. render ---
  log('renderizando o vídeo...');
  const renderArgs = ['remotion', 'render', 'src/index.ts', 'reel', 'out/reel.mp4', '--props=./props.json'];
  if (browser) {
    renderArgs.push(`--browser-executable=${q(browser)}`);
    log(`usando navegador do sistema: ${path.basename(browser)}`);
  } else {
    log('navegador do sistema não encontrado; o Remotion vai baixar o dele (uma vez).');
  }
  execFileSync(win ? 'npx.cmd' : 'npx', renderArgs, {cwd: work, stdio: 'inherit', shell: win});

  // --- 6. copy the MP4 back to the real (spaces-ok) output path ---
  mkdirSync(path.dirname(outPath), {recursive: true});
  copyFileSync(path.join(work, 'out', 'reel.mp4'), outPath);
  log(`pronto: ${outPath}`);
  console.log(`OUT=${outPath}`);
} catch (err) {
  console.error(`[reels] falhou no Remotion: ${err.message}`);
  process.exit(1);
} finally {
  try {
    rmSync(work, {recursive: true, force: true});
  } catch {}
}
