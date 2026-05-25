import os, re, json

today = '2026-05-25'
jekyll_dir = '/home/chubert/alma/_site'
pages_path = '/home/chubert/omni-builder/sites/site_alma/data/pages.json'
report_path = '/home/chubert/omni-builder/sites/site_alma/Master_Report.json'

def extract_main(html):
    m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    return m.group(1).strip() if m else None

def extract_title(html):
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
    return m.group(1).strip() if m else ''

# Load existing pages.json
with open(pages_path) as f:
    existing = json.load(f)
existing_slugs = {p['slug'] for p in existing}

added = []
skipped = []

# Walk entire _site
for root, dirs, files in os.walk(jekyll_dir):
    for fname in files:
        if fname != 'index.html':
            continue
        full_path = os.path.join(root, fname)
        rel = os.path.relpath(full_path, jekyll_dir)
        # slug = directory path, root index = 'index'
        slug = os.path.dirname(rel).replace(os.sep, '/')
        if slug == '.':
            slug = 'index'
        if slug in existing_slugs:
            continue
        with open(full_path, encoding='utf-8', errors='ignore') as f:
            raw = f.read()
        body = extract_main(raw)
        title = extract_title(raw)
        if not body:
            skipped.append(slug)
            continue
        existing.append({'slug': slug, 'title': title, 'body_content': body})
        existing_slugs.add(slug)
        added.append(slug)

with open(pages_path, 'w') as f:
    json.dump(existing, f, indent=2)

# Update Master Report
with open(report_path) as f:
    r = json.load(f)
r['data_schema']['pages.json']['total_pages'] = len(existing)
r['data_schema']['pages.json']['slugs'] = 'see pages.json — too many to list'
r['content_status']['pages_built'] = f'{len(existing)} total pages'
r['content_status']['last_build'] = 'pending'
r['content_status']['jekyll_source'] = jekyll_dir
r['changelog'].append({
    'date': today,
    'change': f'Bulk extracted {len(added)} pages from Jekyll _site into pages.json. {len(skipped)} skipped (no <main>). Total pages now: {len(existing)}'
})
r['last_updated'] = today
with open(report_path, 'w') as f:
    json.dump(r, f, indent=2)

print(f'SUCCESS: added {len(added)} pages, skipped {len(skipped)}, total {len(existing)}')
if skipped:
    print(f'Skipped (no <main>): {skipped[:10]}{"..." if len(skipped)>10 else ""}')
