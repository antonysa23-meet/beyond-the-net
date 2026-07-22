"""Dump the visible text of every page, so a redesign can be proved content-neutral.

    python _tools/content_snapshot.py > _baseline.txt      # before
    python _tools/content_snapshot.py > _after.txt         # after
    diff _baseline.txt _after.txt                          # must be empty

Ignores markup entirely: only the words a visitor reads, in document order.
"""
import glob
import html
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def visible_text(path):
    src = open(path, encoding="utf-8").read()
    # Drop everything that never renders as prose
    src = re.sub(r"(?s)<script.*?</script>", " ", src)
    src = re.sub(r"(?s)<style.*?</style>", " ", src)
    src = re.sub(r"(?s)<head.*?</head>", " ", src)
    src = re.sub(r"(?s)<svg.*?</svg>", " ", src)
    src = re.sub(r"(?s)<!--.*?-->", " ", src)
    # Block-level tags become newlines so word order stays readable
    src = re.sub(r"(?i)<(br|/p|/h[1-6]|/li|/div|/section|/article|/dd|/dt)[^>]*>", "\n", src)
    text = html.unescape(re.sub(r"(?s)<[^>]+>", " ", src))
    out = []
    for line in text.split("\n"):
        line = re.sub(r"[ \t ​]+", " ", line).strip()
        if line:
            out.append(line)
    return out


def main():
    pages = sorted(
        os.path.relpath(p, ROOT).replace("\\", "/")
        for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
        if not os.path.relpath(p, ROOT).replace("\\", "/").startswith(("_", "."))
    )
    for rel in pages:
        print(f"===== {rel}")
        for line in visible_text(os.path.join(ROOT, rel)):
            print(line)
        print()


if __name__ == "__main__":
    sys.exit(main())
