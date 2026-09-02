"""Apply the shared header/footer/font block to every page. Run from the site root:
    python _build/patch_pages.py
Rewrites the <header>...</header>, <footer>...</footer> blocks and the Google Fonts link
in every HTML page under the root and blog/. Idempotent."""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = '<svg class="mark" viewBox="0 0 64 64" aria-hidden="true"><path d="M10 28 H54 V56 H10 Z" fill="#c68b4f"/><path d="M10 28 L4 12 L24 18 L32 28 Z M54 28 L60 12 L40 18 L32 28 Z" fill="#dfae78"/><path d="M24 18 L32 4 L40 18 L32 28 Z" fill="#f0d2ab"/><rect x="29.5" y="28" width="5" height="28" fill="#f26b1d"/><path d="M10 28 H54" stroke="#a9713a" stroke-width="1.5"/><rect x="14" y="44" width="11" height="7" rx="1" fill="#ffffff"/></svg>'
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">'

def header(prefix, current=None):
    def li(href, label, key):
        cur = ' aria-current="page"' if key == current else ''
        return f'      <li><a href="{href}"{cur}>{label}</a></li>'
    return f'''<header>
  <div class="wrap nav">
    <a class="brand" href="{prefix}">{MARK}<span class="word"><b>Way To Store</b><small>Self Storage</small></span></a>
    <ul>
{li(prefix + "#storage", "Storage", "storage")}
{li(prefix + "#offer", "Offer", "offer")}
{li(prefix + "#faq", "Questions", "faq")}
{li(prefix + "#location", "Location", "location")}
{li(prefix + "blog/", "Blog", "blog")}
    </ul>
    <a class="btn" href="tel:+12504427977">250-442-7977</a>
  </div>
</header>'''

def footer(prefix):
    return f'''<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="{prefix}">{MARK}<span class="word"><b>Way To Store</b><small>Self Storage</small></span></a>
        <p>Heated indoor storage with level entry and a fenced compound for RVs, boats, trailers and containers. Locally owned, on Sagamore Road in Grand Forks.</p>
      </div>
      <div>
        <h3>Contact</h3>
        <ul>
          <li><a href="tel:+12504427977">250-442-7977</a></li>
          <li><a href="mailto:info@waytostore.ca">info@waytostore.ca</a></li>
          <li>136 Sagamore Road<br>Grand Forks, BC V0H 1H4</li>
        </ul>
      </div>
      <div>
        <h3>Site</h3>
        <ul>
          <li><a href="{prefix}#storage">Storage</a></li>
          <li><a href="{prefix}#offer">Introductory offer</a></li>
          <li><a href="{prefix}#faq">Common questions</a></li>
          <li><a href="{prefix}blog/">Blog</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">Way To Store Self Storage is operated by 1436894 B.C. Ltd., Grand Forks, British Columbia.</div>
  </div>
</footer>'''

def patch(path, prefix, current):
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<header>.*?</header>", header(prefix, current), s, count=1, flags=re.S)
    s = re.sub(r"<footer>.*?</footer>", footer(prefix), s, count=1, flags=re.S)
    s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">', FONTS, s, count=1)
    path.write_text(s, encoding="utf-8", newline="\n")
    print("patched", path.relative_to(ROOT))

patch(ROOT / "index.html", "./", None)
patch(ROOT / "404.html", "/", None)
for p in sorted((ROOT / "blog").glob("*.html")):
    patch(p, "../", "blog")
