"""Website fixes carried over from the social-campaign review (wf_3dc0d89a-afe), 2026-09-21. Run from the site root."""


def fix(path, pairs):
    s = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
        elif new not in s:
            raise SystemExit("NOT FOUND in %s: %s" % (path, old[:70]))
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    print("fixed", path)


fix("rv-boat-trailer-storage-grand-forks.html", [
    ("work equipment that needs a secure yard between jobs.", "work equipment that needs a fenced yard between jobs."),
    ("Give us the overall length including the hitch when you call and we will confirm a spot that you can get in and out of without a spotter.",
     "Give us the overall length including the hitch when you call and we will tell you what is open that you can get in and out of without a spotter."),
    ("<p>Call with the length and we will hold a space. 136 Sagamore Road,", "<p>Call with the length and we will tell you what is open. 136 Sagamore Road,"),
    ("Tell us the size and whether it is being delivered, and we will pick a spot the truck can reach.",
     "Tell us the size and whether it is being delivered, and we will tell you what we can do."),
])
fix("blog/winter-storage-rv-boat-boundary.html", [
    ("open every tap including the outside shower, and blow out or antifreeze the lines.",
     "open every tap including the outside shower, and either blow the lines out with compressed air or fill them with non-toxic RV antifreeze. RV antifreeze only, never automotive."),
])

css = open("styles.css", encoding="utf-8").read()
if ".linklist" not in css:
    css += """
/* links page (Instagram bio target) */
.linkpage{max-width:560px}
.btn.wide{display:block;text-align:center;margin:26px 0 18px}
.linklist{list-style:none;padding:0;margin:0;display:grid;gap:12px}
.linklist a{display:block;padding:16px 20px;border:1px solid var(--line);border-radius:16px;background:var(--white);color:var(--ink);font-weight:600;text-decoration:none;box-shadow:var(--shadow)}
.linklist a:hover{border-color:var(--accent);color:var(--accent-dark)}
"""
    open("styles.css", "w", encoding="utf-8", newline="\n").write(css)
    print("css: links page styles")
