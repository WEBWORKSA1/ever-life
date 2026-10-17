"""Shared layout for Ever.Life static pages."""
import json

SITE = "https://ever.life"
NAME = "Ever.Life"
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
CONTACT_URL = "https://web.works/contact"

ICONS = {
    "pulse": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l3-8 4 16 3-8h4"/></svg>',
    "hourglass": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2h12M6 22h12M7 2v4a5 5 0 0 0 10 0V2M7 22v-4a5 5 0 0 1 10 0v4"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6z"/><path d="M9 12l2 2 4-4"/></svg>',
    "list": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13C4 7 9 3 20 3c0 11-4 17-9 17z"/><path d="M4 21c4-6 8-9 12-11"/></svg>',
    "moon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    "run": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="14" cy="4" r="2"/><path d="M6 21l3-6 3 2v5M9 11l3-3 3 3 3 1M8 8l4-1"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h6"/></svg>',
    "key": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3L21 2M16 7l3 3M18 5l2 2"/></svg>',
    "trophy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M17 5h3v2a3 3 0 0 1-3 3M7 5H4v2a3 3 0 0 0 3 3"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0M16 3.1a4 4 0 0 1 0 7.8M22 21a7 7 0 0 0-4-6.3"/></svg>',
    "mega": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11v2a1 1 0 0 0 1 1h3l5 4V6L7 10H4a1 1 0 0 0-1 1zM16 8a5 5 0 0 1 0 8M19 5a9 9 0 0 1 0 14"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12v10H4V12M2 7h20v5H2zM12 22V7M12 7H7.5a2.5 2.5 0 1 1 0-5C11 2 12 7 12 7zM12 7h4.5a2.5 2.5 0 1 0 0-5C13 2 12 7 12 7z"/></svg>',
    "brain": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 3 3h0a3 3 0 0 0 3-3V6a3 3 0 0 0-3-3zM15 3a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-3 3h0a3 3 0 0 1-3-3"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>',
    "play": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="3"/><path d="M10 9l5 3-5 3z"/></svg>',
}

LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="18" fill="none" stroke="var(--brand)" stroke-width="2.4"/>'
        '<circle cx="20" cy="20" r="12.5" fill="none" stroke="var(--brand)" stroke-width="2" opacity=".7"/>'
        '<circle cx="20" cy="20" r="7" fill="none" stroke="var(--gold)" stroke-width="2"/><circle cx="20" cy="20" r="2.4" fill="var(--gold)"/></svg>')

NAV = [("Tools", "tools/"), ("Guides", "guides/"), ("Videos", "videos.html"), ("Community", "contests.html"), ("Support", "support.html")]


def honeypot():
    return '<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'


def newsletter_form(r, source="Footer"):
    return f'''<form class="newsletter" data-form="Newsletter" data-success="You're in. Watch your inbox for the next Ever.Life briefing.">
  {honeypot()}<input type="hidden" name="Form" value="Newsletter ({source})">
  <label class="sr-only" for="nl-{source}">Email address</label>
  <input id="nl-{source}" type="email" name="email" placeholder="you@example.com" required>
  <button class="btn btn-primary" type="submit">Subscribe</button>
  <div class="form-status" role="status" style="flex-basis:100%"></div>
</form>'''


def ad(slot):
    return f'<div class="ad-slot" data-slot="{slot}"></div>'


def page(path, title, description, body, active="", head_extra="", scripts=(), schema=None, og_type="website", noindex=False):
    depth = path.count("/")
    r = "../" * depth
    url_path = path[:-10] if path.endswith("index.html") else path
    canonical = f"{SITE}/{url_path}"
    full_title = title if NAME in title else f"{title} | {NAME}"
    nav_links = "".join(
        f'<a href="{r}{href}"{' aria-current="page"' if active == label else ""}>{label}</a>' for label, href in NAV)
    mobile = "".join(f'<a href="{r}{href}">{label}</a>' for label, href in NAV)
    ld = ""
    base_ld = [{
        "@context": "https://schema.org", "@type": "Organization", "name": NAME, "url": SITE + "/",
        "logo": SITE + "/assets/img/logo.svg", "description": "Independent longevity and legacy-planning resource."
    }]
    if schema:
        base_ld.extend(schema if isinstance(schema, list) else [schema])
    for s in base_ld:
        ld += f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
    extra_js = "".join(f'<script src="{r}{s}" defer></script>' for s in scripts)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/og.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1f5c46">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<link rel="icon" href="{r}assets/img/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/style.css">
{ADSENSE}
{ld}{head_extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar">Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership: <a href="{CONTACT_URL}" target="_blank" rel="noopener">web.works/contact</a></div>
<header class="site-header">
  <div class="container nav">
    <a class="logo" href="{r}index.html" aria-label="Ever.Life home">{LOGO}<span>Ever<span class="dot">.</span>Life</span></a>
    <nav class="nav-links" aria-label="Primary">{nav_links}</nav>
    <div class="nav-cta">
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Toggle dark mode">{ICONS["moon"]}</button>
      <a class="btn btn-gold btn-sm" href="{r}get-matched.html">Get Matched</a>
      <button class="icon-btn menu-btn" type="button" data-menu-toggle aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
  <div class="mobile-menu" id="mobile-menu">{mobile}<a href="{r}get-matched.html">Get Matched with an Advisor</a><a href="{r}advertise.html">Advertise &amp; Partner</a><a href="{r}careers.html">Careers</a><a href="{r}contact.html">Contact</a></div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div>
        <a class="logo" href="{r}index.html">{LOGO}<span>Ever<span class="dot">.</span>Life</span></a>
        <p class="muted mt-2">Live longer. Live better. Protect what lasts. Free, independent tools and guides on healthy longevity and legacy planning.</p>
        <h4 class="mt-2">The weekly longevity briefing</h4>
        {newsletter_form(r)}
      </div>
      <div><h4>Explore</h4><ul>
        <li><a href="{r}tools/life-expectancy-calculator.html">Life Expectancy Calculator</a></li>
        <li><a href="{r}tools/biological-age-test.html">Biological Age Test</a></li>
        <li><a href="{r}tools/life-insurance-calculator.html">Life Insurance Calculator</a></li>
        <li><a href="{r}tools/legacy-checklist.html">Legacy Checklist</a></li>
        <li><a href="{r}guides/">All Guides</a></li>
        <li><a href="{r}videos.html">Video Library</a></li>
      </ul></div>
      <div><h4>Get involved</h4><ul>
        <li><a href="{r}get-matched.html">Get Matched with an Advisor</a></li>
        <li><a href="{r}support.html">Support Ever.Life</a></li>
        <li><a href="{r}contests.html">Contests &amp; Prizes</a></li>
        <li><a href="{r}careers.html">Careers &amp; Contributors</a></li>
        <li><a href="{r}advertise.html">Advertise &amp; Partner</a></li>
        <li><a href="{CONTACT_URL}" target="_blank" rel="noopener">Buy / Sponsor this domain</a></li>
      </ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="{r}about.html">About</a></li>
        <li><a href="{r}editorial-policy.html">Editorial Policy</a></li>
        <li><a href="{r}contact.html">Contact</a></li>
        <li><a href="{r}privacy-policy.html">Privacy Policy</a></li>
        <li><a href="{r}cookie-policy.html">Cookie Policy</a></li>
        <li><a href="{r}terms.html">Terms of Use</a></li>
        <li><a href="{r}disclaimer.html">Disclaimer &amp; Trademark Notice</a></li>
      </ul></div>
    </div>
    <div class="legal-strip">
      <p><strong>Medical &amp; financial disclaimer:</strong> Ever.Life publishes general educational information. It is not medical, financial, insurance, tax or legal advice. Always consult a qualified professional about your situation.</p>
      <p><strong>Trademark notice:</strong> Ever.Life is an independent publication. It is not affiliated with, endorsed by, sponsored by or connected to any company, product, service or registered trademark using the name "EverLife", "Everlife", "Ever Life" or any similar name. All third-party names, logos and trademarks belong to their respective owners and are used for identification only.</p>
      <p>&copy; <span data-year>2026</span> Ever.Life. All rights reserved. Original content, design and tools &copy; Ever.Life; reproduction without permission is prohibited.</p>
    </div>
  </div>
</footer>
<div class="cookie" id="cookie" role="dialog" aria-live="polite" aria-label="Cookie notice">
  <strong>Cookies on Ever.Life</strong>
  <p class="mt-0" style="margin:6px 0 0">We and our advertising partners, including Google, use cookies to deliver and measure ads and to improve the site. See our <a href="{r}cookie-policy.html">Cookie Policy</a> and <a href="{r}privacy-policy.html">Privacy Policy</a>.</p>
  <div class="btns"><button class="btn btn-primary btn-sm" data-cookie="all">Accept</button><button class="btn btn-ghost btn-sm" data-cookie="essential">Essential only</button></div>
</div>
<div class="toast" id="toast" role="status"></div>
<script src="{r}assets/js/main.js" defer></script>{extra_js}
</body>
</html>
'''


def hero(title, sub, crumbs=None, r="", eyebrow=None):
    c = ""
    if crumbs:
        c = '<nav class="crumbs" aria-label="Breadcrumb"><a href="' + r + 'index.html">Home</a>' + "".join(
            f' / <a href="{r}{h}">{t}</a>' if h else f" / <span>{t}</span>" for t, h in crumbs) + "</nav>"
    e = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    return f'<section class="page-hero"><div class="container">{c}{e}<h1 style="margin-top:12px">{title}</h1><p>{sub}</p></div></section>'


def status():
    return '<div class="form-status" role="status"></div>'
