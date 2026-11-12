// Checks every calculator against the worked examples published on the pages.
const assert = require('assert');
const C = require('../assets/app.js');
const near = (a, b, tol = 0.05) => assert.ok(Math.abs(a - b) <= tol, `${a} != ${b}`);

// Profit margin: cost 40, price 65 -> profit 25, margin 38.46%, markup 62.5%
let r = C.margin({ cost: 40, price: 65 }, 'price');
near(r.profit, 25); near(r.marginPct, 38.46); near(r.markupPct, 62.5);
// target 50% margin on cost 40 -> 80
near(C.margin({ cost: 40, margin: 50 }, 'target').priceOut, 80);
assert.ok(C.margin({ cost: 40, margin: 100 }, 'target').error);

// Markup: 40 + 50% -> 60, margin 33.3%; 100% -> 50% margin
r = C.markup({ cost: 40, markup: 50 }); near(r.priceOut, 60); near(r.profit, 20); near(r.marginPct, 33.33);
near(C.markup({ cost: 10, markup: 100 }).marginPct, 50);

// Freelance: 60k + 6k at 30%, 6 weeks off, 25 h -> 94,286 revenue, 1,150 h, ~82/h, ~656/day
r = C.freelance({ income: 60000, expenses: 6000, tax: 30, weeksOff: 6, hours: 25 });
near(r.revenue, 94285.71, 0.5); assert.strictEqual(r.billable, 1150); near(r.hourly, 81.99, 0.01); near(r.daily, 655.9, 0.1);

// Break-even: 5000 fixed, 50 price, 20 var -> 167 units, 8350 revenue; +3000 target -> 267
r = C.breakeven({ fixed: 5000, price: 50, variable: 20, target: 3000 });
assert.strictEqual(r.units, 167); near(r.revenue, 8350); near(r.contributionPct, 60); assert.strictEqual(r.unitsTarget, 267);
assert.strictEqual(C.breakeven({ fixed: 3000, price: 50, variable: 20, target: 0 }).units, 100, 'exact division not rounded up');
assert.ok(C.breakeven({ fixed: 1, price: 20, variable: 20 }).error);

// LTV: 50 ARPA, 80% GM, 3% churn, 400 CAC -> LTV 1333, ratio 3.3, payback 10, lifetime 33.3
r = C.ltv({ arpa: 50, gm: 80, churn: 3, cac: 400 });
near(r.ltv, 1333.33, 0.01); near(r.ratio, 3.33, 0.01); near(r.payback, 10); near(r.lifetime, 33.33, 0.01);
assert.ok(C.ltv({ arpa: 50, gm: 80, churn: 0, cac: 400 }).error);

// Price increase: 100, 60, +10% -> can lose 20%, profit +25%; 200 sales -> 160 needed
r = C.priceinc({ price: 100, variable: 60, change: 10, volume: 200 });
near(r.newPrice, 110); near(r.volumeChange, -20); near(r.profitGain, 25); assert.strictEqual(r.salesNeeded, 160);
// -10% discount -> need +33.3% more sales
near(C.priceinc({ price: 100, variable: 60, change: -10, volume: 0 }).volumeChange, 33.33, 0.01);
assert.ok(C.priceinc({ price: 100, variable: 60, change: -50 }).error);

console.log('All calculator tests passed');
