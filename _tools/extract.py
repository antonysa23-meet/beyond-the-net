"""Pull readable text + image references out of the crawled Wix HTML."""
import glob
import html
import os
import re
import sys

CRAWL = os.path.join(os.path.dirname(__file__), "..", "_crawl")


def text_of(path):
    s = open(path, encoding="utf-8").read()
    body = re.sub(r"(?s)<script.*?</script>|<style.*?</style>|<!--.*?-->", "", s)
    txt = html.unescape(re.sub(r"(?s)<[^>]+>", "\n", body))
    out, prev = [], None
    for line in (x.strip() for x in txt.split("\n")):
        if len(line) > 1 and line != prev:
            out.append(line)
            prev = line
    return out


def images_of(path):
    s = html.unescape(open(path, encoding="utf-8").read())
    seen = []
    for m in re.finditer(r"<img[^>]*>", s):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        if src and "wixstatic" in src.group(1):
            mid = re.search(r"/media/([^/\"]+)", src.group(1))
            if mid and mid.group(1) not in [x[0] for x in seen]:
                seen.append((mid.group(1), alt.group(1) if alt else ""))
    return seen


def main(pattern):
    for f in sorted(glob.glob(os.path.join(CRAWL, pattern))):
        name = os.path.basename(f)
        print("=" * 25, name)
        lines = text_of(f)
        # Trim the Wix chrome that wraps every page
        start = next((i for i, l in enumerate(lines) if l == "Search"), 0)
        end = next((i for i, l in enumerate(lines) if l == "bottom of page"), len(lines))
        for l in lines[start + 1:end]:
            print("   ", l)
        print("  -- images --")
        for mid, alt in images_of(f):
            print("    ", mid, "| alt=", alt)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "*.html")
