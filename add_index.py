import json, re

pages_path = '/home/chubert/omni-builder/sites/site_alma/data/pages.json'
jekyll_path = '/home/chubert/alma/_site/index.html'

with open(jekyll_path) as f:
    raw = f.read()

match = re.search(r'<main[^>]*>(.*?)</main>', raw, re.DOTALL)
if not match:
    print('ERROR: no <main> found')
    exit(1)

body = match.group(1).strip()

with open(pages_path) as f:
    pages = json.load(f)

slugs = [p['slug'] for p in pages]
if 'index' in slugs:
    print('index already exists - skipping')
    exit(0)

pages.insert(0, {
    'slug': 'index',
    'title': 'House Clearance Cumbria | Alma Enterprises',
    'body_content': body
})

with open(pages_path, 'w') as f:
    json.dump(pages, f, indent=2)

print('SUCCESS: index page added')
