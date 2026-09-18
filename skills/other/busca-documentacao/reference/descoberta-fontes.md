# descoberta-fontes.md — building the candidate set (R1)

Goal: land on a clean, comparable set of ~5-12 real tools that solve the same problem. Use English
search terms (GitHub/topics are English-keyed). Every operator below was verified returning HTTP 200
with real results in the build research, EXCEPT where a FAIL/AVISO is flagged.

## A. GitHub Topics API — discover the canonical vocabulary FIRST (don't guess tags)
`https://api.github.com/search/topics?q=<termo>` with header `Accept: application/vnd.github.mercy-preview+json`.
Returns canonical sibling topics. Example: `q=note-taking` → note-taking, obsidian-md, note-taking-app,
notion, joplin. Feed those back into `topic:` repo searches to widen/narrow deterministically.
(Verified live: docs.github.com search APIs.)

## B. GitHub repo search — the candidate set
`https://api.github.com/search/repositories?q=<QUERY>&sort=stars&order=desc&per_page=30`
Combine 3-4 qualifiers into ONE query (budget!). Verified-working qualifiers:
- `topic:password-manager stars:100..5000` — topic + star range (verified: 129 repos; buttercup ★4402).
- `kanban in:name,description language:typescript` — keyword in name/desc + language. Use ONE keyword
  here. **AVISO (live test jun/2026):** a MULTI-word `in:name,description` query like `invoice OCR
  in:name,description ...` returns `total_count: 0` (it wants both words literally in the name/desc).
  Split into separate single-word searches (`invoice in:name,description`, `OCR in:name,description`) or,
  better, lead with `topic:` (e.g. `topic:invoice topic:ocr`) which is far more reliable.
- `topic:note-taking pushed:>2025-01-01 stars:>1000` — **`pushed:` filters to ACTIVELY maintained**.
- `topic:crm archived:false stars:>200` — **`archived:false` drops dead projects**.
- `topic:markdown-editor good-first-issues:>5` — beginner-friendly signal.

**AVISO `in:readme` (critic-2 FAIL):** `<termo> in:readme stars:>500` matches the term ANYWHERE in the
README, so star-sorted results are dominated by mega-lists (`sindresorhus/awesome`, `public-apis`), NOT
real apps in the niche. Prefer `topic:` or `in:name,description`. If you must use `in:readme`, do NOT
sort by stars and do NOT promise specific top results — eyeball and filter.

Default recipe: `topic:<canonical> archived:false pushed:>2024-01-01 stars:>200`, sorted by stars,
take the top ~8-12, then de-dupe. **Pick the SPECIFIC topic, not the generic one** (live test jun/2026):
a broad topic like `topic:scheduling` is polluted by job/task schedulers (luigi, cron-likes) and calendar
UIs; the niche-specific `topic:appointment-booking` / `topic:appointment-scheduling` returns the actual
booking apps. Use Topics-API (§A) to find the specific canonical tag first, then search it.

## C. awesome-lists — a pre-curated, human-categorized candidate set
Fetch the **RAW** README, not the rendered page:
`https://raw.githubusercontent.com/<org>/<repo>/HEAD/README.md` (try `HEAD`, fallback `master`/`main`).
(Verified: awesome-selfhosted raw README = 321KB plaintext, HTTP 200.)
- `### ` (H3) headings ARE the categories (Analytics, Automation, Backup, CRM, ...).
- List lines `- [Name](url) - description \`License\` \`Lang\`` give name + desc + stack in one line —
  a ready-made comparison row.
Find the relevant awesome-list with `awesome <niche> github` in WebSearch.

## D. Proprietary / SaaS competitors (no GitHub repo) — `site:` ONLY
**CRITIC-2 FAIL — do NOT WebFetch these (403 Cloudflare "Just a moment"):** alternativeto.net,
producthunt.com, saashub.com all block automated fetch.
- Use WebSearch: `site:alternativeto.net <ferramenta conhecida>` → ranked alternatives + category in the
  result snippets. `<tool> alternatives` (plain WebSearch) also surfaces these pages.
- Product Hunt and SaaSHub are **manual-only**: you may mention "vale olhar no Product Hunt" but never
  script a fetch — the buyer must open it in a browser.

## E. Where features live on a product/doc SITE — crawl order
Verified by live keyword-density probe. Crawl in this order, stop when you have enough:
1. **README** (raw fetch, §F below) — fastest, free.
2. **`/changelog` or GitHub `/releases`** — the single richest feature source (Linear `/changelog` had
   "changelog" 452×; a repo's `https://github.com/<o>/<r>/releases` lists every shipped feature).
3. **`/docs` root** — capability nav (Stripe docs root "onboarding" 131×, "feature" 90×).
4. **`/pricing`** — which features are gated = what the market considers premium (Obsidian `/pricing`).
These paths are CONVENTIONS, not guarantees — try them in order and skip what 404s. Apply the
fetch-integrity gate (`reference/criterios-evidencia.md`) to every page.

## F. The raw-README trick (cheap feature extraction)
`https://raw.githubusercontent.com/<owner>/<repo>/HEAD/README.md`, then keep only lines matching
`^#{1,3}\s` to get the heading skeleton. The feature list lives under a heading literally named
**"Features"**, or a marketing variant (**"Everything you need"**, **"Why <Tool>"**). A **"Stack"**
heading gives the architecture for free. (Verified: usememos/memos has "Features"+"Quick Start"+"Try the
Live Demo"; twentyhq/twenty has "Everything you need"+"Stack".)
**Strip inline HTML** (`<img ...>`, badges) from captured headings before using them (twenty's headings
contain tags).
Some projects (e.g. joplin) push features to a linked docs site — then the README heading list is
meta-only and you follow the link to `/docs`.

## Output of R1
A de-duped list of ~5-12 tools, each with: name, repo/site URL (real, fetched/searched this session),
star count if from GitHub, and whether it's open-source or closed SaaS (decides the extraction path in
`reference/extracao.md`). Anything you couldn't actually load → "Fontes que não consegui ler", not the set.
