# anandrams.github.io

The personal site: writing, project case studies, about and contact.
Jekyll, built by GitHub Pages itself, served from `main` at
<https://anandrams.github.io>.

---

## Run it locally

```bash
bundle install          # first time only
bundle exec jekyll serve --livereload
```

Then open <http://127.0.0.1:4000>. Saving a file rebuilds the page.

`Gemfile` pins the `github-pages` gem, which is the exact set of versions
GitHub Pages runs. So if it builds here, it builds there.

If `bundle install` complains about a missing Ruby or a permissions error,
install Ruby with Homebrew (`brew install ruby`) and add its `bin` to the
path rather than using the one macOS ships.

---

## Publishing

GitHub Pages builds every push to `main`. There is no workflow file and
no `_site` in the repository — pushing the source is the whole deploy.

```bash
git add -A
git commit -m "Add M5 write-up"
git push
```

The build takes about a minute. If it fails, GitHub emails the address on
the account and the Actions tab shows the error.

The previous version of this site is tagged **`v1-site`**, so nothing was
lost: `git show v1-site:index.html` reads the old home page.

---

## Where the content lives

| What | Where | How it's edited |
|---|---|---|
| Articles | `_articles/*.md` | **Generated — don't edit by hand.** Write them in the project repo and run the sync script below. |
| Project case studies | `_projects/*.md` | All in the front matter. Copy `_projects/_TEMPLATE.md`. |
| Posts published elsewhere | `_data/external_writing.yml` | Add an entry with its link. |
| Home, Writing, Projects, About, Contact | `index.html`, `writing.html`, `projects.html`, `about.html`, `contact.html` | Edit directly. |
| Styles | `assets/css/site.css` | One file. The design tokens are at the top; change a colour there and the whole site follows. |
| Behaviour | `assets/js/site.js` | Theme toggle, filters, reading bar, table of contents. |

### Adding an article

Articles are written in the project repository, next to the code they
describe, and copied here:

```bash
python3 tools/sync_articles.py \
  --source ~/Documents/HDD/08_ClaudeCowork/projects/UAV_FW_TM/docs/website_articles
```

That reads every `*.md` in the source folder, rewrites the media paths,
copies the images and videos into `assets/articles/tm1/media/`, and writes
`_articles/*.md`. It is safe to re-run; it overwrites and never deletes.

When a new phase is written up, add its row to the `PHASES` table at the
top of `tools/sync_articles.py` (the phase label, the theme chip and the
thumbnail's alt text) — the script stops and says so if the row is missing,
rather than guessing.

Use `--dry-run` to see what it would do first.

### Adding a project

```bash
cp _projects/_TEMPLATE.md _projects/<slug>.md
```

Fill in the front matter. The template lists every key and what it does.
Set `series_slug` to the same value the project's articles use and the
"Written up in" section fills itself. The file name becomes the URL.

### Correcting a published article

Add a `corrections:` list to that article's front matter:

```yaml
corrections:
  - date: 2026-11-02
    note: "The M3 ceiling figure was 122 m, not 120 m; the plot was regenerated."
```

The article shows them in a dated block at the end. Correcting rather than
quietly swapping is the point — a correction that isn't visible isn't one.

Because `_articles/` is generated, a correction made there is lost on the
next sync. Either make the same correction in the source article, or keep
the correction in the source file's front matter so the sync carries it.

---

## Things still to do

- **Contact form.** Create a form at <https://formspree.io> and paste its
  POST URL into `formspree_endpoint` in `_config.yml`. Until then the
  contact page points at LinkedIn instead of showing a form that goes
  nowhere.
- **LinkedIn mark.** The footer and About use a drawn glyph, not the
  official LinkedIn logo. If you want the real one, take it from LinkedIn's
  brand resources and drop it in `assets/`.
- **Analytics and a custom domain.** Both deliberately left out for now.
  A domain is a `CNAME` file plus DNS records and does not change anything
  else in this repository.

---

## Regenerating the icons

```bash
python3 tools/make_icons.py --fonts <folder with DMMono-Regular.ttf and BricolageGrotesque-Bold.ttf>
```

Writes the favicon, the touch icon, the manifest icons and the link-preview
image into `assets/`. Only needed if the monogram changes.

---

## House rules for anything published here

- Nothing on the site that isn't true and checkable.
- No customer names, product names or project details from the day job.
  Those stay on the résumé and LinkedIn.
- Simulation work says it is simulation, every time.
- Corrections are dated and visible.
- The footer carries "Views are my own and do not reflect my employer." on
  every page; it is set once in `_config.yml`.
