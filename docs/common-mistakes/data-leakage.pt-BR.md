# Data leakage

Data leakage acontece quando o modelo usa informação que não estaria disponível no momento da previsão.

## Exemplo

Usar `duracao_campanha` para prever se o usuário converteu durante a campanha, quando a duração só é conhecida depois do contato.

## Por que é perigoso

Cria scores que parecem ótimos no treino, mas falham no uso real.

## Checagem rápida

Pergunte:

```text
Eu saberia esse valor antes de fazer a previsão?
```

Se não, remova ou isole a feature.
