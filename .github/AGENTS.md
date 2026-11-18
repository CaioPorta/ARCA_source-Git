## Fluxo de desenvolvimento (regras fixas)

**Esconder os detalhes de UI/da camada de teste.** Interações de UI/clique (`qtbot.mouseClick`, `_show_click`, etc.) ficam em funções auxiliar em `tests/libs/ui_helpers.py`. A camada de teste chama essas helpers e não executa Qt inline.

**Seguir a convenção existente ao adicionar helpers.** Nomear no padrão dos já existentes, por exemplo `go_<nome>_page`, mantendo a estrutura (assertiva de botão presente, clique, assertiva do `PageID`).
