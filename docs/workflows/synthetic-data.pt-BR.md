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

## Comparação: Bandit Lab vs. Synthetic Data Lab

É importante distinguir entre estas duas ferramentas educacionais:

| Funcionalidade | Synthetic Data Lab | Multi-Armed Bandit Lab |
|---|---|---|
| **Natureza** | **Dados Logados/Estáticos**: Gera um arquivo CSV de eventos passados (ex: `bank_campaign_bandit`). | **Simulação Ativa**: Um ambiente interativo onde um agente toma decisões e recebe feedback. |
| **Loop de Feedback** | Fixo. Você treina modelos em logs do que já aconteceu. | Dinâmico. A escolha do agente na rodada *N* pode ser avaliada imediatamente. |
| **Uso Principal** | Testar o pipeline `data.py` e `train.py` com logs formatados para Bandit. | Aprender sobre estratégias de exploração/explotação (Epsilon-Greedy, Thompson Sampling). |
| **Artefato** | `data/synthetic/cenario.csv` | Tabelas Markdown e gráficos no Workspace. |

O cenário **`bank_campaign_bandit`** no Synthetic Data Lab funciona como uma ponte: ele fornece as colunas realistas que você veria em um log de Bandit do mundo real, que você pode usar para "aquecer" ou testar suas políticas antes de executar uma simulação completa.

**Nota**: Dados sintéticos são para teste e educação. Eles não refletem a performance no mundo real.
