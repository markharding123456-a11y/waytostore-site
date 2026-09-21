"""Palette v4 (2026-09-21, Claudia: "looks cheap" -> nicer + friendlier). Run from the site root. Idempotent.
Keeps the rust-orange family Mark approved, but: deeper rust, warm cream + espresso instead of white + near-black,
orange as an accent rather than large flat fills, soft shadows instead of hard borders."""
import glob
import re

ACCENT, ACCENT_DARK, TAPE, INK = "#c04f17", "#9a3d10", "#c8551b", "#2a2320"


def sub(s, old, new, label):
    if new in s and old not in s:
        return s
    assert old in s, "NOT FOUND: " + label
    return s.replace(old, new)


p = "styles.css"
s = open(p, encoding="utf-8").read()

s = re.sub(r"/\* Way To Store Self Storage - shared styles.*?\*/\s*", "", s, count=1, flags=re.S)
root = """:root{
  --white:#ffffff;
  --ground:#fffdf9;
  --tint:#f7f0e6;
  --tint-2:#efe4d5;
  --ink:#2a2320;
  --ink-2:#6a5d54;
  --line:#eadfd2;
  --accent:#c04f17;
  --accent-dark:#9a3d10;
  --accent-soft:#fbe6d8;
  --cream:#fff6ec;
  --kraft:#c68b4f;
  --shadow:0 1px 2px rgba(42,35,32,.05),0 10px 28px rgba(42,35,32,.07);
}"""
s = re.sub(r":root\{.*?\n\}", root, s, count=1, flags=re.S)
s = ("/* Way To Store Self Storage - shared styles\n"
     "   Palette v4 (2026-09-21): warm cream ground, espresso text, deep rust accent used sparingly, soft shadows.\n"
     "   Logo: kraft carton with rust tape. Deliberately distinct from HydraClean (navy / gold / red). */\n") + s

s = sub(s, "body{margin:0;background:var(--white);", "body{margin:0;background:var(--ground);", "body bg")
s = sub(s, ".btn{display:inline-block;background:var(--ink);color:var(--white);", ".btn{display:inline-block;background:var(--accent);color:var(--white);", "btn")
s = sub(s, ".btn:hover{background:#000}", ".btn:hover{background:var(--accent-dark)}", "btn hover")
s = sub(s, ".nav .btn{padding:10px 18px;font-size:16px;background:var(--accent);color:var(--ink)}", ".nav .btn{padding:10px 18px;font-size:16px;background:var(--accent);color:var(--white)}", "nav btn")
s = sub(s, ".ribbon{background:var(--accent);color:var(--ink)}", ".ribbon{background:var(--accent-soft);color:var(--ink);border-bottom:1px solid var(--line)}", "ribbon")
s = sub(s, ".ribbon a{color:var(--ink);font-weight:700;white-space:nowrap}", ".ribbon a{color:var(--accent-dark);font-weight:700;white-space:nowrap}", "ribbon a")
s = sub(s, ".hero{padding:64px 0 60px;background:var(--white)}", ".hero{padding:64px 0 60px;background:var(--ground)}", "hero bg")
s = sub(s, ".hero-offer{background:var(--accent);color:var(--ink);border-radius:20px;padding:34px 32px 30px;box-shadow:0 12px 32px rgba(242,107,29,.28)}",
        ".hero-offer{background:var(--accent);color:var(--white);border-radius:24px;padding:34px 32px 30px;box-shadow:0 14px 36px rgba(154,61,16,.26)}", "hero-offer")
s = sub(s, ".hero-offer .terms{font-size:15px;margin:14px 0 0;color:var(--ink);opacity:.85;max-width:none}",
        ".hero-offer .terms{font-size:15px;margin:14px 0 0;color:var(--cream);max-width:none}", "hero-offer terms")
s = sub(s, ".hero-offer .btn{margin-top:22px;font-size:18px;padding:16px 26px}",
        ".hero-offer .btn{margin-top:22px;font-size:18px;padding:16px 26px;background:var(--cream);color:var(--ink)}\n.hero-offer .btn:hover{background:var(--white)}", "hero-offer btn")
s = sub(s, ".offer-block .price{background:var(--accent);color:var(--ink);", ".offer-block .price{background:var(--accent);color:var(--white);", "offer price")
s = sub(s, ".offer-block{margin-top:44px;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);border-radius:20px;overflow:hidden;border:1px solid var(--line)}",
        ".offer-block{margin-top:44px;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);border-radius:24px;overflow:hidden;border:1px solid var(--line);box-shadow:var(--shadow)}", "offer-block")
s = sub(s, ".why div{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:22px 22px 20px}",
        ".why div{background:var(--white);border:1px solid var(--line);border-radius:20px;padding:24px 22px 22px;box-shadow:var(--shadow)}", "why card")
s = sub(s, ".why svg{width:36px;height:36px;color:var(--accent);display:block;margin-bottom:14px}",
        ".why svg{width:56px;height:56px;padding:12px;border-radius:16px;background:var(--accent-soft);color:var(--accent);display:block;margin-bottom:16px}", "why icon")
s = sub(s, ".offer{background:var(--white);border:1px solid var(--line);border-radius:20px;padding:32px 30px 28px}",
        ".offer{background:var(--white);border:1px solid var(--line);border-radius:24px;padding:32px 30px 28px;box-shadow:var(--shadow)}", "offer card")
s = sub(s, "footer{background:var(--ink);color:#c9ccd1;", "footer{background:var(--ink);color:#d9cfc6;", "footer")
s = sub(s, "footer .brand .word small{color:#f7a06e}", "footer .brand .word small{color:#f3b48d}", "footer small")
s = sub(s, "footer p{color:#c9ccd1;", "footer p{color:#d9cfc6;", "footer p")
s = sub(s, "text-transform:uppercase;color:#f7a06e;", "text-transform:uppercase;color:#f3b48d;", "footer h3")
s = sub(s, "footer .legal{border-top:1px solid #33373c;margin-top:32px;padding-top:18px;font-size:14px;color:#9a9fa6}",
        "footer .legal{border-top:1px solid #4a3f39;margin-top:32px;padding-top:18px;font-size:14px;color:#a89a8f}", "footer legal")
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("styles.css -> palette v4")

# logo tape + wordmark colours, theme colour, css version
for f in ["favicon.svg", "logo.svg", "og-image.svg", "_build/mark.svg", "_build/patch_pages.py"] + glob.glob("*.html") + glob.glob("blog/*.html"):
    t = open(f, encoding="utf-8").read()
    n = t.replace('fill="#f26b1d"', 'fill="%s"' % TAPE).replace('content="#f26b1d"', 'content="%s"' % ACCENT)
    if f == "logo.svg":
        n = n.replace('fill="#1c1f22"', 'fill="%s"' % INK).replace('fill="%s">SELF STORAGE' % TAPE, 'fill="%s">SELF STORAGE' % ACCENT)
    if f == "og-image.svg":
        n = n.replace("#1c1f22", INK).replace("#5b6168", "#6a5d54")
        n = n.replace('<rect width="1200" height="16" fill="%s"/>' % TAPE, '<rect width="1200" height="16" fill="%s"/>' % ACCENT)
        n = n.replace('rx="42" fill="%s"/>' % TAPE, 'rx="42" fill="%s"/>' % ACCENT)
        n = n.replace('font-size="34" fill="%s">Half price' % INK, 'font-size="34" fill="#ffffff">Half price')
        n = n.replace('letter-spacing="5" fill="%s"' % TAPE, 'letter-spacing="5" fill="%s"' % ACCENT)
        n = n.replace('<rect width="1200" height="630" fill="#ffffff"/>', '<rect width="1200" height="630" fill="#fffdf9"/>')
    if f == "_build/patch_pages.py":
        n = re.sub(r"CSS_VERSION = '\d+'", "CSS_VERSION = '8'", n)
    if n != t:
        open(f, "w", encoding="utf-8", newline="\n").write(n)
        print("recoloured", f)
