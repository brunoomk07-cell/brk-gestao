#!/usr/bin/env python3
"""Gera os artigos do blog (_src/blog/*.html) no formato: dor → sinais → consequências → dicas rápidas → solução BRK.
A ideia é ajudar o leitor a enxergar o problema e dar algumas dicas, sem entregar o método."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'blog'
SERV = {
    'pj': ('consultoria-financeira-empresas.html', 'Consultoria financeira para empresas'),
    'pf': ('consultoria-financeira-pessoal.html', 'Consultoria financeira pessoal'),
    'mei': ('consultoria-financeira-mei.html', 'Consultoria financeira para MEI'),
}

POSTS = [
    dict(slug='fluxo-de-caixa-pequena-empresa', order=1, tag='Empresas', serv='pj',
         h1='Empresa vende, mas falta dinheiro no caixa? Os sinais de alerta',
         title='Empresa Vende mas Falta Dinheiro no Caixa? 6 Sinais de Alerta | BRK',
         desc='Sua empresa vende bem, mas o dinheiro nunca sobra? Veja os 6 sinais de que o caixa está em risco, o que acontece se nada mudar e como resolver.',
         excerpt='Vender bem e não ter dinheiro para pagar as contas é mais comum do que parece. Veja os sinais de que o caixa da sua empresa está em risco.',
         read=5, wa='Olá! Li o artigo sobre caixa no site da BRK. Minha empresa vende, mas falta dinheiro.',
         hook='<p>Existe uma frase que todo empresário deveria conhecer: <strong>empresa não quebra por falta de lucro, quebra por falta de caixa</strong>. Dá para ter lucro no papel e, mesmo assim, não ter dinheiro para pagar a folha na sexta-feira.</p><p>Hoje, mais de 9 milhões de empresas estão com dívidas em atraso no Brasil, segundo a Serasa Experian — e três quartos dessas dívidas são com fornecedores e contas do dia a dia, não com bancos. É o retrato de negócios que perderam o controle do caixa.</p>',
         signals=['Você só descobre que vai faltar dinheiro quando o boleto já venceu.', 'O saldo do banco é o único "relatório" que você olha.', 'Cheque especial e antecipação de recebíveis viraram rotina.', 'As vendas crescem, mas o aperto também.', 'Você adia pagamentos a fornecedores para fechar o mês.', 'Não sabe dizer quanto terá em caixa daqui a 30 dias.'],
         cons='<p>Sem previsão de caixa, as decisões viram reação: empréstimo às pressas, desconto para vender rápido, fornecedor pago com atraso. Cada uma dessas saídas tem um custo — e ele vai se acumulando até consumir o lucro. É assim que empresas rentáveis entram em crise.</p>',
         tips=['<strong>Tenha uma conta bancária só da empresa.</strong> Sem isso, nenhum controle funciona.', '<strong>Lance as vendas no cartão na data em que o dinheiro cai</strong>, e não na data da venda.', '<strong>Não confie no saldo de hoje:</strong> ele não diz nada sobre os boletos da semana que vem.'],
         hard='<p>Montar uma projeção de caixa confiável exige separar o que é da empresa e o que é dos sócios, entender os prazos reais de recebimento e pagamento e revisar tudo com disciplina. Sozinho, no meio da rotina, quase ninguém consegue.</p>',
         solve=['Enxergar semanas antes quando o caixa vai apertar', 'Parar de pagar juros para fechar o mês', 'Negociar com fornecedores com calma, e não no desespero', 'Uma rotina simples que sua equipe consegue manter'],
         faq=[['Qual a diferença entre lucro e caixa?', 'O lucro mostra se a operação é saudável. O caixa mostra se existe dinheiro na conta na data em que as contas vencem. Uma empresa pode ter lucro e ficar sem caixa — por exemplo, quando vende a prazo e paga à vista.']]),

    dict(slug='separar-financas-pessoais-e-da-empresa', order=2, tag='Empresas', serv='pj',
         h1='Misturar as contas da empresa e as pessoais: o erro que esconde o prejuízo',
         title='Misturar Contas da Empresa e Pessoais Esconde o Prejuízo | BRK',
         desc='Paga contas de casa com o dinheiro da empresa? Entenda por que misturar CPF e CNPJ esconde o prejuízo e trava o crescimento — e como a consultoria resolve.',
         excerpt='Pagar o mercado com o cartão da empresa parece inofensivo. Mas é o erro que mais esconde prejuízo nas pequenas empresas.',
         read=5, wa='Olá! Li o artigo sobre separar as contas no site da BRK e quero organizar isso na minha empresa.',
         hook='<p>Pagar a escola dos filhos com o cartão da empresa. Tirar dinheiro do caixa "só dessa vez". Receber de clientes na conta pessoal. <strong>Misturar o dinheiro do sócio com o do negócio é o erro mais comum das pequenas empresas</strong> — e um dos mais caros.</p><p>O motivo é simples: com as contas misturadas, fica impossível responder à pergunta mais importante de qualquer negócio — <em>a empresa dá lucro ou não?</em></p>',
         signals=['Você não sabe quanto retirou da empresa no último ano.', 'Despesas da casa saem da conta do negócio (ou o contrário).', 'Não existe um valor fixo de retirada.', 'Você acha que a empresa dá lucro, mas o dinheiro nunca sobra.', 'O contador vive pedindo para "separar as coisas".'],
         cons='<p>Uma empresa que dá R$ 5 mil de lucro por mês, com um sócio que retira R$ 12 mil, perde R$ 7 mil de caixa todo mês — e o dono não entende por que precisa de empréstimo. Sem separação, o problema fica invisível até virar dívida.</p>',
         tips=['<strong>Tenha duas contas:</strong> uma da empresa e uma sua. Sem exceção.', '<strong>Retire um valor fixo, na mesma data</strong>, como se fosse um salário.', '<strong>Primeiro o resultado, depois a retirada extra</strong> — nunca o contrário.'],
         hard='<p>O difícil não é abrir outra conta. É descobrir quanto a empresa realmente aguenta pagar de retirada, ajustar a vida pessoal a esse valor e manter a disciplina quando o caixa aperta. É uma decisão financeira e, muitas vezes, familiar.</p>',
         solve=['Saber quanto a empresa realmente lucra', 'Uma retirada fixa e sustentável, sem culpa', 'Regras claras entre os sócios', 'Caixa da empresa protegido das emergências da casa'],
         faq=[['O que é pró-labore?', 'É a remuneração fixa do sócio pelo trabalho na empresa, paga como um salário. A distribuição de lucros é outra coisa e só deve acontecer quando há lucro.']]),

    dict(slug='ponto-de-equilibrio', order=3, tag='Empresas', serv='pj',
         h1='Sua empresa está vendendo o suficiente? O número que quase ninguém sabe',
         title='Quanto Minha Empresa Precisa Vender Para Não Ter Prejuízo? | BRK',
         desc='A maioria dos empresários não sabe quanto precisa vender para não ter prejuízo. Entenda o ponto de equilíbrio, os sinais de risco e calcule o seu grátis.',
         excerpt='Se você não sabe quanto precisa vender por mês para não ter prejuízo, está dirigindo sem painel. Veja por que esse número importa.',
         read=4, wa='Olá! Li o artigo sobre ponto de equilíbrio no site da BRK e quero entender os números da minha empresa.',
         hook='<p>Se alguém perguntasse agora quanto a sua empresa precisa faturar este mês para não ter prejuízo, você saberia responder? A maioria dos pequenos empresários não sabe — e só descobre que o mês foi ruim quando o dinheiro já acabou.</p><p>Esse número tem nome: <strong>ponto de equilíbrio</strong>. Abaixo dele, cada mês consome caixa. Acima dele, a empresa começa a gerar lucro.</p>',
         signals=['Você nunca calculou quanto precisa vender por mês.', 'Contrata ou aumenta a estrutura sem saber se as vendas aguentam.', 'Dá descontos sem saber quanto sobra de cada venda.', 'Os meses "fracos" sempre terminam no vermelho.', 'Você trabalha cada vez mais e o lucro não acompanha.'],
         cons='<p>Sem conhecer esse número, a empresa toma decisões às cegas: uma contratação que parecia pequena, um aluguel um pouco maior, um desconto para "girar estoque" — e, de repente, o negócio precisa vender muito mais só para empatar.</p>',
         tips=['<strong>Descubra o seu número</strong>: quanto precisa vender por mês só para não ter prejuízo.', '<strong>Transforme em meta diária</strong> e acompanhe todo dia.', '<strong>Antes de aumentar a estrutura</strong>, pergunte quanto a mais você vai precisar vender.'],
         hard='<p>O cálculo em si é simples. O difícil é ter os números certos: separar custos fixos e variáveis, saber a margem real de cada produto e entender o que puxa o ponto de equilíbrio para cima. É aí que a maioria das planilhas erra.</p>',
         solve=['A venda mínima do mês clara para você e sua equipe', 'Margem por produto: o que sustenta e o que só dá trabalho', 'Decisões de estrutura com base em números', 'Um plano para aumentar a folga de segurança'],
         faq=[['O pró-labore entra no cálculo?', 'Sim. A retirada dos sócios sai do caixa todo mês e deve ser considerada como despesa fixa.']]),

    dict(slug='dre-gerencial', order=4, tag='Empresas', serv='pj',
         h1='Sua empresa dá lucro mesmo? Por que o faturamento engana',
         title='Minha Empresa Dá Lucro? Por Que o Faturamento Engana | BRK',
         desc='Faturar bem não significa lucrar. Veja os sinais de que sua empresa pode estar dando prejuízo sem você perceber — e como descobrir o lucro real.',
         excerpt='Faturamento alto não é sinônimo de lucro. Veja os sinais de que a sua empresa pode estar dando prejuízo sem você perceber.',
         read=4, wa='Olá! Li o artigo sobre lucro no site da BRK e quero saber se minha empresa realmente dá lucro.',
         hook='<p>"Faturamos R$ 100 mil este mês." Parece ótimo — até alguém perguntar: <strong>e quanto sobrou?</strong> Depois de mercadoria, impostos, taxas, folha, aluguel e retiradas, o que sobra pode ser pouco. Ou negativo.</p><p>Confundir faturamento com lucro é o primeiro passo para decisões erradas: gastar o que não existe, retirar o que a empresa não gerou e crescer no prejuízo.</p>',
         signals=['Você sabe o faturamento, mas não o lucro do mês.', 'O contador entrega relatórios que ninguém lê.', 'Vende cada vez mais e o dinheiro não aparece.', 'Não sabe quais produtos ou serviços dão mais resultado.', 'Juros e tarifas bancárias pesam cada vez mais.'],
         cons='<p>Sem saber o lucro real, a empresa pode passar meses — ou anos — operando no prejuízo, compensado com empréstimos, atrasos e o dinheiro pessoal dos sócios. Quando a conta chega, já é uma crise.</p>',
         tips=['<strong>Separe o que é da empresa e o que é dos sócios</strong> antes de qualquer análise.', '<strong>Olhe o resultado todo mês</strong>, não só no fim do ano.', '<strong>Compare mês a mês:</strong> a tendência diz mais do que o número isolado.'],
         hard='<p>Montar uma visão confiável do resultado exige classificar corretamente cada gasto, separar competência de caixa e interpretar os números para decidir. Se você não tem essa visão hoje, a gente monta com você.</p>',
         solve=['Um relatório mensal simples, que você entende', 'O lucro real da empresa, sem ilusão', 'Os vazamentos identificados e corrigidos', 'Uma reunião mensal de resultados que funciona'],
         faq=[['Isso é diferente do que o contador faz?', 'Sim. A contabilidade cuida das obrigações fiscais. A gestão financeira usa os números para decidir. As duas se complementam, e trabalhamos junto com o seu contador.']]),

    dict(slug='capital-de-giro', order=5, tag='Empresas', serv='pj',
         h1='Falta de capital de giro: por que falta dinheiro mesmo vendendo bem',
         title='Falta de Capital de Giro: Por Que Falta Dinheiro Vendendo Bem | BRK',
         desc='Sua empresa cresce, mas o caixa aperta cada vez mais? Entenda a falta de capital de giro, os sinais de alerta e como a consultoria resolve.',
         excerpt='Vender mais e ter menos dinheiro no caixa. Parece contraditório, mas é o sintoma clássico da falta de capital de giro.',
         read=4, wa='Olá! Li o artigo sobre capital de giro no site da BRK. Minha empresa cresce, mas falta caixa.',
         hook='<p>Mais de três quartos das dívidas em atraso das empresas brasileiras são com fornecedores, prestadores de serviço e contas do dia a dia, segundo a Serasa Experian. Esse é o retrato típico da <strong>falta de capital de giro</strong>: a empresa vende, mas o dinheiro não chega a tempo de pagar as contas.</p>',
         signals=['Você paga fornecedores antes de receber dos clientes.', 'Quanto mais vende a prazo, mais o caixa aperta.', 'Estoque parado ocupa espaço e dinheiro.', 'Antecipação de recebíveis virou rotina.', 'Crescer parece sempre "sufocar" a empresa.'],
         cons='<p>Sem capital de giro, cada venda a prazo precisa ser financiada com dinheiro caro. Os juros comem o lucro, e o crescimento — que deveria ser uma boa notícia — vira o motivo da crise. Muitas empresas quebram justamente quando estão vendendo mais.</p>',
         tips=['<strong>Compare os prazos:</strong> em quantos dias você paga e em quantos recebe?', '<strong>Olhe o estoque parado</strong> como dinheiro parado.', '<strong>Contas a receber em atraso</strong> são capital de giro perdido.'],
         hard='<p>Calcular a necessidade real de capital de giro e reduzi-la envolve prazos, estoque, crédito, preço e negociação — tudo ao mesmo tempo. Cada ajuste mexe nos outros. É um trabalho de estratégia, não de planilha.</p>',
         solve=['Quanto capital de giro sua empresa realmente precisa', 'Menos dependência de crédito caro', 'Crescimento planejado, sem sufocar o caixa', 'Prazos e estoque ajustados à sua realidade'],
         faq=[['Empréstimo para capital de giro resolve?', 'Pode ajudar quando a necessidade é pontual e planejada. Usar empréstimo todo mês para fechar o caixa indica um problema estrutural que precisa ser resolvido na operação.']]),

    dict(slug='indicadores-financeiros-essenciais', order=6, tag='Empresas', serv='pj',
         h1='Você decide no escuro? Os números que todo empresário deveria enxergar',
         title='Indicadores Financeiros: Os Números que Todo Empresário Deve Ver | BRK',
         desc='Decidir sem números custa caro. Conheça os indicadores financeiros que todo pequeno empresário deveria acompanhar e os riscos de não olhar para eles.',
         excerpt='Dirigir uma empresa sem indicadores é como dirigir um carro sem painel. Veja quais números você não pode ignorar.',
         read=4, wa='Olá! Li o artigo sobre indicadores no site da BRK e quero um painel de números para minha empresa.',
         hook='<p>Dirigir uma empresa sem indicadores é como dirigir um carro sem painel: você só descobre que o combustível acabou quando o motor para. A maioria das pequenas empresas decide preço, contratação e investimento na base da sensação — e paga caro por isso.</p>',
         signals=['Você não sabe a margem de lucro da empresa.', 'Não sabe quantos dias leva para receber dos clientes.', 'Decide preços "olhando o concorrente".', 'Não tem uma reunião mensal para olhar os números.', 'Descobre os problemas só quando eles viram crise.'],
         cons='<p>Sem indicadores, os problemas aparecem tarde: a margem vai caindo aos poucos, o prazo de recebimento vai esticando, o endividamento vai subindo. Quando tudo isso chega ao caixa, as opções já são poucas — e caras.</p>',
         tips=['<strong>Margem de contribuição:</strong> quanto sobra de cada venda.', '<strong>Ponto de equilíbrio:</strong> a venda mínima do mês.', '<strong>Ciclo financeiro:</strong> quantos dias a empresa financia a própria operação.', '<strong>Endividamento:</strong> quanto das vendas já está comprometido com dívidas.'],
         hard='<p>Saber o nome dos indicadores é fácil. Difícil é ter dados confiáveis para calculá-los, interpretar o que cada número está dizendo sobre o seu negócio e transformar isso em decisão. Um indicador errado leva a uma decisão errada.</p>',
         solve=['Um painel com os números certos para o seu negócio', 'Alertas antes de o problema chegar ao caixa', 'Reunião mensal de resultados com decisões registradas', 'Metas claras para você e sua equipe'],
         faq=[['Preciso de um sistema caro?', 'Não. Com dados organizados e uma rotina simples já é possível acompanhar os principais indicadores. O que importa é a qualidade da informação e a disciplina de olhar para ela.']]),

    dict(slug='governanca-corporativa-pequenas-empresas', order=7, tag='Governança', serv='pj',
         h1='Conflitos entre sócios e família: quando a empresa precisa de governança',
         title='Governança em Empresa Familiar: Conflitos entre Sócios | BRK',
         desc='Discussões entre sócios, parentes sem função definida e decisões no corredor? Veja os sinais de que sua empresa familiar precisa de governança.',
         excerpt='Governança não é coisa de multinacional. É o que evita que conflitos entre sócios e família destruam o negócio.',
         read=5, wa='Olá! Li o artigo sobre governança no site da BRK e quero organizar a gestão da minha empresa familiar.',
         hook='<p>Sócios que discordam sobre retiradas. Parentes que trabalham sem função definida. Decisões importantes tomadas no corredor. Dinheiro da empresa pagando contas da família. <strong>Esses problemas aparecem com força nas pequenas empresas — e principalmente nas familiares.</strong></p><p>Governança é o conjunto de regras que define como a empresa é dirigida, como as decisões são tomadas e como o dinheiro circula. E ela pode, e deve, ser do tamanho do seu negócio.</p>',
         signals=['Os sócios não sabem quanto cada um retirou no ano.', 'Decisões importantes são tomadas sem números.', 'Familiares ocupam cargos sem função ou metas.', 'Ninguém sabe o que acontece se um sócio quiser sair.', 'As mesmas discussões se repetem todo mês.'],
         cons='<p>Sem regras claras, os conflitos crescem, as decisões travam e o caixa vira campo de disputa. Em empresas familiares, o problema ainda atravessa a mesa do jantar. Muitas empresas saudáveis se perdem na sucessão ou na briga entre sócios.</p>',
         tips=['<strong>Separe os papéis:</strong> ser da família, ser sócio e trabalhar na empresa são coisas diferentes.', '<strong>Defina quem aprova o quê</strong>, e até que valor.', '<strong>Registre as decisões importantes</strong> — nem que seja em uma página.'],
         hard='<p>Governança mexe com poder, dinheiro e relações pessoais. Por isso, quase sempre funciona melhor com alguém de fora, neutro, conduzindo a conversa e estruturando as regras junto com os números.</p>',
         solve=['Papéis e responsabilidades claros para sócios e família', 'Regras de retirada e distribuição de lucros', 'Reunião mensal de resultados com pauta e registro', 'Menos conflito e decisões mais rápidas'],
         faq=[['Empresa pequena precisa de governança?', 'Precisa de governança proporcional ao seu tamanho: regras simples sobre quem decide o quê, como o dinheiro sai da empresa e como os resultados são acompanhados.']]),

    dict(slug='financas-do-mei', order=8, tag='MEI', serv='mei',
         h1='MEI: as armadilhas financeiras que travam o crescimento',
         title='MEI: 5 Armadilhas Financeiras que Travam o Crescimento (2026) | BRK',
         desc='Limite de R$ 81 mil, contas misturadas, preço errado: veja as armadilhas financeiras mais comuns do MEI em 2026 e como evitá-las.',
         excerpt='Ser MEI é simples — e é aí que mora o perigo. Veja as armadilhas que fazem muita gente trabalhar anos sem saber se está ganhando.',
         read=5, wa='Olá! Li o artigo sobre MEI no site da BRK e quero organizar as finanças do meu negócio.',
         hook='<p>Ser MEI é a porta de entrada do empreendedorismo para milhões de brasileiros: pouca burocracia, imposto fixo e baixo custo. Mas essa simplicidade tem um lado perigoso: como tudo é "fácil", muita gente nunca organiza o dinheiro do negócio — e trabalha anos sem saber se está realmente ganhando.</p><p>Em 2026, o limite de faturamento continua em <strong>R$ 81 mil por ano</strong> (média de R$ 6.750 por mês), e o DAS mensal da maioria das atividades fica entre R$ 82 e R$ 87.</p>',
         signals=['O dinheiro das vendas paga as contas de casa.', 'Você não sabe quanto realmente ganha por mês.', 'O preço foi copiado do concorrente.', 'Não acompanha o faturamento acumulado do ano.', 'Não tem nenhuma reserva para os meses fracos.'],
         cons='<p>Sem controle, o MEI trabalha muito e ganha pouco — e ainda corre o risco de estourar o limite sem perceber. Se passar de R$ 97,2 mil (20% acima do teto), o desenquadramento retroage a janeiro, com impostos de microempresa sobre o ano inteiro.</p>',
         tips=['<strong>Separe uma conta só para o negócio</strong>, mesmo que seja uma conta pessoal usada exclusivamente para isso.', '<strong>Some o faturamento do ano todo mês</strong>.', '<strong>Defina um "salário" fixo</strong> para você.'],
         hard='<p>O MEI faz tudo sozinho: vende, entrega, cobra e cuida do dinheiro. Encaixar gestão financeira nessa rotina — e definir preço, retirada e o momento certo de crescer — é onde quase todos travam.</p>',
         solve=['Saber exatamente quanto o seu negócio lucra', 'Preço certo para parar de trabalhar de graça', 'Controle do limite e transição planejada', 'Uma rotina simples, que cabe no seu dia'],
         faq=[['O limite do MEI aumentou em 2026?', 'Não. O limite continua em R$ 81 mil por ano. Existem projetos no Congresso para aumentá-lo, mas nenhum havia sido aprovado até a publicação deste artigo.']]),

    dict(slug='como-sair-das-dividas', order=9, tag='Finanças pessoais', serv='pf',
         h1='Endividado? Por que a dívida não diminui (e o que fazer primeiro)',
         title='Endividado? Por Que a Dívida Não Diminui e o Que Fazer | BRK',
         desc='Paga todo mês e a dívida não diminui? Entenda por que isso acontece, os sinais de alerta e os primeiros passos para sair das dívidas com ajuda profissional.',
         excerpt='Você paga, paga, e a dívida continua do mesmo tamanho. Entenda por que isso acontece e qual é o primeiro passo para sair.',
         read=5, wa='Olá! Li o artigo sobre dívidas no site da BRK e preciso de ajuda para sair das dívidas.',
         hook='<p>Quase 84 milhões de brasileiros estão com o nome negativado, segundo a Serasa. E um dado assusta ainda mais: <strong>42% de quem está inadimplente hoje também estava há dez anos</strong>. Muita gente consegue "limpar o nome" — e volta para o mesmo lugar.</p><p>Isso acontece porque sair das dívidas tem duas partes: resolver a dívida e resolver o que criou a dívida. A maioria só tenta a primeira.</p>',
         signals=['Você paga todo mês e o saldo não cai.', 'Não sabe exatamente quanto deve, nem a quem.', 'Usa um crédito para pagar outro.', 'Já renegociou e voltou a atrasar.', 'Evita atender ligações de cobrança.'],
         cons='<p>Quando os juros do mês são maiores que a parcela, a dívida cresce mesmo com você pagando em dia. O estresse aumenta, o crédito fica mais caro e as opções ficam piores. Sem um plano, o ciclo se repete.</p>',
         tips=['<strong>Coloque todas as dívidas no papel</strong>, com saldo, parcela e juros.', '<strong>Proteja o essencial primeiro:</strong> moradia, comida, contas básicas.', '<strong>Não aceite uma renegociação que não cabe no bolso</strong> só para se livrar da ligação.'],
         hard='<p>Escolher a ordem certa de pagamento, negociar com estratégia, trocar dívidas caras por mais baratas e, principalmente, mudar os hábitos que criaram a dívida — tudo isso ao mesmo tempo, com a pressão das cobranças. É muito difícil fazer sozinho. O primeiro passo é ver o tamanho real do problema — e a gente faz isso com você.</p>',
         solve=['Todas as dívidas organizadas e com data para acabar', 'Um plano que cabe no seu orçamento real', 'Orientação para negociar com bancos e credores', 'Acompanhamento para você não voltar ao mesmo lugar'],
         faq=[['Vale a pena pegar um empréstimo para quitar dívidas?', 'Às vezes sim, às vezes não — depende dos juros, do prazo e do seu orçamento. Essa é uma das decisões que analisamos no diagnóstico, com os seus números.']]),

    dict(slug='cartao-de-credito-rotativo', order=10, tag='Finanças pessoais', serv='pf',
         h1='Pagando o mínimo do cartão? Quanto isso realmente custa',
         title='Pagando o Mínimo do Cartão? Quanto o Rotativo Realmente Custa | BRK',
         desc='Pagar o mínimo da fatura parece alívio, mas custa caro. Entenda o rotativo do cartão, o limite legal de juros e os sinais de que você está preso nessa armadilha.',
         excerpt='Pagar o mínimo da fatura dá alívio no mês — e prende você por muitos outros. Veja quanto isso realmente custa.',
         read=4, wa='Olá! Li o artigo sobre o rotativo do cartão no site da BRK e preciso de ajuda com minha fatura.',
         hook='<p>O cartão de crédito aparece em <strong>85% das famílias endividadas</strong> do Brasil, segundo a CNC. O cartão em si não é o problema — ele é prático e seguro. O problema é o rotativo: o crédito automático que entra em ação quando você paga menos que o total da fatura.</p><p>O rotativo está entre os créditos mais caros do país. Desde 2024, a lei limita os juros e encargos a 100% do valor original da dívida — ou seja, você ainda pode pagar o dobro do que comprou.</p>',
         signals=['Você paga o mínimo ou só uma parte da fatura.', 'Parcelou a fatura mais de uma vez.', 'Usa o limite do cartão como extensão do salário.', 'A fatura do mês que vem já está comprometida.', 'Tem mais de um cartão para "rodar" as contas.'],
         cons='<p>A dívida no rotativo cresce mais rápido do que a maioria das pessoas consegue pagar. Somada às novas compras, vira uma bola de neve que consome o salário antes mesmo de ele cair. Cada mês de atraso torna a saída mais cara.</p>',
         tips=['<strong>Pague sempre o total da fatura</strong> quando possível.', '<strong>Enquanto houver saldo no rotativo</strong>, pare de usar o cartão.', '<strong>Confira o CET</strong> (custo efetivo total) na fatura antes de parcelar.'],
         hard='<p>Sair do rotativo quase sempre exige trocar a dívida por uma mais barata, reorganizar o orçamento e mudar a relação com o cartão — sem deixar as outras contas atrasarem. É um plano completo, não uma decisão isolada.</p>',
         solve=['Um caminho para interromper os juros do rotativo', 'Orçamento reorganizado para não voltar ao cartão', 'Orientação na negociação com o banco', 'A tranquilidade de ver a dívida diminuir'],
         faq=[['Existe limite para os juros do rotativo?', 'Sim. Desde janeiro de 2024, pela Lei 14.690/2023, os juros e encargos do rotativo e do parcelamento da fatura não podem ultrapassar 100% do valor original da dívida.']]),

    dict(slug='orcamento-familiar-50-30-20', order=11, tag='Finanças pessoais', serv='pf',
         h1='O salário acaba antes do mês? As causas mais comuns',
         title='Salário Acaba Antes do Mês? As Causas Mais Comuns | BRK',
         desc='O dinheiro some antes do fim do mês? Veja as causas mais comuns, os sinais de alerta no orçamento familiar e como a consultoria pessoal resolve.',
         excerpt='Se o salário some antes do dia 30, o problema raramente é só a renda. Veja as causas mais comuns — e o que elas dizem sobre o seu orçamento.',
         read=4, wa='Olá! Li o artigo sobre orçamento no site da BRK. Meu salário acaba antes do mês e quero ajuda.',
         hook='<p>Hoje, <strong>82% das famílias brasileiras têm algum tipo de dívida</strong>, segundo a CNC, e quase 3 em cada 10 estão com contas em atraso. Na maioria das vezes, o problema não é só quanto se ganha — é para onde o dinheiro vai sem que ninguém perceba.</p>',
         signals=['Você não sabe quanto gastou no mês passado.', 'Delivery, assinaturas e compras pequenas somam muito.', 'Parcelas antigas comprometem o salário novo.', 'Nada é guardado no início do mês.', 'Cada aumento de salário vira aumento de gastos.'],
         cons='<p>Quando o salário acaba antes do mês, o cartão e o cheque especial passam a cobrir a diferença. Os juros entram, a próxima renda já chega comprometida, e o aperto vira rotina — mesmo para quem ganha bem.</p>',
         tips=['<strong>Anote todos os gastos por 30 dias.</strong> Os vazamentos aparecem sozinhos.', '<strong>Revise as assinaturas</strong> e cancele o que não usa.', '<strong>Compare o que sai com o que entra</strong> e veja quais categorias pesam mais.'],
         hard='<p>Cortar gastos no impulso dura pouco. O que funciona é um orçamento feito para a sua realidade, combinado com a família e acompanhado de perto nos primeiros meses — até virar hábito.</p>',
         solve=['Saber exatamente para onde vai o seu dinheiro', 'Um orçamento realista, combinado em casa', 'Sobra no fim do mês para reserva e objetivos', 'Menos dependência de cartão e cheque especial'],
         faq=[['Preciso ganhar mais para sair do aperto?', 'Nem sempre. Na maioria dos diagnósticos, encontramos dinheiro vazando em gastos pequenos, juros e parcelas. Organizar isso costuma liberar uma boa parte da renda.']]),

    dict(slug='reserva-de-emergencia', order=12, tag='Finanças pessoais', serv='pf',
         h1='Sem reserva de emergência: o risco que transforma imprevisto em dívida',
         title='Sem Reserva de Emergência? O Risco que Vira Dívida | BRK',
         desc='Sem reserva, todo imprevisto vira dívida cara. Entenda o risco de viver sem proteção financeira e descubra quanto você precisa com a nossa calculadora grátis.',
         excerpt='O carro quebra, a renda cai, alguém adoece. Sem reserva, cada imprevisto vira dívida. Veja o tamanho do seu risco.',
         read=4, wa='Olá! Li o artigo sobre reserva de emergência no site da BRK e quero montar a minha.',
         hook='<p>O carro quebra. O celular cai na água. Alguém da família precisa de um remédio caro. A empresa corta vagas. Imprevistos acontecem com todo mundo — a diferença é que, para quem tem reserva, eles são um susto. <strong>Para quem não tem, viram dívida.</strong></p>',
         signals=['Você não aguentaria um mês sem renda.', 'O último imprevisto foi parar no cartão.', 'Nunca sobra para guardar.', 'A "reserva" fica na conta corrente e se mistura com o dia a dia.', 'Sua renda é variável e você não tem colchão.'],
         cons='<p>Sem proteção, cada imprevisto empurra a família para o crédito caro — e um mês ruim desorganiza os seguintes. Para autônomos e MEIs, com renda variável, o risco é ainda maior.</p>',
         tips=['<strong>Descubra quanto você precisa</strong> para atravessar um imprevisto.', '<strong>Guarde no início do mês</strong>, não com o que sobra.', '<strong>Mantenha a reserva separada</strong> do dinheiro do dia a dia.'],
         hard='<p>Para a maioria das pessoas, o problema não é saber que precisa guardar — é conseguir. Isso depende de encontrar os vazamentos, reorganizar o orçamento e decidir a ordem certa entre pagar dívidas e proteger a família.</p>',
         solve=['Quanto você precisa de proteção, para a sua realidade', 'De onde vai sair o dinheiro para guardar', 'A ordem certa entre dívidas e reserva', 'Tranquilidade para enfrentar imprevistos'],
         faq=[['Quanto devo ter de reserva?', 'A referência mais comum é de 3 a 6 meses de gastos essenciais, e de 6 a 12 meses para quem tem renda variável. O valor ideal depende da sua situação.']]),
]


def build(p):
    serv_url, serv_name = SERV[p['serv']]
    meta = {'url': f"blog/{p['slug']}.html", 'order': p['order'], 'tag': p['tag'], 'h1': p['h1'], 'excerpt': p['excerpt'],
            'title': p['title'], 'description': p['desc'], 'date': '2026-09-28', 'wa_text': p['wa'],
            'breadcrumb': [['Início', ''], ['Blog', 'blog/'], [p['h1'], f"blog/{p['slug']}.html"]], 'faq': p['faq']}
    sig = ''.join(f'<li>{s}</li>' for s in p['signals'])
    tips = ''.join(f'<li>{t}</li>' for t in p['tips'])
    sol = ''.join(f'<li><i>✓</i><div><b>{s}</b></div></li>' for s in p['solve'])
    return f'''<!--meta
{json.dumps(meta, ensure_ascii=False, indent=1)}
-->
<div class="container">
  <section class="page-hero">
    <ol class="breadcrumb"><li><a href="{{{{P}}}}index.html">Início</a></li><li><a href="{{{{P}}}}blog/">Blog</a></li><li>{p['tag']}</li></ol>
    <span class="eyebrow">{p['tag']}</span>
    <h1>{p['h1']}</h1>
    <p class="meta"><span>BRK Consultoria Financeira</span><span>Leitura de {p['read']} minutos</span></p>
  </section>
</div>

<section class="section" style="padding-top:44px">
  <article class="container">
    <div class="prose">
      {p['hook']}
      <h2>Sinais de alerta</h2>
      <ul class="risk-list" style="margin:0">{sig}</ul>
      <h2>O que acontece se nada mudar</h2>
      {p['cons']}
      <h2>Dicas rápidas</h2>
      <ul>{tips}</ul>
      <h2>Por que é tão difícil resolver sozinho</h2>
      {p['hard']}
      <div class="tool-cta">
        <b>Como a BRK resolve</b>
        <p>Na <a href="{{{{P}}}}{serv_url}">{serv_name.lower()}</a>, entramos na sua realidade, encontramos a raiz do problema e construímos a solução junto com você. O resultado:</p>
        <ul class="outcomes" style="border:none;background:none;padding:0 0 10px">{sol}</ul>
        <div class="btn-row">
          <a href="{{{{WA_CTX}}}}" class="btn btn-solid" target="_blank" rel="noopener">{{{{WA_ICON}}}} Falar com um consultor</a>
          <a href="{{{{P}}}}contato.html" class="btn">Agendar diagnóstico gratuito</a>
        </div>
      </div>
      <h2>Perguntas frequentes</h2>
<!--FAQ-->
      <p class="sources">Fontes: Serasa, Serasa Experian, CNC (Peic), IBGE e Receita Federal, conforme citados no texto. Conteúdo informativo; cada situação exige análise individual.</p>
    </div>
  </article>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Continue lendo</span><h2 class="section-title">Outros sinais de alerta</h2></div>
    <div class="grid grid-3">
<!--POSTS_RELATED-->
    </div>
  </div>
</section>
'''


if __name__ == '__main__':
    for f in OUT.glob('*.html'):
        f.unlink()
    for p in POSTS:
        (OUT / f"{p['slug']}.html").write_text(build(p), encoding='utf-8')
    print('artigos:', len(POSTS))
