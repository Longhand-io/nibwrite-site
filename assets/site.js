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

  // ---- Gall the guide ----
  var guide = document.getElementById('guide'), say = document.getElementById('say');
  var stops = Array.prototype.slice.call(document.querySelectorAll('[data-gall]'));
  var home = document.querySelector('.bar .gall-l');
  if (!guide || !home || !stops.length || reduce || window.innerWidth < 1100) return;
  var REST = Math.atan2(20 - 50, 94 - 62) * 180 / Math.PI - 10; // the wand's resting direction
  var at = null, current = null, sayTimer = null, outOfWord = false;

  function homePoint() { var r = home.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height * .7 }; }
  function place(p, ms) {
    guide.style.transitionDuration = (ms || 0) + 'ms, 300ms';
    guide.classList.toggle('ride', ms > 0);
    guide.style.transform = 'translate(' + p.x + 'px,' + p.y + 'px)';
    at = p;
    if (ms) setTimeout(function () { guide.classList.remove('ride'); }, ms);
  }
  function aim(p, tx, ty) {
    var flip = tx < p.x;
    guide.classList.toggle('flip', flip);
    var sx = p.x + (flip ? -6 : 6), sy = p.y - 11;
    var want = Math.atan2(ty - sy, tx - sx) * 180 / Math.PI;
    var local = flip ? 180 - want : want;
    var d = ((local - REST + 540) % 360) - 180;
    var wand = guide.querySelector('.wand'); if (wand) wand.setAttribute('transform', 'rotate(' + d.toFixed(1) + ' 62 50)');
  }
  function perchFor(el) {
    // stand in the right-hand gutter beside the section's heading, pointing at it
    var h = el.querySelector('h1, h2, .typed') || el, r = h.getBoundingClientRect(), wrap = el.getBoundingClientRect();
    var x = Math.min(window.innerWidth - 60, Math.max(wrap.right, r.right) + 70);
    if (x > window.innerWidth - 60) x = window.innerWidth - 60;
    var y = Math.max(110, Math.min(window.innerHeight - 80, r.top + r.height / 2 + 10));
    return { p: { x: x, y: y }, tx: r.left + Math.min(r.width, 520) * .55, ty: r.top + r.height / 2 };
  }
  function speak(text, p) {
    if (!say || !text) return;
    say.textContent = text;
    var w = Math.min(230, say.offsetWidth || 230);
    say.style.left = Math.max(12, p.x - w - 44) + 'px';
    say.style.top = (p.y - 70) + 'px';
    say.classList.add('show');
    clearTimeout(sayTimer); sayTimer = setTimeout(function () { say.classList.remove('show'); }, 3600);
  }
  function goTo(el) {
    if (current === el) return;
    current = el;
    if (!el) { // back home into the word
      say.classList.remove('show');
      place(homePoint(), 800);
      setTimeout(function () { if (!current) { guide.classList.remove('show'); home.classList.remove('away'); outOfWord = false; } }, 800);
      return;
    }
    if (!outOfWord) { home.classList.add('away'); place(homePoint(), 0); guide.classList.add('show'); outOfWord = true; }
    var t = perchFor(el);
    requestAnimationFrame(function () { place(t.p, 900); aim(t.p, t.tx, t.ty); });
    setTimeout(function () { if (current === el) speak(el.dataset.gall, t.p); }, 900);
  }
  function pick() {
    if (window.scrollY < 140) return goTo(null);
    var mid = window.innerHeight * .42, best = null, bestD = 1e9;
    stops.forEach(function (el) { var r = el.getBoundingClientRect(); if (r.bottom < 80 || r.top > window.innerHeight - 80) return; var d = Math.abs(r.top + Math.min(r.height, 300) / 2 - mid); if (d < bestD) { bestD = d; best = el; } });
    goTo(best);
  }
  var queued = false;
  addEventListener('scroll', function () { if (queued) return; queued = true; requestAnimationFrame(function () { queued = false; pick(); if (current && !guide.classList.contains('ride')) { var t = perchFor(current); place(t.p, 0); aim(t.p, t.tx, t.ty); } }); }, { passive: true });
  addEventListener('resize', pick);
  // re-aim smoothly after a section change settles
  setInterval(function () { if (current && !guide.classList.contains('ride')) { var t = perchFor(current); place(t.p, 0); aim(t.p, t.tx, t.ty); } }, 400);
  pick();
})();
