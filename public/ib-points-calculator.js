// IB Diploma points calculator.
// Core points matrix and award conditions follow the IB's published DP passing criteria (ibo.org).
(function () {
  var root = document.getElementById('ibcalc');
  if (!root) return;

  var GROUPS = ['Studies in language and literature', 'Language acquisition', 'Individuals and societies', 'Sciences', 'Mathematics', 'The arts or another subject'];
  var subjects = [
    { level: 'HL', grade: 6 }, { level: 'SL', grade: 5 }, { level: 'HL', grade: 5 },
    { level: 'HL', grade: 6 }, { level: 'SL', grade: 5 }, { level: 'SL', grade: 6 }
  ];
  var core = { tok: 'B', ee: 'B', cas: true };
  var target = 35;
  // rows = TOK, columns = EE. -1 = failing condition (E in either).
  var MATRIX = { A: { A: 3, B: 3, C: 2, D: 2 }, B: { A: 3, B: 2, C: 2, D: 1 }, C: { A: 2, B: 2, C: 1, D: 0 }, D: { A: 2, B: 1, C: 0, D: 0 } };

  var list = root.querySelector('.ib-subjects');
  function gradeOpts(sel) {
    var h = '';
    for (var g = 7; g >= 1; g--) h += '<option value="' + g + '"' + (g === sel ? ' selected' : '') + '>' + g + '</option>';
    return h;
  }
  function renderSubjects() {
    var h = '';
    subjects.forEach(function (s, i) {
      h += '<div class="ib-row" data-i="' + i + '">' +
        '<span class="ib-num">' + (i + 1) + '</span>' +
        '<span class="ib-group">' + GROUPS[i] + '</span>' +
        '<span class="ib-level" role="group" aria-label="Level for subject ' + (i + 1) + '">' +
        '<button type="button" data-lv="HL" aria-pressed="' + (s.level === 'HL') + '">HL</button>' +
        '<button type="button" data-lv="SL" aria-pressed="' + (s.level === 'SL') + '">SL</button></span>' +
        '<label class="ib-grade"><span class="sr">Grade for subject ' + (i + 1) + '</span><select>' + gradeOpts(s.grade) + '</select></label>' +
        '</div>';
    });
    list.innerHTML = h;
    list.querySelectorAll('.ib-row').forEach(function (row) {
      var i = Number(row.dataset.i);
      row.querySelectorAll('[data-lv]').forEach(function (b) {
        b.addEventListener('click', function () { subjects[i].level = b.dataset.lv; renderSubjects(); update(); });
      });
      row.querySelector('select').addEventListener('change', function (e) { subjects[i].grade = Number(e.target.value); update(); });
    });
  }

  function corePoints() {
    if (core.tok === 'E' || core.ee === 'E') return 0;
    return MATRIX[core.tok][core.ee];
  }

  function update() {
    var subjPts = subjects.reduce(function (a, s) { return a + s.grade; }, 0);
    var cp = corePoints();
    var total = subjPts + cp;
    var hl = subjects.filter(function (s) { return s.level === 'HL'; }).map(function (s) { return s.grade; }).sort(function (a, b) { return b - a; });
    var sl = subjects.filter(function (s) { return s.level === 'SL'; }).map(function (s) { return s.grade; });
    var hlPts = hl.slice(0, 3).reduce(function (a, b) { return a + b; }, 0);
    var slPts = sl.reduce(function (a, b) { return a + b; }, 0);
    var ones = subjects.filter(function (s) { return s.grade === 1; }).length;
    var twos = subjects.filter(function (s) { return s.grade === 2; }).length;
    var low = subjects.filter(function (s) { return s.grade <= 3; }).length;
    var slNeed = sl.length === 2 ? 5 : 9;

    var checks = [
      ['At least 24 points in total', total >= 24, total + ' points'],
      ['No grade 1 in any subject', ones === 0, ones ? ones + ' grade 1' + (ones > 1 ? 's' : '') : 'none'],
      ['No more than two grade 2s', twos <= 2, twos + ' grade 2' + (twos === 1 ? '' : 's')],
      ['No more than three grades of 3 or below', low <= 3, low + ' at 3 or below'],
      ['At least 12 points at HL' + (hl.length === 4 ? ' (top 3 HL count)' : ''), hl.length >= 3 && hlPts >= 12, hlPts + ' HL points'],
      ['At least ' + slNeed + ' points at SL', sl.length >= 2 && slPts >= slNeed, slPts + ' SL points'],
      ['No E in TOK or the extended essay', core.tok !== 'E' && core.ee !== 'E', 'TOK ' + core.tok + ', EE ' + core.ee],
      ['CAS completed', core.cas, core.cas ? 'done' : 'not done']
    ];
    var failed = checks.filter(function (c) { return !c[1]; });
    var pass = failed.length === 0;

    root.querySelector('.ib-total').textContent = total;
    root.querySelector('.ib-break').textContent = subjPts + ' from subjects + ' + cp + ' core point' + (cp === 1 ? '' : 's');
    root.querySelector('.ib-fill').style.width = (total / 45 * 100) + '%';
    var badge = root.querySelector('.ib-status');
    badge.textContent = pass ? 'Diploma awarded' : 'Diploma not awarded';
    root.querySelector('.ib-result').dataset.pass = pass ? 'yes' : 'no';
    root.querySelector('.ib-checks').innerHTML = checks.map(function (c) {
      return '<li class="' + (c[1] ? 'ok' : 'bad') + '"><span class="ib-tick" aria-hidden="true">' + (c[1] ? '✓' : '✕') + '</span><span>' + c[0] + '</span><b>' + c[2] + '</b></li>';
    }).join('');

    var mix = '';
    if (!((hl.length === 3 && sl.length === 3) || (hl.length === 4 && sl.length === 2))) {
      mix = 'Most diploma students take 3 HL and 3 SL, or 4 HL and 2 SL. You have ' + hl.length + ' HL and ' + sl.length + ' SL.';
    }
    root.querySelector('.ib-mix').textContent = mix;
    root.querySelector('.ib-mix').hidden = !mix;

    var gap = target - total;
    var t = root.querySelector('.ib-target-msg');
    if (gap <= 0) t.textContent = 'You are at or above your target of ' + target + '.';
    else {
      var room = subjects.reduce(function (a, s) { return a + (7 - s.grade); }, 0) + (3 - cp);
      t.textContent = gap > room ? 'A target of ' + target + ' is out of reach with these core grades.' :
        'You need ' + gap + ' more point' + (gap === 1 ? '' : 's') + ' for ' + target + '. That is ' + gap + ' grade step' + (gap === 1 ? '' : 's') + ' across your subjects or core.';
    }
  }

  ['tok', 'ee'].forEach(function (k) {
    root.querySelector('#ib-' + k).addEventListener('change', function (e) { core[k] = e.target.value; update(); });
  });
  root.querySelector('#ib-cas').addEventListener('change', function (e) { core.cas = e.target.checked; update(); });
  root.querySelector('#ib-target').addEventListener('change', function (e) { target = Number(e.target.value); update(); });
  root.querySelector('.ib-reset').addEventListener('click', function () {
    subjects.forEach(function (s, i) { s.grade = 7; s.level = i < 3 ? 'HL' : 'SL'; });
    core = { tok: 'A', ee: 'A', cas: true };
    root.querySelector('#ib-tok').value = 'A'; root.querySelector('#ib-ee').value = 'A'; root.querySelector('#ib-cas').checked = true;
    renderSubjects(); update();
  });
  renderSubjects();
  update();
})();
