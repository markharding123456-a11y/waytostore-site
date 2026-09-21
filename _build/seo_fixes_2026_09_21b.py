"""Fixes from the independent review (workflow wf_a33c32a4-dc6), 2026-09-21. Run from the site root. Idempotent."""


def fix(path, pairs):
    s = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if new in s and old not in s:
            continue
        if old not in s:
            raise SystemExit("NOT FOUND in %s: %s" % (path, old[:80]))
        s = s.replace(old, new)
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    print("fixed", path)


# 1) CRITICAL: the post sold a cheaper "cold unit" that does not exist, and sent loose goods to the open compound.
P = "blog/heated-vs-unheated-storage-grand-forks.html"
fix(P, [
    ("Heated storage costs more than a cold unit or a spot in the yard. For some things it is money well spent. For others it is wasted. Here is how to tell which is which.",
     "Some things need a heated building to survive a winter in storage. Others are perfectly happy parked outside. Here is how to tell which is which."),
    ("      <li><strong>Liquids you are allowed to store.</strong> Cosmetics, cleaning products, water-based paint and anything in a bottle will freeze and split. Note that fuel, propane, solvents and other hazardous materials are not allowed in any unit, heated or not.</li>\n", ""),
    ("    <h2>Fine in the compound or a cold unit</h2>\n    <ul>\n      <li>Vehicles, RVs, boats and trailers that have been winterized. See <a href=\"winter-storage-rv-boat-boundary.html\">our winter checklist</a>.</li>\n      <li>Metal tools without batteries, lightly oiled.</li>\n      <li>Plastic bins of hardware, camping gear, sports equipment, garden tools.</li>\n      <li>Patio furniture, ladders, lumber, building materials, tires.</li>\n      <li>A shipping container you own, and whatever you have packed inside it to your own standard.</li>\n    </ul>\n",
     "    <h2>Fine outdoors in the compound</h2>\n    <ul>\n      <li>RVs, boats and trailers that have been winterized. See <a href=\"winter-storage-rv-boat-boundary.html\">the winter checklist</a>.</li>\n      <li>Cars, trucks and work equipment.</li>\n      <li>A shipping container you own, and whatever you have packed inside it to your own standard.</li>\n    </ul>\n    <p>Some things shrug off the cold but still need a roof and a lock: metal tools, plastic bins of hardware, camping gear, patio furniture, tires. They do not need heat to survive, but they do not belong in an open yard either. Our indoor lockers are all heated, so they go inside with everything else.</p>\n"),
    ("If everything you are storing is on the second list, save your money and take a cold space. If anything is on the first list, it is worth the difference. Most households have a mix, and the answer is a heated unit for the boxes and furniture plus a compound spot for the vehicle or trailer.",
     "If it has wheels or a hull and it has been winterized, it belongs in the compound. Almost everything else belongs indoors, and every indoor locker here is heated, so there is no cheaper cold locker to weigh it against. Most households have a mix, and the answer is a heated locker for the boxes and furniture plus a compound spot for the vehicle or trailer."),
])

# 2) Heated service page: same loose-goods problem, plus a ceiling height nobody has measured.
fix("heated-storage-grand-forks.html", [
    ("          <li>Patio furniture, ladders and building materials</li>\n", ""),
    ("measure your three biggest items, and remember the space is about eight feet high, so stacking does a lot of the work.",
     "measure your three biggest items, and remember that stacking does a lot of the work."),
])

# 3) No claimed track record: advice without "what we see / what we tell customers".
fix("blog/how-much-storage-space-do-i-need.html", [
    ("The most common question we get, and the one people most often get wrong in both directions. Here is how to think about it.",
     "The first question everyone asks, and an easy one to get wrong in both directions. Here is how to think about it."),
    ("Unit sizes are given as floor dimensions in feet. Most indoor units are about eight feet high,",
     "These are the standard sizes the storage industry uses, not a list of what we have open; call us for that. Sizes are given as floor dimensions in feet. Most storage units are about eight feet high,"),
    ("Call us with a list and we will tell you honestly which size to take.", "Call us with a list and we will tell you honestly which of our lockers fits."),
    ("<h2>Three mistakes we see</h2>", "<h2>Three common mistakes</h2>"),
    ("Most people overestimate. Measure your biggest three items, count your boxes, and remember the unit is eight feet tall. Half-empty units are the most common thing we see.",
     "It is easy to overestimate. Measure your biggest three items, count your boxes, and remember how much height there is to stack into. A half-empty unit is money spent on air."),
])
fix("blog/index.html", [
    ("No sales pitch, just what we tell customers on the phone.", "No sales pitch, just plain advice."),
    ("The checklist we use before anything parks in the compound for the season: water, fuel, batteries, tires, pests and paperwork.",
     "A checklist to work through before anything parks for the season: water, fuel, batteries, tires, pests and paperwork."),
])
fix("blog/winter-storage-rv-boat-boundary.html", [
    ('content="The checklist we use before anything parks in the compound for the season."', 'content="A checklist to work through before anything parks for the season."'),
    ("Here is the checklist we use.", "Here is a checklist worth working through."),
    ("Our compound rule is fuel tanks at no more than a quarter full.", "Keep fuel tanks at no more than a quarter full while parked in the compound."),
    ("Many policies allow a reduced storage rate for the months it is parked.", "Some insurers offer a reduced storage rate for the months it is parked."),
])

# 4) Do not imply an insurance product or a pricing guarantee the owner never set.
fix("index.html", [
    ("so check with your insurer or ask us about options.", "so check with your insurer."),
    ("Offer may be withdrawn at any time; the rate you are quoted when you book is the rate you get.", "Offer may be withdrawn at any time."),
])
fix("rv-boat-trailer-storage-grand-forks.html", [
    ("most insurers offer a reduced storage rate for the months a unit is parked, so it is worth a call to yours.",
     "some insurers offer a reduced storage rate for the months a unit is parked, so it is worth a call to yours."),
])

# 5) Privacy page: social tags, and the statutory wording for the response time (PIPA s.1 "day" excludes Saturdays and holidays; s.29, s.31).
fix("privacy.html", [
    ('<meta name="theme-color" content="#f26b1d">\n<!-- fonts -->',
     '<meta property="og:site_name" content="Way To Store Self Storage">\n<meta property="og:title" content="Privacy Policy | Way To Store Self Storage">\n<meta property="og:description" content="How Way To Store Self Storage collects, uses and protects personal information.">\n<meta property="og:type" content="website">\n<meta property="og:url" content="https://waytostore.ca/privacy.html">\n<meta property="og:image" content="https://waytostore.ca/og-image.png">\n<meta name="theme-color" content="#f26b1d">\n<!-- fonts -->'),
    ("Write to the privacy officer. We respond within 30 business days.",
     "Write to the privacy officer. We respond within 30 business days, the time limit the Act sets, and we will tell you if we need an extension the Act allows."),
])
