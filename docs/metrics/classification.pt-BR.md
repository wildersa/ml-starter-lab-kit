# Métricas de classificação

Use métricas de classificação quando o modelo prevê uma categoria (classe).

Para um mergulho profundo em como medir o desempenho do modelo e como isso se relaciona com o valor de negócio, consulte o guia de [Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.pt-BR.md).

## Matriz de Confusão (Confusion Matrix)

- **O que responde:** Quantos itens foram classificados corretamente e que tipo de erros (Falsos Positivos ou Falsos Negativos) o modelo está cometendo.
- **Quando usar:** Sempre. É a base para todas as outras métricas de classificação.
- **Quando evitar:** Nunca, embora para muitas classes (ex: >20), possa se tornar difícil de ler.
- **Armadilha comum:** Ignorar a diagonal. Se a diagonal estiver fraca, seu modelo está essencialmente chutando.
- **Exemplo:** Em um filtro de spam, mostra 80 spams reais capturados, 5 spams reais perdidos e 2 e-mails normais bloqueados erroneamente.

## Acurácia (Accuracy)

- **O que responde:** Qual porcentagem do total de previsões estava correta?
- **Quando usar:** Quando suas classes estão balanceadas (ex: 50% spam, 50% não spam).
- **Quando evitar:** Quando uma classe é muito mais frequente que as outras (dados desbalanceados).
- **Armadilha comum:** Um modelo que sempre prevê "Não é Fraude" em um dataset com 99% de transações legítimas terá 99% de acurácia, mas é inútil.
- **Exemplo:** Um classificador de gato vs cachorro acerta 90 de 100 imagens. Acurácia = 90%.

## Precisão (Precision)

- **O que responde:** De todos os itens que o modelo rotulou como "Positivo", quantos estavam realmente corretos?
- **Quando usar:** Quando o **custo do Falso Positivo** é alto (ex: bloquear a conta de um usuário legítimo).
- **Quando evitar:** Quando perder casos positivos é mais perigoso do que errar sobre um.
- **Armadilha comum:** Ter 100% de precisão prevendo "Positivo" apenas para o único caso mais óbvio, enquanto ignora 99 outros.
- **Exemplo:** Um recomendador de "Investimento Seguro". Você só quer que ele diga "Sim" quando for extremamente provável que seja verdade.

## Recall (Revocação)

- **O que responde:** De todos os itens "Positivos" reais que existem, quantos o modelo encontrou?
- **Quando usar:** Quando o **custo do Falso Negativo** é alto (ex: perder um diagnóstico de câncer).
- **Quando evitar:** Quando o custo de um alarme falso é alto demais.
- **Armadilha comum:** Obter 100% de recall simplesmente rotulando tudo como "Positivo".
- **Exemplo:** Um alarme de segurança. Você quer que ele toque para *cada* invasão, mesmo que ocasionalmente dispare por causa de um gato.

## F1-Score

- **O que responde:** Qual é o equilíbrio harmônico entre Precisão e Recall?
- **Quando usar:** Quando você quer um único número para comparar modelos e tanto a Precisão quanto o Recall são importantes.
- **Quando evitar:** Quando os requisitos de negócio favorecem explicitamente um em detrimento do outro (ex: um sistema de "Segurança em Primeiro Lugar" favorece o Recall).
- **Armadilha comum:** Usá-lo quando as classes estão muito desbalanceadas sem verificar a Precisão/Recall individuais.
- **Exemplo:** Um classificador de intenção de chatbot onde você quer ser tanto preciso quanto abrangente.

## ROC-AUC e PR-AUC

- **O que responde:** Quão bom é o modelo em ordenar itens por probabilidade, independentemente do **Threshold** (limiar) escolhido?
- **Quando usar:** Para avaliar o "poder" geral do modelo antes de escolher um corte específico. Use PR-AUC para datasets altamente desbalanceados.
- **Quando evitar:** Quando você precisa saber o desempenho real em um ponto operacional específico.
- **Armadilha comum:** Um AUC alto não significa que o modelo está pronto para produção; você ainda precisa escolher um bom threshold.
- **Exemplo:** Comparar dois algoritmos de detecção de fraude para ver qual deles "separa" melhor os fraudadores dos clientes.

## Thresholds (Limiares)

- **O que responde:** Em qual probabilidade devo mudar de "Não" para "Sim"?
- **Quando usar:** Sempre que seu modelo gerar probabilidades (0.0 a 1.0).
- **Quando evitar:** Nunca. Escolher um threshold é uma decisão de negócio.
- **Armadilha comum:** Usar o padrão 0.5 para tudo. Se os Falsos Negativos forem caros, você deve baixar o threshold.
- **Exemplo:** Baixar o threshold para 0.2 para capturar mais fraudes potenciais, mesmo que isso aumente os alarmes falsos.
