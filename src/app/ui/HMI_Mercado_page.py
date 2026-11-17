# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:55:39 2021

@author: caiop
"""

import pandas as pd
import numpy as np

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class HMI_Mercado(object):
    def __init__(self, HMI):
        self.HMI = HMI
        QToolTip.setFont(QFont('Arial', 12))

    def CreatePage5(self):
        self.CreatePage13() # Mudar isso aqui, criar outro ramo provavelmente. Com loggedIn True da pra salvar preferências pessoais, tipo ativo favorito etc

    def CreatePage13(self):
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Background_2 = QLabel()
        Background_2 = 'rgb(0, 0, 0)'
        self.Background_2.setStyleSheet("background-color: "+Background_2)

        self.Background_3 = QLabel()
        Background_3 = 'rgb(0, 0, 0)'
        self.Background_3.setStyleSheet("background-color: "+Background_3)

        self.Background_4 = QLabel()
        Background_4 = 'rgb(0, 0, 0)'
        self.Background_4.setStyleSheet("background-color: "+Background_4)

        self.HMI.Label_Titulo = QLabel('Análise do mercado')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignCenter)

        self.HMI.Gif_Mercado1 = QLabel()
        self.HMI.Movie_Mercado1 = QMovie("./images/AnaliseDoMercadoGifIcone.gif")
        self.HMI.Movie_Mercado1.setScaledSize(QSize().scaled(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-110), Qt.KeepAspectRatio))
        self.HMI.Gif_Mercado1.setMovie(self.HMI.Movie_Mercado1)
        self.HMI.Movie_Mercado1.start()

        self.HMI.Button_Mercado1 = QPushButton("Análise do Mercado\nModelo Firnas")
        # self.HMI.Button_Mercado1.pressed.connect(lambda: self.HMI.CreatePage('51'))
        self.HMI.Button_Mercado1.setFont(self.HMI.font24)
        self.HMI.Button_Mercado1.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_Mercado1.setFixedSize(int(self.HMI.frameGeometry().width()/3*.96),int(self.HMI.frameGeometry().height()/5))
        self.HMI.Button_Mercado1.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Mercado1.setToolTip("Análise do Mercado Modelo Firnas")

        self.HMI.Button_MercadoInvisivel1 = QPushButton()
        # self.HMI.Button_MercadoInvisivel1.pressed.connect(lambda: self.HMI.CreatePage('51'))
        self.HMI.Button_MercadoInvisivel1.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_MercadoInvisivel1.setFixedSize(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-110))
        self.HMI.Button_MercadoInvisivel1.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_MercadoInvisivel1.setToolTip("Análise do Mercado Modelo Firnas")

        self.HMI.Gif_Mercado2 = QLabel()
        self.HMI.Movie_Mercado2 = QMovie("./images/AnaliseDoMercadoGifIcone.gif")
        self.HMI.Movie_Mercado2.setScaledSize(QSize().scaled(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-110), Qt.KeepAspectRatio))
        self.HMI.Gif_Mercado2.setMovie(self.HMI.Movie_Mercado2)
        self.HMI.Movie_Mercado2.start()

        self.HMI.Button_Mercado2 = QPushButton("Análise do Mercado\nModelo Isa")
        # self.HMI.Button_Mercado2.pressed.connect(lambda: self.HMI.CreatePage('52'))
        self.HMI.Button_Mercado2.setFont(self.HMI.font24)
        self.HMI.Button_Mercado2.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_Mercado2.setFixedSize(int(self.HMI.frameGeometry().width()/3*.96),int(self.HMI.frameGeometry().height()/5))
        self.HMI.Button_Mercado2.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Mercado2.setToolTip("Análise do Mercado Modelo Isa")

        self.HMI.Button_MercadoInvisivel2 = QPushButton()
        # self.HMI.Button_MercadoInvisivel2.pressed.connect(lambda: self.HMI.CreatePage('52'))
        self.HMI.Button_MercadoInvisivel2.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_MercadoInvisivel2.setFixedSize(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-110))
        self.HMI.Button_MercadoInvisivel2.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_MercadoInvisivel2.setToolTip("Análise do Mercado Modelo Isa")

        self.HMI.Gif_Mercado3 = QLabel()
        self.HMI.Movie_Mercado3 = QMovie("./images/AnaliseDoMercadoGifIcone.gif")
        self.HMI.Movie_Mercado3.setScaledSize(QSize().scaled(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-110), Qt.KeepAspectRatio))
        self.HMI.Gif_Mercado3.setMovie(self.HMI.Movie_Mercado3)
        self.HMI.Movie_Mercado3.start()

        self.HMI.Button_Mercado3 = QPushButton("Análise do Mercado\nModelo Cabrero")
        # self.HMI.Button_Mercado3.pressed.connect(lambda: self.HMI.CreatePage('53'))
        self.HMI.Button_Mercado3.setFont(self.HMI.font24)
        self.HMI.Button_Mercado3.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_Mercado3.setFixedSize(int(self.HMI.frameGeometry().width()/3*.96),int(self.HMI.frameGeometry().height()/5))
        self.HMI.Button_Mercado3.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_Mercado3.setToolTip("Análise do Mercado Modelo Cabrero")

        self.HMI.Button_MercadoInvisivel3 = QPushButton()
        # self.HMI.Button_MercadoInvisivel3.pressed.connect(lambda: self.HMI.CreatePage('53'))
        self.HMI.Button_MercadoInvisivel3.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_MercadoInvisivel3.setFixedSize(int(self.HMI.frameGeometry().width()/3*.98),int(self.HMI.frameGeometry().height()*4/5-110))
        self.HMI.Button_MercadoInvisivel3.setCursor(QCursor(Qt.PointingHandCursor))
        self.HMI.Button_MercadoInvisivel3.setToolTip("Análise do Mercado Modelo Cabrero")

        if self.HMI.frameGeometry().width() < self.HMI.screen_width*0.7:
            self.HMI.Button_Mercado1.setFont(self.HMI.font20)
            self.HMI.Button_Mercado2.setFont(self.HMI.font20)
            self.HMI.Button_Mercado3.setFont(self.HMI.font20)
        else:
            self.HMI.Button_Mercado1.setFont(self.HMI.font24)
            self.HMI.Button_Mercado2.setFont(self.HMI.font24)
            self.HMI.Button_Mercado3.setFont(self.HMI.font24)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.Background_1, 0, 0, 1, 3)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.Background_2, 0, 0, 5, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.Background_3, 0, 1, 5, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.Background_4, 0, 2, 5, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 3, Qt.AlignCenter | Qt.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_Mercado1, 0, 0, 4, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_MercadoInvisivel1, 0, 0, 4, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Mercado1, 4, 0, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_Mercado2, 0, 1, 4, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_MercadoInvisivel2, 0, 1, 4, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Mercado2, 4, 1, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_Mercado3, 0, 2, 4, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_MercadoInvisivel3, 0, 2, 4, 1, Qt.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Mercado3, 4, 2, 1, 1)

    def CreatePage51(self):pass

    def CreatePage52(self):pass

    def CreatePage53(self):pass