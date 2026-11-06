// AP Computer Science score calculator (CSA and CSP).
// Section weights and point totals come from College Board's published exam pages and 2026 scoring guidelines.
// The 1 to 5 cut points are UpskillGrid estimates: College Board does not publish them.
(function () {
  var root = document.getElementById('apcalc');
  if (!root) return;

  var EXAMS = {
    csa: {
      name: 'AP Computer Science A',
      mcq: { max: 42, weight: 55 },
      parts: [
        { id: 'q1', label: 'FRQ 1: Methods and Control Structures', max: 7 },
        { id: 'q2', label: 'FRQ 2: Class Design', max: 7 },
        { id: 'q3', label: 'FRQ 3: Data Analysis with ArrayList', max: 5 },
        { id: 'q4', label: 'FRQ 4: 2D Array', max: 6 }
      ],
      partWeight: 45,
      cuts: [77, 60, 47, 37]
    },
    csp: {
      name: 'AP Computer Science Principles',
      mcq: { max: 70, weight: 70 },
      parts: [
        { id: 'r1', label: 'Video', max: 1 },
        { id: 'r2', label: 'Program requirements', max: 1 },
        { id: 'r3', label: 'Written Response 1: design, function and purpose', max: 1 },
        { id: 'r4', label: 'Written Response 2(a): algorithm development', max: 1 },
        { id: 'r5', label: 'Written Response 2(b): errors and testing', max: 1 },
        { id: 'r6', label: 'Written Response 2(c): data and procedural abstraction', max: 1 }
      ],
      partWeight: 30,
      cuts: [84, 71, 56, 42]
    }
  };
  var LABELS = { 5: 'Extremely well qualified', 4: 'Well qualified', 3: 'Qualified', 2: 'Possibly qualified', 1: 'No recommendation' };

  var current = 'csa';
  var state = { csa: { mcq: 28, q1: 5, q2: 5, q3: 3, q4: 4 }, csp: { mcq: 50, r1: 1, r2: 1, r3: 1, r4: 1, r5: 0, r6: 1 } };

  var form = root.querySelector('.calc-inputs');
  var tabs = root.querySelectorAll('[data-exam]');

  function clamp(v, lo, hi) { v = Math.round(Number(v)); if (isNaN(v)) v = 0; return Math.max(lo, Math.min(hi, v)); }

  function renderInputs() {
    var ex = EXAMS[current], s = state[current], h = '';
    h += '<div class="calc-field"><label for="ap-mcq">Multiple choice: questions correct <span class="calc-max">out of ' + ex.mcq.max + '</span></label>' +
      '<div class="calc-pair"><input type="range" id="ap-mcq-range" min="0" max="' + ex.mcq.max + '" value="' + s.mcq + '" aria-label="Multiple choice correct, slider">' +
      '<input type="number" id="ap-mcq" inputmode="numeric" min="0" max="' + ex.mcq.max + '" value="' + s.mcq + '"></div></div>';
    if (current === 'csa') {
      h += '<p class="calc-sub">Free response points <span class="calc-max">(25 points in total)</span></p>';
      ex.parts.forEach(function (p) {
        var opts = '';
        for (var i = 0; i <= p.max; i++) opts += '<option value="' + i + '"' + (i === s[p.id] ? ' selected' : '') + '>' + i + ' / ' + p.max + '</option>';
        h += '<div class="calc-field calc-row"><label for="ap-' + p.id + '">' + p.label + '</label><select id="ap-' + p.id + '" data-part="' + p.id + '">' + opts + '</select></div>';
      });
    } else {
      h += '<p class="calc-sub">Create task and written response <span class="calc-max">(tick each row you earned, 6 points in total)</span></p>';
      ex.parts.forEach(function (p) {
        h += '<label class="calc-check"><input type="checkbox" data-part="' + p.id + '"' + (s[p.id] ? ' checked' : '') + '> ' + p.label + '</label>';
      });
    }
    form.innerHTML = h;
    var num = document.getElementById('ap-mcq'), rng = document.getElementById('ap-mcq-range');
    num.addEventListener('input', function () { state[current].mcq = clamp(num.value, 0, ex.mcq.max); rng.value = state[current].mcq; update(); });
    num.addEventListener('blur', function () { num.value = state[current].mcq; });
    rng.addEventListener('input', function () { state[current].mcq = clamp(rng.value, 0, ex.mcq.max); num.value = state[current].mcq; update(); });
    form.querySelectorAll('[data-part]').forEach(function (el) {
      el.addEventListener('change', function () {
        state[current][el.dataset.part] = el.type === 'checkbox' ? (el.checked ? 1 : 0) : Number(el.value);
        update();
      });
    });
    update();
  }

  function update() {
    var ex = EXAMS[current], s = state[current];
    var partMax = 0, partGot = 0;
    ex.parts.forEach(function (p) { partMax += p.max; partGot += s[p.id]; });
    var mcqPts = s.mcq / ex.mcq.max * ex.mcq.weight;
    var partPts = partGot / partMax * ex.partWeight;
    var comp = mcqPts + partPts;
    var shown = Math.round(comp);
    var score = 1;
    for (var i = 0; i < ex.cuts.length; i++) { if (comp >= ex.cuts[i]) { score = 5 - i; break; } }

    root.querySelector('.calc-score').textContent = score;
    root.querySelector('.calc-label').textContent = LABELS[score];
    root.querySelector('.calc-comp').textContent = shown + ' / 100';
    root.querySelector('.calc-split').textContent = 'Multiple choice ' + mcqPts.toFixed(1) + ' of ' + ex.mcq.weight +
      ' · ' + (current === 'csa' ? 'Free response ' : 'Section II ') + partPts.toFixed(1) + ' of ' + ex.partWeight;
    root.querySelector('.calc-fill').style.width = Math.min(100, comp) + '%';
    root.querySelector('.calc-result').dataset.score = score;

    var marks = '';
    ex.cuts.forEach(function (c, idx) { marks += '<span class="calc-mark" style="left:' + c + '%"><i>' + (5 - idx) + '</i></span>'; });
    root.querySelector('.calc-marks').innerHTML = marks;

    var note = '';
    if (score < 5) {
      var need = ex.cuts[5 - score - 1] - comp;
      var perMcq = ex.mcq.weight / ex.mcq.max;
      var q = Math.ceil(need / perMcq - 1e-9);
      note = 'You are about ' + Math.ceil(need) + ' composite points from an estimated ' + (score + 1) + '. ';
      if (s.mcq + q <= ex.mcq.max) note += 'That is roughly ' + q + ' more multiple-choice question' + (q === 1 ? '' : 's') + ' correct.';
      else note += 'Extra free-response points will get you there faster.';
    } else {
      note = 'Estimated 5. Keep a safety margin: cut points move a little each year.';
    }
    var nearest = ex.cuts.reduce(function (m, c) { return Math.min(m, Math.abs(comp - c)); }, 100);
    if (nearest < 3) note += ' You are close to a cut point, so the real result could go either way.';
    root.querySelector('.calc-note').textContent = note;
  }

  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      current = t.dataset.exam;
      tabs.forEach(function (o) { o.setAttribute('aria-selected', o === t ? 'true' : 'false'); });
      renderInputs();
    });
  });
  if (location.hash === '#csp') { current = 'csp'; tabs.forEach(function (o) { o.setAttribute('aria-selected', o.dataset.exam === 'csp' ? 'true' : 'false'); }); }
  renderInputs();
})();
