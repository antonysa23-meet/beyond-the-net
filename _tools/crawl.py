"""Crawl the live Wix site and record every reachable page under /beyond-the-net.

Wix renders most listings client-side, but the server response embeds the data in
warmup JSON, so a plain fetch is enough to discover URLs. BFS from the known roots.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from html import unescape

BASE = "https://beyondthenethtx.wixsite.com/beyond-the-net"
HOST = "https://beyondthenethtx.wixsite.com"
OUT = os.path.join(os.path.dirname(__file__), "..", "_crawl")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36"

SEEDS = [
    BASE,
    BASE + "/about",
    BASE + "/programs-and-services",
    BASE + "/get-involved",
    BASE + "/events",
    BASE + "/blog",
    BASE + "/book-online",
]

# Wix app sub-routes we care about; anything else under /beyond-the-net is a normal page.
SKIP = re.compile(
    r"(wix\.com|parastorage|wixstatic|wixpress|sentry|schema\.org|"
    r"/_partials|\.(png|jpg|jpeg|gif|svg|ico|css|js|woff2?|xml|json)($|\?))",
    re.I,
)


def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(1.5 * (i + 1))
        except Exception:
            time.sleep(1.5 * (i + 1))
    return None


def slug(url):
    p = url[len(BASE):].strip("/") or "home"
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", p)[:120]


def links_in(html):
    found = set()
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html):
        u = unescape(m.group(1))
        if u.startswith("/"):
            u = HOST + u
        if not u.startswith(BASE):
            continue
        u = u.split("#")[0].split("?")[0].rstrip("/")
        if SKIP.search(u):
            continue
        found.add(u)
    # Wix embeds route data in JSON blobs; catch relative page links there too
    for m in re.finditer(r'"(?:url|link|pageUrl|slug)"\s*:\s*"(/beyond-the-net/[^"]+)"', html):
        u = HOST + unescape(m.group(1)).split("#")[0].split("?")[0].rstrip("/")
        if not SKIP.search(u):
            found.add(u)
    return found


def main():
    os.makedirs(OUT, exist_ok=True)
    seen, queue, saved = set(), list(SEEDS), []
    while queue:
        url = queue.pop(0).rstrip("/")
        if url in seen:
            continue
        seen.add(url)
        html = fetch(url)
        if html is None:
            print("404  ", url, flush=True)
            continue
        path = os.path.join(OUT, slug(url) + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        saved.append({"url": url, "file": os.path.basename(path), "bytes": len(html)})
        print(f"{len(html):>9}  {url}", flush=True)
        for nxt in links_in(html):
            if nxt not in seen:
                queue.append(nxt)
        time.sleep(0.4)

    with open(os.path.join(OUT, "_index.json"), "w", encoding="utf-8") as f:
        json.dump(saved, f, indent=2)
    print(f"\n{len(saved)} pages saved to {os.path.abspath(OUT)}")


if __name__ == "__main__":
    sys.exit(main())
