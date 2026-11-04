---
name: seo
description: Plan, write, audit and fix websites for Google rankings AND AI answers (SEO, AEO, GEO, AI Overviews / AI Mode, ChatGPT search, Copilot, Perplexity, Gemini, Claude). Use this skill whenever the user wants to rank higher, get indexed, get cited by AI search, write or refresh a blog post or landing page for search, choose keywords or topics, add schema/structured data, fix Search Console issues, check robots.txt / sitemap / llms.txt, review E-E-A-T or trust signals, track AI referrals in GA4, or keep up with Google/AI search updates, even if they only say "SEO", "visibility", "traffic", "Google", or "make this rank".
---

# SEO, AEO and GEO for 2026

The core finding behind this skill: **AEO and GEO are mostly still SEO.** Google says AI Overviews and AI Mode use the same index and ranking as classic Search, with no special requirements beyond being indexed and snippet-eligible. Other AI engines each read a different index (Bing, Brave, their own crawlers), and what correlates most with being cited is **independent proof and brand mentions on other sites**, not markup tricks. So the work splits into three parts, in this order of impact:

1. **Trust and proof** (E-E-A-T): real first-hand content, verifiable testimonials and results, a clearly identified author, and third-party mentions (reviews, directories, YouTube, LinkedIn, podcasts).
2. **Content that answers the real question best**, written so both people and machines can lift the answer.
3. **Technical hygiene** so every engine can crawl, render and trust the page.

Facts change fast (four notable Google changes in 2026 alone). Treat the reference files as a dated snapshot (October 2026) and verify anything time-sensitive with a quick web search before advising on it.

## Pick the workflow

| User wants | Do this | Read |
|---|---|---|
| Write or refresh a post / landing page | Content workflow below | `references/content-playbook.md` |
| Audit a site or page | Audit workflow below | `references/audit-checklist.md` |
| Schema, robots, sitemap, speed, indexing | Technical fixes | `references/technical-schema.md` |
| "Why isn't ChatGPT / Perplexity citing me?" | Engine-by-engine check | `references/ai-engines.md` |
| "What does Google say about X?" | Official guidance | `references/google-guidance.md` |
| Measure results, GA4 AI traffic, Search Console | Measurement | `references/measurement.md` |
| Stay current / set up monitoring | Monitoring routine | `references/monitoring.md` |

## Content workflow (new or refreshed page)

1. **Find the real question.** One primary search phrase per page, plus the sub-questions people (and AI "query fan-out") ask next: cost, how long, how it works, who it's for, alternatives, mistakes. Check what currently ranks and what AI answers cite for it.
2. **Decide the non-commodity angle.** Google's 2026 guidance says to focus on unique, first-hand content. Every page needs at least one thing a generic article can't have: a real example or screenshot, real numbers (or clearly labelled hypothetical ones), a tested workflow, a clear opinion with the reason.
3. **Write answer-first.** Direct answer in the first 2 sentences, a short key-takeaways box, question-style H2s each opening with a self-contained 1 to 2 sentence answer, then detail, lists, a table where it helps, and an FAQ of real questions.
4. **Back claims with sources.** Link 2 to 4 primary sources (government, platform docs, professional bodies, original research) inline and in a sources box. Only use URLs confirmed to exist. Never invent statistics, clients, quotes or results.
5. **Show who wrote it.** Byline, author box with real credentials and links, editorial note. Be honest about AI assistance.
6. **Connect it.** Link to the matching service and industry pages and 1 to 2 related posts; link to the new page from an older relevant page.
7. **Technical finish.** Title ≤60 chars with the phrase, meta description 140 to 160 chars, one H1, canonical, OG/Twitter image, Article/BlogPosting + Breadcrumb JSON-LD with accurate `datePublished`/`dateModified`, sitemap `lastmod` only when content really changed, mobile check (no horizontal scroll at 390px).
8. **Get it discovered.** Sitemap updated, IndexNow ping (Bing, Yandex and others), optional "Request indexing" in Search Console for important pages, share on LinkedIn/YouTube.

Details, templates and the banned-filler list are in `references/content-playbook.md`.

## Audit workflow

Work through `references/audit-checklist.md` and report findings as a prioritized table: **P1** trust/proof and policy risks, **P2** content gaps on money pages, **P3** technical polish. For each gap give the evidence (file/URL), why it matters, and the fix. Fix what you can directly; list what needs the owner (reviews, credentials, Bing setup, videos).

## Things to stop recommending (2026 evidence)

These waste effort; say so plainly if the user asks for them:

- **llms.txt as a ranking lever.** Google says it doesn't use it; a ~300k-domain study found no link to AI citations. Keep one if it exists, but spend no more time on it.
- **FAQ schema for rich results.** FAQ rich results stopped showing on 7 May 2026 (HowTo ended in 2023). FAQPage markup is harmless machine-readable Q&A, nothing more.
- **Extra schema "for AI".** Google's guide lists over-investing in structured data for AI as something to skip; studies show no link between schema coverage and AI citations. Do the basics well.
- **Chunking or rewriting content specially for AI**, or faking freshness by changing dates without real updates.
- **Mass-produced pages** (AI or human): scaled-content abuse policy plus core updates. Many AI-content-at-scale sites lost most of their traffic. Prefer fewer, deeper pages.
- **City/location pages or a Google Business Profile at a virtual address** for remote service businesses. Ineligible and risky; use industry or use-case pages instead.
- **"AI rankings"** as a fixed number. AI answers vary run to run; measure share of mentions across repeated prompts.

## Off-site work (where most AI visibility comes from)

Brand mentions on other sites correlated far more with AI visibility than backlinks in large studies, with YouTube mentions strongest. For service businesses, AI answers lean heavily on review directories (Clutch especially for agencies), LinkedIn and Reddit. Recommend, in order: verified reviews on the directory that matters for the niche, consistent profiles linked from the site and added to schema `sameAs`, founder presence on YouTube and LinkedIn, podcast and guest-expert appearances, and original data others will quote. Mention that these are correlations, not guarantees.

## How to talk to the user

Many owners aren't technical. Lead with what to do and why in plain words, keep jargon out or explain it once, and give click-by-click steps for anything they must do themselves (Search Console, Bing Webmaster Tools, GA4). Be honest about uncertainty: most AI-search evidence is correlational and changes quickly.
