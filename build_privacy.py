#!/usr/bin/env python3
"""Rebuilds diel/privacy/index.html from Diel's docs/privacy-policy.md.
Usage: python3 build_privacy.py path/to/BioTracker/docs/privacy-policy.md"""
import html, re, sys

HEAD = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>Diel Privacy Policy</title>\n<style>\n:root { color-scheme: light dark; --bg:#ffffff; --text:#14181c; --muted:#5d6670; --accent:#1f9e86; }\n@media (prefers-color-scheme: dark) { :root { --bg:#0e1114; --text:#eef1f3; --muted:#9aa3ab; --accent:#4fd1b5; } }\nbody { margin:0; background:var(--bg); color:var(--text); font:17px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }\nmain { max-width:680px; margin:0 auto; padding:48px 20px 64px; }\nh1 { font-size:2rem; margin:0 0 4px; }\nh2 { font-size:1.15rem; margin:32px 0 6px; }\np { margin:0 0 12px; }\n.date { color:var(--muted); font-size:.95rem; margin-bottom:28px; }\na { color:var(--accent); }\n</style>\n</head>\n<body>\n'

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w])_([^_]+)_(?![\w])', r'<em>\1</em>', t)
    return t

body = ['<main>', '<h1>Diel Privacy Policy</h1>']
for line in open(sys.argv[1]).read().splitlines():
    if not line.strip() or line.startswith('Keep this in step') or line.startswith('# '):
        continue
    if line.startswith('## '):
        body.append('<h2>%s</h2>' % inline(line[3:]))
    elif line.startswith('_Effective'):
        body.append('<p class="date">%s</p>' % inline(line.strip('_')))
    else:
        body.append('<p>%s</p>' % inline(line))
body += ['</main>', '</body>', '</html>', '']
open('diel/privacy/index.html', 'w').write(HEAD + '\n'.join(body))
