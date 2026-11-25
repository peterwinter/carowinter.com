"""Tests for check_site.py.  Run:  uv run --with pyyaml --with pytest pytest scripts"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import check_site  # noqa: E402

GOOD = """---
title: "My New Story"
publication: "Bloomberg Businessweek"
date: 2025-03-01
link: https://www.bloomberg.com/story
cover: 2025-03_bloomberg.jpg
pdf: 2025-03_bloomberg.pdf
front_page: yes
favorite: no
---
"""


@pytest.fixture
def site(tmp_path):
    (tmp_path / "_articles").mkdir()
    (tmp_path / "assets/covers").mkdir(parents=True)
    (tmp_path / "assets/pdf").mkdir()
    (tmp_path / "assets/images").mkdir()
    (tmp_path / "assets/covers/2025-03_bloomberg.jpg").write_bytes(b"x")
    (tmp_path / "assets/pdf/2025-03_bloomberg.pdf").write_bytes(b"x")
    (tmp_path / "assets/images/caroline.jpg").write_bytes(b"x")
    (tmp_path / "_config.yml").write_text("title: T\nemail: a@b.com\nlinkedin: https://x\n")
    (tmp_path / "about.md").write_text("---\nlayout: about\nphoto: caroline.jpg\n---\nBio\n")
    return tmp_path


def write(site, text, name="2025-03-my-new-story.md"):
    (site / "_articles" / name).write_text(text)


def errors(site):
    return [p for p in check_site.check_site(site) if p.error]


def only_error(site):
    errs = errors(site)
    assert len(errs) == 1, errs
    return errs[0]


def test_good_article_passes(site):
    write(site, GOOD)
    assert check_site.check_site(site) == []


def test_blank_pdf_is_fine(site):
    write(site, GOOD.replace("pdf: 2025-03_bloomberg.pdf", "pdf:"))
    assert errors(site) == []


def test_missing_cover_file(site):
    write(site, GOOD.replace("cover: 2025-03_bloomberg.jpg", "cover: nope.jpg"))
    e = only_error(site)
    assert "no file called 'nope.jpg'" in e.message and e.line == 6


def test_cover_capitalization_mismatch(site):
    (site / "assets/covers/2025-03_bloomberg.jpg").rename(site / "assets/covers/2025-03_Bloomberg.JPG")
    write(site, GOOD)
    assert "change it to:  cover: 2025-03_Bloomberg.JPG" in only_error(site).message


def test_cover_uploaded_to_wrong_folder(site):
    (site / "assets/covers/2025-03_bloomberg.jpg").rename(site / "assets/pdf/2025-03_bloomberg.jpg")
    write(site, GOOD)
    assert "found at 'assets/pdf/2025-03_bloomberg.jpg'" in only_error(site).message


def test_cover_typo_suggestion(site):
    write(site, GOOD.replace("cover: 2025-03_bloomberg.jpg", "cover: 2025-03_bloomberg.jgp"))
    assert "not an image type" in only_error(site).message
    write(site, GOOD.replace("cover: 2025-03_bloomberg.jpg", "cover: 2025-03_blomberg.jpg"))
    assert "Did you mean '2025-03_bloomberg.jpg'" in only_error(site).message


def test_heic_photo(site):
    (site / "assets/covers/photo.HEIC").write_bytes(b"x")
    write(site, GOOD.replace("cover: 2025-03_bloomberg.jpg", "cover: photo.HEIC"))
    assert "exported as JPEG" in only_error(site).message


def test_missing_pdf_file(site):
    write(site, GOOD.replace("pdf: 2025-03_bloomberg.pdf", "pdf: other.pdf"))
    assert "assets/pdf" in only_error(site).message


def test_missing_closing_quote(site):
    write(site, GOOD.replace('title: "My New Story"', 'title: "My New Story'))
    e = only_error(site)
    assert "typing mistake" in e.message and e.line is not None


def test_unquoted_title_with_colon(site):
    write(site, GOOD.replace('title: "My New Story"', "title: Berlin: A Story"))
    e = only_error(site)
    assert "typing mistake" in e.message and e.line == 2


def test_quotes_inside_title(site):
    write(site, GOOD.replace('title: "My New Story"', 'title: "The "Best" Story"'))
    assert "typing mistake" in only_error(site).message


def test_quoted_yes(site):
    write(site, GOOD.replace("front_page: yes", 'front_page: "yes"'))
    e = only_error(site)
    assert "without quotation marks" in e.message and e.line == 8


def test_partial_date(site):
    write(site, GOOD.replace("date: 2025-03-01", "date: 2025-03"))
    assert "year-month-day" in only_error(site).message


def test_missing_required_field(site):
    write(site, GOOD.replace("link: https://www.bloomberg.com/story\n", ""))
    assert "'link' is missing" in only_error(site).message


def test_link_without_https(site):
    write(site, GOOD.replace("link: https://www.bloomberg.com/story", "link: www.bloomberg.com/story"))
    assert "https://" in only_error(site).message


def test_misspelled_field(site):
    write(site, GOOD.replace("favorite: no", "favourite: no"))
    assert "Did you mean 'favorite'" in only_error(site).message


def test_no_front_matter(site):
    write(site, "title: Oops\n")
    assert "first line" in only_error(site).message


def test_no_closing_dashes(site):
    write(site, GOOD.rstrip().rsplit("---", 1)[0])
    assert "closing ---" in only_error(site).message


def test_image_uploaded_into_articles(site):
    (site / "_articles/cover.jpg").write_bytes(b"x")
    assert "images go in assets/covers" in only_error(site).message


def test_big_cover_is_only_a_warning(site):
    (site / "assets/covers/2025-03_bloomberg.jpg").write_bytes(b"x" * 2_000_000)
    write(site, GOOD)
    problems = check_site.check_site(site)
    assert len(problems) == 1 and not problems[0].error and "2.0 MB" in problems[0].message


def test_about_photo_missing(site):
    (site / "assets/images/caroline.jpg").unlink()
    assert only_error(site).file == "about.md"


def test_config_missing_email(site):
    (site / "_config.yml").write_text("title: T\nlinkedin: https://x\n")
    assert "'email'" in only_error(site).message


def test_real_site_passes():
    assert errors(check_site.ROOT) == []
