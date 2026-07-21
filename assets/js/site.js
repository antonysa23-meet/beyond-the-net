// Beyond the Net — navigation, "More" dropdown, and site search
(function () {
  'use strict';

  var BASE = window.SITE_BASE || '';

  // ------------------------------------------------------------ mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
  }

  // --------------------------------------------------------- More dropdown
  var moreBtn = document.querySelector('.nav__more-btn');
  var moreWrap = document.querySelector('.nav__more');

  if (moreBtn && moreWrap) {
    moreBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = moreBtn.getAttribute('aria-expanded') === 'true';
      moreBtn.setAttribute('aria-expanded', String(!open));
      moreWrap.classList.toggle('is-open', !open);
    });

    document.addEventListener('click', function (e) {
      if (!moreWrap.contains(e.target)) {
        moreBtn.setAttribute('aria-expanded', 'false');
        moreWrap.classList.remove('is-open');
      }
    });
  }

  // ---------------------------------------------------------------- search
  var panel = document.getElementById('search-panel');
  var input = document.getElementById('search-input');
  var results = document.getElementById('search-results');
  var openBtns = document.querySelectorAll('[data-search-open]');
  var closeBtn = document.querySelector('[data-search-close]');

  var docs = null;
  var loading = false;
  var lastFocused = null;
  var GROUPS = ['Services', 'Events', 'Blog Posts', 'Pages'];

  function loadIndex() {
    if (docs || loading) return Promise.resolve(docs);
    loading = true;
    return fetch(BASE + 'assets/search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (j) { docs = j; loading = false; return docs; })
      .catch(function () { loading = false; return []; });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function score(doc, terms) {
    var title = doc.title.toLowerCase();
    var text = doc.text.toLowerCase();
    var total = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      if (title.indexOf(t) !== -1) total += 10;
      else if (text.indexOf(t) !== -1) total += 3;
      else return 0; // every term must appear somewhere
    }
    return total;
  }

  function render(query) {
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);

    // With no query, show a sample of each group — same as the Wix panel's default
    var matches = terms.length
      ? docs.map(function (d) { return { d: d, s: score(d, terms) }; })
            .filter(function (x) { return x.s > 0; })
            .sort(function (a, b) { return b.s - a.s; })
            .map(function (x) { return x.d; })
      : docs.slice();

    if (!matches.length) {
      results.innerHTML = '<p class="search-panel__empty">No results for &ldquo;' +
        escapeHtml(query) + '&rdquo;</p>';
      return;
    }

    var html = '';
    GROUPS.forEach(function (group) {
      var inGroup = matches.filter(function (d) { return d.t === group; });
      if (!inGroup.length) return;
      if (!terms.length) inGroup = inGroup.slice(0, 3);

      html += '<section class="search-group"><h2 class="search-group__title">' +
        group + '</h2><div class="search-group__items">';

      inGroup.forEach(function (d) {
        var media = d.img
          ? '<img src="' + BASE + escapeHtml(d.img) + '" alt="" loading="lazy">'
          : '<span class="search-hit__placeholder" aria-hidden="true"></span>';
        html += '<a class="search-hit" href="' + BASE + escapeHtml(d.url) + '">' +
          media +
          '<span class="search-hit__text">' +
            '<span class="search-hit__title">' + escapeHtml(d.title) + '</span>' +
            '<span class="search-hit__desc">' + escapeHtml(d.desc) + '</span>' +
          '</span></a>';
      });

      html += '</div></section>';
    });

    results.innerHTML = html;
  }

  function openPanel() {
    lastFocused = document.activeElement;
    panel.hidden = false;
    document.body.classList.add('search-open');
    loadIndex().then(function () { render(input.value.trim()); });
    input.focus();
  }

  function closePanel() {
    panel.hidden = true;
    document.body.classList.remove('search-open');
    if (lastFocused) lastFocused.focus();
  }

  if (panel && input && results) {
    Array.prototype.forEach.call(openBtns, function (b) {
      b.addEventListener('click', openPanel);
    });
    if (closeBtn) closeBtn.addEventListener('click', closePanel);

    var timer;
    input.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        if (docs) render(input.value.trim());
      }, 120);
    });

    // Keep focus inside the panel while it's open
    panel.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var focusable = panel.querySelectorAll('input, button, a[href]');
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });
  }

  // Escape closes whichever layer is open
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (panel && !panel.hidden) {
      closePanel();
    } else if (moreWrap && moreWrap.classList.contains('is-open')) {
      moreBtn.setAttribute('aria-expanded', 'false');
      moreWrap.classList.remove('is-open');
      moreBtn.focus();
    } else if (nav && nav.classList.contains('is-open')) {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });
})();
