# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 00:16:18 2021

@author: caiop
"""
from BackgroundProcesses import BackgroundProcess as BP

import yfinance as yf # To evitando de usar essa
from yahoo_fin.stock_info import * # Dar preferencia pra usar essa. Da menos BUG

import pandas as pd
import pandas_datareader.data as web

yf.pdr_override()

from datetime import datetime
from datetime import timedelta

import time
import os
from pathlib import Path
import glob
import shutil

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import codecs
import csv

import requests
import json # ?
from bs4 import BeautifulSoup

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

'''
Descrição:
    A classe YahooFinance tem a finalidade de fornecer informações para o programa principal.

    Segue alguns exemplos de uso da biblioteca yfinance, usada nessa clase:
        Amazon = yf.Ticker("AMZN") # Recupera online as inormações do ticker e salva as informações no dict info
        Amazon.info # dict info que contém todas as informações buscadas online
        print(Amazon.info.keys()) # print isso para ver o que foi recuperado
        Amazon.info['sector'] # retorna o setor do ticker, por exemplo
        Amazon.history(period="max") # retorna o histórico dos preços: date, open, high, low, close, volume, dividends, stocksplits
        Amazon.history(start=datetime.datetime(2012,5,31) , end=datetime.datetime(2013,1,30)) # retorna o histórico dos preços, com intervalo de datas definido
        df = yf.download("AMZN MSFT", start="2019-01-01", end="2020-01-01", group_by="ticker") # retorna um pandas dataframe com ambos os tickers requisitados
        df.AMZN # recupera apenas as informações da Amazon que acabou de ser baixada
        AMZN_historical = AMZN.history(period="max", interval="1wk") # interval= “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

        old  =  pfizer.history(start="2010-01-01",  end=”2020-07-21”)
        old.head()
        old = old.reset_index()
        for i in ['Open', 'High', 'Close', 'Low']:
              old[i]  =  old[i].astype('float64')
        import plotly.graph_objects as go
        fig = go.Figure(data=[go.Candlestick(x=old['Date'],
                                             open=old['Open'],
                                             high=old['High'],
                                             low=old['Low'],
                                             close=old['Close'])])
       fig.show()
       fig = px.line(old, x="Date", y="Open", title='PFizer Stock Prices')
       fig.show()
'''

class YahooFinance(object):
    def __init__(self, HMI):
        super().__init__()
        self.HMI = HMI
        self.SetoresOffline = ['Indefinido',
                               'Bens Indls / Máqs e Equips',
                               'Bens Indls / Mat Transporte',
                               'Bens Indls/Transporte',
                               'Cons N  Básico / Alimentos Processados',
                               'Cons N Cíclico / Bebidas',
                               'Cons N Cíclico / Comércio Distr.',
                               'Cons N Cíclico / Pr Pessoal Limp',
                               'Consumo Cíclico / Comércio',
                               'Consumo Cíclico / Tecid Vest Calç',
                               'Consumo Cíclico/Constr Civil',
                               'Consumo Cíclico/Viagens e Lazer',
                               'Diversos',
                               'Financ e Outros / Explor Imóveis',
                               'Financ e Outros / Interms Financs',
                               'Financ e Outros / Previd  Seguros',
                               'Financeiro e Outros/Serviços Financeiros Diversos',
                               'Mats Básicos / Madeira e Papel',
                               'Mats Básicos / Mineração',
                               'Mats Básicos / Químicos',
                               'Mats Básicos / Sid Metalurgia',
                               'Petróleo/ Gás e Biocombustíveis',
                               'Saúde/Comércio Distr.',
                               'Saúde/SM Hosp An.Diag',
                               'Tec.Informação/Programas Servs',
                               'Telecomunicação',
                               'Utilidade Públ / Água Saneamento',
                               'Utilidade Públ / Energ Elétrica',
                               'Imobiliário']

        self.Thread_GetAllTickers = BP(ThreadName="GetAllTickers", HMI=self.HMI)
        self.Thread_GetAllTickers.start()

    def GetAllTickers(self): # Thread
        try:
            df1 = pd.DataFrame(tickers_dow())
            df2 = pd.DataFrame(tickers_ftse100())
            df3 = pd.DataFrame(tickers_ftse250())
            df4 = pd.DataFrame(tickers_ibovespa())
            df5 = pd.DataFrame(tickers_nasdaq())
            df6 = pd.DataFrame(tickers_nifty50())
            df7 = pd.DataFrame(tickers_niftybank())
            df8 = pd.DataFrame(tickers_other())
            df9 = pd.DataFrame(tickers_sp500())
            df_AllTickers = df1
            df_AllTickers = df_AllTickers.append(df2)
            df_AllTickers = df_AllTickers.append(df3)
            df_AllTickers = df_AllTickers.append(df4)
            df_AllTickers = df_AllTickers.append(df5)
            df_AllTickers = df_AllTickers.append(df6)
            df_AllTickers = df_AllTickers.append(df7)
            df_AllTickers = df_AllTickers.append(df8)
            df_AllTickers = df_AllTickers.append(df9)
            List_AllTickers = sorted(list(set(ticker for ticker in df_AllTickers[0].values.tolist())))
            del List_AllTickers[0]

            self.HMI.DBManager.SetAllTickers(List_AllTickers)
        except:pass

        # self.HMI.ThreadLock.acquire()
        # print(List_AllTickers)
        # self.HMI.ThreadLock.release()

    def GetSetoresBasicos(self):
        return self.SetoresOffline

    def SetoresExistentes(self):
        # Se não houver conexão com a internet, retornar lista vazia
        Setores = []
        df = self.busca_carteira_teorica("IBOV")
        if len(df)>0:
            Setores = df["Setor"]
            Setores = list(dict.fromkeys(Setores))
            Setores.insert(0, "Indefinido")
            Setores.append("Imobiliário")

        # Adicionar ao SetoresOnline: Indefinido e Imobiliário
        else: Setores = self.SetoresOffline
        return Setores

    def GetCotacao(self, ativo, currency):
        # print("Get cotação ",ativo) # Debug
        url = "https://finance.yahoo.com"; timeout = 5
        try: request = requests.get(url, timeout=timeout) # Testa conexão com a internet
        except (requests.ConnectionError, requests.Timeout) as exception: # Sem conexão com a internet
            try: UltimaCotacao = 0 # Buscar cotação na tabela de cotações manual
            except: UltimaCotacao = -1
            finally: return UltimaCotacao

        UltimaCotacao = 0.
        start_date = datetime.strptime((datetime.now()-timedelta(days=2)).strftime("%Y/%m/%d"), "%Y/%m/%d")
        try:
            # print("\nBuscando cotação de ",ativo) # Debug
            try: # Try method 1
                # print("Get Cotacao ativo com primeiro metodo... ") # Debug
                df = get_data(ativo+".SA", start_date=start_date)
                UltimaCotacao = round(float(df["close"][-1]),2)
                # UltimaCotacao = 20. # Debug pra quando desliga a busca online, fica mais rápido pra testes
            except:
                try: # Try method 2
                    # print("Get Cotacao ativo com segundo metodo... ") # Debug
                    data = web.get_data_yahoo(ativo+".SA", start=start_date) # Não funciona bem, apresenta BUGs em momentos aleatórios, mas pode ser uma solução
                    UltimaCotacao = round(float(data["Close"][-1]),2)
                except:
                    try: # Try method 3
                        # print("Get Cotacao ativo com terceiro metodo... ") # Debug
                        df = get_data(ativo, start_date=start_date)
                        UltimaCotacao = round(float(df["close"][-1]),2)
                    except:
                        try: # Try method 4
                            # print("Get Cotacao ativo com quarto metodo... ") # Debug
                            data = web.get_data_yahoo(ativo, start=start_date) # Não funciona bem, apresenta BUGs em momentos aleatórios, mas pode ser uma solução
                            UltimaCotacao = round(float(data["Close"][-1]),2)
                        except:
                            try:
                                # Buscar cotação na tabela de cotações manual
                                # print("Get Cotacao ativo com quinto metodo (última cotação registrada na DB)... ") # Debug
                                UltimaCotacao = 0
                            except: UltimaCotacao = -1
        except Exception as error:
            print("Erro em GetCotacao")
        finally:
            print('UltimaCotacao '+ativo+': ', UltimaCotacao) # Debug
            # if UltimaCotacao > 0:
            #     self.HMI.DBManager.UpdateCotacao(ativo, UltimaCotacao)
            return UltimaCotacao

    def GetCotacaoCripto(self, coin, currency):
        def GetDolarCotacao(currency): # Usei requests pq funciona melhor pra cotação do dólar, dá menos problema
            url = "https://finance.yahoo.com"; timeout = 5
            try: request = requests.get(url, timeout=timeout) # Testa conexão com a internet
            except (requests.ConnectionError, requests.Timeout) as exception: return 0.
            Cotacao = 0.
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
                page = requests.get("https://www.google.com/search?q=USD-"+currency+"&sxsrf=AOaemvIRH-J7aELoY_l_QtAqmIz81znBZQ%3A1636483120575&source=hp&ei=MMCKYZfJIK7M1sQPisiX8A4&iflsig=ALs-wAMAAAAAYYrOQM8rnle2rsgfiF4d2bM-_oRvPR16&oq=USD-BRL&gs_lcp=Cgdnd3Mtd2l6EAMyCQgjECcQRhCCAjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjoHCCMQ6gIQJzoECCMQJzoKCC4QxwEQ0QMQQzoLCC4QgAQQxwEQ0QM6CwguEIAEEMcBEKMCOgUIABCABDoFCC4QgAQ6BAgAEEM6BQgAEJECOgoIABCABBCHAhAUOgYIABAKEB5QghBYrRhgqiBoAXAAeACAAYABiAGSBpIBAzAuN5gBAKABAbABCg&sclient=gws-wiz&ved=0ahUKEwiXodLY9ov0AhUuppUCHQrkBe4Q4dUDCAY&uact=5", headers=headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                valor_dolar = soup.find_all("span",class_="DFlfde SwHCTb")[0]
                Cotacao = float(valor_dolar['data-value'])
            except: print("Erro na recuperação da cotação do dólar.\nFunção geradora do erro: GetDolarCotacao em YahooFinance.py")
            finally: return round(Cotacao, 3)
        def GetCoinCotacaoEmUSD(coin):
            def TemAcessoAInternet():
                url = "https://finance.yahoo.com"; timeout = 5
                try:
                    request = requests.get(url, timeout=timeout) # Testa conexão com a internet
                    return True
                except (requests.ConnectionError, requests.Timeout) as exception: return False
            if not TemAcessoAInternet(): return 0.

            cotacao = 0.
            try: # Try first method
                start_date = datetime.strptime((datetime.now()-timedelta(hours=2)).strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S")
                df = get_data(coin+"-USD", start_date=start_date)
                cotacao = round(data["close"][-1],2)
            except:
                try: # Try second method
                    data = web.get_data_yahoo(coin+"-USD", start=start_date) # Não funciona bem, apresenta BUGs em momentos aleatórios, mas pode ser uma solução
                    cotacao = round(data["Close"][-1],2)
                except: print("Erro na recuperação da cotação do ativo.\nFunção geradora do erro: GetCoinCotacaoEmUSD em YahooFinance.py")
            finally: return round(cotacao, 8)
        UltimaCotacao = 0.
        try:
            print("\nBuscando cotação de ",coin) # Debug
            if coin == currency:
                UltimaCotacao = 1.
            else:
                if currency in ["USD", "BUSD", "USDT", "USDC", "USDP", "TUSD"]:
                    CotacaoDolar = 1. # O próprio dólar em dólar
                else:
                    CotacaoDolar = GetDolarCotacao(currency) # Cotação do dólar na moeda corrente
                    # self.HMI.DBManager.UpdateCotacao("USD", CotacaoDolar)

                if coin in ["USD", "BUSD", "USDT", "USDC", "USDP", "TUSD"]:
                    UltimaCotacao = 1. # A cotação já está em dólar
                else:
                    CotacaoCoinEmUSD = GetCoinCotacaoEmUSD(coin)
                    UltimaCotacao = round(CotacaoCoinEmUSD * float(CotacaoDolar), 8) # Converte para a moeda corrente

                # if UltimaCotacao > 0:
                #     if not coin in ["USD", "BUSD", "USDT", "USDC", "USDP", "TUSD"]:
                        # self.HMI.DBManager.UpdateCotacao(coin, UltimaCotacao)
        except:
            try:
                # Buscar cotação na tabela de cotações manual
                # print("Get Cotacao ativo com quinto metodo (última cotação registrada na DB)... ") # Debug
                UltimaCotacao = 0
            except: UltimaCotacao = -1
        finally:
            print('UltimaCotacao '+coin+': ', UltimaCotacao) # Debug
            return UltimaCotacao, CotacaoDolar

    def isShare(self, ShareToBeChecked):
        # return True # Debug pra quando desliga a busca online, fica mais rápido pra testes
        IsShare = False
        cotacaoTeste = 0
        start_date = datetime.strptime((datetime.now()-timedelta(days=2)).strftime("%Y/%m/%d"), "%Y/%m/%d")

        if not ShareToBeChecked in self.HMI.DBManager.GetAllTickers(): return IsShare # Otimizador

        # check if Share is in yahoo

        def TemAcessoAInternet():
            url = "https://finance.yahoo.com"; timeout = 5
            try:
                request = requests.get(url, timeout=timeout) # Testa conexão com a internet
                return True
            except (requests.ConnectionError, requests.Timeout) as exception: return False
        if not TemAcessoAInternet(): return False

        try:
            data = get_data(ShareToBeChecked+".SA", start_date=start_date)
            cotacaoTeste = float(data["close"][-1])
            IsShare = True
        except:
            try:
                data = web.get_data_yahoo(ShareToBeChecked+".SA", start=start_date) # Não funciona bem, apresenta BUGs em momentos aleatórios, mas pode ser uma solução
                cotacaoTeste = float(data["Close"][-1])
                IsShare = True
            except:
                try:
                    data = get_data(ShareToBeChecked, start_date=start_date)
                    cotacaoTeste = float(data["close"][-1])
                    IsShare = True
                except:
                    try:
                        data = web.get_data_yahoo(ShareToBeChecked, start=start_date) # Não funciona bem, apresenta BUGs em momentos aleatórios, mas pode ser uma solução
                        cotacaoTeste = float(data["Close"][-1])
                        IsShare = True
                    except:
                        cotacaoTeste = 0
                        IsShare = False
        finally:
            # time.sleep(1) # Antibug?
            return IsShare, round(cotacaoTeste,2)

    def busca_carteira_teorica(self, indice, espera = 4):
        '''
        Essa função retorna um df com informações sobre o indice solicitado.
        Para chamar essa função use: exemplo: self.busca_carteira_teorica("IBOV")
        '''
        # print("Buscando Índice "+indice+"...") # Debug
        self.HMI.LW.Label_Titulo.setText("Atualizando lista de Setores\nPor favor aguarde...\nRecuperando informações online.")
        self.HMI.LW.pbar.setValue(1)
        df = []
        url = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/"+indice.upper()+"?language=pt-br"
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")
            options.add_argument('--window-size=1280,1024')
            driver = webdriver.Chrome(chrome_options=options, executable_path = os.getcwd()+'\\chromedriver.exe')
            driver.set_window_size(1280, 720)
            DownloadsPath = str(Path.home() / "Downloads")
            driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': DownloadsPath}}
            driver.execute("send_command", params)
            self.HMI.LW.Label_Titulo.setText("Atualizando lista de Setores\nPor favor aguarde...\nRecuperando informações online.\nConectando ao servidor")
            # print("Abriu navegador") # Debug
            self.HMI.LW.pbar.setValue(20)
            time.sleep(1) # Depende do PC
            driver.get(url)
            # print("Abriu url") # Debug
            self.HMI.LW.Label_Titulo.setText("Atualizando lista de Setores\nPor favor aguarde...\nRecuperando informações online.\nConectando ao servidor")
            self.HMI.LW.pbar.setValue(40)
            time.sleep(espera) # Depende do server e da velocidade da internet
            driver.find_element_by_id("segment").send_keys("Setor de Atuação")
            # print("Selecionou Setor de Atuação") # Debug
            self.HMI.LW.Label_Titulo.setText("Atualizando lista de Setores\nPor favor aguarde...\nRecuperando informações online.\nConectando ao servidor")
            self.HMI.LW.pbar.setValue(50)
            time.sleep(2) # Depende do server
            driver.find_element_by_link_text("Download").click()
            # print("Baixando csv...") # Debug
            self.HMI.LW.Label_Titulo.setText("Atualizando lista de Setores\nPor favor aguarde...\nRecuperando informações online.\nBaixando csv...")
            self.HMI.LW.pbar.setValue(70)
            time.sleep(espera) # Depende do server e da velocidade da internet
            driver.close()
            # print("Fechou navegador\nSubstituindo arquivo no destino") # Debug
            self.HMI.LW.Label_Titulo.setText("Atualizando lista de Setores\nPor favor aguarde...\nAtualizando informações.\nFechou navegador\nSubstituindo arquivo no destino")
            self.HMI.LW.pbar.setValue(80)

            list_of_files = glob.glob(DownloadsPath+"/*")
            Last_File = max(list_of_files, key=os.path.getctime)
            try:os.remove(os.getcwd()+"\\IBOV.csv")
            except:pass
            shutil.move(Last_File, os.getcwd()+"\\IBOV.csv")
            # print("Lendo arquivo csv") # Debug
            self.HMI.LW.pbar.setValue(90)
            self.HMI.LW.Label_Titulo.setText("Atualizando lista de Setores\nPor favor aguarde...\nAtualizando informações.\nLendo arquivo csv...")
            df = pd.read_csv("IBOV.csv", sep=";", encoding="ISO-8859-1", skipfooter=2, engine="python", thousands=".", decimal=",", header=1, index_col=False)
            # print("Leitura realizada com sucesso.") # Debug
            self.HMI.LW.Label_Titulo.setText("Lista de setores atualizada.")
            self.HMI.LW.Label_Titulo.setStyleSheet('color: green')
            self.HMI.LW.pbar.setValue(100)
            try:os.remove(os.getcwd()+"\\IBOV.csv")
            except:pass
            time.sleep(2) # Tempo pra ler que deu certo
            self.HMI.LW.close()
        except Exception as error:
            # print("Ocorreu um erro inesperado.\nTente novamente mais tarde.") # Debug
            self.HMI.LW.Label_Titulo.setStyleSheet('color: red')
            self.HMI.LW.Label_Titulo.setText("Ocorreu um erro inesperado:\nEssa janela fechará automaticamente em 8\n"+str(error))
            time.sleep(1) # Tempo pra ler que deu errado
            self.HMI.LW.Label_Titulo.setText("Ocorreu um erro inesperado:\nEssa janela fechará automaticamente em 7\n"+str(error))
            time.sleep(1) # Tempo pra ler que deu errado
            self.HMI.LW.Label_Titulo.setText("Ocorreu um erro inesperado:\nEssa janela fechará automaticamente em 6\n"+str(error))
            time.sleep(1) # Tempo pra ler que deu errado
            self.HMI.LW.Label_Titulo.setText("Ocorreu um erro inesperado:\nEssa janela fechará automaticamente em 5\n"+str(error))
            time.sleep(1) # Tempo pra ler que deu errado
            self.HMI.LW.Label_Titulo.setText("Ocorreu um erro inesperado:\nEssa janela fechará automaticamente em 4\n"+str(error))
            time.sleep(1) # Tempo pra ler que deu errado
            self.HMI.LW.Label_Titulo.setText("Ocorreu um erro inesperado:\nEssa janela fechará automaticamente em 3\n"+str(error))
            time.sleep(1) # Tempo pra ler que deu errado
            self.HMI.LW.Label_Titulo.setText("Ocorreu um erro inesperado:\nEssa janela fechará automaticamente em 2\n"+str(error))
            time.sleep(1) # Tempo pra ler que deu errado
            self.HMI.LW.Label_Titulo.setText("Ocorreu um erro inesperado:\nEssa janela fechará automaticamente em 1\n"+str(error))
            time.sleep(1) # Tempo pra ler que deu errado
            self.HMI.LW.close()
            df = []
        finally: return df