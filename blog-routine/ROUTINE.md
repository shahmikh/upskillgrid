# Blog routine for upskillgrid.com

One run = one new article. Quality over volume: about 2 strong articles a week is the target.
Follow the SEO skill in `blog-routine/seo/` every time.

## Steps

1. **Get the repo.** Clone `shahmikh/upskillgrid` (or `git pull --ff-only origin main`).
2. **Read the rules.** `blog-routine/seo/SKILL.md`, `references/content-playbook.md`, `references/technical-schema.md`, and `blog-routine/topics.md`.
3. **Pick the topic.** First unused topic in the backlog that does not overlap an existing post. If fewer than 4 remain, add 6 new ones across the four categories: `ai-tools`, `how-to`, `free-courses`, `career-skills`.
4. **Research with real sources.** Official pages first (the company, university or platform). Use only URLs you actually fetched this run. Check every price, trial length, pass mark and date against the page. If a fact cannot be verified, leave it out.
5. **Non-commodity angle.** A comparison table, a decision framework, tested steps, or a clear opinion with the reason. Label example numbers as examples.
6. **Write the post** as `blog-routine/posts/<slug>.json`, copying the shape of an existing file. Rules:
   - Title at most 60 characters. Description 140 to 160 characters. Category is one of the four above.
   - Lead answers the question in the first 2 sentences. 3 to 5 takeaways. Question-style H2s that open with a direct answer. Exactly 3 FAQ items. 2 to 6 sources, each also linked inline.
   - 900 to 1,800 words. Never pad.
   - No invented statistics, studies, quotes, reviews or success stories. No first-person anecdotes that are not plainly true.
   - Confirmed author facts only: Preply Super Tutor, top 15% of computer science tutors on Preply, mechatronics engineering background, teaches Python, Java, AP/IB CS, Security+ and CCNA.
   - No banned filler (see build.py), no em or en dashes, US English.
   - At least 2 related links (other posts or `blog#<category>`). Add one link to the new post from an older relevant post.
7. **Build.** `python3 blog-routine/build.py`. Fix every `[ERROR]` and rerun.
8. **Check.** Copy `public/` to a temp folder, create extensionless copies of each `.html` file, point the temp `sitemap.xml` at `.html` files, then run `NODE_PATH=$(npm root -g) node blog-routine/seo/scripts/site_check.js <temp> https://upskillgrid.com`. No issues allowed on the new page.
9. **Publish.** Move the topic to "Published" in `topics.md` with date and slug. Commit, push to `main`. Cloudflare redeploys in about a minute.
10. **Report.** Send the owner the title and URL (`https://upskillgrid.com/blog-<slug>`).

## Guardrails
- If validation fails after 3 honest attempts or a key fact cannot be verified, do not publish. Note it under "Skipped" and tell the owner.
- Do not add AdSense code or ads.txt until the owner has an approved AdSense publisher ID.
- Never edit `wrangler.jsonc`.
