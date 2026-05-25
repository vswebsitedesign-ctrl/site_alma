import os, re, json

today = '2026-05-25'
pages_path = '/home/chubert/omni-builder/sites/site_alma/data/pages.json'
report_path = '/home/chubert/omni-builder/sites/site_alma/Master_Report.json'

skipped = [
    'about-us',
    'services/end-of-tenancy-clearance',
    'services/bereavement-clearance',
    'services/commercial-clearance',
    'services/house-clearance',
    'services/garage-clearance',
    'services/loft-clearance',
    'services/hoarder-clearance',
    'services/probate-clearance'
]

def extract_body_content(html):
    # Strip nav block
    html = re.sub(r'<nav\b[^>]*>.*?</nav>', '', html, flags=re.DOTALL)
    # Strip footer block
    html = re.sub(r'<footer\b[^>]*>.*?</footer>', '', html, flags=re.DOTALL)
    # Strip fixed floating buttons (contact/call)
    html = re.sub(r'<a[^>]*position:\s*fixed[^>]*>.*?</a>', '', html, flags=re.DOTALL)
    # Extract body contents
    m = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if not m:
        return None
    return m.group(1).strip()

def extract_title(html):
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
    return m.group(1).strip() if m else ''

with open(pages_path) as f:
    existing = json.load(f)
existing_slugs = {p['slug'] for p in existing}

added = []
failed = []

for slug in skipped:
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
    body = extract_body_content(raw)
    title = extract_title(raw)
    if not body:
        failed.append(slug)
        print(f'FAILED: no body content found for {slug}')
        continue
    existing.append({'slug': slug, 'title': title, 'body_content': body})
    existing_slugs.add(slug)
    added.append(slug)

with open(pages_path, 'w') as f:
    json.dump(existing, f, indent=2)

with open(report_path) as f:
    r = json.load(f)
r['data_schema']['pages.json']['total_pages'] = len(existing)
r['content_status']['pages_built'] = f'{len(existing)} total pages'
r['changelog'].append({
    'date': today,
    'change': f'Fixed {len(added)} skipped pages (no <main> tag) by extracting <body> minus nav/footer: {added}'
})
r['last_updated'] = today
with open(report_path, 'w') as f:
    json.dump(r, f, indent=2)

print(f'SUCCESS: added {len(added)}, failed {len(failed)}, total {len(existing)}')
