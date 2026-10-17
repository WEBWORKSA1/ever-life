/* Ever.Life — site script. All runtime settings live in CONFIG. */
(function () {
  "use strict";

  var CONFIG = {
    adClient: "ca-pub-6620975821265271",
    // Optional manual ad units. Leave empty to rely on AdSense Auto ads.
    // Example: adSlots: { top: "1234567890", inArticle: "2345678901", sidebar: "3456789012", footer: "4567890123" }
    adSlots: {},
    // Optional payment links for one-click donations (Stripe Payment Links, PayPal.me, Buy Me a Coffee, etc.).
    // Leave empty and the site collects a support pledge through the form instead.
    payLinks: { once: "", monthly: "" },
    // Encoded inbox (reversed + base64). Never rendered on any page.
    k: "bW9jLmxpYW1nQDFhc2tyb3diZXc="
  };

  function endpoint() {
    try { return "https://formsubmit.co/ajax/" + atob(CONFIG.k).split("").reverse().join(""); }
    catch (e) { return ""; }
  }

  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- Theme ---------- */
  var root = document.documentElement;
  var saved = store.get("el-theme");
  if (saved === "light" || saved === "dark") root.setAttribute("data-theme", saved);
  document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var cur = root.getAttribute("data-theme") ||
        (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      var next = cur === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      store.set("el-theme", next);
    });
  });

  /* ---------- Mobile menu ---------- */
  var mBtn = document.querySelector("[data-menu-toggle]");
  var mMenu = document.getElementById("mobile-menu");
  if (mBtn && mMenu) {
    mBtn.addEventListener("click", function () {
      var open = mMenu.classList.toggle("open");
      mBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* ---------- Reveal on scroll ---------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Toast ---------- */
  function toast(msg) {
    var t = document.getElementById("toast");
    if (!t) return;
    t.textContent = msg; t.classList.add("show");
    setTimeout(function () { t.classList.remove("show"); }, 3200);
  }
  window.ELToast = toast;

  /* ---------- Cookie notice ---------- */
  var cookie = document.getElementById("cookie");
  if (cookie && !store.get("el-cookie")) {
    cookie.classList.add("show");
    cookie.querySelectorAll("[data-cookie]").forEach(function (b) {
      b.addEventListener("click", function () { store.set("el-cookie", b.getAttribute("data-cookie")); cookie.classList.remove("show"); });
    });
  }

  /* ---------- Manual ad units (optional) ---------- */
  document.querySelectorAll(".ad-slot[data-slot]").forEach(function (box) {
    var id = CONFIG.adSlots[box.getAttribute("data-slot")];
    if (!id) return;
    box.innerHTML = '<div class="ad-label">Advertisement</div><ins class="adsbygoogle" style="display:block" data-ad-client="' +
      CONFIG.adClient + '" data-ad-slot="' + id + '" data-ad-format="auto" data-full-width-responsive="true"></ins>';
    try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
  });

  /* ---------- YouTube facades (load iframe only on click) ---------- */
  document.querySelectorAll(".video[data-yt]").forEach(function (v) {
    var id = v.getAttribute("data-yt");
    var title = v.getAttribute("data-title") || "Video";
    v.innerHTML = '<img loading="lazy" alt="' + title.replace(/"/g, "&quot;") + '" src="https://i.ytimg.com/vi/' + id + '/hqdefault.jpg">' +
      '<div class="play"><span><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span></div>';
    v.setAttribute("role", "button"); v.setAttribute("tabindex", "0");
    v.setAttribute("aria-label", "Play: " + title);
    function play() {
      v.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0" title="' +
        title.replace(/"/g, "&quot;") + '" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
    }
    v.addEventListener("click", play);
    v.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); play(); } });
  });

  /* ---------- Filters (guides / videos) ---------- */
  document.querySelectorAll("[data-filter-group]").forEach(function (group) {
    var target = document.querySelector(group.getAttribute("data-filter-group"));
    group.querySelectorAll(".pill").forEach(function (p) {
      p.addEventListener("click", function () {
        group.querySelectorAll(".pill").forEach(function (x) { x.classList.remove("active"); });
        p.classList.add("active");
        var f = p.getAttribute("data-filter");
        target.querySelectorAll("[data-cat]").forEach(function (c) {
          c.style.display = (f === "all" || c.getAttribute("data-cat") === f) ? "" : "none";
        });
      });
    });
  });

  /* ---------- Donation amount chips ---------- */
  document.querySelectorAll("[data-amounts]").forEach(function (wrap) {
    var input = document.querySelector(wrap.getAttribute("data-amounts"));
    wrap.querySelectorAll(".pill").forEach(function (p) {
      p.addEventListener("click", function () {
        wrap.querySelectorAll(".pill").forEach(function (x) { x.classList.remove("active"); });
        p.classList.add("active");
        if (input) input.value = p.getAttribute("data-value");
      });
    });
  });
  document.querySelectorAll("[data-paylink]").forEach(function (a) {
    var url = CONFIG.payLinks[a.getAttribute("data-paylink")];
    if (url) { a.href = url; a.hidden = false; }
  });

  /* ---------- Multi-step lead form ---------- */
  document.querySelectorAll("[data-steps]").forEach(function (form) {
    var steps = form.querySelectorAll(".step");
    var bar = form.querySelector(".progress i");
    var label = form.querySelector("[data-step-label]");
    var i = 0;
    function show(n) {
      steps.forEach(function (s, k) { s.classList.toggle("active", k === n); });
      if (bar) bar.style.width = ((n + 1) / steps.length * 100) + "%";
      if (label) label.textContent = "Step " + (n + 1) + " of " + steps.length;
      var pv = form.querySelector("[data-prev]"), nx = form.querySelector("[data-next]");
      if (pv) pv.hidden = n === 0;
      if (nx) nx.hidden = n === steps.length - 1;
      i = n;
    }
    function valid(n) {
      var ok = true;
      steps[n].querySelectorAll("input,select,textarea").forEach(function (f) {
        if (!f.checkValidity()) { ok = false; }
      });
      if (!ok) {
        var first = steps[n].querySelector(":invalid");
        if (first) { first.reportValidity ? first.reportValidity() : null; }
      }
      return ok;
    }
    form.querySelectorAll("[data-next]").forEach(function (b) {
      b.addEventListener("click", function () { if (valid(i)) show(Math.min(i + 1, steps.length - 1)); });
    });
    form.querySelectorAll("[data-prev]").forEach(function (b) {
      b.addEventListener("click", function () { show(Math.max(i - 1, 0)); });
    });
    // Auto-advance on single-choice steps
    form.querySelectorAll(".step [data-autonext] input[type=radio]").forEach(function (r) {
      r.addEventListener("change", function () { setTimeout(function () { if (valid(i)) show(Math.min(i + 1, steps.length - 1)); }, 220); });
    });
    // Prefill interest from URL (?need=insurance)
    try {
      var need = new URLSearchParams(location.search).get("need");
      if (need) { var r = form.querySelector('input[name="need"][value="' + need + '"]'); if (r) r.checked = true; }
    } catch (e) {}
    show(0);
  });

  /* ---------- Form submission (all forms marked data-form) ---------- */
  document.querySelectorAll("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var status = form.querySelector(".form-status");
      var btn = form.querySelector("[type=submit]");
      var hp = form.querySelector('input[name="_honey"]');
      if (hp && hp.value) return; // bot
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = {};
      new FormData(form).forEach(function (v, k) {
        if (k === "_honey") return;
        data[k] = data[k] ? data[k] + ", " + v : v;
      });
      data._subject = "Ever.Life | " + (form.getAttribute("data-form") || "Form") + " submission";
      data._template = "table";
      data._captcha = "false";
      data["Page"] = location.href;
      data["Submitted"] = new Date().toISOString();
      if (btn) { btn.disabled = true; btn.dataset.txt = btn.textContent; btn.textContent = "Sending…"; }
      fetch(endpoint(), {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (!res.ok || String(res.j.success) === "false") throw new Error("fail");
          form.reset();
          if (status) { status.className = "form-status ok"; status.textContent = form.getAttribute("data-success") || "Thank you. Your message has been received. We'll be in touch shortly."; }
          toast("Sent. Thank you!");
          if (form.hasAttribute("data-steps")) {
            form.querySelectorAll(".step").forEach(function (s) { s.classList.remove("active"); });
            var done = form.querySelector(".step-done"); if (done) done.hidden = false;
            var bar = form.querySelector(".progress i"); if (bar) bar.style.width = "100%";
          }
        })
        .catch(function () {
          if (status) { status.className = "form-status err"; status.textContent = "Something went wrong sending your message. Please try again in a moment."; }
        })
        .then(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.txt || "Submit"; } });
    });
  });

  /* ---------- Year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
