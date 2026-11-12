#!/usr/bin/env python3
"""Assemble skyrundenver.com v0.1 pages from shared partials. Run: python3 -I build_site.py <site dir>"""
import sys, pathlib
SITE = pathlib.Path(sys.argv[1])
CITIES = ['Denver', 'Arvada', 'Wheat Ridge', 'Lakewood', 'Englewood', 'Centennial']

# City rules. Drafted 2026-11-12 from each city's own pages; pending SkyRun Denver sign off (the [Draft] tag comes off on sign off).
RULES_REVIEWED = 'November 12, 2026'
RULES_TAG = '[Draft, pending SkyRun Denver sign off]'
RULES = {
    'Denver': ('A short-term rental license covers stays of 29 nights or fewer and requires the home to be the host\'s primary residence. Stays of 30 nights or more fall under the residential rental property license instead.', 'https://denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Business-Licensing/Business-licenses/Short-term-rentals'),
    'Arvada': ('Short-term rentals are licensed by the city, up to three licenses per person at $350 a year. A 2026 proposal would limit owners to one license and add enforcement, with a council hearing still to come.', 'https://speakup.arvadaco.gov/short-term-rentals'),
    'Wheat Ridge': ('Licensed since 2021. Owner occupied partial home rentals are not capped. Whole home rentals are capped at 2 percent of homes per council district, with waitlists in three of four districts, and a 10 percent lodgers\' tax applies.', 'https://co-wheatridge3.civicplus.com/STR'),
    'Lakewood': ('Licensed since May 2023 and limited to the owner\'s primary residence, with proof of residence, $500,000 liability coverage with a short-term rental endorsement, a third party inspection, and certified notice to neighbors. $150 new, $75 renewal.', 'https://www.lakewoodco.gov/City-Hall/Departments/City-Clerks-Office/CCO-services-permits-registrations/Short-Term-Rental-License'),
    'Englewood': ('Stays under 30 nights need a license and an annual inspection, and the home must be an owner\'s primary residence, 185 days a year, unless the board grants a waiver. City sales tax of 3.8 percent and lodger\'s tax of 2 percent apply.', 'https://englewoodco.gov/government/city-departments/community-development/short-term-rentals-new/frequently-asked-questions-about-short-term-rentals'),
    'Centennial': ('Every short-term rental under 30 nights needs a city license, $150 a year plus a $50 application fee, liability insurance, two off street parking spaces, and occupancy of two per bedroom up to eight. The city pages state no primary residence requirement.', 'https://centennialco.gov/Residents/Living-Here/Short-Term-Rental'),
}
ORIGIN = 'https://skyrundenver.com'

def head(title, desc, path, extra=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{ORIGIN}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SkyRun Denver">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{ORIGIN}{path}">
<meta property="og:image" content="{ORIGIN}/assets/img/skyrun-denver-horizontal.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/assets/fonts/schibsted-grotesk-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
<link rel="icon" href="/assets/img/favicon.png" type="image/png">
{extra}
<!-- GA4: G-SFVBFCQWDM. Installed through Google Tag Manager at launch; see the measurement spec. -->
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def header(current, dark=False, over=False):
    def a(href, label, key, quiet=False):
        cur = ' aria-current="page"' if key == current else ''
        q = ' class="quiet"' if quiet else ''
        return f'<a href="{href}"{cur}{q}>{label}</a>'
    cls = 'site-head' + (' dark' if dark else '') + (' over' if over else '')
    return f"""<header class="{cls}" id="top"><div class="wrap">
  <a class="logo" href="/" aria-label="SkyRun Denver home"><img class="lg-light" src="/assets/img/skyrun-denver-horizontal-white.png" width="922" height="267" alt="SkyRun Vacation Rentals, serving the Denver Metro Area"><img class="lg-dark" src="/assets/img/skyrun-denver-horizontal.png" width="922" height="267" alt=""></a>
  <nav class="nav" id="nav" aria-label="Main">
    {a('/#homes', 'Homes', 'homes')}
    {a('/#month', 'A month with us', 'month')}
    {a('/#paths', 'Two ways to rent', 'paths')}
    {a('/operations', 'Operations', 'operations')}
    {a('/areas', 'Areas we serve', 'areas')}
    {a('https://skyrun.com/denver/', 'Find a stay', 'stay', True)}
    <a class="btn navcta" href="#evaluation">Request a property evaluation</a>
  </nav>
  <a class="btn{' sun' if dark else ''}" href="#evaluation">Request a property evaluation</a>
  <button class="menu" type="button" aria-controls="nav" aria-expanded="false"><span></span><span></span>Menu</button>
</div></header>
<main id="main">
"""

def footer():
    return f'''</main>
<footer class="site-foot"><div class="wrap">
  <div><a class="logo" href="/"><img src="/assets/img/skyrun-denver-horizontal.png" width="922" height="267" alt="SkyRun Vacation Rentals, serving the Denver Metro Area"></a><p class="pend" style="margin-top:12px">SkyRun Denver is an independently owned and operated SkyRun Vacation Rentals location. [Working wording; corporate approved disclosure pending]</p></div>
  <div><h4>Contact</h4><p><a href="tel:+17207281997">720-728-1997</a></p><p><a href="mailto:denver@skyrun.com">denver@skyrun.com</a></p><p>Locally operated, serving Denver, Arvada, Wheat Ridge, Lakewood, Englewood and Centennial.</p></div>
  <div><h4>Homeowners</h4><p><a href="/#paths">Two ways to rent</a></p><p><a href="/operations">Operations</a></p><p><a href="/areas">Areas we serve</a></p><p><a href="/#evaluation">Request a property evaluation</a></p></div>
  <div><h4>Guests and owners</h4><p><a href="https://skyrun.com/denver/" rel="noopener">Find a stay</a></p><p><a href="https://skyrundenver.trackhs.com/owner/" rel="noopener">Owner login</a></p><p><a href="https://skyrun.com/privacy-policy/" rel="noopener">Privacy</a></p></div>
</div></footer>
<a class="btn mcta" href="#evaluation">Request a property evaluation</a>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
'''

def form(page_label):
    opts = ''.join(f'<option>{c}</option>' for c in CITIES) + '<option>Outside these cities</option>'
    return f'''<form class="eval" name="property-evaluation" method="POST" action="/thank-you" data-netlify="true" netlify-honeypot="company" novalidate>
    <input type="hidden" name="form-name" value="property-evaluation">
    <p class="hp" aria-hidden="true"><label>Company <input name="company" tabindex="-1" autocomplete="off"></label></p>
    <div class="f"><label for="first">First name</label><input id="first" name="firstname" autocomplete="given-name" required></div>
    <div class="f"><label for="last">Last name</label><input id="last" name="lastname" autocomplete="family-name" required></div>
    <div class="f"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
    <div class="f"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
    <div class="f"><label for="city">Property city</label><select id="city" name="property_city" required><option value="">Choose</option>{opts}</select></div>
    <div class="f"><label for="type">Property type</label><select id="type" name="property_type"><option value="">Choose</option><option>House</option><option>Townhome</option><option>Condo</option><option>ADU or carriage house</option></select></div>
    <div class="f full"><label for="status">Where things stand today</label><select id="status" name="rental_status"><option value="">Choose</option><option>Renting short-term now</option><option>Renting furnished monthly now</option><option>Working with another manager</option><option>Not renting yet</option></select></div>
    <div class="f full"><label for="notes">Anything we should know (optional)</label><textarea id="notes" name="message"></textarea></div>
    <input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign"><input type="hidden" name="utm_term"><input type="hidden" name="utm_content"><input type="hidden" name="gclid"><input type="hidden" name="landing_page" value="{page_label}">
    <label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree to be contacted by SkyRun Denver about my property.</label>
    <button class="btn" type="submit">Request a property evaluation</button>
    <p class="privacy">We use what you send here to follow up about your property and nothing else. <a href="https://skyrun.com/privacy-policy/" rel="noopener">Privacy policy</a>. [Corporate to confirm the policy covers this site, the form, and analytics]</p>
  </form>'''

def ask(page_label):
    return f'''<section class="ask" id="evaluation"><div class="wrap">
  <div>
    <h2 class="h2 rv" id="ft">Request a property evaluation.</h2>
    <p class="lede">We walk the home, read your city's rules, and tell you which path fits, or whether neither does. No cost, no commitment.</p>
  </div>
  {form(page_label)}
</div></section>
'''

def areas_table():
    rows = ''.join(f'<tr><td>{c}</td><td>{RULES[c][0]} <span class="small">Reviewed {RULES_REVIEWED}. {RULES_TAG}</span></td><td><a href="#evaluation" data-city="{c}">Start in {c}</a></td></tr>' for c in CITIES)
    return f'''<section class="areas" id="areas"><div class="wrap">
  <h2 class="word rv">Six <em class="acc">cities.</em></h2>
  <p class="lede" style="font-size:19px;line-height:1.5;max-width:46ch">Where we work, and what each one asks of you.</p>
  <table class="tbl"><tbody>{rows}
    <tr><td style="font-size:20px;color:var(--mute)">Somewhere else nearby</td><td>Ask. We will tell you straight whether we can cover it.</td><td><a href="#evaluation" data-city="Outside these cities">Ask us</a></td></tr>
  </tbody></table>
  <p class="small" style="margin-top:20px">Full detail for each city, with the map, on <a href="/areas" style="color:var(--sky-ink)">Areas we serve</a>.</p>
</div></section>
'''

def split(page='home'):
    panel = '<a href="https://www.gostayready.com/denver" rel="noopener">StayReady in Denver</a>' if page == 'operations' else '<a href="https://www.gostayready.com/" rel="noopener">About StayReady</a>'
    return f'''<section class="split" id="ops"><div class="wrap">
  <div class="col">
    <h3>Managed by SkyRun Denver</h3>
    <ul>
      <li><b>You.</b> The owner relationship, the rental program, the monthly statement, the call when you have a question.</li>
      <li><b>Guests.</b> Listings, screening, messaging, pricing, reviews.</li>
      <li><b>Money.</b> Monthly owner statements and distribution of net proceeds under the management agreement. Applicable lodging tax coordinated where SkyRun Denver controls the receipts.</li>
      <li><b>Rules.</b> Help understanding rental eligibility and local licensing. Licenses and permits stay in your name.</li>
    </ul>
    <p class="part">SkyRun Denver is an independently owned and operated SkyRun Vacation Rentals location. [Working wording; corporate approved disclosure pending]</p>
  </div>
  <div class="col">
    <h3>Field operations by StayReady</h3>
    <p style="margin:0 0 16px;font-size:15px;color:var(--mute)">The field work between guests, on one accountable record. <a href="/operations" style="color:var(--sky-ink)">See a turnover, hour by hour</a></p>
    <ul>
      <li><b>Cleaning.</b> The 100+ point turnover checklist across eight zones, every stay.</li>
      <li><b>Linens.</b> A managed linen program, swapped per turn.</li>
      <li><b>Restocking.</b> Supplies to par, counted and logged.</li>
      <li><b>Inspections.</b> Every room, photographed.</li>
      <li><b>Maintenance.</b> Repairs dispatched, documented, closed.</li>
      <li><b>Seasonal and exterior.</b> Snow, lawn, irrigation, hot tubs.</li>
    </ul>
    <p class="part">SkyRun Denver manages the owner relationship and the rental program. StayReady is our independent field operations partner for turnover readiness and other approved on site services. {panel}</p>
  </div>
</div></section>
'''

def voice():
    # Owner testimonials, verbatim with permission. Three placeholder slides until Sebastien supplies real ones; nothing in brackets ships.
    slides = [
        ('[Owner review one, in the owner\'s own words, used with permission.]', '[Owner name, neighborhood]', 'Short stays since [year]'),
        ('[Owner review two.]', '[Owner name, neighborhood]', 'Monthly stays since [year]'),
        ('[Owner review three.]', '[Owner name, neighborhood]', 'Short stays since [year]'),
    ]
    items = ''.join(f'<li class="slide"><blockquote>{q}</blockquote><cite>{c}<small>{m}</small></cite></li>' for q, c, m in slides)
    dots = ''.join(f'<button type="button" aria-label="Review {i + 1}"{" aria-current=\"true\"" if i == 0 else ""}></button>' for i in range(len(slides)))
    return f'''<section class="voice" id="reviews" aria-label="Owner reviews"><div class="wrap">
  <div class="voice-head">
    <h2 class="word rv">Owners <em class="acc">say.</em></h2>
    <p class="gline"><span class="stars" aria-hidden="true">★★★★★</span> <a href="https://www.google.com/maps/search/SkyRun+Vacation+Rentals+Denver" rel="noopener">5.0 on Google, 38 reviews</a><br><span class="small">Owner reviews below, in their words, with permission.</span></p>
  </div>
  <div class="carousel">
    <ul class="slides" tabindex="0" aria-live="polite">{items}</ul>
    <div class="ctl"><button type="button" class="prev" aria-label="Previous review">←</button><div class="dots">{dots}</div><button type="button" class="next" aria-label="Next review">→</button></div>
  </div>
</div></section>
'''

def paths():
    return '''<section class="paths" id="paths"><div class="wrap">
  <h2 class="word rv">Two <em class="acc">ways.</em></h2>
  <p class="lede" style="font-size:19px;line-height:1.5;max-width:46ch">Every home is different, and so are the rules in each city. The evaluation starts by working out which path fits yours, and one manager decides with you.</p>
  <div class="paths-ed">
    <div class="path rv d1"><div class="photo" data-label="Photo: a short stay home, staged and guest ready"></div><h3>Short stays</h3><p>Nightly and weekly guests on the major booking sites. Pricing reviewed against comparable Denver homes and moved for events and seasons. The full turn after every stay, run by StayReady.</p><p class="fit">A fit when the home qualifies for a short-term rental license and you want the higher turnover rhythm.</p></div>
    <div class="path rv d2"><div class="photo alt" data-label="Photo: a furnished monthly home, lived in and calm"></div><h3>Monthly stays</h3><p>Furnished stays of 30 nights or more for traveling professionals, relocations, and families between homes. Set per lease, a mid stay check, fewer turnovers.</p><p class="fit">A fit when licensing does not fit, or you prefer fewer guests and steadier months.</p></div>
  </div>
</div></section>
'''

def homes():
    cards = [
        ('Photo: featured managed home, exterior at golden hour', '[Home name]', '[Neighborhood, city] · [Bedrooms and baths] · Short stays'),
        ('Photo: living room, morning light', '[Home name]', '[Neighborhood, city] · Monthly stays'),
        ('Photo: kitchen, staged and guest ready', '[Home name]', '[Neighborhood, city] · Short stays'),
        ('Photo: primary bedroom', '[Home name]', '[Neighborhood, city] · Monthly stays'),
        ('Photo: back patio or yard', '[Home name]', '[Neighborhood, city] · Short stays'),
    ]
    items = ''.join(f'<figure class="card"><div class="photo{" alt" if i % 2 else ""}" data-label="{l}"></div><figcaption><h3>{n}</h3><p>{m}</p></figcaption></figure>' for i, (l, n, m) in enumerate(cards))
    return f"""<section class="homes" id="homes">
  <div class="wrap head"><h2 class="word rv">Homes.</h2><p class="lede" style="font-size:19px;line-height:1.5;max-width:46ch">A few of the homes we manage across the metro. [Real homes, with owner permission and licensed photos, replace these before launch.]</p><p class="hint small">Scroll sideways</p></div>
  <div class="strip" tabindex="0" aria-label="Managed homes gallery">{items}</div>
</section>
"""

def letter():
    return '''<section class="letter" id="letter"><div class="wrap">
  <div><h2 class="word rv">From <em class="acc">us.</em></h2><p class="lede" style="font-size:19px;line-height:1.5;max-width:40ch">What the relationship is, in plain words, from the person who runs it.</p><div class="photo alt" style="margin-top:28px" data-label="Photo: Sebastien and the Denver team"></div></div>
  <div class="card rv d1">
    <p>Hi, I am Sebastien, owner of SkyRun Denver.</p>
    <p>I have always believed there is a big difference between getting a property booked and managing it well. Anyone can put a home on Airbnb. The real value comes from knowing how to position it, when to adjust pricing, which reservations make sense, and how to protect the property and the owner's bottom line along the way.</p>
    <p>Around Denver, there is no one size fits all strategy. Depending on the property, the local regulations, and what you are trying to accomplish, a short-term rental might be the right play. Or a furnished 30+ day rental might make a whole lot more sense. We look at the market, run the numbers, consider the costs, and help you make an informed decision rather than simply telling you what you want to hear.</p>
    <p>Once we have the right strategy, our job is to make the ownership experience easier. We handle the pricing, reservations, guest communication, and ongoing management, with our StayReady partners taking care of the hands on work that keeps the home ready. You will know what is happening with your property, how it is performing, and who to call when something needs attention.</p>
    <p>I am not interested in winning your business with an impressive looking revenue projection that does not hold up in the real world. I would rather show you the opportunities, explain the tradeoffs, and build a relationship that makes sense for both of us.</p>
    <p><strong>If you are considering professional management, let us have a conversation.</strong> Tell me a little about your property and what you are hoping to accomplish. We will figure out whether we are the right fit and what the smartest next move looks like.</p>
    <p class="sig">Sebastien Guite<br><span style="font-weight:400;color:var(--mute)">Location Owner, SkyRun Vacation Rentals Denver Metro</span></p>
  </div>
</div></section>
'''

# ---------------- Home ----------------
serving = ''.join(f'<span>{c}</span>' for c in CITIES)
mq = ''.join(f'<span>{c}</span>' for c in CITIES * 3)
home = head('SkyRun Denver | Short-Term and Furnished Rental Management for Denver Homeowners',
            'SkyRun Denver manages short-term and furnished 30+ day rentals for homeowners in Denver, Arvada, Wheat Ridge, Lakewood, Englewood, and Centennial. Request a property evaluation.', '/') + header('home', over=True) + f"""
<section class="hero-photo">
  <div class="photo rv" data-label="Photo: a managed Denver home at golden hour, full bleed, licensed and credited"></div>
  <div class="wrap copy">
    <p class="kicker">Short-term and furnished rental management, Denver metro</p>
    <h1 class="disp">Every decision about your home, <em class="acc">made in the open.</em></h1>
    <div class="acts"><a class="btn sun" href="#evaluation">Request a property evaluation</a><a class="btn glass" href="#month">See a month with us</a></div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="track">{mq}</div></div>

<section class="hero month" id="month"><div class="wrap">
  <div class="hero-l">
    <p class="kicker">One owner. One home in Wash Park. One month.</p>
    <h2 class="disp sub">This is what a month with us <em class="acc">looks like.</em></h2>
    <p class="lede">SkyRun Denver manages short-term and furnished 30+ day rentals for homeowners across the Denver metro. Every pricing call, every guest, every decision, explained as it happens. Here is one month.</p>
    <div class="acts"><a class="btn" href="#evaluation">Request a property evaluation</a><a class="btn ghost" href="#statement">See the owner statement</a></div>
    <p class="small" style="margin-top:36px"><strong style="color:var(--ink)">Serving</strong> {' · '.join(CITIES)}</p>
  </div>
  <div class="cal" aria-label="A sample month: short stays, turns, service visits, and the decisions behind them">
    <div class="head"><b>November</b><span>Sample month, [home name]</span></div>
    <div class="grid7" role="img" aria-label="Calendar: short stays with a turnover after each one, two StayReady service visits, an inspection flag fixed the same day, and a 30 night furnished stay that begins on the 24th and runs to December 23. Seven numbered decisions are listed below.">
      <div class="d b n" data-n="1">1</div><div class="d b">2</div><div class="d t n" data-n="2">3<em>turn</em></div><div class="d b">4</div><div class="d b">5</div><div class="d b">6</div><div class="d t">7<em>turn</em></div>
      <div class="d b n" data-n="3">8</div><div class="d b">9</div><div class="d t">10<em>turn</em></div><div class="d b">11</div><div class="d b s n" data-n="4">12<em>service</em></div><div class="d b">13</div><div class="d t">14<em>turn</em></div>
      <div class="d b">15</div><div class="d t i n" data-n="5">16<em>turn</em></div><div class="d b">17</div><div class="d b">18</div><div class="d b">19</div><div class="d t">20<em>turn</em></div><div class="d b">21</div>
      <div class="d b">22</div><div class="d t">23<em>turn</em></div><div class="d m n" data-n="6">24<em>night 1</em></div><div class="d m">25</div><div class="d m">26</div><div class="d m">27</div><div class="d m">28</div>
      <div class="d m">29</div><div class="d m n" data-n="7">30</div><div class="d m nx">Dec 1</div><div class="d m nx">2</div><div class="d m nx">3</div><div class="d m nx">4</div><div class="d m nx more">5<em>to Dec 23</em></div>
    </div>
    <p class="keyrow"><span><i></i>Short stay booked</span><span><i class="t"></i>Turnover: clean, linens, restock, inspection</span><span><i class="s"></i>Service visit</span><span><i class="i"></i>Inspection found and fixed</span><span><i class="m"></i>Furnished stay, 30 nights, Nov 24 to Dec 23</span><span>Numbered: a decision below</span></p>
    <div class="ledger">
      <div class="row"><span class="t">1</span><div><h3>Statement sent for October</h3><p>Nights, guests, every charge itemized, what we decided and why. Payout on its way.</p></div><span class="who">Owner relations</span></div>
      <div class="row"><span class="t">3</span><div><h3>First turn of the month</h3><p>Checkout at 10, cleaning crew at 10:40, fresh linens, restocked to par, the 100+ point turnover checklist, inspection with photos. Guest ready by 3:10 for a 4:00 check in. <a href="/operations" style="color:var(--sky-ink)">See the whole turn</a>.</p><div class="photo" data-label="Photo: the home, guest ready"></div></div><span class="who">Operations, by StayReady</span></div>
      <div class="row"><span class="t">8</span><div><h3>Rate raised for a Broncos home weekend</h3><p>Comparable Wash Park homes checked that morning. Two nights repriced, both booked.</p></div><span class="who">Pricing</span></div>
      <div class="row"><span class="t">12</span><div><h3>Property care visit between guests</h3><p>Scheduled under the home's service plan. Findings documented with photos. [Example visit; contents follow each home's agreed plan]</p></div><span class="who">Maintenance, by StayReady</span></div>
      <div class="row"><span class="t">16</span><div><h3>Inspection flagged a loose bath fan, fixed the same turn</h3><p>Found at 1:40, tightened by 2:30, before and after photos attached. The next guest never knew.</p><div class="photo alt" data-label="Photo: the inspection"></div></div><span class="who">Inspection and maintenance, by StayReady</span></div>
      <div class="row"><span class="t">24</span><div><h3>Switched to a 30 night furnished stay</h3><p>A relocating family asked for the full month through December 23. Better for the home in a slow season; we recommended it, you approved it. One turn instead of eight, and a property care visit scheduled under the service plan for December 9.</p></div><span class="who">Owner relations</span></div>
      <div class="row"><span class="t now">30</span><div><h3>Lodging tax coordinated</h3><p>Applicable lodging tax remitted where SkyRun Denver controls the receipts; some booking platforms remit certain taxes directly. Shown on the statement.</p></div><span class="who">Owner relations</span></div>
      <p class="foot">Sample month. Dates, the home, and counts are illustrative until a real month is published with the owner's permission. No revenue figures appear on this site.</p>
    </div>
  </div>
</div></section>

<section class="band"><div class="photo rv" data-label="Photo: the same home, interior, late afternoon, licensed and credited"></div><p class="cap">[Caption: the home, the neighborhood, the photographer]</p></section>

<section class="record" id="statement"><div class="wrap">
  <div>
    <h2 class="word rv">The <em class="acc">first.</em></h2>
    <p class="lede" style="margin-top:18px"><strong style="color:var(--ink)">Your statement, every month.</strong></p>
    <p class="lede">Not a payout and a line. Rental activity, revenue, fees, owner expenses and adjustments, with reservation detail in your owner portal. The decisions behind the numbers, explained when we make them.</p>
    <p class="small" style="margin-top:20px">Counts only. Revenue and fee figures are never published on this site.</p>
  </div>
  <div class="stmt" aria-label="Sample owner statement">
    <div class="top"><span>[Home name], Wash Park</span><span>November statement</span></div>
    <div class="grid">
      <div class="cell"><b>23</b><span>short stay nights, 7 turns</span></div>
      <div class="cell"><b>7</b><span>furnished stay nights, of 30</span></div>
      <div class="cell"><b>2</b><span>service visits</span></div>
      <div class="cell"><b>1</b><span>issue found and fixed</span></div>
    </div>
    <div class="photos"><div class="photo"></div><div class="photo alt"></div><div class="photo"></div><div class="photo alt"></div><div class="photo"></div><div class="photo alt"></div></div>
    <p class="note">Sample counts. Real statements replace these at launch.</p>
  </div>
</div></section>
""" + homes() + paths() + split() + letter() + areas_table() + voice() + ask('home') + footer()
(SITE / 'index.html').write_text(home)

# ---------------- Operations ----------------
ops = head('Operations | What Happens to Your Home Between Guests | SkyRun Denver',
           'One turnover, hour by hour. StayReady runs the cleaning, linens, restocking, inspections, and maintenance behind every SkyRun Denver stay.', '/operations') + header('operations') + '''
<section class="hero"><div class="wrap">
  <div class="hero-l">
    <p class="kicker">Operations. A Tuesday in Wash Park, checkout at 10:00, check in at 4:00.</p>
    <h1 class="disp">Between guests, your home is <em class="acc">StayReady's job.</em></h1>
    <p class="lede">SkyRun Denver manages the stay. StayReady, the <a href="https://www.gostayready.com/hospitality-field-operations" rel="noopener">hospitality field operations company</a> based here in Colorado, runs the work underneath it: cleaning, linens, restocking, inspections, maintenance, seasonal and exterior services, and property readiness. Here is one turn, hour by hour.</p>
    <div class="acts"><a class="btn" href="#evaluation">Request a property evaluation</a><a class="btn ghost" href="#record">See the owner record</a></div>
  </div>
  <div class="cal" aria-label="One turnover, hour by hour"><div class="ledger">
    <div class="head"><span>Time</span><span>What happened</span><span style="text-align:right">Who</span></div>
    <div class="row"><span class="t big">10:00</span><div><h3>Guests check out</h3><p>Smart lock code expires. Checkout photos requested from the guest.</p></div><span class="who">SkyRun Denver</span></div>
    <div class="row"><span class="t big">10:40</span><div><h3>Cleaning team arrives</h3><p>Two person crew working the <a href="https://www.gostayready.com/turnover-cleaning" rel="noopener">100+ point turnover checklist</a> across eight zones: kitchen, baths, floors, every surface.</p><div class="photo" data-label="Photo: crew arrival"></div></div><span class="who">StayReady cleaning</span></div>
    <div class="row"><span class="t big">12:15</span><div><h3>Linens swapped, not washed onsite</h3><p>Fresh set from the linen program. Used set bagged for the laundry route.</p></div><span class="who">StayReady linens</span></div>
    <div class="row"><span class="t big">1:05</span><div><h3>Restocked to par</h3><p>Paper, soap, coffee, dish pods. Counts logged against the home's par list.</p></div><span class="who">StayReady restocking</span></div>
    <div class="row"><span class="t big">1:40</span><div><h3>Inspection, every room</h3><p>A <a href="https://www.gostayready.com/inspections" rel="noopener">readiness inspection</a>: appliances, fixtures, locks, thermostat, staging. Loose bath fan noted and sent to maintenance.</p><div class="photo alt" data-label="Photo: inspection"></div></div><span class="who">StayReady inspection</span></div>
    <div class="row"><span class="t big">2:30</span><div><h3>Bath fan tightened</h3><p>Same day. Before and after photos attached to the home's record.</p></div><span class="who">StayReady maintenance</span></div>
    <div class="row"><span class="t big now">3:10</span><div><h3>Guest ready</h3><p>Record closed. Every step, photo, and count documented for the home.</p></div><span class="who">SkyRun Denver</span></div>
    <div class="row"><span class="t big">4:00</span><div><h3>Next guests check in</h3><p>New lock code live. Welcome message sent.</p></div><span class="who">SkyRun Denver</span></div>
    <p class="foot">Sample turn. Times and the home are illustrative until a real turnover is published with the owner's permission.</p>
  </div></div>
</div></section>

<section class="band"><div class="photo rv" data-label="Photo: the StayReady crew at work in a Denver home, full width, licensed and credited"></div><p class="cap">[Caption: the home, the crew, the photographer]</p></section>

<section class="record" id="record"><div class="wrap">
  <div>
    <h2 class="word rv">The <em class="acc">record.</em></h2>
    <p class="lede" style="margin-top:18px"><strong style="color:var(--ink)">Documented after every stay.</strong></p>
    <p class="lede">Not a monthly summary. The actual checklist, photos, counts, and issues from each turnover, kept on the home's record.</p>
    <p class="small" style="margin-top:20px">[How and when owners see this record is being confirmed; no owner portal delivery is promised until it is]</p>
  </div>
  <div class="stmt" aria-label="Sample owner record">
    <div class="top"><span>[Home name], Wash Park</span><span>Turn closed 3:10 PM</span></div>
    <div class="grid">
      <div class="cell"><b>112</b><span>checklist items passed</span></div>
      <div class="cell"><b>0</b><span>items failed</span></div>
      <div class="cell"><b>14</b><span>photos attached</span></div>
      <div class="cell"><b>1</b><span>issue found and fixed</span></div>
    </div>
    <div class="photos"><div class="photo"></div><div class="photo alt"></div><div class="photo"></div><div class="photo alt"></div><div class="photo"></div><div class="photo alt"></div></div>
    <p class="note">Sample figures. Real records replace these at launch.</p>
  </div>
</div></section>
''' + split('operations') + ask('operations') + footer()
(SITE / 'operations.html').write_text(ops.replace('<section class="band">', '<section class="band">', 1))

# ---------------- Areas ----------------
chips = ''.join(f'<button class="chip" type="button" data-city="{c}" aria-pressed="false">{c}</button>' for c in CITIES)
rules = ''.join(f'<li><b>{c}<small>Reviewed {RULES_REVIEWED}</small></b><p>{RULES[c][0]} <a href="{RULES[c][1]}" rel="noopener" class="src">City source</a>. <a href="#evaluation" data-city="{c}">Start in {c}</a></p><p class="small pend">{RULES_TAG}</p></li>' for c in CITIES)
areas = head('Areas We Serve | Denver, Arvada, Wheat Ridge, Lakewood, Englewood, Centennial | SkyRun Denver',
             'SkyRun Denver manages short-term and furnished rentals in Denver, Arvada, Wheat Ridge, Lakewood, Englewood, and Centennial. Each city has its own rules; the evaluation starts with yours.', '/areas') + header('areas', dark=True) + f'''
<section class="maphero"><div class="wrap">
  <div>
    <h1>Your home is on this map. <em class="acc">So are we.</em></h1>
    <p class="lede">Six Denver metro communities, each with its own short-term rental rules. In Denver, Lakewood, and Englewood a home that is not your primary residence cannot be licensed for short stays, which is where a furnished 30 night stay earns its place. Pick your community to start a property evaluation.</p>
    <p class="pickline" id="pl">Pick your community</p>
    <div class="chips" role="group" aria-labelledby="pl">{chips}<button class="chip" type="button" data-city="Outside these cities" aria-pressed="false">Somewhere else nearby</button></div>
  </div>
  <div class="map">
    <svg viewBox="0 0 600 560" role="img" aria-label="Schematic map of the Denver metro with the six communities SkyRun Denver serves">
      <g class="range">
        <path class="snow" d="M20 40 L60 10 L95 60 L130 25 L165 80 L200 40 L230 95"/>
        <path d="M0 110 L45 80 L80 130 L120 95 L150 150 L185 115 L215 165 L245 135"/>
        <path d="M0 200 L35 170 L70 215 L105 185 L135 240 L170 205 L200 255"/>
        <path d="M0 300 L30 270 L60 315 L95 285 L125 340 L160 305 L190 360"/>
        <path d="M0 400 L30 370 L60 415 L95 385 L125 440 L160 405"/>
        <path d="M0 500 L30 470 L60 515 L95 485"/>
      </g>
      <g class="roads">
        <path class="i" d="M380 0 L385 160 L395 330 L400 470 L410 560"/>
        <path class="i" d="M160 140 L260 220 L330 300 L395 330 L560 300"/>
        <path d="M250 330 L395 330 L540 340"/>
        <path d="M300 420 L410 400 L520 460"/>
        <path d="M330 220 L470 240"/>
      </g>
      <text class="sm" x="20" y="100">Front Range</text>
      <text class="sm" x="392" y="16">I-25</text>
      <text class="sm" x="172" y="134">I-70</text>
      <g class="city" data-city="Arvada"><circle cx="330" cy="255" r="9"/><text x="346" y="260">Arvada</text></g>
      <g class="city" data-city="Wheat Ridge"><circle cx="320" cy="300" r="9"/><text x="336" y="305">Wheat Ridge</text></g>
      <g class="city" data-city="Denver"><circle cx="400" cy="330" r="14"/><text x="420" y="336" style="font-size:18px">Denver</text></g>
      <g class="city" data-city="Lakewood"><circle cx="300" cy="360" r="9"/><text x="316" y="365">Lakewood</text></g>
      <g class="city" data-city="Englewood"><circle cx="395" cy="430" r="9"/><text x="411" y="435">Englewood</text></g>
      <g class="city" data-city="Centennial"><circle cx="470" cy="500" r="9"/><text x="486" y="505">Centennial</text></g>
    </svg>
    <p class="key">Schematic, not to scale. Tap a community to start an evaluation there.</p>
  </div>
</div></section>

<section class="areas" id="rules"><div class="wrap">
  <h2 class="h2 rv">Every city writes its own rules. We know them.</h2>
  <p class="lede" style="font-size:19px;line-height:1.5;margin:20px 0 0;max-width:48ch">Short-term rental licensing, primary residence requirements, and lodging tax differ from one city line to the next. The evaluation starts by reading the rules that apply to your home.</p>
  <ul class="rules">{rules}</ul>
  <p class="small" style="margin-top:20px">Rules summaries are verified against each city's current code and carry the date they were last reviewed. They are general information, not legal advice or a guarantee that a specific home qualifies.</p>
</div></section>
''' + ask('areas') + footer()
(SITE / 'areas.html').write_text(areas)

# ---------------- Thank you ----------------
thanks = head('Evaluation Requested | SkyRun Denver', 'Your property evaluation request is in. The SkyRun Denver team follows up to schedule a walkthrough.', '/thank-you',
              '<meta name="robots" content="noindex">') + header('thanks') + '''
<section class="thanks"><div class="wrap">
  <p class="kicker">Evaluation requested</p>
  <h1 class="h2">Got it. A member of the SkyRun Denver team will be in touch.</h1>
  <p class="lede">We will be in touch soon. We review your home and your city's rules, then schedule a walkthrough. If anything is urgent, call <a href="tel:+17207281997">720-728-1997</a>.</p>
  <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn ghost" href="/operations">See what happens between guests</a><a class="btn ghost" href="/areas">Read your city's rules</a></div>
</div></section>
''' + footer().replace('<a class="btn mcta" href="#evaluation">Request a property evaluation</a>', '')
(SITE / 'thank-you.html').write_text(thanks)

# ---------------- Support files ----------------
(SITE / 'netlify.toml').write_text('''[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

# Pre launch: production is noindexed too. Remove the production block at launch (Round 6).
[context.production]
  command = "printf '/*\\n  X-Robots-Tag: noindex\\n' >> _headers"

# Branch deploys and deploy previews never index.
[context.deploy-preview]
  command = "printf '/*\\n  X-Robots-Tag: noindex\\n' >> _headers"
[context.branch-deploy]
  command = "printf '/*\\n  X-Robots-Tag: noindex\\n' >> _headers"
''')
(SITE / '_redirects').write_text('''/index.html   /            301
/operations.html  /operations  301
/areas.html   /areas       301
/thank-you.html  /thank-you  301
''')
(SITE / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /thank-you\nSitemap: {ORIGIN}/sitemap.xml\n')
(SITE / 'sitemap.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{ORIGIN}/</loc><lastmod>2026-11-06</lastmod></url>
  <url><loc>{ORIGIN}/operations</loc><lastmod>2026-11-06</lastmod></url>
  <url><loc>{ORIGIN}/areas</loc><lastmod>2026-11-06</lastmod></url>
</urlset>
''')
(SITE / 'README.md').write_text('''# skyrundenver.com

v0.3 (2026-11-12): photo led hero, italic serif accents, city marquee, horizontal homes gallery, transparent header over the hero, mobile menu.

v0.2 (2026-11-11): warmer ground, hairline rules, Homes gallery, editorial two paths, letter from Sebastien, one word section titles.

Static site for SkyRun Denver. No build step: HTML, one stylesheet, one script, self hosted fonts. Deploys on push to main via Netlify.

Pages: `/` (A Month With Us), `/operations` (The Turn), `/areas` (the map and city rules), `/thank-you` (conversion page, noindex).

Lead form: Netlify Forms (`property-evaluation`) as the interim capture until the SkyRun Denver HubSpot account is live. Hidden fields carry utm_source, utm_medium, utm_campaign, utm_term, utm_content, gclid, and landing_page. Honeypot field: `company`. Set the Netlify form notification to Sebastien's inbox before launch.

Placeholders are in square brackets. Nothing in brackets ships.

Source pages are assembled by `tools/build_site.py` in the StayReady Websites workspace; edit there and regenerate, or edit the HTML directly and keep the partials in sync by hand.
''')
print('built', [p.name for p in SITE.iterdir()])
