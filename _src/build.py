#!/usr/bin/env python3
"""Gerador do site BRK Gestão Financeira.

Cada página fica em _src/pages/*.html ou _src/blog/*.html, com um bloco de
metadados no topo:  <!--meta { ...json... } -->
Rodar:  python3 _src/build.py
(Pastas que começam com "_" não são publicadas pelo GitHub Pages.)
"""
import json, re, html, datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / '_src'

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO — ao comprar o domínio, troque BASE_URL (ex.: https://brkgestao.com.br/)
# ---------------------------------------------------------------------------
GA4_ID = ''      # ex.: G-XXXXXXX
META_PIXEL_ID = ''  # ex.: 1234567890
TRACK = ''
if GA4_ID:
    TRACK += f'\n<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA4_ID}");</script>'
if META_PIXEL_ID:
    TRACK += f'\n<script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version="2.0";n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,"script","https://connect.facebook.net/en_US/fbevents.js");fbq("init","{META_PIXEL_ID}");fbq("track","PageView");</script>'
BASE_URL = 'https://brkconsultoriafinanceira.com.br/'
BRAND = 'BRK Gestão Financeira'
WHATSAPP = ''
WHATSAPP_DISPLAY = '@brkgestaofinanceira'
WA_TEXT = 'Olá! Vim pelo site da BRK e gostaria de agendar um diagnóstico financeiro gratuito.'
INSTAGRAM = 'https://instagram.com/brkgestaofinanceira'
INSTAGRAM_HANDLE = '@brkgestaofinanceira'
LINKEDIN = ''
CITIES = ['Mauá', 'Santo André', 'São Bernardo do Campo', 'São Caetano do Sul', 'Diadema', 'Ribeirão Pires', 'Rio Grande da Serra']
TODAY = datetime.date.today().isoformat()

WA_URL = 'https://ig.me/m/brkgestaofinanceira'

ICON = {
    'wa': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.49s1.07 2.89 1.22 3.09c.15.2 2.1 3.2 5.08 4.49.71.31 1.27.49 1.7.63.72.23 1.37.2 1.88.12.57-.09 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35zM12.05 21.5h-.01a9.43 9.43 0 0 1-4.8-1.32l-.35-.2-3.57.93.95-3.48-.22-.36A9.41 9.41 0 0 1 2.6 12.05C2.6 6.84 6.84 2.6 12.06 2.6c2.52 0 4.9.99 6.68 2.77a9.37 9.37 0 0 1 2.76 6.68c0 5.21-4.24 9.45-9.45 9.45zm8.04-17.49A11.27 11.27 0 0 0 12.05.7C5.79.7.7 5.79.7 12.05c0 2 .52 3.95 1.52 5.67L.6 23.3l5.72-1.5a11.3 11.3 0 0 0 5.73 1.46h.01c6.26 0 11.35-5.09 11.35-11.35 0-3.03-1.18-5.88-3.32-8.02z"/></svg>',
    'ig': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.8" fill="currentColor"/></svg>',
    'li': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4v11H3v-11zm6.5 0h3.8v1.5h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1v5.45h-4v-4.83c0-1.15-.02-2.63-1.6-2.63-1.6 0-1.85 1.25-1.85 2.55v4.91h-4v-11z"/></svg>',
    'dl': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 19h14"/></svg>',
    'lock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="5" y="11" width="14" height="9" rx="1"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>',
    'pin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    'clock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3 7l9 6 9-6"/></svg>',
}

NAV = [
    ('servicos.html', 'Serviços'),
    ('situacao.html', 'Sua situação'),
    ('blog/', 'Blog'),
]
SCRIPTS = {'chart': 'vendor/chart.umd.js', 'tools': 'tools.js', 'situacao': 'situacao.js', 'news': 'news.js'}


def esc(s):
    return html.escape(s, quote=True)


def read_page(path):
    raw = path.read_text(encoding='utf-8')
    m = re.match(r'\s*<!--meta\s*(\{.*?\})\s*-->\s*', raw, re.S)
    if not m:
        raise SystemExit(f'Sem metadados: {path}')
    meta = json.loads(m.group(1))
    meta['body'] = raw[m.end():]
    return meta


def org_schema():
    return {
        '@context': 'https://schema.org',
        '@type': ['ProfessionalService', 'FinancialService'],
        '@id': BASE_URL + '#organizacao',
        'name': BRAND,
        'alternateName': 'BRK Gestão',
        'description': 'Consultoria financeira para pequenas empresas, MEIs e pessoas físicas em Mauá, Santo André e em todo o Grande ABC, com atendimento online para todo o Brasil. Fluxo de caixa, DRE, precificação, organização de dívidas e educação financeira.',
        'url': BASE_URL,
        'logo': BASE_URL + 'logo.png',
        'image': BASE_URL + 'og-image.png',
        'priceRange': '$$',
        'slogan': 'Salvar empresas e dar liberdade financeira às pessoas, por meio da educação e do direcionamento correto.',
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Mauá', 'addressRegion': 'SP', 'addressCountry': 'BR'},
        'areaServed': [{'@type': 'City', 'name': c} for c in CITIES] + [
            {'@type': 'AdministrativeArea', 'name': 'Grande ABC Paulista'},
            {'@type': 'Country', 'name': 'Brasil'}],
        'sameAs': [INSTAGRAM],
        'knowsAbout': ['Consultoria financeira', 'Fluxo de caixa', 'DRE', 'Precificação', 'Capital de giro',
                       'Ponto de equilíbrio', 'Finanças pessoais', 'Renegociação de dívidas', 'Educação financeira', 'Gestão financeira para MEI'],
        'hasOfferCatalog': {
            '@type': 'OfferCatalog', 'name': 'Serviços de consultoria financeira',
            'itemListElement': [
                {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Consultoria financeira para pequenas empresas', 'url': BASE_URL + 'consultoria-financeira-empresas.html'}},
                {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Consultoria financeira pessoal', 'url': BASE_URL + 'consultoria-financeira-pessoal.html'}},
                {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Consultoria financeira para MEI', 'url': BASE_URL + 'consultoria-financeira-mei.html'}},
                {'@type': 'Offer', 'price': '0', 'priceCurrency': 'BRL', 'itemOffered': {'@type': 'Service', 'name': 'Programa Piloto de CFO terceirizado (3 vagas, 60 dias)'}},
            ]},
    }


def breadcrumb_schema(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE_URL + u}
                                for i, (n, u) in enumerate(items)]}


def faq_schema(faq):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q,
                            'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in faq]}


def faq_html(faq):
    items = '\n'.join(f'<details><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>' for q, a in faq)
    return f'<div class="faq">{items}</div>'


def gate_html(p):
    return f'''
<div class="gate" id="gate" role="dialog" aria-modal="true" aria-labelledby="gate-title" aria-hidden="true">
  <div class="gate-panel">
    <button type="button" class="gate-close js-gate-close" aria-label="Fechar">&times;</button>
    <span class="eyebrow">Biblioteca BRK</span>
    <h2 id="gate-title">Libere seus Guias Fundamentais</h2>
    <p class="gate-intro">Os dois guias são gratuitos. Para liberar o acesso, siga a BRK no Instagram — é onde publicamos conteúdo sobre finanças para empresas e pessoas.</p>
    <div class="gate-progress"><span></span></div>
    <p class="gate-count"><span class="js-count">0</span> de 1 etapa concluída</p>
    <a class="gate-step" data-step="instagram" href="{INSTAGRAM}" target="_blank" rel="noopener">
      <span class="ic">{ICON['ig']}</span><span class="tx"><b>Seguir no Instagram</b><small>{INSTAGRAM_HANDLE}</small></span><span class="st">Seguir</span>
    </a>
    <div class="gate-downloads">
      <a href="{p}guia-preparacao-financeira-pf.pdf" class="btn btn-solid" download>{ICON['dl']} Guia Pessoa Física (PDF)</a>
      <a href="{p}guia-preparacao-gestao-pj.pdf" class="btn" download>{ICON['dl']} Guia Pessoa Jurídica (PDF)</a>
    </div>
    <p class="gate-note gate-note-pending">Siga no Instagram e volte para esta tela. O download é liberado em seguida.</p>
    <p class="gate-note gate-note-done">Acesso liberado. Obrigado por acompanhar — bom estudo!</p>
  </div>
</div>'''


def layout(meta, body, out_path):
    depth = len(Path(out_path).parts) - 1
    p = BASE_URL if meta.get('absolute_assets') else '../' * depth
    url_path = meta.get('url', out_path)
    if url_path.endswith('index.html'):
        url_path = url_path[:-len('index.html')]
    canonical = BASE_URL + url_path
    title = meta['title']
    desc = meta['description']
    og_type = 'article' if meta.get('type') == 'article' else 'website'

    schemas = []
    if meta.get('org_schema'):
        schemas.append(org_schema())
    if meta.get('breadcrumb'):
        schemas.append(breadcrumb_schema(meta['breadcrumb']))
    if meta.get('faq'):
        schemas.append(faq_schema(meta['faq']))
    if meta.get('type') == 'article':
        schemas.append({
            '@context': 'https://schema.org', '@type': 'Article',
            'headline': meta['h1'], 'description': desc,
            'datePublished': meta['date'], 'dateModified': meta.get('updated', meta['date']),
            'mainEntityOfPage': canonical, 'image': BASE_URL + 'og-image.png', 'inLanguage': 'pt-BR',
            'author': {'@type': 'Organization', 'name': BRAND, 'url': BASE_URL},
            'publisher': {'@type': 'Organization', 'name': BRAND, 'logo': {'@type': 'ImageObject', 'url': BASE_URL + 'logo.png'}},
        })
    if meta.get('app'):
        schemas.append({'@context': 'https://schema.org', '@type': 'WebApplication', 'name': meta['app'], 'description': desc,
                        'url': canonical, 'applicationCategory': 'FinanceApplication', 'operatingSystem': 'Web', 'inLanguage': 'pt-BR',
                        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'BRL'},
                        'provider': {'@type': 'Organization', 'name': BRAND, 'url': BASE_URL}})
    if meta.get('service'):
        s = meta['service']
        schemas.append({
            '@context': 'https://schema.org', '@type': 'Service', 'name': s['name'], 'description': desc,
            'serviceType': s['type'], 'url': canonical,
            'provider': {'@id': BASE_URL + '#organizacao', '@type': 'ProfessionalService', 'name': BRAND},
            'areaServed': [{'@type': 'City', 'name': c} for c in CITIES] + [{'@type': 'Country', 'name': 'Brasil'}],
            'audience': {'@type': 'Audience', 'audienceType': s['audience']},
        })
    ld = '\n'.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)

    active = meta.get('nav')
    cur = ' aria-current="page"'
    nav = '\n'.join(
        f'<a href="{p}{href}"{cur if active == href else ""}>{label}</a>' for href, label in NAV)

    faq_block = ''
    if meta.get('faq') and '<!--FAQ-->' in body:
        body = body.replace('<!--FAQ-->', faq_html(meta['faq']))
    wa_ctx = WA_URL
    body = body.replace('{{WA_CTX}}', esc(wa_ctx))
    body = body.replace('{{P}}', p).replace('{{WA}}', esc(WA_URL)).replace('{{WA_ICON}}', ICON['ig']) \
               .replace('{{LOCK}}', ICON['lock']).replace('{{DL}}', ICON['dl']).replace('{{IG}}', INSTAGRAM) \
               .replace('{{LI}}', LINKEDIN).replace('{{WA_DISPLAY}}', WHATSAPP_DISPLAY) \
               .replace('{{ICON_PIN}}', ICON['pin']).replace('{{ICON_CLOCK}}', ICON['clock']) \
               .replace('{{ICON_IG}}', ICON['ig']).replace('{{ICON_LI}}', ICON['li'])

    extra_js = ''.join(f'\n<script src="{p}{SCRIPTS[k]}" defer></script>' for k in meta.get('scripts', []))
    robots = 'noindex, follow' if meta.get('noindex') else 'index, follow, max-image-preview:large, max-snippet:-1'

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#050505">
<meta name="geo.region" content="BR-SP">
<meta name="geo.placename" content="Mauá, Santo André, Grande ABC">
<meta property="og:locale" content="pt_BR">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(meta.get('og_title', title))}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{p}favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="{p}favicon-192.png">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}style.css">
{ld}{TRACK}
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="site-header">
  <div class="container header-inner">
    <a href="{p}index.html" class="logo" aria-label="{BRAND} — página inicial"><img src="{p}logo.png" alt="{BRAND}" width="120" height="52"></a>
    <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="menu" aria-label="Menu principal">
      {nav}
      <a href="{p}piloto.html" class="nav-cta">3 vagas grátis</a>
    </nav>
  </div>
</header>
<main id="conteudo">
{body}
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{p}logo.png" alt="{BRAND}" width="166" height="72" loading="lazy">
        <p>Consultoria financeira para pequenas empresas, MEIs e famílias. Salvar empresas e dar liberdade financeira às pessoas.</p>
        <div class="socials">
          <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram da BRK">{ICON['ig']}</a>
        </div>
      </div>
      <div>
        <h2>Serviços</h2>
        <ul>
          <li><a href="{p}consultoria-financeira-empresas.html">Consultoria para empresas</a></li>
          <li><a href="{p}consultoria-financeira-mei.html">Consultoria para MEI</a></li>
          <li><a href="{p}consultoria-financeira-pessoal.html">Consultoria pessoal</a></li>
          <li><a href="{p}servicos.html">Governança e reestruturação</a></li>
          <li><a href="{p}piloto.html">Programa Piloto (3 vagas)</a></li>
        </ul>
      </div>
      <div>
        <h2>Conteúdo grátis</h2>
        <ul>
          <li><a href="{p}situacao.html">Qual é a sua situação?</a></li>
          <li><a href="{p}blog/">Blog</a></li>
          <li><a href="{p}panorama.html">Panorama</a></li>
          <li><a href="{p}noticias.html">Notícias</a></li>
          <li><a href="{p}index.html#guias">Guias em PDF</a></li>
        </ul>
      </div>
      <div>
        <h2>Atendimento</h2>
        <ul>
          <li><a href="{esc(WA_URL)}" target="_blank" rel="noopener">Direct no Instagram {WHATSAPP_DISPLAY}</a></li>
          <li><a href="{p}consultoria-financeira-grande-abc.html">Mauá, Santo André e Grande ABC</a></li>
          <li><a href="{p}contato.html">Online para todo o Brasil</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© {datetime.date.today().year} {BRAND.upper()}</span>
      <span>Consultoria financeira em Mauá, Santo André e Grande ABC · Atendimento online</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{esc(WA_URL)}" target="_blank" rel="noopener" aria-label="Falar com a BRK no Instagram">{ICON['ig']}</a>
<div class="mobile-cta">
  <a href="{esc(WA_URL)}" class="btn btn-wa" target="_blank" rel="noopener">{ICON['ig']} Direct</a>
  <a href="{p}piloto.html" class="btn btn-solid">Quero uma vaga</a>
</div>
{gate_html(p)}
<script src="{p}main.js" defer></script>{extra_js}
</body>
</html>
'''


def tool_card(t, p):
    return f'''<a class="tool-card" href="{p}{t['url']}">
  <span class="pill">{t['tag']}</span>
  <h3>{t['name']}</h3>
  <p>{t['lead']}</p>
  <span class="more">Simular agora →</span>
</a>'''


def post_card(meta, p):
    return f'''<a class="post-card" href="{p}{meta['url']}">
  <span class="post-tag">{meta['tag']}</span>
  <h3>{meta['h1']}</h3>
  <p>{meta['excerpt']}</p>
  <span class="more">Ler →</span>
</a>'''


def main():
    pages = [read_page(f) for f in sorted((SRC / 'pages').glob('*.html'))]
    posts = [read_page(f) for f in sorted((SRC / 'blog').glob('*.html'))]
    for m in posts:
        m['type'] = 'article'
        m.setdefault('nav', 'blog/')
    posts.sort(key=lambda m: m.get('order', 99))

    written = []
    for m in pages + posts:
        out = m['url']
        depth = len(Path(out).parts) - 1
        p = BASE_URL if m.get('absolute_assets') else '../' * depth
        body = m['body']
        # listas automáticas de artigos
        if '<!--POSTS_ALL-->' in body:
            body = body.replace('<!--POSTS_ALL-->', '\n'.join(post_card(x, p) for x in posts))
        if '<!--POSTS_LATEST-->' in body:
            seen, latest = set(), []
            for x in posts:
                if x.get('tag') not in seen:
                    seen.add(x.get('tag')); latest.append(x)
            body = body.replace('<!--POSTS_LATEST-->', '\n'.join(post_card(x, p) for x in latest[:3]))
        if '<!--POSTS_RELATED-->' in body:
            others = [x for x in posts if x['url'] != m['url']]
            rel = ([x for x in others if x.get('tag') == m.get('tag')] + [x for x in others if x.get('tag') != m.get('tag')])[:3]
            body = body.replace('<!--POSTS_RELATED-->', '\n'.join(post_card(x, p) for x in rel))
        target = ROOT / out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(layout(m, body, out), encoding='utf-8')
        if not m.get('noindex'):
            written.append((m, out))
        print('ok', out)

    # sitemap
    urls = []
    for m, out in written:
        loc = BASE_URL + (out[:-len('index.html')] if out.endswith('index.html') else out)
        pr = m.get('priority', '0.7')
        lastmod = m.get('updated', m.get('date', TODAY))
        urls.append(f'  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod><priority>{pr}</priority></url>')
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n', encoding='utf-8')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n', encoding='utf-8')
    print('sitemap', len(urls), 'urls')


if __name__ == '__main__':
    main()
