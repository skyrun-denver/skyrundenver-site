/* SkyRun Denver site script. v0.1. No dependencies. */
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
  var m = document.querySelector('.mcta'), t = document.getElementById('evaluation');
  if (m && t && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (e) { m.style.visibility = e[0].isIntersecting ? 'hidden' : 'visible'; }, { threshold: 0.05 }).observe(t);
  }

  // One reveal per section heading.
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) { entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, { threshold: 0.3 });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }
})();
