"""Build the Ever.Life static site. Run: python3 build/build.py"""
import json, os, re, html
from layout import page, hero, ICONS, ad, honeypot, status, newsletter_form, CONTACT_URL, SITE
import tools_pages as T

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    OUT.append(path)


VIDEOS = [
    ("ff40YiMmVkU", "How to live to be 100+", "Dan Buettner · TED-Ed", "longevity", "What the world's longest-lived communities share."),
    ("8KkKuTCFvzI", "What makes a good life? Lessons from the longest study on happiness", "Robert Waldinger · TED", "mind", "Eight decades of data point to relationships."),
    ("5MuIMqhT8DM", "Sleep is your superpower", "Matt Walker · TED", "sleep", "Why sleep is a non-negotiable biological necessity."),
    ("BHY0FxzoKZE", "The brain-changing benefits of exercise", "Wendy Suzuki · TED", "fitness", "How movement protects mood, memory and the ageing brain."),
    ("2wseM6wWd74", "The science of cells that never get old", "Elizabeth Blackburn · TED", "science", "Telomeres, stress and how cells age."),
]


def video_card(v, r):
    vid, title, by, cat, desc = v
    return f'''<article class="card reveal" data-cat="{cat}" style="padding:14px"><div class="video" data-yt="{vid}" data-title="{html.escape(title)}"></div>
<div style="padding:12px 6px 4px"><span class="tag">{cat}</span><h3 style="font-size:1.08rem">{title}</h3><p class="muted" style="font-size:.9rem;margin:0">{by} · {desc}</p></div></article>'''


# ---------------- Guides ----------------
def load_guides():
    gdir = os.path.join(ROOT, "content", "guides")
    guides = []
    for fn in sorted(os.listdir(gdir)):
        if not fn.endswith(".html"):
            continue
        raw = open(os.path.join(gdir, fn), encoding="utf-8").read()
        m = re.match(r"\s*<!--META\s*(\{.*?\})\s*-->", raw, re.S)
        meta = json.loads(m.group(1))
        body = raw[m.end():].strip()
        body = body.replace("https://adventisthealthstudy.org/", "https://llu.edu/")
        meta["slug"] = fn[:-5]
        meta["body"] = body
        guides.append(meta)
    order = ["how-to-live-to-100-blue-zones", "healthspan-vs-lifespan", "how-much-life-insurance-do-i-need", "exercise-for-longevity",
             "estate-planning-basics", "sleep-and-longevity", "term-vs-whole-life-insurance", "nutrition-for-longevity",
             "longevity-biomarkers-tests", "digital-legacy-planning"]
    guides.sort(key=lambda g: order.index(g["slug"]) if g["slug"] in order else 99)
    return guides


def guide_card(g, r):
    return f'''<a class="card reveal" href="{r}guides/{g["slug"]}.html" data-cat="{g["category"].lower()}"><span class="tag">{g["category"]}</span>
<h3>{g["title"]}</h3><p>{g.get("excerpt", g["description"])}</p><span class="more">{g.get("readTime", 8)} min read →</span></a>'''


def build_guides(guides):
    r = "../"
    for g in guides:
        body = g["body"]
        legacy = g["category"].lower() == "legacy"
        if legacy:
            cta = f'''<div class="inline-cta"><p>Not sure what coverage or plan fits your family? Compare options from licensed pros.</p><a class="btn btn-gold btn-sm" href="{r}get-matched.html?need={"estate" if "estate" in g["slug"] or "digital" in g["slug"] else "insurance"}">Get matched free</a></div>{ad("inArticle")}'''
        else:
            cta = f'''<div class="inline-cta"><p>How do your habits add up? Get your personal estimate in 2 minutes.</p><a class="btn btn-primary btn-sm" href="{r}tools/life-expectancy-calculator.html">Try the calculator</a></div>{ad("inArticle")}'''
        body = body.replace("<!--CTA-->", cta, 1) if "<!--CTA-->" in body else body + cta
        heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
        toc = "".join(f'<li><a href="#{i}">{re.sub("<.*?>", "", t)}</a></li>' for i, t in heads)
        faqs = re.findall(r"<details><summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>", body, re.S)
        related = [x for x in guides if x["slug"] != g["slug"] and x["category"] == g["category"]][:2]
        related += [x for x in guides if x["slug"] != g["slug"] and x not in related][: 3 - len(related)]
        rel_html = "".join(guide_card(x, r) for x in related)
        side_cta = (f'<div class="card"><h3 style="font-size:1.1rem">Protect what lasts</h3><p>Free quotes for life insurance and estate planning from licensed professionals.</p><a class="btn btn-gold btn-block" href="{r}get-matched.html">Get matched</a></div>'
                    if legacy else
                    f'<div class="card"><h3 style="font-size:1.1rem">How old is your body?</h3><p>Take the free 12-question biological age test.</p><a class="btn btn-primary btn-block" href="{r}tools/biological-age-test.html">Take the test</a></div>')
        content = hero(g["title"], g["description"], [("Guides", "guides/"), (g["category"], None)], r)
        content = content.replace("</p></div></section>",
                                  f'</p><div class="meta-row"><span>By the Ever.Life Editorial Team</span><span>Updated {g["date"]}</span><span>{g.get("readTime", 8)} min read</span><a href="{r}editorial-policy.html">How we research</a></div></div></section>')
        content += f'''<div class="container"><div class="article-layout">
<article class="prose">{body}</article>
<aside class="aside-stack">
  <nav class="card toc" aria-label="On this page"><h4 style="font-family:var(--font-body);font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)">On this page</h4><ol>{toc}</ol></nav>
  {side_cta}
  {ad("sidebar")}
  <div class="card"><h3 style="font-size:1.05rem">Weekly briefing</h3><p class="muted" style="font-size:.9rem">One email a week. Research, tools, no spam.</p>{newsletter_form(r, "Article")}</div>
</aside></div>
<section style="padding-bottom:40px"><h2>Keep reading</h2><div class="grid g3">{rel_html}</div></section></div>'''
        schema = [{
            "@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["description"],
            "datePublished": g["date"], "dateModified": g["date"], "author": {"@type": "Organization", "name": "Ever.Life Editorial Team"},
            "publisher": {"@type": "Organization", "name": "Ever.Life", "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/logo.svg"}},
            "mainEntityOfPage": f"{SITE}/guides/{g['slug']}.html"}]
        if faqs:
            schema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": re.sub("<.*?>", "", q), "acceptedAnswer": {"@type": "Answer", "text": re.sub("<.*?>", "", a)}} for q, a in faqs]})
        write(f"guides/{g['slug']}.html", page(f"guides/{g['slug']}.html", g["title"], g["description"], content, active="Guides", schema=schema, og_type="article"))

    cats = sorted({g["category"] for g in guides})
    pills = '<button class="pill active" data-filter="all" type="button">All</button>' + "".join(
        f'<button class="pill" data-filter="{c.lower()}" type="button">{c}</button>' for c in cats)
    body = hero("Longevity &amp; Legacy Guides", "Evidence-informed, plain-English guides on living longer and better, and on protecting the people and things you care about.", [("Guides", None)], r)
    body += f'''<section class="block"><div class="container">{ad("top")}
<div class="pill-row" data-filter-group="#guide-grid" style="margin-bottom:24px">{pills}</div>
<div class="grid g3" id="guide-grid">{"".join(guide_card(g, r) for g in guides)}</div>
<div class="cta-band reveal" style="margin-top:48px"><div><h3>Have a topic you want covered?</h3><p>Suggest a guide or pitch an article as a contributor.</p></div><div class="stack-sm"><a class="btn btn-gold btn-block" href="{r}contact.html?topic=Guide%20suggestion">Suggest a topic</a><a class="btn btn-ghost btn-block" href="{r}careers.html">Write for us</a></div></div>
</div></section>'''
    write("guides/index.html", page("guides/index.html", "Longevity & Legacy Guides", "Plain-English guides on longevity, sleep, exercise, nutrition, biomarkers, life insurance, estate planning and digital legacy.", body, active="Guides"))


# ---------------- Home ----------------
def build_home(guides):
    r = ""
    rings = "".join(f'<circle class="r" cx="200" cy="200" r="{rad}" stroke-width="{1.2 + (i % 3) * .6}" opacity="{.35 + i * .06}"/>' for i, rad in enumerate(range(186, 20, -17)))
    tools = "".join(f'<a class="card reveal" href="tools/{h}"><div class="ico">{ICONS[i]}</div><h3>{t}</h3><p>{d}</p><span class="more">Open →</span></a>' for h, i, t, d in T.TOOLS)
    pillars = [("moon", "Sleep", "7 to 9 hours, on a regular schedule.", "guides/sleep-and-longevity.html"),
               ("run", "Move", "Cardio base, strength, balance.", "guides/exercise-for-longevity.html"),
               ("leaf", "Eat", "Plant-forward, protein-aware, minimally processed.", "guides/nutrition-for-longevity.html"),
               ("heart", "Connect", "Relationships are a health habit.", "guides/how-to-live-to-100-blue-zones.html"),
               ("pulse", "Measure", "Know the numbers that matter.", "guides/longevity-biomarkers-tests.html")]
    legacy = [("shield", "Coverage", "Income your family can count on.", "guides/how-much-life-insurance-do-i-need.html"),
              ("doc", "Will & estate", "Your wishes, legally clear.", "guides/estate-planning-basics.html"),
              ("key", "Digital legacy", "Accounts, photos, passwords.", "guides/digital-legacy-planning.html")]
    pill_cards = lambda arr: "".join(f'<a class="card reveal" href="{h}" style="padding:20px"><div class="ico">{ICONS[i]}</div><h3 style="font-size:1.1rem">{t}</h3><p style="margin:0;font-size:.93rem">{d}</p></a>' for i, t, d, h in arr)
    needs = [("insurance", "Life insurance"), ("final", "Final expense"), ("estate", "Will &amp; estate"), ("retirement", "Retirement plan"), ("clinic", "Longevity testing")]
    body = f'''<section class="hero"><div class="container hero-grid">
<div>
  <span class="eyebrow">Longevity · Legacy · Free tools</span>
  <h1 style="margin-top:16px">Live longer.<br><em>Leave more.</em></h1>
  <p class="sub">Ever.Life helps you add healthy years to your life and protect what you build along the way, with free calculators, evidence-informed guides and access to licensed professionals when you need them.</p>
  <div class="hero-actions"><a class="btn btn-primary" href="tools/life-expectancy-calculator.html">Calculate my life expectancy</a><a class="btn btn-ghost" href="get-matched.html">Get matched with an advisor</a></div>
  <div class="hero-stats"><div><b>4</b><span>free interactive tools</span></div><div><b>10+</b><span>in-depth guides</span></div><div><b>0</b><span>sign-ups required</span></div></div>
</div>
<div class="rings" aria-hidden="true"><svg viewBox="0 0 400 400">{rings}<circle cx="200" cy="200" r="8" fill="var(--gold)"/></svg>
  <div class="badge b1"><span class="muted">Healthy years gained</span><b>+ up to 10</b></div>
  <div class="badge b2"><span class="muted">Legacy plan</span><b>20 steps</b></div>
</div></div></section>
{ad("top")}
<section class="block alt"><div class="container">
  <div class="section-head reveal"><span class="eyebrow">Start here</span><h2 style="margin-top:12px">Four tools. Two minutes each. Real answers.</h2><p>Private by design: every calculator runs in your browser and nothing you type is stored.</p></div>
  <div class="grid g4">{tools}</div>
</div></section>
<section class="block"><div class="container">
  <div class="grid g2" style="gap:48px;align-items:start">
    <div><div class="section-head reveal"><span class="eyebrow">Half one</span><h2 style="margin-top:12px">Longevity: add life to your years</h2><p>Five pillars account for most of the difference between ageing well and ageing early.</p></div><div class="grid g2">{pill_cards(pillars)}</div></div>
    <div><div class="section-head reveal"><span class="eyebrow">Half two</span><h2 style="margin-top:12px">Legacy: protect what lasts</h2><p>A long life is also a planned one. Three areas protect the people you love.</p></div><div class="grid" style="gap:16px">{pill_cards(legacy)}</div></div>
  </div>
</div></section>
<section class="block alt"><div class="container">
  <div class="section-head reveal"><span class="eyebrow">Guides</span><h2 style="margin-top:12px">Read the research, minus the jargon</h2></div>
  <div class="grid g3">{"".join(guide_card(g, r) for g in guides[:6])}</div>
  <p class="center mt-2"><a class="btn btn-ghost" href="guides/">All guides</a></p>
</div></section>
<section class="block" id="match"><div class="container">
  <div class="cta-band reveal">
    <div><span class="eyebrow" style="background:rgba(255,255,255,.12);color:#fff">Free · No obligation</span>
      <h2 style="margin-top:14px">Get matched with a licensed professional in 60 seconds</h2>
      <p>Life insurance, final expense coverage, wills and estate plans, retirement and longevity testing. Tell us what you need and the right specialist reaches out.</p>
      <div class="trust" style="justify-content:flex-start;color:rgba(255,255,255,.85)"><span>{ICONS["check"]} No cost to you</span><span>{ICONS["lock"]} Private &amp; secure</span><span>{ICONS["check"]} Licensed pros only</span></div></div>
    <form class="card form" data-form="Quick Lead (Home)" data-success="Thank you! A specialist will contact you shortly." style="color:var(--ink)">
      {honeypot()}<input type="hidden" name="Form" value="Quick lead - homepage">
      <div><label for="q-need">I need help with</label><select id="q-need" name="need" required>{"".join(f'<option value="{v}">{t}</option>' for v, t in needs)}</select></div>
      <div class="row two"><div><label for="q-name">First name</label><input id="q-name" name="name" required autocomplete="given-name"></div>
      <div><label for="q-email">Email</label><input id="q-email" type="email" name="email" required autocomplete="email"></div></div>
      <div><label for="q-phone">Phone (optional)</label><input id="q-phone" type="tel" name="phone" autocomplete="tel"></div>
      <label class="check"><input type="checkbox" name="consent" value="yes" required> I agree to be contacted by Ever.Life and partner professionals about my request. See the <a href="privacy-policy.html">Privacy Policy</a>.</label>
      <button class="btn btn-primary btn-block" type="submit">Get my free match</button>{status()}
    </form>
  </div>
</div></section>
<section class="block alt"><div class="container">
  <div class="section-head reveal"><span class="eyebrow">Watch</span><h2 style="margin-top:12px">The best talks on living longer</h2></div>
  <div class="grid g3">{"".join(video_card(v, r) for v in VIDEOS[:3])}</div>
  <p class="center mt-2"><a class="btn btn-ghost" href="videos.html">Full video library</a></p>
</div></section>
{ad("mid")}
<section class="block"><div class="container">
  <div class="section-head reveal"><span class="eyebrow">Community</span><h2 style="margin-top:12px">Build Ever.Life with us</h2></div>
  <div class="grid g4">
    <a class="card reveal" href="support.html"><div class="ico">{ICONS["gift"]}</div><h3>Support</h3><p>Keep the tools free and independent. Every contribution funds content, experts and prizes.</p><span class="more">Become a supporter →</span></a>
    <a class="card reveal" href="contests.html"><div class="ico">{ICONS["trophy"]}</div><h3>Contests &amp; prizes</h3><p>Join the 100-Year Life Challenge and story contests with cash and gear prizes.</p><span class="more">See contests →</span></a>
    <a class="card reveal" href="careers.html"><div class="ico">{ICONS["users"]}</div><h3>Careers</h3><p>Writers, clinicians, video creators and advisors: work with us.</p><span class="more">Open roles →</span></a>
    <a class="card reveal" href="advertise.html"><div class="ico">{ICONS["mega"]}</div><h3>Advertise &amp; partner</h3><p>Reach health-conscious adults planning their future.</p><span class="more">Media kit →</span></a>
  </div>
</div></section>
<section class="block alt"><div class="container" style="max-width:820px">
  <div class="section-head reveal center" style="margin:0 auto 24px"><h2>Questions, answered</h2></div>
  <section class="faq">
    <details><summary>Is Ever.Life free?</summary><p>Yes. Every tool and guide is free and needs no account. We are supported by advertising, reader contributions and partner professionals who pay to be introduced to people who request help.</p></details>
    <details><summary>Are the calculators accurate?</summary><p>They use published population averages and well-studied risk factors, so they are useful for understanding direction and scale. They are not personal medical or financial advice.</p></details>
    <details><summary>What happens when I request a match?</summary><p>Your request goes to our team, who connect you with a licensed professional in your region for the service you chose. There is no cost and no obligation.</p></details>
    <details><summary>Do you sell insurance or legal services?</summary><p>No. Ever.Life is an independent publisher. We are not an insurer, agent, broker, law firm or medical provider.</p></details>
    <details><summary>Is Ever.Life connected to any company called EverLife?</summary><p>No. Ever.Life is an independent publication and is not affiliated with any company, product or trademark using a similar name. See our <a href="disclaimer.html">trademark notice</a>.</p></details>
  </section>
</div></section>'''
    schema = [{"@context": "https://schema.org", "@type": "WebSite", "name": "Ever.Life", "url": SITE + "/"}]
    write("index.html", page("index.html", "Ever.Life: Live Longer, Leave More | Longevity & Legacy Tools",
                             "Free life expectancy calculator, biological age test, life insurance calculator and legacy checklist, plus expert guides on living longer and protecting your family.",
                             body, schema=schema))


# ---------------- Get matched (lead gen) ----------------
def build_get_matched():
    r = ""
    needs = [("insurance", "Life insurance", "Term or permanent quotes"), ("final", "Final expense", "Burial &amp; funeral cover"),
             ("estate", "Will &amp; estate", "Wills, trusts, POA"), ("retirement", "Retirement plan", "Income that lasts"),
             ("clinic", "Longevity testing", "Clinics, labs, coaching"), ("other", "Something else", "Tell us more")]
    countries = ["United States", "Canada", "United Kingdom", "Australia", "India", "Other"]
    body = hero("Get matched with the right professional", "One short form. A licensed specialist in your region for life insurance, final expense coverage, wills and estates, retirement income or longevity testing. Free and no obligation.",
                [("Get Matched", None)], r, "Takes about 60 seconds")
    body += f'''<section class="block" style="padding-top:36px"><div class="container">
<form class="lead-shell form" data-form="Lead - Get Matched" data-steps data-success="Request received. A specialist will reach out within one business day.">
  {honeypot()}<input type="hidden" name="Form" value="Get Matched - multi-step">
  <div style="display:flex;justify-content:space-between;align-items:center"><strong data-step-label>Step 1 of 4</strong><span class="muted" style="font-size:.85rem">{ICONS["lock"].replace('<svg', '<svg style="width:14px;height:14px;display:inline;vertical-align:-2px"')} Private &amp; secure</span></div>
  <div class="progress"><i></i></div>
  <div class="step">
    <h2 style="font-size:1.5rem">What can we help you with?</h2>
    <div class="choice-grid" data-autonext>{"".join(f'<label class="choice"><input type="radio" name="need" value="{v}" required><span>{t}<small>{s}</small></span></label>' for v, t, s in needs)}</div>
  </div>
  <div class="step">
    <h2 style="font-size:1.5rem">A little about you</h2>
    <div class="row two">
      <div><label for="m-age">Age range</label><select id="m-age" name="age_range" required><option value="">Select…</option>{"".join(f"<option>{a}</option>" for a in ["18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"])}</select></div>
      <div><label for="m-country">Country</label><select id="m-country" name="country" required><option value="">Select…</option>{"".join(f"<option>{c}</option>" for c in countries)}</select></div>
      <div><label for="m-region">State / province / region</label><input id="m-region" name="region" required></div>
      <div><label for="m-smoke">Tobacco use in last 12 months?</label><select id="m-smoke" name="tobacco"><option>No</option><option>Yes</option><option>Prefer not to say</option></select></div>
    </div>
  </div>
  <div class="step">
    <h2 style="font-size:1.5rem">Your goals</h2>
    <div class="row two">
      <div><label for="m-amt">Coverage or budget (if known)</label><select id="m-amt" name="amount"><option>Not sure yet</option><option>Under $100,000</option><option>$100,000 to $250,000</option><option>$250,000 to $500,000</option><option>$500,000 to $1M</option><option>Over $1M</option></select></div>
      <div><label for="m-when">When would you like to start?</label><select id="m-when" name="timeline"><option>As soon as possible</option><option>Within 30 days</option><option>In 1 to 3 months</option><option>Just researching</option></select></div>
    </div>
    <div><label for="m-notes">Anything we should know? (optional)</label><textarea id="m-notes" name="notes" placeholder="e.g. family situation, existing coverage, questions"></textarea></div>
  </div>
  <div class="step">
    <h2 style="font-size:1.5rem">Where should we send your match?</h2>
    <div class="row two">
      <div><label for="m-name">Full name</label><input id="m-name" name="name" required autocomplete="name"></div>
      <div><label for="m-email">Email</label><input id="m-email" type="email" name="email" required autocomplete="email"></div>
      <div><label for="m-phone">Phone</label><input id="m-phone" type="tel" name="phone" autocomplete="tel" placeholder="Optional but faster"></div>
      <div><label for="m-time">Best time to reach you</label><select id="m-time" name="best_time"><option>Any time</option><option>Morning</option><option>Afternoon</option><option>Evening</option><option>Email only</option></select></div>
    </div>
    <label class="check"><input type="checkbox" name="consent" value="yes" required> By submitting, I agree that Ever.Life and up to three licensed partner professionals may contact me about my request by email, phone or text, including by automated means. Consent is not a condition of any purchase. I have read the <a href="privacy-policy.html">Privacy Policy</a> and <a href="terms.html">Terms</a>.</label>
    <button class="btn btn-gold btn-block" type="submit">Get my free match</button>
  </div>
  <div class="step-done center" hidden><div class="ico" style="margin:0 auto 12px;width:56px;height:56px;border-radius:999px;background:var(--gold-soft);color:var(--ok);display:grid;place-items:center">{ICONS["check"]}</div><h2>You're matched in the queue</h2><p>A specialist will contact you within one business day. In the meantime, try the <a href="tools/life-insurance-calculator.html">coverage calculator</a> or the <a href="tools/legacy-checklist.html">legacy checklist</a>.</p></div>
  {status()}
  <div class="step-nav"><button class="btn btn-ghost" type="button" data-prev>Back</button><button class="btn btn-primary" type="button" data-next>Continue</button></div>
  <div class="trust"><span>{ICONS["check"]} 100% free</span><span>{ICONS["check"]} No obligation</span><span>{ICONS["lock"]} Never sold for spam</span><span>{ICONS["check"]} Licensed pros only</span></div>
</form>
</div></section>
<section class="block alt"><div class="container">
  <div class="section-head center" style="margin:0 auto 32px"><h2>How it works</h2></div>
  <div class="grid g3">
    <div class="card reveal"><span class="kpi">1</span><h3>Tell us what you need</h3><p>Four short steps. Only the basics a specialist needs to give you real options.</p></div>
    <div class="card reveal"><span class="kpi">2</span><h3>We find the right fit</h3><p>Your request goes to a licensed professional who serves your region and specialty.</p></div>
    <div class="card reveal"><span class="kpi">3</span><h3>You decide</h3><p>Compare options with no pressure. You are never obligated to buy anything.</p></div>
  </div>
  <section class="faq" style="max-width:820px;margin:48px auto 0">
    <details><summary>How much does this cost?</summary><p>Nothing. Partner professionals may compensate Ever.Life for introductions, which keeps the site free. That never changes the price you are offered.</p></details>
    <details><summary>Who will contact me?</summary><p>A licensed professional for the service you selected, such as an insurance agent or broker, estate-planning attorney or notary, or financial planner, depending on your region.</p></details>
    <details><summary>Will my information be sold?</summary><p>Your details are shared only with the professionals needed to answer your request. See our <a href="privacy-policy.html">Privacy Policy</a> for your rights.</p></details>
    <details><summary>Are you a professional or partner who wants leads?</summary><p>Join our partner network on the <a href="advertise.html#partners">Advertise &amp; Partner</a> page.</p></details>
  </section>
</div></section>'''
    write("get-matched.html", page("get-matched.html", "Get Matched: Free Life Insurance & Estate Planning Help",
                                   "Get matched free with a licensed professional for life insurance, final expense, wills and estates, retirement planning or longevity testing. 60 seconds, no obligation.", body))


# ---------------- Videos ----------------
def build_videos():
    r = ""
    cats = sorted({v[3] for v in VIDEOS})
    pills = '<button class="pill active" data-filter="all" type="button">All</button>' + "".join(f'<button class="pill" data-filter="{c}" type="button">{c.title()}</button>' for c in cats)
    body = hero("Longevity Video Library", "Hand-picked talks from scientists and researchers on how to live longer and better. Videos load only when you press play.", [("Videos", None)], r)
    body += f'''<section class="block"><div class="container">{ad("top")}
<div class="pill-row" data-filter-group="#video-grid" style="margin-bottom:24px">{pills}</div>
<div class="grid g3" id="video-grid">{"".join(video_card(v, r) for v in VIDEOS)}</div>
{ad("mid")}
<div class="grid g2" style="margin-top:48px">
  <div class="card"><h2 style="font-size:1.4rem">Suggest a video</h2><p>Found a great talk on longevity, health or legacy planning? Send it in.</p>
    <form class="form" data-form="Video Suggestion">{honeypot()}<input type="hidden" name="Form" value="Video suggestion">
      <div><label for="v-url">YouTube link</label><input id="v-url" name="video_url" type="url" required placeholder="https://www.youtube.com/watch?v=…"></div>
      <div><label for="v-why">Why it's worth watching</label><textarea id="v-why" name="why"></textarea></div>
      <div><label for="v-email">Your email (optional)</label><input id="v-email" name="email" type="email"></div>
      <button class="btn btn-primary" type="submit">Send suggestion</button>{status()}</form></div>
  <div class="card"><h2 style="font-size:1.4rem">Creators: get featured</h2><p>We feature high-quality, accurate creators in our library, newsletter and contests. Sponsored video integrations are also available for aligned brands.</p><a class="btn btn-gold" href="advertise.html">Partner with us</a> <a class="btn btn-ghost" href="careers.html">Create for Ever.Life</a></div>
</div>
<p class="form-note mt-2">Videos are embedded from YouTube in privacy-enhanced mode and remain the property of their creators. Inclusion does not imply endorsement of Ever.Life by the creators.</p>
</div></section>'''
    write("videos.html", page("videos.html", "Longevity Video Library: Best Talks on Living Longer",
                              "Watch the best talks on longevity, sleep, exercise, happiness and healthy ageing, curated by Ever.Life.", body, active="Videos"))


# ---------------- Support / donations ----------------
def build_support():
    r = ""
    alloc = [("Operations &amp; hosting", 30), ("Content &amp; expert review", 30), ("Promotion &amp; marketing", 15), ("Contests &amp; prizes", 15), ("Hiring talent &amp; new tools", 10)]
    bars = "".join(f'<li><span>{n}</span><span><b>{p}%</b></span></li><li style="border:0;padding:0"><div class="meter" style="margin:0 0 6px;width:100%"><i style="width:{p}%"></i></div></li>' for n, p in alloc)
    tiers = [("Supporter", "$5", "/month", ["Keeps one tool online for a month", "Supporter badge in newsletter", "Early access to new tools"], False),
             ("Patron", "$25", "/month", ["Funds an expert-reviewed guide each quarter", "Name on the Supporters wall", "Vote on next guides and tools", "Quarterly behind-the-scenes update"], True),
             ("Founding Sponsor", "$250", "+ one-time", ["Logo/name on the Sponsors page", "Sponsor a contest prize in your name", "Annual impact report", "Direct line to the founder"], False)]
    tier_html = "".join(f'''<div class="card tier reveal{" featured" if f else ""}"><h3>{n}</h3><div class="price">{p}<small> {u}</small></div><ul>{"".join(f"<li>{x}</li>" for x in perks)}</ul>
<a class="btn {"btn-gold" if f else "btn-primary"} btn-block" href="#pledge" onclick="var s=document.getElementById('s-tier');if(s)s.value='{n}'">Choose {n}</a></div>''' for n, p, u, perks, f in tiers)
    body = hero("Support Ever.Life", "Ever.Life is free for everyone. Reader support keeps it independent and funds operations, marketing, new talent, contests and prizes.", [("Support", None)], r, "Reader-supported")
    body += f'''<section class="block"><div class="container">
<div class="grid g3">{tier_html}</div>
<div class="grid g2" style="margin-top:48px;align-items:start">
  <div class="card" id="pledge"><h2 style="font-size:1.5rem">Make a contribution</h2>
    <p class="muted">Pick an amount and tell us how you'd like to give. We'll reply with secure payment options (card, PayPal, bank transfer or UPI) within one business day.</p>
    <div class="pill-row" data-amounts="#s-amount" style="margin-bottom:14px">{"".join(f'<button type="button" class="pill{" active" if a == 25 else ""}" data-value="{a}">${a}</button>' for a in [10, 25, 50, 100, 250, 500])}</div>
    <div class="pill-row" style="margin-bottom:14px"><a class="btn btn-gold btn-sm" data-paylink="once" hidden target="_blank" rel="noopener">Give once now</a><a class="btn btn-primary btn-sm" data-paylink="monthly" hidden target="_blank" rel="noopener">Give monthly now</a></div>
    <form class="form" data-form="Support Pledge" data-success="Thank you for supporting Ever.Life! We'll send secure payment details shortly.">
      {honeypot()}<input type="hidden" name="Form" value="Support / donation pledge">
      <div class="row two"><div><label for="s-amount">Amount (USD)</label><input id="s-amount" name="amount" type="number" min="1" value="25" required></div>
      <div><label for="s-freq">Frequency</label><select id="s-freq" name="frequency"><option>One-time</option><option>Monthly</option><option>Yearly</option></select></div></div>
      <div><label for="s-tier">Tier</label><select id="s-tier" name="tier"><option>Custom</option><option>Supporter</option><option>Patron</option><option>Founding Sponsor</option></select></div>
      <div><label for="s-purpose">Direct my support to</label><select id="s-purpose" name="purpose"><option>Where it's needed most</option><option>Ongoing operations</option><option>Promotions &amp; marketing</option><option>Hiring talent</option><option>Contests &amp; prizes</option></select></div>
      <div class="row two"><div><label for="s-name">Name</label><input id="s-name" name="name" required></div><div><label for="s-email">Email</label><input id="s-email" name="email" type="email" required></div></div>
      <div><label for="s-msg">Message (optional)</label><textarea id="s-msg" name="message" style="min-height:80px"></textarea></div>
      <label class="check"><input type="checkbox" name="public_name" value="yes"> List my name on the Supporters wall</label>
      <button class="btn btn-primary btn-block" type="submit">Send my pledge</button>{status()}
      <p class="form-note">Ever.Life is not a registered charity; contributions are not tax-deductible. Refunds are available within 14 days on request.</p>
    </form></div>
  <div class="stack-sm">
    <div class="card"><h2 style="font-size:1.4rem">Where your money goes</h2><ul class="factors">{bars}</ul></div>
    <div class="card"><h3>Other ways to help</h3><ul style="padding-left:18px;color:var(--ink-2)"><li>Share a tool with someone you care about</li><li><a href="contests.html">Sponsor a contest prize</a></li><li><a href="careers.html">Contribute as a writer or reviewer</a></li><li><a href="advertise.html">Become a partner or advertiser</a></li><li>Subscribe to the weekly briefing (footer)</li></ul></div>
    <div class="card"><h3>Corporate sponsorship</h3><p>Sponsor a tool, a guide series or the whole site. Interested in the domain itself?</p><a class="btn btn-gold btn-sm" href="{CONTACT_URL}" target="_blank" rel="noopener">Contact us</a></div>
  </div>
</div></div></section>'''
    write("support.html", page("support.html", "Support Ever.Life: Keep Longevity Tools Free",
                               "Support Ever.Life with a one-time or monthly contribution. Funds operations, expert content, marketing, new talent, contests and prizes.", body, active="Support"))


# ---------------- Contests ----------------
def build_contests():
    r = ""
    contests = [("trophy", "The 100-Year Life Challenge", "A 30-day habit challenge: move daily, sleep 7+ hours, eat plants, connect with someone. Log your streak and share your progress.", "Grand prize, runner-up prizes and wellness gear"),
                ("doc", "Legacy Letter Story Contest", "Write a 300 to 800 word letter to a future generation: the lessons, values and memories you want to last.", "Cash prizes plus publication on Ever.Life"),
                ("play", "Longevity Creator Award", "Make a short video (under 3 minutes) that teaches one evidence-based healthy-ageing habit.", "Cash prize, feature in our video library and newsletter")]
    cards = "".join(f'<div class="card reveal"><div class="ico">{ICONS[i]}</div><span class="tag">Prizes: {p}</span><h3>{t}</h3><p>{d}</p><a class="btn btn-primary btn-sm" href="#enter" onclick="var s=document.getElementById(\'c-contest\');if(s)s.value=\'{t}\'">Enter / register</a></div>' for i, t, d, p in contests)
    body = hero("Contests &amp; Prizes", "Challenges that make healthy habits stick and stories that last. Free to enter, open to adults worldwide where permitted.", [("Contests", None)], r, "Free to enter")
    body += f'''<section class="block"><div class="container">
<div class="grid g3">{cards}</div>
<div class="grid g2" style="margin-top:48px;align-items:start">
  <div class="card" id="enter"><h2 style="font-size:1.5rem">Enter or register interest</h2><p class="muted">Register now and we'll email you the start date, full prize list and submission link for your contest.</p>
    <form class="form" data-form="Contest Entry" data-success="You're registered! Watch your inbox for the official start date and rules.">
      {honeypot()}<input type="hidden" name="Form" value="Contest entry / registration">
      <div><label for="c-contest">Contest</label><select id="c-contest" name="contest" required>{"".join(f"<option>{c[1]}</option>" for c in contests)}</select></div>
      <div class="row two"><div><label for="c-name">Full name</label><input id="c-name" name="name" required></div><div><label for="c-email">Email</label><input id="c-email" name="email" type="email" required></div></div>
      <div class="row two"><div><label for="c-country">Country</label><input id="c-country" name="country" required></div><div><label for="c-link">Entry link (optional)</label><input id="c-link" name="entry_link" type="url" placeholder="Google Doc, YouTube, Drive…"></div></div>
      <div><label for="c-msg">Tell us about your entry (optional)</label><textarea id="c-msg" name="entry_description" style="min-height:90px"></textarea></div>
      <label class="check"><input type="checkbox" name="age_confirm" value="18+" required> I confirm I am 18 or older and agree to the official rules below.</label>
      <button class="btn btn-gold btn-block" type="submit">Register</button>{status()}</form></div>
  <div class="stack-sm">
    <div class="card"><h3>Sponsor a prize</h3><p>Brands and individuals can fund prizes and get featured to every entrant and our newsletter audience.</p><a class="btn btn-primary btn-sm" href="advertise.html?type=Contest%20sponsorship">Sponsor a contest</a></div>
    <div class="card"><h3>Official rules (summary)</h3><ul style="padding-left:18px;font-size:.92rem;color:var(--ink-2)">
      <li>No purchase or payment necessary to enter or win. A purchase does not improve your chances.</li>
      <li>Open to individuals 18+ where permitted by law. Void where prohibited or restricted.</li>
      <li>Entry periods, prize values and judging criteria are published on each contest's announcement before entries open.</li>
      <li>Skill-based judging on originality, accuracy and usefulness by an Ever.Life panel. Winners are notified by email and announced on this page.</li>
      <li>Entries must be your own original work and must not infringe anyone's rights. You keep ownership; you grant Ever.Life a licence to display your entry.</li>
      <li>Winners may be responsible for taxes. Prizes are not transferable. Ever.Life may substitute a prize of equal or greater value.</li>
      <li>Participation does not constitute medical advice; consult a health professional before starting a new exercise or diet program.</li>
    </ul></div>
  </div>
</div></div></section>'''
    write("contests.html", page("contests.html", "Contests & Prizes: The 100-Year Life Challenge", "Join free Ever.Life contests: the 100-Year Life Challenge, the Legacy Letter story contest and the Longevity Creator Award. Prizes for winners.", body, active="Community"))


# ---------------- Careers ----------------
def build_careers():
    r = ""
    roles = [("Health &amp; Longevity Writer", "Freelance · Remote", "Turn research into clear, accurate guides. Science or health writing background preferred."),
             ("Medical Reviewer (MD, RN, RD, PhD)", "Freelance · Remote", "Review health content for accuracy and safety. Active licence or credential required."),
             ("Licensed Insurance / Estate Advisor Partner", "Partner network", "Licensed agents, brokers, planners and estate lawyers who want qualified introductions."),
             ("Video Creator &amp; Editor", "Freelance · Remote", "Produce short explainers and tool walkthroughs for YouTube and social."),
             ("Community &amp; Contest Manager", "Part-time · Remote", "Run challenges, moderate entries and grow our newsletter community."),
             ("Front-end Developer", "Contract · Remote", "Build new calculators and interactive tools with vanilla JS and accessible design."),
             ("Brand Ambassador", "Commission · Global", "Share Ever.Life tools in your community and earn for partner introductions.")]
    cards = "".join(f'<div class="card reveal"><span class="tag">{t}</span><h3>{n}</h3><p>{d}</p><a class="btn btn-ghost btn-sm" href="#apply" onclick="var s=document.getElementById(\'j-role\');if(s)s.value=\'{html.unescape(n)}\'">Apply</a></div>' for n, t, d in roles)
    body = hero("Careers &amp; Contributors", "Help millions of people live longer and plan better. We work with writers, clinicians, creators, developers and licensed advisors around the world.", [("Careers", None)], r, "We're hiring")
    body += f'''<section class="block"><div class="container"><div class="grid g3">{cards}</div>
<div class="card" id="apply" style="max-width:820px;margin:48px auto 0"><h2 style="font-size:1.5rem">Apply or introduce yourself</h2>
<form class="form" data-form="Careers Application" data-success="Thanks for applying! We review every application and reply within 7 days.">
  {honeypot()}<input type="hidden" name="Form" value="Careers application">
  <div><label for="j-role">Role</label><select id="j-role" name="role" required>{"".join(f"<option>{html.unescape(n)}</option>" for n, _, _ in roles)}<option>Other / open application</option></select></div>
  <div class="row two"><div><label for="j-name">Full name</label><input id="j-name" name="name" required></div><div><label for="j-email">Email</label><input id="j-email" name="email" type="email" required></div>
  <div><label for="j-loc">Location / time zone</label><input id="j-loc" name="location"></div><div><label for="j-link">Portfolio / LinkedIn / CV link</label><input id="j-link" name="portfolio" type="url" required></div></div>
  <div><label for="j-cred">Credentials or licences (if any)</label><input id="j-cred" name="credentials" placeholder="e.g. RN, CFP, licensed agent in Ontario"></div>
  <div><label for="j-why">Why Ever.Life?</label><textarea id="j-why" name="message" required></textarea></div>
  <button class="btn btn-primary btn-block" type="submit">Submit application</button>{status()}
  <p class="form-note">Ever.Life is an equal-opportunity collaborator. We welcome applicants of every background.</p>
</form></div></div></section>'''
    write("careers.html", page("careers.html", "Careers: Write, Review, Create & Partner with Ever.Life", "Join Ever.Life as a health writer, medical reviewer, video creator, developer, community manager or licensed advisor partner.", body))


# ---------------- Advertise ----------------
def build_advertise():
    r = ""
    formats = [("mega", "Sponsored guides", "Expert-reviewed, clearly labelled sponsored content on longevity or planning topics."),
               ("pulse", "Tool sponsorship", "Exclusive 'presented by' placement on a calculator with a contextual call to action."),
               ("doc", "Newsletter placements", "Native placements in the weekly briefing to an opted-in audience."),
               ("shield", "Lead partner program", "Exclusive or shared qualified leads for insurance, estate, retirement and longevity services by region."),
               ("play", "Video integrations", "Sponsor a video series or segment in our library and social channels."),
               ("trophy", "Contest sponsorship", "Fund prizes and get featured to every entrant and winner announcement.")]
    cards = "".join(f'<div class="card reveal"><div class="ico">{ICONS[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in formats)
    body = hero("Advertise &amp; Partner", "Reach adults 30 to 75 who are actively thinking about their health, their family and their future: the most valuable audience in health and financial services.", [("Advertise", None)], r, "Media kit on request")
    body += f'''<section class="block"><div class="container"><div class="grid g3">{cards}</div>
<div class="grid g2" style="margin-top:48px;align-items:start">
  <div class="card" id="partners"><h2 style="font-size:1.5rem">Request the media kit or a partnership</h2>
  <form class="form" data-form="Advertising / Partnership Inquiry" data-success="Thanks! Our partnerships team will reply with the media kit within one business day.">
    {honeypot()}<input type="hidden" name="Form" value="Advertising / partnership inquiry">
    <div><label for="a-type">I'm interested in</label><select id="a-type" name="type" required><option>Advertising</option><option>Sponsorship</option><option>Lead partner program</option><option>Contest sponsorship</option><option>Content partnership</option><option>Buying / investing in this website or domain</option><option>Other</option></select></div>
    <div class="row two"><div><label for="a-name">Name</label><input id="a-name" name="name" required></div><div><label for="a-email">Work email</label><input id="a-email" name="email" type="email" required></div>
    <div><label for="a-co">Company</label><input id="a-co" name="company" required></div><div><label for="a-web">Website</label><input id="a-web" name="website" type="url"></div>
    <div><label for="a-budget">Monthly budget</label><select id="a-budget" name="budget"><option>Under $1,000</option><option>$1,000 to $5,000</option><option>$5,000 to $20,000</option><option>$20,000+</option><option>Prefer to discuss</option></select></div>
    <div><label for="a-region">Target regions</label><input id="a-region" name="regions" placeholder="e.g. US, Canada, UK"></div></div>
    <div><label for="a-msg">Goals and details</label><textarea id="a-msg" name="message" required></textarea></div>
    <button class="btn btn-primary btn-block" type="submit">Send inquiry</button>{status()}
  </form></div>
  <div class="stack-sm">
    <div class="card"><h3>Who reads Ever.Life</h3><ul class="factors"><li><span>Core age range</span><b>30 to 75</b></li><li><span>Top intents</span><b>Health, insurance, estate</b></li><li><span>Primary markets</span><b>US, Canada, UK, AU, India</b></li><li><span>Devices</span><b>Mobile-first</b></li></ul></div>
    <div class="card"><h3>Our standards</h3><p style="font-size:.95rem">All sponsored content is labelled. We do not accept ads for unproven cures, predatory lending or anything that conflicts with our <a href="editorial-policy.html">editorial policy</a>. Advertisers never influence our independent guides or tool results.</p></div>
    <div class="card"><h3>Buy, sponsor or partner on the domain</h3><p>Interested in the Ever.Life domain, the whole website, or a major sponsorship?</p><a class="btn btn-gold btn-sm" href="{CONTACT_URL}" target="_blank" rel="noopener">web.works/contact</a></div>
  </div>
</div></div></section>'''
    write("advertise.html", page("advertise.html", "Advertise & Partner with Ever.Life", "Advertising, sponsorship and lead partnership opportunities with Ever.Life, reaching adults planning for their health, family and future.", body))


# ---------------- About / contact / editorial ----------------
def build_about():
    r = ""
    body = hero("About Ever.Life", "We believe a long life should also be a good one, and a well-planned one. Ever.Life brings both halves together.", [("About", None)], r)
    body += f'''<section class="block"><div class="container"><div class="prose">
<h2 id="mission">Our mission</h2><p>Ever.Life exists to help people add healthy years to their lives and protect the people and things they love along the way. We turn research on healthy ageing into practical steps, and we turn complex planning topics like life insurance, wills and digital legacy into plain English.</p>
<h2 id="what-we-do">What we do</h2><ul><li><strong>Free tools.</strong> Calculators and checklists that run privately in your browser.</li><li><strong>Guides.</strong> Long-form, sourced articles reviewed against our <a href="editorial-policy.html">editorial policy</a>.</li><li><strong>Connections.</strong> When you want expert help, we introduce you to licensed professionals at no cost.</li><li><strong>Community.</strong> Challenges, contests and stories that make healthy habits and legacy planning stick.</li></ul>
<h2 id="how-we-make-money">How we make money</h2><p>Ever.Life is free to use. We earn revenue from advertising (including Google AdSense), reader contributions, and fees from partner professionals when readers ask to be introduced to them. These relationships never change our tool results or what our guides recommend.</p>
<h2 id="independence">Independence</h2><p>Ever.Life is an independent publication. We are not an insurer, broker, law firm or medical provider, and we are not affiliated with any company or trademark using a similar name. See our <a href="disclaimer.html">disclaimer and trademark notice</a>.</p>
<div class="callout"><strong>Get in touch:</strong> Questions, corrections or partnership ideas? Use our <a href="contact.html">contact form</a>.</div>
</div></div></section>'''
    write("about.html", page("about.html", "About Ever.Life", "Ever.Life is an independent longevity and legacy-planning resource with free tools, plain-English guides and connections to licensed professionals.", body))


def build_contact():
    r = ""
    body = hero("Contact Ever.Life", "Questions, corrections, partnerships or press. We read every message and reply within two business days.", [("Contact", None)], r)
    body += f'''<section class="block"><div class="container"><div class="grid g2" style="align-items:start">
<div class="card"><form class="form" data-form="Contact" data-success="Thanks for reaching out! We'll reply within two business days.">
  {honeypot()}<input type="hidden" name="Form" value="General contact">
  <div><label for="ct-topic">Topic</label><select id="ct-topic" name="topic"><option>General question</option><option>Guide suggestion</option><option>Correction</option><option>Partnership / advertising</option><option>Sponsorship</option><option>Domain / website inquiry</option><option>Press</option><option>Privacy request</option></select></div>
  <div class="row two"><div><label for="ct-name">Name</label><input id="ct-name" name="name" required></div><div><label for="ct-email">Email</label><input id="ct-email" name="email" type="email" required></div></div>
  <div><label for="ct-msg">Message</label><textarea id="ct-msg" name="message" required></textarea></div>
  <button class="btn btn-primary btn-block" type="submit">Send message</button>{status()}
</form></div>
<div class="stack-sm">
  <div class="card"><h3>Need expert help?</h3><p>For insurance, estate or retirement questions, our matching service is faster.</p><a class="btn btn-gold btn-sm" href="get-matched.html">Get matched</a></div>
  <div class="card"><h3>Domain, sponsorship &amp; partnership</h3><p>Interested in this website, the domain name, sponsorship, advertising or partnership?</p><a class="btn btn-primary btn-sm" href="{CONTACT_URL}" target="_blank" rel="noopener">web.works/contact</a></div>
  <div class="card"><h3>Medical emergencies</h3><p>Ever.Life cannot help in an emergency. Call your local emergency number immediately.</p></div>
</div></div></div></section>
<script>try{{var t=new URLSearchParams(location.search).get("topic");if(t){{var s=document.getElementById("ct-topic");for(var i=0;i<s.options.length;i++)if(s.options[i].text===t)s.selectedIndex=i;}}}}catch(e){{}}</script>'''
    write("contact.html", page("contact.html", "Contact Ever.Life", "Contact Ever.Life with questions, corrections, guide suggestions, partnership, sponsorship or press inquiries.", body))


def legal_page(path, title, desc, sections, intro):
    r = ""
    content = "".join(f'<h2 id="s{i}">{h}</h2>{b}' for i, (h, b) in enumerate(sections))
    body = hero(title, intro, [(title, None)], r)
    body += f'<section class="block"><div class="container"><div class="prose legal"><p class="muted">Last updated: October 17, 2026</p>{content}</div></div></section>'
    write(path, page(path, title, desc, body))


def build_legal():
    legal_page("editorial-policy.html", "Editorial Policy", "How Ever.Life researches, writes, reviews and updates its longevity and legacy-planning content.", [
        ("Our standards", "<p>Every guide is written to be accurate, useful and easy to understand. We prioritize guidance from public health agencies, peer-reviewed research, professional bodies and government regulators.</p>"),
        ("Research and sourcing", "<p>Each guide lists its key sources. We describe the strength of evidence honestly, flag where research is early or disputed, and avoid sensational claims.</p>"),
        ("Review and updates", "<p>Guides are reviewed periodically and when major guidance changes. The date on each article shows the last substantive update. Health content is reviewed by people with relevant credentials as our reviewer network grows.</p>"),
        ("Independence from advertisers", "<p>Advertisers and partners have no influence over our guides or tool results. Sponsored content is always clearly labelled.</p>"),
        ("Corrections", '<p>Spotted an error? Tell us through the <a href="contact.html?topic=Correction">contact form</a>. We review every report and correct mistakes promptly.</p>'),
        ("Use of AI", "<p>We may use software tools, including AI, to assist with research, drafting and coding. Humans set the editorial direction, and content is checked against our sources before publishing.</p>"),
    ], "How we research, write and keep our content accurate.")

    legal_page("privacy-policy.html", "Privacy Policy", "How Ever.Life collects, uses and protects your information, including cookies and Google AdSense advertising.", [
        ("Who we are", '<p>Ever.Life ("we", "us") operates this website. Questions about this policy can be sent through our <a href="contact.html?topic=Privacy%20request">contact form</a>.</p>'),
        ("Information we collect", "<p><strong>Information you give us:</strong> when you submit a form (contact, get matched, newsletter, support, contest or careers), we collect what you enter, such as your name, email, phone number, region and request details.</p><p><strong>Tool inputs:</strong> our calculators and checklist run in your browser. We do not receive what you type into them. The checklist saves progress only in your browser's local storage.</p><p><strong>Automatic information:</strong> like most websites, our hosting provider and advertising partners may collect technical data such as IP address, browser type, pages viewed and cookie identifiers.</p>"),
        ("How we use information", "<ul><li>To respond to your requests and messages</li><li>To connect you, at your request, with licensed professionals relevant to your request</li><li>To send the newsletter if you subscribe (unsubscribe anytime)</li><li>To administer contests, support pledges and job applications</li><li>To operate, secure and improve the site and show advertising</li></ul>"),
        ("Sharing", "<p>We share your form details only with the partner professionals needed to answer your request, with service providers who process data for us (such as our form-delivery and hosting providers), or when required by law. We do not sell your personal information for money. Some laws treat sharing for advertising as a 'sale' or 'sharing'; see your rights below.</p>"),
        ("Google AdSense and advertising cookies", '<p>We use Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google\'s use of advertising cookies enables it and its partners to serve ads to you based on your visits to this site and/or other sites on the Internet.</p><p>You may opt out of personalized advertising by visiting <a href="https://adssettings.google.com/" target="_blank" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors\' use of cookies at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>. Learn more in <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">how Google uses data from sites that use its services</a>.</p><p>Visitors in the EEA, UK and Switzerland will be shown a consent message before personalized ads are served.</p>'),
        ("Embedded content", "<p>Videos are embedded from YouTube in privacy-enhanced mode and load only when you press play. YouTube's own privacy policy then applies.</p>"),
        ("Your rights", "<p>Depending on where you live (for example under the GDPR, UK GDPR, CCPA/CPRA, PIPEDA or India's DPDP Act), you may have rights to access, correct, delete or port your data, to object to or restrict processing, and to opt out of the sale or sharing of personal information. Submit a request through our contact form and we will respond within the time required by law.</p>"),
        ("Retention and security", "<p>We keep form submissions only as long as needed for the purpose you gave them, then delete them. We use reasonable safeguards, but no online transmission is completely secure.</p>"),
        ("Children", "<p>Ever.Life is intended for adults. We do not knowingly collect personal information from children under 16.</p>"),
        ("Changes", "<p>We may update this policy. The date at the top shows the latest version.</p>"),
    ], "What we collect, why, and the choices you have.")

    legal_page("cookie-policy.html", "Cookie Policy", "How Ever.Life and partners such as Google use cookies and similar technologies.", [
        ("What cookies are", "<p>Cookies are small text files stored on your device. Similar technologies include local storage and pixels.</p>"),
        ("Cookies we use", "<ul><li><strong>Essential:</strong> remember your theme, cookie choice and checklist progress (stored locally in your browser).</li><li><strong>Advertising:</strong> Google AdSense and its partners use cookies to serve and measure ads, including personalized ads where permitted.</li><li><strong>Embedded media:</strong> YouTube may set cookies after you press play on a video.</li></ul>"),
        ("Your choices", '<p>You can choose "Essential only" in our cookie notice, delete cookies in your browser settings, and manage ad personalization at <a href="https://adssettings.google.com/" target="_blank" rel="noopener">Google Ads Settings</a>.</p>'),
    ], "The cookies we and our partners use, and how to control them.")

    legal_page("terms.html", "Terms of Use", "The terms that govern your use of the Ever.Life website, tools and services.", [
        ("Acceptance", "<p>By using Ever.Life you agree to these terms. If you do not agree, please do not use the site.</p>"),
        ("Educational purpose only", '<p>All content and tools are for general educational purposes. They are not medical, financial, insurance, tax or legal advice and do not create a professional relationship. See our <a href="disclaimer.html">Disclaimer</a>.</p>'),
        ("Matching service", "<p>When you request a match, you authorize us to share your details with partner professionals for that purpose. Partners are independent businesses responsible for their own products, advice and licensing. We do not guarantee any outcome, price or eligibility.</p>"),
        ("Contributions and contests", '<p>Support contributions are voluntary and not tax-deductible. Contests are governed by the official rules on the <a href="contests.html">Contests</a> page and each contest announcement.</p>'),
        ("Intellectual property", "<p>The Ever.Life name, design, text, tools and code are protected by copyright and other laws. You may share links and short quotes with attribution. You may not copy or republish substantial content without written permission.</p>"),
        ("User submissions", "<p>You are responsible for anything you submit. Do not submit unlawful, infringing or harmful content. You grant us a non-exclusive licence to use submissions for the purpose you submitted them.</p>"),
        ("Third-party links and ads", "<p>We link to and display ads for third-party sites we do not control and are not responsible for their content or practices.</p>"),
        ("Limitation of liability", "<p>To the fullest extent permitted by law, Ever.Life is not liable for any indirect, incidental or consequential damages arising from your use of the site. The site is provided 'as is' without warranties of any kind.</p>"),
        ("Changes and contact", '<p>We may update these terms at any time. Questions: <a href="contact.html">contact us</a>.</p>'),
    ], "The rules for using Ever.Life.")

    legal_page("disclaimer.html", "Disclaimer & Trademark Notice", "Medical, financial and legal disclaimer, affiliate and advertising disclosure, and trademark and copyright notice for Ever.Life.", [
        ("Medical disclaimer", "<p>Ever.Life provides general health information for education only. It is not a substitute for professional medical advice, diagnosis or treatment. Never ignore professional advice or delay seeking it because of something you read here. In an emergency, call your local emergency number.</p>"),
        ("Financial, insurance and legal disclaimer", "<p>Ever.Life is not an insurance company, agent, broker, financial adviser, law firm or lawyer, and does not sell insurance or legal services. Calculator results are estimates for education only. Laws, products and prices vary by country, state and province; consult a licensed professional before making decisions.</p>"),
        ("Advertising and compensation disclosure", "<p>Ever.Life displays advertising, including Google AdSense, and may receive compensation from partner professionals when readers request introductions. Sponsored content is clearly labelled. Compensation never affects our tool results or editorial recommendations.</p>"),
        ("Trademark notice", '<p>"Ever.Life" is used solely as the name of this independent website, derived from its domain name. Ever.Life is <strong>not affiliated with, endorsed by, sponsored by or otherwise connected to</strong> any company, organization, product, service, app or registered or unregistered trademark that uses the name "EverLife", "Everlife", "Ever Life", "Ever-Life" or any similar name or mark, in any country. Any similarity is coincidental. We make no claim to any third-party mark.</p><p>All other product names, company names, logos and trademarks mentioned on this site are the property of their respective owners and are used for identification and informational purposes only. Their use does not imply affiliation or endorsement.</p><p>If you believe content on this site infringes your trademark, please <a href="contact.html">contact us</a> and we will review it promptly.</p>'),
        ("Copyright notice", '<p>&copy; 2026 Ever.Life. All original text, graphics, design, calculators and code on this website are protected by copyright. Embedded videos and linked resources remain the property of their owners. To report copyright concerns, use our <a href="contact.html">contact form</a> with the URL, the work concerned and your contact details.</p>'),
    ], "Important information about how to use our content, and who we are not.")


def build_404():
    r = ""
    body = """<section class="block center"><div class="container" style="max-width:640px"><span class="eyebrow">404</span><h1 style="margin-top:14px">This page didn't make it.</h1><p class="muted">The link may be old or mistyped. Here are some good places to go instead.</p>
<div class="hero-actions" style="justify-content:center"><a class="btn btn-primary" href="/">Home</a><a class="btn btn-ghost" href="/tools/">Free tools</a><a class="btn btn-ghost" href="/guides/">Guides</a></div></div></section>"""
    out = page("404.html", "Page Not Found", "The page you were looking for could not be found.", body, noindex=True)
    # 404 is served at any depth on the custom domain, so make every local link root-absolute.
    out = re.sub(r'(href|src)="(?!https?:|/|#|mailto:)', r'\1="/', out)
    write("404.html", out)


def build_meta(guides):
    paths = [p for p in OUT if p.endswith(".html") and p != "404.html"]
    urls = ""
    for p in sorted(paths):
        loc = p[:-10] if p.endswith("index.html") else p
        pr = "1.0" if p == "index.html" else ("0.9" if p.startswith("tools/") or p == "get-matched.html" else "0.7")
        urls += f"  <url><loc>{SITE}/{loc}</loc><lastmod>2026-10-17</lastmod><priority>{pr}</priority></url>\n"
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("ads.txt", "google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
    write(".nojekyll", "")
    write("CNAME", "ever.life\n")


if __name__ == "__main__":
    guides = load_guides()
    build_home(guides)
    build_guides(guides)
    write("tools/index.html", T.tools_index())
    write("tools/life-expectancy-calculator.html", T.life_expectancy())
    write("tools/biological-age-test.html", T.biological_age())
    write("tools/life-insurance-calculator.html", T.insurance())
    write("tools/legacy-checklist.html", T.legacy())
    build_get_matched(); build_videos(); build_support(); build_contests(); build_careers(); build_advertise()
    build_about(); build_contact(); build_legal(); build_404()
    build_meta(guides)
    print(f"Built {len(OUT)} files")
