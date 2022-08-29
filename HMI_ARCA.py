# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:55:20 2021

@author: caiop
"""
from BackgroundProcesses import WorkerThread

import time
from copy import copy

import numpy as np
import pandas as pd

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class HMI_ARCA(object):
    def __init__(self, HMI):
        self.HMI = HMI
        self.Flag_RecalcularGraficos = True
        self.GraficoEspecifico_Name = ""
        self.MontanteEmAplicacao = 0
        self.MostrarValoresMaioresQue = 1

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
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Subtitulo1 = QPushButton('Ações e negócios')
        self.HMI.Label_Subtitulo1.pressed.connect(lambda: self.HMI.CreatePage('Info24'))
        self.HMI.Label_Subtitulo1.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: transparent; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo1.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo2 = QPushButton('Real Estate')
        self.HMI.Label_Subtitulo2.pressed.connect(lambda: self.HMI.CreatePage('Info25'))
        self.HMI.Label_Subtitulo2.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: transparent; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo2.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo3 = QPushButton('Caixa')
        self.HMI.Label_Subtitulo3.pressed.connect(lambda: self.HMI.CreatePage('Info26'))
        self.HMI.Label_Subtitulo3.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: transparent; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo3.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo4 = QPushButton('Ativos internacionais')
        self.HMI.Label_Subtitulo4.pressed.connect(lambda: self.HMI.CreatePage('Info27'))
        self.HMI.Label_Subtitulo4.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: transparent; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo4.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo5 = QPushButton()
        self.HMI.Label_Subtitulo5.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: transparent; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo5.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo1_ = QPushButton('Ações e negócios')
        self.HMI.Label_Subtitulo1_.pressed.connect(lambda: self.HMI.CreatePage('Info24'))
        self.HMI.Label_Subtitulo1_.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo1_.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo2_ = QPushButton('Real Estate')
        self.HMI.Label_Subtitulo2_.pressed.connect(lambda: self.HMI.CreatePage('Info25'))
        self.HMI.Label_Subtitulo2_.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo2_.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo3_ = QPushButton('Caixa')
        self.HMI.Label_Subtitulo3_.pressed.connect(lambda: self.HMI.CreatePage('Info26'))
        self.HMI.Label_Subtitulo3_.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo3_.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo4_ = QPushButton('Ativos internacionais')
        self.HMI.Label_Subtitulo4_.pressed.connect(lambda: self.HMI.CreatePage('Info27'))
        self.HMI.Label_Subtitulo4_.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Label_Subtitulo4_.setFont(self.HMI.font16)

        self.HMI.Label_Subtitulo5_ = QPushButton()
        self.HMI.Label_Subtitulo5_.pressed.connect(lambda: self.HMI.CreatePage('Info28'))
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
        self.HMI.Button_Msg3.pressed.connect(lambda: self.HMI.CreatePage('Info21'))
        self.HMI.Button_Msg3.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg3.setFont(self.HMI.font12)

        self.HMI.TextBox_MontanteEmAplicacao = QLineEdit('Calculando...')
        self.HMI.TextBox_MontanteEmAplicacao.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_MontanteEmAplicacao.setFixedWidth(int(self.HMI.frameGeometry().width()/6))
        self.HMI.TextBox_MontanteEmAplicacao.setStyleSheet("background-color: black; color: orange;")
        self.HMI.TextBox_MontanteEmAplicacao.setFont(self.HMI.font12)
        self.HMI.TextBox_MontanteEmAplicacao.setEnabled(False)

        self.HMI.Button_Msg4 = QPushButton('Montante aplicado\n('+self.HMI.DBManager.GetUserCoinCurrency()+")")
        self.HMI.Button_Msg4.pressed.connect(lambda: self.HMI.CreatePage('Info20'))
        self.HMI.Button_Msg4.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg4.setFont(self.HMI.font12)

        self.HMI.TextBox_MontanteAplicado = QLineEdit(str('%.2f' % round(self.HMI.DBManager.GetMontanteAplicado(),2)))
        self.HMI.TextBox_MontanteAplicado.setAlignment(Qt.AlignCenter)
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
            self.HMI.setCursor(Qt.WaitCursor)
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
        self.HMI.Button_AcoesENegociosInvisivel.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_RealEstateInvisivel = QPushButton()
        self.HMI.Button_RealEstateInvisivel.pressed.connect(lambda: self.ProximoGraficoEspecifico("Real Estate"))
        self.HMI.Button_RealEstateInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_RealEstateInvisivel.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_CaixaInvisivel = QPushButton()
        self.HMI.Button_CaixaInvisivel.pressed.connect(lambda: self.ProximoGraficoEspecifico("Caixa"))
        self.HMI.Button_CaixaInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_CaixaInvisivel.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_AcoesInternacionaisInvisivel = QPushButton()
        self.HMI.Button_AcoesInternacionaisInvisivel.pressed.connect(lambda: self.ProximoGraficoEspecifico("Ativos Internacionais"))
        self.HMI.Button_AcoesInternacionaisInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_AcoesInternacionaisInvisivel.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_EspecificaInvisivel = QPushButton()
        self.HMI.Button_EspecificaInvisivel.pressed.connect(lambda: self.CallCreatePage())
        self.HMI.Button_EspecificaInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_EspecificaInvisivel.setCursor(QCursor(Qt.PointingHandCursor))

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
        self.HMI.Button_CarteiraInvisivel.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Msg1 = QPushButton('Nota de equilíbrio: ???/100')
        self.HMI.Button_Msg1.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg1.pressed.connect(lambda: self.HMI.CreatePage('Info16'))
        self.HMI.Button_Msg1.setFont(self.HMI.font12)

        self.HMI.Button_Msg5 = QPushButton('Gasto mensal\n('+self.HMI.DBManager.GetUserCoinCurrency()+")")
        self.HMI.Button_Msg5.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg5.pressed.connect(lambda: self.HMI.CreatePage('Info17'))
        self.HMI.Button_Msg5.setFont(self.HMI.font12)

        self.HMI.Button_Msg6 = QPushButton('Meses de\nreserva')
        self.HMI.Button_Msg6.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg6.pressed.connect(lambda: self.HMI.CreatePage('Info18'))
        self.HMI.Button_Msg6.setFont(self.HMI.font12)

        self.HMI.Button_Msg7 = QPushButton('Aplicar\n('+self.HMI.DBManager.GetUserCoinCurrency()+")")
        self.HMI.Button_Msg7.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_Msg7.pressed.connect(lambda: self.HMI.CreatePage('Info19'))
        self.HMI.Button_Msg7.setFont(self.HMI.font12)

        self.HMI.Label_Msg8 = QLabel('Reserva:')
        self.HMI.Label_Msg8.setStyleSheet('color: white')
        self.HMI.Label_Msg8.setFont(self.HMI.font12)
        self.HMI.Label_Msg8.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg9 = QLabel('        ') # Espaço vazio que serve para ficar centralizado o restante das informações
        self.HMI.Label_Msg9.setStyleSheet('color: white')
        self.HMI.Label_Msg9.setFont(self.HMI.font12)
        self.HMI.Label_Msg9.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_GastoMensal = QLineEdit(str('%.2f' % self.HMI.DBManager.GetGastoMensal()))
        self.HMI.TextBox_GastoMensal.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_GastoMensal.setFixedWidth(int(self.HMI.frameGeometry().width()/10))
        self.HMI.TextBox_GastoMensal.setStyleSheet("background-color: black; color: white;")
        self.HMI.TextBox_GastoMensal.setFont(self.HMI.font12)
        self.HMI.TextBox_GastoMensal.returnPressed.connect(lambda: self.OnButtonPressed("TextBox_GastoMensal"))

        self.HMI.TextBox_MesesDeReserva = QLineEdit(str(int(self.HMI.DBManager.GetMesesDeReserva())))
        self.HMI.TextBox_MesesDeReserva.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_MesesDeReserva.setFixedWidth(int(self.HMI.frameGeometry().width()/20))
        self.HMI.TextBox_MesesDeReserva.setStyleSheet("background-color: black; color: white;")
        self.HMI.TextBox_MesesDeReserva.setFont(self.HMI.font12)
        self.HMI.TextBox_MesesDeReserva.returnPressed.connect(lambda: self.OnButtonPressed("TextBox_MesesDeReserva"))

        self.HMI.TextBox_Aplicar = QLineEdit()
        self.HMI.TextBox_Aplicar.setStyleSheet("background-color: black; color: orange;")
        self.HMI.TextBox_Aplicar.setText('Calculando...')
        self.HMI.TextBox_Aplicar.setAlignment(Qt.AlignCenter)
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
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 6, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Graficos_Subtipos, 1, 0, 1, 6, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Graficos_Subtipos_Invisiveis, 1, 0, 1, 6, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Reserva, 2, 0, 1, 2, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Montantes, 3, 0, 2, 2, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_Carteira, 2, 2, 2, 2, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_CarteiraInvisivel, 2, 2, 2, 2, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Msg1, 4, 2, 1, 2, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.Table_ContasCorrenteHeader, 2, 4, 1, 2, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.Table_ContasCorrente, 3, 4, 2, 2, Qt.AlignHCenter | Qt.AlignTop)

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
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_MostrarValoresMaioresQue = QLabel('Mostrar em ' + UserCoin + '\nvalores maiores que')
        self.HMI.Label_MostrarValoresMaioresQue.setAlignment(Qt.AlignCenter)
        self.HMI.Label_MostrarValoresMaioresQue.setStyleSheet('color: white')
        self.HMI.Label_MostrarValoresMaioresQue.setFont(self.HMI.font12)

        self.HMI.TextBox_MostrarValoresMaioresQue = QLineEdit(str(self.MostrarValoresMaioresQue))
        self.HMI.TextBox_MostrarValoresMaioresQue.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_MostrarValoresMaioresQue.setFixedWidth(int(self.HMI.frameGeometry().width() / 20))
        self.HMI.TextBox_MostrarValoresMaioresQue.setStyleSheet("background-color: black; color: " + FontColorLineEdit + ";")
        self.HMI.TextBox_MostrarValoresMaioresQue.setFont(self.HMI.font12)
        self.HMI.TextBox_MostrarValoresMaioresQue.returnPressed.connect(lambda: self.OnButtonPressed("MostrarValoresMaioresQue"))

        self.HMI.Button_VisaoGeral = QPushButton('Visão Geral')
        self.HMI.Button_VisaoGeral.pressed.connect(lambda: self.OnButtonPressed('Visão Geral'))
        self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
        self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
        self.HMI.Button_VisaoGeral.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_AtivoPorCorretora = QPushButton('Ativo por corretora')
        self.HMI.Button_AtivoPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Ativo por corretora'))
        self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AtivoPorCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_TotalDeUserCoinPorCorretora = QPushButton('Total de ' + UserCoin + ' por corretora')
        self.HMI.Button_TotalDeUserCoinPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Total de UserCoin por corretora'))
        self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_TotalDeUserCoinPorCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Setor = QPushButton('Por setor')
        self.HMI.Button_Setor.pressed.connect(lambda: self.OnButtonPressed('Ativo por setor'))
        self.HMI.Button_Setor.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_Setor.setFont(self.HMI.font16)
        self.HMI.Button_Setor.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.ComboBox_Ativos = QComboBox()
        self.HMI.ComboBox_Ativos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Ativos.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.HMI.TextBox_Custo.setAlignment(Qt.AlignCenter)
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
        self.HMI.TextBox_Retorno.setAlignment(Qt.AlignCenter)
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
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_MostrarValoresMaioresQue, 1, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_MostrarValoresMaioresQue, 2, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_VisaoGeral, 4, 0, 2, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_Setor, 6, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.ComboBox_Ativos, 1, 2, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Custo, 2, 2, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Retorno, 3, 2, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_AtivoPorCorretora, 4, 2, 2, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignCenter | Qt.AlignBottom)
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
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_MostrarValoresMaioresQue = QLabel('Mostrar em ' + UserCoin + '\nvalores maiores que')
        self.HMI.Label_MostrarValoresMaioresQue.setAlignment(Qt.AlignCenter)
        self.HMI.Label_MostrarValoresMaioresQue.setStyleSheet('color: white')
        self.HMI.Label_MostrarValoresMaioresQue.setFont(self.HMI.font12)

        self.HMI.TextBox_MostrarValoresMaioresQue = QLineEdit(str(self.MostrarValoresMaioresQue))
        self.HMI.TextBox_MostrarValoresMaioresQue.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_MostrarValoresMaioresQue.setFixedWidth(int(self.HMI.frameGeometry().width() / 20))
        self.HMI.TextBox_MostrarValoresMaioresQue.setStyleSheet("background-color: black; color: " + FontColorLineEdit + ";")
        self.HMI.TextBox_MostrarValoresMaioresQue.setFont(self.HMI.font12)
        self.HMI.TextBox_MostrarValoresMaioresQue.returnPressed.connect(lambda: self.OnButtonPressed("MostrarValoresMaioresQue"))

        self.HMI.Button_VisaoGeral = QPushButton('Visão Geral')
        self.HMI.Button_VisaoGeral.pressed.connect(lambda: self.OnButtonPressed('Visão Geral'))
        self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
        self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
        self.HMI.Button_VisaoGeral.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_AtivoPorCorretora = QPushButton('Ativo por corretora')
        self.HMI.Button_AtivoPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Ativo por corretora'))
        self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AtivoPorCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_TotalDeUserCoinPorCorretora = QPushButton('Total de ' + UserCoin + ' por corretora')
        self.HMI.Button_TotalDeUserCoinPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Total de UserCoin por corretora'))
        self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_TotalDeUserCoinPorCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Setor = QPushButton('Por setor')
        self.HMI.Button_Setor.pressed.connect(lambda: self.OnButtonPressed('Ativo por setor'))
        self.HMI.Button_Setor.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_Setor.setFont(self.HMI.font16)
        self.HMI.Button_Setor.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.ComboBox_Ativos = QComboBox()
        self.HMI.ComboBox_Ativos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Ativos.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.HMI.TextBox_Custo.setAlignment(Qt.AlignCenter)
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
        self.HMI.TextBox_Retorno.setAlignment(Qt.AlignCenter)
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
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_MostrarValoresMaioresQue, 1, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_MostrarValoresMaioresQue, 2, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_VisaoGeral, 4, 0, 2, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_Setor, 6, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.ComboBox_Ativos, 1, 2, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Custo, 2, 2, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Retorno, 3, 2, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_AtivoPorCorretora, 4, 2, 2, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignCenter | Qt.AlignBottom)
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
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_MostrarValoresMaioresQue = QLabel('Mostrar em ' + UserCoin + '\nvalores maiores que')
        self.HMI.Label_MostrarValoresMaioresQue.setAlignment(Qt.AlignCenter)
        self.HMI.Label_MostrarValoresMaioresQue.setStyleSheet('color: white')
        self.HMI.Label_MostrarValoresMaioresQue.setFont(self.HMI.font12)

        self.HMI.TextBox_MostrarValoresMaioresQue = QLineEdit(str(self.MostrarValoresMaioresQue))
        self.HMI.TextBox_MostrarValoresMaioresQue.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_MostrarValoresMaioresQue.setFixedWidth(int(self.HMI.frameGeometry().width() / 20))
        self.HMI.TextBox_MostrarValoresMaioresQue.setStyleSheet("background-color: black; color: " + FontColorLineEdit + ";")
        self.HMI.TextBox_MostrarValoresMaioresQue.setFont(self.HMI.font12)
        self.HMI.TextBox_MostrarValoresMaioresQue.returnPressed.connect(lambda: self.OnButtonPressed("MostrarValoresMaioresQue"))

        self.HMI.Button_VisaoGeral = QPushButton('Visão Geral')
        self.HMI.Button_VisaoGeral.pressed.connect(lambda: self.OnButtonPressed('Visão Geral'))
        self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
        self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
        self.HMI.Button_VisaoGeral.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_AtivoPorCorretora = QPushButton('Ativo por corretora')
        self.HMI.Button_AtivoPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Ativo por corretora'))
        self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AtivoPorCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_TotalDeUserCoinPorCorretora = QPushButton('Total de ' + UserCoin + ' por corretora')
        self.HMI.Button_TotalDeUserCoinPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Total de UserCoin por corretora'))
        self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_TotalDeUserCoinPorCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Setor = QPushButton('Por setor')
        self.HMI.Button_Setor.pressed.connect(lambda: self.OnButtonPressed('Ativo por setor'))
        self.HMI.Button_Setor.setStyleSheet("background-color: black; color: " + FontColorLineEdit + "; outline: none;")
        self.HMI.Button_Setor.setFont(self.HMI.font16)
        self.HMI.Button_Setor.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.ComboBox_Ativos = QComboBox()
        self.HMI.ComboBox_Ativos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Ativos.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.HMI.TextBox_Custo.setAlignment(Qt.AlignCenter)
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
        self.HMI.TextBox_Retorno.setAlignment(Qt.AlignCenter)
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
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Label_MostrarValoresMaioresQue, 1, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_MostrarValoresMaioresQue, 2, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_VisaoGeral, 4, 0, 2, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_Setor, 6, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.ComboBox_Ativos, 1, 2, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Custo, 2, 2, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.TextBox_Retorno, 3, 2, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.Button_AtivoPorCorretora, 4, 2, 2, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addWidget(self.HMI.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignCenter | Qt.AlignBottom)
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
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_MostrarValoresMaioresQue = QLabel('Mostrar em '+UserCoin+'\nvalores maiores que')
        self.HMI.Label_MostrarValoresMaioresQue.setAlignment(Qt.AlignCenter)
        self.HMI.Label_MostrarValoresMaioresQue.setStyleSheet('color: white')
        self.HMI.Label_MostrarValoresMaioresQue.setFont(self.HMI.font12)

        self.HMI.TextBox_MostrarValoresMaioresQue = QLineEdit(str(self.MostrarValoresMaioresQue))
        self.HMI.TextBox_MostrarValoresMaioresQue.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_MostrarValoresMaioresQue.setFixedWidth(int(self.HMI.frameGeometry().width()/20))
        self.HMI.TextBox_MostrarValoresMaioresQue.setStyleSheet("background-color: black; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_MostrarValoresMaioresQue.setFont(self.HMI.font12)
        self.HMI.TextBox_MostrarValoresMaioresQue.returnPressed.connect(lambda: self.OnButtonPressed("MostrarValoresMaioresQue"))

        self.HMI.Button_VisaoGeral = QPushButton('Visão Geral')
        self.HMI.Button_VisaoGeral.pressed.connect(lambda: self.OnButtonPressed('Visão Geral'))
        self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
        self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
        self.HMI.Button_VisaoGeral.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_AtivoPorCorretora = QPushButton('Ativo por corretora')
        self.HMI.Button_AtivoPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Ativo por corretora'))
        self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AtivoPorCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_TotalDeUserCoinPorCorretora = QPushButton('Total de '+UserCoin+' por corretora')
        self.HMI.Button_TotalDeUserCoinPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Total de UserCoin por corretora'))
        self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_TotalDeUserCoinPorCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Setor = QPushButton('Por setor')
        self.HMI.Button_Setor.pressed.connect(lambda: self.OnButtonPressed('Ativo por setor'))
        self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_Setor.setFont(self.HMI.font16)
        self.HMI.Button_Setor.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.ComboBox_Ativos = QComboBox()
        self.HMI.ComboBox_Ativos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Ativos.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.HMI.TextBox_Custo.setAlignment(Qt.AlignCenter)
        if self.HMI.ShowValues: self.HMI.TextBox_Custo.setText('Custo: '+UserCoin+' '+str(f'{round(self.Custo, 2):.2f}'))
        else: self.HMI.TextBox_Custo.setText('Custo: X')

        self.Retorno = 0
        for ativo in self.ativos: self.Retorno += self.HMI.DBManager.GetEstoqueAtivo(ativo, "Bolsa") * self.HMI.DBManager.GetCotacao(ativo)
        for ativo in coins: self.Retorno += self.HMI.DBManager.GetEstoqueAtivo(ativo, "Cripto") * self.HMI.DBManager.GetCotacao(ativo)

        self.HMI.TextBox_Retorno = QLineEdit()
        self.HMI.TextBox_Retorno.setFixedWidth(int(self.HMI.frameGeometry().width()/5*0.9))
        self.HMI.TextBox_Retorno.setFont(self.HMI.font16)
        self.HMI.TextBox_Retorno.setEnabled(False)
        self.HMI.TextBox_Retorno.setAlignment(Qt.AlignCenter)
        if self.HMI.ShowValues: self.HMI.TextBox_Retorno.setText('Retorno: '+UserCoin+' '+str(f'{round(self.Retorno, 2):.2f}'))
        else: self.HMI.TextBox_Retorno.setText('Retorno: '+str(round((self.Retorno-self.Custo)/self.Custo*100,1))+'%X')
        if self.Retorno >= self.Custo: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

        self.HMI.Button_VerCriptomoedas = QPushButton('Ver criptomoedas ->')
        self.HMI.Button_VerCriptomoedas.pressed.connect(lambda: self.HMI.CreatePage('50'))
        self.HMI.Button_VerCriptomoedas.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_VerCriptomoedas.setFont(QFont('Agency FB', 16))
        self.HMI.Button_VerCriptomoedas.setCursor(QCursor(Qt.PointingHandCursor))

        self.MainGraphIsShowing = "Visão Geral"
        self.HMI.GraphWidget_MainGraph = self.CreateGraph_Page49_MainGraph_VisaoGeral()

        self.HMI.GraphWidget_Subtipos = self.CreateGraph_Page49_Subtipos()

        if self.HMI.ComboBox_Ativos.currentText() == "Vazio":
            self.HMI.Button_Setor.setEnabled(False)
            self.HMI.Button_AtivoPorCorretora.setEnabled(False)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 9, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_MostrarValoresMaioresQue, 1, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_MostrarValoresMaioresQue, 2, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_VisaoGeral, 4, 0, 2, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_Ativos, 1, 2, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Custo, 2, 2, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Retorno, 3, 2, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Setor, 6, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AtivoPorCorretora, 4, 2, 2, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_VerCriptomoedas, 6, 2, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignCenter | Qt.AlignBottom)
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
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_MostrarValoresMaioresQue = QLabel('Mostrar em '+UserCoin+'\nvalores maiores que')
        self.HMI.Label_MostrarValoresMaioresQue.setAlignment(Qt.AlignCenter)
        self.HMI.Label_MostrarValoresMaioresQue.setStyleSheet('color: white')
        self.HMI.Label_MostrarValoresMaioresQue.setFont(self.HMI.font12)

        self.HMI.TextBox_MostrarValoresMaioresQue = QLineEdit(str(self.MostrarValoresMaioresQue))
        self.HMI.TextBox_MostrarValoresMaioresQue.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_MostrarValoresMaioresQue.setFixedWidth(int(self.HMI.frameGeometry().width()/20))
        self.HMI.TextBox_MostrarValoresMaioresQue.setStyleSheet("background-color: black; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_MostrarValoresMaioresQue.setFont(self.HMI.font12)
        self.HMI.TextBox_MostrarValoresMaioresQue.returnPressed.connect(lambda: self.OnButtonPressed("MostrarValoresMaioresQue"))

        self.HMI.Button_VisaoGeral = QPushButton('Visão Geral')
        self.HMI.Button_VisaoGeral.pressed.connect(lambda: self.OnButtonPressed('Visão Geral'))
        self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
        self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
        self.HMI.Button_VisaoGeral.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_AtivoPorCorretora = QPushButton('Ativo por corretora')
        self.HMI.Button_AtivoPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Ativo por corretora'))
        self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AtivoPorCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_TotalDeUserCoinPorCorretora = QPushButton('Total de '+UserCoin+' por corretora')
        self.HMI.Button_TotalDeUserCoinPorCorretora.pressed.connect(lambda: self.OnButtonPressed('Total de UserCoin por corretora'))
        self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
        self.HMI.Button_TotalDeUserCoinPorCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.ComboBox_Ativos = QComboBox()
        self.HMI.ComboBox_Ativos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Ativos.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.HMI.TextBox_Custo.setAlignment(Qt.AlignCenter)
        if self.HMI.ShowValues: self.HMI.TextBox_Custo.setText('Custo: '+UserCoin+' '+str(f'{round(self.Custo, 2):.2f}'))
        else: self.HMI.TextBox_Custo.setText('Custo: X')

        self.Retorno = 0
        for ativo in self.ativos:
            self.Retorno += self.HMI.DBManager.GetEstoqueAtivo(ativo, "Cripto") * self.HMI.DBManager.GetCotacao(ativo)

        self.HMI.TextBox_Retorno = QLineEdit()
        self.HMI.TextBox_Retorno.setFixedWidth(int(self.HMI.frameGeometry().width()/5*0.9))
        self.HMI.TextBox_Retorno.setFont(self.HMI.font16)
        self.HMI.TextBox_Retorno.setEnabled(False)
        self.HMI.TextBox_Retorno.setAlignment(Qt.AlignCenter)
        if self.HMI.ShowValues: self.HMI.TextBox_Retorno.setText('Retorno: '+UserCoin+' '+str(f'{round(self.Retorno, 2):.2f}'))
        else: self.HMI.TextBox_Retorno.setText('Retorno: '+str(round((self.Retorno-self.Custo)/self.Custo*100,1))+'%X')
        if self.Retorno >= self.Custo: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

        self.HMI.Button_VerAtivosInternacionais = QPushButton('Ver ativos internacionais ->')
        self.HMI.Button_VerAtivosInternacionais.pressed.connect(lambda: self.HMI.CreatePage('49'))
        self.HMI.Button_VerAtivosInternacionais.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
        self.HMI.Button_VerAtivosInternacionais.setFont(QFont('Agency FB', 16))
        self.HMI.Button_VerAtivosInternacionais.setCursor(QCursor(Qt.PointingHandCursor))

        self.MainGraphIsShowing = "Visão Geral"
        self.HMI.GraphWidget_MainGraph = self.CreateGraph_Page50_MainGraph_VisaoGeral()

        self.HMI.GraphWidget_Distribuicao = self.CreateGraph_Page50_Distribuicao()

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 9, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_MostrarValoresMaioresQue, 1, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_MostrarValoresMaioresQue, 2, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_VisaoGeral, 3, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_TotalDeUserCoinPorCorretora, 6, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_Ativos, 1, 2, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Custo, 2, 2, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Retorno, 3, 2, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AtivoPorCorretora, 4, 2, 2, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_VerAtivosInternacionais, 6, 2, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_Distribuicao, 7, 0, 3, 3, Qt.AlignCenter | Qt.AlignBottom)
        self.HMI.TextBox_MostrarValoresMaioresQue.clearFocus()

    def CreateGraph_Page11_Carteira_pie(self):
        self.CarteiraGraph_id = 'pie'
        def GetData():
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [0,0,0,0]
            else:
                RVn = self.Soma_AcoesENegocios
                RE = self.Soma_RealEstate
                Caixa = self.Soma_Caixa
                RVi = self.Soma_AtivosInternacionais
                return [RVn,RVi,Caixa,RE] # Ações e Negócios; Ativos Internacionais; Caixa; Real Estate
        self.GraphWidget_Carteira_Storage = plt.figure()
        self.GraphWidget_Carteira_Storage.clear()
        self.GraphWidget_Carteira_Storage.set_facecolor("black")
        data = GetData()
        if sum(data)==0: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if sum(data) > 0:
            plt.pie(data, startangle=90, shadow=True, normalize=normalize, explode=explode,
                    autopct = lambda pct: self.getPercentage(pct, data), colors=['orange','purple','green','blue'])
        else:
            plt.pie(data, startangle=90, shadow=True, normalize=normalize)
        plt.axis('equal')
        plt.tight_layout()

        GraphWidget = FigureCanvas(self.GraphWidget_Carteira_Storage)
        plt.close(self.GraphWidget_Carteira_Storage)
        self.Flag_RecalcularGraficos = False
        return GraphWidget

    def CreateGraph_Page11_Carteira_bar(self):
        self.CarteiraGraph_id = 'bar'
        def GetData():
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [0,0,0,0]
            else:
                RVn = self.Soma_AcoesENegocios
                RE = self.Soma_RealEstate
                Caixa = self.Soma_Caixa
                RVi = self.Soma_AtivosInternacionais
                return [RVn,RE,Caixa,RVi] # Ações e Negócios; Real Estate; Caixa; Ativos Internacionais
        self.GraphWidget_Carteira_Storage, ax = plt.subplots()
        self.GraphWidget_Carteira_Storage.clear()
        self.GraphWidget_Carteira_Storage.set_facecolor("black")
        data = GetData()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        graph = plt.bar(list(range(len(data))), data, width=0.75, align='center', color=['orange','blue','green','purple'])

        percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Carteira_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Carteira_Storage)
        plt.close(self.GraphWidget_Carteira_Storage)
        return GraphWidget

    def CreateGraph_Page11_AcoesENegocios(self):
        def GetData():
            Acoes = 0
            Fundos = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Acoes,Fundos]
            else:
                Acoes,Fundos = self.HMI.DBManager.GetDataForAcoesENegocios()
                self.Soma_AcoesENegocios = sum([Acoes,Fundos])
                return [Acoes,Fundos]
        def GetLabels():
            return ['Ações','Fundos']
        self.GraphWidget_AcoesENegocios_Storage, ax = plt.subplots()
        self.GraphWidget_AcoesENegocios_Storage.clear()
        self.GraphWidget_AcoesENegocios_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        graph = plt.bar(list(range(len(data))), data, linewidth=4, edgecolor='orange', width=0.75, align='center', color='orange')
        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if sum(data)>0: percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else: percentage = list(map(lambda x: round(0,1), data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_AcoesENegocios_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_AcoesENegocios_Storage)
        plt.close(self.GraphWidget_AcoesENegocios_Storage)
        return GraphWidget

    def CreateGraph_Page11_RealEstate(self):
        def GetData():
            Terrenos = 0
            Construcoes = 0
            Fundos = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Terrenos,Construcoes,Fundos]
            else:
                Terrenos,Construcoes,Fundos = self.HMI.DBManager.GetDataForRealEstate()
                self.Soma_RealEstate = sum([Terrenos,Construcoes,Fundos])
                return [Terrenos,Construcoes,Fundos]
        def GetLabels():
            return ['Terren.','Constr.','Fundos']
        self.GraphWidget_RealEstate_Storage, ax = plt.subplots()
        self.GraphWidget_RealEstate_Storage.clear()
        self.GraphWidget_RealEstate_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        graph = plt.bar(list(range(len(data))), data, linewidth=4, edgecolor='blue', width=0.75, align='center', color='blue')
        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if sum(data) > 0:
            percentage = list(map(lambda x: round(x / sum(data) * 100, 1), data))
        else:
            percentage = list(map(lambda x: round(0, 1), data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_RealEstate_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_RealEstate_Storage)
        plt.close(self.GraphWidget_RealEstate_Storage)
        return GraphWidget

    def CreateGraph_Page11_Caixa(self):
        def GetData():
            RF = 0
            TD_TP = 0
            PP = 0
            COE = 0
            Fundos = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [RF,TD_TP,PP,COE,Fundos]
            else:
                RF,TD_TP,PP,COE,Fundos = self.HMI.DBManager.GetDataForCaixa()
                self.Soma_Caixa = sum([RF,TD_TP,PP,COE,Fundos])
                return [RF,TD_TP,PP,COE,Fundos]
        def GetLabels():
            return ['RF','TD/TP','PP','COE','Fundos']
        self.GraphWidget_Caixa_Storage, ax = plt.subplots()
        self.GraphWidget_Caixa_Storage.clear()
        self.GraphWidget_Caixa_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        graph = plt.bar(list(range(len(data))), data, linewidth=4, edgecolor='green', width=0.75, align='center', color='green')
        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if sum(data) > 0:
            percentage = list(map(lambda x: round(x / sum(data) * 100, 1), data))
        else:
            percentage = list(map(lambda x: round(0, 1), data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Caixa_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Caixa_Storage)
        plt.close(self.GraphWidget_Caixa_Storage)
        return GraphWidget

    def CreateGraph_Page11_AtivosInternacionais(self):
        def GetData():
            BDR = 0
            Fundos = 0
            Cripto = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [BDR,Fundos,Cripto]
            else:
                BDR,Fundos = self.HMI.DBManager.GetDataForAtivosInternacionais()
                Top1,Top2,Top3,Outras = self.HMI.DBManager.GetDataForCriptomoedas()
                self.Soma_Criptomoedas = sum([Top1,Top2,Top3,Outras])
                Cripto = self.Soma_Criptomoedas
                self.Soma_AtivosInternacionais = sum([BDR,Fundos,Cripto])
                return [BDR,Fundos,Cripto]
        def GetLabels():
            return ['BDR','Fundos','Cripto']
        self.GraphWidget_AtivosInternacionais_Storage, ax = plt.subplots()
        self.GraphWidget_AtivosInternacionais_Storage.clear()
        self.GraphWidget_AtivosInternacionais_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='purple', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='purple', align='center', color='purple')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_AtivosInternacionais_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_AtivosInternacionais_Storage)
        plt.close(self.GraphWidget_AtivosInternacionais_Storage)
        return GraphWidget

    def CreateGraph_Page11_AcoesNacionais(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Ações e Negócios","Ações Nacionais")
                self.Soma_AcoesENegocios = sum([Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras])
                return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Ações e Negócios","Ações Nacionais")
            return [Label_Top1, Label_Top2, Label_Top3, 'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='orange', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='orange', align='center', color='orange')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_FundosAcoesENegocios(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Ações e Negócios","Fundos de investimentos: Ações e Negócios")
                self.Soma_FundosAcoesENegocios = sum([Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras])
                return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Ações e Negócios","Fundos de investimentos: Ações e Negócios")
            return [Label_Top1, Label_Top2, Label_Top3, 'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='orange', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='orange', align='center', color='orange')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_FII(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Real Estate","Fundos Imobiliários")
                self.Soma_FII = sum([Top1,Top2,Top3,Outras])
                return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Real Estate","Fundos Imobiliários")
            return [Label_Top1, Label_Top2, Label_Top3, 'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='blue', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='blue', align='center', color='blue')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_Terrenos(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Real Estate","Terrenos")
                self.Soma_Terrenos = sum([Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras])
                return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Real Estate","Terrenos")
            return [Label_Top1, Label_Top2, Label_Top3, 'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='blue', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='blue', align='center', color='blue')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_Construcoes(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Real Estate","Construções")
                self.Soma_Construcoes = sum([Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras])
                return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Real Estate","Construções")
            return [Label_Top1, Label_Top2, Label_Top3, 'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='blue', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='blue', align='center', color='blue')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_RendaFixa(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Caixa","Renda Fixa")
                self.Soma_RendaFixa = sum([Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras])
                return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Caixa","Renda Fixa")
            return [Label_Top1, Label_Top2, Label_Top3, 'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='green', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='green', align='center', color='green')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_TesouroDiretoETitulosPublicos(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Caixa","Tesouro Direto e Títulos Públicos")
                self.Soma_TesouroDiretoETitulosPublicos = sum([Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras])
                return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Caixa","Tesouro Direto e Títulos Públicos")
            return [Label_Top1, Label_Top2, Label_Top3, 'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='green', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='green', align='center', color='green')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_PrevidenciaPrivada(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Caixa","Previdência Privada")
                self.Soma_PrevidenciaPrivada = sum([Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras])
                return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Caixa","Previdência Privada")
            return [Label_Top1, Label_Top2, Label_Top3, 'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='green', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='green', align='center', color='green')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_COE(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Caixa","COE")
                self.Soma_COE = sum([Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras])
                return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Caixa","COE")
            return [Label_Top1, Label_Top2, Label_Top3, 'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='green', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='green', align='center', color='green')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_FundosRendaFixa(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Caixa","Fundos de Investimento: Renda Fixa")
                self.Soma_FundosDeRendaFixa = sum([Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras])
                return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Caixa","Fundos de Investimento: Renda Fixa")
            return [Label_Top1, Label_Top2, Label_Top3, 'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='green', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='green', align='center', color='green')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_BDR(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Ativos Internacionais","BDR")
                self.Soma_BDR = sum([Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras])
            return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Ativos Internacionais","BDR")
            return [Label_Top1, Label_Top2, Label_Top3,'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='purple', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='purple', align='center', color='purple')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_FundosAcoesInternacionais(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
                Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Ativos Internacionais","Fundos de Investimento: Ações Internacionais")
                self.Soma_FundosAcoesInternacionais = sum([Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras])
                return [Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras]
        def GetLabels():
            Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras, Label_Top1, Label_Top2, Label_Top3 = self.HMI.DBManager.GetDataFor("Ativos Internacionais","Fundos de Investimento: Ações Internacionais")
            return [Label_Top1, Label_Top2, Label_Top3,'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='purple', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='purple', align='center', color='purple')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_Criptomoedas(self):
        def GetData():
            Top1 = 0
            Top2 = 0
            Top3 = 0
            Outras = 0
            if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...':
                self.Flag_RecalcularGraficos = True
                return [Top1,Top2,Top3,Outras]
            else:
            # Recuperar as 3 criptos com maior CustoDe¨ alocado, somado de todas as corretoras de cripto
            # A 4ª coluna deve ser o patrimonio nas corretoras cripto, menos a conta corrente, menos o CustoDe¨ das 3 maiores, calculada anteriormente
                Top1,Top2,Top3,Outras = self.HMI.DBManager.GetDataForCriptomoedas()
                self.Soma_Criptomoedas = sum([Top1,Top2,Top3,Outras])
                return [Top1,Top2,Top3,Outras]
        def GetLabels():
            # Recuperar as 3 criptos com maior CustoDe¨ alocado, somado de todas as corretoras de cripto
            Top1,Top2,Top3 = self.HMI.DBManager.GetDataLabelsForCriptomoedas()
            return [Top1,Top2,Top3,'Outras']
        self.GraphWidget_Especifica_Storage, ax = plt.subplots()
        self.GraphWidget_Especifica_Storage.clear()
        self.GraphWidget_Especifica_Storage.set_facecolor("black")
        data = GetData()
        labels = GetLabels()
        if 0.0 in data: normalize = False # Bugfix
        else: normalize = True
        explode = ()
        for i in data: explode += (0.03,)

        if self.HMI.Patrimonio == 0 or self.HMI.Patrimonio == 'calculando...' or self.HMI.TextBox_Patrimonio.text() == 'Att. cot. (C)' or self.HMI.TextBox_Patrimonio.text() == '...' or sum(data)==0:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='purple', align='center')
            plt.xticks(list(range(1)), ["..."], rotation=0, color='white', fontsize=18)
        else:
            graph = plt.bar(list(range(len(data))), data, width=0.75, linewidth=4, edgecolor='purple', align='center', color='purple')
            plt.xticks(list(range(len(labels))), labels, rotation=30, color='white', fontsize=14)

        if not sum(data) == 0:
            percentage = list(map(lambda x: round(x/sum(data)*100,1), data))
        else:
            percentage = list(map(lambda x: 0, data))
        for i,p in enumerate(graph):
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            plt.text(x+width/2, y+height*1.01,
                     str(percentage[i])+'%',
                     ha='center', weight='bold', color="w")

        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        self.GraphWidget_Especifica_Storage.set_facecolor("black")

        GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
        plt.close(self.GraphWidget_Especifica_Storage)
        return GraphWidget

    def CreateGraph_Page11_Especifica(self):
        if self.GraficoEspecifico_Name == "":
            self.GraphWidget_Especifica_Storage, ax = plt.subplots()
            self.GraphWidget_Especifica_Storage.clear()
            self.GraphWidget_Especifica_Storage.set_facecolor("black")
            ax = plt.gca()
            ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
            self.GraphWidget_Especifica_Storage.set_facecolor("black")
            GraphWidget = FigureCanvas(self.GraphWidget_Especifica_Storage)
            plt.close(self.GraphWidget_Especifica_Storage)
            return GraphWidget

        self.HMI.GraphWidget_Especifica.deleteLater()

        if self.GraficoEspecifico_Name == "Ações Nacionais":
            self.HMI.Label_Subtitulo5.setText("Ações")
            self.HMI.Label_Subtitulo5_.setText("Ações")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_AcoesNacionais()
        elif self.GraficoEspecifico_Name == "Fundos de investimentos: Ações e Negócios":
            self.HMI.Label_Subtitulo5.setText("Fundos")
            self.HMI.Label_Subtitulo5_.setText("Fundos")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_FundosAcoesENegocios()
        elif self.GraficoEspecifico_Name == "Fundos Imobiliários":
            self.HMI.Label_Subtitulo5.setText("Fundos")
            self.HMI.Label_Subtitulo5_.setText("Fundos")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_FII()
        elif self.GraficoEspecifico_Name == "Terrenos":
            self.HMI.Label_Subtitulo5.setText("Terrenos")
            self.HMI.Label_Subtitulo5_.setText("Terrenos")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_Terrenos()
        elif self.GraficoEspecifico_Name == "Construções":
            self.HMI.Label_Subtitulo5.setText("Construções")
            self.HMI.Label_Subtitulo5_.setText("Construções")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_Construcoes()
        elif self.GraficoEspecifico_Name == "Renda Fixa":
            self.HMI.Label_Subtitulo5.setText("RF")
            self.HMI.Label_Subtitulo5_.setText("RF")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_RendaFixa()
        elif self.GraficoEspecifico_Name == "Tesouro Direto e Títulos Públicos":
            self.HMI.Label_Subtitulo5.setText("TD/TP")
            self.HMI.Label_Subtitulo5_.setText("TD/TP")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_TesouroDiretoETitulosPublicos()
        elif self.GraficoEspecifico_Name == "Previdência Privada":
            self.HMI.Label_Subtitulo5.setText("PP")
            self.HMI.Label_Subtitulo5_.setText("PP")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_PrevidenciaPrivada()
        elif self.GraficoEspecifico_Name == "COE":
            self.HMI.Label_Subtitulo5.setText("COE")
            self.HMI.Label_Subtitulo5_.setText("COE")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_COE()
        elif self.GraficoEspecifico_Name == "Fundos de Investimento: Renda Fixa":
            self.HMI.Label_Subtitulo5.setText("Fundos")
            self.HMI.Label_Subtitulo5_.setText("Fundos")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_FundosRendaFixa()
        elif self.GraficoEspecifico_Name == "BDR":
            self.HMI.Label_Subtitulo5.setText("BDR")
            self.HMI.Label_Subtitulo5_.setText("BDR")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_BDR()
        elif self.GraficoEspecifico_Name == "Fundos de Investimento: Ações Internacionais":
            self.HMI.Label_Subtitulo5.setText("Fundos")
            self.HMI.Label_Subtitulo5_.setText("Fundos")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_FundosAcoesInternacionais()
        elif self.GraficoEspecifico_Name == "Criptomoedas":
            self.HMI.Label_Subtitulo5.setText("Criptomoedas")
            self.HMI.Label_Subtitulo5_.setText("Criptomoedas")
            self.HMI.GraphWidget_Especifica = self.CreateGraph_Page11_Criptomoedas()

        self.HMI.VBoxLayout_Graficos_Subtipos_Especifica.addWidget(self.HMI.GraphWidget_Especifica)

        self.HMI.Button_EspecificaInvisivel.deleteLater()
        self.HMI.Button_EspecificaInvisivel = QPushButton()
        self.HMI.Button_EspecificaInvisivel.pressed.connect(lambda: self.CallCreatePage())
        self.HMI.Button_EspecificaInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
        self.HMI.Button_EspecificaInvisivel.setCursor(QCursor(Qt.PointingHandCursor))
        if self.HMI.frameGeometry().width()/self.HMI.frameGeometry().height() < 1.9577: proporcao = 1/6
        elif self.HMI.frameGeometry().width()/self.HMI.frameGeometry().height() < 2.6202: proporcao = 1/8
        else: proporcao = 1/10
        self.HMI.GraphWidget_Especifica.setFixedSize(int(self.HMI.frameGeometry().width()*proporcao),int(self.HMI.frameGeometry().width()*proporcao))
        self.HMI.Button_EspecificaInvisivel.setFixedSize(int(self.HMI.frameGeometry().height()*proporcao),int(self.HMI.frameGeometry().height()*proporcao))
        self.HMI.VBoxLayout_Graficos_Subtipos_EspecificaInvisiveis.addWidget(self.HMI.Button_EspecificaInvisivel)

    def CreateGraph_Page46_MainGraph_VisaoGeral(self):
        # Gráfico de funil da visão geral
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        for tick in ax.axes.get_xticklines(): tick.set_visible(False)
        for tick in ax.axes.get_yticklines(): tick.set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.xaxis.label.set_color('w'); ax.yaxis.label.set_color('w')
        ax.tick_params(axis='y', colors='w')
        for eixo in ['bottom', 'top', 'right', 'left']: ax.spines[eixo].set_color('black')

        Labels_AN, Labels_Fundos, Values_AN, Values_Fundos, Setores_AN, Setores_Fundos = self.HMI.DBManager.GetDetailedDataForAcoesENegocios()

        ParaOrdenar = [("Ações",sum(Values_AN)),("Fundos",sum(Values_Fundos))]
        Ordenado = sorted(ParaOrdenar, key=lambda tup: tup[1])
        Labels = list(map(lambda tup: tup[0], Ordenado))
        Values = list(map(lambda tup: tup[1], Ordenado))

        Values_SumTotal = sum(Values)

        per = list(map(lambda item: str(f'{round(item/Values_SumTotal*100, 2):.2f}')+"%", Values))

        if Values_SumTotal > 0:
            plt.title('Visão geral', fontsize=26, color='white')
            values_max = max(Values)+2; values_min = 0
            plt.xlim(values_min, values_max)
            heights = [-0.25]
            for y in range(len(Labels)-1): heights.append(0.78+((len(heights)-1)*0.995))
            for idx, val in enumerate(Values):
                left = (values_max - val)/2
                plt.barh(Labels[idx], Values[idx], left = left, color=str('#%02x%02x%02x' % (120, 200, 250)), height=0.8, edgecolor='black')
                if self.HMI.ShowValues:
                    plt.text(values_max/2, heights[idx], str(f'{round(Values[idx], 2):.2f}'), ha='center', fontsize=15, color='g')
                    plt.ylabel(UserCoin, fontsize=11)
                else:
                    plt.text(values_max/2, heights[idx], per[idx], ha='center', fontsize=15, color='g')
        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page46_MainGraph_AtivoPorCorretora(self):
        return self.CreateGraph_AtivoPorCorretora()

    def CreateGraph_Page46_MainGraph_AtivoPorSetor(self):
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()

        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))

        Labels_AN, Labels_Fundos, Values_AN, Values_Fundos, Setores_AN, Setores_Fundos = self.HMI.DBManager.GetDetailedDataForAcoesENegocios()

        Values = []
        Setores = copy(Setores_AN)
        Setores.extend(Setores_Fundos)
        Setores = list(set(Setores))
        Labels = Setores

        for setor in Setores:
            valor = 0
            for i, item in enumerate(Setores_AN):
                if item == setor:
                    valor += Values_AN[i]
            for i, item in enumerate(Setores_Fundos):
                if item == setor:
                    valor += Values_Fundos[i]
            Values.append(valor)

        ParaOrdenar = []
        for i, label in enumerate(Labels):
            ParaOrdenar.append((label,Values[i]))
        Ordenado = sorted(ParaOrdenar, key=lambda tup: tup[1])
        Labels = list(map(lambda tup: tup[0], Ordenado))
        Values = list(map(lambda tup: tup[1], Ordenado))

        values = [x for x in Values if round(x,2) > self.MostrarValoresMaioresQue]
        labels = [Labels[i] for i, x in enumerate(Values) if round(x,2) > self.MostrarValoresMaioresQue]

        explode = ()
        for i in values: explode += (0.03,)

        plt.axis('equal')
        plt.title("Por setor", color='w', fontsize=20)
        plt.tight_layout()

        if sum(values)==0:
            patches, texts = plt.pie([1], labels = ["Vazio"], startangle = 90, shadow = True, normalize = True)
        else:
            patches, texts, pcts = plt.pie(values, labels = labels, startangle = 90, shadow = True, normalize = True, explode = explode,
                                           autopct = lambda pct: self.getPercentage(pct, values))
            plt.setp(pcts, color='white')

        for i, patch in enumerate(patches):
            texts[i].set_color(patch.get_facecolor())

        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page46_Subtipos(self):
        # Gráfico de barras dos subtipos
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        GraphWidget_ax, axs = plt.subplots(nrows=1, ncols=2, figsize=(30,4), clear=True)#, sharey=True)
        GraphWidget_ax.set_facecolor("black")
        if self.HMI.ShowValues: axs[0].set_ylabel(UserCoin, fontsize=11)
        for i in [0,1]:
            axs[i].set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
            axs[i].xaxis.label.set_color('w')
            axs[i].yaxis.label.set_color('w')
            axs[i].yaxis.label.set_color('black')
            axs[i].tick_params(axis='y', colors='black')
            axs[i].tick_params(axis='x', colors='w')
            axs[i].grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)
            for eixo in ['bottom', 'top', 'right', 'left']: axs[i].spines[eixo].set_color('black')
        if self.HMI.ShowValues:
            axs[0].yaxis.label.set_color('w')
            axs[0].tick_params(axis='y', colors='w')

        Labels_0, Labels_1, Values_0, Values_1, Setores_0, Setores_1 = self.HMI.DBManager.GetDetailedDataForAcoesENegocios()

        Values_0_SumTotal = sum(Values_0)
        Labels_0 = [Labels_0[i] for i, x in enumerate(Values_0) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_0 = [x for i, x in enumerate(Values_0) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_1_SumTotal = sum(Values_1)
        Labels_1 = [Labels_1[i] for i, x in enumerate(Values_1) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_1 = [x for i, x in enumerate(Values_1) if round(x,2) > self.MostrarValoresMaioresQue]

        if len(Values_0) > 0 and len(Values_1) > 0:
            for i in [0, 1]: axs[i].set_ylim(0, max(max(Values_0), max(Values_1)) * 1.1)
        elif len(Values_0) > 0:
            for i in [0, 1]: axs[i].set_ylim(0, max(Values_0) * 1.1)
        elif len(Values_1) > 0:
            for i in [0, 1]: axs[i].set_ylim(0, max(Values_1) * 1.1)

        axs[0].set_title('Ações', fontsize=26, color='white')
        if len(Values_0) > 0:
            axs[0].bar(Labels_0, Values_0, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_0)):
                    axs[0].text(n, Values_0[n], str('R$%.2f' % Values_0[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_0)):
                    if Values_0_SumTotal > 0: axs[0].text(n, Values_0[n], str('%.1f' % (Values_0[n]/Values_0_SumTotal*100))+"%", ha='center', fontsize=14, color='g')
                    else: axs[0].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[0].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[0].text(0, 0, '0', ha='center', fontsize=14, color='g')

        axs[1].set_title('Fundos', fontsize=26, color='white')
        if len(Values_1) > 0:
            axs[1].bar(Labels_1, Values_1, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_1)):
                    axs[1].text(n, Values_1[n], str('R$%.2f' % Values_1[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_1)):
                    if Values_1_SumTotal > 0: axs[1].text(n, Values_1[n], str('%.1f' % (Values_1[n]/Values_1_SumTotal*100))+"%", ha='center', fontsize=14, color='g')
                    else: axs[1].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[1].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[1].text(0, 0, '0', ha='center', fontsize=14, color='g')

        GraphWidget = FigureCanvas(GraphWidget_ax)
        plt.close(GraphWidget_ax)
        return GraphWidget

    def CreateGraph_Page47_MainGraph_VisaoGeral(self):
        # Gráfico de funil da visão geral
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        for tick in ax.axes.get_xticklines(): tick.set_visible(False)
        for tick in ax.axes.get_yticklines(): tick.set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.xaxis.label.set_color('w'); ax.yaxis.label.set_color('w')
        ax.tick_params(axis='y', colors='w')
        for eixo in ['bottom', 'top', 'right', 'left']: ax.spines[eixo].set_color('black')

        Labels_Terrenos, Labels_Construcoes, Labels_Fundos, Values_Terrenos, Values_Construcoes, Values_Fundos, Setores_Terrenos, Setores_Construcoes, Setores_Fundos = self.HMI.DBManager.GetDetailedDataForRealEstate()

        ParaOrdenar = [("Terrenos",sum(Values_Terrenos)),("Construções",sum(Values_Construcoes)),("FIIs",sum(Values_Fundos))]
        Ordenado = sorted(ParaOrdenar, key=lambda tup: tup[1])
        Labels = list(map(lambda tup: tup[0], Ordenado))
        Values = list(map(lambda tup: tup[1], Ordenado))

        Values_SumTotal = sum(Values)

        per = list(map(lambda item: str(f'{round(item/Values_SumTotal*100, 2):.2f}')+"%", Values))

        if Values_SumTotal > 0:
            plt.title('Visão geral', fontsize=26, color='white')
            values_max = max(Values)+2; values_min = 0
            plt.xlim(values_min, values_max)
            heights = [-0.25]
            for y in range(len(Labels)-1): heights.append(0.78+((len(heights)-1)*0.995))
            for idx, val in enumerate(Values):
                left = (values_max - val)/2
                plt.barh(Labels[idx], Values[idx], left = left, color=str('#%02x%02x%02x' % (120, 200, 250)), height=0.8, edgecolor='black')
                if self.HMI.ShowValues:
                    plt.text(values_max/2, heights[idx], str(f'{round(Values[idx], 2):.2f}'), ha='center', fontsize=15, color='g')
                    plt.ylabel(UserCoin, fontsize=11)
                else:
                    plt.text(values_max/2, heights[idx], per[idx], ha='center', fontsize=15, color='g')
        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page47_MainGraph_AtivoPorCorretora(self):
        return self.CreateGraph_AtivoPorCorretora()

    def CreateGraph_Page47_MainGraph_AtivoPorSetor(self):
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()

        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))

        Labels_Terrenos, Labels_Construcoes, Labels_Fundos, Values_Terrenos, Values_Construcoes, Values_Fundos, Setores_Terrenos, Setores_Construcoes, Setores_Fundos = self.HMI.DBManager.GetDetailedDataForRealEstate()

        Values = []
        Setores = copy(Setores_Terrenos)
        Setores.extend(Setores_Construcoes)
        Setores.extend(Setores_Fundos)
        Setores = list(set(Setores))
        Labels = Setores

        for setor in Setores:
            valor = 0
            for i, item in enumerate(Setores_Terrenos):
                if item == setor:
                    valor += Values_Terrenos[i]
            for i, item in enumerate(Setores_Construcoes):
                if item == setor:
                    valor += Values_Construcoes[i]
            for i, item in enumerate(Setores_Fundos):
                if item == setor:
                    valor += Values_Fundos[i]
            Values.append(valor)

        ParaOrdenar = []
        for i, label in enumerate(Labels):
            ParaOrdenar.append((label,Values[i]))
        Ordenado = sorted(ParaOrdenar, key=lambda tup: tup[1])
        Labels = list(map(lambda tup: tup[0], Ordenado))
        Values = list(map(lambda tup: tup[1], Ordenado))

        values = [x for x in Values if round(x,2) > self.MostrarValoresMaioresQue]
        labels = [Labels[i] for i, x in enumerate(Values) if round(x,2) > self.MostrarValoresMaioresQue]

        explode = ()
        for i in values: explode += (0.03,)

        plt.axis('equal')
        plt.title("Por setor", color='w', fontsize=20)
        plt.tight_layout()

        if sum(values)==0:
            patches, texts = plt.pie([1], labels = ["Vazio"], startangle = 90, shadow = True, normalize = True)
        else:
            patches, texts, pcts = plt.pie(values, labels = labels, startangle = 90, shadow = True, normalize = True, explode = explode,
                                           autopct = lambda pct: self.getPercentage(pct, values))
            plt.setp(pcts, color='white')

        for i, patch in enumerate(patches):
            texts[i].set_color(patch.get_facecolor())

        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page47_Subtipos(self):
        # Gráfico de barras dos subtipos
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        GraphWidget_ax, axs = plt.subplots(nrows=1, ncols=3, figsize=(30,4), clear=True)#, sharey=True)
        GraphWidget_ax.set_facecolor("black")
        if self.HMI.ShowValues: axs[0].set_ylabel(UserCoin, fontsize=11)
        for i in [0,1,2]:
            axs[i].set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
            axs[i].xaxis.label.set_color('w')
            axs[i].yaxis.label.set_color('w')
            axs[i].yaxis.label.set_color('black')
            axs[i].tick_params(axis='y', colors='black')
            axs[i].tick_params(axis='x', colors='w')
            axs[i].grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)
            for eixo in ['bottom', 'top', 'right', 'left']: axs[i].spines[eixo].set_color('black')
        if self.HMI.ShowValues:
            axs[0].yaxis.label.set_color('w')
            axs[0].tick_params(axis='y', colors='w')

        Labels_0, Labels_1, Labels_2, Values_0, Values_1, Values_2, Setores_0, Setores_1, Setores_2 = self.HMI.DBManager.GetDetailedDataForRealEstate()

        Values_0_SumTotal = sum(Values_0)
        Labels_0 = [Labels_0[i] for i, x in enumerate(Values_0) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_0 = [x for i, x in enumerate(Values_0) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_1_SumTotal = sum(Values_1)
        Labels_1 = [Labels_1[i] for i, x in enumerate(Values_1) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_1 = [x for i, x in enumerate(Values_1) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_2_SumTotal = sum(Values_2)
        Labels_2 = [Labels_2[i] for i, x in enumerate(Values_2) if round(x, 2) > self.MostrarValoresMaioresQue]
        Values_2 = [x for i, x in enumerate(Values_2) if round(x, 2) > self.MostrarValoresMaioresQue]

        if len(Values_0) > 0 and len(Values_1) > 0 and len(Values_2) > 0:
            for i in [0,1,2]: axs[i].set_ylim(0, max(max(max(Values_0), max(Values_1)), max(Values_2)) * 1.1)
        elif len(Values_0) > 0 and len(Values_1) > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, max(max(Values_0), max(Values_1)) * 1.1)
        elif len(Values_0) > 0 and len(Values_2) > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, max(max(Values_0), max(Values_2)) * 1.1)
        elif len(Values_1) > 0 and len(Values_2) > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, max(max(Values_1), max(Values_2)) * 1.1)
        elif len(Values_0) > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, max(Values_0) * 1.1)
        elif len(Values_1) > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, max(Values_1) * 1.1)
        elif len(Values_2) > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, max(Values_2) * 1.1)

        axs[0].set_title('Terrenos', fontsize=26, color='white')
        if len(Values_0) > 0:
            axs[0].bar(Labels_0, Values_0, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_0)):
                    axs[0].text(n, Values_0[n], str('R$%.2f' % Values_0[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_0)):
                    if Values_0_SumTotal > 0: axs[0].text(n, Values_0[n], str('%.1f' % (Values_0[n]/Values_0_SumTotal*100))+"%", ha='center', fontsize=14, color='g')
                    else: axs[0].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[0].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[0].text(0, 0, '0', ha='center', fontsize=14, color='g')

        axs[1].set_title('Construções', fontsize=26, color='white')
        if len(Values_1) > 0:
            axs[1].bar(Labels_1, Values_1, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_1)):
                    axs[1].text(n, Values_1[n], str('R$%.2f' % Values_1[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_1)):
                    if Values_1_SumTotal > 0: axs[1].text(n, Values_1[n], str('%.1f' % (Values_1[n]/Values_1_SumTotal*100))+"%", ha='center', fontsize=14, color='g')
                    else: axs[1].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[1].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[1].text(0, 0, '0', ha='center', fontsize=14, color='g')

        axs[2].set_title('FIIs', fontsize=26, color='white')
        if len(Values_2) > 0:
            axs[2].bar(Labels_2, Values_2, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_2)):
                    axs[2].text(n, Values_2[n], str('R$%.2f' % Values_2[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_2)):
                    if Values_2_SumTotal > 0: axs[2].text(n, Values_2[n], str('%.1f' % (Values_2[n]/Values_2_SumTotal*100))+"%", ha='center', fontsize=14, color='g')
                    else: axs[2].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[2].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[2].text(0, 0, '0', ha='center', fontsize=14, color='g')

        GraphWidget = FigureCanvas(GraphWidget_ax)
        plt.close(GraphWidget_ax)
        return GraphWidget

    def CreateGraph_Page48_MainGraph_VisaoGeral(self):
        # Gráfico de funil da visão geral
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        for tick in ax.axes.get_xticklines(): tick.set_visible(False)
        for tick in ax.axes.get_yticklines(): tick.set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.xaxis.label.set_color('w'); ax.yaxis.label.set_color('w')
        ax.tick_params(axis='y', colors='w')
        for eixo in ['bottom', 'top', 'right', 'left']: ax.spines[eixo].set_color('black')

        Labels_RF, Labels_TDTP, Labels_PP, Labels_COE, Labels_Fundos, Values_RF, Values_TDTP, Values_PP, Values_COE, Values_Fundos, Setores_RF, Setores_TDTP, Setores_PP, Setores_COE, Setores_Fundos = self.HMI.DBManager.GetDetailedDataForCaixa()

        ParaOrdenar = [("RF",sum(Values_RF)),("TD/TP",sum(Values_TDTP)),("PP",sum(Values_PP)),("COE",sum(Values_COE)),("Fundos",sum(Values_Fundos))]
        Ordenado = sorted(ParaOrdenar, key=lambda tup: tup[1])
        Labels = list(map(lambda tup: tup[0], Ordenado))
        Values = list(map(lambda tup: tup[1], Ordenado))

        Values_SumTotal = sum(Values)

        per = list(map(lambda item: str(f'{round(item/Values_SumTotal*100, 2):.2f}')+"%", Values))

        if Values_SumTotal > 0:
            plt.title('Visão geral', fontsize=26, color='white')
            values_max = max(Values)+2; values_min = 0
            plt.xlim(values_min, values_max)
            heights = [-0.25]
            for y in range(len(Labels)-1): heights.append(0.78+((len(heights)-1)*0.995))
            for idx, val in enumerate(Values):
                left = (values_max - val)/2
                plt.barh(Labels[idx], Values[idx], left = left, color=str('#%02x%02x%02x' % (120, 200, 250)), height=0.8, edgecolor='black')
                if self.HMI.ShowValues:
                    plt.text(values_max/2, heights[idx], str(f'{round(Values[idx], 2):.2f}'), ha='center', fontsize=15, color='g')
                    plt.ylabel(UserCoin, fontsize=11)
                else:
                    plt.text(values_max/2, heights[idx], per[idx], ha='center', fontsize=15, color='g')
        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page48_MainGraph_AtivoPorCorretora(self):
        return self.CreateGraph_AtivoPorCorretora()

    def CreateGraph_Page48_MainGraph_AtivoPorSetor(self):
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()

        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))

        Labels_RF, Labels_TDTP, Labels_PP, Labels_COE, Labels_Fundos, Values_RF, Values_TDTP, Values_PP, Values_COE, Values_Fundos, Setores_RF, Setores_TDTP, Setores_PP, Setores_COE, Setores_Fundos = self.HMI.DBManager.GetDetailedDataForCaixa()

        Values = []
        Setores = copy(Setores_RF)
        Setores.extend(Setores_TDTP)
        Setores.extend(Setores_PP)
        Setores.extend(Setores_COE)
        Setores.extend(Setores_Fundos)
        Setores = list(set(Setores))
        Labels = Setores

        for setor in Setores:
            valor = 0
            for i, item in enumerate(Setores_RF):
                if item == setor:
                    valor += Values_RF[i]
            for i, item in enumerate(Setores_TDTP):
                if item == setor:
                    valor += Values_TDTP[i]
            for i, item in enumerate(Setores_PP):
                if item == setor:
                    valor += Values_PP[i]
            for i, item in enumerate(Setores_COE):
                if item == setor:
                    valor += Values_COE[i]
            for i, item in enumerate(Setores_Fundos):
                if item == setor:
                    valor += Values_Fundos[i]
            Values.append(valor)

        ParaOrdenar = []
        for i, label in enumerate(Labels):
            ParaOrdenar.append((label,Values[i]))
        Ordenado = sorted(ParaOrdenar, key=lambda tup: tup[1])
        Labels = list(map(lambda tup: tup[0], Ordenado))
        Values = list(map(lambda tup: tup[1], Ordenado))

        values = [x for x in Values if round(x,2) > self.MostrarValoresMaioresQue]
        labels = [Labels[i] for i, x in enumerate(Values) if round(x,2) > self.MostrarValoresMaioresQue]

        explode = ()
        for i in values: explode += (0.03,)

        plt.axis('equal')
        plt.title("Por setor", color='w', fontsize=20)
        plt.tight_layout()

        if sum(values)==0:
            patches, texts = plt.pie([1], labels = ["Vazio"], startangle = 90, shadow = True, normalize = True)
        else:
            patches, texts, pcts = plt.pie(values, labels = labels, startangle = 90, shadow = True, normalize = True, explode = explode,
                                           autopct = lambda pct: self.getPercentage(pct, values))
            plt.setp(pcts, color='white')

        for i, patch in enumerate(patches):
            texts[i].set_color(patch.get_facecolor())

        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page48_Subtipos(self):
        # Gráfico de barras dos subtipos
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        GraphWidget_ax, axs = plt.subplots(nrows=1, ncols=5, figsize=(30,4), clear=True)#, sharey=True)
        GraphWidget_ax.set_facecolor("black")
        if self.HMI.ShowValues: axs[0].set_ylabel(UserCoin, fontsize=11)
        for i in [0, 1, 2, 3, 4]:
            axs[i].set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
            axs[i].xaxis.label.set_color('w')
            axs[i].yaxis.label.set_color('w')
            axs[i].yaxis.label.set_color('black')
            axs[i].tick_params(axis='y', colors='black')
            axs[i].tick_params(axis='x', colors='w')
            axs[i].grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)
            for eixo in ['bottom', 'top', 'right', 'left']: axs[i].spines[eixo].set_color('black')
        if self.HMI.ShowValues:
            axs[0].yaxis.label.set_color('w')
            axs[0].tick_params(axis='y', colors='w')

        Labels_0, Labels_1, Labels_2, Labels_3, Labels_4, Values_0, Values_1, Values_2, Values_3, Values_4, Setores_0, Setores_1, Setores_2, Setores_3, Setores_4 = self.HMI.DBManager.GetDetailedDataForCaixa()

        Values_0_SumTotal = sum(Values_0)
        Labels_0 = [Labels_0[i] for i, x in enumerate(Values_0) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_0 = [x for i, x in enumerate(Values_0) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_1_SumTotal = sum(Values_1)
        Labels_1 = [Labels_1[i] for i, x in enumerate(Values_1) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_1 = [x for i, x in enumerate(Values_1) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_2_SumTotal = sum(Values_2)
        Labels_2 = [Labels_2[i] for i, x in enumerate(Values_2) if round(x, 2) > self.MostrarValoresMaioresQue]
        Values_2 = [x for i, x in enumerate(Values_2) if round(x, 2) > self.MostrarValoresMaioresQue]
        Values_3_SumTotal = sum(Values_3)
        Labels_3 = [Labels_3[i] for i, x in enumerate(Values_3) if round(x, 2) > self.MostrarValoresMaioresQue]
        Values_3 = [x for i, x in enumerate(Values_3) if round(x, 2) > self.MostrarValoresMaioresQue]
        Values_4_SumTotal = sum(Values_4)
        Labels_4 = [Labels_4[i] for i, x in enumerate(Values_4) if round(x, 2) > self.MostrarValoresMaioresQue]
        Values_4 = [x for i, x in enumerate(Values_4) if round(x, 2) > self.MostrarValoresMaioresQue]

        if len(Values_0) > 0 and len(Values_1) > 0 and len(Values_2) > 0 and len(Values_3) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(max(max(Values_0), max(Values_1)), max(Values_2)), max(Values_3)), max(Values_4)) * 1.1)
        elif len(Values_0) > 0 and len(Values_1) > 0 and len(Values_2) > 0 and len(Values_3) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(max(Values_0), max(Values_1)), max(Values_2)), max(Values_3)) * 1.1)
        elif len(Values_0) > 0 and len(Values_1) > 0 and len(Values_2) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(max(Values_0), max(Values_1)), max(Values_2)), max(Values_4)) * 1.1)
        elif len(Values_0) > 0 and len(Values_2) > 0 and len(Values_3) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(max(Values_0), max(Values_2)), max(Values_3)), max(Values_4)) * 1.1)
        elif len(Values_1) > 0 and len(Values_2) > 0 and len(Values_3) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(max(Values_1), max(Values_2)), max(Values_3)), max(Values_4)) * 1.1)
        elif len(Values_0) > 0 and len(Values_1) > 0 and len(Values_2) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(Values_0), max(Values_1)), max(Values_2)) * 1.1)
        elif len(Values_0) > 0 and len(Values_1) > 0 and len(Values_3) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(Values_0), max(Values_1)), max(Values_3)) * 1.1)
        elif len(Values_0) > 0 and len(Values_1) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(Values_0), max(Values_1)), max(Values_4)) * 1.1)
        elif len(Values_0) > 0 and len(Values_2) > 0 and len(Values_3) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(Values_0), max(Values_2)), max(Values_3)) * 1.1)
        elif len(Values_0) > 0 and len(Values_2) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(Values_0), max(Values_2)), max(Values_4)) * 1.1)
        elif len(Values_0) > 0 and len(Values_3) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(Values_0), max(Values_3)), max(Values_4)) * 1.1)
        elif len(Values_1) > 0 and len(Values_2) > 0 and len(Values_3) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(Values_1), max(Values_2)), max(Values_3)) * 1.1)
        elif len(Values_1) > 0 and len(Values_2) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(Values_1), max(Values_2)), max(Values_4)) * 1.1)
        elif len(Values_1) > 0 and len(Values_3) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(Values_1), max(Values_3)), max(Values_4)) * 1.1)
        elif len(Values_2) > 0 and len(Values_3) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(max(Values_2), max(Values_3)), max(Values_4)) * 1.1)
        elif len(Values_0) > 0 and len(Values_1) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(Values_0), max(Values_1)) * 1.1)
        elif len(Values_0) > 0 and len(Values_2) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(Values_0), max(Values_2)) * 1.1)
        elif len(Values_0) > 0 and len(Values_3) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(Values_0), max(Values_3)) * 1.1)
        elif len(Values_0) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(Values_0), max(Values_4)) * 1.1)
        elif len(Values_1) > 0 and len(Values_2) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(Values_1), max(Values_2)) * 1.1)
        elif len(Values_1) > 0 and len(Values_3) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(Values_1), max(Values_3)) * 1.1)
        elif len(Values_1) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(Values_1), max(Values_4)) * 1.1)
        elif len(Values_2) > 0 and len(Values_3) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(Values_2), max(Values_3)) * 1.1)
        elif len(Values_2) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(Values_2), max(Values_4)) * 1.1)
        elif len(Values_3) > 0 and len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(max(Values_3), max(Values_4)) * 1.1)
        elif len(Values_0) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(Values_0) * 1.1)
        elif len(Values_1) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(Values_1) * 1.1)
        elif len(Values_2) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(Values_2) * 1.1)
        elif len(Values_3) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(Values_3) * 1.1)
        elif len(Values_4) > 0:
            for i in [0, 1, 2, 3, 4]: axs[i].set_ylim(0, max(Values_4) * 1.1)

        axs[0].set_title('RF', fontsize=26, color='white')
        if len(Values_0) > 0:
            axs[0].bar(Labels_0, Values_0, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_0)):
                    axs[0].text(n, Values_0[n], str('R$%.2f' % Values_0[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_0)):
                    if Values_0_SumTotal > 0: axs[0].text(n, Values_0[n], str('%.1f' % (Values_0[n]/Values_0_SumTotal*100))+"%", ha='center', fontsize=14, color='g')
                    else: axs[0].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[0].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[0].text(0, 0, '0', ha='center', fontsize=14, color='g')

        axs[1].set_title('TD e TP', fontsize=26, color='white')
        if len(Values_1) > 0:
            axs[1].bar(Labels_1, Values_1, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_1)):
                    axs[1].text(n, Values_1[n], str('R$%.2f' % Values_1[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_1)):
                    if Values_1_SumTotal > 0: axs[1].text(n, Values_1[n], str('%.1f' % (Values_1[n]/Values_1_SumTotal*100))+"%", ha='center', fontsize=14, color='g')
                    else: axs[1].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[1].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[1].text(0, 0, '0', ha='center', fontsize=14, color='g')

        axs[2].set_title('PP', fontsize=26, color='white')
        if len(Values_2) > 0:
            axs[2].bar(Labels_2, Values_2, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_2)):
                    axs[2].text(n, Values_2[n], str('R$%.2f' % Values_2[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_2)):
                    if Values_2_SumTotal > 0: axs[1].text(n, Values_2[n], str('%.1f' % (Values_2[n]/Values_2_SumTotal*100))+"%", ha='center', fontsize=14, color='g')
                    else: axs[2].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[2].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[2].text(0, 0, '0', ha='center', fontsize=14, color='g')

        axs[3].set_title('COE', fontsize=26, color='white')
        if len(Values_3) > 0:
            axs[3].bar(Labels_3, Values_3, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_3)):
                    axs[3].text(n, Values_3[n], str('R$%.2f' % Values_3[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_3)):
                    if Values_3_SumTotal > 0:
                        axs[3].text(n, Values_3[n], str('%.1f' % (Values_3[n] / Values_3_SumTotal * 100)) + "%", ha='center', fontsize=14, color='g')
                    else:
                        axs[3].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[3].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[3].text(0, 0, '0', ha='center', fontsize=14, color='g')

        axs[4].set_title('Fundos', fontsize=26, color='white')
        if len(Values_4) > 0:
            axs[4].bar(Labels_4, Values_4, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_4)):
                    axs[4].text(n, Values_4[n], str('R$%.2f' % Values_4[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_4)):
                    if Values_4_SumTotal > 0:
                        axs[4].text(n, Values_4[n], str('%.1f' % (Values_4[n] / Values_4_SumTotal * 100)) + "%", ha='center', fontsize=14, color='g')
                    else:
                        axs[4].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[4].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[4].text(0, 0, '0', ha='center', fontsize=14, color='g')

        GraphWidget = FigureCanvas(GraphWidget_ax)
        plt.close(GraphWidget_ax)
        return GraphWidget

    def CreateGraph_Page49_MainGraph_VisaoGeral(self):
        # Gráfico de funil da visão geral
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        for tick in ax.axes.get_xticklines(): tick.set_visible(False)
        for tick in ax.axes.get_yticklines(): tick.set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.xaxis.label.set_color('w'); ax.yaxis.label.set_color('w')
        ax.tick_params(axis='y', colors='w')
        for eixo in ['bottom', 'top', 'right', 'left']: ax.spines[eixo].set_color('black')

        Labels_BDR, Labels_Fundos, Values_BDR, Values_Fundos, Setores_BDR, Setores_Fundos = self.HMI.DBManager.GetDetailedDataForAtivosInternacionais()
        Labels_Cripto, Values_Cripto = self.HMI.DBManager.GetDetailedDataForCriptomoedas()
        ParaOrdenar = [("BDR",sum(Values_BDR)),("Fundos",sum(Values_Fundos)),("Criptos",sum([x[0] + x[1] + x[2] for x in Values_Cripto]))]
        Ordenado = sorted(ParaOrdenar, key=lambda tup: tup[1])
        Labels = list(map(lambda tup: tup[0], Ordenado))
        Values = list(map(lambda tup: tup[1], Ordenado))

        Values_SumTotal = sum(Values)

        per = list(map(lambda item: str(f'{round(item/Values_SumTotal*100, 2):.2f}')+"%", Values))

        if Values_SumTotal > 0:
            plt.title('Visão geral', fontsize=26, color='white')
            values_max = max(Values)+2; values_min = 0
            plt.xlim(values_min, values_max)
            heights = [-0.25]
            for y in range(len(Labels)-1): heights.append(0.78+((len(heights)-1)*0.995))
            for idx, val in enumerate(Values):
                left = (values_max - val)/2
                plt.barh(Labels[idx], Values[idx], left = left, color=str('#%02x%02x%02x' % (120, 200, 250)), height=0.8, edgecolor='black')
                if self.HMI.ShowValues:
                    plt.text(values_max/2, heights[idx], str(f'{round(Values[idx], 2):.2f}'), ha='center', fontsize=15, color='g')
                    plt.ylabel(UserCoin, fontsize=11)
                else:
                    plt.text(values_max/2, heights[idx], per[idx], ha='center', fontsize=15, color='g')
        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page49_MainGraph_AtivoPorCorretora(self):
        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))

        Ativo = self.HMI.ComboBox_Ativos.currentText()
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        if Ativo == "Todos" or Ativo == "Criptos":
            self.HMI.ComboBox_Ativos.setCurrentIndex(1)
            Ativo = self.HMI.ComboBox_Ativos.currentText()
            if Ativo == "Criptos":
                self.HMI.ComboBox_Ativos.setCurrentIndex(0)
                plt.close(GraphWidget_MainGraph)

                MessageBox_Msg1 = QMessageBox.about(self, 'Aviso', 'Não há nenhum ativo a ser mostrado por corretora.\n(Criptomoedas só são detalhadas na página de criptomoedas)')
                self.MainGraphIsShowing = "Visão Geral"
                GraphWidget = self.CreateGraph_Page49_MainGraph_VisaoGeral()
                return GraphWidget

            self.Custo = self.HMI.DBManager.GetCustoAtivo(Ativo, "Bolsa")
            self.Retorno = self.HMI.DBManager.GetEstoqueAtivo(Ativo, "Bolsa") * self.HMI.DBManager.GetCotacao(Ativo)
            if self.HMI.ShowValues:
                self.HMI.TextBox_Custo.setText('Custo: '+UserCoin+' '+str(f'{round(self.Custo, 2):.2f}'))
                self.HMI.TextBox_Retorno.setText('Retorno: '+UserCoin+' '+str(f'{round(self.Retorno, 2):.2f}'))
            else:
                self.HMI.TextBox_Custo.setText('Custo: X')
                self.HMI.TextBox_Retorno.setText('Retorno: '+str(round((self.Retorno-self.Custo)/self.Custo*100,2))+'%X')
            if self.Retorno >= self.Custo:
                self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
            else:
                self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

        CotacaoAtivo = self.HMI.DBManager.GetCotacao(Ativo)

        Labels, Values = self.HMI.DBManager.GetDetailedData_AtivoPorCorretora(Ativo)
        values = [x for x in Values if round(x,2) > self.MostrarValoresMaioresQue]
        labels = [Labels[i] for i, x in enumerate(Values) if round(x,2) > self.MostrarValoresMaioresQue]

        explode = ()
        for i in values: explode += (0.03,)

        plt.axis('equal')
        plt.title("Cotação "+Ativo+": "+UserCoin+str(f'{round(CotacaoAtivo,2):.2f}'), color='w', fontsize=20)
        plt.tight_layout()

        if len(values)==0:
            patches, texts = plt.pie([1], labels = ["Vazio"], startangle = 90, shadow = True, normalize = True)
        else:
            patches, texts, pcts = plt.pie(values, labels = labels, startangle = 90, shadow = True, normalize = True, explode = explode,
                                           autopct = lambda pct: self.getPercentage(pct, values))
            plt.setp(pcts, color='white')

        for i, patch in enumerate(patches):
            texts[i].set_color(patch.get_facecolor())

        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page49_MainGraph_AtivoPorSetor(self):
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()

        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))

        Labels_BDR, Labels_Fundos, Values_BDR, Values_Fundos, Setores_BDR, Setores_Fundos = self.HMI.DBManager.GetDetailedDataForAtivosInternacionais()
        Labels_Cripto, Values_Cripto = self.HMI.DBManager.GetDetailedDataForCriptomoedas()

        Values = []
        Setores = copy(Setores_BDR)
        Setores.extend(Setores_Fundos)
        Setores = list(set(Setores))
        Labels = Setores

        for setor in Setores:
            valor = 0
            for i, item in enumerate(Setores_BDR):
                if item == setor:
                    valor += Values_BDR[i]
            for i, item in enumerate(Setores_Fundos):
                if item == setor:
                    valor += Values_Fundos[i]
            Values.append(valor)

        Labels.append("Criptos")
        Values.append(sum([x[0] + x[1] + x[2] for x in Values_Cripto]))

        ParaOrdenar = []
        for i, label in enumerate(Labels):
            ParaOrdenar.append((label,Values[i]))
        Ordenado = sorted(ParaOrdenar, key=lambda tup: tup[1])
        Labels = list(map(lambda tup: tup[0], Ordenado))
        Values = list(map(lambda tup: tup[1], Ordenado))

        values = [x for x in Values if round(x,2) > self.MostrarValoresMaioresQue]
        labels = [Labels[i] for i, x in enumerate(Values) if round(x,2) > self.MostrarValoresMaioresQue]

        explode = ()
        for i in values: explode += (0.03,)

        plt.axis('equal')
        plt.title("Por setor", color='w', fontsize=20)
        plt.tight_layout()

        if sum(values)==0:
            patches, texts = plt.pie([1], labels = ["Vazio"], startangle = 90, shadow = True, normalize = True)
        else:
            patches, texts, pcts = plt.pie(values, labels = labels, startangle = 90, shadow = True, normalize = True, explode = explode,
                                           autopct = lambda pct: self.getPercentage(pct, values))
            plt.setp(pcts, color='white')

        for i, patch in enumerate(patches):
            texts[i].set_color(patch.get_facecolor())

        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page49_Subtipos(self):
        # Gráfico de barras dos subtipos
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        GraphWidget_ax, axs = plt.subplots(nrows=1, ncols=3, figsize=(30,4), clear=True)#, sharey=True)
        GraphWidget_ax.set_facecolor("black")
        if self.HMI.ShowValues: axs[0].set_ylabel(UserCoin, fontsize=11)
        for i in [0, 1, 2]:
            axs[i].set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
            axs[i].xaxis.label.set_color('w')
            axs[i].yaxis.label.set_color('w')
            axs[i].yaxis.label.set_color('black')
            axs[i].tick_params(axis='y', colors='black')
            axs[i].tick_params(axis='x', colors='w')
            axs[i].grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)
            for eixo in ['bottom', 'top', 'right', 'left']: axs[i].spines[eixo].set_color('black')
        if self.HMI.ShowValues:
            axs[0].yaxis.label.set_color('w')
            axs[0].tick_params(axis='y', colors='w')

        Labels_0, Labels_1, Values_0, Values_1, Setores_0, Setores_1 = self.HMI.DBManager.GetDetailedDataForAtivosInternacionais()
        Labels_2, Values_2 = self.HMI.DBManager.GetDetailedDataForCriptomoedas()
        Values_0_SumTotal = sum(Values_0)
        Labels_0 = [Labels_0[i] for i, x in enumerate(Values_0) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_0 = [x for i, x in enumerate(Values_0) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_1_SumTotal = sum(Values_1)
        Labels_1 = [Labels_1[i] for i, x in enumerate(Values_1) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_1 = [x for i, x in enumerate(Values_1) if round(x,2) > self.MostrarValoresMaioresQue]
        Values_2_SumTotal = sum([x[0]+x[1]+x[2] for x in Values_2])
        Labels_2 = [Labels_2[i] for i, x in enumerate(Values_2) if round(sum(x),2) > self.MostrarValoresMaioresQue]
        Values_2 = [x[0]+x[1]+x[2] for x in Values_2 if round(sum(x),2) > self.MostrarValoresMaioresQue]
        df = pd.DataFrame({'Total': [Values_2_SumTotal for x in Values_2]})

        if len(Values_0) > 0 and len(Values_1) > 0 and Values_2_SumTotal > 0:
            for i in [0,1,2]: axs[i].set_ylim(0, max(max(max(Values_0), max(Values_1)), Values_2_SumTotal) * 1.1)
        elif len(Values_0) > 0 and len(Values_1) > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, max(max(Values_0), max(Values_1)) * 1.1)
        elif len(Values_0) > 0 and Values_2_SumTotal > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, max(max(Values_0), Values_2_SumTotal) * 1.1)
        elif len(Values_1) > 0 and Values_2_SumTotal > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, max(max(Values_1), Values_2_SumTotal) * 1.1)
        elif len(Values_0) > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, max(Values_0) * 1.1)
        elif len(Values_1) > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, max(Values_1) * 1.1)
        elif Values_2_SumTotal > 0:
            for i in [0, 1, 2]: axs[i].set_ylim(0, Values_2_SumTotal * 1.1)

        axs[0].set_title('BDR', fontsize=26, color='white')
        if len(Values_0) > 0:
            axs[0].bar(Labels_0, Values_0, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_0)):
                    axs[0].text(n, Values_0[n], str('R$%.2f' % Values_0[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_0)):
                    if Values_0_SumTotal > 0: axs[0].text(n, Values_0[n], str('%.1f' % (Values_0[n]/Values_0_SumTotal*100))+"%", ha='center', fontsize=14, color='g')
                    else: axs[0].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[0].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[0].text(0, 0, '0', ha='center', fontsize=14, color='g')

        axs[1].set_title('Fundos', fontsize=26, color='white')
        if len(Values_1) > 0:
            axs[1].bar(Labels_1, Values_1, edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues:
                for n in range(len(Labels_1)):
                    axs[1].text(n, Values_1[n], str('R$%.2f' % Values_1[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(Labels_1)):
                    if Values_1_SumTotal > 0: axs[1].text(n, Values_1[n], str('%.1f' % (Values_1[n]/Values_1_SumTotal*100))+"%", ha='center', fontsize=14, color='g')
                    else: axs[1].text(n, 0, '0', ha='center', fontsize=14, color='g')
        else:
            axs[1].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[1].text(0, 0, '0', ha='center', fontsize=14, color='g')

        axs[2].set_title('Criptomoedas', fontsize=26, color='white')
        if Values_2_SumTotal > 0 and Values_2_SumTotal > self.MostrarValoresMaioresQue:
            df['Total'].plot(kind = 'line', ax=axs[2])
            ax2 = axs[2].twinx()
            ax2.yaxis.tick_right()
            ax2.yaxis.label.set_color(str('#%02x%02x%02x' % (0, 250, 180)))
            if self.HMI.ShowValues: ax2.tick_params(axis='y', labelcolor=str('#%02x%02x%02x' % (0, 250, 180)))
            if len(Values_2) > 0:
                ax2.set_ylim(0, max(Values_2) * 1.1)
                ax2.bar(Labels_2, Values_2, facecolor = 'gray', edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            else:
                ax2.yaxis.label.set_color('black')
                ax2.tick_params(axis='y', colors='black')
                ax2.bar(['Vazio'], [Values_2_SumTotal], facecolor = 'black', edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))

            if self.HMI.ShowValues:
                axs[2].text(0, Values_2_SumTotal+1, str('R$%.2f' % Values_2_SumTotal), ha='left', fontsize=14, color='g')
                for n in range(len(Labels_2)):
                    ax2.text(n, Values_2[n], str('R$%.2f' % Values_2[n]), ha='center', fontsize=12, color=str('#%02x%02x%02x' % (0, 250, 180)))
            else:
                for n in range(len(Labels_2)):
                    if Values_2_SumTotal > 0: ax2.text(n, Values_2[n], str('%.1f' % (Values_2[n]/Values_2_SumTotal*100))+"%", ha='center', fontsize=12, color=str('#%02x%02x%02x' % (0, 250, 180)))
                    else: ax2.text(n, 0, "0", ha='center', fontsize=12, color=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[2].grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)
        else:
            axs[2].bar(["Vazio"], [0], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            axs[2].text(0, 0, '0', ha='center', fontsize=14, color='g')

        GraphWidget = FigureCanvas(GraphWidget_ax)
        plt.close(GraphWidget_ax)
        return GraphWidget

    def CreateGraph_Page50_MainGraph_VisaoGeral(self):
        # Gráfico de funil da visão geral
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        for tick in ax.axes.get_xticklines(): tick.set_visible(False)
        for tick in ax.axes.get_yticklines(): tick.set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.xaxis.label.set_color('w'); ax.yaxis.label.set_color('w')
        ax.tick_params(axis='y', colors='w')
        for eixo in ['bottom', 'top', 'right', 'left']: ax.spines[eixo].set_color('black')

        Labels, Values = self.HMI.DBManager.GetDetailedDataForCriptomoedas()
        Values_SumTotal = sum([x[0] + x[1] + x[2] for x in Values])
        values = [sum(x) for x in Values if round(sum(x),2) > self.MostrarValoresMaioresQue]
        per = list(map(lambda item: str(f'{round(item/Values_SumTotal*100, 2):.2f}')+"%", values))
        labels = [Labels[i] for i, x in enumerate(Values) if round(sum(x),2) > self.MostrarValoresMaioresQue]

        if len(values) > 0:
            plt.title('Visão geral', fontsize=26, color='white')
            values_max = max(values)+2; values_min = 0
            plt.xlim(values_min, values_max)
            heights = [-0.25]
            for y in range(len(labels)-1): heights.append(0.78+((len(heights)-1)*0.995))
            for idx, val in enumerate(values):
                left = (values_max - val)/2
                plt.barh(labels[idx], values[idx], left = left, color=str('#%02x%02x%02x' % (120, 200, 250)), height=0.8, edgecolor='black')
                if self.HMI.ShowValues:
                    plt.text(values_max/2, heights[idx], str(f'{round(values[idx], 2):.2f}'), ha='center', fontsize=15, color='g')
                    plt.ylabel(UserCoin, fontsize=11)
                else:
                    plt.text(values_max/2, heights[idx], per[idx], ha='center', fontsize=15, color='g')
        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page50_MainGraph_AtivoPorCorretora(self):
        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))

        Moeda = self.HMI.ComboBox_Ativos.currentText()
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        if Moeda == "Todos":
            self.HMI.ComboBox_Ativos.setCurrentIndex(1)
            Moeda = self.HMI.ComboBox_Ativos.currentText()
            self.Custo = self.HMI.DBManager.GetCustoAtivo(Moeda, "Cripto")
            self.Retorno = self.HMI.DBManager.GetEstoqueAtivo(Moeda, "Cripto") * self.HMI.DBManager.GetCotacao(Moeda)
            if self.HMI.ShowValues:
                self.HMI.TextBox_Custo.setText('Custo: '+UserCoin+' '+str(f'{round(self.Custo, 2):.2f}'))
                self.HMI.TextBox_Retorno.setText('Retorno: '+UserCoin+' '+str(f'{round(self.Retorno, 2):.2f}'))
            else:
                self.HMI.TextBox_Custo.setText('Custo: X')
                self.HMI.TextBox_Retorno.setText('Retorno: '+str(round((self.Retorno-self.Custo)/self.Custo*100,1))+'%X')
            if self.Retorno >= self.Custo:
                self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
            else:
                self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

        CotacaoMoeda = self.HMI.DBManager.GetCotacao(Moeda)

        Labels, Values = self.HMI.DBManager.GetDetailedDataForCriptomoedas_AtivoPorCorretora(Moeda)
        values = [x for x in Values if round(x,2) > self.MostrarValoresMaioresQue]
        labels = [Labels[i] for i, x in enumerate(Values) if round(x,2) > self.MostrarValoresMaioresQue]

        explode = ()
        for i in values: explode += (0.03,)

        plt.axis('equal')
        plt.title("Cotação "+Moeda+": "+UserCoin+str(f'{round(CotacaoMoeda,2):.2f}'), color='w', fontsize=20)
        plt.tight_layout()

        if len(values)==0:
            patches, texts = plt.pie([1], labels = ["Vazio"], startangle = 90, shadow = True, normalize = True)
        else:
            patches, texts, pcts = plt.pie(values, labels = labels, startangle = 90, shadow = True, normalize = True, explode = explode,
                                           autopct = lambda pct: self.getPercentage(pct, values))
            plt.setp(pcts, color='white')

        for i, patch in enumerate(patches):
            texts[i].set_color(patch.get_facecolor())

        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page50_MainGraph_TotalDeUserCoinPorCorretora(self):
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()

        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12,5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))

        Labels, Values = self.HMI.DBManager.GetDetailedDataForCriptomoedas_TotalDeUserCoinPorCorretora()
        values = [x for x in Values if round(x,2) > self.MostrarValoresMaioresQue]
        labels = [Labels[i] for i, x in enumerate(Values) if round(x,2) > self.MostrarValoresMaioresQue]

        explode = ()
        for i in values: explode += (0.03,)

        plt.axis('equal')
        plt.title("Total em "+UserCoin+" por corretora", color='w', fontsize=20)
        plt.tight_layout()

        if len(values)==0:
            patches, texts = plt.pie([1], labels = ["Vazio"], startangle = 90, shadow = True, normalize = True)
        else:
            patches, texts, pcts = plt.pie(values, labels = labels, startangle = 90, shadow = True, normalize = True, explode = explode,
                                           autopct = lambda pct: self.getPercentage(pct, values))
            plt.setp(pcts, color='white')

        for i, patch in enumerate(patches):
            texts[i].set_color(patch.get_facecolor())

        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateGraph_Page50_Distribuicao(self):
        # Gráfico de barras de distribuição de moedas, com separação de Trade, Stake e Hold
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        colors = {'(S) Stake':str('#%02x%02x%02x' % (120, 250, 210)),
                  '(H) Hold':str('#%02x%02x%02x' % (10, 210, 250)),
                  '(T) Trade':str('#%02x%02x%02x' % (120, 200, 250))}
        GraphWidget_ax, ax = plt.subplots(1, figsize=(100,5))
        GraphWidget_ax.clear()
        GraphWidget_ax.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))
        ax.xaxis.label.set_color('w')
        ax.yaxis.label.set_color('w')
        if self.HMI.ShowValues: ax.tick_params(axis='y', colors='w')
        ax.tick_params(axis='x', colors='w')
        for eixo in ['bottom', 'top', 'right', 'left']: ax.spines[eixo].set_color('black')
        Labels, Values = self.HMI.DBManager.GetDetailedDataForCriptomoedas()
        values = [(x[0],x[1],x[2]) for x in Values if round(sum(x),2) > self.MostrarValoresMaioresQue]
        per = []
        for item in values:
            if sum(item) == 0: per_trade = 0
            else: per_trade = round(item[0]/sum(item)*100, 2)
            if sum(item) == 0: per_hold = 0
            else: per_hold = round(item[1]/sum(item)*100, 2)
            if sum(item) == 0: per_stake = 0
            else: per_stake = round(item[2]/sum(item)*100, 2)
            per.append((str(f'{per_trade:.2f}')+"%",
                        str(f'{per_hold:.2f}')+"%",
                        str(f'{per_stake:.2f}')+"%"))
        labels = [Labels[i] for i, x in enumerate(Values) if round(sum(x),2) > self.MostrarValoresMaioresQue]
        if len(values) > 0:
            plt.title('Distribuição', fontsize=26, color='white')
            if self.HMI.ShowValues: plt.ylabel(UserCoin, fontsize=11)
            values_aux = [sum(x) for x in Values if round(sum(x),2) > self.MostrarValoresMaioresQue]
            values_max = max(values_aux)*1.1
            plt.ylim(0, values_max)
            plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)
            handles = [plt.Rectangle((0,0),1,1, color=colors[kind]) for kind in list(colors.keys())]
            plt.legend(handles, list(colors.keys()), prop={'size': 11})

            Trades = list(map(lambda value: value[0], values))
            Holds = list(map(lambda value: value[1], values))
            Stakes = list(map(lambda value: value[2], values))

            def funcao_aux1(values):
                if (values[0] + values[1] + values[2]) > 0:
                    return values[0] / (values[0] + values[1] + values[2]) * 100
                return 0
            def funcao_aux2(values):
                if (values[0] + values[1] + values[2]) > 0:
                    return values[1] / (values[0] + values[1] + values[2]) * 100
                return 0
            def funcao_aux3(values):
                if (values[0] + values[1] + values[2]) > 0:
                    return values[2] / (values[0] + values[1] + values[2]) * 100
                return 0

            TradesPer = list(map(funcao_aux1, values))
            HoldsPer = list(map(funcao_aux2, values))
            StakesPer = list(map(funcao_aux3, values))

            plt.bar(labels, Trades, facecolor=colors['(T) Trade'], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            plt.bar(labels, Holds, bottom=Trades, facecolor=colors['(H) Hold'], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))
            plt.bar(labels, Stakes, bottom=np.add(Holds, Trades), facecolor=colors['(S) Stake'], edgecolor=str('#%02x%02x%02x' % (0, 250, 180)))

            if self.HMI.ShowValues:
                for n in range(len(labels)):
                    if round(Trades[n],2) > 0: # Trade
                        plt.text(n, Trades[n], str('(T)R$%.2f' % Trades[n]), ha='center', fontsize=14, color='g')
                    if round(Holds[n],2) > 0: # Hold
                        plt.text(n, Holds[n]+Trades[n], str('(H)R$%.2f' % Holds[n]), ha='center', fontsize=14, color='g')
                    if round(Stakes[n],2) > 0: # Stake
                        plt.text(n, Stakes[n]+Holds[n]+Trades[n], str('(S)R$%.2f' % Stakes[n]), ha='center', fontsize=14, color='g')
            else:
                for n in range(len(labels)):
                    if round(Trades[n],2) > 0: # Trade
                        plt.text(n, Trades[n], str('(T)%.1f' % TradesPer[n])+"%", ha='center', fontsize=14, color='g')
                    if round(Holds[n],2) > 0: # Hold
                        plt.text(n, Holds[n]+Trades[n], str('(H)%.1f' % HoldsPer[n])+"%", ha='center', fontsize=14, color='g')
                    if round(Stakes[n],2) > 0: # Stake
                        plt.text(n, Stakes[n]+Holds[n]+Trades[n], str('(S)%.1f' % StakesPer[n])+"%", ha='center', fontsize=14, color='g')

        GraphWidget = FigureCanvas(GraphWidget_ax)
        plt.close(GraphWidget_ax)
        return GraphWidget

    def CreateGraph_AtivoPorCorretora(self):
        GraphWidget_MainGraph, ax = plt.subplots(1, figsize=(12, 5))
        GraphWidget_MainGraph.clear()
        GraphWidget_MainGraph.set_facecolor("black")
        ax = plt.gca()
        ax.set_facecolor(str('#%02x%02x%02x' % (0, 0, 0)))

        Ativo = self.HMI.ComboBox_Ativos.currentText()
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        if Ativo == "Todos":
            self.HMI.ComboBox_Ativos.setCurrentIndex(1)
            Ativo = self.HMI.ComboBox_Ativos.currentText()

            self.Custo = self.HMI.DBManager.GetCustoAtivo(Ativo, "Bolsa")
            self.Retorno = self.HMI.DBManager.GetEstoqueAtivo(Ativo, "Bolsa") * self.HMI.DBManager.GetCotacao(Ativo)
            if self.HMI.ShowValues:
                self.HMI.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.Custo, 2):.2f}'))
                self.HMI.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.Retorno, 2):.2f}'))
            else:
                self.HMI.TextBox_Custo.setText('Custo: X')
                self.HMI.TextBox_Retorno.setText('Retorno: ' + str(round((self.Retorno - self.Custo) / self.Custo * 100, 2)) + '%X')
            if self.Retorno >= self.Custo:
                self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
            else:
                self.HMI.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

        CotacaoAtivo = self.HMI.DBManager.GetCotacao(Ativo)

        Labels, Values = self.HMI.DBManager.GetDetailedData_AtivoPorCorretora(Ativo)
        values = [x for x in Values if round(x, 2) > self.MostrarValoresMaioresQue]
        labels = [Labels[i] for i, x in enumerate(Values) if round(x, 2) > self.MostrarValoresMaioresQue]

        explode = ()
        for i in values: explode += (0.03,)

        plt.axis('equal')
        plt.title("Cotação " + Ativo + ": " + UserCoin + str(f'{round(CotacaoAtivo, 2):.2f}'), color='w', fontsize=20)
        plt.tight_layout()

        if len(values) == 0:
            patches, texts = plt.pie([1], labels=["Vazio"], startangle=90, shadow=True, normalize=True)
        else:
            patches, texts, pcts = plt.pie(values, labels=labels, startangle=90, shadow=True, normalize=True, explode=explode,
                                           autopct=lambda pct: self.getPercentage(pct, values))
            plt.setp(pcts, color='white')

        for i, patch in enumerate(patches):
            texts[i].set_color(patch.get_facecolor())

        GraphWidget = FigureCanvas(GraphWidget_MainGraph)
        plt.close(GraphWidget_MainGraph)
        return GraphWidget

    def CreateTable_11_1(self):
        coin = self.HMI.DBManager.GetUserCoinCurrency()
        HHeader = ['Corretora',
                   'Conta-corrente ('+coin+')']
        data = self.HMI.DBManager.GetAllContasCorrente()

        self.Table_ContasCorrenteHeader.setRowCount(1)
        self.Table_ContasCorrenteHeader.setColumnCount(len(HHeader))

        self.Table_ContasCorrenteHeader.setShowGrid(False)
        self.Table_ContasCorrenteHeader.setFont(self.HMI.font12)
        self.Table_ContasCorrenteHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                        color: white;
                                                                        border: 1px solid rgba(0, 0, 0, 0);}
                                                          QTableView {border-top: 0px solid white;
                                                                      border-right: 0px dashed white;
                                                                      border-left: 0px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.Table_ContasCorrenteHeader.verticalHeader().hide()
        self.Table_ContasCorrenteHeader.horizontalHeader().hide()

        celula0 = QTableWidgetItem(str(HHeader[0]))
        celula0.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
        celula0.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        celula1 = QTableWidgetItem(str(HHeader[1]))
        celula1.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
        celula1.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        self.Table_ContasCorrenteHeader.setItem(0, 0, celula0)
        self.Table_ContasCorrenteHeader.setItem(0, 1, celula1)

        self.Table_ContasCorrenteHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.Table_ContasCorrenteHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.Table_ContasCorrenteHeader.resizeColumnsToContents()

    def CreateTable_11_2(self):
        def evt_update_progress_11_2(r, c, text):
            it = self.Table_ContasCorrente.item(r, c)
            if not self.HMI.ShowValues and c == 1: text = "***"
            it = QTableWidgetItem(text)
            it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
            it.setTextAlignment(Qt.AlignCenter)
            self.Table_ContasCorrente.setItem(r, c, it)

        def evt_define_table_width_11_2(data, HHeader):
            def SetTableWidth_11_2(SizeCol0, SizeCol1):
                    self.Table_ContasCorrente.adjustSize()
                    self.Table_ContasCorrente.setColumnWidth(0, SizeCol0)
                    self.Table_ContasCorrente.setColumnWidth(1, SizeCol1)
                    width = self.Table_ContasCorrente.verticalHeader().width()
                    width += self.Table_ContasCorrente.horizontalHeader().length()
                    if self.Table_ContasCorrente.horizontalScrollBar().isVisible():
                        width += self.Table_ContasCorrente.horizontalScrollBar().width()
                    width += self.Table_ContasCorrente.frameWidth() * 2
                    self.Table_ContasCorrente.setFixedWidth(width)

            self.Table_ContasCorrente.setRowCount(len(data))
            self.Table_ContasCorrente.setColumnCount(len(HHeader))
            SizeCol0,SizeCol1 = self.HMI.GetSizeOfTableColumns(data, HHeader)
            SetTableWidth_11_2(SizeCol0, SizeCol1)

        def evt_finished_progress_11_2():
            self.Table_ContasCorrente.setVisible(True)
            self.HMI.unsetCursor()

            data = self.HMI.DBManager.GetAllContasCorrente()
            coin = self.HMI.DBManager.GetUserCoinCurrency()
            HHeader = ['Corretora',
                       'Conta-corrente ('+coin+')']
            SizeCol0,SizeCol1 = self.HMI.GetSizeOfTableColumns(data, HHeader)

            self.Table_ContasCorrenteHeader.adjustSize()
            self.Table_ContasCorrenteHeader.setColumnWidth(0, SizeCol0)
            self.Table_ContasCorrenteHeader.setColumnWidth(1, SizeCol1*.98)

            self.Table_ContasCorrente.adjustSize()
            self.Table_ContasCorrente.setColumnWidth(0, SizeCol0)
            self.Table_ContasCorrente.setColumnWidth(1, SizeCol1*.98)

        self.Thread_CreateTable_11_2 = WorkerThread('Thread_CreateTable_11_2', self.HMI)
        self.Thread_CreateTable_11_2.update_table.connect(evt_update_progress_11_2)
        self.Thread_CreateTable_11_2.finished.connect(evt_finished_progress_11_2)
        self.Thread_CreateTable_11_2.define_table_width.connect(evt_define_table_width_11_2)
        self.Thread_CreateTable_11_2.Function_define_table_width_11_2()
        self.Thread_CreateTable_11_2.start()

    def CallCreatePage(self):
        if self.GraficoEspecifico_Name in ["Ações Nacionais", "Fundos de investimentos: Ações e Negócios"]:
            self.HMI.CreatePage('46')
        elif self.GraficoEspecifico_Name in ["Fundos Imobiliários", "Terrenos", "Construções"]:
            self.HMI.CreatePage('47')
        elif self.GraficoEspecifico_Name in ["Renda Fixa", "Tesouro Direto e Títulos Públicos", "Previdência Privada", "COE", "Fundos de Investimento: Renda Fixa"]:
            self.HMI.CreatePage('48')
        elif self.GraficoEspecifico_Name in ["BDR", "Fundos de Investimento: Ações Internacionais"]:
            self.HMI.CreatePage('49')
        elif self.GraficoEspecifico_Name in ["Criptomoedas"]:
            self.HMI.CreatePage('50')

    def ProximoGraficoEspecifico(self, TipoDeAtivo):
        if TipoDeAtivo == "Ações e Negócios":
            Subtipos = ["Ações Nacionais", "Fundos de investimentos: Ações e Negócios"]
            if self.GraficoEspecifico_Name in Subtipos:
                CurrentIndex = Subtipos.index(self.GraficoEspecifico_Name)
                if len(Subtipos) > CurrentIndex+1: index = CurrentIndex+1
                else: index = 0
                self.GraficoEspecifico_Name = Subtipos[index]
            else:
                self.GraficoEspecifico_Name = Subtipos[0]
        elif TipoDeAtivo == "Real Estate":
            Subtipos = ["Fundos Imobiliários", "Terrenos", "Construções"]
            if self.GraficoEspecifico_Name in Subtipos:
                CurrentIndex = Subtipos.index(self.GraficoEspecifico_Name)
                if len(Subtipos) > CurrentIndex+1: index = CurrentIndex+1
                else: index = 0
                self.GraficoEspecifico_Name = Subtipos[index]
            else:
                self.GraficoEspecifico_Name = Subtipos[0]
        elif TipoDeAtivo == "Caixa":
            Subtipos = ["Renda Fixa", "Tesouro Direto e Títulos Públicos", "Previdência Privada", "COE", "Fundos de Investimento: Renda Fixa"]
            if self.GraficoEspecifico_Name in Subtipos:
                CurrentIndex = Subtipos.index(self.GraficoEspecifico_Name)
                if len(Subtipos) > CurrentIndex+1: index = CurrentIndex+1
                else: index = 0
                self.GraficoEspecifico_Name = Subtipos[index]
            else:
                self.GraficoEspecifico_Name = Subtipos[0]
        elif TipoDeAtivo == "Ativos Internacionais":
            Subtipos = ["BDR", "Fundos de Investimento: Ações Internacionais", "Criptomoedas"]
            if self.GraficoEspecifico_Name in Subtipos:
                CurrentIndex = Subtipos.index(self.GraficoEspecifico_Name)
                if len(Subtipos) > CurrentIndex+1: index = CurrentIndex+1
                else: index = 0
                self.GraficoEspecifico_Name = Subtipos[index]
            else:
                self.GraficoEspecifico_Name = Subtipos[0]
        self.CreateGraph_Page11_Especifica()

    def OnButtonPressed(self, ButtonPressed):
        FontColorLineEdit = "green"
        if ButtonPressed == "Change Carteira Graph":
            self.Flag_RecalcularGraficos = True
            self.HMI.GraphWidget_Carteira.deleteLater()
            if self.CarteiraGraph_id == 'pie': self.HMI.GraphWidget_Carteira = self.CreateGraph_Page11_Carteira_bar()
            elif self.CarteiraGraph_id == 'bar': self.HMI.GraphWidget_Carteira = self.CreateGraph_Page11_Carteira_pie()
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_Carteira, 2, 2, 2, 2, Qt.AlignHCenter | Qt.AlignBottom)
            if self.HMI.frameGeometry().width() / self.HMI.frameGeometry().height() < 1.9577: proporcao = 1 / 6
            elif self.HMI.frameGeometry().width() / self.HMI.frameGeometry().height() < 2.6202: proporcao = 1 / 8
            else: proporcao = 1 / 10
            self.HMI.GraphWidget_Carteira.setFixedSize(int(self.HMI.frameGeometry().width() * proporcao), int(self.HMI.frameGeometry().width() * proporcao))
            self.HMI.Button_CarteiraInvisivel.deleteLater()
            self.HMI.Button_CarteiraInvisivel = QPushButton()
            self.HMI.Button_CarteiraInvisivel.pressed.connect(lambda: self.OnButtonPressed('Change Carteira Graph'))
            self.HMI.Button_CarteiraInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
            self.HMI.Button_CarteiraInvisivel.setFixedSize(int(self.HMI.frameGeometry().width() * proporcao), int(self.HMI.frameGeometry().width() * proporcao))
            self.HMI.Button_CarteiraInvisivel.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_CarteiraInvisivel, 2, 2, 2, 2, Qt.AlignHCenter | Qt.AlignBottom)

        elif ButtonPressed == "TextBox_GastoMensal":
            try:
                aux = float(self.HMI.TextBox_GastoMensal.text())
                self.HMI.TextBox_MesesDeReserva.setFocus()
                self.HMI.DBManager.Update_GastoMensal(aux)
            except:
                self.HMI.TextBox_GastoMensal.setText(str(self.HMI.DBManager.GetGastoMensal()))

        elif ButtonPressed == "TextBox_MesesDeReserva":
            try:
                aux = int(float(self.HMI.TextBox_MesesDeReserva.text()))
                self.HMI.TextBox_MesesDeReserva.setText(str(aux))
                self.HMI.TextBox_MesesDeReserva.clearFocus()
                self.HMI.DBManager.Update_MesesDeReserva(aux)
            except:
                self.HMI.TextBox_MesesDeReserva.setText(str(self.HMI.DBManager.GetMesesDeReserva()))

        elif ButtonPressed == "MostrarValoresMaioresQue":
            self.MostrarValoresMaioresQue = float(self.HMI.TextBox_MostrarValoresMaioresQue.text())
            self.HMI.UpdatePage()
            self.HMI.TextBox_MostrarValoresMaioresQue.clearFocus()

        elif ButtonPressed == "Visão Geral":
            self.MainGraphIsShowing = "Visão Geral"
            self.HMI.UpdatePage()
            self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
            self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
            self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
            try:
                self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
            except:pass
            try:
                self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_Setor.setFont(self.HMI.font16)
            except:pass

        elif ButtonPressed == "Ativo por corretora":
            self.MainGraphIsShowing = "Ativo por corretora"
            self.HMI.UpdatePage()
            self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_VisaoGeral.setFont(self.HMI.font16)
            self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
            self.HMI.Button_AtivoPorCorretora.setFont(QFont('Times New Roman', 18, QFont.Bold))
            try:
                self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
            except:pass
            try:
                self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_Setor.setFont(self.HMI.font16)
            except:pass

        elif ButtonPressed == "Ativo por setor":
            self.MainGraphIsShowing = "Ativo por setor"
            self.HMI.UpdatePage()
            self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_VisaoGeral.setFont(self.HMI.font16)
            self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
            try:
                self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
            except:pass
            try:
                self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
                self.HMI.Button_Setor.setFont(QFont('Times New Roman', 18, QFont.Bold))
            except:pass

        elif ButtonPressed == "Total de UserCoin por corretora":
            self.MainGraphIsShowing = "Total de UserCoin por corretora"
            self.HMI.UpdatePage()
            self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_VisaoGeral.setFont(self.HMI.font16)
            self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
            try:
                self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
                self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(QFont('Times New Roman', 18, QFont.Bold))
            except:pass
            try:
                self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_Setor.setFont(self.HMI.font16)
            except:pass

        elif ButtonPressed == "Desempenho do ativo":
            self.MainGraphIsShowing = "Desempenho do ativo"
            self.HMI.UpdatePage()
            self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_VisaoGeral.setFont(self.HMI.font16)
            self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
            try:
                self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
            except:pass
            try:
                self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_Setor.setFont(self.HMI.font16)
            except:pass

    def getPercentage(self, pct, allvalues):
        absolute = float(pct / 100.*np.sum(allvalues))
        if self.HMI.ShowValues: retorno = "{:.1f}%\n({}{:.2f})".format(pct, self.HMI.DBManager.GetUserCoinCurrency(), absolute)
        else: retorno = "{:.1f}%".format(pct)
        return retorno