"""
Created on Sun Sep  5 01:44:04 2021

@author: Caio Moreira Porta
"""
from src.app.core.logger_setup import logger

import os
import traceback
import sys
import time
import smtplib, ssl
from calendar import monthrange
from PyQt5.QtGui import QCursor, QIcon, QMovie
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QPushButton)
from PyQt5.QtCore import QCoreApplication, QSize, Qt
from ui.popup.LoadingWindow import LoadingWindow
from core.BackgroundProcesses import BackgroundProcess as BP
from ui.pages import PAGE_BY_NAME


class HMI_Presentation:
    def UpdatePage(self):
        if self.PageID== PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id:
            UserCoin = self.DBManager.GetCorretoraCoinCurrency(self.BolsaOuCripto,
                                                               self.ComboBox_Corretoras.currentText())
            corretora = self.ComboBox_Corretoras.currentText()
            self.idxCorretora = self.ComboBox_Corretoras.currentIndex()
            self.Label_Title2.setText(corretora)
            self.TextBox_Msg2.setText(UserCoin+' ~'+str(self.DBManager.GetPatrimonioTotalCorretora(self.ComboBox_Corretoras.currentText(),
                                                                                                   self.BolsaOuCripto,
                                                                                                   )))
            Investido = round(self.DBManager.GetTotalInvestidoEmCorretora(corretora, "Bolsa"), 2)
            self.TextBox_Msg6.setText(UserCoin+' ~'+str(Investido))
            self.TextBox_Msg3.setText(UserCoin+' '+str(self.DBManager.GetValorEmContaCorrente(self.BolsaOuCripto,
                                                                                              self.ComboBox_Corretoras.currentText(),
                                                                                              )))
            self.TextBox_Msg4.setText(self.DBManager.GetDataUltimaOPRegistrada(self.BolsaOuCripto, self.ComboBox_Corretoras.currentText()))
            valor = round(self.DBManager.GetUltimoDepositoOuSaqueRegistrado(self.BolsaOuCripto, corretora),2)
            self.TextBox_Msg5.setText(UserCoin+' '+str(valor))
            if valor >= 0: self.TextBox_Msg5.setStyleSheet('QLineEdit {background-color: black; color: green;}')
            else: self.TextBox_Msg5.setStyleSheet('QLineEdit {background-color: black; color: orange;}')
        elif self.PageID== PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id:
            UserCoin = self.DBManager.GetCorretoraCoinCurrency(self.BolsaOuCripto,
                                                               self.ComboBox_Corretoras.currentText())
            corretora = self.ComboBox_Corretoras.currentText()
            self.Label_Title2.setText(corretora)
            self.TextBox_Msg2.setText(UserCoin+' ~'+str(self.DBManager.GetPatrimonioTotalCorretora(self.ComboBox_Corretoras.currentText(),
                                                                                                   self.BolsaOuCripto,
                                                                                                   )))
            Investido = round(self.DBManager.GetTotalInvestidoEmCorretora(corretora, "Cripto"), 2)
            self.TextBox_Msg6.setText(UserCoin+' ~'+str(Investido))
            self.TextBox_Msg3.setText(UserCoin+' '+str(self.DBManager.GetValorEmContaCorrente(self.BolsaOuCripto,
                                                                                              self.ComboBox_Corretoras.currentText(),
                                                                                              )))
            self.TextBox_Msg4.setText(self.DBManager.GetDataUltimaOPRegistrada(self.BolsaOuCripto, self.ComboBox_Corretoras.currentText()))
            valor = self.DBManager.GetUltimoDepositoOuSaqueRegistrado(self.BolsaOuCripto, corretora)
            self.TextBox_Msg5.setText(UserCoin+' '+str(valor))
            if valor >= 0: self.TextBox_Msg5.setStyleSheet('QLineEdit {background-color: black; color: green;}')
            else: self.TextBox_Msg5.setStyleSheet('QLineEdit {background-color: black; color: orange;}')
        elif self.PageID== PAGE_BY_NAME['EditacaoContasCorrentesBancos'].page_id:
            self.idxBanco = self.ComboBox_Bancos.currentIndex()
            self.Label_Title2.setText(self.ComboBox_Bancos.currentText())
            self.TextBox_Msg2.setText(self.DBManager.GetBancoCoinCurrency(self.ComboBox_Bancos.currentText())+' '+str(self.DBManager.GetValorEmContaCorrente_Banco(self.ComboBox_Bancos.currentText())))
            self.Label_CC.setText("Valor atualizado ("+self.DBManager.GetBancoCoinCurrency(self.ComboBox_Bancos.currentText())+")")
        elif self.PageID== PAGE_BY_NAME['RegistrosBolsa'].page_id:
            self.Label_Msg1.setText('Operações realizadas com '+self.ComboBox_Ativos.currentText())
            self.HMI_Trades.HMI_Trades_Bolsa.CreateTable_23_1() # Table_Operacoes_Realizadas_com_AtivoHeader
            self.HMI_Trades.HMI_Trades_Bolsa.CreateTable_23_2() # Table_Operacoes_Realizadas_com_Ativo (Criada com uma thread)
            self.idxAtivo = self.ComboBox_Ativos.currentIndex()

            self.TextBox_Msg2.setText(str(self.DBManager.GetEstoque(self.BolsaOuCripto,
                                                                    corretora = self.ComboBox_Corretoras.currentText(),
                                                                    ativo = self.ComboBox_Ativos.currentText().replace(" ","_"),
                                                                    )))
        elif self.PageID== PAGE_BY_NAME['InformarDepositosSaqBolsa'].page_id:
            self.ComboBox_Dia.clear()
            for idx, dia in enumerate(range(1,monthrange(int(self.ComboBox_Ano.currentText()),int(self.ComboBox_Mes.currentText()))[1]+1)):
                self.ComboBox_Dia.addItem(str(dia))
        elif self.PageID== PAGE_BY_NAME['AdicionarNovoAtivo'].page_id:
            self.ComboBox_SubtipoDeAtivo.clear()
            for idx, Subtipo in enumerate(self.DBManager.GetSubtiposDeAtivo(self.ComboBox_TipoDeAtivo.currentText())):
                self.ComboBox_SubtipoDeAtivo.addItem(Subtipo)
                try:
                    if Subtipo == self.TextBox_SubtipoDeAtivo.text(): self.idxSubtipoDeAtivo = idx
                except Exception as e:
                    print(e, traceback.format_exception(None, e, e.__traceback__))
            if self.idxSubtipoDeAtivo < len(self.DBManager.GetSubtiposDeAtivo(self.ComboBox_TipoDeAtivo.currentText())):
                self.ComboBox_SubtipoDeAtivo.setCurrentIndex(self.idxSubtipoDeAtivo)
            self.ComboBox_SetorAtivo.clear()
            for idx, Setor in enumerate(self.DBManager.GetSetoresDeAtivo()):
                self.ComboBox_SetorAtivo.addItem(Setor)
                try:
                    if Setor == self.TextBox_SetorAtivo.text(): self.idxSetorAtivo = idx
                except Exception as e:
                    print(e, traceback.format_exception(None, e, e.__traceback__))
            if self.idxSetorAtivo < len(self.DBManager.GetSetoresDeAtivo()):
                self.ComboBox_SetorAtivo.setCurrentIndex(self.idxSetorAtivo)
            if self.ComboBox_TipoDeAtivo.currentText() == "Real Estate":
                self.ComboBox_SetorAtivo.setCurrentIndex(self.ComboBox_SetorAtivo.count()-1)
        elif self.PageID== PAGE_BY_NAME['RenomearAtivo'].page_id:
            self.ComboBox_SubtipoDeAtivo.clear()
            for idx, Subtipo in enumerate(self.DBManager.GetSubtiposDeAtivo(self.ComboBox_TipoDeAtivo.currentText())):
                self.ComboBox_SubtipoDeAtivo.addItem(Subtipo)
                try:
                    if Subtipo == self.TextBox_SubtipoDeAtivo.text(): self.idxSubtipoDeAtivo = idx
                except Exception as e:
                    print(e, traceback.format_exception(None, e, e.__traceback__))
            if self.idxSubtipoDeAtivo < len(self.DBManager.GetSubtiposDeAtivo(self.ComboBox_TipoDeAtivo.currentText())):
                self.ComboBox_SubtipoDeAtivo.setCurrentIndex(self.idxSubtipoDeAtivo)
            self.ComboBox_SetorAtivo.clear()
            for idx, Setor in enumerate(self.DBManager.GetSetoresDeAtivo()):
                self.ComboBox_SetorAtivo.addItem(Setor)
                try:
                    if Setor == self.TextBox_SetorAtivo.text(): self.idxSetorAtivo = idx
                except Exception as e:
                    print(e, traceback.format_exception(None, e, e.__traceback__))
            if self.idxSetorAtivo < len(self.DBManager.GetSetoresDeAtivo()):
                self.ComboBox_SetorAtivo.setCurrentIndex(self.idxSetorAtivo)
            if self.ComboBox_TipoDeAtivo.currentText() == "Real Estate":
                self.ComboBox_SetorAtivo.setCurrentIndex(self.ComboBox_SetorAtivo.count()-1)
        elif self.PageID== PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id:
            self.ComboBox_Dia.clear()
            for idx, dia in enumerate(range(1,monthrange(int(self.ComboBox_Ano.currentText()),int(self.ComboBox_Mes.currentText()))[1]+1)):
                self.ComboBox_Dia.addItem(str(dia))
        elif self.PageID== PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id:
            self.ComboBox_Dia.clear()
            for idx, dia in enumerate(range(1,monthrange(int(self.ComboBox_Ano.currentText()),int(self.ComboBox_Mes.currentText()))[1]+1)):
                self.ComboBox_Dia.addItem(str(dia))

        elif self.PageID== PAGE_BY_NAME['AcoesNegocios'].page_id:
            UserCoin = self.DBManager.GetUserCoinCurrency(self.LoggedIn)
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

            self.HMI_ARCA.Custo = 0
            self.HMI_ARCA.Retorno = 0
            if self.ComboBox_Ativos.currentText() == "Todos":
                for ativo in self.HMI_ARCA.ativos:
                    self.HMI_ARCA.Custo += self.DBManager.GetCustoAtivo(ativo, "Bolsa")
                    self.HMI_ARCA.Retorno += self.DBManager.GetEstoqueAtivo(ativo, "Bolsa") * self.DBManager.GetCotacao(ativo)
                coins = self.DBManager.GetAllAtivos_Cripto()
            elif self.ComboBox_Ativos.currentText() == "Criptos":
                coins = self.DBManager.GetAllAtivos_Cripto()
            else:
                self.HMI_ARCA.Custo = self.DBManager.GetCustoAtivo(self.ComboBox_Ativos.currentText(), "Bolsa")
                self.HMI_ARCA.Retorno = self.DBManager.GetEstoqueAtivo(self.ComboBox_Ativos.currentText(), "Bolsa") * self.DBManager.GetCotacao(self.ComboBox_Ativos.currentText())
            if self.ShowValues:
                self.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Custo, 2):.2f}'))
                self.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Retorno, 2):.2f}'))
            else:
                self.TextBox_Custo.setText('Custo: X')
                self.TextBox_Retorno.setText('Retorno: '+str(round((self.HMI_ARCA.Retorno-self.HMI_ARCA.Custo)/self.HMI_ARCA.Custo*100,1))+'%X')
            if self.HMI_ARCA.Retorno >= self.HMI_ARCA.Custo:
                self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
            else:
                self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')
            self.GraphWidget_Subtipos.deleteLater()
            self.GraphWidget_Subtipos = self.HMI_ARCA.CreateGraph_Page46_Subtipos()
            self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

        elif self.PageID== PAGE_BY_NAME['RealEstate'].page_id:
            UserCoin = self.DBManager.GetUserCoinCurrency(self.LoggedIn)
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

            self.HMI_ARCA.Custo = 0
            self.HMI_ARCA.Retorno = 0
            if self.ComboBox_Ativos.currentText() == "Todos":
                for ativo in self.HMI_ARCA.ativos:
                    self.HMI_ARCA.Custo += self.DBManager.GetCustoAtivo(ativo, "Bolsa")
                    self.HMI_ARCA.Retorno += self.DBManager.GetEstoqueAtivo(ativo, "Bolsa") * self.DBManager.GetCotacao(ativo)
                coins = self.DBManager.GetAllAtivos_Cripto()
            elif self.ComboBox_Ativos.currentText() == "Criptos":
                coins = self.DBManager.GetAllAtivos_Cripto()
            else:
                self.HMI_ARCA.Custo = self.DBManager.GetCustoAtivo(self.ComboBox_Ativos.currentText(), "Bolsa")
                self.HMI_ARCA.Retorno = self.DBManager.GetEstoqueAtivo(self.ComboBox_Ativos.currentText(), "Bolsa") * self.DBManager.GetCotacao(self.ComboBox_Ativos.currentText())
            if self.ShowValues:
                self.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Custo, 2):.2f}'))
                self.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Retorno, 2):.2f}'))
            else:
                self.TextBox_Custo.setText('Custo: X')
                self.TextBox_Retorno.setText('Retorno: '+str(round((self.HMI_ARCA.Retorno-self.HMI_ARCA.Custo)/self.HMI_ARCA.Custo*100,1))+'%X')
            if self.HMI_ARCA.Retorno >= self.HMI_ARCA.Custo:
                self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
            else:
                self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')
            self.GraphWidget_Subtipos.deleteLater()
            self.GraphWidget_Subtipos = self.HMI_ARCA.CreateGraph_Page47_Subtipos()
            self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

        elif self.PageID== PAGE_BY_NAME['Caixa'].page_id:
            UserCoin = self.DBManager.GetUserCoinCurrency(self.LoggedIn)
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

            self.HMI_ARCA.Custo = 0
            self.HMI_ARCA.Retorno = 0
            if self.ComboBox_Ativos.currentText() == "Todos":
                for ativo in self.HMI_ARCA.ativos:
                    self.HMI_ARCA.Custo += self.DBManager.GetCustoAtivo(ativo, "Bolsa")
                    self.HMI_ARCA.Retorno += self.DBManager.GetEstoqueAtivo(ativo, "Bolsa") * self.DBManager.GetCotacao(ativo)
                coins = self.DBManager.GetAllAtivos_Cripto()
            elif self.ComboBox_Ativos.currentText() == "Criptos":
                coins = self.DBManager.GetAllAtivos_Cripto()
            else:
                self.HMI_ARCA.Custo = self.DBManager.GetCustoAtivo(self.ComboBox_Ativos.currentText(), "Bolsa")
                self.HMI_ARCA.Retorno = self.DBManager.GetEstoqueAtivo(self.ComboBox_Ativos.currentText(), "Bolsa") * self.DBManager.GetCotacao(self.ComboBox_Ativos.currentText())
            if self.ShowValues:
                self.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Custo, 2):.2f}'))
                self.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Retorno, 2):.2f}'))
            else:
                self.TextBox_Custo.setText('Custo: X')
                self.TextBox_Retorno.setText('Retorno: '+str(round((self.HMI_ARCA.Retorno-self.HMI_ARCA.Custo)/self.HMI_ARCA.Custo*100,1))+'%X')
            if self.HMI_ARCA.Retorno >= self.HMI_ARCA.Custo:
                self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
            else:
                self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')
            self.GraphWidget_Subtipos.deleteLater()
            self.GraphWidget_Subtipos = self.HMI_ARCA.CreateGraph_Page48_Subtipos()
            self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

        elif self.PageID== PAGE_BY_NAME['AtivosInternacionais'].page_id:
            UserCoin = self.DBManager.GetUserCoinCurrency(self.LoggedIn)
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

            self.HMI_ARCA.Custo = 0
            self.HMI_ARCA.Retorno = 0
            if self.ComboBox_Ativos.currentText() == "Todos":
                for ativo in self.HMI_ARCA.ativos:
                    self.HMI_ARCA.Custo += self.DBManager.GetCustoAtivo(ativo, "Bolsa")
                    self.HMI_ARCA.Retorno += self.DBManager.GetEstoqueAtivo(ativo, "Bolsa") * self.DBManager.GetCotacao(ativo)
                coins = self.DBManager.GetAllAtivos_Cripto()
                for ativo in coins: self.HMI_ARCA.Custo += self.DBManager.GetCustoAtivo(ativo, "Cripto")
                for ativo in coins: self.HMI_ARCA.Retorno += self.DBManager.GetEstoqueAtivo(ativo, "Cripto") * self.DBManager.GetCotacao(ativo)
            elif self.ComboBox_Ativos.currentText() == "Criptos":
                coins = self.DBManager.GetAllAtivos_Cripto()
                for ativo in coins: self.HMI_ARCA.Custo += self.DBManager.GetCustoAtivo(ativo, "Cripto")
                for ativo in coins: self.HMI_ARCA.Retorno += self.DBManager.GetEstoqueAtivo(ativo, "Cripto") * self.DBManager.GetCotacao(ativo)
            else:
                self.HMI_ARCA.Custo = self.DBManager.GetCustoAtivo(self.ComboBox_Ativos.currentText(), "Bolsa")
                self.HMI_ARCA.Retorno = self.DBManager.GetEstoqueAtivo(self.ComboBox_Ativos.currentText(), "Bolsa") * self.DBManager.GetCotacao(self.ComboBox_Ativos.currentText())
            if self.ShowValues:
                self.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Custo, 2):.2f}'))
                self.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Retorno, 2):.2f}'))
            else:
                self.TextBox_Custo.setText('Custo: X')
                self.TextBox_Retorno.setText('Retorno: '+str(round((self.HMI_ARCA.Retorno-self.HMI_ARCA.Custo)/self.HMI_ARCA.Custo*100,1))+'%X')
            if self.HMI_ARCA.Retorno >= self.HMI_ARCA.Custo:
                self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
            else:
                self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')
            self.GraphWidget_Subtipos.deleteLater()
            self.GraphWidget_Subtipos = self.HMI_ARCA.CreateGraph_Page49_Subtipos()
            self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_Subtipos, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

        elif self.PageID== PAGE_BY_NAME['CriptoARCA'].page_id:
            UserCoin = self.DBManager.GetUserCoinCurrency(self.LoggedIn)
            self.GraphWidget_MainGraph.deleteLater()
            if self.HMI_ARCA.MainGraphIsShowing == "Visão Geral":
                self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page50_MainGraph_VisaoGeral()
                self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)

            elif self.HMI_ARCA.MainGraphIsShowing == "Ativo por corretora":
                self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page50_MainGraph_AtivoPorCorretora()
                self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)

            elif self.HMI_ARCA.MainGraphIsShowing == "Total de UserCoin por corretora":
                self.GraphWidget_MainGraph = self.HMI_ARCA.CreateGraph_Page50_MainGraph_TotalDeUserCoinPorCorretora()
                self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_MainGraph, 1, 1, 6, 1, Qt.AlignmentFlag.AlignCenter)

            self.HMI_ARCA.Custo = 0
            self.HMI_ARCA.Retorno = 0
            if self.ComboBox_Ativos.currentText() == "Todos":
                for ativo in self.HMI_ARCA.ativos:
                    self.HMI_ARCA.Custo += self.DBManager.GetCustoAtivo(ativo, "Cripto")
                    self.HMI_ARCA.Retorno += self.DBManager.GetEstoqueAtivo(ativo, "Cripto") * self.DBManager.GetCotacao(ativo)
            else:
                self.HMI_ARCA.Custo = self.DBManager.GetCustoAtivo(self.ComboBox_Ativos.currentText(), "Cripto")
                self.HMI_ARCA.Retorno = self.DBManager.GetEstoqueAtivo(self.ComboBox_Ativos.currentText(), "Cripto") * self.DBManager.GetCotacao(self.ComboBox_Ativos.currentText())
            if self.ShowValues:
                self.TextBox_Custo.setText('Custo: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Custo, 2):.2f}'))
                self.TextBox_Retorno.setText('Retorno: ' + UserCoin + ' ' + str(f'{round(self.HMI_ARCA.Retorno, 2):.2f}'))
            else:
                self.TextBox_Custo.setText('Custo: X')
                self.TextBox_Retorno.setText('Retorno: '+str(round((self.HMI_ARCA.Retorno-self.HMI_ARCA.Custo)/self.HMI_ARCA.Custo*100,1))+'%X')
            if self.HMI_ARCA.Retorno >= self.HMI_ARCA.Custo:
                self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: green;}')
            else:
                self.TextBox_Retorno.setStyleSheet('QLineEdit {background-color: black; color: red;}')
            self.GraphWidget_Distribuicao.deleteLater()
            self.GraphWidget_Distribuicao = self.HMI_ARCA.CreateGraph_Page50_Distribuicao()
            self.F_GLayout[self.GCount-1].addWidget(self.GraphWidget_Distribuicao, 7, 0, 3, 3, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

    def UpdatePatrimonioRendimento(self):
        Background_Header = 'rgb(20, 20, 40)'
        try:
            PatrimonioAux = self.Calcular.Patrimonio()
            if PatrimonioAux >= 0:
                currency = self.DBManager.GetUserCoinCurrency()
                self.TextBox_Patrimonio.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: green; border: 1px solid '+Background_Header+'}')
                self.Patrimonio = PatrimonioAux
                self.TextBox_Patrimonio.setText(currency+str(self.Patrimonio))
                Rendimento = self.Calcular.Rendimento()
                if isinstance(Rendimento, float):
                    self.Rendimento = Rendimento
                    self.TextBox_Rendimento.setText(str(self.Rendimento)+'%')
                    if self.Rendimento >= 0: self.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: green; border: 1px solid '+Background_Header+'}')
                    else: self.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: red; border: 1px solid '+Background_Header+'}')
                else:
                    self.Rendimento = 0
                    self.TextBox_Rendimento.setText('...')
                    self.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: yellow; border: 1px solid '+Background_Header+'}')
            elif PatrimonioAux == -1: # Problema desconhecido, talvez conexão com a internet ou talvez um bug qualquer que na próxima atualização resolve
                self.Patrimonio = 0
                self.TextBox_Patrimonio.setText("...")
                self.TextBox_Patrimonio.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: yellow; border: 1px solid '+Background_Header+'}')
                self.Rendimento = 0
                self.TextBox_Rendimento.setText('...')
                self.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: yellow; border: 1px solid '+Background_Header+'}')
            elif PatrimonioAux == -2: # Tabela de cotações tem algum valor igual a zero
                self.Patrimonio = 0
                self.TextBox_Patrimonio.setText("Att. cot. (C)")
                self.TextBox_Patrimonio.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: orange; border: 1px solid '+Background_Header+'}')
                self.Rendimento = 0
                self.TextBox_Rendimento.setText('Att. cot. (C)')
                self.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: orange; border: 1px solid '+Background_Header+'}')
            return True
        except Exception as e:
            logger.error(e, traceback.format_exception(None, e, e.__traceback__))
            return False
    
    def EnableAllButtons(self, condition = True):
        """Ferramentas"""
        if self.PageID== PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id:
            self.Button_Compra.setEnabled(condition)
            self.Button_Venda.setEnabled(condition)
            self.Button_LimparCampos.setEnabled(condition)
            self.Button_RegistrarOperacao.setEnabled(condition)
            self.Button_Info3.setEnabled(condition)
            self.Button_Info2.setEnabled(condition)
            self.Button_Info4.setEnabled(condition)
            self.Button_Info5.setEnabled(condition)
            self.Button_Info6.setEnabled(condition)
            self.Button_Info7.setEnabled(condition)
            self.Button_Info8.setEnabled(condition)
            self.Button_Perfil.setEnabled(condition)
            self.Button_ShowHideValues.setEnabled(condition)
            self.Button_Home.setEnabled(condition)
            self.Button_Return.setEnabled(condition)

    def GetSizeOfTableColumns(self, data, HHeader):
        coluna = []
        resposta = []
        if not len(data) > 0:
            aux = (' ',)
            for i in range(len(HHeader)-1):
                aux += (' ',)
            data.append(aux)
        for j in range(len(data[0])):
            col = []
            for i, linha in enumerate(data):
                col.append(str(linha[j]))
            col.append(HHeader[j])
            coluna.append(col)

        if self.PageIDAux== PAGE_BY_NAME['InsercaoCotacoesManuais'].page_id:
            col = len(max(coluna[0], key=len))*16 # Ativo
            resposta.append(col)
            col = len(max(coluna[1], key=len))*16 # Data
            resposta.append(col)
            col = len(max(coluna[2], key=len))*16 # Cotação em CURRENCY
            resposta.append(col)

        elif self.PageID== PAGE_BY_NAME['ARCA'].page_id:
            col = len(max(coluna[0], key=len))*10 # Corretora
            resposta.append(col)
            col = len(max(coluna[1], key=len))*9 # Conta-corrente
            resposta.append(col)

        elif self.PageID in [PAGE_BY_NAME['RegistrosBolsa'].page_id, PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id, PAGE_BY_NAME['DeletarOperacoesBolsa'].page_id]:
            col7 = int(self.frameGeometry().width())
            col = len(max(coluna[0], key=len))*10
            col7 -= col
            resposta.append(col)
            col = len(max(coluna[1], key=len))*15
            col7 -= col
            resposta.append(col)
            col = len(max(coluna[2], key=len))*15
            col7 -= col
            resposta.append(col)
            col = len(max(coluna[3], key=len))*18
            col7 -= col
            resposta.append(col)
            col = len(max(coluna[4], key=len))*12
            col7 -= col
            resposta.append(col)
            col = len(max(coluna[5], key=len))*15
            col7 -= col
            resposta.append(col)
            col = len(max(coluna[6], key=len))*12
            col7 -= col
            resposta.append(col)
            col7 -= 44

            if not col7 >= len(max(coluna[7], key=len))*10:
                self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(7, col7)
                col7 = len(max(coluna[7], key=len))*10
            else:
                self.Table_Operacoes_Realizadas_com_AtivoHeader.setColumnWidth(7, col7)

            resposta.append(col7)

        elif self.PageID== PAGE_BY_NAME['InformarDepositosSaqBolsa'].page_id:
            col = len(max(coluna[0], key=len))*9 # Data
            resposta.append(col)
            col = len(max(coluna[1], key=len))*11 # Valores
            resposta.append(col)

        elif self.PageID in [PAGE_BY_NAME['RegistrosCripto'].page_id]:
            col8 = int(self.frameGeometry().width())
            col = len(max(coluna[0], key=len))*8
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[1], key=len))*12
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[2], key=len))*13
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[3], key=len))*13
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[4], key=len))*12
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[5], key=len))*12
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[6], key=len))*10
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[7], key=len))*10
            col8 -= col
            resposta.append(col)
            col8 -= 45

            if not col8 >= len(max(coluna[8], key=len))*10:
                self.Table_Operacoes_RealizadasHeader.setColumnWidth(8, col8)
                col8 = len(max(coluna[8], key=len))*8.5
            else:
                self.Table_Operacoes_RealizadasHeader.setColumnWidth(8, col8)

            resposta.append(col8)

        elif self.PageID in [PAGE_BY_NAME['AlterarOperacaoCripto'].page_id, PAGE_BY_NAME['DeletarOperacaoCripto'].page_id]:
            col8 = int(self.frameGeometry().width())
            col = len(max(coluna[0], key=len))*8
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[1], key=len))*12
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[2], key=len))*13
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[3], key=len))*13
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[4], key=len))*12
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[5], key=len))*12
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[6], key=len))*10
            col8 -= col
            resposta.append(col)
            col = len(max(coluna[7], key=len))*10
            col8 -= col
            resposta.append(col)
            col8 -= 45

            if not col8 >= len(max(coluna[8], key=len))*10:
                self.Table_Operacoes_RealizadasHeader.setColumnWidth(8, col8)
                col8 = len(max(coluna[8], key=len))*8
            else:
                self.Table_Operacoes_RealizadasHeader.setColumnWidth(8, col8)

            resposta.append(col8)

        elif self.PageID== PAGE_BY_NAME['Tributacao'].page_id:
            if not self.DTeST_51 == "DTeST":
                if int(self.frameGeometry().width()*6/20*1.4) < 510:
                    col = len(max(coluna[0], key=len))*4 # MesAno
                    resposta.append(col)
                    col = len(max(coluna[1], key=len))*7 # Resultado Líquido
                    resposta.append(col)
                    col = len(max(coluna[2], key=len))*8 # Imposto devido
                    resposta.append(col)
                    col = len(max(coluna[3], key=len))*8 # Alíquota
                    resposta.append(col)
                    col = len(max(coluna[4], key=len))*7 # Lucro mínimo taxável
                    resposta.append(col)
                    col = len(max(coluna[5], key=len))*8 # Resultado bruto
                    resposta.append(col)
                    col = len(max(coluna[6], key=len))*8 # Prejuízo acumulado
                    resposta.append(col)
                    col = len(max(coluna[7], key=len))*7 # Resultado final
                    resposta.append(col)
                else:
                    col = len(max(coluna[0], key=len))*5 #
                    resposta.append(col)
                    col = len(max(coluna[1], key=len))*10 #
                    resposta.append(col)
                    col = len(max(coluna[2], key=len))*10 #
                    resposta.append(col)
                    col = len(max(coluna[3], key=len))*11 #
                    resposta.append(col)
                    col = len(max(coluna[4], key=len))*10 #
                    resposta.append(col)
                    col = len(max(coluna[5], key=len))*10 #
                    resposta.append(col)
                    col = len(max(coluna[6], key=len))*10 #
                    resposta.append(col)
                    col = len(max(coluna[7], key=len))*10 #
                    resposta.append(col)
            else:
                col = len(max(coluna[0], key=len))*6 #
                resposta.append(col)
                col = len(max(coluna[1], key=len))*10 #
                resposta.append(col)
                col = len(max(coluna[2], key=len))*10 #
                resposta.append(col)
                col = len(max(coluna[3], key=len))*10 #
                resposta.append(col)
                col = len(max(coluna[4], key=len))*10 #
                resposta.append(col)
                col = len(max(coluna[5], key=len))*10 #
                resposta.append(col)

        return resposta

    def SetTableWidth_45_1(self, SizeCol0, SizeCol1, SizeCol2):
            self.Table_CotaçõesManuais.setVisible(False)
            self.Table_CotaçõesManuaisHeader.setVisible(False)

            self.Table_CotaçõesManuais.adjustSize()
            self.Table_CotaçõesManuais.setColumnWidth(0, SizeCol0)
            self.Table_CotaçõesManuais.setColumnWidth(1, SizeCol1)
            self.Table_CotaçõesManuais.setColumnWidth(2, SizeCol2)

            width = self.Table_CotaçõesManuais.verticalHeader().width()
            width += self.Table_CotaçõesManuais.horizontalHeader().length()
            if self.Table_CotaçõesManuais.horizontalScrollBar().isVisible():
                width += self.Table_CotaçõesManuais.horizontalScrollBar().width()
            width += self.Table_CotaçõesManuais.frameWidth() * 2
            self.Table_CotaçõesManuais.setFixedWidth(width)

            self.Table_CotaçõesManuaisHeader.adjustSize()
            self.Table_CotaçõesManuaisHeader.setColumnWidth(0, SizeCol0)
            self.Table_CotaçõesManuaisHeader.setColumnWidth(1, SizeCol1)
            self.Table_CotaçõesManuaisHeader.setColumnWidth(2, SizeCol2)

            self.Table_CotaçõesManuais.setVisible(True)
            self.Table_CotaçõesManuaisHeader.setVisible(True)

    def EnviarEmailDeConfirmacao(self,Email,NomeDeUsuario,CodigoDeConfirmacaoGerado):
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls

        sender_email = "confirmacaodeemailfinancas@gmail.com"
        password = "SenhaDasMinhasFinancas2021"

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server,port)
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(sender_email, password)

            # Send email here
            message = ("Subject: Confirmação de email\n\nOlá "+NomeDeUsuario+"\n\nEste é o seu codigo de verifição de email:\n\n"+CodigoDeConfirmacaoGerado+
                       "\n\n------------------------------------\nEmail Automático do APP Finanças para Confirmação de Email").encode('utf-8').strip()
            receiver_email = Email
            server.sendmail(sender_email, receiver_email, message)
            server.quit()
        except Exception as e:
            # print(e) # Print any error messages
            try:server.quit() # type: ignore[attr-defined]
            except:pass

    def ClearPage(self):
        if self.VersionUpdate:
            self.VersionUpdate = False
            MessageBox_Msg1 = QMessageBox()
            MessageBox_Msg1.setWindowTitle("Atualização disponível")
            MessageBox_Msg1.setText("Esta versão é a "+self.APPVersion+".\nExiste uma versão mais recente disponível ("+self.OnlineVersion+").\nDeseja atualizar agora?\nTambém é possível acessar\nhttps://github.com/CaioPorta/ARCA/tree/main/dist\npara atualizar manualmente.")
            MessageBox_Msg1.setIcon(QMessageBox.Warning)
            MessageBox_Msg1.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            MessageBox_Msg1.setDefaultButton(QMessageBox.Yes)
            MessageBox_Msg1.setWindowIcon(QIcon(".\\images\\logoARCA.png"))
            returnValue = MessageBox_Msg1.exec()
            if returnValue == QMessageBox.Yes:
                self.LW = LoadingWindow.LoadingWindow(self)
                self.LW.show()
                self.VersionChecker.StartThread_UpdateVersion()
                while self.VersionChecker.InProgress:
                    self.LW.Label_Titulo.setText(self.VersionChecker.Title)
                    self.LW.pbar.setValue(self.VersionChecker.Progress)
                    time.sleep(0.2)
                self.LW.close()
            MessageBox_Msg1 = QMessageBox()
            MessageBox_Msg1.setWindowTitle("Reinicialização")
            MessageBox_Msg1.setText("Reinicialização da ARCA necessária.\nUm atalho foi criado na área de tabalho.\nClique em OK para reiniciar.")
            MessageBox_Msg1.setIcon(QMessageBox.Warning)
            MessageBox_Msg1.setStandardButtons(QMessageBox.OK)
            MessageBox_Msg1.setDefaultButton(QMessageBox.OK)
            MessageBox_Msg1.setWindowIcon(QIcon(".\\images\\logoARCA.png"))
            returnValue = MessageBox_Msg1.exec()
            # Close APP
            self.DBManager.Disconnect()
            currdir = os.getcwd()
            os.startfile(currdir + "\\ARCA.exe")
            sys.exit()
            QCoreApplication.quit()

        try: # Cabeçalho
            self.Button_Return.deleteLater()
            self.Button_Home.deleteLater()
            self.Button_ShowHideValues.deleteLater()
            self.Label_Patrimonio.deleteLater()
            self.TextBox_Patrimonio.deleteLater()
            self.Label_Rendimento.deleteLater()
            self.TextBox_Rendimento.deleteLater()
            self.Button_Sair.deleteLater()
            self.Button_AttCotacoes.deleteLater()
            self.Button_AttCotacoesManuais.deleteLater()
            self.Button_Perfil.deleteLater()
            self.Button_Currency.deleteLater()
        except:pass
        try: self.GLayout.removeItem(self.HBoxLayout_Header)
        except:pass

        if self.PageID == "11" and self.PageIDAux == '':
            try:
                self.Button_Msg3.deleteLater()
                self.TextBox_MontanteEmAplicacao.deleteLater()
                self.HBoxLayout_Montantes.removeItem(self.HBoxLayout_Montantes1)
                self.Button_Msg4.deleteLater()
                self.TextBox_MontanteAplicado.deleteLater()
                self.HBoxLayout_Montantes.removeItem(self.HBoxLayout_Montantes2)
                self.F_GLayout[0].removeItem(self.HBoxLayout_Montantes)

                self.Label_Msg9.deleteLater()
                self.Label_Msg8.deleteLater()
                self.HBoxLayout_Reserva.removeItem(self.HBoxLayout_Reserva1)
                self.Button_Msg5.deleteLater()
                self.TextBox_GastoMensal.deleteLater()
                self.HBoxLayout_Reserva.removeItem(self.HBoxLayout_Reserva2)
                self.Button_Msg6.deleteLater()
                self.TextBox_MesesDeReserva.deleteLater()
                self.HBoxLayout_Reserva.removeItem(self.HBoxLayout_Reserva3)
                self.Button_Msg7.deleteLater()
                self.TextBox_Aplicar.deleteLater()
                self.HBoxLayout_Reserva.removeItem(self.HBoxLayout_Reserva4)
                self.F_GLayout[0].removeItem(self.HBoxLayout_Reserva)

                self.Label_Subtitulo1_.deleteLater()
                self.GraphWidget_AcoesENegocios.deleteLater()
                self.Label_Subtitulo2_.deleteLater()
                self.GraphWidget_RealEstate.deleteLater()
                self.Label_Subtitulo3_.deleteLater()
                self.GraphWidget_Caixa.deleteLater()
                self.Label_Subtitulo4_.deleteLater()
                self.GraphWidget_AtivosInternacionais.deleteLater()
                self.Label_Subtitulo5_.deleteLater()
                self.GraphWidget_Especifica.deleteLater()
                self.HBoxLayout_Graficos_Subtipos.removeItem(self.VBoxLayout_Graficos_Subtipos_AcoesENegocios)
                self.HBoxLayout_Graficos_Subtipos.removeItem(self.VBoxLayout_Graficos_Subtipos_RealEstate)
                self.HBoxLayout_Graficos_Subtipos.removeItem(self.VBoxLayout_Graficos_Subtipos_Caixa)
                self.HBoxLayout_Graficos_Subtipos.removeItem(self.VBoxLayout_Graficos_Subtipos_AtivosInternacionais)
                self.HBoxLayout_Graficos_Subtipos.removeItem(self.VBoxLayout_Graficos_Subtipos_Especifica)
                self.F_GLayout[0].removeItem(self.HBoxLayout_Graficos_Subtipos)

                self.Label_Subtitulo1.deleteLater()
                self.Label_Subtitulo2.deleteLater()
                self.Label_Subtitulo3.deleteLater()
                self.Label_Subtitulo4.deleteLater()
                self.Label_Subtitulo5.deleteLater()
                self.Button_AcoesENegociosInvisivel.deleteLater()
                self.Button_RealEstateInvisivel.deleteLater()
                self.Button_CaixaInvisivel.deleteLater()
                self.Button_AcoesInternacionaisInvisivel.deleteLater()
                self.Button_EspecificaInvisivel.deleteLater()
                self.HBoxLayout_Graficos_Subtipos_Invisiveis.removeItem(self.VBoxLayout_Graficos_Subtipos_AcoesENegociosInvisiveis)
                self.HBoxLayout_Graficos_Subtipos_Invisiveis.removeItem(self.VBoxLayout_Graficos_Subtipos_RealEstateInvisiveis)
                self.HBoxLayout_Graficos_Subtipos_Invisiveis.removeItem(self.VBoxLayout_Graficos_Subtipos_CaixaInvisiveis)
                self.HBoxLayout_Graficos_Subtipos_Invisiveis.removeItem(self.VBoxLayout_Graficos_Subtipos_AtivosInternacionaisInvisiveis)
                self.HBoxLayout_Graficos_Subtipos_Invisiveis.removeItem(self.VBoxLayout_Graficos_Subtipos_EspecificaInvisiveis)
                self.F_GLayout[0].removeItem(self.HBoxLayout_Graficos_Subtipos_Invisiveis)
            except Exception as e:print(e) # Debug
            
        elif self.PageID == "23" and self.PageIDAux == '':
            try:
                self.Label_Msg2.deleteLater()
                self.TextBox_Msg2.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Ativo)
                self.F_GLayout[0].removeItem(self.VBoxLayout_Ativo)
            except:pass
        elif self.PageID == "24" and self.PageIDAux == '':
            try:
                self.Button_Calendario.deleteLater()
                self.Button_Relogio.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Data)
            except:pass
        elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id, PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id] and self.PageIDAux == '':
            try:
                self.Button_Calendario.deleteLater()
                self.Button_Relogio.deleteLater()
                self.Button_Info3.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Data)
                self.Button_Compra.deleteLater()
                self.Button_Venda.deleteLater()
                self.Button_Desdobramento.deleteLater()
                self.Button_Grupamento.deleteLater()
                self.Button_Bonificacao.deleteLater()
                self.Button_Info2.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Tipo)
                self.TextBox_Qqt.deleteLater()
                self.Button_Info4.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Qqt)
                self.TextBox_Preco.deleteLater()
                self.Button_Info5.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Preco)
                self.TextBox_Corretagem.deleteLater()
                self.Button_Info6.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Corretagem)
                self.TextBox_TaxaB3.deleteLater()
                self.Button_Info7.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_TaxaB3)
                self.TextBox_Obs.deleteLater()
                self.Button_Info8.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Obs)
            except Exception as e:
                print(e, traceback.format_exception(None, e, e.__traceback__))
        elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id, PAGE_BY_NAME['AlterarNovaOperacaoManualBolsa'].page_id] and self.PageIDAux == '':
            try:
                self.Button_Calendario.deleteLater()
                self.Button_Relogio.deleteLater()
                self.Button_Info3.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Data)
                self.Button_Compra.deleteLater()
                self.Button_Info2.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Tipo)
                self.TextBox_Qqt.deleteLater()
                self.Button_Info4.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Qqt)
                self.TextBox_Preco.deleteLater()
                self.Button_Info5.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Preco)
                self.TextBox_Corretagem.deleteLater()
                self.Button_Info6.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Corretagem)
                self.TextBox_TaxaB3.deleteLater()
                self.Button_Info7.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_TaxaB3)
                self.TextBox_Obs.deleteLater()
                self.Button_Info8.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Obs)
            except Exception as e:
                print(e, traceback.format_exception(None, e, e.__traceback__))
        elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id, PAGE_BY_NAME['AlterarOperacaoCripto'].page_id] and self.PageIDAux == '':
            try:
                self.Button_Calendario.deleteLater()
                self.Button_Relogio.deleteLater()
                self.Button_Info3.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Data)
                self.Button_Compra.deleteLater()
                self.Button_Venda.deleteLater()
                self.Button_Deposito.deleteLater()
                self.Button_Saque.deleteLater()
                self.Button_Drop.deleteLater()
                self.Button_Burn.deleteLater()
                self.Button_Stake.deleteLater()
                self.Button_Unstake.deleteLater()
                self.Button_Hold.deleteLater()
                self.Button_Unhold.deleteLater()
                self.Button_Info14.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Tipo)
                self.TextBox_Par_Esquerda.deleteLater()
                self.Label_Msg12.deleteLater()
                self.TextBox_Par_Direita.deleteLater()
                self.Button_Info15.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Par)
                self.TextBox_Qqt.deleteLater()
                self.Button_Info13.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Qqt)
                self.TextBox_Preco.deleteLater()
                self.Button_Info12.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Preco)
                self.TextBox_Taxa.deleteLater()
                self.Button_Info11.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Taxa)
                self.TextBox_MoedaDaTaxa.deleteLater()
                self.Button_Info10.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_MoedaDaTaxa)
                self.TextBox_Conversao.deleteLater()
                self.Button_BuscarConversao.deleteLater()
                self.Button_Info9.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Conversao)
                self.TextBox_Obs.deleteLater()
                self.Button_Info8.deleteLater()
                self.F_GLayout[0].removeItem(self.HBoxLayout_Obs)
            except Exception as e:
                print(e, traceback.format_exception(None, e, e.__traceback__))

        for i in range(self.GCount):
            while self.F_GLayout[i].count(): # Remove and close every widget from the sub Layout
                item = self.F_GLayout[i].takeAt(0)
                w = item.widget()
                if w is not None:
                    w.close()
            self.GLayout.removeItem(self.F_GLayout[i]) # Delete each sub Layout
            self.GCount -= 1

        try:
            for i in reversed(range(self.GLayout.count())): # Close any remaining direct widget child of the main Layout
                w = self.GLayout.itemAt(i).widget()
                if w is not None:
                    w.close()
        except:pass

    def InsertGridLayout(self, row=1, column=0, panRow=1, panColumn=20): # Adiciona um sub-GridLayout no Grid Principal
        self.F_GLayout.append(QGridLayout())
        self.GCount += 1
        self.GLayout.addLayout(self.F_GLayout[self.GCount-1], row, column, panRow, panColumn)

    def AtualizarCotacoes(self):
        if not self.AtualizarCotacoes_is_running: # Impede mais de um requerimento na atualização de cotações
            self.Movie_AttCotacoes.start()
            # self.Thread_AtualizarCotacoes = WorkerThread('Thread_AtualizarCotacoes', self.HMI)
            self.Thread_AtualizarCotacoes = BP(ThreadName='Thread_AtualizarCotações', HMI=self)
            self.Thread_AtualizarCotacoes.start()

    def AtualizarCotacoes_run(self): # Thread
        # Atualizar tabela de cotações, depois atualizar os valores no HMI
        self.UpdatePatrimonioRendimento()
        currency = self.DBManager.GetUserCoinCurrency()

        corretoras = self.DBManager.GetCorretoras("Bolsa")
        ativos = []
        thread_list = []
        for corretora in corretoras: ativos.extend(self.DBManager.GetAtivos(corretora, "Bolsa"))
        ativos = list(dict.fromkeys(ativos))
        for idx, ativo in enumerate(ativos):
            if self.DBManager.GetModoCotacao(ativo) == "Auto":
                thread_list.append(BP(ThreadName='Thread_GetCotacao', HMI=self, ativo=ativo, currency=currency))

        corretoras = self.DBManager.GetCorretoras("Cripto")
        ativos = []
        for corretora in corretoras: ativos.extend(self.DBManager.GetAtivos(corretora, "Cripto"))
        ativos = list(dict.fromkeys(ativos))
        for ativo in ativos:
            if self.DBManager.GetModoCotacao(ativo) == "Auto":
                thread_list.append(BP(ThreadName='Thread_GetCotacaoCripto', HMI=self, ativo=ativo, currency=currency))

        for thread in thread_list: thread.start()
        for thread in thread_list: thread.join()

        logger.debug('waiting') # Debug
        self.UpdatePatrimonioRendimento()
        if self.PageID in ["18", "19"]: self.UpdatePage()
        logger.debug('UpdatePatrimonioRendimento executed') # Debug

    def PutHeader(self):
        self.Background_Header = QLabel()
        Background_Header = 'rgb(20, 20, 40)'
        self.Background_Header.setStyleSheet("background-color: "+Background_Header)
        self.Background_Header.setFixedHeight(50)

        self.Button_Return = QPushButton()
        self.Button_Return.setFixedSize(40,40)
        self.Button_Return.setIconSize(QSize(35, 35))
        self.Button_Return.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Return.setStyleSheet("QPushButton {background-color: "+Background_Header+"; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_Return.setIcon(QIcon("./images/return_icon.png"))
        self.Button_Return.setToolTip(r"Voltar")

        self.Button_Home = QPushButton()
        self.Button_Home.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Home'].page_id))
        self.Button_Home.setFixedSize(40,40)
        self.Button_Home.setIconSize(QSize(35, 35))
        self.Button_Home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Home.setStyleSheet("QPushButton {background-color: "+Background_Header+"; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_Home.setIcon(QIcon("./images/home_icon.png"))
        self.Button_Home.setToolTip(r"Início")

        self.Button_ShowHideValues = QPushButton()
        self.Button_ShowHideValues.setToolTip(r"Mostrar ou ocultar valores")
        self.Button_ShowHideValues.pressed.connect(lambda: self.OnButtonPressed('ShowHideValues'))
        self.Button_ShowHideValues.setFixedSize(40,40)
        self.Button_ShowHideValues.setIconSize(QSize(35, 35))
        self.Button_ShowHideValues.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ShowHideValues.setStyleSheet("QPushButton {background-color: "+Background_Header+"; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        if not self.ShowValues: self.Button_ShowHideValues.setIcon(QIcon("./images/iconClosedEye.png"))
        else: self.Button_ShowHideValues.setIcon(QIcon("./images/iconOpenEye.png"))

        self.Label_Patrimonio = QPushButton('Patrimônio:')
        self.Label_Patrimonio.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Info23'].page_id))
        self.Label_Patrimonio.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none; alignment: right')
        self.Label_Patrimonio.setFont(self.font14)

        self.TextBox_Patrimonio = QLineEdit()
        self.TextBox_Patrimonio.setFont(self.font14)
        self.TextBox_Patrimonio.setEnabled(False)
        self.TextBox_Patrimonio.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        if isinstance(self.Patrimonio,float):
            self.TextBox_Patrimonio.setText(self.DBManager.GetUserCoinCurrency()+str(self.Patrimonio))
            self.TextBox_Patrimonio.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: green; border: 1px solid '+Background_Header+'}')
        else:
            self.TextBox_Patrimonio.setText(str(self.Patrimonio))
            self.TextBox_Patrimonio.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: orange; border: 1px solid '+Background_Header+'}')
        if self.ShowValues: self.TextBox_Patrimonio.setEchoMode(QLineEdit.Normal)
        else: self.TextBox_Patrimonio.setEchoMode(QLineEdit.Password)

        self.Label_Rendimento = QPushButton('RNB%:')
        self.Label_Rendimento.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Info22'].page_id))
        self.Label_Rendimento.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none; alignment: right')
        self.Label_Rendimento.setFont(self.font14)

        self.TextBox_Rendimento = QLineEdit()
        self.TextBox_Rendimento.setFont(self.font14)
        self.TextBox_Rendimento.setEnabled(False)
        self.TextBox_Rendimento.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        if isinstance(self.Rendimento, float):
            self.TextBox_Rendimento.setText(str(self.Rendimento)+'%')
            if self.Rendimento >= 0: self.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: green; border: 1px solid '+Background_Header+'}')
            else: self.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: red; border: 1px solid '+Background_Header+'}')
        else:
            self.TextBox_Rendimento.setText(str(self.Rendimento))
            self.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: orange; border: 1px solid '+Background_Header+'}')

        self.Button_Sair = QPushButton()
        self.Button_Sair.setToolTip(r"Sair")
        self.Button_Sair.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Login'].page_id))
        self.Button_Sair.setFixedSize(40,40)
        self.Button_Sair.setIconSize(QSize(35, 35))
        self.Button_Sair.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Sair.setStyleSheet("QPushButton {background-color: "+Background_Header+"; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_Sair.setIcon(QIcon("./images/exit_icon.png"))

        self.Button_AttCotacoesManuais = QPushButton()
        self.Button_AttCotacoesManuais.setToolTip(r"Atualizar cotações manuais (C)")
        self.Button_AttCotacoesManuais.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['InsercaoCotacoesManuais'].page_id))
        self.Button_AttCotacoesManuais.setFixedSize(40,40)
        self.Button_AttCotacoesManuais.setIconSize(QSize(35, 35))
        self.Button_AttCotacoesManuais.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_AttCotacoesManuais.setStyleSheet("QPushButton {background-color: "+Background_Header+"; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_AttCotacoesManuais.setIcon(QIcon("./images/iconeAdjustDB.png"))

        self.Button_AttCotacoes = QLabel()
        self.Button_AttCotacoes.mousePressEvent = self.AtualizarCotacoes
        self.Button_AttCotacoes.setStyleSheet("QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_AttCotacoes.setToolTip(r"Atualizar cotações")
        self.Movie_AttCotacoes = QMovie("./images/Updating.gif")
        self.Movie_AttCotacoes.setScaledSize(QSize(50, 50))
        self.Button_AttCotacoes.setFixedSize(50,50)
        self.Button_AttCotacoes.setMovie(self.Movie_AttCotacoes)
        self.Movie_AttCotacoes.jumpToFrame(0)
        if self.AtualizarCotacoes_is_running: self.Movie_AttCotacoes.start()
        else: self.Button_AttCotacoes.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.Button_Perfil = QPushButton()
        self.Button_Perfil.setToolTip(r"Perfil e ferramentas")
        self.Button_Perfil.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Perfil'].page_id))
        self.Button_Perfil.setFixedSize(40,40)
        self.Button_Perfil.setIconSize(QSize(35, 35))
        self.Button_Perfil.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Perfil.setStyleSheet("QPushButton {background-color: "+Background_Header+"; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        try:
            user = str(self.User or "")
            if os.path.exists(os.path.join(os.getcwd(), "images", "ProfilePhoto_"+user+".jpg")):
                self.Button_Perfil.setIcon(QIcon("./images/ProfilePhoto_"+user+".jpg"))
            else:
                self.Button_Perfil.setIcon(QIcon("./images/ProfilePhoto.jpg"))
        except: self.Button_Perfil.setIcon(QIcon("./images/ProfilePhoto.jpg"))

        self.Button_Currency = QPushButton('Moeda corrente: '+self.DBManager.GetUserCoinCurrency(self.LoggedIn))
        self.Button_Currency.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['EscolhaMoeda'].page_id))
        self.Button_Currency.setFixedHeight(40)
        self.Button_Currency.setIconSize(QSize(35, 35))
        self.Button_Currency.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Currency.setStyleSheet("background-color: "+Background_Header+" ; color: rgb(255, 255, 255); border: none; outline: none;")
        self.Button_Currency.setIcon(QIcon("./images/iconeAdjustDB.jpg"))

        self.HBoxLayout_Header = QHBoxLayout()

        if self.PageID== PAGE_BY_NAME['Login'].page_id: pass # Essa não tem cabeçalho

        elif self.PageIDAux== PAGE_BY_NAME['Perfil'].page_id:
            if self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id, PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id, PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id, PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id, PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id, PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id, PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id, PAGE_BY_NAME['AlterarNovaOperacaoManualBolsa'].page_id]: self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['RegistrosBolsa'].page_id))
            elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id, PAGE_BY_NAME['AlterarOperacaoCripto'].page_id]: self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['RegistrosCripto'].page_id))
            else: self.Button_Return.pressed.connect(lambda: self.CreatePage(self.PageID))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)
            self.HMI_ARCA.Flag_RecalcularGraficos = True

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoesManuais, Qt.AlignmentFlag.AlignRight)
            self.HBoxLayout_Header.addWidget(self.Button_Currency)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageIDAux== PAGE_BY_NAME['InsercaoCotacoesManuais'].page_id:
            if self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id, PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id, PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id, PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id, PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id, PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id, PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id, PAGE_BY_NAME['AlterarNovaOperacaoManualBolsa'].page_id]: self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['RegistrosBolsa'].page_id))
            elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id, PAGE_BY_NAME['AlterarOperacaoCripto'].page_id]: self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['RegistrosCripto'].page_id))
            else: self.Button_Return.pressed.connect(lambda: self.CreatePage(self.PageID))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)
            self.HMI_ARCA.Flag_RecalcularGraficos = True

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoesManuais, Qt.AlignmentFlag.AlignRight)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageIDAux in ['14', '15', '17a', '17b', 'ChooseCurrency']:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Perfil'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoesManuais, Qt.AlignmentFlag.AlignRight)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID== PAGE_BY_NAME['AuxilioSenha'].page_id or self.PageID== PAGE_BY_NAME['ImportarUsuario'].page_id or self.PageID== PAGE_BY_NAME['CriarUsuario'].page_id or self.PageID== PAGE_BY_NAME['AlteracaoSenha'].page_id:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Login'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20, Qt.AlignmentFlag.AlignLeft)

        elif self.PageID in [PAGE_BY_NAME['ImportacaoUsuario'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ImportarUsuario'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20, Qt.AlignmentFlag.AlignLeft)

        elif self.PageID== PAGE_BY_NAME['AnaliseMercado'].page_id:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Login'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20, Qt.AlignmentFlag.AlignLeft)

        elif self.PageID== PAGE_BY_NAME['RecuperacaoEmail'].page_id:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['AuxilioSenha'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20, Qt.AlignmentFlag.AlignLeft)

        elif self.PageID== PAGE_BY_NAME['ConfirmacaoEmailCriar'].page_id:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['CriarUsuario'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20, Qt.AlignmentFlag.AlignLeft)

        elif self.PageID== PAGE_BY_NAME['Home'].page_id:
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Sair, Qt.AlignmentFlag.AlignRight)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['ARCA'].page_id, PAGE_BY_NAME['Desempenho'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Home'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoesManuais, Qt.AlignmentFlag.AlignRight)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['AcoesNegocios'].page_id, PAGE_BY_NAME['RealEstate'].page_id, PAGE_BY_NAME['Caixa'].page_id, PAGE_BY_NAME['AtivosInternacionais'].page_id, PAGE_BY_NAME['CriptoARCA'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ARCA'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoesManuais, Qt.AlignmentFlag.AlignRight)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id, PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id, PAGE_BY_NAME['EditacaoContasCorrentesBancos'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['EdicaoNegociacoes'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['AdicionarCorretoraBolsa'].page_id, PAGE_BY_NAME['RenomearCorretoraBolsa'].page_id, PAGE_BY_NAME['RegistrosBolsa'].page_id, PAGE_BY_NAME['InformarDepositosSaqBolsa'].page_id, PAGE_BY_NAME['SaldoContaCorrenteBolsa'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['AdicionarNovoAtivo'].page_id, PAGE_BY_NAME['RenomearAtivo'].page_id, PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id, PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id, PAGE_BY_NAME['DeletarOperacoesBolsa'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['RegistrosBolsa'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['NaoImplementada31a'].page_id, PAGE_BY_NAME['NaoImplementada32a'].page_id, '33a', PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id, PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['AdicionarNovoAtivo'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['AlterarNovaOperacaoManualBolsa'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['NaoImplementada31b'].page_id, PAGE_BY_NAME['NaoImplementada32b'].page_id, '33b', PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id, PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['RenomearAtivo'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['AdicionarCorretoraCripto'].page_id, PAGE_BY_NAME['RenomearCorretoraCripto'].page_id, PAGE_BY_NAME['RegistrosCripto'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id, PAGE_BY_NAME['AlterarOperacaoCripto'].page_id, PAGE_BY_NAME['DeletarOperacaoCripto'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['RegistrosCripto'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in ['42']:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in ['34c', '35c']:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['IdeiaAbandonada'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['EdicaoNegociacoes'].page_id, PAGE_BY_NAME['AnaliseMercadoDup'].page_id, PAGE_BY_NAME['Tributacao'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Home'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['AdicionarNovoBanco'].page_id,'BancosDelete',PAGE_BY_NAME['RenomearBanco'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['EditacaoContasCorrentesBancos'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_AttCotacoes, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Home, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_ShowHideValues, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Patrimonio)
            self.HBoxLayout_Header.addWidget(self.TextBox_Patrimonio, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Label_Rendimento)
            self.HBoxLayout_Header.addWidget(self.TextBox_Rendimento, Qt.AlignmentFlag.AlignLeft)
            self.HBoxLayout_Header.addWidget(self.Button_Perfil, Qt.AlignmentFlag.AlignRight)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20)

        elif self.PageID in [PAGE_BY_NAME['ImportacaoUsuario'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ImportarUsuario'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20, Qt.AlignmentFlag.AlignLeft)

        elif self.PageID in [PAGE_BY_NAME['ConfirmacaoEmailImportar'].page_id]:
            self.Button_Return.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ImportacaoUsuario'].page_id))
            self.GLayout.addWidget(self.Background_Header, 0, 0, 1, 20)

            self.HBoxLayout_Header.addWidget(self.Button_Return, Qt.AlignmentFlag.AlignLeft)
            self.GLayout.addLayout(self.HBoxLayout_Header, 0, 0, 1, 20, Qt.AlignmentFlag.AlignLeft)
