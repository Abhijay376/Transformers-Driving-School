import sys
sys.path.insert(0, "/home/claude/transformers-site")
from build import page_shell, trust_section_html, OUT, set_area_nav_items
import os
import math

# ============================================================
# AREA / SUBURB LANDING PAGES: data
# ============================================================
# Coordinates are approximate suburb-centre lat/long (looked up, not
# survey-grade), used to rank "nearest suburbs" for the areaServed schema
# field. All 8 suburbs sit in the City of Casey / Cardinia Shire growth
# corridor around Pakenham, Transformers Driving School's main service area.
SUBURB_COORDS = {
    "Pakenham": (-38.0736, 145.4854),
    "Officer": (-38.0642, 145.4092),
    "Beaconsfield": (-38.0417, 145.3728),
    "Berwick": (-38.0359, 145.3444),
    "Nar Nar Goon": (-38.0311, 145.5744),
    "Clyde": (-38.1108, 145.3436),
    "Cranbourne": (-38.1136, 145.2833),
    "Cardinia": (-38.1167, 145.4667),
    "Devon Meadows": (-38.1544, 145.3122),
    # extra nearby suburbs, used only as a pool to compute the
    # "nearest suburbs" list for the areaServed schema field
    "Clyde North": (-38.0836, 145.3411),
    "Narre Warren": (-38.0177, 145.3057),
    "Hampton Park": (-38.0139, 145.2489),
    "Hallam": (-38.0004, 145.2649),
    "Botanic Ridge": (-38.1594, 145.2778),
    "Koo Wee Rup": (-38.2214, 145.4964),
}

def haversine_km(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(x))

def nearest_n_suburbs(suburb, n=20):
    origin = SUBURB_COORDS[suburb]
    dists = [(name, haversine_km(origin, coord)) for name, coord in SUBURB_COORDS.items() if name != suburb]
    dists.sort(key=lambda t: t[1])
    return [name for name, _ in dists[:n]]

SUBURB_WIKIDATA = {
    "Pakenham": "Q2046587",
    "Officer": "Q7095039",
    "Beaconsfield": "Q4869287",
    "Berwick": "Q829245",
    "Nar Nar Goon": "Q6961128",
    "Clyde": "Q5133713",
    "Cranbourne": "Q3309297",
    "Devon Meadows": "Q5266013",
}

# Pakenham is the only VicRoads drive test centre this school prepares
# students for, so every suburb page (and Pakenham's own page) points there.
SUBURB_TEST_CENTRE = {
    "Officer": ("Pakenham", "drive-test-pakenham.html"),
    "Beaconsfield": ("Pakenham", "drive-test-pakenham.html"),
    "Berwick": ("Pakenham", "drive-test-pakenham.html"),
    "Nar Nar Goon": ("Pakenham", "drive-test-pakenham.html"),
    "Clyde": ("Pakenham", "drive-test-pakenham.html"),
    "Cranbourne": ("Pakenham", "drive-test-pakenham.html"),
    "Cardinia": ("Pakenham", "drive-test-pakenham.html"),
    "Devon Meadows": ("Pakenham", "drive-test-pakenham.html"),
}

AREA_SUBURBS = ["Officer", "Beaconsfield", "Berwick", "Nar Nar Goon",
                "Clyde", "Cranbourne", "Cardinia", "Devon Meadows"]

# NAP (Name / Address / Phone). No confirmed public storefront address was
# provided for Transformers Driving School, so this is treated as a
# service-area business: no streetAddress is fabricated anywhere on this
# site (unlike the old XDS repo address reuse) -- flagged in the build log.
NAP_NAME = "Transformers Driving School"
NAP_ADDRESS = "Service area business, no public storefront &mdash; lessons come to you across Pakenham and surrounding suburbs"
NAP_PHONE_DISPLAY = "0404 119 119"
NAP_PHONE_TEL = "0404119119"
NAP_EMAIL = "transformers.com.au@gmail.com"

def slugify(suburb):
    return suburb.lower().replace(" ", "-")

def area_page_href(suburb):
    return "area-" + slugify(suburb) + ".html"

# Register the "Areas We Serve" nav dropdown BEFORE any page is generated,
# so every page (including index.html, generated further down) gets it.
set_area_nav_items([
    ("area-" + slugify(s), area_page_href(s), s) for s in AREA_SUBURBS
])

def nap_faq_section(suburb_label, address=NAP_ADDRESS, extra_faqs=None):
    faqs = [
        ("Where is Transformers Driving School located?",
         "Our home base and instructor meeting point is {addr}. We also provide pickup and drop-off for lessons across {area} and surrounding South East Melbourne suburbs, so you don't need to travel to us.".format(addr=address, area=suburb_label)),
        ("What is the best way to contact TDS?",
         "WhatsApp is the fastest way to reach us on {phone}, and most messages get a reply within the hour. You can also call {phone}, or use the Contact Us form on this site.".format(phone=NAP_PHONE_DISPLAY)),
    ]
    if extra_faqs:
        faqs = faqs + extra_faqs
    items = "\n        ".join(
        '''<div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">{q}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">{a}</div></div>
        </div>'''.format(q=q, a=a) for q, a in faqs
    )
    return '''<section class="block block-alt" id="nap-faq">
    <div class="container">
      <div class="info-grid">
        <div class="info-card">
          <h2><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg>Business Details</h2>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg><div><strong>Name</strong><span>{name}</span></div></div>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg><div><strong>Address</strong><span>{addr}</span></div></div>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg><div><strong>Phone</strong><span><a href="tel:{tel}">{phone}</a></span></div></div>
        </div>
        <div class="faq-list">
          {faqs}
        </div>
      </div>
    </div>
  </section>'''.format(name=NAP_NAME, addr=address, tel=NAP_PHONE_TEL, phone=NAP_PHONE_DISPLAY, faqs=items)

SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "DrivingSchool",
  "name": "Transformers Driving School",
  "alternateName": "TDS",
  "telephone": "+61404119119",
  "url": "https://transformersdrivingschool.com.au",
  "areaServed": ["Pakenham", "Officer", "Beaconsfield", "Berwick", "Nar Nar Goon", "Clyde", "Cranbourne", "Cardinia", "Devon Meadows"],
  "keywords": "driving school Pakenham, driving lessons Pakenham, Pakenham driving instructor, VicRoads test preparation Pakenham",
  "sameAs": ["https://au.linkedin.com/in/sol-pakzad-b36761170", "https://www.facebook.com/share/1HmPRyNByw/", "https://www.facebook.com/transformersdrivingschool/"],
  "employee": {
    "@type": "Person",
    "name": "Sol Pakzad",
    "jobTitle": "VicRoads ADI Accredited Driving Instructor",
    "sameAs": ["https://au.linkedin.com/in/sol-pakzad-b36761170", "https://www.facebook.com/share/1HmPRyNByw/", "https://www.facebook.com/transformersdrivingschool/"]
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "5",
    "bestRating": "5",
    "ratingCount": "59",
    "reviewCount": "59"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How many lessons do I need before my VicRoads test?",
      "acceptedAnswer": { "@type": "Answer", "text": "Most learners need between 5 and 10 one-hour lessons on top of supervised practice, depending on experience. Take our free Test Readiness Quiz for a personalised recommendation." }
    },
    {
      "@type": "Question",
      "name": "Can I hire a car for my VicRoads drive test?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Our Express Test Package and Ultimate Test Pass Pack both include use of a fully compliant, dual-control instructor vehicle for your test." }
    },
    {
      "@type": "Question",
      "name": "Do I need a test if I have an overseas driving licence?",
      "acceptedAnswer": { "@type": "Answer", "text": "It depends on which country issued your licence. Recognised countries can usually exchange directly, Experienced Driver Recognition countries may need a knowledge and/or practical test depending on age, and all other countries require the full Victorian licensing process. Use our free Overseas Licence Conversion Checker for your exact pathway." }
    },
    {
      "@type": "Question",
      "name": "Which VicRoads test centre does Transformers Driving School cover?",
      "acceptedAnswer": { "@type": "Answer", "text": "Our instructors prepare students for the VicRoads drive test at Pakenham, with lessons available across Officer, Beaconsfield, Berwick, Nar Nar Goon, Clyde, Cranbourne, Cardinia and Devon Meadows." }
    }
  ]
}
</script>
'''

BYLINE = '<span class="byline"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6 6.6.7-5 4.4 1.5 6.5L12 16.8 6 19.6l1.5-6.5-5-4.4 6.6-.7z"/></svg>Reviewed by Sol Pakzad, VicRoads ADI Accredited Instructor</span>'

PACKAGES_SECTION = '''<section class="block block-alt" id="packages">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">Lessons &amp; Test Packages</span>
        <h2>Our Driving Packages</h2>
        <p>Simple, transparent pricing. Message us on WhatsApp to lock in a time.</p>
      </div>
      <div class="pkg-grid">
        <div class="pkg-card">
          <div class="pkg-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4a1 1 0 011-1h8a1 1 0 011 1v3h3a1 1 0 011 1v11a1 1 0 01-1 1H4a1 1 0 01-1-1V8a1 1 0 011-1h3V4z"/></svg></div>
          <h3>Single Lesson</h3>
          <p class="pkg-sub">1 &times; 1-hour driving lesson</p>
          <div class="pkg-price">$70<span>/lesson</span></div>
          <ul class="pkg-list">
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Pick-up &amp; drop-off included</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Dual-control vehicle</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Flexible scheduling</li>
          </ul>
          <a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I'd%20like%20to%20enquire%20about%20a%20Single%20Lesson%20(%2470).">Enquire on WhatsApp</a>
        </div>
        <div class="pkg-card">
          <div class="pkg-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6 6.6.7-5 4.4 1.5 6.5L12 16.8 6 19.6l1.5-6.5-5-4.4 6.6-.7z"/></svg></div>
          <h3>5-Lesson Pass</h3>
          <p class="pkg-sub">5 &times; 1-hour driving lessons</p>
          <div class="pkg-price">$325<span>/pack</span></div>
          <div class="pkg-note">Save $25 vs. single lessons</div>
          <ul class="pkg-list">
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Consistent instructor</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Progress tracking</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Bulk-rate pricing</li>
          </ul>
          <a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I'd%20like%20to%20book%20the%205-Lesson%20Pass%20(%24325).">Enquire on WhatsApp</a>
        </div>
        <div class="pkg-card featured">
          <span class="pkg-badge">Most Popular</span>
          <div class="pkg-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 11l1.5-4.5A2 2 0 018.4 5h7.2a2 2 0 011.9 1.5L19 11v7a1 1 0 01-1 1h-1a1 1 0 01-1-1v-1H8v1a1 1 0 01-1 1H6a1 1 0 01-1-1v-7z"/></svg></div>
          <h3>Express Test Package</h3>
          <p class="pkg-sub">2 lessons + test car hire</p>
          <div class="pkg-price">$220<span>/package</span></div>
          <ul class="pkg-list">
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Pre-test refresher lesson</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Compliant test-day vehicle</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Pickup from test centre</li>
          </ul>
          <a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I'd%20like%20to%20book%20the%20Express%20Test%20Package%20(%24220).">Enquire on WhatsApp</a>
        </div>
        <div class="pkg-card">
          <div class="pkg-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 1l9 4v6c0 5.2-3.4 9.6-9 11-5.6-1.4-9-5.8-9-11V5z"/></svg></div>
          <h3>Ultimate Test Pass Pack</h3>
          <p class="pkg-sub">Complete package + extras</p>
          <div class="pkg-price">$560<span>/package</span></div>
          <div class="pkg-note">Save $70 &middot; Best value</div>
          <ul class="pkg-list">
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>5 lessons + 1 mock test</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Free test-day vehicle hire</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Full test-route preparation</li>
          </ul>
          <a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I'd%20like%20to%20book%20the%20Ultimate%20Test%20Pass%20Pack%20(%24560).">Enquire on WhatsApp</a>
        </div>
      </div>
      <p class="price-note">Prices shown are indicative starting rates. Ask on WhatsApp for current availability and bulk-package discounts, and gift vouchers are available for any package.</p>
    </div>
  </section>'''

print("part 1 loaded", len(PACKAGES_SECTION))

def centre_packages_section(centre_name):
    return '''<section class="block block-alt">
    <div class="container">
      <div class="section-title"><h2>Our Driving Packages</h2></div>
      <div class="pkg-grid">
        <div class="pkg-card"><h3>Single Lesson</h3><p class="pkg-sub">1 &times; 1-hour lesson</p><div class="pkg-price">$70</div><a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I''d%20like%20a%20Single%20Lesson%20ahead%20of%20my%20{centre}%20test.">Enquire on WhatsApp</a></div>
        <div class="pkg-card"><h3>5-Lesson Pass</h3><p class="pkg-sub">Save $25</p><div class="pkg-price">$325</div><a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I''d%20like%20the%205-Lesson%20Pass%20ahead%20of%20my%20{centre}%20test.">Enquire on WhatsApp</a></div>
        <div class="pkg-card featured"><span class="pkg-badge">Popular for {centre}</span><h3>Express Test Package</h3><p class="pkg-sub">Lessons + test car hire</p><div class="pkg-price">$220</div><a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I''d%20like%20the%20Express%20Test%20Package%20for%20my%20{centre}%20test.">Enquire on WhatsApp</a></div>
        <div class="pkg-card"><h3>Ultimate Test Pass Pack</h3><p class="pkg-sub">Complete package + extras</p><div class="pkg-price">$560</div><a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I''d%20like%20the%20Ultimate%20Test%20Pass%20Pack%20for%20my%20{centre}%20test.">Enquire on WhatsApp</a></div>
      </div>
    </div>
  </section>'''.replace("''", "'").format(centre=centre_name)

TOOLS_LINKS_SECTION = '''<section class="block">
    <div class="container">
      <div class="section-title"><h2>Interactive Tools</h2></div>
      <div class="tools-grid">
        <div class="tool-card"><h3><svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 11l1.5-4.5A2 2 0 018.4 5h7.2a2 2 0 011.9 1.5L19 11v7a1 1 0 01-1 1h-1a1 1 0 01-1-1v-1H8v1a1 1 0 01-1 1H6a1 1 0 01-1-1v-7z"/></svg>VicRoads Test Readiness Quiz</h3><p>Check your weak spots before test day.</p><a href="readiness-quiz.html" class="btn btn-navy btn-block">Start Quiz &rarr;</a></div>
        <div class="tool-card"><h3><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a4 4 0 014 4c0 2-1.5 3.4-2.5 4.4A6 6 0 0116 16v2a2 2 0 01-2 2H10a2 2 0 01-2-2v-2a6 6 0 012.5-5.6C9.5 9.4 8 8 8 6a4 4 0 014-4z"/></svg>Overseas Licence Conversion Checker</h3><p>Converting from overseas? Check eligibility.</p><a href="licence-checker.html" class="btn btn-navy btn-block">Check Eligibility &rarr;</a></div>
      </div>
    </div>
  </section>'''

def instructor_section(centre_name):
    return '''<section class="block">
    <div class="container">
      <div class="section-title"><h2>Your Instructor for {centre}</h2></div>
      <div class="instructor-card" style="max-width:600px;margin:0 auto">
        <div class="instructor-photo">SP</div>
        <div><h3>Sol Pakzad</h3><p>VicRoads ADI Accredited Instructor &middot; 10+ Years Experience</p>
          <a href="https://au.linkedin.com/in/sol-pakzad-b36761170" target="_blank" rel="noopener">View LinkedIn Profile &rarr;</a>&nbsp;&middot;&nbsp;
          <a href="https://www.facebook.com/share/1HmPRyNByw/" target="_blank" rel="noopener">View Facebook Profile &rarr;</a>
        </div>
      </div>
    </div>
  </section>'''.format(centre=centre_name)

VEHICLE_REQ_SECTION = '''<section class="block block-alt">
    <div class="container">
      <div class="section-title"><h2>Vehicle Requirements</h2></div>
      <div class="two-col">
        <div class="info-card"><h3 style="margin-bottom:10px;color:var(--navy)">Using your own vehicle</h3><ul class="bullet-list"><li>Roadworthy and currently registered</li><li>Working horn, indicators, brake lights, headlights, wipers</li><li>Functioning front and rear demisters</li><li>Valid insurance and correctly displayed L-plates</li></ul></div>
        <div class="info-card"><h3 style="margin-bottom:10px;color:var(--navy)">Using an TDS instructor vehicle</h3><ul class="bullet-list"><li>Already meets all VicRoads compliance requirements</li><li>Dual-control for added safety</li><li>Included in the Express Test Package and Ultimate Test Pass Pack</li></ul></div>
      </div>
    </div>
  </section>'''

TERMINATION_CRITICAL_SECTION = '''<div class="two-col" style="margin-top:20px">
        <div class="info-card"><h3 style="margin-bottom:10px;color:var(--navy)">Immediate Termination Errors</h3><ul class="bullet-list x"><li>Intervention by the tester</li><li>Disobeying a direction/sign</li><li>Collision</li><li>Failing to give way</li><li>Excessive speed</li><li>Stopping in a dangerous position</li><li>Failing to stop</li><li>Dangerous action</li></ul></div>
        <div class="info-card"><h3 style="margin-bottom:10px;color:var(--navy)">Critical Errors</h3><p style="font-size:.82rem;color:var(--muted);margin-bottom:10px">More than 1 in Stage 1, or more than 2 overall, ends the test.</p><ul class="bullet-list warn"><li>Too slow</li><li>Fail to look</li><li>Fail to signal</li><li>Blocking a pedestrian crossing</li><li>Mounting the kerb</li><li>Stalling</li><li>Incomplete stop</li><li>Illegal action</li></ul></div>
      </div>'''

print("part 2 loaded")

# ============================================================
# HOME PAGE
# ============================================================
HOME_HERO = '''<section class="hero">
    <div class="container">
      <div>
        <h1>Driving Instructor Pakenham &amp; VicRoads Test Specialists</h1>
        <p class="lead">Professional, friendly and results-driven driving lessons from a VicRoads ADI accredited instructor. We help learners across Pakenham and the Casey/Cardinia growth corridor pass their VicRoads drive test with confidence, the first time.</p>
        <div class="hero-actions">
          <a class="btn btn-wa" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I'd%20like%20to%20book%20a%20driving%20lesson.">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm5.8 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.1.1-1.8-.1-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.8-2.2 1-2.5c.3-.3.6-.4.8-.4h.6c.2 0 .5 0 .7.5.3.7.9 2.2 1 2.4.1.2.1.4 0 .6-.1.2-.2.3-.4.5l-.5.6c-.2.2-.3.4-.1.7.2.3.9 1.5 1.9 2.4 1.3 1.2 2.4 1.5 2.7 1.7.3.2.5.1.7-.1l.9-1c.2-.3.5-.2.8-.1.3.1 2 1 2.3 1.1.3.2.5.2.6.3.1.2.1.9-.1 1.6z"/></svg>
            Chat on WhatsApp for Instant Help
          </a>
          <button class="btn btn-outline" onclick="openContactModal()">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 4h16a1 1 0 011 1v14a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1zm1 2v.6l7 4.7 7-4.7V6H5zm14 2.3l-6.5 4.3a1 1 0 01-1 0L5 8.3V18h14V8.3z"/></svg>
            Contact Us
          </button>
        </div>
        <div class="hero-badges">
          <span class="hero-badge"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6 6.6.7-5 4.4 1.5 6.5L12 16.8 6 19.6l1.5-6.5-5-4.4 6.6-.7z"/></svg>VicRoads ADI Accredited</span>
          <span class="hero-badge"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6 6.6.7-5 4.4 1.5 6.5L12 16.8 6 19.6l1.5-6.5-5-4.4 6.6-.7z"/></svg>10+ Years Experience</span>
        </div>

        <div class="search-wrap">
          <label for="testCenterSearch">Find your VicRoads test centre</label>
          <div class="search-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
            <input type="text" id="testCenterSearch" placeholder="Try &ldquo;Pakenham&rdquo;&hellip;" autocomplete="off" oninput="filterCenters(this.value)" onkeydown="if(event.key==='Enter'){goToFirstCenterMatch(this.value)}">
            <button onclick="goToFirstCenterMatch(document.getElementById('testCenterSearch').value)">Search</button>
          </div>
          <div id="searchResults" class="search-results" hidden></div>
        </div>
      </div>
      <div class="hero-visual instructor-promo">
        <div class="instructor-promo-top">
          <div class="instructor-promo-avatar">SP</div>
          <div>
            <div class="instructor-promo-name">Sol Pakzad</div>
            <div class="instructor-promo-meta">Auto &middot; 10+ yrs instructing</div>
          </div>
        </div>
        <div class="instructor-promo-price">From $70/hr</div>
        <a href="contact-us.html" class="instructor-promo-btn">View Profile</a>
      </div>
    </div>
  </section>'''

WHY_CHOOSE_SECTION = '''<section class="block">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">Why Transformers</span>
        <h2>Why Choose Transformers Driving School?</h2>
        <p>Five reasons Pakenham-area learners trust Transformers Driving School with their VicRoads test prep.</p>
      </div>
      <div class="why-grid">
        <div class="why-card">
          <div class="why-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4a1 1 0 011-1h8a1 1 0 011 1v3h3a1 1 0 011 1v11a1 1 0 01-1 1H4a1 1 0 01-1-1V8a1 1 0 011-1h3V4zm2 3h6V5H9v2zM4 9v10h16V9H4z"/></svg></div>
          <h3>Flexible Instructor Options</h3>
          <p>Not the right fit? Change instructors anytime, no questions asked.</p>
        </div>
        <div class="why-card">
          <div class="why-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 5v5.4l4.2 2.5-.8 1.3-5-3V7h1.6z"/></svg></div>
          <h3>Convenient Online Booking</h3>
          <p>Manage and reschedule your lessons 24/7 from your phone.</p>
        </div>
        <div class="why-card">
          <div class="why-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 11l1.5-4.5A2 2 0 018.4 5h7.2a2 2 0 011.9 1.5L19 11v7a1 1 0 01-1 1h-1a1 1 0 01-1-1v-1H8v1a1 1 0 01-1 1H6a1 1 0 01-1-1v-7zm2.2-1h9.6l-1-3H8.2l-1 3zM7 14a1 1 0 100-2 1 1 0 000 2zm10 0a1 1 0 100-2 1 1 0 000 2z"/></svg></div>
          <h3>Stress-Free Test Package</h3>
          <p>Combined lessons plus test-day car hire in one booking, with zero hassle.</p>
        </div>
        <div class="why-card">
          <div class="why-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M20 7h-3.2a3 3 0 10-5.6-2 3 3 0 10-5.6 2H2a1 1 0 00-1 1v3a1 1 0 001 1h9v9h2v-9h9a1 1 0 001-1V8a1 1 0 00-1-1zM9 7a1 1 0 111-1 1 1 0 01-1 1zm6 0a1 1 0 111-1 1 1 0 01-1 1zM3 13V9h8v4H3zm10 0V9h8v4h-8zM4 15h7v7H5a1 1 0 01-1-1v-6zm9 0h7v6a1 1 0 01-1 1h-6v-7z"/></svg></div>
          <h3>Gift Vouchers</h3>
          <p>Driving lesson gift cards, a popular gift for new P-platers.</p>
        </div>
        <div class="why-card">
          <div class="why-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 1a2 2 0 012 2v1.06A8 8 0 0119.94 10H21a2 2 0 012 2v0a2 2 0 01-2 2h-1.06A8 8 0 0114 19.94V21a2 2 0 01-2 2 2 2 0 01-2-2v-1.06A8 8 0 014.06 14H3a2 2 0 01-2-2 2 2 0 012-2h1.06A8 8 0 0110 4.06V3a2 2 0 012-2zm0 5a6 6 0 100 12 6 6 0 000-12z"/></svg></div>
          <h3>Transparent Pricing</h3>
          <p>Clear, upfront pricing with bulk discounts on lesson packages.</p>
        </div>
      </div>
    </div>
  </section>'''

TOOLS_HOME_SECTION = '''<section class="block" id="tools">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">Free Interactive Tools</span>
        <h2>Check Where You Stand in Under a Minute</h2>
        <p>No phone call needed. Try the quick versions below, or open the full tool for a detailed report.</p>
      </div>
      <div class="tools-grid">
        <div class="tool-card">
          <h3><svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 11l1.5-4.5A2 2 0 018.4 5h7.2a2 2 0 011.9 1.5L19 11v7a1 1 0 01-1 1h-1a1 1 0 01-1-1v-1H8v1a1 1 0 01-1 1H6a1 1 0 01-1-1v-7z"/></svg>VicRoads Test Readiness Quiz</h3>
          <p>3 quick questions to get an instant read on your weak spots.</p>
          <div id="miniQuizArea">
            <div class="quiz-progress" id="miniQuizProgress">Question 1 of 3</div>
            <div class="progress-bar"><div class="progress-fill" id="miniQuizFill" style="width:33%"></div></div>
            <div class="quiz-q" id="miniQuizQ">How confident are you with parallel or reverse parking?</div>
            <div class="quiz-options" id="miniQuizOptions">
              <button onclick="miniAnswerQuiz(0)">Very confident, consistent every time</button>
              <button onclick="miniAnswerQuiz(1)">Somewhat, sometimes need extra attempts</button>
              <button onclick="miniAnswerQuiz(2)">Not confident, I avoid it</button>
            </div>
          </div>
          <div class="tool-result" id="miniQuizResult"></div>
          <a href="readiness-quiz.html" class="tool-link">Take the full 8-question quiz &rarr;</a>
        </div>

        <div class="tool-card">
          <h3><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a4 4 0 014 4c0 2-1.5 3.4-2.5 4.4A6 6 0 0116 16v2a2 2 0 01-2 2H10a2 2 0 01-2-2v-2a6 6 0 012.5-5.6C9.5 9.4 8 8 8 6a4 4 0 014-4z"/></svg>Overseas Licence Conversion Checker</h3>
          <p>Find out in seconds whether you can convert directly, or need a test.</p>
          <div class="tool-field">
            <label>Which country issued your licence?</label>
            <select id="miniCountrySelect">
              <option value="">Select country</option>
              <option value="recognised">UK, Ireland, Canada, Germany, Japan, South Korea</option>
              <option value="edr">India, USA, South Africa, Philippines, Malaysia</option>
              <option value="other">Other country not listed</option>
            </select>
          </div>
          <div class="tool-field">
            <label>Your current age</label>
            <input type="number" id="miniAgeInput" placeholder="e.g. 27" min="16" max="99">
          </div>
          <button class="tool-btn" onclick="miniCheckLicence()">Check My Pathway</button>
          <div class="tool-result" id="miniLicenceResult"></div>
          <a href="licence-checker.html" class="tool-link">Open the full checker with requirements table &rarr;</a>
        </div>
      </div>
    </div>
  </section>'''

REVIEWS_SECTION = '''<section class="block block-alt" id="reviews">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">Social Proof</span>
        <h2>What Learners Say on Facebook</h2>
        <p>Real feedback from Pakenham-area learners who booked lessons with Transformers Driving School.</p>
      </div>
      <div class="fb-reviews-wrap">
        <a class="fb-badge" target="_blank" rel="noopener" href="https://www.facebook.com/transformersdrivingschool/reviews">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1.5 8h1.8v2.2h-1.8V21h-2.4v-8.8H9.7V10h1.4V8.7c0-1.9 1-3 3.2-3h1.8v2.2h-1.2c-.6 0-1.4.2-1.4 1V10z"/></svg>
          <div class="fb-badge-stats">
            <strong>100% Recommended</strong>
            <span>59 reviews on Facebook</span>
          </div>
        </a>
        <div class="fb-review-cards">
          <div class="fb-review-card">
            <div class="fb-review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <p>&ldquo;Passed first go thanks to the local test route practice. Highly recommend Transformers Driving School.&rdquo;</p>
            <span class="fb-review-name">Facebook recommendation</span>
          </div>
          <div class="fb-review-card">
            <div class="fb-review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <p>&ldquo;Patient, friendly instructor and easy online booking. Would recommend to any Pakenham learner.&rdquo;</p>
            <span class="fb-review-name">Facebook recommendation</span>
          </div>
          <div class="fb-review-card">
            <div class="fb-review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <p>&ldquo;Great value test package, car hire made test day stress-free.&rdquo;</p>
            <span class="fb-review-name">Facebook recommendation</span>
          </div>
        </div>
        <a class="btn btn-outline" target="_blank" rel="noopener" href="https://www.facebook.com/transformersdrivingschool/reviews">See All Reviews on Facebook &rarr;</a>
      </div>
    </div>
  </section>'''

AREAS_SECTION = '''<section class="block" id="areas">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">Where We Cover</span>
        <h2>VicRoads Test Centre &amp; Service Areas</h2>
        <p>We prepare students for the VicRoads drive test at Pakenham, with lessons available across Officer, Beaconsfield, Berwick, Nar Nar Goon, Clyde, Cranbourne, Cardinia and Devon Meadows.</p>
      </div>
      <div class="area-grid">
        <a href="drive-test-pakenham.html" class="area-chip">Drive Test Pakenham<small>Test centre guide</small></a>
        <a href="area-officer.html" class="area-chip">Officer<small>Service area</small></a>
        <a href="area-beaconsfield.html" class="area-chip">Beaconsfield<small>Service area</small></a>
        <a href="area-berwick.html" class="area-chip">Berwick<small>Service area</small></a>
        <a href="area-nar-nar-goon.html" class="area-chip">Nar Nar Goon<small>Service area</small></a>
        <a href="area-clyde.html" class="area-chip">Clyde<small>Service area</small></a>
        <a href="area-cranbourne.html" class="area-chip">Cranbourne<small>Service area</small></a>
        <a href="area-cardinia.html" class="area-chip">Cardinia<small>Service area</small></a>
        <a href="area-devon-meadows.html" class="area-chip">Devon Meadows<small>Service area</small></a>
      </div>
    </div>
  </section>'''

FAQ_SECTION = '''<section class="block block-alt" id="faq">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">FAQ</span>
        <h2>Frequently Asked Questions</h2>
      </div>
      <div class="faq-list" id="homeFaqList"></div>
    </div>
  </section>'''

FINAL_CTA_HOME = '''<section class="final-cta" id="contact-info">
    <div class="container">
      <h2>Ready to Book Your First Lesson?</h2>
      <p>Message us on WhatsApp, the fastest way to lock in a time slot with a VicRoads ADI accredited instructor.</p>
      <div class="btn-row">
        <a class="btn btn-wa" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I'd%20like%20to%20book%20a%20driving%20lesson.">Chat on WhatsApp</a>
        <a class="btn btn-outline" href="tel:0404119119">Call 0404 119 119</a>
        <a class="btn btn-outline" href="contact-us.html">Visit Contact Page</a>
      </div>
    </div>
  </section>'''

HOME_BODY = '\n  '.join([
    HOME_HERO,
    trust_section_html(),
    WHY_CHOOSE_SECTION,
    PACKAGES_SECTION,
    TOOLS_HOME_SECTION,
    REVIEWS_SECTION,
    AREAS_SECTION,
    FAQ_SECTION,
    nap_faq_section(
        "Pakenham",
        extra_faqs=[
            ("Does Transformers Driving School offer driving lessons in Pakenham?",
             "Yes, Pakenham is our main service area and the home of our VicRoads test centre guide. We offer driving lessons Pakenham learners can book directly, with flexible instructor options and pickup from home, school or work."),
            ("Which VicRoads test centre do Pakenham learners use?",
             "Pakenham learners sit their practical drive test at <a href=\"drive-test-pakenham.html\">VicRoads Pakenham</a>, and our instructors prepare you specifically for that test centre's local roads."),
            ("How much do driving lessons cost in Pakenham?",
             "Pricing is the same for all Pakenham-area learners. See our Lessons &amp; Test Packages above, from a Single Lesson through to the Ultimate Test Pass Pack, with bulk discounts available, and message us on WhatsApp for current availability."),
        ],
    ),
    FINAL_CTA_HOME,
])

home_html = page_shell(
    title="Driving Instructor Pakenham | VicRoads Test Prep",
    description="VicRoads ADI accredited driving lessons in Pakenham &amp; the Casey/Cardinia corridor. Book a lesson or test package on WhatsApp today.",
    depth=0,
    body_content=HOME_BODY,
    page_key="home",
    schema=SCHEMA,
    breadcrumbs=[("Home", None)],
    show_sidebar=False,
)
open(os.path.join(OUT, "index.html"), "w").write(home_html)
print("index.html written:", len(home_html), "bytes")

# ============================================================
# DRIVE TEST PAKENHAM (only VicRoads centre page for this site)
# ============================================================
# Assumption flagged in the build log / final summary: exact current-day
# local Pakenham test-route street names are not independently confirmed,
# so the "local roads" section below stays general/high-level (major
# arterials + generic manoeuvre streets) rather than naming specific
# addresses or laneways with unconfirmed confidence.
PAKENHAM_HERO = '''<section class="page-hero">
    <div class="container">
      <h1>VicRoads Drive Test Pakenham</h1>
      <p>Everything you need to know about the Pakenham VicRoads test centre: test centre details, the two-stage test format, and how Transformers Driving School instructors prepare Pakenham learners for test day.</p>
      ''' + BYLINE + '''
    </div>
  </section>'''

PAKENHAM_BODY = '\n  '.join([
    PAKENHAM_HERO,
    trust_section_html(),
    '''<section class="block">
    <div class="container">
      <div class="info-grid">
        <div class="info-card">
          <h2><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7zm0 9.5A2.5 2.5 0 1112 6.5a2.5 2.5 0 010 5z"/></svg>Test Centre Details</h2>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg><div><strong>Location</strong><span>VicRoads Pakenham Customer Service Centre, Pakenham VIC 3810 (exact suite/street number changes periodically &mdash; confirm on your booking confirmation)</span></div></div>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 5v5.4l4.2 2.5-.8 1.3-5-3V7h1.6z"/></svg><div><strong>Hours</strong><span>Monday to Friday, 8:30 am to 4:30 pm (by appointment only)</span></div></div>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 16V6a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H8l-4 4v-6z"/></svg><div><strong>Public transit access</strong><span>Close to Pakenham railway station (Pakenham line) and the Pakenham bus interchange, with several local bus routes serving the town centre</span></div></div>
        </div>
        <div class="info-card">
          <h3 style="margin-bottom:10px">Quick facts</h3>
          <ul class="bullet-list">
            <li>Minor faults: up to 15 allowed before failing</li>
            <li>Test runs in two stages: 10 minutes + 20 minutes</li>
            <li>Pre-drive safety check required before you start driving</li>
            <li>One of the busier growth-corridor test centres, so book appointments early</li>
          </ul>
        </div>
      </div>
    </div>
  </section>''',
    '''<section class="block block-alt">
    <div class="container">
      <div class="section-title"><h2>Test Format &amp; Rules</h2></div>
      <div class="two-col">
        <div class="info-card">
          <h3 style="margin-bottom:10px;color:var(--navy)">Minor vs. Major / Dangerous Faults</h3>
          <ul class="bullet-list">
            <li>Minor faults: up to 15 allowed across the whole test</li>
            <li>16th minor fault results in an automatic fail</li>
          </ul>
          <ul class="bullet-list x" style="margin-top:10px">
            <li>Major or dangerous faults result in an immediate fail, regardless of minor fault count</li>
          </ul>
        </div>
        <div class="info-card">
          <h3 style="margin-bottom:10px;color:var(--navy)">Pre-Drive Safety Checks Checklist</h3>
          <ul class="bullet-list">
            <li>Horn</li><li>Indicators</li><li>Wipers</li><li>Brake lights</li><li>Demisters (front &amp; rear)</li><li>Boot</li><li>Ignition in neutral / park before starting</li>
          </ul>
        </div>
      </div>
      <div class="two-col" style="margin-top:20px">
        <div class="stage-card">
          <h3>Stage 1: Basic Controls</h3>
          <div class="stage-meta">Duration: 10 minutes</div>
          <p>Low-risk manoeuvres such as a 3-point turn or reverse parallel park, usually on the quieter residential streets near the centre. You must pass Stage 1 before progressing to Stage 2.</p>
        </div>
        <div class="stage-card">
          <h3>Stage 2: Busy Traffic</h3>
          <div class="stage-meta">Duration: 20 minutes</div>
          <p>Conducted on busier roads around Pakenham: the Princes Highway corridor, roundabouts, lane changes, and complex intersections through the town centre and growth-corridor estates.</p>
        </div>
      </div>
      ''' + TERMINATION_CRITICAL_SECTION + '''
    </div>
  </section>''',
    '''<section class="block">
    <div class="container">
      <div class="section-title">
        <h2>Local Pakenham Test Roads &amp; Fail Points</h2>
        <p>General guidance based on the type of roads used around the Pakenham test centre. Note: exact current test routes vary by tester and can change over time, so treat this as a guide to the kinds of conditions to practise, not a guaranteed route.</p>
      </div>
      <div class="fail-point">
        <div class="fail-num">1</div>
        <div><h3>Princes Highway corridor <span class="speed">80 km/h</span></h3><p>High-speed merging and lane discipline is a common focus, since Pakenham&rsquo;s main highway corridor runs directly through the area.</p></div>
      </div>
      <div class="fail-point">
        <div class="fail-num">2</div>
        <div><h3>Pakenham town centre streets <span class="speed">50 km/h</span></h3><p>Busy town-centre streets with pedestrian crossings and frequent give-way situations near shops and the train station.</p></div>
      </div>
      <div class="fail-point">
        <div class="fail-num">3</div>
        <div><h3>Local roundabouts <span class="speed">50 / 60 km/h</span></h3><p>Roundabout entry and exit lane discipline is a common focus area in Stage 2, given the number of roundabouts across the growth-corridor estates.</p></div>
      </div>
      <div class="fail-point">
        <div class="fail-num">4</div>
        <div><h3>Residential estate streets <span class="speed">40 / 50 km/h</span></h3><p>Quieter residential streets near the centre are commonly used for Stage 1 low-speed manoeuvres such as 3-point turns and reverse parallel parks.</p></div>
      </div>
    </div>
  </section>''',
    VEHICLE_REQ_SECTION,
    instructor_section("Pakenham"),
    centre_packages_section("Pakenham"),
    TOOLS_LINKS_SECTION,
])

pakenham_html = page_shell(
    title="VicRoads Drive Test Pakenham | Test Centre Guide",
    description="Pakenham VicRoads test centre hours, the two-stage test format &amp; local fail points. Book a lesson with Sol Pakzad, VicRoads ADI accredited.",
    depth=0,
    body_content=PAKENHAM_BODY,
    page_key="drive-test-pakenham",
    breadcrumbs=[("Drive Test Pakenham", None)],
)
open(os.path.join(OUT, "drive-test-pakenham.html"), "w").write(pakenham_html)
print("drive-test-pakenham.html written:", len(pakenham_html), "bytes")

# ============================================================
# COUNTRY-SPECIFIC LICENCE CONVERSION PAGES
# ============================================================
TIER_INFO = {
    "recognised": {
        "label": "Recognised Country",
        "summary": "Direct exchange, with no knowledge or practical test required in most cases.",
        "requirement": "No age or experience requirement in most cases.",
    },
    "edr": {
        "label": "Experienced Driver Recognition Country",
        "summary": "A knowledge test is generally required, and a practical driving test as well if you're under 25 or have less driving experience.",
        "requirement": "Under 25 usually needs a knowledge + practical test; 25+ with 3+ years&rsquo; experience may qualify for a more direct pathway.",
    },
    "other": {
        "label": "Full Victorian Licensing Process",
        "summary": "The full Victorian process applies: a knowledge test, a hazard perception test, and a practical driving test.",
        "requirement": "Applies regardless of age or driving experience.",
    },
}

COUNTRIES = [
    {
        "name": "India", "slug": "india", "tier": "edr",
        "note": "Indian driving licences fall under Victoria&rsquo;s Experienced Driver Recognition tier. Requirements depend on your age and years of driving experience on your Indian licence.",
    },
    {
        "name": "Philippines", "slug": "philippines", "tier": "edr",
        "note": "Philippine driving licences fall under Victoria&rsquo;s Experienced Driver Recognition tier. Requirements depend on your age and years of driving experience on your Philippine licence.",
    },
    {
        "name": "China", "slug": "china", "tier": "other",
        "note": "Chinese driving licences are not currently on Victoria&rsquo;s Recognised or Experienced Driver Recognition lists, so the full Victorian licensing process applies.",
    },
    {
        "name": "Sri Lanka", "slug": "sri-lanka", "tier": "other",
        "note": "Sri Lankan driving licences are not currently on Victoria&rsquo;s Recognised or Experienced Driver Recognition lists, so the full Victorian licensing process applies.",
    },
    {
        "name": "Pakistan", "slug": "pakistan", "tier": "other",
        "note": "Pakistani driving licences are not currently on Victoria&rsquo;s Recognised or Experienced Driver Recognition lists, so the full Victorian licensing process applies.",
    },
    {
        "name": "Nepal", "slug": "nepal", "tier": "other",
        "note": "Nepalese driving licences are not currently on Victoria&rsquo;s Recognised or Experienced Driver Recognition lists, so the full Victorian licensing process applies.",
    },
    {
        "name": "United Kingdom", "slug": "uk", "tier": "recognised",
        "note": "UK driving licences are on Victoria&rsquo;s Recognised country list, meaning a direct exchange is usually possible with no test required.",
    },
]

COUNTRY_LINKS_HTML = "\n        ".join(
    '<a href="{slug}-to-vicroads-licence.html" class="area-chip">{name}<small>{label}</small></a>'.format(
        slug=c["slug"], name=c["name"], label=TIER_INFO[c["tier"]]["label"]
    ) for c in COUNTRIES
)

def country_page(country):
    name = country["name"]
    slug = country["slug"]
    tier = TIER_INFO[country["tier"]]
    note = country["note"]

    hero = '''<section class="page-hero">
    <div class="container">
      <h1>{name} to VicRoads Driving Licence Conversion</h1>
      <p>How to convert your {name} driving licence to a Victorian licence: your tier, requirements, and step-by-step process.</p>
      {byline}
    </div>
  </section>'''.format(name=name, byline=BYLINE)

    intro = '''<section class="block">
    <div class="container" style="max-width:800px">
      <p style="font-size:1rem;color:#334155">If you&rsquo;re moving to Victoria with a {name} driving licence and want to convert overseas licence Victoria requirements into a plain checklist, you&rsquo;re in the right place. This guide covers exactly what a {name} licence holder needs to do to convert their licence to a Victorian one, and it forms part of our broader guide to convert international licence Melbourne newcomers can follow for any country.</p>
    </div>
  </section>'''.format(name=name)

    tier_card = '''<section class="block block-alt">
    <div class="container">
      <div class="info-grid">
        <div class="info-card">
          <h2><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm-1.2 14.4l-4.2-4.2 1.4-1.4 2.8 2.8 6-6 1.4 1.4z"/></svg>Your Tier: {label}</h2>
          <p style="font-size:.9rem;color:#334155;margin-bottom:12px">{summary}</p>
          <p style="font-size:.85rem;color:var(--muted)">{note}</p>
        </div>
        <div class="info-card">
          <h3 style="margin-bottom:10px">Age / Experience Requirement</h3>
          <p style="font-size:.88rem;color:var(--muted)">{requirement}</p>
          <div style="margin-top:16px"><a href="licence-checker.html" class="tool-link">Use the full interactive checker for your exact pathway &rarr;</a></div>
        </div>
      </div>
    </div>
  </section>'''.format(label=tier["label"], summary=tier["summary"], note=note, requirement=tier["requirement"])

    steps = '''<section class="block">
    <div class="container">
      <div class="section-title"><h2>Step-by-Step: {name} Licence to Victorian Licence</h2></div>
      <ol class="step-list" style="max-width:700px;margin:0 auto">
        <li><h3>Confirm your tier</h3><p>Use our checker to confirm your {name} licence falls under the {label} tier before starting the process.</p></li>
        <li><h3>Gather your documents</h3><p>Valid {name} licence, passport/visa, proof of Victorian address, and an official English translation if your licence isn&rsquo;t in English.</p></li>
        <li><h3>Book any required tests</h3><p>{summary}</p></li>
        <li><h3>Prepare with a local instructor</h3><p>If a practical test is required, TDS instructors can prepare you for your specific VicRoads test centre. See our guide for Pakenham.</p></li>
        <li><h3>Receive your Victorian licence</h3><p>Once you&rsquo;ve completed the required steps, your Victorian driver licence is issued and your {name} licence is typically surrendered.</p></li>
      </ol>
    </div>
  </section>'''.format(name=name, label=tier["label"], summary=tier["summary"])

    faq = '''<section class="block block-alt">
    <div class="container">
      <div class="section-title"><span class="eyebrow">FAQ</span><h2>{name} Licence Conversion FAQ</h2></div>
      <div class="faq-list">
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">Do I need a driving test to convert my {name} licence in Victoria?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">{summary} Use our checker above (link) to confirm your exact requirement based on your age and experience.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">How can TDS help me convert my {name} licence?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">Our VicRoads ADI accredited instructors prepare {name} licence holders specifically for the Victorian practical test where one is required, including the local test route at Pakenham.</div></div>
        </div>
      </div>
    </div>
  </section>'''.format(name=name, summary=tier["summary"])

    body = '\n  '.join([hero, trust_section_html(), intro, tier_card, steps, faq, TOOLS_LINKS_SECTION])

    html = page_shell(
        title="{name} to VicRoads Licence Conversion | TDS".format(name=name),
        description="Convert your {name} driving licence to a Victorian licence: your tier, requirements &amp; steps. Check your free pathway now.".format(name=name),
        depth=0,
        body_content=body,
        page_key="licence-checker",
        breadcrumbs=[("Licence Checker", "licence-checker.html"), (name, None)],
    )
    fname = "{slug}-to-vicroads-licence.html".format(slug=slug)
    open(os.path.join(OUT, fname), "w").write(html)
    print(fname, "written:", len(html), "bytes")


# ============================================================
# READINESS QUIZ PAGE
# ============================================================
QUIZ_BODY = '\n  '.join([
    '''<section class="page-hero">
    <div class="container">
      <h1>Are You Ready for Your VicRoads Test?</h1>
      <p>8 quick questions. Get your weak spots and a personalised lesson recommendation at the end, completely free.</p>
      ''' + BYLINE + '''
    </div>
  </section>''',
    trust_section_html(),
    '''<section class="block">
    <div class="container" style="max-width:760px">
      <div class="tool-card" style="padding:32px">
        <div id="fullQuizArea">
          <div class="quiz-progress" id="fullQuizProgress">Question 1 of 8</div>
          <div class="progress-bar"><div class="progress-fill" id="fullQuizFill" style="width:12.5%"></div></div>
          <div class="quiz-q" id="fullQuizQ"></div>
          <div class="quiz-options" id="fullQuizOptions"></div>
        </div>
        <div class="tool-result" id="fullQuizResult"></div>
      </div>
      <p class="price-note">This quiz gives general guidance only and is not a substitute for an in-car assessment with a qualified instructor.</p>
    </div>
  </section>''',
    '''<section class="block block-alt">
    <div class="container" style="max-width:800px">
      <div class="section-title">
        <span class="eyebrow">How to Pass Your VicRoads Test</span>
        <h2>How to Pass Your VicRoads Driving Test</h2>
        <p>Straightforward, instructor-reviewed guidance for learners preparing for their VicRoads drive test in Melbourne.</p>
      </div>
      <div class="info-card" style="margin-bottom:16px">
        <h3 style="color:var(--navy);margin-bottom:8px">Common VicRoads Test Fail Reasons</h3>
        <p style="font-size:.9rem;color:var(--muted)">Most learners who don&rsquo;t pass fall down on a small number of repeat issues: incomplete mirror and blind-spot checks, hesitating at roundabouts, poor speed control through school zones, and struggling with parallel or reverse parking under time pressure. The readiness quiz above is built around these exact weak spots so you can target your remaining practice instead of guessing.</p>
      </div>
      <div class="info-card" style="margin-bottom:16px">
        <h3 style="color:var(--navy);margin-bottom:8px">How Many Lessons Before My Driving Test?</h3>
        <p style="font-size:.9rem;color:var(--muted)">There&rsquo;s no single answer, since it depends on your existing supervised driving hours and confidence level. As a general guide, most learners with solid practice need 5 to 10 lessons focused on test-day manoeuvres and their local test route, while learners with less experience or specific weak areas often benefit from a full lesson package such as our 5-Lesson Pass or Ultimate Test Pass Pack. Your quiz result above gives a personalised starting point.</p>
      </div>
      <div class="info-card">
        <h3 style="color:var(--navy);margin-bottom:8px">Driving Test Practice Tips for Melbourne Learners</h3>
        <ul class="bullet-list">
          <li>Practise on or near your actual test route before test day. See our test centre guide for Pakenham.</li>
          <li>Do a full pre-drive safety check every time you practise, not just before the test.</li>
          <li>Book a lesson in the same time slot as your test so you&rsquo;re used to that traffic pattern.</li>
          <li>Focus extra practice on whatever the quiz above flags as your weak spot, rather than just repeating what you&rsquo;re already good at.</li>
        </ul>
      </div>
    </div>
  </section>''',
    '''<section class="block">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">FAQ</span>
        <h2>Readiness &amp; Test Prep FAQ</h2>
      </div>
      <div class="faq-list">
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">Am I ready for my driving test?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">Take the free quiz above. It checks the areas VicRoads testers focus on most (parking, roundabouts, observation, highway merging) and gives you a personalised readiness result in under two minutes.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">What are the most common VicRoads test fail reasons?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">Incomplete observation checks, hesitating at roundabouts, incorrect speed in school zones, and parking manoeuvres that need more than the allowed attempts are the most frequent reasons learners lose enough points to fail.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">How many lessons do I need before my driving test?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">Most learners need 5 to 10 lessons focused on test manoeuvres and their local test route, on top of general supervised practice. Your quiz result above gives a recommendation based on your specific weak spots.</div></div>
        </div>
      </div>
    </div>
  </section>''',
])

quiz_html = page_shell(
    title="VicRoads Test Readiness Quiz | Free Driving Test Check | TDS",
    description="Take our free 8-question VicRoads test readiness quiz to see if you're ready, and get a personalised lesson recommendation in under 2 minutes.",
    depth=0,
    body_content=QUIZ_BODY,
    page_key="readiness-quiz",
    breadcrumbs=[("Readiness Quiz", None)],
)
open(os.path.join(OUT, "readiness-quiz.html"), "w").write(quiz_html)
print("readiness-quiz.html written:", len(quiz_html), "bytes")

# ============================================================
# LICENCE CHECKER PAGE
# ============================================================
CHECKER_BODY = '\n  '.join([
    '''<section class="page-hero">
    <div class="container">
      <h1>Overseas Licence Conversion Checker</h1>
      <p>Find out whether you can convert your overseas licence directly, need a knowledge test only, or must complete the full VicRoads driving test.</p>
      ''' + BYLINE + '''
    </div>
  </section>''',
    trust_section_html(),
    '''<section class="block">
    <div class="container" style="max-width:760px">
      <div class="tool-card" style="padding:32px">
        <div class="tool-field">
          <label>Which country issued your current licence?</label>
          <select id="fullCountrySelect">
            <option value="">Select country</option>
            <option value="recognised">Recognised country (UK, Ireland, Canada, France, Germany, Japan, South Korea, Austria, Switzerland)</option>
            <option value="edr">Experienced Driver Recognition country (India, USA, South Africa, Philippines, Malaysia, Zimbabwe)</option>
            <option value="other">Other country not listed</option>
          </select>
        </div>
        <div class="tool-field">
          <label>Your current age</label>
          <input type="number" id="fullAgeInput" placeholder="e.g. 27" min="16" max="99">
        </div>
        <div class="tool-field">
          <label>Years of driving experience on your overseas licence</label>
          <input type="number" id="fullExpInput" placeholder="e.g. 5" min="0" max="80">
        </div>
        <button class="tool-btn" onclick="fullCheckLicence()">Check My Pathway</button>
        <div class="tool-result" id="fullLicenceResult"></div>
      </div>
    </div>
  </section>''',
    '''<section class="block block-alt">
    <div class="container">
      <div class="section-title">
        <h2>Victoria&rsquo;s 3-Tier Overseas Licence System</h2>
        <p>Every country falls into one of three tiers, which determines what, if anything, you need to do to convert your licence in Victoria.</p>
      </div>
      <div class="table-wrap">
        <table class="req-table">
          <thead><tr><th>Tier</th><th>Example countries</th><th>Age / experience requirement</th><th>What&rsquo;s required</th></tr></thead>
          <tbody>
            <tr><td><strong>1. Recognised country</strong></td><td>UK, Ireland, Canada, Germany, Japan, South Korea</td><td>No specific requirement</td><td>Direct exchange, no test in most cases</td></tr>
            <tr><td><strong>2. Experienced Driver Recognition</strong></td><td>India, USA, South Africa, Philippines, Malaysia</td><td>Under 25 usually needs knowledge + practical test; 25+ with 3+ years&rsquo; experience may qualify for a more direct pathway</td><td>Knowledge test, and often a practical drive test, depending on age/experience</td></tr>
            <tr><td><strong>3. Other country</strong></td><td>All countries not listed under tiers 1 or 2</td><td>Applies regardless of age or experience</td><td>Full Victorian process: knowledge test, hazard perception test, practical driving test</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>''',
    '''<section class="block">
    <div class="container">
      <div class="section-title">
        <h2>Step-by-Step Conversion Process</h2>
      </div>
      <ol class="step-list" style="max-width:700px;margin:0 auto">
        <li><h3>Check your tier</h3><p>Use the checker above to confirm whether your issuing country is Recognised, Experienced Driver Recognition, or Other.</p></li>
        <li><h3>Gather your documents</h3><p>Valid overseas licence, passport/visa, proof of address, and an official translation if your licence isn&rsquo;t in English.</p></li>
        <li><h3>Book a knowledge test (if required)</h3><p>Tiers 2 and 3 generally require a computer-based knowledge test on Victorian road rules.</p></li>
        <li><h3>Complete a hazard perception test (Tier 3)</h3><p>Required as part of the full licensing process for countries not covered by an exchange or recognition agreement.</p></li>
        <li><h3>Take your practical drive test</h3><p>Where required, TDS instructors can prepare you specifically for your local VicRoads test centre. See our test centre guide for Pakenham.</p></li>
        <li><h3>Receive your Victorian licence</h3><p>Once you pass the required steps, your Victorian driver licence is issued and your overseas licence is typically surrendered.</p></li>
      </ol>
    </div>
  </section>''',
    '''<section class="block block-alt" id="country-guides">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">Country-Specific Guides</span>
        <h2>Converting From a Specific Country?</h2>
        <p>We&rsquo;re building detailed, country-specific conversion guides, each covering your exact tier, requirements, and step-by-step process.</p>
      </div>
      <div class="area-grid" id="countryLinksGrid">
        {country_links}
      </div>
    </div>
  </section>''',
    '''<section class="block">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">FAQ</span>
        <h2>Licence Conversion FAQ</h2>
      </div>
      <div class="faq-list">
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">How do I convert an overseas licence in Victoria?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">It depends on which country issued your licence. Use the checker above to find your tier, then follow the step-by-step process: gather your documents, sit a knowledge test if required, complete a hazard perception and/or practical test if required, then receive your Victorian licence.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">Do I need a driving test to convert my licence in Victoria?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">Only if your issuing country isn&rsquo;t in the Recognised tier. Experienced Driver Recognition countries may need a practical test depending on your age and experience, and all other countries require the full Victorian driving test.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">What is the recognised country driving licence list for Victoria?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">Recognised countries, including the UK, Ireland, Canada, France, Germany, Japan, South Korea, Austria and Switzerland, can generally exchange their licence directly for a Victorian one with no test, subject to standard eligibility checks.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">What is an Experienced Driver Recognition country?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">A tier that includes countries such as India, the USA, South Africa, the Philippines and Malaysia. Requirements depend on your age and years of driving experience, typically a knowledge test, and a practical test if you&rsquo;re under 25 or have less experience.</div></div>
        </div>
      </div>
    </div>
  </section>''',
])
CHECKER_BODY = CHECKER_BODY.format(country_links=COUNTRY_LINKS_HTML)

checker_html = page_shell(
    title="Overseas Licence Conversion Checker | Victoria Rules | TDS",
    description="Find out free if you can convert your overseas licence directly, or need a knowledge/practical test in Victoria. Check your tier and requirements now.",
    depth=0,
    body_content=CHECKER_BODY,
    page_key="licence-checker",
    breadcrumbs=[("Licence Checker", None)],
)
open(os.path.join(OUT, "licence-checker.html"), "w").write(checker_html)
print("licence-checker.html written:", len(checker_html), "bytes")

# ============================================================
# CONTACT US PAGE
# ============================================================
CONTACT_BODY = '\n  '.join([
    '''<section class="page-hero">
    <div class="container">
      <h1>Contact Transformers Driving School</h1>
      <p>Questions about lessons, test packages, or which VicRoads test centre suits you? Reach us on WhatsApp, phone, or send an enquiry below.</p>
    </div>
  </section>''',
    trust_section_html(),
    '''<section class="block">
    <div class="container">
      <div class="contact-grid">
        <div>
          <div class="section-title" style="text-align:left;margin-bottom:10px">
            <span class="eyebrow">Get In Touch</span>
            <h2>Ways to Reach Us</h2>
          </div>
          <p style="color:var(--muted);font-size:.9rem">We usually reply within the hour during business hours. WhatsApp is the fastest way to lock in a lesson time.</p>
          <div class="contact-methods">
            <a class="contact-method" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I'd%20like%20to%20get%20in%20touch.">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm5.8 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.1.1-1.8-.1-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.8-2.2 1-2.5c.3-.3.6-.4.8-.4h.6c.2 0 .5 0 .7.5.3.7.9 2.2 1 2.4.1.2.1.4 0 .6-.1.2-.2.3-.4.5l-.5.6c-.2.2-.3.4-.1.7.2.3.9 1.5 1.9 2.4 1.3 1.2 2.4 1.5 2.7 1.7.3.2.5.1.7-.1l.9-1c.2-.3.5-.2.8-.1.3.1 2 1 2.3 1.1.3.2.5.2.6.3.1.2.1.9-.1 1.6z"/></svg>
              <div><strong>WhatsApp</strong><span>0404 119 119 (fastest response)</span></div>
            </a>
            <a class="contact-method" href="tel:0404119119">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
              <div><strong>Call or Text</strong><span>0404 119 119</span></div>
            </a>
            <a class="contact-method" target="_blank" rel="noopener" href="https://au.linkedin.com/in/sol-pakzad-b36761170">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h14zM8.34 18v-8.4H5.67V18h2.67zM7 8.4a1.55 1.55 0 100-3.1 1.55 1.55 0 000 3.1zM18.34 18v-4.6c0-2.46-1.31-3.6-3.06-3.6-1.41 0-2.04.78-2.39 1.32V10h-2.65v8h2.65v-4.47c0-1.18.22-2.32 1.68-2.32 1.45 0 1.47 1.35 1.47 2.4V18h2.3z"/></svg>
              <div><strong>Instructor LinkedIn</strong><span>Sol Pakzad, VicRoads ADI Accredited</span></div>
            </a>
            <a class="contact-method" target="_blank" rel="noopener" href="https://www.facebook.com/share/1HmPRyNByw/">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1.5 8h1.8v2.2h-1.8V21h-2.4v-8.8H9.7V10h1.4V8.7c0-1.9 1-3 3.2-3h1.8v2.2h-1.2c-.6 0-1.4.2-1.4 1V10z"/></svg>
              <div><strong>Instructor Facebook</strong><span>Sol Pakzad, VicRoads ADI Accredited</span></div>
            </a>
          </div>
          <div class="info-card" style="margin-top:20px">
            <h3 style="margin-bottom:10px;color:var(--navy)">Service Areas</h3>
            <p style="font-size:.86rem;color:var(--muted);margin-bottom:10px">Lessons across Pakenham and the Casey/Cardinia growth corridor, with VicRoads test preparation for:</p>
            <ul class="bullet-list">
              <li><a href="drive-test-pakenham.html">Pakenham</a></li>
              <li><a href="area-officer.html">Officer</a></li>
              <li><a href="area-beaconsfield.html">Beaconsfield</a></li>
              <li><a href="area-berwick.html">Berwick</a></li>
              <li><a href="area-nar-nar-goon.html">Nar Nar Goon</a></li>
              <li><a href="area-clyde.html">Clyde</a></li>
              <li><a href="area-cranbourne.html">Cranbourne</a></li>
              <li><a href="area-cardinia.html">Cardinia</a></li>
              <li><a href="area-devon-meadows.html">Devon Meadows</a></li>
            </ul>
          </div>
        </div>

        <div class="tool-card" style="padding:30px">
          <h3 style="margin-bottom:6px">Send Us an Enquiry</h3>
          <p style="color:var(--muted);font-size:.86rem;margin-bottom:20px">Fill in your details and we&rsquo;ll reply by WhatsApp, usually within the hour.</p>
          <div id="pcFormWrap">
            <form id="pcForm" onsubmit="submitContactForm(event,'pc')">
              <div class="form-field">
                <label for="pcName">Full name</label>
                <input type="text" id="pcName" required placeholder="Your name">
              </div>
              <div class="form-field">
                <label for="pcPhone">Phone number</label>
                <input type="tel" id="pcPhone" required placeholder="04xx xxx xxx">
              </div>
              <div class="form-field">
                <label for="pcInterest">I&rsquo;m interested in</label>
                <select id="pcInterest">
                  <option>Single Lesson</option>
                  <option>5-Lesson Pass</option>
                  <option>Express Test Package</option>
                  <option>Ultimate Test Pass Pack</option>
                  <option>Gift Voucher</option>
                  <option>General enquiry</option>
                </select>
              </div>
              <div class="form-field">
                <label for="pcMessage">Message (optional)</label>
                <textarea id="pcMessage" rows="4" placeholder="Tell us a bit about what you need"></textarea>
              </div>
              <button type="submit" class="btn btn-red btn-block">Send Enquiry</button>
              <p class="form-note">Prefer WhatsApp? <a href="https://wa.me/61404119119" target="_blank" rel="noopener" style="color:var(--red);font-weight:700">Chat with us instantly &rarr;</a></p>
            </form>
          </div>
          <div class="form-success" id="pcFormSuccess">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm-1.2 14.4l-4.2-4.2 1.4-1.4 2.8 2.8 6-6 1.4 1.4z"/></svg>
            <h3 style="color:var(--navy);margin-bottom:8px">Thanks, we&rsquo;ll be in touch!</h3>
            <p style="color:var(--muted);font-size:.88rem">For a faster response, message us directly on <a href="https://wa.me/61404119119" target="_blank" rel="noopener" style="color:var(--red);font-weight:700">WhatsApp</a>.</p>
          </div>
        </div>
      </div>
    </div>
  </section>''',
])

contact_html = page_shell(
    title="Contact Transformers Driving School | Book a Lesson",
    description="Contact Transformers Driving School by WhatsApp, phone, or send an online enquiry. VicRoads ADI accredited driving lessons serving Pakenham and surrounding suburbs.",
    depth=0,
    body_content=CONTACT_BODY,
    page_key="contact-us",
    breadcrumbs=[("Contact", None)],
)
open(os.path.join(OUT, "contact-us.html"), "w").write(contact_html)
print("contact-us.html written:", len(contact_html), "bytes")

# ============================================================
# GENERATE ALL COUNTRY-SPECIFIC PAGES
# ============================================================
for c in COUNTRIES:
    country_page(c)

# ============================================================
# AREA / SUBURB LANDING PAGES
# ============================================================
def suburb_page(suburb):
    slug = slugify(suburb)
    centre_name, centre_href = SUBURB_TEST_CENTRE[suburb]
    nearest20 = nearest_n_suburbs(suburb, 20)
    wikidata = SUBURB_WIKIDATA.get(suburb)
    lat, lon = SUBURB_COORDS[suburb]
    map_query = suburb.replace(" ", "+") + "+VIC+Australia"

    is_own_centre = (suburb == centre_name)
    centre_line = (
        "VicRoads {c} is right here in {s}, so it&rsquo;s the natural test centre for local learners.".format(c=centre_name, s=suburb)
        if is_own_centre else
        "The nearest VicRoads drive test centre to {s} is <a href=\"{href}\">VicRoads {c}</a>. Our instructors prepare {s} learners specifically for that centre's local test roads.".format(s=suburb, href=centre_href, c=centre_name)
    )

    hero = '''<section class="page-hero">
    <div class="container">
      <h1>Driving School {suburb}</h1>
      <p>Local, VicRoads ADI accredited driving lessons for {suburb} learners, with pickup included and test preparation for your nearest VicRoads test centre.</p>
      {byline}
    </div>
  </section>'''.format(suburb=suburb, byline=BYLINE)

    intro = '''<section class="block">
    <div class="container" style="max-width:800px">
      <p style="font-size:1rem;color:#334155">Looking for a <strong>driving school {suburb}</strong> learners actually recommend? Transformers Driving School provides <strong>driving lessons {suburb}</strong> residents can book with flexible, VicRoads ADI accredited instructors, with pickup and drop-off from home, school or work, so you don&rsquo;t need to travel to us.</p>
    </div>
  </section>'''.format(suburb=suburb)

    centre_card = '''<section class="block block-alt">
    <div class="container">
      <div class="info-grid">
        <div class="info-card">
          <h2><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg>Nearest VicRoads Test Centre</h2>
          <p style="font-size:.9rem;color:#334155">{centre_line}</p>
          <div style="margin-top:14px"><a href="{href}" class="tool-link">View the full {c} test centre guide &rarr;</a></div>
        </div>
        <div class="info-card">
          <h3 style="margin-bottom:10px">Passing Your Test: {suburb} Tips</h3>
          <ul class="bullet-list">
            <li>Practise on the local {suburb} roads you&rsquo;ll actually be tested near, not just quiet side streets.</li>
            <li>Do a full pre-drive safety check every lesson so it becomes automatic on test day.</li>
            <li>Book your lesson in the same time slot as your test to get used to that traffic pattern.</li>
            <li>Take our free <a href="readiness-quiz.html">Test Readiness Quiz</a> to target your weak spots before booking a test.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>'''.format(centre_line=centre_line, href=centre_href, c=centre_name, suburb=suburb)

    map_section = '''<section class="block">
    <div class="container">
      <div class="section-title"><h2>{suburb} Service Area</h2><p>We provide driving lessons throughout {suburb} and surrounding suburbs, with pickup included.</p></div>
      <div class="map-embed" style="border-radius:12px;overflow:hidden;box-shadow:0 6px 20px rgba(15,23,42,.1)">
        <iframe src="https://www.google.com/maps?q={q}&output=embed" width="100%" height="360" style="border:0;display:block" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{suburb} service area map"></iframe>
      </div>
    </div>
  </section>'''.format(suburb=suburb, q=map_query)

    faq_extra = [
        ("Do you offer driving lessons in {suburb}?".format(suburb=suburb),
         "Yes, {suburb} is one of our core service areas. We offer flexible driving lessons {suburb} learners can book online or via WhatsApp, with pickup and drop-off included.".format(suburb=suburb)),
        ("Which VicRoads test centre will I be tested at from {suburb}?".format(suburb=suburb),
         centre_line),
        ("How much do driving lessons cost in {suburb}?".format(suburb=suburb),
         "Pricing is the same across all our service areas including {suburb}. See our Lessons &amp; Test Packages on the homepage, from a Single Lesson through to the Ultimate Test Pass Pack, and message us on WhatsApp for current availability.".format(suburb=suburb)),
    ]
    nap_faq = nap_faq_section(suburb, extra_faqs=faq_extra)

    # No confirmed public storefront address exists for Transformers Driving
    # School, so this schema is a service-area business: no "address"/
    # streetAddress field is included (unlike the old XDS repo-address reuse),
    # and no aggregateRating is fabricated since there is no real review data
    # for this brand yet.
    area_served_json = ", ".join('"{0}"'.format(n) for n in nearest20)
    sameas = ['"https://au.linkedin.com/in/sol-pakzad-b36761170"', '"https://www.facebook.com/share/1HmPRyNByw/"', '"https://www.facebook.com/transformersdrivingschool/"']
    if wikidata:
        sameas.append('"https://www.wikidata.org/wiki/{0}"'.format(wikidata))
    local_schema = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "DrivingSchool",
  "name": "Transformers Driving School",
  "telephone": "+61404119119",
  "url": "https://transformersdrivingschool.com.au/{href}",
  "areaServed": {{
    "@type": "GeoCircle",
    "geoMidpoint": {{
      "@type": "GeoCoordinates",
      "latitude": {lat},
      "longitude": {lon}
    }}
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": {lat},
    "longitude": {lon}
  }},
  "description": "Driving lessons and VicRoads test preparation in {suburb}, servicing nearby Casey/Cardinia growth-corridor suburbs. Service-area business with no public storefront.",
  "keywords": "driving school {suburb}, driving lessons {suburb}, {suburb} driving instructor, VicRoads test preparation {suburb}",
  "sameAs": [{sameas}]
}}
</script>
'''.format(href=area_page_href(suburb), lat=lat, lon=lon, suburb=suburb, sameas=", ".join(sameas))

    body = '\n  '.join([hero, trust_section_html(), intro, centre_card, map_section, nap_faq, TOOLS_LINKS_SECTION])

    html = page_shell(
        title="Driving School {suburb} | VicRoads Test Prep".format(suburb=suburb),
        description="Driving lessons in {suburb} with pickup included, from a VicRoads ADI accredited instructor. Book on WhatsApp for your nearest test centre.".format(suburb=suburb),
        depth=0,
        body_content=body,
        page_key="area-" + slug,
        schema=local_schema,
        breadcrumbs=[("Areas We Serve", "index.html#areas"), (suburb, None)],
    )
    fname = area_page_href(suburb)
    open(os.path.join(OUT, fname), "w").write(html)
    print(fname, "written:", len(html), "bytes")


for s in AREA_SUBURBS:
    suburb_page(s)
