# referencias-visuais.md — SEE 5+ current real references BEFORE designing (mandatory, every niche)

The design must come from **real, current, beautiful sites you actually LOOKED AT** — not from memory and
not from a built-in template. This runs on EVERY build, for every niche. You CAN see them: the bundled
`assets/referencias.js` screenshots live URLs, and you read the PNGs with vision. Get **at least 5** usable
references in front of your eyes, pull the current design language from them, and design from that.

## Step A — Find candidate references (aim for 6–8 URLs; some will fail)
`WebSearch` for the niche's CURRENT best work. Use TWO kinds of source and mix them:
1. **Showcase / gallery / listicle pages** — the richest source, and they rarely bot-block:
   - *"melhores sites de <nicho> 2026"*, *"best <nicho> websites 2026"*, *"<nicho> website design inspiration"*.
   - Curators: `awwwards.com`, `godly.website`, `land-book.com`, `httpster.net`, `behance.net`, `dribbble.com`,
     `siteinspire.com`, and "X best <niche> websites" blog roundups (sitebuilderreport, framer, etc.).
   - One listicle page can show 5–15 curated current designs as embedded screenshots → screenshot a TALL band
     of it (band 4000–6000) and you see many references in ONE shot.
2. **Named real top sites in the niche** — pick the standout names the search surfaces (e.g. for fine dining:
   noma.dk, ateliercrenn.com, alinearestaurant.com). Their homepages are real-world references.
Collect ~6–8 URLs (over-collect, because ~1 in 3 individual sites will be a bot-wall or JS-only loader).

## Step B — Screenshot them all (one browser launch)
```bash
node "<SKILL>/assets/referencias.js" "<SITE>/_refs" 1600 <url1> <url2> <url3> ...     # individual sites
node "<SKILL>/assets/referencias.js" "<SITE>/_refs" 5000 <listicle-url>               # a showcase page, tall band
```
It writes `_refs/ref-1.png …` and prints a status line per URL:
- `OK` → a real page rendered — READ it.
- `BLANK` / `BLOCKED` / `ERR` → a bot-wall ("verificando…", "checking your browser"), an SPA loader, or a
  cookie-only screen. **SKIP these** — don't waste a read; don't treat them as references.
Keep `_refs/` out of the delivered site (it's scratch — delete before Step 6).

## Step C — LOOK at them (this is the point)
**Read each `OK` PNG with vision.** For the ones that are real, note CONCRETELY:
- BASE: light or dark? warm or cool?
- PALETTE: the actual colors (background, text, the one accent).
- TYPE: serif or sans display? the voice (elegant/bold/editorial)?
- LAYOUT / HERO: full-bleed photo? editorial split? type-first? how is the nav?
- IMAGERY: how is photography used (full-bleed, grid, duotone)? how prominent?
- The "current / expensive" cues — what makes these look 2026, not 2015.
You need **≥5 usable references seen**. If fewer loaded, add 2–3 more URLs (lean on listicle/gallery pages,
which almost never block) and re-run. Only if the web is truly unavailable do you fall back to the encoded
niche DNA — and you SAY so in the receipt.

## Step D — Synthesize, don't copy
Find what the BEST references share, and make THAT your design language — then adapt it to the client's brand
color, content, and the niche's anchor. Never clone one specific site. Write the 4-line brief (BASE · PALETTE ·
TYPE · ANCHOR + section order) from what you saw, and design Step 2 against it.

**Tell the user (PT-BR, honest, builds trust):** *"Antes de montar, olhei alguns sites atuais de referência
do seu nicho — [2-3 nomes] — pra puxar o padrão de design de 2026. O caminho que vi é [claro/escuro], com
[tipo/foto/layout]. Vou montar nessa linha."* Naming the real references you actually looked at is part of
the value.

## What the encoded niche file is for now
`arquitetura-nichos.md` is NOT the look anymore — the LOOK comes from these live references. That file is the
niche's FUNCTIONAL spine (the ANCHOR section, BR trust seals like OAB/CRC/CRO, structure essentials, the menu
pattern) plus a SAFE fallback palette for when the web is down or no reference loads. Lead with what you saw;
use the file for function + as the safety net.

## Honest limits
- You see the RENDERED page (great for look/layout/type/color/imagery), not its code. That's enough to design
  from. You can't "read their CSS" — synthesize from what's visible.
- Bot-walls and heavy SPAs will fail — that's expected and handled (over-collect + skip flagged ones).
- A reference may have a cookie banner or modal over it — you can still read the design through it; just don't
  mistake the banner for the design.
