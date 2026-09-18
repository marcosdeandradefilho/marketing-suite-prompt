# armadilhas-monetizacao.md — real gotchas (R3) + monetization model (R4)

Both sections rely on REAL public signals. A gotcha or a price with no link is not a finding — it goes to
"não confirmado / verificar" (`reference/criterios-evidencia.md`).

## R3 — Mining real gotchas (the "armadilhas conhecidas" the spec sells)
The differentiator is reading REAL pain (GitHub issues, changelogs, reviews), not guessing pitfalls.

### GitHub Issues — by community pain
Search UI or `https://api.github.com/search/issues?q=<QUERY>`. Verified-working qualifiers:
- `reactions:>50`, `reactions:10..100`, `interactions:>100` (interactions = reactions + comments),
  `comments:>30`. Combine with `is:issue label:bug`.
- Sort by pain: `sort:reactions-+1` (👍 = "me too"), `sort:reactions-heart`,
  `sort:reactions-thinking_face` (confusion), `sort:interactions` (combined).
- Worked, most-felt bugs in one repo: `repo:OWNER/REPO is:issue label:bug sort:reactions-+1-desc`.
- Label OR via comma: `label:bug,gotcha,regression`. The 2025 Issues-search rebuild adds boolean
  AND/OR with nested parentheses across fields, e.g. `(type:Bug OR type:Epic)`.
- Niche-wide sweep (not one repo): `is:issue is:open label:bug,regression reactions:>20
  sort:reactions-+1-desc`, optionally scoped `language:python` or by `topic:`.
- **Zero-config path:** hit `https://api.github.com/search/issues?q=<QUERY>` with WebFetch (returns JSON)
  or open the github.com search UI URL — NO `gh` CLI / Bash needed (keeps the skill zero-config).
(Verified live: docs.github.com searching-issues-and-pull-requests; github.blog 2025 rebuild post.)

### Changelogs / release notes — breaking changes = the highest-risk gotchas
- Grep release notes for the uppercase token **`BREAKING CHANGE`** (Conventional Commits footer) and the
  **`!` type suffix** (`feat!:`, `refactor!:`) — both force a SemVer MAJOR bump.
- In Keep-a-Changelog files, breaking changes are sorted FIRST under each version → the top entries of each
  release block are the riskiest. Scan MAJOR jumps specifically (1.x → 2.0.0).
(Source: conventionalcommits.org/en/v1.0.0/; keepachangelog.com.)

### Blog posts / HN / Reddit — experiential gotchas
Exact-phrase searches that surface real failure write-ups:
- `"things I wish I knew" <tool>`, `"lessons learned" <tool> production`, `<tool> gotchas`,
  `"don't make the mistake" <tool>`. Add `site:medium.com` / `site:dev.to` / `site:news.ycombinator.com`.
- HN: `hn.algolia.com` with the tool name, filter by points/comments. Reddit:
  `site:reddit.com <tool> problem|alternative|switched away`. Threads titled "Why we moved off X" or
  "X alternatives" concentrate pitfalls + the churn trigger.
(Source: softwareengineeringdaily.com Kubernetes-gotchas post as a confirmed example.)

### App-store / G2 / Capterra reviews — 1-3★ concentrate the real issues
Filter to 1-2★ (and 3★) reviews — low-rated reviews carry the actionable problems standard sweeps miss.
Bucket complaints into: **functional errors, crashes, feature requests, privacy/ethical, HIDDEN COSTS**.
~11% of complaints blame a RECENT UPDATE — cross-reference review dates against the changelog.
(Source: pmc.ncbi.nlm.nih.gov/articles/PMC11323132/ review-mining study.)

Report each gotcha as: *what breaks → why it matters for the builder → link*. Stamp user reports
"relato não auditado".

## R4 — Detecting the monetization model
### Decision tree (apply in order, on the pricing page)
1. **Permanently free tier alongside paid tiers?** → **freemium**. (A time-limited free TRIAL is NOT
   freemium — that's subscription.)
2. Copy says "per month" / "per year" / "/mo" / "billed annually" with renewal language? → **assinatura**.
3. Single upfront price, NO renewal language? → **pagamento único / perpétuo**.
4. Word "lifetime" / "pay once"? → **vitalício**.
5. No price, "free & open source", GitHub Sponsors / Open Collective / donate button? → **open-source/doação**.
(Source: revenera.com SaaS pricing models guide.)

### Where to look on each surface
- **Pricing page:** count distinct tier cards (industry norm ≈ 3.2 public tiers + 1 custom/Enterprise
  "Contact us" = tiered subscription); a monthly/annual toggle = subscription.
- **README:** top badges — a "Sponsor"/"GitHub Sponsors"/license badge = open-source/donation; a
  "Pro"/"Cloud" link = open-core freemium.
- **App-store listing:** an "In-App Purchases" list = freemium/IAP; a non-zero buy price with no IAP =
  one-time paid app.
- **AppSumo / lifetime-deal check:** `<tool> appsumo` or `<tool> lifetime deal` — an AppSumo listing
  signals a one-time LTD model (often a launch tactic distinct from the main subscription). *(LTD/donation
  detection is reasoned, medium confidence — confirm with a real listing before asserting.)*
(Source: getmonetizely.com 2025 pricing benchmark.)

### Price-band rulers (keep foreign prices as `US$`, never bare `$`)
Generic SaaS bands: starter/basic **US$9-29**, professional **US$25-59**, business **US$49-99**; a common
3-tier ladder is **US$29 / US$49 / US$199**. Charm pricing (US$29 not US$30) is near-universal. **61% of
SaaS now use HYBRID** (flat fee + usage/per-seat) — a page showing a base fee + "per 1,000 requests" /
"per seat" is hybrid, not pure subscription.
(Source: getmonetizely.com.) These are GLOBAL bands — present them as reference, not as what the reader
must charge in R$. If the reader will sell in Brazil, note the model, and that the R$ price is their call.
