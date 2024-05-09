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

class HMI_Trades_Bolsa(object):
    def __init__(self, HMI):
        self.HMI = HMI
        QToolTip.setFont(QFont('Arial', 12))

    def CreatePage18(self): # Edição das negociações na Bolsa
        self.HMI.BolsaOuCripto = "Bolsa" # Variável usada no DBManager

        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        Background_3 = QLabel()
        Background_3.setStyleSheet("background-color: "+black)

        Background_4 = QLabel()
        Background_4.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Edição das negociações na Bolsa')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Button_AddCorretora = QPushButton()
        self.HMI.Button_AddCorretora.setToolTip("Adicionar corretora")
        self.HMI.Button_AddCorretora.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.HMI.Button_AddCorretora.pressed.connect(lambda: self.HMI.CreatePage('20'))
        self.HMI.Button_AddCorretora.setFixedSize(40,40)
        self.HMI.Button_AddCorretora.setIconSize(QSize(35, 35))
        self.HMI.Button_AddCorretora.setIcon(QIcon("./images/add_user.png"))
        self.HMI.Button_AddCorretora.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_DeleteCorretora = QPushButton()
        self.HMI.Button_DeleteCorretora.setToolTip("Deletar corretora")
        self.HMI.Button_DeleteCorretora.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.HMI.Button_DeleteCorretora.pressed.connect(lambda: self.HMI.CreatePage('21'))
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

        CorretoraCoin = self.HMI.DBManager.GetCorretoraCoinCurrency()

        self.HMI.Button_RenameCorretora = QPushButton()
        self.HMI.Button_RenameCorretora.setToolTip("Renomear corretora")
        self.HMI.Button_RenameCorretora.pressed.connect(lambda: self.HMI.CreatePage('22'))
        self.HMI.Button_RenameCorretora.setFixedSize(40,40)
        self.HMI.Button_RenameCorretora.setIconSize(QSize(35, 35))
        self.HMI.Button_RenameCorretora.setIcon(QIcon("./images/Rename.png"))
        self.HMI.Button_RenameCorretora.setStyleSheet("QPushButton {background-color: black; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
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
        self.HMI.TextBox_Msg2.setText(CorretoraCoin+' ~'+str(self.HMI.DBManager.GetPatrimonioTotalCorretora()))
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
        Investido = round(self.HMI.DBManager.GetTotalInvestidoEmCorretora(self.HMI.ComboBox_Corretoras.currentText(), "Bolsa"), 2)
        self.HMI.TextBox_Msg6.setText(CorretoraCoin+' ~'+str(Investido))
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
        self.HMI.TextBox_Msg3.setText(CorretoraCoin+' '+str(self.HMI.DBManager.GetValorEmContaCorrente(self.HMI.ComboBox_Corretoras.currentText())))
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
        self.HMI.TextBox_Msg5.setText(CorretoraCoin+" "+str(valor))
        if valor >= 0: self.HMI.TextBox_Msg5.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Msg5.setStyleSheet('QLineEdit {background-color: black; color: orange;}')
        if self.HMI.ShowValues: self.HMI.TextBox_Msg5.setEchoMode(QLineEdit.Normal)
        else: self.HMI.TextBox_Msg5.setEchoMode(QLineEdit.Password)

        self.HMI.Label_Title3 = QLabel()
        self.HMI.Label_Title3.setText("Editar operações")
        self.HMI.Label_Title3.setStyleSheet('color: white')
        self.HMI.Label_Title3.setFont(self.HMI.font24)

        self.HMI.Gif_AlterarOPBolsa = QLabel()
        self.HMI.Movie_AlterarOPBolsa = QMovie("./images/GIF_Registro.gif")
        self.HMI.Movie_AlterarOPBolsa.setScaledSize(QSize().scaled(self.HMI.frameGeometry().width()*12/20/2,self.HMI.frameGeometry().height()*7/10*.95-30, Qt.KeepAspectRatio))
        self.HMI.Gif_AlterarOPBolsa.setMovie(self.HMI.Movie_AlterarOPBolsa)
        self.HMI.Movie_AlterarOPBolsa.start()

        self.HMI.Button_AlterarOPBolsaInvisivel = QPushButton()
        self.HMI.Button_AlterarOPBolsaInvisivel.setToolTip("Alterar operação feita na B3")
        self.HMI.Button_AlterarOPBolsaInvisivel.pressed.connect(lambda: self.HMI.CreatePage('23'))
        self.HMI.Button_AlterarOPBolsaInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_AlterarOPBolsaInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()*12/20/2),int(self.HMI.frameGeometry().height()*7/10*.95))
        self.HMI.Button_AlterarOPBolsaInvisivel.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_AlterarOPBolsa = QPushButton("Registros")
        self.HMI.Button_AlterarOPBolsa.pressed.connect(lambda: self.HMI.CreatePage('23'))
        self.HMI.Button_AlterarOPBolsa.setToolTip("Alterar operação feita na B3")
        self.HMI.Button_AlterarOPBolsa.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_AlterarOPBolsa.setFont(self.HMI.font16)
        self.HMI.Button_AlterarOPBolsa.setFixedSize(int(self.HMI.frameGeometry().width()*12/20/2),int(self.HMI.frameGeometry().height()*1/10*.95))
        self.HMI.Button_AlterarOPBolsa.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Label_Title4 = QLabel()
        self.HMI.Label_Title4.setText("Movimentação")
        self.HMI.Label_Title4.setStyleSheet('color: white')
        self.HMI.Label_Title4.setFont(self.HMI.font24)

        self.HMI.Gif_DepositosESaquesBolsa = QLabel()
        self.HMI.Movie_DepositosESaquesBolsa = QMovie("./images/GIF_Depósitos e Saques.gif")
        self.HMI.Movie_DepositosESaquesBolsa.setScaledSize(QSize().scaled(self.HMI.frameGeometry().width()*12/20/2,self.HMI.frameGeometry().height()*3/10*.95-30, Qt.KeepAspectRatio))
        self.HMI.Gif_DepositosESaquesBolsa.setMovie(self.HMI.Movie_DepositosESaquesBolsa)
        self.HMI.Movie_DepositosESaquesBolsa.start()

        self.HMI.Button_DepositosESaquesBolsaInvisivel = QPushButton()
        self.HMI.Button_DepositosESaquesBolsaInvisivel.setToolTip("Registro de depósitos e saques")
        self.HMI.Button_DepositosESaquesBolsaInvisivel.pressed.connect(lambda: self.HMI.CreatePage('24'))
        self.HMI.Button_DepositosESaquesBolsaInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_DepositosESaquesBolsaInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()*12/20/2),int(self.HMI.frameGeometry().height()*3/10*.95))
        self.HMI.Button_DepositosESaquesBolsaInvisivel.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_DepositosESaquesBolsa = QPushButton("Depósitos e Saques")
        self.HMI.Button_DepositosESaquesBolsa.pressed.connect(lambda: self.HMI.CreatePage('24'))
        self.HMI.Button_DepositosESaquesBolsa.setToolTip("Registro de depósitos e saques")
        self.HMI.Button_DepositosESaquesBolsa.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_DepositosESaquesBolsa.setFont(self.HMI.font16)
        self.HMI.Button_DepositosESaquesBolsa.setFixedSize(int(self.HMI.frameGeometry().width()*12/20/2),int(self.HMI.frameGeometry().height()*1/10*.95))
        self.HMI.Button_DepositosESaquesBolsa.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Gif_ContaCorrenteBolsa = QLabel()
        self.HMI.Movie_ContaCorrenteBolsa = QMovie("./images/GIF_Em conta-corrente.gif")
        self.HMI.Movie_ContaCorrenteBolsa.setScaledSize(QSize().scaled(self.HMI.frameGeometry().width()*12/20/2,self.HMI.frameGeometry().height()*3/10*.95-30, Qt.KeepAspectRatio))
        self.HMI.Gif_ContaCorrenteBolsa.setMovie(self.HMI.Movie_ContaCorrenteBolsa)
        self.HMI.Movie_ContaCorrenteBolsa.start()

        self.HMI.Button_ContaCorrenteBolsaInvisivel = QPushButton()
        self.HMI.Button_ContaCorrenteBolsaInvisivel.pressed.connect(lambda: self.HMI.CreatePage('25'))
        self.HMI.Button_ContaCorrenteBolsaInvisivel.setToolTip("Registro de valor em conta-corrente")
        self.HMI.Button_ContaCorrenteBolsaInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_ContaCorrenteBolsaInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()*12/20/2),int(self.HMI.frameGeometry().height()*3/10*.95))
        self.HMI.Button_ContaCorrenteBolsaInvisivel.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_ContaCorrenteBolsa = QPushButton("Em conta-corrente")
        self.HMI.Button_ContaCorrenteBolsa.setToolTip("Registro de valor em conta-corrente")
        self.HMI.Button_ContaCorrenteBolsa.pressed.connect(lambda: self.HMI.CreatePage('25'))
        self.HMI.Button_ContaCorrenteBolsa.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_ContaCorrenteBolsa.setFont(self.HMI.font16)
        self.HMI.Button_ContaCorrenteBolsa.setFixedSize(int(self.HMI.frameGeometry().width()*12/20/2),int(self.HMI.frameGeometry().height()*1/10*.95))
        self.HMI.Button_ContaCorrenteBolsa.setCursor(QCursor(Qt.PointingHandCursor))

        if self.HMI.ComboBox_Corretoras.currentText() == '':
            ButtonsEnabled = False
            color = 'red'
        else:
            ButtonsEnabled = True
            color = 'white'
        self.HMI.Button_AlterarOPBolsa.setEnabled(ButtonsEnabled)
        self.HMI.Button_AlterarOPBolsaInvisivel.setEnabled(ButtonsEnabled)
        self.HMI.Button_AlterarOPBolsa.setStyleSheet('background-color: black; color: '+color+'; border: 1px solid rgb(0, 0, 0)')
        self.HMI.Button_DepositosESaquesBolsa.setEnabled(ButtonsEnabled)
        self.HMI.Button_DepositosESaquesBolsaInvisivel.setEnabled(ButtonsEnabled)
        self.HMI.Button_DepositosESaquesBolsa.setStyleSheet('background-color: black; color: '+color+'; border: 1px solid rgb(0, 0, 0)')
        self.HMI.Button_ContaCorrenteBolsa.setEnabled(ButtonsEnabled)
        self.HMI.Button_ContaCorrenteBolsaInvisivel.setEnabled(ButtonsEnabled)
        self.HMI.Button_ContaCorrenteBolsa.setStyleSheet('background-color: black; color: '+color+'; border: 1px solid rgb(0, 0, 0)')

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
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_4, 0, 1, 5, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Title3, 0, 0, 3, 1, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_AlterarOPBolsa, 1, 0, 3, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AlterarOPBolsaInvisivel, 1, 0, 3, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AlterarOPBolsa, 4, 0, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Title4, 0, 1, 1, 1, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_DepositosESaquesBolsa, 1, 1, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DepositosESaquesBolsaInvisivel, 1, 1, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DepositosESaquesBolsa, 2, 1, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_ContaCorrenteBolsa, 3, 1, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_ContaCorrenteBolsaInvisivel, 3, 1, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_ContaCorrenteBolsa, 4, 1, 1, 1, Qt.AlignCenter)

        if len(corretoras) == 0:
            self.HMI.Button_RenameCorretora.setEnabled(False)
            self.HMI.Button_DeleteCorretora.setEnabled(False)

    def CreatePage20(self): # Adicionar nova corretora de bolsa
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Adicionar nova corretora de bolsa')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Insira o nome da corretora:')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font16)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_NovaCorretora = QLineEdit()
        self.HMI.TextBox_NovaCorretora.returnPressed.connect(lambda: self.HMI.CreatePage('18_'))
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
        self.HMI.Button_AdicionarCorretora.pressed.connect(lambda: self.HMI.CreatePage('18_'))
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

    def CreatePage21(self): # Deletar corretora
        MessageBox_Msg1 = QMessageBox()
        MessageBox_Msg1.setWindowTitle("Deletar corretora")
        MessageBox_Msg1.setText("Tem certeza que deseja deletar a "+self.HMI.ComboBox_Corretoras.currentText()+'?\nNote que esse processo é irreversível\ne apagará também todas as operações\nfeitas nessa corretora.')
        MessageBox_Msg1.setIcon(QMessageBox.Question)
        MessageBox_Msg1.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
        MessageBox_Msg1.setDefaultButton(QMessageBox.Cancel)
        MessageBox_Msg1.setWindowIcon(QIcon(".\images\logoARCA.png"))

        returnValue = MessageBox_Msg1.exec()
        if returnValue == QMessageBox.Yes:
            self.HMI.DBManager.DeleteCorretora()
            self.HMI.CreatePage('18')

    def CreatePage22(self): # Renomear corretora da bolsa
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Renomear corretora da bolsa')
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
        self.HMI.TextBox_NovoNomeCorretora.returnPressed.connect(lambda: self.HMI.CreatePage('18_'))
        self.HMI.TextBox_NovoNomeCorretora.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))

        self.HMI.Button_RenomearCorretora = QPushButton('Seguinte')
        self.HMI.Button_RenomearCorretora.pressed.connect(lambda: self.HMI.CreatePage('18_'))
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

        self.HMI.TextBox_NovoNomeCorretora.setFocus()

    def CreatePage23(self): # Registros
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

        self.HMI.Button_AddAtivo = QPushButton()
        self.HMI.Button_AddAtivo.pressed.connect(lambda: self.HMI.CreatePage('26'))
        self.HMI.Button_AddAtivo.setFixedSize(40,40)
        self.HMI.Button_AddAtivo.setIconSize(QSize(35, 35))
        self.HMI.Button_AddAtivo.setIcon(QIcon("./images/add_user.png"))
        self.HMI.Button_AddAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AddAtivo.setToolTip("Adicionar ativo")
        self.HMI.Button_AddAtivo.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")

        try: self.HMI.ComboBox_Ativos.deleteLater()
        except: pass        
        self.HMI.ComboBox_Ativos = QComboBox()
        self.HMI.ComboBox_Ativos.setEnabled(True)
        self.HMI.ComboBox_Ativos.setFont(self.HMI.font16)
        self.HMI.ComboBox_Ativos.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_Ativos.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        self.HMI.ComboBox_Ativos.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        ativos = self.HMI.DBManager.GetAtivos()
        for idx, ativo in enumerate(ativos):
            self.HMI.ComboBox_Ativos.addItem(ativo)
        if self.HMI.idxAtivo < len(ativos):
            self.HMI.ComboBox_Ativos.setCurrentIndex(self.HMI.idxAtivo)

        self.HMI.Button_RenameAtivo = QPushButton()
        self.HMI.Button_RenameAtivo.setToolTip("Registro de depósitos e saques")
        self.HMI.Button_RenameAtivo.pressed.connect(lambda: self.HMI.CreatePage('27'))
        self.HMI.Button_RenameAtivo.setFixedSize(40,40)
        self.HMI.Button_RenameAtivo.setIconSize(QSize(35, 35))
        self.HMI.Button_RenameAtivo.setIcon(QIcon("./images/Rename.png"))
        self.HMI.Button_RenameAtivo.setStyleSheet("QPushButton {background-color: black; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.HMI.Button_RenameAtivo.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Label_Msg2 = QLabel('Em estoque:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font12)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Msg2 = QLineEdit()
        self.HMI.TextBox_Msg2.setText(str(self.HMI.DBManager.GetEstoque()))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Password)
        if float(self.HMI.TextBox_Msg2.text()) >= 0: self.HMI.TextBox_Msg2.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Msg2.setStyleSheet('QLineEdit {background-color: black; color: red;}')
        self.HMI.TextBox_Msg2.setFont(self.HMI.font12)
        self.HMI.TextBox_Msg2.setEnabled(False)
        self.HMI.TextBox_Msg2.setAlignment(Qt.AlignLeft)

        self.HMI.Button_DTeST = QPushButton()
        self.HMI.Button_DTeST.setToolTip("Alterar apresentação de DT e ST")
        self.HMI.Button_DTeST.pressed.connect(lambda: self.OnButtonPressed('ChangeDTeST'))
        self.HMI.Button_DTeST.setFixedSize(70*3+5,35*3+5)
        self.HMI.Button_DTeST.setIconSize(QSize(70*3, 35*3))
        self.HMI.Button_DTeST.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_DTeST.setCursor(QCursor(Qt.PointingHandCursor))
        if self.HMI.DTeST == "NotDefined":
            self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Trades Brutos.png"))
            self.HMI.DTeST = ""
        elif self.HMI.DTeST == "": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Trades Brutos.png"))
        elif self.HMI.DTeST == "DTeST": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Day Trades e Swing Trades.png"))
        elif self.HMI.DTeST == "ST": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas ST.png"))
        elif self.HMI.DTeST == "DT": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas DT.png"))

        self.HMI.Button_AddOperacao = QPushButton('Adicionar operação')
        self.HMI.Button_AddOperacao.pressed.connect(lambda: self.HMI.CreatePage('28'))
        self.HMI.Button_AddOperacao.setFixedSize(160,40)
        self.HMI.Button_AddOperacao.setIconSize(QSize(35, 35))
        self.HMI.Button_AddOperacao.setIcon(QIcon("./images/add_user.png"))
        self.HMI.Button_AddOperacao.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AddOperacao.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)}')

        self.HMI.Button_AlterarOperacao = QPushButton('Alterar operação')
        self.HMI.Button_AlterarOperacao.pressed.connect(lambda: self.HMI.CreatePage('29'))
        self.HMI.Button_AlterarOperacao.setFixedSize(160,40)
        self.HMI.Button_AlterarOperacao.setIconSize(QSize(35, 35))
        self.HMI.Button_AlterarOperacao.setIcon(QIcon("./images/iconeAdjustDB.png"))
        self.HMI.Button_AlterarOperacao.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AlterarOperacao.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)}')

        self.HMI.Button_DeletarOperacao = QPushButton('Deletar operação')
        self.HMI.Button_DeletarOperacao.pressed.connect(lambda: self.HMI.CreatePage('30'))
        self.HMI.Button_DeletarOperacao.setFixedSize(160,40)
        self.HMI.Button_DeletarOperacao.setIconSize(QSize(35, 35))
        self.HMI.Button_DeletarOperacao.setIcon(QIcon("./images/delete_broker.png"))
        self.HMI.Button_DeletarOperacao.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_DeletarOperacao.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)}')

        self.HMI.Label_Msg1 = QLabel('Operações realizadas com '+self.HMI.ComboBox_Ativos.currentText())
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font20)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignLeft)

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader = QTableWidget()
        self.HMI.Table_Operacoes_Realizadas_com_Ativo = QTableWidget()

        self.CreateTable_23_1() # Table_Operacoes_Realizadas_com_AtivoHeader
        self.CreateTable_23_2() # Table_Operacoes_Realizadas_com_Ativo (Criada com uma thread)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 3, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_3, 4, 0, 8, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 10, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AddAtivo, 2, 0, 1, 1, Qt.AlignRight)

        self.HMI.VBoxLayout_Ativo = QVBoxLayout()
        self.HMI.VBoxLayout_Ativo.addWidget(self.HMI.ComboBox_Ativos, Qt.AlignCenter)
        self.HMI.HBoxLayout_Ativo = QHBoxLayout()
        self.HMI.HBoxLayout_Ativo.addWidget(self.HMI.Label_Msg2, Qt.AlignCenter)
        self.HMI.HBoxLayout_Ativo.addWidget(self.HMI.TextBox_Msg2, Qt.AlignCenter)
        self.HMI.VBoxLayout_Ativo.addLayout(self.HMI.HBoxLayout_Ativo, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount - 1].addLayout(self.HMI.VBoxLayout_Ativo, 1, 1, 3, 2, Qt.AlignCenter)
        # self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_Ativos, 2, 1, 1, 2, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RenameAtivo, 2, 3, 1, 1, Qt.AlignLeft)
        # self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 3, 1, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        # self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg2, 3, 2, 1, 1, Qt.AlignCenter | Qt.AlignLeft)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DTeST, 1, 6, 3, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AddOperacao, 1, 7, 1, 3, Qt.AlignCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AlterarOperacao, 2, 7, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DeletarOperacao, 3, 7, 1, 3, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 4, 0, 1, 10, Qt.AlignLeft | Qt.AlignVCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader, 5, 0, 1, 10, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas_com_Ativo, 6, 0, 6, 10, Qt.AlignHCenter | Qt.AlignTop)

        if not len(ativos) > 0:
            self.HMI.Button_DTeST.setEnabled(False)
            self.HMI.Button_AddOperacao.setEnabled(False)
            self.HMI.Button_AlterarOperacao.setEnabled(False)
            self.HMI.Button_DeletarOperacao.setEnabled(False)
            self.HMI.Button_RenameAtivo.setEnabled(False)

    def CreatePage24(self): # Informar depósitos e saques
        black = 'rgb(0, 0, 0)'
        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel()
        self.HMI.Label_Titulo.setText('Informar depósitos e saques efetuados na\n'+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)

        self.HMI.Label_Msg1 = QLabel()
        self.HMI.Label_Msg1.setText('\n\n\nRealizei um ')
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font16)

        self.HMI.Button_Deposito = QPushButton('DEPÓSITO')
        self.HMI.Button_Deposito.pressed.connect(lambda: self.OnButtonPressed('Deposito'))
        self.HMI.Button_Deposito.setStyleSheet('background-color: black; color: green')
        self.HMI.Button_Deposito.setFont(self.HMI.font20)
        self.HMI.Button_Deposito.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Deposito = True

        self.HMI.Button_Saque = QPushButton('saque')
        self.HMI.Button_Saque.pressed.connect(lambda: self.OnButtonPressed('Saque'))
        self.HMI.Button_Saque.setStyleSheet('background-color: black; color: gray')
        self.HMI.Button_Saque.setFont(self.HMI.font16)
        self.HMI.Button_Saque.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Label_Msg2 = QLabel()
        self.HMI.Label_Msg2.setText(' no valor de '+self.HMI.DBManager.GetCorretoraCoinCurrency())
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)

        self.HMI.TextBox_Valor = QLineEdit()
        if self.HMI.ShowValues:
            self.HMI.TextBox_Valor.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Valor.setEchoMode(QLineEdit.Password)
        self.HMI.TextBox_Valor.setFont(self.HMI.font16)
        self.HMI.TextBox_Valor.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_Valor.setStyleSheet('color: green')
        # self.HMI.TextBox_Valor.returnPressed.connect(lambda: self.HMI.CreatePage('24_'))

        self.HMI.Label_Msg3 = QLabel()
        self.HMI.Label_Msg3.setText(' no dia ')
        self.HMI.Label_Msg3.setAlignment(Qt.AlignCenter)
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font16)

        self.HMI.Selecao_Ano = str(datetime.now().year)
        self.HMI.Selecao_Mes = str(datetime.now().month)
        self.HMI.Selecao_Dia = str(datetime.now().day)

        self.HMI.Button_Calendario = QPushButton(self.HMI.Selecao_Ano+"/"+self.HMI.Selecao_Mes+"/"+self.HMI.Selecao_Dia)
        self.HMI.Button_Calendario.setFont(self.HMI.font16)
        self.HMI.Button_Calendario.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.Button_Calendario.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Calendario.pressed.connect(lambda: self.HMI.OnButtonPressed("Abrir Calendário"))

        self.HMI.Selecao_Hora = '00'
        self.HMI.Selecao_Minuto = '00'
        self.HMI.Selecao_Segundo = '00'

        self.HMI.Button_Relogio = QPushButton(self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo)
        self.HMI.Button_Relogio.setFont(self.HMI.font16)
        self.HMI.Button_Relogio.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.Button_Relogio.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Relogio.pressed.connect(lambda: self.HMI.OnButtonPressed("Abrir Relógio"))

        self.HMI.Button_Voltar = QPushButton("Voltar")
        self.HMI.Button_Voltar.pressed.connect(lambda: self.HMI.CreatePage('18'))
        self.HMI.Button_Voltar.setStyleSheet('background-color: gray; color: black')
        self.HMI.Button_Voltar.setFont(self.HMI.font16)
        self.HMI.Button_Voltar.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Voltar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Voltar.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Voltar.setIcon(QIcon("./images/Voltar.png"))

        self.HMI.Button_Registrar = QPushButton("Registrar")
        self.HMI.Button_Registrar.pressed.connect(lambda: self.HMI.CreatePage('24_'))
        self.HMI.Button_Registrar.setStyleSheet('background-color: green; color: black')
        self.HMI.Button_Registrar.setFont(self.HMI.font16)
        self.HMI.Button_Registrar.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Registrar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Registrar.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Registrar.setIcon(QIcon("./images/log_in.png"))

        self.HMI.Table_DepositosESaques_Header = QTableWidget()
        self.HMI.Table_DepositosESaques = QTableWidget()

        self.CreateTable_24_1() # Table_Operacoes_Realizadas_com_AtivoHeader
        self.CreateTable_24_2() # Table_Operacoes_Realizadas_com_Ativo (Criada com uma thread)

        self.HMI.Button_DeleteRegistro = QPushButton()
        self.HMI.Button_DeleteRegistro.setToolTip("Deletar registro")
        self.HMI.Button_DeleteRegistro.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.HMI.Button_DeleteRegistro.pressed.connect(lambda: self.OnButtonPressed('Delete Registro'))
        self.HMI.Button_DeleteRegistro.setFixedSize(40,40)
        self.HMI.Button_DeleteRegistro.setIconSize(QSize(35, 35))
        self.HMI.Button_DeleteRegistro.setIcon(QIcon("./images/delete_broker.png"))
        self.HMI.Button_DeleteRegistro.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 4)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 8, 4)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 4, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DeleteRegistro, 1, 3, 1, 1, Qt.AlignRight | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_DepositosESaques_Header, 2, 3, 1, 1, Qt.AlignRight | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_DepositosESaques, 3, 3, 1, 1, Qt.AlignRight | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 2, 4, Qt.AlignCenter) # 'Realizei um '
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Deposito, 3, 0, 1, 2, Qt.AlignRight | Qt.AlignVCenter) # Depósito
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Saque, 3, 2, 1, 2, Qt.AlignLeft | Qt.AlignVCenter) # Saque
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 4, 0, 1, 2, Qt.AlignVCenter | Qt.AlignRight) # ' no valor de '
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Valor, 4, 2, 1, 2, Qt.AlignVCenter | Qt.AlignLeft) # Valor
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 5, 0, 1, 4, Qt.AlignCenter) # ' no valor de '
        self.HMI.HBoxLayout_Data = QHBoxLayout()
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Calendario, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Relogio, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Data, 6, 0, 1, 4, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Voltar, 8, 0, 1, 2, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Registrar, 8, 2, 1, 2, Qt.AlignCenter)
        self.HMI.TextBox_Valor.setFocus()

    def CreatePage25(self): # Saldo em conta-corrente
        CorretoraCoin = self.HMI.DBManager.GetCorretoraCoinCurrency()
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel()
        self.HMI.Label_Titulo.setText('Saldo em conta-corrente na\n'+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)

        self.HMI.Label_Msg1 = QLabel()
        self.HMI.Label_Msg1.setText('Registrado')
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font16)

        self.HMI.TextBox_Msg2 = QLineEdit()
        self.HMI.TextBox_Msg2.setText(CorretoraCoin+' '+str(self.HMI.DBManager.GetValorEmContaCorrente(self.HMI.ComboBox_Corretoras.currentText())))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Password)
        self.HMI.TextBox_Msg2.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        self.HMI.TextBox_Msg2.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg2.setEnabled(False)
        self.HMI.TextBox_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg3 = QLabel()
        self.HMI.Label_Msg3.setText('Valor atualizado ('+CorretoraCoin+')')
        self.HMI.Label_Msg3.setAlignment(Qt.AlignCenter)
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font16)

        self.HMI.TextBox_CCAtualizada = QLineEdit()
        if self.HMI.ShowValues:
            self.HMI.TextBox_CCAtualizada.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_CCAtualizada.setEchoMode(QLineEdit.Password)
        self.HMI.TextBox_CCAtualizada.returnPressed.connect(lambda: self.HMI.CreatePage('18_'))
        self.HMI.TextBox_CCAtualizada.setFont(self.HMI.font16)
        self.HMI.TextBox_CCAtualizada.setAlignment(Qt.AlignCenter)

        self.HMI.Button_Voltar = QPushButton("Deixar como está")
        self.HMI.Button_Voltar.pressed.connect(lambda: self.HMI.CreatePage('18'))
        self.HMI.Button_Voltar.setStyleSheet('background-color: gray; color: black')
        self.HMI.Button_Voltar.setFont(self.HMI.font16)
        self.HMI.Button_Voltar.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Voltar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Voltar.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Voltar.setIcon(QIcon("./images/Voltar.png"))

        self.HMI.Button_Atualizar = QPushButton("Atualizar")
        self.HMI.Button_Atualizar.pressed.connect(lambda: self.HMI.CreatePage('18_'))
        self.HMI.Button_Atualizar.setStyleSheet('background-color: green; color: black')
        self.HMI.Button_Atualizar.setFont(self.HMI.font16)
        self.HMI.Button_Atualizar.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Atualizar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Atualizar.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Atualizar.setIcon(QIcon("./images/log_in.png"))

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 5, 2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 2, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 2, 0, Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg2, 3, 0, Qt.AlignTop | Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 2, 1, Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_CCAtualizada, 3, 1, Qt.AlignTop | Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Voltar, 5, 0, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Atualizar, 5, 1, Qt.AlignCenter)
        self.HMI.TextBox_CCAtualizada.setFocus()

    def CreatePage26(self): # Adicionar novo ativo
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Adicionar novo ativo')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Insira o nome do ativo:')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font16)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_NomeNovoAtivo = QLineEdit()
        self.HMI.TextBox_NomeNovoAtivo.setFont(self.HMI.font18)
        self.HMI.TextBox_NomeNovoAtivo.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_NomeNovoAtivo.returnPressed.connect(lambda: self.HMI.CreatePage_Decisao())
        self.HMI.TextBox_NomeNovoAtivo.setFixedWidth(int(self.HMI.frameGeometry().width()/8*0.9))
        completer = QCompleter(self.HMI.DBManager.GetAllTickers())
        self.HMI.TextBox_NomeNovoAtivo.setCompleter(completer)

        self.HMI.Label_Msg2 = QLabel('Selecione o tipo do ativo:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.ComboBox_TipoDeAtivo = QComboBox()
        self.HMI.ComboBox_TipoDeAtivo.setEditable(True)
        self.HMI.ComboBox_TipoDeAtivo.setFont(self.HMI.font16)
        self.HMI.ComboBox_TipoDeAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_TipoDeAtivo.setStyleSheet("background-color: rgb(10, 10, 10); color: rgb(255, 255, 255); border: none")
        self.HMI.ComboBox_TipoDeAtivo.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        for idx, Tipo in enumerate(self.HMI.DBManager.GetTiposDeAtivo()):
            self.HMI.ComboBox_TipoDeAtivo.addItem(Tipo)
            try:
                if Tipo == self.HMI.TextBox_TipoAtivo.text(): self.HMI.idxTipoDeAtivo = idx
            except:pass
        if self.HMI.idxTipoDeAtivo < len(self.HMI.DBManager.GetTiposDeAtivo()):
            self.HMI.ComboBox_TipoDeAtivo.setCurrentIndex(self.HMI.idxTipoDeAtivo)
        line_edit = self.HMI.ComboBox_TipoDeAtivo.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)

        self.HMI.Button_AddTipoAtivo = QPushButton()
        self.HMI.Button_AddTipoAtivo.setToolTip("Adicionar tipo de ativo")
        self.HMI.Button_AddTipoAtivo.pressed.connect(lambda: self.HMI.CreatePage('31a'))
        self.HMI.Button_AddTipoAtivo.setFixedSize(40,40)
        self.HMI.Button_AddTipoAtivo.setIconSize(QSize(35, 35))
        self.HMI.Button_AddTipoAtivo.setIcon(QIcon("./images/add_user.png"))
        self.HMI.Button_AddTipoAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AddTipoAtivo.setStyleSheet("QToolTip {background-color: black; color: white;border: black solid 1px}")

        self.HMI.Label_Msg3 = QLabel('Selecione o sub-tipo do ativo:')
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font16)
        self.HMI.Label_Msg3.setAlignment(Qt.AlignCenter)

        self.HMI.ComboBox_SubtipoDeAtivo = QComboBox()
        self.HMI.ComboBox_SubtipoDeAtivo.setEditable(True)
        self.HMI.ComboBox_SubtipoDeAtivo.setFont(self.HMI.font16)
        self.HMI.ComboBox_SubtipoDeAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_SubtipoDeAtivo.setStyleSheet("background-color: rgb(10, 10, 10); color: rgb(255, 255, 255); border: none")
        for idx, SubTipo in enumerate(self.HMI.DBManager.GetSubtiposDeAtivo()):
            self.HMI.ComboBox_SubtipoDeAtivo.addItem(SubTipo)
            try:
                if SubTipo == self.HMI.TextBox_SubTipoAtivo.text(): self.HMI.idxSubtipoDeAtivo = idx
            except:pass
        if self.HMI.idxSubtipoDeAtivo < len(self.HMI.DBManager.GetSubtiposDeAtivo()):
            self.HMI.ComboBox_SubtipoDeAtivo.setCurrentIndex(self.HMI.idxSubtipoDeAtivo)
        line_edit = self.HMI.ComboBox_SubtipoDeAtivo.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)

        self.HMI.Button_AddSubTipoAtivo = QPushButton()
        self.HMI.Button_AddSubTipoAtivo.pressed.connect(lambda: self.HMI.CreatePage('32a'))
        self.HMI.Button_AddSubTipoAtivo.setFixedSize(40,40)
        self.HMI.Button_AddSubTipoAtivo.setIconSize(QSize(35, 35))
        self.HMI.Button_AddSubTipoAtivo.setIcon(QIcon("./images/add_user.png"))
        self.HMI.Button_AddSubTipoAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AddSubTipoAtivo.setToolTip("Adicionar subtipo de ativo")
        self.HMI.Button_AddSubTipoAtivo.setStyleSheet("QToolTip {background-color: black; color: white;border: black solid 1px}")

        self.HMI.Label_Msg4 = QLabel('Selecione o setor do ativo:')
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font16)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignCenter)

        self.HMI.ComboBox_SetorAtivo = QComboBox()
        self.HMI.ComboBox_SetorAtivo.setEditable(True)
        self.HMI.ComboBox_SetorAtivo.setFont(self.HMI.font16)
        self.HMI.ComboBox_SetorAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_SetorAtivo.setStyleSheet("background-color: rgb(10, 10, 10); color: rgb(255, 255, 255); border: none")
        for idx, Setor in enumerate(self.HMI.DBManager.GetSetoresDeAtivo()):
            self.HMI.ComboBox_SetorAtivo.addItem(Setor)
            try:
                if Setor == self.HMI.TextBox_SetorAtivo.text(): self.HMI.idxSetorAtivo = idx
            except:pass
        if self.HMI.idxSetorAtivo < len(self.HMI.DBManager.GetSetoresDeAtivo()):
            self.HMI.ComboBox_SetorAtivo.setCurrentIndex(self.HMI.idxSetorAtivo)
        line_edit = self.HMI.ComboBox_SetorAtivo.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)

        self.HMI.Button_AddSetorAtivo = QPushButton()
        self.HMI.Button_AddSetorAtivo.pressed.connect(lambda: self.HMI.CreatePage('33'))
        self.HMI.Button_AddSetorAtivo.setFixedSize(40,40)
        self.HMI.Button_AddSetorAtivo.setIconSize(QSize(35, 35))
        self.HMI.Button_AddSetorAtivo.setIcon(QIcon("./images/update.png"))
        self.HMI.Button_AddSetorAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AddSetorAtivo.setToolTip("Adicionar setor de ativo")
        self.HMI.Button_AddSetorAtivo.setStyleSheet("QToolTip {background-color: black; color: white;border: black solid 1px}")

        self.HMI.Button_Seguinte = QPushButton('Seguinte')
        self.HMI.Button_Seguinte.pressed.connect(lambda: self.HMI.CreatePage_Decisao())
        self.HMI.Button_Seguinte.setFont(self.HMI.font16)
        self.HMI.Button_Seguinte.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Seguinte.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Seguinte.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_Seguinte.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Seguinte.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Label_Msg5 = QLabel('A etapa seguinte pode levar alguns minutos...')
        self.HMI.Label_Msg5.setStyleSheet('color: white')
        self.HMI.Label_Msg5.setFont(self.HMI.font12)
        self.HMI.Label_Msg5.setAlignment(Qt.AlignCenter)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 19, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 4, 0, 1, 3, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_NomeNovoAtivo, 5, 0, 1, 3, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 6, 0, 1, 3, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_TipoDeAtivo, 7, 1, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        # self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AddTipoAtivo, 7, 2, 1, 1, Qt.AlignLeft | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 8, 0, 1, 3, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_SubtipoDeAtivo, 9, 1, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        # self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AddSubTipoAtivo, 9, 2, 1, 1, Qt.AlignLeft | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 10, 0, 1, 3, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_SetorAtivo, 11, 1, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AddSetorAtivo, 11, 2, 1, 1, Qt.AlignLeft | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Seguinte, 13, 0, 2, 3, Qt.AlignHCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 15, 0, 1, 3, Qt.AlignHCenter | Qt.AlignBottom)

        self.HMI.unsetCursor()
        self.HMI.TextBox_NomeNovoAtivo.setFocus()

    def CreatePage27(self): # Renomear ativo
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Renomear ativo '+self.HMI.ComboBox_Ativos.currentText())
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Insira o novo nome do ativo:')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font16)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_NovoNomeAtivo = QLineEdit(self.HMI.ComboBox_Ativos.currentText())
        self.HMI.TextBox_NovoNomeAtivo.setAlignment(Qt.AlignCenter)
        self.HMI.TextBox_NovoNomeAtivo.setFont(self.HMI.font18)
        self.HMI.TextBox_NovoNomeAtivo.returnPressed.connect(lambda: self.HMI.CreatePage_Decisao())
        self.HMI.TextBox_NovoNomeAtivo.setFixedWidth(int(self.HMI.frameGeometry().width()/8*0.9))
        completer = QCompleter(self.HMI.DBManager.GetAllTickers())
        self.HMI.TextBox_NovoNomeAtivo.setCompleter(completer)

        self.HMI.Label_Msg2 = QLabel('Insira o tipo do ativo:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.ComboBox_TipoDeAtivo = QComboBox()
        self.HMI.ComboBox_TipoDeAtivo.setEditable(True)
        self.HMI.ComboBox_TipoDeAtivo.setFont(self.HMI.font16)
        self.HMI.ComboBox_TipoDeAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_TipoDeAtivo.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255); border: none")
        self.HMI.ComboBox_TipoDeAtivo.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        tipodeativo = self.HMI.DBManager.GetTipoDeAtivoDeAtivo(self.HMI.ComboBox_Ativos.currentText())
        for idx, Tipo in enumerate(self.HMI.DBManager.GetTiposDeAtivo()):
            self.HMI.ComboBox_TipoDeAtivo.addItem(Tipo)
            try:
                if Tipo == tipodeativo: self.HMI.idxTipoDeAtivo = idx
            except: pass
        if self.HMI.idxTipoDeAtivo < len(self.HMI.DBManager.GetTiposDeAtivo()):
            self.HMI.ComboBox_TipoDeAtivo.setCurrentIndex(self.HMI.idxTipoDeAtivo)
        line_edit = self.HMI.ComboBox_TipoDeAtivo.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)

        self.HMI.Label_Msg3 = QLabel('Insira o sub-tipo do ativo:')
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font16)
        self.HMI.Label_Msg3.setAlignment(Qt.AlignCenter)

        self.HMI.ComboBox_SubtipoDeAtivo = QComboBox()
        self.HMI.ComboBox_SubtipoDeAtivo.setEditable(True)
        self.HMI.ComboBox_SubtipoDeAtivo.setFont(self.HMI.font16)
        self.HMI.ComboBox_SubtipoDeAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_SubtipoDeAtivo.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255); border: none")
        subtipodeativo = self.HMI.DBManager.GetSubtipoDeAtivoDeAtivo(self.HMI.ComboBox_Ativos.currentText())
        for idx, SubTipo in enumerate(self.HMI.DBManager.GetSubtiposDeAtivo()):
            self.HMI.ComboBox_SubtipoDeAtivo.addItem(SubTipo)
            try:
                if SubTipo == subtipodeativo: self.HMI.idxSubtipoDeAtivo = idx
            except: pass
        if self.HMI.idxSubtipoDeAtivo < len(self.HMI.DBManager.GetSubtiposDeAtivo()):
            self.HMI.ComboBox_SubtipoDeAtivo.setCurrentIndex(self.HMI.idxSubtipoDeAtivo)
        line_edit = self.HMI.ComboBox_SubtipoDeAtivo.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)

        self.HMI.Label_Msg4 = QLabel('Insira o setor do ativo:')
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font16)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignCenter)

        self.HMI.ComboBox_SetorAtivo = QComboBox()
        self.HMI.ComboBox_SetorAtivo.setEditable(True)
        self.HMI.ComboBox_SetorAtivo.setFont(self.HMI.font16)
        self.HMI.ComboBox_SetorAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_SetorAtivo.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255); border: none")
        setorativo = self.HMI.DBManager.GetSetorDeAtivo(self.HMI.ComboBox_Ativos.currentText())
        for idx, Setor in enumerate(self.HMI.DBManager.GetSetoresDeAtivo()):
            self.HMI.ComboBox_SetorAtivo.addItem(Setor)
            try:
                if Setor == setorativo: self.HMI.idxSetorAtivo = idx
            except: pass
        if self.HMI.idxSetorAtivo < len(self.HMI.DBManager.GetSetoresDeAtivo()):
            self.HMI.ComboBox_SetorAtivo.setCurrentIndex(self.HMI.idxSetorAtivo)
        line_edit = self.HMI.ComboBox_SetorAtivo.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)

        self.HMI.Button_AddSetorAtivo = QPushButton()
        self.HMI.Button_AddSetorAtivo.pressed.connect(lambda: self.HMI.CreatePage('33'))
        self.HMI.Button_AddSetorAtivo.setFixedSize(40,40)
        self.HMI.Button_AddSetorAtivo.setIconSize(QSize(35, 35))
        self.HMI.Button_AddSetorAtivo.setIcon(QIcon("./images/update.png"))
        self.HMI.Button_AddSetorAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AddSetorAtivo.setToolTip("Adicionar setor de ativo")
        self.HMI.Button_AddSetorAtivo.setStyleSheet("QToolTip {background-color: black; color: white;border: black solid 1px}")

        self.HMI.Button_Seguinte = QPushButton('Seguinte')
        self.HMI.Button_Seguinte.pressed.connect(lambda: self.HMI.CreatePage_Decisao())
        self.HMI.Button_Seguinte.setFont(self.HMI.font16)
        self.HMI.Button_Seguinte.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Seguinte.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Seguinte.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_Seguinte.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Seguinte.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Label_Msg5 = QLabel('A etapa a seguir pode levar alguns minutos...')
        self.HMI.Label_Msg5.setStyleSheet('color: white')
        self.HMI.Label_Msg5.setFont(self.HMI.font12)
        self.HMI.Label_Msg5.setAlignment(Qt.AlignCenter)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 19, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 4, 0, 1, 3, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_NovoNomeAtivo, 5, 0, 1, 3, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 6, 0, 1, 3, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_TipoDeAtivo, 7, 1, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 8, 0, 1, 3, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_SubtipoDeAtivo, 9, 1, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 10, 0, 1, 3, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_SetorAtivo, 11, 1, 1, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AddSetorAtivo, 11, 2, 1, 1, Qt.AlignLeft | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Seguinte, 13, 0, 2, 3, Qt.AlignHCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 15, 0, 1, 3, Qt.AlignHCenter | Qt.AlignBottom)

        self.HMI.unsetCursor()
        self.HMI.TextBox_NovoNomeAtivo.setFocus()

    def CreatePage28(self): # Informar nova operação
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

        self.HMI.Label_Msg1 = QLabel('Adicionar nova operação da '+self.HMI.ComboBox_Ativos.currentText())
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font24)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg9 = QLabel('Modo da cotação:')
        self.HMI.Label_Msg9.setStyleSheet('color: white')
        self.HMI.Label_Msg9.setFont(self.HMI.font14)
        self.HMI.Label_Msg9.setAlignment(Qt.AlignRight)

        Modo = self.HMI.DBManager.GetModoCotacao()
        self.HMI.TextBox_Modo = QLineEdit(Modo)
        self.HMI.TextBox_Modo.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Modo.setStyleSheet("background-color: black; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Modo.setFont(self.HMI.font14)
        self.HMI.TextBox_Modo.setEnabled(False)

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
        self.HMI.Button_Compra.pressed.connect(lambda: self.OnButtonPressed('Compra'))
        self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Compra.setFont(self.HMI.font20)
        self.HMI.Button_Compra.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.TipoDeOperacao = "Compra"

        self.HMI.Button_Venda = QPushButton('venda')
        self.HMI.Button_Venda.pressed.connect(lambda: self.OnButtonPressed('Venda'))
        self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Venda.setFont(self.HMI.font16)
        self.HMI.Button_Venda.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Desdobramento = QPushButton('Desdobramento')
        self.HMI.Button_Desdobramento.pressed.connect(lambda: self.OnButtonPressed('Desdobramento'))
        self.HMI.Button_Desdobramento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Desdobramento.setFont(self.HMI.font16)
        self.HMI.Button_Desdobramento.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Grupamento = QPushButton('Grupamento')
        self.HMI.Button_Grupamento.pressed.connect(lambda: self.OnButtonPressed('Grupamento'))
        self.HMI.Button_Grupamento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Grupamento.setFont(self.HMI.font16)
        self.HMI.Button_Grupamento.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Button_Bonificacao = QPushButton('Bonificação')
        self.HMI.Button_Bonificacao.pressed.connect(lambda: self.OnButtonPressed('Bonificação'))
        self.HMI.Button_Bonificacao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Bonificacao.setFont(self.HMI.font16)
        self.HMI.Button_Bonificacao.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Label_Msg4 = QLabel('Quantidade:')
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font14)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Qqt = QLineEdit()
        self.HMI.TextBox_Qqt.setValidator(QIntValidator())
        self.HMI.TextBox_Qqt.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Qqt.setFont(self.HMI.font14)
        self.HMI.TextBox_Qqt.returnPressed.connect(lambda: self.HMI.CreatePage('28'))

        self.HMI.Label_Msg5 = QLabel('Preço:')
        self.HMI.Label_Msg5.setStyleSheet('color: white')
        self.HMI.Label_Msg5.setFont(self.HMI.font14)
        self.HMI.Label_Msg5.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Preco = QLineEdit()
        self.HMI.TextBox_Preco.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_Preco.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Preco.setFont(self.HMI.font14)
        self.HMI.TextBox_Preco.returnPressed.connect(lambda: self.HMI.CreatePage('28'))

        self.HMI.Label_Msg6 = QLabel('Corretagem:')
        self.HMI.Label_Msg6.setStyleSheet('color: white')
        self.HMI.Label_Msg6.setFont(self.HMI.font14)
        self.HMI.Label_Msg6.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Corretagem = QLineEdit()
        self.HMI.TextBox_Corretagem.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_Corretagem.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Corretagem.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Corretagem.setFont(self.HMI.font14)
        self.HMI.TextBox_Corretagem.returnPressed.connect(lambda: self.HMI.CreatePage('28'))

        self.HMI.Label_Msg7 = QLabel('Taxa B3:')
        self.HMI.Label_Msg7.setStyleSheet('color: white')
        self.HMI.Label_Msg7.setFont(self.HMI.font14)
        self.HMI.Label_Msg7.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_TaxaB3 = QLineEdit(self.HMI.DBManager.GetTaxaB3Per())
        self.HMI.TextBox_TaxaB3.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_TaxaB3.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_TaxaB3.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_TaxaB3.setFont(self.HMI.font14)
        self.HMI.TextBox_TaxaB3.returnPressed.connect(lambda: self.HMI.CreatePage('28'))

        self.HMI.Label_Msg8 = QLabel('Observação:')
        self.HMI.Label_Msg8.setStyleSheet('color: white')
        self.HMI.Label_Msg8.setFont(self.HMI.font14)
        self.HMI.Label_Msg8.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Obs = QLineEdit()
        self.HMI.TextBox_Obs.setFixedWidth(int(self.HMI.frameGeometry().width()*4/7*0.9))
        self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Obs.setFont(self.HMI.font14)
        self.HMI.TextBox_Obs.returnPressed.connect(lambda: self.HMI.CreatePage('28'))

        self.HMI.Button_LimparCampos = QPushButton('Limpar\ncampos')
        self.HMI.Button_LimparCampos.pressed.connect(lambda: self.HMI.LimparPage())
        self.HMI.Button_LimparCampos.setFont(self.HMI.font16)
        self.HMI.Button_LimparCampos.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_LimparCampos.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_LimparCampos.setStyleSheet("background-color: rgb(100, 100, 100)")

        self.HMI.Button_RegistrarOperacao = QPushButton('Registrar\noperação')
        self.HMI.Button_RegistrarOperacao.pressed.connect(lambda: self.HMI.CreatePage('28'))
        self.HMI.Button_RegistrarOperacao.setFont(self.HMI.font16)
        self.HMI.Button_RegistrarOperacao.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_RegistrarOperacao.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_RegistrarOperacao.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_RegistrarOperacao.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_RegistrarOperacao.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Button_Info2 = QPushButton()
        self.HMI.Button_Info2.pressed.connect(lambda: self.HMI.CreatePage('Info2'))
        self.HMI.Button_Info2.setFixedSize(40,40)
        self.HMI.Button_Info2.setIconSize(QSize(35, 35))
        self.HMI.Button_Info2.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info2.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info2.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info3 = QPushButton()
        self.HMI.Button_Info3.pressed.connect(lambda: self.HMI.CreatePage('Info3'))
        self.HMI.Button_Info3.setFixedSize(40,40)
        self.HMI.Button_Info3.setIconSize(QSize(35, 35))
        self.HMI.Button_Info3.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info3.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info3.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info4 = QPushButton()
        self.HMI.Button_Info4.pressed.connect(lambda: self.HMI.CreatePage('Info4'))
        self.HMI.Button_Info4.setFixedSize(40,40)
        self.HMI.Button_Info4.setIconSize(QSize(35, 35))
        self.HMI.Button_Info4.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info4.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info4.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info5 = QPushButton()
        self.HMI.Button_Info5.pressed.connect(lambda: self.HMI.CreatePage('Info5'))
        self.HMI.Button_Info5.setFixedSize(40,40)
        self.HMI.Button_Info5.setIconSize(QSize(35, 35))
        self.HMI.Button_Info5.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info5.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info5.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info6 = QPushButton()
        self.HMI.Button_Info6.pressed.connect(lambda: self.HMI.CreatePage('Info6'))
        self.HMI.Button_Info6.setFixedSize(40,40)
        self.HMI.Button_Info6.setIconSize(QSize(35, 35))
        self.HMI.Button_Info6.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info6.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info6.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info7 = QPushButton()
        self.HMI.Button_Info7.pressed.connect(lambda: self.HMI.CreatePage('Info7'))
        self.HMI.Button_Info7.setFixedSize(40,40)
        self.HMI.Button_Info7.setIconSize(QSize(35, 35))
        self.HMI.Button_Info7.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info7.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info7.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info8 = QPushButton()
        self.HMI.Button_Info8.pressed.connect(lambda: self.HMI.CreatePage('Info8'))
        self.HMI.Button_Info8.setFixedSize(40,40)
        self.HMI.Button_Info8.setIconSize(QSize(35, 35))
        self.HMI.Button_Info8.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info8.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info8.setIcon(QIcon("./images/Info.png"))

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 7)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 11, 7)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 7, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 2, 0, 1, 7, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg9, 4, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Modo, 4, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 5, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Data
        self.HMI.HBoxLayout_Data = QHBoxLayout()
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Calendario, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Relogio, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Info3, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Data, 5, 1, 1, 7, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 6, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_Tipo = QHBoxLayout()
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Compra)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Venda)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Desdobramento)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Grupamento)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Bonificacao)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Info2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Tipo, 6, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 7, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_Qqt = QHBoxLayout()
        self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.TextBox_Qqt)
        self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.Button_Info4)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Qqt, 7, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 8, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_Preco = QHBoxLayout()
        self.HMI.HBoxLayout_Preco.addWidget(self.HMI.TextBox_Preco)
        self.HMI.HBoxLayout_Preco.addWidget(self.HMI.Button_Info5)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Preco, 8, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg6, 9, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_Corretagem = QHBoxLayout()
        self.HMI.HBoxLayout_Corretagem.addWidget(self.HMI.TextBox_Corretagem)
        self.HMI.HBoxLayout_Corretagem.addWidget(self.HMI.Button_Info6)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Corretagem, 9, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg7, 10, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_TaxaB3 = QHBoxLayout()
        self.HMI.HBoxLayout_TaxaB3.addWidget(self.HMI.TextBox_TaxaB3)
        self.HMI.HBoxLayout_TaxaB3.addWidget(self.HMI.Button_Info7)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_TaxaB3, 10, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg8, 11, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_Obs = QHBoxLayout()
        self.HMI.HBoxLayout_Obs.addWidget(self.HMI.TextBox_Obs)
        self.HMI.HBoxLayout_Obs.addWidget(self.HMI.Button_Info8)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Obs, 11, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_LimparCampos, 7, 5, 2, 2, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RegistrarOperacao, 9, 5, 2, 2, Qt.AlignVCenter | Qt.AlignRight)

        self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
        self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Qqt)
        self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
        self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Corretagem)
        self.HMI.setTabOrder(self.HMI.TextBox_Corretagem,self.HMI.TextBox_TaxaB3)
        self.HMI.setTabOrder(self.HMI.TextBox_TaxaB3,self.HMI.TextBox_Obs)
        self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
        self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
        self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
        self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info2)
        self.HMI.setTabOrder(self.HMI.Button_Info2,self.HMI.Button_Info4)
        self.HMI.setTabOrder(self.HMI.Button_Info4,self.HMI.Button_Info5)
        self.HMI.setTabOrder(self.HMI.Button_Info5,self.HMI.Button_Info6)
        self.HMI.setTabOrder(self.HMI.Button_Info6,self.HMI.Button_Info7)
        self.HMI.setTabOrder(self.HMI.Button_Info7,self.HMI.Button_Info8)

        self.HMI.TextBox_Qqt.setFocus()

    def CreatePage29(self): # Alterar operações
        self.item += 1

        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        black = "rgb(0,0,0)"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Alterar operações da '+self.HMI.ComboBox_Ativos.currentText()+' na '+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.Operacoes=[]
        for idx in self.HMI.Table_Operacoes_Realizadas_com_Ativo.selectedIndexes():
            self.Operacoes.append(idx.row())
        self.Operacoes = list(dict.fromkeys(self.Operacoes))

        if len(self.Operacoes) > 0:

            self.HMI.Label_Msg1 = QLabel('Alteração na operação '+str(self.item+1)+' de '+str(len(self.Operacoes)))
            self.HMI.Label_Msg1.setStyleSheet('color: white')
            self.HMI.Label_Msg1.setFont(self.HMI.font24)
            self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

            self.HMI.Table_Operacoes_SelecionadasHeader = QTableWidget()
            self.HMI.Table_Operacoes_Selecionadas = QTableWidget()

            self.CreateTable_29_1() # Table_Operacoes_SelecionadasHeader
            self.CreateTable_29_2() # Table_Operacoes_Selecionadas (Mostra apenas o item selecionado)

            self.HMI.Label_Msg9 = QLabel('Modo da cotação:')
            self.HMI.Label_Msg9.setStyleSheet('color: white')
            self.HMI.Label_Msg9.setFont(self.HMI.font14)
            self.HMI.Label_Msg9.setAlignment(Qt.AlignRight)

            Modo = self.HMI.DBManager.GetModoCotacao()
            self.HMI.TextBox_Modo = QLineEdit(Modo)
            self.HMI.TextBox_Modo.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Modo.setStyleSheet("background-color: black; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Modo.setFont(self.HMI.font14)
            self.HMI.TextBox_Modo.setEnabled(False)

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
            self.HMI.Button_Compra.pressed.connect(lambda: self.OnButtonPressed('Compra'))
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setFont(self.HMI.font20)
            self.HMI.Button_Compra.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.TipoDeOperacao = "Compra"

            self.HMI.Button_Venda = QPushButton('venda')
            self.HMI.Button_Venda.pressed.connect(lambda: self.OnButtonPressed('Venda'))
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Button_Desdobramento = QPushButton('Desdobramento')
            self.HMI.Button_Desdobramento.pressed.connect(lambda: self.OnButtonPressed('Desdobramento'))
            self.HMI.Button_Desdobramento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Desdobramento.setFont(self.HMI.font16)
            self.HMI.Button_Desdobramento.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Button_Grupamento = QPushButton('Grupamento')
            self.HMI.Button_Grupamento.pressed.connect(lambda: self.OnButtonPressed('Grupamento'))
            self.HMI.Button_Grupamento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Grupamento.setFont(self.HMI.font16)
            self.HMI.Button_Grupamento.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Button_Bonificacao = QPushButton('Bonificação')
            self.HMI.Button_Bonificacao.pressed.connect(lambda: self.OnButtonPressed('Bonificação'))
            self.HMI.Button_Bonificacao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Bonificacao.setFont(self.HMI.font16)
            self.HMI.Button_Bonificacao.setCursor(QCursor(Qt.PointingHandCursor))

            self.HMI.Label_Msg4 = QLabel('Quantidade:')
            self.HMI.Label_Msg4.setStyleSheet('color: white')
            self.HMI.Label_Msg4.setFont(self.HMI.font14)
            self.HMI.Label_Msg4.setAlignment(Qt.AlignRight)

            self.HMI.TextBox_Qqt = QLineEdit()
            self.HMI.TextBox_Qqt.setValidator(QIntValidator())
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

            self.HMI.Label_Msg6 = QLabel('Corretagem:')
            self.HMI.Label_Msg6.setStyleSheet('color: white')
            self.HMI.Label_Msg6.setFont(self.HMI.font14)
            self.HMI.Label_Msg6.setAlignment(Qt.AlignRight)

            self.HMI.TextBox_Corretagem = QLineEdit()
            self.HMI.TextBox_Corretagem.setValidator(QDoubleValidator(0.99,99.99,2))
            self.HMI.TextBox_Corretagem.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Corretagem.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Corretagem.setFont(self.HMI.font14)

            self.HMI.Label_Msg7 = QLabel('Taxa B3:')
            self.HMI.Label_Msg7.setStyleSheet('color: white')
            self.HMI.Label_Msg7.setFont(self.HMI.font14)
            self.HMI.Label_Msg7.setAlignment(Qt.AlignRight)

            self.HMI.TextBox_TaxaB3 = QLineEdit()
            self.HMI.TextBox_TaxaB3.setValidator(QDoubleValidator(0.99,99.99,2))
            self.HMI.TextBox_TaxaB3.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_TaxaB3.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_TaxaB3.setFont(self.HMI.font14)

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
            self.HMI.Button_RegistrarOperacao.pressed.connect(lambda: self.OnButtonPressed('Page29_Next'))
            self.HMI.Button_RegistrarOperacao.setFont(self.HMI.font16)
            self.HMI.Button_RegistrarOperacao.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
            self.HMI.Button_RegistrarOperacao.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
            self.HMI.Button_RegistrarOperacao.setIcon(QIcon("./images/log_in.png"))
            self.HMI.Button_RegistrarOperacao.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_RegistrarOperacao.setStyleSheet("background-color: rgb(20, 120, 30)")

            self.HMI.Button_Info2 = QPushButton()
            self.HMI.Button_Info2.pressed.connect(lambda: self.HMI.CreatePage('Info2'))
            self.HMI.Button_Info2.setFixedSize(40,40)
            self.HMI.Button_Info2.setIconSize(QSize(35, 35))
            self.HMI.Button_Info2.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info2.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info2.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info3 = QPushButton()
            self.HMI.Button_Info3.pressed.connect(lambda: self.HMI.CreatePage('Info3'))
            self.HMI.Button_Info3.setFixedSize(40,40)
            self.HMI.Button_Info3.setIconSize(QSize(35, 35))
            self.HMI.Button_Info3.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info3.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info3.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info4 = QPushButton()
            self.HMI.Button_Info4.pressed.connect(lambda: self.HMI.CreatePage('Info4'))
            self.HMI.Button_Info4.setFixedSize(40,40)
            self.HMI.Button_Info4.setIconSize(QSize(35, 35))
            self.HMI.Button_Info4.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info4.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info4.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info5 = QPushButton()
            self.HMI.Button_Info5.pressed.connect(lambda: self.HMI.CreatePage('Info5'))
            self.HMI.Button_Info5.setFixedSize(40,40)
            self.HMI.Button_Info5.setIconSize(QSize(35, 35))
            self.HMI.Button_Info5.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info5.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info5.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info6 = QPushButton()
            self.HMI.Button_Info6.pressed.connect(lambda: self.HMI.CreatePage('Info6'))
            self.HMI.Button_Info6.setFixedSize(40,40)
            self.HMI.Button_Info6.setIconSize(QSize(35, 35))
            self.HMI.Button_Info6.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info6.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info6.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info7 = QPushButton()
            self.HMI.Button_Info7.pressed.connect(lambda: self.HMI.CreatePage('Info7'))
            self.HMI.Button_Info7.setFixedSize(40,40)
            self.HMI.Button_Info7.setIconSize(QSize(35, 35))
            self.HMI.Button_Info7.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info7.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info7.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info8 = QPushButton()
            self.HMI.Button_Info8.pressed.connect(lambda: self.HMI.CreatePage('Info8'))
            self.HMI.Button_Info8.setFixedSize(40,40)
            self.HMI.Button_Info8.setIconSize(QSize(35, 35))
            self.HMI.Button_Info8.setCursor(QCursor(Qt.PointingHandCursor))
            self.HMI.Button_Info8.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info8.setIcon(QIcon("./images/Info.png"))

            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 10)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 11, 10)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 10, Qt.AlignCenter)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 1, 10, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_SelecionadasHeader, 2, 0, 1, 10, Qt.AlignHCenter | Qt.AlignBottom)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Selecionadas, 3, 0, 1, 10, Qt.AlignHCenter | Qt.AlignTop)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg9, 4, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Modo, 4, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 5, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Data
            self.HMI.HBoxLayout_Data = QHBoxLayout()
            self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Calendario, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Relogio, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Info3, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Data, 5, 1, 1, 7, Qt.AlignVCenter | Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 6, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
            self.HMI.HBoxLayout_Tipo = QHBoxLayout()
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Compra)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Venda)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Desdobramento)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Grupamento)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Bonificacao)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Info2)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Tipo, 6, 1, 1, 1, Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 7, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
            self.HMI.HBoxLayout_Qqt = QHBoxLayout()
            self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.TextBox_Qqt)
            self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.Button_Info4)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Qqt, 7, 1, 1, 1, Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 8, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
            self.HMI.HBoxLayout_Preco = QHBoxLayout()
            self.HMI.HBoxLayout_Preco.addWidget(self.HMI.TextBox_Preco)
            self.HMI.HBoxLayout_Preco.addWidget(self.HMI.Button_Info5)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Preco, 8, 1, 1, 1, Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg6, 9, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
            self.HMI.HBoxLayout_Corretagem = QHBoxLayout()
            self.HMI.HBoxLayout_Corretagem.addWidget(self.HMI.TextBox_Corretagem)
            self.HMI.HBoxLayout_Corretagem.addWidget(self.HMI.Button_Info6)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Corretagem, 9, 1, 1, 1, Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg7, 10, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
            self.HMI.HBoxLayout_TaxaB3 = QHBoxLayout()
            self.HMI.HBoxLayout_TaxaB3.addWidget(self.HMI.TextBox_TaxaB3)
            self.HMI.HBoxLayout_TaxaB3.addWidget(self.HMI.Button_Info7)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_TaxaB3, 10, 1, 1, 1, Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg8, 11, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
            self.HMI.HBoxLayout_Obs = QHBoxLayout()
            self.HMI.HBoxLayout_Obs.addWidget(self.HMI.TextBox_Obs)
            self.HMI.HBoxLayout_Obs.addWidget(self.HMI.Button_Info8)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Obs, 11, 1, 1, 1, Qt.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_LimparCampos, 7, 8, 2, 2, Qt.AlignVCenter | Qt.AlignRight)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RegistrarOperacao, 9, 8, 2, 2, Qt.AlignVCenter | Qt.AlignRight)

            # Completar os textBoxes
            for i, item in enumerate(self.data_23_1):
                if i == self.Operacoes[self.item]:
                    data = str(item[0])
                    data = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
                    ano = str(data.year)
                    mes = str(data.month)
                    dia = str(data.day)
                    if data.hour < 10:
                        hora = "0"+str(data.hour)
                    else:
                        hora = str(data.hour)
                    if data.minute < 10:
                        minuto = "0"+str(data.minute)
                    else:
                        minuto = str(data.minute)
                    if data.second < 10:
                        segundo = "0"+str(data.second)
                    else:
                        segundo = str(data.second)
                    Tipo = str(item[1])
                    Qqt = str(item[2])
                    Preco = str(item[3])
                    Corretagem = str(item[4])
                    TaxaB3Per= str(item[5])+"%"
                    TaxaB3 = str(item[6])
                    Obs = str(item[7])
            self.HMI.Button_Calendario.setText(ano+"/"+mes+"/"+dia)
            self.HMI.Button_Relogio.setText(hora+":"+minuto+":"+segundo)
            self.HMI.Selecao_Ano = ano
            self.HMI.Selecao_Mes = mes
            self.HMI.Selecao_Dia = dia
            self.HMI.Selecao_Hora = hora
            self.HMI.Selecao_Minuto = minuto
            self.HMI.Selecao_Segundo = segundo
            if Tipo == "Compra": self.OnButtonPressed('Compra')
            else: self.OnButtonPressed('Venda')
            self.HMI.TextBox_Qqt.setText(Qqt)
            self.HMI.TextBox_Preco.setText(Preco)
            self.HMI.TextBox_Corretagem.setText(Corretagem)
            self.HMI.TextBox_TaxaB3.setText(TaxaB3Per)
            self.HMI.TextBox_Obs.setText(Obs)

            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Qqt)
            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Corretagem)
            self.HMI.setTabOrder(self.HMI.TextBox_Corretagem,self.HMI.TextBox_TaxaB3)
            self.HMI.setTabOrder(self.HMI.TextBox_TaxaB3,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info2)
            self.HMI.setTabOrder(self.HMI.Button_Info2,self.HMI.Button_Info4)
            self.HMI.setTabOrder(self.HMI.Button_Info4,self.HMI.Button_Info5)
            self.HMI.setTabOrder(self.HMI.Button_Info5,self.HMI.Button_Info6)
            self.HMI.setTabOrder(self.HMI.Button_Info6,self.HMI.Button_Info7)
            self.HMI.setTabOrder(self.HMI.Button_Info7,self.HMI.Button_Info8)

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

    def CreatePage30(self): # Deletar operações
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Deletar operações da '+self.HMI.ComboBox_Ativos.currentText()+' na '+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Operações selecionadas para serem deletadas:')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font24)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.Operacoes = [] # Será usada para fazer a tabela dessa pagina, com apenas os itens selecionados
        for idx in self.HMI.Table_Operacoes_Realizadas_com_Ativo.selectedIndexes():
            self.Operacoes.append(idx.row())
        self.Operacoes = list(dict.fromkeys(self.Operacoes))

        self.HMI.Button_Cancelar = QPushButton('Cancelar')
        self.HMI.Button_Cancelar.pressed.connect(lambda: self.HMI.CreatePage('23'))
        self.HMI.Button_Cancelar.setFont(self.HMI.font16)
        self.HMI.Button_Cancelar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Cancelar.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_Cancelar.setIcon(QIcon("./images/Voltar.png"))
        self.HMI.Button_Cancelar.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Cancelar.setStyleSheet("background-color: rgb(200, 100, 100)")

        self.HMI.Button_DeletarOperacoes = QPushButton('Deletar\noperações')
        self.HMI.Button_DeletarOperacoes.pressed.connect(lambda: self.OnButtonPressed('Deletar Ativos da Pagina 23'))
        self.HMI.Button_DeletarOperacoes.setFont(self.HMI.font16)
        self.HMI.Button_DeletarOperacoes.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_DeletarOperacoes.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_DeletarOperacoes.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_DeletarOperacoes.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_DeletarOperacoes.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader = QTableWidget()
        self.HMI.Table_Operacoes_Realizadas_com_Ativo = QTableWidget()

        self.CreateTable_30_1() # Table_Operacoes_Realizadas_com_AtivoHeader
        self.CreateTable_30_2() # Table_Operacoes_Realizadas_com_Ativo (Mostra apenas os itens selecionados)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 13, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 10, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 2, 0, 1, 10, Qt.AlignLeft | Qt.AlignVCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader, 3, 0, 1, 10, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas_com_Ativo, 4, 0, 6, 10, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Cancelar, 12, 0, 1, 6, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DeletarOperacoes, 12, 5, 1, 6, Qt.AlignCenter)

    def CreatePage34a(self): # "Cotação do ativo '"+self.HMI.TextBox_NomeNovoAtivo.text()+"' foi encontrada online"
        black = 'rgb(0, 0, 0)'
        green = 'rgb(10, 15, 10)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.CotacaoNovoAtivo = self.HMI.Cache_Cotacao

        self.HMI.Label_Titulo = QLabel("Cotação do ativo '"+self.HMI.TextBox_NomeNovoAtivo.text()+"' foi encontrada online.")
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font24)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel("A cotação correspondente encontrada\nautomaticamente está em torno de\n"+self.HMI.DBManager.GetUserCoinCurrency()+str(self.HMI.CotacaoNovoAtivo)+'.')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font24)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg2 = QLabel("A cotação encontrada está correta?")
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font24)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.Button_Voltar = QPushButton('Não. Voltar,\nrenomear ativo e\ntentar novamente.')
        self.HMI.Button_Voltar.pressed.connect(lambda: self.HMI.CreatePage('26'))
        self.HMI.Button_Voltar.setFont(self.HMI.font16)
        self.HMI.Button_Voltar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Voltar.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Voltar.setIcon(QIcon("./images/Voltar.png"))
        self.HMI.Button_Voltar.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Voltar.setStyleSheet("background-color: rgb(120, 20, 30)")

        self.HMI.Button_AtivarModoManual = QPushButton('Não, mas continue\ne ative o modo manual.')
        self.HMI.Button_AtivarModoManual.pressed.connect(lambda: self.HMI.CreatePage('36a_Manual'))
        self.HMI.Button_AtivarModoManual.setFont(self.HMI.font16)
        self.HMI.Button_AtivarModoManual.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_AtivarModoManual.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_AtivarModoManual.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_AtivarModoManual.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AtivarModoManual.setStyleSheet("background-color: rgb(120, 120, 30)")

        self.HMI.Button_Seguinte = QPushButton('Sim, está correto!')
        self.HMI.Button_Seguinte.pressed.connect(lambda: self.HMI.CreatePage('36a_Auto'))
        self.HMI.Button_Seguinte.setFont(self.HMI.font16)
        self.HMI.Button_Seguinte.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Seguinte.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Seguinte.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_Seguinte.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Seguinte.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Button_Info1 = QPushButton('O que é modo manual?')
        self.HMI.Button_Info1.pressed.connect(lambda: self.HMI.CreatePage('Info1'))
        self.HMI.Button_Info1.setFont(self.HMI.font16)
        self.HMI.Button_Info1.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Info1.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Info1.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info1.setStyleSheet("background-color: rgb(100, 100, 100)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 4, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 2, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Voltar, 3, 0, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AtivarModoManual, 3, 1, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Seguinte, 3, 2, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Info1, 4, 1, 1, 1, Qt.AlignCenter)

    def CreatePage35a(self): # "Cotação do ativo '"+self.HMI.TextBox_NomeNovoAtivo.text()+"'\nnão foi encontrada online."
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel("Cotação do ativo '"+self.HMI.TextBox_NomeNovoAtivo.text()+"'\nnão foi encontrada online.")
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font24)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel("Verifique a sua conexão com a internet\nou tente voltar e renomear o ativo.\nSe preferir, ative o modo manual e\ninsira a cotação desse ativo manualmente\nquando solicitado futuramente.")
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font22)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.Button_Voltar = QPushButton('Voltar,\nrenomear ativo e\ntentar novamente.')
        self.HMI.Button_Voltar.pressed.connect(lambda: self.HMI.CreatePage('26'))
        self.HMI.Button_Voltar.setFont(self.HMI.font16)
        self.HMI.Button_Voltar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Voltar.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Voltar.setIcon(QIcon("./images/Voltar.png"))
        self.HMI.Button_Voltar.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Voltar.setStyleSheet("background-color: rgb(120, 20, 30)")

        self.HMI.Button_AtivarModoManual = QPushButton('Ative o modo manual\npara esse ativo.')
        self.HMI.Button_AtivarModoManual.pressed.connect(lambda: self.HMI.CreatePage('36b_Manual'))
        self.HMI.Button_AtivarModoManual.setFont(self.HMI.font16)
        self.HMI.Button_AtivarModoManual.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_AtivarModoManual.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_AtivarModoManual.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_AtivarModoManual.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AtivarModoManual.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Button_Info1 = QPushButton('O que é modo manual?')
        self.HMI.Button_Info1.pressed.connect(lambda: self.HMI.CreatePage('Info1'))
        self.HMI.Button_Info1.setFont(self.HMI.font16)
        self.HMI.Button_Info1.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Info1.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Info1.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info1.setStyleSheet("background-color: rgb(100, 100, 100)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 3, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Voltar, 2, 0, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AtivarModoManual, 2, 2, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Info1, 3, 2, 1, 1, Qt.AlignCenter)

        self.HMI.unsetCursor()

    def CreatePage36a(self): # Informar nova operação
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

        self.HMI.Label_Msg1 = QLabel('Adicionar nova operação da '+self.HMI.TextBox_NomeNovoAtivo.text())
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font24)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg9 = QLabel('Modo da cotação:')
        self.HMI.Label_Msg9.setStyleSheet('color: white')
        self.HMI.Label_Msg9.setFont(self.HMI.font14)
        self.HMI.Label_Msg9.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Modo = QLineEdit("Manual" if self.HMI.ModoManualAtivo else "Automático")
        self.HMI.TextBox_Modo.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Modo.setStyleSheet("background-color: black; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Modo.setFont(self.HMI.font14)
        self.HMI.TextBox_Modo.setEnabled(False)

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
        self.HMI.Button_Compra.pressed.connect(lambda: self.OnButtonPressed('Compra'))
        self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Compra.setFont(self.HMI.font20)
        self.HMI.Button_Compra.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.TipoDeOperacao = "Compra"

        self.HMI.Button_Venda = QPushButton('Venda')
        self.HMI.Button_Venda.pressed.connect(lambda: self.OnButtonPressed('Venda'))
        self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Venda.setFont(self.HMI.font16)
        self.HMI.Button_Venda.setCursor(QCursor(Qt.PointingHandCursor))

        self.HMI.Label_Msg4 = QLabel('Quantidade:')
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font14)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Qqt = QLineEdit()
        self.HMI.TextBox_Qqt.setValidator(QIntValidator())
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

        self.HMI.Label_Msg6 = QLabel('Corretagem:')
        self.HMI.Label_Msg6.setStyleSheet('color: white')
        self.HMI.Label_Msg6.setFont(self.HMI.font14)
        self.HMI.Label_Msg6.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_Corretagem = QLineEdit()
        self.HMI.TextBox_Corretagem.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_Corretagem.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Corretagem.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Corretagem.setFont(self.HMI.font14)

        self.HMI.Label_Msg7 = QLabel('Taxa B3:')
        self.HMI.Label_Msg7.setStyleSheet('color: white')
        self.HMI.Label_Msg7.setFont(self.HMI.font14)
        self.HMI.Label_Msg7.setAlignment(Qt.AlignRight)

        self.HMI.TextBox_TaxaB3 = QLineEdit(self.HMI.DBManager.GetTaxaB3Per())
        self.HMI.TextBox_TaxaB3.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_TaxaB3.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_TaxaB3.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_TaxaB3.setFont(self.HMI.font14)

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
        self.HMI.Button_RegistrarOperacao.pressed.connect(lambda: self.HMI.CreatePage('28'))
        self.HMI.Button_RegistrarOperacao.setFont(self.HMI.font16)
        self.HMI.Button_RegistrarOperacao.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_RegistrarOperacao.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_RegistrarOperacao.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_RegistrarOperacao.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_RegistrarOperacao.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Button_Info2 = QPushButton()
        self.HMI.Button_Info2.pressed.connect(lambda: self.HMI.CreatePage('Info2'))
        self.HMI.Button_Info2.setFixedSize(40,40)
        self.HMI.Button_Info2.setIconSize(QSize(35, 35))
        self.HMI.Button_Info2.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info2.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info2.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info3 = QPushButton()
        self.HMI.Button_Info3.pressed.connect(lambda: self.HMI.CreatePage('Info3'))
        self.HMI.Button_Info3.setFixedSize(40,40)
        self.HMI.Button_Info3.setIconSize(QSize(35, 35))
        self.HMI.Button_Info3.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info3.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info3.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info4 = QPushButton()
        self.HMI.Button_Info4.pressed.connect(lambda: self.HMI.CreatePage('Info4'))
        self.HMI.Button_Info4.setFixedSize(40,40)
        self.HMI.Button_Info4.setIconSize(QSize(35, 35))
        self.HMI.Button_Info4.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info4.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info4.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info5 = QPushButton()
        self.HMI.Button_Info5.pressed.connect(lambda: self.HMI.CreatePage('Info5'))
        self.HMI.Button_Info5.setFixedSize(40,40)
        self.HMI.Button_Info5.setIconSize(QSize(35, 35))
        self.HMI.Button_Info5.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info5.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info5.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info6 = QPushButton()
        self.HMI.Button_Info6.pressed.connect(lambda: self.HMI.CreatePage('Info6'))
        self.HMI.Button_Info6.setFixedSize(40,40)
        self.HMI.Button_Info6.setIconSize(QSize(35, 35))
        self.HMI.Button_Info6.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info6.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info6.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info7 = QPushButton()
        self.HMI.Button_Info7.pressed.connect(lambda: self.HMI.CreatePage('Info7'))
        self.HMI.Button_Info7.setFixedSize(40,40)
        self.HMI.Button_Info7.setIconSize(QSize(35, 35))
        self.HMI.Button_Info7.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info7.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info7.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info8 = QPushButton()
        self.HMI.Button_Info8.pressed.connect(lambda: self.HMI.CreatePage('Info8'))
        self.HMI.Button_Info8.setFixedSize(40,40)
        self.HMI.Button_Info8.setIconSize(QSize(35, 35))
        self.HMI.Button_Info8.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info8.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info8.setIcon(QIcon("./images/Info.png"))

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 7)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 11, 7)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 7, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 2, 0, 1, 7, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg9, 4, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Modo, 4, 1, 1, 1, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 5, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Data
        self.HMI.HBoxLayout_Data = QHBoxLayout()
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Calendario, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Relogio, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Info3, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Data, 5, 1, 1, 7, Qt.AlignVCenter | Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 6, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_Tipo = QHBoxLayout()
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Compra)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Info2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Tipo, 6, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 7, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_Qqt = QHBoxLayout()
        self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.TextBox_Qqt)
        self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.Button_Info4)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Qqt, 7, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 8, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_Preco = QHBoxLayout()
        self.HMI.HBoxLayout_Preco.addWidget(self.HMI.TextBox_Preco)
        self.HMI.HBoxLayout_Preco.addWidget(self.HMI.Button_Info5)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Preco, 8, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg6, 9, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_Corretagem = QHBoxLayout()
        self.HMI.HBoxLayout_Corretagem.addWidget(self.HMI.TextBox_Corretagem)
        self.HMI.HBoxLayout_Corretagem.addWidget(self.HMI.Button_Info6)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Corretagem, 9, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg7, 10, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_TaxaB3 = QHBoxLayout()
        self.HMI.HBoxLayout_TaxaB3.addWidget(self.HMI.TextBox_TaxaB3)
        self.HMI.HBoxLayout_TaxaB3.addWidget(self.HMI.Button_Info7)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_TaxaB3, 10, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg8, 11, 0, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.HBoxLayout_Obs = QHBoxLayout()
        self.HMI.HBoxLayout_Obs.addWidget(self.HMI.TextBox_Obs)
        self.HMI.HBoxLayout_Obs.addWidget(self.HMI.Button_Info8)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Obs, 11, 1, 1, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_LimparCampos, 7, 5, 2, 2, Qt.AlignVCenter | Qt.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RegistrarOperacao, 9, 5, 2, 2, Qt.AlignVCenter | Qt.AlignRight)

        self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
        self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Qqt)
        self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
        self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Corretagem)
        self.HMI.setTabOrder(self.HMI.TextBox_Corretagem,self.HMI.TextBox_TaxaB3)
        self.HMI.setTabOrder(self.HMI.TextBox_TaxaB3,self.HMI.TextBox_Obs)
        self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
        self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
        self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
        self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info2)
        self.HMI.setTabOrder(self.HMI.Button_Info2,self.HMI.Button_Info4)
        self.HMI.setTabOrder(self.HMI.Button_Info4,self.HMI.Button_Info5)
        self.HMI.setTabOrder(self.HMI.Button_Info5,self.HMI.Button_Info6)
        self.HMI.setTabOrder(self.HMI.Button_Info6,self.HMI.Button_Info7)
        self.HMI.setTabOrder(self.HMI.Button_Info7,self.HMI.Button_Info8)

        self.HMI.TextBox_Qqt.setFocus()

    def CreatePage31b(self): # Adicionar novo tipo de ativo
        black = 'rgb(0, 0, 0)'
        green = 'rgb(10, 15, 10)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)
        Background_3 = QLabel()
        Background_3.setStyleSheet("background-color: "+green)
        Background_4 = QLabel()
        Background_4.setStyleSheet("background-color: "+green)

        self.HMI.Label_Titulo = QLabel('Adicionar novo tipo de ativo')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Sugestão:')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font20)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg2 = QLabel('Ações e Negócios\nReal Estate\nCaixa\nAtivos Internacionais')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font14)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.Label_NovoTipoAtivo = QLabel('Insira o nome do novo tipo de ativo:')
        self.HMI.Label_NovoTipoAtivo.setStyleSheet('color: white')
        self.HMI.Label_NovoTipoAtivo.setFont(self.HMI.font16)
        self.HMI.Label_NovoTipoAtivo.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_NovoTipoAtivo = QLineEdit()
        self.HMI.TextBox_NovoTipoAtivo.returnPressed.connect(lambda: self.HMI.CreatePage('27'))
        self.HMI.TextBox_NovoTipoAtivo.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))

        self.HMI.Button_Seguinte = QPushButton('Seguinte')
        self.HMI.Button_Seguinte.pressed.connect(lambda: self.HMI.CreatePage('27'))
        self.HMI.Button_Seguinte.setFont(self.HMI.font16)
        self.HMI.Button_Seguinte.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Seguinte.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Seguinte.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_Seguinte.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Seguinte.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 4)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 7, 4)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_3, 2, 1, 1, 2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_4, 3, 1, 1, 2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 4, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 2, 1, 1, 2, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 3, 1, 1, 2, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_NovoTipoAtivo, 4, 1, 1, 2, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_NovoTipoAtivo, 5, 1, 1, 2, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Seguinte, 6, 1, 2, 2, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.TextBox_NovoTipoAtivo.setFocus()

    def CreatePage32b(self): # Adicionar novo sub-tipo de ativo
        black = 'rgb(0, 0, 0)'
        green = 'rgb(10, 15, 10)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)
        Background_3 = QLabel()
        Background_3.setStyleSheet("background-color: "+green)
        Background_4 = QLabel()
        Background_4.setStyleSheet("background-color: "+green)
        Background_5 = QLabel()
        Background_5.setStyleSheet("background-color: "+green)
        Background_6 = QLabel()
        Background_6.setStyleSheet("background-color: "+green)
        Background_7 = QLabel()
        Background_7.setStyleSheet("background-color: "+green)

        self.HMI.Label_Titulo = QLabel('Adicionar novo sub-tipo de ativo')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Sugestão:')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font16)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignRight)

        self.HMI.Label_Msg2 = QLabel('Ações e Negócios:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignRight)

        self.HMI.Label_Msg3 = QLabel('Real Estate:')
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font16)
        self.HMI.Label_Msg3.setAlignment(Qt.AlignRight)

        self.HMI.Label_Msg4 = QLabel('Caixa:')
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font16)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignRight)

        self.HMI.Label_Msg5 = QLabel('Ativos Internacionais:')
        self.HMI.Label_Msg5.setStyleSheet('color: white')
        self.HMI.Label_Msg5.setFont(self.HMI.font16)
        self.HMI.Label_Msg5.setAlignment(Qt.AlignRight)

        self.HMI.Label_Msg6 = QLabel('Ações Nacionais\nFundos de investimentos: Ações Nacionais')
        self.HMI.Label_Msg6.setStyleSheet('color: white')
        self.HMI.Label_Msg6.setFont(self.HMI.font12)
        self.HMI.Label_Msg6.setAlignment(Qt.AlignLeft)

        self.HMI.Label_Msg7 = QLabel('Fundos Imobiliários\nFundos de Investimento: Real Estate')
        self.HMI.Label_Msg7.setStyleSheet('color: white')
        self.HMI.Label_Msg7.setFont(self.HMI.font12)
        self.HMI.Label_Msg7.setAlignment(Qt.AlignLeft)

        self.HMI.Label_Msg8 = QLabel('Renda Fixa\nFundos de Investimento: Renda Fixa\nTesouro Direto e Títulos Públicos\nPrevidência Privada\nCOE')
        self.HMI.Label_Msg8.setStyleSheet('color: white')
        self.HMI.Label_Msg8.setFont(self.HMI.font12)
        self.HMI.Label_Msg8.setAlignment(Qt.AlignLeft)

        self.HMI.Label_Msg9 = QLabel('BDR\nFundos de Investimento: Ações Internacionais')
        self.HMI.Label_Msg9.setStyleSheet('color: white')
        self.HMI.Label_Msg9.setFont(self.HMI.font12)
        self.HMI.Label_Msg9.setAlignment(Qt.AlignLeft)

        self.HMI.Label_NovoTipoAtivo = QLabel('Insira o tipo de ativo:')
        self.HMI.Label_NovoTipoAtivo.setStyleSheet('color: white')
        self.HMI.Label_NovoTipoAtivo.setFont(self.HMI.font16)
        self.HMI.Label_NovoTipoAtivo.setAlignment(Qt.AlignCenter)

        self.HMI.ComboBox_TipoDeAtivo = QComboBox()
        self.HMI.ComboBox_TipoDeAtivo.setFont(self.HMI.font16)
        self.HMI.ComboBox_TipoDeAtivo.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_TipoDeAtivo.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        self.HMI.ComboBox_TipoDeAtivo.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        for idx, Tipo in enumerate(self.HMI.DBManager.GetTiposDeAtivo()):
            self.HMI.ComboBox_TipoDeAtivo.addItem(Tipo)
            try:
                if Tipo == self.HMI.TextBox_TipoAtivo.text(): self.HMI.idxTipoDeAtivo = idx
            except: pass
        if self.HMI.idxTipoDeAtivo < len(self.HMI.DBManager.GetTiposDeAtivo()):
            self.HMI.ComboBox_TipoDeAtivo.setCurrentIndex(self.HMI.idxTipoDeAtivo)

        self.HMI.Label_NovoSubtipoAtivo = QLabel('Insira o nome do novo sub-tipo de ativo:')
        self.HMI.Label_NovoSubtipoAtivo.setStyleSheet('color: white')
        self.HMI.Label_NovoSubtipoAtivo.setFont(self.HMI.font16)
        self.HMI.Label_NovoSubtipoAtivo.setAlignment(Qt.AlignCenter)

        self.HMI.TextBox_NovoSubtipoAtivo = QLineEdit()
        self.HMI.TextBox_NovoSubtipoAtivo.returnPressed.connect(lambda: self.HMI.CreatePage('27'))
        self.HMI.TextBox_NovoSubtipoAtivo.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))

        self.HMI.Button_Seguinte = QPushButton('Seguinte')
        self.HMI.Button_Seguinte.pressed.connect(lambda: self.HMI.CreatePage('27'))
        self.HMI.Button_Seguinte.setFont(self.HMI.font16)
        self.HMI.Button_Seguinte.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Seguinte.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Seguinte.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_Seguinte.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Seguinte.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 4)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 13, 4)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_3, 3, 1, 1, 2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_4, 4, 1, 1, 2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_5, 5, 1, 1, 2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_6, 6, 1, 1, 2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_7, 2, 1, 1, 2)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 4, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 2, 1, 1, 2, Qt.AlignCenter) # Sugestão:
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 3, 1, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Ações e Negócios
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 4, 1, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Real Estate
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 5, 1, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Caixa
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 6, 1, 1, 1, Qt.AlignVCenter | Qt.AlignRight) # Ativos Internacionais
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg6, 3, 2, 1, 1, Qt.AlignTop | Qt.AlignLeft) # Ações Nacionais\nFundos de investimentos: Ações Nacionais
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg7, 4, 2, 1, 1, Qt.AlignTop | Qt.AlignLeft) # Fundos Imobiliários\nFundos de Investimento: Real Estate
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg8, 5, 2, 1, 1, Qt.AlignTop | Qt.AlignLeft) # Renda Fixa\nFundos de Investiometnos: Renda Fixa\nTesouro Direto e Títulos Públicos\nPrevidência Privada\nCOE
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg9, 6, 2, 1, 1, Qt.AlignTop | Qt.AlignLeft) # BDR\nFundos de Investimento: Ações Internacionais
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_NovoTipoAtivo, 7, 1, 1, 2, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_TipoDeAtivo, 8, 1, 1, 2, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_NovoSubtipoAtivo, 9, 1, 1, 2, Qt.AlignHCenter | Qt.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_NovoSubtipoAtivo, 10, 1, 1, 2, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Seguinte, 11, 1, 2, 2, Qt.AlignHCenter | Qt.AlignTop)
        self.HMI.TextBox_NovoSubtipoAtivo.setFocus()

    def CreatePage34b(self): # "Cotação do ativo '"+self.HMI.TextBox_NovoNomeAtivo.text()+"' foi encontrada online."
        black = 'rgb(0, 0, 0)'
        green = 'rgb(10, 15, 10)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.CotacaoNovoAtivo = self.HMI.YahooFinance.GetCotacao(self.HMI.TextBox_NovoNomeAtivo.text(), self.HMI.DBManager.GetUserCoinCurrency())

        self.HMI.Label_Titulo = QLabel("Cotação do ativo '"+self.HMI.TextBox_NovoNomeAtivo.text()+"' foi encontrada online.")
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font24)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel("A cotação correspondente encontrada automaticamente\nestá em torno de "+self.HMI.DBManager.GetUserCoinCurrency()+str(self.HMI.CotacaoNovoAtivo)+'.')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font24)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg2 = QLabel("A cotação encontrada está correta?")
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font24)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.Button_Voltar = QPushButton('Não. Voltar,\nrenomear ativo e\ntentar novamente.')
        self.HMI.Button_Voltar.pressed.connect(lambda: self.HMI.CreatePage('27'))
        self.HMI.Button_Voltar.setFont(self.HMI.font16)
        self.HMI.Button_Voltar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Voltar.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Voltar.setIcon(QIcon("./images/Voltar.png"))
        self.HMI.Button_Voltar.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Voltar.setStyleSheet("background-color: rgb(120, 20, 30)")

        self.HMI.Button_AtivarModoManual = QPushButton('Não, mas continue\ne ative o modo manual.')
        self.HMI.Button_AtivarModoManual.pressed.connect(lambda: self.HMI.CreatePage('_23_'))
        self.HMI.Button_AtivarModoManual.setFont(self.HMI.font16)
        self.HMI.Button_AtivarModoManual.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_AtivarModoManual.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_AtivarModoManual.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_AtivarModoManual.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AtivarModoManual.setStyleSheet("background-color: rgb(120, 120, 30)")

        self.HMI.Button_Seguinte = QPushButton('Sim, está correto!')
        self.HMI.Button_Seguinte.pressed.connect(lambda: self.HMI.CreatePage('23_'))
        self.HMI.Button_Seguinte.setFont(self.HMI.font16)
        self.HMI.Button_Seguinte.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Seguinte.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Seguinte.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_Seguinte.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Seguinte.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Button_Info1 = QPushButton('O que é modo manual?')
        self.HMI.Button_Info1.pressed.connect(lambda: self.HMI.CreatePage('Info1'))
        self.HMI.Button_Info1.setFont(self.HMI.font16)
        self.HMI.Button_Info1.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Info1.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Info1.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info1.setStyleSheet("background-color: rgb(100, 100, 100)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 4, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 2, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Voltar, 3, 0, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AtivarModoManual, 3, 1, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Seguinte, 3, 2, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Info1, 4, 1, 1, 1, Qt.AlignCenter)

    def CreatePage35b(self): # "Cotação do ativo '"+self.HMI.TextBox_NovoNomeAtivo.text()+"'\nnão foi encontrada online."
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel("Cotação do ativo '"+self.HMI.TextBox_NovoNomeAtivo.text()+"'\nnão foi encontrada online.")
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font24)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel("Verifique a sua conexão com a internet\nou tente voltar e renomear o ativo.\nSe preferir, ative o modo manual e\ninsira a cotação desse ativo manualmente\nquando solicitado futuramente.")
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font22)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.Button_Voltar = QPushButton('Voltar,\nrenomear ativo e\ntentar novamente.')
        self.HMI.Button_Voltar.pressed.connect(lambda: self.HMI.CreatePage('27'))
        self.HMI.Button_Voltar.setFont(self.HMI.font16)
        self.HMI.Button_Voltar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Voltar.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Voltar.setIcon(QIcon("./images/Voltar.png"))
        self.HMI.Button_Voltar.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Voltar.setStyleSheet("background-color: rgb(120, 20, 30)")

        self.HMI.Button_AtivarModoManual = QPushButton('Ative o modo manual\npara esse ativo.')
        self.HMI.Button_AtivarModoManual.pressed.connect(lambda: self.HMI.CreatePage('23_'))
        self.HMI.Button_AtivarModoManual.setFont(self.HMI.font16)
        self.HMI.Button_AtivarModoManual.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_AtivarModoManual.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_AtivarModoManual.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_AtivarModoManual.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_AtivarModoManual.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Button_Info1 = QPushButton('O que é modo manual?')
        self.HMI.Button_Info1.pressed.connect(lambda: self.HMI.CreatePage('Info1'))
        self.HMI.Button_Info1.setFont(self.HMI.font16)
        self.HMI.Button_Info1.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_Info1.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Info1.setStyleSheet("background-color: rgb(100, 100, 100)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 4, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 1, 3, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Voltar, 3, 0, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AtivarModoManual, 3, 2, 1, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Info1, 4, 2, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)

    def CreateTable_23_1(self):
        HHeader = ['Data',
                   'Tipo',
                   'Qqt',
                   'Preço',
                   'Corretagem',
                   'Taxa B3%',
                   'Taxa B3',
                   'Obs']
        fakedata = [('','','','','','','','')]

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setRowCount(1)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnCount(len(HHeader))

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setShowGrid(False)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setFont(self.HMI.font16)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.verticalHeader().hide()
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.horizontalHeader().hide()

        for col in range(len(HHeader)):
            celula = QTableWidgetItem(str(HHeader[col]))
            celula.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
            celula.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
            self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setItem(0, col, celula)

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.resizeColumnsToContents()

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.adjustSize()
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(7, SizeCol7)

    def CreateTable_23_2(self):
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setFixedHeight(int(self.HMI.frameGeometry().height()*6/20*1.4))

        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setShowGrid(False)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setFont(self.HMI.font14)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                  color: white;
                                                                                  border: 1px solid rgba(0, 0, 0, 0);}
                                                                    QTableView {border-bottom: 2px dashed white;
                                                                                border-right: 1px solid white;
                                                                                border-left: 1px solid white;}
                                                                    QTableView::item {border-bottom: 1px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.verticalHeader().hide()
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.horizontalHeader().hide()
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setSelectionBehavior(QAbstractItemView.SelectRows)

        HHeader = ['Data',
                   'Tipo',
                   'Qqt',
                   'Preço',
                   'Corretagem',
                   'Taxa B3%',
                   'Taxa B3',
                   'Obs']
        self.data_23_1 = self.HMI.DBManager.GetAllOperacoes(self.HMI.DTeST)
        self.data_23_1 = self.data_23_1[::-1]
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setRowCount(len(self.data_23_1))
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnCount(len(HHeader))
        for i, item in enumerate(self.data_23_1):
            for j in range(len(item)):
                if self.HMI.ShowValues:
                    if isinstance(item[j], float):
                        text = str('%.2f' % item[j])
                    else:
                        text = str(item[j])
                else:
                    if j in [2, 3, 4, 6]:
                        text = '***'
                    else: text = str(item[j])
                it = self.HMI.Table_Operacoes_Realizadas_com_Ativo.item(i, j)
                it = QTableWidgetItem(text)
                it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                if not self.HMI.DTeST == "": it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
                it.setTextAlignment(Qt.AlignCenter)
                if "VAZIO" in item: it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
                if text in ["Compra"]: it.setForeground(QBrush(QColor('green')))
                elif text in ["Venda"]: it.setForeground(QBrush(QColor('red')))
                if j == 7:
                    it.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.HMI.Table_Operacoes_Realizadas_com_Ativo.setItem(i, j, it)

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.HMI.GetSizeOfTableColumns(self.data_23_1, HHeader)

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.adjustSize()
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(6, SizeCol6)

        self.HMI.Table_Operacoes_Realizadas_com_Ativo.adjustSize()
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(7, SizeCol7)

    def CreateTable_24_1(self):
        HHeader = ['Data',
                   'Movimentação']
        fakedata = [('','')]

        self.HMI.Table_DepositosESaques_Header.setRowCount(1)
        self.HMI.Table_DepositosESaques_Header.setColumnCount(len(HHeader))

        self.HMI.Table_DepositosESaques_Header.setShowGrid(False)
        self.HMI.Table_DepositosESaques_Header.setFont(self.HMI.font16)
        self.HMI.Table_DepositosESaques_Header.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_DepositosESaques_Header.verticalHeader().hide()
        self.HMI.Table_DepositosESaques_Header.horizontalHeader().hide()

        for col in range(len(HHeader)):
            celula = QTableWidgetItem(str(HHeader[col]))
            celula.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
            celula.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
            self.HMI.Table_DepositosESaques_Header.setItem(0, col, celula)

        self.HMI.Table_DepositosESaques_Header.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_DepositosESaques_Header.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.HMI.Table_DepositosESaques_Header.resizeColumnsToContents()

        SizeCol0,SizeCol1 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
        self.HMI.Table_DepositosESaques_Header.adjustSize()
        self.HMI.Table_DepositosESaques_Header.setColumnWidth(0, SizeCol0)
        self.HMI.Table_DepositosESaques_Header.setColumnWidth(1, SizeCol1)

    def CreateTable_24_2(self):
        self.HMI.Table_DepositosESaques.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_DepositosESaques.setFixedHeight(int(self.HMI.frameGeometry().height()*5/20*1.4))

        self.HMI.Table_DepositosESaques.setShowGrid(False)
        self.HMI.Table_DepositosESaques.setFont(self.HMI.font14)
        self.HMI.Table_DepositosESaques.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                  color: white;
                                                                                  border: 1px solid rgba(0, 0, 0, 0);}
                                                                    QTableView {border-bottom: 2px dashed white;
                                                                                border-right: 1px solid white;
                                                                                border-left: 1px solid white;}
                                                                    QTableView::item {border-bottom: 1px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
        self.HMI.Table_DepositosESaques.verticalHeader().hide()
        self.HMI.Table_DepositosESaques.horizontalHeader().hide()
        self.HMI.Table_DepositosESaques.setSelectionBehavior(QAbstractItemView.SelectRows)

        #Create Thread
        HHeader = ['Data',
                   'Movimentação']
        self.data_24_1 = self.HMI.DBManager.GetDepositosESaques()
        self.HMI.Table_DepositosESaques.setRowCount(len(self.data_24_1))
        self.HMI.Table_DepositosESaques.setColumnCount(len(HHeader))
        for i, item in enumerate(self.data_24_1):
            for j in range(len(item)):
                if j == 1:
                    if self.HMI.ShowValues:
                        text = str(abs(item[j]))
                    else:
                        if j in [1]:
                            text = "***"
                        else: text = str(item[j])
                else:
                    text = str(item[j])
                it = self.HMI.Table_DepositosESaques.item(i, j)
                it = QTableWidgetItem(text)
                it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                it.setTextAlignment(Qt.AlignCenter)
                if text in ["Compra"]: it.setForeground(QBrush(QColor('green')))
                elif text in ["Venda"]: it.setForeground(QBrush(QColor('red')))
                if item[1] < 0: it.setForeground(QBrush(QColor('orange')))
                else: it.setForeground(QBrush(QColor(0, 255, 0)))
                self.HMI.Table_DepositosESaques.setItem(i, j, it)

        SizeCol0,SizeCol1 = self.HMI.GetSizeOfTableColumns(self.data_24_1, HHeader)

        self.HMI.Table_DepositosESaques_Header.adjustSize()
        self.HMI.Table_DepositosESaques_Header.setColumnWidth(0, SizeCol0)
        self.HMI.Table_DepositosESaques_Header.setColumnWidth(1, SizeCol1)

        self.HMI.Table_DepositosESaques.adjustSize()
        self.HMI.Table_DepositosESaques.setColumnWidth(0, SizeCol0)
        self.HMI.Table_DepositosESaques.setColumnWidth(1, SizeCol1)

    def CreateTable_29_1(self):
        HHeader = ['Data',
                   'Tipo',
                   'Qqt',
                   'Preço',
                   'Corretagem',
                   'Taxa B3%',
                   'Taxa B3',
                   'Obs']
        fakedata = [('','','','','','','','')]

        self.HMI.Table_Operacoes_SelecionadasHeader.setRowCount(1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnCount(len(HHeader))

        self.HMI.Table_Operacoes_SelecionadasHeader.setShowGrid(False)
        self.HMI.Table_Operacoes_SelecionadasHeader.setFont(self.HMI.font16)
        self.HMI.Table_Operacoes_SelecionadasHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_Operacoes_SelecionadasHeader.verticalHeader().hide()
        self.HMI.Table_Operacoes_SelecionadasHeader.horizontalHeader().hide()

        for col in range(len(HHeader)):
            celula = QTableWidgetItem(str(HHeader[col]))
            celula.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
            celula.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
            self.HMI.Table_Operacoes_SelecionadasHeader.setItem(0, col, celula)

        self.HMI.Table_Operacoes_SelecionadasHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_SelecionadasHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.HMI.Table_Operacoes_SelecionadasHeader.resizeColumnsToContents()

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
        self.HMI.Table_Operacoes_SelecionadasHeader.adjustSize()
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(7, SizeCol7)

    def CreateTable_29_2(self):
        self.HMI.Table_Operacoes_Selecionadas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_Selecionadas.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))

        self.HMI.Table_Operacoes_Selecionadas.setShowGrid(False)
        self.HMI.Table_Operacoes_Selecionadas.setFont(self.HMI.font14)
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
                   'Tipo',
                   'Qqt',
                   'Preço',
                   'Corretagem',
                   'Taxa B3%',
                   'Taxa B3',
                   'Obs']
        self.HMI.Table_Operacoes_Selecionadas.setRowCount(1)
        self.HMI.Table_Operacoes_Selecionadas.setColumnCount(len(HHeader))
        for i, item in enumerate(self.data_23_1):
            if i == self.Operacoes[self.item]:
                for j in range(len(item)):
                    if isinstance(item[j], float):
                        text = str('%.2f' % item[j])
                    else:
                        text = str(item[j])
                    it = self.HMI.Table_Operacoes_Selecionadas.item(0, j)
                    it = QTableWidgetItem(text)
                    it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
                    it.setTextAlignment(Qt.AlignCenter)
                    if text in ["Compra"]: it.setForeground(QBrush(QColor('green')))
                    elif text in ["Venda"]: it.setForeground(QBrush(QColor('red')))
                    if j == 7:
                        it.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    self.HMI.Table_Operacoes_Selecionadas.setItem(0, j, it)

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.HMI.GetSizeOfTableColumns(self.data_23_1, HHeader)

        self.HMI.Table_Operacoes_SelecionadasHeader.adjustSize()
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(7, SizeCol7)

        self.HMI.Table_Operacoes_Selecionadas.adjustSize()
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(7, SizeCol7)

    def CreateTable_30_1(self):
        HHeader = ['Data',
                   'Tipo',
                   'Qqt',
                   'Preço',
                   'Corretagem',
                   'Taxa B3%',
                   'Taxa B3',
                   'Obs']
        fakedata = [('','','','','','','','')]

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setRowCount(1)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnCount(len(HHeader))

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setShowGrid(False)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setFont(self.HMI.font16)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.verticalHeader().hide()
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.horizontalHeader().hide()

        for col in range(len(HHeader)):
            celula = QTableWidgetItem(str(HHeader[col]))
            celula.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
            celula.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
            self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setItem(0, col, celula)

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.resizeColumnsToContents()

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.adjustSize()
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(7, SizeCol7)

    def CreateTable_30_2(self):
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setFixedHeight(int(self.HMI.frameGeometry().height()*6/20*1.4))

        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setShowGrid(False)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setFont(self.HMI.font14)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                  color: white;
                                                                                  border: 1px solid rgba(0, 0, 0, 0);}
                                                                    QTableView {border-bottom: 2px dashed white;
                                                                                border-right: 1px solid white;
                                                                                border-left: 1px solid white;}
                                                                    QTableView::item {border-bottom: 1px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.verticalHeader().hide()
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.horizontalHeader().hide()
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setSelectionBehavior(QAbstractItemView.SelectRows)

        HHeader = ['Data',
                   'Tipo',
                   'Qqt',
                   'Preço',
                   'Corretagem',
                   'Taxa B3%',
                   'Taxa B3',
                   'Obs']
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setRowCount(len(self.Operacoes))
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnCount(len(HHeader))
        linha = -1
        for i, item in enumerate(self.data_23_1):
            if i in self.Operacoes:
                linha += 1
                for j in range(len(item)):
                    if isinstance(item[j], float):
                        text = str('%.2f' % item[j])
                    else:
                        text = str(item[j])
                    it = self.HMI.Table_Operacoes_Realizadas_com_Ativo.item(linha, j)
                    it = QTableWidgetItem(text)
                    it.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
                    it.setTextAlignment(Qt.AlignCenter)
                    if text in ["Compra"]: it.setForeground(QBrush(QColor('green')))
                    elif text in ["Venda"]: it.setForeground(QBrush(QColor('red')))
                    if j == 7:
                        it.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    self.HMI.Table_Operacoes_Realizadas_com_Ativo.setItem(linha, j, it)

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.HMI.GetSizeOfTableColumns(self.data_23_1, HHeader)

        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.adjustSize()
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(7, SizeCol7)

        self.HMI.Table_Operacoes_Realizadas_com_Ativo.adjustSize()
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(7, SizeCol7)

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

        elif ButtonPressed == 'Deposito':
            self.HMI.Button_Deposito.setStyleSheet('background-color: black; color: green')
            self.HMI.Button_Deposito.setText("DEPÓSITO")
            self.HMI.Button_Deposito.setFont(self.HMI.font20)
            self.HMI.Button_Saque.setStyleSheet('background-color: black; color: gray')
            self.HMI.Button_Saque.setText("saque")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Deposito = True
            self.HMI.TextBox_Valor.setStyleSheet('color: green')
            BackgroundLineEdit = "rgb(0,10,30)"
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: green")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: green")
            self.HMI.TextBox_Valor.setFocus()

        elif ButtonPressed == 'Saque':
            self.HMI.Button_Deposito.setStyleSheet('background-color: black; color: gray')
            self.HMI.Button_Deposito.setText("depósito")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setStyleSheet('background-color: black; color: orange')
            self.HMI.Button_Saque.setText("SAQUE")
            self.HMI.Button_Saque.setFont(self.HMI.font20)
            self.HMI.Deposito = False
            self.HMI.TextBox_Valor.setStyleSheet('color: orange')
            BackgroundLineEdit = "rgb(0,10,30)"
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: orange")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: orange")
            self.HMI.TextBox_Valor.setFocus()

        elif ButtonPressed == 'Delete Registro':
            if not self.HMI.DBManager.FLAG:
                TotalSelecao=[]
                for idx in self.HMI.Table_DepositosESaques.selectedIndexes():
                    TotalSelecao.append(idx.row())
                TotalSelecao = list(dict.fromkeys(TotalSelecao))
                MessageBox_Msg1 = QMessageBox()
                MessageBox_Msg1.setWindowTitle("Deletar registros de movimentações")
                MessageBox_Msg1.setText("Tem certeza que deseja deletar "+str(len(TotalSelecao))+" registros?\n\n")
                MessageBox_Msg1.setIcon(QMessageBox.Warning)
                MessageBox_Msg1.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
                MessageBox_Msg1.setDefaultButton(QMessageBox.Cancel)
                MessageBox_Msg1.setWindowIcon(QIcon(".\images\logoARCA.png"))

                returnValue = MessageBox_Msg1.exec()
                if returnValue == QMessageBox.Yes:
                    self.HMI.DBManager.DeleteDepositoOuSaque(TotalSelecao)
                    self.HMI.CreatePage('24')
            else:
                MessageBox_Msg1 = QMessageBox.about(self.HMI,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')

        elif ButtonPressed == 'Compra':
            BackgroundLineEdit = "rgb(0,10,30)"
            FontColorLineEdit = "green"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("COMPRA")
            self.HMI.Button_Compra.setFont(self.HMI.font20)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("venda")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Desdobramento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Grupamento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Bonificacao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Modo.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Corretagem.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_TaxaB3.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TipoDeOperacao = "Compra"
            if "Desdobramento;" in self.HMI.TextBox_Obs.text() or "Grupamento;" in self.HMI.TextBox_Obs.text():
                self.HMI.TextBox_Corretagem.setText("0")
                self.HMI.TextBox_TaxaB3.setText("0")
            self.HMI.TextBox_Qqt.setFocus()

        elif ButtonPressed == 'Venda':
            BackgroundLineEdit = "rgb(30,5,10)"
            FontColorLineEdit = "orange"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("compra")
            self.HMI.Button_Compra.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("VENDA")
            self.HMI.Button_Venda.setFont(self.HMI.font20)
            self.HMI.Button_Desdobramento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Grupamento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Bonificacao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Modo.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Corretagem.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_TaxaB3.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TipoDeOperacao = "Venda"
            if "Desdobramento;" in self.HMI.TextBox_Obs.text() or "Grupamento;" in self.HMI.TextBox_Obs.text():
                self.HMI.TextBox_Qqt.setText(str(int(self.HMI.DBManager.GetEstoque(self.HMI.ComboBox_Ativos.currentText()))))
                self.HMI.TextBox_Preco.setText(str(self.HMI.DBManager.GetPrecoMedio(self.HMI.ComboBox_Ativos.currentText())))
                self.HMI.TextBox_Corretagem.setText("0")
                self.HMI.TextBox_TaxaB3.setText("0")
            self.HMI.TextBox_Qqt.setFocus()

        elif ButtonPressed == 'Desdobramento':
            if not "Desdobramento;" in self.HMI.TextBox_Obs.text():
                self.HMI.TextBox_Obs.setText("Desdobramento; "+self.HMI.TextBox_Obs.text().replace("Grupamento; ","").replace("Grupamento;","").replace("Bonificação; ","").replace("Bonificação;",""))
                if self.HMI.TipoDeOperacao == "Venda":
                    self.HMI.TextBox_Qqt.setText(str(int(self.HMI.DBManager.GetEstoque(self.HMI.ComboBox_Ativos.currentText()))))
                    self.HMI.TextBox_Preco.setText(str(self.HMI.DBManager.GetPrecoMedio(self.HMI.ComboBox_Ativos.currentText())))
                    self.HMI.TextBox_Corretagem.setText("0")
                    self.HMI.TextBox_TaxaB3.setText("0")
                elif self.HMI.TipoDeOperacao == "Compra":
                    self.HMI.TextBox_Corretagem.setText("0")
                    self.HMI.TextBox_TaxaB3.setText("0")
            else:
                self.HMI.TextBox_Obs.setText(self.HMI.TextBox_Obs.text().replace("Desdobramento; ","").replace("Desdobramento;",""))

        elif ButtonPressed == 'Grupamento':
            if not "Grupamento;" in self.HMI.TextBox_Obs.text():
                self.HMI.TextBox_Obs.setText("Grupamento; "+self.HMI.TextBox_Obs.text().replace("Desdobramento; ","").replace("Desdobramento;","").replace("Bonificação; ","").replace("Bonificação;",""))
                if self.HMI.TipoDeOperacao == "Venda":
                    self.HMI.TextBox_Qqt.setText(str(int(self.HMI.DBManager.GetEstoque(self.HMI.ComboBox_Ativos.currentText()))))
                    self.HMI.TextBox_Preco.setText(str(self.HMI.DBManager.GetPrecoMedio(self.HMI.ComboBox_Ativos.currentText())))
                    self.HMI.TextBox_Corretagem.setText("0")
                    self.HMI.TextBox_TaxaB3.setText("0")
                elif self.HMI.TipoDeOperacao == "Compra":
                    self.HMI.TextBox_Corretagem.setText("0")
                    self.HMI.TextBox_TaxaB3.setText("0")
            else:
                self.HMI.TextBox_Obs.setText(self.HMI.TextBox_Obs.text().replace("Grupamento; ","").replace("Grupamento;",""))

        elif ButtonPressed == 'Bonificação':
            if not "Bonificação;" in self.HMI.TextBox_Obs.text():
                if self.HMI.TipoDeOperacao == "Venda":
                    self.HMI.TextBox_Obs.setText(self.HMI.TextBox_Obs.text().replace("Desdobramento; ","").replace("Desdobramento;","").replace("Grupamento; ","").replace("Grupamento;","").replace("Bonificação; ","").replace("Bonificação;",""))
                elif self.HMI.TipoDeOperacao == "Compra":
                    self.HMI.TextBox_Obs.setText("Bonificação; "+self.HMI.TextBox_Obs.text().replace("Desdobramento; ","").replace("Desdobramento;","").replace("Grupamento; ","").replace("Grupamento;",""))
                    self.HMI.TextBox_Corretagem.setText("0")
                    self.HMI.TextBox_TaxaB3.setText("0")
            else:
                self.HMI.TextBox_Obs.setText(self.HMI.TextBox_Obs.text().replace("Bonificação; ","").replace("Bonificação;",""))

        elif ButtonPressed == "Page29_Next":
            try:
                if not self.HMI.DBManager.FLAG:
                    Data = self.HMI.Selecao_Ano+'/'+self.HMI.Selecao_Mes+'/'+self.HMI.Selecao_Dia+" "+self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo
                    Tipo = self.HMI.TipoDeOperacao
                    if "," in self.HMI.TextBox_Qqt.text() or "." in self.HMI.TextBox_Qqt.text():
                        raise ValueError("Valor inválido!")
                    Qqt = int(self.HMI.TextBox_Qqt.text())
                    Preco = float(self.HMI.TextBox_Preco.text().replace(",","."))
                    Corretagem = float(self.HMI.TextBox_Corretagem.text().replace(",","."))
                    if "%" in self.HMI.TextBox_TaxaB3.text():
                        TaxaB3Per = float(self.HMI.TextBox_TaxaB3.text().replace("%","").replace(",","."))
                        TaxaB3 = round(TaxaB3Per/100*Qqt*Preco,2)
                    else:
                        TaxaB3 = float(self.HMI.TextBox_TaxaB3.text().replace(",","."))
                        TaxaB3Per = round(TaxaB3/Qqt/Preco*100,2)
                    Obs = self.HMI.TextBox_Obs.text().replace("ST; ","").replace("DT; ","")
                    Item = len(self.HMI.HMI_Trades.HMI_Trades_Bolsa.data_23_1)-self.HMI.HMI_Trades.HMI_Trades_Bolsa.Operacoes[self.HMI.HMI_Trades.HMI_Trades_Bolsa.item]-1
                    
                    if self.HMI.DBManager.AlterOperacao(Item, Data, Tipo, Qqt, Preco, Corretagem, TaxaB3, TaxaB3Per, Obs):
                        if self.HMI.HMI_Trades.HMI_Trades_Bolsa.item+1 >= len(self.HMI.HMI_Trades.HMI_Trades_Bolsa.Operacoes):
                            self.HMI.CreatePage('23') # Última alteração da lista
                        else:
                            self.HMI.CreatePage('29') # Ir pra próxima alteração
                    else:
                        try: self.HMI.Label_Erro1.deleteLater()
                        except: pass
                        self.HMI.Label_Erro1 = QLabel()
                        self.HMI.Label_Erro1.setStyleSheet('color: red')
                        self.HMI.Label_Erro1.setFont(self.HMI.font12)
                        self.HMI.Label_Erro1.setAlignment(Qt.AlignCenter)
                        self.HMI.Label_Erro1.setText('Data inválida.\nTalvez já tenha uma operação nesse momento.') # Substitui a string do erro mais provável
                        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Erro1, 6, 7, 1, 1, Qt.AlignCenter)
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
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Erro1, 6, 7, 1, 1, Qt.AlignCenter)

        elif ButtonPressed == 'Deletar Ativos da Pagina 23':
            if not self.HMI.DBManager.FLAG:
                self.HMI.DBManager.DeleteOperacao(self.HMI.HMI_Trades.HMI_Trades_Bolsa.Operacoes)
                self.HMI.CreatePage('23')
            else:
                MessageBox_Msg1 = QMessageBox.about(self.HMI,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')