/* BRK Gestão Financeira — jogo "Sobreviva ao Mês" */
(function () {
    'use strict';
    var host = document.getElementById('game');
    if (!host) return;
    var brl = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });
    function m(v) { return brl.format(Math.round(v)); }
    function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

    // Cada escolha altera: saldo (conta), divida (cartão/empréstimo), reserva e paz (tranquilidade, 0 a 100)
    var EVENTS = [
        { when: 'Semana 1 · Segunda-feira', title: 'Promoção relâmpago', text: 'Aquele tênis que você queria está por R$ 450 — "só hoje", em até 10x no cartão.', choices: [
            { t: 'Compro parcelado em 10x', fx: { divida: 450, paz: 5 }, lesson: 'Parcela pequena engana: somadas, as compras parceladas comprometem os próximos meses antes de o salário cair.' },
            { t: 'Coloco na lista e espero 48 horas', fx: { paz: 2 }, lesson: 'A regra das 48 horas corta boa parte das compras por impulso. Se ainda fizer sentido depois, compre com planejamento.' },
            { t: 'Compro à vista, com o saldo', fx: { saldo: -450, paz: 5 }, lesson: 'Comprar à vista evita juros, mas o dinheiro sai do mês. Tinha espaço no orçamento para isso?' }] },
        { when: 'Semana 1 · Sábado', title: 'Mercado do mês', text: 'Hora de abastecer a despensa. Você vai com lista ou sem lista?', choices: [
            { t: 'Faço lista e comparo preços', fx: { saldo: -700, paz: 3 }, lesson: 'Lista de compras e comparação de preços reduzem o gasto de mercado sem reduzir a qualidade.' },
            { t: 'Vou sem lista e pego o que der vontade', fx: { saldo: -950 }, lesson: 'Sem lista, o carrinho enche de itens que não estavam nos planos. A diferença, aqui, foi de R$ 250.' }] },
        { when: 'Semana 2 · Quarta-feira', title: 'Imprevisto', text: 'O pneu furou e não tem conserto. O novo custa R$ 280.', choices: [
            { t: 'Uso a reserva de emergência', fx: { reserva: -280, paz: 5 }, lesson: 'É para isso que a reserva existe: o imprevisto virou um susto, não uma dívida. Depois, é só recompor.' },
            { t: 'Passo no cartão e pago depois', fx: { divida: 280, paz: -3 }, lesson: 'Sem reserva, o imprevisto vira dívida — e, se a fatura não for paga inteira, entra no rotativo.' },
            { t: 'Pago com o saldo da conta', fx: { saldo: -280 }, lesson: 'Resolveu, mas apertou o resto do mês. Por isso a reserva é separada do dinheiro do dia a dia.' }] },
        { when: 'Semana 2 · Sexta-feira', title: 'Convite da turma', text: 'Os amigos marcaram um churrasco. A sua parte fica em R$ 120.', choices: [
            { t: 'Vou e divido a conta', fx: { saldo: -120, paz: 10 }, lesson: 'Lazer faz parte do orçamento! O problema não é gastar com o que importa — é gastar sem planejar.' },
            { t: 'Sugiro fazer em casa, cada um leva algo', fx: { saldo: -40, paz: 8 }, lesson: 'Dá para manter a vida social gastando menos. Boa alternativa.' },
            { t: 'Não vou para economizar', fx: { paz: -10 }, lesson: 'Cortar todo o lazer costuma dar errado a médio prazo. Um orçamento sustentável tem espaço para o que você gosta.' }] },
        { when: 'Semana 3 · Segunda-feira', title: 'Empréstimo pré-aprovado', text: 'O app do banco oferece R$ 3.000 "na hora", para pagar em 12x de R$ 325.', choices: [
            { t: 'Pego para ter uma folga', fx: { saldo: 3000, divida: 3900, paz: 4 }, lesson: 'A folga é ilusória: você recebe R$ 3.000 e deve R$ 3.900. Empréstimo sem objetivo claro vira dívida cara.' },
            { t: 'Recuso — não preciso', fx: { paz: 3 }, lesson: 'Crédito fácil não é renda. Só faz sentido para trocar uma dívida mais cara ou para algo planejado.' }] },
        { when: 'Semana 3 · Quinta-feira', title: 'Cansaço depois do trabalho', text: 'A semana está puxada. Delivery todos os dias?', choices: [
            { t: 'Peço delivery a semana toda', fx: { saldo: -250, paz: 4 }, lesson: 'Delivery frequente é um dos maiores "vazamentos" do orçamento: parece pouco por dia e pesa no mês.' },
            { t: 'Cozinho no domingo e congelo marmitas', fx: { saldo: -60, paz: 2 }, lesson: 'Um pouco de planejamento economizou quase R$ 200 nesta semana.' }] },
        { when: 'Semana 4 · Terça-feira', title: 'As assinaturas', text: 'Você percebe que paga 4 streamings e 2 apps: R$ 140 por mês. Usa mesmo todos?', choices: [
            { t: 'Mantenho todas', fx: { saldo: -140 }, lesson: 'Assinaturas esquecidas são dinheiro que sai todo mês sem você perceber.' },
            { t: 'Cancelo as que não uso', fx: { saldo: -60, paz: 2 }, lesson: 'Revisar assinaturas a cada três meses é um hábito simples que libera dinheiro todo mês.' }] },
        { when: 'Semana 4 · Dia 30', title: 'Fim do mês', text: 'O mês acabou. O que você faz com o que sobrou na conta?', final: true, choices: [
            { t: 'Pago toda a fatura do cartão e guardo o resto', fx: { pagaDivida: true, guardaResto: 1 }, lesson: 'Excelente: pagar a fatura inteira evita o rotativo, e o que sobra reforça a reserva.' },
            { t: 'Guardo metade na reserva', fx: { guardaResto: 0.5 }, lesson: 'Guardar é ótimo — mas, se havia fatura em aberto, pagar a dívida cara vem antes.' },
            { t: 'Comemoro com um jantar de R$ 200', fx: { saldo: -200, paz: 6 }, lesson: 'Comemorar é bom, mas sem um plano o mês seguinte começa do mesmo jeito.' }] }
    ];

    var S;
    function reset() { S = { saldo: 2000, divida: 0, reserva: 300, paz: 60, i: 0, log: [] }; }
    function hud() {
        return '<div class="hud">' +
            '<div><small>Saldo</small><b class="' + (S.saldo < 0 ? 'neg' : '') + '">' + m(S.saldo) + '</b></div>' +
            '<div><small>Dívidas</small><b class="' + (S.divida > 0 ? 'neg' : '') + '">' + m(S.divida) + '</b></div>' +
            '<div><small>Reserva</small><b>' + m(S.reserva) + '</b></div>' +
            '<div><small>Tranquilidade</small><b>' + Math.round(S.paz) + '/100</b></div></div>';
    }
    function apply(fx) {
        if (fx.saldo) S.saldo += fx.saldo;
        if (fx.divida) S.divida += fx.divida;
        if (fx.paz) S.paz = Math.max(0, Math.min(100, S.paz + fx.paz));
        if (fx.reserva) {
            var need = -fx.reserva;
            if (need > 0) { var use = Math.min(S.reserva, need); S.reserva -= use; S.saldo -= (need - use); }
            else S.reserva += fx.reserva;
        }
        if (fx.pagaDivida && S.saldo > 0) { var pg = Math.min(S.saldo, S.divida); S.saldo -= pg; S.divida -= pg; }
        if (fx.guardaResto && S.saldo > 0) { var g = S.saldo * fx.guardaResto; S.saldo -= g; S.reserva += g; }
        if (S.saldo < 0) { S.divida += -S.saldo; S.saldo = 0; S.paz = Math.max(0, S.paz - 8); S.log.push('O saldo ficou negativo e entrou no cheque especial.'); }
    }
    function show() {
        var e = EVENTS[S.i];
        host.innerHTML = hud() + '<div class="event"><span class="when">' + esc(e.when) + ' · ' + (S.i + 1) + '/' + EVENTS.length + '</span><h2>' + esc(e.title) + '</h2><p>' + esc(e.text) + '</p>' +
            '<div class="quiz-opts">' + e.choices.map(function (c, k) { return '<button type="button" class="quiz-opt" data-k="' + k + '"><span class="k">' + 'ABC'[k] + '</span><span>' + esc(c.t) + '</span></button>'; }).join('') + '</div><div data-after></div></div>';
        host.querySelectorAll('.quiz-opt').forEach(function (b) {
            b.addEventListener('click', function () {
                var c = e.choices[+b.dataset.k];
                host.querySelectorAll('.quiz-opt').forEach(function (x) { x.disabled = true; });
                b.classList.add('right');
                apply(c.fx);
                host.querySelector('.hud').outerHTML = hud();
                host.querySelector('[data-after]').innerHTML = '<div class="flash">' + esc(c.lesson) + '</div><div class="quiz-nav"><button type="button" class="btn btn-solid" data-next>' + (S.i + 1 < EVENTS.length ? 'Continuar' : 'Ver resultado') + '</button></div>';
                host.querySelector('[data-next]').addEventListener('click', function () { S.i++; if (S.i < EVENTS.length) { show(); host.scrollIntoView({ behavior: 'smooth', block: 'start' }); } else end(); });
            });
        });
    }
    function end() {
        var patrimonio = S.saldo + S.reserva - S.divida;
        var pts = Math.max(0, Math.min(100, Math.round(40 + patrimonio / 40 + (S.paz - 60) / 4)));
        var title, text;
        if (pts >= 70) { title = 'Mestre do orçamento'; text = 'Você terminou o mês com as contas sob controle, reserva protegida e sem abrir mão de viver. É exatamente esse equilíbrio que buscamos na consultoria.'; }
        else if (pts >= 45) { title = 'Chegou lá, mas no limite'; text = 'Você sobreviveu ao mês, mas algumas decisões deixaram marcas no próximo. Pequenos ajustes de hábito fariam uma grande diferença.'; }
        else { title = 'O mês venceu você'; text = 'As decisões do mês viraram dívida — e o próximo mês já começa no aperto. A boa notícia: esse ciclo tem solução, com método.'; }
        var juros = S.divida > 0 ? '<p>Atenção: sua dívida de ' + m(S.divida) + ', se ficar no rotativo do cartão a juros de cerca de 13% ao mês, vira aproximadamente ' + m(S.divida * 1.13) + ' em 30 dias.</p>' : '';
        host.innerHTML = hud() + '<div class="quiz-result" style="margin-top:10px"><div class="score-ring"><svg viewBox="0 0 170 170" aria-hidden="true"><circle cx="85" cy="85" r="70" fill="none" stroke="rgba(212,175,55,0.15)" stroke-width="12"/><circle cx="85" cy="85" r="70" fill="none" stroke="#D4AF37" stroke-width="12" stroke-dasharray="' + (2 * Math.PI * 70) + '" stroke-dashoffset="' + (2 * Math.PI * 70 * (1 - pts / 100)) + '"/></svg><div class="n">' + pts + '<small>PONTOS</small></div></div>' +
            '<h2>' + title + '</h2><p>' + text + '</p>' + juros +
            '<p>Resultado do mês: saldo ' + m(S.saldo) + ' + reserva ' + m(S.reserva) + ' − dívidas ' + m(S.divida) + ' = <b style="color:var(--gold-primary)">' + m(patrimonio) + '</b>.</p>' +
            '<div class="tool-cta" style="text-align:left;max-width:620px;margin:24px auto 0"><b>No jogo são oito decisões. Na vida real, são centenas por mês.</b><p>No diagnóstico gratuito, mostramos onde as suas decisões do dia a dia estão custando mais caro — e como virar o jogo de verdade.</p><div class="btn-row"><a class="btn btn-solid" href="' + (host.dataset.wa || '#') + '" target="_blank" rel="noopener">Falar com um consultor</a><a class="btn" href="' + (host.dataset.contact || '#') + '">Agendar diagnóstico</a></div></div>' +
            '<div class="btn-row"><button type="button" class="btn" data-again>Jogar de novo</button></div></div>';
        host.querySelector('[data-again]').addEventListener('click', function () { reset(); show(); });
        host.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    var start = host.querySelector('[data-start]');
    reset();
    if (start) start.addEventListener('click', show); else show();
})();
