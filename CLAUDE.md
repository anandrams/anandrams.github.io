# CLAUDE.md — context for this repository

Personal site for Anand Ram Sathyanarayanan. Jekyll, built by GitHub Pages
itself from `main`, served at <https://anandrams.github.io>.

Rebuilt in October 2026. The previous version is tagged **`v1-site`**, and
its pages are kept in `_archive/v1/` (excluded from the build). Nothing from
it is live.

---

## Shape of the site

Five pages, built from a small set of layouts:

```
index.html      Home       hero, the current project, the latest writing
writing.html    /writing/  every article, filterable in the browser
projects.html   /projects/ the project cards
about.html      /about/
contact.html    /contact/
404.html
feed.xml        the writing feed, hand-written (not jekyll-feed)
```

Two collections:

```
_articles/   one file per article   -> /writing/<slug>/   layout: article
_projects/   one file per project   -> /projects/<slug>/  layout: project
```

Supporting files:

```
_layouts/    default, page, article, project
_includes/   header.html, footer.html
_data/       external_writing.yml  — posts published on LinkedIn
assets/css/site.css   every style, tokens at the top
assets/js/site.js     theme toggle, filters, reading bar, TOC, captions
tools/                sync_articles.py, make_icons.py (excluded from build)
```

---

## Rules that matter here

These came from the owner and are not negotiable:

1. **Nothing on the site that isn't true.** No invented metrics, no inferred
   claims, no rounded-up anything. If a number isn't in a source document,
   it doesn't go on the page.
2. **No day-job detail.** No customer names, product names, or project
   specifics from Siemens or its clients. Method language only. The résumé
   and LinkedIn carry that material; the site does not.
3. **Simulation says it's simulation.** Every TM-1 article and the project
   page state that no aircraft was built or flown.
4. **Corrections are dated and visible**, never silent edits.
5. The footer disclaimer ("Views are my own and do not reflect my employer.")
   appears on every page, set once in `_config.yml`.

---

## How content gets in

**Articles are generated, not written here.** They live in the project
repository and are imported:

```bash
python3 tools/sync_articles.py \
  --source ~/Documents/HDD/08_ClaudeCowork/projects/UAV_FW_TM/docs/website_articles
```

Editing a file in `_articles/` directly is wrong — the next sync overwrites
it. Change the source article instead.

A new phase needs a row in the `PHASES` table at the top of that script
(phase label, theme chip, thumbnail alt text). The script stops with a clear
message if the row is missing rather than guessing.

**Project Notes** is the third Writing format, alongside Article and Essay:
one page per project holding the concepts, equations and lessons behind it
(`_articles/tm1-uav-project-notes.md`). It is **hand-written**, not generated
— the sync script only overwrites files named after a source slug, so it
survives a re-sync. It shares the project's `series_slug` but has no `part`,
which is what keeps it out of the numbered series: no progress bar, no
previous/next, not counted in "Part 7 of 7". The project page links to it and
each article's sidebar links to it.

The series is called **TM-1 UAV**. Do not call it "project notes" — that
phrase now means the format above. `sync_articles.py` rewrites the old phrase
out of the caveat line it lifts from the source articles.

**Projects** are front matter only: copy `_projects/_TEMPLATE.md`, which
documents every key. All seven sections (Why / What was built / How it was
built / Results / Decisions worth arguing about / Phase log / Written up in)
come from that front matter, so every project reads the same way. A section
whose key is absent is skipped.

**The block diagrams are markup, not images** — the `diagram:` and `loop:`
lists in a project's front matter. They stay sharp, work in both themes, and
are readable by a screen reader.

---

## Design

Tokens live at the top of `assets/css/site.css` and nowhere else.

- Light: `--bg #F5F2EA` `--surface #FCFBF7` `--ink #16191C` `--muted #4F5A63`
  `--line #D8D2C2` `--chip #ECE7DA` `--accent #B8420C`
- Dark: `--bg #101418` `--surface #161B20` `--ink #ECE9E1` `--muted #A3AEB7`
  `--line #2A323A` `--chip #1E252C` `--accent #F08A4B`
- Type: Bricolage Grotesque (display), IBM Plex Sans (UI and body),
  DM Mono (labels, dates, small structural text), Source Serif 4 (article prose)
- Article column is 65ch; the page grid is 1200px with a 48px gutter
  (20px on phones).

Accessibility rules the design holds to: 4.5:1 text contrast in both themes,
44px minimum touch targets, a visible 2px focus ring, every control a real
link/button/input, and all motion dropped under `prefers-reduced-motion`.

Dark mode follows the OS unless the visitor picks a theme; the choice is kept
in `localStorage` and applied before first paint by an inline script in
`_layouts/default.html`.

---

## Build notes

- GitHub Pages builds this natively, so **only its allowed plugins work**:
  `jekyll-seo-tag` and `jekyll-sitemap` here. Don't add others — they'd work
  locally and silently do nothing in production.
- `Gemfile` pins the `github-pages` gem so local matches production.
- Display equations stay as `<script type="math/tex">` from kramdown and are
  rendered by KaTeX, loaded only on pages with `math: true`. If KaTeX fails
  to load, `site.js` shows the LaTeX source rather than dropping the equation.
- Wide tables get a scroll container added by `site.js`, so a table never
  pushes the article column sideways on a phone.
- Filtering hides entries with the `hidden` attribute; `[hidden]` is forced
  to `display: none !important` in the CSS because the layout classes would
  otherwise win.
- `readbar` and `nav_section` live in `_config.yml` defaults, **not** in a
  layout's front matter. Jekyll exposes a layout's own front matter as
  `layout`, not `page`, so set there they silently never fire.
- The home page picks its project by `featured: true`, not by name. Matching
  on a name broke once already when the project was renamed.

Run it locally with `bundle exec jekyll serve --livereload`.

---

## Still open

- `formspree_endpoint` in `_config.yml` is empty, so the contact page shows a
  LinkedIn fallback instead of a form.
- The LinkedIn icon is a drawn glyph, not the official mark.
- No analytics and no custom domain yet; both were deliberately deferred.
- `vendor/bundle/` is committed from the old site and is dead weight
  (excluded from the build). Worth removing, but ask first.
- The source articles in the project repo still open with "TM-1 project
  notes, milestone M4…". `SIMNOTE_FIXES` in `sync_articles.py` rewrites that
  on import; delete it once the source says "TM-1 UAV".
