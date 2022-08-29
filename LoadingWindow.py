# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 13:08:15 2021

@author: caiop
"""

import pandas as pd
import numpy as np

import ctypes

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class LoadingWindow(QWidget):
    def __init__(self, HMI):
        self.HMI = HMI
        self.DBManager = HMI.DBManager
        super().__init__()

        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.screen_height = screensize[1] # FHD
        self.screen_width = screensize[0] # FHD

        self.setAutoFillBackground(True)
        background = self.palette()
        background.setColor(self.backgroundRole(), QColor(str('#%02x%02x%02x' % (5, 8, 15))))
        self.setPalette(background)
        self.setFixedSize(QSize(int(self.screen_width*0.3), int(self.screen_height*0.2)))
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.Label_Titulo = QLabel()
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.HMI.font14)
        self.Label_Titulo.setAlignment(Qt.AlignCenter)
        self.Label_Titulo.setText("Por favor aguarde...")

        self.pbar = QProgressBar()
        self.pbar.setValue(0)
        self.layout.addWidget(self.Label_Titulo)
        self.layout.addWidget(self.pbar)