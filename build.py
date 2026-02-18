#!/usr/bin/env python3
"""Generates index.html and README.md from resume.yaml."""

import yaml
from pathlib import Path

CSS = """\
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}

  @page{size:letter;margin:10mm 14mm 10mm 14mm}

  html{
    -webkit-print-color-adjust:exact;
    print-color-adjust:exact;
  }

  body{
    font-family:'Lato',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
    font-weight:400;
    font-size:9.5pt;
    line-height:1.4;
    color:#2b2b2b;
    max-width:215.9mm;
    margin:0 auto;
    padding:10mm 14mm;
    background:#fff;
    -webkit-font-smoothing:antialiased;
    -moz-osx-font-smoothing:grayscale;
  }

  a{color:#2563EB;text-decoration:none}
  a:hover{text-decoration:underline}

  /* ════════════ HEADER ════════════ */
  .h{text-align:center;padding-bottom:1.5mm}

  .h-name{
    font-size:25pt;
    font-weight:300;
    letter-spacing:2.5px;
    text-transform:uppercase;
    color:#1a1a1a;
  }

  .h-sub{
    margin-top:0.3mm;
    font-size:9pt;
    font-weight:400;
    color:#888;
    letter-spacing:0.3px;
  }

  .h-contact{
    margin-top:0.8mm;
    font-size:8.5pt;
    font-weight:400;
    color:#444;
    letter-spacing:0.2px;
  }
  .h-contact a{color:#444}
  .h-contact .d{
    display:inline;
    margin:0 6px;
    color:#bbb;
  }

  .h-pos{
    margin-top:0.8mm;
    font-size:9.5pt;
    font-weight:400;
    color:#555;
    font-style:italic;
    line-height:1.4;
    max-width:540px;
    margin-left:auto;
    margin-right:auto;
  }

  /* ════════════ SECTIONS ════════════ */
  .s{margin-top:3mm}

  .s-title{
    font-size:9.5pt;
    font-weight:700;
    letter-spacing:2px;
    text-transform:uppercase;
    color:#1a1a1a;
    padding-bottom:1.5mm;
    border-bottom:1.5px solid #1a1a1a;
    margin-bottom:2mm;
  }

  /* ════════════ ENTRIES ════════════ */
  .e{margin-bottom:2.5mm}
  .e:last-child{margin-bottom:0}

  .e-row{
    display:flex;
    justify-content:space-between;
    align-items:baseline;
  }

  .e-org{
    font-size:10.5pt;
    font-weight:700;
    color:#1a1a1a;
  }
  .e-loc{
    font-size:8.5pt;
    font-weight:400;
    color:#666;
    flex-shrink:0;
    margin-left:12px;
  }

  .e-role{
    font-size:8.5pt;
    font-weight:400;
    font-style:italic;
    color:#444;
    margin-top:0.3mm;
  }
  .e-date{
    font-size:8.5pt;
    font-weight:400;
    color:#666;
    flex-shrink:0;
    margin-left:12px;
    white-space:nowrap;
  }

  /* ════════════ BULLET LISTS ════════════ */
  ul.b{
    margin-top:1mm;
    padding-left:14px;
    list-style:none;
  }
  ul.b li{
    position:relative;
    font-size:9.5pt;
    font-weight:400;
    color:#2b2b2b;
    line-height:1.4;
  }
  ul.b li+li{margin-top:0.8mm}
  ul.b li.proj{margin-top:1.5mm}
  ul.b li::before{
    content:"–";
    position:absolute;
    left:-14px;
    color:#999;
    font-weight:300;
  }
  ul.b li strong{
    font-weight:700;
    color:#1a1a1a;
  }

  /* ════════════ EARLIER ROLES ════════════ */
  .earlier{
    margin-top:1.5mm;
  }
  .earlier-head{
    font-size:9.5pt;
    color:#444;
  }
  .earlier-head strong{
    color:#1a1a1a;
  }
  .earlier-note{
    font-size:9pt;
    color:#555;
    margin-top:0.3mm;
    line-height:1.4;
    padding-left:14px;
  }

  /* ════════════ SKILLS ════════════ */
  .sk{
    display:grid;
    grid-template-columns:auto 1fr;
    gap:1.5mm 12px;
    font-size:9.5pt;
    margin-top:1mm;
  }
  .sk-l{
    font-weight:700;
    color:#1a1a1a;
    white-space:nowrap;
  }
  .sk-v{color:#2b2b2b}

  /* ════════════ SCREEN ════════════ */
  @media screen{
    html{background:#f0f0f0}
    body{margin:48px auto;box-shadow:0 1px 4px rgba(0,0,0,0.15)}
  }

  /* ════════════ PRINT ════════════ */
  @media print{
    body{padding:0;max-width:none}
    a{color:#2563EB !important}
    .s{break-inside:avoid}
  }"""


def html_escape(text: str) -> str:
    """Escape &, <, > for HTML, then convert thin spaces to HTML entities."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("\u2009", "&#8201;")
    return text


def render_bullet(b) -> str:
    if isinstance(b, str):
        return f"      <li>{html_escape(b)}</li>"
    heading = html_escape(b["heading"])
    text = html_escape(b["text"])
    return f'      <li class="proj"><strong>{heading}</strong> {text}</li>'


def render_bullets(bullets) -> str:
    items = "\n".join(render_bullet(b) for b in bullets)
    return f"    <ul class=\"b\">\n{items}\n    </ul>"


def render_experience_full(entry) -> str:
    lines = []
    lines.append('  <div class="e">')
    lines.append('    <div class="e-row">')
    lines.append(f'      <span class="e-org">{html_escape(entry["company"])}</span>')
    lines.append(f'      <span class="e-loc">{html_escape(entry["location"])}</span>')
    lines.append("    </div>")
    lines.append('    <div class="e-row">')
    lines.append(f'      <span class="e-role">{html_escape(entry["role"])}</span>')
    lines.append(f'      <span class="e-date">{html_escape(entry["dates"])}</span>')
    lines.append("    </div>")
    lines.append(render_bullets(entry["bullets"]))
    lines.append("  </div>")
    return "\n".join(lines)


def render_experience_earlier(entry) -> str:
    company = html_escape(entry["company"])
    role = html_escape(entry["role"])
    dates = html_escape(entry["dates"])
    note = html_escape(entry["note"])
    lines = []
    lines.append('  <div class="earlier">')
    lines.append(f'    <div class="earlier-head"><strong>{company}</strong> \u00b7 {role} \u00b7 {dates}</div>')
    lines.append(f'    <div class="earlier-note">{note}</div>')
    lines.append("  </div>")
    return "\n".join(lines)


def render_education(entry) -> str:
    lines = []
    lines.append('  <div class="e">')
    lines.append('    <div class="e-row">')
    lines.append(f'      <span class="e-org">{html_escape(entry["institution"])}</span>')
    lines.append(f'      <span class="e-loc">{html_escape(entry["location"])}</span>')
    lines.append("    </div>")
    lines.append('    <div class="e-row">')
    lines.append(f'      <span class="e-role">{html_escape(entry["degree"])}</span>')
    lines.append(f'      <span class="e-date">{html_escape(entry["dates"])}</span>')
    lines.append("    </div>")
    lines.append(render_bullets(entry["bullets"]))
    lines.append("  </div>")
    return "\n".join(lines)


def render_skills(skills) -> str:
    lines = []
    for s in skills:
        lines.append(f'    <span class="sk-l">{html_escape(s["label"])}</span>')
        lines.append(f'    <span class="sk-v">{html_escape(s["value"])}</span>')
    return "\n".join(lines)


def render_html(data: dict) -> str:
    contact = data["contact"]

    experience_blocks = []
    for entry in data["experience"]:
        if entry.get("earlier"):
            experience_blocks.append(render_experience_earlier(entry))
        else:
            experience_blocks.append(render_experience_full(entry))

    education_blocks = []
    for entry in data["education"]:
        education_blocks.append(render_education(entry))

    parts = []
    name = html_escape(data["name"])
    title = f"{name} - Resume"
    summary = html_escape(data["summary"])
    pages_url = data.get("pages_url", "")

    parts.append(f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta property="og:title" content="{title}">
<meta property="og:description" content="{summary}">
<meta property="og:type" content="website">
<meta property="og:url" content="{pages_url}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='4' fill='%231a1a1a'/><text x='16' y='22.5' font-family='system-ui,-apple-system,sans-serif' font-size='17' font-weight='700' fill='%23fff' text-anchor='middle' letter-spacing='-0.5'>AS</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400&display=swap" rel="stylesheet">
<style>""")
    parts.append(CSS)
    parts.append("""\
</style>
</head>
<body>

<!-- ══════════════ HEADER ══════════════ -->
<header class="h">""")
    parts.append(f'  <div class="h-name">{name}</div>')
    parts.append(f'  <div class="h-sub">{html_escape(data["location"])}</div>')

    github = html_escape(contact["github"])
    linkedin = html_escape(contact["linkedin"])
    contact_line = (
        f'  <div class="h-contact">\n'
        f'    <a href="https://{contact["github"]}">{github}</a>\n'
        f'    <span class="d">\u00b7</span>\n'
        f'    <a href="https://www.{contact["linkedin"]}">{linkedin}</a>\n'
        f'  </div>'
    )
    parts.append(contact_line)
    parts.append(
        f'  <div class="h-pos">{summary}</div>'
    )
    parts.append("</header>")

    # Experience
    parts.append("")
    parts.append("<!-- ══════════════ EXPERIENCE ══════════════ -->")
    parts.append('<section class="s">')
    parts.append('  <div class="s-title">Experience</div>')
    parts.append("")
    parts.append(("\n\n").join(experience_blocks))
    parts.append("</section>")

    # Education
    parts.append("")
    parts.append("<!-- ══════════════ EDUCATION ══════════════ -->")
    parts.append('<section class="s">')
    parts.append('  <div class="s-title">Education</div>')
    parts.append("\n".join(education_blocks))
    parts.append("</section>")

    # Skills
    parts.append("")
    parts.append("<!-- ══════════════ SKILLS ══════════════ -->")
    parts.append('<section class="s">')
    parts.append('  <div class="s-title">Skills &amp; Interests</div>')
    parts.append('  <div class="sk">')
    parts.append(render_skills(data["skills"]))
    parts.append("  </div>")
    parts.append("</section>")

    parts.append("")
    parts.append("</body>")
    parts.append("</html>")

    return "\n".join(parts) + "\n"


def render_md(data: dict) -> str:
    contact = data["contact"]
    lines = []
    lines.append(f"# {data['name']}")
    lines.append("")
    lines.append(
        f"{data['location']} · "
        f"[GitHub](https://{contact['github']}) · "
        f"[LinkedIn](https://www.{contact['linkedin']})"
    )
    lines.append("")
    lines.append(f"*{data['summary']}*")
    lines.append("")

    # Experience
    lines.append("## Experience")
    lines.append("")
    for entry in data["experience"]:
        if entry.get("earlier"):
            lines.append(f"**{entry['company']}** · {entry['role']} · *{entry['dates']}*")
            lines.append("")
            lines.append(entry["note"])
            lines.append("")
        else:
            lines.append(f"### {entry['company']} · {entry['location']}")
            lines.append(f"**{entry['role']}** · *{entry['dates']}*")
            lines.append("")
            for b in entry["bullets"]:
                if isinstance(b, str):
                    lines.append(f"- {b}")
                else:
                    lines.append(f"- **{b['heading']}** {b['text']}")
            lines.append("")

    # Education
    lines.append("## Education")
    lines.append("")
    for entry in data["education"]:
        lines.append(f"### {entry['institution']} · {entry['location']}")
        lines.append(f"**{entry['degree']}** · *{entry['dates']}*")
        lines.append("")
        for b in entry["bullets"]:
            lines.append(f"- {b}")
        lines.append("")

    # Skills
    lines.append("## Skills & Interests")
    lines.append("")
    for s in data["skills"]:
        lines.append(f"**{s['label']}:** {s['value']}")
    lines.append("")

    return "\n".join(lines)


def main():
    root = Path(__file__).resolve().parent
    with open(root / "resume.yaml") as f:
        data = yaml.safe_load(f)

    html = render_html(data)
    (root / "index.html").write_text(html)
    print("Wrote index.html")

    md = render_md(data)
    (root / "README.md").write_text(md)
    print("Wrote README.md")


if __name__ == "__main__":
    main()
