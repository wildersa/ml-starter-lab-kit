# Fluxo de Dados Sintéticos

O Synthetic Data Lab permite gerar datasets controlados e determinísticos para testar seu pipeline ou estudar cenários específicos de ML antes de usar dados reais.

## Passos do fluxo

1.  **Configurar**: Edite `configs/synthetic_data.json` para selecionar um cenário (classificação, regressão, séries temporais, etc.) e seus parâmetros.
2.  **Gerar**: Execute o comando synthetic:
    ```bash
    python -m <package>.lab synthetic
    ```
3.  **Inspecionar**: Verifique em `data/synthetic/` o CSV e os metadados, e revise o relatório em `reports/synthetic-data-summary.md`.
4.  **Conectar**:
    - **Automático**: Se `activate_as_project_dataset` for `true` na config, o arquivo `configs/config.json` principal do projeto é atualizado automaticamente.
    - **Manual**: Atualize `data.raw_path` e `target.column` em `configs/config.json` usando os valores sugeridos na saída do terminal.

## Integração com o Pipeline

Uma vez ativado, o dado sintético flui através dos comandos padrão:

```bash
python -m <package>.lab data      # Prepara o dado bruto sintético
python -m <package>.lab train     # Treina com o dado sintético
python -m <package>.lab evaluate  # Avalia a performance
```

## Quando usar

- **Teste de pipeline**: Garanta que o `data.py` e o `train.py` lidam com o formato de dado esperado.
- **Aprendizado**: Experimente como dados desbalanceados (Classificação) ou ruído (Regressão) afetam as métricas.
- **Exploração MAB**: Use cenários de Bandit para entender exploração/explotação sem riscos reais.

**Nota**: Dados sintéticos são para teste e educação. Eles não refletem a performance no mundo real.
