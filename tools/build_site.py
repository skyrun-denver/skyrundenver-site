#!/usr/bin/env python3
"""Assemble skyrundenver.com v0.1 pages from shared partials. Run: python3 -I build_site.py <site dir>"""
import sys, pathlib
SITE = pathlib.Path(sys.argv[1])

# Cache busters: assets are served immutable for a year, so every CSS or JS change must change the URL.
import hashlib
def _v(path):
    f = SITE / path
    return hashlib.sha1(f.read_bytes()).hexdigest()[:8] if f.exists() else '0'
CSS_V = _v('assets/css/site.css')
JS_V = _v('assets/js/site.js')
CITIES = ['Denver', 'Arvada', 'Wheat Ridge', 'Lakewood', 'Englewood', 'Centennial']

# City rules. Drafted 2026-11-12 from each city's own pages; pending SkyRun Denver sign off (the [Draft] tag comes off on sign off).
# Photos. SkyRun Denver homes only: Kiela's shortlist (Drive folder 1qmCP4P8oT_n0ZMtdn68XQcQ64kC3fTxw, Nov 13) and the
# Cabin Door Media shoot of 192 S Madison St (Nov 3). Nothing that appears on gostayready.com. Web files are made by
# tools/make_photos.py, which applies the shared grade (tools/grade.py). Photo plan: https://claude.ai/artifact/MXL6ypCmvhDjeahW4uvgCA
PHOTOS = {
    'Photo: a managed Denver home at golden hour, full bleed, licensed and credited': ('rooftop-skyline', 'Rooftop deck with a fire table and a view of downtown Denver', '50% 62%', True),
    'Photo: the same home, interior, late afternoon, licensed and credited': ('living-kitchen', 'Open living room and kitchen in a managed Denver home', '50% 55%', False),
    'Photo: featured managed home, exterior at golden hour': ('townhome-exterior', 'Modern two story Denver townhome with a fenced front yard', '50% 50%', False),
    'Photo: kitchen, staged and guest ready': ('madison-kitchen', 'Kitchen with a waterfall island, pendant lights, and double ovens', '50% 50%', False),
    'Photo: primary bedroom': ('madison-bedroom', 'Primary bedroom with blue pillows and a textured accent wall', '50% 50%', False),
    'Photo: living room with character': ('brick-living', 'Living room with exposed brick walls and mid century chairs', '50% 50%', False),
    'Photo: back patio or yard': ('patio-firepit', 'Stone patio with built in seating around a fire pit', '50% 60%', False),
    'Photo: a short stay home, staged and guest ready': ('backyard-hot-tub', 'Backyard with a hot tub, fire pit, and stone seating', '55% 60%', False),
    'Photo: a furnished monthly home, lived in and calm': ('brick-reading-nook', 'Sitting area with two leather chairs against an exposed brick wall', '50% 55%', False),
    'Photo: the home, guest ready': ('living-lounge', 'Living room with an orange sofa and tall windows', '45% 50%', False),
}
def bust(html):
    """Add a content hash to every /assets/img URL. /assets/* is served immutable, so a changed photo needs a new URL."""
    import re
    return re.sub(r'(/assets/img/[\w/.-]+?\.(?:webp|png|jpg))(?![\w?])', lambda m: m.group(1) + '?v=' + _v(m.group(1).lstrip('/')), html)

def photos(html):
    import re
    def sub(m):
        cls, label = m.group(1), m.group(2)
        if label not in PHOTOS:
            return m.group(0)
        name, alt, pos, eager = PHOTOS[label]
        load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
        sizes = '100vw' if eager or 'band' in cls else '(max-width: 700px) 100vw, 50vw'
        big = f', /assets/img/homes/{name}-2400.webp 2400w' if (SITE / f'assets/img/homes/{name}-2400.webp').exists() else ''
        return (f'<div class="{cls} has-img"><img src="/assets/img/homes/{name}-1440.webp" '
                f'srcset="/assets/img/homes/{name}-800.webp 800w, /assets/img/homes/{name}-1440.webp 1440w{big}" sizes="{sizes}" '
                f'alt="{alt}" style="object-position:{pos}" {load}></div>')
    return re.sub(r'<div class="(photo[^"]*)"(?: style="[^"]*")? data-label="([^"]*)"></div>', sub, html)

RULES_REVIEWED = 'November 12, 2026'
RULES_TAG = ''  # Rules approved for launch with the site (Nov 19)
RULES = {
    'Denver': ('A short-term rental license covers stays of 29 nights or fewer and requires the home to be the host\'s primary residence. Stays of 30 nights or more fall under the residential rental property license instead.', 'https://denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Business-Licensing/Business-licenses/Short-term-rentals'),
    'Arvada': ('A short-term rental permit and a city business license are both required. Under rules in effect since May 1, 2026, one permit is allowed per lot (the main home or an accessory unit, not both), occupancy is two per bedroom plus two, and a home may operate up to 240 days in any 365.', 'https://www.arvadaco.gov/1507/Operating-a-short-term-rental'),
    'Wheat Ridge': ('Licensed since 2021. Owner occupied partial home rentals are not capped. Whole home rentals are capped at 2 percent of homes per council district, with waitlists in three of four districts, and a 10 percent lodgers\' tax applies.', 'https://co-wheatridge3.civicplus.com/STR'),
    'Lakewood': ('Licensed since May 2023 and limited to the owner\'s primary residence, with proof of residence, $500,000 liability coverage with a short-term rental endorsement, a third party inspection, and certified notice to neighbors. $150 new, $75 renewal.', 'https://www.lakewoodco.gov/City-Hall/Departments/City-Clerks-Office/CCO-services-permits-registrations/Short-Term-Rental-License'),
    'Englewood': ('Stays under 30 nights need a license and an annual inspection, and the home must be an owner\'s primary residence, 185 days a year, unless the board grants a waiver. City sales tax of 3.8 percent and lodger\'s tax of 2 percent apply.', 'https://englewoodco.gov/government/city-departments/community-development/short-term-rentals-new/frequently-asked-questions-about-short-term-rentals'),
    'Centennial': ('Every short-term rental under 30 nights needs a city license, $150 a year plus a $50 application fee, liability insurance, two off street parking spaces, and occupancy of two per bedroom up to eight. The city pages state no primary residence requirement.', 'https://centennialco.gov/Residents/Living-Here/Short-Term-Rental'),
}
ORIGIN = 'https://skyrundenver.com'

# Direct link to the SkyRun Denver Google Business Profile (share link from Matt, Nov 15, 2026).
GBP = 'https://maps.app.goo.gl/jnpnfg5YrXfy4CqS9'

MAP_SVG = '''<svg viewBox="0 0 600 560" role="img" aria-label="Schematic map of the Denver metro with the six communities SkyRun Denver serves">
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
    </svg>'''

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
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_V}">
<link rel="icon" href="/assets/img/favicon.png" type="image/png">
{extra}
{HS_TRACKING}
<meta name="msvalidate.01" content="4C8477B52376714CF481D739F1D6C362">
{tags()}
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
    {a('/#month', 'How We Work', 'month')}
    {a('/#ready', '5-Star Ready', 'ready')}
    {a('/operations', 'Operations', 'operations')}
    {a('/areas', 'Areas', 'areas')}
    <a href="https://skyrun.com/blog/category/denver/" rel="noopener">Insights</a>
    <a class="btn navcta" href="#evaluation">Request a Property Evaluation</a>
  </nav>
  <a class="btn{' sun' if dark else ''}" href="#evaluation">Request a Property Evaluation</a>
  <button class="menu" type="button" aria-controls="nav" aria-expanded="false"><span></span><span></span>Menu</button>
</div></header>
<main id="main">
"""

def footer():
    return f'''</main>
<footer class="site-foot"><div class="wrap">
  <div><a class="logo" href="/"><img src="/assets/img/skyrun-denver-horizontal.png" width="922" height="267" alt="SkyRun Vacation Rentals, serving the Denver Metro Area"></a><p class="small" style="margin-top:12px">SkyRun Denver is an independently owned and operated SkyRun Vacation Rentals location.</p></div>
  <div><p class="fh">Contact</p><p><a href="tel:+17207281997">720-728-1997</a></p><p><a href="mailto:denver@skyrun.com">denver@skyrun.com</a></p><p>Locally owned and operated. Serving the Denver Metro area, including Denver, Arvada, Wheat Ridge, Lakewood, Englewood and Centennial.</p></div>
  <div><p class="fh">Homeowners</p><p><a href="/#paths">Two Ways to Rent</a></p><p><a href="/#ready">5-Star Ready</a></p><p><a href="/operations">Operations</a></p><p><a href="/areas">Areas We Serve</a></p><p><a href="https://skyrun.com/blog/category/denver/" rel="noopener">Insights</a></p><p><a href="/#evaluation">Request a Property Evaluation</a></p></div>
  <div><p class="fh">Owners</p><p><a href="https://skyrundenver.trackhs.com/owner/" rel="noopener">Owner Login</a></p><p><a href="/privacy">Privacy</a></p></div>
</div></footer>
<a class="btn mcta" href="#evaluation">Request a Property Evaluation</a>
<script src="/assets/js/site.js?v={JS_V}" defer></script>
</body>
</html>
'''

# HubSpot (portal 247984825, form "skyrundenver.com Property Evaluation"). Option values are the
# internal values of Sebastien's HubSpot properties; labels are his HubSpot labels.
HS_PORTAL = '247984825'
HS_FORM = 'eaa2f3be-9d2d-499a-ac90-660144fdbfbb'
HS_TYPES = [('single_family_house', 'Single-family house'), ('townhome', 'Townhome'), ('condominium', 'Condominium'),
            ('duplex_or_multifamily', 'Duplex or multifamily'), ('apartment', 'Apartment'), ('other', 'Other')]
HS_STRATEGY = [('short_stays_under_30_days', 'Short stays (under 30 days)'), ('furnished_stays_30_days', 'Furnished stays (30+ days)'),
               ('hybrid_or_flexible', 'Hybrid or flexible'), ('not_sure_yet', 'Not sure yet')]
HS_START = [('as_soon_as_property_is_ready', 'As soon as the property is ready'), ('within_1_3_months', 'Within 1 to 3 months'),
            ('within_3_6_months', 'Within 3 to 6 months'), ('more_than_6_months', 'More than 6 months'), ('exploring_options', 'Exploring options')]
HS_FOUND = [('google_search', 'Google search'), ('google_maps', 'Google Maps'), ('existing_owner_referral', 'Referral from a SkyRun owner'),
            ('realtor_referral', 'Realtor referral'), ('other_referral', 'Other referral'), ('social_media', 'Social media'),
            ('direct_mail', 'Direct mail'), ('other_or_not_sure', 'Other or not sure')]
HS_TRACKING = '<script id="hs-script-loader" async defer src="https://js-na2.hs-scripts.com/247984825.js"></script>'

# Ad and analytics tags. Each stays off until its ID is filled in (accounts are Sebastien's, per the HQ ruling).
GA4_ID = ''          # Google Analytics 4 measurement ID, e.g. G-XXXXXXXXXX
ADS_ID = ''          # Google Ads tag ID, e.g. AW-123456789
ADS_LEAD_LABEL = ''  # Google Ads conversion label for the property evaluation lead
META_PIXEL = ''      # Meta pixel ID
def tags():
    out = []
    first = GA4_ID or ADS_ID
    if first:
        cfg = ''.join(f"gtag('config','{i}');" for i in (GA4_ID, ADS_ID) if i)
        out.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={first}"></script>'
                   f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());{cfg}</script>")
    if ADS_ID and ADS_LEAD_LABEL:
        out.append(f"<script>window.SRD_ADS_LEAD='{ADS_ID}/{ADS_LEAD_LABEL}';</script>")
    if META_PIXEL:
        out.append("<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};"
                   "if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;"
                   "s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');"
                   f"fbq('init','{META_PIXEL}');fbq('track','PageView');</script>")
    return '\n'.join(out)

def form(page_label):
    opts = ''.join(f'<option value="{c.lower().replace(" ", "_")}">{c}</option>' for c in CITIES) + '<option value="other_needs_territory_approval">Another Denver Metro city</option>'
    def sel(pairs):
        return ''.join(f'<option value="{v}">{t}</option>' for v, t in pairs)
    return f'''<form class="eval" name="property-evaluation" method="POST" action="/thank-you" data-netlify="true" netlify-honeypot="bot-field" data-hs-do-not-collect="true" data-hs-portal="{HS_PORTAL}" data-hs-form="{HS_FORM}" novalidate>
    <input type="hidden" name="form-name" value="property-evaluation">
    <p class="hp" aria-hidden="true"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
    <div class="f"><label for="first">First name</label><input id="first" name="firstname" autocomplete="given-name" required></div>
    <div class="f"><label for="last">Last name</label><input id="last" name="lastname" autocomplete="family-name" required></div>
    <div class="f"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
    <div class="f"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
    <div class="f"><label for="city">Property city</label><select id="city" name="skyrun_property_city" required><option value="">Choose</option>{opts}</select></div>
    <div class="f"><label for="type">Property type</label><select id="type" name="skyrun_property_type"><option value="">Choose</option>{sel(HS_TYPES)}</select></div>
    <div class="f full"><label for="strategy">Rental approach you are considering</label><select id="strategy" name="skyrun_rental_strategy"><option value="">Choose</option>{sel(HS_STRATEGY)}</select></div>
    <div class="f"><label for="start">Target start</label><select id="start" name="skyrun_start_window"><option value="">Choose</option>{sel(HS_START)}</select></div>
    <div class="f"><label for="found">How did you hear about us</label><select id="found" name="skyrun_discovery_channel"><option value="">Choose</option>{sel(HS_FOUND)}</select></div>
    <div class="f full"><label for="notes">Anything we should know (optional)</label><textarea id="notes" name="message"></textarea></div>
    <input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign"><input type="hidden" name="utm_term"><input type="hidden" name="utm_content"><input type="hidden" name="gclid"><input type="hidden" name="skyrun_inquiry_landing_page" value="{page_label}">
    <label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree to be contacted by SkyRun Denver about my property.</label>
    <button class="btn" type="submit">Request a Property Evaluation</button>
    <p class="form-err small" role="alert" hidden></p>
    <p class="privacy">We use what you send here to follow up about your property and nothing else. <a href="/privacy">Privacy policy</a>.</p>
  </form>'''

def ask(page_label):
    return f'''<section class="ask" id="evaluation"><div class="wrap">
  <div>
    <h2 class="h2 rv" id="ft">Tell us about your property.</h2>
    <p class="lede">Share a few details about your home and what you're hoping to accomplish. We'll review the initial fit and discuss sensible next steps. If the property appears to be a fit, we'll discuss a walkthrough and prepare a written property-specific recommendation once we have enough information. Revenue ranges are provided only when supported by data.</p>
    <p class="nocost">No cost. No commitment.</p>
    <p class="small" style="margin-top:12px">An evaluation is not an offer to manage your property or a guarantee of licensing eligibility.</p>
  </div>
  {form(page_label)}
</div></section>
'''

def areas_table():
    rows = ''.join(f'<tr><td>{c}</td><td>{RULES[c][0]} <span class="small">Reviewed {RULES_REVIEWED}.</span></td><td><a href="#evaluation" data-city="{c}">Start in {c}</a></td></tr>' for c in CITIES)
    return f'''<section class="areas" id="areas"><div class="wrap">
  <h2 class="word rv">Six <em class="acc">cities.</em></h2>
  <p class="lede" style="font-size:19px;line-height:1.5;max-width:46ch">Where we work, and what each one asks of you.</p>
  <table class="tbl"><tbody>{rows}
  </tbody></table>
  <p class="small" style="margin-top:20px">Full detail for each city, with the map, on <a href="/areas" style="color:var(--sky-ink)">Areas We Serve</a>.</p>
</div></section>
'''

def split_home():
    return '''<section class="duo" id="ops"><div class="wrap">
  <h2 class="h2 rv">One management relationship. <em class="acc">Clear responsibilities.</em></h2>
  <div class="duo-cols">
    <div class="col"><h3>SkyRun Denver</h3><p>Your rental strategy, pricing, reservations, guest communication, financial reporting, and management decisions.</p></div>
    <div class="col"><h3>StayReady</h3><p>Our independent field-operations partner, supporting assigned turnovers, property readiness, and approved on-site services. <a class="quietlink" href="https://www.gostayready.com/" rel="noopener">About StayReady</a></p></div>
  </div>
  <p class="duo-close">SkyRun remains accountable to you.</p>
  <p><a class="arrow" href="/operations">See how operations work</a></p>
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
    <p class="part">SkyRun Denver is an independently owned and operated SkyRun Vacation Rentals location.</p>
  </div>
  <div class="col">
    <h3>Field operations by StayReady</h3>
    <p style="margin:0 0 16px;font-size:15px;color:var(--mute)">The field work between guests, on one accountable record. <a href="/operations" style="color:var(--sky-ink)">See a turnover, hour by hour</a></p>
    <ul>
      <li><b>Cleaning.</b> The turnover checklist across eight zones, every stay.</li>
      <li><b>Linens.</b> A managed linen program, swapped per turn.</li>
      <li><b>Restocking.</b> Supplies to par, counted and logged.</li>
      <li><b>Inspections.</b> Readiness inspections, documented with photos.</li>
      <li><b>Maintenance.</b> Repairs dispatched, documented, closed.</li>
      <li><b>Seasonal and exterior.</b> Snow, lawn, irrigation, and hot tubs, where included in the home's service plan.</li>
    </ul>
    <p class="part">SkyRun Denver manages the owner relationship and the rental program. StayReady is our independent field operations partner for turnover readiness and other approved onsite services. {panel}</p>
  </div>
</div></section>
'''

def voice():
    # Excerpts approved verbatim by Sebastien in v2.1 (Nov 15, 2026). Do not edit wording or add excerpts.
    quotes = [
        ("When we decided to jump into the rental property world, I was completely lost and honestly a little scared. Sebastien made the whole process seem even enjoyable.", 'Jasmine Solis'),
        ("Unbelievable communication. Always quick with a response. Beyond professional and transparent. Set proper expectations but even ended up over delivering.", 'Anthony Iacobucci'),
    ]
    cards = ''.join(f'<figure class="q rv d{i + 1}"><blockquote>{t}</blockquote><figcaption>{n} · Google review</figcaption></figure>' for i, (t, n) in enumerate(quotes))
    return f'''<section class="voice" id="reviews"><div class="wrap">
  <h2 class="h2 rv">Hear it from <em class="acc">homeowners.</em></h2>
  <div class="quotes">{cards}</div>
</div></section>
'''

def cred():
    return f'''<section class="cred" aria-label="Local ownership and Google rating"><div class="wrap">
  <p><span>Locally owned and operated</span><span><b class="stars" aria-hidden="true">★</b> 5.0 on Google</span><span>40 reviews</span></p>
  <a class="arrow" href="{GBP}" rel="noopener">Read our Google reviews</a>
</div></section>
'''

def paths():
    return '''<section class="paths" id="paths"><div class="wrap">
  <h2 class="h2 rv">Not every property belongs on <em class="acc">Airbnb.</em></h2>
  <p class="lede" style="font-size:19px;line-height:1.5;max-width:52ch;margin-top:20px">Short stays and furnished 30+ day rentals serve different goals.</p>
  <div class="paths-ed">
    <div class="path rv d1"><div class="photo" data-label="Photo: a short stay home, staged and guest ready"></div><h3>Short-term rentals</h3><p>Flexible nightly and weekly stays for eligible properties, supported by active pricing, guest management, and coordinated operations.</p></div>
    <div class="path rv d2"><div class="photo alt" data-label="Photo: a furnished monthly home, lived in and calm"></div><h3>Furnished 30+ day rentals</h3><p>Longer stays for relocation, temporary housing, and other furnished-rental needs, with a different pricing and management approach.</p></div>
  </div>
  <p style="margin-top:clamp(28px,3vw,44px)"><a class="btn ghost" href="#evaluation">Find My Property's Fit</a></p>
</div></section>
'''

def ready():
    # Gate names from Sebastien's approved v2.1 copy; checked Nov 19 against Owner Onboarding Packet V6 (same six gates and three outcomes).
    gates = ['Agreement and intake', 'Rental compliance', 'Operational walkthrough and action plan',
             'Corrections and 150-point inspection', 'Inventory and operating setup', 'Guest-ready design and launch']
    items = ''.join(f'<li><span class="n">{i + 1:02d}</span><h3>{t}</h3></li>' for i, t in enumerate(gates))
    return f'''<section class="ready" id="ready"><div class="wrap">
  <div class="ready-top">
    <div><p class="kicker">5-Star Ready</p><h2 class="h2 rv">The listing is the easy part. <em class="acc">Getting the home ready is the work.</em></h2></div>
    <div class="ready-copy">
      <p class="lede">A home needs more than attractive photos to be ready for guests. Our 5-Star Ready process covers safety, compliance, function, comfort, supplies, presentation and guest appeal.</p>
      <p class="lede">We identify what needs attention, coordinate appropriate work with approved partners including StayReady, and make a documented readiness decision. SkyRun has final launch approval.</p>
    </div>
  </div>
  <ol class="gates" aria-label="The six readiness gates">{items}</ol>
  <div class="ready-foot">
    <p class="outcomes" aria-label="Readiness outcomes"><span class="o-ready">5-Star Ready</span><span class="o-cond">Conditional Approval</span><span class="o-hold">Hold</span></p>
    <p class="small fine">5-Star Ready is our operating standard for preparing a home. It is not a guarantee of five-star guest reviews or a promise that every home will launch.</p>
  </div>
</div></section>
'''

# Direction C (approved by Matt, Nov 18): people first. Until real photos exist these render as labeled
# placeholders on the private draft site. Before launch, add the files and set the names, or remove the blocks.
SEB_PORTRAIT = 'sebastien-guite'  # headshot from Sebastien, Nov 19 (SG-Head Shot.jpg in the shared photo folder)
#  # e.g. 'sebastien-portrait' (assets/img/people/<name>-800.webp), square crop for the hero card
SEB_LETTER = 'sebastien-guite'
#    # e.g. 'sebastien-vertical' (assets/img/people/<name>-800.webp), vertical portrait beside the letter
TEAM_PHOTO = None     # e.g. 'denver-team' (assets/img/people/<name>-1440.webp), wide, the team at a managed home

def lead_card():
    if SEB_PORTRAIT:
        ph = f'<img class="ph" src="/assets/img/people/{SEB_PORTRAIT}-square-256.webp" alt="Sebastien Guite" width="64" height="64">'
    else:
        return ''  # hidden until the portrait arrives
    return f'<div class="lead-card">{ph}<p><b>Sebastien Guite</b><br>Location Owner, SkyRun Vacation Rentals Denver Metro</p></div>'

def people():
    if TEAM_PHOTO:
        return (f'<section class="people" aria-label="The SkyRun Denver team"><div class="photo has-img"><img src="/assets/img/people/{TEAM_PHOTO}-1440.webp" '
                f'srcset="/assets/img/people/{TEAM_PHOTO}-800.webp 800w, /assets/img/people/{TEAM_PHOTO}-1440.webp 1440w" sizes="100vw" alt="The SkyRun Denver team at a managed home" loading="lazy" decoding="async"></div></section>\n')
    return ''  # hidden until the team photo arrives

SHOW_HOMES = True  # Review preview only. Set False at launch unless names, classifications, images and permissions are verified.

def homes():
    if not SHOW_HOMES:
        return ''
    labels = ['Photo: featured managed home, exterior at golden hour', 'Photo: kitchen, staged and guest ready',
              'Photo: primary bedroom', 'Photo: living room with character', 'Photo: back patio or yard']
    items = ''.join(f'<figure class="card"><div class="photo" data-label="{l}"></div></figure>' for l in labels)
    return f"""<section class="homes" id="homes">
  <div class="wrap head"><h2 class="word rv">Homes.</h2><p class="lede" style="font-size:19px;line-height:1.5;max-width:46ch">A few of the homes we manage across Denver Metro.</p><p class="hint small">Scroll sideways</p></div>
  <div class="strip" tabindex="0" aria-label="Managed homes gallery">{items}</div>
</section>
"""

def letter():
    portrait = (f'<div class="photo has-img portrait" style="margin-top:28px"><img src="/assets/img/people/{SEB_LETTER}-800.webp" srcset="/assets/img/people/{SEB_LETTER}-800.webp 800w, /assets/img/people/{SEB_LETTER}-1200.webp 1200w" sizes="(max-width: 700px) 70vw, 420px" alt="Sebastien Guite, Location Owner of SkyRun Denver" width="800" height="991" loading="lazy" decoding="async"></div>' if SEB_LETTER else '')
    return '''<section class="letter" id="letter"><div class="wrap">
  <div><p class="kicker">From Sebastien</p><h2 class="h2 rv">I'd rather give you a plan that holds up than <em class="acc">a number that sounds good.</em></h2>''' + portrait + '''</div>
  <div class="card rv d1">
    <p>I'm Sebastien, owner of SkyRun Denver.</p>
    <p>I believe there's a big difference between getting a property booked and managing it well.</p>
    <p>Before taking on a home, I want to understand what you're trying to accomplish, what the numbers suggest, what the property needs, and whether we can genuinely help.</p>
    <p>Sometimes short stays make sense. Sometimes a furnished 30+ day rental is the better move. And sometimes neither is the right answer.</p>
    <p>When we do manage your home, you should know what's happening, how it's performing, and who to call.</p>
    <p>If you're considering professional management, let's have a conversation about the property and see what makes sense.</p>
    <p class="sig">Sebastien Guite<br><span style="font-weight:400;color:var(--mute)">Location Owner, SkyRun Vacation Rentals Denver Metro</span></p>
  </div>
</div></section>
'''

def metro():
    small_map = MAP_SVG.replace(' data-city="', ' data-place="').replace('role="img" aria-label="Schematic map of the Denver metro with the six communities SkyRun Denver serves"', 'aria-hidden="true" focusable="false"')
    return f'''<section class="metro" id="metro"><div class="wrap">
  <div>
    <h2 class="h2 rv">Denver Metro. <em class="acc">Every property is different.</em></h2>
    <p class="lede">We manage short-term and furnished rentals across the Denver Metro area. Location, local requirements, property condition, and your goals all help determine the right approach.</p>
    <p><a class="arrow" href="/areas">Explore our service areas</a></p>
  </div>
  <div class="map mini">{small_map}<a class="map-link" href="/areas" aria-label="Explore our service areas"></a></div>
</div></section>
'''

# ---------------- Home ----------------
home = head('SkyRun Denver | Short-Term and Furnished Rental Management for Denver Homeowners',
            'SkyRun Denver manages short-term and furnished 30+ day rentals for homeowners in Denver, Arvada, Wheat Ridge, Lakewood, Englewood, and Centennial. Request a property evaluation.', '/') + header('home', over=True) + """
<section class="hero-photo">
  <div class="photo rv" data-label="Photo: a managed Denver home at golden hour, full bleed, licensed and credited"></div>
  <div class="wrap copy">
    <p class="kicker">Denver Metro · Short-term &amp; furnished 30+ day rental management</p>
    <h1 class="disp">The right rental strategy. <em class="acc">A home that's ready for it.</em></h1>
    <p class="lede">We look at your goals, local rules, and operating costs before recommending short stays, furnished 30+ day rentals, or neither. If the property is a fit, we help get it ready and manage the details.</p>
    <div class="acts"><a class="btn sun" href="#evaluation">Request a Property Evaluation</a><a class="btn glass" href="#month">See How We Work</a></div>
    """ + lead_card() + """
  </div>
</section>
""" + paths() + cred() + ready() + voice() + f"""
<section class="hero month" id="month"><div class="wrap">
  <div class="hero-l">
    <div class="stick">
    <p class="kicker">Illustrative property: One owner. Their primary residence in Wash Park. One month.</p>
    <h2 class="disp sub">One home. Plenty of moving parts. <em class="acc">One accountable manager.</em></h2>
    <p class="lede">Pricing, guest communication, turnovers, property care, and owner reporting all require attention. Here's an illustrative look at how SkyRun coordinates the moving pieces throughout a month.</p>
    </div>
  </div>
  <div class="cal" aria-label="An illustrative month: short stays, turnovers, a property care visit, and a furnished 30+ day stay">
    <div class="head"><b>November</b></div>
    <div class="grid7" role="img" aria-label="Illustrative calendar: short stays with a turnover after each one, a property care visit on the 12th, an issue flagged and routed on the 16th, and a furnished stay that begins on the 24th and runs to December 23. Seven numbered entries are listed below.">
      <div class="d b n" data-n="1">1</div><div class="d b">2</div><div class="d t n" data-n="2">3<em>turn</em></div><div class="d b">4</div><div class="d b">5</div><div class="d b">6</div><div class="d t">7<em>turn</em></div>
      <div class="d b n" data-n="3">8</div><div class="d b">9</div><div class="d t">10<em>turn</em></div><div class="d b">11</div><div class="d b s n" data-n="4">12<em>care</em></div><div class="d b">13</div><div class="d t">14<em>turn</em></div>
      <div class="d b">15</div><div class="d t i n" data-n="5">16<em>turn</em></div><div class="d b">17</div><div class="d b">18</div><div class="d b">19</div><div class="d t">20<em>turn</em></div><div class="d b">21</div>
      <div class="d b">22</div><div class="d t">23<em>turn</em></div><div class="d m n" data-n="6">24<em>night 1</em></div><div class="d m">25</div><div class="d m">26</div><div class="d m">27</div><div class="d m">28</div>
      <div class="d m">29</div><div class="d m n" data-n="7">30</div><div class="d m nx">Dec 1</div><div class="d m nx">2</div><div class="d m nx">3</div><div class="d m nx">4</div><div class="d m nx more">5<em>to Dec 23</em></div>
    </div>
    <p class="keyrow"><span><i></i>Short stay booked</span><span><i class="t"></i>Turnover</span><span><i class="s"></i>Property care visit</span><span><i class="i"></i>Issue flagged and routed</span><span><i class="m"></i>Furnished stay, Nov 24 to Dec 23</span><span>Numbered: an entry below</span></p>
    <div class="ledger">
      <div class="row"><span class="t">1</span><div><h3>Owner statement for October</h3><p>Rental activity, fees, expenses and owner proceeds summarized under the management agreement.</p></div><span class="who">Owner reporting</span></div>
      <div class="row"><span class="t">3</span><div><h3>First turn of the month</h3><p>Cleaning, linens, supplies and readiness work coordinated; any concerns documented and routed.</p><div class="photo" data-label="Photo: the home, guest ready"></div></div><span class="who">Operations</span></div>
      <div class="row"><span class="t">8</span><div><h3>Rate reviewed for a Broncos home weekend</h3><p>Comparable homes and event demand reviewed; pricing adjusted when the data warrants it.</p></div><span class="who">Pricing</span></div>
      <div class="row"><span class="t">12</span><div><h3>Property care visit between guests</h3><p>Work scheduled only under the home's agreed service plan; findings documented.</p></div><span class="who">Property care</span></div>
      <div class="row"><span class="t">16</span><div><h3>Turnover check flags an issue</h3><p>A concern documented and routed for follow-up.</p></div><span class="who">Operations</span></div>
      <div class="row"><span class="t">24</span><div><h3>Furnished 30+ day stay approved</h3><p>A longer-stay request assessed against the calendar, local rules, economics and the owner's goals, then approved by the owner.</p></div><span class="who">Owner relations</span></div>
      <div class="row"><span class="t now">30</span><div><h3>Lodging tax coordinated</h3><p>Applicable responsibilities handled according to the booking channel and management arrangement.</p></div><span class="who">Owner reporting</span></div>
      <p class="foot">Illustrative timeline, not a record of actual bookings or results. Local eligibility, service schedules and management responsibilities vary by property and agreement.</p>
    </div>
  </div>
</div></section>

<section class="band"><div class="photo rv" data-label="Photo: the same home, interior, late afternoon, licensed and credited"></div></section>

<section class="record" id="statement"><div class="wrap">
  <div>
    <p class="kicker">Owner statement</p>
    <h2 class="h2 rv">Your month, <em class="acc">in one statement.</em></h2>
    <p class="lede" style="margin-top:24px">A clear picture of rental activity, revenue, fees, expenses, and owner proceeds. Reservation details are available through your owner portal, and we're here to explain the numbers when questions come up.</p>
    <p class="small" style="margin-top:20px">Illustrative statement. Actual owner financial records remain private.</p>
  </div>
  <div class="stmt" aria-label="Illustrative owner statement">
    <div class="top"><span>Wash Park home</span></div>
    <div class="grid">
      <div class="cell"><b>23</b><span>short stay nights, 7 turnovers</span></div>
      <div class="cell"><b>7</b><span>furnished stay nights in November</span></div>
      <div class="cell"><b>1</b><span>property care visit</span></div>
      <div class="cell"><b>1</b><span>issue flagged and routed</span></div>
    </div>
  </div>
</div></section>
""" + people() + homes() + split_home() + letter() + metro() + ask('home') + footer()
(SITE / 'index.html').write_text(bust(photos(home)))

# ---------------- Operations ----------------
ops = head('Operations | What Happens to Your Home Between Guests | SkyRun Denver',
           'One turnover, hour by hour. StayReady runs the cleaning, linens, restocking, inspections, and maintenance behind every SkyRun Denver stay.', '/operations') + header('operations') + '''
<section class="hero"><div class="wrap">
  <div class="hero-l">
    <p class="kicker">Operations. A Tuesday in Wash Park, checkout at 10:00, check in at 4:00.</p>
    <h1 class="disp ops">Between checkout and check in, <em class="acc">the details matter.</em></h1>
    <p class="lede">A successful turnover is more than changing linens. The property needs to be cleaned, reset, supplied, checked for issues, and ready for the next arrival. StayReady, the <a href="https://www.gostayready.com/hospitality-field-operations" rel="noopener">hospitality field operations company</a> based here in Colorado, executes and documents its assigned field work. SkyRun Denver keeps responsibility for the overall rental program and owner communication.</p>
    <ol class="steps"><li>Plan the turn</li><li>Clean and reset</li><li>Flag and route issues</li><li>Confirm readiness for the next arrival</li></ol>
    <div class="acts"><a class="btn" href="#evaluation">Evaluate My Property</a><a class="btn ghost" href="#record">See the Record</a></div>
  </div>
  <h2 class="sr-only">One turnover, hour by hour</h2><div class="cal" aria-label="One turnover, hour by hour"><div class="ledger">
    <div class="head"><span>Time</span><span>What happened</span><span style="text-align:right">Who</span></div>
    <div class="row"><span class="t big">10:00</span><div><h3>Guests check out</h3><p>Smart lock code expires. Checkout photos requested from the guest.</p></div><span class="who">SkyRun Denver</span></div>
    <div class="row"><span class="t big">10:40</span><div><h3>Cleaning team arrives</h3><p>Two person crew working the <a href="https://www.gostayready.com/turnover-cleaning" rel="noopener">turnover checklist</a> across eight zones: kitchen, baths, floors, every surface.</p></div><span class="who">StayReady cleaning</span></div>
    <div class="row"><span class="t big">12:15</span><div><h3>Linens swapped, not washed onsite</h3><p>Fresh set from the linen program. Used set bagged for the laundry route.</p></div><span class="who">StayReady linens</span></div>
    <div class="row"><span class="t big">1:05</span><div><h3>Restocked to par</h3><p>Paper, soap, coffee, dish pods. Counts logged against the home's par list.</p></div><span class="who">StayReady restocking</span></div>
    <div class="row"><span class="t big">1:40</span><div><h3>Inspection, every room</h3><p>A <a href="https://www.gostayready.com/inspections" rel="noopener">readiness inspection</a>: appliances, fixtures, locks, thermostat, staging. Loose bath fan noted and sent to maintenance.</p></div><span class="who">StayReady inspection</span></div>
    <div class="row"><span class="t big">2:30</span><div><h3>Bath fan tightened</h3><p>Same day. Before and after photos attached to the home's record.</p></div><span class="who">StayReady maintenance</span></div>
    <div class="row"><span class="t big now">3:10</span><div><h3>Guest ready</h3><p>Record closed. Every step, photo, and count documented for the home.</p></div><span class="who">SkyRun Denver</span></div>
    <div class="row"><span class="t big">4:00</span><div><h3>Next guests check in</h3><p>New lock code live. Welcome message sent.</p></div><span class="who">SkyRun Denver</span></div>
    <p class="foot">Illustrative timeline. Actual tasks depend on each home's agreed service plan.</p>
  </div></div>
</div></section>


<section class="record" id="record"><div class="wrap">
  <div>
    <h2 class="word rv">The <em class="acc">record.</em></h2>
    <p class="lede" style="margin-top:18px"><strong style="color:var(--ink)">Documented after every stay.</strong></p>
    <p class="lede">Not a monthly summary. The actual checklist, photos, counts, and issues from each turnover, kept on the home's record.</p>
    <ul class="rp-holds">
      <li><b>Checklist by zone.</b> Every room and outdoor space, marked complete or flagged.</li>
      <li><b>Time stamped photos.</b> What the home looked like before the next guest arrived.</li>
      <li><b>Issues and who fixed them.</b> What was found, where it was routed, and when it closed.</li>
      <li><b>Supply counts.</b> Restocked against your home's par levels, so nothing runs out mid stay.</li>
    </ul>
    <p class="small" style="margin-top:20px">StayReady executes and documents its assigned field work. SkyRun Denver shares what matters with you.</p>
  </div>
  <div class="report rv" aria-label="Sample turnover report">
    <div class="rp-head">
      <div><p class="rp-lbl">Sample turnover report</p><p class="rp-title">Wash Park home</p></div>
      <span class="rp-status">Guest ready</span>
    </div>
    <dl class="rp-meta"><div><dt>Inspected by</dt><dd>StayReady</dd></div><div><dt>Turn closed</dt><dd>3:10 PM</dd></div><div><dt>Next arrival</dt><dd>4:00 PM</dd></div></dl>
    <div class="rp-stats">
      <div><b>8</b><span>zones checked</span></div>
      <div><b>14</b><span>photos attached</span></div>
      <div><b>1</b><span>issue fixed same day</span></div>
      <div><b>0</b><span>open items at check in</span></div>
    </div>
    <div class="rp-sec">
      <div class="rp-sec-h"><span class="rp-n">01</span><h3>Photo record</h3><span class="rp-count">14 photos</span></div>
      <div class="rp-photos">
        <figure><img src="/assets/img/homes/madison-dining-800.webp" alt="" loading="lazy" decoding="async"><figcaption>Dining</figcaption></figure>
        <figure><img src="/assets/img/homes/madison-primary-800.webp" alt="" loading="lazy" decoding="async"><figcaption>Primary bedroom</figcaption></figure>
        <figure><img src="/assets/img/homes/madison-bath-800.webp" alt="" loading="lazy" decoding="async"><figcaption>Primary bath</figcaption></figure>
        <figure class="more"><img src="/assets/img/homes/madison-courtyard-800.webp" alt="" loading="lazy" decoding="async"><figcaption>Courtyard</figcaption><span>+10</span></figure>
      </div>
    </div>
    <div class="rp-sec">
      <div class="rp-sec-h"><span class="rp-n">02</span><h3>Readiness checklist</h3><span class="rp-count">8 of 8 zones</span></div>
      <ul class="rp-zones">
        <li>Entry and access</li><li>Kitchen</li><li>Living areas</li><li>Bedrooms</li>
        <li>Bathrooms</li><li>Linens staged</li><li>Supplies to par</li><li>Outdoor spaces</li>
      </ul>
    </div>
    <div class="rp-sec">
      <div class="rp-sec-h"><span class="rp-n">03</span><h3>Issues and routing</h3><span class="rp-count">2 logged, 0 open</span></div>
      <ul class="rp-issues">
        <li><div><b>Primary bath fan loose</b><span>Found at 1:40 PM inspection. Routed to maintenance, tightened 2:30 PM, before and after photos attached.</span></div><em class="ok">Fixed</em></li>
        <li><div><b>Phone charger left in bedroom 2</b><span>Bagged, labeled, and logged for the guest.</span></div><em>Logged</em></li>
      </ul>
    </div>
    <div class="rp-sec">
      <div class="rp-sec-h"><span class="rp-n">04</span><h3>Supply counts</h3><span class="rp-count">Counted against par</span></div>
      <ul class="rp-par">
        <li><span>Coffee pods</span><b>20 of 20</b></li><li><span>Paper towels</span><b>6 of 6</b></li><li><span>Dish pods</span><b>24 of 24</b></li><li><span>Bath towels</span><b>8 of 8</b></li>
      </ul>
    </div>
    <p class="note">Sample record. Figures vary by home and stay.</p>
  </div>
</div></section>
''' + split('operations') + ask('operations') + footer()
(SITE / 'operations.html').write_text(bust(photos(ops)).replace('<section class="band">', '<section class="band">', 1))

# ---------------- Areas ----------------
chips = ''.join(f'<button class="chip" type="button" data-city="{c}" aria-pressed="false">{c}</button>' for c in CITIES)
rules = ''.join(f'<li><b>{c}<small>Reviewed {RULES_REVIEWED}</small></b><p>{RULES[c][0]} <a href="{RULES[c][1]}" rel="noopener" class="src">City source</a>. <a href="#evaluation" data-city="{c}">Start in {c}</a></p></li>' for c in CITIES)
areas = head('Areas We Serve | Denver, Arvada, Wheat Ridge, Lakewood, Englewood, Centennial | SkyRun Denver',
             'SkyRun Denver manages short-term and furnished rentals in Denver, Arvada, Wheat Ridge, Lakewood, Englewood, and Centennial. Each city has its own rules; the evaluation starts with yours.', '/areas') + header('areas', dark=True) + f'''
<section class="maphero"><div class="wrap">
  <div>
    <h1>The Denver metro is not one <em class="acc">rental market.</em></h1>
    <p class="lede">Rules, property types, owner priorities, and demand patterns change across Denver, Arvada, Wheat Ridge, Lakewood, Englewood, and Centennial. We start with your address and the city's current requirements before making a recommendation.</p>
    <p class="pickline" id="pl">Pick your community to check your property's fit</p>
    <div class="chips" role="group" aria-labelledby="pl">{chips}</div>
  </div>
  <div class="map">
    {MAP_SVG}
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
def fix_cta(html):
    return html.replace('href="#evaluation"', 'href="/#evaluation"')

thanks = head('Evaluation Requested | SkyRun Denver', 'Your property evaluation request is in. The SkyRun Denver team follows up to schedule a walkthrough.', '/thank-you',
              '<meta name="robots" content="noindex">') + header('thanks') + '''
<section class="thanks"><div class="wrap">
  <p class="kicker">Evaluation requested</p>
  <h1 class="h2">Thanks for reaching out.</h1>
  <p class="lede">We will review your information and be in touch soon. If anything is urgent, call <a href="tel:+17207281997">720-728-1997</a>.</p>
  <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn ghost" href="/operations">See What Happens Between Guests</a><a class="btn ghost" href="/areas">Read Your City's Rules</a></div>
</div></section>
''' + footer().replace('<a class="btn mcta" href="#evaluation">Request a Property Evaluation</a>', '')
(SITE / 'thank-you.html').write_text(fix_cta(thanks))

# ---------------- Privacy ----------------
def fix_cta(html):
    return html.replace('href="#evaluation"', 'href="/#evaluation"')

privacy = head('Privacy | SkyRun Denver', 'How SkyRun Denver collects, uses, and protects the information you share through skyrundenver.com.', '/privacy') + header('privacy', dark=True) + """
<section class="legal"><div class="wrap">
  <p class="kicker">Privacy</p>
  <h1 class="h2">How we handle your information.</h1>
  <p class="small">Effective November 19, 2026</p>
  <p>This notice covers skyrundenver.com, operated by SkyRun Denver, an independently owned and operated SkyRun Vacation Rentals location serving the Denver Metro area. It explains what we collect through this site, how we use it, and the choices you have.</p>

  <h2>What we collect</h2>
  <p><b>Information you give us.</b> When you request a property evaluation, we collect your name, email, phone number, property city, property type, the rental approach you are considering, your target start, how you heard about us, and anything you add in the notes field.</p>
  <p><b>Information collected automatically.</b> When you visit the site, we and our service providers may collect the page you arrived on, the referring page or campaign (such as UTM tags or a Google click ID), your browser and device type, and general location based on your IP address. Some of this is collected with cookies or similar technologies.</p>

  <h2>How we use it</h2>
  <ul>
    <li>To respond to your inquiry, evaluate your property, and follow up about management.</li>
    <li>To understand how owners find us and which pages and campaigns are useful.</li>
    <li>To measure and improve our advertising, including showing relevant ads to people who visited the site.</li>
    <li>To keep the site secure and working properly.</li>
  </ul>
  <p>We do not sell your personal information.</p>

  <h2>Who we share it with</h2>
  <p>We share information only with service providers that help us run the site and our business, such as our website host and form processor (Netlify), our customer relationship management system (HubSpot), analytics and advertising platforms (such as Google and Meta), and SkyRun Vacation Rentals systems used to manage owner relationships. We may also share information when required by law.</p>

  <h2>Cookies and your choices</h2>
  <p>You can block or delete cookies in your browser settings. You can manage ad personalization through <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a> and your Facebook or Instagram ad preferences, and you can opt out of Google Analytics with the <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">Google Analytics opt out browser add on</a>.</p>
  <p>If we contact you by email, you can unsubscribe at any time using the link in the message or by replying to ask us to stop.</p>

  <h2>Access, correction, and deletion</h2>
  <p>You can ask us what information we hold about you, ask us to correct it, or ask us to delete it. Email <a href="mailto:denver@skyrun.com">denver@skyrun.com</a> or call <a href="tel:+17207281997">720-728-1997</a>. We will respond within a reasonable time and may need to confirm your identity first.</p>

  <h2>How long we keep it</h2>
  <p>We keep inquiry information for as long as it is useful to respond to you and manage any resulting relationship, and as required for our records. We delete or anonymize it when it is no longer needed.</p>

  <h2>Security</h2>
  <p>We use reasonable safeguards to protect the information you share, including encrypted connections to this site. No method of transmission or storage is completely secure.</p>

  <h2>Other sites</h2>
  <p>This site links to other sites, including the owner login and SkyRun Vacation Rentals pages. Their privacy practices are governed by their own policies.</p>

  <h2>Children</h2>
  <p>This site is intended for property owners and is not directed to children under 13. We do not knowingly collect information from children.</p>

  <h2>Changes and contact</h2>
  <p>We may update this notice from time to time and will change the effective date above when we do. Questions can go to <a href="mailto:denver@skyrun.com">denver@skyrun.com</a>.</p>
</div></section>
""" + footer()
(SITE / 'privacy.html').write_text(fix_cta(privacy))

# ---------------- 404 ----------------
nf = head('Page Not Found | SkyRun Denver', 'This page could not be found.', '/404', '<meta name="robots" content="noindex">') + header('404', dark=True) + """
<section class="thanks"><div class="wrap">
  <p class="kicker">Page not found</p>
  <h1 class="h2">This page moved or never existed.</h1>
  <p class="lede">Start from the homepage, or tell us about your property and we will take it from there.</p>
  <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="/">Go to the Homepage</a><a class="btn ghost" href="/#evaluation">Request a Property Evaluation</a></div>
</div></section>
""" + footer()
(SITE / '404.html').write_text(fix_cta(nf))

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

# Live since Nov 19, 2026: production indexes. Previews and branch deploys never do.
# Branch deploys and deploy previews never index.
[context.deploy-preview]
  command = "printf '/*\\n  X-Robots-Tag: noindex\\n' >> _headers"
[context.branch-deploy]
  command = "printf '/*\\n  X-Robots-Tag: noindex\\n' >> _headers"
''')
(SITE / '_redirects').write_text('''/index.html   /            301!
/operations.html  /operations  301!
/areas.html   /areas       301!
/thank-you.html  /thank-you  301!
/privacy.html  /privacy  301!
https://www.skyrundenver.com/*  https://skyrundenver.com/:splat  301!
''')
(SITE / '8c222801ef906b1e3962ef81529f8cab.txt').write_text('8c222801ef906b1e3962ef81529f8cab')  # IndexNow key
(SITE / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
(SITE / 'sitemap.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{ORIGIN}/</loc><lastmod>2026-11-19</lastmod></url>
  <url><loc>{ORIGIN}/operations</loc><lastmod>2026-11-19</lastmod></url>
  <url><loc>{ORIGIN}/areas</loc><lastmod>2026-11-19</lastmod></url>
  <url><loc>{ORIGIN}/privacy</loc><lastmod>2026-11-19</lastmod></url>
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
