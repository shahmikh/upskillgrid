# Measuring SEO and AI visibility

## Google Search Console
- Performance: queries, pages, CTR, position. Use the branded vs non-branded filter (Nov 2025) to watch brand growth. AI Mode traffic is counted inside "Web" totals; the AI features reports (Jun 2026) show AI Overviews/AI Mode impressions only (no clicks, no queries).
- Pages (indexing): "Alternate page with proper canonical tag" and "Page with redirect" are normal; "Crawled/Discovered – currently not indexed" usually resolves as the site gains trust and internal links.
- Sitemaps: submit once; Google re-reads on its own. Resubmit only if the URL changes or to force a re-read.
- URL Inspection → Request indexing for important new pages (~10/day).
- Refresh targets: pages at positions 8–30 or with high impressions and low CTR.

## Bing Webmaster Tools
- Import from Search Console, submit sitemap, check AI Performance (Copilot/Bing AI citations, cited pages, grounding queries; no clicks).

## GA4: AI search channel (step by step)
1. Admin → Data display → Channel groups → Create new channel group (copy of default), e.g. "Channels with AI".
2. Add new channel "AI search": Source matches regex
   `.*(chatgpt|openai|perplexity|claude\.ai|anthropic|gemini\.google|bard\.google|copilot\.microsoft|copilot\.com|meta\.ai|deepseek|grok|you\.com|phind|mistral).*`
3. Save channel → click **Reorder** → drag "AI search" above "Referral" → Apply → Save group. (If it's below Referral it never matches.)
4. Reports → Acquisition → Traffic acquisition → switch the primary dimension to the new channel group.
Treat counts as a floor: many AI apps strip referrers (Claude rarely passes one). AI referrals were ~0.3% of web traffic in 2025–26 studies.

## Manual AI visibility panel (monthly)
- Fixed list of 20–50 buyer prompts ("best AI automation consultant for dental practices", "how much does an AI receptionist cost"…).
- Run each several times in ChatGPT, Perplexity, Gemini, Google AI Mode, Copilot and Claude; log whether the brand is mentioned, which pages are cited, and which competitors/sources appear. AI answers rarely repeat exactly (SparkToro: <1 in 100 chance of the same list twice), so track share of mentions over time.
- Paid trackers if budget allows: Semrush AI Toolkit, Ahrefs Brand Radar, Profound.

## Leading indicators to report
- Indexed pages (Google and Bing), impressions trend, branded search growth, Copilot citations, directory profiles indexed and review counts, third-party mentions, panel mention share, AI-channel sessions and conversions (forms, bookings).

## Sanity checks
- Don't double-count GA4 (direct gtag plus a GA4 tag in GTM).
- Add a "How did you hear about us?" free-text field to booking/contact forms; people often say "ChatGPT".
