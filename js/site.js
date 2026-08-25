/* Swiftheat — one script for the whole site.
   Three small, independent pieces: the mobile nav, the product finder, and the
   enquiry form that composes a readable email. Nothing here is required for the
   content to be readable; the page works with the script blocked. */
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
    var to = form.getAttribute('data-to') || 'enquiry@swiftheat.co.in';
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

})();
