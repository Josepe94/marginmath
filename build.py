"""Builds the static calculator site into ./docs (no dependencies, Python 3.9+).

Edit SITE below (name, URL, affiliate offers, legal details) and run:
    python3 build.py
Then publish the ./docs folder (GitHub Pages / Cloudflare Pages).
"""
import json
import html
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent
OUT = ROOT / "docs"  # GitHub Pages serves /docs

# ----------------------------------------------------------------------------- CONFIG
SITE = {
    "name": "MarginMath",                       # provisional brand: change here
    "tagline": "Free pricing and profit calculators for small businesses, freelancers and SaaS founders.",
    "base_url": "https://josepe94.github.io/marginmath",  # no trailing slash; set your real URL
    "lang": "en",
    "google_site_verification": "",             # Search Console meta tag content (optional)
    "contact_email": "hello@example.com",
    # Legal notice (Spain, LSSI art. 10): fill in before going live.
    "owner_name": "[Your full name]",
    "owner_nif": "[Your NIF]",
    "owner_city": "Murcia, Spain",
    # Affiliate offers: leave url "" until you are approved; empty offers are not shown.
    "offers": {
        "accounting": {"title": "Track every margin automatically",
                       "text": "Accounting software that shows profit per product and per client, so you don't need a spreadsheet.",
                       "cta": "Try it free", "url": ""},
        "invoicing": {"title": "Get paid faster",
                      "text": "Send professional invoices and accept card payments in minutes.",
                      "cta": "See invoicing tool", "url": ""},
        "crm": {"title": "Grow revenue, not just margins",
                "text": "A free CRM to follow up every lead and quote.",
                "cta": "Get the free CRM", "url": ""},
        "analytics": {"title": "Your SaaS metrics, live",
                      "text": "Connect your billing and see MRR, churn and LTV update every day.",
                      "cta": "Connect your billing", "url": ""},
        "email": {"title": "Turn visitors into customers",
                  "text": "Email marketing built for creators and small businesses. Free up to your first subscribers.",
                  "cta": "Start for free", "url": ""},
    },
}

# ----------------------------------------------------------------------------- TOOLS
# Each tool: slug, title, h1, meta description, fields, outputs, js (name of compute fn), content blocks.
TOOLS = [
    {
        "slug": "profit-margin-calculator",
        "nav": "Profit margin",
        "title": "Profit Margin Calculator — Margin, Markup & Profit from Cost and Price",
        "h1": "Profit Margin Calculator",
        "desc": "Enter cost and selling price to get gross margin, markup and profit, or enter a target margin to get the price you need. Free, instant, no sign-up.",
        "lead": "Type your cost and selling price to see your profit, gross margin and markup. Switch mode to find the price that hits a target margin.",
        "js": "margin",
        "modes": [("price", "I know cost and price"), ("target", "I want a target margin")],
        "fields": [
            {"id": "cost", "label": "Cost per unit", "money": True, "value": 40, "modes": ["price", "target"]},
            {"id": "price", "label": "Selling price", "money": True, "value": 65, "modes": ["price"]},
            {"id": "margin", "label": "Target gross margin", "suffix": "%", "value": 40, "modes": ["target"]},
        ],
        "outputs": [("profit", "Profit per unit", "money"), ("marginPct", "Gross margin", "pct"),
                    ("markupPct", "Markup", "pct"), ("priceOut", "Selling price", "money")],
        "offer": "accounting",
        "how": """<p>Margin and markup describe the same profit from two different angles, which is why they are so often confused.</p>
<ul><li><strong>Profit</strong> = Price − Cost</li><li><strong>Gross margin</strong> = Profit ÷ Price × 100</li><li><strong>Markup</strong> = Profit ÷ Cost × 100</li><li><strong>Price for a target margin</strong> = Cost ÷ (1 − Margin)</li></ul>
<p>Margin can never reach 100% (that would mean a product that cost nothing), while markup has no upper limit.</p>""",
        "example": """<p>A product costs <strong>$40</strong> and sells for <strong>$65</strong>. Profit is $25, gross margin is 25 ÷ 65 = <strong>38.5%</strong> and markup is 25 ÷ 40 = <strong>62.5%</strong>.</p>
<p>If you want a 50% margin on the same product, the price must be 40 ÷ (1 − 0.50) = <strong>$80</strong>, not $60. Adding 50% to cost gives a 50% <em>markup</em>, which is only a 33.3% margin.</p>""",
        "faq": [
            ("What is a good profit margin?", "It depends on the industry. Retail gross margins are often in the 25–50% range, software and digital products commonly exceed 70%, and grocery or wholesale can run under 20%. Compare yourself with businesses that have a similar cost structure, not with a universal number."),
            ("Is margin the same as markup?", "No. Margin divides profit by the selling price; markup divides profit by the cost. The same $25 profit on a $40 cost and $65 price is a 38.5% margin but a 62.5% markup."),
            ("Does this calculate net profit margin?", "It calculates gross margin per unit: price minus the direct cost of the product. Net margin also subtracts overheads such as rent, salaries, software and taxes, so it is always lower."),
            ("How do I convert markup to margin?", "Margin = Markup ÷ (1 + Markup). A 50% markup is 0.5 ÷ 1.5 = 33.3% margin. Use the markup calculator for the reverse direction."),
        ],
        "related": ["markup-calculator", "break-even-calculator", "price-increase-calculator"],
    },
    {
        "slug": "markup-calculator",
        "nav": "Markup",
        "title": "Markup Calculator — Selling Price from Cost and Markup %",
        "h1": "Markup Calculator",
        "desc": "Add a markup percentage to your cost and get the selling price, profit and resulting gross margin. Includes a markup to margin conversion table.",
        "lead": "Enter your cost and the markup you want to apply. You get the selling price, the profit per unit and the gross margin that markup really gives you.",
        "js": "markup",
        "fields": [
            {"id": "cost", "label": "Cost per unit", "money": True, "value": 40},
            {"id": "markup", "label": "Markup", "suffix": "%", "value": 50},
        ],
        "outputs": [("priceOut", "Selling price", "money"), ("profit", "Profit per unit", "money"), ("marginPct", "Gross margin", "pct")],
        "offer": "invoicing",
        "how": """<ul><li><strong>Selling price</strong> = Cost × (1 + Markup)</li><li><strong>Profit</strong> = Price − Cost</li><li><strong>Gross margin</strong> = Markup ÷ (1 + Markup)</li></ul>
<table class="ref"><thead><tr><th>Markup</th><th>Equals margin</th></tr></thead><tbody>
<tr><td>25%</td><td>20.0%</td></tr><tr><td>33.3%</td><td>25.0%</td></tr><tr><td>50%</td><td>33.3%</td></tr><tr><td>66.7%</td><td>40.0%</td></tr><tr><td>100%</td><td>50.0%</td></tr><tr><td>150%</td><td>60.0%</td></tr><tr><td>200%</td><td>66.7%</td></tr></tbody></table>""",
        "example": """<p>You buy an item for <strong>$40</strong> and apply a <strong>50%</strong> markup: the price is 40 × 1.5 = <strong>$60</strong>, profit is $20 and gross margin is 20 ÷ 60 = <strong>33.3%</strong>. Doubling the cost (100% markup, also called keystone pricing) gives a 50% margin.</p>""",
        "faq": [
            ("What markup should I use?", "Work backwards from the margin you need to cover overheads and profit. If your overheads eat 30% of revenue and you want 10% net profit, you need about a 40% gross margin, which is a 66.7% markup."),
            ("What is keystone pricing?", "Keystone pricing means doubling the wholesale cost, a 100% markup. It produces a 50% gross margin and is a common starting point in retail."),
            ("Why is my margin lower than my markup?", "Because markup is measured against the smaller number (cost) and margin against the larger one (price). For any positive profit, margin is always lower than markup."),
            ("Can markup be over 100%?", "Yes. A 200% markup means the price is three times the cost. Margin, however, can never reach 100%."),
        ],
        "related": ["profit-margin-calculator", "freelance-hourly-rate-calculator", "price-increase-calculator"],
    },
    {
        "slug": "freelance-hourly-rate-calculator",
        "nav": "Freelance rate",
        "title": "Freelance Hourly Rate Calculator — What Should I Charge per Hour?",
        "h1": "Freelance Hourly Rate Calculator",
        "desc": "Work out the hourly and day rate you need as a freelancer from your target take-home pay, business expenses, taxes, time off and real billable hours.",
        "lead": "Start from the income you want to keep, add your business costs and taxes, and divide by the hours you can actually bill. Most freelancers underestimate the last part.",
        "js": "freelance",
        "fields": [
            {"id": "income", "label": "Target take-home pay per year", "money": True, "value": 60000},
            {"id": "expenses", "label": "Business expenses per year", "money": True, "value": 6000, "hint": "Software, equipment, insurance, accountant, coworking…"},
            {"id": "tax", "label": "Tax and social contributions", "suffix": "%", "value": 30, "hint": "Your effective rate on profit, not the top bracket."},
            {"id": "weeksOff", "label": "Weeks off per year", "value": 6, "hint": "Holidays, public holidays and sick days."},
            {"id": "hours", "label": "Billable hours per week", "value": 25, "hint": "Hours you can invoice, not hours you work."},
        ],
        "outputs": [("hourly", "Minimum hourly rate", "money"), ("daily", "Day rate (8 billable h)", "money"),
                    ("revenue", "Revenue needed per year", "money"), ("billable", "Billable hours per year", "num")],
        "offer": "invoicing",
        "how": """<ol><li><strong>Revenue needed</strong> = (Take-home pay + Expenses) ÷ (1 − Tax rate)</li><li><strong>Billable hours</strong> = (52 − Weeks off) × Billable hours per week</li><li><strong>Hourly rate</strong> = Revenue needed ÷ Billable hours</li></ol>
<p>The tax step is approximate: it applies one effective rate to everything you earn after expenses. Your real tax depends on your country and your deductions, so ask an accountant before committing to a price.</p>""",
        "example": """<p>To take home <strong>$60,000</strong> with $6,000 of expenses and a 30% effective tax rate, you need (60,000 + 6,000) ÷ 0.70 = <strong>$94,286</strong> of revenue. With 6 weeks off and 25 billable hours a week you have 1,150 billable hours, so your minimum rate is <strong>$82 per hour</strong>, roughly $656 per 8-hour day.</p>""",
        "faq": [
            ("How many billable hours does a freelancer have?", "Far fewer than 40 a week. Sales, admin, invoicing and learning typically take 30–50% of working time, so 20–30 billable hours a week is a realistic range for most solo freelancers."),
            ("Should I charge hourly or per project?", "Use this hourly figure as your floor. Per-project or value-based pricing can earn more once you can estimate scope well, but the quote should never work out below your minimum hourly rate."),
            ("How do I convert a salary into a freelance rate?", "A common rule of thumb is to divide the annual salary by 1,000 to get a rough hourly rate, because freelancers pay their own taxes, benefits, equipment and unpaid time. This calculator does the full version."),
            ("Does this include VAT or sales tax?", "No. Rates here are before VAT or sales tax, which you add on top of your invoices where it applies."),
        ],
        "related": ["markup-calculator", "break-even-calculator", "profit-margin-calculator"],
    },
    {
        "slug": "break-even-calculator",
        "nav": "Break-even",
        "title": "Break-Even Calculator — Units and Revenue to Cover Your Costs",
        "h1": "Break-Even Point Calculator",
        "desc": "Find how many units you must sell each month to cover fixed costs, the break-even revenue and your contribution margin per unit.",
        "lead": "Enter your monthly fixed costs, your price and the variable cost of each unit. The calculator shows how many sales you need before you make any profit.",
        "js": "breakeven",
        "fields": [
            {"id": "fixed", "label": "Fixed costs per month", "money": True, "value": 5000, "hint": "Rent, salaries, software, insurance: costs that don't change with sales."},
            {"id": "price", "label": "Price per unit", "money": True, "value": 50},
            {"id": "variable", "label": "Variable cost per unit", "money": True, "value": 20, "hint": "Materials, payment fees, shipping, commissions."},
            {"id": "target", "label": "Target profit per month (optional)", "money": True, "value": 0},
        ],
        "outputs": [("units", "Break-even units per month", "int"), ("revenue", "Break-even revenue", "money"),
                    ("contribution", "Contribution margin per unit", "money"), ("contributionPct", "Contribution margin ratio", "pct"),
                    ("unitsTarget", "Units to reach target profit", "int")],
        "offer": "accounting",
        "how": """<ul><li><strong>Contribution margin</strong> = Price − Variable cost</li><li><strong>Break-even units</strong> = Fixed costs ÷ Contribution margin</li><li><strong>Break-even revenue</strong> = Break-even units × Price</li><li><strong>Units for a target profit</strong> = (Fixed costs + Target profit) ÷ Contribution margin</li></ul>""",
        "example": """<p>With <strong>$5,000</strong> of monthly fixed costs, a <strong>$50</strong> price and <strong>$20</strong> of variable cost, each sale contributes $30. You break even at 5,000 ÷ 30 = <strong>167 units</strong> a month ($8,350 of revenue). To make $3,000 of profit you need 267 units.</p>""",
        "faq": [
            ("What happens if my price is below my variable cost?", "You can never break even: every extra sale loses money. Raise the price or cut the variable cost before worrying about volume."),
            ("Should I round the break-even units up?", "Yes. You can't sell part of a unit, so the calculator rounds up to the next whole unit."),
            ("Is break-even analysis useful for services?", "Yes. Treat one billable hour or one project as a unit, and use the direct costs of delivering it (subcontractors, tools) as the variable cost."),
            ("How can I lower my break-even point?", "Three levers: cut fixed costs, raise prices, or reduce the variable cost per unit. Price usually has the biggest effect because it raises the contribution of every sale."),
        ],
        "related": ["profit-margin-calculator", "price-increase-calculator", "ltv-cac-calculator"],
    },
    {
        "slug": "ltv-cac-calculator",
        "nav": "LTV:CAC",
        "title": "LTV to CAC Calculator — Customer Lifetime Value, Ratio and Payback",
        "h1": "LTV to CAC Calculator",
        "desc": "Calculate customer lifetime value from ARPA, gross margin and churn, then compare it with acquisition cost: LTV:CAC ratio and CAC payback period in months.",
        "lead": "Enter what an average customer pays per month, your gross margin, your monthly churn and what it costs to acquire a customer.",
        "js": "ltv",
        "fields": [
            {"id": "arpa", "label": "Average revenue per account per month (ARPA)", "money": True, "value": 50},
            {"id": "gm", "label": "Gross margin", "suffix": "%", "value": 80},
            {"id": "churn", "label": "Monthly churn", "suffix": "%", "value": 3, "hint": "Share of customers who cancel each month."},
            {"id": "cac", "label": "Customer acquisition cost (CAC)", "money": True, "value": 400},
        ],
        "outputs": [("ltv", "Customer lifetime value (LTV)", "money"), ("ratio", "LTV : CAC", "ratio"),
                    ("payback", "CAC payback period", "months"), ("lifetime", "Average customer lifetime", "months")],
        "offer": "analytics",
        "how": """<ul><li><strong>Customer lifetime</strong> = 1 ÷ Monthly churn</li><li><strong>LTV</strong> = ARPA × Gross margin ÷ Monthly churn</li><li><strong>LTV : CAC</strong> = LTV ÷ CAC</li><li><strong>CAC payback</strong> = CAC ÷ (ARPA × Gross margin)</li></ul>
<p>This is the simple, margin-based LTV used by most SaaS dashboards. It assumes churn stays constant and ignores expansion revenue and discounting.</p>""",
        "example": """<p>A customer pays <strong>$50</strong> a month at an 80% gross margin, so you keep $40 a month. With <strong>3%</strong> monthly churn the average customer stays 33 months and is worth 40 ÷ 0.03 = <strong>$1,333</strong>. If acquiring them costs $400, LTV:CAC is <strong>3.3 : 1</strong> and you recover the CAC in 10 months.</p>""",
        "faq": [
            ("What is a good LTV:CAC ratio?", "3:1 is the widely quoted benchmark for a healthy subscription business. Below 1:1 you lose money on every customer; far above 5:1 can mean you are under-investing in growth."),
            ("What is a good CAC payback period?", "Many SaaS investors look for payback under 12 months for small-business customers. Enterprise products often accept 18–24 months because customers stay longer."),
            ("Should LTV use revenue or gross margin?", "Gross margin. Using raw revenue overstates what a customer is worth because it ignores hosting, support and payment costs."),
            ("How do I use annual churn?", "Convert it to monthly first: monthly churn ≈ 1 − (1 − annual churn)^(1/12). For 30% annual churn that is about 2.9% per month."),
        ],
        "related": ["break-even-calculator", "price-increase-calculator", "profit-margin-calculator"],
    },
    {
        "slug": "price-increase-calculator",
        "nav": "Price increase",
        "title": "Price Increase Calculator — How Many Customers Can You Lose and Still Profit?",
        "h1": "Price Increase Calculator",
        "desc": "Before raising prices, see how many sales you could lose and still earn the same profit, and how much more you make if nobody leaves. Works for price cuts too.",
        "lead": "Thinking about raising (or cutting) your prices? Enter your current price, the variable cost per sale and the change you are considering.",
        "js": "priceinc",
        "fields": [
            {"id": "price", "label": "Current price", "money": True, "value": 100},
            {"id": "variable", "label": "Variable cost per sale", "money": True, "value": 60},
            {"id": "change", "label": "Price change", "suffix": "%", "value": 10, "hint": "Use a negative number for a discount, e.g. −15."},
            {"id": "volume", "label": "Current sales per month (optional)", "value": 200},
        ],
        "outputs": [("newPrice", "New price", "money"), ("volumeChange", "Sales change that keeps the same profit", "pctSigned"),
                    ("profitGain", "Profit change if sales stay the same", "pctSigned"), ("salesNeeded", "Sales per month for the same profit", "int")],
        "offer": "crm",
        "how": """<ul><li><strong>Contribution per sale</strong> = Price − Variable cost</li><li><strong>Break-even sales change</strong> = (Old contribution ÷ New contribution) − 1</li><li><strong>Profit change at the same volume</strong> = Price change ÷ Old contribution</li></ul>
<p>The lower your margin, the more powerful a price increase is, and the more dangerous a discount.</p>""",
        "example": """<p>You sell at <strong>$100</strong> with <strong>$60</strong> of variable cost, so each sale contributes $40. A <strong>10%</strong> price increase lifts the contribution to $50: you could lose up to <strong>20%</strong> of your sales and still earn the same profit, and if nobody leaves your profit rises by 25%.</p>
<p>The same maths warns about discounts: a 10% discount drops the contribution to $30, so you would need <strong>33% more sales</strong> just to stand still.</p>""",
        "faq": [
            ("How much should I raise my prices?", "Many businesses test 5–15% increases on new customers first. Use this calculator to see the sales drop you can tolerate, then compare it with what you actually see in the test."),
            ("Why does a small discount need so many extra sales?", "Because a discount comes entirely out of your margin. If your margin is thin, a 10% discount can remove a third or more of the profit on every sale."),
            ("Does this include fixed costs?", "Fixed costs don't change with a price move, so they cancel out: keeping the same total contribution keeps the same profit."),
            ("What is price elasticity?", "It measures how much demand changes when the price changes. This calculator doesn't need it: it tells you the break-even elasticity, which you then compare with what you expect from your customers."),
        ],
        "related": ["profit-margin-calculator", "break-even-calculator", "markup-calculator"],
    },
]

TOOL_BY_SLUG = {t["slug"]: t for t in TOOLS}
E = html.escape


# ----------------------------------------------------------------------------- TEMPLATES
def url(path=""):
    return f"{SITE['base_url']}/{path}".rstrip("/") + ("/" if path and not path.endswith(".html") and not path.endswith(".xml") else "")


def rel(path, depth):
    """Relative link from a page at given depth (0 = root)."""
    return ("../" * depth) + path


def layout(title, desc, body, depth, canonical, schema=None):
    nav = "".join(f'<a href="{rel(t["slug"] + "/", depth)}">{E(t["nav"])}</a>' for t in TOOLS)
    verify = f'<meta name="google-site-verification" content="{E(SITE["google_site_verification"])}">' if SITE["google_site_verification"] else ""
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    year = date.today().year
    return f"""<!doctype html>
<html lang="{SITE['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{E(canonical)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{E(canonical)}">
{verify}
<link rel="icon" href="{rel('assets/favicon.svg', depth)}" type="image/svg+xml">
<link rel="stylesheet" href="{rel('assets/style.css', depth)}">
{ld}
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="{rel('', depth) or './'}">{E(SITE['name'])}</a>
  <nav class="nav">{nav}</nav>
</div></header>
<main class="wrap">{body}</main>
<footer class="foot"><div class="wrap">
  <p>{E(SITE['name'])} · {E(SITE['tagline'])}</p>
  <p><a href="{rel('about/', depth)}">About</a> · <a href="{rel('privacy/', depth)}">Privacy</a> · <a href="{rel('legal/', depth)}">Legal notice</a> · <a href="{rel('disclosure/', depth)}">Affiliate disclosure</a></p>
  <p class="muted">Results are estimates for planning purposes, not financial, tax or legal advice. © {year} {E(SITE['name'])}</p>
</div></footer>
<script src="{rel('assets/app.js', depth)}" defer></script>
</body>
</html>
"""


def field_html(f, modes):
    attrs = f'data-modes="{" ".join(f.get("modes", []))}"' if f.get("modes") else ""
    pre = '<span class="pre" data-currency>$</span>' if f.get("money") else ""
    suf = f'<span class="suf">{E(f["suffix"])}</span>' if f.get("suffix") else ""
    hint = f'<small>{E(f["hint"])}</small>' if f.get("hint") else ""
    return f"""<label class="field" {attrs}><span class="lbl">{E(f['label'])}</span>
<span class="inp">{pre}<input type="number" inputmode="decimal" step="any" name="{f['id']}" value="{f['value']}">{suf}</span>{hint}</label>"""


def offer_html(key):
    o = SITE["offers"].get(key) or {}
    if not o.get("url"):
        return ""
    return f"""<aside class="offer"><div><strong>{E(o['title'])}</strong><p>{E(o['text'])}</p></div>
<a class="btn" href="{E(o['url'])}" rel="sponsored noopener" target="_blank">{E(o['cta'])}</a>
<small class="muted">Affiliate link: we may earn a commission at no extra cost to you.</small></aside>"""


def tool_page(t):
    depth = 1
    modes = t.get("modes")
    mode_html = ""
    if modes:
        opts = "".join(f'<button type="button" data-mode="{m}" class="{"on" if i == 0 else ""}">{E(l)}</button>' for i, (m, l) in enumerate(modes))
        mode_html = f'<div class="modes" role="tablist">{opts}</div>'
    fields = "".join(field_html(f, modes) for f in t["fields"])
    outs = "".join(f'<div class="out" data-out="{k}" data-fmt="{fmt}"><span>{E(lbl)}</span><b>–</b></div>' for k, lbl, fmt in t["outputs"])
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in t["faq"])
    related = "".join(f'<a class="card" href="../{s}/"><b>{E(TOOL_BY_SLUG[s]["h1"])}</b><span>{E(TOOL_BY_SLUG[s]["desc"][:110])}…</span></a>' for s in t["related"])
    body = f"""
<article class="tool">
  <h1>{E(t['h1'])}</h1>
  <p class="lead">{E(t['lead'])}</p>
  <form class="calc" data-tool="{t['js']}" onsubmit="return false">
    <div class="calc-top">{mode_html}<label class="cur">Currency <select data-currency-select><option>$</option><option>€</option><option>£</option><option>₹</option><option>A$</option><option>C$</option></select></label></div>
    <div class="fields">{fields}</div>
    <div class="outs" aria-live="polite">{outs}</div>
    <p class="err" hidden></p>
  </form>
  {offer_html(t['offer'])}
  <section><h2>How it works</h2>{t['how']}</section>
  <section><h2>Worked example</h2>{t['example']}</section>
  <section class="faq"><h2>Frequently asked questions</h2>{faq}</section>
  <section><h2>Related calculators</h2><div class="cards">{related}</div></section>
</article>"""
    canonical = url(t["slug"] + "/")
    schema = [
        {"@context": "https://schema.org", "@type": "WebApplication", "name": t["h1"], "url": canonical,
         "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": t["desc"]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": SITE["name"], "item": url()},
            {"@type": "ListItem", "position": 2, "name": t["h1"], "item": canonical}]},
    ]
    return layout(t["title"], t["desc"], body, depth, canonical, schema)


def home_page():
    cards = "".join(f'<a class="card" href="{t["slug"]}/"><b>{E(t["h1"])}</b><span>{E(t["desc"])}</span></a>' for t in TOOLS)
    body = f"""<section class="hero"><h1>Pricing &amp; profit calculators that show their work</h1>
<p class="lead">{E(SITE['tagline'])} Every calculator explains the formula and a worked example, runs in your browser and never asks for an email.</p></section>
<div class="cards grid">{cards}</div>"""
    schema = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"], "url": url()}]
    return layout(f"{SITE['name']} — Free Profit, Pricing & SaaS Calculators", SITE["tagline"], body, 0, url(), schema)


def simple_page(slug, title, inner):
    return layout(f"{title} — {SITE['name']}", f"{title} for {SITE['name']}.", f'<article class="prose"><h1>{E(title)}</h1>{inner}</article>', 1, url(slug + "/"))


def legal_pages():
    s = SITE
    return {
        "about": ("About", f"""<p>{E(s['name'])} builds small, honest calculators for people who price things for a living: shop owners, freelancers, agencies and SaaS founders.</p>
<p>Every tool runs entirely in your browser. We show the formula and a worked example so you can check the result yourself, and we review each calculator against standard accounting definitions.</p>
<p>Spotted an error or want a new calculator? Write to <a href="mailto:{E(s['contact_email'])}">{E(s['contact_email'])}</a>.</p>"""),
        "privacy": ("Privacy policy", f"""<p><strong>Controller:</strong> {E(s['owner_name'])}, {E(s['owner_city'])}. Contact: {E(s['contact_email'])}.</p>
<p><strong>What we collect:</strong> nothing you type into a calculator leaves your device. The site does not use analytics or advertising cookies. Our host (GitHub Pages or Cloudflare Pages) processes technical data such as your IP address to deliver the pages and protect against abuse.</p>
<p><strong>Local storage:</strong> we remember your chosen currency symbol in your browser. You can clear it at any time from your browser settings.</p>
<p><strong>Affiliate links:</strong> when you click one, the partner site may set its own cookies under its own privacy policy.</p>
<p><strong>Your rights:</strong> under the GDPR you can request access, rectification or erasure of any personal data we hold by writing to the address above, and complain to the Spanish Data Protection Agency (aepd.es).</p>
<p>If we add advertising in the future, this policy and a consent banner will be updated before any advertising cookie is set.</p>"""),
        "legal": ("Legal notice", f"""<p>In compliance with Spanish Law 34/2002 (LSSI-CE):</p>
<ul><li><strong>Owner:</strong> {E(s['owner_name'])}</li><li><strong>Tax ID (NIF):</strong> {E(s['owner_nif'])}</li><li><strong>Address:</strong> {E(s['owner_city'])}</li><li><strong>Email:</strong> {E(s['contact_email'])}</li></ul>
<p>The calculators are provided free of charge and for information only. Results are estimates and do not constitute financial, tax or legal advice. Check important decisions with a qualified professional.</p>"""),
        "disclosure": ("Affiliate disclosure", """<p>Some pages contain affiliate links. If you click one and buy, we may earn a commission at no extra cost to you. Affiliate links are always marked and never change a calculator's result.</p>
<p>We only recommend tools that are relevant to the calculator on the page.</p>"""),
    }


# ----------------------------------------------------------------------------- BUILD
def build():
    if OUT.exists():
        for p in sorted(OUT.rglob("*"), reverse=True):
            p.unlink() if p.is_file() else p.rmdir()
    (OUT / "assets").mkdir(parents=True)
    for name in ("style.css", "app.js", "favicon.svg"):
        (OUT / "assets" / name).write_text((ROOT / "assets" / name).read_text(encoding="utf-8"), encoding="utf-8")
    (OUT / "index.html").write_text(home_page(), encoding="utf-8")
    for t in TOOLS:
        d = OUT / t["slug"]
        d.mkdir()
        (d / "index.html").write_text(tool_page(t), encoding="utf-8")
    for slug, (title, inner) in legal_pages().items():
        d = OUT / slug
        d.mkdir()
        (d / "index.html").write_text(simple_page(slug, title, inner), encoding="utf-8")
    (OUT / "404.html").write_text(layout(f"Page not found — {SITE['name']}", "Page not found", '<article class="prose"><h1>Page not found</h1><p><a href="./">Go to all calculators</a></p></article>', 0, url()), encoding="utf-8")
    today = date.today().isoformat()
    urls = [url()] + [url(t["slug"] + "/") for t in TOOLS] + [url(s + "/") for s in ("about", "privacy", "legal", "disclosure")]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {url('sitemap.xml')}\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built {len(TOOLS)} calculators + {len(legal_pages())} pages into {OUT}")


if __name__ == "__main__":
    build()
