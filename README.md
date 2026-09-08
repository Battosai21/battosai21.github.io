# Portfolio

A single-page portfolio site, generated from a structured data file and
auto-deployed to GitHub Pages on every push.

## How it works

```
data/resume.json        ← CV data (work, skills, projects, etc.)
data/biography.json     ← homepage story: intro + year-by-year chapters
templates/index.html.j2 ← biography homepage (scrollable story + timeline)
templates/resume.html.j2← résumé page
build.py                ← reads both data files, renders both templates
output/                 ← generated site: index.html, resume.html, assets/
.github/workflows/deploy.yml ← builds + deploys automatically on push
```

The homepage (`index.html`) is a scrollable biography with a sticky
year-timeline at the top — clicking a year jumps to that chapter, and
the active year highlights as you scroll. A "Jump to résumé →" link in
the header (and footer) takes visitors straight to `resume.html`,
which has its own "← Back to my story" link.

You edit the two JSON files, push to `main`, and GitHub Actions
rebuilds both pages and republishes them automatically.

## One-time setup

1. Create a new GitHub repo (e.g. `yourusername.github.io` for a root
   domain, or any name for a project site).
2. Push this folder's contents to the repo's `main` branch.
3. In the repo, go to **Settings → Pages** and set **Source** to
   **GitHub Actions**.
4. Push any change (or re-run the workflow from the **Actions** tab).
   Your site will be live at `https://yourusername.github.io/reponame/`
   (or `https://yourusername.github.io/` if you used the special repo
   name above).

## Local development

```bash
pip install -r requirements.txt
python dev.py
```

Then open `http://localhost:8000`. This watches `data/`, `templates/`,
and `assets/` for changes and rebuilds automatically — just refresh
your browser after saving an edit. No need to push to GitHub to see
changes. Pass a different port with `python dev.py 8080` if 8000 is
taken.

For a one-off build without the watcher:

```bash
python build.py
# open output/index.html directly, or serve it:
cd output && python -m http.server 8000
```

## Updating your info

**The biography (`data/biography.json`)** — an `intro` string plus a
`chapters` array. Each chapter needs a `year`, `title`, `text`, and
optional `image` path. Add, remove, or reorder chapters freely — the
timeline and page both rebuild from whatever's in the array. Years
don't need to be evenly spaced or continuous.

**The résumé (`data/resume.json`)** — follows a structure loosely based
on the [JSON Resume](https://jsonresume.org/) schema:

- `basics` — name, title, contact info, profile links, summary
- `work` — job history
- `military` — military/reserve service (delete this section from both
  the JSON and template if not relevant to you)
- `projects` — things you've built, with optional links and tags
- `skills` — grouped skill tags
- `languages`
- `certifications`

Every field maps directly to something in `templates/index.html.j2`,
so if you want to change what's *displayed* (not just the content),
that's the file to edit. Sections are hidden automatically if their
data is empty.

## Customizing the design

Colors, fonts, and spacing are all defined as CSS in the `<style>`
block at the top of `templates/index.html.j2`. The key variables are
at the top under `:root` if you want to change the palette quickly.

## Adding photos

Drop images into `assets/images/` (there's a `biography/` subfolder
for chapter photos and a `projects/` subfolder for project photos) and
reference them by path in the matching JSON file. `build.py` copies
the whole `assets/` folder into `output/` on every build, so new
images just work once referenced — no other wiring needed.
Recommended aspect ratios: square for the profile photo, 16:10 for
chapter and project photos, so nothing gets stretched or cropped
oddly.

## Ideas for making it more "dynamic"

- Add a step to the GitHub Action that pulls live data (e.g. your
  GitHub contribution stats, or a Play Store app rating) into
  `data/resume.json` before the build step, using a small Python
  script and the relevant API.
- Add a `schedule:` trigger to `.github/workflows/deploy.yml` (cron)
  so the site rebuilds periodically even without a manual push.
- Export `data/resume.json` to PDF using a JSON Resume theme/CLI if
  you want a matching downloadable CV alongside the website.
