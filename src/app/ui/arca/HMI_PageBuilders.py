# -*- coding: utf-8 -*-
"""
ARCA behaviour split into a single concern.
HMI_PageBuilders - pagebuilders helpers (inherited by the composition root).
"""
from core.BackgroundProcesses import (WorkerThread)
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas)
from PyQt5.QtGui import (QFont, QCursor)
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QTableWidget,
)
from PyQt5.QtCore import (Qt)
from ui.pages import (PAGE_BY_NAME)


class HMI_PageBuilders:
    def CreatePage11(self): # Página inicial

        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: black")
        Background_1.setFixedHeight(int(self.HMI.screen_height*1/24))

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: black")

        self.HMI.Label_Titulo = QLabel('ARCA')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Subtitulo1 = QPushButton('Ações e negócios')
        self.HMI.Label_Subtitulo1.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info24'].page_id))
        self.HMI.Label_Subtitulo1.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: transparent; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo1.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo2 = QPushButton('Real Estate')
        self.HMI.Label_Subtitulo2.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info25'].page_id))
        self.HMI.Label_Subtitulo2.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: transparent; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo2.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo3 = QPushButton('Caixa')
        self.HMI.Label_Subtitulo3.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info26'].page_id))
        self.HMI.Label_Subtitulo3.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: transparent; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo3.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo4 = QPushButton('Ativos internacionais')
        self.HMI.Label_Subtitulo4.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info27'].page_id))
        self.HMI.Label_Subtitulo4.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: transparent; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo4.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo5 = QPushButton()
        self.HMI.Label_Subtitulo5.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: transparent; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo5.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo1_ = QPushButton('Ações e negócios')
        self.HMI.Label_Subtitulo1_.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info24'].page_id))
        self.HMI.Label_Subtitulo1_.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo1_.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo2_ = QPushButton('Real Estate')
        self.HMI.Label_Subtitulo2_.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info25'].page_id))
        self.HMI.Label_Subtitulo2_.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo2_.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo3_ = QPushButton('Caixa')
        self.HMI.Label_Subtitulo3_.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info26'].page_id))
        self.HMI.Label_Subtitulo3_.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo3_.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo4_ = QPushButton('Ativos internacionais')
        self.HMI.Label_Subtitulo4_.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info27'].page_id))
        self.HMI.Label_Subtitulo4_.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo4_.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo5_ = QPushButton()
        self.HMI.Label_Subtitulo5_.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info28'].page_id))
        self.HMI.Label_Subtitulo5_.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo5_.setFont(self.HMI.font16)

        if self.GraficoEspecifico_Name == "Ações Nacionais":
            self.HMI.Label_Subtitulo5.setText("Ações")
            self.HMI.Label_Subtitulo5_.setText("Ações")
        elif self.GraficoEspecifico_Name == "Fundos de investimentos: Ações e Negócios":
            self.HMI.Label_Subtitulo5.setText("Fundos")
            self.HMI.Label_Subtitulo5_.setText("Fundos")
        elif self.GraficoEspecifico_Name == "Fundos Imobiliários":
            self.HMI.Label_Subtitulo5.setText("Fundos")
            self.HMI.Label_Subtitulo5_.setText("Fundos")
        elif self.GraficoEspecifico_Name == "Terrenos":
            self.HMI.Label_Subtitulo5.setText("Terrenos")
            self.HMI.Label_Subtitulo5_.setText("Terrenos")
        elif self.GraficoEspecifico_Name == "Construções":
            self.HMI.Label_Subtitulo5.setText("Construções")
            self.HMI.Label_Subtitulo5_.setText("Construções")
        elif self.GraficoEspecifico_Name == "Renda Fixa":
            self.HMI.Label_Subtitulo5.setText("RF")
            self.HMI.Label_Subtitulo5_.setText("RF")
        elif self.GraficoEspecifico_Name == "Tesouro Direto e Títulos Públicos":
            self.HMI.Label_Subtitulo5.setText("TD/TP")
            self.HMI.Label_Subtitulo5_.setText("TD/TP")
        elif self.GraficoEspecifico_Name == "Previdência Privada":
            self.HMI.Label_Subtitulo5.setText("PP")
            self.HMI.Label_Subtitulo5_.setText("PP")
        elif self.GraficoEspecifico_Name == "COE":
            self.HMI.Label_Subtitulo5.setText("COE")
            self.HMI.Label_Subtitulo5_.setText("COE")
        elif self.GraficoEspecifico_Name == "Fundos de Investimento: Renda Fixa":
            self.HMI.Label_Subtitulo5.setText("Fundos")
            self.HMI.Label_Subtitulo5_.setText("Fundos")
        elif self.GraficoEspecifico_Name == "BDR":
            self.HMI.Label_Subtitulo5.setText("BDR")
            self.HMI.Label_Subtitulo5_.setText("BDR")
        elif self.GraficoEspecifico_Name == "Fundos de Investimento: Ações Internacionais":
            self.HMI.Label_Subtitulo5.setText("Fundos")
            self.HMI.Label_Subtitulo5_.setText("Fundos")
        elif self.GraficoEspecifico_Name == "Criptomoedas":
            self.HMI.Label_Subtitulo5.setText("Criptomoedas")
            self.HMI.Label_Subtitulo5_.setText("Criptomoedas")


        self.HMI.Button_Msg3 = QPushButton('Montante em aplicação\n('+self.HMI.DBManager.GetUserCoinCurrency()+")")
        self.HMI.Button_Msg3.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info21'].page_id))
        self.HMI.Button_Msg3.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg3.setFont(self.HMI.font12)

        self.HMI.TextBox_MontanteEmAplicacao = QLineEdit('Calculando...')
        self.HMI.TextBox_MontanteEmAplicacao.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_MontanteEmAplicacao.setFixedWidth(int(self.HMI.frameGeometry().width()/6))
        self.HMI.TextBox_MontanteEmAplicacao.setStyleSheet("background-color: black; color: orange;")
        self.HMI.TextBox_MontanteEmAplicacao.setFont(self.HMI.font12)
        self.HMI.TextBox_MontanteEmAplicacao.setEnabled(False)

        self.HMI.Button_Msg4 = QPushButton('Montante aplicado\n('+self.HMI.DBManager.GetUserCoinCurrency()+")")
        self.HMI.Button_Msg4.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info20'].page_id))
        self.HMI.Button_Msg4.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg4.setFont(self.HMI.font12)

        self.HMI.TextBox_MontanteAplicado = QLineEdit(str('%.2f' % round(self.HMI.DBManager.GetMontanteAplicado(),2)))
        self.HMI.TextBox_MontanteAplicado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_MontanteAplicado.setFixedWidth(int(self.HMI.frameGeometry().width()/6))
        self.HMI.TextBox_MontanteAplicado.setStyleSheet("background-color: black; color: white;")
        self.HMI.TextBox_MontanteAplicado.setFont(self.HMI.font12)
        self.HMI.TextBox_MontanteAplicado.setEnabled(False)

        self.HMI.HBoxLayout_Montantes1 = QVBoxLayout()
        self.HMI.HBoxLayout_Montantes1.addWidget(self.HMI.Button_Msg3)
        self.HMI.HBoxLayout_Montantes1.addWidget(self.HMI.TextBox_MontanteEmAplicacao)
        self.HMI.HBoxLayout_Montantes2 = QVBoxLayout()
        self.HMI.HBoxLayout_Montantes2.addWidget(self.HMI.Button_Msg4)
        self.HMI.HBoxLayout_Montantes2.addWidget(self.HMI.TextBox_MontanteAplicado)
        self.HMI.HBoxLayout_Montantes = QHBoxLayout()
        self.HMI.HBoxLayout_Montantes.addLayout(self.HMI.HBoxLayout_Montantes2)
        self.HMI.HBoxLayout_Montantes.addLayout(self.HMI.HBoxLayout_Montantes1)

        if self.Flag_RecalcularGraficos:
            self.HMI.setCursor(Qt.CursorShape.WaitCursor)
            self.GraficoEspecifico_Name = ""
            self.loadingThread = WorkerThread('Thread_LoadingARCApage', self.HMI)
            self.loadingThread.start()
            self.HMI.GraphWidget_AcoesENegocios = self.CreateGraph_Page11_AcoesENegocios()
            self.HMI.GraphWidget_RealEstate = self.CreateGraph_Page11_RealEstate()
            self.HMI.GraphWidget_Caixa = self.CreateGraph_Page11_Caixa()
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_Especifica()
            self.HMI.GraphWidget_AtivosInternacionais = self.CreateGraph_Page11_AtivosInternacionais()
            self.HMI.GraphWidget_Carteira = self.CreateGraph_Page11_Carteira_pie()
            self.HMI.unsetCursor()
        else:
            self.HMI.TextBox_MontanteEmAplicacao.setStyleSheet("background-color: black; color: green;")
            self.HMI.TextBox_MontanteEmAplicacao.setText(str('%.2f' % self.MontanteEmAplicacao))
            self.HMI.GraphWidget_AcoesENegocios = FigureCanvas(self.GraphWidget_AcoesENegocios_Storage)
            self.HMI.GraphWidget_RealEstate = FigureCanvas(self.GraphWidget_RealEstate_Storage)
            self.HMI.GraphWidget_Caixa = FigureCanvas(self.GraphWidget_Caixa_Storage)
            self.HMI.GraphWidget_Especifica = FigureCanvas(self.GraphWidget_Especifica_Storage)
            self.HMI.GraphWidget_AtivosInternacionais = FigureCanvas(self.GraphWidget_AtivosInternacionais_Storage)
            self.HMI.GraphWidget_Carteira = FigureCanvas(self.GraphWidget_Carteira_Storage)

        self.HMI.Button_AcoesENegociosInvisivel = QPushButton()
        self.HMI.Button_AcoesENegociosInvisivel.pressed.connect(lambda: self.ProximoGraficoEspecifico("Ações e Negócios"))
        self.HMI.Button_AcoesENegociosInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_AcoesENegociosInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_RealEstateInvisivel = QPushButton()
        self.HMI.Button_RealEstateInvisivel.pressed.connect(lambda: self.ProximoGraficoEspecifico("Real Estate"))
        self.HMI.Button_RealEstateInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_RealEstateInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_CaixaInvisivel = QPushButton()
        self.HMI.Button_CaixaInvisivel.pressed.connect(lambda: self.ProximoGraficoEspecifico("Caixa"))
        self.HMI.Button_CaixaInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_CaixaInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_AcoesInternacionaisInvisivel = QPushButton()
        self.HMI.Button_AcoesInternacionaisInvisivel.pressed.connect(lambda: self.ProximoGraficoEspecifico("Ativos Internacionais"))
        self.HMI.Button_AcoesInternacionaisInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_AcoesInternacionaisInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_EspecificaInvisivel = QPushButton()
        self.HMI.Button_EspecificaInvisivel.pressed.connect(lambda: self.CallCreatePage())
        self.HMI.Button_EspecificaInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_EspecificaInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.HBoxLayout_Graficos_Subtipos = QHBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_AcoesENegocios = QVBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_AcoesENegocios.addWidget(self.HMI.Label_Subtitulo1_)
        self.HMI.VBoxLayout_Graficos_Subtipos_AcoesENegocios.addWidget(self.HMI.GraphWidget_AcoesENegocios)
        self.HMI.VBoxLayout_Graficos_Subtipos_RealEstate = QVBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_RealEstate.addWidget(self.HMI.Label_Subtitulo2_)
        self.HMI.VBoxLayout_Graficos_Subtipos_RealEstate.addWidget(self.HMI.GraphWidget_RealEstate)
        self.HMI.VBoxLayout_Graficos_Subtipos_Caixa = QVBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_Caixa.addWidget(self.HMI.Label_Subtitulo3_)
        self.HMI.VBoxLayout_Graficos_Subtipos_Caixa.addWidget(self.HMI.GraphWidget_Caixa)
        self.HMI.VBoxLayout_Graficos_Subtipos_AtivosInternacionais = QVBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_AtivosInternacionais.addWidget(self.HMI.Label_Subtitulo4_)
        self.HMI.VBoxLayout_Graficos_Subtipos_AtivosInternacionais.addWidget(self.HMI.GraphWidget_AtivosInternacionais)
        self.HMI.VBoxLayout_Graficos_Subtipos_Especifica = QVBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_Especifica.addWidget(self.HMI.Label_Subtitulo5_)
        self.HMI.VBoxLayout_Graficos_Subtipos_Especifica.addWidget(self.HMI.GraphWidget_Especifica)
        self.HMI.HBoxLayout_Graficos_Subtipos.addLayout(self.HMI.VBoxLayout_Graficos_Subtipos_AcoesENegocios)
        self.HMI.HBoxLayout_Graficos_Subtipos.addLayout(self.HMI.VBoxLayout_Graficos_Subtipos_RealEstate)
        self.HMI.HBoxLayout_Graficos_Subtipos.addLayout(self.HMI.VBoxLayout_Graficos_Subtipos_Caixa)
        self.HMI.HBoxLayout_Graficos_Subtipos.addLayout(self.HMI.VBoxLayout_Graficos_Subtipos_AtivosInternacionais)
        self.HMI.HBoxLayout_Graficos_Subtipos.addLayout(self.HMI.VBoxLayout_Graficos_Subtipos_Especifica)

        self.HMI.HBoxLayout_Graficos_Subtipos_Invisiveis = QHBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_AcoesENegociosInvisiveis = QVBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_AcoesENegociosInvisiveis.addWidget(self.HMI.Label_Subtitulo1)
        self.HMI.VBoxLayout_Graficos_Subtipos_AcoesENegociosInvisiveis.addWidget(self.HMI.Button_AcoesENegociosInvisivel)
        self.HMI.VBoxLayout_Graficos_Subtipos_RealEstateInvisiveis = QVBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_RealEstateInvisiveis.addWidget(self.HMI.Label_Subtitulo2)
        self.HMI.VBoxLayout_Graficos_Subtipos_RealEstateInvisiveis.addWidget(self.HMI.Button_RealEstateInvisivel)
        self.HMI.VBoxLayout_Graficos_Subtipos_CaixaInvisiveis = QVBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_CaixaInvisiveis.addWidget(self.HMI.Label_Subtitulo3)
        self.HMI.VBoxLayout_Graficos_Subtipos_CaixaInvisiveis.addWidget(self.HMI.Button_CaixaInvisivel)
        self.HMI.VBoxLayout_Graficos_Subtipos_AtivosInternacionaisInvisiveis = QVBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_AtivosInternacionaisInvisiveis.addWidget(self.HMI.Label_Subtitulo4)
        self.HMI.VBoxLayout_Graficos_Subtipos_AtivosInternacionaisInvisiveis.addWidget(self.HMI.Button_AcoesInternacionaisInvisivel)
        self.HMI.VBoxLayout_Graficos_Subtipos_EspecificaInvisiveis = QVBoxLayout()
        self.HMI.VBoxLayout_Graficos_Subtipos_EspecificaInvisiveis.addWidget(self.HMI.Label_Subtitulo5)
        self.HMI.VBoxLayout_Graficos_Subtipos_EspecificaInvisiveis.addWidget(self.HMI.Button_EspecificaInvisivel)
        self.HMI.HBoxLayout_Graficos_Subtipos_Invisiveis.addLayout(self.HMI.VBoxLayout_Graficos_Subtipos_AcoesENegociosInvisiveis)
        self.HMI.HBoxLayout_Graficos_Subtipos_Invisiveis.addLayout(self.HMI.VBoxLayout_Graficos_Subtipos_RealEstateInvisiveis)
        self.HMI.HBoxLayout_Graficos_Subtipos_Invisiveis.addLayout(self.HMI.VBoxLayout_Graficos_Subtipos_CaixaInvisiveis)
        self.HMI.HBoxLayout_Graficos_Subtipos_Invisiveis.addLayout(self.HMI.VBoxLayout_Graficos_Subtipos_AtivosInternacionaisInvisiveis)
        self.HMI.HBoxLayout_Graficos_Subtipos_Invisiveis.addLayout(self.HMI.VBoxLayout_Graficos_Subtipos_EspecificaInvisiveis)

        self.HMI.Button_CarteiraInvisivel = QPushButton()
        self.HMI.Button_CarteiraInvisivel.pressed.connect(lambda: self.OnButtonPressed('Change Carteira Graph'))
        self.HMI.Button_CarteiraInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_CarteiraInvisivel.setFixedSize(int(self.HMI.frameGeometry().height()*1/5),int(self.HMI.frameGeometry().height()*1/5))
        self.HMI.Button_CarteiraInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Msg1 = QPushButton('Nota de equilíbrio: ???/100')
        self.HMI.Button_Msg1.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg1.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info16'].page_id))
        self.HMI.Button_Msg1.setFont(self.HMI.font12)

        self.HMI.Button_Msg5 = QPushButton('Gasto mensal\n('+self.HMI.DBManager.GetUserCoinCurrency()+")")
        self.HMI.Button_Msg5.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg5.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info17'].page_id))
        self.HMI.Button_Msg5.setFont(self.HMI.font12)

        self.HMI.Button_Msg6 = QPushButton('Meses de\nreserva')
        self.HMI.Button_Msg6.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg6.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info18'].page_id))
        self.HMI.Button_Msg6.setFont(self.HMI.font12)

        self.HMI.Button_Msg7 = QPushButton('Aplicar\n('+self.HMI.DBManager.GetUserCoinCurrency()+")")
        self.HMI.Button_Msg7.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg7.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info19'].page_id))
        self.HMI.Button_Msg7.setFont(self.HMI.font12)

        self.HMI.Label_Msg8 = QLabel('Reserva:')
        self.HMI.Label_Msg8.setStyleSheet('color: white')
        self.HMI.Label_Msg8.setFont(self.HMI.font12)
        self.HMI.Label_Msg8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Msg9 = QLabel('        ') # Espaço vazio que serve para ficar centralizado o restante das informações
        self.HMI.Label_Msg9.setStyleSheet('color: white')
        self.HMI.Label_Msg9.setFont(self.HMI.font12)
        self.HMI.Label_Msg9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.TextBox_GastoMensal = QLineEdit(str('%.2f' % self.HMI.DBManager.GetGastoMensal()))
        self.HMI.TextBox_GastoMensal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_GastoMensal.setFixedWidth(int(self.HMI.frameGeometry().width()/10))
        self.HMI.TextBox_GastoMensal.setStyleSheet("background-color: black; color: white;")
        self.HMI.TextBox_GastoMensal.setFont(self.HMI.font12)
        self.HMI.TextBox_GastoMensal.returnPressed.connect(lambda: self.OnButtonPressed("TextBox_GastoMensal"))

        self.HMI.TextBox_MesesDeReserva = QLineEdit(str(int(self.HMI.DBManager.GetMesesDeReserva())))
        self.HMI.TextBox_MesesDeReserva.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_MesesDeReserva.setFixedWidth(int(self.HMI.frameGeometry().width()/20))
        self.HMI.TextBox_MesesDeReserva.setStyleSheet("background-color: black; color: white;")
        self.HMI.TextBox_MesesDeReserva.setFont(self.HMI.font12)
        self.HMI.TextBox_MesesDeReserva.returnPressed.connect(lambda: self.OnButtonPressed("TextBox_MesesDeReserva"))

        self.HMI.TextBox_Aplicar = QLineEdit()
        self.HMI.TextBox_Aplicar.setStyleSheet("background-color: black; color: orange;")
        self.HMI.TextBox_Aplicar.setText('Calculando...')
        self.HMI.TextBox_Aplicar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_Aplicar.setFixedWidth(int(self.HMI.frameGeometry().width()/10))
        self.HMI.TextBox_Aplicar.setFont(self.HMI.font12)
        self.HMI.TextBox_Aplicar.setEnabled(False)

        self.HMI.HBoxLayout_Reserva1 = QVBoxLayout()
        self.HMI.HBoxLayout_Reserva1.addWidget(self.HMI.Label_Msg9) # Label_Msg8
        self.HMI.HBoxLayout_Reserva1.addWidget(self.HMI.Label_Msg8)
        self.HMI.HBoxLayout_Reserva2 = QVBoxLayout()
        self.HMI.HBoxLayout_Reserva2.addWidget(self.HMI.Button_Msg5) # TextBox_GastoMensal
        self.HMI.HBoxLayout_Reserva2.addWidget(self.HMI.TextBox_GastoMensal)
        self.HMI.HBoxLayout_Reserva3 = QVBoxLayout()
        self.HMI.HBoxLayout_Reserva3.addWidget(self.HMI.Button_Msg6) # TextBox_MesesDeReserva
        self.HMI.HBoxLayout_Reserva3.addWidget(self.HMI.TextBox_MesesDeReserva)
        self.HMI.HBoxLayout_Reserva4 = QVBoxLayout()
        self.HMI.HBoxLayout_Reserva4.addWidget(self.HMI.Button_Msg7) # TextBox_Aplicar
        self.HMI.HBoxLayout_Reserva4.addWidget(self.HMI.TextBox_Aplicar)
        self.HMI.HBoxLayout_Reserva = QHBoxLayout()
        self.HMI.HBoxLayout_Reserva.addLayout(self.HMI.HBoxLayout_Reserva1)
        self.HMI.HBoxLayout_Reserva.addLayout(self.HMI.HBoxLayout_Reserva2)
        self.HMI.HBoxLayout_Reserva.addLayout(self.HMI.HBoxLayout_Reserva3)
        self.HMI.HBoxLayout_Reserva.addLayout(self.HMI.HBoxLayout_Reserva4)

        self.Table_ContasCorrenteHeader = QTableWidget()
        self.Table_ContasCorrente = QTableWidget()

        self.CreateTable_11_2() # Table_ContasCorrente (Criada com uma thread)
        self.CreateTable_11_1() # Table_ContasCorrenteHeader

        self.Table_ContasCorrente.setShowGrid(False)
        self.Table_ContasCorrente.setFont(self.HMI.font10)
        self.Table_ContasCorrente.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                 color: white;
                                                                 border: 1px solid rgba(0, 0, 0, 0);}
                                                   QTableView {border-bottom: 0px dashed white;
                                                               border-right: 0px solid white;
                                                               border-left: 0px solid white;}
                                                   QTableView::item {border-bottom: 0.5px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
        self.Table_ContasCorrente.verticalHeader().hide()
        self.Table_ContasCorrente.horizontalHeader().hide()

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 6)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 4, 6)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 6, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Graficos_Subtipos, 1, 0, 1, 6, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Graficos_Subtipos_Invisiveis, 1, 0, 1, 6, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Reserva, 2, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Montantes, 3, 0, 2, 2, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_Carteira, 2, 2, 2, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_CarteiraInvisivel, 2, 2, 2, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Msg1, 4, 2, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.Table_ContasCorrenteHeader, 2, 4, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.Table_ContasCorrente, 3, 4, 2, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        if self.HMI.frameGeometry().width()/self.HMI.frameGeometry().height() < 1.9577: proporcao = 1/6
        elif self.HMI.frameGeometry().width()/self.HMI.frameGeometry().height() < 2.6202: proporcao = 1/8
        else: proporcao = 1/10

        self.HMI.Button_CarteiraInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.Button_AcoesENegociosInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.Button_RealEstateInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.Button_CaixaInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.Button_AcoesInternacionaisInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.Button_EspecificaInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.GraphWidget_Carteira.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.GraphWidget_AcoesENegocios.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.GraphWidget_RealEstate.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.GraphWidget_Caixa.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.GraphWidget_AtivosInternacionais.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.GraphWidget_Especifica.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))

        self.Thread_TextBox_Aplicar = WorkerThread('Thread_TextBox_Aplicar', self.HMI)
        self.Thread_TextBox_Aplicar.start()
        
        if self.HMI.ShowValues:
            self.HMI.TextBox_Aplicar.setEchoMode(QLineEdit.Normal)
            self.HMI.TextBox_GastoMensal.setEchoMode(QLineEdit.Normal)
            self.HMI.TextBox_GastoMensal.setEnabled(True)
            self.HMI.TextBox_MontanteAplicado.setEchoMode(QLineEdit.Normal)
            self.HMI.TextBox_MontanteEmAplicacao.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Aplicar.setEchoMode(QLineEdit.Password)
            self.HMI.TextBox_GastoMensal.setEchoMode(QLineEdit.Password)
            self.HMI.TextBox_GastoMensal.setEnabled(False)
            self.HMI.TextBox_MontanteAplicado.setEchoMode(QLineEdit.Password)
            self.HMI.TextBox_MontanteEmAplicacao.setEchoMode(QLineEdit.Password)

        self.HMI.TextBox_MesesDeReserva.clearFocus()


    def CreatePage46(self): # Página Ações e Negócios
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()

        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: black")
        Background_1.setFixedHeight(int(self.HMI.screen_height * 1 / 24))

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: black")

        self.HMI.Label_Titulo = QLabel('ARCA: Ações e Negócios')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_MostrarValoresMaioresQue = QLabel('Mostrar em ' + UserCoin + '\nvalores maiores que')
        self.HMI.Label_MostrarValoresMaioresQue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.Label_MostrarValoresMaioresQue.setStyleSheet('color: white')
        self.HMI.Label_MostrarValoresMaioresQue.setFont(self.HMI.font12)

        self.HMI.TextBox_MostrarValoresMaioresQue = QLineEdit(str(self.MostrarValoresMaioresQue))
        self.HMI.TextBox_MostrarValoresMaioresQue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_MostrarValoresMaioresQue.setFixedWidth(int(self.HMI.frameGeometry().width() / 20))
        self.HMI.TextBox_MostrarValoresMaioresQue.setStyleSheet("background-color: black; color: " + FontColorLineEdit + ";")
        self.HMI.TextBox_MostrarValoresMaioresQue.setFont(self.HMI.font12)
        self.HMI.TextBox_MostrarValoresMaioresQue.returnPressed.connect(lambda: self.OnButtonPressed("MostrarValoresMaioresQue"))

        self.HMI.Button_VisaoGeral = QPushButton('Visão Geral')
        self.HMI.Button_VisaoGeral.pressed.connect(lambda: self.OnButtonPressed('Visão Geral'))
        self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
        self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
        self.HMI.Button_VisaoGeral.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_AtivoPorCorretora = QPushButton('Ativo por corretora')
        self.HMI.Button_AtivoPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Ativo por corretora'))
        self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AtivoPorCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_TotalDeUserCoinPorCorretora = QPushButton('Total de ' + UserCoin + ' por corretora')
        self.HMI.Button_TotalDeUserCoinPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Total de UserCoin por corretora'))
        self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_TotalDeUserCoinPorCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Setor = QPushButton('Por setor')
        self.HMI.Button_Setor.pressed.connect(lambda: self.OnButtonPressed('Ativo por setor'))
        self.HMI.Button_Setor.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_Setor.setFont(self.HMI.font16)
        self.HMI.Button_Setor.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.ComboBox_Ativos = QComboBox()
        self.HMI.ComboBox_Ativos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Ativos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.ComboBox_Ativos.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        self.HMI.ComboBox_Ativos.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        self.ativos, self.volume = self.HMI.DBManager.GetAllAtivosPorTipoDeAtivo_Bolsa(TipoDeAtivo="Ações e Negócios")
        self.ativos = sorted(self.ativos)

        if sum(self.volume) > 0:
            self.HMI.ComboBox_Ativos.addItem("Todos")
            for idx, ativo in enumerate(self.ativos): self.HMI.ComboBox_Ativos.addItem(ativo)
        else:
            self.HMI.ComboBox_Ativos.addItem("Vazio")
        self.HMI.ComboBox_Ativos.setCurrentIndex(0)

        self.Custo = 0
        for ativo in self.ativos: self.Custo += self.HMI.DBManager.GetCustoAtivo(ativo, "Bolsa")  # Calcula a soma dos custos de TODOS os ativos

        self.HMI.TextBox_Custo = QLineEdit()
        self.HMI.TextBox_Custo.setFixedWidth(int(self.HMI.frameGeometry().width() / 5 * 0.9))
        self.HMI.TextBox_Custo.setStyleSheet('QLineEdit {background-color: black; color: white;}')
        self.HMI.TextBox_Custo.setFont(self.HMI.font16)
        self.HMI.TextBox_Custo.setEnabled(False)
        self.HMI.TextBox_Custo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.HMI.ShowValues:
            self.HMI.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.Custo, 2):.2f}'))
        else:
            self.HMI.TextBox_Custo.setText('Custo: X')

        self.Retorno = 0
        for ativo in self.ativos: self.Retorno += self.HMI.DBManager.GetEstoqueAtivo(ativo, "Bolsa") * self.HMI.DBManager.GetCotacao(ativo)

        self.HMI.TextBox_Retorno = QLineEdit()
        self.HMI.TextBox_Retorno.setFixedWidth(int(self.HMI.frameGeometry().width() / 5 * 0.9))
        self.HMI.TextBox_Retorno.setFont(self.HMI.font16)
        self.HMI.TextBox_Retorno.setEnabled(False)
        self.HMI.TextBox_Retorno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.HMI.ShowValues: self.HMI.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.Retorno, 2):.2f}'))
        else: self.HMI.TextBox_Retorno.setText('Retorno: ' + str(round((self.Retorno - self.Custo) / self.Custo * 100, 1)) + '%X')
        if self.Retorno >= self.Custo: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

        self.MainGraphIsShowing = "Visão Geral"
        self.HMI.GraphWidget_MainGraph = self.CreateGraph_Page46_MainGraph_VisaoGeral()

        self.HMI.GraphWidget_Subtipos = self.CreateGraph_Page46_Subtipos()

        if self.HMI.ComboBox_Ativos.currentText() == "Vazio":
            self.HMI.Button_Setor.setEnabled(False)
            self.HMI.Button_AtivoPorCorretora.setEnabled(False)

        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(Background_2, 1, 0, 9, 3)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_MostrarValoresMaioresQue, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_MostrarValoresMaioresQue, 2, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_VisaoGeral, 4, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_Setor, 6, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.ComboBox_Ativos, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Custo, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Retorno, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_AtivoPorCorretora, 4, 2, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.TextBox_MostrarValoresMaioresQue.clearFocus()


    def CreatePage47(self): # Página Real Estate
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()

        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: black")
        Background_1.setFixedHeight(int(self.HMI.screen_height * 1 / 24))

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: black")

        self.HMI.Label_Titulo = QLabel('ARCA: Real Estate')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_MostrarValoresMaioresQue = QLabel('Mostrar em ' + UserCoin + '\nvalores maiores que')
        self.HMI.Label_MostrarValoresMaioresQue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.Label_MostrarValoresMaioresQue.setStyleSheet('color: white')
        self.HMI.Label_MostrarValoresMaioresQue.setFont(self.HMI.font12)

        self.HMI.TextBox_MostrarValoresMaioresQue = QLineEdit(str(self.MostrarValoresMaioresQue))
        self.HMI.TextBox_MostrarValoresMaioresQue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_MostrarValoresMaioresQue.setFixedWidth(int(self.HMI.frameGeometry().width() / 20))
        self.HMI.TextBox_MostrarValoresMaioresQue.setStyleSheet("background-color: black; color: " + FontColorLineEdit + ";")
        self.HMI.TextBox_MostrarValoresMaioresQue.setFont(self.HMI.font12)
        self.HMI.TextBox_MostrarValoresMaioresQue.returnPressed.connect(lambda: self.OnButtonPressed("MostrarValoresMaioresQue"))

        self.HMI.Button_VisaoGeral = QPushButton('Visão Geral')
        self.HMI.Button_VisaoGeral.pressed.connect(lambda: self.OnButtonPressed('Visão Geral'))
        self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
        self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
        self.HMI.Button_VisaoGeral.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_AtivoPorCorretora = QPushButton('Ativo por corretora')
        self.HMI.Button_AtivoPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Ativo por corretora'))
        self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AtivoPorCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_TotalDeUserCoinPorCorretora = QPushButton('Total de ' + UserCoin + ' por corretora')
        self.HMI.Button_TotalDeUserCoinPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Total de UserCoin por corretora'))
        self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_TotalDeUserCoinPorCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Setor = QPushButton('Por setor')
        self.HMI.Button_Setor.pressed.connect(lambda: self.OnButtonPressed('Ativo por setor'))
        self.HMI.Button_Setor.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_Setor.setFont(self.HMI.font16)
        self.HMI.Button_Setor.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.ComboBox_Ativos = QComboBox()
        self.HMI.ComboBox_Ativos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Ativos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.ComboBox_Ativos.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        self.HMI.ComboBox_Ativos.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        self.ativos, self.volume = self.HMI.DBManager.GetAllAtivosPorTipoDeAtivo_Bolsa(TipoDeAtivo="Real Estate")
        self.ativos = sorted(self.ativos)

        if sum(self.volume) > 0:
            self.HMI.ComboBox_Ativos.addItem("Todos")
            for idx, ativo in enumerate(self.ativos): self.HMI.ComboBox_Ativos.addItem(ativo)
        else:
            self.HMI.ComboBox_Ativos.addItem("Vazio")
        self.HMI.ComboBox_Ativos.setCurrentIndex(0)

        self.Custo = 0
        for ativo in self.ativos: self.Custo += self.HMI.DBManager.GetCustoAtivo(ativo, "Bolsa")  # Calcula a soma dos custos de TODOS os ativos

        self.HMI.TextBox_Custo = QLineEdit()
        self.HMI.TextBox_Custo.setFixedWidth(int(self.HMI.frameGeometry().width() / 5 * 0.9))
        self.HMI.TextBox_Custo.setStyleSheet('QLineEdit {background-color: black; color: white;}')
        self.HMI.TextBox_Custo.setFont(self.HMI.font16)
        self.HMI.TextBox_Custo.setEnabled(False)
        self.HMI.TextBox_Custo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.HMI.ShowValues:
            self.HMI.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.Custo, 2):.2f}'))
        else:
            self.HMI.TextBox_Custo.setText('Custo: X')

        self.Retorno = 0
        for ativo in self.ativos: self.Retorno += self.HMI.DBManager.GetEstoqueAtivo(ativo, "Bolsa") * self.HMI.DBManager.GetCotacao(ativo)

        self.HMI.TextBox_Retorno = QLineEdit()
        self.HMI.TextBox_Retorno.setFixedWidth(int(self.HMI.frameGeometry().width() / 5 * 0.9))
        self.HMI.TextBox_Retorno.setFont(self.HMI.font16)
        self.HMI.TextBox_Retorno.setEnabled(False)
        self.HMI.TextBox_Retorno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.HMI.ShowValues: self.HMI.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.Retorno, 2):.2f}'))
        else: self.HMI.TextBox_Retorno.setText('Retorno: ' + str(round((self.Retorno - self.Custo) / self.Custo * 100, 1)) + '%X')
        if self.Retorno >= self.Custo: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

        self.MainGraphIsShowing = "Visão Geral"
        self.HMI.GraphWidget_MainGraph = self.CreateGraph_Page47_MainGraph_VisaoGeral()

        self.HMI.GraphWidget_Subtipos = self.CreateGraph_Page47_Subtipos()

        if self.HMI.ComboBox_Ativos.currentText() == "Vazio":
            self.HMI.Button_Setor.setEnabled(False)
            self.HMI.Button_AtivoPorCorretora.setEnabled(False)

        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(Background_2, 1, 0, 9, 3)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_MostrarValoresMaioresQue, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_MostrarValoresMaioresQue, 2, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_VisaoGeral, 4, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_Setor, 6, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.ComboBox_Ativos, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Custo, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Retorno, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_AtivoPorCorretora, 4, 2, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.TextBox_MostrarValoresMaioresQue.clearFocus()


    def CreatePage48(self): # Página Caixa
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()

        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: black")
        Background_1.setFixedHeight(int(self.HMI.screen_height * 1 / 24))

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: black")

        self.HMI.Label_Titulo = QLabel('ARCA: Caixa')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_MostrarValoresMaioresQue = QLabel('Mostrar em ' + UserCoin + '\nvalores maiores que')
        self.HMI.Label_MostrarValoresMaioresQue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.Label_MostrarValoresMaioresQue.setStyleSheet('color: white')
        self.HMI.Label_MostrarValoresMaioresQue.setFont(self.HMI.font12)

        self.HMI.TextBox_MostrarValoresMaioresQue = QLineEdit(str(self.MostrarValoresMaioresQue))
        self.HMI.TextBox_MostrarValoresMaioresQue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_MostrarValoresMaioresQue.setFixedWidth(int(self.HMI.frameGeometry().width() / 20))
        self.HMI.TextBox_MostrarValoresMaioresQue.setStyleSheet("background-color: black; color: " + FontColorLineEdit + ";")
        self.HMI.TextBox_MostrarValoresMaioresQue.setFont(self.HMI.font12)
        self.HMI.TextBox_MostrarValoresMaioresQue.returnPressed.connect(lambda: self.OnButtonPressed("MostrarValoresMaioresQue"))

        self.HMI.Button_VisaoGeral = QPushButton('Visão Geral')
        self.HMI.Button_VisaoGeral.pressed.connect(lambda: self.OnButtonPressed('Visão Geral'))
        self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
        self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
        self.HMI.Button_VisaoGeral.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_AtivoPorCorretora = QPushButton('Ativo por corretora')
        self.HMI.Button_AtivoPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Ativo por corretora'))
        self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AtivoPorCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_TotalDeUserCoinPorCorretora = QPushButton('Total de ' + UserCoin + ' por corretora')
        self.HMI.Button_TotalDeUserCoinPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Total de UserCoin por corretora'))
        self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_TotalDeUserCoinPorCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Setor = QPushButton('Por setor')
        self.HMI.Button_Setor.pressed.connect(lambda: self.OnButtonPressed('Ativo por setor'))
        self.HMI.Button_Setor.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_Setor.setFont(self.HMI.font16)
        self.HMI.Button_Setor.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.ComboBox_Ativos = QComboBox()
        self.HMI.ComboBox_Ativos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Ativos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.ComboBox_Ativos.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        self.HMI.ComboBox_Ativos.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        self.ativos, self.volume = self.HMI.DBManager.GetAllAtivosPorTipoDeAtivo_Bolsa(TipoDeAtivo="Caixa")
        self.ativos = sorted(self.ativos)

        if sum(self.volume) > 0:
            self.HMI.ComboBox_Ativos.addItem("Todos")
            for idx, ativo in enumerate(self.ativos): self.HMI.ComboBox_Ativos.addItem(ativo)
        else:
            self.HMI.ComboBox_Ativos.addItem("Vazio")
        self.HMI.ComboBox_Ativos.setCurrentIndex(0)

        self.Custo = 0
        for ativo in self.ativos: self.Custo += self.HMI.DBManager.GetCustoAtivo(ativo, "Bolsa")  # Calcula a soma dos custos de TODOS os ativos

        self.HMI.TextBox_Custo = QLineEdit()
        self.HMI.TextBox_Custo.setFixedWidth(int(self.HMI.frameGeometry().width() / 5 * 0.9))
        self.HMI.TextBox_Custo.setStyleSheet('QLineEdit {background-color: black; color: white;}')
        self.HMI.TextBox_Custo.setFont(self.HMI.font16)
        self.HMI.TextBox_Custo.setEnabled(False)
        self.HMI.TextBox_Custo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.HMI.ShowValues:
            self.HMI.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.Custo, 2):.2f}'))
        else:
            self.HMI.TextBox_Custo.setText('Custo: X')

        self.Retorno = 0
        for ativo in self.ativos: self.Retorno += self.HMI.DBManager.GetEstoqueAtivo(ativo, "Bolsa") * self.HMI.DBManager.GetCotacao(ativo)

        self.HMI.TextBox_Retorno = QLineEdit()
        self.HMI.TextBox_Retorno.setFixedWidth(int(self.HMI.frameGeometry().width() / 5 * 0.9))
        self.HMI.TextBox_Retorno.setFont(self.HMI.font16)
        self.HMI.TextBox_Retorno.setEnabled(False)
        self.HMI.TextBox_Retorno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.HMI.ShowValues: self.HMI.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.Retorno, 2):.2f}'))
        else: self.HMI.TextBox_Retorno.setText('Retorno: ' + str(round((self.Retorno - self.Custo) / self.Custo * 100, 1)) + '%X')
        if self.Retorno >= self.Custo: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

        self.MainGraphIsShowing = "Visão Geral"
        self.HMI.GraphWidget_MainGraph = self.CreateGraph_Page48_MainGraph_VisaoGeral()

        self.HMI.GraphWidget_Subtipos = self.CreateGraph_Page48_Subtipos()

        if self.HMI.ComboBox_Ativos.currentText() == "Vazio":
            self.HMI.Button_Setor.setEnabled(False)
            self.HMI.Button_AtivoPorCorretora.setEnabled(False)

        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(Background_2, 1, 0, 9, 3)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_MostrarValoresMaioresQue, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_MostrarValoresMaioresQue, 2, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_VisaoGeral, 4, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_Setor, 6, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.ComboBox_Ativos, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Custo, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Retorno, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_AtivoPorCorretora, 4, 2, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.TextBox_MostrarValoresMaioresQue.clearFocus()


    def CreatePage49(self): # Página Ativos Internacionais
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()

        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: black")
        Background_1.setFixedHeight(int(self.HMI.screen_height*1/24))

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: black")

        self.HMI.Label_Titulo = QLabel('ARCA: Ativos Internacionais')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_MostrarValoresMaioresQue = QLabel('Mostrar em '+UserCoin+'\nvalores maiores que')
        self.HMI.Label_MostrarValoresMaioresQue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.Label_MostrarValoresMaioresQue.setStyleSheet('color: white')
        self.HMI.Label_MostrarValoresMaioresQue.setFont(self.HMI.font12)

        self.HMI.TextBox_MostrarValoresMaioresQue = QLineEdit(str(self.MostrarValoresMaioresQue))
        self.HMI.TextBox_MostrarValoresMaioresQue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_MostrarValoresMaioresQue.setFixedWidth(int(self.HMI.frameGeometry().width()/20))
        self.HMI.TextBox_MostrarValoresMaioresQue.setStyleSheet("background-color: black; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_MostrarValoresMaioresQue.setFont(self.HMI.font12)
        self.HMI.TextBox_MostrarValoresMaioresQue.returnPressed.connect(lambda: self.OnButtonPressed("MostrarValoresMaioresQue"))

        self.HMI.Button_VisaoGeral = QPushButton('Visão Geral')
        self.HMI.Button_VisaoGeral.pressed.connect(lambda: self.OnButtonPressed('Visão Geral'))
        self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
        self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
        self.HMI.Button_VisaoGeral.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_AtivoPorCorretora = QPushButton('Ativo por corretora')
        self.HMI.Button_AtivoPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Ativo por corretora'))
        self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AtivoPorCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_TotalDeUserCoinPorCorretora = QPushButton('Total de '+UserCoin+' por corretora')
        self.HMI.Button_TotalDeUserCoinPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Total de UserCoin por corretora'))
        self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_TotalDeUserCoinPorCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Setor = QPushButton('Por setor')
        self.HMI.Button_Setor.pressed.connect(lambda: self.OnButtonPressed('Ativo por setor'))
        self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_Setor.setFont(self.HMI.font16)
        self.HMI.Button_Setor.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.ComboBox_Ativos = QComboBox()
        self.HMI.ComboBox_Ativos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Ativos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.ComboBox_Ativos.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        self.HMI.ComboBox_Ativos.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        self.ativos, self.volume = self.HMI.DBManager.GetAllAtivosPorTipoDeAtivo_Bolsa(TipoDeAtivo = "Ativos Internacionais")
        self.ativos.append("Criptos")
        Labels_2, Values_2 = self.HMI.DBManager.GetDetailedDataForCriptomoedas()
        Values_2_SumTotal = sum([x[0] + x[1] + x[2] for x in Values_2])
        self.volume.append(Values_2_SumTotal)

        # Ordenar
        ParaOrdenar = []
        for i, ativo in enumerate(self.ativos):
            ParaOrdenar.append((ativo,self.volume[i]))
        Ordenado = sorted(ParaOrdenar, key=lambda tup: tup[1])
        self.ativos = list(map(lambda tup: tup[0], Ordenado))
        self.volume = list(map(lambda tup: tup[1], Ordenado))
        self.ativos = sorted(self.ativos)

        if sum(self.volume)>0:
            self.HMI.ComboBox_Ativos.addItem("Todos")
            for idx, ativo in enumerate(self.ativos): self.HMI.ComboBox_Ativos.addItem(ativo)
        else:
            self.HMI.ComboBox_Ativos.addItem("Vazio")
        self.HMI.ComboBox_Ativos.setCurrentIndex(0)

        self.Custo = 0
        coins = self.HMI.DBManager.GetAllAtivos_Cripto()
        for ativo in self.ativos: self.Custo += self.HMI.DBManager.GetCustoAtivo(ativo, "Bolsa") # Calcula a soma dos custos de TODOS os ativos
        for ativo in coins: self.Custo += self.HMI.DBManager.GetCustoAtivo(ativo, "Cripto")

        self.HMI.TextBox_Custo = QLineEdit()
        self.HMI.TextBox_Custo.setFixedWidth(int(self.HMI.frameGeometry().width()/5*0.9))
        self.HMI.TextBox_Custo.setStyleSheet('QLineEdit {background-color: black; color: white;}')
        self.HMI.TextBox_Custo.setFont(self.HMI.font16)
        self.HMI.TextBox_Custo.setEnabled(False)
        self.HMI.TextBox_Custo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.HMI.ShowValues: self.HMI.TextBox_Custo.setText('Custo: '+UserCoin+' '+str(f'{round(self.Custo, 2):.2f}'))
        else: self.HMI.TextBox_Custo.setText('Custo: X')

        self.Retorno = 0
        for ativo in self.ativos: self.Retorno += self.HMI.DBManager.GetEstoqueAtivo(ativo, "Bolsa") * self.HMI.DBManager.GetCotacao(ativo)
        for ativo in coins: self.Retorno += self.HMI.DBManager.GetEstoqueAtivo(ativo, "Cripto") * self.HMI.DBManager.GetCotacao(ativo)

        self.HMI.TextBox_Retorno = QLineEdit()
        self.HMI.TextBox_Retorno.setFixedWidth(int(self.HMI.frameGeometry().width()/5*0.9))
        self.HMI.TextBox_Retorno.setFont(self.HMI.font16)
        self.HMI.TextBox_Retorno.setEnabled(False)
        self.HMI.TextBox_Retorno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.HMI.ShowValues: self.HMI.TextBox_Retorno.setText('Retorno: '+UserCoin+' '+str(f'{round(self.Retorno, 2):.2f}'))
        else: self.HMI.TextBox_Retorno.setText('Retorno: '+str(round((self.Retorno-self.Custo)/self.Custo*100,1))+'%X')
        if self.Retorno >= self.Custo: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

        self.HMI.Button_VerCriptomoedas = QPushButton('Ver criptomoedas ->')
        self.HMI.Button_VerCriptomoedas.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['CriptoARCA'].page_id))
        self.HMI.Button_VerCriptomoedas.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_VerCriptomoedas.setFont(QFont('Agency FB', 16))
        self.HMI.Button_VerCriptomoedas.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.MainGraphIsShowing = "Visão Geral"
        self.HMI.GraphWidget_MainGraph = self.CreateGraph_Page49_MainGraph_VisaoGeral()

        self.HMI.GraphWidget_Subtipos = self.CreateGraph_Page49_Subtipos()

        if self.HMI.ComboBox_Ativos.currentText() == "Vazio":
            self.HMI.Button_Setor.setEnabled(False)
            self.HMI.Button_AtivoPorCorretora.setEnabled(False)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 9, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_MostrarValoresMaioresQue, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_MostrarValoresMaioresQue, 2, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_VisaoGeral, 4, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_Ativos, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Custo, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Retorno, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Setor, 6, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AtivoPorCorretora, 4, 2, 2, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_VerCriptomoedas, 6, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.TextBox_MostrarValoresMaioresQue.clearFocus()


    def CreatePage50(self): # Página Criptomoedas
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()

        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: black")
        Background_1.setFixedHeight(int(self.HMI.screen_height*1/24))

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: black")

        self.HMI.Label_Titulo = QLabel('ARCA: Criptomoedas')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_MostrarValoresMaioresQue = QLabel('Mostrar em '+UserCoin+'\nvalores maiores que')
        self.HMI.Label_MostrarValoresMaioresQue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.Label_MostrarValoresMaioresQue.setStyleSheet('color: white')
        self.HMI.Label_MostrarValoresMaioresQue.setFont(self.HMI.font12)

        self.HMI.TextBox_MostrarValoresMaioresQue = QLineEdit(str(self.MostrarValoresMaioresQue))
        self.HMI.TextBox_MostrarValoresMaioresQue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_MostrarValoresMaioresQue.setFixedWidth(int(self.HMI.frameGeometry().width()/20))
        self.HMI.TextBox_MostrarValoresMaioresQue.setStyleSheet("background-color: black; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_MostrarValoresMaioresQue.setFont(self.HMI.font12)
        self.HMI.TextBox_MostrarValoresMaioresQue.returnPressed.connect(lambda: self.OnButtonPressed("MostrarValoresMaioresQue"))

        self.HMI.Button_VisaoGeral = QPushButton('Visão Geral')
        self.HMI.Button_VisaoGeral.pressed.connect(lambda: self.OnButtonPressed('Visão Geral'))
        self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
        self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
        self.HMI.Button_VisaoGeral.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_AtivoPorCorretora = QPushButton('Ativo por corretora')
        self.HMI.Button_AtivoPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Ativo por corretora'))
        self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AtivoPorCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_TotalDeUserCoinPorCorretora = QPushButton('Total de '+UserCoin+' por corretora')
        self.HMI.Button_TotalDeUserCoinPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Total de UserCoin por corretora'))
        self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_TotalDeUserCoinPorCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.ComboBox_Ativos = QComboBox()
        self.HMI.ComboBox_Ativos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Ativos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.ComboBox_Ativos.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        self.HMI.ComboBox_Ativos.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        self.ativos = self.HMI.DBManager.GetAllAtivos_Cripto()
        if len(self.ativos) > 0:
            self.HMI.ComboBox_Ativos.addItem("Todos")
            for idx, ativo in enumerate(self.ativos): self.HMI.ComboBox_Ativos.addItem(ativo)
        else: self.HMI.ComboBox_Ativos.addItem("Vazio")
        self.HMI.ComboBox_Ativos.setCurrentIndex(0)

        self.Custo = 0
        for ativo in self.ativos: self.Custo += self.HMI.DBManager.GetCustoAtivo(ativo, "Cripto")

        self.HMI.TextBox_Custo = QLineEdit()
        self.HMI.TextBox_Custo.setFixedWidth(int(self.HMI.frameGeometry().width()/5*0.9))
        self.HMI.TextBox_Custo.setStyleSheet('QLineEdit {background-color: black; color: white;}')
        self.HMI.TextBox_Custo.setFont(self.HMI.font16)
        self.HMI.TextBox_Custo.setEnabled(False)
        self.HMI.TextBox_Custo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.HMI.ShowValues: self.HMI.TextBox_Custo.setText('Custo: '+UserCoin+' '+str(f'{round(self.Custo, 2):.2f}'))
        else: self.HMI.TextBox_Custo.setText('Custo: X')

        self.Retorno = 0
        for ativo in self.ativos:
            self.Retorno += self.HMI.DBManager.GetEstoqueAtivo(ativo, "Cripto") * self.HMI.DBManager.GetCotacao(ativo)

        self.HMI.TextBox_Retorno = QLineEdit()
        self.HMI.TextBox_Retorno.setFixedWidth(int(self.HMI.frameGeometry().width()/5*0.9))
        self.HMI.TextBox_Retorno.setFont(self.HMI.font16)
        self.HMI.TextBox_Retorno.setEnabled(False)
        self.HMI.TextBox_Retorno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.HMI.ShowValues: self.HMI.TextBox_Retorno.setText('Retorno: '+UserCoin+' '+str(f'{round(self.Retorno, 2):.2f}'))
        else: self.HMI.TextBox_Retorno.setText('Retorno: '+str(round((self.Retorno-self.Custo)/self.Custo*100,1))+'%X')
        if self.Retorno >= self.Custo: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

        self.HMI.Button_VerAtivosInternacionais = QPushButton('Ver ativos internacionais ->')
        self.HMI.Button_VerAtivosInternacionais.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['AtivosInternacionais'].page_id))
        self.HMI.Button_VerAtivosInternacionais.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_VerAtivosInternacionais.setFont(QFont('Agency FB', 16))
        self.HMI.Button_VerAtivosInternacionais.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.MainGraphIsShowing = "Visão Geral"
        self.HMI.GraphWidget_MainGraph = self.CreateGraph_Page50_MainGraph_VisaoGeral()

        self.HMI.GraphWidget_Distribuicao = self.CreateGraph_Page50_Distribuicao()

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 9, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_MostrarValoresMaioresQue, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_MostrarValoresMaioresQue, 2, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_VisaoGeral, 3, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_TotalDeUserCoinPorCorretora, 6, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_Ativos, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Custo, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Retorno, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AtivoPorCorretora, 4, 2, 2, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_VerAtivosInternacionais, 6, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_Distribuicao, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.TextBox_MostrarValoresMaioresQue.clearFocus()
