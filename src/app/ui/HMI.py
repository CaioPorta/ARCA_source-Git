"""Created on Sun Sep  5 01:44:04 2021

@author: Caio Moreira Porta
"""

"""Main window (IHMmain) and application entry point (graphical_thread).

IHMmain is a single QWidget subclass whose behaviour is split across several
baseless mixin modules (one file per concern) that are re-composed here so the
public surface stays `from ui.HMI import IHMmain` / `graphical_thread`:

    HMI_PageNavigation   - CreatePage dispatcher + navigation decisions
    HMI_Presentation     - page rendering, layout helpers, header, tables
    HMI_PageBuilders     - per-page widget builders (CreatePage0..N)
    HMI_Events           - button/key/event handlers

Only the lifecycle/core methods below live in this file; everything else is
defined in the mixins and inherited automatically.
"""

import ctypes
import sys
from PyQt5.QtGui import QFont, QCursor, QPixmap, QIcon, QColor
from PyQt5.QtWidgets import QWidget, QToolTip, QApplication, QGridLayout
from PyQt5.QtCore import QSize, QCoreApplication
from threading import Lock

import core.DBManager as DBManager
import core.YahooFinance as YahooFinance
import core.Calcular as Calcular
import core.VersionChecker as VersionChecker
import ui.trades.HMI_Trades_page as HMI_Trades_page
import ui.tributacao.HMI_Tributacao_page as HMI_Tributacao_page
import ui.arca.HMI_ARCA_page as HMI_ARCA_page
import ui.desempenho.HMI_Desempenho_page as HMI_Desempenho_page
import ui.mercado.HMI_Mercado_page as HMI_Mercado_page
from ui.pages import PAGE_BY_NAME

from ui.home_and_parameters.HMI_PageNavigation import HMI_PageNavigation
from ui.home_and_parameters.HMI_Presentation import HMI_Presentation
from ui.home_and_parameters.HMI_PageBuilders import HMI_PageBuilders
from ui.home_and_parameters.HMI_Events import HMI_Events


class IHMmain(HMI_PageNavigation, HMI_Presentation, HMI_PageBuilders, HMI_Events, QWidget):
    """Main application window. Behaviour is composed from the mixins above;
    only lifecycle/core state lives here on purpose (see module docstring)."""

    def __init__(self):
        self.APPVersion = "Versão Beta 0.0.5.5.33.2" #AnáliseDoMercado.Desempenho.ARCA.Tributação.NegociaçõesEGestãoDeDB.HMI
        self.OnlineVersion = ""
        super().__init__()
        self.setObjectName("IHM")

        # Initial parameters definition

        # HMI fixed parameters
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.screen_height = screensize[1]
        self.screen_width = screensize[0]
        self.font8 = QFont('Times New Roman', 8)
        self.font8.setBold(False)
        self.font9 = QFont('Times New Roman', 9)
        self.font9.setBold(False)
        self.font10 = QFont('Times New Roman', 10)
        self.font10.setBold(False)
        self.font12 = QFont('Times New Roman', 12)
        self.font12.setBold(False)
        self.font14 = QFont('Times New Roman', 14)
        self.font16 = QFont('Times New Roman', 16)
        self.font18 = QFont('Times New Roman', 18)
        self.font20 = QFont('Times New Roman', 20, QFont.Bold)
        self.font22 = QFont('Times New Roman', 22, QFont.Bold)
        self.font24 = QFont('Cooper Black', 24, QFont.Bold)
        self.font26 = QFont('Cooper Black', 26, QFont.Bold)
        self.font28 = QFont('Cooper Black', 28, QFont.Bold)
        self.font30 = QFont('Cooper Black', 30, QFont.Bold)
        QToolTip.setFont(QFont('Arial', 12))

        pixmap = QPixmap("./images/ThinkingMonkey.png")
        self.CustomCursor_ThinkingMonkey = QCursor(pixmap, 32, 32)

        # Layout creation

        # Window creation
        self.setWindowTitle("Finanças")
        self.setWindowIcon(QIcon(".\\images\\logoARCA.png"))
        self.setAutoFillBackground(True)
        background = self.palette()
        background.setColor(self.backgroundRole(), QColor(str('#%02x%02x%02x' % (5, 5, 15))))
        self.setPalette(background)
        self.setMinimumSize(QSize(int(self.screen_width*0.5), int(self.screen_height*0.6)))
        self.showMaximized()

        self.GLayout = QGridLayout()
        self.setLayout(self.GLayout)

        self.installEventFilter(self)

        # Inicialização do programa
        self.F_GLayout = [] # GridLayouts que ficam dentro do GLayout
        self.GCount = 0 # Contador de GridLayouts que tem no GLayout
        self.HBoxCount = 0 # Contador de HBoxLayouts que tem no GLayout
        self.VBoxCount = 0 # Contador de VBoxLayouts que tem no GLayout
        self.PageID= PAGE_BY_NAME['Login'].page_id
        self.PageIDAux = ''
        self.OutraJanelaAberta = False
        self.ClockWindowOpen = False
        self.CalendarWindowOpen = False
        self.VersionUpdate = False

    def initialize(self, check_version=True):
        self.CreatePage(PAGE_BY_NAME['Login'].page_id) # Página inicial do programa
        if check_version:
            self.VersionChecker = VersionChecker.VersionChecker(self)

    def InicializacaoUsuario(self):
        # Inicialização usuário
        self.idxCorretora = 0 # Memoriza qual corretora que estava sendo observada antes de trocar de página
        self.idxBanco = 0
        self.idxPapel = 0 # Memoriza qual papel que estava sendo observado antes de trocar de página
        self.idxAtivo = 0
        self.idxTipoDeAtivo = 0
        self.idxSubtipoDeAtivo = 0
        self.idxSetorAtivo = 0
        self.DTeST = "NotDefined"
        self.Patrimonio = 'calculando...'
        self.Rendimento = 'calculando...'
        self.SumContasCorrentes = 0.
        self.Cache_Cotacao = 0.
        self.AtualizarCotacoes_is_running = False
        self.ThreadLock = Lock()

        self.LoggedIn = False
        self.ShowValues = True
        self.filedialogIsOpen = False
        self.ParteImportacao = 1

        self.YahooFinance = YahooFinance.YahooFinance(self)
        self.DBManager = DBManager.DBManager(self)
        self.Calcular = Calcular.Calcular(self)

        self.DBManager.Disconnect()

        self.HMI_Trades = HMI_Trades_page.HMI_Trades(self)
        self.HMI_Tributacao = HMI_Tributacao_page.HMI_Tributacao(self)
        self.HMI_ARCA = HMI_ARCA_page.HMI_ARCA(self)
        self.HMI_Desempenho = HMI_Desempenho_page.HMI_Desempenho(self)
        self.HMI_Mercado = HMI_Mercado_page.HMI_Mercado(self)
