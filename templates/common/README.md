# Common Generated Modules

The generator can evolve to create optional support modules.

Suggested modules:

| Module | Purpose | Dependency policy |
|---|---|---|
| `eda.py` | dataset summary helpers | standard library first |
| `visualization.py` | chart placeholders/helpers | add matplotlib only if needed |
| `metrics.py` | simple metric wrappers and references | standard library first |
| `optimization.py` | simple grid/random search structure | no optimization library by default |
| `notebook_factory.py` | create starter notebooks | standard library |

The rule is simple: generate structure first, add libraries only when the project actually needs them.
