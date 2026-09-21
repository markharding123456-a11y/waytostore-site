"""Site stamper. Run from the site root:   python _build/patch_pages.py
For every HTML page it (idempotently):
  - rewrites <header> (desktop nav + CSS-only phone menu) and <footer>
  - swaps the fonts block for self-hosted preloads, versions styles.css
  - ensures og:locale + twitter:card
  - GENERATES FAQPage JSON-LD from the visible <div class="faq"> block
  - GENERATES BreadcrumbList JSON-LD from the visible <div class="crumbs"> block
Edit this script, not the pages, for nav / footer / schema-generation changes."""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://waytostore.ca/"
CSS_VERSION = '9'
MARK = '<svg class="mark" viewBox="0 0 64 64" aria-hidden="true"><path d="M10 28 H54 V56 H10 Z" fill="#c68b4f"/><path d="M10 28 L4 12 L24 18 L32 28 Z M54 28 L60 12 L40 18 L32 28 Z" fill="#dfae78"/><path d="M24 18 L32 4 L40 18 L32 28 Z" fill="#f0d2ab"/><rect x="29.5" y="28" width="5" height="28" fill="#c8551b"/><path d="M10 28 H54" stroke="#a9713a" stroke-width="1.5"/><rect x="14" y="44" width="11" height="7" rx="1" fill="#ffffff"/></svg>'

NAV = [("heated-storage-grand-forks.html", "Heated storage", "heated"),
       ("rv-boat-trailer-storage-grand-forks.html", "RV &amp; boat storage", "rv"),
       ("#offer", "Offer", "offer"),
       ("#faq", "Questions", "faq"),
       ("#location", "Location", "location"),
       ("blog/", "Blog", "blog")]


def header(prefix, current=None):
    def items(indent):
        out = []
        for href, label, key in NAV:
            cur = ' aria-current="page"' if key == current else ''
            out.append(f'{indent}<li><a href="{prefix}{href}"{cur}>{label}</a></li>')
        return "\n".join(out)
    return f'''<header>
  <div class="wrap nav">
    <a class="brand" href="{prefix}">{MARK}<span class="word"><b>Way To Store</b><small>Self Storage</small></span></a>
    <ul class="nav-desktop">
{items("      ")}
    </ul>
    <a class="btn" href="tel:+12504427977">250-442-7977</a>
    <details class="nav-mobile">
      <summary aria-label="Menu"><span></span><span></span><span></span></summary>
      <ul>
{items("        ")}
      </ul>
    </details>
  </div>
</header>'''


def footer(prefix):
    return f'''<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="{prefix}">{MARK}<span class="word"><b>Way To Store</b><small>Self Storage</small></span></a>
        <p>Heated indoor storage with level entry and a fenced compound for RVs, boats, trailers and containers. Locally owned, on Sagamore Road in Grand Forks, serving Boundary Country.</p>
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
        <h3>Storage</h3>
        <ul>
          <li><a href="{prefix}heated-storage-grand-forks.html">Heated storage units</a></li>
          <li><a href="{prefix}rv-boat-trailer-storage-grand-forks.html">RV, boat and trailer storage</a></li>
          <li><a href="{prefix}#offer">Introductory offer</a></li>
          <li><a href="{prefix}#faq">Common questions</a></li>
          <li><a href="{prefix}blog/">Blog</a></li>
          <li><a href="{prefix}privacy.html">Privacy</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">&copy; Way To Store Self Storage Ltd., 136 Sagamore Road, Grand Forks, British Columbia.</div>
  </div>
</footer>'''


def strip_tags(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s))).strip()


def gen_block(s, name, data):
    """Insert or replace a generated JSON-LD block tagged data-gen=name, just before </head>."""
    pat = re.compile(r'<script type="application/ld\+json" data-gen="%s">.*?</script>\n?' % name, re.S)
    s = pat.sub("", s)
    if data is None:
        return s
    block = '<script type="application/ld+json" data-gen="%s">\n%s\n</script>\n' % (name, json.dumps(data, indent=2, ensure_ascii=False))
    return s.replace("</head>", block + "</head>", 1)


def faq_schema(s):
    m = re.search(r'<div class="faq">(.*?)</div>\s*</div>\s*</section>', s, re.S)
    if not m:
        return None
    qa = re.findall(r"<details>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>", m.group(1), re.S)
    if not qa:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip_tags(q),
                            "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in qa]}


def crumb_schema(s, page_url):
    m = re.search(r'<div class="crumbs">(.*?)</div>', s, re.S)
    if not m:
        return None
    parts = [p.strip() for p in m.group(1).split(" / ")]
    items = []
    for i, part in enumerate(parts, 1):
        a = re.search(r'<a href="([^"]*)">(.*?)</a>', part)
        if a:
            href = a.group(1)
            url = SITE if href in ("../", "./", "/") else (SITE + "blog/" if href == "./" or href.endswith("blog/") else SITE + href.lstrip("./"))
            if href == "./" and "/blog/" in page_url:
                url = SITE + "blog/"
            items.append({"@type": "ListItem", "position": i, "name": strip_tags(a.group(2)), "item": url})
        else:
            items.append({"@type": "ListItem", "position": i, "name": strip_tags(part), "item": page_url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def patch(path, prefix, current):
    s = path.read_text(encoding="utf-8")
    asset = '' if prefix == './' else prefix
    rel = path.relative_to(ROOT).as_posix()
    page_url = SITE + ("" if rel == "index.html" else rel.replace("blog/index.html", "blog/"))
    s = re.sub(r"<header>.*?</header>", header(prefix, current), s, count=1, flags=re.S)
    s = re.sub(r"<footer>.*?</footer>", footer(prefix), s, count=1, flags=re.S)
    fonts = ('<!-- fonts -->'
             f'<link rel="preload" href="{asset}fonts/sora-normal-1.woff2" as="font" type="font/woff2" crossorigin>'
             f'<link rel="preload" href="{asset}fonts/source-sans-3-normal-3.woff2" as="font" type="font/woff2" crossorigin>'
             '<!-- /fonts -->')
    if '<!-- fonts -->' in s:
        s = re.sub(r'<!-- fonts -->.*?<!-- /fonts -->', fonts, s, count=1, flags=re.S)
    else:
        s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">', fonts, s, count=1)
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"[^>]*>\s*', '', s)
    s = re.sub(r'href="((?:\.\./|/)?)styles\.css(?:\?v=\d+)?"', lambda m: 'href="%sstyles.css?v=%s"' % (m.group(1), CSS_VERSION), s)
    if 'favicon.ico' not in s:
        s = re.sub(r'(<link rel="icon" href="([^"]*)favicon\.svg" type="image/svg\+xml">)',
                   r'\1\n<link rel="icon" href="\2favicon.ico" sizes="32x32">', s, count=1)
    if 'property="og:image"' in s:
        if 'property="og:locale"' not in s:
            s = re.sub(r'(<meta property="og:image"[^>]*>)', r'\1\n<meta property="og:locale" content="en_CA">', s, count=1)
        if 'name="twitter:card"' not in s:
            s = re.sub(r'(<meta property="og:locale"[^>]*>)', r'\1\n<meta name="twitter:card" content="summary_large_image">', s, count=1)
    if rel != "404.html":
        s = gen_block(s, "faq", faq_schema(s))
        s = gen_block(s, "breadcrumbs", crumb_schema(s, page_url))
    path.write_text(s, encoding="utf-8", newline="\n")
    print("patched", rel)


CURRENT = {"heated-storage-grand-forks.html": "heated", "rv-boat-trailer-storage-grand-forks.html": "rv"}
for p in sorted(ROOT.glob("*.html")):
    if p.name == "404.html":
        patch(p, "/", None)
    elif p.name.startswith(("brand-options", "options-preview")):
        continue
    else:
        patch(p, "./", CURRENT.get(p.name))
for p in sorted((ROOT / "blog").glob("*.html")):
    patch(p, "../", "blog")
