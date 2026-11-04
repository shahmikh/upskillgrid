# How AI engines find and cite sources (snapshot: October 2026)

## Bot types (allow search + user bots to be cited; training bots are a business choice)

| Vendor | Training | Search index | User-triggered fetch |
|---|---|---|---|
| OpenAI | GPTBot | OAI-SearchBot | ChatGPT-User |
| Anthropic | ClaudeBot | Claude-SearchBot | Claude-User |
| Perplexity | (none declared) | PerplexityBot | Perplexity-User |
| Google | Google-Extended (token, controls Gemini training/grounding) | Googlebot | Google-agent fetchers |
| Apple | Applebot-Extended (token) | Applebot | |
| Microsoft | | Bingbot | |
| Meta | Meta-ExternalAgent | | Meta-ExternalFetcher |

- Blocking OAI-SearchBot removes a site from ChatGPT answers (except navigational links); robots changes take ~24h. User-triggered fetchers may not fully follow robots.txt.
- Docs: OpenAI developers.openai.com/api/docs/bots (IP lists openai.com/gptbot.json, /searchbot.json, /chatgpt-user.json); Anthropic support.claude.com article 8896518; Perplexity docs.perplexity.ai/docs/resources/perplexity-crawlers; Apple support.apple.com/en-us/119829.

## Where answers come from

| Engine | Index | Practical lever |
|---|---|---|
| Google AI Overviews / AI Mode / Gemini | Google index (renders JS) | Normal SEO, Search Console |
| ChatGPT search | Bing data + OpenAI's own crawl + licensed partners (reportedly some Google results) | Bing Webmaster Tools, IndexNow, crawlable HTML |
| Microsoft Copilot | Bing | Bing Webmaster Tools, accurate sitemap lastmod, IndexNow |
| Claude | Brave Search results (inferred, not officially confirmed) + Claude-SearchBot | Don't block Googlebot (Brave follows its rules); allow Claude bots |
| Perplexity | Own crawler | Allow bots; crawlable HTML |

**Bing matters as much as Google** for AI visibility: verify in Bing Webmaster Tools (it can import from Search Console), submit the sitemap, use IndexNow. Bing's AI Performance report (public preview Feb 2026) shows Copilot citations, cited pages and grounding queries (no clicks). Bing's content advice: clear headings, concise sections, tables/FAQs, data-backed claims, regular updates.

## Rendering
Most AI crawlers (OpenAI, Anthropic, Perplexity, Meta, Common Crawl) don't execute JavaScript. Google and Apple do. Put all important content, numbers and links in the initial HTML. Make sure a CDN/firewall isn't blocking AI search bots.

## What correlates with being cited (correlation, not proof)
- Brand mentions on other sites: 0.664 correlation with AI Overview visibility (Ahrefs, 75k brands) vs ~0.218 for backlinks. YouTube mentions strongest (~0.737, Dec 2025 follow-up).
- For agency/B2B service queries, answers come mostly from third parties: Clutch ~84.5% of review-site citations in ChatGPT (Hall, 456k citations); only ~5% of B2B citations from the brand's own site (Wellows). Reddit and LinkedIn in top cited domains (Semrush), though shares swing (ChatGPT cut Reddit from ~60% to ~10% of responses in Sept 2025).
- GEO paper (Princeton/IIT, KDD 2024): adding citations, quotations and statistics raised visibility up to ~40% on a test engine; keyword stuffing hurt.
- Freshness: AI-cited pages ~25.7% fresher than organic results (Ahrefs, 17M citations). Fake date bumps don't help.
- Answer placement: ~44% of ChatGPT citations come from the first 30% of a page (Kevin Indig analysis). Put the answer first.
- Overlap with Google top 10 for AI Overview citations: roughly 17–38% depending on study. Ranking helps but isn't required.
- No measurable effect: llms.txt (SE Ranking, ~300k domains; 97% of llms.txt files got zero requests per Ahrefs logs), schema coverage (Search Atlas).

## Diagnosing "why am I not cited?"
1. Is the page indexed in Google and Bing? (site: search, Search Console, Bing Webmaster Tools)
2. Are search/user bots allowed in robots.txt and not blocked by the host/CDN?
3. Is the answer in plain HTML near the top?
4. Does the page have something non-commodity (data, example, opinion) and sources?
5. Do independent sites mention the brand for this topic (directories, reviews, YouTube, LinkedIn, Reddit, lists)? This is usually the gap.
6. Run the prompt several times per engine; judge share of mentions, not one result.
