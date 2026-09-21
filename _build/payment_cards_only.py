"""Claudia (Controller), 2026-09-21: credit card payments only. Run from the site root. Idempotent."""
import json
import re


def fix(path, pairs):
    s = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
        elif new not in s:
            raise SystemExit("NOT FOUND in %s: %s" % (path, old[:70]))
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    print("fixed", path)


fix("index.html", [
    ("<div><dt>Payment</dt><dd>E-transfer, credit card or cheque</dd></div>", "<div><dt>Payment</dt><dd>Credit card, billed monthly</dd></div>"),
    ("<p>A short rental agreement and the first month's rent. Month to month after that, with e-transfer, credit card or cheque.</p>",
     "<p>A short rental agreement and the first month's rent on your credit card. Month to month after that, billed to the same card.</p>"),
])

# structured data: say how you take payment
p = "index.html"
s = open(p, encoding="utf-8").read()
m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
d = json.loads(m.group(2))
biz = [n for n in d["@graph"] if n.get("@type") == "SelfStorage"][0]
biz["paymentAccepted"] = "Credit Card"
s = s[:m.start(2)] + "\n" + json.dumps(d, indent=2, ensure_ascii=False) + "\n" + s[m.end(2):]
open(p, "w", encoding="utf-8", newline="\n").write(s)

fix("profile-text.md", [
    ("Month-to-month rentals, pay by e-transfer, credit card or cheque.", "Month-to-month rentals, paid by credit card."),
])
