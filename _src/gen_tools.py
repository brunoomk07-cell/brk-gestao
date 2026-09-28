#!/usr/bin/env python3
"""Gera as páginas de ferramentas (_src/pages/ferramentas-*.html) a partir das especificações abaixo."""
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
        title='Calculadora de Ponto de Equilíbrio Online e Grátis | BRK',
        desc='Calcule grátis o ponto de equilíbrio da sua empresa: quanto precisa vender por mês e por dia para não ter prejuízo, com gráfico de faturamento x custos.',
        lead='Descubra quanto sua empresa precisa faturar por mês — e por dia — para cobrir todos os custos. Ajuste os valores e veja o gráfico mudar na hora.',
        inputs=[money('fat', 'Faturamento mensal atual', 100000), pct('cv', 'Custos variáveis (% do faturamento)', 65, 'Mercadoria ou insumos, impostos sobre a venda, taxas de cartão e comissões.'),
                money('fixas', 'Despesas fixas mensais', 30000, 'Aluguel, folha, pró-labore, contador, sistemas, contas fixas.'), pct('dias', 'Dias úteis no mês', 26, '', 'dias')],
        results=[('pe', 'Ponto de equilíbrio', 'wide'), ('mc', 'Margem de contribuição'), ('lucro', 'Lucro operacional'), ('dia', 'Meta diária mínima', 'wide')],
        caption='A linha dourada é o faturamento; a tracejada, o custo total. Onde elas se cruzam está o ponto de equilíbrio.',
        body='''<h2>Como usar o resultado</h2>
<p>O ponto de equilíbrio é o faturamento em que a empresa não tem lucro nem prejuízo. Abaixo dele, cada mês consome caixa; acima dele, sobra dinheiro. A fórmula é simples: <strong>despesas fixas ÷ margem de contribuição</strong>.</p>
<ul><li><strong>Transforme em meta diária</strong> e acompanhe as vendas todo dia.</li><li><strong>Teste decisões antes de tomá-las:</strong> uma contratação ou um aluguel maior sobem o ponto de equilíbrio. Veja quanto.</li><li><strong>Melhore a margem</strong> revendo preço, custo de compra e mix de produtos.</li></ul>
<p>Quer entender o conceito em detalhe? Leia o artigo <a href="{{P}}blog/ponto-de-equilibrio.html">Ponto de equilíbrio: quanto sua empresa precisa vender</a>.</p>''',
        faq=[["O pró-labore entra nas despesas fixas?", "Sim. A retirada dos sócios sai do caixa todo mês e deve entrar no cálculo, senão o ponto de equilíbrio parece menor do que é."],
             ["O que são custos variáveis?", "São os custos que aumentam ou diminuem junto com as vendas: mercadoria, matéria-prima, impostos sobre a venda, taxas de cartão e comissões."]],
    ),
    dict(
        slug='simulador-quitar-dividas', tool='dividas', tag='Pessoa física',
        name='Simulador para quitar dívidas',
        title='Simulador para Quitar Dívidas: Monte seu Plano Grátis | BRK',
        desc='Simule grátis quanto tempo leva para sair das dívidas. Compare os métodos avalanche e bola de neve e veja quanto economiza em juros pagando um valor extra.',
        lead='Liste suas dívidas, informe quanto consegue pagar a mais por mês e veja em quanto tempo você fica livre — e quanto economiza de juros.',
        inputs=['<div data-debts></div><button type="button" class="add-btn" data-add>+ Adicionar dívida</button>',
                money('extra', 'Valor extra por mês (além das parcelas mínimas)', 500, 'Quanto você consegue direcionar a mais para as dívidas.'),
                seg('metodo', 'Estratégia', [('avalanche', 'Avalanche (juros maiores)'), ('bola', 'Bola de neve (saldos menores)')], 'avalanche')],
        results=[('total', 'Total devido hoje'), ('prazo', 'Livre das dívidas em'), ('juros', 'Juros pagos no plano'), ('economia', 'Economia x só o mínimo')],
        caption='Saldo total das dívidas mês a mês: com o plano (dourado) e pagando só o mínimo (tracejado).',
        body='''<h2>Avalanche ou bola de neve?</h2>
<p><strong>Avalanche</strong>: você concentra o dinheiro extra na dívida de juros mais altos. Matematicamente, é o método que paga menos juros. <strong>Bola de neve</strong>: você quita primeiro as dívidas de menor saldo. Paga um pouco mais de juros, mas as vitórias rápidas ajudam a manter a motivação.</p>
<p>Nos dois métodos, quando uma dívida acaba, o valor que ia para ela passa a reforçar a próxima. É esse efeito que acelera a quitação.</p>
<p>Leia também: <a href="{{P}}blog/como-sair-das-dividas.html">Como sair das dívidas: um passo a passo realista</a>.</p>''',
        faq=[["Onde encontro a taxa de juros de cada dívida?", "Na fatura do cartão (procure pelo CET ou taxa do rotativo), no contrato do empréstimo ou no aplicativo do banco. Se não encontrar, pergunte ao atendimento: você tem direito a essa informação."],
             ["E se o simulador disser que a dívida nunca acaba?", "Significa que o que você paga por mês não cobre os juros. O caminho é renegociar, buscar uma linha de crédito mais barata para trocar a dívida ou aumentar o valor destinado a ela."]],
    ),
    dict(
        slug='calculadora-reserva-de-emergencia', tool='reserva', tag='Pessoa física',
        name='Calculadora de reserva de emergência',
        title='Calculadora de Reserva de Emergência: Quanto Guardar | BRK',
        desc='Calcule quanto você precisa ter na reserva de emergência e em quanto tempo chega lá guardando um valor por mês. Grátis, com gráfico.',
        lead='Descubra o valor ideal da sua reserva e quando você vai completá-la, guardando um valor fixo por mês.',
        inputs=[money('gastos', 'Gastos essenciais por mês', 3000, 'Moradia, alimentação, contas, transporte, saúde, escola.'),
                seg('meses', 'Quantos meses de proteção', [('3', '3 meses'), ('6', '6 meses'), ('12', '12 meses')], '6'),
                money('tem', 'Quanto já tenho guardado', 1000), money('aporte', 'Quanto posso guardar por mês', 400),
                pct('taxa', 'Rendimento estimado ao mês', 0.8, 'Aproximado, em aplicação segura com resgate rápido.')],
        results=[('meta', 'Meta da reserva'), ('falta', 'Quanto falta'), ('prazo', 'Tempo para completar'), ('pct', 'Você já tem')],
        caption='Evolução da reserva mês a mês até a meta (linha tracejada).',
        body='''<h2>Quantos meses escolher?</h2>
<p><strong>3 a 6 meses</strong> para quem tem renda estável, como carteira assinada. <strong>6 a 12 meses</strong> para autônomos, MEIs, profissionais com renda variável ou quem é a única fonte de renda da família.</p>
<p>A reserva deve ficar em uma aplicação segura, com resgate rápido e rendimento que ao menos acompanhe a inflação. Não é dinheiro para investir em risco.</p>
<p>Guia completo: <a href="{{P}}blog/reserva-de-emergencia.html">Reserva de emergência: quanto guardar e por onde começar</a>.</p>''',
        faq=[["Devo montar a reserva antes de pagar as dívidas?", "Comece com um degrau pequeno — um mês de gastos essenciais — enquanto ataca as dívidas mais caras. Sem nenhuma reserva, qualquer imprevisto vira uma nova dívida."]],
    ),
    dict(
        slug='simulador-juros-cartao-de-credito', tool='cartao', tag='Pessoa física',
        name='Simulador de juros do cartão (rotativo)',
        title='Simulador de Juros do Cartão de Crédito e Rotativo | BRK',
        desc='Veja quanto a dívida do cartão de crédito custa em juros no rotativo e quanto tempo leva para quitar. Compare pagando o dobro por mês. Simulador grátis.',
        lead='Veja o tamanho real de uma dívida no rotativo do cartão — e o que muda quando você aumenta o pagamento mensal.',
        inputs=[money('saldo', 'Valor da dívida no cartão', 3000), pct('taxa', 'Juros do rotativo ao mês', 13, 'Confira a taxa na sua fatura. O rotativo está entre os créditos mais caros do país.'),
                money('pag', 'Quanto você paga por mês', 350)],
        results=[('prazo', 'Tempo para quitar'), ('juros', 'Juros pagos'), ('total', 'Total pago'), ('dobro', 'Pagando o dobro')],
        caption='Saldo da dívida mês a mês com o pagamento informado (vermelho) e com o dobro (dourado).',
        body='''<h2>Como sair do rotativo</h2>
<ol><li><strong>Pare de usar o cartão</strong> enquanto houver saldo no rotativo.</li><li><strong>Negocie com o banco</strong> um parcelamento com juros menores, ou troque a dívida por uma linha mais barata, como o consignado.</li><li><strong>Use o dinheiro extra</strong> — 13º, restituição, renda extra — para abater o saldo.</li></ol>
<p>Desde 2024, a lei limita os juros e encargos do rotativo e do parcelamento da fatura a 100% do valor original da dívida. Mesmo com esse teto, a dívida pode dobrar.</p>
<p>Leia: <a href="{{P}}blog/cartao-de-credito-rotativo.html">Rotativo do cartão: como sair dessa armadilha</a>.</p>''',
        faq=[["O que é o rotativo do cartão?", "É o crédito que o banco concede automaticamente quando você paga menos que o total da fatura. O valor que ficou para trás entra no rotativo, com juros muito altos."]],
    ),
    dict(
        slug='planilha-orcamento-50-30-20', tool='orcamento', tag='Pessoa física',
        name='Orçamento 50-30-20',
        title='Calculadora de Orçamento 50-30-20 Online | BRK Gestão',
        desc='Divida sua renda pela regra 50-30-20 (necessidades, desejos e futuro) e compare com seus gastos reais em um gráfico. Ferramenta grátis de orçamento pessoal.',
        lead='A regra 50-30-20 é um ponto de partida simples: 50% para necessidades, 30% para desejos e 20% para o futuro e para quitar dívidas. Compare com o seu orçamento real.',
        inputs=[money('renda', 'Renda líquida mensal', 4500), money('nec', 'Seus gastos com necessidades', 2950, 'Moradia, mercado, contas, transporte, saúde.'),
                money('des', 'Seus gastos com desejos', 1000, 'Lazer, delivery, compras, assinaturas.'), money('fut', 'Quanto você guarda ou paga de dívidas', 550)],
        results=[('nec', 'Ideal para necessidades'), ('des', 'Ideal para desejos'), ('fut', 'Ideal para o futuro'), ('sobra', 'Sobra no seu mês')],
        caption='Barras claras: ideal pela regra. Barras cheias: seu orçamento (vermelho indica acima do ideal).',
        body='''<h2>A regra não é lei — é bússola</h2>
<p>Em muitas famílias, só a moradia já passa de 30% da renda. Tudo bem: a regra serve para mostrar onde está o desequilíbrio. Se as necessidades passam de 50%, o ajuste costuma estar em moradia, transporte ou contas fixas. Se o futuro está abaixo de 20%, comece com 5% e aumente aos poucos.</p>
<p>Guia completo: <a href="{{P}}blog/orcamento-familiar-50-30-20.html">Orçamento familiar com a regra 50-30-20</a>.</p>''',
        faq=[["Pagar dívida entra em qual parte?", "Na parte do futuro (20%). Enquanto houver dívidas caras, esse dinheiro deve ir para elas; depois, para a reserva e os investimentos."]],
    ),
    dict(
        slug='simulador-dre-pro-labore', tool='dre', tag='Empresas',
        name='Simulador de DRE e pró-labore',
        title='Simulador de DRE Simplificada e Pró-labore Grátis | BRK',
        desc='Monte a DRE simplificada da sua empresa em segundos: margem de contribuição, lucro operacional e quanto sobra depois do pró-labore, com gráfico em cascata.',
        lead='Veja, em um gráfico em cascata, para onde vai cada real que sua empresa fatura — e se o pró-labore cabe no resultado.',
        inputs=[money('fat', 'Faturamento do mês', 100000), pct('cmv', 'Mercadoria ou insumos (% do faturamento)', 55), pct('imp', 'Impostos sobre a venda (%)', 8),
                pct('tax', 'Taxas de cartão e comissões (%)', 2), money('fixas', 'Despesas fixas', 30000), money('pl', 'Pró-labore e retiradas dos sócios', 12000)],
        results=[('mc', 'Margem de contribuição', 'wide'), ('lucro', 'Lucro operacional'), ('caixa', 'Sobra após retiradas'), ('plmax', 'Pró-labore sustentável (até)', 'wide')],
        caption='Gráfico em cascata: do faturamento até a sobra de caixa depois das retiradas.',
        body='''<h2>O que o gráfico mostra</h2>
<p>A DRE (Demonstração do Resultado) mostra se a empresa dá lucro. A versão gerencial, simplificada, cabe em uma página e responde às perguntas que importam: quanto sobra de cada venda, quanto custa manter a estrutura e quanto os sócios podem retirar sem sufocar o caixa.</p>
<p>O "pró-labore sustentável" é uma referência prudente: até 80% do lucro operacional, deixando uma parte para formar reserva na empresa.</p>
<p>Leia: <a href="{{P}}blog/dre-gerencial.html">DRE gerencial: como montar e usar</a> e <a href="{{P}}blog/separar-financas-pessoais-e-da-empresa.html">como definir o pró-labore</a>.</p>''',
        faq=[["DRE é a mesma coisa que fluxo de caixa?", "Não. A DRE mostra lucro ou prejuízo pelo regime de competência (o que foi vendido e gasto no período). O fluxo de caixa mostra quando o dinheiro entra e sai da conta. As duas visões se complementam."]],
    ),
    dict(
        slug='calculadora-limite-mei', tool='mei', tag='MEI',
        name='Calculadora do limite do MEI',
        title='Calculadora do Limite do MEI 2026 (R$ 81 mil) | BRK',
        desc='Projete seu faturamento anual e veja se vai estourar o limite do MEI de R$ 81 mil em 2026. Descubra a média mensal máxima para continuar MEI.',
        lead='Acompanhe o faturamento acumulado do ano e descubra se você vai passar do limite de R$ 81 mil — antes que isso aconteça.',
        inputs=[money('feito', 'Faturado no ano até agora', 52000), pct('mes', 'Mês atual (1 a 12)', 8, 'Ex.: agosto = 8.', 'º mês'), money('media', 'Média mensal prevista até dezembro', 7000)],
        results=[('proj', 'Projeção para o ano'), ('pct', 'Do limite de R$ 81 mil'), ('resta', 'Ainda pode faturar'), ('max', 'Média máxima por mês')],
        caption='Faturamento acumulado, projeção até dezembro e as linhas do limite e da tolerância de 20%.',
        body='''<h2>O que acontece se passar do limite</h2>
<p>Se o faturamento do ano passar de R$ 81 mil em até 20% (até R$ 97,2 mil), o desenquadramento vale a partir de janeiro do ano seguinte e você paga um DAS complementar sobre o excesso. Acima de 20%, o desenquadramento retroage a janeiro do ano em que o limite foi estourado.</p>
<p>Para quem abriu o MEI no meio do ano, o limite é proporcional: R$ 6.750 por mês de atividade.</p>
<p>Guia completo: <a href="{{P}}blog/financas-do-mei.html">Finanças do MEI na prática</a>.</p>''',
        faq=[["O limite do MEI aumentou em 2026?", "Não. O limite continua em R$ 81 mil por ano. Existem projetos no Congresso para aumentá-lo, mas nenhum havia sido aprovado até a última atualização desta página."]],
    ),
    dict(
        slug='simulador-liberdade-financeira', tool='liberdade', tag='Pessoa física',
        name='Simulador de liberdade financeira',
        title='Simulador de Juros Compostos e Liberdade Financeira | BRK',
        desc='Simule quanto seu dinheiro pode crescer com aportes mensais e juros compostos, e quanta renda mensal esse patrimônio poderia gerar. Grátis, com gráfico.',
        lead='Veja o poder dos juros compostos: quanto seu patrimônio pode crescer guardando todo mês — e quanta renda ele poderia gerar.',
        inputs=[money('ini', 'Valor inicial', 5000), money('aporte', 'Aporte mensal', 500), pct('taxa', 'Rentabilidade real ao ano', 4, 'Acima da inflação. Use valores conservadores, como 3% a 5%.'),
                pct('anos', 'Prazo', 20, '', 'anos')],
        results=[('total', 'Patrimônio final'), ('aportado', 'Total guardado'), ('juros', 'Rendimentos'), ('renda', 'Renda mensal possível')],
        caption='A parte clara é o que você guardou; a dourada, o que os juros compostos acrescentaram.',
        body='''<h2>Liberdade financeira é constância</h2>
<p>O segredo dos juros compostos é o tempo: nos primeiros anos, o crescimento vem quase todo dos seus aportes; depois, os rendimentos passam a trabalhar por você. Por isso, começar cedo — mesmo com pouco — vale mais do que começar tarde com muito.</p>
<p>Esta simulação é educativa e usa uma taxa real constante. Rendimentos reais variam, e investimentos com retorno maior envolvem riscos maiores.</p>''',
        faq=[["O que é rentabilidade real?", "É o rendimento acima da inflação. Se um investimento rende 10% ao ano e a inflação é de 5%, a rentabilidade real é de cerca de 4,8%."]],
    ),
]


def page(t):
    meta = {
        'url': f"ferramentas/{t['slug']}.html", 'nav': 'ferramentas/', 'title': t['title'], 'description': t['desc'],
        'priority': '0.8', 'scripts': ['chart', 'tools'],
        'breadcrumb': [['Início', ''], ['Ferramentas', 'ferramentas/'], [t['name'], f"ferramentas/{t['slug']}.html"]],
        'faq': t['faq'], 'app': t['name'],
    }
    inputs = ''.join(t['inputs'])
    return f'''<!--meta
{json.dumps(meta, ensure_ascii=False, indent=1)}
-->
<div class="container">
  <section class="page-hero">
    <ol class="breadcrumb"><li><a href="{{{{P}}}}index.html">Início</a></li><li><a href="{{{{P}}}}ferramentas/">Ferramentas</a></li><li>{t['name']}</li></ol>
    <span class="eyebrow">Ferramenta gratuita · {t['tag']}</span>
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
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="prose">
      {t['body']}
      <div class="callout">
        <h3>Quer ajuda para aplicar isso na sua realidade?</h3>
        <p>Na consultoria, fazemos essas contas com os seus números reais e montamos um plano de ação. O diagnóstico é gratuito — presencial no Grande ABC ou online.</p>
        <p><a href="{{{{WA}}}}" target="_blank" rel="noopener">Falar pelo WhatsApp →</a></p>
      </div>
      <h2>Perguntas frequentes</h2>
<!--FAQ-->
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Mais ferramentas</span><h2 class="section-title">Continue simulando</h2></div>
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
    # índice usado pelo build para os cards
    idx = [{'url': f"ferramentas/{t['slug']}.html", 'name': t['name'], 'tag': t['tag'], 'lead': t['lead']} for t in TOOLS]
    (Path(__file__).resolve().parent / 'tools_index.json').write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding='utf-8')
