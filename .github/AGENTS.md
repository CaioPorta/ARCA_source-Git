## Fluxo de desenvolvimento dos testes (regras fixas)

**Esconder os detalhes de UI/da camada de teste.** Interações de UI/clique (`qtbot.mouseClick`, `_show_click`, etc.) ficam em funções auxiliar em `tests/libs/ui_helpers.py`. A camada de teste chama essas helpers e não executa Qt inline.

**Seguir a convenção existente ao adicionar helpers.** Nomear no padrão dos já existentes, por exemplo `go_<nome>_page`, mantendo a estrutura (assertiva de botão presente, clique, assertiva do `PageID`).

Evitar de fazer assert na tests\libs\ui_helpers.py

Evitar de usar PAGE_BY_NAME nos tests. Usar apenas no helper, se realmente necessario.

Commentar a acao e resultado esperado antes das principais acoes de teste.

Manter o mesmo padrao entre os diferentes testes.

This file has the mapping of the pages ID and Names: src\app\ui\pages.py

Prefira usar qtbot.mouseClick. Não use pressed.emit.
