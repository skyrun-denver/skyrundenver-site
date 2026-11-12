/* SkyRun Denver site script. v0.3. No dependencies. */
(function () {
  'use strict';

  // Carry campaign parameters into the form's hidden fields and remember them for later pages.
  var params = new URLSearchParams(location.search);
  var keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid'];
  try {
    keys.forEach(function (k) {
      if (params.get(k)) sessionStorage.setItem('sr_' + k, params.get(k));
    });
    if (!sessionStorage.getItem('sr_landing_page')) sessionStorage.setItem('sr_landing_page', location.pathname);
  } catch (e) {}
  document.querySelectorAll('form.eval').forEach(function (form) {
    keys.forEach(function (k) {
      var f = form.querySelector('input[name="' + k + '"]');
      var v = null;
      try { v = sessionStorage.getItem('sr_' + k); } catch (e) {}
      if (f && v) f.value = v;
    });
    var lp = form.querySelector('input[name="landing_page"]');
    if (lp) { try { lp.value = sessionStorage.getItem('sr_landing_page') || location.pathname; } catch (e) { lp.value = location.pathname; } }
    form.addEventListener('submit', function () {
      var b = form.querySelector('button[type=submit]');
      if (b) { b.disabled = true; b.textContent = 'Sending'; }
    });
  });

  // City links and chips fill the form's city field.
  var citySel = document.getElementById('city');
  var formTitle = document.getElementById('ft');
  function setCity(name, scroll) {
    if (!citySel) return;
    citySel.value = name;
    if (formTitle) formTitle.textContent = name && name !== 'Outside these cities' ? 'Request a property evaluation for your ' + name + ' home.' : 'Request a property evaluation.';
    document.querySelectorAll('.chip').forEach(function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-city') === name ? 'true' : 'false'); });
    document.querySelectorAll('.map .city').forEach(function (c) { c.classList.toggle('on', c.getAttribute('data-city') === name); });
    if (scroll) {
      var target = document.getElementById('evaluation');
      if (target) target.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      setTimeout(function () { var f = document.getElementById('first'); if (f) f.focus({ preventScroll: true }); }, 700);
    }
  }
  document.querySelectorAll('a[data-city]').forEach(function (a) { a.addEventListener('click', function () { setCity(a.getAttribute('data-city'), false); }); });
  document.querySelectorAll('.chip[data-city]').forEach(function (c) { c.addEventListener('click', function () { setCity(c.getAttribute('data-city'), true); }); });
  document.querySelectorAll('.map .city').forEach(function (c) {
    c.setAttribute('tabindex', '0'); c.setAttribute('role', 'button');
    c.addEventListener('click', function () { setCity(c.getAttribute('data-city'), true); });
    c.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setCity(c.getAttribute('data-city'), true); } });
  });
  if (citySel) citySel.addEventListener('change', function () { if (citySel.value) setCity(citySel.value, false); });

  // Phone CTA hides when the form is on screen.
  var m = document.querySelector('.mcta'), t = document.getElementById('evaluation'), hp = document.querySelector('.hero-photo');
  if (m && 'IntersectionObserver' in window) {
    var hide = { form: false, hero: false };
    var apply = function () { m.style.visibility = (hide.form || hide.hero) ? 'hidden' : 'visible'; };
    if (t) new IntersectionObserver(function (e) { hide.form = e[0].isIntersecting; apply(); }, { threshold: 0.05 }).observe(t);
    if (hp) new IntersectionObserver(function (e) { hide.hero = e[0].isIntersecting; apply(); }, { threshold: 0.15 }).observe(hp);
  }


  // Header over the photo hero turns solid once the hero scrolls away. Mobile menu toggle.
  var head = document.querySelector('.site-head');
  if (head && head.classList.contains('over')) {
    var onScroll = function () { head.classList.toggle('solid', window.scrollY > 40); };
    onScroll(); addEventListener('scroll', onScroll, { passive: true });
  }
  var menu = document.querySelector('.menu'), nav = document.getElementById('nav');
  if (menu && nav) {
    menu.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menu.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (head) head.classList.toggle('solid', open || window.scrollY > 40);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { if (nav.classList.contains('open')) menu.click(); }); });
  }

  // Owner review carousel: native scroll snap, buttons and dots just move it.
  var car = document.querySelector('.carousel');
  if (car) {
    var track = car.querySelector('.slides'), slides = track.children, dots = car.querySelectorAll('.dots button');
    var go = function (i) { i = (i + slides.length) % slides.length; track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); };
    var cur = function () { return Math.round(track.scrollLeft / track.clientWidth); };
    car.querySelector('.prev').addEventListener('click', function () { go(cur() - 1); });
    car.querySelector('.next').addEventListener('click', function () { go(cur() + 1); });
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); }); });
    track.addEventListener('scroll', function () { var i = cur(); dots.forEach(function (d, k) { if (k === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); }); }, { passive: true });
  }

  // One reveal per section heading.
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) { entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, { threshold: 0.3 });
    rv.forEach(function (el) { if (el.closest('.hero-photo')) { requestAnimationFrame(function(){ el.classList.add('in'); }); } else { io.observe(el); } });
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }
})();
