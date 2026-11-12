# skyrundenver.com

v0.3 (2026-11-12): photo led hero, italic serif accents, city marquee, horizontal homes gallery, transparent header over the hero, mobile menu.

v0.2 (2026-11-11): warmer ground, hairline rules, Homes gallery, editorial two paths, letter from Sebastien, one word section titles.

Static site for SkyRun Denver. No build step: HTML, one stylesheet, one script, self hosted fonts. Deploys on push to main via Netlify.

Pages: `/` (A Month With Us), `/operations` (The Turn), `/areas` (the map and city rules), `/thank-you` (conversion page, noindex).

Lead form: Netlify Forms (`property-evaluation`) as the interim capture until the SkyRun Denver HubSpot account is live. Hidden fields carry utm_source, utm_medium, utm_campaign, utm_term, utm_content, gclid, and landing_page. Honeypot field: `company`. Set the Netlify form notification to Sebastien's inbox before launch.

Placeholders are in square brackets. Nothing in brackets ships.

Source pages are assembled by `tools/build_site.py` in the StayReady Websites workspace; edit there and regenerate, or edit the HTML directly and keep the partials in sync by hand.
