# -*- coding: utf-8 -*-
"""
Tributacao behaviour split into a single concern.
HMI_PageBuilders - pagebuilders helpers (inherited by the composition root).
"""
from PyQt5.QtGui import (QCursor, QIcon)
from PyQt5.QtWidgets import (QLabel, QPushButton, QLineEdit, QToolTip, QTableWidget)
from PyQt5.QtCore import (QSize, Qt)


class HMI_PageBuilders:
    def CreatePage51(self):
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)
        Background_3 = QLabel()
        Background_3.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Tributação')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Msg2 = QLabel('Resultado geral líquido:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.TextBox_Msg2 = QLineEdit()
        self.HMI.TextBox_Msg2.setText(str(self.HMI.DBManager.GetResultadoGeralLiquido()))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Password)
        if float(self.HMI.TextBox_Msg2.text()) >= 0: self.HMI.TextBox_Msg2.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Msg2.setStyleSheet('QLineEdit {background-color: black; color: red;}')
        self.HMI.TextBox_Msg2.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg2.setEnabled(False)
        self.HMI.TextBox_Msg2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.HMI.Button_DTeST = QPushButton()
        self.HMI.Button_DTeST.pressed.connect(lambda: self.OnButtonPressed('ChangeDTeST'))
        self.HMI.Button_DTeST.setFixedSize(70*3+5,35*3+5)
        self.HMI.Button_DTeST.setIconSize(QSize(70*3, 35*3))
        self.HMI.Button_DTeST.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_DTeST.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Day Trades e Swing Trades.png"))
        self.HMI.Button_DTeST.setToolTip("Alterar apresentação (DT e ST)")
        self.HMI.DTeST_51 = "DTeST"

        self.HMI.Button_CriptoeB3 = QPushButton()
        self.HMI.Button_CriptoeB3.pressed.connect(lambda: self.OnButtonPressed('ChangeCriptoeB3'))
        self.HMI.Button_CriptoeB3.setFixedSize(70*3+5,35*3+5)
        self.HMI.Button_CriptoeB3.setIconSize(QSize(70*3, 35*3))
        self.HMI.Button_CriptoeB3.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_CriptoeB3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_CriptoeB3.setIcon(QIcon("./images/Visualizar cripto e B3.png"))
        self.HMI.Button_CriptoeB3.setToolTip("Alterar apresentação (cripto e B3)")
        self.HMI.CriptoeB3_51 = "CriptoeB3"

        self.HMI.Label_Msg3 = QLabel('Resultado líquido (último mês):')
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font12)
        self.HMI.Label_Msg3.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.TextBox_Msg3 = QLineEdit()
        self.HMI.TextBox_Msg3.setText(str(self.HMI.DBManager.GetResultadoLiquidoUltimoMes()))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg3.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg3.setEchoMode(QLineEdit.Password)
        if float(self.HMI.TextBox_Msg3.text()) >= 0: self.HMI.TextBox_Msg3.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Msg3.setStyleSheet('QLineEdit {background-color: black; color: red;}')
        self.HMI.TextBox_Msg3.setFont(self.HMI.font12)
        self.HMI.TextBox_Msg3.setEnabled(False)
        self.HMI.TextBox_Msg3.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.HMI.Label_Msg4 = QLabel('Imposto de DT devido (último mês):')
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font12)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.TextBox_Msg4 = QLineEdit()
        self.HMI.TextBox_Msg4.setText(str(self.HMI.DBManager.GetImpostoDevidoDeDTUltimoMes()))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg4.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg4.setEchoMode(QLineEdit.Password)
        self.HMI.TextBox_Msg4.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        self.HMI.TextBox_Msg4.setFont(self.HMI.font12)
        self.HMI.TextBox_Msg4.setEnabled(False)
        self.HMI.TextBox_Msg4.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.HMI.Button_RegistrarMudancas = QPushButton()
        self.HMI.Button_RegistrarMudancas.pressed.connect(lambda: self.OnButtonPressed('ExportIR'))
        self.HMI.Button_RegistrarMudancas.setFixedSize(40,40)
        self.HMI.Button_RegistrarMudancas.setIconSize(QSize(35, 35))
        self.HMI.Button_RegistrarMudancas.setIcon(QIcon("./images/ExportIR.png"))
        self.HMI.Button_RegistrarMudancas.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_RegistrarMudancas.setToolTip("Exportar Informe de Rendimentos")
        self.HMI.Button_RegistrarMudancas.setStyleSheet('QPushButton{background-color: gray} QToolTip {background-color: black; color: white;border: black solid 1px}')

        # self.HMI.Button_Imprimir = QPushButton()
        # self.HMI.Button_Imprimir.pressed.connect(lambda: self.OnButtonPressed('Gerar Excel de Tributação'))
        # self.HMI.Button_Imprimir.setFixedSize(40,40)
        # self.HMI.Button_Imprimir.setIconSize(QSize(35, 35))
        # self.HMI.Button_Imprimir.setIcon(QIcon("./images/printer.png"))
        # self.HMI.Button_Imprimir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # self.HMI.Button_Imprimir.setStyleSheet('QPushButton {background-color: black; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        # self.HMI.Button_Imprimir.setToolTip("Gerar Excel de Tributação")

        self.HMI.Table_Tributacao_Header = QTableWidget()
        self.HMI.Table_Tributacao = QTableWidget()

        self.CreateTable_51_1()
        self.CreateTable_51_2()

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 3, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_3, 4, 0, 8, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 10, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg2, 1, 2, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg3, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 3, 1, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg4, 3, 2, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DTeST, 1, 5, 3, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_CriptoeB3, 1, 6, 3, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RegistrarMudancas, 4, 0, 1, 10, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        # self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Imprimir, 5, 0, 1, 10, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Tributacao_Header, 5, 0, 1, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Tributacao, 6, 0, 6, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
