/* Calculator logic. Pure functions in CALC are also exported for tests (Node). */
(function (root) {
  'use strict';

  var pct = function (v) { return v / 100; };

  var CALC = {
    margin: function (v, mode) {
      var cost = v.cost;
      if (!(cost >= 0)) return { error: 'Enter a cost of 0 or more.' };
      var price;
      if (mode === 'target') {
        var m = pct(v.margin);
        if (!(m < 1)) return { error: 'A gross margin must be below 100%.' };
        price = cost / (1 - m);
      } else {
        price = v.price;
        if (!(price > 0)) return { error: 'Enter a selling price above 0.' };
      }
      var profit = price - cost;
      return {
        profit: profit,
        marginPct: profit / price * 100,
        markupPct: cost > 0 ? profit / cost * 100 : null,
        priceOut: price
      };
    },

    markup: function (v) {
      if (!(v.cost > 0)) return { error: 'Enter a cost above 0.' };
      if (!(v.markup > -100)) return { error: 'Markup must be above −100%.' };
      var price = v.cost * (1 + pct(v.markup));
      var profit = price - v.cost;
      return { priceOut: price, profit: profit, marginPct: profit / price * 100 };
    },

    freelance: function (v) {
      var t = pct(v.tax);
      if (!(t >= 0 && t < 1)) return { error: 'Tax rate must be between 0% and 99%.' };
      if (!(v.weeksOff >= 0 && v.weeksOff < 52)) return { error: 'Weeks off must be between 0 and 51.' };
      if (!(v.hours > 0)) return { error: 'Enter your billable hours per week.' };
      var revenue = ((v.income || 0) + (v.expenses || 0)) / (1 - t);
      var billable = (52 - v.weeksOff) * v.hours;
      var hourly = revenue / billable;
      return { hourly: hourly, daily: hourly * 8, revenue: revenue, billable: billable };
    },

    breakeven: function (v) {
      var c = v.price - v.variable;
      if (!(v.price > 0)) return { error: 'Enter a price above 0.' };
      if (!(c > 0)) return { error: 'Your price must be higher than the variable cost per unit, or you can never break even.' };
      var units = Math.ceil((v.fixed || 0) / c - 1e-9);
      return {
        units: units,
        revenue: units * v.price,
        contribution: c,
        contributionPct: c / v.price * 100,
        unitsTarget: v.target > 0 ? Math.ceil(((v.fixed || 0) + v.target) / c - 1e-9) : null
      };
    },

    ltv: function (v) {
      var gm = pct(v.gm), churn = pct(v.churn);
      if (!(v.arpa > 0)) return { error: 'Enter the average revenue per account.' };
      if (!(gm > 0 && gm <= 1)) return { error: 'Gross margin must be between 1% and 100%.' };
      if (!(churn > 0 && churn <= 1)) return { error: 'Monthly churn must be above 0%.' };
      var monthlyProfit = v.arpa * gm;
      var ltv = monthlyProfit / churn;
      return {
        ltv: ltv,
        ratio: v.cac > 0 ? ltv / v.cac : null,
        payback: v.cac > 0 ? v.cac / monthlyProfit : null,
        lifetime: 1 / churn
      };
    },

    priceinc: function (v) {
      var c0 = v.price - v.variable;
      if (!(v.price > 0)) return { error: 'Enter your current price.' };
      if (!(c0 > 0)) return { error: 'Your current price must be above the variable cost per sale.' };
      var newPrice = v.price * (1 + pct(v.change));
      var c1 = newPrice - v.variable;
      if (!(c1 > 0)) return { error: 'With that discount every sale loses money: the new price is below the variable cost.' };
      return {
        newPrice: newPrice,
        volumeChange: (c0 / c1 - 1) * 100,
        profitGain: (newPrice - v.price) / c0 * 100,
        salesNeeded: v.volume > 0 ? Math.ceil(v.volume * c0 / c1 - 1e-9) : null
      };
    }
  };

  if (typeof module !== 'undefined' && module.exports) { module.exports = CALC; return; }

  // ------------------------------------------------------------------ browser UI
  var store = {
    get: function (k) { try { return root.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { root.localStorage.setItem(k, v); } catch (e) { /* ignore */ } }
  };
  var symbol = store.get('mm-currency') || '$';

  function fmt(value, kind) {
    if (value === null || value === undefined || !isFinite(value)) return '–';
    var n2 = function (x, d) { return x.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }); };
    switch (kind) {
      case 'money': return (value < 0 ? '−' : '') + symbol + n2(Math.abs(value), 2);
      case 'pct': return n2(value, 1) + '%';
      case 'pctSigned': return (value > 0 ? '+' : value < 0 ? '−' : '') + n2(Math.abs(value), 1) + '%';
      case 'int': return Math.round(value).toLocaleString('en-US');
      case 'num': return n2(value, 0);
      case 'ratio': return n2(value, 1) + ' : 1';
      case 'months': return n2(value, 1) + ' months';
      default: return String(value);
    }
  }

  function setup(form) {
    var tool = form.getAttribute('data-tool');
    var mode = (form.querySelector('[data-mode].on') || {}).getAttribute ? form.querySelector('[data-mode].on').getAttribute('data-mode') : null;
    var err = form.querySelector('.err');

    function applyMode() {
      form.querySelectorAll('[data-modes]').forEach(function (el) {
        var modes = el.getAttribute('data-modes').split(' ').filter(Boolean);
        el.hidden = modes.length > 0 && mode && modes.indexOf(mode) === -1;
      });
    }

    function run() {
      var v = {};
      form.querySelectorAll('input[name]').forEach(function (i) {
        v[i.name] = i.value === '' ? NaN : parseFloat(i.value);
      });
      var r = CALC[tool](v, mode);
      if (r.error) { err.textContent = r.error; err.hidden = false; }
      else { err.hidden = true; }
      form.querySelectorAll('[data-out]').forEach(function (o) {
        o.querySelector('b').textContent = r.error ? '–' : fmt(r[o.getAttribute('data-out')], o.getAttribute('data-fmt'));
      });
      form.querySelectorAll('[data-currency]').forEach(function (s) { s.textContent = symbol; });
    }

    form.querySelectorAll('[data-mode]').forEach(function (b) {
      b.addEventListener('click', function () {
        form.querySelectorAll('[data-mode]').forEach(function (x) { x.classList.toggle('on', x === b); });
        mode = b.getAttribute('data-mode');
        applyMode(); run();
      });
    });
    var sel = form.querySelector('[data-currency-select]');
    if (sel) {
      sel.value = symbol;
      sel.addEventListener('change', function () { symbol = sel.value; store.set('mm-currency', symbol); run(); });
    }
    form.addEventListener('input', run);
    applyMode(); run();
  }

  document.querySelectorAll('form.calc').forEach(setup);
})(typeof window !== 'undefined' ? window : this);
