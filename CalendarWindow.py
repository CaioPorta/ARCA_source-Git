# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 12:36:00 2021

@author: caiop
"""

import ctypes

import pandas as pd
import numpy as np

from datetime import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class CalendarWindow(QWidget):
    def __init__(self, HMI):
        self.HMI = HMI
        super().__init__()
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.screen_height = screensize[1] # FHD
        self.screen_width = screensize[0] # FHD

        self.setAutoFillBackground(True)
        background = self.palette()
        background.setColor(self.backgroundRole(), QColor(str('#%02x%02x%02x' % (10, 40, 60))))
        self.setPalette(background)
        self.setFixedSize(QSize(int(self.screen_width*0.4), int(self.screen_height*0.5)))
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.Label_Titulo = QLabel()
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.HMI.font22)
        self.Label_Titulo.setAlignment(Qt.AlignCenter)
        self.Label_Titulo.setText("Selecione a data")

        import calendar
        from datetime import datetime

        self.calendar = QCalendarWidget()
        self.calendar.setDateEditAcceptDelay(10000)
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        currentDay = datetime.now().day
        self.calendar.setMinimumDate(QDate(1950, 1, 1))
        self.calendar.setMaximumDate(QDate(currentYear, currentMonth, currentDay))
        self.calendar.setSelectedDate(QDate(int(self.HMI.Selecao_Ano), int(self.HMI.Selecao_Mes), int(self.HMI.Selecao_Dia)))
        self.calendar.setFixedHeight(int(self.HMI.frameGeometry().width()*2/10*0.9))
        self.calendar.setStyleSheet("background-color : "+str('#%02x%02x%02x' % (100, 180, 240))+";")

        self.Button_Cancelar = QPushButton('Cancelar')
        self.Button_Cancelar.pressed.connect(lambda: self.Close())
        self.Button_Cancelar.setFont(self.HMI.font16)
        self.Button_Cancelar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/15*0.9),int(self.HMI.frameGeometry().height()/15*0.9)))
        self.Button_Cancelar.setFixedSize(int(self.HMI.frameGeometry().width()*2/15*0.9),int(self.HMI.frameGeometry().width()*1/15*0.9))
        self.Button_Cancelar.setIcon(QIcon("./images/Voltar.png"))
        self.Button_Cancelar.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_Cancelar.setStyleSheet("background-color: rgb(200, 100, 100)")

        self.Button_SelecionarData = QPushButton('Selecionar ano,\nmês e\ndia')
        self.Button_SelecionarData.pressed.connect(lambda: self.OnButtonPressed())
        self.Button_SelecionarData.setFont(self.HMI.font16)
        self.Button_SelecionarData.setIconSize(QSize(int(self.HMI.frameGeometry().height()/15*0.9),int(self.HMI.frameGeometry().height()/15*0.9)))
        self.Button_SelecionarData.setFixedSize(int(self.HMI.frameGeometry().width()*2/15*0.9),int(self.HMI.frameGeometry().width()*1/15*0.9))
        self.Button_SelecionarData.setIcon(QIcon("./images/log_in.png"))
        self.Button_SelecionarData.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button_SelecionarData.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.layout.addWidget(self.Label_Titulo, Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addWidget(self.calendar, Qt.AlignCenter)
        self.layoutH = QHBoxLayout()
        self.layout.addLayout(self.layoutH)
        self.layoutH.addWidget(self.Button_Cancelar, Qt.AlignLeft)
        self.layoutH.addWidget(self.Button_SelecionarData, Qt.AlignRight)

    def Abrir(self):
        self.show()
        self.HMI.OutraJanelaAberta = True
        self.HMI.CalendarWindowOpen = True

    def Close(self):
        self.close()
        self.HMI.OutraJanelaAberta = False
        self.HMI.CalendarWindowOpen = False

    def OnButtonPressed(self):
        DataSelecionada = self.calendar.selectedDate().toPyDate()
        self.HMI.Selecao_Ano = str(DataSelecionada.year)
        self.HMI.Selecao_Mes = str(DataSelecionada.month)
        self.HMI.Selecao_Dia = str(DataSelecionada.day)
        self.HMI.Button_Calendario.setText(self.HMI.Selecao_Ano+"/"+self.HMI.Selecao_Mes+"/"+self.HMI.Selecao_Dia)
        self.Close()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.Close()
