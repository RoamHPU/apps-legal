#!/usr/bin/env python3
"""Convert the per-app markdown legal docs into static HTML pages for GitHub Pages."""
import os
import markdown
from pathlib import Path

BASE = Path(__file__).parent
ROOT = BASE.parent

PAGES = [
    ("receiptsnap", "privacy", "ReceiptSnap by Roam — Privacy Policy",
     ROOT / "receipt-snap" / "store" / "privacy-policy.md"),
    ("receiptsnap", "support", "ReceiptSnap by Roam — Support",
     ROOT / "receipt-snap" / "store" / "support.md"),
    ("receiptsnap", "terms", "ReceiptSnap by Roam — Terms of Use",
     ROOT / "receipt-snap" / "store" / "terms.md"),
    ("filesnap-docs", "privacy", "FileSnap Docs by Roam — Privacy Policy",
     ROOT / "file-snap-docs" / "store" / "privacy-policy.md"),
    ("filesnap-docs", "support", "FileSnap Docs by Roam — Support",
     ROOT / "file-snap-docs" / "store" / "support.md"),
    ("filesnap-docs", "terms", "FileSnap Docs by Roam — Terms of Use",
     ROOT / "file-snap-docs" / "store" / "terms.md"),
]

PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="robots" content="index,follow">
<style>
:root {{
  --fg: #1a1a1a;
  --muted: #555;
  --bg: #ffffff;
  --accent: #0066cc;
  --rule: #e6e6e6;
  --code-bg: #f4f4f4;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --fg:#eee; --muted:#aaa; --bg:#111; --accent:#6cb6ff; --rule:#333; --code-bg:#1d1d1d; }}
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: var(--bg); color: var(--fg); }}
body {{ font: 16px/1.6 -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif; }}
main {{ max-width: 720px; margin: 0 auto; padding: 32px 20px 64px; }}
nav.crumbs {{ font-size: 13px; color: var(--muted); margin-bottom: 12px; }}
nav.crumbs a {{ color: var(--muted); }}
h1 {{ font-size: 28px; line-height: 1.2; margin: 8px 0 24px; }}
h2 {{ font-size: 20px; margin: 32px 0 12px; padding-bottom: 6px; border-bottom: 1px solid var(--rule); }}
h3 {{ font-size: 16px; margin: 24px 0 8px; }}
p, li {{ color: var(--fg); }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 14px; }}
th, td {{ padding: 8px 10px; text-align: left; border: 1px solid var(--rule); vertical-align: top; }}
th {{ background: var(--code-bg); }}
code {{ background: var(--code-bg); padding: 1px 5px; border-radius: 3px; font: 13px/1.4 ui-monospace, "SF Mono", Menlo, Consolas, monospace; }}
pre {{ background: var(--code-bg); padding: 12px 14px; border-radius: 6px; overflow-x: auto; }}
pre code {{ background: none; padding: 0; }}
hr {{ border: 0; border-top: 1px solid var(--rule); margin: 32px 0; }}
footer {{ font-size: 12px; color: var(--muted); margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--rule); }}
em {{ color: var(--muted); font-style: normal; }}
blockquote {{ border-left: 3px solid var(--rule); margin: 16px 0; padding: 4px 16px; color: var(--muted); }}
</style>
</head>
<body>
<main>
<nav class="crumbs"><a href="/apps-legal/">Roam HPU Apps — Legal</a></nav>
{body}
<footer>© 2026 Roam — Human Potential Unleashed Pty Ltd. ABN 58 663 682 906.</footer>
</main>
</body>
</html>
"""

INDEX_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Roam HPU Apps — Legal &amp; Support</title>
<style>
body {{ font: 16px/1.6 -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif; max-width: 720px; margin: 0 auto; padding: 32px 20px; color: #1a1a1a; }}
@media (prefers-color-scheme: dark) {{ body {{ background:#111; color:#eee; }} a {{ color:#6cb6ff; }} }}
h1 {{ font-size: 24px; }}
h2 {{ font-size: 18px; margin-top: 32px; }}
ul {{ padding-left: 20px; }}
a {{ color: #0066cc; }}
</style>
</head>
<body>
<h1>Roam HPU Apps — Legal &amp; Support</h1>
<p>Privacy policies, terms of use, and support pages for our published iPhone apps.</p>
<h2>ReceiptSnap by Roam</h2>
<ul>
<li><a href="receiptsnap/privacy.html">Privacy Policy</a></li>
<li><a href="receiptsnap/support.html">Support</a></li>
<li><a href="receiptsnap/terms.html">Terms of Use</a></li>
</ul>
<h2>FileSnap Docs by Roam</h2>
<ul>
<li><a href="filesnap-docs/privacy.html">Privacy Policy</a></li>
<li><a href="filesnap-docs/support.html">Support</a></li>
<li><a href="filesnap-docs/terms.html">Terms of Use</a></li>
</ul>
<p style="margin-top:48px;font-size:12px;color:#666">© 2026 Roam — Human Potential Unleashed Pty Ltd. ABN 58 663 682 906. Contact: ben.lewis@roamhpu.co</p>
</body>
</html>
"""

md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])

for app, page, title, src in PAGES:
    src_text = src.read_text()
    md.reset()
    body = md.convert(src_text)
    out_path = BASE / app / f"{page}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(PAGE_TEMPLATE.format(title=title, body=body))
    print(f"wrote {out_path.relative_to(BASE)}")

(BASE / "index.html").write_text(INDEX_TEMPLATE)
print("wrote index.html")

# .nojekyll so GitHub Pages serves files as-is, no Jekyll build step
(BASE / ".nojekyll").touch()
print("wrote .nojekyll")
