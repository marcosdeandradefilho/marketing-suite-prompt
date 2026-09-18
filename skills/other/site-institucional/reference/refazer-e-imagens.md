# refazer-e-imagens.md — rebuild-from-URL path + REAL zero-config imagery

Two things the skill can't fake: the client's REAL content, and good photography. This file covers how
to recover real content from an existing site, and how to put REAL, relevant photos into the site with
no API key. Bad/missing images are the #1 cheapening tell across every niche — get this right.

## Imagery: REAL photos via Pexels (zero-config, no key) — the default
**Do NOT use Lorem Picsum** (random images, often unreachable, and they make a site look stock/broken)
and **never `source.unsplash.com`** (sunset 2021, dead). Use **Pexels direct image hotlinks** — free for
commercial use, no attribution required, and the image URL is derivable from the photo page URL.

**The URL pattern (stable, no key):**
```
https://images.pexels.com/photos/<ID>/pexels-photo-<ID>.jpeg?auto=compress&cs=tinysrgb&w=1600
```
`<ID>` is the number at the end of a Pexels photo page URL: `pexels.com/photo/<slug>-<ID>/`.

**How to find good, niche-true IDs (when web is available):** `WebSearch` with
`site:pexels.com <subject>` — e.g. `site:pexels.com cozy french bistro interior`, `site:pexels.com
plated fine dining dish`, `site:pexels.com modern dental office`, `site:pexels.com architecture interior`.
The result titles describe each photo (the slug) so you can pick relevant ones; take the trailing `<ID>`.
Pick a small set that matches the niche + the section (hero, the anchor, gallery, team/portrait).

**Download them LOCAL (preferred for a deliverable).** Hotlinking works but depends on Pexels uptime and
can be slow; downloading makes the site self-contained, faster, and robust. Save into the site's `img/`:
```bash
curl -s -L "https://images.pexels.com/photos/<ID>/pexels-photo-<ID>.jpeg?auto=compress&cs=tinysrgb&w=1600" -o "site-<cliente>/img/hero.jpg"
```
Reference locally (`<img src="img/hero.jpg">`). Keep total deploy < 50MB; request sensible widths
(hero ~1600–1920, supporting ~1000–1200, gallery thumbs ~700–800). Pexels license: free personal +
commercial, attribution not required, modification allowed; NOT allowed: reselling unaltered copies on
stock platforms, implying endorsement, depicting identifiable people in a bad light.

**Mark every photo as swappable.** It's a real photo but still a placeholder for the client's own:
add a `<!-- TROCAR: foto X -->` next to each, and give the swap instructions on delivery (below).

**Always verify images RENDER.** In the visual review (`revisao-visual.md`), confirm no image box is
empty. The usual cause is CSS, not the file — see the `height:100%` collapse pitfall in
`tecnica-qualidade.md`. Use `aspect-ratio` + `width:100%` on images, never `height:100%` inside an
indefinite-height grid/flex.

### When NO good photo fits / web is unavailable (fallback only)
A designed placeholder that reads intentional (never a grey box): a block with reserved `aspect-ratio`,
a subtle brand-tinted gradient, a centered inline-SVG icon, and a small label ("Foto: ambiente da clínica")
+ the `<!-- TROCAR -->` marker. Better to be image-light with strong type/whitespace than to fill with junk.

### Icons
**Lucide** (MIT, ~1500 icons) — paste the raw inline `<svg>` (zero runtime dep, stylable via `currentColor`).
Heroicons (MIT) is a fine alternative. Never use emoji as icons.

### Texture / no-raster premium touches (pure CSS)
Subtle inline-SVG `feTurbulence` grain at ~3–6% opacity over flat color; 2–3 soft low-saturation
`radial-gradient` blobs; hairline frames; `clip-path` accents. All zero-asset. (Keep a full-page fixed
grain filter light — heavy turbulence over a tall page is expensive to rasterize.)

### Logo
Client has a logo (found on rebuild or supplied) → reuse as-is; never redraw it. No logo → a clean
**wordmark** in the chosen display font (tracked/weighted for a logo feel), optionally with one inline-SVG
mark. Zero-config (Google Fonts). Tell the user it's a placeholder until they have a real logo.

## Rebuild-from-URL path
1. **Fetch:** `WebFetch <url>` with a TARGETED extraction prompt — WebFetch returns Markdown (styling is
   stripped), so ask for what you need verbatim: *"List every service/dish, price, phone, e-mail, address,
   business hours, and social link (instagram/whatsapp/ifood/facebook) on this page verbatim, plus the page
   title, all headings, and the main body copy."*
2. **Capture the ANCHOR content.** For a restaurant the menu is often on a separate page or a PDF/image —
   if the first fetch misses it, fetch the menu/cardápio page too, or ask the user to paste it. A rebuilt
   restaurant site WITHOUT the real menu is worse than the original. Same for an architect's projects, a
   firm's results, a clinic's treatments.
3. **Two hard limits:** (a) NO JavaScript rendering — SPA/builder sites (Wix dynamic, React) may come back
   nearly empty; (b) output truncated ~100KB. Near-empty extraction → fall back to asking the user; never fabricate.
4. **Redirects:** cross-host redirects are returned, not followed — re-call once with the redirect URL.
5. **Fallback (blocked/empty/JS-only):** ask the user (PT-BR) to paste the site's text/screenshots or fill a
   short intake (nome · serviços/cardápio · telefone/WhatsApp · endereço · horário · redes · cores). Never scrape elsewhere.
6. **Brand recovery is best-effort:** logo is recoverable (header `<img>`/`og:image`) → reuse. Colors/fonts
   usually are NOT (stripped) → ask, or propose from the niche; never claim you "detected" a palette you guessed.
7. **Detect the niche** from the content → apply its DNA (`arquitetura-nichos.md`), then rebuild premium.
8. **INVIOLABLE:** real services, prices, phone, address, hours, CNPJ come ONLY from the user / fetched page.
   Anything unknown → a marked `<!-- TROCAR: ... -->` placeholder, never a fabricated fact.

## TROCAR handoff checklist (output in PT-BR, anti-guru)
```
As fotos são reais (do Pexels, uso comercial liberado), mas são temporárias — troque pelas fotos do
próprio negócio quando tiver:
1) Use as fotos do cliente, ou baixe em pexels.com / pexels.com/pt-br (uso comercial, sem precisar dar crédito).
2) Salve na pasta /img com nomes tipo hero.jpg, prato-1.jpg.
3) No HTML, procure os comentários <!-- TROCAR: foto X --> e troque o arquivo da imagem.
4) Cada bloco já tem o tamanho/recorte certo (aspect-ratio), então a foto nova encaixa sem quebrar o layout.
Licença Pexels: não revenda a foto crua e pessoas identificáveis não podem aparecer de forma ofensiva.
```
