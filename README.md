# Ever.Life

**Live longer. Leave more.** A free longevity and legacy-planning hub. It includes:
- Interactive calculators and expert-style guides
- A video library and multi-step lead generation
- Support/donation tiers, contests, careers and advertiser pages

Static site, 100% compatible with GitHub Pages (free plan).

## Structure
```
index.html              Home
get-matched.html        Multi-step lead-generation funnel
tools/                  Life expectancy, biological age, life insurance (DIME), legacy checklist
guides/                 10 long-form guides + index
videos.html             Video library (click-to-load YouTube)
support.html            Donations / sponsorship tiers
contests.html           Contests & prizes + official rules
careers.html            Roles + application form
advertise.html          Advertising, sponsorship, lead-partner inquiries
about / contact / editorial-policy / privacy-policy / cookie-policy / terms / disclaimer
assets/css, assets/js   Styles, site script (forms, theme, ads), tools script
content/guides          Article sources (HTML fragments with META header)
build/                  Python generator (python3 build/build.py)
ads.txt, sitemap.xml, robots.txt, .nojekyll
```

## Edit and rebuild
Edit `build/*.py` or `content/guides/*.html`, then run `python3 build/build.py`.

## Settings (assets/js/main.js → CONFIG)
- `adSlots`: paste AdSense ad-unit slot IDs (top, inArticle, sidebar, mid) once approved. Auto ads work without them.
- `payLinks`: add Stripe/PayPal/BMC links to enable one-click donations.
- Forms: delivered via FormSubmit.
  - The very first submission sends a one-time activation email to the site inbox. Click "Activate" once.
  - The inbox address is encoded and never shown on the site.

## Custom domain (ever.life)
1. DNS:
   - A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - CNAME `www` → `webworksa1.github.io`
2. Repo → Settings → Pages → Custom domain: `ever.life` → Enforce HTTPS.
3. Google Search Console: submit `https://ever.life/sitemap.xml`. Then apply for AdSense with ever.life.

See `BUILD-PROMPT.md` for the full phase-wise build prompt and research.
