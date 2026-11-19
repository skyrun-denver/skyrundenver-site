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
    if (!sessionStorage.getItem('sr_landing_page')) sessionStorage.setItem('sr_landing_page', location.origin + location.pathname + location.search);
  } catch (e) {}
  document.querySelectorAll('form.eval').forEach(function (form) {
    keys.forEach(function (k) {
      var f = form.querySelector('input[name="' + k + '"]');
      var v = null;
      try { v = sessionStorage.getItem('sr_' + k); } catch (e) {}
      if (f && v) f.value = v;
    });
    var lp = form.querySelector('input[name="skyrun_inquiry_landing_page"]');
    var here = location.origin + location.pathname;
    if (lp) { try { lp.value = sessionStorage.getItem('sr_landing_page') || here; } catch (e) { lp.value = here; } }
    form.addEventListener('submit', function (ev) {
      if (form.dataset.sent) return;            // second pass: let the Netlify post go through
      ev.preventDefault();
      var err = form.querySelector('.form-err');
      if (!form.checkValidity()) {
        var bad = form.querySelector(':invalid');
        if (err) { err.textContent = 'Please complete the highlighted fields.'; err.hidden = false; }
        if (bad) { bad.scrollIntoView({ block: 'center' }); }
        form.reportValidity();
        return;
      }
      var trap = form.querySelector('input[name="bot-field"]');
      if (trap && trap.value) { form.dataset.sent = '1'; HTMLFormElement.prototype.submit.call(form); return; }   // bots: Netlify files it as spam
      var b = form.querySelector('button[type=submit]');
      if (b) { b.disabled = true; b.textContent = 'Sending'; }
      if (err) err.hidden = true;
      var names = ['firstname', 'lastname', 'email', 'phone', 'skyrun_property_city', 'skyrun_property_type', 'skyrun_rental_strategy',
                   'skyrun_start_window', 'skyrun_discovery_channel', 'message', 'skyrun_inquiry_landing_page'];
      var fields = [];
      names.forEach(function (n) {
        var el = form.elements[n];
        if (el && el.value) fields.push({ objectTypeId: '0-1', name: n, value: el.value });
      });
      var hutk = (document.cookie.match(/(?:^|; )hubspotutk=([^;]+)/) || [])[1];
      var ctx = { pageUri: location.href, pageName: document.title };
      if (hutk) ctx.hutk = hutk;
      var done = false;
      var finish = function () {
        if (done) return; done = true;
        try { window.dataLayer = window.dataLayer || []; window.dataLayer.push({ event: 'generate_lead', form: 'property_evaluation', city: form.elements.skyrun_property_city.value }); } catch (e) {}
        try {   // Ad and analytics conversions; each fires only when its tag is on the page (see tags() in build_site.py)
          var city = form.elements.skyrun_property_city.value;
          if (window.gtag) {
            window.gtag('event', 'generate_lead', { form: 'property_evaluation', city: city });
            if (window.SRD_ADS_LEAD) window.gtag('event', 'conversion', { send_to: window.SRD_ADS_LEAD });
          }
          if (window.fbq) window.fbq('track', 'Lead', { content_name: 'property_evaluation' });
        } catch (e) {}
        form.dataset.sent = '1';
        HTMLFormElement.prototype.submit.call(form);   // Netlify copy and the thank you page
      };
      var url = 'https://api.hsforms.com/submissions/v3/integration/submit/' + form.dataset.hsPortal + '/' + form.dataset.hsForm;
      try {
        fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, keepalive: true,
          body: JSON.stringify({ fields: fields, context: ctx }) })
          .then(function (r) { if (!r.ok && window.console) console.warn('HubSpot submission', r.status); })
          .catch(function () {})
          .then(finish);
      } catch (e) { finish(); }
      setTimeout(finish, 4000);
    });
  });

  // City links and chips fill the form's city field.
  var citySel = document.getElementById('city');
  var formTitle = document.getElementById('ft');
  function setCity(name, scroll) {
    if (!citySel) return;
    var opt = Array.prototype.find.call(citySel.options, function (o) { return o.text === name || o.value === name; });
    citySel.value = opt ? opt.value : '';
    if (opt) name = opt.text;
    if (formTitle && formTitle.firstChild && formTitle.firstChild.nodeType === 3) formTitle.firstChild.nodeValue = name && name !== 'Another Denver Metro city' ? 'Tell us about your ' + name + ' property.' : 'Tell us about your property.';
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
  if (citySel) citySel.addEventListener('change', function () { if (citySel.value) setCity(citySel.options[citySel.selectedIndex].text, false); });

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
