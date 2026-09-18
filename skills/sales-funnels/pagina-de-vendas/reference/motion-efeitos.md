# motion-efeitos.md — premium effects, zero-build, degrade-safe, fast on a Brazilian phone

Motion is the strongest "muito foda" signal, but a sales page lives
or dies on a phone over mobile data. RESTRAINT: 1-2 purposeful effects beat a fireworks show. Every effect ships
with the reduced-motion gate AND a JS-off visible baseline. Animate ONLY `transform` and `opacity`.

## MANDATORY accessibility gate — prefers-reduced-motion (always, on everything)
The CSS guard does NOT stop GSAP/Lenis (JS-driven). You MUST do BOTH:
```css
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{ animation-duration:.01ms!important; animation-iteration-count:1!important;
    transition-duration:.01ms!important; scroll-behavior:auto!important; }
  .js .reveal{ opacity:1; transform:none; }   /* show content, no fly-in */
}
```
```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
// if reduce === true: do NOT init Lenis, do NOT create ScrollTrigger reveals (set final state instantly)
```
**JS-off baseline:** put `<script>document.documentElement.classList.add('js')</script>` in `<head>` and gate
hidden states on `.js`, so JS-off users and crawlers see full content:
```css
.reveal{opacity:1;transform:none}              /* default visible */
.js .reveal{opacity:0;transform:translateY(28px);transition:opacity .7s ease,transform .7s ease}
.js .reveal.is-visible{opacity:1;transform:none}
```

## Tier 0 — always, no library (covers ~98% of browsers)
IntersectionObserver reveal (most robust no-lib mechanism), CSS transitions on hover, `position:sticky`,
`scroll-snap` where it fits.
```js
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target);}}),{threshold:.15,rootMargin:'0px 0px -10% 0px'});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
```

## Tier 1 — CSS scroll-driven (zero JS, progressive — Firefox just shows content)
```css
@keyframes reveal{from{opacity:0;clip-path:inset(0 60% 0 50%)}to{opacity:1;clip-path:inset(0 0 0 0)}}
@supports (animation-timeline: view()){ .revealing{animation:auto linear reveal both;animation-timeline:view();animation-range:entry 25% cover 50%} }
```
**Scroll progress bar, 100% CSS** (animate scaleX, GPU-composited; degrades to nothing):
```css
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
#progress{position:fixed;left:0;top:0;width:100%;height:4px;background:var(--c-acc);transform-origin:0 50%;animation:grow auto linear;animation-timeline:scroll()}
```

## Tier 2 — GSAP + ScrollTrigger + Lenis (CDN, free/MIT, default ON for premium desktop)
GSAP is 100% free since 2025 (SplitText included). Use 3.13+. Lenis is MIT.
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrollTrigger.min.js"></script>
<script src="https://unpkg.com/lenis@1.3.23/dist/lenis.min.js"></script>
```
```js
if(window.gsap && !reduce){
  gsap.registerPlugin(ScrollTrigger);
  const lenis=new Lenis(); lenis.on('scroll',ScrollTrigger.update);
  gsap.ticker.add(t=>lenis.raf(t*1000)); gsap.ticker.lagSmoothing(0);
  gsap.utils.toArray('.reveal').forEach(el=>gsap.from(el,{y:40,opacity:0,duration:.8,ease:'power2.out',scrollTrigger:{trigger:el,start:'top 85%'}}));
}
```
**SplitText headline reveal** (HEADLINE only, never body): `new SplitText('.hero h1',{type:'lines',mask:'lines',autoSplit:true})` then `gsap.from(split.lines,{yPercent:100,opacity:0,duration:1,ease:'power4.out',stagger:.08,...})`.
**Magnetic button** (use `gsap.quickTo`, the official high-frequency-event optimum):
```js
const xTo=gsap.quickTo(btn,'x',{duration:.6,ease:'power3.out'}), yTo=gsap.quickTo(btn,'y',{duration:.6,ease:'power3.out'});
btn.addEventListener('mousemove',e=>{const r=btn.getBoundingClientRect();xTo((e.clientX-r.left-r.width/2)*.4);yTo((e.clientY-r.top-r.height/2)*.4);});
btn.addEventListener('mouseleave',()=>gsap.to(btn,{x:0,y:0,duration:.6,ease:'elastic.out(1,0.3)'}));
```
**Parallax/pin without scroll-jacking:** `scrub:1` (number, not `true`) for soft inertia; `ease:'none'`; apply to MEDIA, never text.

## Background effects (CSS, cheap)
**Mesh "aurora"** (<1KB, no WebGL; dark = hsl lightness 30-40%, alpha 0.4-0.6, stronger looks neon):
```css
background-color:#0a0a12;
background-image:radial-gradient(at 30% 20%,hsla(40,80%,40%,.5) 0,transparent 50%),radial-gradient(at 80% 60%,hsla(20,70%,35%,.45) 0,transparent 50%);
```
**Animated gradient with @property** (interpolates color; Firefox fallback = `background-size:200%` + animate `background-position`):
```css
@property --g1{syntax:"<color>";initial-value:#C8962B;inherits:false}
@property --g2{syntax:"<color>";initial-value:#1A1714;inherits:false}
.bg{background:linear-gradient(135deg,var(--g1),var(--g2));animation:cores 10s ease infinite}
@keyframes cores{0%,100%{--g1:#C8962B;--g2:#1A1714}50%{--g1:#E0AE3C;--g2:#2A2520}}
```
**Grão/noise** (kills the flat look), as `::after` `mix-blend-mode:overlay;opacity:.06-.12;pointer-events:none`:
```html
<svg style="position:fixed;inset:0;width:100%;height:100%;pointer-events:none;opacity:.07;mix-blend-mode:overlay;z-index:1"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>
```
**Glassmorphism (saturate, not just blur — `-webkit-` mandatory for Safari):**
```css
backdrop-filter:blur(14px) saturate(180%);-webkit-backdrop-filter:blur(14px) saturate(180%);
background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;
```
NEVER put text over 10% opacity glass: add a ~30% solid film behind the text. Blur 12-16px on a big card (not 20+).
**Marquee** (logos/depoimentos, 100% CSS): two identical `.marquee__content` (2nd `aria-hidden="true"`), `overflow:hidden`, `@keyframes scroll{to{transform:translateX(calc(-100% - var(--gap)))}}`, pause on `:hover`.
**Spotlight/cursor-glow** (desktop only): `radial-gradient(circle at var(--x) var(--y),rgba(255,255,255,.4),transparent 40%)` + a mousemove that sets `--x/--y`.

## Mobile rules (most traffic is here — do NOT ship desktop motion to phones)
- **No magnetic button, no cursor-glow, no spotlight on touch** (there's no mouse — wasted JS, can feel broken).
  Gate them behind `matchMedia('(hover:hover) and (pointer:fine)').matches`.
- **Lighten parallax** or drop it on small screens (heavy on low-end Android). Keep simple scroll reveals.
- Sticky mobile CTA bar instead of hover effects (see `componentes-conversao.md`).
- Tap targets 44-48px; no effect that delays the first tap.

## Performance budget (a beautiful page that loads in 8s is a loss)
- **Hero is the LCP:** never lazy-load it; mesh/gradient hero is cheapest. If a hero VIDEO: muted, `playsinline`,
  `preload="none"` or a poster, lazy-init; never autoplay a heavy file on mobile data.
- `font-display:swap` + preconnect both Google origins; request only the weights used; prefer variable fonts.
- All `<script>` are `defer`; GSAP/Lenis load after content. Keep total JS small.
- Every `<img>` has explicit `width`+`height` (reserve space, CLS≈0) + `loading="lazy"` below the fold +
  `decoding="async"`.
- **CDN fallback (make-or-break):** wrap GSAP use in `if(window.gsap){...}`. If GSAP/Lenis fail to load, the
  page still works on Tier 0 (IntersectionObserver) + the JS-off baseline. The page NEVER depends on the CDN to
  show content.

## AVOID (cheesy / dated / anti-premium)
Heavy whole-page parallax, scroll-jacking, slow preloaders/splash, autoplay carousels without a pause control,
neumorphism, SplitText on body text, blur >30px or blur without saturate (gray fog), `will-change` on
everything, animating width/top/left (jank), decorative motion with no function ("functional over decorative").
