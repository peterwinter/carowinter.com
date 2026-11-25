# carowinter.com

This is the code and content for **carowinter.com**. You can do everything below on github.com, in your web browser. After any change, the live site updates on its own within a minute or two.

## Add a new article

**1. Upload the cover image** (a square image works best)

- Open the `assets/covers` folder → **Add file** → **Upload files**
- Name it like the others: `2025-03_bloomberg.jpg` (year-month_publication)
- Click **Commit changes**

**2. Upload the PDF** (optional)

- Same steps, in the `assets/pdf` folder.

**3. Create the article**

- Open the `_articles` folder → **Add file** → **Create new file**
- Name it with the date and a few words of the title: `2025-03-my-new-story.md`
- Paste this in and fill it out:

```
---
title: "My New Story"
publication: "Bloomberg Businessweek"
date: 2025-03-01
link: https://www.bloomberg.com/...
cover: 2025-03_bloomberg.jpg
pdf: 2025-03_bloomberg.pdf
front_page: yes
favorite: no
---
```

- Click **Commit changes**. That's it.

**What the fields mean**

| Field | What it does |
|---|---|
| `title` | Shown on the Articles page. Keep the quotation marks. |
| `publication` | Exactly `"Bloomberg Businessweek"` puts it under the Bloomberg menu; anything else goes under "The New York Times + More". |
| `date` | Year-month-day. The day isn't shown, so `01` is fine. Articles are sorted by this. |
| `link` | Where the title links to. |
| `cover` | File name of the image you uploaded in step 1. |
| `pdf` | File name of the PDF from step 2. Leave blank if there isn't one. |
| `front_page` | `yes` = can appear in the random covers on the home page. |
| `favorite` | `yes` = shows under "Some Favorites". |

## Change something else

- **Fix a typo in an article** → open its file in `_articles`, click the ✏️ pencil, edit, **Commit changes**.
- **Remove an article** → open its file, click **⋯** → **Delete file**.
- **Edit the About page text** → `about.md`, the text below the `---` lines.
- **Change the About photo** → upload a new image to `assets/images`, then change `photo:` in `about.md`.
- **Change your email or LinkedIn** → `_config.yml`.

## If something breaks

Every change is saved in the history, so nothing is ever lost. If the site stops updating, the most common cause is a typo between the `---` lines (a missing quotation mark or colon). Open the **Actions** tab to see a red ✗ on the change that failed, then fix or undo that file.

---

<details>
<summary>For techie helpers</summary>

Jekyll site built by GitHub Pages (no Actions workflow needed). Articles are a Jekyll collection in `_articles/` (front matter only, `output: false`); `index.html` shuffles the `front_page` covers client-side; `articles.html` filters by URL hash (`#bloomberg`, `#other`, `#favorites`). Styles in `assets/css/style.css`.

Local preview (needs Ruby 3.3; `github-pages` doesn't support Ruby 4 yet):

```
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve      # http://localhost:4000
```
</details>
