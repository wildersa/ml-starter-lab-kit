# Multi-Armed Bandits

Bandits são usados quando um sistema precisa escolher entre opções e aprender com feedback.

Eles ajudam a equilibrar:

- exploração: testar opções incertas;
- explotação: usar opções que já funcionam bem.

## Ideia básica

```text
contexto -> escolher braço -> observar recompensa -> atualizar política
```

## Exemplos

- escolher qual oferta mostrar;
- escolher qual banner exibir;
- escolher variações de assunto de e-mail;
- dividir tráfego entre alternativas;
- testar recomendações com exploração controlada.

## Algoritmos comuns

| Algoritmo | Use quando |
|---|---|
| Epsilon-greedy | você quer um baseline muito simples |
| Thompson Sampling | você quer exploração probabilística |
| UCB | você quer exploração baseada em incerteza |
| LinUCB | você quer usar features de contexto |

## Métricas úteis

Veja [métricas de bandits](../metrics/bandits.pt-BR.md).

Métricas comuns:

- recompensa;
- recompensa acumulada;
- regret;
- taxa de exploração;
- taxa de conversão;
- fairness de exposição.

## Diferença para teste A/B

Teste A/B normalmente espera o fim do experimento para escolher um vencedor.

Bandits atualizam decisões durante o experimento.

## Aviso prático

Não otimize só clique se o objetivo real envolve conversão, segurança, suitability ou confiança do usuário.
