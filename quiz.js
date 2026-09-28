/* BRK Gestão Financeira — motor de quizzes */
(function () {
    'use strict';
    var host = document.getElementById('quiz');
    var dataEl = document.getElementById('quiz-data');
    if (!host || !dataEl) return;
    var Q = JSON.parse(dataEl.textContent);
    var i = 0, answers = [], score = 0;
    var KEYS = 'ABCDE';

    function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
    function top() {
        return '<div class="quiz-top"><span>Pergunta ' + (i + 1) + ' de ' + Q.questions.length + '</span><span>' + esc(Q.label || '') + '</span></div>' +
            '<div class="quiz-bar"><span style="width:' + (i / Q.questions.length * 100) + '%"></span></div>';
    }
    function render() {
        var q = Q.questions[i];
        var opts = q.options.map(function (o, k) {
            return '<button type="button" class="quiz-opt" data-k="' + k + '"><span class="k">' + KEYS[k] + '</span><span>' + esc(o.t) + '</span></button>';
        }).join('');
        host.innerHTML = top() + '<h2 class="quiz-q">' + esc(q.q) + '</h2><div class="quiz-opts">' + opts + '</div><div data-after></div>';
        host.querySelectorAll('.quiz-opt').forEach(function (b) { b.addEventListener('click', function () { choose(+b.dataset.k); }); });
        var h = host.querySelector('.quiz-q'); if (i > 0 && h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
        if (i > 0) host.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    function choose(k) {
        var q = Q.questions[i], btns = host.querySelectorAll('.quiz-opt');
        answers.push(k);
        if (Q.mode === 'knowledge') {
            btns.forEach(function (b, n) { b.disabled = true; if (n === q.correct) b.classList.add('right'); else if (n === k) b.classList.add('wrong'); });
            if (k === q.correct) score++;
            host.querySelector('[data-after]').innerHTML = '<div class="quiz-explain"><b>' + (k === q.correct ? 'Correto! ' : 'Não foi dessa vez. ') + '</b>' + esc(q.explain) + '</div>' +
                '<div class="quiz-nav"><button type="button" class="btn btn-solid" data-next>' + (i + 1 < Q.questions.length ? 'Próxima pergunta' : 'Ver resultado') + '</button></div>';
            host.querySelector('[data-next]').addEventListener('click', next);
        } else {
            btns.forEach(function (b, n) { if (n === k) b.classList.add('right'); b.disabled = true; });
            setTimeout(next, 260);
        }
    }
    function next() { i++; if (i < Q.questions.length) render(); else result(); }

    function ring(pct) {
        var r = 70, c = 2 * Math.PI * r;
        return '<div class="score-ring"><svg viewBox="0 0 170 170" aria-hidden="true"><circle cx="85" cy="85" r="' + r + '" fill="none" stroke="rgba(212,175,55,0.15)" stroke-width="12"/>' +
            '<circle cx="85" cy="85" r="' + r + '" fill="none" stroke="#D4AF37" stroke-width="12" stroke-linecap="butt" stroke-dasharray="' + c + '" stroke-dashoffset="' + c + '" data-arc/></svg>' +
            '<div class="n"><span data-num>0</span><small>' + (Q.mode === 'knowledge' ? 'ACERTOS' : 'DE 100') + '</small></div></div>';
    }
    function animate(pct, shown) {
        var arc = host.querySelector('[data-arc]'), num = host.querySelector('[data-num]'), c = 2 * Math.PI * 70, t0 = null;
        function step(t) {
            if (!t0) t0 = t; var p = Math.min((t - t0) / 900, 1), e = 1 - Math.pow(1 - p, 3);
            arc.setAttribute('stroke-dashoffset', c * (1 - pct / 100 * e));
            num.textContent = Math.round(shown * e);
            if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }
    function result() {
        var pct, shown, band, tips = [];
        if (Q.mode === 'knowledge') {
            pct = score / Q.questions.length * 100; shown = score;
        } else {
            var tot = 0, max = 0, areas = {};
            Q.questions.forEach(function (q, n) {
                var pts = q.options[answers[n]].p, mx = Math.max.apply(null, q.options.map(function (o) { return o.p; }));
                tot += pts; max += mx;
                if (q.area) { areas[q.area] = areas[q.area] || [0, 0]; areas[q.area][0] += pts; areas[q.area][1] += mx; }
                if (pts <= 1 && q.tip) tips.push(q.tip);
            });
            pct = max ? tot / max * 100 : 0; shown = Math.round(pct);
        }
        band = Q.bands.filter(function (b) { return pct >= b.min; })[0] || Q.bands[Q.bands.length - 1];
        var tipsHtml = tips.length ? '<p class="eyebrow" style="margin:26px 0 4px">Pontos de risco encontrados</p><ul class="risk-list">' + tips.slice(0, 5).map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('') + '</ul>' : '';
        var pitch = Q.pitch ? '<div class="tool-cta" style="text-align:left;max-width:620px;margin:26px auto 0"><b>' + esc(Q.pitch.title) + '</b><p>' + esc(Q.pitch.text) + '</p><div class="btn-row">' +
            (Q.wa ? '<a class="btn btn-solid" href="' + Q.wa + '" target="_blank" rel="noopener">Falar com um consultor</a>' : '') +
            (Q.cta ? '<a class="btn" href="' + Q.cta.href + '">' + esc(Q.cta.label) + '</a>' : '') + '</div></div>' : '';
        var radar = (Q.mode !== 'knowledge' && Q.radar && window.Chart) ? '<div class="chart-box sq" style="max-width:520px;margin:10px auto 0"><canvas aria-label="Gráfico radar com a nota de cada área"></canvas></div>' : '';
        host.innerHTML = '<div class="quiz-bar"><span style="width:100%"></span></div><div class="quiz-result">' + ring(pct) +
            '<h2>' + esc(band.title) + '</h2><p>' + esc(band.text) + '</p>' + radar + tipsHtml + pitch +
            '<div class="btn-row">' + (!Q.pitch && Q.cta ? '<a class="btn btn-solid" href="' + Q.cta.href + '">' + esc(Q.cta.label) + '</a>' : '') +
            '<button type="button" class="btn" data-again>Refazer o teste</button></div>' +
            '<p style="margin-top:22px;font-size:0.84rem"><a href="#" data-share>Compartilhar este teste</a></p></div>';
        animate(pct, shown);
        host.querySelector('[data-again]').addEventListener('click', function () { i = 0; answers = []; score = 0; render(); });
        host.querySelector('[data-share]').addEventListener('click', function (e) {
            e.preventDefault();
            var data = { title: document.title, text: Q.share || 'Faça este teste:', url: location.href.split('#')[0] };
            if (navigator.share) navigator.share(data).catch(function () {});
            else if (navigator.clipboard) navigator.clipboard.writeText(data.url).then(function () { e.target.textContent = 'Link copiado!'; });
        });
        if (radar) {
            var labels = Object.keys(areas), vals = labels.map(function (a) { return Math.round(areas[a][0] / areas[a][1] * 100); });
            Chart.defaults.color = '#bdbdbd'; Chart.defaults.font.family = "'Montserrat', sans-serif";
            new Chart(host.querySelector('canvas'), {
                type: 'radar',
                data: { labels: labels, datasets: [{ label: 'Sua empresa', data: vals, borderColor: '#D4AF37', backgroundColor: 'rgba(212,175,55,0.22)', pointBackgroundColor: '#D4AF37', borderWidth: 2 }] },
                options: { maintainAspectRatio: false, scales: { r: { min: 0, max: 100, ticks: { display: false, stepSize: 25 }, grid: { color: 'rgba(212,175,55,0.15)' }, angleLines: { color: 'rgba(212,175,55,0.15)' }, pointLabels: { color: '#e6e6e6', font: { size: 12, weight: '600' } } } },
                    plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return ' ' + c.parsed.r + '/100'; } } } } }
            });
        }
        host.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    host.querySelector('[data-start]') ? host.querySelector('[data-start]').addEventListener('click', render) : render();
})();
