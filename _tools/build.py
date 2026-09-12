"""Generate every page of the site from shared templates + content.py.

Run:  python _tools/build.py
Output: HTML at the repo root plus assets/search-index.json

The five main pages keep their hand-tuned markup, stored in _partials/; this script
only wraps them in the shared header/footer so the chrome never drifts between pages.
"""
import datetime
import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PARTIALS = os.path.join(ROOT, "_partials")
SITE_URL = (f"https://{C.CUSTOM_DOMAIN}/" if C.CUSTOM_DOMAIN
            else "https://antonysa23-meet.github.io/beyond-the-net/")
# Every <title> ends with this, so each page carries the name people search for
BRAND = "Beyond the Net Houston"
TAGLINE = ("Beyond the Net Houston (HTX) is a youth volleyball mentorship nonprofit founded by "
           "Carlos Cruz and Arman Najari of Rice University.")

SEARCH_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path></svg>'
)
INSTAGRAM_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
    '<rect x="3" y="3" width="18" height="18" rx="5"></rect>'
    '<circle cx="12" cy="12" r="4"></circle>'
    '<circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"></circle></svg>'
)

NAV = [
    ("index.html", "Home"),
    ("programs-and-services.html", "Programs &amp; Services"),
    ("about.html", "About"),
    ("get-involved.html", "Get Involved"),
]
MORE = [
    ("events.html", "Events"),
]
if C.SHOW_BLOG:
    MORE.append(("blog/", "Blog"))
if C.SHOW_SERVICES:
    MORE.append(("book-online/", "Book Online"))
FOOTER_NAV = [
    ("programs-and-services.html", "Programs &amp; Services"),
    ("about.html", "About"),
    ("events.html", "Events"),
    ("get-involved.html", "Reach Out"),
]


def esc(s):
    return html.escape(s, quote=True)


def header(p, active):
    def item(href, label, in_more=False):
        cur = ' aria-current="page"' if href == active else ""
        return f'<li><a href="{p}{href}"{cur}>{label}</a></li>'

    main_items = "\n        ".join(item(h, l) for h, l in NAV)
    more_items = "\n            ".join(item(h, l) for h, l in MORE)
    return f"""<header class="site-header">
  <div class="site-header__inner">
    <a class="brand" href="{p}index.html">
      <span class="brand__name">Beyond the Net</span>
      <span class="brand__city">Houston</span>
    </a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">
      <span></span><span></span><span></span>
      <span class="visually-hidden">Menu</span>
    </button>

    <nav class="nav" id="primary-nav" aria-label="Main">
      <ul class="nav__list">
        {main_items}
        <li class="nav__more">
          <button class="nav__more-btn" type="button" aria-expanded="false" aria-controls="more-menu">
            More <span class="nav__caret" aria-hidden="true"></span>
          </button>
          <ul class="nav__submenu" id="more-menu">
            {more_items}
          </ul>
        </li>
      </ul>
      <button class="nav__search" type="button" aria-label="Search" data-search-open>
        {SEARCH_ICON}
      </button>
    </nav>
  </div>
</header>

<div class="search-panel" id="search-panel" hidden>
  <div class="search-panel__bar">
    <label class="visually-hidden" for="search-input">Search</label>
    <div class="search-panel__field">
      {SEARCH_ICON}
      <input id="search-input" type="search" placeholder="Search" autocomplete="off">
    </div>
    <button class="search-panel__close" type="button" data-search-close>Close</button>
  </div>
  <div class="search-panel__results" id="search-results" aria-live="polite"></div>
</div>"""


def footer(p):
    links = "\n        ".join(f'<li><a href="{p}{h}">{l}</a></li>' for h, l in FOOTER_NAV)
    return f"""<footer class="site-footer">
  <div class="site-footer__inner">
    <div>
      <a class="brand" href="{p}index.html">
        <span class="brand__name">Beyond the Net</span>
        <span class="brand__city">Houston</span>
      </a>
      <p class="footer__about">{esc(TAGLINE)}</p>
      <p class="footer__contact">
        Want to bring us to your school or have general inquiries? Email us:<br>
        <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>
      </p>
      <a class="footer__social" href="{C.INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">
        {INSTAGRAM_ICON}
      </a>
    </div>

    <nav class="footer__nav" aria-label="Footer">
      <ul>
        {links}
      </ul>
    </nav>
  </div>

  <div class="site-footer__credit">
    <p>Developed by <a href="mailto:antony.saleh2017@gmail.com">Antony Saleh</a></p>
  </div>
</footer>"""


def last_modified(path):
    """Date this page last changed, for <lastmod>. Taken from git so it stays stable
    between rebuilds; a rebuild that changes nothing must not bump every date."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                             cwd=ROOT, capture_output=True, text=True, timeout=10)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return datetime.date.today().isoformat()


def canonical_url(path):
    return SITE_URL + ("" if path == "index.html" else path.replace("index.html", ""))


def structured_data():
    """schema.org graph for the home page: the organization, its alternate names and
    founders, and the site itself. This is what lets Google match searches like
    "beyond the net rice university" or "beyond the net carlos cruz" to this site."""
    org_id = SITE_URL + "#organization"
    rice = {"@type": "CollegeOrUniversity", "name": "Rice University",
            "sameAs": "https://www.rice.edu/"}
    graph = [
        {
            "@type": "NGO",
            "@id": org_id,
            "name": "Beyond the Net",
            "alternateName": C.ALT_NAMES,
            "url": SITE_URL,
            "logo": SITE_URL + "assets/img/logo.png",
            "image": SITE_URL + "assets/img/volleyball-court.jpg",
            "description": TAGLINE + " We mentor underserved youth in post-secondary "
                           "education, healthy lifestyles, and character development - "
                           "with volleyball as our medium.",
            "email": C.EMAIL,
            "sameAs": [C.INSTAGRAM],
            "address": {"@type": "PostalAddress", "addressLocality": "Houston",
                        "addressRegion": "TX", "addressCountry": "US"},
            "areaServed": {"@type": "City", "name": "Houston, Texas"},
            "founder": [
                {"@type": "Person", "name": f["name"], "jobTitle": f["role"],
                 "email": f["email"], "affiliation": rice}
                for f in C.FOUNDERS
            ],
            "knowsAbout": ["Youth mentorship", "College readiness", "Volleyball",
                           "First-generation students"],
        },
        {
            "@type": "WebSite",
            "@id": SITE_URL + "#website",
            "name": "Beyond the Net",
            "alternateName": C.ALT_NAMES,
            "url": SITE_URL,
            "publisher": {"@id": org_id},
        },
    ]
    data = json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, indent=1)
    # "</" inside a <script> block would end it early
    return data.replace("</", "<\\/")


def shell(path, title, desc, body, active="", share_img="assets/img/volleyball-court.jpg"):
    depth = path.count("/")
    p = "../" * depth
    # Absolute URLs — Open Graph consumers do not resolve relative paths
    canonical = canonical_url(path)
    extra_head = ""
    if path == "index.html":
        if C.GOOGLE_SITE_VERIFICATION:
            extra_head += (f'<meta name="google-site-verification" '
                           f'content="{esc(C.GOOGLE_SITE_VERIFICATION)}">\n')
        extra_head += (f'<script type="application/ld+json">\n{structured_data()}\n'
                       f'</script>\n')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(", ".join(C.KEYWORDS))}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Beyond the Net">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(SITE_URL + share_img)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(SITE_URL + share_img)}">
<meta name="theme-color" content="#c2274b">
<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{p}assets/img/logo.png" type="image/png" sizes="512x512">
<link rel="apple-touch-icon" href="{p}assets/img/logo.png">
<link rel="stylesheet" href="{p}assets/css/style.css">
{extra_head}</head>
<body>

<a class="skip-link" href="#main">Skip to Main Content</a>

{header(p, active)}

<main id="main">

{body}

</main>

{footer(p)}

<script>window.SITE_BASE = "{p}";</script>
<script src="{p}assets/js/site.js"></script>
</body>
</html>
"""


def not_found():
    """404.html is served for any missing URL at any depth, so relative asset
    paths would break. Everything here is absolute."""
    extra = f'\n        <a href="{SITE_URL}blog/">Blog</a>' if C.SHOW_BLOG else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page Not Found | Beyond The Net</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#c2274b">
<link rel="icon" href="{SITE_URL}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{SITE_URL}assets/css/style.css">
</head>
<body>

<main id="main">
  <section class="notfound">
    <div class="container">
      <p class="notfound__code">404</p>
      <h1>There&rsquo;s nothing here&hellip;</h1>
      <p class="notfound__text">We can&rsquo;t find the page you&rsquo;re looking for.
        Check the URL, or head back home.</p>
      <a class="btn" href="{SITE_URL}">Go Home</a>

      <nav class="notfound__links" aria-label="Site">
        <a href="{SITE_URL}programs-and-services.html">Programs &amp; Services</a>
        <a href="{SITE_URL}about.html">About</a>
        <a href="{SITE_URL}events.html">Events</a>{extra}
        <a href="{SITE_URL}get-involved.html">Reach Out</a>
      </nav>
    </div>
  </section>
</main>

</body>
</html>
"""


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  {path}")


# ------------------------------------------------------------------ page bodies

def blog_index(p):
    cards = []
    for post in C.POSTS:
        img = (f'<a class="post-card__media" href="{p}post/{post["slug"]}/">'
               f'<img src="{p}assets/img/{post["image"]}" alt="" width="1200" height="685" loading="lazy"></a>'
               ) if post["image"] else ""
        cards.append(f"""      <article class="post-card">
        {img}
        <div class="post-card__body">
          <p class="post-card__meta">{esc(post["author"])} &middot; <time datetime="{post["iso"]}">{esc(post["date"])}</time> &middot; {esc(post["read"])}</p>
          <h2><a href="{p}post/{post["slug"]}/">{esc(post["title"])}</a></h2>
          <p class="post-card__excerpt">{esc(post["body"][0])}</p>
          <a class="post-card__more" href="{p}post/{post["slug"]}/">Read More</a>
        </div>
      </article>""")
    return f"""  <section class="page-intro">
    <div class="container">
      <h1>Blog</h1>
      <p>Stories and guidance on mentorship, college readiness, and leadership from the Beyond the Net team.</p>
    </div>
  </section>

  <section class="post-list">
    <div class="container">
{chr(10).join(cards)}
    </div>
  </section>"""


def post_page(post, p):
    others = [x for x in C.POSTS if x["slug"] != post["slug"]]
    recent = "\n".join(
        f'        <li><a href="{p}post/{o["slug"]}/">{esc(o["title"])}</a></li>' for o in others
    )
    hero = (f'    <div class="container"><img class="post__hero" src="{p}assets/img/{post["image"]}"'
            f' alt="" width="1200" height="685"></div>') if post["image"] else ""
    paras = "\n".join(f"      <p>{esc(t)}</p>" for t in post["body"])
    return f"""  <section class="post">
    <div class="container">
      <p class="post__back"><a href="{p}blog/">&larr; All Posts</a></p>
      <h1>{esc(post["title"])}</h1>
      <p class="post__meta">{esc(post["author"])} &middot; <time datetime="{post["iso"]}">{esc(post["date"])}</time> &middot; {esc(post["read"])}</p>
    </div>
{hero}
    <div class="container post__body">
{paras}
    </div>

    <div class="container">
      <h2 class="post__recent-title">Recent Posts</h2>
      <ul class="post__recent">
{recent}
      </ul>
    </div>
  </section>"""


def booking_index(p):
    cards = []
    for s in C.SERVICES:
        img = (f'<a class="service-card__media" href="{p}service-page/{s["slug"]}/">'
               f'<img src="{p}assets/img/{s["image"]}" alt="" width="1200" height="800" loading="lazy"></a>'
               ) if s["image"] else ""
        meta = " &middot; ".join(x for x in [s["duration"], s["price"], s["location"]] if x)
        cta = (f'<a class="btn" href="{p}service-page/{s["slug"]}/">{esc(s["cta"])}</a>'
               if s["cta"] else
               f'<a class="service-card__more" href="{p}service-page/{s["slug"]}/">Learn More</a>')
        cards.append(f"""      <article class="service-card">
        {img}
        <div class="service-card__body">
          <h2><a href="{p}service-page/{s["slug"]}/">{esc(s["title"])}</a></h2>
          <p class="service-card__tagline">{esc(s["tagline"])}</p>
          <p class="service-card__meta">{meta}</p>
          {cta}
        </div>
      </article>""")
    return f"""  <section class="page-intro">
    <div class="container">
      <h1>Book Online</h1>
      <p>Sessions and mentorship offered by Beyond the Net.</p>
    </div>
  </section>

  <section class="service-list">
    <div class="container">
{chr(10).join(cards)}
    </div>
  </section>"""


def service_page(s, p):
    rows = []
    if s["duration"]:
        rows.append(("Duration", esc(s["duration"])))
    rows.append(("Price", esc(s["price_long"])))
    rows.append(("Location", esc(s["location"])))
    detail = "\n".join(
        f'        <div class="service__row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows
    )
    notice = (f'      <p class="service__notice">{esc(s["unavailable"])}</p>'
              if s["unavailable"] else "")
    cta = (f'      <a class="btn" href="mailto:{C.EMAIL}?subject={esc(s["title"])}">{esc(s["cta"])}</a>'
           if s["cta"] else
           f'      <a class="btn" href="mailto:{C.EMAIL}?subject={esc(s["title"])}">Contact Us</a>')
    hero = (f'    <div class="container"><img class="service__hero" src="{p}assets/img/{s["image"]}"'
            f' alt="" width="1200" height="800"></div>') if s["image"] else ""
    return f"""  <section class="service">
    <div class="container">
      <p class="post__back"><a href="{p}book-online/">&larr; Service list</a></p>
      <h1>{esc(s["title"])}</h1>
      <p class="service__tagline">{esc(s["tagline"])}</p>
{notice}
    </div>
{hero}
    <div class="container">
      <dl class="service__detail">
{detail}
      </dl>

      <h2 class="service__heading">Service Description</h2>
      <p class="service__desc">{esc(s["description"])}</p>

      <h2 class="service__heading">Contact Details</h2>
      <p class="service__desc">{esc(s["address"])}<br>
        <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>

{cta}
    </div>
  </section>"""


def event_page(e, p):
    hero = (f'    <div class="container"><img class="event__hero" src="{p}assets/img/{e["image"]}"'
            f' alt="" width="1200" height="685"></div>') if e["image"] else ""
    return f"""  <section class="event">
    <div class="container">
      <p class="post__back"><a href="{p}events.html">&larr; See other events</a></p>
      <h1>{esc(e["title"])}</h1>
      <p class="event__when"><time datetime="{e["iso"]}">{esc(e["short_date"])}</time> &middot; {esc(e["venue"])}</p>
      <p class="event__summary">{esc(e["summary"])}</p>
      <p class="event__status">{esc(e["status"])}</p>
    </div>
{hero}
    <div class="container">
      <h2 class="service__heading">Time &amp; Location</h2>
      <p class="service__desc">{esc(e["when"])}<br>{esc(e["where"])}</p>

      <h2 class="service__heading">About the Event</h2>
      <p class="service__desc">{esc(e["about"])}</p>

      <a class="btn" href="mailto:{C.EMAIL}?subject={esc(e["title"])}">Ask About This Event</a>
    </div>
  </section>"""


def events_page(p):
    """The live site shows no upcoming events; past events are listed beneath."""
    past = "\n".join(f"""        <li class="past-event">
          <a href="{p}event-details/{e["slug"]}/">
            <span class="past-event__date"><time datetime="{e["iso"]}">{esc(e["short_date"])}</time></span>
            <span class="past-event__title">{esc(e["title"])}</span>
            <span class="past-event__venue">{esc(e["venue"])}</span>
          </a>
        </li>""" for e in C.EVENTS)
    body = open(os.path.join(PARTIALS, "events.html"), encoding="utf-8").read().rstrip()
    return f"""{body}

  <section class="past-events">
    <div class="container">
      <h2>Past Events</h2>
      <ul class="past-events__list">
{past}
      </ul>
    </div>
  </section>"""


# ---------------------------------------------------------------- search index

def search_index():
    docs = []
    for e in C.EVENTS:
        docs.append({"t": "Events", "title": e["title"], "url": f"event-details/{e['slug']}/",
                     "desc": f"{e['when']} — {e['where']}",
                     "img": f"assets/img/{e['image']}" if e["image"] else "",
                     "text": " ".join([e["title"], e["summary"], e["about"], e["venue"], e["where"]])})
    if C.SHOW_SERVICES:
        for s in C.SERVICES:
            docs.append({"t": "Services", "title": s["title"], "url": f"service-page/{s['slug']}/",
                         "desc": s["description"],
                         "img": f"assets/img/{s['image']}" if s["image"] else "",
                         "text": " ".join([s["title"], s["tagline"], s["description"], s["price"]])})
    if C.SHOW_BLOG:
        for b in C.POSTS:
            docs.append({"t": "Blog Posts", "title": b["title"], "url": f"post/{b['slug']}/",
                         "desc": b["body"][0],
                         "img": f"assets/img/{b['image']}" if b["image"] else "",
                         "text": " ".join([b["title"]] + b["body"])})
    # Site pages: index the visible prose of each static page
    site_pages = [("index.html", "Home"), ("about.html", "About"),
                  ("programs-and-services.html", "Programs & Services"),
                  ("get-involved.html", "Get Involved"), ("events.html", "Events")]
    if C.SHOW_BLOG:
        site_pages.append(("blog/", "Blog"))
    if C.SHOW_SERVICES:
        site_pages.append(("book-online/", "Book Online"))
    for path, title in site_pages:
        src = {"blog/": None, "book-online/": None}.get(path, path)
        text = title
        if src:
            partial = os.path.join(PARTIALS, os.path.splitext(src)[0] + ".html")
            if os.path.exists(partial):
                raw = open(partial, encoding="utf-8").read()
                text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))).strip()
        docs.append({"t": "Pages", "title": title, "url": path,
                     "desc": text[:160], "img": "", "text": f"{title} {text}"})
    return docs


# ------------------------------------------------------------------------ main

def main():
    print("Building pages:")

    pages = [
        ("index.html", f"{BRAND} (HTX) | Youth Volleyball Mentorship Nonprofit",
         "Beyond the Net Houston (HTX) mentors underserved youth in college readiness, healthy "
         "lifestyles, and character development through volleyball. Founded by Carlos Cruz "
         "and Arman Najari of Rice University.", "index.html"),
        ("about.html", f"About {BRAND} | Carlos Cruz & Arman Najari, Rice University",
         "Meet the founders of Beyond the Net Houston, Carlos Cruz and Arman Najari of Rice "
         "University, and learn about our vision, mission, and values.", "about.html"),
        ("programs-and-services.html", f"Programs & Services | {BRAND}",
         "Learn more about how Beyond the Net impacts Houston youth - on and off the court: "
         "college application help, mentorship, volleyball, and volunteer hours.",
         "programs-and-services.html"),
        ("get-involved.html", f"Get Involved | {BRAND}",
         "Volunteer, partner, or bring Beyond the Net Houston to your school. Students, "
         "teachers, parents, and future volunteers - we would love to hear from you!",
         "get-involved.html"),
    ]
    for path, title, desc, active in pages:
        body = open(os.path.join(PARTIALS, path), encoding="utf-8").read().rstrip()
        write(path, shell(path, title, desc, body, active))

    write("events.html", shell(
        "events.html", f"Events | {BRAND}",
        "Stay tuned for upcoming Beyond the Net Houston events and workshops designed to "
        "support and empower youth in our community.", events_page(""), "events.html"))

    sitemap = ["index.html", "about.html", "programs-and-services.html",
               "get-involved.html", "events.html"]

    if C.SHOW_BLOG:
        write("blog/index.html", shell(
            "blog/index.html", f"Blog | {BRAND}",
            "Stories and guidance on mentorship, college readiness, and leadership.",
            blog_index("../"), "blog/"))
        sitemap.append("blog/index.html")

        for post in C.POSTS:
            path = f"post/{post['slug']}/index.html"
            write(path, shell(path, f"{post['title']} | {BRAND}",
                              post["body"][0][:155], post_page(post, "../../"), "blog/"))
            sitemap.append(path)

    if C.SHOW_SERVICES:
        write("book-online/index.html", shell(
            "book-online/index.html", f"Book Online | {BRAND}",
            "Sessions and mentorship offered by Beyond the Net.",
            booking_index("../"), "book-online/"))
        sitemap.append("book-online/index.html")

        for s in C.SERVICES:
            path = f"service-page/{s['slug']}/index.html"
            write(path, shell(path, f"{s['title']} | {BRAND}", s["description"][:155],
                              service_page(s, "../../"), "book-online/"))
            sitemap.append(path)

    for e in C.EVENTS:
        path = f"event-details/{e['slug']}/index.html"
        write(path, shell(path, f"{e['title']} | {BRAND}", e["summary"][:155],
                          event_page(e, "../../"), "events.html"))
        sitemap.append(path)

    write("404.html", not_found())

    # GitHub Pages reads this file to serve the site on its own domain
    if C.CUSTOM_DOMAIN:
        write("CNAME", C.CUSTOM_DOMAIN + "\n")

    urls = "\n".join(
        f"  <url><loc>{esc(canonical_url(p))}</loc>"
        f"<lastmod>{last_modified(p)}</lastmod></url>" for p in sitemap)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f"{urls}\n</urlset>\n")
    # Crawlers only read robots.txt at the root of a host, so on the github.io project
    # URL this file is inert. It takes effect once the site moves to its own domain.
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")

    docs = search_index()
    with open(os.path.join(ROOT, "assets", "search-index.json"), "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, separators=(",", ":"))
    print(f"\n  assets/search-index.json ({len(docs)} documents)")


if __name__ == "__main__":
    main()
