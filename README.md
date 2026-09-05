# Portfolio

A single-page portfolio site, generated from a structured data file and
auto-deployed to GitHub Pages on every push.

## How it works

```
data/resume.json        ← your info lives here (edit this)
templates/index.html.j2 ← Jinja2 template (rarely needs editing)
build.py                ← reads the data, renders the template
output/index.html       ← generated site (don't edit directly)
.github/workflows/deploy.yml ← builds + deploys automatically on push
```

You edit `data/resume.json`, push to `main`, and GitHub Actions rebuilds
the site and publishes it to GitHub Pages automatically. No manual
deploy step.

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
python build.py
# open output/index.html in a browser
```

## Updating your info

Edit `data/resume.json` — it follows a structure loosely based on the
[JSON Resume](https://jsonresume.org/) schema:

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

## Ideas for making it more "dynamic"

- Add a step to the GitHub Action that pulls live data (e.g. your
  GitHub contribution stats, or a Play Store app rating) into
  `data/resume.json` before the build step, using a small Python
  script and the relevant API.
- Add a `schedule:` trigger to `.github/workflows/deploy.yml` (cron)
  so the site rebuilds periodically even without a manual push.
- Export `data/resume.json` to PDF using a JSON Resume theme/CLI if
  you want a matching downloadable CV alongside the website.
