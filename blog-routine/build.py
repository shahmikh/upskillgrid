#!/usr/bin/env python3
"""Build upskillgrid.com.

Posts live in blog-routine/posts/<slug>.json. Every run rebuilds the whole site into public/:
home, blog index, static pages, every post, sitemap.xml and robots.txt.

Usage:  python3 blog-routine/build.py            (validate + build everything)
        python3 blog-routine/build.py --check    (validate posts only)

Exits non-zero when a post breaks a rule from blog-routine/seo (title/description length,
banned filler, dash characters, missing sections, broken internal links, unlinked sources).
"""
import datetime
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
POSTS = ROOT / "blog-routine" / "posts"
SITE = "https://upskillgrid.com"
BRAND = "UpskillGrid"
PERSON_ID = SITE + "/about#person"
ORG_ID = SITE + "/#org"
CONTACT_EMAIL = "hello@upskillgrid.com"
LINKEDIN = "https://www.linkedin.com/in/syed-shahmikh-ali-6b962b201/"
PERSONAL_SITE = "https://shahmikh.com"

CATEGORIES = [
    ("ai-tools", "AI Tools", "Honest looks at AI tools: what they do, what they cost and who they suit.", "ic-green", "AI"),
    ("how-to", "How-To Guides", "Step-by-step tech guides you can follow on your own laptop or phone.", "ic-indigo", "1-2"),
    ("free-courses", "Free Courses & Certificates", "Which courses and certificates are really free, and which only look free.", "ic-amber", "✓"),
    ("career-skills", "Career Skills", "Which skills and certifications are worth your time for a tech job.", "ic-rose", "↗"),
]
CAT = {c[0]: c for c in CATEGORIES}

BANNED = [
    r"in today'?s fast[- ]paced", r"in the digital age", r"\bunlock", r"\bunleash", r"\belevate",
    r"game[- ]changer", r"\bdive in", r"navigate the landscape", r"it'?s important to note",
    r"in conclusion", r"whether you'?re", r"look no further", r"\bseamless", r"\brobust",
    r"\bleverag", r"supercharge",
]


def esc(s):
    return html.escape(s, quote=True)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


# ---------------------------------------------------------------- layout

def header(active=""):
    def a(href, label, key):
        cls = ' class="is-active"' if key == active else ""
        return '<a href="%s"%s>%s</a>' % (href, cls, label)
    links = "".join([
        a("/", "Home", "home"),
        a("blog#ai-tools", "AI Tools", "ai-tools"),
        a("blog#how-to", "How-To", "how-to"),
        a("blog#free-courses", "Free Courses", "free-courses"),
        a("blog#career-skills", "Career Skills", "career-skills"),
        a("blog", "All Guides", "blog"),
        a("about", "About", "about"),
    ])
    return """<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container nav-row">
    <a href="/" class="brand"><img src="logo.svg" width="34" height="34" alt=""><span class="brand-text">Upskill<b>Grid</b></span></a>
    <nav class="nav-links" id="nav-links" aria-label="Primary">%s</nav>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu"><span></span></button>
  </div>
</header>
""" % links


FOOTER = """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div><h4>UpskillGrid</h4><p>Practical guides on AI tools, tech how-tos, free courses and career skills. Every guide is checked against official sources and dated.</p></div>
      <div><h4>Guides</h4><ul><li><a href="blog#ai-tools">AI Tools</a></li><li><a href="blog#how-to">How-To Guides</a></li><li><a href="blog#free-courses">Free Courses</a></li><li><a href="blog#career-skills">Career Skills</a></li></ul></div>
      <div><h4>Site</h4><ul><li><a href="about">About</a></li><li><a href="contact">Contact</a></li><li><a href="editorial-policy">Editorial policy</a></li></ul></div>
      <div><h4>Legal</h4><ul><li><a href="privacy">Privacy policy</a></li><li><a href="terms">Terms of use</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>&copy; {year} UpskillGrid. All rights reserved.</span><span>Run by <a href="about">Syed Shahmikh Ali</a></span></div>
  </div>
</footer>
<script src="main.js" defer></script>
""".replace("{year}", str(datetime.date.today().year))


def head(title, desc, path, og_type="website", extra="", ld=None, noindex=False):
    url = SITE + ("/" + path if path else "/")
    ld_html = ""
    if ld:
        ld_html = '<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(
            {"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False, indent=2)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<meta name="theme-color" content="#0F172A">
<link rel="icon" href="logo.svg" type="image/svg+xml">
<link rel="icon" href="favicon.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="canonical" href="{url}">
<link rel="preload" href="fonts/plus-jakarta-sans-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
<meta property="og:site_name" content="UpskillGrid">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}/og-image.png">
{extra}{ld}</head>
<body>
""".format(title=esc(title), desc=esc(desc), url=url, og_type=og_type, site=SITE, extra=extra, ld=ld_html,
           robots=robots)


def page(title, desc, path, body, active="", og_type="website", extra="", ld=None, noindex=False):
    return head(title, desc, path, og_type, extra, ld, noindex) + header(active) + '<main id="main">\n' + body + \
        "\n</main>\n" + FOOTER + "</body>\n</html>\n"


PERSON = {
    "@type": "Person", "@id": PERSON_ID, "name": "Syed Shahmikh Ali", "url": SITE + "/about",
    "image": SITE + "/headshot.jpg", "jobTitle": "Computer science tutor and founder of UpskillGrid",
    "sameAs": [LINKEDIN, PERSONAL_SITE],
    "knowsAbout": ["Artificial intelligence tools", "Python", "Java", "CompTIA Security+", "Cisco CCNA",
                   "Computer science education"],
}
ORG = {
    "@type": "Organization", "@id": ORG_ID, "name": BRAND, "url": SITE + "/", "logo": SITE + "/logo.png",
    "email": CONTACT_EMAIL, "founder": {"@id": PERSON_ID},
}

AUTHOR_BOX = """<aside class="author-box">
  <img src="headshot.jpg" alt="Syed Shahmikh Ali" width="72" height="72" loading="lazy">
  <div>
    <p class="author-name">About the author</p>
    <p><a href="about">Syed Shahmikh Ali</a> is a Preply Super Tutor, in the top 15% of computer science tutors on Preply, with a mechatronics engineering background. He teaches Python, Java, AP and IB computer science, Security+ and CCNA one to one, and started UpskillGrid to give learners straight answers about AI tools and free courses.</p>
    <p class="post-note">Editorial note: this guide is checked against the sources listed above. Prices and course terms change, so confirm on the official page before you pay. Spot a mistake? Tell us through the <a href="contact">contact page</a> and we will fix it.</p>
  </div>
</aside>"""


# ---------------------------------------------------------------- posts

def load(slug):
    return json.loads((POSTS / (slug + ".json")).read_text(encoding="utf-8"))


def all_posts():
    return sorted((load(p.stem) for p in POSTS.glob("*.json")), key=lambda x: (x["published"], x["slug"]),
                  reverse=True)


STATIC_PAGES = ["about", "contact", "privacy", "terms", "editorial-policy", "blog"]


def target_exists(href, slugs):
    f = href.split("#")[0]
    if f in ("", "/"):
        return True
    if f in STATIC_PAGES:
        return True
    if f.startswith("blog-") and f[5:] in slugs:
        return True
    return (PUB / f).exists()


def validate(p, slugs):
    errs, warns = [], []
    for key in ["slug", "title", "h1", "description", "category", "published", "modified", "read_min",
                "card_summary", "lead", "takeaways", "sections", "faq", "sources", "related"]:
        if key not in p:
            errs.append("missing field: " + key)
    if errs:
        return errs, warns, 0
    if p["category"] not in CAT:
        errs.append("unknown category: " + p["category"])
    if len(p["title"]) > 60:
        errs.append("title is %d chars (max 60)" % len(p["title"]))
    if not 140 <= len(p["description"]) <= 160:
        errs.append("description is %d chars (need 140-160)" % len(p["description"]))
    if not 3 <= len(p["takeaways"]) <= 5:
        errs.append("need 3-5 takeaways")
    if len(p["sections"]) < 4:
        errs.append("need at least 4 sections")
    if len(p["faq"]) != 3:
        errs.append("need exactly 3 FAQ items")
    if not 2 <= len(p["sources"]) <= 6:
        errs.append("need 2-6 sources")
    if len(p["related"]) < 2:
        errs.append("need at least 2 related links")
    body = " ".join([p["lead"]] + p["takeaways"] + [s["h2"] + " " + s["html"] for s in p["sections"]]
                    + [f["q"] + " " + f["a"] for f in p["faq"]])
    text = plain(body)
    for pat in BANNED:
        m = re.search(pat, text + " " + p["title"] + " " + p["description"], re.I)
        if m:
            errs.append("banned filler phrase: %r" % m.group(0))
    if re.search("[—–]", text + p["title"] + p["description"]):
        errs.append("dash characters found; use commas or periods")
    words = len(text.split())
    if words < 700:
        warns.append("only %d words" % words)
    if words > 2400:
        warns.append("%d words is long; check for padding" % words)
    for s in p["sources"]:
        if not s["url"].startswith("https://"):
            errs.append("source is not https: " + s["url"])
        if s["url"] not in body:
            errs.append("source not linked inline in the article: " + s["url"])
    for m in re.finditer(r'href="([^"]+)"', body):
        h = m.group(1)
        if h.startswith(("http", "#", "mailto:")):
            continue
        if not target_exists(h, slugs):
            errs.append("internal link target missing: " + h)
    for r in p["related"]:
        if not target_exists(r["href"], slugs):
            errs.append("related link target missing: " + r["href"])
    ids = [s["id"] for s in p["sections"]]
    if len(ids) != len(set(ids)):
        errs.append("duplicate section ids")
    return errs, warns, words


def render_post(p):
    slug = p["slug"]
    path = "blog-" + slug
    url = SITE + "/" + path
    cat = CAT[p["category"]]
    toc = "".join('<li><a href="#%s">%s</a></li>' % (s["id"], esc(s["h2"])) for s in p["sections"])
    toc += '<li><a href="#faq">Frequently asked questions</a></li><li><a href="#sources">Sources</a></li>'
    sections = "".join('\n    <h2 id="%s">%s</h2>\n    %s\n' % (s["id"], esc(s["h2"]), s["html"]) for s in p["sections"])
    faq = "".join('\n      <details class="faq-item"><summary>%s</summary><p>%s</p></details>' % (esc(f["q"]), f["a"])
                  for f in p["faq"])
    sources = "".join('<li><a href="%s" rel="noopener">%s</a></li>' % (esc(s["url"]), esc(s["title"])) for s in p["sources"])
    related = "".join('<li><a href="%s">%s</a></li>' % (esc(r["href"]), esc(r["title"])) for r in p["related"])
    takeaways = "".join("<li>%s</li>" % t for t in p["takeaways"])
    ld = [
        PERSON, ORG,
        {"@type": "BlogPosting", "headline": p["title"], "description": p["description"],
         "image": [SITE + "/og-image.png"], "datePublished": p["published"], "dateModified": p["modified"],
         "author": {"@id": PERSON_ID}, "publisher": {"@id": ORG_ID}, "inLanguage": "en",
         "articleSection": cat[1], "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "citation": [s["url"] for s in p["sources"]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE + "/blog"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f["q"],
                                             "acceptedAnswer": {"@type": "Answer", "text": plain(f["a"])}} for f in p["faq"]]},
    ]
    extra = '<meta property="article:published_time" content="%s">\n<meta property="article:modified_time" content="%s">\n' % (
        p["published"], p["modified"])
    body = """<section class="page-hero">
  <div class="container">
    <p class="crumbs"><a href="/">Home</a> / <a href="blog#{catid}">{catname}</a></p>
    <p class="eyebrow">{catname} · {mins} min read</p>
    <h1>{h1}</h1>
    <p class="post-byline">By <a href="about">Syed Shahmikh Ali</a> · Published {pubh} · Updated {modh}</p>
  </div>
</section>
<article class="container">
  <div class="prose">
    <p class="post-lead">{lead}</p>
    <div class="takeaways"><h2>Key takeaways</h2><ul>{takeaways}</ul></div>
    <nav class="toc" aria-label="Contents"><p class="toc-title">In this guide</p><ol>{toc}</ol></nav>
{sections}
    <h2 id="faq">Frequently asked questions</h2>
    <div class="faq-list">{faq}
    </div>
    <h2 id="sources">Sources</h2>
    <ul class="post-sources">{sources}</ul>
    <h2>Related reading</h2>
    <ul class="post-sources">{related}</ul>
    {author}
  </div>
</article>
<section class="cta-band">
  <div class="container">
    <p class="eyebrow">Keep going</p>
    <h2>More free, checked guides on AI tools and tech skills</h2>
    <a href="blog" class="btn btn--green">Browse all guides</a>
  </div>
</section>""".format(catid=cat[0], catname=esc(cat[1]), mins=p["read_min"], h1=esc(p["h1"]),
                     pubh=human_date(p["published"]), modh=human_date(p["modified"]), lead=p["lead"],
                     takeaways=takeaways, toc=toc, sections=sections, faq=faq, sources=sources, related=related,
                     author=AUTHOR_BOX)
    return page(p["title"], p["description"], path, body, active=p["category"], og_type="article", extra=extra, ld=ld)


def human_date(iso):
    d = datetime.date.fromisoformat(iso[:10])
    return d.strftime("%-d %B %Y")


def card(p):
    cat = CAT[p["category"]]
    return """<a href="blog-{slug}" class="card"><span class="pill">{cat}</span><h3>{h1}</h3><p>{summary}</p><span class="meta">{mins} min read · {date}</span></a>""".format(
        slug=p["slug"], cat=esc(cat[1]), h1=esc(p["h1"]), summary=esc(p["card_summary"]), mins=p["read_min"],
        date=human_date(p["modified"]))


# ---------------------------------------------------------------- static pages

def build_home(posts):
    tiles = "".join("""<a class="tile" href="blog#{id}"><div class="tile-icon {ic}">{icon}</div><h3>{name}</h3><p>{blurb}</p></a>""".format(
        id=c[0], name=esc(c[1]), blurb=esc(c[2]), ic=c[3], icon=c[4]) for c in CATEGORIES)
    latest = "".join(card(p) for p in posts[:6]) or '<p class="empty-note">The first guides are on their way.</p>'
    body = """<section class="hero">
  <div class="container">
    <p class="eyebrow">AI tools · How-tos · Free courses</p>
    <h1>Learn the tech skills that matter, <em>without paying for hype</em></h1>
    <p class="lead">Plain-English guides to AI tools, step-by-step tech how-tos, and free courses and certificates. We check every claim against the official source and tell you what is really free.</p>
    <div class="hero-actions"><a class="btn btn--green" href="blog">Read the guides</a><a class="btn btn--ghost" href="about">Who writes this</a></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head"><p class="eyebrow">What we cover</p><h2>Four topics, one goal: useful skills</h2></div>
    <div class="tiles">{tiles}</div>
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <div class="section-head"><p class="eyebrow">Latest guides</p><h2>New on UpskillGrid</h2></div>
    <div class="cards">{latest}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head"><p class="eyebrow">How we work</p><h2>Checked, dated and honest about cost</h2>
    <p>Each guide links to the official pages it relies on, shows when it was last updated, and separates “free to learn” from “free certificate”. If something costs money, we say so up front. Read our <a href="editorial-policy">editorial policy</a>.</p></div>
  </div>
</section>""".format(tiles=tiles, latest=latest)
    ld = [ORG, PERSON, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND,
                        "publisher": {"@id": ORG_ID}, "inLanguage": "en"}]
    return page("UpskillGrid: AI Tools, Tech How-Tos and Free Courses",
                "Plain-English guides to AI tools, tech how-tos and free courses with certificates. Every guide is checked against official sources and says what is really free.",
                "", body, active="home", ld=ld)


def build_blog(posts):
    blocks = []
    for c in CATEGORIES:
        items = [p for p in posts if p["category"] == c[0]]
        inner = "".join(card(p) for p in items) if items else '<p class="empty-note">First guides in this topic are coming soon.</p>'
        blocks.append("""<div class="cat-block" id="{id}"><h2><span class="tile-icon {ic}" style="width:36px;height:36px;font-size:.9rem;display:inline-grid;place-items:center;border-radius:10px">{icon}</span>{name}</h2><p>{blurb}</p><div class="cards">{inner}</div></div>""".format(
            id=c[0], name=esc(c[1]), blurb=esc(c[2]), ic=c[3], icon=c[4], inner=inner))
    body = """<section class="page-hero"><div class="container"><p class="eyebrow">All guides</p><h1>Guides on AI tools, tech skills and free courses</h1><p>Every guide answers one question properly, links to its sources and shows when it was last checked.</p></div></section>
<section class="section"><div class="container">%s</div></section>""" % "".join(blocks)
    ld = [ORG, {"@type": "CollectionPage", "name": "UpskillGrid guides", "url": SITE + "/blog",
                "mainEntity": {"@type": "ItemList", "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "url": SITE + "/blog-" + p["slug"]} for i, p in enumerate(posts)]}}]
    return page("All Guides: AI Tools, How-Tos and Free Courses",
                "Browse every UpskillGrid guide on AI tools, tech how-tos, free courses with certificates and career skills, each checked against official sources.",
                "blog", body, active="blog", ld=ld)


def simple(title, desc, path, h1, intro, inner, ld=None, eyebrow=""):
    eb = '<p class="eyebrow">%s</p>' % eyebrow if eyebrow else ""
    body = """<section class="page-hero"><div class="container">%s<h1>%s</h1><p>%s</p></div></section>
<div class="container"><div class="prose">%s</div></div>""" % (eb, esc(h1), intro, inner)
    return page(title, desc, path, body, active=path, ld=ld)


def build_about():
    inner = """<img src="headshot.jpg" alt="Syed Shahmikh Ali" width="160" height="160" style="border-radius:50%;margin-bottom:20px">
<h2>Who runs UpskillGrid</h2>
<p>UpskillGrid is run by <strong>Syed Shahmikh Ali</strong>. I studied mechatronics engineering and now teach computer science and IT one to one. On Preply I am a Super Tutor and in the top 15% of computer science tutors. I teach Python, Java, AP and IB computer science, CompTIA Security+ and Cisco CCNA.</p>
<p>Students ask me the same questions every week: which AI tool should I use, is this course really free, will this certificate help me get a job. UpskillGrid is where I answer those questions properly, once, with sources.</p>
<h2>What you will find here</h2>
<ul>
<li><strong>AI tools:</strong> what a tool does, what it costs and who it suits.</li>
<li><strong>How-to guides:</strong> numbered steps you can follow.</li>
<li><strong>Free courses and certificates:</strong> what is free to learn, what has a free certificate, and what needs payment.</li>
<li><strong>Career skills:</strong> which skills and certifications are worth the time.</li>
</ul>
<h2>How guides are made</h2>
<p>Every guide links to the official pages it relies on, and shows a published and updated date. Prices, free trials and course rules change often, so always confirm on the official page before you pay. Our full approach is in the <a href="editorial-policy">editorial policy</a>.</p>
<h2>Elsewhere</h2>
<ul><li><a href="https://shahmikh.com" rel="noopener">shahmikh.com</a>, my tutoring site</li><li><a href="{LI}" rel="noopener">LinkedIn</a></li></ul>
<p>Questions or corrections: <a href="contact">contact page</a>.</p>""".replace("{LI}", LINKEDIN)
    ld = [PERSON, ORG, {"@type": "ProfilePage", "url": SITE + "/about", "mainEntity": {"@id": PERSON_ID}}]
    return simple("About UpskillGrid and Syed Shahmikh Ali",
                  "UpskillGrid is run by Syed Shahmikh Ali, a Preply Super Tutor who teaches computer science and IT. Learn who writes the guides and how they are checked.",
                  "about", "About UpskillGrid", "Who writes these guides, and how they are checked.", inner, ld, "About")


def build_contact():
    inner = """<h2>Email</h2>
<p>The fastest way to reach us is email: <a href="mailto:{e}">{e}</a>. We read every message and usually reply within two working days.</p>
<h2>What to write to us about</h2>
<ul>
<li><strong>Corrections:</strong> if a price, link or course rule in a guide is wrong or out of date, send the page link and what changed. We fix confirmed errors and update the date on the page.</li>
<li><strong>Guide requests:</strong> tell us which AI tool, course or skill you want explained.</li>
<li><strong>Everything else:</strong> partnerships and general questions.</li>
</ul>
<p>We do not accept payment to change what a guide says about a product.</p>""".format(e=CONTACT_EMAIL)
    return simple("Contact UpskillGrid",
                  "Contact UpskillGrid by email to report a correction, request a guide on an AI tool or free course, or ask a general question. We reply within two working days.",
                  "contact", "Contact us", "Corrections, guide requests and questions are all welcome.", inner, [ORG], "Contact")


def build_editorial():
    inner = """<h2>Our standards</h2>
<ul>
<li><strong>Sources first.</strong> Facts about prices, free trials, certificates and course rules come from the official page of the company or university. Each guide lists its sources and links them where the claim is made.</li>
<li><strong>Dated.</strong> Every guide shows when it was published and when it was last updated. We only change the updated date when the content really changes.</li>
<li><strong>Clear about cost.</strong> We separate “free to learn”, “free badge”, “free certificate” and “paid”. If we could not confirm whether something is free, we say so or leave it out.</li>
<li><strong>No invented numbers.</strong> We do not make up statistics, reviews or success stories. Example numbers are labelled as examples.</li>
<li><strong>Independent.</strong> No company pays to appear in a guide or to change what we say. If we ever use affiliate links, the guide will say so clearly.</li>
</ul>
<h2>Corrections</h2>
<p>Found something wrong? Send the page link to <a href="mailto:{e}">{e}</a>. We check it against the official source and update the guide if it needs fixing.</p>
<h2>Advertising</h2>
<p>UpskillGrid may show ads, for example through Google AdSense, to keep the guides free. Ads are kept separate from guide content and never decide what we recommend.</p>""".format(e=CONTACT_EMAIL)
    return simple("Editorial Policy: How UpskillGrid Guides Are Made",
                  "How UpskillGrid researches, checks, dates and corrects its guides on AI tools and free courses, and how we keep advertising separate from what we recommend.",
                  "editorial-policy", "Editorial policy", "How guides are researched, checked and corrected.", inner, [ORG], "Standards")


def build_privacy():
    today = human_date(datetime.date.today().isoformat())
    inner = """<p><em>Last updated: {d}</em></p>
<p>This policy explains what information upskillgrid.com (“UpskillGrid”, “we”) collects and how it is used. If you have questions, email <a href="mailto:{e}">{e}</a>.</p>
<h2>Information we collect</h2>
<ul>
<li><strong>Email you send us.</strong> If you email us, we receive your email address and message and use them only to reply.</li>
<li><strong>Server and security logs.</strong> The site is hosted on Cloudflare. Like most hosts, Cloudflare processes technical data such as IP address, browser type and pages requested to deliver and protect the site.</li>
</ul>
<p>We do not ask you to create an account and we do not sell personal information.</p>
<h2>Cookies and advertising</h2>
<p>We may use Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on a user’s prior visits to this website or other websites. Google’s use of advertising cookies enables it and its partners to serve ads to you based on your visit to this site and/or other sites on the Internet.</p>
<p>You can opt out of personalized advertising by visiting Google’s <a href="https://adssettings.google.com" rel="noopener">Ads Settings</a>. You can also opt out of some third-party vendors’ use of cookies for personalized advertising at <a href="https://www.aboutads.info/choices/" rel="noopener">aboutads.info</a>. To learn how Google uses information from sites that use its services, see <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">How Google uses information from sites or apps that use our services</a>.</p>
<p>Where the law requires it, for example in the EEA and the UK, you will be asked for consent before personalized ads or non-essential cookies are used.</p>
<h2>Analytics</h2>
<p>If we add analytics to measure which guides are useful, we will update this page to name the tool and what it collects.</p>
<h2>Links to other sites</h2>
<p>Guides link to official course and product pages. Those sites have their own privacy policies, which we do not control.</p>
<h2>Children</h2>
<p>This site is meant for a general audience and is not directed at children under 13. We do not knowingly collect personal information from children.</p>
<h2>Your choices and rights</h2>
<p>You can ask us to delete any email correspondence with you. Depending on where you live, you may have other rights over your personal data. Contact us to use them.</p>
<h2>Changes</h2>
<p>We will post any changes to this policy on this page and update the date at the top.</p>""".format(d=today, e=CONTACT_EMAIL)
    return simple("Privacy Policy | UpskillGrid",
                  "Read how UpskillGrid handles your data, including emails you send us, hosting logs, and cookies used by Google AdSense, plus how to opt out of personalized ads.",
                  "privacy", "Privacy policy", "What we collect, why, and the choices you have.", inner, [ORG])


def build_terms():
    today = human_date(datetime.date.today().isoformat())
    inner = """<p><em>Last updated: {d}</em></p>
<h2>Using this site</h2>
<p>UpskillGrid provides general information about AI tools, technology skills, online courses and certificates. By using the site you agree to these terms.</p>
<h2>No guarantees</h2>
<p>We check guides against official sources, but prices, free trials, course content and certificate rules are set by other companies and change often. Always confirm details on the official page before you sign up or pay. Information here is not professional, legal or financial advice.</p>
<h2>Third-party links</h2>
<p>We link to other websites for reference. We are not responsible for their content, prices or policies.</p>
<h2>Content</h2>
<p>Guides and images on this site belong to UpskillGrid unless stated otherwise. You may link to any page and quote short parts with a link back. Please do not copy whole guides.</p>
<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:{e}">{e}</a>.</p>""".format(d=today, e=CONTACT_EMAIL)
    return simple("Terms of Use | UpskillGrid",
                  "The terms for using UpskillGrid: guides are general information, course prices and rules change, so confirm details on official pages before you pay.",
                  "terms", "Terms of use", "The short version: guides are general information, so check official pages before you pay.", inner, [ORG])


def build_404():
    body = """<section class="page-hero"><div class="container"><p class="eyebrow">Error 404</p><h1>That page is not here</h1><p>The link may be old or mistyped. Try the guides instead.</p><a class="btn btn--primary" href="/blog">Browse all guides</a></div></section>"""
    return page("Page not found | UpskillGrid",
                "The page you were looking for does not exist on UpskillGrid. Browse our guides on AI tools, tech how-tos, free courses and career skills instead of this missing one.",
                "404", body, noindex=True)


# ---------------------------------------------------------------- outputs

def clean_links(s):
    s = re.sub(r'href="index\.html((?:#[^"]*)?)"', lambda m: 'href="/%s"' % m.group(1), s)
    return re.sub(r'href="(?!https?:|mailto:|#|/)([^"#?]+)\.html((?:[#?][^"]*)?)"', r'href="\1\2"', s)


def write(name, s):
    (PUB / name).write_text(clean_links(s), encoding="utf-8")


def build_sitemap(posts):
    today = datetime.date.today().isoformat()
    newest = max([p["modified"][:10] for p in posts], default=today)
    urls = [("", newest), ("blog", newest), ("about", None), ("contact", None), ("editorial-policy", None),
            ("privacy", None), ("terms", None)]
    urls += [("blog-" + p["slug"], p["modified"][:10]) for p in posts]
    lm_file = ROOT / "blog-routine" / "static_lastmod.json"
    static_lm = json.loads(lm_file.read_text()) if lm_file.exists() else {}
    rows = []
    for path, lm in urls:
        lm = lm or static_lm.setdefault(path or "home", today)
        loc = SITE + ("/" + path if path else "/")
        rows.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (loc, lm))
    lm_file.write_text(json.dumps(static_lm, indent=2) + "\n")
    (PUB / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "\n".join(rows) + "\n</urlset>\n", encoding="utf-8")


ROBOTS = """# Search engines and AI search/user agents are welcome.
User-agent: *
Allow: /

Sitemap: https://upskillgrid.com/sitemap.xml
"""


def main():
    check_only = "--check" in sys.argv
    posts = all_posts()
    slugs = {p["slug"] for p in posts}
    failed = False
    for p in posts:
        errs, warns, words = validate(p, slugs)
        for w in warns:
            print("[warn] %s: %s" % (p["slug"], w))
        for e in errs:
            print("[ERROR] %s: %s" % (p.get("slug", "?"), e))
        if errs:
            failed = True
        else:
            print("[ok] %s: %d words" % (p["slug"], words))
    if failed:
        sys.exit(1)
    if check_only:
        return
    for p in posts:
        write("blog-%s.html" % p["slug"], render_post(p))
    write("index.html", build_home(posts))
    write("blog.html", build_blog(posts))
    write("about.html", build_about())
    write("contact.html", build_contact())
    write("editorial-policy.html", build_editorial())
    write("privacy.html", build_privacy())
    write("terms.html", build_terms())
    write("404.html", build_404())
    build_sitemap(posts)
    (PUB / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    print("[ok] site built: %d posts, sitemap and robots.txt written" % len(posts))


if __name__ == "__main__":
    main()
