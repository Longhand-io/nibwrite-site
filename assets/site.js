// Oakfall site: the theme toggle, the typed banner, the snapshot tint, Gall's life in the word,
// and Gall the guide, who steps out of the word and follows the reader down the page.
(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- theme: Moss light by default; forest dark on request ----
  var btn = document.getElementById('theme');
  var cur = 'light';
  try { cur = localStorage.getItem('oakfall.theme') === 'dark' ? 'dark' : 'light'; } catch (e) {}
  function applyTheme() {
    if (cur === 'dark') root.setAttribute('data-theme', 'dark'); else root.removeAttribute('data-theme');
    if (btn) { btn.textContent = cur === 'dark' ? 'Light' : 'Dark'; btn.setAttribute('aria-label', cur === 'dark' ? 'Switch to light' : 'Switch to dark'); }
    document.querySelectorAll('img[data-light]').forEach(function (img) { img.src = cur === 'dark' ? img.dataset.dark : img.dataset.light; });
  }
  if (btn) btn.addEventListener('click', function () { cur = cur === 'dark' ? 'light' : 'dark'; try { localStorage.setItem('oakfall.theme', cur); } catch (e) {} applyTheme(); });
  applyTheme();

  // ---- the typed banner ----
  var word = document.querySelector('.typed .word');
  if (word) {
    var words = (word.dataset.words || word.textContent).split('|');
    if (reduce) { word.textContent = words[words.length - 1]; }
    else {
      var wi = 0, ci = words[0].length, deleting = false;
      word.textContent = words[0];
      var tick = function () {
        var w = words[wi];
        if (!deleting) {
          if (ci < w.length) { ci++; word.textContent = w.slice(0, ci); return setTimeout(tick, 85 + Math.random() * 60); }
          deleting = true; return setTimeout(tick, wi === words.length - 1 ? 3600 : 1700);
        }
        if (ci > 0) { ci--; word.textContent = w.slice(0, ci); return setTimeout(tick, 38); }
        deleting = false; wi = (wi + 1) % words.length; setTimeout(tick, 260);
      };
      setTimeout(function () { deleting = true; tick(); }, 2200);
    }
  }

  // ---- the snapshot tints in once it is seen ----
  var cmp = document.getElementById('compare');
  if (cmp) {
    if (reduce || !('IntersectionObserver' in window)) cmp.classList.remove('quiet');
    else new IntersectionObserver(function (es, o) { es.forEach(function (e) { if (e.isIntersecting) { setTimeout(function () { cmp.classList.remove('quiet'); }, 300); o.disconnect(); } }); }, { threshold: .4 }).observe(cmp);
  }

  // ---- Gall in the word: blinks, turns over like a leaf ----
  var ls = Array.prototype.slice.call(document.querySelectorAll('.gall-l'));
  function turn(el) { el.classList.remove('turn'); void el.offsetWidth; el.classList.add('turn'); setTimeout(function () { el.classList.remove('turn'); }, 1500); }
  function blink(el) { el.classList.add('blink'); setTimeout(function () { el.classList.remove('blink'); }, 130); }
  ls.forEach(function (el) { el.addEventListener('click', function (ev) { ev.preventDefault(); turn(el); }); });
  if (!reduce) {
    setTimeout(function () { ls.forEach(turn); }, 900);
    (function life() { setTimeout(function () { ls.forEach(function (el) { if (!el.classList.contains('away')) (Math.random() < .18 ? turn : blink)(el); }); life(); }, 3200 + Math.random() * 3500); })();
  }

  // ---- Gall the guide: one frame loop chases his spot, so scrolling never jumps ----
  var guide = document.getElementById('guide'), say = document.getElementById('say');
  var stops = Array.prototype.slice.call(document.querySelectorAll('[data-gall]'));
  var home = document.querySelector('.bar .gall-l');
  if (!guide || !home || !stops.length || reduce || window.innerWidth < 1100) return;
  var REST = Math.atan2(20 - 50, 94 - 62) * 180 / Math.PI - 10; // the wand's resting direction
  var wand = guide.querySelector('.wand');
  var pos = null, current = null, out = false, last = 0, sayTimer = null, spoken = null, flipped = false, angle = 0;

  function homePoint() { var r = home.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height * .7 }; }
  function spotFor(el) {
    var h = el.querySelector('h1, h2, .typed') || el, r = h.getBoundingClientRect(), w = el.getBoundingClientRect();
    var x = Math.min(window.innerWidth - 56, Math.max(w.right, r.right) + 70);
    var y = Math.max(160, Math.min(window.innerHeight - 70, r.top + r.height / 2 + 10));
    return { x: x, y: y, tx: r.left + Math.min(r.width, 520) * .55, ty: r.top + r.height / 2 };
  }
  function pick() {
    if (window.scrollY < 140) return null;
    var mid = window.innerHeight * .42, best = null, bestD = 1e9;
    for (var i = 0; i < stops.length; i++) {
      var r = stops[i].getBoundingClientRect();
      if (r.bottom < 80 || r.top > window.innerHeight - 80) continue;
      var d = Math.abs(r.top + Math.min(r.height, 300) / 2 - mid);
      if (d < bestD) { bestD = d; best = stops[i]; }
    }
    return best;
  }
  function speak(el) {
    if (spoken === el) return;
    spoken = el;
    clearTimeout(sayTimer);
    say.classList.remove('show');
    if (!el) return;
    sayTimer = setTimeout(function () { say.textContent = el.dataset.gall; say.classList.add('show'); sayTimer = setTimeout(function () { say.classList.remove('show'); }, 3400); }, 420);
  }
  function frame(t) {
    var dt = Math.min(64, t - (last || t)); last = t;
    var next = pick();
    if (next !== current) { current = next; speak(next); }
    var target;
    if (current) {
      var sp = spotFor(current);
      target = sp;
      if (!out) { out = true; home.classList.add('away'); pos = homePoint(); guide.classList.add('show'); }
    } else {
      target = homePoint();
    }
    if (out && pos) {
      // exponential chase: about 90 ms to close most of the gap, at any frame rate
      var k = 1 - Math.exp(-dt / 90);
      pos.x += (target.x - pos.x) * k;
      pos.y += (target.y - pos.y) * k;
      var dist = Math.hypot(target.x - pos.x, target.y - pos.y);
      guide.classList.toggle('ride', dist > 6);
      guide.style.transform = 'translate3d(' + pos.x.toFixed(1) + 'px,' + pos.y.toFixed(1) + 'px,0)';
      // face and aim at the heading, easing the arm round
      if (current) {
        var flip = target.tx < pos.x;
        if (flip !== flipped) { flipped = flip; guide.classList.toggle('flip', flip); }
        var sx = pos.x + (flip ? -7 : 7), sy = pos.y - 13;
        var want = Math.atan2(target.ty - sy, target.tx - sx) * 180 / Math.PI;
        var local = flip ? 180 - want : want;
        var d = ((local - REST + 540) % 360) - 180;
        angle += (d - angle) * Math.min(1, k * 1.4);
        wand.setAttribute('transform', 'rotate(' + angle.toFixed(1) + ' 62 50)');
        say.style.left = Math.max(12, pos.x - say.offsetWidth - 46) + 'px';
        say.style.top = (pos.y - 74) + 'px';
      } else if (dist < 3) {
        // home: he becomes the l again
        out = false; guide.classList.remove('show', 'ride'); home.classList.remove('away');
      }
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
