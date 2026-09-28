/* BRK Gestão Financeira — ferramentas interativas e gráficos */
(function () {
    'use strict';
    if (!window.Chart) return;

    // ---------- Tema dos gráficos ----------
    var GOLD = '#D4AF37', GOLD2 = '#F1D78A', BRONZE = '#9C7A2B', GRAY = '#6d6d6d', TEXT = '#bdbdbd', GRID = 'rgba(212,175,55,0.10)';
    var RED = '#e07a5f', GREEN = '#7fc8a9';
    var PALETTE = [GOLD, '#8a8a8a', GOLD2, BRONZE, '#4a4a4a', '#c9c9c9', '#5e4a17'];
    var small = window.matchMedia('(max-width: 860px)').matches;
    Chart.defaults.color = TEXT;
    Chart.defaults.font.family = "'Montserrat', system-ui, sans-serif";
    Chart.defaults.font.size = small ? 11 : 12;
    Chart.defaults.borderColor = GRID;
    Chart.defaults.plugins.legend.labels.boxWidth = 12;
    Chart.defaults.plugins.legend.labels.boxHeight = 12;
    Chart.defaults.plugins.tooltip.backgroundColor = '#141414';
    Chart.defaults.plugins.tooltip.borderColor = 'rgba(212,175,55,0.5)';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.titleColor = '#fff';
    Chart.defaults.plugins.tooltip.bodyColor = '#e6e6e6';
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.maintainAspectRatio = false;
    Chart.defaults.animation.duration = 450;

    // ---------- Utilidades ----------
    var brl = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });
    var brl2 = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', minimumFractionDigits: 2, maximumFractionDigits: 2 });
    var num1 = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 1 });
    function money(v) { return brl.format(Math.round(v || 0)); }
    function short(v) {
        var a = Math.abs(v);
        if (a >= 1e6) return 'R$ ' + num1.format(v / 1e6) + ' mi';
        if (a >= 1e3) return 'R$ ' + num1.format(v / 1e3) + ' mil';
        return brl.format(v);
    }
    function val(root, name) {
        var el = root.querySelector('[name="' + name + '"]');
        if (!el) return 0;
        var v = parseFloat(String(el.value).replace(',', '.'));
        return isFinite(v) ? v : 0;
    }
    function set(root, key, text, cls) {
        var el = root.querySelector('[data-out="' + key + '"]');
        if (!el) return;
        el.textContent = text;
        var box = el.closest('.result');
        if (box) { box.classList.remove('bad', 'good'); if (cls) box.classList.add(cls); }
    }
    function say(root, html) { var el = root.querySelector('[data-out="verdict"]'); if (el) el.innerHTML = html; }
    function months(n) {
        if (!isFinite(n)) return 'Nunca';
        if (n < 12) return n + (n === 1 ? ' mês' : ' meses');
        var y = Math.floor(n / 12), m = n % 12;
        return y + (y === 1 ? ' ano' : ' anos') + (m ? ' e ' + m + (m === 1 ? ' mês' : ' meses') : '');
    }
    function moneyAxis() { return { ticks: { callback: function (v) { return short(v); } }, grid: { color: GRID } }; }
    function tipMoney() { return { callbacks: { label: function (c) { return ' ' + c.dataset.label + ': ' + money(c.parsed.y !== undefined ? c.parsed.y : c.parsed); } } }; }
    function makeChart(root, cfg) {
        var cv = root.querySelector('canvas');
        if (!cv) return null;
        if (cv._chart) { cv._chart.destroy(); }
        cv._chart = new Chart(cv, cfg);
        return cv._chart;
    }
    function bind(root, fn) {
        var t;
        root.addEventListener('input', function () { clearTimeout(t); t = setTimeout(fn, 120); });
        root.querySelectorAll('.seg').forEach(function (seg) {
            seg.addEventListener('click', function (e) {
                var b = e.target.closest('button'); if (!b) return;
                seg.querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b); });
                seg.dataset.value = b.dataset.v; fn();
            });
        });
        fn();
    }
    function segVal(root, name, def) { var s = root.querySelector('.seg[data-name="' + name + '"]'); return s && s.dataset.value ? s.dataset.value : def; }

    var TOOLS = {};

    // 1. Ponto de equilíbrio
    TOOLS.pe = function (root) {
        bind(root, function () {
            var fat = val(root, 'fat'), cv = val(root, 'cv'), fixas = val(root, 'fixas'), dias = val(root, 'dias') || 26;
            var mc = 1 - cv / 100;
            if (mc <= 0) { say(root, 'Os custos variáveis não podem ser 100% ou mais do faturamento — nesse caso, cada venda dá prejuízo.'); return; }
            var pe = fixas / mc, lucro = fat * mc - fixas, seg = fat > 0 ? (fat - pe) / fat * 100 : 0;
            set(root, 'pe', money(pe));
            set(root, 'mc', num1.format(mc * 100) + '%');
            set(root, 'lucro', money(lucro), lucro >= 0 ? 'good' : 'bad');
            set(root, 'dia', money(pe / dias));
            say(root, fat >= pe
                ? 'Sua empresa está <b>' + num1.format(seg) + '% acima</b> do ponto de equilíbrio. Esse é o seu colchão: as vendas podem cair até esse percentual antes de dar prejuízo.'
                : 'Atenção: o faturamento atual está <b>' + money(pe - fat) + ' abaixo</b> do ponto de equilíbrio. Faltam cerca de ' + money((pe - fat) / dias) + ' por dia útil para empatar.');
            var max = Math.max(fat, pe) * 1.4 || 10000, pts = 12, r = [], c = [];
            for (var i = 0; i <= pts; i++) { var x = max * i / pts; r.push({ x: x, y: x }); c.push({ x: x, y: fixas + x * cv / 100 }); }
            makeChart(root, {
                type: 'line',
                data: { datasets: [
                    { label: 'Faturamento', data: r, borderColor: GOLD, backgroundColor: GOLD, pointRadius: 0, borderWidth: 2.5 },
                    { label: 'Custo total', data: c, borderColor: '#9a9a9a', backgroundColor: '#9a9a9a', pointRadius: 0, borderWidth: 2, borderDash: [6, 5] },
                    { label: 'Ponto de equilíbrio', data: [{ x: pe, y: pe }], type: 'scatter', pointRadius: 7, pointHoverRadius: 9, backgroundColor: '#fff', borderColor: GOLD, borderWidth: 3 },
                    { label: 'Você hoje', data: [{ x: fat, y: fat }], type: 'scatter', pointRadius: 6, backgroundColor: fat >= pe ? GREEN : RED, borderColor: '#000', borderWidth: 1 }
                ] },
                options: { parsing: false, scales: { x: { type: 'linear', title: { display: !small, text: 'Faturamento mensal' }, ticks: { callback: function (v) { return short(v); }, maxTicksLimit: small ? 4 : 7 }, grid: { color: GRID } }, y: moneyAxis() },
                    plugins: { legend: { position: 'bottom' }, tooltip: { callbacks: { label: function (ctx) { return ' ' + ctx.dataset.label + ': ' + money(ctx.parsed.y); } } } } }
            });
        });
    };

    // 2. Plano para quitar dívidas
    TOOLS.dividas = function (root) {
        var list = root.querySelector('[data-debts]');
        var tpl = function (d) {
            return '<div class="debt-row">' +
                '<div class="field"><label>Dívida</label><input type="text" data-k="nome" value="' + d.nome + '"></div>' +
                '<div class="field"><label>Saldo (R$)</label><input type="number" inputmode="decimal" min="0" data-k="saldo" value="' + d.saldo + '"></div>' +
                '<div class="field"><label>Juros % mês</label><input type="number" inputmode="decimal" min="0" step="0.1" data-k="juros" value="' + d.juros + '"></div>' +
                '<div class="field"><label>Parcela mín.</label><input type="number" inputmode="decimal" min="0" data-k="min" value="' + d.min + '"></div>' +
                '<button type="button" class="icon-btn" aria-label="Remover dívida" data-del>×</button></div>';
        };
        var start = [
            { nome: 'Cartão (rotativo)', saldo: 4000, juros: 12, min: 400 },
            { nome: 'Cheque especial', saldo: 1500, juros: 7.5, min: 150 },
            { nome: 'Empréstimo pessoal', saldo: 8000, juros: 3.5, min: 450 }
        ];
        list.innerHTML = start.map(tpl).join('');
        root.querySelector('[data-add]').addEventListener('click', function () {
            list.insertAdjacentHTML('beforeend', tpl({ nome: 'Nova dívida', saldo: 1000, juros: 3, min: 100 }));
            calc();
        });
        list.addEventListener('click', function (e) { if (e.target.closest('[data-del]')) { e.target.closest('.debt-row').remove(); calc(); } });

        function read() {
            return Array.prototype.map.call(list.querySelectorAll('.debt-row'), function (r) {
                var g = function (k) { var v = parseFloat(r.querySelector('[data-k="' + k + '"]').value); return isFinite(v) ? v : 0; };
                return { nome: r.querySelector('[data-k="nome"]').value || 'Dívida', saldo: g('saldo'), juros: g('juros') / 100, min: g('min') };
            }).filter(function (d) { return d.saldo > 0; });
        }
        function sim(debts, extra, method, redistribute) {
            var ds = debts.map(function (d) { return { nome: d.nome, saldo: d.saldo, juros: d.juros, min: d.min }; });
            var budget = ds.reduce(function (s, d) { return s + d.min; }, 0) + extra;
            var totalInt = 0, series = [ds.reduce(function (s, d) { return s + d.saldo; }, 0)], order = [];
            for (var m = 1; m <= 360; m++) {
                var live = ds.filter(function (d) { return d.saldo > 0.5; });
                if (!live.length) return { months: m - 1, interest: totalInt, series: series, order: order };
                live.forEach(function (d) { var i = d.saldo * d.juros; d.saldo += i; totalInt += i; });
                var avail = redistribute ? budget : budget;
                live.forEach(function (d) { var p = Math.min(d.min, d.saldo); d.saldo -= p; avail -= p; });
                if (!redistribute) avail = Math.min(avail, extra);
                live.sort(method === 'bola' ? function (a, b) { return a.saldo - b.saldo; } : function (a, b) { return b.juros - a.juros; });
                for (var k = 0; k < live.length && avail > 0.005; k++) { var p2 = Math.min(avail, live[k].saldo); live[k].saldo -= p2; avail -= p2; }
                live.forEach(function (d) { if (d.saldo <= 0.5 && order.indexOf(d.nome) < 0) order.push(d.nome); });
                var tot = ds.reduce(function (s, d) { return s + Math.max(d.saldo, 0); }, 0);
                series.push(tot);
                if (m > 24 && tot > series[0] * 1.5) return { months: Infinity, interest: totalInt, series: series, order: order };
            }
            return { months: Infinity, interest: totalInt, series: series, order: order };
        }
        function calc() {
            var debts = read(), extra = val(root, 'extra'), method = segVal(root, 'metodo', 'avalanche');
            if (!debts.length) { say(root, 'Adicione pelo menos uma dívida.'); return; }
            var plan = sim(debts, extra, method, true), base = sim(debts, 0, method, false);
            var total = debts.reduce(function (s, d) { return s + d.saldo; }, 0);
            set(root, 'total', money(total));
            set(root, 'prazo', months(plan.months), isFinite(plan.months) ? 'good' : 'bad');
            set(root, 'juros', money(plan.interest));
            set(root, 'economia', isFinite(base.months) ? money(Math.max(base.interest - plan.interest, 0)) : 'O mínimo não quita', isFinite(base.months) ? 'good' : 'bad');
            if (!isFinite(plan.months)) say(root, 'Com esses valores, <b>a dívida não para de crescer</b>: os juros do mês são maiores que o que você consegue pagar. É hora de renegociar ou trocar a dívida cara por uma mais barata.');
            else say(root, 'Ordem de quitação: <b>' + plan.order.join(' → ') + '</b>. ' + (isFinite(base.months) ? 'Pagando só o mínimo, levaria ' + months(base.months) + '.' : 'Pagando só o mínimo, <b>você nunca sairia da dívida</b>.'));
            var n = Math.min(Math.max(plan.series.length, isFinite(base.months) ? base.series.length : 60), 120);
            var labels = []; for (var i = 0; i < n; i++) labels.push(i);
            makeChart(root, {
                type: 'line',
                data: { labels: labels, datasets: [
                    { label: 'Com o plano', data: plan.series.slice(0, n), borderColor: GOLD, backgroundColor: 'rgba(212,175,55,0.15)', fill: true, pointRadius: 0, borderWidth: 2.5, tension: 0.2 },
                    { label: 'Só o mínimo', data: base.series.slice(0, n), borderColor: '#8a8a8a', borderDash: [6, 5], pointRadius: 0, borderWidth: 2, tension: 0.2 }
                ] },
                options: { scales: { x: { title: { display: true, text: 'Meses' }, ticks: { maxTicksLimit: small ? 6 : 12 }, grid: { color: GRID } }, y: moneyAxis() },
                    plugins: { legend: { position: 'bottom' }, tooltip: { callbacks: { title: function (c) { return 'Mês ' + c[0].label; }, label: function (c) { return ' ' + c.dataset.label + ': ' + money(c.parsed.y); } } } } }
            });
        }
        bind(root, calc);
    };

    // 3. Reserva de emergência
    TOOLS.reserva = function (root) {
        bind(root, function () {
            var gastos = val(root, 'gastos'), mult = parseFloat(segVal(root, 'meses', '6')), tem = val(root, 'tem'), aporte = val(root, 'aporte'), taxa = val(root, 'taxa') / 100;
            var meta = gastos * mult, saldo = tem, serie = [tem], n = 0;
            while (saldo < meta && n < 600) { saldo = saldo * (1 + taxa) + aporte; serie.push(saldo); n++; }
            var ok = saldo >= meta;
            set(root, 'meta', money(meta));
            set(root, 'falta', money(Math.max(meta - tem, 0)));
            set(root, 'prazo', ok ? months(n) : 'Aumente o aporte', ok ? 'good' : 'bad');
            set(root, 'pct', num1.format(meta > 0 ? Math.min(tem / meta * 100, 100) : 0) + '%');
            var d = new Date(); d.setMonth(d.getMonth() + n);
            say(root, tem >= meta ? 'Parabéns: sua reserva já está completa. Mantenha-a em um lugar seguro e com resgate rápido.' :
                ok ? 'Guardando ' + money(aporte) + ' por mês, você completa a reserva em <b>' + d.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' }) + '</b>. Primeiro degrau (1 mês de gastos): ' + money(gastos) + '.' :
                'Com aporte zero a reserva não cresce. Comece com qualquer valor — até R$ 50 por mês fazem diferença.');
            var labels = serie.map(function (_, i) { return i; }).slice(0, 121);
            makeChart(root, {
                type: 'line',
                data: { labels: labels, datasets: [
                    { label: 'Sua reserva', data: serie.slice(0, 121), borderColor: GOLD, backgroundColor: 'rgba(212,175,55,0.18)', fill: true, pointRadius: 0, borderWidth: 2.5 },
                    { label: 'Meta', data: labels.map(function () { return meta; }), borderColor: '#9a9a9a', borderDash: [6, 5], pointRadius: 0, borderWidth: 1.5 }
                ] },
                options: { scales: { x: { title: { display: true, text: 'Meses' }, ticks: { maxTicksLimit: small ? 6 : 12 }, grid: { color: GRID } }, y: moneyAxis() },
                    plugins: { legend: { position: 'bottom' }, tooltip: { callbacks: { title: function (c) { return 'Mês ' + c[0].label; }, label: function (c) { return ' ' + c.dataset.label + ': ' + money(c.parsed.y); } } } } }
            });
        });
    };

    // 4. Custo do rotativo do cartão (com teto de juros de 100% do valor original)
    TOOLS.cartao = function (root) {
        function run(saldo0, taxa, pag) {
            var saldo = saldo0, juros = 0, pago = 0, serie = [saldo0], m = 0;
            while (saldo > 0.5 && m < 240) {
                var j = saldo * taxa;
                if (juros + j > saldo0) j = Math.max(saldo0 - juros, 0); // teto: juros e encargos até 100% da dívida original
                juros += j; saldo += j;
                var p = Math.min(pag, saldo); saldo -= p; pago += p; m++; serie.push(saldo);
            }
            return { m: saldo <= 0.5 ? m : Infinity, juros: juros, pago: pago, serie: serie };
        }
        bind(root, function () {
            var s = val(root, 'saldo'), t = val(root, 'taxa') / 100, p = val(root, 'pag');
            var a = run(s, t, p), b = run(s, t, p * 2);
            set(root, 'prazo', months(a.m), isFinite(a.m) ? '' : 'bad');
            set(root, 'juros', money(a.juros), 'bad');
            set(root, 'total', money(a.pago));
            set(root, 'dobro', isFinite(b.m) ? months(b.m) : '—', 'good');
            say(root, 'Pagando ' + money(p) + ' por mês, você paga <b>' + money(a.juros) + ' só de juros</b>. Dobrando o pagamento, quita em ' + months(b.m) + ' e economiza ' + money(Math.max(a.juros - b.juros, 0)) + '. Pela lei, desde 2024 os juros e encargos do rotativo e do parcelamento da fatura não podem passar de 100% do valor original da dívida — por isso a simulação para de somar juros nesse limite.');
            var n = Math.max(a.serie.length, b.serie.length), labels = []; for (var i = 0; i < n; i++) labels.push(i);
            makeChart(root, {
                type: 'line',
                data: { labels: labels, datasets: [
                    { label: 'Pagando ' + money(p), data: a.serie, borderColor: RED, pointRadius: 0, borderWidth: 2.5, tension: 0.2 },
                    { label: 'Pagando ' + money(p * 2), data: b.serie, borderColor: GOLD, backgroundColor: 'rgba(212,175,55,0.15)', fill: true, pointRadius: 0, borderWidth: 2.5, tension: 0.2 }
                ] },
                options: { scales: { x: { title: { display: true, text: 'Meses' }, ticks: { maxTicksLimit: small ? 6 : 12 }, grid: { color: GRID } }, y: moneyAxis() },
                    plugins: { legend: { position: 'bottom' }, tooltip: { callbacks: { title: function (c) { return 'Mês ' + c[0].label; }, label: function (c) { return ' Saldo: ' + money(c.parsed.y); } } } } }
            });
        });
    };

    // 5. Orçamento 50-30-20
    TOOLS.orcamento = function (root) {
        bind(root, function () {
            var r = val(root, 'renda'), n = val(root, 'nec'), d = val(root, 'des'), f = val(root, 'fut');
            set(root, 'nec', money(r * 0.5)); set(root, 'des', money(r * 0.3)); set(root, 'fut', money(r * 0.2));
            var real = n + d + f, sobra = r - real;
            set(root, 'sobra', money(sobra), sobra >= 0 ? 'good' : 'bad');
            var msg = [];
            if (real > 0) {
                if (n > r * 0.5) msg.push('Seus gastos essenciais estão em <b>' + num1.format(n / r * 100) + '%</b> da renda (o ideal é até 50%). Revise moradia, transporte e contas fixas.');
                if (d > r * 0.3) msg.push('Os gastos com desejos passam de 30%: há espaço para cortar sem afetar o essencial.');
                if (f < r * 0.2) msg.push('Você está guardando ' + num1.format(f / r * 100) + '% da renda. Tente chegar a 20%, mesmo que aos poucos.');
                if (!msg.length) msg.push('Seu orçamento está dentro da regra 50-30-20. Excelente!');
            } else msg.push('Preencha seus gastos reais para comparar com o ideal.');
            say(root, msg.join(' '));
            makeChart(root, {
                type: 'bar',
                data: { labels: ['Necessidades', 'Desejos', 'Futuro / dívidas'], datasets: [
                    { label: 'Ideal (50-30-20)', data: [r * 0.5, r * 0.3, r * 0.2], backgroundColor: 'rgba(212,175,55,0.35)', borderColor: GOLD, borderWidth: 1 },
                    { label: 'Seu orçamento', data: [n, d, f], backgroundColor: [n > r * 0.5 ? RED : GOLD, d > r * 0.3 ? RED : GOLD, f < r * 0.2 ? '#8a8a8a' : GREEN] }
                ] },
                options: { scales: { y: moneyAxis(), x: { grid: { display: false } } }, plugins: { legend: { position: 'bottom' }, tooltip: tipMoney() } }
            });
        });
    };

    // 6. DRE simplificada + pró-labore
    TOOLS.dre = function (root) {
        bind(root, function () {
            var fat = val(root, 'fat'), cmv = fat * val(root, 'cmv') / 100, imp = fat * val(root, 'imp') / 100, tax = fat * val(root, 'tax') / 100, fixas = val(root, 'fixas'), pl = val(root, 'pl');
            var mc = fat - cmv - imp - tax, lucro = mc - fixas, caixa = lucro - pl;
            set(root, 'mc', money(mc) + ' (' + num1.format(fat ? mc / fat * 100 : 0) + '%)');
            set(root, 'lucro', money(lucro), lucro >= 0 ? 'good' : 'bad');
            set(root, 'caixa', money(caixa), caixa >= 0 ? 'good' : 'bad');
            set(root, 'plmax', money(Math.max(lucro * 0.8, 0)));
            say(root, caixa < 0
                ? 'As retiradas estão <b>' + money(-caixa) + ' acima</b> do que a empresa gera por mês. Isso consome o caixa e, cedo ou tarde, vira empréstimo.'
                : 'Depois das retiradas, sobram <b>' + money(caixa) + '</b> por mês para reserva, investimentos e imprevistos.');
            var steps = [['Faturamento', fat], ['Mercadoria/insumos', -cmv], ['Impostos', -imp], ['Taxas', -tax], ['Despesas fixas', -fixas], ['Pró-labore', -pl]];
            var acc = 0, bars = [], colors = [], labels = [];
            steps.forEach(function (s, i) {
                var a = acc, b = i === 0 ? s[1] : acc + s[1];
                bars.push([Math.min(a, b), Math.max(a, b)]); colors.push(i === 0 ? GOLD : 'rgba(224,122,95,0.75)'); labels.push(s[0]); acc = b;
            });
            labels.push('Sobra de caixa'); bars.push([Math.min(0, acc), Math.max(0, acc)]); colors.push(acc >= 0 ? GREEN : RED);
            makeChart(root, {
                type: 'bar',
                data: { labels: labels, datasets: [{ label: 'Valor', data: bars, backgroundColor: colors, borderSkipped: false }] },
                options: { indexAxis: small ? 'y' : 'x', scales: small ? { x: moneyAxis(), y: { grid: { display: false } } } : { y: moneyAxis(), x: { grid: { display: false }, ticks: { maxRotation: 0, autoSkip: false, font: { size: 11 } } } },
                    plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { var r = c.raw; return ' ' + money(r[1] - r[0]); } } } } }
            });
        });
    };

    // 7. Limite do MEI
    TOOLS.mei = function (root) {
        var LIM = 81000, TOL = 97200;
        bind(root, function () {
            var feito = val(root, 'feito'), mes = Math.min(Math.max(Math.round(val(root, 'mes')) || 1, 1), 12), media = val(root, 'media');
            var rest = 12 - mes, proj = feito + media * rest, maxMedia = rest > 0 ? (LIM - feito) / rest : 0;
            set(root, 'proj', money(proj), proj > LIM ? 'bad' : 'good');
            set(root, 'pct', num1.format(proj / LIM * 100) + '%', proj > LIM ? 'bad' : '');
            set(root, 'resta', money(Math.max(LIM - feito, 0)));
            set(root, 'max', rest > 0 ? money(Math.max(maxMedia, 0)) : '—');
            say(root, proj <= LIM ? 'Mantendo essa média, você fecha o ano <b>dentro do limite</b> do MEI, com folga de ' + money(LIM - proj) + '.'
                : proj <= TOL ? 'Projeção <b>acima de R$ 81 mil, mas dentro da tolerância de 20%</b>. Você seria desenquadrado a partir de janeiro do ano seguinte e pagaria um DAS complementar sobre o excesso. Planeje a transição com seu contador.'
                : 'Projeção <b>acima de R$ 97,2 mil</b>: o desenquadramento seria retroativo a janeiro, com impostos de microempresa sobre o ano todo. Converse com um contador o quanto antes.');
            var labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'], real = [], prj = [];
            for (var i = 1; i <= 12; i++) {
                real.push(i <= mes ? feito * i / mes : null);
                prj.push(i < mes ? null : feito + media * (i - mes));
            }
            makeChart(root, {
                type: 'line',
                data: { labels: labels, datasets: [
                    { label: 'Faturado (acumulado)', data: real, borderColor: GOLD, backgroundColor: 'rgba(212,175,55,0.18)', fill: true, pointRadius: small ? 2 : 3, borderWidth: 2.5 },
                    { label: 'Projeção', data: prj, borderColor: GOLD2, borderDash: [6, 5], pointRadius: 0, borderWidth: 2 },
                    { label: 'Limite R$ 81 mil', data: labels.map(function () { return LIM; }), borderColor: RED, pointRadius: 0, borderWidth: 1.5 },
                    { label: 'Tolerância R$ 97,2 mil', data: labels.map(function () { return TOL; }), borderColor: '#8a8a8a', borderDash: [3, 4], pointRadius: 0, borderWidth: 1.5 }
                ] },
                options: { scales: { y: moneyAxis(), x: { grid: { display: false } } }, plugins: { legend: { position: 'bottom' }, tooltip: tipMoney() } }
            });
        });
    };

    // 8. Simulador de liberdade financeira (juros compostos)
    TOOLS.liberdade = function (root) {
        bind(root, function () {
            var ini = val(root, 'ini'), ap = val(root, 'aporte'), taxa = val(root, 'taxa') / 100, anos = Math.min(Math.max(Math.round(val(root, 'anos')) || 1, 1), 50);
            var im = Math.pow(1 + taxa, 1 / 12) - 1, saldo = ini, apt = ini, labels = [], s1 = [], s2 = [];
            for (var y = 1; y <= anos; y++) {
                for (var m = 0; m < 12; m++) { saldo = saldo * (1 + im) + ap; apt += ap; }
                labels.push(y + (small ? '' : 'º ano')); s1.push(apt); s2.push(saldo - apt);
            }
            var renda = saldo * im;
            set(root, 'total', short(saldo));
            set(root, 'aportado', short(apt));
            set(root, 'juros', short(saldo - apt), 'good');
            set(root, 'renda', money(renda) + '/mês');
            say(root, 'Em ' + anos + ' anos, os rendimentos representariam <b>' + num1.format(saldo > 0 ? (saldo - apt) / saldo * 100 : 0) + '%</b> do patrimônio. Com ' + short(saldo) + ', esse dinheiro poderia gerar cerca de <b>' + money(renda) + ' por mês</b> sem reduzir o valor real — considerando a taxa real informada (já descontada a inflação).');
            makeChart(root, {
                type: 'bar',
                data: { labels: labels, datasets: [
                    { label: 'Quanto você guardou', data: s1, backgroundColor: 'rgba(212,175,55,0.45)', stack: 's' },
                    { label: 'Rendimentos', data: s2, backgroundColor: GOLD, stack: 's' }
                ] },
                options: { scales: { x: { stacked: true, grid: { display: false }, ticks: { maxTicksLimit: small ? 6 : 15 } }, y: Object.assign(moneyAxis(), { stacked: true }) }, plugins: { legend: { position: 'bottom' }, tooltip: tipMoney() } }
            });
        });
    };

    // ---------- Gráficos do Panorama ----------
    var PANORAMA = {
        selic: function (cv) {
            new Chart(cv, { type: 'bar', data: { labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', 'set/26'], datasets: [{ label: 'Selic (% ao ano)', data: [13.75, 7, 6.5, 4.5, 2, 9.25, 13.75, 11.75, 12.25, 15, 13.75], backgroundColor: function (c) { return c.dataIndex >= 9 ? GOLD : 'rgba(212,175,55,0.45)'; } }] },
                options: { scales: { y: { ticks: { callback: function (v) { return v + '%'; } } }, x: { grid: { display: false } } }, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return ' Selic: ' + String(c.parsed.y).replace('.', ',') + '% a.a.'; } } } } } });
        },
        familias: function (cv) {
            new Chart(cv, { type: 'line', data: { labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026*'], datasets: [
                { label: 'Famílias endividadas', data: [59.0, 62.2, 59.8, 65.6, 66.3, 76.3, 78.0, 77.6, 76.7, 78.9, 80.4], borderColor: GOLD, backgroundColor: 'rgba(212,175,55,0.15)', fill: true, borderWidth: 2.5, pointRadius: small ? 2 : 3, tension: 0.25 },
                { label: 'Com contas em atraso', data: [24.0, 25.7, 22.8, 24.5, 25.2, 26.2, 30.0, 28.8, 29.3, 29.4, 29.6], borderColor: '#9a9a9a', borderWidth: 2, pointRadius: small ? 2 : 3, tension: 0.25 }
            ] }, options: { scales: { y: { min: 0, max: 100, ticks: { callback: function (v) { return v + '%'; } } }, x: { grid: { display: false } } }, plugins: { legend: { position: 'bottom' }, tooltip: { callbacks: { label: function (c) { return ' ' + c.dataset.label + ': ' + String(c.parsed.y).replace('.', ',') + '%'; } } } } } });
        },
        negativados: function (cv) {
            new Chart(cv, { type: 'bar', data: { labels: ['2016', 'Início 2020', 'Fev/2026', 'Ago/2026'], datasets: [{ label: 'Milhões de pessoas', data: [59.2, 63.8, 81.7, 84.0], backgroundColor: ['rgba(212,175,55,0.35)', 'rgba(212,175,55,0.5)', 'rgba(212,175,55,0.75)', GOLD] }] },
                options: { scales: { y: { beginAtZero: true, ticks: { callback: function (v) { return v + ' mi'; } } }, x: { grid: { display: false } } }, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return ' ' + String(c.parsed.y).replace('.', ',') + ' milhões'; } } } } } });
        },
        empresas: function (cv) {
            new Chart(cv, { type: 'bar', data: { labels: ['Dez/2023', 'Dez/2024', 'Dez/2025', 'Jul/2026'], datasets: [{ label: 'Milhões de empresas', data: [6.6, 6.9, 8.9, 9.2], backgroundColor: ['rgba(212,175,55,0.35)', 'rgba(212,175,55,0.5)', 'rgba(212,175,55,0.75)', GOLD] }] },
                options: { scales: { y: { beginAtZero: true, ticks: { callback: function (v) { return v + ' mi'; } } }, x: { grid: { display: false } } }, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return ' ' + String(c.parsed.y).replace('.', ',') + ' milhões de CNPJs'; } } } } } });
        },
        setores: function (cv) {
            new Chart(cv, { type: 'doughnut', data: { labels: ['Serviços', 'Comércio', 'Indústria', 'Outros'], datasets: [{ data: [55.2, 32.7, 8.1, 4.0], backgroundColor: [GOLD, '#8a8a8a', GOLD2, '#3d3d3d'], borderColor: '#050505', borderWidth: 3 }] },
                options: { cutout: '62%', plugins: { legend: { position: 'bottom' }, tooltip: { callbacks: { label: function (c) { return ' ' + c.label + ': ' + String(c.parsed).replace('.', ',') + '%'; } } } } } });
        },
        credores: function (cv) {
            new Chart(cv, { type: 'bar', data: { labels: ['Serviços', 'Bancos e cartões', 'Cooperativas', 'Água, luz e gás', 'Telefonia', 'Outros'], datasets: [{ data: [31.7, 19.7, 8.5, 6.9, 6.2, 27.0], backgroundColor: [GOLD, '#8a8a8a', GOLD2, BRONZE, '#5a5a5a', '#3d3d3d'] }] },
                options: { indexAxis: 'y', scales: { x: { ticks: { callback: function (v) { return v + '%'; } } }, y: { grid: { display: false } } }, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return ' ' + String(c.parsed.x).replace('.', ',') + '% das dívidas'; } } } } } });
        },
        sobrevivencia: function (cv) {
            new Chart(cv, { type: 'doughnut', data: { labels: ['Ainda ativas após 5 anos', 'Fecharam em até 5 anos'], datasets: [{ data: [37.6, 62.4], backgroundColor: [GOLD, '#3d3d3d'], borderColor: '#050505', borderWidth: 3 }] },
                options: { cutout: '62%', plugins: { legend: { position: 'bottom' }, tooltip: { callbacks: { label: function (c) { return ' ' + c.label + ': ' + String(c.parsed).replace('.', ',') + '%'; } } } } } });
        }
    };

    function init() {
        document.querySelectorAll('[data-tool]').forEach(function (el) { var f = TOOLS[el.dataset.tool]; if (f) f(el); });
        var charts = document.querySelectorAll('canvas[data-chart]');
        if (!charts.length) return;
        var draw = function (cv) { if (cv._done) return; cv._done = true; var f = PANORAMA[cv.dataset.chart]; if (f) f(cv); };
        if ('IntersectionObserver' in window) {
            var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { draw(e.target); io.unobserve(e.target); } }); }, { rootMargin: '120px' });
            charts.forEach(function (c) { io.observe(c); });
        } else charts.forEach(draw);
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
