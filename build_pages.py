#!/usr/bin/env python3
"""Little Gem — template-v2 page builder (2026-11-21, t_3e4eb1a5).
Writes public/*.html + sitemap.xml + robots.txt + favicon.svg from one source.
Re-pin the demo host by editing HOST here (one token) and re-running."""
import json, os

HOST = "little-gem-demo.up.railway.app"
ORIGIN = "https://" + HOST
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

# ---- verified facts (sources on card t_3e4eb1a5) ----
# address 4235 E Madison St, Seattle WA 98112 (owner via What Now Seattle; space = former Independent Pizzeria)
# takeout hoped Dec 2026 no dates; opening early 2027 (What Now, owner interview)
# recipes incl dough taught by IP owners Tom Siegel & Tora B. Hennessey (Seattle Times via What Now)
# wood-fired oven "fired up again soon" (Little Gem IG 10-30); wine + low-alc cocktails (What Now)
# geo 47.6359824,-122.2773761 (Apple Maps place entry for the address)
MAPQ = "4235+E+Madison+St,+Seattle,+WA+98112"
MAPURL = f"https://maps.google.com/maps?q={MAPQ}"
IGURL = "https://www.instagram.com/littlegemseattle/"

GEM = ('<svg class="mark" viewBox="0 0 100 100" role="img" aria-label="Little Gem emblem: a faceted gemstone">'
       '<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'
       '<path d="M50 8 79 22 92 50 79 78 50 92 21 78 8 50 21 22Z" stroke-width="4"/>'
       '<path d="M50 26 65 33 71 50 65 67 50 74 35 67 29 50 35 33Z" stroke-width="3"/>'
       '<path d="M50 8v18M79 22l-14 11M92 50H71M79 78l-14-11M50 92V74M21 78l14-11M8 50h21M21 22l14 11" stroke-width="2.5"/>'
       '<path d="M35 33l30 34M65 33l-30 34" stroke="#b9892f" stroke-width="2"/></g></svg>')

HEROART = ('<svg class="heroart" viewBox="0 0 560 520" role="img" aria-label="Illustration of a wood-fired pizza seen from above, glowing with gold sparkles">'
 '<g fill="none"><circle cx="280" cy="256" r="232" stroke="#5c1c2e" stroke-width="2"/><circle cx="280" cy="256" r="222" stroke="#b9892f" stroke-width="1" opacity=".55"/></g>'
 '<g fill="none"><circle cx="280" cy="256" r="205" fill="#e8c185"/><circle cx="280" cy="256" r="172" fill="#a63a44"/>'
 '<g fill="#8a5a2e"><circle cx="96" cy="200" r="5"/><circle cx="120" cy="332" r="4"/><circle cx="248" cy="52" r="5"/><circle cx="368" cy="58" r="4"/><circle cx="456" cy="152" r="5"/><circle cx="462" cy="344" r="4"/><circle cx="336" cy="448" r="5"/><circle cx="208" cy="452" r="4"/><circle cx="70" cy="268" r="4"/></g>'
 '<g fill="#f4ead3" opacity=".95"><ellipse cx="206" cy="182" rx="36" ry="25" transform="rotate(-12 206 182)"/><ellipse cx="338" cy="158" rx="30" ry="21" transform="rotate(14 338 158)"/><ellipse cx="372" cy="252" rx="27" ry="23" transform="rotate(-8 372 252)"/><ellipse cx="252" cy="306" rx="33" ry="22" transform="rotate(9 252 306)"/><ellipse cx="168" cy="272" rx="24" ry="19"/><ellipse cx="310" cy="352" rx="28" ry="20" transform="rotate(-14 310 352)"/></g>'
 '<g fill="#6f8350"><path d="M246 210q20 -16 40 0q-20 22 -40 0Z"/><path d="M330 232q18 -14 36 0q-18 20 -36 0Z"/><path d="M212 336q18 -14 36 0q-18 20 -36 0Z"/><path d="M322 300q16 -13 32 0q-16 18 -32 0Z"/><path d="M270 156q16 -13 32 0q-16 18 -32 0Z"/></g>'
 '<g fill="#e5b45a"><path d="M0-24C4-9 9-4 24 0C9 4 4 9 0 24C-4 9 -9 4 -24 0C-9-4 -4-9 0-24Z" transform="translate(72 78)"/>'
 '<path d="M0-16C3-6 6-3 16 0C6 3 3 6 0 16C-3 6 -6 3 -16 0C-6-3 -3-6 0-16Z" transform="translate(492 96)"/>'
 '<path d="M0-20C3-8 8-3 20 0C8 3 3 8 0 20C-3 8 -8 3 -20 0C-8-3 -3-8 0-20Z" transform="translate(452 446)"/>'
 '<circle cx="58" cy="140" r="4"/><circle cx="506" cy="42" r="3.5"/><circle cx="524" cy="330" r="4"/><circle cx="112" cy="444" r="3.5"/></g></g></svg>')

def head(title, desc, path, og=True):
    ogmeta = ""
    if og:
        ogmeta = (f'<meta property="og:title" content="{title}">\n'
                  f'<meta property="og:description" content="{desc}">\n'
                  f'<meta property="og:url" content="{ORIGIN}{path}">\n'
                  f'<meta property="og:image" content="{ORIGIN}/og.png">\n'
                  f'<meta property="og:type" content="website">\n'
                  f'<meta name="twitter:card" content="summary_large_image">\n')
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
      f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
      f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
      f'<meta name="robots" content="noindex, nofollow">\n'
      f'<link rel="canonical" href="{ORIGIN}{path}">\n'
      f'<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
      + ogmeta +
      f'<link rel="stylesheet" href="/style.css">\n</head>\n<body>\n'
      f'<a class="skip" href="#main">Skip to content</a>\n<div class="band" aria-hidden="true"></div>\n'
      f'<header class="top"><div class="wrap"><a class="brand" href="/">{GEM}<span class="word">Little Gem'
      '<small>Neighborhood Pizzeria · Madison Park, Seattle</small></span></a>'
      '<nav class="main" aria-label="Main"><ul><li><a href="/our-pizza">Our Pizza</a></li>'
      '<li><a href="/wood-fired-pizza-madison-park">Wood-Fired</a></li>'
      '<li><a href="/pizza-takeout-madison-park">Takeout</a></li>'
      '<li><a href="/faq">FAQ</a></li><li><a class="btn" href="/contact">Opening news</a></li></ul></nav></div></header>\n'
      '<main id="main">\n</main>\n'
      '<footer class="site"><div class="wrap"><div class="nap"><p class="fbrand">Little Gem</p>'
      '<address>4235 E Madison St<br>Madison Park · Seattle, Washington 98112<br>Neighborhood pizzeria · opening early 2027</address></div>'
      '<nav aria-label="Footer"><ul><li><a href="/our-pizza">Our Pizza</a></li>'
      '<li><a href="/wood-fired-pizza-madison-park">Wood-Fired</a></li>'
      '<li><a href="/pizza-takeout-madison-park">Takeout</a></li>'
      '<li><a href="/faq">FAQ</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy">Privacy</a></li></ul></nav>'
      f'<p class="socials"><a href="{IGURL}" rel="noopener">Instagram</a></p>'
      '<p class="footline">© 2026 Little Gem · Madison Park&apos;s neighborhood pizzeria · 4235 E Madison St, Seattle, WA</p></div></footer>\n'
      '<!-- BUILT-2026-11-21 -->\n')

MAPCELL = (f'<div class="mapcell"><iframe src="https://www.google.com/maps?q={MAPQ}&amp;output=embed" '
  'title="Map: Little Gem, 4235 E Madison St, Seattle, WA 98112" loading="lazy"></iframe></div>')
MAPNOTE = (f'<p class="mapnote"><a href="{MAPURL}" rel="noopener">Open in Google Maps →</a> — dates, menu and '
  'ordering news go out on Instagram first.</p>')

REST = {
  "@type": "Restaurant", "@id": ORIGIN + "/#littlegem", "name": "Little Gem",
  "alternateName": "Little Gem Seattle",
  "description": "Madison Park's neighborhood pizzeria at 4235 E Madison Street — carrying on the space, the wood-fired oven and the dough recipe of the Independent Pizzeria, with wine and low-alcohol cocktails alongside. Takeout planned for December 2026; opening early 2027.",
  "url": ORIGIN + "/", "image": ORIGIN + "/og.png",
  "servesCuisine": "Pizza",
  "address": {"@type": "PostalAddress", "streetAddress": "4235 E Madison St",
              "addressLocality": "Seattle", "addressRegion": "WA", "postalCode": "98112", "addressCountry": "US"},
  "geo": {"@type": "GeoCoordinates", "latitude": 47.6359824, "longitude": -122.2773761},
  "hasMap": MAPURL, "sameAs": [IGURL],
}

def ld(blocks):
    return "".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=1)}\n</script>\n' for b in blocks)

def graph(node):  # wraps detail-page nodes with a restaurant stub reference
    return {**node, "provider": {"@type": "Restaurant", "@id": REST["@id"], "name": "Little Gem",
            "address": REST["address"]}}

def crumbs(name, path):
    return {"@type": "BreadcrumbList", "@id": ORIGIN + path + "/#bc", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": ORIGIN + path}]}

def webpage(name, path):
    return {"@type": "WebPage", "@id": ORIGIN + path + "/#page", "url": ORIGIN + path,
            "name": name, "inLanguage": "en-US"}

# ---------------- pages ----------------
PAGES = {}

PAGES["index.html"] = dict(
 title="Little Gem — Madison Park's Neighborhood Pizzeria, Seattle",
 desc="A wood-fired pizzeria taking over 4235 E Madison Street — the Independent Pizzeria's space, oven and dough recipe. Takeout planned for December 2026; opening early 2027. Madison Park, Seattle WA 98112.",
 body=(
  '<section class="hero"><div class="wrap"><div class="herotext">'
  '<span class="label">Opening early 2027 · Madison Park · 4235 E Madison St</span>'
  '<h1>Little <em>Gem</em></h1>'
  '<p class="sub">Madison Park&rsquo;s neighborhood pizzeria, carrying on the space, the wood-fired oven and '
  'the dough recipe of the beloved Independent Pizzeria at 4235 E Madison Street — with wine and low-alcohol '
  'cocktails poured alongside the pies.</p>'
  '<hr class="rule"><div class="ctas"><a class="btn" href="' + IGURL + '" rel="noopener">Follow on Instagram</a>'
  '<a class="btn ghost" href="/contact">Send us a note</a></div>'
  '<p class="heronote">Address and opening window per the owner&rsquo;s November 2026 interview with What Now Seattle.</p>'
  '</div><div class="heroartcell">' + HEROART + '</div></div></section>'

  '<section class="block"><div class="wrap"><span class="label">The hand-me-down</span>'
  '<h2>Same corner. Same oven. New chapter.</h2>'
  '<p class="lede">Little Gem is taking over 4235 E Madison Street — the address the Independent Pizzeria made a '
  'neighborhood institution over nearly 17 years — and with it, its pizza recipes.</p>'
  '<span class="qsrc">space, tenure and handover per What Now Seattle and The Seattle Times</span>'
  '<div class="strip">'
  '<div class="chip"><h3>The dough, passed down</h3><p>The pizzeria&rsquo;s longtime owners are teaching the new '
  'team their recipes and techniques — the dough recipe included — so the pie you love is the pie that comes back.</p>'
  '<p><a href="/our-pizza">Read the lineage →</a></p></div>'
  '<div class="chip gold"><h3>The oven stays lit</h3><p>This is a wood-fired address, and Little Gem&rsquo;s own '
  'first Instagram post said the quiet part: the oven &ldquo;will be fired up again soon.&rdquo;</p>'
  '<p><a href="/wood-fired-pizza-madison-park">Wood-fired pizza →</a></p></div>'
  '<div class="chip basil"><h3>Takeout first</h3><p>Takeout is planned to start in December 2026 — no dates set '
  'yet — with the full opening penciled for early 2027.</p>'
  '<p><a href="/pizza-takeout-madison-park">Takeout details →</a></p></div></div>'
  '<div class="openstrip"><div><h3>When do the doors open?</h3><p>The plan, from the owner&rsquo;s interview with '
  'What Now Seattle: takeout hoped for December 2026 with no dates set, and a full opening planned for early 2027. '
  'The moment a date is real, it goes out on Instagram first — and lands here.</p>'
  '<span class="qsrc">What Now Seattle, owner interview, November 2026</span></div>'
  '<a class="btn ghost" href="/contact">Get opening news</a></div></div></section>'

  '<section class="quotband"><div class="wrap"><blockquote>&ldquo;It&rsquo;s an honor to continue to offer your '
  'pizzas to the community.&rdquo;<span class="qsrc">Little Gem&rsquo;s first Instagram post, Nov 1, 2026 — to the '
  'Independent Pizzeria&rsquo;s owners</span></blockquote></div></section>'

  '<section class="block"><div class="wrap"><span class="label">Find the corner</span>'
  '<h2>4235 E Madison Street</h2>'
  '<div class="mapgrid"><div><p class="lede">Madison Park, Seattle, Washington 98112 — the corner the neighborhood '
  'already knows.</p><span class="qsrc">address confirmed by the owner to What Now Seattle; same address as The '
  'Independent Pizzeria&rsquo;s last listings (Seattle Met business directory, Yelp, Apple Maps)</span>'
  '<div class="ctas" style="margin-top:22px"><a class="btn" href="/contact">Ask us anything</a></div></div>'
  '<div>' + MAPCELL + MAPNOTE + '</div></div></div></section>'

  '<section class="callband"><div class="wrap"><div><h2>Questions before opening day?</h2>'
  '<p>Leave a note — menu wishes, requests, or just wanting to know when the counter opens. Every message reaches '
  'the team, and the team is reading before day one.</p></div><div class="ctas" style="margin:0">'
  '<a class="btn" href="/contact">Contact us</a><a class="btn ghost" href="' + IGURL + '" rel="noopener">Follow on Instagram</a></div></div></section>'
 ),
 ld=ld([{"@context": "https://schema.org", "@graph": [REST, webpage("Little Gem", "/"), crumbs("Little Gem", "/")]}]),
)

PAGES["our-pizza.html"] = dict(
 title="Our Pizza — Little Gem, Madison Park Seattle",
 desc="The wood-fired pizza of 4235 E Madison Street, carried on from the Independent Pizzeria's recipes — dough included — with wine and low-alcohol cocktails planned alongside. Menu lands before opening.",
 body=(
  '<section class="minihero"><div class="wrap"><span class="label">The hand-me-down menu</span>'
  '<h1>Our pizza — <em>and what to pour beside it</em></h1>'
  '<p class="sub">Everything Little Gem serves starts with the recipes this corner is known for. The menu is being '
  'finalized now; it lands on Instagram before the first pie comes out of the oven.</p></div></section>'

  '<section class="block"><div class="wrap"><div class="prose"><span class="label">Same recipes, new hands</span>'
  '<h2>The lineage of a neighborhood pie</h2>'
  '<p>When The Independent Pizzeria closed in October 2026 after nearly 17 years, the plan was already in motion: '
  'its owners are teaching Little Gem&rsquo;s team the recipes and techniques that made the place — the dough '
  'included.</p><span class="qsrc">What Now Seattle, citing The Seattle Times, 2026</span>'
  '<p>That is the whole idea of Little Gem: not a new pizza brand, but the neighborhood&rsquo;s pizza, carried on '
  '— from the same wood-fired oven, at the same address, with a short, thoughtful drinks list beside it.</p>'
  '<span class="qsrc">wine and low-alcohol cocktails per the owner&rsquo;s What Now Seattle interview</span></div>'
  '<div class="menueta"><p><strong>Menu status:</strong> nothing published yet — no pie names, prices, hours or '
  'ordering channels are posted here before the shop announces them. Watch <a href="' + IGURL + '" rel="noopener">@littlegemseattle</a> '
  'for the drop, or leave a note with what you want on the menu.</p></div>'
  '<div class="strip">'
  '<div class="chip"><h3>Dough, handed down</h3><p>The dough recipe changed hands straight from the old kitchen '
  'to the new one — the most valuable thing in the building.</p><p><a href="/wood-fired-pizza-madison-park">How it gets fired →</a></p></div>'
  '<div class="chip basil"><h3>Wine + low-alc</h3><p>A glass worth having alongside the pie: wine and low-alcohol '
  'cocktails are planned for the list.</p><p><a href="/faq">Ask the pouring questions →</a></p></div>'
  '<div class="chip gold"><h3>Takeout first</h3><p>Counter service comes before dining-room night: takeout is '
  'planned for December 2026, dates pending.</p><p><a href="/pizza-takeout-madison-park">Takeout details →</a></p></div></div></div></section>'

  '<section class="callband"><div class="wrap"><div><h2>Tell us what you miss about the old menu</h2>'
  '<p>The team is reading notes before opening — a neighborhood wish list is worth more than any marketing plan.</p></div>'
  '<div class="ctas" style="margin:0"><a class="btn" href="/contact">Send a wish</a>'
  '<a class="btn ghost" href="' + IGURL + '" rel="noopener">Follow on Instagram</a></div></div></section>'
 ),
 ld=ld([{"@context": "https://schema.org", "@graph": [webpage("Our Pizza", "/our-pizza"), crumbs("Our Pizza", "/our-pizza")]}]),
)

PAGES["wood-fired-pizza-madison-park.html"] = dict(
 title="Wood-Fired Pizza — Little Gem, Madison Park Seattle",
 desc="The oven at 4235 E Madison Street is coming back to life: wood-fired pizza in Madison Park, Seattle, from the recipes the neighborhood grew up on. Takeout planned for December 2026.",
 body=(
  '<section class="minihero"><div class="wrap"><span class="label">The oven</span>'
  '<h1>Wood-fired pizza, <em>Madison Park</em></h1>'
  '<p class="sub">4235 E Madison Street has pulled wood-fired pies for years. Little Gem is bringing the fire back '
  '— and the takeout counter will be the first thing to glow.</p></div></section>'

  '<section class="block"><div class="wrap"><div class="prose"><span class="label">A wood-fired address</span>'
  '<h2>Nearly 17 years of fire</h2>'
  '<p>Wood-fired pizza is what The Independent Pizzeria made here for nearly 17 years — it&rsquo;s how the corner '
  'became the neighborhood&rsquo;s spot, and it&rsquo;s the practice Little Gem is carrying on. The new team said '
  'it plainly in its own first posts: the oven &ldquo;will be fired up again soon.&rdquo;</p>'
  '<span class="qsrc">wood-fired practice and tenure per the Seattle Met business directory and What Now Seattle; '
  'oven promise per Little Gem on Instagram, Oct 30, 2026</span>'
  '<p>Wood-fired, done right, means a hot oven, fast cooks and a crust with char on the ridge. The dough going '
  'into it is the neighborhood&rsquo;s own — handed down recipe and technique from the kitchen that made it famous.</p></div>'
  '<div class="strip">'
  '<div class="chip"><h3>Dough, passed down</h3><p>Same recipe, taught hand-to-hand by the pizzeria&rsquo;s '
  'former owners.</p><p><a href="/our-pizza">Read the lineage →</a></p></div>'
  '<div class="chip gold"><h3>First pies: takeout</h3><p>The oven&rsquo;s first runs feed the takeout counter — '
  'planned for December 2026.</p><p><a href="/pizza-takeout-madison-park">Takeout details →</a></p></div>'
  '<div class="chip basil"><h3>Beside the pie</h3><p>Wine and low-alcohol cocktails are planned once the room is '
  'open.</p><p><a href="/faq">See the FAQ →</a></p></div></div></div></section>'

  '<section class="block" style="padding-top:0"><div class="wrap"><span class="label">Find the corner</span>'
  '<h2>Where the fire is</h2><div class="mapgrid"><div><p class="lede">4235 E Madison St, Madison Park, Seattle, '
  'WA 98112 — the address the neighborhood already walks to.</p>'
  '<span class="qsrc">address per the owner&rsquo;s What Now Seattle interview; coordinates per the address&rsquo;s Apple Maps place entry</span></div>'
  '<div>' + MAPCELL + MAPNOTE + '</div></div></div></section>'

  '<section class="callband"><div class="wrap"><div><h2>Counting down to the first pie?</h2>'
  '<p>Leave a note and we&rsquo;ll tell you the moment dates and ordering are set.</p></div>'
  '<div class="ctas" style="margin:0"><a class="btn" href="/contact">Get opening news</a>'
  '<a class="btn ghost" href="' + IGURL + '" rel="noopener">Follow on Instagram</a></div></div></section>'
 ),
 ld=ld([{"@context": "https://schema.org", "@graph": [
   graph({"@type": "Service", "@id": ORIGIN + "/wood-fired-pizza-madison-park/#service",
          "serviceType": "Wood-fired pizza", "name": "Wood-Fired Pizza",
          "description": "Neighborhood wood-fired pizza served from the oven at 4235 E Madison St, made from the Independent Pizzeria's handed-down dough recipe.",
          "areaServed": "Madison Park, Seattle, WA", "url": ORIGIN + "/wood-fired-pizza-madison-park"}),
   webpage("Wood-Fired Pizza", "/wood-fired-pizza-madison-park"),
   crumbs("Wood-Fired Pizza", "/wood-fired-pizza-madison-park")]}]),
)

PAGES["pizza-takeout-madison-park.html"] = dict(
 title="Pizza Takeout — Little Gem, Madison Park Seattle",
 desc="Takeout at 4235 E Madison Street, Madison Park, Seattle — planned to begin December 2026, no dates set. Full opening early 2027. Ordering channels announced on Instagram first.",
 body=(
  '<section class="minihero"><div class="wrap"><span class="label">First up</span>'
  '<h1>Takeout, <em>planned for December</em></h1>'
  '<p class="sub">The first thing Little Gem will do is slide pies across the counter: takeout at 4235 E Madison '
  'Street is planned to begin in December 2026 — no dates set yet.</p></div></section>'

  '<section class="block"><div class="wrap"><div class="prose"><span class="label">Honest blanks</span>'
  '<h2>What&rsquo;s known, what isn&rsquo;t</h2>'
  '<p><strong>Known:</strong> takeout comes first, planned for December 2026; the full opening is planned for early '
  '2027. The pies will be the old corner&rsquo;s recipes, fired in the same oven.</p>'
  '<span class="qsrc">opening plan per the owner&rsquo;s What Now Seattle interview; recipes per The Seattle Times</span>'
  '<p><strong>Not yet:</strong> exact dates, the full menu, and how ordering will work — counter, phone, or app. '
  'Nothing is announced yet, so nothing is claimed here. When the shop says it, it lands on Instagram first and '
  'then on this page.</p></div>'
  '<div class="strip">'
  '<div class="chip"><h3>The corner</h3><p>4235 E Madison St — the address the neighborhood already knows by '
  'heart.</p><p><a href="/">See the map →</a></p></div>'
  '<div class="chip gold"><h3>The pizza</h3><p>Same dough recipe, same wood-fired oven, recipes handed down from '
  'the old kitchen.</p><p><a href="/our-pizza">Read the lineage →</a></p></div>'
  '<div class="chip basil"><h3>Opening news</h3><p>Want the date text-first when it drops? The form reaches the '
  'team directly.</p><p><a href="/contact">Send a note →</a></p></div></div></div></section>'

  '<section class="block" style="padding-top:0"><div class="wrap"><span class="label">Find the counter</span>'
  '<h2>Where the pies will land</h2><div class="mapgrid"><div><p class="lede">4235 E Madison St, Madison Park, '
  'Seattle, WA 98112.</p><span class="qsrc">address per the owner&rsquo;s What Now Seattle interview</span></div>'
  '<div>' + MAPCELL + MAPNOTE + '</div></div></div></section>'

  '<section class="callband"><div class="wrap"><div><h2>Want the takeout date the day it&rsquo;s set?</h2>'
  '<p>Follow the shop on Instagram, or leave your email on the contact page — the team answers every note.</p></div>'
  '<div class="ctas" style="margin:0"><a class="btn" href="/contact">Ask for the date</a>'
  '<a class="btn ghost" href="' + IGURL + '" rel="noopener">Follow on Instagram</a></div></div></section>'
 ),
 ld=ld([{"@context": "https://schema.org", "@graph": [
   graph({"@type": "Service", "@id": ORIGIN + "/pizza-takeout-madison-park/#service",
          "serviceType": "Pizza takeout", "name": "Pizza Takeout",
          "description": "Counter takeout of wood-fired pizza at 4235 E Madison St, planned to begin December 2026 with dates pending.",
          "areaServed": "Madison Park, Seattle, WA", "url": ORIGIN + "/pizza-takeout-madison-park"}),
   webpage("Pizza Takeout", "/pizza-takeout-madison-park"),
   crumbs("Pizza Takeout", "/pizza-takeout-madison-park")]}]),
)

FAQS = [
 ("When is Little Gem opening?",
  "Takeout first: the owner told What Now Seattle that takeout is hoped to start in December 2026 — no dates set — with the full opening planned for early 2027. When a date is real, it goes out on <a href=\"https://www.instagram.com/littlegemseattle/\" rel=\"noopener\">@littlegemseattle</a> first."),
 ("Where exactly is Little Gem?",
  "4235 E Madison Street in Madison Park, Seattle (98112) — the corner home of The Independent Pizzeria for its final nearly 17 years. The address was confirmed by the owner to What Now Seattle."),
 ("Is it the same pizza as the old Independent Pizzeria?",
  "That&rsquo;s the plan, right down to the dough: the Independent Pizzeria&rsquo;s former owners are teaching Little Gem&rsquo;s team their recipes and techniques, dough recipe included (What Now Seattle, citing The Seattle Times). Little Gem put it best in its first post: &ldquo;It&rsquo;s an honor to continue to offer your pizzas to the community.&rdquo;"),
 ("Who is behind Little Gem?",
  "A veteran of Seattle&rsquo;s bar and restaurant scene — a 2026 James Beard Award semifinalist for Outstanding Professional in Cocktail Service — stepping behind the pizza peel. Full introductions land with the menu announcement."),
 ("Will the pizza be wood-fired?",
  "Yes — 4235 E Madison Street is a wood-fired pizza kitchen, and Little Gem&rsquo;s own account promised the oven &ldquo;will be fired up again soon.&rdquo;"),
 ("Is there a menu yet?",
  "Not yet. Pie names, prices, hours and ordering channels get published when the shop itself announces them, on Instagram first. This site deliberately doesn&rsquo;t guess."),
 ("What will you pour?",
  "Wine and low-alcohol cocktails alongside the pizza, per the owner&rsquo;s interview with What Now Seattle."),
 ("How do I hear about opening day first?",
  "Two front doors: follow <a href=\"https://www.instagram.com/littlegemseattle/\" rel=\"noopener\">@littlegemseattle</a> on Instagram, or leave a note on the <a href=\"/contact\">contact page</a> — dates, menu and ordering news land there first."),
]

PAGES["faq.html"] = dict(
 title="Opening Questions — Little Gem, Madison Park Seattle",
 desc="Straight answers on dates, the dough recipe, wood-fired pizza and the planned wine list at 4235 E Madison Street, Madison Park, Seattle. Anything unannounced is marked pending, not guessed.",
 body=(
  '<section class="minihero"><div class="wrap"><span class="label">Everything we know</span>'
  '<h1>Madison Park&rsquo;s pizza <em>questions</em>, answered</h1>'
  '<p class="sub">Short answers with sources — and honest blanks: anything the shop hasn&rsquo;t announced yet is '
  'left pending rather than guessed.</p></div></section>'

  '<section class="block"><div class="wrap"><div class="faqsec"><div class="faqsec">' +
  "".join(f'<details><summary>{q}</summary><div class="qa"><p>{a}</p></div></details>' for q, a in FAQS) +
  '</div><p style="margin-top:28px">Something we didn&rsquo;t cover? <a href="/contact">Send a note</a> — '
  'every message gets an answer.</p></div></div></section>'
 ),
 ld=ld([{"@context": "https://schema.org", "@graph": [
   {"@type": "FAQPage", "@id": ORIGIN + "/faq/#faq", "mainEntity": [
     {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a.replace('&rsquo;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"')}} for q, a in FAQS]},
   webpage("Opening Questions", "/faq"), crumbs("Opening Questions", "/faq")]}]),
)

PAGES["contact.html"] = dict(
 title="Contact — Little Gem, 4235 E Madison St, Seattle",
 desc="Questions, menu wishes, opening news — the contact form reaches the team while the shop is pre-opening. 4235 E Madison St, Madison Park, Seattle WA 98112.",
 body=(
  '<section class="minihero"><div class="wrap"><span class="label">Before opening day</span>'
  '<h1>Send <em>a note</em></h1>'
  '<p class="sub">Questions, menu wishes, neighborly nudges — the form is the front door while the shop is '
  'pre-opening, and the team is reading.</p></div></section>'

  '<section class="block"><div class="wrap"><div class="mapgrid">'
  '<div><h2>Talk to the team</h2>'
  '<form class="cform" method="post" action="/contact">'
  '<label class="cfield"><span>Name *</span><input name="name" required autocomplete="name" placeholder="Your name"></label>'
  '<label class="cfield"><span>Phone</span><input name="phone" autocomplete="tel" placeholder="Optional"></label>'
  '<label class="cfield wide"><span>Email</span><input name="email" type="email" autocomplete="email" placeholder="Optional — so we can reply there"></label>'
  '<label class="cfield wide"><span>Message *</span><textarea name="message" required placeholder="Menu wishes, opening-date questions, anything…"></textarea></label>'
  '<p class="cnote">* required. The shop doesn&rsquo;t have a phone line yet — this form reaches the team directly, '
  'and every note gets an answer. We use what you leave only to reply — see <a href="/privacy">privacy</a>.</p>'
  '<div class="cfield wide"><button class="btn" type="submit">Send it</button></div></form></div>'
  '<div>' + MAPCELL +
  '<div class="infofoot"><h3>The corner</h3><address>4235 E Madison St<br>Madison Park · Seattle, WA 98112</address>'
  '<p style="margin-top:10px">Hours and a shop phone arrive with opening day — until then, this form and '
  '<a href="' + IGURL + '" rel="noopener">@littlegemseattle</a> are the front doors.</p></div>' + MAPNOTE + '</div>'
  '</div></div></section>'
 ),
 ld=ld([{"@context": "https://schema.org", "@graph": [webpage("Contact", "/contact"), crumbs("Contact", "/contact")]}]),
)

PAGES["privacy.html"] = dict(
 title="Privacy Policy — Little Gem, Madison Park Seattle",
 desc="How Little Gem handles what you leave on this site: the contact note only. No trackers, no cookies, no advertising, no data sale.",
 body=(
  '<section class="minihero"><div class="wrap"><span class="label">The short version</span>'
  '<h1>Privacy, <em>plainly</em></h1>'
  '<p class="sub">This site collects as little as it can. What you leave here stays with the shop.</p>'
  '<div class="ctas" style="margin-top:20px"><a class="btn" href="/contact">Contact the shop</a>'
  '<a class="btn ghost" href="/">Front page</a></div></div></section>'

  '<section class="block"><div class="wrap"><div class="prose">'
  '<h2>What gets kept</h2>'
  '<p class="lede">Fill in the contact form and the shop receives your name, email, phone (if you left one) and '
  'your message. That&rsquo;s it. It&rsquo;s used to answer you and kept by the Little Gem team — not shared, not '
  'sold, not used for advertising.</p>'
  '<p style="margin-top:16px">The map image is served by Google Maps, which sees your IP address while the map '
  'loads. The web host also logs routine technical details (IP address, browser type) to keep the site running.</p>'
  '<h2 style="margin-top:44px">What doesn&rsquo;t happen</h2>'
  '<p class="lede">No advertising networks. No tracking scripts. No analytics cookies. No third-party pixels. '
  'Nothing you type here builds a profile about you.</p>'
  '<p style="margin-top:16px">To see or have removed anything held from you, say the word on the '
  '<a href="/contact">contact page</a>.</p></div></div></section>'
 ),
 ld=ld([{"@context": "https://schema.org", "@graph": [webpage("Privacy", "/privacy"), crumbs("Privacy", "/privacy")]}]),
)

PAGES["404.html"] = dict(
 title="Page not found — Little Gem, Madison Park Seattle",
 desc="The page you were after isn't here. Back to Little Gem — the neighborhood pizzeria coming to 4235 E Madison Street, Madison Park, Seattle.",
 body=(
  '<section class="hero solo"><div class="wrap"><div class="herotext"><span class="label">404</span>'
  '<h1>This page is <em>not on the menu</em></h1>'
  '<p class="sub">Whatever you were after isn&rsquo;t here. The front page has everything that is.</p>'
  '<hr class="rule"><div class="ctas"><a class="btn" href="/">Front page</a>'
  '<a class="btn ghost" href="/contact">Contact us</a></div></div></div></section>'
 ), ld="",
)

PAGES["thanks.html"] = dict(
 title="Message sent — Little Gem, Madison Park Seattle",
 desc="Your note reached Little Gem — the neighborhood pizzeria coming to 4235 E Madison Street, Madison Park, Seattle.",
 body=(
  '<section class="hero solo"><div class="wrap"><div class="herotext"><span class="label">Message received</span>'
  '<h1>Your note <em>came through</em></h1>'
  '<p class="sub">Thank you — the team reads every one. Opening news (dates, menu, ordering) goes out on Instagram '
  'first, so follow along so you don&rsquo;t miss it.</p><hr class="rule">'
  '<div class="ctas"><a class="btn" href="' + IGURL + '" rel="noopener">Follow on Instagram</a>'
  '<a class="btn ghost" href="/">Back to the front page</a></div></div></div></section>'
 ), ld="",
)

for fname, P in PAGES.items():
    path = "/" if fname == "index.html" else "/" + fname[:-5]
    doc = head(P["title"], P["desc"], path) + P["body"] + "\n" + P["ld"] + "</body>\n</html>\n"
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(doc)
    print("wrote", fname, len(doc), "bytes")

core = ["/", "/our-pizza", "/wood-fired-pizza-madison-park", "/pizza-takeout-madison-park",
        "/faq", "/contact", "/privacy"]
sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f'<url><loc>{ORIGIN}{p if p != "/" else "/"}</loc><lastmod>2026-11-21</lastmod></url>\n'
                .replace("</loc>", "</loc>") for p in core).replace(ORIGIN + "//", ORIGIN + "/")
      + "</urlset>\n")
sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f'<url><loc>{ORIGIN}{p}</loc><lastmod>2026-11-21</lastmod></url>\n' for p in core)
      + "</urlset>\n")
open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n")
open(os.path.join(OUT, "favicon.svg"), "w").write(
 '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="18" fill="#471122"/>'
 '<g fill="none" stroke="#f6efe0" stroke-linecap="round" stroke-linejoin="round">'
 '<path d="M50 14 76 27 88 50 76 73 50 86 24 73 12 50 24 27Z" stroke-width="5"/>'
 '<path d="M50 28 62 34 68 50 62 66 50 72 38 66 32 50 38 34Z" stroke-width="4"/></g>'
 '<path d="M38 34l24 32" stroke="#b9892f" stroke-width="3" fill="none" stroke-linecap="round"/></svg>')
print("sitemap/robots/favicon written")
