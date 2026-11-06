// Free Tools hub: live search with suggestions, category filter tabs, and a quick AP estimate widget.
(function () {
  // ---------- filter tabs + category cards
  var cards = Array.prototype.slice.call(document.querySelectorAll('.th-card'));
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.th-tab'));
  var empty = document.querySelector('.th-empty');
  var activeCat = 'all', query = '';

  function apply() {
    var shown = 0;
    cards.forEach(function (c) {
      var okCat = activeCat === 'all' || c.dataset.cat === activeCat;
      var okQ = !query || c.dataset.search.indexOf(query) > -1;
      var ok = okCat && okQ;
      c.classList.toggle('is-hidden', !ok);
      if (ok) shown++;
    });
    if (empty) empty.hidden = shown > 0;
  }
  function setCat(cat) {
    activeCat = cat;
    tabs.forEach(function (t) { t.setAttribute('aria-pressed', t.dataset.cat === cat ? 'true' : 'false'); });
    apply();
  }
  tabs.forEach(function (t) { t.addEventListener('click', function () { setCat(t.dataset.cat); }); });
  document.querySelectorAll('[data-jump-cat]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      setCat(el.dataset.jumpCat);
      document.getElementById('all-tools').scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // ---------- search with suggestions
  var input = document.getElementById('th-q');
  var list = document.getElementById('th-suggest');
  var form = document.getElementById('th-search');
  var sel = -1, matches = [];
  function renderSuggest() {
    list.innerHTML = '';
    sel = -1;
    if (!query) { list.hidden = true; return; }
    matches = cards.filter(function (c) { return c.dataset.search.indexOf(query) > -1; }).slice(0, 6);
    if (!matches.length) {
      list.innerHTML = '<li class="th-sug-none">No tool yet. <a href="contact">Ask us to build it</a></li>';
    }
    matches.forEach(function (c, i) {
      var li = document.createElement('li');
      li.setAttribute('role', 'option');
      li.id = 'th-opt-' + i;
      li.innerHTML = '<span class="th-sug-name">' + c.dataset.name + '</span><span class="th-sug-meta">' +
        (c.tagName === 'A' ? c.dataset.catname : 'Coming soon') + '</span>';
      li.addEventListener('mousedown', function (e) { e.preventDefault(); go(c); });
      list.appendChild(li);
    });
    list.hidden = false;
  }
  function go(c) {
    if (c.tagName === 'A') { location.href = c.getAttribute('href'); return; }
    list.hidden = true;
    c.scrollIntoView({ behavior: 'smooth', block: 'center' });
    c.classList.add('is-flash');
    setTimeout(function () { c.classList.remove('is-flash'); }, 1200);
  }
  function highlight() {
    Array.prototype.forEach.call(list.children, function (li, i) { li.classList.toggle('is-sel', i === sel); });
    input.setAttribute('aria-activedescendant', sel > -1 ? 'th-opt-' + sel : '');
  }
  if (input) {
    input.addEventListener('input', function () { query = input.value.trim().toLowerCase(); apply(); renderSuggest(); });
    input.addEventListener('keydown', function (e) {
      if (list.hidden || !matches.length) return;
      if (e.key === 'ArrowDown') { sel = Math.min(sel + 1, matches.length - 1); highlight(); e.preventDefault(); }
      else if (e.key === 'ArrowUp') { sel = Math.max(sel - 1, 0); highlight(); e.preventDefault(); }
      else if (e.key === 'Escape') { list.hidden = true; }
    });
    input.addEventListener('blur', function () { setTimeout(function () { list.hidden = true; }, 120); });
    input.addEventListener('focus', function () { if (query) renderSuggest(); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (matches.length) go(matches[sel > -1 ? sel : 0]);
      else document.getElementById('all-tools').scrollIntoView({ behavior: 'smooth' });
    });
  }
  document.querySelectorAll('[data-fill]').forEach(function (b) {
    b.addEventListener('click', function () { input.value = b.dataset.fill; input.dispatchEvent(new Event('input')); input.focus(); });
  });

  // ---------- quick AP estimate
  var qe = document.getElementById('quick-ap');
  if (qe) {
    var EX = { csa: { w: 55, cuts: [77, 60, 47, 37], part: 'Free response' }, csp: { w: 70, cuts: [84, 71, 56, 42], part: 'Create task + written response' } };
    var exam = 'csa';
    var mc = qe.querySelector('#qa-mc'), fr = qe.querySelector('#qa-fr');
    var mcOut = qe.querySelector('#qa-mc-out'), frOut = qe.querySelector('#qa-fr-out');
    var big = qe.querySelector('.qa-score'), comp = qe.querySelector('.qa-comp'), ring = qe.querySelector('.qa-ring-fg');
    var partLabel = qe.querySelector('.qa-part');
    var shown = 0, raf;
    function animateTo(n) {
      cancelAnimationFrame(raf);
      var start = shown, t0 = null;
      function step(ts) {
        if (!t0) t0 = ts;
        var k = Math.min(1, (ts - t0) / 350);
        var v = Math.round(start + (n - start) * k);
        big.textContent = v;
        if (k < 1) raf = requestAnimationFrame(step); else shown = n;
      }
      raf = requestAnimationFrame(step);
    }
    function calc() {
      var e = EX[exam];
      var c = mc.value * e.w / 100 + fr.value * (100 - e.w) / 100;
      var s = 1;
      for (var i = 0; i < 4; i++) { if (c >= e.cuts[i]) { s = 5 - i; break; } }
      mcOut.textContent = mc.value + '%';
      frOut.textContent = fr.value + '%';
      comp.textContent = 'Composite ' + Math.round(c) + ' / 100';
      ring.style.strokeDashoffset = String(302 - 302 * s / 5);
      qe.dataset.score = s;
      animateTo(s);
      mc.style.setProperty('--fill', mc.value + '%');
      fr.style.setProperty('--fill', fr.value + '%');
    }
    qe.querySelectorAll('[data-qa-exam]').forEach(function (b) {
      b.addEventListener('click', function () {
        exam = b.dataset.qaExam;
        qe.querySelectorAll('[data-qa-exam]').forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
        partLabel.textContent = EX[exam].part;
        calc();
      });
    });
    mc.addEventListener('input', calc);
    fr.addEventListener('input', calc);
    calc();
  }
})();
