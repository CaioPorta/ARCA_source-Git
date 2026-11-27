# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:54:52 2021

@author: Caio Moreira Porta
"""
from datetime import datetime
import traceback

from PyQt5.QtGui import (
    QFont, QCursor,
    QIcon, QColor, QMovie,
    QBrush, QIntValidator, QDoubleValidator
)
from PyQt5.QtWidgets import (
    QLabel, QPushButton, QLineEdit,
    QComboBox, QHBoxLayout, QVBoxLayout,
    QToolTip, QMessageBox,
    QTableWidget, QTableWidgetItem,
    QAbstractScrollArea, QCompleter, QAbstractItemView
)
from PyQt5.QtCore import (
    QSize, Qt
)

from ui.pages import PAGE_BY_NAME


class HMI_Presentation:
    """Table rendering / presentation helpers (CreateTable*) for HMI_Trades_Bolsa."""
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
            celula.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            celula.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
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
        self.data_23_1 = self.HMI.DBManager.GetAllOperacoes(self.HMI.BolsaOuCripto,
                                                            self.HMI.ComboBox_Corretoras.currentText(),
                                                            self.HMI.ComboBox_Ativos.currentText(),
                                                            self.HMI.DTeST,
                                                            )
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
                if not self.HMI.DTeST == "": it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if "VAZIO" in item: it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
                if text in ["Compra"]: it.setForeground(QBrush(QColor('green')))
                elif text in ["Venda"]: it.setForeground(QBrush(QColor('red')))
                if j == 7:
                    it.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
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
            celula.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            celula.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
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
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
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
            celula.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            celula.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
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
                    it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if text in ["Compra"]: it.setForeground(QBrush(QColor('green')))
                    elif text in ["Venda"]: it.setForeground(QBrush(QColor('red')))
                    if j == 7:
                        it.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
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
            celula.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            celula.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
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
                    it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if text in ["Compra"]: it.setForeground(QBrush(QColor('green')))
                    elif text in ["Venda"]: it.setForeground(QBrush(QColor('red')))
                    if j == 7:
                        it.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
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

