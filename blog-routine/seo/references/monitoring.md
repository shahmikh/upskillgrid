# Monitoring search and AI-search changes

Check weekly (automate where possible). Confirm industry reports against an official source before acting.

## Official sources
| Source | URL / feed | Cadence |
|---|---|---|
| Google Search Status Dashboard (core/spam updates, incidents) | status.search.google.com; Atom: status.search.google.com/en/feed.atom | Daily–weekly |
| Google Search Central Blog | developers.google.com/search/blog (feed likely /search/blog/feed.xml) | Weekly |
| Google docs updates (deprecations like FAQ rich results) | developers.google.com/search/updates | Weekly |
| Google generative AI guide / AI features page | developers.google.com/search/docs/fundamentals/ai-optimization-guide; /search/docs/appearance/ai-features | Monthly |
| Google crawlers | developers.google.com/crawling | Monthly |
| Search Off the Record podcast | developers.google.com/search/podcasts/search-off-the-record | Weekly |
| Google Search Central on X | @googlesearchc (Search Liaison inactive since Aug 2025) | Weekly |
| Bing Webmaster Blog | blogs.bing.com/webmaster (feed /webmaster/feed) | Weekly |
| OpenAI bots | developers.openai.com/api/docs/bots; IP JSONs openai.com/gptbot.json, searchbot.json, chatgpt-user.json | Weekly diff |
| Anthropic crawlers | support.claude.com/en/articles/8896518 | Weekly diff |
| Perplexity crawlers | docs.perplexity.ai/docs/resources/perplexity-crawlers | Weekly diff |
| Apple Applebot | support.apple.com/en-us/119829 | Monthly |
| ChatGPT release notes | help.openai.com/en/articles/6825453 | Monthly |

## Industry (early signals)
- Search Engine Roundtable (seroundtable.com/index.rdf), Search Engine Land (searchengineland.com/feed), Search Engine Journal (searchenginejournal.com/feed/).
- Volatility trackers (Semrush Sensor, MozCast, Algoroo): spikes are unconfirmed until the Status Dashboard confirms.

## Routine
1. Weekly: scan the sources above for the last 7 days (feeds or web search). Note anything affecting structured data, crawlers/user agents, spam policies, Search Console/Bing features, or AI features.
2. Act only on changes relevant to the site: update templates/schema, robots.txt for new bot names, writing rules for policy changes. During a core update, pause big changes.
3. Log each check with date, source URL and action in a changelog file; summarize in 3–5 lines.
4. Monthly: Search Console (branded split, AI reports), Bing AI Performance, prompt panel, robots.txt vs current AI user agents.
5. Quarterly: confirm all monitored URLs still resolve (several moved in 2025–26), check bot directories (e.g. Dark Visitors) for new AI agents, re-check IndexNow participants.

Sandboxed agents often can't fetch these sites directly; use web search results pointing to the official pages, and say when something couldn't be verified.
