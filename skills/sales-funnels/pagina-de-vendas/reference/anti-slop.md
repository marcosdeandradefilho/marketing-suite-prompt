# anti-slop.md — the AI-slop cluster to FORBID + the premium alternative for each

Read BEFORE writing any CSS. The single biggest risk is a page that
looks AI-generated: a fixed, recognizable cluster of defaults. The rule is concrete: **name the generic default
and forbid it, then ship the alternative.** In the render loop (`tecnica-render.md`), you LOOK at the screenshot
and count these tells. **5+ tells = "heavy slop" = FAIL → fix and re-render.**

## Myth, dismantled
A page does NOT convert better for being ugly. **CLAREZA + CREDIBILIDADE + 1 CTA focado** converts; the ugly
guru page hits that by accident (it's harder to ruin). Quality pages convert better than slop, not worse.
Position every build as **"premium QUE converte"**, never "feio que converte". And steal the guru page's
MECHANICS while changing the skin: the guru page works because of zero cognitive friction + one action per
screen + brutal eye-direction. Replace the hand-drawn yellow arrow with eye-gaze (a photo looking at the CTA) /
a thin pointing line / isolated color contrast on the CTA alone.

## The 15 AI-slop tells → premium alternative (LOOK for these on the render)
| Forbid (slop tell) | Premium alternative |
|---|---|
| Inter em TUDO (headline + body) | A personality sans (Geist/Hanken/Bricolage) OR an editorial serif (Instrument Serif/Fraunces); headline-font ≠ body-font |
| Space Grotesk italic on the highlight word | Instrument Serif italic, used with intent |
| "VibeCode purple" (indigo→violet, `#6366f1`, from-indigo→purple gradient) | Neutrals + ONE rare accent you own (gold, emerald, royal blue, terracotta). NEVER indigo as default |
| Dark mode roxo + mid-gray text (fails WCAG AA) | Contrast that passes AA; dark with one disciplined accent |
| Gradients on everything + big colored glows | Subtle mesh + 1-2 glass surfaces |
| Centered hero text + 2 buttons on light-gray | Editorial asymmetric OR oversized type-forward hero; ONE primary CTA |
| A badge/pill logo above the H1 | Remove it |
| **Colored border on the left/top of cards** (the #1 tell-tale) | Separate by whitespace + type weight, not a colored stripe |
| 3 identical feature cards, icon on top, same size | Break symmetry: varied sizes/weights, bento or alternating rows |
| Visible 1,2,3 numbered sequence | Editorial/bento grid |
| Emoji in the nav/bullets/sections | Inline-SVG line icons (Lucide) styled with currentColor, OR nothing |
| Headings/labels in ALL CAPS everywhere | Hierarchy by weight/size (CAPS only for small mono eyebrows) |
| Stock photo "pessoas colaborando" | Real screenshot/clip of the product |
| Generic diffuse `0.1` shadow on everything | Shadow with intent, OR a border, OR nothing |
| shadcn defaults left untouched | Fine only if you customize the tokens (color/radius/shadow); a starting point, not the product |
| Leftover "Lorem ipsum" | Real approved copy only; unknown → marked `<!-- TROCAR -->` in PT-BR, never lorem |
| Fake testimonials with stock/AI faces | Real proof (nome + cidade) or a marked placeholder + initials circle, never a fabricated face |

## The 4 signals that make it look CARO (enforce these)
1. **Whitespace** (the #1 luxury signal): 80-120px+ between sections. "Emptiness creates value."
2. **Restricted palette** (3-5 colors; the one accent is a deliberate choice reserved for CTAs).
3. **Intentional typography** (≤2 faces, weight contrast, generous leading; the headline font is a choice).
4. **Subtle motion with purpose** (1-2 animations + the reduced-motion gate). Not a fireworks show.
What slop is MISSING that you must add: real visual hierarchy, deliberate color theory, intentional type
pairing, whitespace as structure, brand voice/personality, AND forms/CTAs that actually WORK (focus states,
validation, ARIA — see `componentes-conversao.md`).

## Contrast gate (run on the built page — the dark-roxo-cinza tell is a real WCAG failure)
For every text-on-surface pair, ensure contrast ≥ **4.5:1** (normal text) / **3:1** (large ≥24px or ≥18.66px
bold, and UI/icons). Compute relative luminance: linearize each channel `cs=ch/255; c = cs<=0.03928 ? cs/12.92
: ((cs+0.055)/1.055)^2.4`; `L=0.2126R+0.7152G+0.0722B`; contrast `=(Llight+0.05)/(Ldark+0.05)`. If the accent
fails as a button with white text, do one of: restrict the accent to large/decorative use, generate a
darker/lighter text variant, or darken the surface. Never ship an inaccessible CTA. Logo/wordmark text is exempt
but still aim for legibility.

## Execution bugs that instantly kill "premium" (never repeat these)
- **Nothing illegible behind text.** A giant decorative number/word (e.g. a big "16") or a watermark placed
  BEHIND a heading must either sit in its OWN space (text above/below it, not crossing) OR be faint enough
  (opacity ≤ .10) AND tested on the render that the text on top is fully readable. A bright color behind small
  text (e.g. an amber "16" under an eyebrow + subtitle) can make both unreadable. Render it and LOOK before trusting it.
- **A sales page does not need a sticky top nav.** The job is "scroll down to the offer", not navigate. Use a
  simple non-sticky logo header, or none. If you do keep a nav, **never put the price in it** (price before
  value = the master anti-rule; the visitor must be sold before seeing the number). The first price on the
  page appears in the offer block, not the header.
- **No orphaned grid cells.** A "wide"/featured card in an N-column grid must make the rows still fill (e.g. a
  full-width feature card + the rest in 2 columns = even rows). A `span 2` card in a 3-col grid with 6 siblings
  leaves a visible hole. Render and check the grid closes.
- **Consistent vertical rhythm.** Every section uses the SAME `padding-block` token. A block that hugs the next
  one (tiny gap) while the previous gap is huge reads amateur. Integrate the guarantee right under the offer
  card with a small controlled margin, not a section break.
- **The price must dominate the offer card.** The final number is the largest type in that block (clamp to
  ~64-110px), isolated with whitespace, the struck anchor small above it. A price you have to hunt for = a
  weak offer.

## Sales page ≠ institutional (design consequence)
The sales page is long, copy-first, CTA-heavy, proof-heavy. The design's job is to keep the eye moving down and
make the CTA inevitable: a clear single column for reading, full-bleed bands to break rhythm, the accent only on
CTAs, proof shown generously, the offer block visually distinct (the one place the page "stops" the eye). If you
catch yourself reaching for the same palette/layout you used on a different product, that's the slop relapse;
re-derive from THIS product's niche and voice.
