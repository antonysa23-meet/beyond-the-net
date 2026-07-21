# Beyond the Net — Houston

Static rebuild of the Beyond the Net website, migrated off Wix so it can be hosted on
GitHub Pages: free, faster, version-controlled, and editable without the Wix editor.

Beyond the Net is a Houston youth-mentorship nonprofit that mentors underserved youth in
post-secondary education, healthy lifestyles, and character development — with volleyball
as its medium.

## Structure

```
index.html                    Home
about.html                    Mission, vision, values, team
programs-and-services.html    Programs overview + "How We Help" cards
get-involved.html             Ways to get involved and contact details
events.html                   Upcoming events
assets/css/style.css          All styling (single stylesheet, CSS custom properties)
assets/js/site.js             Mobile navigation toggle
assets/img/                   Photography and logos
```

No build step and no dependencies — plain HTML, CSS, and a few lines of JavaScript.

## Running locally

```bash
python -m http.server 8000
```

Then open <http://localhost:8000>.

## Editing

- **Text** lives directly in the HTML files. Search for the sentence you want to change.
- **Colors and fonts** are CSS custom properties at the top of `assets/css/style.css`
  (`--brand`, `--ink`, `--slate`, `--serif`, `--sans`).
- **Images** go in `assets/img/`. Keep them under roughly 250 KB so pages stay fast, and
  update the `width`/`height` attributes on the `<img>` tag to match the new file so the
  layout doesn't shift while loading.
- **Adding an event**: replace the "No events at the moment" block in `events.html`.

The desktop layout mirrors the measurements of the original 1425px Wix canvas; the
stylesheet collapses to stacked layouts at 1120px, 900px, and 620px.

## Deploying

Pushing to `main` publishes automatically via GitHub Pages.
