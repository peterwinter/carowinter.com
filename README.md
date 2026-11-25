# carowinter.com

This is everything that makes up **carowinter.com**: the articles, images, PDFs and design. You manage it all on **github.com in your web browser**. There's nothing to install.

**How it works:** you change a file here and click **Commit changes**. GitHub checks your change for mistakes and, if it looks good, updates the live website within about 2 minutes. If it finds a mistake, the website stays as it was and GitHub tells you what to fix. You can't break the live site by accident, and every earlier version is saved.

**Contents**

1. [Getting set up (once)](#1-getting-set-up-once)
2. [Add an article](#2-add-an-article)
3. [Edit or remove an article](#3-edit-or-remove-an-article)
4. [Change the About page](#4-change-the-about-page)
5. [Check that your change is live](#5-check-that-your-change-is-live)
6. [If you see a red ✗](#6-if-you-see-a-red-)
7. [Other things you can change](#7-other-things-you-can-change)

---

## 1. Getting set up (once)

1. Sign in at [github.com](https://github.com).
2. Bookmark this page (the repository's main page). This is "home base" for the website.
3. GitHub will ask you to turn on **two-factor authentication** (a second login step using your phone). Follow its instructions. The easiest choice is a **passkey** (Touch ID on your Mac), or the **GitHub Mobile** app on your phone.

That's it.

> **A few words you'll see on GitHub**
> - **Repository** (or "repo"): this whole collection of files.
> - **Commit**: saving a change. Each commit is kept forever in the history.
> - **main**: the version of the files that's on the live website. You always work on main.

---

## 2. Add an article

Do these three steps in order. Each one ends with clicking **Commit changes**.

### Step 1: Upload the cover image

1. Click the **`assets`** folder, then **`covers`**.
2. Click **Add file** (top right) → **Upload files**.
3. Drag in the image. Name it like the others, for example **`2025-03_bloomberg.jpg`** (year-month_publication). It's easiest to rename it on your Mac *before* uploading.
4. Click **Commit changes**.

Tips:
- **Square images** look best. About **800 × 800 pixels** is plenty; huge images make the page slow.
- Use **.jpg** or **.png**. iPhone photos (.heic) won't show in most browsers: open them in Preview → File → Export → JPEG first.

### Step 2: Upload the PDF (optional)

Same as Step 1, but in the **`assets`** → **`pdf`** folder. Name it like **`2025-03_bloomberg.pdf`**.

The browser can upload files up to **25 MB**. If a PDF is bigger, ask Peter.

### Step 3: Create the article

1. Go back to home base and click the **`_articles`** folder.
2. Click **Add file** → **Create new file**.
3. In the name box, type the date and a few words of the title, ending in **`.md`**. For example: **`2025-03-my-new-story.md`**
4. Copy this template (there's a copy button in the top-right corner of the box), paste it in, and fill it out:

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

5. Click **Commit changes** (top right), then **Commit changes** again in the pop-up.

Wait about 2 minutes and the article is on the site.

**What each line means**

| Line | What to write |
|---|---|
| `title` | The headline, **inside quotation marks**. If the headline itself contains a quote mark, use a single one: `"Why 'Free' Isn't"` |
| `publication` | Also in quotation marks. Exactly `"Bloomberg Businessweek"` puts it under the Bloomberg menu; anything else goes under "The New York Times + More". |
| `date` | Year-month-day: `2025-03-01`. The day isn't shown on the site, so `01` is fine. Articles are sorted newest first. |
| `link` | The web address of the article, starting with `https://` |
| `cover` | The **exact** file name of the image from Step 1, including capital letters. |
| `pdf` | The exact file name of the PDF from Step 2. If there's no PDF, leave it empty: `pdf:` |
| `front_page` | `yes` = it can be one of the random covers on the home page. Otherwise `no`. |
| `favorite` | `yes` = it shows under "Some Favorites". Otherwise `no`. |

Keep the `---` lines at the top and bottom, and keep a space after each colon.

---

## 3. Edit or remove an article

**To edit:** open **`_articles`**, click the article's file, click the **pencil ✏️** (top right), make your change, then **Commit changes**.

**To remove:** open the file, click the **⋯** button (top right) → **Delete file** → **Commit changes**. You can also delete its cover and PDF the same way, but that's optional.

**To stop it showing on the home page** without removing it, change `front_page: yes` to `front_page: no`.

---

## 4. Change the About page

**The text:** open **`about.md`**, click the pencil ✏️, and edit the text **below** the second `---` line. Then **Commit changes**.

- Leave a blank line between paragraphs.
- For *italics*, put asterisks around words: `*The New York Times Magazine*`
- For a link: `[Knight Science Journalism](https://ksj.mit.edu)`

**The photo:**

1. Upload the new photo to **`assets`** → **`images`** (like Step 1 above).
2. Open **`about.md`**, click the pencil, and change the `photo:` line to the new file name, for example `photo: caroline-2025.jpg`.
3. **Commit changes**.

---

## 5. Check that your change is live

On home base, next to the latest change (just above the list of files), there's a small symbol:

| Symbol | Meaning |
|---|---|
| 🟡 yellow dot | GitHub is checking and publishing (about 2 minutes). |
| ✅ green check | Done. Your change is live. |
| ❌ red ✗ | Something needs fixing. See below. The website still shows the previous version. |

Then look at carowinter.com. If you don't see your change, your browser may be showing an old copy: press **⌘ Cmd + Shift + R** to reload.

---

## 6. If you see a red ✗

You'll also get an email from GitHub saying the "Publish website" run failed.

1. Click the red ✗, then **Details** next to "Check for mistakes".
2. The message names the file and the problem, and usually says how to fix it. For example:
   - *cover: there is no file called '2025-03-bloomberg.jpg' in the assets/covers folder. Did you mean '2025-03_bloomberg.jpg'?*
   - *There is a typing mistake on or just before line 2. Common causes: a missing quotation mark…*
3. Open that file, click the pencil ✏️, fix it, and **Commit changes**. When the check passes, the site updates on its own.

**Common causes**
- The `cover:` or `pdf:` name doesn't exactly match the uploaded file (watch capital letters, `-` vs `_`, `.jpg` vs `.jpeg`).
- A missing quotation mark around a title, or a missing space after a colon.
- The article was created before its image was uploaded. Just upload the image and the ✗ clears.

Stuck? Ask Peter. Nothing is ever lost: every earlier version of every file is saved in the history.

---

## 7. Other things you can change

All in **`_config.yml`** (click it, then the pencil):
- **Email address** and **LinkedIn link** in the footer.
- **How many covers** show on the home page (`home_page_covers: 12`).

Ask Peter before changing other files. They control the design and how the site is built.

---

<details>
<summary><b>For techie helpers</b></summary>

**Stack:** Jekyll (GitHub Pages' `github-pages` gem), published by the GitHub Actions workflow in `.github/workflows/publish.yml`: check → build → deploy. Repo Settings → Pages → Source must be **GitHub Actions**.

**Layout**
- `_articles/*.md`: one file per article, front matter only (Jekyll collection with `output: false`).
- `index.html`: home page; shuffles `front_page` covers client-side.
- `articles.html`: article grid; filters by URL hash (`#bloomberg`, `#other`, `#favorites`).
- `about.md` + `_layouts/about.html`: About page.
- `_layouts/`, `_includes/`, `assets/css/style.css`: design.
- `scripts/check_site.py`: content validator run before every deploy. Errors block the deploy; warnings don't.

**Tests and checks** (needs [uv](https://docs.astral.sh/uv/))

```
uv run --with pyyaml --with pytest pytest scripts   # tests for the checker
uv run --with pyyaml python scripts/check_site.py    # check the content
```

**Local preview** (needs Ruby 3.3; `github-pages` doesn't support Ruby 4 yet)

```
brew install ruby@3.3
export PATH=/opt/homebrew/opt/ruby@3.3/bin:$PATH
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve      # http://localhost:4000
```
</details>
