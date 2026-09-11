"""Check every generated page: internal links resolve, images exist, assets are wired,
and the search-engine basics (titles, descriptions, structured data, sitemap) are in place."""
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from html import unescape
from urllib.parse import urljoin

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def page_paths():
    out = []
    for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        if rel.startswith(("_", ".")):
            continue
        out.append(rel)
    return sorted(out)


def main():
    problems = []
    pages = page_paths()
    for rel in pages:
        src = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        base = os.path.dirname(rel)

        refs = []
        refs += [(m, "href") for m in re.findall(r'href="([^"]+)"', src)]
        refs += [(m, "src") for m in re.findall(r'src="([^"]+)"', src)]

        for target, kind in refs:
            target = unescape(target)
            if re.match(r"^(https?:|mailto:|#|data:)", target):
                continue
            clean = target.split("#")[0].split("?")[0]
            if not clean:
                continue
            resolved = os.path.normpath(os.path.join(base, clean))
            candidates = [resolved]
            if clean.endswith("/") or not os.path.splitext(clean)[1]:
                candidates.append(os.path.join(resolved, "index.html"))
            if not any(os.path.exists(os.path.join(ROOT, c)) for c in candidates):
                problems.append(f"{rel}: {kind}=\"{target}\" -> missing")

        # 404.html is standalone by design: absolute asset URLs, no nav or search
        if rel != "404.html":
            for needed in ["assets/css/style.css", "assets/js/site.js"]:
                depth = rel.count("/")
                expect = ("../" * depth) + needed
                if expect not in src:
                    problems.append(f"{rel}: does not reference {expect}")

            if "search-panel" not in src:
                problems.append(f"{rel}: missing search panel")

            # Search engines: every page needs a branded title, a description, a canonical
            title = re.search(r"<title>([^<]*)</title>", src)
            if not title or "Beyond the Net Houston" not in unescape(title.group(1)):
                problems.append(f"{rel}: <title> does not name Beyond the Net Houston")
            if not re.search(r'<meta name="description" content="[^"]{50,}"', src):
                problems.append(f"{rel}: missing or too-short meta description")
            if '<link rel="canonical"' not in src:
                problems.append(f"{rel}: missing canonical link")

        for block in re.findall(r'(?s)<script type="application/ld\+json">(.*?)</script>', src):
            try:
                json.loads(block)
            except ValueError as e:
                problems.append(f"{rel}: invalid JSON-LD ({e})")

    home = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    if "application/ld+json" not in home:
        problems.append("index.html: missing schema.org structured data")

    # Sitemap: every URL must exist, and every real page must be listed
    site_url = re.search(r'<link rel="canonical" href="([^"]+)"', home).group(1)
    sitemap_path = os.path.join(ROOT, "sitemap.xml")
    listed = set()
    if not os.path.exists(sitemap_path):
        problems.append("sitemap.xml: missing")
    else:
        for loc in ET.parse(sitemap_path).getroot().iter(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            if not loc.text.startswith(site_url):
                problems.append(f"sitemap.xml: {loc.text} is off-site")
                continue
            rel = loc.text[len(site_url):] or "index.html"
            if rel.endswith("/"):
                rel += "index.html"
            listed.add(rel)
            if not os.path.exists(os.path.join(ROOT, rel)):
                problems.append(f"sitemap.xml: {loc.text} -> missing")
        for rel in pages:
            if rel != "404.html" and rel not in listed:
                problems.append(f"sitemap.xml: does not list {rel}")

    print(f"Checked {len(pages)} pages")
    for p in pages:
        print("  ", p)
    if problems:
        print(f"\n{len(problems)} PROBLEM(S):")
        for p in problems:
            print("  -", p)
        return 1
    print("\nAll internal links, images, shared assets, SEO tags and the sitemap check out.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
