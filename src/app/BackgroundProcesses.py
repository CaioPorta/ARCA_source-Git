# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 17:53:09 2021

@author: caiop
"""
import threading
from threading import Thread
import time

import requests

from datetime import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from playsound import playsound

class BackgroundProcess(Thread):
    def __init__(self, ThreadName, HMI, ativo = '', currency = '', Cotacoes=[]):
        Thread.__init__(self)
        self.HMI = HMI
        self.ThreadName = ThreadName
        self.ativo = ativo
        self.currency = currency
        self.Cotacoes = Cotacoes

    def run(self):
        try:
            if self.ThreadName == "GetAllTickers":
                time.sleep(0.1)
                self.HMI.YahooFinance.GetAllTickers()
            elif self.ThreadName == 'Thread_AtualizarCotações':
                self.Thread_AtualizarCotacoes()
            elif self.ThreadName == 'Thread_GetCotacao':
                Cotacao = float(self.HMI.YahooFinance.GetCotacao(self.ativo, self.currency))
                if Cotacao > 0: self.HMI.DBManager.UpdateCotacao(self.ativo, Cotacao)
            elif self.ThreadName == 'Thread_GetCotacaoCripto':
                Cotacao, CotacaoDolar = self.HMI.YahooFinance.GetCotacaoCripto(self.ativo, self.currency)
                if Cotacao > 0 and not self.ativo in ["USD", "BUSD", "USDT", "USDC", "USDP", "TUSD"]:
                    self.HMI.DBManager.UpdateCotacao(self.ativo, Cotacao)
                if CotacaoDolar > 0: self.HMI.DBManager.UpdateCotacao("USD", CotacaoDolar)
            elif self.ThreadName == 'Thread_GetCotacaoCripto_FromExcelImportation':
                def AtivoExisteNaTabelaDeCotacoes(ativo):
                    Table, cursor = self.HMI.DBManager.GetDataDB("SELECT * FROM Cotações")
                    aux = list(filter(lambda x: x[2]==ativo, Table))
                    if len(aux)>0: return True
                    else: return False
                def AtivoExisteNaFolhaDeCotacoes(ativo, Cotacoes):
                    try:
                        Cotacao = [item[3] for item in Cotacoes if item[2] == ativo][0]
                        if Cotacao>0: return True
                        else: return False
                    except: pass

                if not self.ativo == self.currency and not AtivoExisteNaTabelaDeCotacoes(self.ativo):
                        Cotacao = 0.
                        Modo = "Manual"
                        try:
                            Cotacao, CotacaoDolar = self.HMI.YahooFinance.GetCotacaoCripto(self.ativo, self.currency)
                            if Cotacao > 0: Modo = "Auto"
                        except:pass
                        finally:
                            self.HMI.DBManager.AddRowInCurrentDB('Cotações', [('Modo', Modo),
                                                                              ('DataDeAtualização', datetime.strptime(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")),
                                                                              ('Ativo', self.ativo),
                                                                              ('Cotação', Cotacao)])
        except Exception as error: print("Error in ",self.ThreadName, "\n", error)

    def Thread_AtualizarCotacoes(self):
        try:
            self.HMI.AtualizarCotacoes_running = True
            try:
                self.HMI.Movie_AttCotacoes.start()
                self.HMI.Button_AttCotacoes.unsetCursor()
            except:pass
            finally:
                try: self.HMI.DBManager.AtualizarCotacoes_run()
                except:pass
        except Exception as e:
            self.HMI.ThreadLock.acquire()
            print(e)
            self.HMI.ThreadLock.release()
        finally:
            try:
                self.HMI.Movie_AttCotacoes.stop()
                self.HMI.Movie_AttCotacoes.jumpToFrame(0)
            except:pass
            try:
                playsound("./sounds/Coins Dropping.mp3")
                self.HMI.AtualizarCotacoes_running = False
                self.HMI.Button_AttCotacoes.setCursor(QCursor(Qt.PointingHandCursor))
            except:pass

class WorkerThread(QThread):
    update_table = pyqtSignal(int, int, str)
    define_table_width = pyqtSignal(list, list)
    def __init__(self, ThreadName, HMI):
        super().__init__()
        self.__id = ThreadName
        self.__abort = False
        self.HMI = HMI # Da permissão a todo o controle do HMI

    def run(self):
        if self.__id == 'Thread_CreateTable_11_2':
            self.Thread_CreateTable_11_2()
        elif self.__id == 'Thread_CalcularTributacao':
            self.HMI.DBManager.LW.show()
            self.Thread_CalcularTributacao()
        elif self.__id == 'Thread_EsmaecerMsgSucesso':
            self.Thread_EsmaecerMsgSucesso()
        elif self.__id == 'Thread_BuscarSetoresExistentes':
            self.Thread_BuscarSetoresExistentes()
        elif self.__id == 'Thread_LoadingARCApage':
            self.Thread_LoadingARCApage()
        elif self.__id == 'Thread_TextBox_Aplicar':
            self.Thread_TextBox_Aplicar()
        elif self.__id == 'Thread_CheckVersion':
            self.HMI.VersionChecker.CheckVersion()
        elif self.__id == 'Thread_UpdateVersion':
            self.HMI.VersionChecker.UpdateVersion()

    def Thread_CreateTable_11_2(self):
        data = self.HMI.DBManager.GetAllContasCorrente()
        for i, item in enumerate(data):
            time.sleep(1/60)
            self.update_table.emit(i,0,str(item[0]))
            self.update_table.emit(i,1,str(item[1]))

    def Function_define_table_width_11_2(self):
        HHeader = ['Corretora',
                   'Conta-corrente em '+self.HMI.DBManager.GetUserCoinCurrency()]
        data = self.HMI.DBManager.GetAllContasCorrente()
        self.define_table_width.emit(data, HHeader)

    def Thread_CalcularTributacao(self):
        try:
            self.HMI.DBManager.LW.show()
            time.sleep(0.5)
            self.HMI.HMI_Tributacao.CalcularTributacao()
            self.HMI.DBManager.LW.close()
            self.HMI.DBManager.FLAG = False
        except:pass

    def Thread_EsmaecerMsgSucesso(self):
        try:self.HMI.Msg.Esmaecer()
        except:pass

    def Thread_BuscarSetoresExistentes(self):
        try:
            self.HMI.setCursor(Qt.WaitCursor)
            Setores = self.HMI.YahooFinance.SetoresExistentes()
            if len(Setores) > 0:
                Atualizou = self.HMI.DBManager.AlterSetores(Setores)
                if Atualizou:
                    self.HMI.UpdatePage()
            self.HMI.unsetCursor()
        except:pass

    def Thread_LoadingARCApage(self):
        try:
            ContaCorrente = 0
            corretoras = self.HMI.DBManager.GetCorretoras("Bolsa")
            for corretora in corretoras:
                ContaCorrente += float(self.HMI.DBManager.GetValorEmContaCorrente(corretora, "Bolsa"))
            corretoras = self.HMI.DBManager.GetCorretoras("Cripto")
            for corretora in corretoras:
                ContaCorrente += float(self.HMI.DBManager.GetValorEmContaCorrente(corretora, "Cripto"))
            self.HMI.SumContasCorrentes = ContaCorrente
            self.HMI.HMI_ARCA.MontanteEmAplicacao = round(self.HMI.DBManager.GetMontanteNasCorretoras() - ContaCorrente, 2)
            if self.HMI.PageID == '11' and self.HMI.PageIDAux == '':
                self.HMI.TextBox_MontanteEmAplicacao.setText(str('%.2f' % self.HMI.HMI_ARCA.MontanteEmAplicacao))
                self.HMI.TextBox_MontanteEmAplicacao.setStyleSheet("background-color: black; color: green;")

        except:pass

    def Thread_TextBox_Aplicar(self):
        while self.HMI.PageID == "11" and self.HMI.PageIDAux == '':
            try:
                if isinstance(self.HMI.Patrimonio, float):
                    text = round((self.HMI.Patrimonio-int(float(self.HMI.TextBox_MesesDeReserva.text()))*float(self.HMI.TextBox_GastoMensal.text()))-float(self.HMI.TextBox_MontanteEmAplicacao.text()), 2)
                    if text >= 0:
                        self.HMI.TextBox_Aplicar.setStyleSheet("background-color: black; color: green;")
                    else:
                        text = max(-self.HMI.Patrimonio + self.HMI.SumContasCorrentes, text)
                        self.HMI.TextBox_Aplicar.setStyleSheet("background-color: black; color: red;")
                else:
                    text = "Calculando..."
                    self.HMI.TextBox_Aplicar.setStyleSheet("background-color: black; color: orange;")
                self.HMI.TextBox_Aplicar.setText(str(text))
                if text == "Calculando...": time.sleep(0.1)
                else: time.sleep(1)
            except Exception as e: time.sleep(2)