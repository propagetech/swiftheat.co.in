/* Swiftheat — one script for the whole site.
   Four small, independent pieces: the mobile nav, the product finder, the
   enquiry form that composes a readable email, and the photograph gallery.
   Nothing here is required for the content to be readable; the page works
   with the script blocked. */
(function () {
  'use strict';

  document.documentElement.classList.remove('nojs');

  /* ---------- mobile navigation ---------- */
  (function nav() {
    var btn = document.querySelector('.navtoggle');
    var panel = document.getElementById('mainnav');
    if (!btn || !panel) return;

    function closed() { return btn.getAttribute('aria-expanded') !== 'true'; }
    function set(open) {
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      panel.hidden = !open;
    }
    // The nav is only ever hidden on touch widths. Above that the media query
    // shows it regardless, so the hidden attribute has to come off again.
    var mq = window.matchMedia('(max-width:980px)');
    function sync() { set(!mq.matches ? true : false); }
    if (mq.addEventListener) mq.addEventListener('change', sync);
    sync();

    btn.addEventListener('click', function () { set(closed()); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !closed() && mq.matches) { set(false); btn.focus(); }
    });
  })();

  /* ---------- product finder ---------- */
  (function finder() {
    var form = document.getElementById('finder');
    if (!form) return;
    var items = Array.prototype.slice.call(document.querySelectorAll('#productList > li'));
    var count = document.getElementById('finderCount');
    var selects = Array.prototype.slice.call(form.querySelectorAll('select'));

    function matches(li) {
      return selects.every(function (s) {
        if (!s.value) return true;
        var have = (li.getAttribute('data-' + s.getAttribute('data-facet')) || '').split('|');
        return have.indexOf(s.value) > -1;
      });
    }
    function apply() {
      var shown = 0;
      items.forEach(function (li) {
        var ok = matches(li);
        li.hidden = !ok;
        if (ok) shown++;
      });
      if (count) {
        if (shown === 0) {
          count.textContent = 'Nothing matches every filter. Clear one, or describe the '
            + 'application and we will propose an element type.';
        } else if (shown === items.length) {
          count.textContent = 'Showing all ' + items.length + ' product families.';
        } else {
          count.textContent = 'Showing ' + shown + ' of ' + items.length + ' product families.';
        }
      }
    }
    form.addEventListener('change', apply);
    form.addEventListener('submit', function (e) { e.preventDefault(); apply(); });
    var reset = document.getElementById('finderReset');
    if (reset) reset.addEventListener('click', function () {
      selects.forEach(function (s) { s.value = ''; });
      apply();
    });
    apply();
  })();

  /* ---------- enquiry form ---------- */
  /* Reads whatever fieldsets the page happens to carry, so one function serves
     the scoped form on every product page, every industry page and the contact
     page. The composed message goes to the visitor's own mail application: no
     server, no database, nothing stored anywhere. */
  (function rfq() {
    var form = document.getElementById('rfqForm');
    if (!form) return;
    var pre = document.getElementById('mailPreview');
    var btn = document.getElementById('composeBtn');
    var to = form.getAttribute('data-to') || 'sales@swiftheat.co.in';
    var subject = form.getAttribute('data-subject') || 'Website enquiry';
    var heading = form.getAttribute('data-heading') || 'ENQUIRY';

    function labelFor(el) {
      var id = el.id;
      var lab = id ? form.querySelector('label[for="' + id + '"]') : null;
      var text = lab ? lab.textContent : (el.getAttribute('aria-label') || el.name || '');
      return text.replace(/\*/g, '').replace(/\s+/g, ' ').trim();
    }
    function pad(label, width) {
      while (label.length < width) label += ' ';
      return label;
    }
    function compose() {
      var lines = [heading.toUpperCase(), ''];
      var any = false;
      Array.prototype.forEach.call(form.querySelectorAll('fieldset'), function (fs) {
        var rows = [];
        Array.prototype.forEach.call(fs.querySelectorAll('input,select,textarea'), function (el) {
          if (el.type === 'button' || el.type === 'submit') return;
          var v = (el.value || '').trim();
          if (el.type === 'checkbox' && !el.checked) return;
          if (el.type === 'checkbox') v = 'Yes';
          if (!v) return;
          rows.push('  ' + pad(labelFor(el), 24) + v);
          any = true;
        });
        if (rows.length) {
          var lg = fs.querySelector('legend');
          var name = lg ? lg.textContent.replace(/^\s*\d+\s*/, '').trim() : '';
          lines.push(name.toUpperCase());
          lines = lines.concat(rows);
          lines.push('');
        }
      });
      if (!any) return null;
      lines.push('Sent from swiftheat.co.in');
      return lines.join('\n');
    }
    function refresh() {
      if (!pre) return;
      pre.textContent = compose() || 'Fill in the form and the enquiry appears here.';
    }
    form.addEventListener('input', refresh);
    form.addEventListener('change', refresh);
    form.addEventListener('submit', function (e) { e.preventDefault(); send(); });

    function send() {
      var body = compose();
      if (!body) { refresh(); return; }
      var comp = form.querySelector('[name="Company"]');
      var sub = subject + (comp && comp.value.trim() ? ' from ' + comp.value.trim() : '');
      window.location.href = 'mailto:' + to
        + '?subject=' + encodeURIComponent(sub)
        + '&body=' + encodeURIComponent(body);
    }
    if (btn) btn.addEventListener('click', send);
    refresh();
  })();

  /* ---------- photograph gallery ---------- */
  /* Each [data-gallery] is one set. Tiles are ordinary links, so with the
     script blocked they still open the picture. With it, they open a dialog
     you can slide left and right, with the keyboard and with a swipe. */
  (function gallery() {
    var groups = Array.prototype.slice.call(document.querySelectorAll('[data-gallery]'));
    if (!groups.length || typeof HTMLDialogElement !== 'function') return;

    var dlg = document.createElement('dialog');
    dlg.className = 'gallery';
    dlg.setAttribute('aria-label', 'Product photographs');
    dlg.innerHTML =
      '<div class="gallery-bar">'
      + '<p class="gallery-count"></p>'
      + '<button type="button" class="gallery-close" aria-label="Close">'
      + '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">'
      + '<path d="M2 2l10 10M12 2L2 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
      + '</svg></button></div>'
      + '<div class="gallery-stage-wrap">'
      + '<button type="button" class="gallery-prev" aria-label="Previous photograph">'
      + '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">'
      + '<path d="M9 2L4 7l5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
      + '</svg></button>'
      + '<div class="gallery-stage"><div class="gallery-track"></div></div>'
      + '<button type="button" class="gallery-next" aria-label="Next photograph">'
      + '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">'
      + '<path d="M5 2l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
      + '</svg></button></div>'
      + '<p class="gallery-cap" aria-live="polite"></p>';
    document.body.appendChild(dlg);

    var track = dlg.querySelector('.gallery-track');
    var stage = dlg.querySelector('.gallery-stage');
    var countEl = dlg.querySelector('.gallery-count');
    var capEl = dlg.querySelector('.gallery-cap');
    var slides = [];
    var index = 0;
    var startX = 0;

    function imageLinks(group) {
      return Array.prototype.filter.call(group.querySelectorAll('a[href]'), function (a) {
        return a.querySelector('img');
      });
    }

    function itemsFrom(group) {
      return imageLinks(group).map(function (a) {
        var img = a.querySelector('img');
        return {
          src: a.getAttribute('href'),
          alt: a.getAttribute('data-caption') || img.getAttribute('alt') || '',
          w: img.getAttribute('width') || '',
          h: img.getAttribute('height') || ''
        };
      });
    }

    function render(items) {
      track.innerHTML = '';
      slides = items;
      dlg.classList.toggle('gallery-multi', items.length > 1);
      items.forEach(function (item) {
        var slide = document.createElement('div');
        slide.className = 'gallery-slide';
        var img = document.createElement('img');
        img.src = item.src;
        img.alt = item.alt;
        if (item.w) img.width = item.w;
        if (item.h) img.height = item.h;
        slide.appendChild(img);
        track.appendChild(slide);
      });
    }

    function show(i) {
      if (!slides.length) return;
      index = (i + slides.length) % slides.length;
      track.style.transform = 'translateX(' + (-100 * index) + '%)';
      countEl.textContent = (index + 1) + ' of ' + slides.length;
      capEl.textContent = slides[index].alt;
    }

    function open(group, i) {
      var label = group.getAttribute('data-gallery');
      dlg.setAttribute('aria-label', label || 'Product photographs');
      render(itemsFrom(group));
      dlg.showModal();
      show(i);
    }

    function close() {
      if (dlg.open) dlg.close();
    }

    groups.forEach(function (group) {
      imageLinks(group).forEach(function (a, i) {
        a.addEventListener('click', function (e) {
          if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
          e.preventDefault();
          open(group, i);
        });
      });
    });

    dlg.querySelector('.gallery-close').addEventListener('click', close);
    dlg.querySelector('.gallery-prev').addEventListener('click', function () { show(index - 1); });
    dlg.querySelector('.gallery-next').addEventListener('click', function () { show(index + 1); });
    dlg.addEventListener('click', function (e) {
      var r = dlg.getBoundingClientRect();
      if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) {
        close();
      }
    });
    dlg.addEventListener('keydown', function (e) {
      if (slides.length < 2) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); show(index + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(index - 1); }
    });

    stage.addEventListener('pointerdown', function (e) { startX = e.clientX; });
    stage.addEventListener('pointerup', function (e) {
      if (slides.length < 2) return;
      var dx = e.clientX - startX;
      if (dx > 40) show(index - 1);
      else if (dx < -40) show(index + 1);
    });
  })();

})();
