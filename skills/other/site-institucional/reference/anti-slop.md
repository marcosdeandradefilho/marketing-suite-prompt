# anti-slop.md — the AI-slop cluster to FORBID + the premium alternative for each

Read this BEFORE writing any CSS. The single biggest risk for an AI-generated site is that it looks
AI-generated: a fixed, recognizable cluster of defaults. The rule is concrete — **name the generic
default and forbid it**, then ship the alternative. This list prevents slop; the real ENFORCEMENT is
seeing the rendered page and grading it (`revisao-visual.md`) — a checklist can't catch an ugly result,
only your eyes can. Sources: prg.sh "What AI Slop Actually Looks Like", dev.to "why everything is purple",
MDN, WCAG, 60-30-10.

## The canonical AI-slop signature (FORBID this exact combo)
Inter/Roboto font · purple/indigo accent (`#6366f1` indigo-500 lineage) · hero = centered text + one/two
CTA buttons · three feature cards in a row each with a generic icon · white/light-gray background · rounded
corners on EVERY box · uniform subtle shadows at exactly `0.1` opacity. If a build drifts toward this, stop
and re-decide.

### Why purple? (so the model doesn't relapse)
Tailwind UI demos shipped `bg-indigo-500` / `text-indigo-600` / `from-indigo-500 to-purple-600` gradients
years ago; that code saturated GitHub/tutorials and LLMs learned "web button = purple" as a probability
distribution. **Guardrail: never emit indigo/violet/purple as a default accent or gradient. ALWAYS require a
deliberate palette (60-30-10, one accent reserved for CTAs). If you have no brand color, use the niche
palette hint — never fall back to indigo.**

## Forbid → premium alternative (the table)
| AI-slop tell | Premium alternative |
|---|---|
| Inter/Roboto/Poppins as the headline font | Serif display (Fraunces/Instrument Serif/Newsreader) + grotesque body (Hanken/Bricolage/Space Grotesk) pairing |
| Indigo/violet accent, `from-indigo→purple` gradient | ONE confident brand/niche accent reserved only for CTAs; gradients only as subtle 2-3-blob mesh, low saturation, never indigo |
| Hero = centered text + 2 buttons on light-gray | Editorial asymmetric hero: oversized display headline left + visual right, or full-bleed cinematic; ONE primary CTA |
| 3 identical feature cards in a row, each an icon | Bento grid of varied sizes, OR alternating image/text rows; differentiated cards; icons inline-SVG (Lucide), not emoji |
| Rounded corners on everything | Varied radii used with intent (sharp + soft); sharp/editorial for premium, soft only where it earns it |
| Uniform `0.1`-opacity shadows everywhere | Layered/colored shadows used sparingly; elevation only where it means something; often borders/contrast instead |
| Emoji as section/feature icons | Inline-SVG icon set (Lucide, MIT) styled with `currentColor` |
| Leftover "Lorem ipsum" | Real client copy ONLY; if unknown, a marked `<!-- TROCAR: texto -->` placeholder in PT-BR, never lorem |
| Fake testimonials with stock/AI avatars | Real depoimentos (nome + bairro/cidade) or a clearly-marked placeholder; initials-circle instead of a fake face |
| Perfectly predictable order (hero→3 features→testimonial→pricing→CTA), all centered | Keep the BR section order but vary the visual arrangement per section; left-aligned long-form text; whitespace as structure |
| Timid washed-out palette, everything `#fff`/`#000` | Off-white + near-black slate + one bold accent; real contrast (60-30-10) |
| **Dark/moody base on a niche that wants light+warm** (restaurant, clinic, dental, local) | Default LIGHT per the niche; dark only for steakhouse/bar/barbershop/strength-gym/luxury (`arquitetura-nichos.md`) |
| **Empty image box** (placeholder didn't render, or Picsum dead) | Real photo (Pexels, `refazer-e-imagens.md`); fix the `height:100%` collapse (`tecnica-qualidade.md`); verify every image renders in the review |
| **Generic "Entradas/Principais" cards for a restaurant** | The REAL menu, typeset (3-tier hierarchy, 1–2 columns) — the menu IS the site |

## What AI slop is MISSING (enforce these too)
Real **visual hierarchy** (not just bigger=header) · deliberate **color theory** (the one accent is a
choice) · intentional **type pairing** · **whitespace as a design element** · **brand voice/personality**.
AND — critically for an institutional site — **forms that actually WORK**: required-field indicators, input
validation, error states, ARIA labels, keyboard navigation, `:focus-visible`. "An LLM generates a contact
form that looks like a form but doesn't work like one" — don't be that. See `lock-in-br.md` (form spec) and
`tecnica-qualidade.md` (a11y).

## Per-niche differentiation (so two sites don't look identical)
A clínica estética (rose/nude/dourado, serif elegante, antes&depois) must NOT look like an advogado (azul-
marinho/grafite/bordô, serif clássica sóbria, áreas de atuação) or an academia (preto/neon, bold condensada,
planos). Pull the palette + tone + section emphasis + trust seal from `arquitetura-nichos.md` for the actual
niche — never reuse one look for all. If you catch yourself reaching for the same palette/layout twice, that's
the slop relapse — re-derive from the niche.

## Quick self-check before shipping CSS
- [ ] Headline font is NOT Inter/Roboto/Poppins; there is a serif+grotesque pairing.
- [ ] Accent is NOT indigo/violet/purple; it's one niche/brand color reserved for CTAs.
- [ ] Hero is NOT centered-text-plus-two-buttons; it's editorial/asymmetric or cinematic.
- [ ] Serviços are NOT three identical centered icon cards; layout varies (bento/rows).
- [ ] No emoji icons, no lorem ipsum, no fake faces, no `0.1` uniform shadow on everything.
- [ ] The contact form has required markers + validation + ARIA (it WORKS).
- [ ] The palette/layout differs from a different niche's.
