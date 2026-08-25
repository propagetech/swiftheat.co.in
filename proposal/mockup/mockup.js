// Live preview of the enquiry email. Demonstrates the mailto approach: the form
// composes a readable message and hands it to the visitor's own mail application,
// so nothing is stored on a server and no backend has to be secured.
(function () {
  var form = document.getElementById('rfqForm');
  var pre = document.getElementById('mailPreview');
  var btn = document.getElementById('composeBtn');
  if (!form || !pre || !btn) return;

  var GROUPS = [
    ['What you need', ['Enquiry type', 'Quantity', 'Required by']],
    ['Application', ['Industry', 'Machine', 'Operating temperature']],
    ['Heater specification', ['Sheath diameter', 'Overall length', 'Heated length',
      'Wattage', 'Voltage', 'Sheath material', 'Termination', 'Lead protection',
      'Lead length', 'Thermocouple', 'Bore diameter', 'Mounting']],
    ['Customer', ['Name', 'Company', 'Email', 'Phone']]
  ];

  function val(name) {
    var el = form.querySelector('[name="' + name + '"]');
    if (!el) return '';
    return (el.value || '').trim();
  }

  function pad(label, width) {
    while (label.length < width) label += ' ';
    return label;
  }

  function compose() {
    var lines = ['ENQUIRY: CARTRIDGE HEATERS', ''];
    var any = false;
    GROUPS.forEach(function (g) {
      var rows = [];
      g[1].forEach(function (name) {
        var v = val(name);
        if (v) { rows.push('  ' + pad(name, 22) + v); any = true; }
      });
      if (rows.length) {
        lines.push(g[0].toUpperCase());
        lines = lines.concat(rows);
        lines.push('');
      }
    });
    var notes = val('Notes');
    if (notes) { lines.push('NOTES'); lines.push('  ' + notes); lines.push(''); any = true; }
    if (!any) return null;
    lines.push('Sent from swiftheat.co.in');
    return lines.join('\n');
  }

  function refresh() {
    var body = compose();
    pre.textContent = body || 'Fill in the form and the enquiry appears here.';
  }

  form.addEventListener('input', refresh);
  form.addEventListener('change', refresh);

  btn.addEventListener('click', function () {
    var body = compose();
    if (!body) { refresh(); return; }
    var company = val('Company');
    var subject = 'Cartridge heater enquiry' + (company ? ' from ' + company : '');
    // Real site would use the confirmed enquiry address.
    window.location.href = 'mailto:enquiry@swiftheat.co.in'
      + '?subject=' + encodeURIComponent(subject)
      + '&body=' + encodeURIComponent(body);
  });

  refresh();
})();
