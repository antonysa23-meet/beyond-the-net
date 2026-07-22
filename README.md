# Beyond the Net — Houston

Static rebuild of the Beyond the Net website, migrated off Wix so it can be hosted on
GitHub Pages: free, faster, version-controlled, and editable without the Wix editor.

Beyond the Net is a Houston youth-mentorship nonprofit that mentors underserved youth in
post-secondary education, healthy lifestyles, and character development — with volleyball
as its medium.

## Pages

```
index.html                          Home
about.html                          Mission, vision, values, team
programs-and-services.html          Programs overview + "How We Help" cards
get-involved.html                   Ways to get involved and contact details
events.html                         Upcoming events + past events list
blog/                               Blog index
post/<slug>/                        3 blog posts
event-details/<slug>/               3 past events
```

URLs mirror the original Wix paths, so existing links and bookmarks keep working.

The Wix Bookings pages (Book Online and the three paid services) are turned off via
`SHOW_SERVICES = False` in `_tools/content.py`. Their content and images are still in the
repo — set the flag to `True` and rebuild to bring the pages, the nav entry, and their
search results back.

## Structure

```
assets/css/style.css         All styling (single stylesheet, CSS custom properties)
assets/js/site.js            Mobile nav, "More" dropdown, site search
assets/search-index.json     Generated search index
assets/img/                  Photography and logos
_partials/                   Hand-tuned page bodies for the five main pages
_tools/                      Build and maintenance scripts (not served)
```

## Editing

Pages are generated so the header, footer, and search stay identical everywhere.

```bash
python _tools/build.py
```

- **Blog posts, services, events** live in `_tools/content.py`. Edit there and rebuild.
- **The five main pages** keep their hand-tuned markup in `_partials/`. Edit the HTML in
  that folder — not the generated file at the repo root — then rebuild.
- **Colors and fonts** are CSS custom properties at the top of `assets/css/style.css`
  (`--brand`, `--ink`, `--slate`, `--serif`, `--sans`).
- **Images** go in `assets/img/`. Keep them under roughly 250 KB, and set `width`/`height`
  on the `<img>` so the layout doesn't shift while loading.

Search is client-side: `build.py` writes `assets/search-index.json` from the same content,
so it stays in sync automatically. No backend required.

### Checking your work

```bash
python _tools/verify.py     # every internal link, image, and shared asset resolves
python -m http.server 8000  # then open http://localhost:8000
```

`_tools/crawl.py` re-crawls the original Wix site if you ever need to diff against it.

## Deploying

Pushing to `main` publishes automatically via GitHub Pages.

## Notes

- The body font is **Mulish**, standing in for Wix's licensed Avenir. Display type is
  **Forum**, the same font the original used.
- Wix pages that were unfinished template boilerplate (`/adults`, `/parenting`, `/youth`,
  `/seniors`, `/portfolio`, and the placeholder privacy/refund/terms pages) were **not**
  carried over — they contained generic Wix filler text, not Beyond the Net's content.
- Content text reproduces the original exactly, including its typos.
