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


class HMI_Events:
    """Button/event handlers (OnButtonPressed) for HMI_Trades_Bolsa."""
    def OnButtonPressed(self, ButtonPressed):
        if ButtonPressed == 'ChangeDTeST':
            if self.HMI.DTeST == "": self.HMI.DTeST = "DTeST"
            elif self.HMI.DTeST == "DTeST": self.HMI.DTeST = "ST"
            elif self.HMI.DTeST == "ST": self.HMI.DTeST = "DT"
            elif self.HMI.DTeST == "DT": self.HMI.DTeST = ""

            if self.HMI.DTeST == "":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Trades Brutos.png"))
                # Habilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(True)
                self.HMI.Button_DeletarOperacao.setEnabled(True)
            elif self.HMI.DTeST == "DTeST":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Day Trades e Swing Trades.png"))
                # Desabilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(False)
                self.HMI.Button_DeletarOperacao.setEnabled(False)
            elif self.HMI.DTeST == "ST":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas ST.png"))
                # Desabilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(False)
                self.HMI.Button_DeletarOperacao.setEnabled(False)
            elif self.HMI.DTeST == "DT":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas DT.png"))
                # Desabilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(False)
                self.HMI.Button_DeletarOperacao.setEnabled(False)

            if self.HMI.PageID == PAGE_BY_NAME['RegistrosBolsa'].page_id:
                self.HMI.Table_Operacoes_Realizadas_com_Ativo.deleteLater()
                self.HMI.Table_Operacoes_Realizadas_com_Ativo = QTableWidget()
                self.HMI.HMI_Trades.HMI_Trades_Bolsa.CreateTable_23_2()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas_com_Ativo, 6, 0, 6, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

            if self.HMI.PageID == PAGE_BY_NAME['RegistrosCripto'].page_id:
                self.HMI.Table_Operacoes_Realizadas.deleteLater()
                self.HMI.Table_Operacoes_Realizadas = QTableWidget()
                self.HMI.HMI_Trades.HMI_Trades_Criptomoedas.CreateTable_40_2()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas, 6, 0, 6, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

            elif self.HMI.PageID == PAGE_BY_NAME['Tributacao'].page_id:
                if self.HMI.DTeST_51 == "DTeST": self.HMI.DTeST_51 = "ST"
                elif self.HMI.DTeST_51 == "ST": self.HMI.DTeST_51 = "DT"
                elif self.HMI.DTeST_51 == "DT": self.HMI.DTeST_51 = "DTeST"

                if self.HMI.DTeST_51 == "DTeST":
                    self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Day Trades e Swing Trades.png"))
                elif self.HMI.DTeST_51 == "ST":
                    self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas ST.png"))
                elif self.HMI.DTeST_51 == "DT":
                    self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas DT.png"))
                self.HMI.Table_Tributacao_Header.deleteLater()
                self.HMI.Table_Tributacao_Header = QTableWidget()
                self.HMI.HMI_Tributacao.CreateTable_51_1()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Tributacao_Header, 5, 0, 1, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
                self.HMI.Table_Tributacao.deleteLater()
                self.HMI.Table_Tributacao = QTableWidget()
                self.HMI.HMI_Tributacao.CreateTable_51_2()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Tributacao, 6, 0, 6, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        elif ButtonPressed == 'Deposito':
            self.HMI.Button_Deposito.setStyleSheet('background-color: black; color: green')
            self.HMI.Button_Deposito.setText("DEPÓSITO")
            self.HMI.Button_Deposito.setFont(self.HMI.font20)
            self.HMI.Button_Saque.setStyleSheet('background-color: black; color: gray')
            self.HMI.Button_Saque.setText("saque")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Deposito = True
            self.HMI.TextBox_Valor.setStyleSheet('color: green')
            BackgroundLineEdit = "rgb(0,10,30)"
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: green")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: green")
            self.HMI.TextBox_Valor.setFocus()

        elif ButtonPressed == 'Saque':
            self.HMI.Button_Deposito.setStyleSheet('background-color: black; color: gray')
            self.HMI.Button_Deposito.setText("depósito")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setStyleSheet('background-color: black; color: orange')
            self.HMI.Button_Saque.setText("SAQUE")
            self.HMI.Button_Saque.setFont(self.HMI.font20)
            self.HMI.Deposito = False
            self.HMI.TextBox_Valor.setStyleSheet('color: orange')
            BackgroundLineEdit = "rgb(0,10,30)"
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: orange")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: orange")
            self.HMI.TextBox_Valor.setFocus()

        elif ButtonPressed == 'Delete Registro':
            if not self.HMI.DBManager.CalcularTributacao_is_running:
                TotalSelecao=[]
                for idx in self.HMI.Table_DepositosESaques.selectedIndexes():
                    TotalSelecao.append(idx.row())
                TotalSelecao = list(dict.fromkeys(TotalSelecao))
                MessageBox_Msg1 = QMessageBox()
                MessageBox_Msg1.setWindowTitle("Deletar registros de movimentações")
                MessageBox_Msg1.setText("Tem certeza que deseja deletar "+str(len(TotalSelecao))+" registros?\n\n")
                MessageBox_Msg1.setIcon(QMessageBox.Warning)
                MessageBox_Msg1.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
                MessageBox_Msg1.setDefaultButton(QMessageBox.Cancel)
                MessageBox_Msg1.setWindowIcon(QIcon(".\\images\\logoARCA.png"))

                returnValue = MessageBox_Msg1.exec()
                if returnValue == QMessageBox.Yes:
                    DeuBom = self.HMI.DBManager.DeleteDepositoOuSaque(self.HMI.BolsaOuCripto,
                                                                    self.HMI.ComboBox_Corretoras.currentText(),
                                                                    TotalSelecao,
                                                                    self.HMI.HMI_Trades.HMI_Trades_Bolsa.data_24_1,
                                                                    )
                    if DeuBom:
                        self.HMI.HMI_Presentation.UpdatePatrimonioRendimento()
                        self.HMI.CreatePage(PAGE_BY_NAME['InformarDepositosSaqBolsa'].page_id)
            else:
                MessageBox_Msg1 = QMessageBox.about(self.HMI,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')

        elif ButtonPressed == 'Compra':
            BackgroundLineEdit = "rgb(0,10,30)"
            FontColorLineEdit = "green"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("COMPRA")
            self.HMI.Button_Compra.setFont(self.HMI.font20)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("venda")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Desdobramento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Grupamento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Bonificacao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Modo.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Corretagem.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_TaxaB3.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TipoDeOperacao = "Compra"
            if "Desdobramento;" in self.HMI.TextBox_Obs.text() or "Grupamento;" in self.HMI.TextBox_Obs.text():
                self.HMI.TextBox_Corretagem.setText("0")
                self.HMI.TextBox_TaxaB3.setText("0")
            self.HMI.TextBox_Qqt.setFocus()

        elif ButtonPressed == 'Venda':
            BackgroundLineEdit = "rgb(30,5,10)"
            FontColorLineEdit = "orange"
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setText("compra")
            self.HMI.Button_Compra.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setText("VENDA")
            self.HMI.Button_Venda.setFont(self.HMI.font20)
            self.HMI.Button_Desdobramento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Grupamento.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Bonificacao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Modo.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Corretagem.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_TaxaB3.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TipoDeOperacao = "Venda"
            if "Desdobramento;" in self.HMI.TextBox_Obs.text() or "Grupamento;" in self.HMI.TextBox_Obs.text():
                self.HMI.TextBox_Qqt.setText(str(int(self.HMI.DBManager.GetEstoque(self.HMI.BolsaOuCripto,
                                                                                   self.HMI.ComboBox_Corretoras.currentText(),
                                                                                   self.HMI.ComboBox_Ativos.currentText(),
                                                                                   ))))
                self.HMI.TextBox_Preco.setText(str(self.HMI.DBManager.GetPrecoMedio(self.HMI.ComboBox_Ativos.currentText(),
                                                                                    self.HMI.ComboBox_Corretoras.currentText(),
                                                                                    self.HMI.BolsaOuCripto,
                                                                                    )))
                self.HMI.TextBox_Corretagem.setText("0")
                self.HMI.TextBox_TaxaB3.setText("0")
            self.HMI.TextBox_Qqt.setFocus()

        elif ButtonPressed == 'Desdobramento':
            if not "Desdobramento;" in self.HMI.TextBox_Obs.text():
                self.HMI.TextBox_Obs.setText("Desdobramento; "+self.HMI.TextBox_Obs.text().replace("Grupamento; ","").replace("Grupamento;","").replace("Bonificação; ","").replace("Bonificação;",""))
                if self.HMI.TipoDeOperacao == "Venda":
                    self.HMI.TextBox_Qqt.setText(str(int(self.HMI.DBManager.GetEstoque(self.HMI.BolsaOuCripto,
                                                                                       self.HMI.ComboBox_Corretoras.currentText(),
                                                                                       self.HMI.ComboBox_Ativos.currentText(),
                                                                                       ))))
                    self.HMI.TextBox_Preco.setText(str(self.HMI.DBManager.GetPrecoMedio(self.HMI.ComboBox_Ativos.currentText(),
                                                                                        self.HMI.ComboBox_Corretoras.currentText(),
                                                                                        self.HMI.BolsaOuCripto,
                                                                                        )))
                    self.HMI.TextBox_Corretagem.setText("0")
                    self.HMI.TextBox_TaxaB3.setText("0")
                elif self.HMI.TipoDeOperacao == "Compra":
                    self.HMI.TextBox_Corretagem.setText("0")
                    self.HMI.TextBox_TaxaB3.setText("0")
            else:
                self.HMI.TextBox_Obs.setText(self.HMI.TextBox_Obs.text().replace("Desdobramento; ","").replace("Desdobramento;",""))

        elif ButtonPressed == 'Grupamento':
            if not "Grupamento;" in self.HMI.TextBox_Obs.text():
                self.HMI.TextBox_Obs.setText("Grupamento; "+self.HMI.TextBox_Obs.text().replace("Desdobramento; ","").replace("Desdobramento;","").replace("Bonificação; ","").replace("Bonificação;",""))
                if self.HMI.TipoDeOperacao == "Venda":
                    self.HMI.TextBox_Qqt.setText(str(int(self.HMI.DBManager.GetEstoque(self.HMI.BolsaOuCripto,
                                                                                       self.HMI.ComboBox_Corretoras.currentText(),
                                                                                       self.HMI.ComboBox_Ativos.currentText(),
                                                                                       ))))
                    self.HMI.TextBox_Preco.setText(str(self.HMI.DBManager.GetPrecoMedio(self.HMI.ComboBox_Ativos.currentText(),
                                                                                        self.HMI.ComboBox_Corretoras.currentText(),
                                                                                        self.HMI.BolsaOuCripto,
                                                                                        )))
                    self.HMI.TextBox_Corretagem.setText("0")
                    self.HMI.TextBox_TaxaB3.setText("0")
                elif self.HMI.TipoDeOperacao == "Compra":
                    self.HMI.TextBox_Corretagem.setText("0")
                    self.HMI.TextBox_TaxaB3.setText("0")
            else:
                self.HMI.TextBox_Obs.setText(self.HMI.TextBox_Obs.text().replace("Grupamento; ","").replace("Grupamento;",""))

        elif ButtonPressed == 'Bonificação':
            if not "Bonificação;" in self.HMI.TextBox_Obs.text():
                if self.HMI.TipoDeOperacao == "Venda":
                    self.HMI.TextBox_Obs.setText(self.HMI.TextBox_Obs.text().replace("Desdobramento; ","").replace("Desdobramento;","").replace("Grupamento; ","").replace("Grupamento;","").replace("Bonificação; ","").replace("Bonificação;",""))
                elif self.HMI.TipoDeOperacao == "Compra":
                    self.HMI.TextBox_Obs.setText("Bonificação; "+self.HMI.TextBox_Obs.text().replace("Desdobramento; ","").replace("Desdobramento;","").replace("Grupamento; ","").replace("Grupamento;",""))
                    self.HMI.TextBox_Corretagem.setText("0")
                    self.HMI.TextBox_TaxaB3.setText("0")
            else:
                self.HMI.TextBox_Obs.setText(self.HMI.TextBox_Obs.text().replace("Bonificação; ","").replace("Bonificação;",""))

        elif ButtonPressed == "Page29_Next":
            try:
                if not self.HMI.DBManager.CalcularTributacao_is_running:
                    Data = self.HMI.Selecao_Ano+'/'+self.HMI.Selecao_Mes+'/'+self.HMI.Selecao_Dia+" "+self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo
                    Tipo = self.HMI.TipoDeOperacao
                    if "," in self.HMI.TextBox_Qqt.text() or "." in self.HMI.TextBox_Qqt.text():
                        raise ValueError("Valor inválido!")
                    Qqt = int(self.HMI.TextBox_Qqt.text())
                    Preco = float(self.HMI.TextBox_Preco.text().replace(",","."))
                    Corretagem = float(self.HMI.TextBox_Corretagem.text().replace(",","."))
                    if "%" in self.HMI.TextBox_TaxaB3.text():
                        TaxaB3Per = float(self.HMI.TextBox_TaxaB3.text().replace("%","").replace(",","."))
                        TaxaB3 = round(TaxaB3Per/100*Qqt*Preco,2)
                    else:
                        TaxaB3 = float(self.HMI.TextBox_TaxaB3.text().replace(",","."))
                        TaxaB3Per = round(TaxaB3/Qqt/Preco*100,2)
                    Obs = self.HMI.TextBox_Obs.text().replace("ST; ","").replace("DT; ","")
                    Item = len(self.HMI.HMI_Trades.HMI_Trades_Bolsa.data_23_1)-self.HMI.HMI_Trades.HMI_Trades_Bolsa.Operacoes[self.HMI.HMI_Trades.HMI_Trades_Bolsa.item]-1
                    ativo = self.ComboBox_Ativos.currentText()
                    Corretora = self.HMI.ComboBox_Corretoras.currentText()
                    if self.HMI.DBManager.AlterOperacao(self.HMI.BolsaOuCripto,
                                                        Corretora,
                                                        ativo,
                                                        Item,
                                                        Data,
                                                        Tipo,
                                                        Qqt,
                                                        Preco,
                                                        Corretagem,
                                                        TaxaB3,
                                                        TaxaB3Per,
                                                        Obs
                                                        ):
                        # self.CalcularTributacao() # Via thread
                        self.HMI.HMI_Tributacao.CalcularTributacao_SemThread() # Via sequencial
                        self.HMI_Presentation.UpdatePatrimonioRendimento()
                        self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
                        if self.HMI.HMI_Trades.HMI_Trades_Bolsa.item+1 >= len(self.HMI.HMI_Trades.HMI_Trades_Bolsa.Operacoes):
                            self.HMI.CreatePage(PAGE_BY_NAME['RegistrosBolsa'].page_id) # Última alteração da lista
                        else:
                            self.HMI.CreatePage(PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id) # Ir pra próxima alteração
                    else:
                        try: self.HMI.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.HMI.Label_Erro1 = QLabel()
                        self.HMI.Label_Erro1.setStyleSheet('color: red')
                        self.HMI.Label_Erro1.setFont(self.HMI.font12)
                        self.HMI.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.HMI.Label_Erro1.setText('Data inválida.\nTalvez já tenha uma operação nesse momento.') # Substitui a string do erro mais provável
                        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Erro1, 6, 7, 1, 1, Qt.AlignmentFlag.AlignCenter)
                else:
                    MessageBox_Msg1 = QMessageBox.about(self.HMI,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')
            except:
                try: self.HMI.Label_Erro1.deleteLater()
                except Exception as e:
                    print(e, traceback.format_exception(None, e, e.__traceback__))
                self.HMI.Label_Erro1 = QLabel()
                self.HMI.Label_Erro1.setStyleSheet('color: red')
                self.HMI.Label_Erro1.setFont(self.HMI.font12)
                self.HMI.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.HMI.Label_Erro1.setText('Confira os valores inseridos.') # Substitui a string do erro mais provável
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Erro1, 6, 7, 1, 1, Qt.AlignmentFlag.AlignCenter)

        elif ButtonPressed == 'Deletar Ativos da Pagina 23':
            if not self.HMI.DBManager.CalcularTributacao_is_running:
                Corretora = self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")
                table_data = self.HMI.HMI_Trades.HMI_Trades_Bolsa.data_23_1
                ativo = self.HMI.ComboBox_Ativos.currentText().replace(" ","_")
                _, need_CalcularTributacao = self.HMI.DBManager.DeleteOperacao(self.HMI.HMI_Trades.HMI_Trades_Bolsa.Operacoes,
                                                                                table_data,
                                                                                Corretora,
                                                                                self.HMI.BolsaOuCripto,
                                                                                ativo,
                                                                                )
                if need_CalcularTributacao:
                    self.HMI.HMI_Presentation.UpdatePatrimonioRendimento()
                    # self.CalcularTributacao() # Via thread
                    self.HMI.HMI_Tributacao.CalcularTributacao_SemThread() # Via sequencial
                self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
                self.HMI.CreatePage(PAGE_BY_NAME['RegistrosBolsa'].page_id)
            else:
                MessageBox_Msg1 = QMessageBox.about(self.HMI,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')
