"""
Created on Sun Sep  5 01:44:04 2021

@author: Caio Moreira Porta
"""
import os
import sqlite3
import tkinter
from tkinter import filedialog
import xlsxwriter
from openpyxl import load_workbook
import win32com.client as win32
from PIL import Image
from datetime import datetime
from shutil import copyfile
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import (QAbstractScrollArea, QLineEdit, QMessageBox,
                             QPushButton, QTableWidget)
from PyQt5.QtCore import QEvent, QSize, Qt
from core.BackgroundProcesses import BackgroundProcess as BP
from ui.popup.CalendarWindow import CalendarWindow as Calendario
from ui.popup.RelogioWindow import RelogioWindow as Relogio
from ui.pages import PAGE_BY_NAME


class HMI_Events:
    def OnButtonPressed(self, ButtonPressed):
        if ButtonPressed == "ShowHideValues":
            self.HMI_ARCA.Flag_RecalcularGraficos = True
            if self.ShowValues:
                self.ShowValues = not self.ShowValues
                self.Button_ShowHideValues.setIcon(QIcon("./images/iconClosedEye.png"))
                self.TextBox_Patrimonio.setEchoMode(QLineEdit.Password)
            else:
                self.ShowValues = not self.ShowValues
                self.Button_ShowHideValues.setIcon(QIcon("./images/iconOpenEye.png"))
                self.TextBox_Patrimonio.setEchoMode(QLineEdit.Normal)

            if self.PageID== PAGE_BY_NAME['ARCA'].page_id: # ARCA
                try:
                    if self.ShowValues:
                        self.TextBox_Aplicar.setEchoMode(QLineEdit.Normal)
                        self.TextBox_GastoMensal.setEchoMode(QLineEdit.Normal)
                        self.TextBox_GastoMensal.setEnabled(True)
                        self.TextBox_MontanteAplicado.setEchoMode(QLineEdit.Normal)
                        self.TextBox_MontanteEmAplicacao.setEchoMode(QLineEdit.Normal)
                    else:
                        self.TextBox_Aplicar.setEchoMode(QLineEdit.Password)
                        self.TextBox_GastoMensal.setEchoMode(QLineEdit.Password)
                        self.TextBox_GastoMensal.setEnabled(False)
                        self.TextBox_MontanteAplicado.setEchoMode(QLineEdit.Password)
                        self.TextBox_MontanteEmAplicacao.setEchoMode(QLineEdit.Password)
                except: pass
                try:
                    self.GraphWidget_Carteira.deleteLater()
                    if self.HMI_ARCA.CarteiraGraph_id == 'pie': self.GraphWidget_Carteira = self.HMI_ARCA.CreateGraph_Page11_Carteira_pie()
                    else: self.GraphWidget_Carteira = self.HMI_ARCA.CreateGraph_Page11_Carteira_bar()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_Carteira, 2, 2, 2, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
                    self.Button_CarteiraInvisivel.deleteLater()
                    self.Button_CarteiraInvisivel = QPushButton()
                    self.Button_CarteiraInvisivel.pressed.connect(lambda: self.HMI_ARCA.OnButtonPressed('Change Carteira Graph'))
                    self.Button_CarteiraInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
                    if self.frameGeometry().width() / self.frameGeometry().height() < 1.9577: proporcao = 1 / 6
                    elif self.frameGeometry().width() / self.frameGeometry().height() < 2.6202: proporcao = 1 / 8
                    else: proporcao = 1 / 10
                    self.GraphWidget_Carteira.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.Button_CarteiraInvisivel.setFixedSize(int(self.frameGeometry().height()*proporcao),int(self.frameGeometry().height()*proporcao))
                    self.Button_CarteiraInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                    self.F_GLayout[self.GCount-1].addWidget(self.Button_CarteiraInvisivel, 2, 2, 2, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
                except: pass
                try:
                    self.HMI_ARCA.Table_ContasCorrente.deleteLater()
                    self.HMI_ARCA.Table_ContasCorrente = QTableWidget()
                    self.HMI_ARCA.Table_ContasCorrente.setShowGrid(False)
                    self.HMI_ARCA.Table_ContasCorrente.setFont(self.font10)
                    self.HMI_ARCA.Table_ContasCorrente.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                                      color: white;
                                                                                      border: 1px solid rgba(0, 0, 0, 0);}
                                                                        QTableView {border-bottom: 0px dashed white;
                                                                                    border-right: 0px solid white;
                                                                                    border-left: 0px solid white;}
                                                                        QTableView::item {border-bottom: 0.5px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
                    self.HMI_ARCA.Table_ContasCorrente.verticalHeader().hide()
                    self.HMI_ARCA.Table_ContasCorrente.horizontalHeader().hide()
                    self.F_GLayout[self.GCount-1].addWidget(self.HMI_ARCA.Table_ContasCorrente, 3, 4, 2, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
                    self.HMI_ARCA.CreateTable_11_2() # Table_ContasCorrente (Criada com uma thread)
                except: pass

            elif self.PageID== PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id: # BolsaPage
                if self.ShowValues:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Normal)
                    self.TextBox_Msg3.setEchoMode(QLineEdit.Normal)
                    self.TextBox_Msg5.setEchoMode(QLineEdit.Normal)
                    self.TextBox_Msg6.setEchoMode(QLineEdit.Normal)
                else:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Password)
                    self.TextBox_Msg3.setEchoMode(QLineEdit.Password)
                    self.TextBox_Msg5.setEchoMode(QLineEdit.Password)
                    self.TextBox_Msg6.setEchoMode(QLineEdit.Password)

            elif self.PageID== PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id: # CriptomoedasPage
                if self.ShowValues:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Normal)
                    self.TextBox_Msg3.setEchoMode(QLineEdit.Normal)
                    self.TextBox_Msg5.setEchoMode(QLineEdit.Normal)
                    self.TextBox_Msg6.setEchoMode(QLineEdit.Normal)
                else:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Password)
                    self.TextBox_Msg3.setEchoMode(QLineEdit.Password)
                    self.TextBox_Msg5.setEchoMode(QLineEdit.Password)
                    self.TextBox_Msg6.setEchoMode(QLineEdit.Password)

            elif self.PageID== PAGE_BY_NAME['EditacaoContasCorrentesBancos'].page_id: # BancosPage
                if self.ShowValues:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Normal)
                else:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Password)

            elif self.PageID== PAGE_BY_NAME['RegistrosBolsa'].page_id: # RegistrosPage
                if self.ShowValues:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Normal) # Estoque
                else:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Password) # Estoque
                self.HMI_Trades.HMI_Trades_Bolsa.CreateTable_23_2() # Table

            elif self.PageID== PAGE_BY_NAME['InformarDepositosSaqBolsa'].page_id: # Depositos e Saques Page
                if self.ShowValues:
                    self.HMI_Trades.HMI_Trades_Bolsa.CreateTable_24_2() # Table
                else:
                    self.HMI_Trades.HMI_Trades_Bolsa.CreateTable_24_2() # Table

            elif self.PageID== PAGE_BY_NAME['SaldoContaCorrenteBolsa'].page_id: # Conta-corrente Page
                if self.ShowValues:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Normal)
                else:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Password)

            elif self.PageID== PAGE_BY_NAME['RegistrosCripto'].page_id:
                self.HMI_Trades.HMI_Trades_Criptomoedas.CreateTable_40_2() # Table

            elif self.PageID == "46":
                if self.ShowValues:
                    UserCoin = self.DBManager.GetUserCoinCurrency()
                    self.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Custo, 2):.2f}'))
                    self.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Retorno, 2):.2f}'))
                else:
                    self.TextBox_Custo.setText('Custo: X')
                    self.TextBox_Retorno.setText('Retorno: '+str(round((self.HMI_ARCA.Retorno-self.HMI_ARCA.Custo)/self.HMI_ARCA.Custo*100,1))+'%X')
                if self.HMI_ARCA.Retorno >= self.HMI_ARCA.Custo:
                    self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
                else:
                    self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

                self.GraphWidget_MainGraph.deleteLater()
                if self.HMI_ARCA.MainGraphIsShowing == "Visão Geral":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page46_MainGraph_VisaoGeral()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
                elif self.HMI_ARCA.MainGraphIsShowing == "Ativo por corretora":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page46_MainGraph_AtivoPorCorretora()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
                elif self.HMI_ARCA.MainGraphIsShowing == "Ativo por setor":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page46_MainGraph_AtivoPorSetor()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)

                self.GraphWidget_Subtipos.deleteLater()
                self.GraphWidget_Subtipos = self.HMI_ARCA.CreateGraph_Page46_Subtipos()
                self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

            elif self.PageID == "47":
                if self.ShowValues:
                    UserCoin = self.DBManager.GetUserCoinCurrency()
                    self.TextBox_Custo.setText('Custo: '+UserCoin+' '+str(f'{round(self.HMI_ARCA.Custo, 2):.2f}'))
                    self.TextBox_Retorno.setText('Retorno: '+UserCoin+' '+str(f'{round(self.HMI_ARCA.Retorno, 2):.2f}'))
                else:
                    self.TextBox_Custo.setText('Custo: X')
                    self.TextBox_Retorno.setText('Retorno: '+str(round((self.HMI_ARCA.Retorno-self.HMI_ARCA.Custo)/self.HMI_ARCA.Custo*100,1))+'%X')
                if self.HMI_ARCA.Retorno >= self.HMI_ARCA.Custo:
                    self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
                else:
                    self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

                self.GraphWidget_MainGraph.deleteLater()
                if self.HMI_ARCA.MainGraphIsShowing == "Visão Geral":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page47_MainGraph_VisaoGeral()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
                elif self.HMI_ARCA.MainGraphIsShowing == "Ativo por corretora":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page47_MainGraph_AtivoPorCorretora()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
                elif self.HMI_ARCA.MainGraphIsShowing == "Ativo por setor":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page47_MainGraph_AtivoPorSetor()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)

                self.GraphWidget_Subtipos.deleteLater()
                self.GraphWidget_Subtipos = self.HMI_ARCA.CreateGraph_Page47_Subtipos()
                self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

            elif self.PageID == "48":
                if self.ShowValues:
                    UserCoin = self.DBManager.GetUserCoinCurrency()
                    self.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Custo, 2):.2f}'))
                    self.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Retorno, 2):.2f}'))
                else:
                    self.TextBox_Custo.setText('Custo: X')
                    self.TextBox_Retorno.setText('Retorno: '+str(round((self.HMI_ARCA.Retorno-self.HMI_ARCA.Custo)/self.HMI_ARCA.Custo*100,1))+'%X')
                if self.HMI_ARCA.Retorno >= self.HMI_ARCA.Custo:
                    self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
                else:
                    self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

                self.GraphWidget_MainGraph.deleteLater()
                if self.HMI_ARCA.MainGraphIsShowing == "Visão Geral":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page48_MainGraph_VisaoGeral()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
                elif self.HMI_ARCA.MainGraphIsShowing == "Ativo por corretora":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page48_MainGraph_AtivoPorCorretora()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
                elif self.HMI_ARCA.MainGraphIsShowing == "Ativo por setor":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page48_MainGraph_AtivoPorSetor()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)

                self.GraphWidget_Subtipos.deleteLater()
                self.GraphWidget_Subtipos = self.HMI_ARCA.CreateGraph_Page48_Subtipos()
                self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

            elif self.PageID == "49":
                if self.ShowValues:
                    UserCoin = self.DBManager.GetUserCoinCurrency()
                    self.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Custo, 2):.2f}'))
                    self.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Retorno, 2):.2f}'))
                else:
                    self.TextBox_Custo.setText('Custo: X')
                    self.TextBox_Retorno.setText('Retorno: '+str(round((self.HMI_ARCA.Retorno-self.HMI_ARCA.Custo)/self.HMI_ARCA.Custo*100,1))+'%X')
                if self.HMI_ARCA.Retorno >= self.HMI_ARCA.Custo:
                    self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
                else:
                    self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')

                self.GraphWidget_MainGraph.deleteLater()
                if self.HMI_ARCA.MainGraphIsShowing == "Visão Geral":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page49_MainGraph_VisaoGeral()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
                elif self.HMI_ARCA.MainGraphIsShowing == "Ativo por corretora":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page49_MainGraph_AtivoPorCorretora()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
                elif self.HMI_ARCA.MainGraphIsShowing == "Ativo por setor":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page49_MainGraph_AtivoPorSetor()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)

                self.GraphWidget_Subtipos.deleteLater()
                self.GraphWidget_Subtipos = self.HMI_ARCA.CreateGraph_Page49_Subtipos()
                self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

            elif self.PageID == "50":
                if self.ShowValues:
                    UserCoin = self.DBManager.GetUserCoinCurrency()
                    self.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Custo, 2):.2f}'))
                    self.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Retorno, 2):.2f}'))
                else:
                    self.TextBox_Custo.setText('Custo: X')
                    self.TextBox_Retorno.setText('Retorno: '+str(round((self.HMI_ARCA.Retorno-self.HMI_ARCA.Custo)/self.HMI_ARCA.Custo*100,1))+'%X')
                if self.HMI_ARCA.Retorno >= self.HMI_ARCA.Custo:
                    self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
                else:
                    self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')
                self.GraphWidget_MainGraph.deleteLater()
                if self.HMI_ARCA.MainGraphIsShowing == "Visão Geral":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page50_MainGraph_VisaoGeral()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
                elif self.HMI_ARCA.MainGraphIsShowing == "Ativo por corretora":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page50_MainGraph_AtivoPorCorretora()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)
                elif self.HMI_ARCA.MainGraphIsShowing == "Total de UserCoin por corretora":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page50_MainGraph_TotalDeUserCoinPorCorretora()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 2, 1, 5, 1, Qt.AlignmentFlag.AlignCenter)
                elif self.HMI_ARCA.MainGraphIsShowing == "Desempenho do ativo":
                    self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page50_MainGraph_DesempenhoDoAtivo()
                    self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)

                self.GraphWidget_Distribuicao.deleteLater()
                self.GraphWidget_Distribuicao = self.HMI_ARCA.CreateGraph_Page50_Distribuicao()
                self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_Distribuicao, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

            elif self.PageID== PAGE_BY_NAME['Tributacao'].page_id: # Tributação Page
                if self.ShowValues:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Normal)
                    self.TextBox_Msg3.setEchoMode(QLineEdit.Normal)
                    self.TextBox_Msg4.setEchoMode(QLineEdit.Normal)
                else:
                    self.TextBox_Msg2.setEchoMode(QLineEdit.Password)
                    self.TextBox_Msg3.setEchoMode(QLineEdit.Password)
                    self.TextBox_Msg4.setEchoMode(QLineEdit.Password)
                self.HMI_Tributacao.CreateTable_51_2()

        elif ButtonPressed == 'Atualizar Tabela de Cotações':
            for row in range(self.Table_CotaçõesManuais.rowCount()):
                if not str(self.data_45_1[row][2]) == str(self.Table_CotaçõesManuais.item(row, 2).text()):
                    # Apenas atualizar os ativos que são diferentes do início
                    self.DBManager.UpdateCotacao(self.data_45_1[row][0], self.Table_CotaçõesManuais.item(row, 2).text())
            self.DBManager.AtualizarCotacoes()

            self.CreatePage(self.PageID)

        elif ButtonPressed == 'RemoveUnusedAtivosFromCotacoes':
            self.DBManager.RemoveUnusedAtivosFromCotacoes()
            self.CreatePage("45")

        elif ButtonPressed == 'Path Padrão':
            self.Button_PathPadrao.setText("PADRÃO")
            self.Button_PathEspecifico.setText("específico")
            self.TextBox_Path.setText("")
            self.Button_PathEspecifico.setStyleSheet("background-color: black; color: white;")
            self.Button_PathPadrao.setStyleSheet("background-color: green; color: white;")

        elif ButtonPressed == 'Path Específico':
            if not self.filedialogIsOpen:
                root = tkinter.Tk()
                root.withdraw() # Used to hide tkinter window
                self.filedialogIsOpen = True
                Path = filedialog.askdirectory() # Select folder path
                self.filedialogIsOpen = False
                try:
                    if len(Path)>0:
                        self.Button_PathPadrao.setText("padrão")
                        self.Button_PathEspecifico.setText("ESPECÍFICO")
                        self.TextBox_Path.setText(Path)
                        self.Button_PathEspecifico.setStyleSheet("background-color: green; color: white;")
                        self.Button_PathPadrao.setStyleSheet("background-color: black; color: white;")
                except:pass

        elif ButtonPressed == "Change UserPath":
            def UpdateUserPath(UserName, PathNovo):
                currdir = os.getcwd()
                conn = sqlite3.connect(currdir+'\\Users.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE Usuários SET Path = (?) Where Usuário = (?)", [(PathNovo), UserName])
                conn.commit()
                conn.close()
            if not self.filedialogIsOpen:
                root = tkinter.Tk()
                root.withdraw() # Used to hide tkinter window
                self.filedialogIsOpen = True
                Path = filedialog.askdirectory() # Select folder path
                self.filedialogIsOpen = False
                try:
                    if len(Path) > 0 and not self.DBManager.UserPath == Path:
                        self.DBManager.Disconnect()
                        UpdateUserPath(self.User, Path)
                        copyfile(self.DBManager.UserPath+"/"+self.User+'.db', Path+"/"+self.User+'.db')
                        os.remove(self.DBManager.UserPath+"/"+self.User+'.db')
                        self.DBManager.UserPath = Path
                        self.DBManager.ConnectToDB(Path+"\\"+self.User+".db")
                except Exception as e: print(e)

        elif ButtonPressed == "ChangeProfilePhoto":
            root = tkinter.Tk()
            root.withdraw() # Used to hide tkinter window
            currdir = os.getcwd() # Get current directory
            if not self.filedialogIsOpen:
                self.filedialogIsOpen = True
                DB_Path = filedialog.askopenfilename(parent=root, title='Selecione a sua foto', filetypes=[("Arquivos JPG", ".jpg")]) # Select folder path
                self.setCursor(Qt.CursorShape.WaitCursor)
                self.filedialogIsOpen = False
                if len(DB_Path)>0:
                    try:
                        copyfile(DB_Path,currdir+"\\images\\ProfilePhoto_"+self.User+'.jpg')
                        im = Image.open(".\\images\\ProfilePhoto_"+self.User+'.jpg')
                        img_width, img_height = im.size
                        crop_width = min(im.size)
                        crop_height = min(im.size)
                        im.crop(((img_width - crop_width) // 2,
                                 (img_height - crop_height) // 2,
                                 (img_width + crop_width) // 2,
                                 (img_height + crop_height) // 2)).save(".\\images\\ProfilePhoto_"+self.User+'.jpg', quality=95)
                    except: pass
                self.unsetCursor()
                self.CreatePage(PAGE_BY_NAME['Perfil'].page_id)

        elif ButtonPressed == "ExportToExcel":
            if not self.filedialogIsOpen:
                MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Para continuar a exportação,\nSALVE seu trabalho de todas as planilhas EXCEL abertas.')
                root = tkinter.Tk()
                root.withdraw() # Used to hide tkinter window
                self.filedialogIsOpen = True
                DB_Path = filedialog.askdirectory() # Select folder path
                self.setCursor(Qt.CursorShape.WaitCursor)
                self.filedialogIsOpen = False
                try:
                    if len(DB_Path)>0:
                        agora = datetime.now().strftime("%Y %m %d")
                        FileName = self.User+"_database_"+agora+'.xlsx'
                        workbook = xlsxwriter.Workbook(DB_Path+"/"+FileName)
                        conn = sqlite3.connect(self.User+'.db')
                        tables, cursor = self.DBManager.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
                        tables = list(map(lambda x: x[0], tables))
                        for table in tables[1:]:
                            try: worksheet = workbook.add_worksheet(name=table[0:31])
                            except Exception as e:print(e)

                            CONTENT, cursor = self.DBManager.GetDataDB('SELECT * FROM '+table)
                            headers = list(map(lambda x: x[0], cursor.description))
                            row1 = []
                            if len(CONTENT)>0: row1 = CONTENT[0]
                            else: worksheet.write(0, 0, "Nada declarado aqui")
                            for column_number, item in enumerate(row1):
                                worksheet.write(0, column_number, headers[column_number])

                            for row_number, row in enumerate(CONTENT):
                                for column_number, item in enumerate(row):
                                    try: worksheet.write(row_number+1, column_number, item)
                                    except Exception as e:print(e)
                        workbook.close()

                        excel = win32.gencache.EnsureDispatch('Excel.Application')
                        wb = excel.Workbooks.Open(DB_Path+"/"+FileName)
                        for table in tables[1:]:
                            ws = wb.Worksheets(table[0:31])
                            ws.Columns.AutoFit()
                        wb.Save()
                        wb.Close(True)
                        # excel.Application.Quit() # Bugado
                        os.startfile(DB_Path+"/"+FileName)
                except Exception as e:
                    print(e)
                    try:workbook.close()
                    except Exception as e: print(e)
                    try:wb.Close(True)
                    except Exception as e:print(e)
                finally: self.unsetCursor()

        elif ButtonPressed == "ExportToDB":
            root = tkinter.Tk()
            root.withdraw() # use to hide tkinter window
            currdir = os.getcwd() # Get current directory
            if not self.filedialogIsOpen:
                self.filedialogIsOpen = True
                DB_Path = filedialog.askdirectory(parent=root, initialdir=currdir, title='Selecione a pasta para salvar seu backup') # Select folder path
                self.filedialogIsOpen = False
                if len(DB_Path)>0:
                    try:
                        copyfile(currdir+"\\"+self.User+'.db', DB_Path+"\\"+self.User+' Database '+str(datetime.now().strftime("%Y %m %d %H %M %S"))+'.db')
                        MessageBox_Msg1 = QMessageBox.about(self,'Informação','Exportação bem sucedida.')
                    except: MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Exportação mal sucedida.')

        elif ButtonPressed == "ImportFromDB":
            def TrocaUserName(NomeVelho, NomeNovo):
                self.DBManager.ModifyDB("UPDATE Usuários SET Usuário = (?) Where Usuário = (?)", [(NomeNovo), NomeVelho])

            def TrocaUserEmail(EmailVelho, EmailNovo):
                self.DBManager.ModifyDB("UPDATE Usuários SET Email = (?) Where Email = (?)", [(EmailNovo), EmailVelho])

            def UpdateUserPath(UserName, PathNovo):
                currdir = os.getcwd()
                conn = sqlite3.connect(currdir+'/Users.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE Usuários SET Path = (?) Where Usuário = (?)", [(PathNovo), UserName])
                conn.commit()
                conn.close()

            root = tkinter.Tk()
            root.withdraw() # use to hide tkinter window
            currdir = os.getcwd() # Get current directory
            if not self.filedialogIsOpen:
                self.filedialogIsOpen = True
                file_path = filedialog.askopenfilename(filetypes=[("DB files", "*.db")])
                self.filedialogIsOpen = False
                if len(file_path)>0:
                    try:
                        conn = sqlite3.connect(file_path)
                        cursor = conn.cursor()
                        corretoras = list(cursor.execute("SELECT * FROM Corretoras"))
                        TableNames = list(cursor.execute("SELECT name FROM sqlite_master WHERE type='table';"))
                        TableNames = list(map(lambda x: x[0],TableNames))
                        if not ("TiposDeAtivo" in TableNames and
                                "SubtiposDeAtivo" in TableNames and
                                "Setores" in TableNames and
                                "Bolsa" in TableNames and
                                "Cotações" in TableNames and
                                "MoedasFiat" in TableNames and
                                "TributaçãoDTBolsa" in TableNames and
                                "TributaçãoSTBolsa" in TableNames and
                                "TributaçãoDTCripto" in TableNames and
                                "TributaçãoSTCripto" in TableNames): raise ValueError("Faltam dados,")

                        retorno = list(cursor.execute("SELECT * FROM Perfil"))
                        UserName = str(retorno[0][0])
                        UserEmail = str(retorno[0][2])
                        UserPath = os.path.split(file_path)[0]

                        conn.close()

                        # Verificar se usuário já existe
                        self.DBManager.CriarDB('Users.db') # Create Usuários.db IF NOT EXISTS
                        self.DBManager.ConnectToDB('Users.db') # Connect to Users.db
                        self.DBManager.CreateTableInCurrentDB('Usuários', [('Usuário', 'TEXT'), ('Email', 'TEXT'), ('Path', 'TEXT')]) # Create Table Usuários IF NOT EXISTS

                        retorno, cursor = self.DBManager.GetDataDB("SELECT * FROM Usuários")
                        retorno = list(filter(lambda x: x[0]==UserName or x[1]==UserEmail, retorno))

                        if len(retorno) > 0: # Usuário já está aqui dentro do programa.
                            # Escolher com qual db quer ficar.
                            MessageBox_Msg1 = QMessageBox()
                            MessageBox_Msg1.setWindowTitle("Escolha um")
                            if retorno[0][0] == UserName and retorno[0][1] == UserEmail: MessageBox_Msg1.setText("Já existe um usuário com esse nome e email na base de dados.\nDeseja substitui-lo?")
                            if retorno[0][0] == UserName: MessageBox_Msg1.setText("Já existe um usuário com esse nome na base de dados.\nDeseja substitui-lo?")
                            if retorno[0][1] == UserEmail: MessageBox_Msg1.setText("Já existe um usuário com esse email na base de dados.\nDeseja substitui-lo?")
                            MessageBox_Msg1.setIcon(QMessageBox.Warning)
                            MessageBox_Msg1.setStandardButtons(QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
                            MessageBox_Msg1.setDefaultButton(QMessageBox.No)
                            MessageBox_Msg1.setWindowIcon(QIcon(".\\images\\logoARCA.png"))
                            returnValue = MessageBox_Msg1.exec()

                            if returnValue == QMessageBox.No: raise ValueError("Usuário já existe.")
                            elif returnValue == QMessageBox.Cancel: raise ValueError("Operação cancelada.")
                            elif returnValue == QMessageBox.Yes:
                                Flag_TrocaUserName = False
                                Flag_TrocaUserEmail = False
                                # Se diferente, escolher qual UserName manter
                                if not retorno[0][0] == UserName:
                                    MessageBox_Msg1 = QMessageBox()
                                    MessageBox_Msg1.setWindowTitle("Escolha um")
                                    MessageBox_Msg1.setText("Os nomes de usuário são diferentes.\nPressione 'Yes' para escolher o nome "+retorno[0][0]+" ou\npressione 'No' para escolher '"+UserName+"'.\n'Cancel' cancela a importação.")
                                    MessageBox_Msg1.setIcon(QMessageBox.Warning)
                                    MessageBox_Msg1.setStandardButtons(QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
                                    MessageBox_Msg1.setDefaultButton(QMessageBox.No)
                                    MessageBox_Msg1.setWindowIcon(QIcon(".\\images\\logoARCA.png"))
                                    returnValue = MessageBox_Msg1.exec()

                                    if returnValue == QMessageBox.Cancel: raise ValueError("Operação cancelada.")
                                    elif returnValue == QMessageBox.Yes: UserName = retorno[0][0]
                                    elif returnValue == QMessageBox.No: Flag_TrocaUserName = True

                                # Se diferente, escolher qual UserEmail manter
                                if not retorno[0][1] == UserEmail:
                                    MessageBox_Msg1 = QMessageBox()
                                    MessageBox_Msg1.setWindowTitle("Escolha um")
                                    MessageBox_Msg1.setText("Os emails de usuário são diferentes.\nPressione 'Yes' para escolher o email "+retorno[0][1]+" ou\npressione 'No' para escolher '"+UserEmail+"'.\n'Cancel' cancela a importação.")
                                    MessageBox_Msg1.setIcon(QMessageBox.Warning)
                                    MessageBox_Msg1.setStandardButtons(QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
                                    MessageBox_Msg1.setDefaultButton(QMessageBox.No)
                                    MessageBox_Msg1.setWindowIcon(QIcon(".\\images\\logoARCA.png"))
                                    returnValue = MessageBox_Msg1.exec()

                                    if returnValue == QMessageBox.Cancel: raise ValueError("Operação cancelada.")
                                    elif returnValue == QMessageBox.Yes: pass
                                    elif returnValue == QMessageBox.No: Flag_TrocaUserEmail = True

                                if Flag_TrocaUserName: TrocaUserName(retorno[0][0], UserName)
                                if Flag_TrocaUserEmail: TrocaUserEmail(retorno[0][1], UserEmail)
                                UpdateUserPath(UserName, UserPath)
                                try:os.remove(os.path.split(file_path)[0]+"\\"+UserName+".db")
                                except:pass
                                os.rename(file_path, os.path.split(file_path)[0]+"\\"+UserName+".db")

                        else: # Usuário nunca esteve nessa versão do programa
                            # Adicionar Usuário e Email
                            self.DBManager.AddRowInCurrentDB('Usuários', [('Usuário',UserName), ('Email',UserEmail), ('Path', UserPath)])
                        # Disconnect from Users.db
                        self.DBManager.Disconnect()

                        MessageBox_Msg1 = QMessageBox.about(self,'Informação','Importação bem sucedida.\nBem-vindo de volta '+UserName+'.\nAcesse suas informações entrando\npela página inicial.')
                        self.CreatePage("0")
                    except Exception as msg:
                        if "Usuário já existe." in repr(msg):
                            self.DBManager.Disconnect()
                            MessageBox_Msg1 = QMessageBox.about(self,'Informação','Importação cancelada.\n'+str(msg))
                        elif "Operação cancelada." in repr(msg):
                            self.DBManager.Disconnect()
                            MessageBox_Msg1 = QMessageBox.about(self,'Informação','Importação cancelada.')
                        else:
                            MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Importação mal sucedida.\n'+str(msg)+'\nArquivo fora do formato padrão\nOU\nusuário já existe.')

        elif ButtonPressed == "ImportFromExcel":
            root = tkinter.Tk()
            root.withdraw() # use to hide tkinter window
            currdir = os.getcwd() # Get current directory
            if not self.filedialogIsOpen:
                self.filedialogIsOpen = True
                Excel_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
                self.filedialogIsOpen = False
                if len(Excel_file_path)>0:
                    try:
                        # Abre excel
                        workbook = load_workbook(filename=Excel_file_path)
                        # Verifica se tem as folhas base
                        TableNames = workbook.sheetnames
                        corretoras = []
                        if not ("Bolsa" in TableNames and
                                "Cotações" in TableNames and
                                "Corretoras" in TableNames and
                                "Bancos" in TableNames): raise ValueError('''Faltam dados básicos.\nVerifique se consta as seguintes folhas no arquivo excel:\n
                                                                             01 - Bolsa\n
                                                                             02 - Cotações\n
                                                                             03 - Corretoras\n
                                                                             04 - Bancos''')
                        for sheet in TableNames: # Get corretoras
                            if "¨Bolsa¨DepSaq" in sheet:
                                corretora = sheet.replace("¨Bolsa¨DepSaq","")
                                corretora = corretora.replace("¨","")
                                corretoras.append(corretora+"¨Bolsa")
                            elif "OPs¨" in sheet and "¨Cripto¨Bruto" in sheet:
                                corretora = sheet.replace("¨Cripto¨Bruto","")
                                corretora = corretora.replace("OPs¨","")
                                corretoras.append(corretora+"¨Cripto")

                        # Verificar se tem a mesma quantidade de corretoras encontradas nas folhas também na folha de corretoras
                        CorretorasFromCorretoras = list(map(lambda cell: cell.value, workbook["Corretoras"]["A"]))[1:]
                        for corretora in corretoras:
                            if not corretora in CorretorasFromCorretoras: raise ValueError("Faltam dados.\n"+corretora+" possui folha Bruto, mas não consta na folha Corretoras.")
                        for corretora in CorretorasFromCorretoras:
                            if not corretora in corretoras: raise ValueError("Faltam dados.\n"+corretora+" consta na folha Corretoras, mas não possui a folha Bruto.")
                        if (any(CorretorasFromCorretoras.count(element) > 1 for element in CorretorasFromCorretoras) or
                            any(corretoras.count(element) > 1 for element in corretoras)):
                            raise ValueError("Há uma corretora duplicada.")

                        CorretorasFromCorretorasA = list(map(lambda cell: cell.value, workbook["Corretoras"]["A"]))[1:]
                        CorretorasFromCorretorasB = list(map(lambda cell: cell.value, workbook["Corretoras"]["B"]))[1:]
                        CorretorasFromCorretorasC = list(map(lambda cell: cell.value, workbook["Corretoras"]["C"]))[1:]
                        CorretorasFromCorretoras = []
                        for idx in range(len(CorretorasFromCorretorasA)):
                            if CorretorasFromCorretorasA[idx] != None or CorretorasFromCorretorasB[idx] != None or CorretorasFromCorretorasC[idx] != None:
                                CorretorasFromCorretoras.append((CorretorasFromCorretorasA[idx], CorretorasFromCorretorasB[idx], CorretorasFromCorretorasC[idx]))

                        UserName = self.TextBox_NomeDeUsuario.text()
                        UserPswd = self.TextBox_Senha1.text()
                        UserEmail = self.TextBox_Email.text().lower()
                        UserCoin = self.ComboBox_Currency.currentText().upper()
                        UserPath = self.TextBox_Path.text()
                        currdir = os.getcwd() # Get current directory
                        if UserPath == '': UserPath = currdir

                        # Import basis

                        # Create DB
                        try:
                            self.DBManager.User = UserName; self.DBManager.Senha = UserPswd; self.DBManager.Email = UserEmail; self.DBManager.UserPath = UserPath

                            # Create Usuários.db IF NOT EXISTS
                            self.DBManager.CriarDB(currdir+'\\Users.db')
                            # Connect to Users.db
                            self.DBManager.ConnectToDB(currdir+'\\Users.db')
                            # Create Table Usuários IF NOT EXISTS
                            self.DBManager.CreateTableInCurrentDB('Usuários', [('Usuário', 'TEXT'), ('Email', 'TEXT'), ('Path', 'TEXT')])
                            # Adicionar Usuário e Email
                            self.DBManager.AddRowInCurrentDB('Usuários', [('Usuário',UserName), ('Email',UserEmail), ('Path', UserPath)])
                            # Disconnect from Users.db
                            self.DBManager.Disconnect()

                            # Criar user.db
                            self.DBManager.CriarDB(UserPath+"\\"+UserName+'.db')
                            # Connect to User.db
                            self.DBManager.ConnectToDB(UserPath+"\\"+UserName+'.db')
                            # Create Table Perfil
                            self.DBManager.CreateTableInCurrentDB('Perfil', [('Usuário', 'TEXT'), ('Senha','TEXT'), ('Email', 'TEXT'), ('TaxaB3Per','REAL'), ('MoedaCorrente','TEXT'), ('GastoMensal', 'REAL'), ('MesesDeReserva', 'REAL')])
                            # Adicionar Usuário, Senha, Email, TaxaB3Per = 0.03%
                            self.DBManager.AddRowInCurrentDB('Perfil', [('Usuário',UserName), ('Senha',UserPswd), ('Email',UserEmail), ('TaxaB3Per',0.03), ('MoedaCorrente',UserCoin), ('GastoMensal', 0), ('MesesDeReserva', 6)])
                            # Create Table Perfil_TiposDeAtivos
                            self.DBManager.CreateTableInCurrentDB('TiposDeAtivo', [('TipoDeAtivo', 'TEXT')])
                            # Adicionar os Tipos básicos
                            if "TiposDeAtivo" in TableNames: TiposDeAtivo = list(map(lambda cell: cell.value, workbook["TiposDeAtivo"]["A"]))[1:]
                            else: TiposDeAtivos = self.DBManager.TiposDeAtivosBasicos
                            for TipoDeAtivo in TiposDeAtivo:
                                self.DBManager.AddRowInCurrentDB('TiposDeAtivo', [('TipoDeAtivo', TipoDeAtivo)])
                            # Create Table Perfil_SubtipoDeAtivos
                            self.DBManager.CreateTableInCurrentDB('SubtiposDeAtivo', [('TipoDeAtivo', 'TEXT'),('SubtipoDeAtivo', 'TEXT')])
                            # Adicionar os Subtipos básicos
                            if "SubtiposDeAtivo" in TableNames:
                                SubtiposDeAtivoA = list(map(lambda cell: cell.value, workbook["SubtiposDeAtivo"]["A"]))[1:]
                                SubtiposDeAtivoB = list(map(lambda cell: cell.value, workbook["SubtiposDeAtivo"]["B"]))[1:]
                                SubtiposDeAtivo = []
                                for idx in range(len(SubtiposDeAtivoA)):
                                    if SubtiposDeAtivoA[idx] != None or SubtiposDeAtivoB[idx] != None:
                                        SubtiposDeAtivo.append((SubtiposDeAtivoA[idx], SubtiposDeAtivoB[idx]))
                            else: SubtiposDeAtivo = self.DBManager.SubtiposDeAtivosBasicos
                            for item in SubtiposDeAtivo:
                                TipoDeAtivo = item[0]
                                SubtipoDeAtivo = item[1]
                                self.DBManager.AddRowInCurrentDB('SubtiposDeAtivo', [('TiposDeAtivo', TipoDeAtivo),('SubtipoDeAtivo', SubtipoDeAtivo)])
                            # Create Table Setores
                            self.DBManager.CreateTableInCurrentDB('Setores', [('Setor', 'TEXT')])
                            # Adicionar os Setores básicos
                            if "Setores" in TableNames: Setores = list(map(lambda cell: cell.value, workbook["Setores"]["A"]))[1:]
                            else: Setores = self.DBManager.SetoresBasicos
                            for Setor in Setores:
                                self.DBManager.AddRowInCurrentDB('Setores', [('Setor', Setor)])
                            # Create Table Bolsa
                            self.DBManager.CreateTableInCurrentDB('Bolsa', [('Ativo', 'TEXT'),('TipoDeAtivo', 'TEXT'),('SubtipoDeAtivo', 'TEXT'),('Setor', 'TEXT')])
                            BolsaA = list(map(lambda cell: cell.value, workbook["Bolsa"]["A"]))[1:]
                            BolsaB = list(map(lambda cell: cell.value, workbook["Bolsa"]["B"]))[1:]
                            BolsaC = list(map(lambda cell: cell.value, workbook["Bolsa"]["C"]))[1:]
                            BolsaD = list(map(lambda cell: cell.value, workbook["Bolsa"]["D"]))[1:]
                            Bolsa = []
                            for idx in range(len(BolsaA)):
                                if BolsaA[idx] != None or BolsaB[idx] != None or BolsaC[idx] != None or BolsaD[idx] != None:
                                    Bolsa.append((BolsaA[idx], BolsaB[idx], BolsaC[idx], BolsaD[idx]))
                            # Create Table Cotações
                            self.DBManager.CreateTableInCurrentDB('Cotações', [('Modo', 'TEXT'),('DataDeAtualização', 'DATETIME'),('Ativo', 'TEXT'),('Cotação', 'REAL')])
                            if not UserCoin == "USD": self.DBManager.AddRowInCurrentDB('Cotações', [('Modo', 'Auto'),('DataDeAtualização', datetime.strptime(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")),('Ativo', 'USD'),('Cotação', 0.)])
                            CotacoesA = list(map(lambda cell: cell.value, workbook["Cotações"]["A"]))[1:]
                            CotacoesB = list(map(lambda cell: cell.value, workbook["Cotações"]["B"]))[1:]
                            CotacoesC = list(map(lambda cell: cell.value, workbook["Cotações"]["C"]))[1:]
                            CotacoesD = list(map(lambda cell: cell.value, workbook["Cotações"]["D"]))[1:]
                            Cotacoes = []
                            for idx in range(len(CotacoesA)):
                                if CotacoesA[idx] != None or CotacoesB[idx] != None or CotacoesC[idx] != None or CotacoesD[idx] != None:
                                    Cotacoes.append((CotacoesA[idx], CotacoesB[idx], CotacoesC[idx], CotacoesD[idx]))
                            # Create Table Tributação
                            self.DBManager.CreateTableInCurrentDB('TributaçãoDTBolsa', [('MesAno', 'DATETIME'),('Resultado', 'REAL'),('PrejuizoAcumulado', 'REAL'),('ResultadoFinal', 'REAL'),('Alíquota', 'REAL'),('LucroMínimoTaxável', 'REAL'),('ImpostoDevido', 'REAL'),('ResultadoLíquido', 'REAL')])
                            self.DBManager.CreateTableInCurrentDB('TributaçãoSTBolsa', [('MesAno', 'DATETIME'),('Resultado', 'REAL'),('PrejuizoAcumulado', 'REAL'),('ResultadoFinal', 'REAL'),('Alíquota', 'REAL'),('LucroMínimoTaxável', 'REAL'),('ImpostoDevido', 'REAL'),('ResultadoLíquido', 'REAL')])
                            self.DBManager.CreateTableInCurrentDB('TributaçãoDTCripto', [('MesAno', 'DATETIME'),('Resultado', 'REAL'),('PrejuizoAcumulado', 'REAL'),('ResultadoFinal', 'REAL'),('Alíquota', 'REAL'),('LucroMínimoTaxável', 'REAL'),('ImpostoDevido', 'REAL'),('ResultadoLíquido', 'REAL')])
                            self.DBManager.CreateTableInCurrentDB('TributaçãoSTCripto', [('MesAno', 'DATETIME'),('Resultado', 'REAL'),('PrejuizoAcumulado', 'REAL'),('ResultadoFinal', 'REAL'),('Alíquota', 'REAL'),('LucroMínimoTaxável', 'REAL'),('ImpostoDevido', 'REAL'),('ResultadoLíquido', 'REAL')])
                            # Create Table Corretoras
                            self.DBManager.CreateTableInCurrentDB('Corretoras', [('Corretora', 'TEXT'),('MoedaCorrente', 'TEXT'),('ContaCorrente', 'REAL')])
                            CorretorasA = list(map(lambda cell: cell.value, workbook["Corretoras"]["A"]))[1:]
                            CorretorasB = list(map(lambda cell: cell.value, workbook["Corretoras"]["B"]))[1:]
                            CorretorasC = list(map(lambda cell: cell.value, workbook["Corretoras"]["C"]))[1:]
                            Corretoras = []
                            for idx in range(len(CorretorasA)):
                                if CorretorasA[idx] != None or CorretorasB[idx] != None or CorretorasC[idx] != None:
                                    Corretoras.append((CorretorasA[idx], CorretorasB[idx], CorretorasC[idx]))
                            # Create Table Bancos
                            self.DBManager.CreateTableInCurrentDB('Bancos', [('Banco', 'TEXT'),('MoedaCorrente', 'TEXT'),('ContaCorrente', 'REAL')])
                            BancosA = list(map(lambda cell: cell.value, workbook["Bancos"]["A"]))[1:]
                            BancosB = list(map(lambda cell: cell.value, workbook["Bancos"]["B"]))[1:]
                            BancosC = list(map(lambda cell: cell.value, workbook["Bancos"]["C"]))[1:]
                            Bancos = []
                            for idx in range(len(BancosA)):
                                if BancosA[idx] != None or BancosB[idx] != None or BancosC[idx] != None:
                                    Bancos.append((BancosA[idx], BancosB[idx], BancosC[idx]))
                            for banco in Bancos:
                                self.DBManager.AddRowInCurrentDB('Bancos', [('Banco', banco[0]), ('MoedaCorrente', banco[1]), ('ContaCorrente', banco[2])])
                            # Create Table MoedasFiat
                            self.DBManager.CreateTableInCurrentDB('MoedasFiat', [('MoedaFiat', 'TEXT')])
                            if "MoedasFiat" in TableNames: MoedasFiat = list(map(lambda cell: cell.value, workbook["MoedasFiat"]["A"]))[1:]
                            else: MoedasFiat = self.DBManager.series_BasicInfo_MoedasFiat
                            for Moeda in MoedasFiat:
                                self.DBManager.AddRowInCurrentDB('MoedasFiat', [('MoedaFiat', Moeda)])
                        except:
                            print("Problema na criação da DB.")
                            raise ValueError("Houve algum problema na criação da DB.\nVerifique os dados na tabela a ser importada\ne tente novamente.")

                        if "Tickers" in TableNames:
                            Tickers = list(map(lambda cell: cell.value, workbook["Tickers"]["A"]))[1:]
                            self.DBManager.SetAllTickers(Tickers)
                        else:
                            print("Getting all tickers online")
                            self.YahooFinance.GetAllTickers()

                        for corretora, MoedaCorrente, ContaCorrente in CorretorasFromCorretoras:
                            if "¨Bolsa" in corretora:
                                BolsaOuCripto = "Bolsa"
                                Corretora = corretora.replace("¨Bolsa","")
                                self.DBManager.AddRowInCurrentDB('Corretoras', [('Corretora', Corretora+"¨"+BolsaOuCripto),('MoedaCorrente', MoedaCorrente),('ContaCorrente', ContaCorrente)])
                                # Create Table DepósitosESaques
                                self.DBManager.CreateTableInCurrentDB("¨"+Corretora+"¨"+BolsaOuCripto+"¨DepSaq", [('Data', 'DATETIME'),('Valor', 'REAL')])
                                # Importar ¨DepSaq
                                DepSaqA = list(map(lambda cell: cell.value, workbook["¨"+Corretora+"¨"+BolsaOuCripto+"¨DepSaq"]["A"]))[1:]
                                DepSaqB = list(map(lambda cell: cell.value, workbook["¨"+Corretora+"¨"+BolsaOuCripto+"¨DepSaq"]["B"]))[1:]
                                DepSaq = []
                                for idx in range(len(DepSaqA)):
                                    if DepSaqA[idx] != None or DepSaqB[idx] != None:
                                        DepSaq.append((DepSaqA[idx], DepSaqB[idx]))
                                for info in DepSaq:
                                    self.DBManager.AddRowInCurrentDB("¨"+Corretora+"¨"+BolsaOuCripto+"¨DepSaq", [('Data', info[0]),('Valor', info[1])])

                            elif "¨Cripto" in corretora:
                                BolsaOuCripto = "Cripto"
                                Corretora = corretora.replace("¨Cripto","")
                                self.DBManager.AddRowInCurrentDB('Corretoras', [('Corretora', Corretora+"¨"+BolsaOuCripto),('MoedaCorrente', MoedaCorrente),('ContaCorrente', ContaCorrente)])

                                TableName = str('OPs'+'¨'+Corretora+'¨'+BolsaOuCripto)
                                TableNameBruto = TableName+'¨Bruto'
                                TableNameRefinado = TableName+'¨Refinado'

                                self.DBManager.CreateTableInCurrentDB(TableNameRefinado, [('Observação', 'TEXT'),
                                                                                          ('Resultado', 'REAL'),
                                                                                          ('Data', 'DATETIME'),
                                                                                          ('Tipo', 'TEXT'),
                                                                                          ('ParEsquerdo', 'TEXT'),
                                                                                          ('ParDireito', 'TEXT'),
                                                                                          ('Preço', 'REAL'),
                                                                                          ('Qqt', 'REAL'),
                                                                                          ('Taxa', 'REAL'),
                                                                                          ('MoedaDaTaxa', 'TEXT'),
                                                                                          ('Conversão', 'REAL')])

                                self.DBManager.CreateTableInCurrentDB(TableNameBruto, [('Observação', 'TEXT'),
                                                                                       ('Data', 'DATETIME'),
                                                                                       ('Tipo', 'TEXT'),
                                                                                       ('ParEsquerdo', 'TEXT'),
                                                                                       ('ParDireito', 'TEXT'),
                                                                                       ('Preço', 'REAL'),
                                                                                       ('Qqt', 'REAL'),
                                                                                       ('Taxa', 'REAL'),
                                                                                       ('MoedaDaTaxa', 'TEXT'),
                                                                                       ('Conversão', 'REAL')])

                        AtivosInseridos = []
                        for sheet in TableNames:
                            if "OPs¨" in sheet and "¨Bolsa¨Bruto" in sheet:
                                try:
                                    ativo = sheet.replace("OPs¨","").replace("¨Bolsa¨Bruto","")
                                    ativo = ativo[0:ativo.find("¨")]
                                    corretora = sheet.replace("OPs¨","").replace("¨Bolsa¨Bruto","").replace(ativo+"¨","")
                                    ModoManualAtivo = [item[0] for item in Cotacoes if item[2] == ativo][0]
                                    if not ModoManualAtivo == 'Manual': ativo = ativo.upper()
                                    if ativo not in AtivosInseridos:
                                        self.DBManager.AddRowInCurrentDB('Bolsa', [('Ativo', ativo.replace(" ","_")),
                                                                                   ('TipoDeAtivo', [item[1] for item in Bolsa if item[0] == ativo][0]),
                                                                                   ('SubtipoDeAtivo', [item[2] for item in Bolsa if item[0] == ativo][0]),
                                                                                   ('Setor', [item[3] for item in Bolsa if item[0] == ativo][0])])
                                        self.DBManager.AddRowInCurrentDB('Cotações', [('Modo', ModoManualAtivo),
                                                                                      ('DataDeAtualização', [item[1] for item in Cotacoes if item[2] == ativo][0]),
                                                                                      ('Ativo', ativo),
                                                                                      ('Cotação', [item[3] for item in Cotacoes if item[2] == ativo][0])])
                                        AtivosInseridos.append(ativo)
                                    TableName = str('OPs¨'+ativo.replace(" ","_")+
                                                    '¨'+corretora.replace(" ","_")+
                                                    '¨Bolsa')
                                    TableNameBruto = TableName+'¨Bruto'; TableNameDT = TableName+'¨DT'; TableNameST = TableName+'¨ST'
                                    self.DBManager.CreateTableInCurrentDB(TableNameDT, [('Data', 'DATETIME'),
                                                                                        ('Tipo', 'TEXT'),
                                                                                        ('Qqt', 'INTEGER'),
                                                                                        ('Preço', 'REAL'),
                                                                                        ('Corretagem', 'REAL'),
                                                                                        ('TaxaB3Per', 'REAL'),
                                                                                        ('TaxaB3', 'REAL'),
                                                                                        ('Obs', 'TEXT'),
                                                                                        ('Estoque', 'INTEGER'),
                                                                                        ('CustoDaOperação', 'REAL'),
                                                                                        ('CustoTotal', 'REAL'),
                                                                                        ('CustoMédio', 'REAL'),
                                                                                        ('Resultado', 'REAL')])
                                    self.DBManager.CreateTableInCurrentDB(TableNameST, [('Data', 'DATETIME'),
                                                                                        ('Tipo', 'TEXT'),
                                                                                        ('Qqt', 'INTEGER'),
                                                                                        ('Preço', 'REAL'),
                                                                                        ('Corretagem', 'REAL'),
                                                                                        ('TaxaB3Per', 'REAL'),
                                                                                        ('TaxaB3', 'REAL'),
                                                                                        ('Obs', 'TEXT'),
                                                                                        ('Estoque', 'INTEGER'),
                                                                                        ('CustoDaOperação', 'REAL'),
                                                                                        ('CustoTotal', 'REAL'),
                                                                                        ('CustoMédio', 'REAL'),
                                                                                        ('Resultado', 'REAL')])
                                    self.DBManager.CreateTableInCurrentDB(TableNameBruto, [('Data', 'DATETIME'),
                                                                                           ('Tipo', 'TEXT'),
                                                                                           ('Qqt', 'INTEGER'),
                                                                                           ('Preço', 'REAL'),
                                                                                           ('Corretagem', 'REAL'),
                                                                                           ('TaxaB3Per', 'REAL'),
                                                                                           ('TaxaB3', 'REAL'),
                                                                                           ('Obs', 'TEXT'),
                                                                                           ('Estoque', 'INTEGER'),
                                                                                           ('CustoDaOperação', 'REAL'),
                                                                                           ('CustoTotal', 'REAL'),
                                                                                           ('CustoMédio', 'REAL'),
                                                                                           ('Resultado', 'REAL')])
                                    DadosA = list(map(lambda cell: cell.value, workbook[TableNameBruto]["A"]))[1:]
                                    DadosB = list(map(lambda cell: cell.value, workbook[TableNameBruto]["B"]))[1:]
                                    DadosC = list(map(lambda cell: cell.value, workbook[TableNameBruto]["C"]))[1:]
                                    DadosD = list(map(lambda cell: cell.value, workbook[TableNameBruto]["D"]))[1:]
                                    DadosE = list(map(lambda cell: cell.value, workbook[TableNameBruto]["E"]))[1:]
                                    DadosF = list(map(lambda cell: cell.value, workbook[TableNameBruto]["F"]))[1:]
                                    DadosG = list(map(lambda cell: cell.value, workbook[TableNameBruto]["G"]))[1:]
                                    DadosH = list(map(lambda cell: cell.value, workbook[TableNameBruto]["H"]))[1:]
                                    DadosI = list(map(lambda cell: cell.value, workbook[TableNameBruto]["I"]))[1:]
                                    DadosJ = list(map(lambda cell: cell.value, workbook[TableNameBruto]["J"]))[1:]
                                    DadosK = list(map(lambda cell: cell.value, workbook[TableNameBruto]["K"]))[1:]
                                    DadosL = list(map(lambda cell: cell.value, workbook[TableNameBruto]["L"]))[1:]
                                    DadosM = list(map(lambda cell: cell.value, workbook[TableNameBruto]["M"]))[1:]
                                    Dados = []
                                    for idx in range(len(DadosA)):
                                        if DadosA[idx] != None:
                                            Dados.append((DadosA[idx], DadosB[idx], DadosC[idx], DadosD[idx], DadosE[idx], DadosF[idx], DadosG[idx], DadosH[idx], DadosI[idx],DadosJ[idx], DadosK[idx], DadosL[idx], DadosM[idx]))
                                    for row in Dados:
                                        Obs = ''
                                        if row[7] != None: Obs = row[7]
                                        self.DBManager.AddRowInCurrentDB(TableNameBruto, [('Data', row[0]),
                                                                                          ('Tipo', row[1]),
                                                                                          ('Qqt', row[2]),
                                                                                          ('Preço', row[3]),
                                                                                          ('Corretagem', row[4]),
                                                                                          ('TaxaB3Per', row[5]),
                                                                                          ('TaxaB3', row[6]),
                                                                                          ('Obs', Obs),
                                                                                          ('Estoque', row[8]),
                                                                                          ('CustoDaOperação', row[9]),
                                                                                          ('CustoTotal', row[10]),
                                                                                          ('CustoMédio', row[11]),
                                                                                          ('Resultado', row[12])])
                                        if not 'Fundos Imobiliários' == [item[2] for item in Bolsa if item[0] == ativo][0]:
                                            self.DBManager.AddRowInCurrentDB(TableNameST, [('Data', row[0]),
                                                                                           ('Tipo', row[1]),
                                                                                           ('Qqt', row[2]),
                                                                                           ('Preço', row[3]),
                                                                                           ('Corretagem', row[4]),
                                                                                           ('TaxaB3Per', row[5]),
                                                                                           ('TaxaB3', row[6]),
                                                                                           ('Obs', Obs),
                                                                                           ('Estoque', row[8]),
                                                                                           ('CustoDaOperação', row[9]),
                                                                                           ('CustoTotal', row[10]),
                                                                                           ('CustoMédio', row[11]),
                                                                                           ('Resultado', row[12])])
                                    # Separar DT e ST se não for FII. Se for FII fazer só pra DT
                                    if not 'Fundos Imobiliários' == [item[2] for item in Bolsa if item[0] == ativo][0]:
                                        self.DBManager.SepararDTeST(TableName)
                                        self.DBManager.CalcularCelsAutomatizadas(TableNameBruto)
                                        self.DBManager.CalcularCelsAutomatizadas(TableNameDT)
                                        self.DBManager.CalcularCelsAutomatizadas(TableNameST)
                                    else:
                                        self.DBManager.CopiarBrutoPraDT(TableName)
                                        self.DBManager.CalcularCelsAutomatizadas(TableNameBruto)
                                        self.DBManager.CalcularCelsAutomatizadas(TableNameDT)
                                except: raise ValueError("Verifique se a tabela de cotações contém\ntodos os ativos a serem processados.")

                            elif "OPs¨" in sheet and "¨Cripto¨Bruto" in sheet:
                                def ThereIsAnotherOPWithTheSameDate(TableName, data):
                                    Table_Inicial, cursor = self.DBManager.GetDataDB("SELECT rowid, * FROM "+TableName+"¨Bruto")
                                    if "¨Bolsa" in TableName:
                                        aux = list(filter(lambda x: datetime.strptime(x[1],"%Y-%m-%d %H:%M:%S") == data, Table_Inicial))
                                    else:
                                        aux = list(filter(lambda x: datetime.strptime(x[2],"%Y-%m-%d %H:%M:%S") == data, Table_Inicial))
                                    if len(aux)>0: return True
                                    return False

                                corretora = sheet.replace("OPs¨","").replace("¨Cripto¨Bruto","")
                                TableName = str('OPs'+
                                                '¨'+corretora.replace(" ","_")+
                                                '¨Cripto')
                                TableNameBruto = TableName+'¨Bruto'
                                TableNameRefinado = TableName+'¨Refinado'
                                DadosA = list(map(lambda cell: cell.value, workbook[TableNameBruto]["A"]))[1:]
                                DadosB = list(map(lambda cell: cell.value, workbook[TableNameBruto]["B"]))[1:]
                                DadosC = list(map(lambda cell: cell.value, workbook[TableNameBruto]["C"]))[1:]
                                DadosD = list(map(lambda cell: cell.value, workbook[TableNameBruto]["D"]))[1:]
                                DadosE = list(map(lambda cell: cell.value, workbook[TableNameBruto]["E"]))[1:]
                                DadosF = list(map(lambda cell: cell.value, workbook[TableNameBruto]["F"]))[1:]
                                DadosG = list(map(lambda cell: cell.value, workbook[TableNameBruto]["G"]))[1:]
                                DadosH = list(map(lambda cell: cell.value, workbook[TableNameBruto]["H"]))[1:]
                                DadosI = list(map(lambda cell: cell.value, workbook[TableNameBruto]["I"]))[1:]
                                DadosJ = list(map(lambda cell: cell.value, workbook[TableNameBruto]["J"]))[1:]
                                Dados = []
                                for idx in range(len(DadosA)):
                                    if DadosC[idx] != None:
                                        Obs = ''
                                        ParDireito = ''
                                        Conversao = 1
                                        if DadosA[idx] != None: Obs = DadosA[idx]
                                        if DadosE[idx] != None: ParDireito = DadosE[idx]
                                        if DadosJ[idx] != None: Conversao = DadosJ[idx]
                                        Dados.append((Obs, DadosB[idx], DadosC[idx], DadosD[idx], ParDireito, DadosF[idx], DadosG[idx], DadosH[idx], DadosI[idx], Conversao))

                                for row in Dados:
                                    if not isinstance(row[1], datetime): data = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                                    else: data = row[1]
                                    if ThereIsAnotherOPWithTheSameDate(TableName, data): raise ValueError("Há uma operação na mesma data.\nVerifique em "+TableNameBruto+" no momento "+data.strftime("%d/%m/%Y %H:%M:%S")+"\ne tente novamente.")
                                    if data > datetime.now(): raise ValueError("Há uma operação ocorrendo no futuro.\nArrume isso em "+TableNameBruto+" no momento "+data.strftime("%d/%m/%Y %H:%M:%S")+"\ne tente novamente.")

                                    Taxa = 0; MoedaDaTaxa = UserCoin; Conversao = 1; ParDireito = ''

                                    if row[7]>0: Taxa = round(row[7],8)
                                    if len(row[8])>0: MoedaDaTaxa = row[8]
                                    if row[9]>0: Conversao = round(row[9],8)
                                    if len(row[4])>0: ParDireito = row[4]

                                    Obs = ''
                                    if row[0] != None: Obs = row[0]
                                    self.DBManager.AddRowInCurrentDB(TableNameBruto, [('Observação', Obs),
                                                                                      ('Data', data),
                                                                                      ('Tipo', row[2]),
                                                                                      ('ParEsquerdo', row[3]),
                                                                                      ('ParDireito', ParDireito),
                                                                                      ('Preço', round(row[5],8)),
                                                                                      ('Qqt', round(row[6],8)),
                                                                                      ('Taxa', Taxa),
                                                                                      ('MoedaDaTaxa', MoedaDaTaxa),
                                                                                      ('Conversão', Conversao)])

                                self.DBManager.CalcularCelsAutomatizadas_CriptoRefinado(TableName)

                                def GetRowId(corretora):
                                    retorno, cursor = self.DBManager.GetDataDB("SELECT rowid, * FROM Corretoras")
                                    retorno = list(filter(lambda x: str(x).find(corretora+"¨Cripto")>-1, retorno))
                                    retorno = retorno[0][0]
                                    return str(retorno)
                                # Update Conta Corrente em Table ContaCorrente_Corretora_BolsaOuCripto
                                Valor = self.DBManager.GetEstoque(ativo = UserCoin, corretora = corretora, BolsaOuCripto = "Cripto")
                                self.DBManager.ModifyDB("UPDATE Corretoras SET ContaCorrente = (?) Where rowid = "+GetRowId(corretora), [(Valor)])

                                # Verificar se os dois ativos estão na Cotações (DB). Se não estiverem, coloque e atualize a cotação se for encontrado online.
                                def AtivoExisteNaTabelaDeCotacoes(ativo):
                                    Table, cursor = self.DBManager.GetDataDB("SELECT * FROM Cotações")
                                    aux = list(filter(lambda x: x[2]==ativo, Table))
                                    if len(aux)>0: return True
                                    else: return False
                                def AtivoExisteNaFolhaDeCotacoes(ativo, Cotacoes):
                                    try:
                                        Cotacao = [item[3] for item in Cotacoes if item[2] == ativo][0]
                                        if Cotacao>0: return True
                                        else: return False
                                    except: pass

                                TableBruto, cursor = self.DBManager.GetDataDB("SELECT * FROM "+TableNameBruto)
                                ListaComParesDaEsquerda = [row[3] for row in TableBruto]
                                ListaComParesDaDireita = [row[4] for row in TableBruto]
                                ListaDeMoedas = ListaComParesDaEsquerda
                                ListaDeMoedas.extend(ListaComParesDaDireita)
                                ListaDeMoedas = list(map(lambda coin: coin.upper(), ListaDeMoedas))
                                ListaDeMoedas = list(dict.fromkeys(ListaDeMoedas))
                                try:ListaDeMoedas.remove('')
                                except:pass
                                try:ListaDeMoedas.remove(None)
                                except:pass
                                qqtMoedasNovas = 0

                                for coin in ListaDeMoedas:
                                    if (not coin == UserCoin and
                                        not AtivoExisteNaTabelaDeCotacoes(coin) and
                                        not AtivoExisteNaFolhaDeCotacoes(coin, Cotacoes)):
                                        qqtMoedasNovas += 1
                                if qqtMoedasNovas == 1: MessageBox_Msg1 = QMessageBox.about(self,'Aviso',"Identificamos uma nova moeda na base de dados proveniente da\n"+TableNameBruto+".\nA operação seguinte pode levar alguns minutos,\npois irá buscar online a cotação atual da moeda.\nNÃO FECHE O PROGRAMA DURANTE O PROCESSO SEGUINTE!")
                                elif qqtMoedasNovas > 1: MessageBox_Msg1 = QMessageBox.about(self,'Aviso',"Identificamos novas moedas na base de dados ("+str(qqtMoedasNovas)+") proveniente da\n"+TableNameBruto+".\nA operação seguinte pode levar alguns minutos,\npois irá buscar online a cotação atual de cada moeda.\nNÃO FECHE O PROGRAMA DURANTE O PROCESSO SEGUINTE!")

                                thread_list = []
                                for coin in ListaDeMoedas:
                                    thread_list.append(BP(ThreadName='Thread_GetCotacaoCripto_FromExcelImportation',
                                                          HMI=self,
                                                          ativo=coin,
                                                          currency=UserCoin,
                                                          Cotacoes=Cotacoes))

                                for thread in thread_list: thread.start()
                                for thread in thread_list: thread.join()

                        # self.DBManager.CalcularTributacao() # Via thread
                        self.HMI_Tributacao.CalcularTributacao_SemThread() # Via sequencial, mas tem que comentar as linhas que tem self.HMI.DBManager.LW... em HMI_Tributação.py # Debug
                        self.DBManager.UpdatePatrimonioRendimento()

                        MessageBox_Msg1 = QMessageBox.about(self,'Informação','Importação bem sucedida.\nBem-vindo de volta '+UserName+'\nAcesse sua conta entrando pela página inicial.')
                    except Exception as msg:
                        if "Operação cancelada." in repr(msg):
                            self.DBManager.Disconnect()
                            MessageBox_Msg1 = QMessageBox.about(self,'Informação','Importação cancelada.')
                        else:
                            try:
                                self.DBManager.DeleteUserDB()
                            except:
                                self.DBManager.Disconnect()
                                print("Problema ao cancelar o processo...\nArquivo de usuário pode ter sido criado, mas deve estar corrompido.")
                            MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Importação mal sucedida.\n(Arquivo fora do formato esperado)\n'+str(msg))
                    finally:
                        self.CreatePage("0")

        elif ButtonPressed == "Abrir Calendário":
            if not self.OutraJanelaAberta:
                self.Window_Calendario = Calendario(self)
                self.Window_Calendario.Abrir()
            elif self.CalendarWindowOpen:
                self.Window_Calendario.close()
                self.Window_Calendario.show()
            elif self.ClockWindowOpen:
                self.Window_Relogio.close()
                self.Window_Relogio.show()

        elif ButtonPressed == "Abrir Relógio":
            if not self.OutraJanelaAberta:
                self.Window_Relogio = Relogio(self)
                self.Window_Relogio.Abrir()
            elif self.CalendarWindowOpen:
                self.Window_Calendario.close()
                self.Window_Calendario.show()
            elif self.ClockWindowOpen:
                self.Window_Relogio.close()
                self.Window_Relogio.show()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            if self.PageIDAux in ['9', '45']:
                if self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id, PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id, PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id, PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id, PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id, PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id, PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id, PAGE_BY_NAME['AlterarNovaOperacaoManualBolsa'].page_id]: self.CreatePage(PAGE_BY_NAME['RegistrosBolsa'].page_id)
                elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id, PAGE_BY_NAME['AlterarOperacaoCripto'].page_id]: self.CreatePage(PAGE_BY_NAME['RegistrosCripto'].page_id)
                else: self.CreatePage(self.PageID)
            elif self.PageIDAux in ['14', '15', '17a', '17b', 'ChooseCurrency']:
                self.CreatePage(PAGE_BY_NAME['Perfil'].page_id)
            elif self.PageID in [PAGE_BY_NAME['AuxilioSenha'].page_id, PAGE_BY_NAME['ImportarUsuario'].page_id, PAGE_BY_NAME['CriarUsuario'].page_id, PAGE_BY_NAME['AnaliseMercado'].page_id, PAGE_BY_NAME['AlteracaoSenha'].page_id]:
                self.CreatePage(PAGE_BY_NAME['Home'].page_id)
            elif self.PageID in [PAGE_BY_NAME['RecuperacaoEmail'].page_id]:
                self.CreatePage(PAGE_BY_NAME['AuxilioSenha'].page_id)
            elif self.PageID in [PAGE_BY_NAME['ConfirmacaoEmailCriar'].page_id]:
                self.CreatePage(PAGE_BY_NAME['CriarUsuario'].page_id)
            elif self.PageID in [PAGE_BY_NAME['EdicaoNegociacoes'].page_id, PAGE_BY_NAME['ARCA'].page_id, PAGE_BY_NAME['AnaliseMercadoDup'].page_id, PAGE_BY_NAME['Desempenho'].page_id, PAGE_BY_NAME['Tributacao'].page_id]:
                self.CreatePage(PAGE_BY_NAME['MinhaCarteira'].page_id)
            elif self.PageID in [PAGE_BY_NAME['AcoesNegocios'].page_id, PAGE_BY_NAME['RealEstate'].page_id, PAGE_BY_NAME['Caixa'].page_id, PAGE_BY_NAME['AtivosInternacionais'].page_id, PAGE_BY_NAME['CriptoARCA'].page_id]:
                self.CreatePage(PAGE_BY_NAME['ARCA'].page_id)
            elif self.PageID in [PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id, PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id, PAGE_BY_NAME['EditacaoContasCorrentesBancos'].page_id]:
                self.CreatePage(PAGE_BY_NAME['EdicaoNegociacoes'].page_id)
            elif self.PageID in['BancosAdd','BancosRename']:
                self.CreatePage(PAGE_BY_NAME['EditacaoContasCorrentesBancos'].page_id)
            elif self.PageID in [PAGE_BY_NAME['AdicionarCorretoraBolsa'].page_id, PAGE_BY_NAME['RenomearCorretoraBolsa'].page_id, PAGE_BY_NAME['RegistrosBolsa'].page_id, PAGE_BY_NAME['InformarDepositosSaqBolsa'].page_id, PAGE_BY_NAME['SaldoContaCorrenteBolsa'].page_id]:
                self.CreatePage(PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id)
            elif self.PageID in [PAGE_BY_NAME['AdicionarNovoAtivo'].page_id, PAGE_BY_NAME['RenomearAtivo'].page_id, PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id, PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id, PAGE_BY_NAME['DeletarOperacoesBolsa'].page_id]:
                self.CreatePage(PAGE_BY_NAME['RegistrosBolsa'].page_id)
            elif self.PageID in [PAGE_BY_NAME['NaoImplementada31a'].page_id, PAGE_BY_NAME['NaoImplementada32a'].page_id, '33a', PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id, PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id]:
                self.CreatePage(PAGE_BY_NAME['AdicionarNovoAtivo'].page_id)
            elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id]:
                self.CreatePage(PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id)
            elif self.PageID in [PAGE_BY_NAME['AlterarNovaOperacaoManualBolsa'].page_id]:
                self.CreatePage(PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id)
            elif self.PageID in [PAGE_BY_NAME['NaoImplementada31b'].page_id, PAGE_BY_NAME['NaoImplementada32b'].page_id, '33b', PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id, PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id]:
                self.CreatePage(PAGE_BY_NAME['RenomearAtivo'].page_id)
            elif self.PageID in [PAGE_BY_NAME['AdicionarCorretoraCripto'].page_id, PAGE_BY_NAME['RenomearCorretoraCripto'].page_id, PAGE_BY_NAME['RegistrosCripto'].page_id]:
                self.CreatePage(PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id)
            elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id, PAGE_BY_NAME['AlterarOperacaoCripto'].page_id, PAGE_BY_NAME['DeletarOperacaoCripto'].page_id]:
                self.CreatePage(PAGE_BY_NAME['RegistrosCripto'].page_id)
            elif self.PageID in ['42']:
                self.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id)
            elif self.PageID in ['34c', '35c']:
                self.CreatePage(PAGE_BY_NAME['IdeiaAbandonada'].page_id)
            elif self.PageID in [PAGE_BY_NAME['ImportacaoUsuario'].page_id]:
                self.CreatePage(PAGE_BY_NAME['ImportarUsuario'].page_id)
            elif self.PageID in [PAGE_BY_NAME['ConfirmacaoEmailImportar'].page_id]:
                self.CreatePage(PAGE_BY_NAME['ImportacaoUsuario'].page_id)
        elif key == Qt.Key_H: self.OnButtonPressed('ShowHideValues')
        elif key == Qt.Key_P: self.CreatePage(PAGE_BY_NAME['Perfil'].page_id)
        elif key == Qt.Key_C: self.CreatePage(PAGE_BY_NAME['InsercaoCotacoesManuais'].page_id)
        elif key == Qt.Key_M: self.CreatePage(PAGE_BY_NAME['MinhaCarteira'].page_id)
        elif key == Qt.Key_N: self.CreatePage(PAGE_BY_NAME['EdicaoNegociacoes'].page_id)
        elif key == Qt.Key_T: self.CreatePage(PAGE_BY_NAME['Tributacao'].page_id)
        elif key == Qt.Key_A: self.CreatePage(PAGE_BY_NAME['ARCA'].page_id)
        elif key == Qt.Key_D: self.CreatePage(PAGE_BY_NAME['Desempenho'].page_id)

    def eventFilter(self, obj, event): # Função pra redimensionar alguns elementos do IHM dinamicamente
        if event.type() == QEvent.Resize:
            try:
                if self.PageIDAux== PAGE_BY_NAME['Perfil'].page_id:
                    self.Button_ProfilePhoto.setFixedSize(int(self.frameGeometry().width()/8),int(self.frameGeometry().width()/8))
                    self.Button_ProfilePhoto.setIconSize(QSize(int(self.frameGeometry().width()/8*.95),int(self.frameGeometry().width()/8*.95)))

                    self.Button_ExportDBToDB.setFixedSize(int(self.frameGeometry().width()*15/20/2),int(self.frameGeometry().height()-160))
                    self.Button_ExportDBToDB.setIconSize(QSize(int(self.frameGeometry().width()*15/20/2*.98),int(self.frameGeometry().height())))

                    self.Button_ExportDBToExcel.setFixedSize(int(self.frameGeometry().width()*15/20/2),int(self.frameGeometry().height()-160))
                    self.Button_ExportDBToExcel.setIconSize(QSize(int(self.frameGeometry().width()*15/20/2*.98),int(self.frameGeometry().height())))

                elif self.PageIDAux== PAGE_BY_NAME['InsercaoCotacoesManuais'].page_id:
                    HHeader = ['Ativo',
                               'Última atualização',
                               'Cotação em '+self.DBManager.GetUserCoinCurrency()]
                    SizeCol0, SizeCol1, SizeCol2 = self.GetSizeOfTableColumns(self.data_45_1, HHeader)
                    self.SetTableWidth_45_1(SizeCol0, SizeCol1, SizeCol2)
                    self.Table_CotaçõesManuais.setFixedHeight(int(self.frameGeometry().height()*6/10))

                elif self.PageID== PAGE_BY_NAME['Home'].page_id: # Home Page Not Logged In
                    self.Button_Mercado.setFixedSize(int(self.frameGeometry().width()*3/4*.9),int(self.frameGeometry().height()/4*.95))
                    self.Movie_Mercado.setScaledSize(QSize().scaled(int(self.frameGeometry().width()*3/4*.90),int(self.frameGeometry().height()*3/4*.95), Qt.KeepAspectRatio))
                    self.TextBox_NomeDeUsuario.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.TextBox_Senha.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_LogIn.setFixedSize(int(self.frameGeometry().width()/3*0.9),int(self.frameGeometry().height()/10))
                    self.Button_LogIn.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_MercadoInvisivel.setFixedSize(int(self.frameGeometry().width()*3/4*.90),int(self.frameGeometry().height()*3/4*.95))

                elif self.PageID== PAGE_BY_NAME['MinhaCarteira'].page_id:
                    self.Movie_Negociações.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20), Qt.KeepAspectRatio))
                    self.Button_Negociações.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
                    self.Button_NegociaçõesInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-160))

                    self.Movie_Tributacao.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20), Qt.KeepAspectRatio))
                    self.Button_Tributacao.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
                    self.Button_TributacaoInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-160))

                    self.Movie_ARCA.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20), Qt.KeepAspectRatio))
                    self.Button_ARCA.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
                    self.Button_ARCAInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20))

                    self.Movie_Desempenho.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20), Qt.KeepAspectRatio))
                    self.Button_Desempenho.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
                    self.Button_DesempenhoInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20))

                    self.Movie_Mercado.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-110), Qt.KeepAspectRatio))
                    self.Button_Mercado.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
                    self.Button_MercadoInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-110))

                elif self.PageID== PAGE_BY_NAME['ImportarUsuario'].page_id:
                    self.Button_ExportDBToExcel.setFixedSize(int(self.frameGeometry().width()*2/5),int(self.frameGeometry().height()-160))
                    self.Button_ExportDBToDB.setFixedSize(int(self.frameGeometry().width()*2/5),int(self.frameGeometry().height()-160))

                elif self.PageID== PAGE_BY_NAME['CriarUsuario'].page_id:
                    minimo = 24
                    maximo = 36
                    a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
                    b = self.screen_width-(a/minimo)
                    razao = (self.frameGeometry().width()-b)/a
                    self.Label_NomeDeUsuario.setText('Nome de usuário:'+str((' ')*int(self.frameGeometry().width()*razao)))

                    minimo = 19
                    maximo = 21
                    a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
                    b = self.screen_width-(a/minimo)
                    razao = (self.frameGeometry().width()-b)/a
                    self.Label_Email.setText('Email:'+str((' ')*int(self.frameGeometry().width()*razao)))

                    minimo = 19
                    maximo = 21
                    a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
                    b = self.screen_width-(a/minimo)
                    razao = (self.frameGeometry().width()-b)/a
                    self.Label_Senha1.setText('Senha:'+str((' ')*int(self.frameGeometry().width()*razao)))

                    minimo = 24
                    maximo = 39
                    a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
                    b = self.screen_width-(a/minimo)
                    razao = (self.frameGeometry().width()-b)/a
                    self.Label_Senha2.setText('Confirme a senha:'+str((' ')*int(self.frameGeometry().width()*razao)))

                    self.TextBox_NomeDeUsuario.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.TextBox_Email.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                    self.TextBox_Senha1.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.TextBox_Senha2.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                    self.Button_ConfirmacaoDeEmail.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_ConfirmacaoDeEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['EdicaoNegociacoes'].page_id:
                    self.Button_TradesCriptomoedasInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-160))
                    self.Button_TradesCriptomoedas.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
                    self.Movie_TradesCriptomoedas.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-160), Qt.KeepAspectRatio))
                    self.Button_TradesBolsaInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-160))
                    self.Button_TradesBolsa.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
                    self.Movie_TradesBolsa.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-160), Qt.KeepAspectRatio))
                    self.Button_BancosInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-160))
                    self.Button_Bancos.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
                    self.Movie_Bancos.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-160), Qt.KeepAspectRatio))

                elif self.PageID== PAGE_BY_NAME['EditacaoContasCorrentesBancos'].page_id:
                    self.Button_AtuatizarCC.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_AtuatizarCC.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['AdicionarNovoBanco'].page_id:
                    self.Button_AdicionarBanco.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_AdicionarBanco.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['RenomearBanco'].page_id:
                    self.Button_RenomearBanco.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_RenomearBanco.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['ARCA'].page_id:
                    if self.frameGeometry().width()/self.frameGeometry().height() < 1.9577: proporcao = 1/6
                    elif self.frameGeometry().width()/self.frameGeometry().height() < 2.6202: proporcao = 1/8
                    else: proporcao = 1/10

                    self.Button_CarteiraInvisivel.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.Button_AcoesENegociosInvisivel.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.Button_RealEstateInvisivel.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.Button_CaixaInvisivel.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.Button_AcoesInternacionaisInvisivel.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.Button_EspecificaInvisivel.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.GraphWidget_Carteira.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.GraphWidget_AcoesENegocios.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.GraphWidget_RealEstate.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.GraphWidget_Caixa.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.GraphWidget_AtivosInternacionais.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))
                    self.GraphWidget_Especifica.setFixedSize(int(self.frameGeometry().width()*proporcao),int(self.frameGeometry().width()*proporcao))

                    self.TextBox_MontanteNasCorretoras.setFixedWidth(int(self.frameGeometry().width()/6))
                    self.TextBox_MontanteAplicado.setFixedWidth(int(self.frameGeometry().width()/6))

                    self.TextBox_GastoMensal.setFixedWidth(int(self.frameGeometry().width()/10))
                    self.TextBox_MesesDeReserva.setFixedWidth(int(self.frameGeometry().width()/20))
                    self.TextBox_Aplicar.setFixedWidth(int(self.frameGeometry().width()/10))

                    self.Table_ContasCorrente.setFixedHeight(int(self.frameGeometry().height()*3/10))

                elif self.PageID== PAGE_BY_NAME['Desempenho'].page_id:
                    self.Movie_Grafico2.setScaledSize(QSize().scaled(int(self.frameGeometry().width()),int(self.frameGeometry().height()/5*.95), Qt.KeepAspectRatio))
                    self.Movie_Grafico1.setScaledSize(QSize().scaled(int(self.frameGeometry().width()),int(self.frameGeometry().height()/5*.95), Qt.KeepAspectRatio))

                elif self.PageID in [PAGE_BY_NAME['AnaliseMercado'].page_id,PAGE_BY_NAME['AnaliseMercadoDup'].page_id]:
                    self.Movie_Mercado1.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-110), Qt.KeepAspectRatio))
                    self.Button_Mercado1.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
                    self.Button_MercadoInvisivel1.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-110))
                    self.Movie_Mercado2.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-110), Qt.KeepAspectRatio))
                    self.Button_Mercado2.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
                    self.Button_MercadoInvisivel2.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-110))
                    self.Movie_Mercado3.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-110), Qt.KeepAspectRatio))
                    self.Button_Mercado3.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
                    self.Button_MercadoInvisivel3.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-110))
                    if self.frameGeometry().width() < self.screen_width*0.7:
                        self.Button_Mercado1.setFont(self.font20)
                        self.Button_Mercado2.setFont(self.font20)
                        self.Button_Mercado3.setFont(self.font20)
                    else:
                        self.Button_Mercado1.setFont(self.font24)
                        self.Button_Mercado2.setFont(self.font24)
                        self.Button_Mercado3.setFont(self.font24)

                elif self.PageID== PAGE_BY_NAME['MudarSenha'].page_id:
                    minimo = 23
                    maximo = 43
                    a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
                    b = self.screen_width-(a/minimo)
                    razao = (self.frameGeometry().width()-b)/a
                    self.Label_SenhaAtual.setText('Insira a senha atual:'+str((' ')*int(self.frameGeometry().width()*razao)))

                    minimo = 33
                    maximo = 47
                    a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
                    b = self.screen_width-(a/minimo)
                    razao = (self.frameGeometry().width()-b)/a
                    self.Label_Senha1.setText('Crie uma nova senha:'+str((' ')*int(self.frameGeometry().width()*razao)))

                    minimo = 21
                    maximo = 38
                    a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
                    b = self.screen_width-(a/minimo)
                    razao = (self.frameGeometry().width()-b)/a
                    self.Label_Senha2.setText('Confirme a senha:'+str((' ')*int(self.frameGeometry().width()*razao)))

                elif self.PageID== PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id:
                    self.Movie_AlterarOPBolsa.setScaledSize(QSize().scaled(int(self.frameGeometry().width()*12/20/2),int(self.frameGeometry().height()*7/10*.95-30), Qt.KeepAspectRatio))
                    self.Button_AlterarOPBolsaInvisivel.setFixedSize(int(self.frameGeometry().width()*12/20/2),int(self.frameGeometry().height()*7/10*.95))
                    self.Button_AlterarOPBolsa.setFixedSize(int(self.frameGeometry().width()*12/20/2),int(self.frameGeometry().height()*1/10*.95))
                    self.Movie_DepositosESaquesBolsa.setScaledSize(QSize().scaled(int(self.frameGeometry().width()*12/20/2),int(self.frameGeometry().height()*3/10*.95-30), Qt.KeepAspectRatio))
                    self.Button_DepositosESaquesBolsaInvisivel.setFixedSize(int(self.frameGeometry().width()*12/20/2),int(self.frameGeometry().height()*3/10*.95))
                    self.Button_DepositosESaquesBolsa.setFixedSize(int(self.frameGeometry().width()*12/20/2),int(self.frameGeometry().height()*1/10*.95))
                    self.Movie_ContaCorrenteBolsa.setScaledSize(QSize().scaled(int(self.frameGeometry().width()*12/20/2),int(self.frameGeometry().height()*3/10*.95-30), Qt.KeepAspectRatio))
                    self.Button_ContaCorrenteBolsaInvisivel.setFixedSize(int(self.frameGeometry().width()*12/20/2),int(self.frameGeometry().height()*3/10*.95))
                    self.Button_ContaCorrenteBolsa.setFixedSize(int(self.frameGeometry().width()*12/20/2),int(self.frameGeometry().height()*1/10*.95))

                elif self.PageID== PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id:
                    self.Movie_AlterarOPCriptomoedas.setScaledSize(QSize().scaled(int(self.frameGeometry().width()*12/20),int(self.frameGeometry().height()*7/10*.95-60), Qt.KeepAspectRatio))
                    self.Button_AlterarOPCriptomoedasInvisivel.setFixedSize(int(self.frameGeometry().width()*12/20),int(self.frameGeometry().height()*7/10*.95))
                    self.Button_AlterarOPCriptomoedas.setFixedSize(int(self.frameGeometry().width()*12/20),int(self.frameGeometry().height()*1/10*.95))

                elif self.PageID== PAGE_BY_NAME['AdicionarCorretoraBolsa'].page_id:
                    self.TextBox_NovaCorretora.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_AdicionarCorretora.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_AdicionarCorretora.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID == PAGE_BY_NAME['ConfirmarDeletarCorretoraBolsa'].page_id:pass

                elif self.PageID== PAGE_BY_NAME['RenomearCorretoraBolsa'].page_id:
                    self.TextBox_NovoNomeCorretora.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_RenomearCorretora.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_RenomearCorretora.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['RegistrosBolsa'].page_id:
                    HHeader = ['Data',
                               'Tipo',
                               'Qqt',
                               'Preço',
                               'Corretagem',
                               'Taxa B3%',
                               'Taxa B3',
                               'Obs']
                    SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.GetSizeOfTableColumns(self.HMI_Trades.HMI_Trades_Bolsa.data_23_1, HHeader)

                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setFixedHeight(int(self.frameGeometry().height()*1/20))
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.adjustSize()
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(0, SizeCol0)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(1, SizeCol1)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(2, SizeCol2)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(3, SizeCol3)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(4, SizeCol4)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(5, SizeCol5)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(6, SizeCol6)

                    self.Table_Operacoes_Realizadas_com_Ativo.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
                    self.Table_Operacoes_Realizadas_com_Ativo.setFixedHeight(int(self.frameGeometry().height()*6/20*1.4))
                    self.Table_Operacoes_Realizadas_com_Ativo.resizeColumnsToContents()
                    self.Table_Operacoes_Realizadas_com_Ativo.adjustSize()
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(0, SizeCol0)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(1, SizeCol1)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(2, SizeCol2)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(3, SizeCol3)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(4, SizeCol4)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(5, SizeCol5)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(6, SizeCol6)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(7, SizeCol7)

                elif self.PageID== PAGE_BY_NAME['InformarDepositosSaqBolsa'].page_id:
                    self.Button_Voltar.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Voltar.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Registrar.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Registrar.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Table_DepositosESaques.setFixedHeight(int(self.frameGeometry().height()*5/20*1.4))

                elif self.PageID== PAGE_BY_NAME['SaldoContaCorrenteBolsa'].page_id:
                    self.Button_Voltar.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Voltar.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Atualizar.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Atualizar.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['AdicionarNovoAtivo'].page_id:
                    self.TextBox_NomeNovoAtivo.setFixedWidth(int(self.frameGeometry().width()/8*0.9))
                    self.Button_Seguinte.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Seguinte.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['RenomearAtivo'].page_id:
                    self.TextBox_NovoNomeAtivo.setFixedWidth(int(self.frameGeometry().width()/8*0.9))
                    self.Button_Seguinte.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Seguinte.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id:
                    self.TextBox_Qqt.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Preco.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Corretagem.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_TaxaB3.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Obs.setFixedWidth(int(self.frameGeometry().width()*4/7*0.9))
                    self.Button_LimparCampos.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))
                    self.Button_RegistrarOperacao.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_RegistrarOperacao.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))

                elif self.PageID== PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id:
                    HHeader = ['Data',
                               'Tipo',
                               'Qqt',
                               'Preço',
                               'Corretagem',
                               'Taxa B3%',
                               'Taxa B3',
                               'Obs']
                    SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.GetSizeOfTableColumns(self.HMI_Trades.HMI_Trades_Bolsa.data_23_1, HHeader)

                    self.Table_Operacoes_SelecionadasHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
                    self.Table_Operacoes_SelecionadasHeader.setFixedHeight(int(self.frameGeometry().height()*1/20))
                    self.Table_Operacoes_SelecionadasHeader.adjustSize()
                    self.Table_Operacoes_SelecionadasHeader.setColumnWidth(0, SizeCol0)
                    self.Table_Operacoes_SelecionadasHeader.setColumnWidth(1, SizeCol1)
                    self.Table_Operacoes_SelecionadasHeader.setColumnWidth(2, SizeCol2)
                    self.Table_Operacoes_SelecionadasHeader.setColumnWidth(3, SizeCol3)
                    self.Table_Operacoes_SelecionadasHeader.setColumnWidth(4, SizeCol4)
                    self.Table_Operacoes_SelecionadasHeader.setColumnWidth(5, SizeCol5)
                    self.Table_Operacoes_SelecionadasHeader.setColumnWidth(6, SizeCol6)
                    self.Table_Operacoes_SelecionadasHeader.setColumnWidth(7, SizeCol7)

                    self.Table_Operacoes_Selecionadas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
                    self.Table_Operacoes_Selecionadas.setFixedHeight(int(self.frameGeometry().height()*1/20))
                    self.Table_Operacoes_Selecionadas.resizeColumnsToContents()
                    self.Table_Operacoes_Selecionadas.adjustSize()
                    self.Table_Operacoes_Selecionadas.setColumnWidth(0, SizeCol0)
                    self.Table_Operacoes_Selecionadas.setColumnWidth(1, SizeCol1)
                    self.Table_Operacoes_Selecionadas.setColumnWidth(2, SizeCol2)
                    self.Table_Operacoes_Selecionadas.setColumnWidth(3, SizeCol3)
                    self.Table_Operacoes_Selecionadas.setColumnWidth(4, SizeCol4)
                    self.Table_Operacoes_Selecionadas.setColumnWidth(5, SizeCol5)
                    self.Table_Operacoes_Selecionadas.setColumnWidth(6, SizeCol6)
                    self.Table_Operacoes_Selecionadas.setColumnWidth(7, SizeCol7)

                    self.Button_LimparCampos.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))
                    self.Button_RegistrarOperacao.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_RegistrarOperacao.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))
                    self.TextBox_Qqt.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Preco.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Corretagem.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_TaxaB3.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Obs.setFixedWidth(int(self.frameGeometry().width()*4/7*0.9))

                elif self.PageID== PAGE_BY_NAME['DeletarOperacoesBolsa'].page_id:
                    HHeader = ['Data',
                               'Tipo',
                               'Qqt',
                               'Preço',
                               'Corretagem',
                               'Taxa B3%',
                               'Taxa B3',
                               'Obs']
                    SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.GetSizeOfTableColumns(self.HMI_Trades.HMI_Trades_Bolsa.data_23_1, HHeader)

                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setFixedHeight(int(self.frameGeometry().height()*1/20))
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.adjustSize()
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(0, SizeCol0)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(1, SizeCol1)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(2, SizeCol2)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(3, SizeCol3)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(4, SizeCol4)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(5, SizeCol5)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(6, SizeCol6)
                    self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(7, SizeCol7)

                    self.Table_Operacoes_Realizadas_com_Ativo.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
                    self.Table_Operacoes_Realizadas_com_Ativo.setFixedHeight(int(self.frameGeometry().height()*6/20*1.4))
                    self.Table_Operacoes_Realizadas_com_Ativo.resizeColumnsToContents()
                    self.Table_Operacoes_Realizadas_com_Ativo.adjustSize()
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(0, SizeCol0)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(1, SizeCol1)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(2, SizeCol2)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(3, SizeCol3)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(4, SizeCol4)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(5, SizeCol5)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(6, SizeCol6)
                    self.Table_Operacoes_Realizadas_com_Ativo.setColumnWidth(7, SizeCol7)

                    self.Button_Cancelar.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))
                    self.Button_DeletarOperacoes.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_DeletarOperacoes.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))

                elif self.PageID== PAGE_BY_NAME['NaoImplementada31a'].page_id:
                    self.TextBox_NovoTipoDeAtivo.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Seguinte.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Seguinte.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['NaoImplementada31b'].page_id:
                    self.TextBox_NovoTipoDeAtivo.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Seguinte.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Seguinte.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['NaoImplementada32a'].page_id:
                    self.TextBox_NovoSubtipoDeAtivo.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Seguinte.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Seguinte.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['NaoImplementada32b'].page_id:
                    self.TextBox_NovoSubtipoDeAtivo.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Seguinte.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Seguinte.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID == PAGE_BY_NAME['33a'].page_id:
                    self.TextBox_NovoTipoSetor.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Seguinte.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Seguinte.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID == PAGE_BY_NAME['33b'].page_id:
                    self.TextBox_NovoSetor.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Seguinte.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Seguinte.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id:
                    self.Button_Voltar.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Voltar.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_AtivarModoManual.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_AtivarModoManual.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Seguinte.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Seguinte.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Info1.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Info1.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id:
                    self.Button_Voltar.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Voltar.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_AtivarModoManual.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_AtivarModoManual.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Seguinte.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Seguinte.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Info1.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Info1.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id:
                    self.Button_Voltar.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Voltar.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_AtivarModoManual.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_AtivarModoManual.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Info1.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))

                elif self.PageID== PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id:
                    self.Button_Voltar.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Voltar.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_AtivarModoManual.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_AtivarModoManual.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
                    self.Button_Info1.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

                elif self.PageID== PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id:
                    self.TextBox_Modo.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Qqt.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Preco.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Corretagem.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_TaxaB3.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Obs.setFixedWidth(int(self.frameGeometry().width()*4/7*0.9))
                    self.Button_LimparCampos.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))
                    self.Button_RegistrarOperacao.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_RegistrarOperacao.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))

                elif self.PageID== PAGE_BY_NAME['RegistrosCripto'].page_id:
                    HHeader = ['Data',
                               'Par',
                               'Tipo',
                               'Preço',
                               'Qqt',
                               'Taxa',
                               'Moeda da taxa',
                               'Conversão',
                               'Obs']
                    SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7,SizeCol8 = self.GetSizeOfTableColumns(self.HMI_Trades.HMI_Trades_Criptomoedas.data_40_1, HHeader)

                    self.Table_Operacoes_RealizadasHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
                    self.Table_Operacoes_RealizadasHeader.setFixedHeight(int(self.frameGeometry().height()*1/20))
                    self.Table_Operacoes_RealizadasHeader.adjustSize()
                    self.Table_Operacoes_RealizadasHeader.setColumnWidth(0, SizeCol0)
                    self.Table_Operacoes_RealizadasHeader.setColumnWidth(1, SizeCol1)
                    self.Table_Operacoes_RealizadasHeader.setColumnWidth(2, SizeCol2)
                    self.Table_Operacoes_RealizadasHeader.setColumnWidth(3, SizeCol3)
                    self.Table_Operacoes_RealizadasHeader.setColumnWidth(4, SizeCol4)
                    self.Table_Operacoes_RealizadasHeader.setColumnWidth(5, SizeCol5)
                    self.Table_Operacoes_RealizadasHeader.setColumnWidth(6, SizeCol6)
                    self.Table_Operacoes_RealizadasHeader.setColumnWidth(7, SizeCol7)

                    self.Table_Operacoes_Realizadas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
                    self.Table_Operacoes_Realizadas.setFixedHeight(int(self.frameGeometry().height()*6/20*1.4))
                    self.Table_Operacoes_Realizadas.resizeColumnsToContents()
                    self.Table_Operacoes_Realizadas.adjustSize()
                    self.Table_Operacoes_Realizadas.setColumnWidth(0, SizeCol0)
                    self.Table_Operacoes_Realizadas.setColumnWidth(1, SizeCol1)
                    self.Table_Operacoes_Realizadas.setColumnWidth(2, SizeCol2)
                    self.Table_Operacoes_Realizadas.setColumnWidth(3, SizeCol3)
                    self.Table_Operacoes_Realizadas.setColumnWidth(4, SizeCol4)
                    self.Table_Operacoes_Realizadas.setColumnWidth(5, SizeCol5)
                    self.Table_Operacoes_Realizadas.setColumnWidth(6, SizeCol6)
                    self.Table_Operacoes_Realizadas.setColumnWidth(7, SizeCol7)
                    self.Table_Operacoes_Realizadas.setColumnWidth(8, SizeCol8)

                elif self.PageID== PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id:
                    self.TextBox_Par_Esquerda.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Par_Direita.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Qqt.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Preco.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Taxa.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_MoedaDaTaxa.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Conversao.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.Button_BuscarConversao.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Obs.setFixedWidth(int(self.frameGeometry().width()*4/7*0.9))
                    self.Button_LimparCampos.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))
                    self.Button_RegistrarOperacao.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_RegistrarOperacao.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))

                elif self.PageID== PAGE_BY_NAME['AlterarOperacaoCripto'].page_id:
                    self.HMI_Trades.HMI_Trades_Criptomoedas.CreateTable_43_1() # Table_Operacoes_SelecionadasHeader
                    self.HMI_Trades.HMI_Trades_Criptomoedas.CreateTable_43_2() # Table_Operacoes_Selecionadas (Mostra apenas o item selecionado)

                    self.TextBox_Par_Esquerda.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Par_Direita.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Qqt.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Preco.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Taxa.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_MoedaDaTaxa.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Conversao.setFixedWidth(int(self.frameGeometry().width()/7*0.9))
                    self.TextBox_Obs.setFixedWidth(int(self.frameGeometry().width()*4/7*0.9))
                    self.Button_LimparCampos.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))
                    self.Button_RegistrarOperacao.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_RegistrarOperacao.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))

                elif self.PageID== PAGE_BY_NAME['DeletarOperacaoCripto'].page_id:
                    self.HMI_Trades.HMI_Trades_Criptomoedas.CreateTable_44_1() # Table_Operacoes_SelecionadasHeader
                    self.HMI_Trades.HMI_Trades_Criptomoedas.CreateTable_44_2() # Table_Operacoes_Selecionadas (Mostra apenas o item selecionado)

                    self.Button_Cancelar.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_Cancelar.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))
                    self.Button_DeletarOperacoes.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
                    self.Button_DeletarOperacoes.setFixedSize(int(self.frameGeometry().width()*2/10*0.9),int(self.frameGeometry().width()*1/10*0.9))

                elif self.PageID== PAGE_BY_NAME['Tributacao'].page_id:
                    self.Table_Tributacao.setFixedHeight(int(self.frameGeometry().height()*6/20*1.4))
                    if not self.DTeST_51 == "DTeST":
                        HHeader = ['Mês/Ano',
                                   'Resultado líquido',
                                   'Imposto devido',
                                   'Alíquota',
                                   'Lucro mínimo taxável',
                                   'Resultado bruto',
                                   'Prejuízo acumulado',
                                   'Resultado final']

                        if int(self.frameGeometry().width()*6/20*1.4) < 510:
                            self.Table_Tributacao_Header.setFont(self.font10)
                            self.Table_Tributacao.setFont(self.font10)
                        else:
                            self.Table_Tributacao_Header.setFont(self.font14)
                            self.Table_Tributacao.setFont(self.font14)
                    else:
                        HHeader = ['Mês/Ano',
                                   'Resultado líquido',
                                   'Imposto devido',
                                   'Resultado bruto',
                                   'Prejuízo acumulado',
                                   'Resultado final']
                    if not self.DTeST_51 == "DTeST":
                        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5,SizeCol6,SizeCol7 = self.GetSizeOfTableColumns(self.HMI_Tributacao.data_51_1, HHeader)

                        self.Table_Tributacao_Header.adjustSize()
                        self.Table_Tributacao_Header.setColumnWidth(0, SizeCol0)
                        self.Table_Tributacao_Header.setColumnWidth(1, SizeCol1)
                        self.Table_Tributacao_Header.setColumnWidth(2, SizeCol2)
                        self.Table_Tributacao_Header.setColumnWidth(3, SizeCol3)
                        self.Table_Tributacao_Header.setColumnWidth(4, SizeCol4)
                        self.Table_Tributacao_Header.setColumnWidth(5, SizeCol5)
                        self.Table_Tributacao_Header.setColumnWidth(6, SizeCol6)
                        self.Table_Tributacao_Header.setColumnWidth(7, SizeCol7)

                        self.Table_Tributacao.adjustSize()
                        self.Table_Tributacao.setColumnWidth(0, SizeCol0)
                        self.Table_Tributacao.setColumnWidth(1, SizeCol1)
                        self.Table_Tributacao.setColumnWidth(2, SizeCol2)
                        self.Table_Tributacao.setColumnWidth(3, SizeCol3)
                        self.Table_Tributacao.setColumnWidth(4, SizeCol4)
                        self.Table_Tributacao.setColumnWidth(5, SizeCol5)
                        self.Table_Tributacao.setColumnWidth(6, SizeCol6)
                        self.Table_Tributacao.setColumnWidth(7, SizeCol7)
                    else:
                        SizeCol0,SizeCol1,SizeCol2,SizeCol3,SizeCol4,SizeCol5 = self.GetSizeOfTableColumns(self.HMI_Tributacao.data_51_1, HHeader)

                        self.Table_Tributacao_Header.adjustSize()
                        self.Table_Tributacao_Header.setColumnWidth(0, SizeCol0)
                        self.Table_Tributacao_Header.setColumnWidth(1, SizeCol1)
                        self.Table_Tributacao_Header.setColumnWidth(2, SizeCol2)
                        self.Table_Tributacao_Header.setColumnWidth(3, SizeCol3)
                        self.Table_Tributacao_Header.setColumnWidth(4, SizeCol4)
                        self.Table_Tributacao_Header.setColumnWidth(5, SizeCol5)

                        self.Table_Tributacao.adjustSize()
                        self.Table_Tributacao.setColumnWidth(0, SizeCol0)
                        self.Table_Tributacao.setColumnWidth(1, SizeCol1)
                        self.Table_Tributacao.setColumnWidth(2, SizeCol2)
                        self.Table_Tributacao.setColumnWidth(3, SizeCol3)
                        self.Table_Tributacao.setColumnWidth(4, SizeCol4)
                        self.Table_Tributacao.setColumnWidth(5, SizeCol5)

            except:pass
        return False
