# Templates comuns

Templates reutilizáveis para módulos opcionais gerados pelo `create_ml_starter.py`.

Eles são intencionalmente leves e evitam dependências externas. A ideia é dar um ponto de partida limpo, não um framework completo.

## Templates

| Template | Módulo gerado | Objetivo |
|---|---|---|
| `eda.py.tpl` | `eda.py` | helpers básicos de inspeção de dados |
| `preprocessing.py.tpl` | `preprocessing.py` | nulos, conversão de tipos, scaling simples |
| `visualization.py.tpl` | `visualization.py` | helpers/placeholder para gráficos, sem dependência de plot por padrão |
| `metrics.py.tpl` | `metrics.py` | métricas simples com biblioteca padrão |
| `optimization.py.tpl` | `optimization.py` | estrutura simples para grid/random search |
| `feature_measurement.py.tpl` | `feature_measurement.py` | comparar impacto de features e documentar decisões de manter/remover |
| `notebook_factory.py.tpl` | `notebook_factory.py` | criação de notebooks `.ipynb` usando JSON |

## Regra de dependências

Mantenha os templates primeiro com biblioteca padrão.

Se um projeto precisar de pandas, scikit-learn, matplotlib, xgboost, TensorFlow, Keras, PyTorch ou outra biblioteca, adicione isso apenas no projeto gerado quando fizer sentido.

## Placeholders

Templates podem usar estes placeholders:

```text
{{PROJECT_NAME}}
{{PACKAGE_NAME}}
{{TASK}}
```
