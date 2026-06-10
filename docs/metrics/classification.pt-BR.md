# Métricas de Classificação

Use métricas de classificação quando seu modelo prevê uma categoria ou rótulo (ex: "Spam" vs. "Não Spam").

A escolha da métrica correta depende do **custo de estar errado** de diferentes maneiras.

## Matriz de Confusão

Uma tabela que resume o desempenho do modelo comparando os rótulos previstos com os rótulos reais.

- **O que responde**: Onde exatamente meu modelo está se confundindo?
- **Quando usar**: Sempre. É a base para todas as outras métricas de classificação.
- **Exemplo**: Uma tabela mostrando que seu modelo identificou corretamente 90 e-mails como "Spam", mas classificou incorretamente 10 e-mails "Não Spam" como "Spam".

## Acurácia (Accuracy)

- **O que responde**: Qual fração de todas as previsões estava correta?
- **Quando usar**: Quando suas classes têm tamanhos aproximadamente iguais (dataset balanceado).
- **Quando evitar**: Quando uma classe é muito mais frequente que as outras (dataset desbalanceado).
- **Armadilha comum**: Uma acurácia alta em um dataset desbalanceado (ex: 99% de acurácia porque 99% dos dados pertencem a uma classe) pode esconder um modelo que falha completamente na classe minoritária.
- **Exemplo**: Em um dataset com 50% gatos e 50% cachorros, uma acurácia de 0,90 significa que 9 de cada 10 animais foram identificados corretamente.

## Precisão (Precision)

- **O que responde**: De todos os casos previstos como positivos, quantos eram realmente positivos?
- **Quando usar**: Quando o custo de um **Falso Positivo** (FP) é alto.
- **Armadilha comum**: Otimizar apenas para precisão pode levar a perder muitos casos positivos (baixo recall).
- **Exemplo**: Uma pessoa inocente sendo enviada para a prisão. Alta precisão garante que apenas os verdadeiramente culpados sejam condenados.

## Recall (Sensibilidade)

- **O que responde**: De todos os casos positivos reais, quantos o modelo encontrou?
- **Quando usar**: Quando o custo de um **Falso Negativo** (FN) é alto.
- **Armadilha comum**: É fácil obter um recall alto prevendo "Positivo" para tudo, o que arruína a precisão.
- **Exemplo**: Uma pessoa doente sendo informada de que está saudável. Recall alto garante que encontremos o maior número possível de pessoas doentes.

## F1-Score

- **O que responde**: Qual é o equilíbrio harmônico entre Precisão e Recall?
- **Quando usar**: Quando você precisa de um único número para comparar modelos e se preocupa tanto com FP quanto com FN.
- **Armadilha comum**: Trata Precisão e Recall como igualmente importantes, o que pode não ser verdade para o seu caso de negócio específico.
- **Exemplo**: Um F1 de 0,85 sugere um forte equilíbrio entre encontrar todos os positivos e garantir que os encontrados estejam corretos.

## ROC-AUC e PR-AUC

- **O que responde**: Quão bom é o modelo em ranquear itens por probabilidade?
- **Quando usar**: Quando você ainda não decidiu um **Threshold** (limite) final. Use PR-AUC para datasets altamente desbalanceados.
- **Quando evitar**: Quando você precisa saber o desempenho real em um ponto operacional específico.
- **Exemplo**: Um AUC de 0,90 significa que há 90% de chance de o modelo classificar uma instância positiva aleatória acima de uma instância negativa aleatória.

## Entendendo Thresholds (Limites)

Modelos de classificação geralmente retornam uma probabilidade (0.0 a 1.0). O **Threshold** (padrão 0.5) é o ponto de corte onde você decide rotular algo como "Positivo".

- Aumentar o threshold (ex: para 0.8) aumenta a Precisão, mas diminui o Recall.
- Diminuir o threshold (ex: para 0.2) aumenta o Recall, mas diminui a Precisão.

---

### Dica Prática

Sempre verifique o [Checklist Antes da Avaliação](../checklists/before-evaluation.pt-BR.md) para garantir que suas métricas sejam confiáveis e correspondam aos seus objetivos de negócio.
