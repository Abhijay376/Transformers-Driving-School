import os

OUT = "/home/claude/transformers-site"
PAGES_OUT = os.path.join(OUT, "pages")
os.makedirs(PAGES_OUT, exist_ok=True)

NAV_ITEMS = [
    ("home", "index.html", "Home"),
    ("drive-test-pakenham", "drive-test-pakenham.html", "Drive Test Pakenham"),
    ("readiness-quiz", "readiness-quiz.html", "Readiness Quiz"),
    ("licence-checker", "licence-checker.html", "Licence Checker"),
    ("contact-us", "contact-us.html", "Contact"),
]

# Areas We Serve dropdown, filled in by build_pages.py via set_area_nav_items()
# before header_html()/page_shell() are called for area pages, so the dropdown
# lists every suburb landing page. List of (page_key, href, label) tuples.
AREA_NAV_ITEMS = []

def set_area_nav_items(items):
    global AREA_NAV_ITEMS
    AREA_NAV_ITEMS = items

def asset_prefix(depth):
    return "../" * depth

def nav_links_html(depth):
    prefix = asset_prefix(depth)
    items = []
    for key, href, label in NAV_ITEMS:
        items.append('<a href="{p}{href}" data-page="{key}">{label}</a>'.format(p=prefix, href=href, key=key, label=label))
    links_html = "\n      ".join(items)

    if AREA_NAV_ITEMS:
        dd_links = "\n          ".join(
            '<a href="{p}{href}" data-page="{key}">{label}</a>'.format(p=prefix, href=href, key=key, label=label)
            for key, href, label in AREA_NAV_ITEMS
        )
        dropdown = '''<div class="nav-dropdown">
        <button class="nav-dropdown-toggle" type="button" onclick="toggleAreaDropdown(this)">Areas We Serve
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
        </button>
        <div class="nav-dropdown-menu">
          {links}
        </div>
      </div>'''.format(links=dd_links)
        links_html = links_html + "\n      " + dropdown
    return links_html

def breadcrumb_html(trail, depth):
    """trail: list of (label, href_or_None) tuples, href relative to site root
    (e.g. 'index.html', 'drive-test-frankston.html'); href=None for current page.
    Always render 'Home' as the implicit first crumb unless already present."""
    if not trail:
        return ""
    prefix = asset_prefix(depth)
    if trail[0][0] != "Home":
        trail = [("Home", "index.html")] + list(trail)

    crumb_parts = []
    ld_items = []
    for i, (label, href) in enumerate(trail):
        if href:
            crumb_parts.append('<a href="{p}{href}">{label}</a>'.format(p=prefix, href=href, label=label))
        else:
            crumb_parts.append('<span aria-current="page">{label}</span>'.format(label=label))
        ld_items.append('''{{
      "@type": "ListItem",
      "position": {pos},
      "name": "{label}",
      "item": "https://transformersdrivingschool.com.au/{href}"
    }}'''.format(pos=i + 1, label=label, href=(href or "")))

    visible = '<nav class="crumb-bar" aria-label="Breadcrumb"><div class="container breadcrumb">' + \
        ' <span class="crumb-sep">/</span> '.join(crumb_parts) + '</div></nav>'

    schema = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [{items}]
}}
</script>
'''.format(items=",".join(ld_items))

    return visible + "\n" + schema


def sidebar_html(depth):
    """Sidebar linking to the 4 VicRoads drive test centre pages and the
    'driving instructor' service-area pages (the 11 suburb 'Areas We Serve'
    landing pages). Country licence-conversion pages are treated as tool
    pages, not instructor service pages, so they are intentionally excluded
    here -- see build log for this call."""
    prefix = asset_prefix(depth)
    centre_items = "\n        ".join(
        '<li><a href="{p}{href}" data-page="{key}">{label}</a></li>'.format(p=prefix, href=href, key=key, label=label)
        for key, href, label in NAV_ITEMS if key.startswith("drive-test-")
    )
    area_items = "\n        ".join(
        '<li><a href="{p}{href}" data-page="{key}">{label}</a></li>'.format(p=prefix, href=href, key=key, label=label)
        for key, href, label in AREA_NAV_ITEMS
    )
    return '''<aside class="page-sidebar">
    <div class="sidebar-box">
      <h3>VicRoads Drive Test Centre</h3>
      <ul class="sidebar-links">
        {centres}
      </ul>
    </div>
    <div class="sidebar-box">
      <h3>Driving Instructor Areas We Serve</h3>
      <ul class="sidebar-links">
        {areas}
      </ul>
    </div>
    <div class="sidebar-box sidebar-cta">
      <p>Ready to book a lesson?</p>
      <a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I''d%20like%20to%20book%20a%20driving%20lesson.">Chat on WhatsApp</a>
    </div>
  </aside>'''.replace("''", "'").format(centres=centre_items, areas=area_items)


def header_html(depth):
    prefix = asset_prefix(depth)
    return '''<header class="site-header">
  <div class="header-row container">
    <a href="{p}index.html" class="brand">
      <img src="{p}logo.png" alt="Transformers Driving School" class="logo-img">
      <span class="brand-text">
        <span class="brand-tagline">VicRoads Test Specialists</span>
      </span>
    </a>
    <div class="header-actions">
      <a href="tel:0404119119" class="phone-link">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
        <span class="phone-link-text">0404 119 119</span>
      </a>
      <a class="btn btn-wa" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I'd%20like%20to%20know%20more%20about%20driving%20lessons.">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm5.8 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.1.1-1.8-.1-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.8-2.2 1-2.5c.3-.3.6-.4.8-.4h.6c.2 0 .5 0 .7.5.3.7.9 2.2 1 2.4.1.2.1.4 0 .6-.1.2-.2.3-.4.5l-.5.6c-.2.2-.3.4-.1.7.2.3.9 1.5 1.9 2.4 1.3 1.2 2.4 1.5 2.7 1.7.3.2.5.1.7-.1l.9-1c.2-.3.5-.2.8-.1.3.1 2 1 2.3 1.1.3.2.5.2.6.3.1.2.1.9-.1 1.6z"/></svg>
        <span class="btn-label">WhatsApp</span>
      </a>
      <button class="btn btn-red" onclick="openContactModal()">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 4h16a1 1 0 011 1v14a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1zm1 2v.6l7 4.7 7-4.7V6H5zm14 2.3l-6.5 4.3a1 1 0 01-1 0L5 8.3V18h14V8.3z"/></svg>
        <span class="btn-label">Contact Us</span>
      </button>
    </div>
  </div>
  <nav class="main-nav">
    <div class="container">
      <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
        Menu
      </button>
      <div class="nav-links" id="navLinks">
        {links}
      </div>
    </div>
  </nav>
</header>'''.format(p=prefix, links=nav_links_html(depth))

def trust_section_html():
    return '''<section class="trust-section">
  <div class="container">
    <span class="item"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>10+ Years Experience</span>
    <span class="item"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Test-Day Car Options</span>
    <span class="item"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Flexible Instructor Options</span>
    <span class="item"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>VicRoads ADI Accredited Instructors</span>
  </div>
</section>'''

def footer_html(depth):
    prefix = asset_prefix(depth)
    return '''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="brand" style="margin-bottom:12px">
          <span class="footer-logo-wrap"><img src="{p}logo.png" alt="Transformers Driving School" class="logo-img"></span>
        </div>
        <p style="max-width:280px">VicRoads ADI accredited driving instructors serving Pakenham, Officer, Berwick, Cranbourne and surrounding Casey &amp; Cardinia growth corridor suburbs.</p>
      </div>
      <div>
        <h4>Quick Links</h4>
        <ul>
          <li><a href="{p}index.html">Home</a></li>
          <li><a href="{p}index.html#packages">Packages</a></li>
          <li><a href="{p}readiness-quiz.html">Readiness Quiz</a></li>
          <li><a href="{p}licence-checker.html">Licence Checker</a></li>
        </ul>
      </div>
      <div>
        <h4>Test Centre</h4>
        <ul>
          <li><a href="{p}drive-test-pakenham.html">Drive Test Pakenham</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:0404119119">0404 119 119</a></li>
          <li><a href="https://wa.me/61404119119" target="_blank" rel="noopener">WhatsApp Us</a></li>
          <li><a href="{p}contact-us.html">Contact Page</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Transformers Driving School. All rights reserved.</span>
      <span>|</span>
      <span>0404 119 119</span>
      <span>|</span>
      <span class="tagline">Drive Your Way Forward!</span>
    </div>
  </div>
</footer>'''.format(p=prefix)

WA_FLOAT = '''<a class="wa-float" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I'd%20like%20to%20know%20more%20about%20driving%20lessons." aria-label="Chat on WhatsApp">
  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm5.8 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.1.1-1.8-.1-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.8-2.2 1-2.5c.3-.3.6-.4.8-.4h.6c.2 0 .5 0 .7.5.3.7.9 2.2 1 2.4.1.2.1.4 0 .6-.1.2-.2.3-.4.5l-.5.6c-.2.2-.3.4-.1.7.2.3.9 1.5 1.9 2.4 1.3 1.2 2.4 1.5 2.7 1.7.3.2.5.1.7-.1l.9-1c.2-.3.5-.2.8-.1.3.1 2 1 2.3 1.1.3.2.5.2.6.3.1.2.1.9-.1 1.6z"/></svg>
</a>'''

MODAL = '''<div class="modal-overlay" id="contactModal" hidden>
  <div class="modal-box">
    <button class="modal-close" onclick="closeContactModal()" aria-label="Close">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
    </button>
    <div id="cfFormWrap">
      <h3>Quick Enquiry</h3>
      <p class="sub">Fill in your details and we'll reply by WhatsApp, usually within the hour. For opening hours and more contact options, visit our full <a href="__CONTACT_HREF__" style="color:var(--red);font-weight:700">Contact page</a>.</p>
      <form id="cfForm" onsubmit="submitContactForm(event,'cf')">
        <div class="form-field">
          <label for="cfName">Full name</label>
          <input type="text" id="cfName" required placeholder="Your name">
        </div>
        <div class="form-field">
          <label for="cfPhone">Phone number</label>
          <input type="tel" id="cfPhone" required placeholder="04xx xxx xxx">
        </div>
        <div class="form-field">
          <label for="cfInterest">I'm interested in</label>
          <select id="cfInterest">
            <option>Single Lesson</option>
            <option>5-Lesson Pass</option>
            <option>Express Test Package</option>
            <option>Ultimate Test Pass Pack</option>
            <option>Gift Voucher</option>
            <option>General enquiry</option>
          </select>
        </div>
        <div class="form-field">
          <label for="cfMessage">Message (optional)</label>
          <textarea id="cfMessage" rows="3" placeholder="Tell us a bit about what you need"></textarea>
        </div>
        <button type="submit" class="btn btn-red btn-block">Send Enquiry</button>
        <p class="form-note">Prefer WhatsApp? <a href="https://wa.me/61404119119" target="_blank" rel="noopener" style="color:var(--red);font-weight:700">Chat with us instantly &rarr;</a></p>
      </form>
    </div>
    <div class="form-success" id="cfFormSuccess">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm-1.2 14.4l-4.2-4.2 1.4-1.4 2.8 2.8 6-6 1.4 1.4z"/></svg>
      <h3 style="color:var(--navy);margin-bottom:8px">Thanks, we'll be in touch!</h3>
      <p style="color:var(--muted);font-size:.88rem">For a faster response, message us directly on <a href="https://wa.me/61404119119" target="_blank" rel="noopener" style="color:var(--red);font-weight:700">WhatsApp</a>.</p>
    </div>
  </div>
</div>'''

GA4_SNIPPET = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YBVP7W4B3Y"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-YBVP7W4B3Y');
</script>
'''

SEARCH_CONSOLE_META = '<meta name="google-site-verification" content="PASTE_YOUR_VERIFICATION_CODE_HERE">\n'

FAVICON_LINKS = '''<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{p}favicon-32.png">
<link rel="icon" type="image/png" sizes="180x180" href="{p}favicon-180.png">
<link rel="apple-touch-icon" sizes="180x180" href="{p}apple-touch-icon.png">
'''

def fb_reviews_banner_html():
    """Slim sitewide Facebook reviews banner. Full detailed reviews section
    with review cards stays homepage-only (REVIEWS_SECTION in build_pages.py)."""
    return '''<a class="fb-reviews-banner" target="_blank" rel="noopener" href="https://www.facebook.com/transformersdrivingschool/reviews">
  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1.5 8h1.8v2.2h-1.8V21h-2.4v-8.8H9.7V10h1.4V8.7c0-1.9 1-3 3.2-3h1.8v2.2h-1.2c-.6 0-1.4.2-1.4 1V10z"/></svg>
  <span><strong>&#9733; 100% Recommended</strong> &middot; 59 Reviews on Facebook</span>
  <span class="fb-reviews-banner-cta">See Reviews &rarr;</span>
</a>'''

def page_shell(title, description, depth, body_content, page_key, extra_head="", schema="",
               breadcrumbs=None, show_sidebar=True):
    prefix = asset_prefix(depth)
    modal = MODAL.replace("__CONTACT_HREF__", prefix + "contact-us.html")
    crumbs = breadcrumb_html(breadcrumbs, depth)
    fb_banner = fb_reviews_banner_html()

    if show_sidebar:
        body = '<div class="page-layout container">\n<div class="page-main">\n{main}\n</div>\n{sidebar}\n</div>'.format(
            main=body_content, sidebar=sidebar_html(depth))
    else:
        body = body_content

    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
{search_console}{ga4}{favicon}<link rel="stylesheet" href="{p}site.css">
{extra_head}{schema}</head>
<body data-page="{page_key}">
{header}
{fb_banner}
{crumbs}
{body}
{footer}
{wa_float}
{modal}
<script src="{p}site.js"></script>
</body>
</html>
'''.format(title=title, description=description, p=prefix, extra_head=extra_head, schema=schema,
           search_console=SEARCH_CONSOLE_META, ga4=GA4_SNIPPET, favicon=FAVICON_LINKS.format(p=prefix),
           page_key=page_key, header=header_html(depth), fb_banner=fb_banner, crumbs=crumbs, body=body,
           footer=footer_html(depth), wa_float=WA_FLOAT, modal=modal)

print("helpers loaded")
