# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 16:17:33 2021

@author: caiop
"""
import pandas as pd
import numpy as np

import sys
import ctypes
import time

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from BackgroundProcesses import WorkerThread

class OperacaoRegistradaComSucesso(QWidget):
    def __init__(self, HMI, tempo):
        self.HMI = HMI
        self.tempo = tempo
        super().__init__()
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.screen_height = screensize[1] # FHD
        self.screen_width = screensize[0] # FHD
        x_pos = int(self.screen_width/2-int(self.screen_width*0.15))
        y_pos = int(self.screen_height/2+int(self.screen_height*0.15))
        width = int(self.screen_width*0.3)
        height = int(self.screen_height*0.1)
        self.setGeometry(x_pos, y_pos, width, height)

        self.setAutoFillBackground(True)
        background = self.palette()
        background.setColor(self.backgroundRole(), QColor(str('#%02x%02x%02x' % (0,0,0))))
        self.setPalette(background)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.Label_Titulo = QLabel()
        self.Label_Titulo.setStyleSheet('color: green')
        self.Label_Titulo.setFont(self.HMI.font22)
        self.Label_Titulo.setAlignment(Qt.AlignCenter)
        self.Label_Titulo.setText("Operação registrada com sucesso")
        self.layout.addWidget(self.Label_Titulo, Qt.AlignHCenter | Qt.AlignTop)
        self.show()
        self.worker = WorkerThread('Thread_EsmaecerMsgSucesso', self.HMI)
        self.worker.start()

    def Esmaecer(self):
        tempo = self.tempo*10
        for i in range(tempo):
            time.sleep(tempo*0.001)
            self.Label_Titulo.setStyleSheet('color: rgba(20,255,20,'+str((tempo-i)/tempo)+');')
        self.close()