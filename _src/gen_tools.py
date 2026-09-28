#!/usr/bin/env python3
"""Gera as páginas de ferramentas (_src/pages/ferramentas-*.html) a partir das especificações abaixo.
Filosofia: a ferramenta revela o tamanho do problema; a solução é apresentada no diagnóstico."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'pages'


def money(name, label, value, hint=''):
    h = f'<p class="hint">{hint}</p>' if hint else ''
    return f'<div class="field"><label for="{name}">{label}</label><div class="input-money"><span>R$</span><input type="number" inputmode="decimal" min="0" step="any" id="{name}" name="{name}" value="{value}"></div>{h}</div>'


def pct(name, label, value, hint='', suffix='%'):
    h = f'<p class="hint">{hint}</p>' if hint else ''
    return f'<div class="field"><label for="{name}">{label}</label><div class="input-suffix"><input type="number" inputmode="decimal" min="0" step="any" id="{name}" name="{name}" value="{value}"><span>{suffix}</span></div>{h}</div>'


def seg(name, label, options, default):
    on = ' class="on"'
    btns = ''.join(f'<button type="button" data-v="{v}"{on if v == default else ""}>{t}</button>' for v, t in options)
    return f'<div class="field"><label>{label}</label><div class="seg" data-name="{name}" data-value="{default}">{btns}</div></div>'


def results(items):
    out = []
    for key, label, *rest in items:
        cls = ' wide' if rest and rest[0] == 'wide' else ''
        out.append(f'<div class="result{cls}"><small>{label}</small><b data-out="{key}">—</b></div>')
    return '<div class="results">' + ''.join(out) + '</div>'


TOOLS = [
    dict(
        slug='calculadora-ponto-de-equilibrio', tool='pe', tag='Empresas',
        name='Calculadora de ponto de equilíbrio',
        title='Calculadora de Ponto de Equilíbrio Grátis e Online | BRK',
        desc='Descubra grátis quanto sua empresa precisa vender por mês para não ter prejuízo — e quanto falta. Calculadora de ponto de equilíbrio com gráfico.',
        lead='Sua empresa está vendendo o suficiente para pagar a própria estrutura? Coloque seus números e descubra a venda mínima para não ter prejuízo — e a distância até ela.',
        wa='Olá! Usei a calculadora de ponto de equilíbrio no site da BRK e quero entender os números da minha empresa.',
        inputs=[money('fat', 'Faturamento mensal atual', 100000), pct('cv', 'Custos variáveis (% do faturamento)', 65, 'Mercadoria ou insumos, impostos sobre a venda, taxas de cartão e comissões.'),
                money('fixas', 'Despesas fixas mensais', 30000, 'Aluguel, folha, pró-labore, contador, sistemas, contas fixas.'), pct('dias', 'Dias úteis no mês', 26, '', 'dias')],
        results=[('pe', 'Venda mínima para não ter prejuízo', 'wide'), ('mc', 'Margem de contribuição'), ('lucro', 'Lucro operacional'), ('dia', 'Meta diária mínima', 'wide')],
        caption='A linha dourada é o faturamento; a tracejada, o custo total. Abaixo do cruzamento, a empresa perde dinheiro.',
        cta_title='Esse número está perto demais — ou longe demais?',
        cta_text='Saber o ponto de equilíbrio é só o começo. No diagnóstico, mostramos o que está puxando esse número para cima e quais ajustes trazem a sua empresa para uma zona segura.',
        reveal='''<h2>O que esse número revela</h2>
<p>O ponto de equilíbrio é a linha que separa o lucro do prejuízo. A maioria dos pequenos empresários nunca calculou esse número — e só descobre que o mês foi ruim quando o dinheiro já acabou.</p>
<ul><li><strong>Folga pequena</strong> entre o faturamento e o ponto de equilíbrio significa que qualquer queda de vendas vira prejuízo.</li><li><strong>Margem de contribuição baixa</strong> costuma indicar preço defasado, custo de compra alto ou produtos que vendem muito e deixam pouco.</li><li><strong>Despesas fixas altas</strong> fazem a empresa precisar vender cada vez mais só para empatar.</li></ul>
<p>Descobrir qual desses fatores pesa mais no seu caso — e como corrigir sem sufocar a operação — é exatamente o trabalho da consultoria.</p>''',
        faq=[["O pró-labore entra nas despesas fixas?", "Sim. A retirada dos sócios sai do caixa todo mês e deve entrar no cálculo, senão o ponto de equilíbrio parece menor do que é."],
             ["O que são custos variáveis?", "São os custos que sobem e descem junto com as vendas: mercadoria, matéria-prima, impostos sobre a venda, taxas de cartão e comissões."]],
    ),
    dict(
        slug='simulador-quitar-dividas', tool='dividas', tag='Pessoa física',
        name='Simulador de dívidas: quanto você ainda vai pagar',
        title='Simulador de Dívidas: Quanto Tempo e Juros Até Quitar? | BRK',
        desc='Simule grátis quanto tempo suas dívidas vão durar e quanto você vai pagar de juros. Veja o que acontece pagando só o mínimo.',
        lead='Coloque suas dívidas e veja a verdade: quanto tempo elas ainda vão durar, quanto você vai pagar só de juros — e o que acontece se continuar pagando apenas o mínimo.',
        wa='Olá! Usei o simulador de dívidas no site da BRK e preciso de ajuda para sair das dívidas.',
        inputs=['<div data-debts></div><button type="button" class="add-btn" data-add>+ Adicionar dívida</button>',
                money('extra', 'Quanto consigo pagar a mais por mês', 500, 'Além das parcelas mínimas.')],
        results=[('total', 'Total devido hoje'), ('prazo', 'Livre das dívidas em'), ('juros', 'Juros que ainda vai pagar'), ('economia', 'Só pagando o mínimo')],
        caption='Saldo total das dívidas mês a mês: com um pagamento extra (dourado) e pagando só o mínimo (tracejado).',
        cta_title='Existe um caminho mais rápido e mais barato para sair dessa.',
        cta_text='A ordem certa de pagamento, a renegociação bem feita e a troca de dívidas caras podem cortar meses — e milhares de reais em juros. No diagnóstico gratuito, montamos esse plano com os seus números.',
        reveal='''<h2>O que esse número revela</h2>
<p>A maioria das pessoas endividadas não sabe quanto deve de verdade — nem quanto ainda vai pagar de juros. Quando os juros do mês são maiores que a parcela, a dívida não diminui: ela cresce, mesmo com você pagando em dia.</p>
<ul><li><strong>Pagar só o mínimo</strong> quase sempre significa pagar a dívida várias vezes.</li><li><strong>Dívidas diferentes têm custos muito diferentes</strong> — e a ordem de pagamento muda completamente o resultado.</li><li><strong>Renegociar sem estratégia</strong> pode trocar uma dívida cara por outra mais longa e mais cara ainda.</li></ul>
<p>Sair das dívidas exige um plano feito para o seu orçamento — e disciplina para não voltar. É isso que construímos com você.</p>''',
        faq=[["Onde encontro a taxa de juros de cada dívida?", "Na fatura do cartão (procure pelo CET ou taxa do rotativo), no contrato do empréstimo ou no aplicativo do banco. Você tem direito a essa informação."],
             ["E se o simulador disser que a dívida nunca acaba?", "Significa que o valor pago por mês não cobre os juros. Nesse caso, é urgente reorganizar as dívidas — e é exatamente o tipo de situação em que um plano profissional faz mais diferença."]],
    ),
    dict(
        slug='calculadora-reserva-de-emergencia', tool='reserva', tag='Pessoa física',
        name='Calculadora de reserva de emergência',
        title='Reserva de Emergência: Você Está Protegido? Calcule Grátis | BRK',
        desc='Calcule quanto você precisa ter guardado para imprevistos e em quanto tempo chega lá. Descubra o quanto está exposto hoje.',
        lead='Se a sua renda parasse hoje, por quanto tempo você aguentaria? Descubra o tamanho da proteção que você precisa — e o quanto está exposto agora.',
        wa='Olá! Usei a calculadora de reserva de emergência no site da BRK e quero organizar minhas finanças.',
        inputs=[money('gastos', 'Gastos essenciais por mês', 3000, 'Moradia, alimentação, contas, transporte, saúde, escola.'),
                seg('meses', 'Quantos meses de proteção', [('3', '3 meses'), ('6', '6 meses'), ('12', '12 meses')], '6'),
                money('tem', 'Quanto já tenho guardado', 1000), money('aporte', 'Quanto consigo guardar por mês', 400),
                pct('taxa', 'Rendimento estimado ao mês', 0.8)],
        results=[('meta', 'Proteção necessária'), ('falta', 'Quanto falta'), ('prazo', 'Tempo para completar'), ('pct', 'Você está protegido em')],
        caption='Evolução da reserva mês a mês até a proteção necessária (linha tracejada).',
        cta_title='Não consegue guardar? O problema raramente é a renda.',
        cta_text='Na maioria dos casos, o dinheiro para a reserva existe — ele só está vazando em lugares que você não vê. No diagnóstico, encontramos esses vazamentos e montamos um plano realista.',
        reveal='''<h2>O que esse número revela</h2>
<p>Sem reserva, qualquer imprevisto — um conserto, uma doença, uma demissão — vira dívida cara no cartão ou no cheque especial. É assim que muitas famílias entram no ciclo do endividamento.</p>
<p>Quanto menor a sua proteção hoje, maior o risco de um mês ruim desorganizar os próximos. Quem tem renda variável, como autônomos e MEIs, precisa de uma proteção ainda maior.</p>''',
        faq=[["Devo montar a reserva antes de pagar as dívidas?", "Depende das suas dívidas, dos juros e do seu orçamento. Essa é uma das decisões que definimos com você no diagnóstico, com base nos seus números."]],
    ),
    dict(
        slug='simulador-juros-cartao-de-credito', tool='cartao', tag='Pessoa física',
        name='Simulador de juros do cartão (rotativo)',
        title='Simulador de Juros do Cartão: Quanto Custa o Rotativo? | BRK',
        desc='Veja quanto a dívida do cartão de crédito vai custar em juros no rotativo e quanto tempo leva para quitar. Simulador grátis com gráfico.',
        lead='Pagando o mínimo da fatura? Veja quanto essa dívida realmente vai custar — e por quanto tempo ela vai te acompanhar.',
        wa='Olá! Usei o simulador de juros do cartão no site da BRK e preciso de ajuda com minha dívida.',
        inputs=[money('saldo', 'Valor da dívida no cartão', 3000), pct('taxa', 'Juros do rotativo ao mês', 13, 'Confira a taxa na sua fatura.'),
                money('pag', 'Quanto você paga por mês', 350)],
        results=[('prazo', 'Tempo para quitar'), ('juros', 'Juros pagos'), ('total', 'Total pago'), ('dobro', 'Pagando o dobro')],
        caption='Saldo da dívida mês a mês com o pagamento informado (vermelho) e com o dobro (dourado).',
        cta_title='O rotativo tem saída — mas não é pagando o mínimo.',
        cta_text='Existem formas de interromper essa dívida e parar de pagar juros tão altos. No diagnóstico gratuito, analisamos a sua situação e mostramos o caminho mais barato para sair.',
        reveal='''<h2>O que esse número revela</h2>
<p>O rotativo do cartão está entre os créditos mais caros do país e aparece em mais de 8 em cada 10 famílias endividadas. Uma dívida pequena pode dobrar em poucos meses.</p>
<p>Desde 2024, a lei limita os juros e encargos do rotativo e do parcelamento da fatura a 100% do valor original da dívida. Mesmo com esse teto, você pode acabar pagando o dobro do que comprou.</p>''',
        faq=[["O que é o rotativo do cartão?", "É o crédito que o banco concede automaticamente quando você paga menos que o total da fatura. O valor que ficou para trás entra no rotativo, com juros muito altos."]],
    ),
    dict(
        slug='planilha-orcamento-50-30-20', tool='orcamento', tag='Pessoa física',
        name='Orçamento 50-30-20: seu dinheiro está equilibrado?',
        title='Orçamento 50-30-20: Seu Salário Está Equilibrado? Teste Grátis | BRK',
        desc='Compare seus gastos com a regra 50-30-20 e descubra, em um gráfico, onde o seu orçamento está desequilibrado.',
        lead='Coloque sua renda e seus gastos e veja, num gráfico, onde o seu orçamento está desequilibrado em relação a uma referência saudável.',
        wa='Olá! Usei a ferramenta de orçamento no site da BRK e quero organizar minhas finanças.',
        inputs=[money('renda', 'Renda líquida mensal', 4500), money('nec', 'Gastos com necessidades', 2950, 'Moradia, mercado, contas, transporte, saúde.'),
                money('des', 'Gastos com desejos', 1000, 'Lazer, delivery, compras, assinaturas.'), money('fut', 'Quanto você guarda ou paga de dívidas', 550)],
        results=[('nec', 'Referência: necessidades'), ('des', 'Referência: desejos'), ('fut', 'Referência: futuro'), ('sobra', 'Sobra no seu mês')],
        caption='Barras claras: referência. Barras cheias: seu orçamento (vermelho indica desequilíbrio).',
        cta_title='Viu o desequilíbrio. E agora?',
        cta_text='Cortar no escuro raramente funciona — e quase nunca dura. No diagnóstico, identificamos onde ajustar sem sacrificar o que importa para você e sua família.',
        reveal='''<h2>O que esse número revela</h2>
<p>A regra 50-30-20 é uma referência simples: metade da renda para necessidades, 30% para desejos e 20% para o futuro. Quando uma dessas partes estoura, o orçamento fica frágil — e o dinheiro acaba antes do mês.</p>
<p>O mais comum é o "futuro" ficar perto de zero. É o sinal de que não sobra nada para reserva, investimentos ou para sair das dívidas.</p>''',
        faq=[["E se minha realidade não cabe na regra?", "A regra é só uma referência. O plano ideal depende da sua renda, do custo de vida da sua região e dos seus objetivos — é isso que definimos na consultoria."]],
    ),
    dict(
        slug='simulador-dre-pro-labore', tool='dre', tag='Empresas',
        name='Simulador: sua empresa está perdendo caixa?',
        title='Empresa Perdendo Dinheiro? Simulador de DRE Grátis | BRK',
        desc='Veja em um gráfico em cascata para onde vai cada real que sua empresa fatura — e se as retiradas dos sócios estão consumindo o caixa.',
        lead='Veja, em um gráfico em cascata, para onde vai cada real que a sua empresa fatura — e se as retiradas estão maiores do que o negócio aguenta.',
        wa='Olá! Usei o simulador de DRE no site da BRK e quero entender o resultado da minha empresa.',
        inputs=[money('fat', 'Faturamento do mês', 100000), pct('cmv', 'Mercadoria ou insumos (% do faturamento)', 55), pct('imp', 'Impostos sobre a venda (%)', 8),
                pct('tax', 'Taxas de cartão e comissões (%)', 2), money('fixas', 'Despesas fixas', 30000), money('pl', 'Retiradas dos sócios', 12000)],
        results=[('mc', 'Margem de contribuição', 'wide'), ('lucro', 'Lucro operacional'), ('caixa', 'Sobra após retiradas'), ('plmax', 'Retirada que o negócio aguenta', 'wide')],
        caption='Do faturamento até a sobra de caixa depois das retiradas.',
        cta_title='Se a sobra ficou no vermelho, o caixa está sangrando.',
        cta_text='Esse é um dos problemas mais comuns — e mais silenciosos — das pequenas empresas. No diagnóstico gratuito, mostramos exatamente onde está o vazamento e como corrigir.',
        reveal='''<h2>O que esse número revela</h2>
<p>Muitas empresas dão lucro no papel e, mesmo assim, vivem pedindo empréstimo. O motivo mais comum: os sócios retiram mais do que o negócio gera, ou a margem já chega baixa demais para pagar a estrutura.</p>
<p>O resultado aparece devagar — cheque especial aqui, antecipação ali — até virar uma dívida difícil de controlar. Enxergar isso cedo é o que separa um ajuste simples de uma crise.</p>''',
        faq=[["Isso é o mesmo que a DRE do meu contador?", "A lógica é parecida, mas a DRE gerencial é feita para decidir, não para o fisco. Na consultoria, montamos a sua DRE gerencial com os números reais e ensinamos a usá-la."]],
    ),
    dict(
        slug='calculadora-limite-mei', tool='mei', tag='MEI',
        name='Calculadora do limite do MEI',
        title='Calculadora do Limite do MEI 2026: Vai Estourar os R$ 81 Mil? | BRK',
        desc='Projete seu faturamento anual e veja se vai estourar o limite do MEI de R$ 81 mil em 2026 — antes que isso vire um problema com impostos.',
        lead='Você vai estourar o limite do MEI este ano? Projete o faturamento e descubra antes que isso vire um problema com impostos.',
        wa='Olá! Usei a calculadora do limite do MEI no site da BRK e quero me planejar.',
        inputs=[money('feito', 'Faturado no ano até agora', 52000), pct('mes', 'Mês atual (1 a 12)', 8, 'Ex.: agosto = 8.', 'º mês'), money('media', 'Média mensal prevista até dezembro', 7000)],
        results=[('proj', 'Projeção para o ano'), ('pct', 'Do limite de R$ 81 mil'), ('resta', 'Ainda pode faturar'), ('max', 'Média máxima por mês')],
        caption='Faturamento acumulado, projeção até dezembro e as linhas do limite e da tolerância de 20%.',
        cta_title='Crescer é ótimo. Crescer sem planejamento sai caro.',
        cta_text='Passar do limite muda os impostos, o preço e o caixa do seu negócio. No diagnóstico, preparamos a transição para que o crescimento vire lucro — e não susto.',
        reveal='''<h2>O que esse número revela</h2>
<p>O limite do MEI é de R$ 81 mil por ano. Se o faturamento passar em até 20%, o desenquadramento vale a partir de janeiro seguinte, com imposto extra sobre o excesso. Acima de 20%, ele retroage a janeiro do próprio ano — e os impostos de microempresa incidem sobre todo o período.</p>
<p>Muitos MEIs só percebem isso quando a conta chega. E, sem ajustar preço e estrutura, a mudança de regime pode transformar crescimento em prejuízo.</p>''',
        faq=[["O limite do MEI aumentou em 2026?", "Não. O limite continua em R$ 81 mil por ano. Existem projetos no Congresso para aumentá-lo, mas nenhum havia sido aprovado até a última atualização desta página."]],
    ),
    dict(
        slug='simulador-liberdade-financeira', tool='liberdade', tag='Pessoa física',
        name='Simulador de liberdade financeira',
        title='Simulador de Liberdade Financeira e Juros Compostos Grátis | BRK',
        desc='Simule quanto seu patrimônio pode crescer guardando todo mês e quanta renda ele poderia gerar. Grátis, com gráfico.',
        lead='Veja onde você pode chegar guardando todo mês — e quanta renda esse patrimônio poderia gerar para você.',
        wa='Olá! Usei o simulador de liberdade financeira no site da BRK e quero montar meu plano.',
        inputs=[money('ini', 'Valor inicial', 5000), money('aporte', 'Quanto posso guardar por mês', 500), pct('taxa', 'Rentabilidade real ao ano', 4, 'Acima da inflação. Use valores conservadores.'),
                pct('anos', 'Prazo', 20, '', 'anos')],
        results=[('total', 'Patrimônio final'), ('aportado', 'Total guardado'), ('juros', 'Rendimentos'), ('renda', 'Renda mensal possível')],
        caption='A parte clara é o que você guardou; a dourada, o que os juros compostos acrescentaram.',
        cta_title='O difícil não é a conta. É conseguir guardar todo mês.',
        cta_text='Liberdade financeira começa com um orçamento que sobra. No diagnóstico gratuito, descobrimos quanto você realmente pode guardar e o que está impedindo isso hoje.',
        reveal='''<h2>O que esse número revela</h2>
<p>Com tempo e constância, os rendimentos passam a trabalhar por você. Mas a simulação só vira realidade se sobrar dinheiro todo mês — e é aí que a maioria das pessoas trava.</p>
<p>Esta simulação é educativa e usa uma taxa real constante. Rendimentos reais variam, e investimentos com retorno maior envolvem riscos maiores.</p>''',
        faq=[["O que é rentabilidade real?", "É o rendimento acima da inflação. Se um investimento rende 10% ao ano e a inflação é de 5%, a rentabilidade real é de cerca de 4,8%."]],
    ),
]


def page(t):
    meta = {
        'url': f"ferramentas/{t['slug']}.html", 'nav': 'ferramentas/', 'title': t['title'], 'description': t['desc'],
        'priority': '0.8', 'scripts': ['chart', 'tools'], 'wa_text': t['wa'],
        'breadcrumb': [['Início', ''], ['Simuladores', 'ferramentas/'], [t['name'], f"ferramentas/{t['slug']}.html"]],
        'faq': t['faq'], 'app': t['name'],
    }
    inputs = ''.join(t['inputs'])
    return f'''<!--meta
{json.dumps(meta, ensure_ascii=False, indent=1)}
-->
<div class="container">
  <section class="page-hero">
    <ol class="breadcrumb"><li><a href="{{{{P}}}}index.html">Início</a></li><li><a href="{{{{P}}}}ferramentas/">Simuladores</a></li><li>{t['name']}</li></ol>
    <span class="eyebrow">Simulador gratuito · {t['tag']}</span>
    <h1>{t['name']}</h1>
    <p class="lead">{t['lead']}</p>
  </section>
</div>

<section class="section" style="padding-top:40px">
  <div class="container">
    <div class="tool" data-tool="{t['tool']}">
      <div class="tool-panel">
        <h2>Seus números</h2>
        {inputs}
      </div>
      <div>
        {results(t['results'])}
        <div class="verdict" data-out="verdict" aria-live="polite"></div>
        <div class="chart-box tall"><canvas role="img" aria-label="Gráfico: {t['name']}"></canvas></div>
        <p class="chart-caption">{t['caption']}</p>
        <div class="tool-cta">
          <b>{t['cta_title']}</b>
          <p>{t['cta_text']}</p>
          <div class="btn-row">
            <a href="{{{{WA_CTX}}}}" class="btn btn-solid" target="_blank" rel="noopener">{{{{WA_ICON}}}} Falar com um consultor</a>
            <a href="{{{{P}}}}contato.html" class="btn">Agendar diagnóstico</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="prose">
      {t['reveal']}
      <h2>Perguntas frequentes</h2>
<!--FAQ-->
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Os números mostram o problema. <em>Nós mostramos a solução.</em></h2>
    <p>Diagnóstico gratuito, presencial em Mauá, Santo André e Grande ABC ou online.</p>
    <div class="btn-row">
      <a href="{{{{P}}}}contato.html" class="btn btn-solid">Agendar diagnóstico gratuito</a>
      <a href="{{{{WA_CTX}}}}" class="btn btn-wa" target="_blank" rel="noopener">{{{{WA_ICON}}}} WhatsApp</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Outros simuladores</span><h2 class="section-title">Descubra outros pontos de risco</h2></div>
    <div class="grid grid-3">
<!--TOOLS_RELATED-->
    </div>
  </div>
</section>
'''


if __name__ == '__main__':
    for t in TOOLS:
        (OUT / f"ferramentas-{t['slug']}.html").write_text(page(t), encoding='utf-8')
        print('ok', t['slug'])
    idx = [{'url': f"ferramentas/{t['slug']}.html", 'name': t['name'], 'tag': t['tag'], 'lead': t['lead']} for t in TOOLS]
    (Path(__file__).resolve().parent / 'tools_index.json').write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding='utf-8')
