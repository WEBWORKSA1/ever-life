/* Ever.Life — interactive tools. Educational estimates only. */
(function () {
  "use strict";
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function num(v, d) { var n = parseFloat(v); return isNaN(n) ? (d || 0) : n; }
  function val(form, name) { var el = form.elements[name]; if (!el) return ""; return el.value; }
  function money(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
  function round1(n) { return Math.round(n * 10) / 10; }
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ================= Life expectancy calculator ================= */
  // Approximate period life expectancy at birth (years). Rounded figures from national statistics agencies / WHO.
  var BASE = {
    us: { m: 75.8, f: 81.1, label: "United States" },
    ca: { m: 79.5, f: 84.0, label: "Canada" },
    uk: { m: 79.0, f: 82.9, label: "United Kingdom" },
    au: { m: 81.1, f: 85.1, label: "Australia" },
    in: { m: 70.5, f: 73.6, label: "India" },
    eu: { m: 78.5, f: 83.8, label: "European Union (avg.)" },
    world: { m: 71.0, f: 76.0, label: "Global average" }
  };
  var le = $("#le-form");
  if (le) {
    var run = function () {
      var c = BASE[val(le, "country")] || BASE.us;
      var sex = val(le, "sex") === "f" ? "f" : "m";
      var age = Math.max(0, Math.min(110, num(val(le, "age"), 35)));
      var base = c[sex];
      // Survivor adjustment: people who already reached an age have a higher expected total lifespan.
      var remaining = Math.max(2, (base - age) + 0.0018 * age * age);
      var factors = [];
      var add = function (label, yrs) { if (yrs) factors.push([label, yrs]); };
      var h = num(val(le, "height"), 170) / 100, w = num(val(le, "weight"), 70);
      var bmi = h > 0 ? w / (h * h) : 22;
      if (bmi < 18.5) add("Underweight BMI", -2); else if (bmi < 25) add("Healthy BMI", 0.5);
      else if (bmi < 30) add("Overweight BMI", -1); else if (bmi < 35) add("Obesity (class I)", -3); else add("Obesity (class II+)", -6);
      add({ never: "", former: "Former smoker", current: "Current smoker" }[val(le, "smoke")] || "", { never: 0, former: -2.5, current: -10 }[val(le, "smoke")] || 0);
      add({ none: "Inactive lifestyle", some: "", regular: "Meets activity guidelines", high: "Very active + strength training" }[val(le, "exercise")] || "", { none: -3, some: 0, regular: 3, high: 4 }[val(le, "exercise")] || 0);
      add({ poor: "Diet high in processed food", avg: "", good: "Plant-forward / Mediterranean diet" }[val(le, "diet")] || "", { poor: -2, avg: 0, good: 2 }[val(le, "diet")] || 0);
      add({ heavy: "Heavy drinking", moderate: "", none: "" }[val(le, "alcohol")] || "", { heavy: -4, moderate: 0, none: 0 }[val(le, "alcohol")] || 0);
      add({ short: "Sleep under 6 hours", ok: "7 to 9 hours of sleep", long: "Sleep over 9 hours" }[val(le, "sleep")] || "", { short: -2, ok: 1, long: -1 }[val(le, "sleep")] || 0);
      add({ isolated: "Socially isolated", some: "", strong: "Strong social ties" }[val(le, "social")] || "", { isolated: -2.5, some: 0, strong: 1.5 }[val(le, "social")] || 0);
      add({ high: "High chronic stress", mid: "", low: "Low stress / good coping" }[val(le, "stress")] || "", { high: -1.5, mid: 0, low: 1 }[val(le, "stress")] || 0);
      add({ long: "Parents/grandparents lived past 85", avg: "", short: "Close family died before 65" }[val(le, "family")] || "", { long: 2, avg: 0, short: -2 }[val(le, "family")] || 0);
      $$('input[name="cond"]:checked', le).forEach(function (cb) {
        var map = { diabetes: ["Diabetes", -4], heart: ["Heart disease", -5], bp: ["High blood pressure", -2], lung: ["Chronic lung disease", -4], cancer: ["Cancer history", -3] };
        if (map[cb.value]) add(map[cb.value][0], map[cb.value][1]);
      });
      add({ yes: "Regular check-ups and screenings", no: "Skips preventive check-ups" }[val(le, "checkups")] || "", { yes: 1, no: -1 }[val(le, "checkups")] || 0);
      // Lifestyle effects shrink with age, since fewer years remain to be influenced.
      var scale = Math.max(0.25, 1 - age / 110);
      var adj = factors.reduce(function (s, f) { return s + f[1]; }, 0) * scale;
      var est = Math.max(age + 1, age + remaining + adj);
      est = Math.min(est, 105);
      $("#le-result").textContent = round1(est);
      $("#le-remaining").textContent = round1(est - age);
      $("#le-range").textContent = Math.round(est - 5) + " to " + Math.round(Math.min(est + 5, 108));
      $("#le-base").textContent = c.label + " " + (sex === "f" ? "female" : "male") + " average at birth: " + base + " years";
      $("#le-bmi").textContent = round1(bmi);
      var pct = Math.min(100, Math.round(age / est * 100));
      $("#le-meter").style.width = pct + "%";
      $("#le-pct").textContent = pct + "%";
      var ul = $("#le-factors"); ul.innerHTML = "";
      factors.filter(function (f) { return f[0] && f[1] !== 0; }).sort(function (a, b) { return a[1] - b[1]; }).forEach(function (f) {
        var li = document.createElement("li");
        var v = round1(f[1] * scale);
        li.innerHTML = "<span>" + f[0] + "</span><span class='" + (v >= 0 ? "pos" : "neg") + "'>" + (v > 0 ? "+" : "") + v + " yrs</span>";
        ul.appendChild(li);
      });
      if (!ul.children.length) ul.innerHTML = "<li><span>No major adjustments</span><span>0</span></li>";
      // Life grid: one cell per year
      var g = $("#le-grid"); if (g) {
        var total = Math.ceil(est); g.innerHTML = "";
        g.style.gridTemplateColumns = "repeat(10,1fr)";
        for (var i = 0; i < total; i++) { var cell = document.createElement("i"); cell.className = i < age ? "lived" : "left"; cell.title = "Age " + (i + 1); g.appendChild(cell); }
      }
      $("#le-out").hidden = false;
    };
    le.addEventListener("input", run);
    le.addEventListener("change", run);
    le.addEventListener("submit", function (e) { e.preventDefault(); run(); $("#le-out").scrollIntoView({ behavior: "smooth", block: "start" }); });
    run();
  }

  /* ================= Biological age test ================= */
  var ba = $("#ba-form");
  if (ba) {
    var runBA = function () {
      var age = Math.max(18, Math.min(100, num(val(ba, "age"), 40)));
      var total = 0, answered = 0, tips = [];
      $$(".q", ba).forEach(function (q) {
        var r = $("input:checked", q);
        if (r) { answered++; var p = num(r.value); total += p; if (p > 0 && q.dataset.tip) tips.push(q.dataset.tip); }
      });
      var bio = Math.max(18, Math.round((age + total) * 10) / 10);
      var diff = round1(bio - age);
      $("#ba-result").textContent = bio;
      $("#ba-diff").textContent = (diff > 0 ? "+" : "") + diff + " years vs. calendar age";
      $("#ba-diff").style.color = diff > 0 ? "var(--danger)" : "var(--ok)";
      $("#ba-verdict").textContent = diff <= -4 ? "Excellent. Your habits look like those of someone notably younger." :
        diff <= 0 ? "Good. Your habits are in line with or better than your calendar age." :
        diff <= 4 ? "Room to improve. A few changes could pay off over the next decade." :
        "Your habits are ageing you faster. The upside of change is large.";
      $("#ba-answered").textContent = answered + " of " + $$(".q", ba).length + " answered";
      var ul = $("#ba-tips"); ul.innerHTML = "";
      tips.slice(0, 5).forEach(function (t) { var li = document.createElement("li"); li.textContent = t; ul.appendChild(li); });
      if (!tips.length) ul.innerHTML = "<li>Keep going. Your answers show strong fundamentals.</li>";
      $("#ba-meter").style.width = Math.max(4, Math.min(100, 50 + diff * 5)) + "%";
    };
    ba.addEventListener("change", runBA);
    ba.addEventListener("input", runBA);
    ba.addEventListener("submit", function (e) { e.preventDefault(); runBA(); $("#ba-out").scrollIntoView({ behavior: "smooth" }); });
    runBA();
  }

  /* ================= Life insurance needs (DIME) ================= */
  var li = $("#li-form");
  if (li) {
    var runLI = function () {
      var debt = num(val(li, "debt")), income = num(val(li, "income")), years = num(val(li, "years"), 10),
        mort = num(val(li, "mortgage")), kids = num(val(li, "kids")), edu = num(val(li, "edu"), 50000),
        fin = num(val(li, "final"), 15000), savings = num(val(li, "savings")), existing = num(val(li, "existing"));
      $$("[data-range-out]", li).forEach(function (o) { var f = li.elements[o.getAttribute("data-range-out")]; if (f) o.textContent = f.value; });
      var parts = [["Debts", debt], ["Income replacement", income * years], ["Mortgage", mort], ["Education", kids * edu], ["Final expenses", fin]];
      var gross = parts.reduce(function (s, p) { return s + p[1]; }, 0);
      var need = Math.max(0, gross - savings - existing);
      var rounded = need > 0 ? Math.ceil(need / 50000) * 50000 : 0;
      $("#li-result").textContent = money(rounded);
      $("#li-gross").textContent = money(gross);
      $("#li-less").textContent = "−" + money(savings + existing);
      var ul = $("#li-parts"); ul.innerHTML = "";
      parts.forEach(function (p) {
        var pct = gross ? Math.round(p[1] / gross * 100) : 0;
        var el = document.createElement("li");
        el.innerHTML = "<span>" + p[0] + " <small class='muted'>(" + pct + "%)</small></span><span>" + money(p[1]) + "</span>";
        ul.appendChild(el);
      });
      var youngest = num(val(li, "youngest"));
      var term = kids > 0 ? Math.max(10, Math.ceil((23 - youngest) / 5) * 5) : (mort > 0 ? 20 : 10);
      term = Math.min(30, term);
      $("#li-term").textContent = term + "-year term";
      $("#li-multiple").textContent = income ? round1(rounded / income) + "× income" : "—";
    };
    li.addEventListener("input", runLI);
    li.addEventListener("submit", function (e) { e.preventDefault(); runLI(); $("#li-out").scrollIntoView({ behavior: "smooth" }); });
    runLI();
  }

  /* ================= Legacy checklist ================= */
  var cl = $("#legacy-list");
  if (cl) {
    var KEY = "el-legacy-v1";
    var saved = {};
    try { saved = JSON.parse(store.get(KEY) || "{}") || {}; } catch (e) { saved = {}; }
    var boxes = $$("input[type=checkbox]", cl);
    var update = function () {
      var done = 0;
      boxes.forEach(function (b) { b.closest("li").classList.toggle("done", b.checked); if (b.checked) done++; saved[b.id] = b.checked; });
      store.set(KEY, JSON.stringify(saved));
      var pct = Math.round(done / boxes.length * 100);
      $("#cl-pct").textContent = pct + "%";
      $("#cl-count").textContent = done + " of " + boxes.length + " complete";
      $("#cl-meter").style.width = pct + "%";
      $("#cl-msg").textContent = pct === 100 ? "Outstanding. Your legacy plan is complete. Review it once a year." :
        pct >= 60 ? "Strong progress. Finish the remaining items this quarter." :
        pct >= 25 ? "Good start. Prioritize the will, beneficiaries and coverage next." :
        "Start with the first three items. They protect your family the most.";
    };
    boxes.forEach(function (b) { if (saved[b.id]) b.checked = true; b.addEventListener("change", update); });
    var pr = $("#cl-print"); if (pr) pr.addEventListener("click", function () { window.print(); });
    var rs = $("#cl-reset"); if (rs) rs.addEventListener("click", function () { boxes.forEach(function (b) { b.checked = false; }); update(); });
    update();
  }
})();
