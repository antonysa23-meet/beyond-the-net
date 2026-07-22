"""Check every generated page: internal links resolve, images exist, assets are wired."""
import glob
import os
import re
import sys
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

    print(f"Checked {len(pages)} pages")
    for p in pages:
        print("  ", p)
    if problems:
        print(f"\n{len(problems)} PROBLEM(S):")
        for p in problems:
            print("  -", p)
        return 1
    print("\nAll internal links, images, and shared assets resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
