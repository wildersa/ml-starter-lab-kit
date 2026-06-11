# Métricas de Visão Computacional

As tarefas de visão (Classificação, Detecção, Segmentação) requerem métricas que levem em conta tanto o "quê" quanto o "onde" em uma imagem.

Para um mergulho profundo em como medir o desempenho do modelo e como isso se relaciona com o valor de negócio, consulte o guia de [Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.pt-BR.md).

## Classificação de Imagem (Acurácia, F1, etc.)

- **O que responde:** O modelo identificou corretamente o objeto principal na imagem?
- **Quando usar:** Quando sua saída é um único rótulo (label) para toda a imagem.
- **Quando evitar:** Quando a imagem contém vários objetos importantes que precisam ser identificados.
- **Armadilha comum:** Ignorar objetos pequenos ou fundos que podem estar confundindo o modelo (ex: um modelo que aprende a identificar "vacas" apenas porque vê "grama verde").
- **Exemplo:** Um modelo rotulando uma imagem como "Gato" com 95% de confiança.

## mAP (mean Average Precision)

- **O que responde:** Na Detecção de Objetos, quão bom o modelo é em encontrar as caixas (boxes) e rotulá-las corretamente?
- **Quando usar:** A métrica padrão para Detecção de Objetos (ex: encontrar carros em uma rua).
- **Quando evitar:** Quando você só se importa se um objeto está presente, não onde ele está localizado.
- **Armadilha comum:** Comparar o mAP entre diferentes limiares de IoU sem especificar qual foi usado (ex: mAP@0.5 vs mAP@0.75).
- **Exemplo:** Um modelo com 0,8 de mAP é geralmente muito bom tanto em localizar quanto em identificar objetos.

## IoU (Intersection over Union)

- **O que responde:** Quanto a caixa/máscara prevista se sobrepõe à caixa/máscara real?
- **Quando usar:** Para medir a precisão da localização em Detecção e Segmentação.
- **Quando evitar:** Como uma métrica isolada para valor de negócio, pois não diz se a classificação estava correta.
- **Armadilha comum:** Definir um limiar de IoU muito rigoroso para o problema (ex: exigir 90% de sobreposição para um objeto muito borrado).
- **Exemplo:** Um IoU de 0,7 significa que 70% da área das duas caixas é compartilhada.

## Dice Score (F1-score para máscaras)

- **O que responde:** Quão semelhante é a forma prevista à forma real na Segmentação de Imagens?
- **Quando usar:** Muito comum em imagens médicas (segmentação de tumores, órgãos).
- **Quando evitar:** Quando você tem muitos objetos pequenos e desconectados.
- **Armadilha comum:** É muito sensível a objetos pequenos; alguns pixels de erro podem mudar drasticamente a pontuação para uma máscara minúscula.
- **Exemplo:** Um Dice score de 0,9 em uma segmentação de pulmão significa que a máscara prevista quase coincide perfeitamente com a realidade.
