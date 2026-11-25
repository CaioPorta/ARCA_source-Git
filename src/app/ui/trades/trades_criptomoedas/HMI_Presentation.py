# -*- coding: utf-8 -*-
"""
Criptomoedas behaviour split into a single concern.
HMI_Presentation - presentation helpers (inherited by the composition root).
"""
from PyQt5.QtGui import (QColor, QBrush)
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QAbstractScrollArea,
    QAbstractItemView,
)
from PyQt5.QtCore import (Qt)


class HMI_Presentation:
    def CreateTable_40_1(self):
        HHeader = ['Data',
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        fakedata = [('','','','','','','','','')]

        self.HMI.Table_Operacoes_RealizadasHeader.setRowCount(1)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnCount(len(HHeader))

        self.HMI.Table_Operacoes_RealizadasHeader.setShowGrid(False)
        self.HMI.Table_Operacoes_RealizadasHeader.setFont(self.HMI.font14)
        self.HMI.Table_Operacoes_RealizadasHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_Operacoes_RealizadasHeader.verticalHeader().hide()
        self.HMI.Table_Operacoes_RealizadasHeader.horizontalHeader().hide()

        for col in range(len(HHeader)):
            it = QTableWidgetItem(str(HHeader[col]))
            it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            it.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            self.HMI.Table_Operacoes_RealizadasHeader.setItem(0, col, it)

        self.HMI.Table_Operacoes_RealizadasHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_RealizadasHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.HMI.Table_Operacoes_RealizadasHeader.resizeColumnsToContents()

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
        self.HMI.Table_Operacoes_RealizadasHeader.adjustSize()
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(7, SizeCol7)


    def CreateTable_40_2(self):
        self.HMI.Table_Operacoes_Realizadas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_Realizadas.setFixedHeight(int(self.HMI.frameGeometry().height()*6/20*1.4))

        self.HMI.Table_Operacoes_Realizadas.setShowGrid(False)
        self.HMI.Table_Operacoes_Realizadas.setFont(self.HMI.font12)
        self.HMI.Table_Operacoes_Realizadas.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                            color: white;
                                                                            border: 1px solid rgba(0, 0, 0, 0);}
                                                              QTableView {border-bottom: 2px dashed white;
                                                                          border-right: 1px solid white;
                                                                          border-left: 1px solid white;}
                                                              QTableView::item {border-bottom: 1px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
        self.HMI.Table_Operacoes_Realizadas.verticalHeader().hide()
        self.HMI.Table_Operacoes_Realizadas.horizontalHeader().hide()
        self.HMI.Table_Operacoes_Realizadas.setSelectionBehavior(QAbstractItemView.SelectRows)

        HHeader = ['Data',
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        self.data_40_1 = self.HMI.DBManager.GetAllOperacoes(self.HMI.DTeST)
        self.data_40_1 = self.data_40_1[::-1]
        self.HMI.Table_Operacoes_Realizadas.setRowCount(len(self.data_40_1))
        self.HMI.Table_Operacoes_Realizadas.setColumnCount(len(HHeader))
        for i, item in enumerate(self.data_40_1):
            for j in range(len(item)):
                if isinstance(item[j], float):
                    if self.HMI.ShowValues:
                        text = str('%.8f' % item[j])
                    else:
                        text = "***"
                else:
                    text = str(item[j])

                it = self.HMI.Table_Operacoes_Realizadas.item(i, j)
                it = QTableWidgetItem(text)
                it.setFlags(it.flags() & ~Qt.ItemIsEditable) # selecionar a linha inteira
                if not self.HMI.DTeST == "": it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if "VAZIO" in item: it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
                if text in ["Compra", "Drop", "Depósito"]: it.setForeground(QBrush(QColor('green')))
                elif text in ["Venda", "Burn", "Saque"]: it.setForeground(QBrush(QColor('red')))
                if j == 8:
                    it.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                self.HMI.Table_Operacoes_Realizadas.setItem(i, j, it)

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(self.data_40_1, HHeader)

        self.HMI.Table_Operacoes_RealizadasHeader.adjustSize()
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_RealizadasHeader.setColumnWidth(7, SizeCol7)

        self.HMI.Table_Operacoes_Realizadas.adjustSize()
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(7, SizeCol7)
        self.HMI.Table_Operacoes_Realizadas.setColumnWidth(8, SizeCol8)


    def CreateTable_40_3(self):
        HHeader = ['Moeda',
                   'Estoque']
        fakedata = [('','')]

        self.HMI.Table_EstoqueHeader.setRowCount(1)
        self.HMI.Table_EstoqueHeader.setColumnCount(len(HHeader))

        self.HMI.Table_EstoqueHeader.setShowGrid(False)
        self.HMI.Table_EstoqueHeader.setFont(self.HMI.font14)
        self.HMI.Table_EstoqueHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_EstoqueHeader.verticalHeader().hide()
        self.HMI.Table_EstoqueHeader.horizontalHeader().hide()

        for col in range(len(HHeader)):
            it = QTableWidgetItem(str(HHeader[col]))
            it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            it.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            self.HMI.Table_EstoqueHeader.setItem(0, col, it)

        self.HMI.Table_EstoqueHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_EstoqueHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/28))
        self.HMI.Table_EstoqueHeader.setFixedWidth(int(self.HMI.frameGeometry().width() * 5 / 40 * 1.1))
        self.HMI.Table_EstoqueHeader.resizeColumnsToContents()

        SizeCol0, SizeCol1 = 100, 100
        self.HMI.Table_EstoqueHeader.adjustSize()
        self.HMI.Table_EstoqueHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_EstoqueHeader.setColumnWidth(1, SizeCol1)


    def CreateTable_40_4(self):
        self.HMI.Table_Estoque.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Estoque.setFixedHeight(int(self.HMI.frameGeometry().height()*2/20))
        self.HMI.Table_Estoque.setFixedWidth(int(self.HMI.frameGeometry().width() * 5 / 40*1.1))

        self.HMI.Table_Estoque.setShowGrid(False)
        self.HMI.Table_Estoque.setFont(self.HMI.font12)
        self.HMI.Table_Estoque.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                            color: white;
                                                                            border: 1px solid rgba(0, 0, 0, 0);}
                                                              QTableView {border-bottom: 2px dashed white;
                                                                          border-right: 1px solid white;
                                                                          border-left: 1px solid white;}
                                                              QTableView::item {border-bottom: 1px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
        self.HMI.Table_Estoque.verticalHeader().hide()
        self.HMI.Table_Estoque.horizontalHeader().hide()
        self.HMI.Table_Estoque.setSelectionBehavior(QAbstractItemView.SelectRows)

        HHeader = ['Moeda',
                   'Estoque']
        self.data_40_3 = self.HMI.DBManager.GetAllAtivosPorCorretora_Cripto(self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Table_Estoque.setRowCount(len(self.data_40_3))
        self.HMI.Table_Estoque.setColumnCount(len(HHeader))
        for i, item in enumerate(self.data_40_3):
            for j in range(len(item)):
                if isinstance(item[j], float):
                    if self.HMI.ShowValues:
                        text = str('%.8f' % item[j])
                    else:
                        text = "***"
                else:
                    text = str(item[j])

                it = self.HMI.Table_Estoque.item(i, j)
                it = QTableWidgetItem(text)
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
                self.HMI.Table_Estoque.setItem(i, j, it)

        SizeCol0, SizeCol1 = int(self.HMI.frameGeometry().width() * 2 / 40), int(self.HMI.frameGeometry().width() * 3 / 40)

        self.HMI.Table_EstoqueHeader.adjustSize()
        self.HMI.Table_EstoqueHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_EstoqueHeader.setColumnWidth(1, SizeCol1)

        self.HMI.Table_Estoque.adjustSize()
        self.HMI.Table_Estoque.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Estoque.setColumnWidth(1, SizeCol1)


    def CreateTable_43_1(self):
        HHeader = ['Data',
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        fakedata = [('','','','','','','','','')]

        self.HMI.Table_Operacoes_SelecionadasHeader.setRowCount(1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnCount(len(HHeader))

        self.HMI.Table_Operacoes_SelecionadasHeader.setShowGrid(False)
        self.HMI.Table_Operacoes_SelecionadasHeader.setFont(self.HMI.font14)
        self.HMI.Table_Operacoes_SelecionadasHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_Operacoes_SelecionadasHeader.verticalHeader().hide()
        self.HMI.Table_Operacoes_SelecionadasHeader.horizontalHeader().hide()

        for col in range(len(HHeader)):
            it = QTableWidgetItem(str(HHeader[col]))
            it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            it.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            self.HMI.Table_Operacoes_SelecionadasHeader.setItem(0, col, it)

        self.HMI.Table_Operacoes_SelecionadasHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_SelecionadasHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.HMI.Table_Operacoes_SelecionadasHeader.resizeColumnsToContents()

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
        self.HMI.Table_Operacoes_SelecionadasHeader.adjustSize()
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(7, SizeCol7)


    def CreateTable_43_2(self):
        self.HMI.Table_Operacoes_Selecionadas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_Selecionadas.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))

        self.HMI.Table_Operacoes_Selecionadas.setShowGrid(False)
        self.HMI.Table_Operacoes_Selecionadas.setFont(self.HMI.font12)
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
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        self.HMI.Table_Operacoes_Selecionadas.setRowCount(1)
        self.HMI.Table_Operacoes_Selecionadas.setColumnCount(len(HHeader))
        for i, item in enumerate(self.data_40_1):
            if i == self.Operacoes[self.item]:
                for j in range(len(item)):
                    if isinstance(item[j], float):
                        text = str('%.8f' % item[j])
                    else:
                        text = str(item[j])
                    it = self.HMI.Table_Operacoes_Selecionadas.item(0, j)
                    it = QTableWidgetItem(text)
                    it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if text in ["Compra", "Drop", "Depósito"]: it.setForeground(QBrush(QColor('green')))
                    elif text in ["Venda", "Burn", "Saque"]: it.setForeground(QBrush(QColor('red')))
                    if j == 8:
                        it.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                    self.HMI.Table_Operacoes_Selecionadas.setItem(0, j, it)

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(self.data_40_1, HHeader)

        self.HMI.Table_Operacoes_SelecionadasHeader.adjustSize()
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(7, SizeCol7)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(8, SizeCol8)

        self.HMI.Table_Operacoes_Selecionadas.adjustSize()
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(7, SizeCol7)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(8, SizeCol8)


    def CreateTable_44_1(self):
        HHeader = ['Data',
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        fakedata = [('','','','','','','','','')]

        self.HMI.Table_Operacoes_SelecionadasHeader.setRowCount(1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnCount(len(HHeader))

        self.HMI.Table_Operacoes_SelecionadasHeader.setShowGrid(False)
        self.HMI.Table_Operacoes_SelecionadasHeader.setFont(self.HMI.font14)
        self.HMI.Table_Operacoes_SelecionadasHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                           color: white;
                                                                                           border: 1px solid rgba(0, 0, 0, 0);}
                                                                             QTableView {border-top: 2px solid white;
                                                                                         border-right: 2px dashed white;
                                                                                         border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_Operacoes_SelecionadasHeader.verticalHeader().hide()
        self.HMI.Table_Operacoes_SelecionadasHeader.horizontalHeader().hide()

        for col in range(len(HHeader)):
            it = QTableWidgetItem(str(HHeader[col]))
            it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            it.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            self.HMI.Table_Operacoes_SelecionadasHeader.setItem(0, col, it)

        self.HMI.Table_Operacoes_SelecionadasHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_SelecionadasHeader.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.HMI.Table_Operacoes_SelecionadasHeader.resizeColumnsToContents()

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
        self.HMI.Table_Operacoes_SelecionadasHeader.adjustSize()
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(7, SizeCol7)


    def CreateTable_44_2(self):
        self.HMI.Table_Operacoes_Selecionadas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Operacoes_Selecionadas.setFixedHeight(int(self.HMI.frameGeometry().height()*6/20*1.4))

        self.HMI.Table_Operacoes_Selecionadas.setShowGrid(False)
        self.HMI.Table_Operacoes_Selecionadas.setFont(self.HMI.font12)
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
                   'Par',
                   'Tipo',
                   'Preço',
                   'Qqt',
                   'Taxa',
                   'Moeda da taxa',
                   'Conversão',
                   'Obs']
        self.HMI.Table_Operacoes_Selecionadas.setRowCount(len(self.Operacoes))
        self.HMI.Table_Operacoes_Selecionadas.setColumnCount(len(HHeader))
        linha = -1
        for i, item in enumerate(self.data_40_1):
            if i in self.Operacoes:
                linha += 1
                for j in range(len(item)):
                    if isinstance(item[j], float):
                        text = str('%.8f' % item[j])
                    else:
                        text = str(item[j])
                    it = self.HMI.Table_Operacoes_Selecionadas.item(linha, j)
                    it = QTableWidgetItem(text)
                    it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if text in ["Compra", "Drop", "Depósito"]: it.setForeground(QBrush(QColor('green')))
                    elif text in ["Venda", "Burn", "Saque"]: it.setForeground(QBrush(QColor('red')))
                    if j == 8:
                        it.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                    self.HMI.Table_Operacoes_Selecionadas.setItem(linha, j, it)

        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.HMI.GetSizeOfTableColumns(self.data_40_1, HHeader)

        self.HMI.Table_Operacoes_SelecionadasHeader.adjustSize()
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(7, SizeCol7)
        self.HMI.Table_Operacoes_SelecionadasHeader.setColumnWidth(8, SizeCol8)

        self.HMI.Table_Operacoes_Selecionadas.adjustSize()
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(0, SizeCol0)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(1, SizeCol1)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(2, SizeCol2)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(3, SizeCol3)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(4, SizeCol4)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(5, SizeCol5)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(6, SizeCol6)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(7, SizeCol7)
        self.HMI.Table_Operacoes_Selecionadas.setColumnWidth(8, SizeCol8)
