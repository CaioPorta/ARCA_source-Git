 # -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 12:52:30 2021

@author: caiop
"""

import pandas as pd
import numpy as np

from functools import cached_property
import math

import sys
import ctypes

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class RelogioWindow(QWidget):
    def __init__(self, HMI):
        self.HMI = HMI
        QToolTip.setFont(QFont('Arial', 12))
        super().__init__()
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.screen_height = screensize[1] # FHD
        self.screen_width = screensize[0] # FHD

        self.setAutoFillBackground(True)
        background = self.palette()
        background.setColor(self.backgroundRole(), QColor(str('#%02x%02x%02x' % (10, 40, 60))))
        self.setPalette(background)
        self.setFixedSize(QSize(int(self.screen_width*0.4), int(self.screen_height*0.8)))
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.Selecao_Hora = self.HMI.Selecao_Hora
        self.Selecao_Minuto = self.HMI.Selecao_Minuto
        self.Selecao_Segundo = self.HMI.Selecao_Segundo
        self.Cursor_idx = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.Label_Titulo = QLabel()
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.HMI.font22)
        self.Label_Titulo.setAlignment(Qt.AlignCenter)
        self.Label_Titulo.setFixedHeight(int(self.HMI.frameGeometry().width() * 1 / 15))
        self.Label_Titulo.setText("Selecione a hora, o minuto e o segundo")

        self.Button_HoraUp = QPushButton()
        self.Button_HoraUp.pressed.connect(lambda: self.OnButtonPressed("Button_HoraUp"))
        self.Button_HoraUp.setIconSize(QSize(int(self.HMI.frameGeometry().height() / 15), int(self.HMI.frameGeometry().height() / 15)))
        self.Button_HoraUp.setFixedSize(int(self.HMI.frameGeometry().width() * 1 / 15), int(self.HMI.frameGeometry().width() * 1 / 15))
        self.Button_HoraUp.setIcon(QIcon("./images/up.png"))
        self.Button_HoraUp.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_HoraUp.setToolTip("Aumentar 1 hora")
        self.Button_HoraUp.setStyleSheet("QPushButton {background-color: rgb(10, 40, 60); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")

        self.Button_Hora = QPushButton(self.Selecao_Hora)
        self.Button_Hora.pressed.connect(lambda: self.OnButtonPressed("Button_Hora"))
        self.Button_Hora.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_Hora.setFont(QFont('Times New Roman', 40))
        self.Button_Hora.setFixedSize(int(self.HMI.frameGeometry().width() * 1 / 15), int(self.HMI.frameGeometry().width() * 1 / 15))
        self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")

        self.Button_HoraDown = QPushButton()
        self.Button_HoraDown.pressed.connect(lambda: self.OnButtonPressed("Button_HoraDown"))
        self.Button_HoraDown.setIconSize(QSize(int(self.HMI.frameGeometry().height() / 15), int(self.HMI.frameGeometry().height() / 15)))
        self.Button_HoraDown.setFixedSize(int(self.HMI.frameGeometry().width() * 1 / 15), int(self.HMI.frameGeometry().width() * 1 / 15))
        self.Button_HoraDown.setIcon(QIcon("./images/down.png"))
        self.Button_HoraDown.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_HoraDown.setStyleSheet("QPushButton {background-color: rgb(10, 40, 60); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_HoraDown.setToolTip("Diminuir 1 hora")

        self.Button_MinutoUp = QPushButton()
        self.Button_MinutoUp.pressed.connect(lambda: self.OnButtonPressed("Button_MinutoUp"))
        self.Button_MinutoUp.setIconSize(QSize(int(self.HMI.frameGeometry().height() / 15), int(self.HMI.frameGeometry().height() / 15)))
        self.Button_MinutoUp.setFixedSize(int(self.HMI.frameGeometry().width() * 1 / 15), int(self.HMI.frameGeometry().width() * 1 / 15))
        self.Button_MinutoUp.setIcon(QIcon("./images/up.png"))
        self.Button_MinutoUp.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_MinutoUp.setToolTip("Aumentar 1 minuto")
        self.Button_MinutoUp.setStyleSheet("QPushButton {background-color: rgb(10, 40, 60); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")

        self.Button_Minuto = QPushButton(self.Selecao_Minuto)
        self.Button_Minuto.pressed.connect(lambda: self.OnButtonPressed("Button_Minuto"))
        self.Button_Minuto.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_Minuto.setFont(QFont('Times New Roman', 40))
        self.Button_Minuto.setFixedSize(int(self.HMI.frameGeometry().width() * 1 / 15), int(self.HMI.frameGeometry().width() * 1 / 15))
        self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")

        self.Button_MinutoDown = QPushButton()
        self.Button_MinutoDown.pressed.connect(lambda: self.OnButtonPressed("Button_MinutoDown"))
        self.Button_MinutoDown.setIconSize(QSize(int(self.HMI.frameGeometry().height() / 15), int(self.HMI.frameGeometry().height() / 15)))
        self.Button_MinutoDown.setFixedSize(int(self.HMI.frameGeometry().width() * 1 / 15), int(self.HMI.frameGeometry().width() * 1 / 15))
        self.Button_MinutoDown.setIcon(QIcon("./images/down.png"))
        self.Button_MinutoDown.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_MinutoDown.setToolTip("Diminuir 1 minuto")
        self.Button_MinutoDown.setStyleSheet("QPushButton {background-color: rgb(10, 40, 60); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")

        self.Button_SegundoUp = QPushButton()
        self.Button_SegundoUp.pressed.connect(lambda: self.OnButtonPressed("Button_SegundoUp"))
        self.Button_SegundoUp.setIconSize(QSize(int(self.HMI.frameGeometry().height() / 15), int(self.HMI.frameGeometry().height() / 15)))
        self.Button_SegundoUp.setFixedSize(int(self.HMI.frameGeometry().width() * 1 / 15), int(self.HMI.frameGeometry().width() * 1 / 15))
        self.Button_SegundoUp.setIcon(QIcon("./images/up.png"))
        self.Button_SegundoUp.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_SegundoUp.setToolTip("Aumentar 1 segundo")
        self.Button_SegundoUp.setStyleSheet("QPushButton {background-color: rgb(10, 40, 60); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")

        self.Button_Segundo = QPushButton(self.Selecao_Segundo)
        self.Button_Segundo.pressed.connect(lambda: self.OnButtonPressed("Button_Segundo"))
        self.Button_Segundo.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_Segundo.setFont(QFont('Times New Roman', 40))
        self.Button_Segundo.setFixedSize(int(self.HMI.frameGeometry().width() * 1 / 15), int(self.HMI.frameGeometry().width() * 1 / 15))
        self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")

        self.Button_SegundoDown = QPushButton()
        self.Button_SegundoDown.pressed.connect(lambda: self.OnButtonPressed("Button_SegundoDown"))
        self.Button_SegundoDown.setIconSize(QSize(int(self.HMI.frameGeometry().height() / 15), int(self.HMI.frameGeometry().height() / 15)))
        self.Button_SegundoDown.setFixedSize(int(self.HMI.frameGeometry().width() * 1 / 15), int(self.HMI.frameGeometry().width() * 1 / 15))
        self.Button_SegundoDown.setIcon(QIcon("./images/down.png"))
        self.Button_SegundoDown.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_SegundoDown.setToolTip("Diminuir 1 segundo")
        self.Button_SegundoDown.setStyleSheet("QPushButton {background-color: rgb(10, 40, 60); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")

        self.Button_Cancelar = QPushButton('Cancelar')
        self.Button_Cancelar.pressed.connect(lambda: self.Close())
        self.Button_Cancelar.setFont(self.HMI.font16)
        self.Button_Cancelar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/15*0.9),int(self.HMI.frameGeometry().height()/15*0.9)))
        self.Button_Cancelar.setFixedSize(int(self.HMI.frameGeometry().width()*2/15*0.9),int(self.HMI.frameGeometry().width()*1/15*0.9))
        self.Button_Cancelar.setIcon(QIcon("./images/Voltar.png"))
        self.Button_Cancelar.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_Cancelar.setStyleSheet("background-color: rgb(200, 100, 100)")

        self.Button_SelecionarData = QPushButton('Selecionar')
        self.Button_SelecionarData.pressed.connect(lambda: self.OnButtonPressed("Button_SelecionarData"))
        self.Button_SelecionarData.setFont(self.HMI.font16)
        self.Button_SelecionarData.setIconSize(QSize(int(self.HMI.frameGeometry().height()/15*0.9),int(self.HMI.frameGeometry().height()/15*0.9)))
        self.Button_SelecionarData.setFixedSize(int(self.HMI.frameGeometry().width()*2/15*0.9),int(self.HMI.frameGeometry().width()*1/15*0.9))
        self.Button_SelecionarData.setIcon(QIcon("./images/log_in.png"))
        self.Button_SelecionarData.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_SelecionarData.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.layout.addWidget(self.Label_Titulo, Qt.AlignHCenter | Qt.AlignTop)
        self.HBoxLayout_DataUp = QHBoxLayout()
        self.HBoxLayout_DataUp.addWidget(self.Button_HoraUp, Qt.AlignCenter | Qt.AlignBottom)
        self.HBoxLayout_DataUp.addWidget(self.Button_MinutoUp, Qt.AlignCenter | Qt.AlignBottom)
        self.HBoxLayout_DataUp.addWidget(self.Button_SegundoUp, Qt.AlignCenter | Qt.AlignBottom)
        self.layout.addLayout(self.HBoxLayout_DataUp)
        self.HBoxLayout_Data = QHBoxLayout()
        self.HBoxLayout_Data.addWidget(self.Button_Hora, Qt.AlignCenter)
        self.HBoxLayout_Data.addWidget(self.Button_Minuto, Qt.AlignCenter)
        self.HBoxLayout_Data.addWidget(self.Button_Segundo, Qt.AlignCenter)
        self.layout.addLayout(self.HBoxLayout_Data)
        self.HBoxLayout_DataDown = QHBoxLayout()
        self.HBoxLayout_DataDown.addWidget(self.Button_HoraDown, Qt.AlignCenter | Qt.AlignTop)
        self.HBoxLayout_DataDown.addWidget(self.Button_MinutoDown, Qt.AlignCenter | Qt.AlignTop)
        self.HBoxLayout_DataDown.addWidget(self.Button_SegundoDown, Qt.AlignCenter | Qt.AlignTop)
        self.layout.addLayout(self.HBoxLayout_DataDown)
        self.layoutH = QHBoxLayout()
        self.layout.addLayout(self.layoutH)
        self.layoutH.addWidget(self.Button_Cancelar, Qt.AlignLeft)
        self.layoutH.addWidget(self.Button_SelecionarData, Qt.AlignRight)

    def Abrir(self):
        self.show()
        self.HMI.OutraJanelaAberta = True
        self.HMI.ClockWindowOpen = True

    def RegistraHora(self):
        self.HMI.Selecao_Hora = self.Selecao_Hora
        self.HMI.Selecao_Minuto = self.Selecao_Minuto
        self.HMI.Selecao_Segundo = self.Selecao_Segundo
        self.HMI.Button_Relogio.setText(self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo)

    def Close(self):
        self.close()
        self.HMI.OutraJanelaAberta = False
        self.HMI.ClockWindowOpen = False

    def OnButtonPressed(self, OnButtonPressed):
        if "Button_SelecionarData" == OnButtonPressed:
            self.RegistraHora()
            self.Close()
        elif "Button_HoraUp" == OnButtonPressed:
            self.Cursor_idx = 0
            self.Selecao_Hora = str('%02d' % (int(self.Selecao_Hora)+1,))
            if self.Selecao_Hora == "24": self.Selecao_Hora = "00"
            self.Button_Hora.setText(self.Selecao_Hora)
            self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
            self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
        elif "Button_Hora" == OnButtonPressed:
            self.Cursor_idx = 0
            self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
            self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
        elif "Button_HoraDown" == OnButtonPressed:
            self.Cursor_idx = 0
            self.Selecao_Hora = str('%02d' % (int(self.Selecao_Hora)-1,))
            if self.Selecao_Hora == "-1": self.Selecao_Hora = "23"
            self.Button_Hora.setText(self.Selecao_Hora)
            self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
            self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
        elif "Button_MinutoUp" == OnButtonPressed:
            self.Cursor_idx = 2
            self.Selecao_Minuto = str('%02d' % (int(self.Selecao_Minuto) + 1,))
            if self.Selecao_Minuto == "60": self.Selecao_Minuto = "00"
            self.Button_Minuto.setText(self.Selecao_Minuto)
            self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
            self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
        elif "Button_Minuto" == OnButtonPressed:
            self.Cursor_idx = 2
            self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
            self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
        elif "Button_MinutoDown" == OnButtonPressed:
            self.Cursor_idx = 2
            self.Selecao_Minuto = str('%02d' % (int(self.Selecao_Minuto) - 1,))
            if self.Selecao_Minuto == "-1": self.Selecao_Minuto = "59"
            self.Button_Minuto.setText(self.Selecao_Minuto)
            self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
            self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
        elif "Button_SegundoUp" == OnButtonPressed:
            self.Cursor_idx = 4
            self.Selecao_Segundo = str('%02d' % (int(self.Selecao_Segundo) + 1,))
            if self.Selecao_Segundo == "60": self.Selecao_Segundo = "00"
            self.Button_Segundo.setText(self.Selecao_Segundo)
            self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
        elif "Button_Segundo" == OnButtonPressed:
            self.Cursor_idx = 4
            self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
        elif "Button_SegundoDown" == OnButtonPressed:
            self.Cursor_idx = 4
            self.Selecao_Segundo = str('%02d' % (int(self.Selecao_Segundo) - 1,))
            if self.Selecao_Segundo == "-1": self.Selecao_Segundo = "59"
            self.Button_Segundo.setText(self.Selecao_Segundo)
            self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")

    def keyPressEvent(self, event):
        key = event.key()
        num = 'not a number'
        if key == Qt.Key_Escape: # Esc
            self.Close()
        elif key == 16777221: # Enter
            self.RegistraHora()
            self.Close()
        elif key == 16777219: # Backspace
            self.Cursor_idx -= 1
            if self.Cursor_idx == -1: self.Cursor_idx = 0

            if self.Cursor_idx == 0:
                self.Selecao_Hora = "00"
                self.Button_Hora.setText(self.Selecao_Hora)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            elif self.Cursor_idx == 1:
                self.Selecao_Hora = self.Selecao_Hora[0]+"0"
                self.Button_Hora.setText(self.Selecao_Hora)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            elif self.Cursor_idx == 2:
                self.Selecao_Minuto = "00"
                self.Button_Minuto.setText(self.Selecao_Minuto)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            elif self.Cursor_idx == 3:
                self.Selecao_Minuto = self.Selecao_Minuto[0]+"0"
                self.Button_Minuto.setText(self.Selecao_Minuto)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            elif self.Cursor_idx == 4:
                self.Selecao_Segundo = "00"
                self.Button_Segundo.setText(self.Selecao_Segundo)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
            elif self.Cursor_idx == 5:
                self.Selecao_Segundo = self.Selecao_Segundo[0]+"0"
                self.Button_Segundo.setText(self.Selecao_Segundo)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")

        elif key == 48: num =  '0'
        elif key == 49: num =  '1'
        elif key == 50: num =  '2'
        elif key == 51: num =  '3'
        elif key == 52: num =  '4'
        elif key == 53: num =  '5'
        elif key == 54: num =  '6'
        elif key == 55: num =  '7'
        elif key == 56: num =  '8'
        elif key == 57: num =  '9'

        if not num == 'not a number':
            if self.Cursor_idx == 0:
                if int(num) > 2: num = "2"
                self.Selecao_Hora = num+self.Selecao_Hora[1]
                self.Button_Hora.setText(self.Selecao_Hora)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            elif self.Cursor_idx == 1:
                self.Selecao_Hora = self.Selecao_Hora[0]+num
                if int(self.Selecao_Hora) > 23: self.Selecao_Hora = "23"
                self.Button_Hora.setText(self.Selecao_Hora)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            elif self.Cursor_idx == 2:
                if int(num) > 5: num = "5"
                self.Selecao_Minuto = num+self.Selecao_Minuto[1]
                self.Button_Minuto.setText(self.Selecao_Minuto)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
            elif self.Cursor_idx == 3:
                self.Selecao_Minuto = self.Selecao_Minuto[0]+num
                self.Button_Minuto.setText(self.Selecao_Minuto)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
            elif self.Cursor_idx == 4:
                if int(num) > 5: num = "5"
                self.Selecao_Segundo = num+self.Selecao_Segundo[1]
                self.Button_Segundo.setText(self.Selecao_Segundo)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
            elif self.Cursor_idx == 5:
                self.Selecao_Segundo = self.Selecao_Segundo[0]+num
                self.Button_Segundo.setText(self.Selecao_Segundo)
                self.Button_Hora.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Minuto.setStyleSheet("background-color: rgb(10, 40, 60); color: white; border: none; outline: none;")
                self.Button_Segundo.setStyleSheet("background-color: rgb(10, 40, 60); color: green; border: none; outline: none;")
            if self.Cursor_idx <= 5: self.Cursor_idx += 1