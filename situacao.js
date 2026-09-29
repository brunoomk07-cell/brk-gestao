/* BRK — quiz curto de situação (só mostra o nível de alerta) */
(function () {
    var Q = {
        pj: ['O dinheiro da empresa acaba antes do fim do mês, mesmo vendendo bem?', 'Você não sabe dizer quanto a empresa realmente lucra?', 'Contas da empresa e pessoais se misturam?', 'Você usa cheque especial, empréstimo ou cartão para pagar contas do dia a dia?', 'Você é surpreendido por contas que não estavam previstas?'],
        pf: ['O salário acaba antes do fim do mês?', 'Você usa o cartão de crédito para fechar o mês?', 'Você tem dívidas que não diminuem, mesmo pagando?', 'Você não sabe para onde vai o seu dinheiro?', 'Um imprevisto de um mês de salário te colocaria no vermelho?']
    };
    var R = [
        { t: 'Atenção', h: 'Sinais iniciais de descontrole', m: 'Ainda dá para corrigir o rumo com facilidade. Mas, sem um plano, esses sinais tendem a crescer. Um diagnóstico mostra o que fazer primeiro.' },
        { t: 'Alerta', h: 'Você está no caminho do aperto', m: 'Vários pontos já estão pesando. O problema raramente melhora sozinho. Um plano sob medida evita que ele se agrave.' },
        { t: 'Crítico', h: 'Sua situação pede ação agora', m: 'Cada mês sem direção torna a saída mais cara. O caminho existe, mas depende de olhar os seus números reais com quem sabe conduzir.' }
    ];
    var $ = function (i) { return document.getElementById(i); };
    var set, i, score;
    function show(id) { ['sit-pick', 'sit-q', 'sit-res'].forEach(function (x) { $(x).hidden = x !== id; }); }
    function ask() {
        $('sit-text').textContent = Q[set][i];
        $('sit-prog').style.width = (i / Q[set].length * 100) + '%';
    }
    document.querySelectorAll('[data-set]').forEach(function (b) {
        b.addEventListener('click', function () { set = b.getAttribute('data-set'); i = 0; score = 0; show('sit-q'); ask(); });
    });
    document.querySelectorAll('.sit-opts button').forEach(function (b) {
        b.addEventListener('click', function () {
            score += +b.getAttribute('data-v'); i++;
            if (i < Q[set].length) { ask(); return; }
            var r = R[score <= 3 ? 0 : score <= 7 ? 1 : 2];
            $('sit-level').textContent = 'Nível: ' + r.t;
            $('sit-title').textContent = r.h;
            $('sit-msg').textContent = r.m;
            show('sit-res');
        });
    });
})();
