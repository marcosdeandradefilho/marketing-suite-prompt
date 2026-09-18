# card-visual.md — faithful tweet card + zero-config PNG render (read after approval)

The card must look like a REAL tweet screenshot — that credibility is what makes the format work. The
exact command below produces a 1080x1350 PNG. (Sources: Chrome headless docs, Twitter Dim palette.)

## Generic-default to FORBID (output-generator guardrail)
Never ship the Canva-default look: no purple/teal gradient background, no rounded-everything, no
drop-shadow glow, no centered emoji, no Inter-everywhere. The card is a FLAT, opaque tweet surface
with X's real colors and a system font. Restraint reads as authentic; decoration reads as fake.

## Color tokens (use exactly)
**Light / branco (THE DEFAULT — it's what viralizes in BR feeds; it's the classic "tweet print" look):**
- bg `#FFFFFF` · border `#EFF3F4` · text primary `#0F1419` · text secondary (@handle, timestamp, counts) `#536471`
- accent / verified badge `#1D9BF0` · like `#F91880` · retweet `#00BA7C`

> Default to WHITE unless the user asks for dark. (Creator's market call: brancos performam mais no BR.)

**Dark "Dim" (option — only if the user asks for escuro):**
- bg `#15202B` (puxa pro azul-escuro; true-black `#000000` é mais neutro) · border/divider `#38444D`
- text primary `#E7E9EA` · text secondary `#71767B` · accent `#1D9BF0`

Paint the bg on a wrapper `<div>`, NEVER on `<body>` (a body bg can render white in headless). The
slide is always opaque — don't rely on `--default-background-color=0` transparency (unreliable in CLI).

## Typography (honest fallback)
X uses "Chirp" (proprietary, not distributable). Use the system stack — on Windows it resolves to
Segoe UI, a close honest approximation (never claim it's the exact font):
`font-family: 'Chirp', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;`
At the 1080-wide slide scale, scale text UP so it reads at Instagram size: body **32-44px**, display
name **30-34px** weight 700, @handle/timestamp **26-28px** weight 400 grey. Line-height ~1.35 on body.

## Verified badge SVG (inline, zero-config) — OFF by default (see SKILL.md rule 4)
```html
<svg viewBox="0 0 24 24" width="34" height="34" aria-label="Verificado" style="vertical-align:-6px;margin-left:8px">
  <path fill="#1D9BF0" d="M22.25 12c0-1.43-.88-2.67-2.19-3.34.46-1.39.2-2.9-.81-3.91s-2.52-1.27-3.91-.81c-.66-1.31-1.91-2.19-3.34-2.19s-2.67.88-3.33 2.19c-1.4-.46-2.91-.2-3.92.81s-1.26 2.52-.8 3.91c-1.31.67-2.2 1.91-2.2 3.34s.89 2.67 2.2 3.34c-.46 1.39-.21 2.9.8 3.91s2.52 1.26 3.91.81c.67 1.31 1.91 2.19 3.34 2.19s2.68-.88 3.34-2.19c1.39.46 2.9.2 3.91-.81s1.27-2.52.81-3.91c1.31-.67 2.19-1.91 2.19-3.34zm-11.71 4.2L6.8 12.46l1.41-1.42 2.26 2.26 4.8-5.23 1.47 1.36-6.2 6.77z"/>
</svg>
```

## Avatar
Circle, ~120px at 1080 scale. Photo: `<img>` with `width:120px;height:120px;border-radius:50%;object-fit:cover;`
(width==height + object-fit or it distorts). Prefer a **base64 data URI** for a self-contained slide
(`src="data:image/jpeg;base64,…"`), or a `file:///C:/.../foto.jpg` path. No photo → initials circle:
```html
<div style="width:120px;height:120px;border-radius:50%;background:#1D9BF0;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:48px">IA</div>
```
To base64 a photo on Windows (zero-config, no install):
`powershell -Command "[Convert]::ToBase64String([IO.File]::ReadAllBytes('C:\caminho\foto.jpg'))"`

## Slide HTML skeleton (one file per slide, sized exactly to the window)
```html
<!doctype html><html><head><meta charset="utf-8"><style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1080px;height:1350px}
  .slide{width:1080px;height:1350px;background:#FFFFFF;display:flex;align-items:center;justify-content:center;
         font-family:'Chirp',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
  .card{width:920px;padding:56px 60px;color:#0F1419}                /* WHITE is the default; for dark swap to bg #15202B / color #E7E9EA */
  .head{display:flex;align-items:center;gap:20px;margin-bottom:28px}
  .avatar{width:120px;height:120px;border-radius:50%;object-fit:cover;flex:0 0 auto}
  .name{font-size:32px;font-weight:700;line-height:1.1;display:flex;align-items:center}
  .handle{font-size:28px;color:#536471;margin-top:6px}             /* dark: #71767B */
  .body{font-size:44px;line-height:1.38;font-weight:400;white-space:pre-wrap}
  .meta{font-size:26px;color:#536471;margin-top:34px}              /* dark: #71767B */
</style></head><body>
  <div class="slide"><div class="card">
    <div class="head">
      <img class="avatar" src="data:image/jpeg;base64,…">      <!-- or initials div -->
      <div>
        <div class="name">Nome <!-- selo SVG aqui SÓ se aprovado --></div>
        <div class="handle">@usuario</div>
      </div>
    </div>
    <div class="body">TEXTO DO TWEET (este slide)</div>
    <div class="meta">14:32 · 9 de jun de 2026</div>           <!-- optional -->
  </div></div>
</body></html>
```
**The card is JUST the tweet** — avatar + name + @handle + body (+ optional timestamp). Do NOT render a
secondary "subtitle" / grey caption / "continua →" line under the tweet: real viral tweet-carousels (Bruno
Perini, Tedson Santos etc.) don't use one — it screams "post de template". The pull to the next slide comes
from the NARRATIVE, and if you want an explicit hook it goes INSIDE the tweet text as its own last line, never
as a separate styled element. Keep the card vertically centered with comfortable margins; the body text is the
largest element. Engagement row (reply/RT/like/views) is OPTIONAL — a cleaner card without it usually reads
better; omit rather than fake exact icon counts.

## Render to PNG 1080x1350 (verified Windows command)
1. **Find the binary first** (don't assume PATH): try `where msedge`, then `where chrome`, then the
   common paths `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` and
   `C:\Program Files\Google\Chrome\Application\chrome.exe`.
2. **One HTML per slide**, then screenshot each (the `--screenshot` flag captures the VIEWPORT, not a
   tall page — a single long HTML would clip). Command:
```
msedge --headless=old --disable-gpu --hide-scrollbars --force-device-scale-factor=1 ^
  --screenshot="C:\full\path\slide-01.png" --window-size=1080,1350 ^
  --user-data-dir=%TEMP%\edge-shot "file:///C:/full/path/slide-01.html"
```
3. **CRITICAL — spaces in the path silently break the render.** If the project/Desktop path has a
   space (e.g. `C:\Users\João\Desktop\meu projeto\…`), Edge headless throws *"Multiple targets are not
   supported"* and writes NO PNG (very common on BR machines — usernames and folders with spaces). The
   robust fix: build + render in a **spaceless temp working dir**, then copy the PNGs back to the final
   folder. The PowerShell loop below does exactly that and is the recommended path on Windows:
```powershell
$edge = (Get-Command msedge -ErrorAction SilentlyContinue).Source
if(-not $edge){ $edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" }
$work = Join-Path $env:TEMP ("carrossel-" + [guid]::NewGuid().ToString("N").Substring(0,8))  # spaceless
New-Item -ItemType Directory -Force $work | Out-Null
foreach($f in Get-ChildItem "$dir\slide-*.html" | Sort-Object Name){
  Copy-Item $f.FullName (Join-Path $work $f.Name)
  $src = Join-Path $work $f.Name
  $png = Join-Path $work ($f.BaseName + ".png")
  & $edge --headless=old --disable-gpu --hide-scrollbars --force-device-scale-factor=1 `
    "--screenshot=$png" --window-size=1080,1350 "--user-data-dir=$work\udd" `
    ("file:///" + ($src -replace '\\','/'))
  Copy-Item $png (Join-Path $dir ($f.BaseName + ".png"))   # back to the real (spaced) folder
}
Remove-Item $work -Recurse -Force
```
For crisper text: `--force-device-scale-factor=2` with `--window-size=540,675` → a 1080x1350 @2x PNG.

## Windows gotchas (all real, verified)
- **Spaces in the path** → *"Multiple targets are not supported"* and no PNG written. Render from a
  spaceless temp dir and copy the PNGs back (see step 3 above). This is the most common silent failure.
- Prefer **`--headless=old`** — `--headless=new` can ignore `--window-size` (if it exceeds desktop
  resolution) and can refuse to write the file when a browser window is already open.
- Always pass a throwaway **`--user-data-dir=%TEMP%\edge-shot`** — colliding with the running profile
  is the #1 "nothing happens" cause on Windows.
- `--hide-scrollbars` stops a scrollbar gutter from eating edge pixels / shifting the card.
- Add `--timeout=5000` if a photo/font is still settling so the capture isn't mid-load.
- Mac/Linux: same flags, binary is `"Microsoft Edge"`/`google-chrome`/`chromium`; paths differ.

## Quality pass (LOOK at the PNG — don't trust the code)
After rendering slide 1, **Read the PNG visually** and check: text not clipped at edges, avatar is a
clean circle, accents/PT-BR characters render, the body is legible at small size, the card reads as a
real tweet (not a Canva post). Regenerate on fail (cap a couple tries; keep the best). If you can't
render, say it wasn't eye-checked.

## Degraded mode (no Edge/Chrome found)
Ship the `.html` slides + `copy.md`. Tell the user (PT-BR) to open each HTML and capture it: DevTools →
right-click the `.card` node → **"Capturar captura de tela do nó"** for exact bounds, or **Win+Shift+S**
(Recorte) and crop. Never fabricate the PNG. Label: "render automático indisponível — gere o print manual".
