# -*- coding: utf-8 -*-
"""
Desempenho behaviour split into a single concern.
HMI_PageBuilders - pagebuilders helpers (inherited by the composition root).
"""
from PyQt5.QtGui import (QCursor, QMovie)
from PyQt5.QtWidgets import (QLabel, QComboBox)
from PyQt5.QtCore import (QSize, Qt)


class HMI_PageBuilders:
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
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Rentabilidade da Carteira')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font20)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Msg2 = QLabel('Desempenho percentual')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Msg3 = QLabel('Período: ')
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font14)
        self.HMI.Label_Msg3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.ComboBox_PeriodoDesempenhoPercentual = QComboBox()
        self.HMI.ComboBox_PeriodoDesempenhoPercentual.setFont(self.HMI.font14)
        self.HMI.ComboBox_PeriodoDesempenhoPercentual.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.ComboBox_PeriodoDesempenhoPercentual.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        for periodo in ['No mês','3 meses','1 ano','Máximo']:
            self.HMI.ComboBox_PeriodoDesempenhoPercentual.addItem(periodo)

        self.HMI.Gif_Grafico1 = QLabel()
        self.HMI.Movie_Grafico1 = QMovie("./images/Loading4.gif")
        self.HMI.Movie_Grafico1.setScaledSize(QSize().scaled(int(self.HMI.frameGeometry().width()),int(self.HMI.frameGeometry().height()/5*.95), Qt.KeepAspectRatio))
        self.HMI.Gif_Grafico1.setMovie(self.HMI.Movie_Grafico1)
        self.HMI.Movie_Grafico1.start()

        self.HMI.Label_Msg4 = QLabel('Desempenho em '+self.HMI.DBManager.GetUserCoinCurrency())
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font16)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Msg5 = QLabel('Período: ')
        self.HMI.Label_Msg5.setStyleSheet('color: white')
        self.HMI.Label_Msg5.setFont(self.HMI.font14)
        self.HMI.Label_Msg5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.ComboBox_PeriodoDesempenhoCurrency = QComboBox()
        self.HMI.ComboBox_PeriodoDesempenhoCurrency.setFont(self.HMI.font14)
        self.HMI.ComboBox_PeriodoDesempenhoCurrency.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.ComboBox_PeriodoDesempenhoCurrency.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        for periodo in ['3 meses','1 ano']:
            self.HMI.ComboBox_PeriodoDesempenhoCurrency.addItem(periodo)

        self.HMI.Gif_Grafico2 = QLabel()
        self.HMI.Movie_Grafico2 = QMovie("./images/Loading4.gif")
        self.HMI.Movie_Grafico2.setScaledSize(QSize().scaled(int(self.HMI.frameGeometry().width()),int(self.HMI.frameGeometry().height()/5*.95), Qt.KeepAspectRatio))
        self.HMI.Gif_Grafico2.setMovie(self.HMI.Movie_Grafico2)
        self.HMI.Movie_Grafico2.start()

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 20)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 20, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 7, 20)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 1, 3, Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 2, 0, 1, 3, Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 3, 0, Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_PeriodoDesempenhoPercentual, 3, 1, Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_Grafico1, 4, 0, 1, 20, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 5, 0, 1, 3, Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 6, 0, 1, 3, Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_PeriodoDesempenhoCurrency, 6, 1, Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_Grafico2, 7, 0, 1, 20, Qt.AlignmentFlag.AlignCenter)
