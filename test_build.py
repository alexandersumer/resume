#!/usr/bin/env python3
"""Tests for resume build system."""

import subprocess
import yaml
from pathlib import Path

from build import (
    html_escape,
    render_bullet,
    render_bullets,
    render_experience_full,
    render_experience_earlier,
    render_education,
    render_skills,
    render_html,
    render_md,
)

ROOT = Path(__file__).resolve().parent

# ── Golden reference: build output must match index.html on disk ──

GOLDEN_HTML = (ROOT / "index.html").read_text()


def load_data():
    with open(ROOT / "resume.yaml") as f:
        return yaml.safe_load(f)


# ═══════════════════════════════════════════════════════════════
#  Golden-master: generated HTML must match the original exactly
# ═══════════════════════════════════════════════════════════════

def test_html_matches_golden():
    html = render_html(load_data())
    assert html == GOLDEN_HTML, _diff_hint(GOLDEN_HTML, html)


def _diff_hint(expected, actual):
    """Return first divergence to make failures actionable."""
    for i, (a, b) in enumerate(zip(expected, actual)):
        if a != b:
            ctx = expected[max(0, i - 40):i + 40]
            return f"First diff at char {i}: ...{ctx!r}..."
    if len(expected) != len(actual):
        return f"Length mismatch: expected {len(expected)}, got {len(actual)}"
    return "Unknown diff"


# ═══════════════════════════════════════════════════════════════
#  html_escape
# ═══════════════════════════════════════════════════════════════

def test_escape_ampersand():
    assert html_escape("R&D") == "R&amp;D"

def test_escape_angle_brackets():
    assert html_escape("<b>hi</b>") == "&lt;b&gt;hi&lt;/b&gt;"

def test_escape_thin_space():
    assert html_escape("20\u2009GB") == "20&#8201;GB"

def test_escape_combined():
    assert html_escape("A & B < C\u2009D") == "A &amp; B &lt; C&#8201;D"

def test_escape_passthrough():
    assert html_escape("plain text") == "plain text"


# ═══════════════════════════════════════════════════════════════
#  Bullet rendering
# ═══════════════════════════════════════════════════════════════

def test_bullet_plain():
    result = render_bullet("Simple point.")
    assert result == "      <li>Simple point.</li>"

def test_bullet_with_heading():
    result = render_bullet({"heading": "Title:", "text": "Description."})
    assert result == "      <li><strong>Title:</strong> Description.</li>"

def test_bullet_escapes_content():
    result = render_bullet("Uses <foo> & bar")
    assert "&lt;foo&gt;" in result
    assert "&amp;" in result

def test_bullets_list():
    result = render_bullets(["First.", "Second."])
    assert result.startswith('    <ul class="b">')
    assert result.endswith("    </ul>")
    assert result.count("<li>") == 2


# ═══════════════════════════════════════════════════════════════
#  Experience rendering
# ═══════════════════════════════════════════════════════════════

def test_experience_full_structure():
    entry = {
        "company": "Acme",
        "location": "NYC",
        "role": "Engineer",
        "dates": "2020 – Present",
        "bullets": ["Built things."],
    }
    html = render_experience_full(entry)
    assert 'class="e-org"' in html
    assert 'class="e-loc"' in html
    assert 'class="e-role"' in html
    assert 'class="e-date"' in html
    assert "Built things." in html

def test_experience_earlier_structure():
    entry = {
        "company": "StartupCo",
        "dates": "2018 – 2019",
        "earlier": True,
        "note": "Did good work.",
    }
    html = render_experience_earlier(entry)
    assert 'class="earlier"' in html
    assert 'class="earlier-note"' in html
    assert "Did good work." in html
    assert "e-loc" not in html  # no location for earlier entries

def test_experience_full_escapes():
    entry = {
        "company": "A&B Corp",
        "location": "Here",
        "role": "Dev",
        "dates": "2020",
        "bullets": ["20\u2009GB storage"],
    }
    html = render_experience_full(entry)
    assert "A&amp;B Corp" in html
    assert "20&#8201;GB" in html


# ═══════════════════════════════════════════════════════════════
#  Education rendering
# ═══════════════════════════════════════════════════════════════

def test_education_structure():
    entry = {
        "institution": "MIT",
        "location": "Cambridge",
        "degree": "BS CS",
        "dates": "2016 – 2020",
        "bullets": ["Dean's list."],
    }
    html = render_education(entry)
    assert 'class="e-org"' in html
    assert "MIT" in html
    assert "Dean's list." in html


# ═══════════════════════════════════════════════════════════════
#  Skills rendering
# ═══════════════════════════════════════════════════════════════

def test_skills_structure():
    skills = [{"label": "Languages", "value": "Python, Go"}]
    html = render_skills(skills)
    assert 'class="sk-l"' in html
    assert 'class="sk-v"' in html
    assert "Languages" in html
    assert "Python, Go" in html


# ═══════════════════════════════════════════════════════════════
#  Full HTML structure
# ═══════════════════════════════════════════════════════════════

def test_html_is_valid_document():
    html = render_html(load_data())
    assert html.startswith("<!DOCTYPE html>")
    assert html.strip().endswith("</html>")
    assert "<style>" in html
    assert "</style>" in html

def test_html_has_inline_svg_favicon():
    html = render_html(load_data())
    assert 'rel="icon"' in html
    assert "data:image/svg+xml" in html
    assert ">AS</text>" in html

def test_html_og_tags_data_driven():
    data = load_data()
    html = render_html(data)
    assert f'og:title" content="{data["name"]} - Resume"' in html
    assert f'og:url" content="{data["pages_url"]}"' in html
    assert 'og:description" content="' in html
    # OG description should contain start of summary
    assert data["summary"][:40] in html

def test_html_contains_all_sections():
    html = render_html(load_data())
    assert "HEADER" in html
    assert "EXPERIENCE" in html
    assert "EDUCATION" in html
    assert "SKILLS" in html

def test_html_contains_all_companies():
    html = render_html(load_data())
    assert "Atlassian" in html
    assert "Sympli" in html
    assert "WiseTech Global" in html

def test_html_contains_contact_info():
    html = render_html(load_data())
    assert "github.com/alexandersumer" in html
    assert "linkedin.com/in/alexandersumer" in html

def test_html_thin_space_rendered():
    html = render_html(load_data())
    assert "20&#8201;GB" in html


# ═══════════════════════════════════════════════════════════════
#  YAML schema validation
# ═══════════════════════════════════════════════════════════════

def test_yaml_has_required_top_level_keys():
    data = load_data()
    for key in ("name", "location", "contact", "summary", "experience", "education", "skills"):
        assert key in data, f"Missing top-level key: {key}"

def test_yaml_contact_has_all_fields():
    contact = load_data()["contact"]
    for key in ("github", "linkedin"):
        assert key in contact, f"Missing contact field: {key}"

def test_yaml_experience_types():
    data = load_data()
    full = [e for e in data["experience"] if not e.get("earlier")]
    earlier = [e for e in data["experience"] if e.get("earlier")]
    assert len(full) >= 1
    assert len(earlier) >= 1
    for e in full:
        assert "bullets" in e
        assert "role" in e
    for e in earlier:
        assert "note" in e

def test_yaml_bullets_polymorphic():
    data = load_data()
    bullets = data["experience"][0]["bullets"]
    has_plain = any(isinstance(b, str) for b in bullets)
    has_dict = any(isinstance(b, dict) for b in bullets)
    assert has_plain, "Expected at least one plain string bullet"
    assert has_dict, "Expected at least one heading/text bullet"


# ═══════════════════════════════════════════════════════════════
#  Markdown output
# ═══════════════════════════════════════════════════════════════

def test_md_starts_with_name():
    md = render_md(load_data())
    assert "# Alexander Sumer" in md

def test_md_contains_no_html():
    md = render_md(load_data())
    assert "<div" not in md
    assert "<span" not in md
    assert "<ul" not in md

def test_md_contains_all_sections():
    md = render_md(load_data())
    assert "## Experience" in md
    assert "## Education" in md
    assert "## Skills & Interests" in md

def test_md_contains_all_companies():
    md = render_md(load_data())
    assert "Atlassian" in md
    assert "Sympli" in md
    assert "WiseTech Global" in md

def test_md_contact_links():
    md = render_md(load_data())
    assert "[GitHub]" in md
    assert "[LinkedIn]" in md

def test_md_no_resume_heading():
    md = render_md(load_data())
    lines = md.strip().split("\n")
    # No line should contain just "resume" as a heading
    for line in lines:
        stripped = line.strip().lstrip("#").strip()
        assert stripped.lower() != "resume"

def test_md_ends_with_newline():
    md = render_md(load_data())
    assert md.endswith("\n")

def test_md_earlier_entries_not_h3():
    """Earlier roles should be bold inline, not ### headings."""
    md = render_md(load_data())
    assert "### Sympli" not in md
    assert "**Sympli**" in md


# ═══════════════════════════════════════════════════════════════
#  build.py CLI integration
# ═══════════════════════════════════════════════════════════════

def test_build_script_runs_cleanly():
    result = subprocess.run(
        ["python3", "build.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "Wrote index.html" in result.stdout
    assert "Wrote README.md" in result.stdout

def test_build_output_files_exist():
    subprocess.run(["python3", "build.py"], cwd=ROOT, check=True)
    assert (ROOT / "index.html").exists()
    assert (ROOT / "README.md").exists()
