/* BRK Gestão Financeira — painel de notícias do Sebrae (atualizado automaticamente a cada 3 horas) */
(function () {
    'use strict';
    var boxes = document.querySelectorAll('[data-news]');
    if (!boxes.length) return;
    var LIVE = 'https://raw.githubusercontent.com/brunoomk07-cell/brk-gestao/main/noticias.json';
    var local = boxes[0].getAttribute('data-local') || 'noticias.json';

    function esc(s) { var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
    function when(iso) {
        var d = new Date(iso), diff = (Date.now() - d) / 36e5;
        if (diff < 1) return 'agora há pouco';
        if (diff < 24) return 'há ' + Math.floor(diff) + ' h';
        if (diff < 48) return 'ontem';
        return d.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' });
    }
    function render(data) {
        boxes.forEach(function (box) {
            var n = +box.getAttribute('data-limit') || 12;
            var cat = box.getAttribute('data-filter') || '';
            var items = data.items.filter(function (it) { return !cat || it.category === cat; }).slice(0, n);
            box.innerHTML = items.map(function (it) {
                return '<a class="news-card" href="' + esc(it.link) + '" target="_blank" rel="noopener">' +
                    '<span class="src"><span>' + esc(it.category || it.source) + '</span><time datetime="' + esc(it.date) + '">' + when(it.date) + '</time></span>' +
                    '<h3>' + esc(it.title) + '</h3>' + (it.summary ? '<p>' + esc(it.summary) + '</p>' : '') +
                    '<span class="more">Ler no Sebrae ↗</span></a>';
            }).join('');
            var st = document.querySelector(box.getAttribute('data-status') || '#news-status');
            if (st) st.textContent = 'Fonte: Agência Sebrae de Notícias · atualizado ' + new Date(data.updated).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
        });
        var filters = document.querySelector('[data-news-filters]');
        if (filters && !filters.children.length) {
            var cats = [];
            data.items.forEach(function (it) { if (it.category && cats.indexOf(it.category) < 0) cats.push(it.category); });
            filters.innerHTML = '<button type="button" class="on" data-v="">Todas</button>' + cats.map(function (c) { return '<button type="button" data-v="' + esc(c) + '">' + esc(c) + '</button>'; }).join('');
            filters.addEventListener('click', function (e) {
                var b = e.target.closest('button'); if (!b) return;
                filters.querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b); });
                boxes.forEach(function (bx) { bx.setAttribute('data-filter', b.dataset.v); });
                render(data);
            });
        }
    }
    function fail() { boxes.forEach(function (b) { b.innerHTML = '<p class="news-status">Não foi possível carregar as notícias agora. <a href="https://agenciasebrae.com.br/" target="_blank" rel="noopener">Acesse a Agência Sebrae →</a></p>'; }); }
    function get(url) { return fetch(url, { cache: 'no-store' }).then(function (r) { if (!r.ok) throw 0; return r.json(); }); }
    get(LIVE).catch(function () { return get(local); }).then(function (d) { if (d && d.items && d.items.length) render(d); else fail(); }).catch(fail);
})();
