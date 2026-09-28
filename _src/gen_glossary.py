#!/usr/bin/env python3
"""Gera a página do glossário financeiro (_src/pages/aprenda-glossario.html)."""
import json, unicodedata
from pathlib import Path

TERMS = [
    ("Amortização", "Parte da parcela de um empréstimo que reduz a dívida de fato. O resto da parcela são juros.", "Numa parcela de R$ 500, R$ 350 podem ser amortização e R$ 150, juros."),
    ("Ativo", "Tudo o que a empresa ou a pessoa possui e que tem valor econômico: dinheiro, estoque, contas a receber, equipamentos, imóveis.", ""),
    ("Balanço patrimonial", "Relatório que mostra, em uma data, o que a empresa tem (ativos), o que deve (passivos) e o patrimônio dos sócios.", ""),
    ("Bola de neve (método)", "Estratégia para quitar dívidas começando pelas de menor saldo, para ganhar motivação com vitórias rápidas.", ""),
    ("Capital de giro", "Dinheiro necessário para manter a operação funcionando entre o pagamento a fornecedores e o recebimento dos clientes.", "Se você paga o estoque à vista e recebe em 30 dias, precisa de capital de giro para cobrir esse intervalo."),
    ("CDI", "Taxa de juros praticada entre bancos, que acompanha de perto a Selic. É referência para muitos investimentos de renda fixa.", ""),
    ("CET (Custo Efetivo Total)", "Custo real de um empréstimo ou financiamento, somando juros, tarifas, seguros e impostos. É o número certo para comparar ofertas.", ""),
    ("Ciclo financeiro", "Número de dias entre pagar o fornecedor e receber do cliente. Quanto maior, mais capital de giro a empresa precisa.", "Prazo de estoque (30) + prazo de recebimento (30) − prazo de pagamento (20) = 40 dias."),
    ("CMV", "Custo da Mercadoria Vendida: quanto custaram os produtos que foram efetivamente vendidos no período.", ""),
    ("Compliance", "Conjunto de práticas para garantir que a empresa cumpra leis, normas e regras internas.", ""),
    ("Conselho consultivo", "Grupo de conselheiros, muitas vezes externos, que orienta os sócios em decisões estratégicas, sem poder legal de decisão.", ""),
    ("Custo fixo", "Gasto que existe independentemente do volume de vendas: aluguel, folha administrativa, contador, sistemas.", ""),
    ("Custo variável", "Gasto que aumenta ou diminui junto com as vendas: mercadoria, matéria-prima, impostos sobre a venda, comissões, taxas de cartão.", ""),
    ("DAS", "Documento de Arrecadação do Simples Nacional. Para o MEI, é o boleto mensal de valor fixo que reúne INSS, ICMS e/ou ISS.", ""),
    ("Depreciação", "Perda de valor de um bem (máquina, veículo, computador) com o uso e o tempo, registrada como despesa ao longo da vida útil.", ""),
    ("Desenquadramento do MEI", "Saída do regime de MEI, obrigatória quando o faturamento anual passa do limite ou quando a atividade deixa de ser permitida.", ""),
    ("Distribuição de lucros", "Parte do lucro da empresa repassada aos sócios depois de apurado o resultado. Diferente do pró-labore, só existe se houver lucro.", ""),
    ("DRE", "Demonstração do Resultado do Exercício: relatório que mostra receitas, custos, despesas e o lucro ou prejuízo de um período.", ""),
    ("EBITDA", "Lucro antes de juros, impostos sobre o lucro, depreciação e amortização. Mede a geração de caixa da operação.", ""),
    ("Endividamento", "Situação de quem tem dívidas, estejam elas em dia ou não. Diferente de inadimplência, que é ter dívidas em atraso.", ""),
    ("Fluxo de caixa", "Registro e projeção de todas as entradas e saídas de dinheiro, com as datas em que acontecem.", ""),
    ("Giro de estoque", "Quantas vezes o estoque é vendido e reposto em um período. Estoque parado é dinheiro parado.", ""),
    ("Governança corporativa", "Conjunto de regras, papéis e rotinas que organiza como a empresa é dirigida, controlada e como as decisões são tomadas.", ""),
    ("Inadimplência", "Situação de quem está com contas ou dívidas em atraso.", ""),
    ("Índice de liquidez corrente", "Ativo circulante dividido pelo passivo circulante. Acima de 1, a empresa tem mais recursos de curto prazo do que dívidas de curto prazo.", ""),
    ("IPCA", "Índice oficial de inflação do Brasil, calculado pelo IBGE.", ""),
    ("Juros compostos", "Juros calculados sobre o valor inicial mais os juros já acumulados — os 'juros sobre juros'.", "R$ 1.000 a 1% ao mês viram cerca de R$ 1.127 em 12 meses."),
    ("Juros simples", "Juros calculados sempre sobre o valor inicial, sem incidir sobre os juros anteriores.", ""),
    ("Liquidez", "Facilidade de transformar um bem ou investimento em dinheiro sem perder valor.", ""),
    ("Lucro bruto", "Faturamento menos impostos sobre a venda e o custo das mercadorias ou serviços vendidos.", ""),
    ("Lucro líquido", "O que sobra depois de todos os custos, despesas, juros e impostos. É o resultado final da empresa.", ""),
    ("Lucro operacional", "Resultado da atividade principal da empresa, antes de juros e impostos sobre o lucro.", ""),
    ("Margem de contribuição", "O que sobra de cada venda depois dos custos variáveis. É o dinheiro que paga as despesas fixas e gera lucro.", "Venda de R$ 100 com R$ 65 de custos variáveis = margem de R$ 35 (35%)."),
    ("Margem líquida", "Lucro líquido dividido pelo faturamento. Mostra quanto de cada real vendido vira lucro.", ""),
    ("Markup", "Índice aplicado sobre o custo para chegar ao preço de venda, considerando despesas, impostos e a margem de lucro desejada.", ""),
    ("MEI", "Microempreendedor Individual: regime simplificado para quem fatura até R$ 81 mil por ano, com imposto fixo mensal (DAS).", ""),
    ("Passivo", "Tudo o que a empresa deve: fornecedores, empréstimos, impostos, salários a pagar.", ""),
    ("Patrimônio líquido", "Diferença entre o que a empresa tem (ativos) e o que deve (passivos). É o valor que pertence aos sócios.", ""),
    ("Ponto de equilíbrio", "Faturamento em que a empresa não tem lucro nem prejuízo. Calcula-se dividindo as despesas fixas pela margem de contribuição.", "R$ 30 mil de despesas fixas ÷ 35% de margem = R$ 85.714."),
    ("Prazo médio de pagamento", "Média de dias que a empresa leva para pagar seus fornecedores.", ""),
    ("Prazo médio de recebimento", "Média de dias que a empresa leva para receber de seus clientes.", ""),
    ("Precificação", "Processo de definir o preço de venda a partir dos custos, das despesas, dos impostos, da margem desejada e do mercado.", ""),
    ("Pró-labore", "Remuneração fixa do sócio pelo trabalho que ele exerce na empresa, com valor e data definidos.", ""),
    ("Recuperação judicial", "Processo legal que permite a uma empresa em crise renegociar suas dívidas com os credores, sob supervisão da Justiça, para evitar a falência.", ""),
    ("Regime de caixa e de competência", "No regime de caixa, receitas e despesas contam na data em que o dinheiro entra ou sai. No de competência, contam na data em que a venda ou o gasto aconteceu.", ""),
    ("Reserva de emergência", "Dinheiro guardado em aplicação segura e de resgate rápido para cobrir imprevistos e perda de renda. Recomenda-se de 3 a 12 meses de gastos essenciais.", ""),
    ("Rotativo do cartão", "Crédito automático usado quando se paga menos que o total da fatura. Está entre as linhas de crédito mais caras do país.", ""),
    ("Selic", "Taxa básica de juros da economia brasileira, definida pelo Copom do Banco Central. Influencia todos os juros do país.", ""),
    ("Simples Nacional", "Regime tributário simplificado para micro e pequenas empresas, que reúne vários impostos em uma única guia.", ""),
    ("Ticket médio", "Valor médio de cada venda: faturamento dividido pelo número de vendas.", ""),
]


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(c if c.isalnum() else '-' for c in s).strip('-').replace('--', '-')


def main():
    terms = sorted(TERMS, key=lambda t: slug(t[0]))
    letters = sorted({slug(t[0])[0].upper() for t in terms})
    blocks, cur = [], None
    for name, defi, ex in terms:
        L = slug(name)[0].upper()
        anchor = f' id="letra-{L}"' if L != cur else ''
        cur = L
        exh = f'<p class="ex"><b>Exemplo:</b> {ex}</p>' if ex else ''
        blocks.append(f'<div class="term"{anchor} data-term="{name.lower()} {defi.lower()}"><h3 id="{slug(name)}">{name}</h3><p>{defi}</p>{exh}</div>')
    schema = {'@context': 'https://schema.org', '@type': 'DefinedTermSet', 'name': 'Glossário financeiro BRK',
              'hasDefinedTerm': [{'@type': 'DefinedTerm', 'name': n, 'description': d} for n, d, _ in terms]}
    meta = {'url': 'aprenda/glossario.html', 'nav': 'aprenda/', 'title': 'Glossário Financeiro: Termos de Finanças Explicados | BRK',
            'description': f'Glossário com {len(terms)} termos de finanças pessoais e empresariais explicados em linguagem simples: DRE, EBITDA, capital de giro, margem, Selic, MEI e mais.',
            'priority': '0.7', 'scripts': ['glossary'],
            'breadcrumb': [['Início', ''], ['Aprenda', 'aprenda/'], ['Glossário', 'aprenda/glossario.html']]}
    letter_links = ''.join(f'<a href="#letra-{L}">{L}</a>' for L in letters)
    html = f'''<!--meta
{json.dumps(meta, ensure_ascii=False, indent=1)}
-->
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
<div class="container">
  <section class="page-hero">
    <ol class="breadcrumb"><li><a href="{{{{P}}}}index.html">Início</a></li><li><a href="{{{{P}}}}aprenda/">Aprenda</a></li><li>Glossário</li></ol>
    <span class="eyebrow">Aprenda · {len(terms)} termos</span>
    <h1>Glossário financeiro</h1>
    <p class="lead">Os termos de finanças pessoais, finanças corporativas e governança que mais aparecem no dia a dia — explicados sem complicação.</p>
  </section>
</div>
<section class="section" style="padding-top:30px">
  <div class="container narrow">
    <div class="gloss-search"><div class="field"><label for="busca">Buscar termo</label><input type="search" id="busca" placeholder="Ex.: capital de giro, EBITDA, Selic…" autocomplete="off"></div></div>
    <nav class="letters" aria-label="Letras">{letter_links}</nav>
    <div id="terms">
{chr(10).join(blocks)}
    </div>
    <p id="noterm" style="display:none;color:var(--text-muted);padding:20px 0">Nenhum termo encontrado. <a href="{{{{WA}}}}" target="_blank" rel="noopener">Pergunte pelo WhatsApp →</a></p>
  </div>
</section>
'''
    (Path(__file__).resolve().parent / 'pages' / 'aprenda-glossario.html').write_text(html, encoding='utf-8')
    print('glossário:', len(terms), 'termos')


if __name__ == '__main__':
    main()
