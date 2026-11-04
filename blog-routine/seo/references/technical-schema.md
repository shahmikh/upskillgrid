# Technical SEO and structured data

## Crawl and index
- **robots.txt**: allow Googlebot, Bingbot, Applebot and AI search/user bots (OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User). Training bots (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot, Meta-ExternalAgent) are a business decision; blocking them doesn't hurt search visibility. Include `Sitemap:`.
- **XML sitemap**: every indexable URL, accurate `<lastmod>` only for meaningful content changes (Google and Bing ignore untrustworthy lastmod; Bing uses it to schedule AI-search recrawls). No noindex/redirected URLs.
- **IndexNow**: key file at the root, POST changed URLs to api.indexnow.org after each publish (Bing, Yandex, Seznam, Naver). Automate it (CI job on push) where possible.
- **Canonical**: self-referencing absolute canonical on every page; consistent trailing slashes; one version of the domain (https, www or not) with 301 redirects.
- **Rendering**: main content, links, prices and stats in the initial HTML (most AI crawlers don't run JS). Animated counters should already show the real value in HTML.
- **404** page returns a 404 status and is noindex; no soft 404s.
- **Search Console + Bing Webmaster Tools** both verified; sitemap submitted to both. "Request indexing" for key new pages (limited quota). The Google Indexing API is only for job postings and livestreams; don't use it for normal pages.
- Search Console "Alternate page with proper canonical tag" and "Page with redirect" are normal when canonicals/redirects are correct.

## Page-level tags
- `<title>` ≤60 chars; meta description 140–160 chars; one H1; `lang` attribute; mobile viewport.
- Open Graph (og:title, og:description, og:image 1200x630, og:url, og:type) and `twitter:card` summary_large_image with image. Per-page share images improve social click-through.
- Articles: `article:published_time` and `article:modified_time`.

## Structured data (JSON-LD, must match visible content)
Worth doing:
- **Organization / ProfessionalService** on the home page: name, url, logo (real image file), image, description, contactPoint, areaServed, `sameAs` (LinkedIn, YouTube, directory profiles once live), `founder` → Person.
- **WebSite** on the home page.
- **Person** with stable `@id`, jobTitle, image, sameAs, knowsAbout; **ProfilePage** on the About page.
- **Article/BlogPosting**: headline, description, image, datePublished, dateModified (real), author (Person with url to About), publisher, mainEntityOfPage, optional `citation` array of source URLs.
- **BreadcrumbList** on inner pages.
- **Service** on service pages (provider, areaServed, serviceType; add offers/price ranges only if real and shown).
- **VideoObject** for embedded videos: name, description, thumbnailUrl, uploadDate in full ISO 8601 with timezone (e.g. 2026-09-29T09:00:00+00:00), contentUrl/embedUrl.
- **FAQPage**: optional, harmless, no rich results since May 2026.
- **CollectionPage/ItemList** for hubs and case-study lists.
Avoid: self-serving Review/AggregateRating for your own business (no stars, policy risk), markup for content not on the page, LocalBusiness with a virtual address.

Validate: parse every JSON-LD block; use Google's Rich Results Test / Schema Markup Validator when online.

## Performance (page experience)
- Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1 (measure with PageSpeed Insights / CrUX, not guesses).
- Load heavy scripts (3D, demos, chat widgets) after the page is interactive; lazy-load below-the-fold images with width/height set; WebP/AVIF images; preconnect fonts and avoid render-blocking font CSS; don't load the same analytics twice (gtag + GTM both firing GA4 double-counts).
- Mobile: no horizontal scroll at 390px wide; tap targets large enough; tables wrap.

## Policy-sensitive technical items
- No cloaking, hidden text, sneaky redirects, back-button hijacking, doorway/city pages, or intrusive interstitials.

## Bundled check script
`scripts/site_check.js` loads every URL in sitemap.xml from a local checkout in headless Chromium (iPhone 13 viewport) and reports horizontal scroll, title/description length, H1 count, JSON-LD validity, broken internal links and JS errors:
`NODE_PATH=$(npm root -g) node scripts/site_check.js /path/to/site https://example.com`
