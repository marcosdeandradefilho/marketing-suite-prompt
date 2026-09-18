# render-pdf.md — HTML → PDF com zero config (verificado em máquina real)

> The zero-config path: render a self-contained HTML via the **headless browser already on the
> machine** (Edge on Windows, Chrome/Edge on Mac/Linux). No pip, no npm, no API key. Python
> stdlib has NO PDF generator and reportlab/weasyprint need installs — so we DON'T use Python.
> Verified 2026-06 on Windows 11: Edge `--headless=new --print-to-pdf` produced a valid `%PDF-`
> with forced background colors.

## 1. Write the self-contained HTML first
The proposal is ONE `.html` file with **everything inline**: CSS in a `<style>` tag, the logo and
any image as **base64 data URIs**, fonts via system stacks (no web fonts). This matters because:
- **Headless gotcha (confirmed):** headless Chrome/Edge SILENTLY refuses to fetch external
  resources referenced from CSS (`url(file://...)` images come out invisible). **base64 data URIs
  DO work.** So embed images as `<img src="data:image/png;base64,....">` or CSS `url(data:...)`.
- A fully self-contained HTML also means the **Ctrl+P fallback looks identical** and the file is
  portable (you can send the HTML itself if needed).

Keep base64 images reasonably small (a logo, not a hero photo) — base64 inflates ~33%.

### Embedding the logo as base64
If the brand kit / user gives a logo file path, convert it inline. Example (Node, no deps):
```bash
node -e "const fs=require('fs'),p=process.argv[1];const b=fs.readFileSync(p).toString('base64');const ext=(p.split('.').pop()||'png').toLowerCase();const mime=ext==='svg'?'image/svg+xml':ext==='jpg'||ext==='jpeg'?'image/jpeg':'image/'+ext;process.stdout.write('data:'+mime+';base64,'+b)" "C:/caminho/logo.png"
```
Capture the output and drop it into the `<img src="...">`. If no logo, use a text-based cover.

## 2. Detect a headless browser for this OS
Probe these paths in order; use the first that exists. (Edge ships on every Windows 11; Chrome is
common on Mac/Linux.)

**Windows** (PowerShell `Test-Path`):
1. `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
2. `C:\Program Files\Microsoft\Edge\Application\msedge.exe`
3. `C:\Program Files\Google\Chrome\Application\chrome.exe`
4. `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`

**macOS** (`test -f` / `ls`):
1. `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
2. `/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge`
3. `/Applications/Chromium.app/Contents/MacOS/Chromium`

**Linux** (`command -v` / `which`):
1. `google-chrome` / `/usr/bin/google-chrome`
2. `chromium` / `chromium-browser` / `/usr/bin/chromium`
3. `microsoft-edge` / `/usr/bin/microsoft-edge`

Narrate plainly: *"Achei o navegador, gerando o PDF..."* — never expose the binary path/flags.

## 3. Run the render (exact command)
Use `--headless=new` (≈5× faster than the old mode; the critic confirmed `new` over `old`).
Always use **forward slashes** in the `file:///` URL and quote paths.

**Windows (PowerShell):**
```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless=new --disable-gpu --no-pdf-header-footer "--print-to-pdf=C:/Users/.../.claude/propostas/<slug>-<data>-proposta.pdf" "file:///C:/Users/.../.claude/propostas/<slug>-<data>-proposta.html"
```
**macOS / Linux (bash):**
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="/abs/path/<slug>-<data>-proposta.pdf" "file:///abs/path/<slug>-<data>-proposta.html"
```
Flags:
- `--headless=new` — modern headless (fast).
- `--disable-gpu` — avoids GPU quirks in headless.
- `--no-pdf-header-footer` — removes the browser's URL/date header & footer (clean page). (Older
  Edge builds use `--print-to-pdf-no-header`; if the modern flag is ignored, that's the fallback.)
- `--print-to-pdf="<out>"` — output path. `file:///<abs html>` — input.

## 4. Confirm the PDF actually rendered (don't bluff)
After the command, verify the file exists and is non-trivial:
- Check the file exists and size > ~5 KB.
- Optionally confirm it starts with the bytes `%PDF-`.
If it didn't render, do NOT claim success — fall through to the fallback and say so.

## 5. CSS that the headless engines actually honor (put in the HTML)
- `@page { size: A4 landscape; margin: 0 }` — the deck is **landscape**; the template already sets this.
  `--print-to-pdf` honors the `@page size` (incl. `landscape`), so the command below needs no extra flag.
  Control real margins via inner `.slide` padding (more predictable than `@page margin` across engines).
- `-webkit-print-color-adjust: exact; print-color-adjust: exact;` on `body` — **forces background
  colors/gradients to print** (without it the cover/section bars come out white). **Essential.**
- `page-break-inside: avoid;` (and `break-inside: avoid;`) on tables/cards/pricing blocks.
- Font sizes in `pt`. Running headers/footers via `@page` margin boxes work only on newer Chrome
  (131+) — don't depend on them; put the footer in normal flow at the bottom of each section instead.

## 6. Fallback — no headless browser found
If no binary is detected, the self-contained HTML is the deliverable. Tell the user in ONE line:
> *"Não achei um navegador pra gerar o PDF automático aqui. Abri a proposta em HTML: abre o arquivo
> `<caminho>` no navegador e faz **Ctrl+P → Salvar como PDF**. Fica idêntico — o arquivo é
> completo, não depende de internet nem de mais nada."*
Never present this as a failure of the proposal — the document is done; only the auto-conversion
step couldn't run. The HTML is self-contained, so the user's Ctrl+P produces the same PDF.

## Fontes
- learn.microsoft.com (.../ms-edge-installation-location, .../how-to-print-to-pdf-with-no-header) — Edge path + no-header flag.
- andre.arko.net/2025/05/25/chrome-headless-print-to-pdf — the url()-in-CSS gotcha; base64 works.
- groups.google.com/.../headless-dev (EaorgNBWmYU) — headless=new vs old (new ~5× faster).
- whizz-tech.com/.../edge-prints-without-backgrounds — print-color-adjust:exact forces backgrounds.
- pdf4.dev/blog/css-print-styles-pdf-guide & developer.chrome.com/blog/print-margins — @page support, margin boxes (Chrome 131+).
- nutrient.io / glukhov.org — confirmation that Python stdlib has no PDF path (browser is the zero-config answer).
