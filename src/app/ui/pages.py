"""
Central map of every ARCA screen, keyed by its PageID.

Both the app (``from ui.pages import ...``) and the tests (which add ``src/app`` to sys.path) share
this single source of truth, so PageID literals like '0' or '5' are never hardcoded twice.

Usage:
    from ui.pages import PAGES, PAGE_BY_ID, PAGE_BY_NAME

    # Index access, like "page[0] is Home, page[5] is Análise do Mercado":
    PAGES[0].name   # -> 'Home'
    PAGES[5].page_id  # -> '5'

    # Look up by the PageID string the app sets on window.PageID:
    PAGE_BY_ID['5'].name  # -> 'Análise do Mercado'

    # Or by display name:
    PAGE_BY_NAME['Tributacao'].page_id  # -> '51'
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class PageInfo:
    """One screen in the app. ``page_id`` is the exact string HMI sets on ``self.PageID``."""
    page_id: str
    name: str
    description: str = ''
    is_aux: bool = False          # True for sub-pages reached via PageIDAux, not top-level screens.
    parent: Optional[str] = None  # PageID that navigates here (None for root / dialogs).


# Top-level navigation order, by numeric PageID. ``PAGES[0]`` is Home, ``PAGES[5]`` is Análise do Mercado.
PAGES: list[PageInfo] = [
    PageInfo('0', 'Home', "Tela inicial / login ('Entrar')"),
    PageInfo('1', 'MinhaCarteira', "Dashboard logado ('Minha carteira')", parent='0'),
    PageInfo('2', 'AuxilioSenha', "Esqueci a senha ('Auxílio de senha')", parent='0'),
    PageInfo('3', 'ImportarUsuario', "Importar usuário", parent='0'),
    PageInfo('3b', 'ImportacaoUsuario', "Importação de usuário (após importar)", parent='3'),
    PageInfo('4', 'CriarUsuario', "Criar novo usuário", parent='0'),
    PageInfo('5', 'AnaliseMercado', "Análise do Mercado", parent='1'),
    PageInfo('6', 'RecuperacaoEmail', "Recuperação por email ('Confirmação de email')", parent='2'),
    PageInfo('7', 'AlteracaoSenha', "Alteração de senha", parent='6'),
    PageInfo('8', 'ConfirmacaoEmailCriar', "Confirmação de email (criar conta)", parent='4'),
    PageInfo('8b', 'ConfirmacaoEmailImportar', "Confirmação de email (importar usuário)", parent='3b'),
    PageInfo('10', 'EdicaoNegociacoes', "Edição das negociações", parent='1'),
    PageInfo('11', 'ARCA', "Hub ARCA", parent='1'),
    PageInfo('12', 'Desempenho', "Desempenho da Carteira", parent='1'),
    PageInfo('13', 'AnaliseMercadoDup', "Análise do Mercado (página duplicada de '5')", parent='1'),
    PageInfo('18', 'EdicaoNegociacoesBolsa', "Edição das negociações na Bolsa", parent='10'),
    PageInfo('19', 'EdicaoNegociacoesCripto', "Edição das negociações em criptomoedas", parent='10'),
    PageInfo('20', 'AdicionarCorretoraBolsa', "Adicionar nova corretora de bolsa", parent='18'),
    PageInfo('22', 'RenomearCorretoraBolsa', "Renomear corretora da bolsa", parent='18'),
    PageInfo('23', 'RegistrosBolsa', "Registros (Bolsa)", parent='18'),
    PageInfo('24', 'InformarDepositosSaqBolsa', "Informar depósitos e saques na {Corretora}", parent='18'),
    PageInfo('25', 'SaldoContaCorrenteBolsa', "Saldo em conta-corrente na {Corretora}", parent='18'),
    PageInfo('26', 'AdicionarNovoAtivo', "Adicionar novo ativo", parent='18'),
    PageInfo('27', 'RenomearAtivo', "Renomear ativo {Ativo}", parent='18'),
    PageInfo('28', 'InformarNovaOperacaoBolsa', "Informar nova operação na {Corretora}", parent='18'),
    PageInfo('29', 'AlterarOperacoesBolsa', "Alterar operações de {Ativo} na {Corretora}", parent='18'),
    PageInfo('30', 'DeletarOperacoesBolsa', "Deletar operações de {Ativo} na {Corretora}", parent='18'),
    PageInfo('34a', 'CotacaoEncontradaBolsa', "Cotação de {Ativo} encontrada online (auto)", parent='18'),
    PageInfo('34b', 'CotacaoEncontradaManualBolsa', "Cotação de {Ativo} encontrada online (manual)", parent='18'),
    PageInfo('35a', 'CotacaoNaoEncontradaBolsa', "Cotação de {Ativo} não encontrada online (auto)", parent='18'),
    PageInfo('35b', 'CotacaoNaoEncontradaManualBolsa', "Cotação de {Ativo} não encontrada online (manual)", parent='18'),
    PageInfo('36a', 'InformarNovaOperacaoManualBolsa', "Informar nova operação na {Corretora} (manual)", parent='18'),
    PageInfo('36b', 'AlterarNovaOperacaoManualBolsa', "Alterar nova operação na {Corretora} (manual)", parent='18'),
    PageInfo('37', 'AdicionarCorretoraCripto', "Adicionar nova corretora de criptomoedas", parent='19'),
    PageInfo('39', 'RenomearCorretoraCripto', "Renomear corretora de criptomoedas", parent='19'),
    PageInfo('40', 'RegistrosCripto', "Registros (Criptomoedas)", parent='19'),
    PageInfo('41', 'InformarNovaOperacaoCripto', "Informar nova operação na {Corretora}", parent='19'),
    PageInfo('43', 'AlterarOperacaoCripto', "Alterar operações na {Corretora}", parent='19'),
    PageInfo('44', 'DeletarOperacaoCripto', "Deletar operações na {Corretora}", parent='19'),
    PageInfo('46', 'AcoesNegocios', "ARCA: Ações e Negócios", parent='11'),
    PageInfo('47', 'RealEstate', "ARCA: Real Estate", parent='11'),
    PageInfo('48', 'Caixa', "ARCA: Caixa", parent='11'),
    PageInfo('49', 'AtivosInternacionais', "ARCA: Ativos Internacionais", parent='11'),
    PageInfo('50', 'CriptoARCA', "ARCA: Criptomoedas", parent='11'),
    PageInfo('51', 'Tributacao', "Tributação", parent='1'),
]

# Every screen, including aux sub-pages and confirm dialogs. This is the authoritative lookup by the
# exact string HMI assigns to window.PageID.
ALL_PAGES: list[PageInfo] = PAGES + [
    PageInfo('9', 'Perfil', "Perfil e ferramentas (via PageIDAux)", is_aux=True, parent='1'),
    PageInfo('14', 'MudarEmail', "Alteração de email (via PageIDAux)", is_aux=True, parent='9'),
    PageInfo('15', 'MudarSenha', "Alteração de senha (via PageIDAux)", is_aux=True, parent='9'),
    PageInfo('17a', 'ConfirmacaoEmailPosMudanca', "Confirmação de email (após mudar email)", is_aux=True, parent='14'),
    PageInfo('17b', 'ConfirmacaoLogout', "Confirmação de email (encerrar conta/logout)", is_aux=True, parent='16'),
    PageInfo('45', 'InsercaoCotacoesManuais', "Inserção das cotações manualmente (via PageIDAux)", is_aux=True, parent=None),
    PageInfo('ChooseCurrency', 'EscolhaMoeda', "Escolha a sua moeda corrente (via PageIDAux)", is_aux=True, parent='9'),

    PageInfo('16', 'ConfirmarEncerrarConta', "Encerrar conta (diálogo de confirmação)", is_aux=True, parent='9'),
    PageInfo('21', 'ConfirmarDeletarCorretoraBolsa', "Deletar corretora (Bolsa - diálogo)", parent='18'),
    PageInfo('38', 'ConfirmarDeletarCorretoraCripto', "Deletar corretora (Criptomoedas - diálogo)", parent='19'),
    PageInfo('Bancos', 'EditacaoContasCorrentesBancos', "Edição das Contas-Correntes em Bancos", parent='18'),
    PageInfo('BancosAdd', 'AdicionarNovoBanco', "Adicionar novo banco", parent='Bancos'),
    PageInfo('BancosRename', 'RenomearBanco', "Renomear banco", parent='Bancos'),
    PageInfo('ImportFromExcel', 'ImportandoDadosExcel', "Importando dados do excel", parent=None),

    PageInfo('31a', 'NaoImplementada31a', "Funcionalidade ainda não implementada.", parent=None),
    PageInfo('31b', 'NaoImplementada31b', "Funcionalidade ainda não implementada.", parent=None),
    PageInfo('32a', 'NaoImplementada32a', "Funcionalidade ainda não implementada.", parent=None),
    PageInfo('32b', 'NaoImplementada32b', "Funcionalidade ainda não implementada.", parent=None),
]

PAGE_BY_ID: dict[str, PageInfo] = {p.page_id: p for p in ALL_PAGES}
PAGE_BY_NAME: dict[str, PageInfo] = {p.name: p for p in ALL_PAGES}


def page_id(name: str) -> str:
    """Return the PageID string for a display name (e.g. ``page_id('AnaliseMercado')`` -> '5')."""
    return PAGE_BY_NAME[name].page_id


def page_name(page_id_str: str) -> str:
    """Return the display name for a PageID string (e.g. ``page_name('5')`` -> 'AnaliseMercado')."""
    return PAGE_BY_ID[page_id_str].name
