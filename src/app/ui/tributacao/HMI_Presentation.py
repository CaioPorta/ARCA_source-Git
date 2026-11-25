# -*- coding: utf-8 -*-
"""
Tributacao behaviour split into a single concern.
HMI_Presentation - presentation helpers (inherited by the composition root).
"""
from datetime import (datetime)
from PyQt5.QtGui import (QColor, QBrush)
from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, QAbstractScrollArea)
from PyQt5.QtCore import (Qt)


class HMI_Presentation:
    def CreateTable_51_1(self):
        if not self.HMI.DTeST_51 == "DTeST":
            HHeader = ['Mês/Ano',
                       'Resultado líquido',
                       'Imposto devido',
                       'Alíquota',
                       'Lucro mínimo taxável',
                       'Resultado bruto',
                       'Prejuízo acumulado',
                       'Resultado final']
            fakedata = [('','','','','','','','')]
        else:
            HHeader = ['Mês/Ano',
                       'Resultado líquido',
                       'Imposto devido',
                       'Resultado bruto',
                       'Prejuízo acumulado',
                       'Resultado final']
            fakedata = [('','','','','','')]

        self.HMI.Table_Tributacao_Header.setRowCount(1)
        self.HMI.Table_Tributacao_Header.setColumnCount(len(HHeader))

        self.HMI.Table_Tributacao_Header.setShowGrid(False)
        self.HMI.Table_Tributacao_Header.setFont(self.HMI.font16)
        self.HMI.Table_Tributacao_Header.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                        color: white;
                                                                        border: 1px solid rgba(0, 0, 0, 0);}
                                                            QTableView {border-top: 2px solid white;
                                                                        border-right: 2px dashed white;
                                                                        border-left: 2px dashed white;}
                                                            QTableView::item {border-right: 1px dashed white}''') # gridline-color: rgba(255, 255, 255, 0)

        self.HMI.Table_Tributacao_Header.verticalHeader().hide()
        self.HMI.Table_Tributacao_Header.horizontalHeader().hide()

        for col in range(len(HHeader)):
            celula = QTableWidgetItem(str(HHeader[col]))
            celula.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            celula.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            self.HMI.Table_Tributacao_Header.setItem(0, col, celula)

        self.HMI.Table_Tributacao_Header.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Tributacao_Header.setFixedHeight(int(self.HMI.frameGeometry().height()*1/20))
        self.HMI.Table_Tributacao_Header.resizeColumnsToContents()

        if not self.HMI.DTeST_51 == "DTeST":
            SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
            self.HMI.Table_Tributacao_Header.adjustSize()
            self.HMI.Table_Tributacao_Header.setColumnWidth(0, SizeCol0)
            self.HMI.Table_Tributacao_Header.setColumnWidth(1, SizeCol1)
            self.HMI.Table_Tributacao_Header.setColumnWidth(2, SizeCol2)
            self.HMI.Table_Tributacao_Header.setColumnWidth(3, SizeCol3)
            self.HMI.Table_Tributacao_Header.setColumnWidth(4, SizeCol4)
            self.HMI.Table_Tributacao_Header.setColumnWidth(5, SizeCol5)
            self.HMI.Table_Tributacao_Header.setColumnWidth(6, SizeCol6)
            self.HMI.Table_Tributacao_Header.setColumnWidth(7, SizeCol7)
        else:
            SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5 = self.HMI.GetSizeOfTableColumns(fakedata, HHeader)
            self.HMI.Table_Tributacao_Header.adjustSize()
            self.HMI.Table_Tributacao_Header.setColumnWidth(0, SizeCol0)
            self.HMI.Table_Tributacao_Header.setColumnWidth(1, SizeCol1)
            self.HMI.Table_Tributacao_Header.setColumnWidth(2, SizeCol2)
            self.HMI.Table_Tributacao_Header.setColumnWidth(3, SizeCol3)
            self.HMI.Table_Tributacao_Header.setColumnWidth(4, SizeCol4)
            self.HMI.Table_Tributacao_Header.setColumnWidth(5, SizeCol5)


    def CreateTable_51_2(self):
        self.HMI.Table_Tributacao.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.HMI.Table_Tributacao.setFixedHeight(int(self.HMI.frameGeometry().height()*6/20*1.4))
        self.HMI.Table_Tributacao.setShowGrid(False)
        self.HMI.Table_Tributacao.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                 color: white;
                                                                 border: 1px solid rgba(0, 0, 0, 0);}
                                                   QTableView {border-bottom: 2px dashed white;
                                                               border-right: 1px solid white;
                                                               border-left: 1px solid white;}
                                                   QTableView::item {border-bottom: 1px dashed white;border-right: 1px dashed white}''') # gridline-color: rgba(255, 255, 255, 0)
        self.HMI.Table_Tributacao.verticalHeader().hide()
        self.HMI.Table_Tributacao.horizontalHeader().hide()

        #Create Thread
        if not self.HMI.DTeST_51 == "DTeST":
            HHeader = ['Mês/Ano',
                       'Resultado líquido',
                       'Imposto devido',
                       'Alíquota',
                       'Lucro mínimo taxável',
                       'Resultado bruto',
                       'Prejuízo acumulado',
                       'Resultado final']
            if int(self.HMI.frameGeometry().width()*6/20*1.4) < 510:
                self.HMI.Table_Tributacao_Header.setFont(self.HMI.font10)
                self.HMI.Table_Tributacao.setFont(self.HMI.font10)
            else:
                self.HMI.Table_Tributacao_Header.setFont(self.HMI.font14)
                self.HMI.Table_Tributacao.setFont(self.HMI.font14)
        else:
            HHeader = ['Mês/Ano',
                       'Resultado líquido',
                       'Imposto devido',
                       'Resultado bruto',
                       'Prejuízo acumulado',
                       'Resultado final']
            self.HMI.Table_Tributacao_Header.setFont(self.HMI.font14)
            self.HMI.Table_Tributacao.setFont(self.HMI.font14)
        self.data_51_1 = self.HMI.DBManager.GetAllTributacoes()
        self.data_51_1 = self.data_51_1[::-1]
        self.HMI.Table_Tributacao.setRowCount(len(self.data_51_1))
        self.HMI.Table_Tributacao.setColumnCount(len(HHeader))
        for i, item in enumerate(self.data_51_1):
            for j in range(len(item)):
                it = self.HMI.Table_Tributacao.item(i, j)
                if self.HMI.ShowValues:
                    if j == 0: text = datetime.strptime(item[j], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
                    elif '%' in str(item[j]): text = str(round(item[j],2))+'%'
                    else: text = str(round(abs(item[j]),2))
                    it = QTableWidgetItem(text)
                    it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable)) # Desabilita selecionar o item
                    it.setFlags(it.flags() & ~Qt.ItemIsEditable) # Desabilita a edição do item
                else:
                    # Filtrar colunas que não serão mostradas
                    if not self.HMI.DTeST_51 == "DTeST":
                        if j in [1,2,5,6,7]: text = '***'
                        elif j == 0: text = datetime.strptime(item[j], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
                        else: text = str(item[j])
                    else:
                        if not j == 0: text = '***'
                        else: text = datetime.strptime(item[j], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
                    it = QTableWidgetItem(text)
                    # Desabilitar todos os itens
                    it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable)) # Desabilita selecionar o item
                    it.setFlags(it.flags() & ~Qt.ItemIsEditable) # Desabilita a edição do item
                if j == 0: pass
                elif not '%' in str(item[j]) and float(item[j]) < 0: it.setForeground(QBrush(QColor('orange')))
                else: it.setForeground(QBrush(QColor(0, 255, 0)))

                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.HMI.Table_Tributacao.setItem(i, j, it)


        if not self.HMI.DTeST_51 == "DTeST":
            SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.HMI.GetSizeOfTableColumns(self.data_51_1, HHeader)

            self.HMI.Table_Tributacao_Header.adjustSize()
            self.HMI.Table_Tributacao_Header.setColumnWidth(0, SizeCol0)
            self.HMI.Table_Tributacao_Header.setColumnWidth(1, SizeCol1)
            self.HMI.Table_Tributacao_Header.setColumnWidth(2, SizeCol2)
            self.HMI.Table_Tributacao_Header.setColumnWidth(3, SizeCol3)
            self.HMI.Table_Tributacao_Header.setColumnWidth(4, SizeCol4)
            self.HMI.Table_Tributacao_Header.setColumnWidth(5, SizeCol5)
            self.HMI.Table_Tributacao_Header.setColumnWidth(6, SizeCol6)
            self.HMI.Table_Tributacao_Header.setColumnWidth(7, SizeCol7)

            self.HMI.Table_Tributacao.adjustSize()
            self.HMI.Table_Tributacao.setColumnWidth(0, SizeCol0)
            self.HMI.Table_Tributacao.setColumnWidth(1, SizeCol1)
            self.HMI.Table_Tributacao.setColumnWidth(2, SizeCol2)
            self.HMI.Table_Tributacao.setColumnWidth(3, SizeCol3)
            self.HMI.Table_Tributacao.setColumnWidth(4, SizeCol4)
            self.HMI.Table_Tributacao.setColumnWidth(5, SizeCol5)
            self.HMI.Table_Tributacao.setColumnWidth(6, SizeCol6)
            self.HMI.Table_Tributacao.setColumnWidth(7, SizeCol7)
        else:
            SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5 = self.HMI.GetSizeOfTableColumns(self.data_51_1, HHeader)

            self.HMI.Table_Tributacao_Header.adjustSize()
            self.HMI.Table_Tributacao_Header.setColumnWidth(0, SizeCol0)
            self.HMI.Table_Tributacao_Header.setColumnWidth(1, SizeCol1)
            self.HMI.Table_Tributacao_Header.setColumnWidth(2, SizeCol2)
            self.HMI.Table_Tributacao_Header.setColumnWidth(3, SizeCol3)
            self.HMI.Table_Tributacao_Header.setColumnWidth(4, SizeCol4)
            self.HMI.Table_Tributacao_Header.setColumnWidth(5, SizeCol5)

            self.HMI.Table_Tributacao.adjustSize()
            self.HMI.Table_Tributacao.setColumnWidth(0, SizeCol0)
            self.HMI.Table_Tributacao.setColumnWidth(1, SizeCol1)
            self.HMI.Table_Tributacao.setColumnWidth(2, SizeCol2)
            self.HMI.Table_Tributacao.setColumnWidth(3, SizeCol3)
            self.HMI.Table_Tributacao.setColumnWidth(4, SizeCol4)
            self.HMI.Table_Tributacao.setColumnWidth(5, SizeCol5)
