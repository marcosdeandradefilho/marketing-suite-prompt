# motion-efeitos.md — premium motion, zero-config CDN, degrade-safe

Motion is the strongest "muito foda" signal, but it's also where a deliverable client site breaks
(JS off, reduced-motion, slow device, Firefox). Use a LAYERED strategy where each tier degrades to
the one below, and ALWAYS ship the accessibility + JS-off guards. Sources: gsap.com, lenis (darkroom-
engineering), MDN/caniuse, web.dev, Codrops.

## The layered strategy (pick per build; premium default = through Tier 2)
- **TIER 0 — always, no lib:** CSS transitions on hover, `scroll-snap`, `position:sticky`,
  IntersectionObserver `.js`-gated reveals, the `prefers-reduced-motion` guard. Covers ~98% of browsers.
- **TIER 1 — progressive, no lib:** CSS scroll-driven `animation-timeline: view()` reveals (Firefox just
  shows content, no animation — fine). ~82% support, always treated as enhancement.
- **TIER 2 — premium, opt-in via CDN (DEFAULT ON for premium builds):** GSAP + ScrollTrigger (reveal/pin/
  parallax) + Lenis smooth scroll. The look top agencies use; pure HTML, no build.

## TIER 0 — the always-on baseline
```css
/* reveal, gated by the .js class so JS-off / crawlers see content */
.reveal{ opacity:1; transform:none; }              /* default: visible */
.js .reveal{ opacity:0; transform:translateY(28px); transition:opacity .7s ease, transform .7s ease; }
.js .reveal.is-visible{ opacity:1; transform:none; }
```
```html
<script>document.documentElement.classList.add('js')</script>  <!-- in <head>, before CSS paints -->
```
```js
// IntersectionObserver reveal — ~98% supported, most robust no-lib mechanism
const io = new IntersectionObserver((es)=>es.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('is-visible'); io.unobserve(e.target);} }), {threshold:0.15, rootMargin:'0px 0px -10% 0px'});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
```

## MANDATORY accessibility — prefers-reduced-motion (make-or-break)
The CSS global guard does NOT stop GSAP tweens or Lenis (both JS-driven). You MUST do BOTH:
```css
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{ animation-duration:.01ms!important; animation-iteration-count:1!important;
    transition-duration:.01ms!important; scroll-behavior:auto!important; }
  .js .reveal{ opacity:1; transform:none; }   /* show content, no fly-in */
}
```
```js
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
// if reduce === true: DO NOT init Lenis, DO NOT create ScrollTrigger reveals (or set y:0/opacity:1 instantly)
```
WCAG also requires a pause control for any autoplay/looping motion longer than 5s — so no autoplaying
carousels without a control.

## TIER 2 — GSAP + ScrollTrigger + Lenis (exact CDN, free/MIT)
GSAP core is 100% FREE for commercial use since 2025-04-29 (Webflow), including former Club plugins
(SplitText, ScrollSmoother, etc). Use **3.13.0+**. Lenis is MIT (`lenis`, NOT the deprecated
`@studio-freight/lenis`).
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.3.23/dist/lenis.min.js"></script>
```
```js
if(!reduce){
  gsap.registerPlugin(ScrollTrigger);
  // Lenis smooth scroll, synced to GSAP ticker (disable autoRaf when GSAP-driven)
  const lenis = new Lenis();
  gsap.ticker.add((t)=>lenis.raf(t*1000));
  gsap.ticker.lagSmoothing(0);
  lenis.on('scroll', ScrollTrigger.update);

  // reveal-on-scroll (staggered), transform+opacity only = compositor 60fps
  gsap.utils.toArray('.reveal').forEach(el=>{
    gsap.from(el,{ y:40, opacity:0, duration:.8, ease:'power2.out',
      scrollTrigger:{ trigger:el, start:'top 85%' } });
  });
  // parallax (GPU-friendly)
  gsap.to('.parallax-img',{ yPercent:-20, ease:'none',
    scrollTrigger:{ trigger:'.parallax-section', start:'top bottom', end:'bottom top', scrub:true } });
  // pin a section while content animates
  ScrollTrigger.create({ trigger:'.pin-section', start:'top top', end:'+=100%', pin:true });
}
```
When GSAP drives reveals, set the `.reveal` base to visible for reduced-motion/JS-off and let GSAP take over
only when `!reduce` (don't leave elements stuck at opacity:0 if the script is skipped).

## TIER 1 — CSS-native scroll-driven (no JS, progressive)
```css
@keyframes reveal { from{ opacity:0; transform:translateY(40px);} to{ opacity:1; transform:none;} }
@supports (animation-timeline: view()){
  .reveal-css{ animation: reveal linear both; animation-timeline: view(); animation-range: entry 0% cover 30%; }
}
```
Support 2026: Chrome/Edge 115+, Safari 26+, **Firefox NOT supported** (disabled by default) → content must
default visible; the animation only enhances. Same for View Transitions API (~88%) and `@starting-style`.

## Tasteful microinteraction set (recommend)
Subtle staggered reveal-on-scroll · smooth hover states (color/underline/lift via transform) · magnetic or
underline-grow buttons · image hover zoom (`transform:scale`) · text/split reveal on the hero headline ·
counters (anos/clientes) · custom cursor only for portfolio/agência (optional) · page-load reveal (short).

## AVOID (cheesy / dated / anti-premium)
Heavy whole-page parallax · slow/heavy preloaders or splash screens · autoplay carousels (esp. without a
pause control) · animating layout properties (width/height/top/left — jank) · `will-change` on everything ·
motion that fires before content is readable. Animate ONLY `transform` and `opacity`.

## Performance rules
Transform/opacity = compositor thread = 60fps. Never animate layout props. Lazy-init below-the-fold effects.
Keep total motion JS tiny and `defer`-loaded. The hero (LCP) must paint fast — motion enhances, never blocks.
