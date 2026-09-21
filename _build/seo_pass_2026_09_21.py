"""One-off content edits for the 2026-09-21 SEO pass. Idempotent where practical. Run from the site root."""
import json
import re


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8", newline="\n").write(s)


def replace_once(s, a, b, path):
    if b in s:
        return s          # already applied
    if a not in s:
        raise SystemExit("NOT FOUND in %s: %s" % (path, a[:70]))
    return s.replace(a, b, 1)


# ---------------- home page
p = "index.html"
s = read(p)
s = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="Heated storage units with level drive-up entry, plus a fenced compound for RVs, boats and trailers in Grand Forks, BC. Half price first month. 250-442-7977.">',
           s, count=1)
m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
d = json.loads(m.group(2))
d["@graph"] = [n for n in d["@graph"] if n.get("@type") != "FAQPage"]   # the stamper generates FAQPage from the visible FAQ
s = s[:m.start(2)] + "\n" + json.dumps(d, indent=2, ensure_ascii=False) + "\n" + s[m.end(2):]
s = replace_once(s, '    <h2>Two kinds of storage, one gate.</h2>\n',
                 '    <h2>Two kinds of storage, one gate.</h2>\n    <p class="section-intro">Looking for storage units in Grand Forks, BC? Way To Store has two kinds behind one gate on Sagamore Road, for households and businesses in Grand Forks, Christina Lake, Greenwood, Midway and the rest of Boundary Country.</p>\n', p)
s = replace_once(s, 'stays dry and above freezing. Level entry from where you park.</p>',
                 'stays dry and above freezing. Level entry from where you park. More on our <a href="heated-storage-grand-forks.html">heated storage units</a>, or read <a href="blog/heated-vs-unheated-storage-grand-forks.html">what actually needs the heat</a>.</p>', p)
s = replace_once(s, '          <li>A range of unit sizes. Call for current sizes and rates.</li>',
                 '          <li>A range of unit sizes. See <a href="blog/how-much-storage-space-do-i-need.html">how much space you need</a>, then call for sizes and rates.</li>', p)
s = replace_once(s, 'Room, too, for shipping containers and sea cans if you need a place to park one.</p>',
                 'Room, too, for shipping containers and sea cans if you need a place to park one. Details on <a href="rv-boat-trailer-storage-grand-forks.html">RV, boat and trailer storage</a>, plus our <a href="blog/winter-storage-rv-boat-boundary.html">winter storage checklist</a>.</p>', p)
write(p, s)

# ---------------- blog index
p = "blog/index.html"
s = read(p)
s = re.sub(r"<title>.*?</title>", "<title>Storage Tips for Grand Forks &amp; the Boundary | Way To Store</title>", s, count=1, flags=re.S)
s = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="Plain storage advice from Way To Store in Grand Forks, BC: choosing a unit size, winter RV and boat prep, and what needs a heated unit.">', s, count=1)
s = replace_once(s, '<p class="lede">Plain advice from the people who run the place. No sales pitch, just what we tell customers on the phone.</p>',
                 '<p class="lede">Plain advice from the people who run the storage on Sagamore Road, for Grand Forks, Christina Lake, Greenwood, Midway and the rest of Boundary Country. No sales pitch, just what we tell customers on the phone.</p>', p)
s = re.sub(r'<h3>(<a href="[^"]+\.html">.*?</a>)</h3>', r"<h2>\1</h2>", s)
write(p, s)

# ---------------- blog posts
posts = {
    "blog/how-much-storage-space-do-i-need.html": (
        "How Much Storage Space Do I Need? | Way To Store", None,
        [("heated-vs-unheated-storage-grand-forks.html", "Heated or unheated storage: what actually needs the heat"),
         ("../heated-storage-grand-forks.html", "Heated storage units in Grand Forks"),
         ("../rv-boat-trailer-storage-grand-forks.html", "RV, boat and trailer storage")]),
    "blog/winter-storage-rv-boat-boundary.html": (
        "Winter RV &amp; Boat Storage Prep in the Boundary | Way To Store",
        "A practical winter storage checklist for RVs and boats in Grand Forks and Christina Lake: water, fuel, batteries, tires, pests and paperwork.",
        [("../rv-boat-trailer-storage-grand-forks.html", "RV, boat and trailer storage in Grand Forks"),
         ("heated-vs-unheated-storage-grand-forks.html", "Heated or unheated storage: what actually needs the heat"),
         ("how-much-storage-space-do-i-need.html", "How much storage space do I need?")]),
    "blog/heated-vs-unheated-storage-grand-forks.html": (
        "Heated vs Unheated Storage in Grand Forks | Way To Store", None,
        [("../heated-storage-grand-forks.html", "Heated storage units in Grand Forks"),
         ("how-much-storage-space-do-i-need.html", "How much storage space do I need?"),
         ("winter-storage-rv-boat-boundary.html", "Getting an RV or boat ready for winter storage")]),
}
for path, (title, desc, links) in posts.items():
    s = read(path)
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, s, count=1, flags=re.S)
    if desc:
        s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % desc, s, count=1)
    rel = '    <aside class="related"><h2>Keep reading</h2><ul>' + "".join('<li><a href="%s">%s</a></li>' % (h, t) for h, t in links) + "</ul></aside>\n"
    s = re.sub(r'    <aside class="related">.*?</aside>\n', "", s, flags=re.S)
    s = s.replace("  </article>\n</main>", rel + "  </article>\n</main>", 1)
    write(path, s)
print("pages edited")

# ---------------- stylesheet
p = "styles.css"
css = read(p)
if ".nav-mobile" not in css:
    old = (".nav ul{display:flex;gap:26px;list-style:none;margin:0;padding:0}\n"
           ".nav ul a{color:var(--ink);text-decoration:none;font-weight:600;font-size:16px}\n"
           ".nav ul a:hover,.nav ul a[aria-current]{color:var(--accent)}")
    new = (".nav ul{list-style:none;margin:0;padding:0}\n"
           ".nav-desktop{display:flex;gap:22px}\n"
           ".nav ul a{color:var(--ink);text-decoration:none;font-weight:600;font-size:16px}\n"
           ".nav ul a:hover,.nav ul a[aria-current]{color:var(--accent)}\n"
           ".nav-mobile{display:none;position:relative}\n"
           ".nav-mobile summary{list-style:none;cursor:pointer;width:44px;height:44px;display:flex;flex-direction:column;justify-content:center;gap:5px;padding:0 10px;border:2px solid var(--ink);border-radius:10px}\n"
           ".nav-mobile summary::-webkit-details-marker{display:none}\n"
           ".nav-mobile summary span{display:block;height:3px;background:var(--ink);border-radius:2px}\n"
           ".nav-mobile ul{position:absolute;right:0;top:54px;background:var(--white);border:1px solid var(--line);border-radius:14px;box-shadow:0 14px 34px rgba(0,0,0,.14);padding:8px;min-width:240px;display:grid}\n"
           ".nav-mobile ul a{display:block;padding:13px 14px;font-size:17px;border-radius:8px}\n"
           ".nav-mobile ul a:hover{background:var(--tint)}")
    assert old in css, "nav css anchor not found"
    css = css.replace(old, new, 1)
    old_m = "@media (max-width:820px){\n  .nav ul{display:none}\n"
    assert old_m in css, "media anchor not found"
    css = css.replace(old_m, "@media (max-width:980px){\n  .nav-desktop{display:none}\n  .nav-mobile{display:block}\n", 1)
if ".hero.service" not in css:
    css += """
/* service pages, related reading, small helpers (SEO pass 2026-09-21) */
.hero.service{padding:48px 0 56px}
.hero.service h1{max-width:18ch}
.hero.service .lede{max-width:60ch}
.section-intro{font-size:19px;color:var(--ink-2);margin:14px 0 0;max-width:70ch}
.prose{margin-top:22px}
.prose p{max-width:70ch;font-size:18px}
.why.three{grid-template-columns:repeat(3,1fr)}
@media (max-width:900px){.why.three{grid-template-columns:1fr}}
.muted-note{margin:26px 0 0;color:var(--ink-2);font-size:17px;max-width:70ch}
.after-list{margin:18px 0 0;font-size:17px}
.cta-row{display:flex;flex-wrap:wrap;gap:24px 48px;align-items:center;justify-content:space-between}
.cta-row p{margin:12px 0 0;color:var(--ink-2)}
.cta-row .actions{margin-top:0}
.post-list h2{font-size:22px}
.post-list h2 a{color:var(--ink);text-decoration:none}
.post-list h2 a:hover{color:var(--accent)}
.related{margin-top:44px;padding-top:22px;border-top:3px solid var(--ink)}
.related h2{font-size:20px;margin:0 0 10px}
.related ul{list-style:none;padding:0;margin:0;display:grid;gap:8px}
.related a{font-weight:600}
"""
write(p, css)

# ---------------- sitemap
urls = [("", "1.0"), ("heated-storage-grand-forks.html", "0.9"), ("rv-boat-trailer-storage-grand-forks.html", "0.9"),
        ("blog/", "0.6"), ("blog/how-much-storage-space-do-i-need.html", "0.5"),
        ("blog/winter-storage-rv-boat-boundary.html", "0.5"), ("blog/heated-vs-unheated-storage-grand-forks.html", "0.5"),
        ("privacy.html", "0.2")]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, pr in urls:
    sm.append("  <url><loc>https://waytostore.ca/%s</loc><lastmod>2026-09-21</lastmod><priority>%s</priority></url>" % (u, pr))
sm.append("</urlset>")
write("sitemap.xml", "\n".join(sm) + "\n")
print("css + sitemap done")
