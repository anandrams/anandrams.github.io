/* ------------------------------------------------------------------
   site.js — everything the pages need at runtime.

   Each block is independent and bails out quietly if its elements
   aren't on the page, so one missing feature never breaks the rest.
   Nothing here is required to read the site: the HTML works with
   JavaScript switched off.
   ------------------------------------------------------------------ */

(function () {
  'use strict';

  /* ---------- 1. theme toggle -------------------------------------
     The stored value wins over the OS preference. The pre-paint
     script in <head> has already applied it; this only handles the
     click and keeps the button's label honest.
     --------------------------------------------------------------- */

  var themeBtn = document.getElementById('theme-toggle');

  function currentTheme() {
    var set = document.documentElement.getAttribute('data-theme');
    if (set) return set;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function labelTheme() {
    if (!themeBtn) return;
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    themeBtn.setAttribute('aria-label', 'Switch to ' + next + ' theme');
  }

  if (themeBtn) {
    labelTheme();
    themeBtn.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      labelTheme();
    });
  }

  /* ---------- 2. collapsing nav (small screens) ------------------- */

  var navBtn = document.getElementById('nav-toggle');
  var nav = document.getElementById('nav');

  if (navBtn && nav) {
    navBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      navBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      navBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
  }

  /* ---------- 3. wide tables get their own scroll container -------
     kramdown emits a bare <table>; a wide one would otherwise push
     the article column sideways on a phone.
     --------------------------------------------------------------- */

  Array.prototype.forEach.call(document.querySelectorAll('.prose table'), function (table) {
    if (table.parentNode.classList.contains('table-scroll')) return;
    var box = document.createElement('div');
    box.className = 'table-scroll';
    table.parentNode.insertBefore(box, table);
    box.appendChild(table);
  });

  /* ---------- 3b. figure captions ---------------------------------
     In the source, the line under a figure is a paragraph in italics.
     Mark those paragraphs so they can be styled as captions — and only
     those, not a paragraph that merely contains an italic phrase.
     --------------------------------------------------------------- */

  Array.prototype.forEach.call(document.querySelectorAll('.prose p'), function (p) {
    if (p.children.length !== 1) return;
    var only = p.children[0];
    if (only.tagName !== 'EM') return;
    if (p.textContent.trim() !== only.textContent.trim()) return;
    p.classList.add('cap');
  });

  /* ---------- 4. display maths ------------------------------------
     kramdown hands LaTeX to the page as <script type="math/tex">.
     KaTeX renders it in place; if KaTeX fails to load, the raw
     LaTeX is simply not shown rather than shown broken.
     --------------------------------------------------------------- */

  /* Markdown engines disagree about what to do with $$...$$, and which
     one GitHub Pages uses has changed before. Rather than depend on it,
     collect every shape the LaTeX can arrive in, then render the lot. */

  function collectMath(root) {
    var found = [];

    function take(node, display, tex) {
      var holder = document.createElement(display ? 'div' : 'span');
      holder.className = 'math-src';
      holder.textContent = tex;
      node.parentNode.replaceChild(holder, node);
      found.push({ el: holder, display: display });
    }

    // Shape 1: kramdown's MathJax output, <script type="math/tex">.
    // The browser never displays these, so without this step the
    // equation is simply missing from the page.
    Array.prototype.forEach.call(
      root.querySelectorAll('script[type^="math/tex"]'),
      function (node) {
        take(node, /mode=display/.test(node.getAttribute('type') || ''), node.textContent);
      }
    );

    // Shape 2: kramdown with no math engine, <div class="math">.
    Array.prototype.forEach.call(
      root.querySelectorAll('div.math, span.math'),
      function (node) {
        var tex = node.textContent.trim()
          .replace(/^\$\$/, '').replace(/\$\$$/, '')
          .replace(/^\\\[/, '').replace(/\\\]$/, '');
        take(node, node.tagName === 'DIV', tex);
      }
    );

    return found;
  }

  function renderMath() {
    var katex = window.katex;

    collectMath(document).forEach(function (item) {
      if (!katex) {
        // KaTeX didn't load. Show the LaTeX source rather than dropping
        // the equation out of the page entirely.
        item.el.className = 'mathblock mathraw';
        return;
      }
      var holder = document.createElement(item.display ? 'div' : 'span');
      holder.className = item.display ? 'mathblock' : 'mathinline';
      try {
        katex.render(item.el.textContent.trim(), holder, {
          displayMode: item.display,
          throwOnError: false
        });
        item.el.parentNode.replaceChild(holder, item.el);
      } catch (e) {
        item.el.className = 'mathblock mathraw';
      }
    });

    // Shape 3: the markdown engine left $$...$$ sitting in the text.
    // KaTeX's own auto-render walks the text nodes and picks those up.
    // It skips pre and code, so a dollar sign in a code block is safe.
    if (window.renderMathInElement) {
      Array.prototype.forEach.call(document.querySelectorAll('.prose'), function (el) {
        try {
          window.renderMathInElement(el, {
            delimiters: [
              { left: '$$', right: '$$', display: true },
              { left: '\\[', right: '\\]', display: true },
              { left: '\\(', right: '\\)', display: false }
            ],
            ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'option'],
            throwOnError: false
          });
        } catch (e) {}
      });
    }
  }

  if (document.querySelector('.prose')) {
    if (typeof window.katex !== 'undefined') {
      renderMath();
    } else {
      // The KaTeX tags are deferred too; wait for them before giving up.
      window.addEventListener('load', renderMath);
    }
  }

  /* ---------- 5. reading progress --------------------------------- */

  var bar = document.getElementById('readbar');

  if (bar) {
    var fill = bar.querySelector('i');
    var ticking = false;

    function progress() {
      var doc = document.documentElement;
      var scrollable = doc.scrollHeight - window.innerHeight;
      var pct = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
      pct = Math.max(0, Math.min(100, pct));
      fill.style.width = pct.toFixed(1) + '%';
      bar.setAttribute('aria-valuenow', Math.round(pct));
      ticking = false;
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(progress);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    progress();
  }

  /* ---------- 6. table of contents: mark the section in view ------ */

  var toc = document.querySelector('.toc');

  if (toc && 'IntersectionObserver' in window) {
    var links = {};
    Array.prototype.forEach.call(toc.querySelectorAll('a[href^="#"]'), function (a) {
      links[a.getAttribute('href').slice(1)] = a;
    });

    var headings = Object.keys(links)
      .map(function (id) { return document.getElementById(id); })
      .filter(Boolean);

    if (headings.length) {
      var seen = [];

      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          var id = entry.target.id;
          var at = seen.indexOf(id);
          if (entry.isIntersecting && at === -1) seen.push(id);
          if (!entry.isIntersecting && at !== -1) seen.splice(at, 1);
        });

        // The topmost heading currently on screen wins; if none are,
        // keep the last one that was.
        if (!seen.length) return;
        var best = headings.filter(function (h) { return seen.indexOf(h.id) !== -1; })[0];
        if (!best) return;

        Object.keys(links).forEach(function (id) {
          links[id].classList.toggle('on', id === best.id);
        });
      }, { rootMargin: '-80px 0px -60% 0px' });

      headings.forEach(function (h) { obs.observe(h); });
    }
  }

  /* ---------- 7. filters (Writing index, Projects index) ----------
     Markup contract:
       [data-filter-scope]            wrapper for one filterable set
         [data-group="format"]          a row of buttons
           button[data-value="Essay"]   "" (or absent) means "all"
         [data-filter-search] input     free-text box (optional)
         [data-filter-count]            "N of M" readout (optional)
         [data-item]                    each filterable item, carrying
                                        data-format / data-series /
                                        data-theme (space-separated,
                                        multiple values allowed)
     --------------------------------------------------------------- */

  Array.prototype.forEach.call(document.querySelectorAll('[data-filter-scope]'), function (scope) {
    var items = Array.prototype.slice.call(scope.querySelectorAll('[data-item]'));
    var groups = Array.prototype.slice.call(scope.querySelectorAll('[data-group]'));
    var search = scope.querySelector('[data-filter-search]');
    var count = scope.querySelector('[data-filter-count]');
    var empty = scope.querySelector('[data-filter-empty]');

    if (!items.length) return;

    // The chosen value for each group, '' meaning no filter.
    var chosen = {};
    groups.forEach(function (g) { chosen[g.getAttribute('data-group')] = ''; });

    function matches(item) {
      var ok = Object.keys(chosen).every(function (group) {
        var want = chosen[group];
        if (!want) return true;
        var have = (item.getAttribute('data-' + group) || '').split(/\s*\|\s*/);
        return have.indexOf(want) !== -1;
      });

      if (ok && search && search.value.trim()) {
        var needle = search.value.trim().toLowerCase();
        ok = (item.textContent + ' ' + (item.getAttribute('data-keywords') || ''))
          .toLowerCase()
          .indexOf(needle) !== -1;
      }

      return ok;
    }

    function apply() {
      var shown = 0;
      items.forEach(function (item) {
        var on = matches(item);
        item.hidden = !on;
        if (on) shown++;
      });
      if (count) {
        var nouns = (scope.getAttribute('data-filter-noun') || 'entry|entries').split('|');
        count.textContent = shown === items.length
          ? items.length + ' ' + (items.length === 1 ? nouns[0] : nouns[1])
          : shown + ' of ' + items.length;
      }
      if (empty) empty.hidden = shown !== 0;
    }

    groups.forEach(function (group) {
      var name = group.getAttribute('data-group');
      var buttons = Array.prototype.slice.call(group.querySelectorAll('button[data-value]'));

      buttons.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var value = btn.getAttribute('data-value') || '';
          // Clicking the active filter again clears it.
          chosen[name] = (chosen[name] === value) ? '' : value;
          buttons.forEach(function (b) {
            var v = b.getAttribute('data-value') || '';
            b.setAttribute('aria-pressed', v === chosen[name] ? 'true' : 'false');
          });
          apply();
        });
      });

      // "All" starts pressed.
      buttons.forEach(function (b) {
        var v = b.getAttribute('data-value') || '';
        b.setAttribute('aria-pressed', v === '' ? 'true' : 'false');
      });
    });

    if (search) {
      search.addEventListener('input', apply);
      search.addEventListener('search', apply);
    }

    apply();
  });

})();
