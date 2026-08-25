// Mobile contents toggle. The nav is visible by default and only collapses on
// small screens, so a JS failure leaves the site fully navigable.
(function () {
  var btn = document.querySelector('.railtoggle');
  var nav = document.getElementById('contents');
  if (!btn || !nav) return;
  var small = window.matchMedia('(max-width: 900px)');
  function sync() {
    if (small.matches) { nav.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
    else { nav.hidden = false; btn.setAttribute('aria-expanded', 'true'); }
  }
  btn.addEventListener('click', function () {
    var open = nav.hidden;
    nav.hidden = !open;
    btn.setAttribute('aria-expanded', String(open));
  });
  small.addEventListener('change', sync);
  sync();
})();
