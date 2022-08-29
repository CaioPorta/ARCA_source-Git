# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:55:28 2021

Assista essa aula:
https://www.youtube.com/watch?v=G2Tr2dcjR3U

@author: caiop
"""

import pandas as pd
import numpy as np

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class HMI_Desempenho(object):
    def __init__(self, HMI):
        self.HMI = HMI
        QToolTip.setFont(QFont('Arial', 12))

    def CreatePage12(self):
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        Background_3 = QLabel()
        Background_3.setStyleSheet("background-color: "+black)

        Background_4 = QLabel()
        Background_4.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Desempenho da Carteira')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Rentabilidade da Carteira')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font20)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg2 = QLabel('Desempenho percentual')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg3 = QLabel('Período: ')
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font14)
        self.HMI.Label_Msg3.setAlignment(Qt.AlignCenter)

        self.HMI.ComboBox_PeriodoDesempenhoPercentual = QComboBox()
        self.HMI.ComboBox_PeriodoDesempenhoPercentual.setFont(self.HMI.font14)
        self.HMI.ComboBox_PeriodoDesempenhoPercentual.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_PeriodoDesempenhoPercentual.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        for periodo in ['No mês','3 meses','1 ano','Máximo']:
            self.HMI.ComboBox_PeriodoDesempenhoPercentual.addItem(periodo)

        self.HMI.Gif_Grafico1 = QLabel()
        self.HMI.Movie_Grafico1 = QMovie("./images/Loading4.gif")
        self.HMI.Movie_Grafico1.setScaledSize(QSize().scaled(self.HMI.frameGeometry().width(),self.HMI.frameGeometry().height()/5*.95, Qt.KeepAspectRatio))
        self.HMI.Gif_Grafico1.setMovie(self.HMI.Movie_Grafico1)
        self.HMI.Movie_Grafico1.start()

        self.HMI.Label_Msg4 = QLabel('Desempenho em '+self.HMI.DBManager.GetUserCoinCurrency())
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font16)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignCenter)

        self.HMI.Label_Msg5 = QLabel('Período: ')
        self.HMI.Label_Msg5.setStyleSheet('color: white')
        self.HMI.Label_Msg5.setFont(self.HMI.font14)
        self.HMI.Label_Msg5.setAlignment(Qt.AlignCenter)

        self.HMI.ComboBox_PeriodoDesempenhoCurrency = QComboBox()
        self.HMI.ComboBox_PeriodoDesempenhoCurrency.setFont(self.HMI.font14)
        self.HMI.ComboBox_PeriodoDesempenhoCurrency.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.ComboBox_PeriodoDesempenhoCurrency.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        for periodo in ['3 meses','1 ano']:
            self.HMI.ComboBox_PeriodoDesempenhoCurrency.addItem(periodo)

        self.HMI.Gif_Grafico2 = QLabel()
        self.HMI.Movie_Grafico2 = QMovie("./images/Loading4.gif")
        self.HMI.Movie_Grafico2.setScaledSize(QSize().scaled(self.HMI.frameGeometry().width(),self.HMI.frameGeometry().height()/5*.95, Qt.KeepAspectRatio))
        self.HMI.Gif_Grafico2.setMovie(self.HMI.Movie_Grafico2)
        self.HMI.Movie_Grafico2.start()

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 20)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 20, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 7, 20)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 1, 3, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 2, 0, 1, 3, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 3, 0, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_PeriodoDesempenhoPercentual, 3, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_Grafico1, 4, 0, 1, 20, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 5, 0, 1, 3, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 6, 0, 1, 3, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_PeriodoDesempenhoCurrency, 6, 1, Qt.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_Grafico2, 7, 0, 1, 20, Qt.AlignCenter)


        # self.HMI.GraphWidget = pg.PlotWidget()
        # self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget, 2, 2, 2, 2, Qt.AlignHCenter | Qt.AlignBottom)

        # hour = [1,2,3,4,5,6,7,8,9,10] # Exemplo 1
        # temperature = [30,32,34,32,33,31,29,32,35,45]
        # self.HMI.GraphWidget.plot(hour, temperature)
        # self.HMI.GraphWidget.setRange(xRange=[0, 8], yRange=[0, 40])


        # bufferSize = 1000 # Exemplo 2
        # self.data = np.zeros(bufferSize)
        # self.data2 = np.random.normal(size=bufferSize)
        # self.curve = self.HMI.GraphWidget.plot()
        # self.curve.setData()
        # self.line = self.HMI.GraphWidget.addLine(x=0)
        # self.HMI.GraphWidget.setRange(xRange=[0, bufferSize], yRange=[-50, 50])
        # self.i = 0

        # def update():
        #       n = 10  # update 10 samples per iteration
        #       rand = np.random.normal(size=n)
        #       # self.data[self.i:self.i+n] = np.clip(self.data[self.i-1] + rand, -50, 50)
        #       self.data[self.i:self.i+n] = np.clip(self.data2[self.i+1], -50, 50)
        #       self.curve.setData(self.data)
        #       self.i = (self.i + n) % bufferSize
        #       self.line.setValue(self.i)
        #       if (self.data==self.data2).all():#np.array_equal(self.data, self.data2):
        #           print("ok")
        #           self.timer.stop()

        # self.update = update
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.update)
        # self.timer.start(15)