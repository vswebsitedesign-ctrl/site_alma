#!/usr/bin/env python3
import json, os, shutil, sys

DOMAIN = "https://alma-enterprises.co.uk"
EXCLUDED_SLUGS = {'footer', 'navigation', 'cta', 'location', 'service-location', ''}

def build():
    pages_path = 'data/pages.json'
    if not os.path.exists(pages_path):
        print("ERROR: pages.json not found")
        sys.exit(1)
    with open(pages_path, 'r') as f:
        pages = json.load(f)
    with open('theme/base.html', 'r') as f:
        template = f.read()
    if os.path.exists('build'):
        shutil.rmtree('build')
    os.makedirs('build')

    sitemap_urls = []

    for page in pages:
        slug = page['slug']

        # Skip Jekyll template fragments
        if slug in EXCLUDED_SLUGS:
            continue

        content = page.get('body_content', '')
        title = page.get('title', '')
        description = page.get('description', '')

        # Homepage slug fix — canonical and og:url must output / not /index/
        if slug == 'index':
            canonical_slug = ''
        else:
            canonical_slug = slug

        canonical_url = f"{DOMAIN}/{canonical_slug}/" if canonical_slug else f"{DOMAIN}/"

        html = template
        html = html.replace('{{ content }}', content)
        html = html.replace('{{ title }}', title)
        html = html.replace('{{ description }}', description)
        html = html.replace('{{ slug }}/', canonical_slug + '/' if canonical_slug else '')
        html = html.replace('{{ slug }}', canonical_slug)

        out_dir = os.path.join('build', slug) if slug else 'build'
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w') as f:
            f.write(html)

        sitemap_urls.append(canonical_url)

    # Copy homepage to build/index.html
    src = os.path.join('build', 'index', 'index.html')
    if os.path.exists(src):
        shutil.copy(src, 'build/index.html')

    # Generate sitemap.xml
    with open('build/sitemap.xml', 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in sitemap_urls:
            f.write(f'  <url><loc>{url}</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>\n')
        f.write('</urlset>\n')

    # Generate robots.txt
    with open('build/robots.txt', 'w') as f:
        f.write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')

    # Copy assets
    if os.path.exists('assets'):
        shutil.copytree('assets', 'build/assets', dirs_exist_ok=True)

    print(f"Built {len([p for p in pages if p['slug'] not in EXCLUDED_SLUGS])} pages (skipped {len(EXCLUDED_SLUGS)} junk slugs)")
    print(f"sitemap.xml generated with {len(sitemap_urls)} URLs")
    print(f"robots.txt generated")

if __name__ == '__main__':
    build()
