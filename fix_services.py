import os, re, json

today = '2026-05-25'
pages_path = '/home/chubert/omni-builder/sites/site_alma/data/pages.json'
report_path = '/home/chubert/omni-builder/sites/site_alma/Master_Report.json'

slugs = [
    'services/end-of-tenancy-clearance',
    'services/bereavement-clearance',
    'services/commercial-clearance',
    'services/house-clearance',
    'services/garage-clearance',
    'services/loft-clearance',
    'services/hoarder-clearance',
    'services/probate-clearance'
]

def extract_content(html):
    # Strip nav
    html = re.sub(r'<nav\b[^>]*>.*?</nav>', '', html, flags=re.DOTALL)
    # Strip footer
    html = re.sub(r'<footer\b[^>]*>.*?</footer>', '', html, flags=re.DOTALL)
    # Strip fixed floating buttons
    html = re.sub(r'<a[^>]*position:\s*fixed[^>]*>.*?</a>', '', html, flags=re.DOTALL)
    return html.strip()

def extract_title(html):
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
    return m.group(1).strip() if m else ''

with open(pages_path) as f:
    existing = json.load(f)
existing_slugs = {p['slug'] for p in existing}

added = []
failed = []

for slug in slugs:
    if slug in existing_slugs:
        print(f'SKIP {slug}: already exists')
        continue
    html_path = f'/home/chubert/alma/_site/{slug}/index.html'
    if not os.path.exists(html_path):
        failed.append(slug)
        print(f'MISSING: {html_path}')
        continue
    with open(html_path, encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    body = extract_content(raw)
    title = extract_title(raw)
    if not body:
        failed.append(slug)
        print(f'FAILED: empty content for {slug}')
        continue
    existing.append({'slug': slug, 'title': title, 'body_content': body})
    existing_slugs.add(slug)
    added.append(slug)
    print(f'OK: {slug}')

with open(pages_path, 'w') as f:
    json.dump(existing, f, indent=2)

with open(report_path) as f:
    r = json.load(f)
r['data_schema']['pages.json']['total_pages'] = len(existing)
r['content_status']['pages_built'] = f'{len(existing)} total pages'
r['changelog'].append({
    'date': today,
    'change': f'Fixed {len(added)} service pages (no html/body tags) by stripping nav/footer from raw content: {added}'
})
r['last_updated'] = today
with open(report_path, 'w') as f:
    json.dump(r, f, indent=2)

print(f'SUCCESS: added {len(added)}, failed {len(failed)}, total {len(existing)}')
