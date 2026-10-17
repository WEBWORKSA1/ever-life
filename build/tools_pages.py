"""Interactive tool pages."""
from layout import page, hero, ICONS, ad


def opt(pairs, sel=None):
    return "".join(f'<option value="{v}"{" selected" if v == sel else ""}>{t}</option>' for v, t in pairs)


def radios(name, pairs, checked):
    return "".join(
        f'<label class="choice"><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{t}</span></label>'
        for v, t in pairs)


def tool_cta(r, text, need="insurance"):
    return f'''<div class="cta-band reveal" style="margin-top:40px">
  <div><h3>{text}</h3><p>Compare options from licensed professionals in a 60-second request. Free, no obligation, your details are never sold for spam.</p></div>
  <div class="stack-sm"><a class="btn btn-gold btn-block" href="{r}get-matched.html?need={need}">Get matched free</a><a class="btn btn-ghost btn-block" href="{r}tools/">More free tools</a></div>
</div>'''


def life_expectancy():
    r = "../"
    countries = [("us", "United States"), ("ca", "Canada"), ("uk", "United Kingdom"), ("au", "Australia"), ("in", "India"), ("eu", "European Union"), ("world", "Other / global average")]
    body = hero("Life Expectancy Calculator", "Estimate how long you may live based on where you live, your age and 12 evidence-linked lifestyle factors. Then see which habits add or remove the most years.",
                [("Tools", "tools/"), ("Life Expectancy Calculator", None)], r, "Free tool · 2 minutes")
    body += f'''<section class="block" style="padding-top:32px"><div class="container">{ad("top")}
<div class="tool-wrap">
<form id="le-form" class="card form" novalidate>
  <h2 style="font-size:1.4rem">About you</h2>
  <div class="row two">
    <div><label for="le-country">Country</label><select id="le-country" name="country">{opt(countries, "us")}</select></div>
    <div><label for="le-age">Current age</label><input id="le-age" name="age" type="number" min="0" max="110" value="35" inputmode="numeric"></div>
  </div>
  <div><label>Sex (used for actuarial baseline)</label><div class="choice-grid">{radios("sex", [("m", "Male"), ("f", "Female")], "m")}</div></div>
  <div class="row two">
    <div><label for="le-h">Height (cm)</label><input id="le-h" name="height" type="number" min="100" max="230" value="172"></div>
    <div><label for="le-w">Weight (kg)</label><input id="le-w" name="weight" type="number" min="30" max="300" value="74"></div>
  </div>
  <h2 style="font-size:1.4rem;margin-top:10px">Lifestyle</h2>
  <div class="row two">
    <div><label for="le-smoke">Smoking</label><select id="le-smoke" name="smoke">{opt([("never", "Never smoked"), ("former", "Former smoker"), ("current", "Current smoker")])}</select></div>
    <div><label for="le-ex">Physical activity</label><select id="le-ex" name="exercise">{opt([("none", "Rarely active"), ("some", "Some activity"), ("regular", "150+ min/week"), ("high", "300+ min/week + strength")], "some")}</select></div>
    <div><label for="le-diet">Diet</label><select id="le-diet" name="diet">{opt([("poor", "Mostly processed / fast food"), ("avg", "Mixed / average"), ("good", "Plant-forward, whole foods")], "avg")}</select></div>
    <div><label for="le-alc">Alcohol</label><select id="le-alc" name="alcohol">{opt([("none", "None"), ("moderate", "Light to moderate"), ("heavy", "Heavy (15+ drinks/week)")], "moderate")}</select></div>
    <div><label for="le-sleep">Sleep</label><select id="le-sleep" name="sleep">{opt([("short", "Under 6 hours"), ("ok", "7 to 9 hours"), ("long", "Over 9 hours")], "ok")}</select></div>
    <div><label for="le-social">Social connection</label><select id="le-social" name="social">{opt([("isolated", "Often isolated"), ("some", "Average"), ("strong", "Strong ties, community")], "some")}</select></div>
    <div><label for="le-stress">Stress</label><select id="le-stress" name="stress">{opt([("high", "High, ongoing"), ("mid", "Moderate"), ("low", "Low / well managed")], "mid")}</select></div>
    <div><label for="le-fam">Family longevity</label><select id="le-fam" name="family">{opt([("long", "Parents/grandparents 85+"), ("avg", "Average / unknown"), ("short", "Close family died before 65")], "avg")}</select></div>
    <div><label for="le-chk">Preventive check-ups</label><select id="le-chk" name="checkups">{opt([("yes", "Yes, regularly"), ("no", "Rarely or never")], "yes")}</select></div>
  </div>
  <fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:600;font-size:.9rem;margin-bottom:6px">Diagnosed conditions (optional)</legend>
    <div class="choice-grid">
      {"".join(f'<label class="choice"><input type="checkbox" name="cond" value="{v}"><span>{t}</span></label>' for v, t in [("diabetes", "Diabetes"), ("heart", "Heart disease"), ("bp", "High blood pressure"), ("lung", "Lung disease"), ("cancer", "Cancer history")])}
    </div></fieldset>
  <button class="btn btn-primary btn-block" type="submit">Calculate my life expectancy</button>
  <p class="form-note">Runs entirely in your browser. Nothing you enter here is stored or sent anywhere.</p>
</form>
<aside class="result" id="le-out" aria-live="polite">
  <span class="tag">Your estimate</span>
  <div class="big"><span id="le-result">80</span> <small style="font-size:1.1rem;color:var(--muted)">years</small></div>
  <p class="muted" id="le-base"></p>
  <p>Likely range: <strong id="le-range"></strong> · About <strong id="le-remaining"></strong> years ahead · BMI <strong id="le-bmi"></strong></p>
  <div class="meter"><i id="le-meter"></i></div>
  <p class="form-note">You have lived about <strong id="le-pct"></strong> of your estimated lifespan.</p>
  <h3 style="font-size:1.05rem;margin-top:16px">What moved your number</h3>
  <ul class="factors" id="le-factors"></ul>
  <h3 style="font-size:1.05rem;margin-top:18px">Your life in years</h3>
  <div class="life-grid" id="le-grid" aria-hidden="true"></div>
  <p class="form-note" style="margin-top:10px">Green squares are years lived. Gold squares are years ahead.</p>
  <a class="btn btn-gold btn-block mt-2" href="{r}tools/life-insurance-calculator.html">Protect those years: check your coverage</a>
</aside>
</div>
{ad("inArticle")}
<div class="prose" style="margin-top:48px">
<h2 id="how-it-works">How this calculator works</h2>
<p>We start from the average period life expectancy at birth for your country and sex, rounded from national statistics agencies and the World Health Organization. Because people who have already reached a given age have survived earlier risks, the estimate is adjusted upward for your current age. We then apply directional adjustments for well-studied factors such as smoking, physical activity, body weight, sleep, diet, alcohol and social connection.</p>
<p>The size of each adjustment reflects the general direction and rough magnitude reported in large population studies, and it shrinks as you get older because fewer years remain to be influenced. It is a teaching tool, not a prediction for any individual.</p>
<h2 id="biggest-levers">The biggest levers you control</h2>
<ul>
<li><strong>Not smoking</strong> is consistently linked with roughly a decade of additional life compared with continuing to smoke.</li>
<li><strong>Regular physical activity</strong> and higher cardiorespiratory fitness are among the strongest predictors of a longer life.</li>
<li><strong>Healthy body weight, sleep and diet</strong> lower the risk of cardiovascular and metabolic disease, the leading causes of death in most countries.</li>
<li><strong>Social connection</strong> has an association with survival similar in size to other well-known lifestyle risks.</li>
</ul>
<div class="callout"><strong>Important:</strong> This estimate is for education and motivation only. It does not account for your full medical history and is not medical advice. Talk with your doctor about your personal risk.</div>
<p>Keep going: read <a href="{r}guides/healthspan-vs-lifespan.html">healthspan vs. lifespan</a>, take the <a href="{r}tools/biological-age-test.html">biological age test</a>, or start the <a href="{r}tools/legacy-checklist.html">legacy checklist</a>.</p>
</div>
{tool_cta(r, "Planning for the years ahead? Make sure your family is protected.")}
</div></section>'''
    schema = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Life Expectancy Calculator", "applicationCategory": "HealthApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    return page("tools/life-expectancy-calculator.html", "Life Expectancy Calculator: How Long Will I Live?",
                "Free life expectancy calculator. Estimate your lifespan from your country, age and 12 lifestyle factors, and see which habits add or remove years.",
                body, active="Tools", scripts=["assets/js/tools.js"], schema=schema)


BA_QUESTIONS = [
    ("How many days a week do you get 30+ minutes of moderate exercise?", [("-2", "5 or more"), ("-1", "3 to 4"), ("1", "1 to 2"), ("3", "Rarely")], "Build toward 150 minutes of moderate activity per week; even brisk walking counts."),
    ("Do you do strength or resistance training?", [("-1.5", "2+ times a week"), ("0", "Occasionally"), ("1.5", "Never")], "Add two short strength sessions a week to protect muscle and bone."),
    ("How many hours do you usually sleep?", [("-1", "7 to 9 hours"), ("1", "6 to 7 hours"), ("2.5", "Under 6 hours")], "Protect a consistent 7 to 9 hour sleep window, including weekends."),
    ("How would you describe your diet?", [("-2", "Mostly whole, plant-forward foods"), ("0", "Mixed"), ("2.5", "Mostly processed / fast food")], "Shift a few meals a week toward vegetables, legumes, whole grains and fish."),
    ("Do you smoke or vape nicotine?", [("-0.5", "Never"), ("1.5", "Quit"), ("6", "Yes")], "Quitting nicotine is the single largest health upgrade available. Ask your doctor about support."),
    ("Weekly alcoholic drinks?", [("-0.5", "0 to 2"), ("0.5", "3 to 7"), ("3", "8 or more")], "Cut back on alcohol; fewer drinks is better for long-term health."),
    ("How is your stress most weeks?", [("-1", "Low / well managed"), ("0.5", "Moderate"), ("2", "High")], "Add a daily stress ritual: a walk outdoors, breathing practice or time with friends."),
    ("How connected do you feel to friends, family or community?", [("-1.5", "Very connected"), ("0", "Somewhat"), ("2", "Often lonely")], "Schedule regular time with people you care about; connection is protective."),
    ("Waist size relative to height?", [("-1", "Waist less than half my height"), ("1", "About half"), ("2.5", "More than half")], "Waist-to-height ratio over 0.5 is a useful flag to discuss with your doctor."),
    ("Can you climb 4 flights of stairs without stopping?", [("-1.5", "Easily"), ("0.5", "With effort"), ("2.5", "No")], "Improve cardio fitness gradually; it is one of the strongest predictors of longevity."),
    ("How often do you sit for 8+ hours a day?", [("-0.5", "Rarely"), ("0.5", "Some days"), ("1.5", "Most days")], "Break up sitting every 30 to 60 minutes with a short walk or stretch."),
    ("Do you know your blood pressure, cholesterol and blood sugar numbers?", [("-1", "Yes, all in range"), ("0.5", "Not sure"), ("2", "One or more is high")], "Book a check-up and learn your core numbers; most risks are treatable when caught early."),
]


def biological_age():
    r = "../"
    qs = ""
    for i, (q, choices, tip) in enumerate(BA_QUESTIONS):
        qs += f'''<fieldset class="q card" data-tip="{tip}" style="padding:18px"><legend style="font-weight:600;margin-bottom:8px;float:left;width:100%">{i + 1}. {q}</legend>
<div class="choice-grid">{radios(f"q{i}", choices, None)}</div></fieldset>'''
    body = hero("Biological Age Test", "Your calendar age counts birthdays. Your biological age reflects how your habits are shaping your body. Answer 12 quick questions to estimate yours.",
                [("Tools", "tools/"), ("Biological Age Test", None)], r, "Free quiz · 3 minutes")
    body += f'''<section class="block" style="padding-top:32px"><div class="container">{ad("top")}
<div class="tool-wrap">
<form id="ba-form" class="form" novalidate>
  <div class="card"><label for="ba-age">Your current age</label><input id="ba-age" name="age" type="number" min="18" max="100" value="40"></div>
  {qs}
  <button class="btn btn-primary btn-block" type="submit">See my result</button>
</form>
<aside class="result" id="ba-out" aria-live="polite">
  <span class="tag">Estimated biological age</span>
  <div class="big" id="ba-result">40</div>
  <p style="font-weight:700" id="ba-diff"></p>
  <div class="meter"><i id="ba-meter"></i></div>
  <p id="ba-verdict"></p>
  <p class="form-note" id="ba-answered"></p>
  <h3 style="font-size:1.05rem;margin-top:16px">Your top opportunities</h3>
  <ul id="ba-tips" style="padding-left:18px"></ul>
  <a class="btn btn-gold btn-block mt-2" href="{r}tools/life-expectancy-calculator.html">Next: estimate your life expectancy</a>
</aside></div>
<div class="prose" style="margin-top:48px">
<h2 id="what-is-biological-age">What is biological age?</h2>
<p>Biological age is an estimate of how old your body seems compared with the average person of your calendar age. Researchers measure it with blood markers, fitness tests and DNA methylation "clocks". This quiz uses lifestyle factors that are strongly associated with healthy ageing, so it is a fast, free way to see where you stand and what to work on.</p>
<p>Lab-based biological age tests vary widely between companies and are still being validated, so treat any single number with caution. Our guide to <a href="{r}guides/longevity-biomarkers-tests.html">longevity biomarkers</a> explains which numbers have the strongest evidence.</p>
<div class="callout"><strong>Note:</strong> This quiz is educational and not a diagnosis. Speak with a health professional before making major changes.</div>
</div>
{tool_cta(r, "Want a professional longevity assessment or health testing?", "clinic")}
</div></section>'''
    return page("tools/biological-age-test.html", "Biological Age Test: How Old Is Your Body Really?",
                "Take the free 12-question biological age test. See how your sleep, exercise, diet, stress and connection compare with your calendar age, plus your top fixes.",
                body, active="Tools", scripts=["assets/js/tools.js"])


def insurance():
    r = "../"
    def money_in(name, label, value, hint=""):
        return f'<div><label for="li-{name}">{label}</label><input id="li-{name}" name="{name}" type="number" min="0" step="1000" value="{value}" inputmode="numeric">{f"<span class=form-note>{hint}</span>" if hint else ""}</div>'
    body = hero("Life Insurance Needs Calculator", "How much life insurance do you actually need? Use the DIME method (Debt, Income, Mortgage, Education) that many advisors start with, and get a clear number in seconds.",
                [("Tools", "tools/"), ("Life Insurance Calculator", None)], r, "Free tool · DIME method")
    body += f'''<section class="block" style="padding-top:32px"><div class="container">{ad("top")}
<div class="tool-wrap">
<form id="li-form" class="card form" novalidate>
  <h2 style="font-size:1.4rem">Your obligations</h2>
  <div class="row two">
    {money_in("debt", "Debts (cards, car, loans)", 15000)}
    {money_in("mortgage", "Mortgage balance", 250000)}
    {money_in("income", "Annual income to replace", 70000)}
    <div><label for="li-years">Years of income to replace: <span class="range-out" data-range-out="years">10</span></label><input id="li-years" name="years" type="range" min="1" max="30" value="10"></div>
    <div><label for="li-kids">Children needing education</label><input id="li-kids" name="kids" type="number" min="0" max="10" value="2"></div>
    <div><label for="li-youngest">Age of youngest child</label><input id="li-youngest" name="youngest" type="number" min="0" max="25" value="4"></div>
    {money_in("edu", "Education cost per child", 60000)}
    {money_in("final", "Final expenses", 15000, "Funeral, legal and estate costs.")}
  </div>
  <h2 style="font-size:1.4rem;margin-top:8px">What you already have</h2>
  <div class="row two">
    {money_in("savings", "Savings &amp; investments", 40000)}
    {money_in("existing", "Existing life insurance", 0, "Include coverage through work.")}
  </div>
  <button class="btn btn-primary btn-block" type="submit">Calculate my coverage</button>
  <p class="form-note">Runs in your browser. Nothing is stored or sent.</p>
</form>
<aside class="result" id="li-out" aria-live="polite">
  <span class="tag">Suggested coverage</span>
  <div class="big" id="li-result">$0</div>
  <p>That is about <strong id="li-multiple"></strong>. A common starting point is a <strong id="li-term"></strong> policy.</p>
  <ul class="factors" id="li-parts"></ul>
  <ul class="factors" style="margin-top:8px"><li><span><strong>Total need</strong></span><span id="li-gross"></span></li><li><span>Less savings &amp; existing cover</span><span id="li-less"></span></li></ul>
  <a class="btn btn-gold btn-block mt-2" href="{r}get-matched.html?need=insurance">Get free quotes for this amount</a>
  <p class="form-note" style="margin-top:8px">Estimates are educational. A licensed advisor can tailor coverage to your situation.</p>
</aside></div>
{ad("inArticle")}
<div class="prose" style="margin-top:48px">
<h2 id="dime">How the DIME method works</h2>
<p>DIME adds up four things your family would need to cover if your income stopped: <strong>D</strong>ebts, <strong>I</strong>ncome replacement for a set number of years, the <strong>M</strong>ortgage balance and <strong>E</strong>ducation costs for children. We add final expenses, then subtract savings and any coverage you already have. The result is rounded up to the nearest $50,000, the increments in which many policies are sold.</p>
<h2 id="term-length">Choosing a term length</h2>
<p>A simple rule is to keep coverage in force until your largest obligations end, typically when your youngest child is financially independent or your mortgage is paid off. Read our full guides on <a href="{r}guides/how-much-life-insurance-do-i-need.html">how much life insurance you need</a> and <a href="{r}guides/term-vs-whole-life-insurance.html">term vs. whole life insurance</a>.</p>
<div class="callout"><strong>Disclaimer:</strong> Ever.Life is not an insurance company, agent or broker and does not sell insurance. This tool is for education only.</div>
</div>
{tool_cta(r, "Ready to lock in a rate while you're young and healthy?")}
</div></section>'''
    schema = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Life Insurance Needs Calculator", "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    return page("tools/life-insurance-calculator.html", "Life Insurance Calculator: How Much Coverage Do I Need?",
                "Free life insurance needs calculator using the DIME method. Add debts, income, mortgage and education, subtract savings, and get a recommended coverage amount.",
                body, active="Tools", scripts=["assets/js/tools.js"], schema=schema)


CHECKLIST = [
    ("Protect your family", [
        ("Write or update your will", "Name an executor and say who receives what."),
        ("Name guardians for minor children", "Usually done in your will. Ask the people first."),
        ("Get enough life insurance", "Use the coverage calculator, then compare quotes."),
        ("Review every beneficiary designation", "Retirement accounts, insurance and bank accounts. These override your will."),
    ]),
    ("Plan for incapacity", [
        ("Financial power of attorney", "Someone you trust to handle money if you cannot."),
        ("Healthcare directive / living will", "Write down the care you would and would not want."),
        ("Healthcare proxy", "Name a person to make medical decisions for you."),
        ("Share your doctors and medications list", "Store it where your proxy can find it."),
    ]),
    ("Organize your affairs", [
        ("Create an asset & account inventory", "Banks, investments, property, pensions, debts."),
        ("Set up a password manager with emergency access", "Your digital accounts are part of your estate."),
        ("Use platforms' legacy-contact features", "Email, phone, photo and social accounts."),
        ("Store original documents safely", "Tell your executor where they are."),
    ]),
    ("Leave more than money", [
        ("Write a letter of instruction", "Practical wishes, contacts and where things are."),
        ("Record your story or an ethical will", "Values, lessons and memories for the next generation."),
        ("Decide on funeral and memorial wishes", "Saves your family hard decisions."),
        ("Choose causes you want to support", "Charitable gifts can be part of your plan."),
    ]),
    ("Keep it current", [
        ("Consider a trust if you own property in several places", "Ask an estate lawyer if probate avoidance makes sense."),
        ("Review your plan every 3 to 5 years", "And after marriage, divorce, births, moves or deaths."),
        ("Tell your executor and family where everything is", "A plan nobody can find does not help."),
        ("Book a session with an estate-planning professional", "Rules differ by country, state and province."),
    ]),
]


def legacy():
    r = "../"
    groups = ""
    n = 0
    for title, items in CHECKLIST:
        lis = ""
        for t, d in items:
            n += 1
            lis += f'<li><label><input type="checkbox" id="lg{n}"><span>{t}<small>{d}</small></span></label></li>'
        groups += f'<h2 style="font-size:1.3rem;margin-top:28px">{title}</h2><ul class="checklist">{lis}</ul>'
    body = hero("Legacy Planning Checklist", "Twenty steps that protect the people you love and make sure your wishes are followed. Tick them off as you go; your progress is saved on this device.",
                [("Tools", "tools/"), ("Legacy Checklist", None)], r, "Free interactive checklist")
    body += f'''<section class="block" style="padding-top:32px"><div class="container">{ad("top")}
<div class="tool-wrap">
<div id="legacy-list">{groups}</div>
<aside class="result" aria-live="polite">
  <span class="tag">Your progress</span>
  <div class="big" id="cl-pct">0%</div>
  <p class="muted" id="cl-count"></p>
  <div class="meter"><i id="cl-meter"></i></div>
  <p id="cl-msg"></p>
  <div class="pill-row mt-2"><button class="btn btn-ghost btn-sm" id="cl-print" type="button">Print checklist</button><button class="btn btn-ghost btn-sm" id="cl-reset" type="button">Reset</button></div>
  <a class="btn btn-gold btn-block mt-2" href="{r}get-matched.html?need=estate">Get help with your will or estate plan</a>
  <p class="form-note" style="margin-top:8px">Saved only in this browser. Nothing is sent to us.</p>
</aside></div>
<div class="prose" style="margin-top:48px"><p>New to this? Start with our <a href="{r}guides/estate-planning-basics.html">estate planning basics</a> and <a href="{r}guides/digital-legacy-planning.html">digital legacy</a> guides. Laws differ by jurisdiction, so confirm details with a licensed professional.</p></div>
{tool_cta(r, "Want an expert to help you finish your plan?", "estate")}
</div></section>'''
    return page("tools/legacy-checklist.html", "Legacy Planning Checklist: 20 Steps to Protect Your Family",
                "Free interactive legacy planning checklist: will, guardians, beneficiaries, power of attorney, healthcare directive, digital accounts and more. Track your progress.",
                body, active="Tools", scripts=["assets/js/tools.js"])


TOOLS = [
    ("life-expectancy-calculator.html", "hourglass", "Life Expectancy Calculator", "See how long you may live and which 12 habits move the number most."),
    ("biological-age-test.html", "pulse", "Biological Age Test", "12 questions that estimate whether your body is ageing faster or slower than the calendar."),
    ("life-insurance-calculator.html", "shield", "Life Insurance Calculator", "The DIME method in one screen: the coverage your family would need."),
    ("legacy-checklist.html", "list", "Legacy Checklist", "20 steps from will to digital accounts, saved as you go."),
]


def tools_index():
    r = "../"
    cards = "".join(f'<a class="card reveal" href="{r}tools/{h}"><div class="ico">{ICONS[i]}</div><h3>{t}</h3><p>{d}</p><span class="more">Open tool →</span></a>' for h, i, t, d in TOOLS)
    body = hero("Free Longevity &amp; Legacy Tools", "Interactive calculators that turn big questions into clear numbers. Private by design: everything runs in your browser.", [("Tools", None)], r)
    body += f'<section class="block"><div class="container">{ad("top")}<div class="grid g2">{cards}</div>{tool_cta(r, "Turn your numbers into a plan with a licensed professional.")}</div></section>'
    return page("tools/index.html", "Free Longevity & Legacy Calculators", "Free life expectancy calculator, biological age test, life insurance needs calculator and legacy planning checklist. Private, instant, no sign-up.", body, active="Tools")
