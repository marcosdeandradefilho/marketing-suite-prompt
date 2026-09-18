# revisao-visual.md — RENDER the site, LOOK at it, FIX it (the make-or-break loop)

This is the single most important step and the one most generators skip. **The #1 reason an
AI-built site looks cheap is that nobody ever looked at it.** Code that validates can still be ugly:
collapsed images, broken contrast, cramped spacing, a hero that reads wrong. You cannot judge a
website without seeing the pixels. So before delivering, you RENDER the site to an image, READ that
image, grade it, and FIX what's wrong — then render again. Loop until it actually looks good.

Never tell the user a site "looks premium / is ready" if you have not seen it rendered. If you
couldn't render (no browser/Node), say so plainly — never claim a visual review you didn't do.

## How to render (zero-config, uses the browser already on the machine)

The skill bundles `assets/render.js` — a tiny Node script that drives the installed Chrome or Edge
headless via the DevTools Protocol (no npm, no Puppeteer). It waits for fonts + images (download AND
decode) so the screenshot is faithful, and forces scroll-reveal elements visible so nothing is hidden.

Run it (replace `<SKILL>` with this skill's folder path, `<SITE>` with the generated folder). Args:
`<fileOrUrl> <out.png> [width=1440] [mobile=0] [clipY] [clipH]`.

**Capture in REGION CROPS — this is the primary, reliable method.** A one-shot full-page capture stalls
on long pages (a full restaurant menu, a long scroll), so don't depend on it. Instead capture the page in
readable bands (each ≤ ~2000px tall) plus mobile. You also SEE detail far better in crops than in a squished
tall image:
```bash
# desktop, in bands (clipY clipH). Pick offsets so each band covers a section.
node "<SKILL>/assets/render.js" "<SITE>/index.html" "<SITE>/_review/d-hero.png"   1440 0 0    1300
node "<SKILL>/assets/render.js" "<SITE>/index.html" "<SITE>/_review/d-anchor.png" 1440 0 1300 1800   # the ANCHOR section
node "<SKILL>/assets/render.js" "<SITE>/index.html" "<SITE>/_review/d-mid.png"    1440 0 3100 1800
node "<SKILL>/assets/render.js" "<SITE>/index.html" "<SITE>/_review/d-foot.png"   1440 0 4900 1800
# full mobile (390) — short enough to capture whole; ALWAYS do this one
node "<SKILL>/assets/render.js" "<SITE>/index.html" "<SITE>/_review/mobile.png"   390 1
```
A short page (no long list) can be captured whole at 1440 with no clip — fine when it works. The script
caps a no-clip capture at 6000px and prints the FULL page height, so use that printed height to plan your
band offsets; it also has a watchdog (~55s) that kills the browser and exits cleanly if a capture stalls
(no zombie processes — just re-run with crops). The **hero and the ANCHOR section** are the two bands that
matter most — always look at those.

Then **Read each PNG** (you can see images) and grade it. Put review shots in a `_review/` subfolder and
delete it before final delivery (it must not ship).

Tips:
- Always check **mobile (390)** — most BR local-business traffic is mobile. Cramped/overflowing mobile is
  a common miss, and the mobile page is usually short enough to capture whole.
- Re-render the affected band(s) after every fix round. Don't fix blind.

## The 15-point "is this beautiful?" rubric (grade the screenshot, each yes/no)

Aim for **13+**. Below 11 it still looks amateur — fix and re-render. Be honest; grade what you SEE.

1. **Type pairing** — heading font is NOT Inter/Roboto/Poppins; there's a real display↔body contrast (serif display + grotesque body, or a distinctive grotesque).
2. **Hierarchy** — biggest headline ≥ 3× body size, clear size/weight steps between levels.
3. **Tracking** — large headings look tightened (`-0.02em`), not loose/default.
4. **Measure** — body text capped (~60–75ch), never running the full container width.
5. **Whitespace** — sections have generous breathing room (96–160px desktop padding); nothing cramped.
6. **Neutrals** — background is a tinted off-white/near-black, NOT pure `#fff`/`#000`.
7. **Accent discipline** — exactly ONE accent, used only on actions/highlights (<10% of surface).
8. **No AI gradient** — no purple→blue/indigo gradient anywhere.
9. **Layout** — intentional structure (asymmetry / editorial / real grid), not everything center-stacked.
10. **Spacing consistency** — gaps read as one system (8px scale); no random odd values, even rhythm.
11. **Imagery** — every image actually RENDERS (no empty boxes), real/relevant, consistently treated.
12. **Hero** — one clear message + one primary CTA, strong type; not a slider, not multi-CTA clutter.
13. **Chrome restraint** — subtle hairline borders/shadows, consistent radii; no glassmorphism, no heavy soft shadows everywhere.
14. **No slop markers** — no emoji icons/bullets, no colored left-border cards, no lorem ipsum, no broken/placeholder links.
15. **Niche fit + cohesion** — it looks like THIS industry (a restaurant looks appetizing/warm, a law firm authoritative) and like ONE committed brand decision, not averaged defaults. The niche's ANCHOR section (menu / portfolio / before-after / results) is present and prominent.

## Failure → fix map (what to change when a screenshot looks wrong)

| What you see | Fix |
|---|---|
| Empty box where an image should be | Image didn't render. Almost always `height:100%` on an `<img>` inside an indefinite-height grid/flex collapsing it → use `aspect-ratio` + `width:100%` instead (see `tecnica-qualidade.md`). Or a dead src (Picsum is unreliable → use Pexels per `refazer-e-imagens.md`). Verify the image loads. |
| Dark, murky, "moody" where it should be inviting | Wrong base for the niche. Food/wellness/local/trust → LIGHT + warm. Re-derive palette (`arquitetura-nichos.md`). |
| Looks like a generic landing/sales page | Drop the marketing skeleton (stat-strip + repeated CTA banners). Lead with the niche's ANCHOR content (menu/portfolio/results), quieter rhythm. |
| Cramped, everything close together | Increase section padding to 96–160px; raise gaps to the 8px scale; cap text measure. |
| Headline weak / not much bigger than body | Push hero headline to `clamp(2.8rem, …, 6rem)`, tighten tracking, raise contrast. |
| Looks flat / sterile / "default" | Tinted neutrals (not #fff/#000), one confident accent, a subtle grain or near-tone gradient, real photography, asymmetric layout. |
| Text hard to read on an image | Add a scrim gradient behind hero text; check AA contrast. |
| Purple/indigo anywhere as accent | Replace with the niche/brand accent reserved for CTAs. |
| Mobile overflows / text touches edges | Add page gutters (20–24px), stack splits, let the menu/nav collapse, re-check at 390. |

## Loop discipline
- Round 1: render full desktop + mobile + hero/anchor crops. Grade. List the 2–5 worst issues.
- Fix those at the ROOT in the CSS/HTML (not band-aids). Re-render the affected views.
- Round 2 (and 3 if needed): re-grade. Stop when ≥13/15 AND every image renders AND mobile is clean.
- Cap at ~3 rounds; if still failing one stubborn thing, say so honestly in the receipt rather than
  shipping a quiet defect. Diminishing returns past 3 rounds usually means a structural rethink.

## Degraded mode (be honest)
- **No Chrome/Edge, or Node missing / < v21** → you cannot auto-review. Build to the written spec,
  then tell the user in PT-BR: *"Não consegui abrir o site aqui pra revisar no olho — abre o
  index.html no navegador (e no celular) e me diz o que ajustar."* Flag `confere você: revisão
  visual` in the receipt. NEVER claim it looks good unseen.
- **A region won't capture / times out on a huge page** → cap the height or capture in halves; the
  script caps very long pages at 16000px by default.
