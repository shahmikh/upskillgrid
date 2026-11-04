# upskillgrid.com

Static site for upskillgrid.com (AI tools, tech how-tos, free courses and career skills), deployed to Cloudflare Workers (static assets).

Owner: Syed Shahmikh Ali

- `public/` is the website Cloudflare serves. It is generated, so edit posts and `blog-routine/build.py`, not the HTML.
- `blog-routine/posts/*.json` holds each article.
- `python3 blog-routine/build.py` validates every post against the SEO rules and rebuilds all pages, the sitemap and robots.txt.
- `blog-routine/ROUTINE.md` is the step-by-step for publishing a new article.
- `wrangler.jsonc` tells Cloudflare what to publish.
