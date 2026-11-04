# Site audit checklist

Report as a prioritized table (gap, evidence, why it matters, fix). Fix what you can; list what needs the owner.

## P1: Trust, proof and policy risk
- [ ] Testimonials verifiable? (real names/roles/companies, photos, links to original reviews). Unverifiable ones → ask the owner; remove if not real.
- [ ] Case studies with real outcome numbers and their own URLs? Big claims ("1,500+ projects") backed by something?
- [ ] Clear author identity on content: byline, author box, About page with credentials, contact details, editorial/AI disclosure.
- [ ] Third-party corroboration: directory profiles (Clutch/G2/GoodFirms etc. by niche) live, indexed, with reviews; LinkedIn and YouTube linking back; profiles in schema sameAs.
- [ ] Publishing pattern: no mass-produced or templated thin pages; each page has a non-commodity element. Programmatic city pages = risk.
- [ ] No invented statistics, fake reviews, hidden text, doorway pages, back-button hijacking.

## P2: Content coverage
- [ ] Money pages (services, pricing, industries) answer cost, timeline, what's included, who it's for, proof, FAQ.
- [ ] Pricing information exists (ranges or pricing factors).
- [ ] Honest comparison content for "X vs Y" buyer questions.
- [ ] Original data or first-hand examples somewhere on the site.
- [ ] Posts answer-first: lead answer, takeaways, question H2s with direct answers, FAQ, sources, author box, internal links.
- [ ] Refresh candidates from Search Console (positions 8–30, high impressions/low CTR).
- [ ] Internal links: every page linked from at least one other relevant page besides the index.

## P2: Measurement
- [ ] Search Console verified, sitemap submitted, branded filter and AI reports checked.
- [ ] Bing Webmaster Tools verified, sitemap submitted, AI Performance checked.
- [ ] GA4 custom channel group "AI search" above Referral (regex on chatgpt, openai, perplexity, claude.ai, gemini.google, copilot, etc.).
- [ ] Monthly prompt panel (20–50 buyer prompts × several runs × each engine) logged.
- [ ] Analytics not double-firing.

## P3: Technical
- [ ] robots.txt allows search + AI search/user bots; Sitemap line present.
- [ ] Sitemap complete, lastmod accurate; IndexNow key + pings (ideally automated).
- [ ] Every page: unique title ≤60, description 140–160, one H1, canonical, OG/Twitter image, valid JSON-LD.
- [ ] Organization/ProfessionalService with logo and sameAs; Person/ProfilePage; BlogPosting dates real; BreadcrumbList; VideoObject uploadDate with timezone.
- [ ] Key content and numbers present in static HTML (not JS-only).
- [ ] No horizontal scroll at 390px; tables wrap; images sized and lazy-loaded.
- [ ] Core Web Vitals measured (PageSpeed/CrUX); heavy scripts deferred; fonts non-blocking.
- [ ] 404 returns 404 + noindex; redirects 301; one canonical domain.
- [ ] Internal working files (notes, drafts, reports) excluded from the published site.

## Keep as-is (don't waste time)
- Permissive robots.txt, existing llms.txt, existing FAQPage markup, Search Console AI features opted in, no restrictive nosnippet/max-snippet.
