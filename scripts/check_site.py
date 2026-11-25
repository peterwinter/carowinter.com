#!/usr/bin/env python3
"""Check the website's content for mistakes before it is published.

Runs automatically on GitHub every time something is changed (see
.github/workflows/publish.yml). If it finds an error, the site is not updated
and the change gets a red X with a message explaining what to fix.

Run it yourself with:  python3 scripts/check_site.py   (needs: pip install pyyaml)
"""
from __future__ import annotations

import datetime
import difflib
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = ["title", "publication", "date", "link", "cover"]
OPTIONAL = ["pdf", "front_page", "favorite"]
YES_NO = ["front_page", "favorite"]
IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
BIG_IMAGE_MB = 1


@dataclass
class Problem:
    file: str
    message: str
    line: int | None = None
    error: bool = True  # False = warning (site still publishes)


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_front_matter(path: Path, root: Path) -> tuple[dict | None, list[Problem]]:
    """Return the settings between the two '---' lines at the top of a file."""
    name = rel(path, root)
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, [Problem(name, "The first line of this file must be exactly --- (three dashes).", 1)]
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return None, [Problem(name, "The settings at the top of this file need a closing --- line.", 1)]
    try:
        data = yaml.safe_load("\n".join(lines[1:end])) or {}
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        line = mark.line + 2 if mark else None
        where = f" on or just before line {line}" if line else ""
        return None, [Problem(
            name,
            f"There is a typing mistake{where}. Common causes: a missing quotation mark, "
            "a quotation mark inside a title (use ' instead), or a missing space after a colon. "
            f"(Details: {getattr(e, 'problem', e)})",
            line,
        )]
    if not isinstance(data, dict):
        return None, [Problem(name, "The settings at the top of this file should look like  name: value  on each line.", 2)]
    data["__lines__"] = {
        line.split(":", 1)[0].strip(): i + 1
        for i, line in enumerate(lines[: end + 1])
        if ":" in line and not line.startswith((" ", "\t"))
    }
    return data, []


def find_elsewhere(filename: str, root: Path) -> list[str]:
    """Look for a file with this name anywhere in the site (to spot wrong-folder uploads)."""
    hits = []
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith((".", "_site", "vendor"))]
        for f in files:
            if f.lower() == filename.lower():
                hits.append(rel(Path(dirpath) / f, root))
    return hits


def check_file_exists(value, folder: str, field: str, article: str, line: int | None, root: Path,
                      allowed_types: set[str] | None = None) -> list[Problem]:
    problems: list[Problem] = []
    filename = str(value).strip()
    target_dir = root / folder
    if "/" in filename:
        return [Problem(article, f"{field}: should be just the file name (like  photo.jpg ), without any folder.", line)]
    suffix = Path(filename).suffix.lower()
    if allowed_types and suffix not in allowed_types:
        hint = " iPhone photos (.heic) need to be exported as JPEG first." if suffix in {".heic", ".heif"} else ""
        return [Problem(article, f"{field}: '{filename}' is not an image type web browsers can show. Use .jpg or .png.{hint}", line)]
    existing = sorted(p.name for p in target_dir.iterdir()) if target_dir.is_dir() else []
    # Compare names exactly: Macs ignore capital letters in file names, but the web server doesn't.
    if filename in existing:
        return []
    same_but_case = [f for f in existing if f.lower() == filename.lower()]
    if same_but_case:
        msg = (f"{field}: '{filename}' was not found, but '{same_but_case[0]}' was. "
               f"Capital letters must match exactly, so change it to:  {field}: {same_but_case[0]}")
    else:
        msg = f"{field}: there is no file called '{filename}' in the {folder} folder."
        elsewhere = find_elsewhere(filename, root)
        if elsewhere:
            msg += f" It was found at '{elsewhere[0]}'; it needs to be uploaded to the {folder} folder instead."
        else:
            close = difflib.get_close_matches(filename, existing, n=1, cutoff=0.8)
            if close:
                msg += f" Did you mean '{close[0]}'?"
            else:
                msg += f" Upload it to {folder} (or check the spelling)."
    problems.append(Problem(article, msg, line))
    return problems


def check_article(path: Path, root: Path) -> list[Problem]:
    name = rel(path, root)
    data, problems = read_front_matter(path, root)
    if data is None:
        return problems
    lines = data.pop("__lines__")

    for key in data:
        if key not in REQUIRED + OPTIONAL:
            close = difflib.get_close_matches(str(key), REQUIRED + OPTIONAL, n=1)
            hint = f" Did you mean '{close[0]}'?" if close else f" Allowed: {', '.join(REQUIRED + OPTIONAL)}."
            problems.append(Problem(name, f"Unknown setting '{key}'.{hint}", lines.get(key)))

    for key in REQUIRED:
        if data.get(key) in (None, ""):
            problems.append(Problem(name, f"'{key}' is missing or empty. Every article needs: {', '.join(REQUIRED)}.", lines.get(key)))

    date = data.get("date")
    if date not in (None, "") and not isinstance(date, (datetime.date, datetime.datetime)):
        problems.append(Problem(name, f"date: '{date}' is not a full date. Write it as year-month-day without quotes, like  date: 2025-03-01", lines.get("date")))

    link = data.get("link")
    if link and not str(link).startswith(("http://", "https://")):
        problems.append(Problem(name, f"link: should be a full web address starting with https://", lines.get("link")))

    for key in YES_NO:
        if key in data and not isinstance(data[key], bool):
            problems.append(Problem(name, f"{key}: must be  yes  or  no  (without quotation marks). It is currently: {data[key]!r}", lines.get(key)))

    if data.get("cover"):
        problems += check_file_exists(data["cover"], "assets/covers", "cover", name, lines.get("cover"), root, IMAGE_TYPES)
        cover = root / "assets/covers" / str(data["cover"]).strip()
        if cover.is_file() and cover.stat().st_size > BIG_IMAGE_MB * 1_000_000:
            mb = cover.stat().st_size / 1_000_000
            problems.append(Problem(name, f"The cover image is {mb:.1f} MB, which makes the page slow. Under 0.5 MB is ideal (about 800 pixels wide is plenty).", lines.get("cover"), error=False))

    if data.get("pdf"):
        problems += check_file_exists(data["pdf"], "assets/pdf", "pdf", name, lines.get("pdf"), root, {".pdf"})

    return problems


def check_about(root: Path) -> list[Problem]:
    path = root / "about.md"
    if not path.is_file():
        return [Problem("about.md", "about.md is missing. The About page needs it.")]
    data, problems = read_front_matter(path, root)
    if data is None:
        return problems
    lines = data.pop("__lines__")
    if data.get("photo"):
        problems += check_file_exists(data["photo"], "assets/images", "photo", "about.md", lines.get("photo"), root, IMAGE_TYPES)
    return problems


def check_config(root: Path) -> list[Problem]:
    try:
        data = yaml.safe_load((root / "_config.yml").read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        line = mark.line + 1 if mark else None
        return [Problem("_config.yml", "There is a typing mistake in this file (often a missing space after a colon).", line)]
    problems = []
    for key in ["title", "email", "linkedin"]:
        if not data.get(key):
            problems.append(Problem("_config.yml", f"'{key}' is missing or empty."))
    return problems


def check_site(root: Path = ROOT) -> list[Problem]:
    problems = check_config(root) + check_about(root)
    articles = root / "_articles"
    for path in sorted(articles.iterdir()):
        if path.name.startswith("."):
            continue
        if path.suffix != ".md":
            hint = ""
            if path.suffix.lower() in IMAGE_TYPES | {".heic"}:
                hint = " It looks like an image; images go in assets/covers."
            elif path.suffix.lower() == ".pdf":
                hint = " PDFs go in assets/pdf."
            problems.append(Problem(rel(path, root), f"Files in _articles must end in .md.{hint}"))
            continue
        problems += check_article(path, root)
    return problems


def report(problems: list[Problem], n_articles: int) -> None:
    on_github = os.environ.get("GITHUB_ACTIONS") == "true"
    errors = [p for p in problems if p.error]
    warnings = [p for p in problems if not p.error]
    for p in problems:
        kind = "error" if p.error else "warning"
        where = f"{p.file}" + (f", line {p.line}" if p.line else "")
        print(f"{'ERROR' if p.error else 'warning'}: {where}: {p.message}")
        if on_github:
            loc = f"file={p.file}" + (f",line={p.line}" if p.line else "")
            print(f"::{kind} {loc}::{p.message}")
    if errors:
        headline = f"Found {len(errors)} problem(s). The website was NOT updated. Fix the file(s) above and the site will update automatically."
    else:
        headline = f"All {n_articles} articles look good" + (f" ({len(warnings)} warning(s), site still publishes)." if warnings else ".")
    print(headline)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"### {'❌' if errors else '✅'} {headline}\n\n")
            for p in problems:
                where = f"`{p.file}`" + (f" line {p.line}" if p.line else "")
                f.write(f"- {'**Error**' if p.error else 'Warning'} in {where}: {p.message}\n")


def main() -> int:
    problems = check_site(ROOT)
    n = len(list((ROOT / "_articles").glob("*.md")))
    report(problems, n)
    return 1 if any(p.error for p in problems) else 0


if __name__ == "__main__":
    sys.exit(main())
