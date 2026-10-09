#!/usr/bin/env python3
"""Busca as últimas notícias da Agência Sebrae (RSS) e grava noticias.json.
Roda automaticamente pelo GitHub Actions (.github/workflows/noticias.yml).
Usa só a biblioteca padrão do Python."""
import json, re, html, sys, datetime, email.utils, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEEDS = [('Agência Sebrae', 'https://agenciasebrae.com.br/feed/')]
OUT = Path(__file__).resolve().parent.parent / 'noticias.json'
LIMIT = 24


def clean(s, n=None):
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s*(O post .*? apareceu primeiro em .*)$', '', s)
    if n and len(s) > n:
        s = s[:n].rsplit(' ', 1)[0].rstrip(',.;:') + '…'
    return s


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (BRK Consultoria Financeira news bot)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main():
    items = []
    for source, url in FEEDS:
        try:
            root = ET.fromstring(fetch(url))
        except Exception as e:
            print('falha ao ler', url, e, file=sys.stderr)
            continue
        for it in root.iter('item'):
            g = lambda t: (it.findtext(t) or '').strip()
            try:
                dt = email.utils.parsedate_to_datetime(g('pubDate')).astimezone(datetime.timezone.utc)
            except Exception:
                dt = datetime.datetime.now(datetime.timezone.utc)
            items.append({'title': clean(g('title')), 'link': g('link'), 'date': dt.isoformat(),
                          'category': clean(g('category')), 'summary': clean(g('description'), 220), 'source': source})
    if not items:
        print('nenhuma notícia obtida; mantendo arquivo atual')
        return
    items.sort(key=lambda x: x['date'], reverse=True)
    data = {'updated': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'items': items[:LIMIT]}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    print('notícias:', len(data['items']))


if __name__ == '__main__':
    main()
