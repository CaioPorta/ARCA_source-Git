# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:54:52 2021

@author: caiop
"""

import pandas as pd
import numpy as np
import time

from datetime import datetime
from calendar import monthrange

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class HMI_Trades_Criptomoedas(object):
    def __init__(self, HMI):
        self.HMI = HMI
        QToolTip.setFont(QFont('Arial', 12))

    def CreatePage19(self): # Edição das negociações em criptomoedas
        self.HMI.BolsaOuCripto = "Cripto" # Variável usada no DBManager

        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        Background_3 = QLabel()
        Background_3.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Edição das negociações em criptomoedas')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Button_AddCorretora = QPushButton()
        self.HMI.Button_AddCorretora.setToolTip("Adicionar corretora")
        self.HMI.Button_AddCorretora.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.HMI.Button_AddCorretora.pressed.connect(lambda: self.HMI.CreatePage('37'))
        self.HMI.Button_AddCorretora.setFixedSize(40,40)
        self.HMI.Button_AddCorretora.setIconSize(QSize(35, 35))
        self.HMI.Button_AddCorretora.setIcon(QIcon("./images/add_user.png"))
        self.HMI.Button_AddCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_DeleteCorretora = QPushButton()
        self.HMI.Button_DeleteCorretora.setToolTip("Deletar corretora")
        self.HMI.Button_DeleteCorretora.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.HMI.Button_DeleteCorretora.pressed.connect(lambda: self.HMI.CreatePage('38'))
        self.HMI.Button_DeleteCorretora.setFixedSize(40,40)
        self.HMI.Button_DeleteCorretora.setIconSize(QSize(35, 35))
        self.HMI.Button_DeleteCorretora.setIcon(QIcon("./images/delete_broker.png"))
        self.HMI.Button_DeleteCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.ComboBox_Corretoras = QComboBox()
        self.HMI.ComboBox_Corretoras.setFont(self.HMI.font16)
        self.HMI.ComboBox_Corretoras.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_Corretoras.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        self.HMI.ComboBox_Corretoras.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        corretoras = self.HMI.DBManager.GetCorretoras()
        for idx, corretora in enumerate(corretoras):
            self.HMI.ComboBox_Corretoras.addItem(corretora)
            try:
                if corretora == self.HMI.TextBox_NovaCorretora.text(): self.HMI.idxCorretora = idx
            except: pass
        if self.HMI.idxCorretora < len(corretoras):
            self.HMI.ComboBox_Corretoras.setCurrentIndex(self.HMI.idxCorretora)

        UserCoin = self.HMI.DBManager.GetCorretoraCoinCurrency()

        self.HMI.Button_RenameCorretora = QPushButton()
        self.HMI.Button_RenameCorretora.setToolTip("Renomear corretora")
        self.HMI.Button_RenameCorretora.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.HMI.Button_RenameCorretora.pressed.connect(lambda: self.HMI.CreatePage('39'))
        self.HMI.Button_RenameCorretora.setFixedSize(40,40)
        self.HMI.Button_RenameCorretora.setIconSize(QSize(35, 35))
        self.HMI.Button_RenameCorretora.setIcon(QIcon("./images/Rename.png"))
        self.HMI.Button_RenameCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Label_Title11 = QLabel()
        self.HMI.Label_Title11.setText('Editar\noperações da')
        self.HMI.Label_Title11.setStyleSheet('color: white')
        self.HMI.Label_Title11.setFont(self.HMI.font24)
        self.HMI.Label_Title11.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Title2 = QLabel()
        self.HMI.Label_Title2.setText(self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Title2.setStyleSheet('color: green')
        self.HMI.Label_Title2.setFont(self.HMI.font26)

        self.HMI.Label_Msg1 = QLabel()
        self.HMI.Label_Msg1.setText("Visão geral")
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font22)

        self.HMI.Label_Msg2 = QLabel()
        self.HMI.Label_Msg2.setText("Patrimônio:")
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_Msg2 = QLineEdit()
        self.HMI.TextBox_Msg2.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        self.HMI.TextBox_Msg2.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg2.setEnabled(False)
        self.HMI.TextBox_Msg2.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_Msg2.setText(UserCoin+' ~'+str(self.HMI.DBManager.GetPatrimonioTotalCorretora()))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Password)

        self.HMI.Label_Msg6 = QLabel()
        self.HMI.Label_Msg6.setText("Investido:")
        self.HMI.Label_Msg6.setStyleSheet('color: white')
        self.HMI.Label_Msg6.setFont(self.HMI.font16)
        self.HMI.Label_Msg6.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_Msg6 = QLineEdit()
        self.HMI.TextBox_Msg6.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        self.HMI.TextBox_Msg6.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg6.setEnabled(False)
        self.HMI.TextBox_Msg6.setAlignment(Qt.AlignCenter)
        Investido = round(self.HMI.DBManager.GetTotalInvestidoEmCorretora(self.HMI.ComboBox_Corretoras.currentText(), "Cripto"), 2)
        self.HMI.TextBox_Msg6.setText(UserCoin+' ~'+str(Investido))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg6.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg6.setEchoMode(QLineEdit.Password)

        self.HMI.Label_Msg3 = QLabel()
        self.HMI.Label_Msg3.setText("Conta-Corrente:")
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font16)
        self.HMI.Label_Msg3.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_Msg3 = QLineEdit()
        self.HMI.TextBox_Msg3.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        self.HMI.TextBox_Msg3.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg3.setEnabled(False)
        self.HMI.TextBox_Msg3.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_Msg3.setText(UserCoin+' '+str(self.HMI.DBManager.GetValorEmContaCorrente(self.HMI.ComboBox_Corretoras.currentText(), "Cripto")))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg3.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg3.setEchoMode(QLineEdit.Password)

        self.HMI.Label_Msg4 = QLabel()
        self.HMI.Label_Msg4.setText("Última operação:")
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font16)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_Msg4 = QLabel()
        self.HMI.TextBox_Msg4.setStyleSheet('color: green')
        self.HMI.TextBox_Msg4.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg4.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_Msg4.setText(self.HMI.DBManager.GetDataUltimaOPRegistrada(self.HMI.ComboBox_Corretoras.currentText()))

        self.HMI.Label_Msg5 = QLabel()
        self.HMI.Label_Msg5.setText("Último depósito/saque:")
        self.HMI.Label_Msg5.setStyleSheet('color: white')
        self.HMI.Label_Msg5.setFont(self.HMI.font16)
        self.HMI.Label_Msg5.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_Msg5 = QLineEdit()
        self.HMI.TextBox_Msg5.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg5.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_Msg5.setEnabled(False)
        valor = round(self.HMI.DBManager.GetUltimoDepositoOuSaqueRegistrado(self.HMI.ComboBox_Corretoras.currentText()),2)
        if valor >= 0: self.HMI.TextBox_Msg5.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Msg5.setStyleSheet('QLineEdit {background-color: black; color: orange;}')
        self.HMI.TextBox_Msg5.setText(UserCoin+' '+str(valor))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg5.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg5.setEchoMode(QLineEdit.Password)

        self.HMI.Label_Title3 = QLabel()
        self.HMI.Label_Title3.setText("Editar operações")
        self.HMI.Label_Title3.setStyleSheet('color: white')
        self.HMI.Label_Title3.setFont(self.HMI.font24)

        self.HMI.Gif_AlterarOPCriptomoedas = QLabel()
        self.HMI.Movie_AlterarOPCriptomoedas = QMovie("./images/GIF_Registro.gif")
        self.HMI.Movie_AlterarOPCriptomoedas.setScaledSize(QSize().scaled(self.HMI.frameGeometry().width()*12/20,self.HMI.frameGeometry().height()*7/10*.95-60, Qt.KeepAspectRatio))
        self.HMI.Gif_AlterarOPCriptomoedas.setMovie(self.HMI.Movie_AlterarOPCriptomoedas)
        self.HMI.Movie_AlterarOPCriptomoedas.start()

        self.HMI.Button_AlterarOPCriptomoedasInvisivel = QPushButton()
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.setToolTip("Alterar operações de criptomoedas")
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.pressed.connect(lambda: self.HMI.CreatePage('40'))
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()*12/20),int(self.HMI.frameGeometry().height()*7/10*.95))
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_AlterarOPCriptomoedas = QPushButton("Registros")
        self.HMI.Button_AlterarOPCriptomoedas.setToolTip("Alterar operações de criptomoedas")
        self.HMI.Button_AlterarOPCriptomoedas.pressed.connect(lambda: self.HMI.CreatePage('40'))
        self.HMI.Button_AlterarOPCriptomoedas.setStyleSheet('QPushButton{background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_AlterarOPCriptomoedas.setFont(self.HMI.font16)
        self.HMI.Button_AlterarOPCriptomoedas.setFixedSize(int(self.HMI.frameGeometry().width()*12/20),int(self.HMI.frameGeometry().height()*1/10*.95))
        self.HMI.Button_AlterarOPCriptomoedas.setCursor(QCursor(Qt.PointingHandCursor))

        if self.HMI.ComboBox_Corretoras.currentText() == '':
            ButtonsEnabled = False
            color = 'red'
        else:
            ButtonsEnabled = True
            color = 'white'
        self.HMI.Button_AlterarOPCriptomoedas.setEnabled(ButtonsEnabled)
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.setEnabled(ButtonsEnabled)
        self.HMI.Button_AlterarOPCriptomoedas.setStyleSheet('background-color: black; color: '+color+'; border: 1px solid rgb(0, 0, 0)')

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 1, Qt.AlignCenter)

        self.HMI.InsertGridLayout(2, 0, 1, 8)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 0, 0, 15, 4)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AddCorretora, 0, 0, 1, 1, Qt.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DeleteCorretora, 1, 0, 1, 1, Qt.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_Corretoras, 0, 1, 2, 2, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RenameCorretora, 0, 3, 2, 1, Qt.AlignLeft | Qt.AlignVCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Title11, 2, 0, 1, 4, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Title2, 3, 0, 1, 4, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 4, 0, 1, 4, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 5, 0, 1, 4, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg2, 6, 0, 1, 4, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg6, 7, 0, 1, 4, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg6, 8, 0, 1, 4, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 9, 0, 1, 4, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg3, 10, 0, 1, 4, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 11, 0, 1, 4, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg4, 12, 0, 1, 4, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 13, 0, 1, 4, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg5, 14, 0, 1, 4, Qt.AlignHCenter | Qt.AlignTop)

        self.HMI.InsertGridLayout(2, 8, 1, 12)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_3, 0, 0, 5, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Title3, 0, 0, 3, 1, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_AlterarOPCriptomoedas, 1, 0, 3, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AlterarOPCriptomoedasInvisivel, 1, 0, 3, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AlterarOPCriptomoedas, 4, 0, 1, 1, Qt.AlignCenter)

        if len(corretoras) == 0:
            self.HMI.Button_RenameCorretora.setEnabled(False)
            self.HMI.Button_DeleteCorretora.setEnabled(False)

    def CreatePage37(self): # Adicionar nova corretora de criptomoedas
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Adicionar nova corretora de criptomoedas')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Insira o nome da nova corretora:')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font16)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_NovaCorretora = QLineEdit()
        self.HMI.TextBox_NovaCorretora.returnPressed.connect(lambda: self.HMI.CreatePage('19_'))
        self.HMI.TextBox_NovaCorretora.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))

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

        self.HMI.Button_AdicionarCorretora = QPushButton('Seguinte')
        self.HMI.Button_AdicionarCorretora.pressed.connect(lambda: self.HMI.CreatePage('19_'))
        self.HMI.Button_AdicionarCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AdicionarCorretora.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_AdicionarCorretora.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_AdicionarCorretora.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_AdicionarCorretora.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AdicionarCorretora.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 19, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 7, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_NovaCorretora, 8, 0, 1, 1, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 10, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_Currency, 11, 0, 1, 1, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AdicionarCorretora, 12, 0, 2, 1, Qt.AlignHCenter)
        self.HMI.TextBox_NovaCorretora.setFocus()

    def CreatePage38(self): # Deletar corretora
        MessageBox_Msg1 = QMessageBox()
        MessageBox_Msg1.setWindowTitle("Deletar corretora (cripto)")
        MessageBox_Msg1.setText("Tem certeza que deseja deletar a "+self.HMI.ComboBox_Corretoras.currentText())
        MessageBox_Msg1.setIcon(QMessageBox.Question)
        MessageBox_Msg1.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
        MessageBox_Msg1.setDefaultButton(QMessageBox.Cancel)
        MessageBox_Msg1.setWindowIcon(QIcon(".\images\logoARCA.png"))

        returnValue = MessageBox_Msg1.exec()
        if returnValue == QMessageBox.Yes:
            self.HMI.DBManager.DeleteCorretora()
            self.HMI.CreatePage('19')

    def CreatePage39(self): # Renomear corretora de criptomoedas
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Renomear corretora de criptomoedas')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Renomear corretora \n'+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font22)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg2 = QLabel('Insira o novo nome da corretora:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_NovoNomeCorretora = QLineEdit()
        self.HMI.TextBox_NovoNomeCorretora.returnPressed.connect(lambda: self.HMI.CreatePage('19_'))
        self.HMI.TextBox_NovoNomeCorretora.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))

        self.HMI.Button_RenomearCorretora = QPushButton('Seguinte')
        self.HMI.Button_RenomearCorretora.pressed.connect(lambda: self.HMI.CreatePage('19_'))
        self.HMI.Button_RenomearCorretora.setFont(self.HMI.font16)
        self.HMI.Button_RenomearCorretora.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_RenomearCorretora.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_RenomearCorretora.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_RenomearCorretora.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_RenomearCorretora.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 19, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 7, 0, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 9, 0, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_NovoNomeCorretora, 10, 0, 1, 1, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RenomearCorretora, 12, 0, 2, 1, Qt.AlignHCenter)

    def CreatePage40(self): # Registros
        self.item = -1

        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)
        Background_3 = QLabel()
        Background_3.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Registros')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Button_AddOperacao = QPushButton('Adicionar operação')
        self.HMI.Button_AddOperacao.pressed.connect(lambda: self.HMI.CreatePage('41'))
        self.HMI.Button_AddOperacao.setFixedSize(160,40)
        self.HMI.Button_AddOperacao.setIconSize(QSize(35, 35))
        self.HMI.Button_AddOperacao.setIcon(QIcon("./images/add_user.png"))
        self.HMI.Button_AddOperacao.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AddOperacao.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)}')

        self.HMI.Button_AlterarOperacao = QPushButton('Alterar operação')
        self.HMI.Button_AlterarOperacao.pressed.connect(lambda: self.HMI.CreatePage('43'))
        self.HMI.Button_AlterarOperacao.setFixedSize(160,40)
        self.HMI.Button_AlterarOperacao.setIconSize(QSize(35, 35))
        self.HMI.Button_AlterarOperacao.setIcon(QIcon("./images/iconeAdjustDB.png"))
        self.HMI.Button_AlterarOperacao.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AlterarOperacao.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)}')

        self.HMI.Button_DeletarOperacao = QPushButton('Deletar operação')
        self.HMI.Button_DeletarOperacao.pressed.connect(lambda: self.HMI.CreatePage('44'))
        self.HMI.Button_DeletarOperacao.setFixedSize(160,40)
        self.HMI.Button_DeletarOperacao.setIconSize(QSize(35, 35))
        self.HMI.Button_DeletarOperacao.setIcon(QIcon("./images/delete_broker.png"))
        self.HMI.Button_DeletarOperacao.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_DeletarOperacao.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)}')

        self.HMI.Button_DTeST = QPushButton()
        self.HMI.Button_DTeST.setToolTip("Alterar apresentação de DT e ST")
        self.HMI.Button_DTeST.pressed.connect(lambda: self.OnButtonPressed('ChangeDTeST'))
        self.HMI.Button_DTeST.setFixedSize(70*3+5,35*3+5)
        self.HMI.Button_DTeST.setIconSize(QSize(70*3, 35*3))
        self.HMI.Button_DTeST.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_DTeST.setCursor(QCursor(Qt.PointingHandCursor))
        if self.HMI.DTeST == "NotDefined":
            self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Trades Brutos.png"))
            self.HMI.DTeST = ""
        elif self.HMI.DTeST == "": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Trades Brutos.png"))
        elif self.HMI.DTeST == "DTeST": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Day Trades e Swing Trades.png"))
        elif self.HMI.DTeST == "ST": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas ST.png"))
        elif self.HMI.DTeST == "DT": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas DT.png"))

        self.HMI.Label_Msg1 = QLabel('Operações realizadas na '+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font20)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignLeft)

        self.HMI.Table_Operacoes_RealizadasHeader = QTableWidget()
        self.HMI.Table_Operacoes_Realizadas = QTableWidget()

        self.HMI.Table_EstoqueHeader = QTableWidget()
        self.HMI.Table_Estoque = QTableWidget()

        self.CreateTable_40_1() # Table_Operacoes_RealizadasHeader
        self.CreateTable_40_2() # Table_Operacoes_Realizadas (Criada com uma thread)

        self.CreateTable_40_3()  # Table_EstoqueHeader
        self.CreateTable_40_4()  # Table_Estoque (Criada com uma thread)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 3, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_3, 4, 0, 8, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 10, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_EstoqueHeader, 1, 0, 1, 5, Qt.AlignCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Estoque, 2, 0, 2, 5, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AddOperacao, 1, 5, 1, 5, Qt.AlignCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AlterarOperacao, 2, 5, 1, 5, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DeletarOperacao, 3, 5, 1, 5, Qt.AlignCenter | Qt.AlignTop)
        # self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DTeST, 1, 8, 3, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 4, 0, 1, 10, Qt.AlignLeft | Qt.AlignVCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_RealizadasHeader, 5, 0, 1, 10, Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas, 6, 0, 6, 10, Qt.AlignTop)

    def CreatePage41(self): # Informar nova operação
        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        black = "rgb(0,0,0)"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Informar nova operação na '+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg2 = QLabel('Data:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font14)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignRight)

        self.HMI.Selecao_Ano = str(datetime.now().year)
        self.HMI.Selecao_Mes = str(datetime.now().month)
        self.HMI.Selecao_Dia = str(datetime.now().day)

        self.HMI.Button_Calendario = QPushButton(self.HMI.Selecao_Ano+"/"+self.HMI.Selecao_Mes+"/"+self.HMI.Selecao_Dia)
        self.HMI.Button_Calendario.setFont(self.HMI.font16)
        self.HMI.Button_Calendario.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.Button_Calendario.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Calendario.pressed.connect(lambda: self.HMI.OnButtonPressed("Abrir Calendário"))

        self.HMI.Selecao_Hora = str(datetime.now().hour)
        self.HMI.Selecao_Minuto = '00'
        self.HMI.Selecao_Segundo = '00'

        self.HMI.Button_Relogio = QPushButton(self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo)
        self.HMI.Button_Relogio.setFont(self.HMI.font16)
        self.HMI.Button_Relogio.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.Button_Relogio.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Relogio.pressed.connect(lambda: self.HMI.OnButtonPressed("Abrir Relógio"))

        self.HMI.Label_Msg3 = QLabel('Tipo:')
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font14)
        self.HMI.Label_Msg3.setAlignment(Qt.AlignRight)

        self.HMI.Button_Compra = QPushButton('COMPRA')
        self.HMI.Button_Compra.pressed.connect(lambda: self.OnButtonPressed('Compra_Cripto'))
        self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Compra.setFont(self.HMI.font20)
        self.HMI.Button_Compra.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.TipoDeOperacao = 'Compra'

        self.HMI.Button_Venda = QPushButton('venda')
        self.HMI.Button_Venda.pressed.connect(lambda: self.OnButtonPressed('Venda_Cripto'))
        self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Venda.setFont(self.HMI.font16)
        self.HMI.Button_Venda.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Deposito = QPushButton('depósito')
        self.HMI.Button_Deposito.pressed.connect(lambda: self.OnButtonPressed('Depósito_Cripto'))
        self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Deposito.setFont(self.HMI.font16)
        self.HMI.Button_Deposito.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Saque = QPushButton('saque')
        self.HMI.Button_Saque.pressed.connect(lambda: self.OnButtonPressed('Saque_Cripto'))
        self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Saque.setFont(self.HMI.font16)
        self.HMI.Button_Saque.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Drop = QPushButton('drop')
        self.HMI.Button_Drop.pressed.connect(lambda: self.OnButtonPressed('Drop_Cripto'))
        self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Drop.setFont(self.HMI.font16)
        self.HMI.Button_Drop.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Burn = QPushButton('burn')
        self.HMI.Button_Burn.pressed.connect(lambda: self.OnButtonPressed('Burn_Cripto'))
        self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Burn.setFont(self.HMI.font16)
        self.HMI.Button_Burn.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Stake = QPushButton('stake')
        self.HMI.Button_Stake.pressed.connect(lambda: self.OnButtonPressed('Stake_Cripto'))
        self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Stake.setFont(self.HMI.font16)
        self.HMI.Button_Stake.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Unstake = QPushButton('unstake')
        self.HMI.Button_Unstake.pressed.connect(lambda: self.OnButtonPressed('Unstake_Cripto'))
        self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Unstake.setFont(self.HMI.font16)
        self.HMI.Button_Unstake.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Hold = QPushButton('hold')
        self.HMI.Button_Hold.pressed.connect(lambda: self.OnButtonPressed('Hold_Cripto'))
        self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Hold.setFont(self.HMI.font16)
        self.HMI.Button_Hold.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Unhold = QPushButton('unhold')
        self.HMI.Button_Unhold.pressed.connect(lambda: self.OnButtonPressed('Unhold_Cripto'))
        self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Unhold.setFont(self.HMI.font16)
        self.HMI.Button_Unhold.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Label_Msg10 = QLabel('Par:')
        self.HMI.Label_Msg10.setStyleSheet('color: white')
        self.HMI.Label_Msg10.setFont(self.HMI.font14)
        self.HMI.Label_Msg10.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Par_Esquerda = QLineEdit()
        self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
        self.HMI.TextBox_Par_Esquerda.returnPressed.connect(lambda: self.HMI.CreatePage('41'))
        self.HMI.TextBox_Par_Esquerda.textChanged.connect(self.Auto_Capital_Par_Esquerda)

        self.HMI.Label_Msg12 = QLabel('/')
        self.HMI.Label_Msg12.setStyleSheet('color: white')
        self.HMI.Label_Msg12.setFont(self.HMI.font14)
        self.HMI.Label_Msg12.setFixedWidth(int(self.HMI.frameGeometry().width()/20*0.9))
        self.HMI.Label_Msg12.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_Par_Direita = QLineEdit()
        self.HMI.TextBox_Par_Direita.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Par_Direita.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Par_Direita.setFont(self.HMI.font14)
        self.HMI.TextBox_Par_Direita.returnPressed.connect(lambda: self.HMI.CreatePage('41'))
        self.HMI.TextBox_Par_Direita.textChanged.connect(self.Auto_Capital_Par_Direita)

        self.HMI.Label_Msg4 = QLabel('Quantidade:')
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font14)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Qqt = QLineEdit()
        self.HMI.TextBox_Qqt.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_Qqt.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Qqt.setFont(self.HMI.font14)
        self.HMI.TextBox_Qqt.returnPressed.connect(lambda: self.HMI.CreatePage('41'))

        self.HMI.Label_Msg5 = QLabel('Preço:')
        self.HMI.Label_Msg5.setStyleSheet('color: white')
        self.HMI.Label_Msg5.setFont(self.HMI.font14)
        self.HMI.Label_Msg5.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Preco = QLineEdit()
        self.HMI.TextBox_Preco.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_Preco.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Preco.setFont(self.HMI.font14)
        self.HMI.TextBox_Preco.returnPressed.connect(lambda: self.HMI.CreatePage('41'))

        self.HMI.Label_Msg6 = QLabel('Taxa:')
        self.HMI.Label_Msg6.setStyleSheet('color: white')
        self.HMI.Label_Msg6.setFont(self.HMI.font14)
        self.HMI.Label_Msg6.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Taxa = QLineEdit('0')
        self.HMI.TextBox_Taxa.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_Taxa.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Taxa.setFont(self.HMI.font14)
        self.HMI.TextBox_Taxa.returnPressed.connect(lambda: self.HMI.CreatePage('41'))

        self.HMI.Label_Msg7 = QLabel('Moeda da taxa:')
        self.HMI.Label_Msg7.setStyleSheet('color: white')
        self.HMI.Label_Msg7.setFont(self.HMI.font14)
        self.HMI.Label_Msg7.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_MoedaDaTaxa = QLineEdit(self.HMI.DBManager.GetUserCoinCurrency())
        self.HMI.TextBox_MoedaDaTaxa.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_MoedaDaTaxa.setFont(self.HMI.font14)
        self.HMI.TextBox_MoedaDaTaxa.returnPressed.connect(lambda: self.HMI.CreatePage('41'))
        self.HMI.TextBox_MoedaDaTaxa.textChanged.connect(self.Auto_Capital_MoedaDaTaxa)

        self.HMI.Label_Msg11 = QLabel('Conversão:')
        self.HMI.Label_Msg11.setStyleSheet('color: white')
        self.HMI.Label_Msg11.setFont(self.HMI.font14)
        self.HMI.Label_Msg11.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Conversao = QLineEdit('1')
        self.HMI.TextBox_Conversao.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_Conversao.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Conversao.setFont(self.HMI.font14)
        self.HMI.TextBox_Conversao.returnPressed.connect(lambda: self.HMI.CreatePage('41'))

        self.HMI.Button_BuscarConversao = QPushButton('Buscar')
        self.HMI.Button_BuscarConversao.pressed.connect(lambda: self.OnButtonPressed('BuscarConversaoAutomaticamente'))
        self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_BuscarConversao.setFont(self.HMI.font16)
        self.HMI.Button_BuscarConversao.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_BuscarConversao.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))

        self.HMI.Label_Msg8 = QLabel('Observação:')
        self.HMI.Label_Msg8.setStyleSheet('color: white')
        self.HMI.Label_Msg8.setFont(self.HMI.font14)
        self.HMI.Label_Msg8.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Obs = QLineEdit()
        self.HMI.TextBox_Obs.setFixedWidth(int(self.HMI.frameGeometry().width()*4/7*0.9))
        self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Obs.setFont(self.HMI.font14)
        self.HMI.TextBox_Obs.returnPressed.connect(lambda: self.HMI.CreatePage('41'))

        self.HMI.Button_LimparCampos = QPushButton('Limpar\ncampos')
        self.HMI.Button_LimparCampos.pressed.connect(lambda: self.HMI.LimparPage())
        self.HMI.Button_LimparCampos.setFont(self.HMI.font16)
        self.HMI.Button_LimparCampos.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_LimparCampos.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_LimparCampos.setStyleSheet("background-color: rgb(100, 100, 100)")

        self.HMI.Button_RegistrarOperacao = QPushButton('Registrar\noperação')
        self.HMI.Button_RegistrarOperacao.pressed.connect(lambda: self.HMI.CreatePage('41'))
        self.HMI.Button_RegistrarOperacao.setFont(self.HMI.font16)
        self.HMI.Button_RegistrarOperacao.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_RegistrarOperacao.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_RegistrarOperacao.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_RegistrarOperacao.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_RegistrarOperacao.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Button_Info3 = QPushButton()
        self.HMI.Button_Info3.pressed.connect(lambda: self.HMI.CreatePage('Info3'))
        self.HMI.Button_Info3.setFixedSize(40,40)
        self.HMI.Button_Info3.setIconSize(QSize(35, 35))
        self.HMI.Button_Info3.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info3.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info3.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info14 = QPushButton()
        self.HMI.Button_Info14.pressed.connect(lambda: self.HMI.CreatePage('Info14'))
        self.HMI.Button_Info14.setFixedSize(40,40)
        self.HMI.Button_Info14.setIconSize(QSize(35, 35))
        self.HMI.Button_Info14.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info14.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info14.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info15 = QPushButton()
        self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
        self.HMI.Button_Info15.setFixedSize(40,40)
        self.HMI.Button_Info15.setIconSize(QSize(35, 35))
        self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info12 = QPushButton()
        self.HMI.Button_Info12.pressed.connect(lambda: self.HMI.CreatePage('Info12'))
        self.HMI.Button_Info12.setFixedSize(40,40)
        self.HMI.Button_Info12.setIconSize(QSize(35, 35))
        self.HMI.Button_Info12.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info12.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info12.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info13 = QPushButton()
        self.HMI.Button_Info13.pressed.connect(lambda: self.HMI.CreatePage('Info13'))
        self.HMI.Button_Info13.setFixedSize(40,40)
        self.HMI.Button_Info13.setIconSize(QSize(35, 35))
        self.HMI.Button_Info13.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info13.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info13.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info11 = QPushButton()
        self.HMI.Button_Info11.pressed.connect(lambda: self.HMI.CreatePage('Info11'))
        self.HMI.Button_Info11.setFixedSize(40,40)
        self.HMI.Button_Info11.setIconSize(QSize(35, 35))
        self.HMI.Button_Info11.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info11.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info11.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info10 = QPushButton()
        self.HMI.Button_Info10.pressed.connect(lambda: self.HMI.CreatePage('Info10'))
        self.HMI.Button_Info10.setFixedSize(40,40)
        self.HMI.Button_Info10.setIconSize(QSize(35, 35))
        self.HMI.Button_Info10.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info10.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info10.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info9 = QPushButton()
        self.HMI.Button_Info9.pressed.connect(lambda: self.HMI.CreatePage('Info9'))
        self.HMI.Button_Info9.setFixedSize(40,40)
        self.HMI.Button_Info9.setIconSize(QSize(35, 35))
        self.HMI.Button_Info9.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info9.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info9.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info8 = QPushButton()
        self.HMI.Button_Info8.pressed.connect(lambda: self.HMI.CreatePage('Info8'))
        self.HMI.Button_Info8.setFixedSize(40,40)
        self.HMI.Button_Info8.setIconSize(QSize(35, 35))
        self.HMI.Button_Info8.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info8.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info8.setIcon(QIcon("./images/Info.png"))

        self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
        self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
        self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
        self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
        self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)

        self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
        self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
        self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)

        self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
        self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
        self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
        self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
        self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
        self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
        self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
        self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)
        self.HMI.setTabOrder(self.HMI.Button_Info8,self.HMI.TextBox_Par_Esquerda)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 8)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 9, 8)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 8, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 1, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Data
        self.HMI.HBoxLayout_Data = QHBoxLayout()
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Calendario, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Relogio, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Info3, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Data, 1, 1, 1, 7, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 2, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Tipo
        self.HMI.HBoxLayout_Tipo = QHBoxLayout()
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Compra, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Venda, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Deposito, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Saque, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Drop, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Burn, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Stake, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Unstake, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Hold, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Unhold, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Info14, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Tipo, 2, 1, 1, 7, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg10, 3, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Par
        self.HMI.HBoxLayout_Par = QHBoxLayout()
        self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
        self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
        self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)

        if self.HMI.TipoDeOperacao in ['Compra', 'Venda']:
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Label_Msg12, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Direita, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Par_Direita)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Direita,self.HMI.TextBox_Qqt)

        self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 4, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Qqt
        self.HMI.HBoxLayout_Qqt = QHBoxLayout()
        self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.TextBox_Qqt)
        self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.Button_Info13)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Qqt, 4, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 5, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Preço
        self.HMI.HBoxLayout_Preco = QHBoxLayout()
        self.HMI.HBoxLayout_Preco.addWidget(self.HMI.TextBox_Preco)
        self.HMI.HBoxLayout_Preco.addWidget(self.HMI.Button_Info12)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Preco, 5, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg6, 6, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Taxa
        self.HMI.HBoxLayout_Taxa = QHBoxLayout()
        self.HMI.HBoxLayout_Taxa.addWidget(self.HMI.TextBox_Taxa)
        self.HMI.HBoxLayout_Taxa.addWidget(self.HMI.Button_Info11)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Taxa, 6, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg7, 7, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Moeda da taxa
        self.HMI.HBoxLayout_MoedaDaTaxa = QHBoxLayout()
        self.HMI.HBoxLayout_MoedaDaTaxa.addWidget(self.HMI.TextBox_MoedaDaTaxa)
        self.HMI.HBoxLayout_MoedaDaTaxa.addWidget(self.HMI.Button_Info10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_MoedaDaTaxa, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg11, 8, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Conversão
        self.HMI.HBoxLayout_Conversao = QHBoxLayout()
        self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.TextBox_Conversao)
        self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.Button_BuscarConversao)
        self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.Button_Info9)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Conversao, 8, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg8, 9, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Observação
        self.HMI.HBoxLayout_Obs = QHBoxLayout()
        self.HMI.HBoxLayout_Obs.addWidget(self.HMI.TextBox_Obs)
        self.HMI.HBoxLayout_Obs.addWidget(self.HMI.Button_Info8)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Obs, 9, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_LimparCampos, 3, 6, 3, 2, Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RegistrarOperacao, 7, 6, 3, 2, Qt.AlignTop)

        self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
        self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
        self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
        self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
        self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
        self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
        self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
        self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
        self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
        self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
        self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
        self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
        self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
        self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
        self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
        self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

        self.HMI.TextBox_Par_Esquerda.setFocus()

    def CreatePage43(self): # Alterar operações
        self.item += 1

        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        black = "rgb(0,0,0)"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Alterar operações na '+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.Operacoes=[]
        for idx in self.HMI.Table_Operacoes_Realizadas.selectedIndexes():
            self.Operacoes.append(idx.row())
        self.Operacoes = list(dict.fromkeys(self.Operacoes))

        if len(self.Operacoes) > 0:

            self.HMI.Label_Msg1 = QLabel('Alteração na operação '+str(self.item+1)+' de '+str(len(self.Operacoes)))
            self.HMI.Label_Msg1.setStyleSheet('color: white')
            self.HMI.Label_Msg1.setFont(self.HMI.font24)
            self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

            self.HMI.Table_Operacoes_SelecionadasHeader = QTableWidget()
            self.HMI.Table_Operacoes_Selecionadas = QTableWidget()

            self.CreateTable_43_1() # Table_Operacoes_SelecionadasHeader
            self.CreateTable_43_2() # Table_Operacoes_Selecionadas (Mostra apenas o item selecionado)

            self.HMI.Label_Msg2 = QLabel('Data:')
            self.HMI.Label_Msg2.setStyleSheet('color: white')
            self.HMI.Label_Msg2.setFont(self.HMI.font14)
            self.HMI.Label_Msg2.setAlignment(Qt.AlignRight)

            self.HMI.Selecao_Ano = str('%02d' % (datetime.now().year,))
            self.HMI.Selecao_Mes = str('%02d' % (datetime.now().month,))
            self.HMI.Selecao_Dia = str('%02d' % (datetime.now().day,))

            self.HMI.Button_Calendario = QPushButton(self.HMI.Selecao_Ano+"/"+self.HMI.Selecao_Mes+"/"+self.HMI.Selecao_Dia)
            self.HMI.Button_Calendario.setFont(self.HMI.font16)
            self.HMI.Button_Calendario.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.Button_Calendario.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.pressed.connect(lambda: self.HMI.OnButtonPressed("Abrir Calendário"))

            self.HMI.Selecao_Hora = str('%02d' % (datetime.now().hour,))
            self.HMI.Selecao_Minuto = str('%02d' % (0,))
            self.HMI.Selecao_Segundo = str('%02d' % (0,))

            self.HMI.Button_Relogio = QPushButton(self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo)
            self.HMI.Button_Relogio.setFont(self.HMI.font16)
            self.HMI.Button_Relogio.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.Button_Relogio.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.pressed.connect(lambda: self.HMI.OnButtonPressed("Abrir Relógio"))

            self.HMI.Label_Msg3 = QLabel('Tipo:')
            self.HMI.Label_Msg3.setStyleSheet('color: white')
            self.HMI.Label_Msg3.setFont(self.HMI.font14)
            self.HMI.Label_Msg3.setAlignment(Qt.AlignRight)

            self.HMI.Button_Compra = QPushButton('COMPRA')
            self.HMI.Button_Compra.pressed.connect(lambda: self.OnButtonPressed('Compra_Cripto'))
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setFont(self.HMI.font20)
            self.HMI.Button_Compra.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.TipoDeOperacao = 'Compra'

            self.HMI.Button_Venda = QPushButton('venda')
            self.HMI.Button_Venda.pressed.connect(lambda: self.OnButtonPressed('Venda_Cripto'))
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Button_Deposito = QPushButton('depósito')
            self.HMI.Button_Deposito.pressed.connect(lambda: self.OnButtonPressed('Depósito_Cripto'))
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Deposito.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Button_Saque = QPushButton('saque')
            self.HMI.Button_Saque.pressed.connect(lambda: self.OnButtonPressed('Saque_Cripto'))
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Button_Drop = QPushButton('drop')
            self.HMI.Button_Drop.pressed.connect(lambda: self.OnButtonPressed('Drop_Cripto'))
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setFont(self.HMI.font16)
            self.HMI.Button_Drop.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Button_Burn = QPushButton('burn')
            self.HMI.Button_Burn.pressed.connect(lambda: self.OnButtonPressed('Burn_Cripto'))
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setFont(self.HMI.font16)
            self.HMI.Button_Burn.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Button_Stake = QPushButton('stake')
            self.HMI.Button_Stake.pressed.connect(lambda: self.OnButtonPressed('Stake_Cripto'))
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setFont(self.HMI.font16)
            self.HMI.Button_Stake.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Button_Unstake = QPushButton('unstake')
            self.HMI.Button_Unstake.pressed.connect(lambda: self.OnButtonPressed('Unstake_Cripto'))
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setFont(self.HMI.font16)
            self.HMI.Button_Unstake.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Button_Hold = QPushButton('hold')
            self.HMI.Button_Hold.pressed.connect(lambda: self.OnButtonPressed('Hold_Cripto'))
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setFont(self.HMI.font16)
            self.HMI.Button_Hold.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Button_Unhold = QPushButton('unhold')
            self.HMI.Button_Unhold.pressed.connect(lambda: self.OnButtonPressed('Unhold_Cripto'))
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setFont(self.HMI.font16)
            self.HMI.Button_Unhold.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Label_Msg10 = QLabel('Par:')
            self.HMI.Label_Msg10.setStyleSheet('color: white')
            self.HMI.Label_Msg10.setFont(self.HMI.font14)
            self.HMI.Label_Msg10.setAlignment(Qt.AlignRight)

            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.TextBox_Par_Esquerda.textChanged.connect(self.Auto_Capital_Par_Esquerda)

            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.Label_Msg12.setStyleSheet('color: white')
            self.HMI.Label_Msg12.setFont(self.HMI.font14)
            self.HMI.Label_Msg12.setFixedWidth(int(self.HMI.frameGeometry().width()/20*0.9))
            self.HMI.Label_Msg12.setAlignment(Qt.AlignCenter)

            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.TextBox_Par_Direita.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Direita.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Direita.setFont(self.HMI.font14)
            self.HMI.TextBox_Par_Direita.textChanged.connect(self.Auto_Capital_Par_Direita)

            self.HMI.Label_Msg4 = QLabel('Quantidade:')
            self.HMI.Label_Msg4.setStyleSheet('color: white')
            self.HMI.Label_Msg4.setFont(self.HMI.font14)
            self.HMI.Label_Msg4.setAlignment(Qt.AlignRight)

            self.HMI.TextBox_Qqt = QLineEdit()
            self.HMI.TextBox_Qqt.setValidator(QDoubleValidator(0.99,99.99,2))
            self.HMI.TextBox_Qqt.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setFont(self.HMI.font14)

            self.HMI.Label_Msg5 = QLabel('Preço:')
            self.HMI.Label_Msg5.setStyleSheet('color: white')
            self.HMI.Label_Msg5.setFont(self.HMI.font14)
            self.HMI.Label_Msg5.setAlignment(Qt.AlignRight)

            self.HMI.TextBox_Preco = QLineEdit()
            self.HMI.TextBox_Preco.setValidator(QDoubleValidator(0.99,99.99,2))
            self.HMI.TextBox_Preco.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setFont(self.HMI.font14)

            self.HMI.Label_Msg6 = QLabel('Taxa:')
            self.HMI.Label_Msg6.setStyleSheet('color: white')
            self.HMI.Label_Msg6.setFont(self.HMI.font14)
            self.HMI.Label_Msg6.setAlignment(Qt.AlignRight)

            self.HMI.TextBox_Taxa = QLineEdit()
            self.HMI.TextBox_Taxa.setValidator(QDoubleValidator(0.99,99.99,2))
            self.HMI.TextBox_Taxa.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setFont(self.HMI.font14)

            self.HMI.Label_Msg7 = QLabel('Moeda da taxa:')
            self.HMI.Label_Msg7.setStyleSheet('color: white')
            self.HMI.Label_Msg7.setFont(self.HMI.font14)
            self.HMI.Label_Msg7.setAlignment(Qt.AlignRight)

            self.HMI.TextBox_MoedaDaTaxa = QLineEdit()
            self.HMI.TextBox_MoedaDaTaxa.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setFont(self.HMI.font14)
            self.HMI.TextBox_MoedaDaTaxa.textChanged.connect(self.Auto_Capital_MoedaDaTaxa)

            self.HMI.Label_Msg11 = QLabel('Conversão:')
            self.HMI.Label_Msg11.setStyleSheet('color: white')
            self.HMI.Label_Msg11.setFont(self.HMI.font14)
            self.HMI.Label_Msg11.setAlignment(Qt.AlignRight)

            self.HMI.TextBox_Conversao = QLineEdit()
            self.HMI.TextBox_Conversao.setValidator(QDoubleValidator(0.99,99.99,2))
            self.HMI.TextBox_Conversao.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setFont(self.HMI.font14)

            self.HMI.Button_BuscarConversao = QPushButton('Buscar')
            self.HMI.Button_BuscarConversao.pressed.connect(lambda: self.OnButtonPressed('BuscarConversaoAutomaticamente'))
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_BuscarConversao.setFont(self.HMI.font16)
            self.HMI.Button_BuscarConversao.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_BuscarConversao.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))

            self.HMI.Label_Msg8 = QLabel('Observação:')
            self.HMI.Label_Msg8.setStyleSheet('color: white')
            self.HMI.Label_Msg8.setFont(self.HMI.font14)
            self.HMI.Label_Msg8.setAlignment(Qt.AlignRight)

            self.HMI.TextBox_Obs = QLineEdit()
            self.HMI.TextBox_Obs.setFixedWidth(int(self.HMI.frameGeometry().width()*4/7*0.9))
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setFont(self.HMI.font14)

            self.HMI.Button_LimparCampos = QPushButton('Limpar\ncampos')
            self.HMI.Button_LimparCampos.pressed.connect(lambda: self.HMI.LimparPage())
            self.HMI.Button_LimparCampos.setFont(self.HMI.font16)
            self.HMI.Button_LimparCampos.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
            self.HMI.Button_LimparCampos.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_LimparCampos.setStyleSheet("background-color: rgb(100, 100, 100)")

            self.HMI.Button_RegistrarOperacao = QPushButton('Registrar\noperação')
            self.HMI.Button_RegistrarOperacao.pressed.connect(lambda: self.OnButtonPressed('Page43_Next'))
            self.HMI.Button_RegistrarOperacao.setFont(self.HMI.font16)
            self.HMI.Button_RegistrarOperacao.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
            self.HMI.Button_RegistrarOperacao.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
            self.HMI.Button_RegistrarOperacao.setIcon(QIcon("./images/log_in.png"))
            self.HMI.Button_RegistrarOperacao.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_RegistrarOperacao.setStyleSheet("background-color: rgb(20, 120, 30)")

            self.HMI.Button_Info3 = QPushButton()
            self.HMI.Button_Info3.pressed.connect(lambda: self.HMI.CreatePage('Info3'))
            self.HMI.Button_Info3.setFixedSize(40,40)
            self.HMI.Button_Info3.setIconSize(QSize(35, 35))
            self.HMI.Button_Info3.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info3.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info3.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info14 = QPushButton()
            self.HMI.Button_Info14.pressed.connect(lambda: self.HMI.CreatePage('Info14'))
            self.HMI.Button_Info14.setFixedSize(40,40)
            self.HMI.Button_Info14.setIconSize(QSize(35, 35))
            self.HMI.Button_Info14.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info14.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info14.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info12 = QPushButton()
            self.HMI.Button_Info12.pressed.connect(lambda: self.HMI.CreatePage('Info12'))
            self.HMI.Button_Info12.setFixedSize(40,40)
            self.HMI.Button_Info12.setIconSize(QSize(35, 35))
            self.HMI.Button_Info12.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info12.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info12.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info13 = QPushButton()
            self.HMI.Button_Info13.pressed.connect(lambda: self.HMI.CreatePage('Info13'))
            self.HMI.Button_Info13.setFixedSize(40,40)
            self.HMI.Button_Info13.setIconSize(QSize(35, 35))
            self.HMI.Button_Info13.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info13.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info13.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info11 = QPushButton()
            self.HMI.Button_Info11.pressed.connect(lambda: self.HMI.CreatePage('Info11'))
            self.HMI.Button_Info11.setFixedSize(40,40)
            self.HMI.Button_Info11.setIconSize(QSize(35, 35))
            self.HMI.Button_Info11.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info11.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info11.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info10 = QPushButton()
            self.HMI.Button_Info10.pressed.connect(lambda: self.HMI.CreatePage('Info10'))
            self.HMI.Button_Info10.setFixedSize(40,40)
            self.HMI.Button_Info10.setIconSize(QSize(35, 35))
            self.HMI.Button_Info10.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info10.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info10.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info9 = QPushButton()
            self.HMI.Button_Info9.pressed.connect(lambda: self.HMI.CreatePage('Info9'))
            self.HMI.Button_Info9.setFixedSize(40,40)
            self.HMI.Button_Info9.setIconSize(QSize(35, 35))
            self.HMI.Button_Info9.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info9.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info9.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info8 = QPushButton()
            self.HMI.Button_Info8.pressed.connect(lambda: self.HMI.CreatePage('Info8'))
            self.HMI.Button_Info8.setFixedSize(40,40)
            self.HMI.Button_Info8.setIconSize(QSize(35, 35))
            self.HMI.Button_Info8.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info8.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info8.setIcon(QIcon("./images/Info.png"))

            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 9)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 13, 9)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 9, Qt.AlignCenter)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 1, 9, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_SelecionadasHeader, 2, 0, 1, 9, Qt.AlignHCenter | Qt.AlignBottom)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Selecionadas, 3, 0, 1, 9, Qt.AlignHCenter | Qt.AlignTop)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 5, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Data

            self.HMI.HBoxLayout_Data = QHBoxLayout()
            self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Calendario, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Relogio, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Info3, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Data, 5, 1, 1, 8, Qt.AlignVCenter | Qt.AlignLeft)

            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 6, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Tipo
            self.HMI.HBoxLayout_Tipo = QHBoxLayout()
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Compra, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Venda, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Deposito, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Saque, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Drop, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Burn, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Stake, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Unstake, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Hold, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Unhold, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Info14, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Tipo, 6, 1, 1, 8, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg10, 7, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Par
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignLeft)
            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)

            if self.HMI.TipoDeOperacao in ['Compra', 'Venda']:
                self.HMI.HBoxLayout_Par.addWidget(self.HMI.Label_Msg12, Qt.AlignLeft)
                self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Direita, Qt.AlignLeft)
                self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Par_Direita)
                self.HMI.setTabOrder(self.HMI.TextBox_Par_Direita,self.HMI.TextBox_Qqt)

            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 8, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Qqt
            self.HMI.HBoxLayout_Qqt = QHBoxLayout()
            self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.TextBox_Qqt)
            self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.Button_Info13)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Qqt, 8, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 9, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Preço
            self.HMI.HBoxLayout_Preco = QHBoxLayout()
            self.HMI.HBoxLayout_Preco.addWidget(self.HMI.TextBox_Preco)
            self.HMI.HBoxLayout_Preco.addWidget(self.HMI.Button_Info12)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Preco, 9, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg6, 10, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Taxa
            self.HMI.HBoxLayout_Taxa = QHBoxLayout()
            self.HMI.HBoxLayout_Taxa.addWidget(self.HMI.TextBox_Taxa)
            self.HMI.HBoxLayout_Taxa.addWidget(self.HMI.Button_Info11)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Taxa, 10, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg7, 11, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Moeda da taxa
            self.HMI.HBoxLayout_MoedaDaTaxa = QHBoxLayout()
            self.HMI.HBoxLayout_MoedaDaTaxa.addWidget(self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.HBoxLayout_MoedaDaTaxa.addWidget(self.HMI.Button_Info10)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_MoedaDaTaxa, 11, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg11, 12, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Conversão
            self.HMI.HBoxLayout_Conversao = QHBoxLayout()
            self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.TextBox_Conversao)
            self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.Button_BuscarConversao)
            self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.Button_Info9)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Conversao, 12, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg8, 13, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Observação
            self.HMI.HBoxLayout_Obs = QHBoxLayout()
            self.HMI.HBoxLayout_Obs.addWidget(self.HMI.TextBox_Obs)
            self.HMI.HBoxLayout_Obs.addWidget(self.HMI.Button_Info8)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Obs, 13, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_LimparCampos, 7, 7, 3, 2, Qt.AlignBottom)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RegistrarOperacao, 11, 7, 3, 2, Qt.AlignTop)
            self.HMI.TextBox_Par_Esquerda.setFocus()

            # Completar os textBoxes
            for i, item in enumerate(self.data_40_1):
                if i == self.Operacoes[self.item]:
                    data = str(item[0])
                    data = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
                    ano = str('%02d' % (data.year,))
                    mes = str('%02d' % (data.month,))
                    dia = str('%02d' % (data.day,))
                    hora = str('%02d' % (data.hour,))
                    minuto = str('%02d' % (data.minute,))
                    segundo = str('%02d' % (data.second,))
                    Tipo = str(item[2])
                    if "/" in item[1]:
                        ParEsquerdo = item[1][:item[1].index("/",0)]
                        ParDireito = item[1][item[1].index("/",0)+1:]
                    else:
                        ParEsquerdo = item[1]
                        ParDireito = ''
                    Preco = str('%.8f' % item[3])
                    Qqt = str('%.8f' % item[4])
                    Taxa = str('%.8f' % item[5])
                    MoedaDaTaxa= str(item[6])
                    Conversao = str('%.8f' % item[7])
                    Obs = str(item[8])
            self.HMI.TextBox_Obs.setText(Obs)
            self.HMI.Button_Calendario.setText(ano+"/"+mes+"/"+dia)
            self.HMI.Button_Relogio.setText(hora+":"+minuto+":"+segundo)
            self.HMI.Selecao_Ano = ano
            self.HMI.Selecao_Mes = mes
            self.HMI.Selecao_Dia = dia
            self.HMI.Selecao_Hora = hora
            self.HMI.Selecao_Minuto = minuto
            self.HMI.Selecao_Segundo = segundo
            if Tipo == "Compra": self.OnButtonPressed('Compra_Cripto')
            elif Tipo == "Venda": self.OnButtonPressed('Venda_Cripto')
            elif Tipo == "Depósito": self.OnButtonPressed('Depósito_Cripto')
            elif Tipo == "Saque": self.OnButtonPressed('Saque_Cripto')
            elif Tipo == "Drop": self.OnButtonPressed('Drop_Cripto')
            elif Tipo == "Burn": self.OnButtonPressed('Burn_Cripto')
            elif Tipo == "Stake": self.OnButtonPressed('Stake_Cripto')
            elif Tipo == "Unstake": self.OnButtonPressed('Unstake_Cripto')
            elif Tipo == "Hold": self.OnButtonPressed('Hold_Cripto')
            elif Tipo == "Unhold": self.OnButtonPressed('Unhold_Cripto')
            self.HMI.TextBox_Par_Esquerda.setText(ParEsquerdo)
            self.HMI.TextBox_Par_Direita.setText(ParDireito)
            self.HMI.TextBox_Preco.setText(Preco)
            self.HMI.TextBox_Qqt.setText(Qqt)
            self.HMI.TextBox_Taxa.setText(Taxa)
            self.HMI.TextBox_MoedaDaTaxa.setText(MoedaDaTaxa)
            self.HMI.TextBox_Conversao.setText(Conversao)

            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Qqt.setFocus()

        else:
            self.HMI.Label_Msg1 = QLabel('Nenhuma operação foi selecionada na página anterior.')
            self.HMI.Label_Msg1.setStyleSheet('color: white')
            self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 10)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 11, 10)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 10, Qt.AlignCenter)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 1, 10, Qt.AlignCenter)
            self.HMI.unsetCursor()

    def CreatePage44(self): # Deletar operações
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Deletar operações na '+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Operações selecionadas para serem deletadas:')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font24)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.Operacoes = [] # Será usada para fazer a tabela dessa pagina, com apenas os itens selecionados
        for idx in self.HMI.Table_Operacoes_Realizadas.selectedIndexes():
            self.Operacoes.append(idx.row())
        self.Operacoes = list(dict.fromkeys(self.Operacoes))

        self.HMI.Button_Cancelar = QPushButton('Cancelar')
        self.HMI.Button_Cancelar.pressed.connect(lambda: self.HMI.CreatePage('40'))
        self.HMI.Button_Cancelar.setFont(self.HMI.font16)
        self.HMI.Button_Cancelar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Cancelar.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_Cancelar.setIcon(QIcon("./images/Voltar.png"))
        self.HMI.Button_Cancelar.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Cancelar.setStyleSheet("background-color: rgb(200, 100, 100)")

        self.HMI.Button_DeletarOperacoes = QPushButton('Deletar\noperações')
        self.HMI.Button_DeletarOperacoes.pressed.connect(lambda: self.OnButtonPressed('Deletar Ativos da Pagina 44'))
        self.HMI.Button_DeletarOperacoes.setFont(self.HMI.font16)
        self.HMI.Button_DeletarOperacoes.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_DeletarOperacoes.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_DeletarOperacoes.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_DeletarOperacoes.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_DeletarOperacoes.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Table_Operacoes_SelecionadasHeader = QTableWidget()
        self.HMI.Table_Operacoes_Selecionadas = QTableWidget()

        self.CreateTable_44_1() # Table_Operacoes_SelecionadasHeader
        self.CreateTable_44_2() # Table_Operacoes_Selecionadas (Mostra apenas os itens selecionados)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 13, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 10, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 2, 0, 1, 10, Qt.AlignLeft | Qt.AlignVCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_SelecionadasHeader, 3, 0, 1, 10, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Selecionadas, 4, 0, 6, 10, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Cancelar, 12, 0, 1, 6, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DeletarOperacoes, 12, 5, 1, 6, Qt.AlignCenter)

    def CreateTable_40_1(self):
        HHeader = ['Data',
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        fakedata = [('','','','','','','','','')]

        self.HMI.Table_Operacoes_RealizadasHeader.setRowCount(1)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnCount(len(HHeader))

        self.HMI.Table_Operacoes_RealizadasHeader.setShowGrid(False)
        self.HMI.Table_Operacoes_RealizadasHeader.setFont(self.HMI.font14)
        self.HMI.Table_Operacoes_RealizadasHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_Operacoes_RealizadasHeader.verticalHeader().hide()
        self.HMI.Table_Operacoes_RealizadasHeader.horizontalHeader().hide()

        for col in range(len(HHeader)):
            it = QTableWidgetItem(str(HHeader[col]))
            it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
            it.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
            self.HMI.Table_Operacoes_RealizadasHeader.setItem(0, col, it)

        self.HMI.Table_Operacoes_RealizadasHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_RealizadasHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.HMI.Table_Operacoes_RealizadasHeader.resizeColumnsToContents()

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
        self.HMI.Table_Operacoes_RealizadasHeader.adjustSize()
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(7, SizeCol7)

    def CreateTable_40_2(self):
        self.HMI.Table_Operacoes_Realizadas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_Realizadas.setFixedHeight(int(self.HMI.frameGeometry().height()*6/20*1.4))

        self.HMI.Table_Operacoes_Realizadas.setShowGrid(False)
        self.HMI.Table_Operacoes_Realizadas.setFont(self.HMI.font12)
        self.HMI.Table_Operacoes_Realizadas.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                            color: white;
                                                                            border: 1px solid rgba(0, 0, 0, 0);}
                                                              QTableView {border-bottom: 2px dashed white;
                                                                          border-right: 1px solid white;
                                                                          border-left: 1px solid white;}
                                                              QTableView::item {border-bottom: 1px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
        self.HMI.Table_Operacoes_Realizadas.verticalHeader().hide()
        self.HMI.Table_Operacoes_Realizadas.horizontalHeader().hide()
        self.HMI.Table_Operacoes_Realizadas.setSelectionBehavior(QAbstractItemView.SelectRows)

        HHeader = ['Data',
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        self.data_40_1 = self.HMI.DBManager.GetAllOperacoes(self.HMI.DTeST)
        self.data_40_1 = self.data_40_1[::-1]
        self.HMI.Table_Operacoes_Realizadas.setRowCount(len(self.data_40_1))
        self.HMI.Table_Operacoes_Realizadas.setColumnCount(len(HHeader))
        for i, item in enumerate(self.data_40_1):
            for j in range(len(item)):
                if isinstance(item[j], float):
                    if self.HMI.ShowValues:
                        text = str('%.8f' % item[j])
                    else:
                        text = "***"
                else:
                    text = str(item[j])

                it = self.HMI.Table_Operacoes_Realizadas.item(i, j)
                it = QTableWidgetItem(text)
                it.setFlags(it.flags() & ~Qt.ItemIsEditable) # selecionar a linha inteira
                if not self.HMI.DTeST == "": it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
                it.setTextAlignment(Qt.AlignCenter)
                if "VAZIO" in item: it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
                if text in ["Compra", "Drop", "Depósito"]: it.setForeground(QBrush(QColor('green')))
                elif text in ["Venda", "Burn", "Saque"]: it.setForeground(QBrush(QColor('red')))
                if j == 8:
                    it.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.HMI.Table_Operacoes_Realizadas.setItem(i, j, it)

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(self.data_40_1, HHeader)

        self.HMI.Table_Operacoes_RealizadasHeader.adjustSize()
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(7, SizeCol7)

        self.HMI.Table_Operacoes_Realizadas.adjustSize()
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(7, SizeCol7)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(8, SizeCol8)

    def CreateTable_40_3(self):
        HHeader = ['Moeda',
                   'Estoque']
        fakedata = [('','')]

        self.HMI.Table_EstoqueHeader.setRowCount(1)
        self.HMI.Table_EstoqueHeader.setColumnCount(len(HHeader))

        self.HMI.Table_EstoqueHeader.setShowGrid(False)
        self.HMI.Table_EstoqueHeader.setFont(self.HMI.font14)
        self.HMI.Table_EstoqueHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_EstoqueHeader.verticalHeader().hide()
        self.HMI.Table_EstoqueHeader.horizontalHeader().hide()

        for col in range(len(HHeader)):
            it = QTableWidgetItem(str(HHeader[col]))
            it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
            it.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
            self.HMI.Table_EstoqueHeader.setItem(0, col, it)

        self.HMI.Table_EstoqueHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_EstoqueHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/28))
        self.HMI.Table_EstoqueHeader.setFixedWidth(int(self.HMI.frameGeometry().width() * 5 / 40 * 1.1))
        self.HMI.Table_EstoqueHeader.resizeColumnsToContents()

        SizeCol0, SizeCol1 = 100, 100
        self.HMI.Table_EstoqueHeader.adjustSize()
        self.HMI.Table_EstoqueHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_EstoqueHeader.setColumnWidth(1, SizeCol1)

    def CreateTable_40_4(self):
        self.HMI.Table_Estoque.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Estoque.setFixedHeight(int(self.HMI.frameGeometry().height()*2/20))
        self.HMI.Table_Estoque.setFixedWidth(int(self.HMI.frameGeometry().width() * 5 / 40*1.1))

        self.HMI.Table_Estoque.setShowGrid(False)
        self.HMI.Table_Estoque.setFont(self.HMI.font12)
        self.HMI.Table_Estoque.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                            color: white;
                                                                            border: 1px solid rgba(0, 0, 0, 0);}
                                                              QTableView {border-bottom: 2px dashed white;
                                                                          border-right: 1px solid white;
                                                                          border-left: 1px solid white;}
                                                              QTableView::item {border-bottom: 1px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
        self.HMI.Table_Estoque.verticalHeader().hide()
        self.HMI.Table_Estoque.horizontalHeader().hide()
        self.HMI.Table_Estoque.setSelectionBehavior(QAbstractItemView.SelectRows)

        HHeader = ['Moeda',
                   'Estoque']
        self.data_40_3 = self.HMI.DBManager.GetAllAtivosPorCorretora_Cripto(self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Table_Estoque.setRowCount(len(self.data_40_3))
        self.HMI.Table_Estoque.setColumnCount(len(HHeader))
        for i, item in enumerate(self.data_40_3):
            for j in range(len(item)):
                if isinstance(item[j], float):
                    if self.HMI.ShowValues:
                        text = str('%.8f' % item[j])
                    else:
                        text = "***"
                else:
                    text = str(item[j])

                it = self.HMI.Table_Estoque.item(i, j)
                it = QTableWidgetItem(text)
                it.setTextAlignment(Qt.AlignCenter)
                it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
                self.HMI.Table_Estoque.setItem(i, j, it)

        SizeCol0, SizeCol1 = int(self.HMI.frameGeometry().width() * 2 / 40), int(self.HMI.frameGeometry().width() * 3 / 40)

        self.HMI.Table_EstoqueHeader.adjustSize()
        self.HMI.Table_EstoqueHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_EstoqueHeader.setColumnWidth(1, SizeCol1)

        self.HMI.Table_Estoque.adjustSize()
        self.HMI.Table_Estoque.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Estoque.setColumnWidth(1, SizeCol1)

    def CreateTable_43_1(self):
        HHeader = ['Data',
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        fakedata = [('','','','','','','','','')]

        self.HMI.Table_Operacoes_SelecionadasHeader.setRowCount(1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnCount(len(HHeader))

        self.HMI.Table_Operacoes_SelecionadasHeader.setShowGrid(False)
        self.HMI.Table_Operacoes_SelecionadasHeader.setFont(self.HMI.font14)
        self.HMI.Table_Operacoes_SelecionadasHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_Operacoes_SelecionadasHeader.verticalHeader().hide()
        self.HMI.Table_Operacoes_SelecionadasHeader.horizontalHeader().hide()

        for col in range(len(HHeader)):
            it = QTableWidgetItem(str(HHeader[col]))
            it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
            it.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
            self.HMI.Table_Operacoes_SelecionadasHeader.setItem(0, col, it)

        self.HMI.Table_Operacoes_SelecionadasHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_SelecionadasHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.HMI.Table_Operacoes_SelecionadasHeader.resizeColumnsToContents()

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
        self.HMI.Table_Operacoes_SelecionadasHeader.adjustSize()
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(7, SizeCol7)

    def CreateTable_43_2(self):
        self.HMI.Table_Operacoes_Selecionadas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_Selecionadas.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))

        self.HMI.Table_Operacoes_Selecionadas.setShowGrid(False)
        self.HMI.Table_Operacoes_Selecionadas.setFont(self.HMI.font12)
        self.HMI.Table_Operacoes_Selecionadas.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                           color: white;
                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                             QTableView {border-bottom: 2px dashed white;
                                                                         border-right: 1px solid white;
                                                                         border-left: 1px solid white;}
                                                             QTableView::item {border-bottom: 1px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
        self.HMI.Table_Operacoes_Selecionadas.verticalHeader().hide()
        self.HMI.Table_Operacoes_Selecionadas.horizontalHeader().hide()
        self.HMI.Table_Operacoes_Selecionadas.setSelectionBehavior(QAbstractItemView.SelectRows)

        HHeader = ['Data',
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        self.HMI.Table_Operacoes_Selecionadas.setRowCount(1)
        self.HMI.Table_Operacoes_Selecionadas.setColumnCount(len(HHeader))
        for i, item in enumerate(self.data_40_1):
            if i == self.Operacoes[self.item]:
                for j in range(len(item)):
                    if isinstance(item[j], float):
                        text = str('%.8f' % item[j])
                    else:
                        text = str(item[j])
                    it = self.HMI.Table_Operacoes_Selecionadas.item(0, j)
                    it = QTableWidgetItem(text)
                    it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
                    it.setTextAlignment(Qt.AlignCenter)
                    if text in ["Compra", "Drop", "Depósito"]: it.setForeground(QBrush(QColor('green')))
                    elif text in ["Venda", "Burn", "Saque"]: it.setForeground(QBrush(QColor('red')))
                    if j == 8:
                        it.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    self.HMI.Table_Operacoes_Selecionadas.setItem(0, j, it)

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(self.data_40_1, HHeader)

        self.HMI.Table_Operacoes_SelecionadasHeader.adjustSize()
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(7, SizeCol7)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(8, SizeCol8)

        self.HMI.Table_Operacoes_Selecionadas.adjustSize()
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(7, SizeCol7)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(8, SizeCol8)

    def CreateTable_44_1(self):
        HHeader = ['Data',
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        fakedata = [('','','','','','','','','')]

        self.HMI.Table_Operacoes_SelecionadasHeader.setRowCount(1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnCount(len(HHeader))

        self.HMI.Table_Operacoes_SelecionadasHeader.setShowGrid(False)
        self.HMI.Table_Operacoes_SelecionadasHeader.setFont(self.HMI.font14)
        self.HMI.Table_Operacoes_SelecionadasHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_Operacoes_SelecionadasHeader.verticalHeader().hide()
        self.HMI.Table_Operacoes_SelecionadasHeader.horizontalHeader().hide()

        for col in range(len(HHeader)):
            it = QTableWidgetItem(str(HHeader[col]))
            it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
            it.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
            self.HMI.Table_Operacoes_SelecionadasHeader.setItem(0, col, it)

        self.HMI.Table_Operacoes_SelecionadasHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_SelecionadasHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.HMI.Table_Operacoes_SelecionadasHeader.resizeColumnsToContents()

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
        self.HMI.Table_Operacoes_SelecionadasHeader.adjustSize()
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(7, SizeCol7)

    def CreateTable_44_2(self):
        self.HMI.Table_Operacoes_Selecionadas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_Selecionadas.setFixedHeight(int(self.HMI.frameGeometry().height()*6/20*1.4))

        self.HMI.Table_Operacoes_Selecionadas.setShowGrid(False)
        self.HMI.Table_Operacoes_Selecionadas.setFont(self.HMI.font12)
        self.HMI.Table_Operacoes_Selecionadas.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                           color: white;
                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                             QTableView {border-bottom: 2px dashed white;
                                                                         border-right: 1px solid white;
                                                                         border-left: 1px solid white;}
                                                             QTableView::item {border-bottom: 1px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
        self.HMI.Table_Operacoes_Selecionadas.verticalHeader().hide()
        self.HMI.Table_Operacoes_Selecionadas.horizontalHeader().hide()
        self.HMI.Table_Operacoes_Selecionadas.setSelectionBehavior(QAbstractItemView.SelectRows)

        HHeader = ['Data',
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        self.HMI.Table_Operacoes_Selecionadas.setRowCount(len(self.Operacoes))
        self.HMI.Table_Operacoes_Selecionadas.setColumnCount(len(HHeader))
        linha = -1
        for i, item in enumerate(self.data_40_1):
            if i in self.Operacoes:
                linha += 1
                for j in range(len(item)):
                    if isinstance(item[j], float):
                        text = str('%.8f' % item[j])
                    else:
                        text = str(item[j])
                    it = self.HMI.Table_Operacoes_Selecionadas.item(linha, j)
                    it = QTableWidgetItem(text)
                    it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
                    it.setTextAlignment(Qt.AlignCenter)
                    if text in ["Compra", "Drop", "Depósito"]: it.setForeground(QBrush(QColor('green')))
                    elif text in ["Venda", "Burn", "Saque"]: it.setForeground(QBrush(QColor('red')))
                    if j == 8:
                        it.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    self.HMI.Table_Operacoes_Selecionadas.setItem(linha, j, it)

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(self.data_40_1, HHeader)

        self.HMI.Table_Operacoes_SelecionadasHeader.adjustSize()
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(7, SizeCol7)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(8, SizeCol8)

        self.HMI.Table_Operacoes_Selecionadas.adjustSize()
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(7, SizeCol7)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(8, SizeCol8)

    def OnButtonPressed(self, ButtonPressed):
        if ButtonPressed == 'ChangeDTeST':
            if self.HMI.DTeST == "": self.HMI.DTeST = "DTeST"
            elif self.HMI.DTeST == "DTeST": self.HMI.DTeST = "ST"
            elif self.HMI.DTeST == "ST": self.HMI.DTeST = "DT"
            elif self.HMI.DTeST == "DT": self.HMI.DTeST = ""

            if self.HMI.DTeST == "":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Trades Brutos.png"))
                # Habilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(True)
                self.HMI.Button_DeletarOperacao.setEnabled(True)
            elif self.HMI.DTeST == "DTeST":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Day Trades e Swing Trades.png"))
                # Desabilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(False)
                self.HMI.Button_DeletarOperacao.setEnabled(False)
            elif self.HMI.DTeST == "ST":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas ST.png"))
                # Desabilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(False)
                self.HMI.Button_DeletarOperacao.setEnabled(False)
            elif self.HMI.DTeST == "DT":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas DT.png"))
                # Desabilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(False)
                self.HMI.Button_DeletarOperacao.setEnabled(False)

            if self.HMI.PageID == '23':
                self.HMI.Table_Operacoes_Realizadas_com_Ativo.deleteLater()
                self.HMI.Table_Operacoes_Realizadas_com_Ativo = QTableWidget()
                self.HMI.HMI_Trades.HMI_Trades_Bolsa.CreateTable_23_2()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas_com_Ativo, 6, 0, 6, 10, Qt.AlignHCenter | Qt.AlignTop)

            if self.HMI.PageID == '40':
                self.HMI.Table_Operacoes_Realizadas.deleteLater()
                self.HMI.Table_Operacoes_Realizadas = QTableWidget()
                self.HMI.HMI_Trades.HMI_Trades_Criptomoedas.CreateTable_40_2()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas, 6, 0, 6, 10, Qt.AlignHCenter | Qt.AlignTop)

            elif self.HMI.PageID == '51':
                if self.HMI.DTeST_51 == "DTeST": self.HMI.DTeST_51 = "ST"
                elif self.HMI.DTeST_51 == "ST": self.HMI.DTeST_51 = "DT"
                elif self.HMI.DTeST_51 == "DT": self.HMI.DTeST_51 = "DTeST"

                if self.HMI.DTeST_51 == "DTeST":
                    self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Day Trades e Swing Trades.png"))
                elif self.HMI.DTeST_51 == "ST":
                    self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas ST.png"))
                elif self.HMI.DTeST_51 == "DT":
                    self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas DT.png"))
                self.HMI.Table_Tributacao_Header.deleteLater()
                self.HMI.Table_Tributacao_Header = QTableWidget()
                self.HMI.HMI_Tributacao.CreateTable_51_1()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Tributacao_Header, 5, 0, 1, 10, Qt.AlignHCenter | Qt.AlignBottom)
                self.HMI.Table_Tributacao.deleteLater()
                self.HMI.Table_Tributacao = QTableWidget()
                self.HMI.HMI_Tributacao.CreateTable_51_2()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Tributacao, 6, 0, 6, 10, Qt.AlignHCenter | Qt.AlignTop)

        elif ButtonPressed == 'Compra_Cripto':
            self.HMI.TipoDeOperacao = 'Compra'
            BackgroundLineEdit = "rgb(0,10,30)"
            FontColorLineEdit = "green"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("COMPRA")
            self.HMI.Button_Compra.setFont(self.HMI.font20)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("venda")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setText("depósito")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setText("saque")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setText("drop")
            self.HMI.Button_Drop.setFont(self.HMI.font16)
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setText("burn")
            self.HMI.Button_Burn.setFont(self.HMI.font16)
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setText("stake")
            self.HMI.Button_Stake.setFont(self.HMI.font16)
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setText("unstake")
            self.HMI.Button_Unstake.setFont(self.HMI.font16)
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setText("hold")
            self.HMI.Button_Hold.setFont(self.HMI.font16)
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setText("unhold")
            self.HMI.Button_Unhold.setFont(self.HMI.font16)
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")

            self.HMI.Label_Msg10.setText("Par:")
            self.HMI.Label_Msg5.setText("Preço:")

            try:
                self.HMI.TextBox_Par_Esquerda.deleteLater()
                self.HMI.Button_Info15.deleteLater()
                self.HMI.Label_Msg12.deleteLater()
                self.HMI.TextBox_Par_Direita.deleteLater()
            except: pass
            black = "rgb(0,0,0)"
            self.HMI.F_GLayout[0].removeItem(self.HMI.HBoxLayout_Par)
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignLeft)
            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.Label_Msg12.setStyleSheet('color: white')
            self.HMI.Label_Msg12.setFont(self.HMI.font14)
            self.HMI.Label_Msg12.setFixedWidth(int(self.HMI.frameGeometry().width()/20*0.9))
            self.HMI.Label_Msg12.setAlignment(Qt.AlignCenter)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Label_Msg12, Qt.AlignLeft)
            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.TextBox_Par_Direita.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Direita.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Direita.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Direita, Qt.AlignLeft)
            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignLeft)

            if self.HMI.PageID == '41': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            elif self.HMI.PageID == '43': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Par_Direita)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Direita,self.HMI.TextBox_Qqt)
            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Par_Esquerda.setFocus()

        elif ButtonPressed == 'Venda_Cripto':
            self.HMI.TipoDeOperacao = 'Venda'
            BackgroundLineEdit = "rgb(30,5,10)"
            FontColorLineEdit = "orange"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("compra")
            self.HMI.Button_Compra.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("VENDA")
            self.HMI.Button_Venda.setFont(self.HMI.font20)
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setText("depósito")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setText("saque")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setText("drop")
            self.HMI.Button_Drop.setFont(self.HMI.font16)
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setText("burn")
            self.HMI.Button_Burn.setFont(self.HMI.font16)
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setText("stake")
            self.HMI.Button_Stake.setFont(self.HMI.font16)
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setText("unstake")
            self.HMI.Button_Unstake.setFont(self.HMI.font16)
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setText("hold")
            self.HMI.Button_Hold.setFont(self.HMI.font16)
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setText("unhold")
            self.HMI.Button_Unhold.setFont(self.HMI.font16)
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")

            self.HMI.Label_Msg10.setText("Par:")
            self.HMI.Label_Msg5.setText("Preço:")

            try:
                self.HMI.TextBox_Par_Esquerda.deleteLater()
                self.HMI.Button_Info15.deleteLater()
                self.HMI.Label_Msg12.deleteLater()
                self.HMI.TextBox_Par_Direita.deleteLater()
            except: pass
            black = "rgb(0,0,0)"
            self.HMI.F_GLayout[0].removeItem(self.HMI.HBoxLayout_Par)
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignLeft)
            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.Label_Msg12.setStyleSheet('color: white')
            self.HMI.Label_Msg12.setFont(self.HMI.font14)
            self.HMI.Label_Msg12.setFixedWidth(int(self.HMI.frameGeometry().width()/20*0.9))
            self.HMI.Label_Msg12.setAlignment(Qt.AlignCenter)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Label_Msg12, Qt.AlignLeft)
            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.TextBox_Par_Direita.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Direita.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Direita.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Direita, Qt.AlignLeft)
            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignLeft)

            if self.HMI.PageID == '41': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            elif self.HMI.PageID == '43': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Par_Direita)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Direita,self.HMI.TextBox_Qqt)
            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Par_Esquerda.setFocus()

        elif ButtonPressed == 'Depósito_Cripto':
            self.HMI.TipoDeOperacao = 'Depósito'
            BackgroundLineEdit = "rgb(0,10,30)"
            FontColorLineEdit = "green"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("compra")
            self.HMI.Button_Compra.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("venda")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setText("DEPÓSITO")
            self.HMI.Button_Deposito.setFont(self.HMI.font20)
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setText("saque")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setText("drop")
            self.HMI.Button_Drop.setFont(self.HMI.font16)
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setText("burn")
            self.HMI.Button_Burn.setFont(self.HMI.font16)
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setText("stake")
            self.HMI.Button_Stake.setFont(self.HMI.font16)
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setText("unstake")
            self.HMI.Button_Unstake.setFont(self.HMI.font16)
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setText("hold")
            self.HMI.Button_Hold.setFont(self.HMI.font16)
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setText("unhold")
            self.HMI.Button_Unhold.setFont(self.HMI.font16)
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color:"+ FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")

            self.HMI.Label_Msg10.setText("Moeda:")
            self.HMI.TextBox_Preco.setText("1")
            self.HMI.Label_Msg5.setText("Preço Médio:")

            try:
                self.HMI.TextBox_Par_Esquerda.deleteLater()
                self.HMI.Button_Info15.deleteLater()
                self.HMI.Label_Msg12.deleteLater()
                self.HMI.TextBox_Par_Direita.deleteLater()
            except: pass
            black = "rgb(0,0,0)"
            self.HMI.F_GLayout[0].removeItem(self.HMI.HBoxLayout_Par)
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignLeft)
            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignLeft)

            if self.HMI.PageID == '41': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            elif self.HMI.PageID == '43': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)
            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Par_Esquerda.setFocus()

        elif ButtonPressed == 'Saque_Cripto':
            self.HMI.TipoDeOperacao = 'Saque'
            BackgroundLineEdit = "rgb(30,5,10)"
            FontColorLineEdit = "orange"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("compra")
            self.HMI.Button_Compra.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("venda")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setText("depósito")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setText("SAQUE")
            self.HMI.Button_Saque.setFont(self.HMI.font20)
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setText("drop")
            self.HMI.Button_Drop.setFont(self.HMI.font16)
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setText("burn")
            self.HMI.Button_Burn.setFont(self.HMI.font16)
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setText("stake")
            self.HMI.Button_Stake.setFont(self.HMI.font16)
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setText("unstake")
            self.HMI.Button_Unstake.setFont(self.HMI.font16)
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setText("hold")
            self.HMI.Button_Hold.setFont(self.HMI.font16)
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setText("unhold")
            self.HMI.Button_Unhold.setFont(self.HMI.font16)
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")

            self.HMI.Label_Msg10.setText("Moeda:")
            self.HMI.TextBox_Preco.setText("1")
            self.HMI.Label_Msg5.setText("Preço Médio:")

            try:
                self.HMI.TextBox_Par_Esquerda.deleteLater()
                self.HMI.Button_Info15.deleteLater()
                self.HMI.Label_Msg12.deleteLater()
                self.HMI.TextBox_Par_Direita.deleteLater()
            except: pass
            black = "rgb(0,0,0)"
            self.HMI.F_GLayout[0].removeItem(self.HMI.HBoxLayout_Par)
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignLeft)
            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignLeft)

            if self.HMI.PageID == '41': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            elif self.HMI.PageID == '43': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)
            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Par_Esquerda.setFocus()

        elif ButtonPressed == 'Drop_Cripto':
            self.HMI.TipoDeOperacao = 'Drop'
            BackgroundLineEdit = "rgb(0,10,30)"
            FontColorLineEdit = "green"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("compra")
            self.HMI.Button_Compra.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("venda")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setText("depósito")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setText("saque")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setText("DROP")
            self.HMI.Button_Drop.setFont(self.HMI.font20)
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setText("burn")
            self.HMI.Button_Burn.setFont(self.HMI.font16)
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setText("stake")
            self.HMI.Button_Stake.setFont(self.HMI.font16)
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setText("unstake")
            self.HMI.Button_Unstake.setFont(self.HMI.font16)
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setText("hold")
            self.HMI.Button_Hold.setFont(self.HMI.font16)
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setText("unhold")
            self.HMI.Button_Unhold.setFont(self.HMI.font16)
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")

            self.HMI.Label_Msg10.setText("Moeda:")
            self.HMI.TextBox_Preco.setText("0")
            self.HMI.Label_Msg5.setText("Preço Médio:")

            try:
                self.HMI.TextBox_Par_Esquerda.deleteLater()
                self.HMI.Button_Info15.deleteLater()
                self.HMI.Label_Msg12.deleteLater()
                self.HMI.TextBox_Par_Direita.deleteLater()
            except: pass
            black = "rgb(0,0,0)"
            self.HMI.F_GLayout[0].removeItem(self.HMI.HBoxLayout_Par)
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignLeft)
            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignLeft)

            if self.HMI.PageID == '41': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            elif self.HMI.PageID == '43': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)
            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Par_Esquerda.setFocus()

        elif ButtonPressed == 'Burn_Cripto':
            self.HMI.TipoDeOperacao = 'Burn'
            BackgroundLineEdit = "rgb(30,5,10)"
            FontColorLineEdit = "orange"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("compra")
            self.HMI.Button_Compra.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("venda")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setText("depósito")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setText("saque")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setText("drop")
            self.HMI.Button_Drop.setFont(self.HMI.font16)
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setText("BURN")
            self.HMI.Button_Burn.setFont(self.HMI.font20)
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setText("stake")
            self.HMI.Button_Stake.setFont(self.HMI.font16)
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setText("unstake")
            self.HMI.Button_Unstake.setFont(self.HMI.font16)
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setText("hold")
            self.HMI.Button_Hold.setFont(self.HMI.font16)
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setText("unhold")
            self.HMI.Button_Unhold.setFont(self.HMI.font16)
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")

            self.HMI.Label_Msg10.setText("Moeda:")
            self.HMI.TextBox_Preco.setText("1")
            self.HMI.Label_Msg5.setText("Preço Médio:")

            try:
                self.HMI.TextBox_Par_Esquerda.deleteLater()
                self.HMI.Button_Info15.deleteLater()
                self.HMI.Label_Msg12.deleteLater()
                self.HMI.TextBox_Par_Direita.deleteLater()
            except: pass
            black = "rgb(0,0,0)"
            self.HMI.F_GLayout[0].removeItem(self.HMI.HBoxLayout_Par)
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignLeft)
            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignLeft)

            if self.HMI.PageID == '41': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            elif self.HMI.PageID == '43': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)
            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Par_Esquerda.setFocus()

        elif ButtonPressed == 'Stake_Cripto':
            self.HMI.TipoDeOperacao = 'Stake'
            BackgroundLineEdit = "rgb(0,10,30)"
            FontColorLineEdit = "green"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("compra")
            self.HMI.Button_Compra.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("venda")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setText("depósito")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setText("saque")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setText("drop")
            self.HMI.Button_Drop.setFont(self.HMI.font16)
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setText("burn")
            self.HMI.Button_Burn.setFont(self.HMI.font16)
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setText("STAKE")
            self.HMI.Button_Stake.setFont(self.HMI.font20)
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setText("unstake")
            self.HMI.Button_Unstake.setFont(self.HMI.font16)
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setText("hold")
            self.HMI.Button_Hold.setFont(self.HMI.font16)
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setText("unhold")
            self.HMI.Button_Unhold.setFont(self.HMI.font16)
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")

            self.HMI.Label_Msg10.setText("Moeda:")
            self.HMI.TextBox_Preco.setText("1")
            self.HMI.Label_Msg5.setText("Preço Médio:")

            try:
                self.HMI.TextBox_Par_Esquerda.deleteLater()
                self.HMI.Button_Info15.deleteLater()
                self.HMI.Label_Msg12.deleteLater()
                self.HMI.TextBox_Par_Direita.deleteLater()
            except: pass
            black = "rgb(0,0,0)"
            self.HMI.F_GLayout[0].removeItem(self.HMI.HBoxLayout_Par)
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignLeft)
            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignLeft)

            if self.HMI.PageID == '41': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            elif self.HMI.PageID == '43': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)
            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Par_Esquerda.setFocus()

        elif ButtonPressed == 'Unstake_Cripto':
            self.HMI.TipoDeOperacao = 'Unstake'
            BackgroundLineEdit = "rgb(30,5,10)"
            FontColorLineEdit = "orange"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("compra")
            self.HMI.Button_Compra.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("venda")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setText("depósito")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setText("saque")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setText("drop")
            self.HMI.Button_Drop.setFont(self.HMI.font16)
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setText("burn")
            self.HMI.Button_Burn.setFont(self.HMI.font16)
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setText("stake")
            self.HMI.Button_Stake.setFont(self.HMI.font16)
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setText("UNSTAKE")
            self.HMI.Button_Unstake.setFont(self.HMI.font20)
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setText("hold")
            self.HMI.Button_Hold.setFont(self.HMI.font16)
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setText("unhold")
            self.HMI.Button_Unhold.setFont(self.HMI.font16)
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")

            self.HMI.Label_Msg10.setText("Moeda:")
            self.HMI.TextBox_Preco.setText("1")
            self.HMI.Label_Msg5.setText("Preço Médio:")

            try:
                self.HMI.TextBox_Par_Esquerda.deleteLater()
                self.HMI.Button_Info15.deleteLater()
                self.HMI.Label_Msg12.deleteLater()
                self.HMI.TextBox_Par_Direita.deleteLater()
            except: pass
            black = "rgb(0,0,0)"
            self.HMI.F_GLayout[0].removeItem(self.HMI.HBoxLayout_Par)
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignLeft)
            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignLeft)

            if self.HMI.PageID == '41': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            elif self.HMI.PageID == '43': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)
            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Par_Esquerda.setFocus()

        elif ButtonPressed == 'Hold_Cripto':
            self.HMI.TipoDeOperacao = 'Hold'
            BackgroundLineEdit = "rgb(0,10,30)"
            FontColorLineEdit = "green"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("compra")
            self.HMI.Button_Compra.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("venda")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setText("depósito")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setText("saque")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setText("drop")
            self.HMI.Button_Drop.setFont(self.HMI.font16)
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setText("burn")
            self.HMI.Button_Burn.setFont(self.HMI.font16)
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setText("stake")
            self.HMI.Button_Stake.setFont(self.HMI.font16)
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setText("unstake")
            self.HMI.Button_Unstake.setFont(self.HMI.font16)
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setText("HOLD")
            self.HMI.Button_Hold.setFont(self.HMI.font20)
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setText("unhold")
            self.HMI.Button_Unhold.setFont(self.HMI.font16)
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")

            self.HMI.Label_Msg10.setText("Moeda:")
            self.HMI.TextBox_Preco.setText("1")
            self.HMI.Label_Msg5.setText("Preço Médio:")

            try:
                self.HMI.TextBox_Par_Esquerda.deleteLater()
                self.HMI.Button_Info15.deleteLater()
                self.HMI.Label_Msg12.deleteLater()
                self.HMI.TextBox_Par_Direita.deleteLater()
            except: pass
            black = "rgb(0,0,0)"
            self.HMI.F_GLayout[0].removeItem(self.HMI.HBoxLayout_Par)
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignLeft)
            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignLeft)

            if self.HMI.PageID == '41': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            elif self.HMI.PageID == '43': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)
            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Par_Esquerda.setFocus()

        elif ButtonPressed == 'Unhold_Cripto':
            self.HMI.TipoDeOperacao = 'Unhold'
            BackgroundLineEdit = "rgb(30,5,10)"
            FontColorLineEdit = "orange"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("compra")
            self.HMI.Button_Compra.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("venda")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setText("depósito")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setText("saque")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setText("drop")
            self.HMI.Button_Drop.setFont(self.HMI.font16)
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setText("burn")
            self.HMI.Button_Burn.setFont(self.HMI.font16)
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setText("stake")
            self.HMI.Button_Stake.setFont(self.HMI.font16)
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setText("unstake")
            self.HMI.Button_Unstake.setFont(self.HMI.font16)
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setText("hold")
            self.HMI.Button_Hold.setFont(self.HMI.font16)
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setText("UNHOLD")
            self.HMI.Button_Unhold.setFont(self.HMI.font20)
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")

            self.HMI.Label_Msg10.setText("Moeda:")
            self.HMI.TextBox_Preco.setText("1")
            self.HMI.Label_Msg5.setText("Preço Médio:")

            try:
                self.HMI.TextBox_Par_Esquerda.deleteLater()
                self.HMI.Button_Info15.deleteLater()
                self.HMI.Label_Msg12.deleteLater()
                self.HMI.TextBox_Par_Direita.deleteLater()
            except: pass
            black = "rgb(0,0,0)"
            self.HMI.F_GLayout[0].removeItem(self.HMI.HBoxLayout_Par)
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignLeft)
            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage('Info15'))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignLeft)

            if self.HMI.PageID == '41': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            elif self.HMI.PageID == '43': self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)

            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)
            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Par_Esquerda.setFocus()

        elif ButtonPressed == "BuscarConversaoAutomaticamente":
            Data = self.HMI.Selecao_Ano+'/'+self.HMI.Selecao_Mes+'/'+self.HMI.Selecao_Dia+" "+self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo
            UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
            if self.HMI.TipoDeOperacao in ["Compra","Venda"]: Coin = self.HMI.TextBox_Par_Direita.text()
            else: Coin = self.HMI.TextBox_Par_Esquerda.text()

            if UserCoin == "USD" and Coin in ["USD", "BUSD", "USDT", "USDC", "USDP", "TUSD"]: self.HMI.TextBox_Conversao.setText("1")
            elif Coin == UserCoin: self.HMI.TextBox_Conversao.setText("1")
            else:
                MessageBox_Msg1 = QMessageBox()
                MessageBox_Msg1.setWindowTitle("Tem certeza?")
                MessageBox_Msg1.setText("Vamos buscar online a cotação (em "+UserCoin+") de\n"+Coin+"\nno dia\n"+Data+"\n\nA seguinte etapa pode levar alguns minutos.\nTem certeza que deseja continuar?")
                MessageBox_Msg1.setIcon(QMessageBox.Question)
                MessageBox_Msg1.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                MessageBox_Msg1.setDefaultButton(QMessageBox.Yes)
                MessageBox_Msg1.setWindowIcon(QIcon(".\images\logoARCA.png"))
                returnValue = MessageBox_Msg1.exec()

                if returnValue == QMessageBox.Yes:
                    Conversao, CotacaoUSD = self.HMI.YahooFinance.GetCotacaoCripto(Coin, UserCoin, Data)
                    self.HMI.TextBox_Conversao.setText(str(Conversao))

        elif ButtonPressed == "Page43_Next":
            try:
                if not self.HMI.DBManager.FLAG:
                    Data = self.HMI.Selecao_Ano+'/'+self.HMI.Selecao_Mes+'/'+self.HMI.Selecao_Dia+" "+self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo
                    Tipo = self.HMI.TipoDeOperacao
                    ParEsquerdo = self.HMI.TextBox_Par_Esquerda.text()
                    ParDireito = self.HMI.TextBox_Par_Direita.text()
                    Qqt = float(self.HMI.TextBox_Qqt.text())
                    Preco = float(self.HMI.TextBox_Preco.text())
                    Taxa = float(self.HMI.TextBox_Taxa.text())
                    MoedaDaTaxa = self.HMI.TextBox_MoedaDaTaxa.text()
                    Conversao = float(self.HMI.TextBox_Conversao.text())
                    Obs = self.HMI.TextBox_Obs.text()
                    Item = len(self.HMI.HMI_Trades.HMI_Trades_Criptomoedas.data_40_1)-self.HMI.HMI_Trades.HMI_Trades_Criptomoedas.Operacoes[self.HMI.HMI_Trades.HMI_Trades_Criptomoedas.item]-1

                    if self.HMI.DBManager.AlterOperacao_Cripto(Item, Data, Tipo, ParEsquerdo, ParDireito, Qqt, Preco, Taxa, MoedaDaTaxa, Conversao, Obs):
                        if self.HMI.HMI_Trades.HMI_Trades_Criptomoedas.item+1 >= len(self.HMI.HMI_Trades.HMI_Trades_Criptomoedas.Operacoes):
                            self.HMI.CreatePage('40') # Última alteração da lista
                        else: self.HMI.CreatePage('43') # Ir pra próxima alteração
                    else:
                        try: self.HMI.Label_Erro1.deleteLater()
                        except: pass
                        self.HMI.Label_Erro1 = QLabel()
                        self.HMI.Label_Erro1.setStyleSheet('color: red')
                        self.HMI.Label_Erro1.setFont(self.HMI.font12)
                        self.HMI.Label_Erro1.setAlignment(Qt.AlignCenter)
                        self.HMI.Label_Erro1.setText('Data inválida.\nTalvez já tenha uma operação nesse momento.') # Substitui a string do erro mais provável
                        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Erro1, 10, 7, 1, 1, Qt.AlignCenter)
                else:
                    MessageBox_Msg1 = QMessageBox.about(self.HMI,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')
            except:
                try: self.HMI.Label_Erro1.deleteLater()
                except: pass
                self.HMI.Label_Erro1 = QLabel()
                self.HMI.Label_Erro1.setStyleSheet('color: red')
                self.HMI.Label_Erro1.setFont(self.HMI.font12)
                self.HMI.Label_Erro1.setAlignment(Qt.AlignCenter)
                self.HMI.Label_Erro1.setText('Confira os valores inseridos.') # Substitui a string do erro mais provável
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Erro1, 10, 7, 1, 1, Qt.AlignCenter)

        elif ButtonPressed == 'Deletar Ativos da Pagina 44':
            if not self.HMI.DBManager.FLAG:
                self.HMI.DBManager.DeleteOperacao(self.HMI.HMI_Trades.HMI_Trades_Criptomoedas.Operacoes)
                self.HMI.CreatePage('40')
            else:
                MessageBox_Msg1 = QMessageBox.about(self.HMI,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')

    def Auto_Capital_Par_Esquerda(self, txt):
        txt = self.HMI.TextBox_Par_Esquerda.text()
        self.HMI.TextBox_Par_Esquerda.setText(txt.upper())

    def Auto_Capital_Par_Direita(self, txt):
        txt = self.HMI.TextBox_Par_Direita.text()
        self.HMI.TextBox_Par_Direita.setText(txt.upper())

    def Auto_Capital_MoedaDaTaxa(self, txt):
        self.HMI.TextBox_MoedaDaTaxa.setText(txt.upper())