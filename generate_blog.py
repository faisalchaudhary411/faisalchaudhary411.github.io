import json
import os
import re
from datetime import datetime

# Read blog posts from JSON
try:
    with open('blog_posts.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
except FileNotFoundError:
    posts = []

# Ensure blog directory exists
os.makedirs('blog', exist_ok=True)

# Shared CSS/JS for all blog pages
SHARED_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow">
  <meta name="author" content="VoxCraft Studio">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{og_title}">
  <meta name="twitter:description" content="{og_desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root { --bg: #0a0812; --surface: #120f1e; --border: rgba(255,255,255,0.07); --purple: #7c3aed; --violet: #a78bfa; --blue: #60a5fa; --text: #f1f0f5; --muted: rgba(255,255,255,0.45); --faint: rgba(255,255,255,0.08); }
    body { background: var(--bg); color: var(--text); font-family: 'DM Sans', sans-serif; font-size: 16px; line-height: 1.7; }
    nav { position: fixed; top: 0; left: 0; right: 0; z-index: 100; display: flex; align-items: center; justify-content: space-between; padding: 1rem 2rem; background: rgba(10,8,18,0.85); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); }
    .nav-logo { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.25rem; background: linear-gradient(135deg, #fff 0%, var(--violet) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-decoration: none; }
    .nav-links { display: flex; gap: 1.5rem; align-items: center; }
    .nav-links a { color: var(--muted); text-decoration: none; font-size: 0.9rem; transition: color 0.2s; }
    .nav-links a:hover { color: var(--text); }
    .nav-cta { background: var(--purple); color: white !important; padding: 0.45rem 1.1rem; border-radius: 8px; font-weight: 500; font-size: 0.88rem !important; text-decoration: none; transition: background 0.2s; }
    .nav-cta:hover { background: #6d28d9; }
    main { max-width: 720px; margin: 0 auto; padding: 7rem 1.5rem 4rem; }
    .blog-meta { display: inline-block; background: rgba(124,58,237,0.1); border: 1px solid rgba(124,58,237,0.2); border-radius: 8px; padding: 0.3rem 0.8rem; font-size: 0.75rem; color: var(--violet); margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.08em; }
    h1 { font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800; line-height: 1.15; margin-bottom: 1rem; }
    h2 { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; color: var(--violet); margin-top: 2rem; margin-bottom: 0.75rem; }
    h3 { font-size: 1.1rem; font-weight: 600; color: var(--text); margin-top: 1.5rem; margin-bottom: 0.5rem; }
    p { color: var(--muted); margin-bottom: 1rem; }
    ul, ol { color: var(--muted); margin: 0 0 1rem 1.5rem; }
    li { margin-bottom: 0.4rem; }
    a { color: var(--violet); text-decoration: none; }
    a:hover { text-decoration: underline; }
    code { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 0.15rem 0.4rem; font-family: monospace; font-size: 0.9em; color: var(--violet); }
    pre { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; overflow-x: auto; margin-bottom: 1rem; }
    pre code { background: none; border: none; padding: 0; }
    blockquote { border-left: 3px solid var(--purple); padding-left: 1rem; margin: 1.5rem 0; color: var(--muted); font-style: italic; }
    img { max-width: 100%; border-radius: 8px; margin: 1rem 0; }
    .back-link { display: inline-flex; align-items: center; gap: 0.4rem; color: var(--muted); font-size: 0.9rem; margin-bottom: 1.5rem; }
    .back-link:hover { color: var(--violet); }
    footer { border-top: 1px solid var(--border); padding: 2rem 1.5rem; text-align: center; margin-top: 3rem; }
    .footer-links { display: flex; flex-wrap: wrap; gap: 1.5rem; justify-content: center; margin-bottom: 0.75rem; }
    .footer-links a { color: var(--muted); text-decoration: none; font-size: 0.85rem; }
    .footer-links a:hover { color: var(--text); }
    .footer-copy { font-size: 0.8rem; color: rgba(255,255,255,0.2); }
    @media (max-width: 600px) { nav { padding: 0.9rem 1.2rem; } .nav-links a:not(.nav-cta) { display: none; } main { padding: 6rem 1.2rem 3rem; } }
  </style>
</head>
<body>
<nav>
  <a class="nav-logo" href="/">VoxCraft</a>
  <div class="nav-links">
    <a href="/blog/">Blog</a>
    <a href="/">Home</a>
    <a href="https://app.voxcraft.site" class="nav-cta" target="_blank">Launch App &rarr;</a>
  </div>
</nav>
<main>
"""

SHARED_FOOT = """</main>
<footer>
  <div class="footer-links">
    <a href="/">Home</a>
    <a href="/blog/">Blog</a>
    <a href="/privacy.html">Privacy</a>
    <a href="/terms.html">Terms</a>
    <a href="/contact.html">Contact</a>
    <a href="/about.html">About</a>
  </div>
  <div class="footer-copy">&copy; 2026 VoxCraft Studio</div>
</footer>
</body>
</html>"""

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:80]

def format_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%B %d, %Y")
    except:
        return date_str

def content_to_html(content):
    html = content
    html = html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    html = re.sub(r'^&gt; (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    lines = html.split('\n')
    result = []
    in_list = False
    list_type = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                result.append('<ul>')
                in_list = True
                list_type = 'ul'
            result.append('<li>' + stripped[2:] + '</li>')
        elif re.match(r'^\d+\. ', stripped):
            if not in_list:
                result.append('<ol>')
                in_list = True
                list_type = 'ol'
            result.append('<li>' + re.sub(r'^\d+\. ', '', stripped) + '</li>')
        else:
            if in_list:
                result.append('</' + list_type + '>')
                in_list = False
                list_type = None
            if stripped:
                result.append('<p>' + line + '</p>')

    if in_list:
        result.append('</' + list_type + '>')

    html = '\n'.join(result)
    html = re.sub(r'<p>\s*</p>', '', html)
    return html

# Generate individual post pages
post_slugs = []
for post in posts:
    slug = slugify(post.get('title', 'untitled'))
    post_slugs.append({
        'slug': slug,
        'title': post.get('title', 'Untitled'),
        'date': post.get('date', ''),
        'category': post.get('category', 'Guide'),
        'excerpt': post.get('excerpt', '')
    })

    filename = 'blog/' + slug + '.html'

    title = post.get('title', 'Untitled') + ' &mdash; VoxCraft Studio'
    description = post.get('excerpt', 'Read this guide on VoxCraft Studio.')
    canonical = 'https://voxcraft.site/blog/' + slug + '.html'
    og_title = post.get('title', 'Untitled')
    og_desc = post.get('excerpt', '')

    content_html = content_to_html(post.get('content', ''))
    date_formatted = format_date(post.get('date', ''))
    category = post.get('category', 'Guide')

    html = SHARED_HEAD.format(
        title=title, description=description, canonical=canonical,
        og_title=og_title, og_desc=og_desc
    )

    html += '<a href="/blog/" class="back-link">&larr; Back to Blog</a>\n'
    html += '<div class="blog-meta">' + category + ' &middot; ' + date_formatted + '</div>\n'
    html += '<h1>' + post.get('title', 'Untitled') + '</h1>\n'
    html += content_html + '\n'
    html += SHARED_FOOT

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print('Generated: ' + filename)

# Generate blog index page
index_html = SHARED_HEAD.format(
    title='Blog &mdash; VoxCraft Studio | AI Audio Tips &amp; Guides',
    description='Guides, tutorials, and tips for AI text-to-speech, voice generation, and audio content creation.',
    canonical='https://voxcraft.site/blog/',
    og_title='VoxCraft Blog',
    og_desc='Guides, tutorials, and AI audio tips'
)

index_html += '<h1>VoxCraft Blog</h1>\n'
index_html += '<p style="color: var(--muted); margin-bottom: 2rem;">Guides, tutorials, and tips for AI audio creation</p>\n'
index_html += '<div style="display: flex; flex-direction: column; gap: 1.5rem;">\n'

for post in post_slugs:
    index_html += '<article style="background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem;">\n'
    index_html += '  <div class="blog-meta">' + post['category'] + ' &middot; ' + format_date(post['date']) + '</div>\n'
    index_html += '  <h2 style="margin-top: 0.5rem; font-size: 1.2rem;"><a href="/blog/' + post['slug'] + '.html">' + post['title'] + '</a></h2>\n'
    index_html += '  <p style="margin-bottom: 0;">' + post['excerpt'] + '</p>\n'
    index_html += '</article>\n'

index_html += '</div>\n'
index_html += SHARED_FOOT

with open('blog/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print('Generated: blog/index.html')

# Generate sitemap
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += '  <url><loc>https://voxcraft.site/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
sitemap += '  <url><loc>https://voxcraft.site/blog/</loc><changefreq>daily</changefreq><priority>0.9</priority></url>\n'
sitemap += '  <url><loc>https://voxcraft.site/privacy.html</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>\n'
sitemap += '  <url><loc>https://voxcraft.site/terms.html</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>\n'
sitemap += '  <url><loc>https://voxcraft.site/contact.html</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>\n'
sitemap += '  <url><loc>https://voxcraft.site/about.html</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'

for post in post_slugs:
    sitemap += '  <url><loc>https://voxcraft.site/blog/' + post['slug'] + '.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'

sitemap += '</urlset>'

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

print('Generated: sitemap.xml')
print('Total posts generated: ' + str(len(posts)))
