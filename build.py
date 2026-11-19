import re, json, os, glob, html, datetime

BASE = 'https://yojanaurja.devidlaid004.workers.dev'
SKIP = {'index.html', 'about.html', 'contact.html', 'privacy-policy.html', 'disclaimer.html', 'articles.html'}
NO_ADS = {'privacy-policy.html', 'contact.html', 'disclaimer.html', 'about.html'}
TAGS = ['<script src="ads.js" defer></script>', '<script src="ads-more.js" defer></script>']
today = datetime.date.today().isoformat()

old = {}
if os.path.exists('articles.json'):
    try:
        for a in json.load(open('articles.json', encoding='utf-8')):
            old[a['slug']] = a.get('date', today)
    except Exception:
        pass

def wrap(t, n=14, maxl=3):
    lines, cur = [], ''
    for w in t.split():
        if not cur or len(cur) + len(w) + 1 <= n:
            cur = (cur + ' ' + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > maxl:
        lines = lines[:maxl]
        lines[-1] += '…'
    return lines

def thumb(title):
    short = re.split(r'[:：]', title)[0].strip()
    lines = wrap(short)
    f = "font-family=\"'Noto Sans Devanagari','Mukta',Arial,sans-serif\""
    texts = ''
    for i, l in enumerate(lines):
        color = '#b7f36b' if i == len(lines) - 1 else '#ffffff'
        texts += f'<text x="70" y="{230 + i*96}" {f} font-size="76" font-weight="800" fill="{color}">{html.escape(l)}</text>\n'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#071a18"/><stop offset="1" stop-color="#1b4a33"/></linearGradient>
<radialGradient id="glow" cx="0.8" cy="0.2" r="0.6"><stop offset="0" stop-color="#b7f36b" stop-opacity="0.35"/><stop offset="1" stop-color="#b7f36b" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1200" height="630" fill="url(#bg)"/>
<rect width="1200" height="630" fill="url(#glow)"/>
<g stroke="#b7f36b" stroke-width="6" stroke-linecap="round">
<line x1="990" y1="40" x2="990" y2="75"/><line x1="990" y1="205" x2="990" y2="240"/>
<line x1="885" y1="140" x2="920" y2="140"/><line x1="1060" y1="140" x2="1095" y2="140"/>
<line x1="916" y1="66" x2="940" y2="90"/><line x1="1040" y1="190" x2="1064" y2="214"/>
<line x1="1064" y1="66" x2="1040" y2="90"/><line x1="940" y1="190" x2="916" y2="214"/>
</g>
<circle cx="990" cy="140" r="52" fill="#b7f36b"/>
<g transform="translate(690,330) skewX(-18)">
<rect width="440" height="230" rx="10" fill="#0e3a30" stroke="#b7f36b" stroke-width="5"/>
<g stroke="#b7f36b" stroke-opacity="0.7" stroke-width="3">
<line x1="110" y1="0" x2="110" y2="230"/><line x1="220" y1="0" x2="220" y2="230"/><line x1="330" y1="0" x2="330" y2="230"/>
<line x1="0" y1="77" x2="440" y2="77"/><line x1="0" y1="153" x2="440" y2="153"/>
</g></g>
<rect x="70" y="70" width="250" height="52" rx="26" fill="#183a2b"/>
<text x="195" y="106" text-anchor="middle" {f} font-size="28" font-weight="700" fill="#b7f36b">ताज़ा जानकारी</text>
{texts}<text x="70" y="570" {f} font-size="36" font-weight="800" fill="#ffffff">योजना<tspan fill="#b7f36b">ऊर्जा</tspan></text>
</svg>'''

articles = []
for fn in sorted(glob.glob('*.html')):
    if fn in SKIP or fn.startswith('google'):
        continue
    src = open(fn, encoding='utf-8').read()
    t = re.search(r'<title>(.*?)</title>', src, re.S)
    d = re.search(r'<meta name="description" content="(.*?)"', src, re.S)
    title = html.unescape(t.group(1)).split(' | ')[0].strip() if t else fn
    desc = html.unescape(d.group(1)).strip() if d else ''
    if len(desc) > 110:
        desc = desc[:107].rstrip() + '...'
    slug = fn[:-5]
    articles.append({'slug': slug, 'title': title, 'desc': desc, 'date': old.get(slug, today)})

articles.sort(key=lambda a: (a['date'], a['slug']), reverse=True)

os.makedirs('thumbs', exist_ok=True)
for a in articles:
    open(f"thumbs/{a['slug']}.svg", 'w', encoding='utf-8').write(thumb(a['title']))

json.dump(articles, open('articles.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

urls = [('', '1.0', 'daily'), ('about.html', '0.6', 'monthly'), ('contact.html', '0.6', 'monthly'),
        ('privacy-policy.html', '0.5', 'yearly'), ('disclaimer.html', '0.5', 'yearly')]
out = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p, pr, cf in urls:
    out += f'  <url>\n    <loc>{BASE}/{p}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n'
for a in articles:
    out += f'  <url>\n    <loc>{BASE}/{a["slug"]}.html</loc>\n    <lastmod>{a["date"]}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
out += '</urlset>\n'
open('sitemap.xml', 'w', encoding='utf-8').write(out)
print('done', len(articles), 'articles')

for fn in glob.glob('*.html'):
    if fn.startswith('google') or fn in NO_ADS:
        continue
    page = open(fn, encoding='utf-8').read()
    add = ''
    for tag in TAGS:
        if tag not in page:
            add += tag + '\n'
    if add and '</body>' in page:
        open(fn, 'w', encoding='utf-8').write(page.replace('</body>', add + '</body>'))
        print('ads added to', fn)
