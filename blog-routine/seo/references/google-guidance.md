# Google official guidance (snapshot: October 2026)

Verify time-sensitive items with a web search before quoting them; Google changes things several times a year.

## AI Overviews and AI Mode
- Same indexing and ranking systems as classic Search. No extra requirements, no special optimizations: a page must be indexed and eligible to show a snippet. Source: Search Central "AI features and your website" (developers.google.com/search/docs/appearance/ai-features).
- Both use **query fan-out**: several related sub-searches per question. Pages that answer sub-questions (cost, timeline, comparisons, how-to steps) get pulled in even if they don't rank top 10 for the main query.
- May 2025 post "Top ways to ensure your content performs well in Google's AI experiences": unique non-commodity content; prepare for longer, follow-up questions; good page experience (all devices, fast, main content clear); crawlable/indexable; structured data that matches visible content.
- May 2026 "Guide to Optimizing for Generative AI Features" (developers.google.com/search/docs/fundamentals/ai-optimization-guide): focus on unique, first-hand content. Explicitly skip llms.txt, content chunking, AI-specific rewriting, inauthentic brand mentions, and over-investing in structured data for AI.
- Controls: Google-Extended affects Gemini training/grounding only, not AI Overviews. `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex` do affect AI features but also normal snippets. Since June 2026 there is a site-wide opt-out from Search AI features in Search Console (UK CMA pressure); Google says it doesn't affect classic ranking. Recommend staying opted in unless there's a business reason.

## Helpful content, E-E-A-T and AI-generated content
- "Creating helpful, reliable, people-first content": write for people, show first-hand Experience, Expertise, Authoritativeness and Trust (trust matters most). Ask "Who, How, Why": who made it (clear authorship), how (disclose automation/AI where readers would expect it), why (to help people, not to rank).
- AI-assisted content is allowed if it's helpful and original. Quality Rater Guidelines (Jan 2025) tell raters to give the Lowest rating to main content made with automated tools with little effort or originality; Sept 2025 update reportedly tightened this.
- Self-serving or unverifiable trust claims (fake testimonials, invented stats) undermine trust.

## Spam policies to respect
- Scaled content abuse (mass pages with little value, any production method), site reputation abuse, expired domain abuse (all from March 2024, still in force).
- Back button hijacking: new policy announced April 2026, enforced from 15 June 2026. Don't interfere with the browser back button.
- Since 30 Aug 2026, site-reputation-abuse manual actions no longer apply for users in the EEA; affected sections may be ranked separately instead.

## Core and spam updates (dates)
- 2025 core: Mar 13–27, Jun 30–Jul 17, Dec 11–29. 2025 spam: Aug 26–Sep 21/22.
- 2026 core: Mar 27–~Apr 8, May 21–Jun 2 (plus a Discover-only core update from Feb 5). 2026 spam: Mar 24, Jun 24, Aug 18–21, Sep 24–Oct 8.
- During a rollout, don't make big site changes or draw conclusions; compare Search Console after it completes.

## Structured data status
- Removed/limited: HowTo results (2023); FAQ rich results stopped showing 7 May 2026, docs removed June 2026; June 2025 dropped Course Info, Claim Review, Estimated Salary, Learning Video, Special Announcement, Vehicle Listing (Book Actions reinstated); more types lost Search Console reporting from Jan 2026.
- Still supported and worth doing: Organization (logo, sameAs), LocalBusiness (only for real eligible locations), Article/BlogPosting, BreadcrumbList, ProfilePage/Person, VideoObject (docs updated Sept 2026), Review snippets (not for a business's reviews of itself), Product where relevant.
- Structured data must match visible content.

## Search Console changes
- Jun 2025: AI Mode clicks/impressions counted inside "Web" totals. Jun 2025: Insights report. Nov 2025: branded vs non-branded queries filter. Jun 2026: separate AI features reports (impressions only, no clicks or queries) and the AI opt-out setting.

## llms.txt
- Gary Illyes (Jul 2025): Google doesn't support it and has no plans to. John Mueller compared it to the keywords meta tag. The May 2026 guide lists it as something to skip.

## Technical basics Google still emphasizes
- Crawlable links, indexable pages, canonical tags, XML sitemaps with accurate `lastmod` (Google ignores lastmod it can't trust), mobile-first, Core Web Vitals (LCP, INP, CLS) as a light ranking signal and part of page experience.
- Crawler docs moved to developers.google.com/crawling; IP lists are common-crawlers.json / special-crawlers.json.
