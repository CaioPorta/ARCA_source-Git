# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:54:52 2021

@author: caiop
"""

import pandas as pd
import numpy as np

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import HMI_Trades_Bolsa
import HMI_Trades_Criptomoedas

class HMI_Trades(object):
    def __init__(self, HMI):
        self.HMI = HMI
        QToolTip.setFont(QFont('Arial', 12))
        self.HMI_Trades_Bolsa = HMI_Trades_Bolsa.HMI_Trades_Bolsa(HMI)
        self.HMI_Trades_Criptomoedas = HMI_Trades_Criptomoedas.HMI_Trades_Criptomoedas(HMI)

    def CreatePage10(self):
        self.HMI.DTeST = "NotDefined"

        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: black")

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: black")

        Background_3 = QLabel()
        Background_3.setStyleSheet("background-color: black")

        Background_4 = QLabel()
        Background_4.setStyleSheet("background-color: black")

        self.HMI.Label_Titulo = QLabel('Edição das negociações')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Gif_TradesBolsa = QLabel()
        self.HMI.Movie_TradesBolsa = QMovie("./images/Trades_Bolsa_Icon.gif")
        self.HMI.Movie_TradesBolsa.setScaledSize(QSize().scaled(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-160), Qt.KeepAspectRatio))
        self.HMI.Gif_TradesBolsa.setMovie(self.HMI.Movie_TradesBolsa)
        self.HMI.Movie_TradesBolsa.start()

        self.HMI.Button_TradesBolsaInvisivel = QPushButton()
        self.HMI.Button_TradesBolsaInvisivel.pressed.connect(lambda: self.HMI.CreatePage('18'))
        self.HMI.Button_TradesBolsaInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_TradesBolsaInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-160))
        self.HMI.Button_TradesBolsaInvisivel.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_TradesBolsaInvisivel.setToolTip("Negociações B3")

        self.HMI.Button_TradesBolsa = QPushButton("Bolsa")
        self.HMI.Button_TradesBolsa.pressed.connect(lambda: self.HMI.CreatePage('18'))
        self.HMI.Button_TradesBolsa.setFont(self.HMI.font24)
        self.HMI.Button_TradesBolsa.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_TradesBolsa.setFixedSize(int(self.HMI.frameGeometry().width()/3*.96),int(self.HMI.frameGeometry().height()/5))
        self.HMI.Button_TradesBolsa.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_TradesBolsa.setToolTip("Negociações B3")

        self.HMI.Gif_TradesCriptomoedas = QLabel()
        self.HMI.Movie_TradesCriptomoedas = QMovie("./images/Trade_Cripto_Icon.gif")
        self.HMI.Movie_TradesCriptomoedas.setScaledSize(QSize().scaled(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-160), Qt.KeepAspectRatio))
        self.HMI.Gif_TradesCriptomoedas.setMovie(self.HMI.Movie_TradesCriptomoedas)
        self.HMI.Movie_TradesCriptomoedas.start()

        self.HMI.Button_TradesCriptomoedas = QPushButton("Criptomoedas")
        self.HMI.Button_TradesCriptomoedas.pressed.connect(lambda: self.HMI.CreatePage('19'))
        self.HMI.Button_TradesCriptomoedas.setFont(self.HMI.font24)
        self.HMI.Button_TradesCriptomoedas.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_TradesCriptomoedas.setFixedSize(int(self.HMI.frameGeometry().width()/3*.96),int(self.HMI.frameGeometry().height()/5))
        self.HMI.Button_TradesCriptomoedas.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_TradesCriptomoedas.setToolTip("Negociações de criptomoedas")

        self.HMI.Button_TradesCriptomoedasInvisivel = QPushButton()
        self.HMI.Button_TradesCriptomoedasInvisivel.pressed.connect(lambda: self.HMI.CreatePage('19'))
        self.HMI.Button_TradesCriptomoedasInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_TradesCriptomoedasInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-160))
        self.HMI.Button_TradesCriptomoedasInvisivel.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_TradesCriptomoedasInvisivel.setToolTip("Negociações de criptomoedas")

        self.HMI.Gif_Bancos = QLabel()
        self.HMI.Movie_Bancos = QMovie("./images/Bancos_Icon.gif")
        self.HMI.Movie_Bancos.setScaledSize(QSize().scaled(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-160), Qt.KeepAspectRatio))
        self.HMI.Gif_Bancos.setMovie(self.HMI.Movie_Bancos)
        self.HMI.Movie_Bancos.start()

        self.HMI.Button_BancosInvisivel = QPushButton()
        self.HMI.Button_BancosInvisivel.pressed.connect(lambda: self.HMI.CreatePage('Bancos'))
        self.HMI.Button_BancosInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_BancosInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-160))
        self.HMI.Button_BancosInvisivel.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_BancosInvisivel.setToolTip("Bancos")

        self.HMI.Button_Bancos = QPushButton("Bancos")
        self.HMI.Button_Bancos.pressed.connect(lambda: self.HMI.CreatePage('Bancos'))
        self.HMI.Button_Bancos.setFont(self.HMI.font24)
        self.HMI.Button_Bancos.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_Bancos.setFixedSize(int(self.HMI.frameGeometry().width()/3*.96),int(self.HMI.frameGeometry().height()/5))
        self.HMI.Button_Bancos.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Bancos.setToolTip("Bancos")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 0, 0, 5, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_3, 0, 1, 5, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_4, 0, 2, 5, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 2, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_TradesBolsa, 1, 0, 3, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_TradesBolsaInvisivel, 1, 0, 3, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_TradesBolsa, 4, 0, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_TradesCriptomoedas, 1, 1, 3, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_TradesCriptomoedasInvisivel, 1, 1, 3, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_TradesCriptomoedas, 4, 1, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_Bancos, 0, 2, 4, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_BancosInvisivel, 0, 2, 4, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Bancos, 4, 2, 1, 1)

        self.HMI.unsetCursor()

    def CreatePageBancos(self):
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_1.setFixedHeight(int(self.HMI.screen_height/20))

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        Background_3 = QLabel()
        Background_3.setStyleSheet("background-color: "+black)

        Background_4 = QLabel()
        Background_4.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Edição das Contas-Correntes em Bancos')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)
        self.HMI.Label_Titulo.setFixedHeight(int(self.HMI.screen_height/20))

        self.HMI.Button_AddBanco = QPushButton()
        self.HMI.Button_AddBanco.pressed.connect(lambda: self.HMI.CreatePage('BancosAdd'))
        self.HMI.Button_AddBanco.setFixedSize(40,40)
        self.HMI.Button_AddBanco.setIconSize(QSize(35, 35))
        self.HMI.Button_AddBanco.setIcon(QIcon("./images/add_user.png"))
        self.HMI.Button_AddBanco.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AddBanco.setToolTip("Adicionar banco")
        self.HMI.Button_AddBanco.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")

        self.HMI.Button_DeleteBanco = QPushButton()
        self.HMI.Button_DeleteBanco.pressed.connect(lambda: self.HMI.CreatePage('BancosDelete'))
        self.HMI.Button_DeleteBanco.setFixedSize(40,40)
        self.HMI.Button_DeleteBanco.setIconSize(QSize(35, 35))
        self.HMI.Button_DeleteBanco.setIcon(QIcon("./images/delete_broker.png"))
        self.HMI.Button_DeleteBanco.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_DeleteBanco.setToolTip("Deletar banco")
        self.HMI.Button_DeleteBanco.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")

        self.HMI.ComboBox_Bancos = QComboBox()
        self.HMI.ComboBox_Bancos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Bancos.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_Bancos.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        self.HMI.ComboBox_Bancos.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        for idx, banco in enumerate(self.HMI.DBManager.GetBancos()):
            self.HMI.ComboBox_Bancos.addItem(banco)
            try:
                if banco == self.HMI.TextBox_NovoBanco.text(): self.HMI.idxBanco = idx
            except: pass
        if self.HMI.idxBanco < len(self.HMI.DBManager.GetBancos()):
            self.HMI.ComboBox_Bancos.setCurrentIndex(self.HMI.idxBanco)

        self.HMI.Button_RenameBanco = QPushButton()
        self.HMI.Button_RenameBanco.pressed.connect(lambda: self.HMI.CreatePage('BancosRename'))
        self.HMI.Button_RenameBanco.setFixedSize(40,40)
        self.HMI.Button_RenameBanco.setIconSize(QSize(35, 35))
        self.HMI.Button_RenameBanco.setIcon(QIcon("./images/Rename.png"))
        self.HMI.Button_RenameBanco.setStyleSheet("QPushButton {background-color: black; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.HMI.Button_RenameBanco.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_RenameBanco.setToolTip("Renomear banco")

        self.HMI.Label_Title11 = QLabel()
        self.HMI.Label_Title11.setText('Editar\nConta-Corrente do')
        self.HMI.Label_Title11.setStyleSheet('color: white')
        self.HMI.Label_Title11.setFont(self.HMI.font24)
        self.HMI.Label_Title11.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Title2 = QLabel()
        self.HMI.Label_Title2.setText(self.HMI.ComboBox_Bancos.currentText())
        self.HMI.Label_Title2.setStyleSheet('color: green')
        self.HMI.Label_Title2.setFont(self.HMI.font26)

        self.HMI.Label_Msg2 = QLabel()
        self.HMI.Label_Msg2.setText("Registrado")
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_Msg2 = QLineEdit()
        self.HMI.TextBox_Msg2.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        self.HMI.TextBox_Msg2.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg2.setEnabled(False)
        self.HMI.TextBox_Msg2.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_Msg2.setText(self.HMI.DBManager.GetBancoCoinCurrency(self.HMI.ComboBox_Bancos.currentText())+' '+str(self.HMI.DBManager.GetValorEmContaCorrente_Banco(self.HMI.ComboBox_Bancos.currentText())))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Password)

        self.HMI.Label_CC = QLabel()
        self.HMI.Label_CC.setText("Valor atualizado ("+self.HMI.DBManager.GetBancoCoinCurrency(self.HMI.ComboBox_Bancos.currentText())+")")
        self.HMI.Label_CC.setStyleSheet('color: white')
        self.HMI.Label_CC.setFont(self.HMI.font16)
        self.HMI.Label_CC.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_CC = QLineEdit()
        self.HMI.TextBox_CC.returnPressed.connect(lambda: self.OnButtonPressed('BancosUpdateCC'))
        self.HMI.TextBox_CC.setStyleSheet('QLineEdit {background-color: white; color: green;}')
        self.HMI.TextBox_CC.setFont(self.HMI.font16)
        self.HMI.TextBox_CC.setAlignment(Qt.AlignCenter)

        self.HMI.Button_AtuatizarCC = QPushButton("Atualizar")
        self.HMI.Button_AtuatizarCC.pressed.connect(lambda: self.OnButtonPressed('BancosUpdateCC'))
        self.HMI.Button_AtuatizarCC.setStyleSheet('QPushButton {background-color: green; color: black} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_AtuatizarCC.setFont(self.HMI.font16)
        self.HMI.Button_AtuatizarCC.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AtuatizarCC.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_AtuatizarCC.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_AtuatizarCC.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_AtuatizarCC.setToolTip("Atualizar valor em conta corrente")

        if self.HMI.ComboBox_Bancos.currentText() == '':
            ButtonsEnabled = False
            color = 'red'
        else:
            ButtonsEnabled = True
            color = 'white'

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 1, Qt.AlignCenter)

        self.HMI.InsertGridLayout(2, 0, 1, 8)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 0, 0, 10, 4)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AddBanco, 0, 0, 1, 1, Qt.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DeleteBanco, 1, 0, 1, 1, Qt.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_Bancos, 0, 1, 2, 2, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RenameBanco, 0, 3, 2, 1, Qt.AlignLeft | Qt.AlignVCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Title11, 2, 0, 1, 4, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Title2, 3, 0, 1, 4, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 5, 0, 1, 4, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg2, 6, 0, 1, 4, Qt.AlignHCenter | Qt.AlignTop)

        self.HMI.InsertGridLayout(2, 8, 1, 12)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_3, 0, 0, 5, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_CC, 1, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_CC, 2, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AtuatizarCC, 3, 0, 1, 1, Qt.AlignCenter)

        if len(self.HMI.DBManager.GetBancos()) == 0:
            self.HMI.Button_RenameBanco.setEnabled(False)
            self.HMI.Button_DeleteBanco.setEnabled(False)
            self.HMI.TextBox_CC.setEnabled(False)
            self.HMI.Button_AtuatizarCC.setEnabled(False)
        else: self.HMI.TextBox_CC.setFocus()

    def CreatePageBancosAdd(self):
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Adicionar novo banco')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Insira o nome do banco:')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font16)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_NovoBanco = QLineEdit()
        self.HMI.TextBox_NovoBanco.returnPressed.connect(lambda: self.HMI.CreatePage('Bancos_'))
        self.HMI.TextBox_NovoBanco.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))

        self.HMI.Label_Msg2 = QLabel('Moeda Corrente:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.ComboBox_Currency = QComboBox()
        self.HMI.ComboBox_Currency.setFont(self.HMI.font16)
        self.HMI.ComboBox_Currency.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_Currency.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(0, 255, 0);")
        idxUserCoin = 0
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        for idx, coin in enumerate(self.HMI.DBManager.GetMoedasFiat()):
            self.HMI.ComboBox_Currency.addItem(coin)
            if coin == UserCoin: idxUserCoin = idx
        self.HMI.ComboBox_Currency.setCurrentIndex(idxUserCoin)

        self.HMI.Button_AdicionarBanco = QPushButton('Seguinte')
        self.HMI.Button_AdicionarBanco.pressed.connect(lambda: self.HMI.CreatePage('Bancos_'))
        self.HMI.Button_AdicionarBanco.setFont(self.HMI.font16)
        self.HMI.Button_AdicionarBanco.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_AdicionarBanco.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_AdicionarBanco.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_AdicionarBanco.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AdicionarBanco.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 19, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 7, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_NovoBanco, 8, 0, 1, 1, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 10, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_Currency, 11, 0, 1, 1, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AdicionarBanco, 12, 0, 2, 1, Qt.AlignHCenter)

        self.HMI.TextBox_NovoBanco.setFocus()

    def CreatePageBancosDelete(self):
        MessageBox_Msg1 = QMessageBox()
        MessageBox_Msg1.setWindowTitle("Deletar banco")
        MessageBox_Msg1.setText("Tem certeza que deseja deletar o "+self.HMI.ComboBox_Bancos.currentText()+'?\nNote que esse processo é irreversível.')
        MessageBox_Msg1.setIcon(QMessageBox.Question)
        MessageBox_Msg1.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
        MessageBox_Msg1.setDefaultButton(QMessageBox.Cancel)
        MessageBox_Msg1.setWindowIcon(QIcon(".\images\logoARCA.png"))

        returnValue = MessageBox_Msg1.exec()
        if returnValue == QMessageBox.Yes:
            self.HMI.DBManager.DeleteBanco()
            self.HMI.CreatePage('Bancos')

    def CreatePageBancosRename(self):
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Renomear banco')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Renomear banco \n'+self.HMI.ComboBox_Bancos.currentText())
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font22)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg2 = QLabel('Insira o novo nome do banco:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_NovoNomeBanco = QLineEdit()
        self.HMI.TextBox_NovoNomeBanco.returnPressed.connect(lambda: self.HMI.CreatePage('Bancos_'))
        self.HMI.TextBox_NovoNomeBanco.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))

        self.HMI.Button_RenomearBanco = QPushButton('Seguinte')
        self.HMI.Button_RenomearBanco.pressed.connect(lambda: self.HMI.CreatePage('Bancos_'))
        self.HMI.Button_RenomearBanco.setFont(self.HMI.font16)
        self.HMI.Button_RenomearBanco.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_RenomearBanco.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_RenomearBanco.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_RenomearBanco.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_RenomearBanco.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 19, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 7, 0, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 9, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_NovoNomeBanco, 10, 0, 1, 1, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RenomearBanco, 12, 0, 2, 1, Qt.AlignHCenter)

        self.HMI.TextBox_NovoNomeBanco.setFocus()

    def OnButtonPressed(self, ButtonPressed):
        if ButtonPressed == 'BancosUpdateCC':
            try:
                teste = float(self.HMI.TextBox_CC.text())
                self.HMI.DBManager.UpdateContaCorrente_Banco()
                self.HMI.TextBox_CC.setStyleSheet('background-color: white; color: green')
                self.HMI.TextBox_CC.setText('')
                self.HMI.TextBox_Msg2.setText(self.HMI.DBManager.GetBancoCoinCurrency(self.HMI.ComboBox_Bancos.currentText())+' '+str(self.HMI.DBManager.GetValorEmContaCorrente_Banco(self.HMI.ComboBox_Bancos.currentText())))
            except:
                self.HMI.TextBox_CC.setStyleSheet('background-color: white; color: red')