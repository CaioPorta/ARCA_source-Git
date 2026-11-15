# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 01:44:04 2021

@author: caiop
"""
import os
from os.path import exists
import sys
import copy
import time
from datetime import datetime
from datetime import timedelta

import sqlite3
from sqlite3 import Error

import threading
from threading import Lock
from BackgroundProcesses import BackgroundProcess as BP
from BackgroundProcesses import WorkerThread

import LoadingWindow

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class DBManager(object):
#%% init
    def __init__(self, HMI):
        self.HMI = HMI
        self.ThreadLock = Lock()
        self.TiposDeAtivosBasicos = ['Ações e Negócios',
                                     'Real Estate',
                                     'Caixa',
                                     'Ativos Internacionais']
        self.SubtiposDeAtivosBasicos = [('Ações e Negócios','Ações Nacionais'),
                                        ('Ações e Negócios','Fundos de investimentos: Ações e Negócios'),
                                        ('Real Estate','Fundos Imobiliários'),
                                        ('Real Estate','Terrenos'),
                                        ('Real Estate','Construções'),
                                        ('Caixa','Renda Fixa'),
                                        ('Caixa','Tesouro Direto e Títulos Públicos'),
                                        ('Caixa','Previdência Privada'),
                                        ('Caixa','COE'),
                                        ('Caixa','Fundos de Investimento: Renda Fixa'),
                                        ('Ativos Internacionais','BDR'),
                                        ('Ativos Internacionais','Fundos de Investimento: Ações Internacionais')]
        self.SetoresBasicos = self.HMI.YahooFinance.GetSetoresBasicos()
        # if not len(self.SetoresBasicos)>0: self.SetoresBasicos = self.HMI.YahooFinance.GetSetoresBasicos()
        self.MoedasFiatBasicas = ['CNY','USD','EUR','JPY','INR','RUB','GBP','CHF','KRW','MXN','CAD','BRL','AUD','SAR','HKD','TWD','TRY','SGD','SEK','ZAR','ILS']

        self.FLAG = False

        self.SumContasCorrentes = 0

        self.conn = None
        self.User = None

    def __str__(self):
        def chk_conn(conn):
            try:
               conn.cursor()
               return True
            except Exception:
               return False

        if chk_conn(self.conn): return "Conectado a base de dados: " + str(self.User) + ".db"
        else: return "Nenhuma base de dados conectada"

#%% Sobre o Usuário

    def CriarNovoPerfil(self, user='', senha='', email='', moedacorrente='', userpath=''): # Cria e conecta
        try:
            if len(user)==0: self.User = self.HMI.TextBox_NomeDeUsuario.text()
            else: self.User = user
            if len(senha)==0: self.Senha = self.HMI.TextBox_Senha1.text()
            else: self.Senha = senha
            if len(email)==0: self.Email = self.HMI.TextBox_Email.text()
            else: self.Email = email
            if len(moedacorrente)==0: moedacorrente = self.HMI.ComboBox_Currency.currentText()
            if len(userpath)==0: self.UserPath = self.HMI.TextBox_Path.text()
            else: self.UserPath = userpath
            currdir = os.getcwd() # Get current directory
            if self.UserPath == '': self.UserPath = currdir

            # Create Usuários.db IF NOT EXISTS
            self.CriarDB(currdir+'\\Users.db')
            # Connect to Users.db
            self.ConnectToDB(currdir+'\\Users.db')
            # Create Table Usuários IF NOT EXISTS
            self.CreateTableInCurrentDB('Usuários', [('Usuário', 'TEXT'), ('Email', 'TEXT'), ('Path', 'TEXT')])
            # Adicionar Usuário e Email
            self.AddRowInCurrentDB('Usuários', [('Usuário',self.User), ('Email',self.Email), ('Path', self.UserPath)])
            # Disconnect from Users.db
            self.Disconnect()

            # Criar user.db
            self.CriarDB(self.UserPath+"\\"+self.User+'.db')
            # Connect to User.db
            self.ConnectToDB(self.UserPath+"\\"+self.User+'.db')
            # Create Table Perfil
            self.CreateTableInCurrentDB('Perfil', [('Usuário', 'TEXT'), ('Senha','TEXT'), ('Email', 'TEXT'), ('TaxaB3Per','REAL'), ('MoedaCorrente','TEXT'), ('GastoMensal', 'REAL'), ('MesesDeReserva', 'REAL')])
            # Adicionar Usuário, Senha, Email, TaxaB3Per = 0.03%
            self.AddRowInCurrentDB('Perfil', [('Usuário',self.User), ('Senha',self.Senha), ('Email',self.Email), ('TaxaB3Per',0.03), ('MoedaCorrente',moedacorrente), ('GastoMensal', 0), ('MesesDeReserva', 6)])
            # Create Table Perfil_TiposDeAtivos
            self.CreateTableInCurrentDB('TiposDeAtivo', [('TipoDeAtivo', 'TEXT')])
            # Adicionar os Tipos básicos
            for TipoDeAtivo in self.TiposDeAtivosBasicos:
                self.AddRowInCurrentDB('TiposDeAtivo', [('TipoDeAtivo', TipoDeAtivo)])
            # Create Table Perfil_SubtipoDeAtivos
            self.CreateTableInCurrentDB('SubtiposDeAtivo', [('TipoDeAtivo', 'TEXT'),('SubtipoDeAtivo', 'TEXT')])
            # Adicionar os Subtipos básicos
            for item in self.SubtiposDeAtivosBasicos:
                TipoDeAtivo = item[0]
                SubtipoDeAtivo = item[1]
                self.AddRowInCurrentDB('SubtiposDeAtivo', [('TiposDeAtivo', TipoDeAtivo),('SubtipoDeAtivo', SubtipoDeAtivo)])
            # Create Table Setores
            self.CreateTableInCurrentDB('Setores', [('Setor', 'TEXT')])
            # Adicionar os Setores básicos
            for Setor in self.SetoresBasicos:
                self.AddRowInCurrentDB('Setores', [('Setor', Setor)])
            # Create Table Bolsa
            self.CreateTableInCurrentDB('Bolsa', [('Ativo', 'TEXT'),('TipoDeAtivo', 'TEXT'),('SubtipoDeAtivo', 'TEXT'),('Setor', 'TEXT')])
            # Create Table Cotações
            self.CreateTableInCurrentDB('Cotações', [('Modo', 'TEXT'),('DataDeAtualização', 'DATETIME'),('Ativo', 'TEXT'),('Cotação', 'REAL')])
            if not moedacorrente == "USD": self.AddRowInCurrentDB('Cotações', [('Modo', 'Auto'),('DataDeAtualização', datetime.strptime(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")),('Ativo', 'USD'),('Cotação', 0.)])
            # Create Table Tributação
            self.CreateTableInCurrentDB('TributaçãoDTBolsa', [('MesAno', 'DATETIME'),('Resultado', 'REAL'),('PrejuizoAcumulado', 'REAL'),('ResultadoFinal', 'REAL'),('Alíquota', 'REAL'),('LucroMínimoTaxável', 'REAL'),('ImpostoDevido', 'REAL'),('ResultadoLíquido', 'REAL')])
            self.CreateTableInCurrentDB('TributaçãoSTBolsa', [('MesAno', 'DATETIME'),('Resultado', 'REAL'),('PrejuizoAcumulado', 'REAL'),('ResultadoFinal', 'REAL'),('Alíquota', 'REAL'),('LucroMínimoTaxável', 'REAL'),('ImpostoDevido', 'REAL'),('ResultadoLíquido', 'REAL')])
            self.CreateTableInCurrentDB('TributaçãoDTCripto', [('MesAno', 'DATETIME'),('Resultado', 'REAL'),('PrejuizoAcumulado', 'REAL'),('ResultadoFinal', 'REAL'),('Alíquota', 'REAL'),('LucroMínimoTaxável', 'REAL'),('ImpostoDevido', 'REAL'),('ResultadoLíquido', 'REAL')])
            self.CreateTableInCurrentDB('TributaçãoSTCripto', [('MesAno', 'DATETIME'),('Resultado', 'REAL'),('PrejuizoAcumulado', 'REAL'),('ResultadoFinal', 'REAL'),('Alíquota', 'REAL'),('LucroMínimoTaxável', 'REAL'),('ImpostoDevido', 'REAL'),('ResultadoLíquido', 'REAL')])
            # Create Table Corretoras
            self.CreateTableInCurrentDB('Corretoras', [('Corretora', 'TEXT'),('MoedaCorrente', 'TEXT'),('ContaCorrente', 'REAL')])
            # Create Table Bancos
            self.CreateTableInCurrentDB('Bancos', [('Banco', 'TEXT'),('MoedaCorrente', 'TEXT'),('ContaCorrente', 'REAL')])
            # Create Table MoedasFiat
            self.CreateTableInCurrentDB('MoedasFiat', [('MoedaFiat', 'TEXT')])
            for Moeda in self.MoedasFiatBasicas:
                self.AddRowInCurrentDB('MoedasFiat', [('MoedaFiat', Moeda)])

            return True
        except Exception as e:
            print(e)

    def CheckIfEmailExists(self, EmailToCheck):
        Exists = False
        try:
            currdir = os.getcwd() # Get current directory
            conn = sqlite3.connect(currdir+'\\Users.db')
            retorno = list(conn.execute("SELECT Email FROM Usuários WHERE Email = (?)",[(EmailToCheck)]))
            for row in retorno:
                retorno = list(conn.execute("SELECT Path FROM Usuários WHERE Usuário = (?)",[(UserToCheck)]))
                UserPath = retorno[0][0]
                file_exists = exists(UserPath+"\\"+UserToCheck+".db")
                if file_exists:
                    Exists = True
                else:
                    Exists = "Arquivo não encontrado"
        except:pass
        finally:conn.close()
        return Exists

    def CheckIfUserExists(self, UserToCheck):
        Exists = False
        try:
            currdir = os.getcwd() # Get current directory
            conn = sqlite3.connect(currdir+'\\Users.db')
            retorno = list(conn.execute("SELECT Usuário FROM Usuários WHERE Usuário = (?)",[(UserToCheck)]))
            for row in retorno:
                retorno = list(conn.execute("SELECT Path FROM Usuários WHERE Usuário = (?)",[(UserToCheck)]))
                UserPath = retorno[0][0]
                file_exists = exists(UserPath+"\\"+UserToCheck+".db")
                if file_exists:
                    Exists = True
                else:
                    # print("usuário ta na user.db mas nao tem o arquivo.db")
                    Exists = "Arquivo não encontrado"
        except:pass
        finally:conn.close()
        return Exists

    def ChangePassword(self, NewPassword):
        self.ModifyDB("UPDATE Perfil SET Senha = (?)", [(NewPassword)])

    def ChangeEmail(self, NewEmail): # Ninguém chama essa por enquanto, mas já funciona
        if not self.CheckIfEmailExists(NewEmail):
            self.ModifyDB("UPDATE Perfil SET Email = (?)", [(NewEmail)])
            return True
        return False

    def GetUserPathByUserName(self, user):
        currdir = os.getcwd()
        self.ConnectToDB(currdir+'\\Users.db')
        retorno, cursor = self.GetDataDB("SELECT Path FROM Usuários WHERE Usuário = (?)", [(user)])
        self.Disconnect()
        return retorno[0][0]

    def GoodPassword(self, user, senha):
        UserPath = self.GetUserPathByUserName(user)
        self.ConnectToDB(UserPath+"\\"+user+".db")
        retorno, cursor = self.GetDataDB("SELECT * FROM Perfil")
        if retorno[0][1] == senha:
            self.Disconnect()
            return True
        else:
            self.Disconnect()
            return False

    def DeleteUserDB (self):
        self.Disconnect()
        os.remove(self.UserPath+"\\"+self.User+".db")
        currdir = os.getcwd()
        self.ConnectToDB(currdir+'\\Users.db')
        self.ModifyDB("DELETE FROM Usuários WHERE Usuário = (?)",(self.User))
        self.Disconnect()
        return False

    def ConnectTo(self, user, senha):
        # Se senha correta, connect
        resposta = self.CheckIfUserExists(user)
        if resposta == "Arquivo não encontrado":
            return "Arquivo não existe"
        elif resposta:
            Resposta = self.GoodPassword(user, senha)
            if Resposta == "Arquivo não existe":
                return "Arquivo não existe"
            elif Resposta:
                self.User = user
                self.Email = self.GetEmailByUser(user)
                self.UserPath = self.GetUserPathByUserName(user)
                self.ConnectToDB(self.UserPath+"\\"+user+".db")
                return True
        return False

    def ConnectToDB(self, DB):
        self.conn = sqlite3.connect(DB, check_same_thread=False)

    def Disconnect(self): # Só será desconectada se a FLAG estiver em FALSE, condição imposta lá na thread principal
        # Close connection
        try: self.conn.close()
        except: pass
        finally: return False  # Set self.LoggedIn as False

#%% Adições

    def AddBanco(self):
        def BancoExists(Banco):
            retorno, cursor = self.GetDataDB("SELECT * FROM Bancos")
            retorno = list(filter(lambda x: str("¨"+Banco+"¨").lower() == str(x[0]).lower(), retorno))
            if len(retorno)>0: return True
            return False
        Banco = self.HMI.TextBox_NovoBanco.text().replace(" ","_")
        if BancoExists(Banco): return False
        MoedaCorrente = self.HMI.ComboBox_Currency.currentText()
        self.AddRowInCurrentDB('Bancos', [('Banco', "¨"+Banco+"¨"),('MoedaCorrente', MoedaCorrente),('ContaCorrente', 0)])
        return True

    def AddCorretora(self):
        self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
        def CorretoraExists(corretora):
            retorno, cursor = self.GetDataDB("SELECT * FROM Corretoras")
            retorno = list(filter(lambda x: str(corretora+"¨"+self.HMI.BolsaOuCripto).lower() == str(x[0]).lower(), retorno))
            if len(retorno)>0: return True
            return False
        # Adicionar linha na Table Corretoras: Nome da corretora e coin currency
        BolsaOuCripto = self.HMI.BolsaOuCripto
        Corretora = self.HMI.TextBox_NovaCorretora.text().replace(" ","_")
        if CorretoraExists(Corretora): return False
        if BolsaOuCripto == 'Bolsa':
            MoedaCorrente = self.HMI.ComboBox_Currency.currentText()
            self.AddRowInCurrentDB('Corretoras', [('Corretora', Corretora+"¨"+BolsaOuCripto),('MoedaCorrente', MoedaCorrente),('ContaCorrente', 0)])
            # Create Table DepósitosESaques
            self.CreateTableInCurrentDB("¨"+Corretora+"¨"+BolsaOuCripto+"¨DepSaq", [('Data', 'DATETIME'),('Valor', 'REAL')])

        elif BolsaOuCripto == 'Cripto':
            MoedaCorrente = self.HMI.ComboBox_Currency.currentText()

            self.AddRowInCurrentDB('Corretoras', [('Corretora', Corretora+"¨"+BolsaOuCripto),('MoedaCorrente', MoedaCorrente),('ContaCorrente', 0)])

            TableName = str('OPs'+'¨'+Corretora+'¨'+BolsaOuCripto)
            TableNameBruto = TableName+'¨Bruto'
            TableNameRefinado = TableName+'¨Refinado'

            self.CreateTableInCurrentDB(TableNameRefinado, [('Observação', 'TEXT'),
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

            self.CreateTableInCurrentDB(TableNameBruto, [('Observação', 'TEXT'),
                                                        ('Data', 'DATETIME'),
                                                        ('Tipo', 'TEXT'),
                                                        ('ParEsquerdo', 'TEXT'),
                                                        ('ParDireito', 'TEXT'),
                                                        ('Preço', 'REAL'),
                                                        ('Qqt', 'REAL'),
                                                        ('Taxa', 'REAL'),
                                                        ('MoedaDaTaxa', 'TEXT'),
                                                        ('Conversão', 'REAL')])
        return True

    def AddAtivo(self):
        try:
            self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
            # Adicionar linha na Table Bolsa
            ativo = self.HMI.TextBox_NomeNovoAtivo.text()
            ModoManualAtivo = self.HMI.ModoManualAtivo
            if not ModoManualAtivo: ativo = ativo.upper()
            retorno, cursor = self.GetDataDB("SELECT * FROM Bolsa")
            retorno = list(filter(lambda x: str(x[0]).find(ativo.replace(" ","_"))>-1, retorno))
            if len(retorno) == 0:
                self.AddRowInCurrentDB("Bolsa", [('Ativo', ativo.replace(" ","_")),
                                                 ('TipoDeAtivo', self.HMI.ComboBox_TipoDeAtivo.currentText()),
                                                 ('SubtipoDeAtivo', self.HMI.ComboBox_SubtipoDeAtivo.currentText()),
                                                 ('Setor', self.HMI.ComboBox_SetorAtivo.currentText())])

                # Adicionar linha na Table Cotações: Se modo manual, add 0 à cotação
                Cotacao = 0.
                try:
                    if not ModoManualAtivo: Cotacao = self.HMI.YahooFinance.GetCotacao(ativo, self.GetUserCoinCurrency())
                except:pass
                self.AddRowInCurrentDB('Cotações', [('Modo', "Manual" if ModoManualAtivo else "Auto"),
                                                    ('DataDeAtualização', datetime.strptime(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")),
                                                    ('Ativo', ativo),
                                                    ('Cotação', Cotacao)])

            TableName = str('OPs¨'+ativo.replace(" ","_")+
                            '¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                            '¨'+self.HMI.BolsaOuCripto)
            TableNameBruto = TableName+'¨Bruto'
            TableNameDT = TableName+'¨DT'
            TableNameST = TableName+'¨ST'
            self.CreateTableInCurrentDB(TableNameDT, [('Data', 'DATETIME'),
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
            self.CreateTableInCurrentDB(TableNameST, [('Data', 'DATETIME'),
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
            self.CreateTableInCurrentDB(TableNameBruto, [('Data', 'DATETIME'),
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
        except:pass
        finally: self.AtualizarCotacoes()

    def AddOperacao(self):
        self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
        def ThereIsAnotherOPWithTheSameDate(TableName, data):
            Table_Inicial, cursor = self.GetDataDB("SELECT rowid, * FROM "+TableName+"¨Bruto")
            if "¨Bolsa" in TableName:
                aux = list(filter(lambda x: datetime.strptime(x[1],"%Y-%m-%d %H:%M:%S") == data, Table_Inicial))
            else:
                aux = list(filter(lambda x: datetime.strptime(x[2],"%Y-%m-%d %H:%M:%S") == data, Table_Inicial))
            if len(aux)>0: return True
            return False
        try:
            if self.HMI.BolsaOuCripto == "Bolsa":
                if self.HMI.PageID in ['36a','36b']: ativo = self.HMI.TextBox_NomeNovoAtivo.text().replace(" ","_")
                elif self.HMI.PageID == '28': ativo = self.HMI.ComboBox_Ativo.currentText().replace(" ","_")
                # Adicionar linha na Table OPs_Ativo_Corretora_Bolsa_DT. (Add novos dados. Células de cálculo automatizado, inserir zero)
                TableName = str('OPs¨'+ativo+
                                '¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                                '¨'+self.HMI.BolsaOuCripto)
                TableNameBruto = TableName+'¨Bruto'
                TableNameDT = TableName+'¨DT'
                TableNameST = TableName+'¨ST'
                data = self.HMI.Selecao_Dia+"/"+self.HMI.Selecao_Mes+"/"+self.HMI.Selecao_Ano+" "+self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo
                data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
                if "%" in self.HMI.TextBox_TaxaB3.text():
                    TaxaB3Per = float(self.HMI.TextBox_TaxaB3.text().replace("%",""))
                    TaxaB3 = round(TaxaB3Per/100*int(self.HMI.TextBox_Qqt.text())*float(self.HMI.TextBox_Preco.text()),2)
                else:
                    TaxaB3 = float(self.HMI.TextBox_TaxaB3.text())
                    TaxaB3Per = round(TaxaB3/int(self.HMI.TextBox_Qqt.text())/float(self.HMI.TextBox_Preco.text())*100,2)

                if ThereIsAnotherOPWithTheSameDate(TableName, data): return False
                if data > datetime.now(): return False

                self.AddRowInCurrentDB(TableNameBruto, [('Data', data),
                                                        ('Tipo', "Compra" if self.HMI.Compra else "Venda"),
                                                        ('Qqt', int(self.HMI.TextBox_Qqt.text())),
                                                        ('Preço', float(self.HMI.TextBox_Preco.text())),
                                                        ('Corretagem', float(self.HMI.TextBox_Corretagem.text())),
                                                        ('TaxaB3Per', TaxaB3Per),
                                                        ('TaxaB3', TaxaB3),
                                                        ('Obs', self.HMI.TextBox_Obs.text()),
                                                        ('Estoque', 'NULL'),
                                                        ('CustoDaOperação', TaxaB3+float(self.HMI.TextBox_Corretagem.text())),
                                                        ('CustoTotal', 'NULL'),
                                                        ('CustoMédio', 'NULL'),
                                                        ('Resultado', 'NULL')])
                if not 'Fundos Imobiliários' == self.GetSubtipoDeAtivoDeAtivo(ativo):
                    self.AddRowInCurrentDB(TableNameST, [('Data', data),
                                                        ('Tipo', "Compra" if self.HMI.Compra else "Venda"),
                                                        ('Qqt', int(self.HMI.TextBox_Qqt.text())),
                                                        ('Preço', float(self.HMI.TextBox_Preco.text())),
                                                        ('Corretagem', float(self.HMI.TextBox_Corretagem.text())),
                                                        ('TaxaB3Per', TaxaB3Per),
                                                        ('TaxaB3', TaxaB3),
                                                        ('Obs', self.HMI.TextBox_Obs.text()),
                                                        ('Estoque', 'NULL'),
                                                        ('CustoDaOperação', TaxaB3+float(self.HMI.TextBox_Corretagem.text())),
                                                        ('CustoTotal', 'NULL'),
                                                        ('CustoMédio', 'NULL'),
                                                        ('Resultado', 'NULL')])
                # Separar DT e ST se não for FII. Se for FII fazer só pra DT
                if not 'Fundos Imobiliários' == self.GetSubtipoDeAtivoDeAtivo(ativo):
                    self.SepararDTeST(TableName)
                    # Calcular todas as células automatizadas e fazer update pra cada célula
                    self.CalcularCelsAutomatizadas(TableNameBruto)
                    self.CalcularCelsAutomatizadas(TableNameDT)
                    self.CalcularCelsAutomatizadas(TableNameST)
                else:
                    self.CopiarBrutoPraDT(TableName)
                    # Calcular todas as células automatizadas e fazer update pra cada célula
                    self.CalcularCelsAutomatizadas(TableNameBruto)
                    self.CalcularCelsAutomatizadas(TableNameDT)
            elif self.HMI.BolsaOuCripto == "Cripto":
                TableName = str('OPs'+
                                '¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                                '¨'+self.HMI.BolsaOuCripto)
                TableNameBruto = TableName+'¨Bruto'
                TableNameRefinado = TableName+'¨Refinado'
                data = self.HMI.Selecao_Dia+"/"+self.HMI.Selecao_Mes+"/"+self.HMI.Selecao_Ano+" "+self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo
                data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')

                if ThereIsAnotherOPWithTheSameDate(TableName, data): return False
                if data > datetime.now(): return False

                Taxa = 0; MoedaDaTaxa = self.GetUserCoinCurrency(); Conversao = 1

                if len(self.HMI.TextBox_Taxa.text())>0: Taxa = round(float(self.HMI.TextBox_Taxa.text()),8)
                if len(self.HMI.TextBox_MoedaDaTaxa.text())>0: MoedaDaTaxa = self.HMI.TextBox_MoedaDaTaxa.text()
                if len(self.HMI.TextBox_Conversao.text())>0: Conversao = round(float(self.HMI.TextBox_Conversao.text()),8)

                self.AddRowInCurrentDB(TableNameBruto, [('Observação', self.HMI.TextBox_Obs.text() if not self.HMI.TextBox_Obs.text() == '' else " "),
                                                        ('Data', data),
                                                        ('Tipo', self.HMI.TipoDeOperacao),
                                                        ('ParEsquerdo', self.HMI.TextBox_Par_Esquerda.text()),
                                                        ('ParDireito', self.HMI.TextBox_Par_Direita.text()),
                                                        ('Preço', round(float(self.HMI.TextBox_Preco.text()),8)),
                                                        ('Qqt', round(float(self.HMI.TextBox_Qqt.text()),8)),
                                                        ('Taxa', Taxa),
                                                        ('MoedaDaTaxa', MoedaDaTaxa),
                                                        ('Conversão', Conversao)])
                self.CalcularCelsAutomatizadas_CriptoRefinado(TableName)
                self.UpdateContaCorrente_Cripto()

                # Verificar se os dois ativos estão na Cotações. Se não estiverem, coloque e atualize a cotação se for encontrado online.
                def AtivoExisteNaTabelaDeCotacoes(ativo):
                    Table, cursor = self.GetDataDB("SELECT * FROM Cotações")
                    aux = list(filter(lambda x: x[2]==ativo, Table))
                    if len(aux)>0:
                        return True
                    return False

                ativo = self.HMI.TextBox_Par_Esquerda.text()
                if not AtivoExisteNaTabelaDeCotacoes(ativo):
                    Cotacao = 0.
                    Modo = "Manual"
                    try:
                        Cotacao = self.HMI.YahooFinance.GetCotacaoCripto(ativo, self.GetUserCoinCurrency())
                        if Cotacao > 0: Modo = "Auto"
                    except:pass
                    self.AddRowInCurrentDB('Cotações', [('Modo', Modo),
                                                        ('DataDeAtualização', datetime.strptime(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")),
                                                        ('Ativo', ativo),
                                                        ('Cotação', Cotacao)])
                ativo = self.HMI.TextBox_Par_Direita.text()
                if not AtivoExisteNaTabelaDeCotacoes(ativo) and not ativo == "":
                    Cotacao = 0.
                    Modo = "Manual"
                    try:
                        Cotacao = self.HMI.YahooFinance.GetCotacaoCripto(ativo, self.GetUserCoinCurrency())
                        if Cotacao > 0: Modo = "Auto"
                    except:pass
                    self.AddRowInCurrentDB('Cotações', [('Modo', Modo),
                                                        ('DataDeAtualização', datetime.strptime(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")),
                                                        ('Ativo', ativo),
                                                        ('Cotação', Cotacao)])
        except Exception as e:pass
        finally:
            # Calcular a tributação devida de ST e de DT
            self.CalcularTributacao()
            self.UpdatePatrimonioRendimento()
            return True

    def AddTipoDeAtivo(self): # Eu uso isso ainda?
        # Adicionar linha nova
        TipoDeAtivo = self.HMI.TextBox_NovoTipoDeAtivo.text()
        self.AddRowInCurrentDB('TiposDeAtivos', [('TiposDeAtivos', TipoDeAtivo)])

    def AddSubtipoDeAtivo(self): # Eu uso isso ainda?
        # Adicionar linha nova: (Tipo de ativo, Subtipo de Ativo)
        TipoDeAtivo = self.HMI.ComboBox_TipoDeAtivo.currentText()
        SubtipoDeAtivo =self.HMI.TextBox_NovoSubtipoDeAtivo.text()
        self.AddRowInCurrentDB('SubtipoDeAtivos', [('TiposDeAtivos', TipoDeAtivo),('SubtiposDeAtivos', SubtipoDeAtivo)])

    def AddSetor(self): # Eu uso isso ainda?
        # Adicionar linha nova
        Setor = self.HMI.TextBox_NovoSetor.text()
        self.AddRowInCurrentDB('Setores', [('Setor', Setor)])

    def AddDepositoOuSaque(self, Data, Valor):
        # Verificar se já tem movimentação nessa data. Se sim, return False
        def ThereIsAnotherOPWithTheSameDate(TableName, data):
            Table, cursor = self.GetDataDB("SELECT rowid, * FROM "+TableName)
            aux = list(filter(lambda x: datetime.strptime(x[1],"%Y-%m-%d %H:%M:%S") == data, Table))
            if len(aux)>0: return True
            return False
        corretora = self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")
        if ThereIsAnotherOPWithTheSameDate("¨"+corretora+"¨"+self.HMI.BolsaOuCripto+"¨DepSaq", Data):
            return False
        # Adicionar linha nova: (Data, Valor)
        self.AddRowInCurrentDB("¨"+corretora+"¨"+self.HMI.BolsaOuCripto+"¨DepSaq", [('Data', Data),('Valor', Valor)])
        self.SortByDate("¨"+corretora+"¨"+self.HMI.BolsaOuCripto+"¨DepSaq")

        retorno, cursor = self.GetDataDB("SELECT * FROM ¨"+corretora+"¨"+self.HMI.BolsaOuCripto+"¨DepSaq")
        if len(retorno)==1: self.ModifyDB("VACUUM")
        self.UpdatePatrimonioRendimento()
        return True

#%% Updates

    def UpdateTaxa(self, TaxaB3Per):
        # Update TaxaB3Per em Table Perfil
        self.ModifyDB("UPDATE Perfil SET TaxaB3Per = (?)", [(TaxaB3Per)])


    def UpdateContaCorrente_Banco(self):
        def GetRowId(Banco):
            retorno, cursor = self.GetDataDB("SELECT rowid, * FROM Bancos")
            retorno = list(filter(lambda x: str(x).find("¨"+Banco+"¨")>-1, retorno))
            retorno = retorno[0][0]
            return str(retorno)
        # Update Conta Corrente em Table ContaCorrente_Corretora_BolsaOuCripto
        Valor = float(self.HMI.TextBox_CC.text())
        self.ModifyDB("UPDATE Bancos SET ContaCorrente = (?) Where rowid = "+GetRowId(self.HMI.ComboBox_Bancos.currentText().replace(" ","_")), [(Valor)])

        self.UpdatePatrimonioRendimento()

    def UpdateContaCorrente(self):
        def GetRowId(corretora):
            retorno, cursor = self.GetDataDB("SELECT rowid, * FROM Corretoras")
            retorno = list(filter(lambda x: str(x).find(corretora)>-1, retorno))
            retorno = retorno[0][0]
            return str(retorno)
        # Update Conta Corrente em Table ContaCorrente_Corretora_BolsaOuCripto
        Valor = float(self.HMI.TextBox_CCAtualizada.text())
        self.ModifyDB("UPDATE Corretoras SET ContaCorrente = (?) Where rowid = "+GetRowId(self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")), [(Valor)])
        self.UpdatePatrimonioRendimento()

    def UpdateContaCorrente_Cripto(self):
        def GetRowId(corretora):
            retorno, cursor = self.GetDataDB("SELECT rowid, * FROM Corretoras")
            retorno = list(filter(lambda x: str(x).find(corretora+"¨Cripto")>-1, retorno))
            retorno = retorno[0][0]
            return str(retorno)
        # Update Conta Corrente em Table ContaCorrente_Corretora_BolsaOuCripto
        corretora = self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")
        Valor = self.GetEstoque(ativo = self.GetUserCoinCurrency(), corretora = corretora, BolsaOuCripto = "Cripto")
        self.ModifyDB("UPDATE Corretoras SET ContaCorrente = (?) Where rowid = "+GetRowId(corretora), [(Valor)])

    def Update_GastoMensal(self, Valor):
        self.ModifyDB("UPDATE Perfil SET GastoMensal = (?)", [(Valor)])

    def Update_MesesDeReserva(self, Valor):
        self.ModifyDB("UPDATE Perfil SET MesesDeReserva = (?)", [(Valor)])

    def UpdateCotacao(self, ativo, Valor):
        def GetRowId(ativo):
            retorno, cursor = self.GetDataDB("SELECT rowid, * FROM Cotações")
            retorno2 = list(filter(lambda x: str(x).find(ativo)>-1, retorno))
            if len(retorno2)>0:
                RowId = retorno2[0][0]
            else:
                retorno2 = list(filter(lambda x: str(x).find(ativo+"-USD")>-1, retorno))
                if len(retorno2)>0:
                    RowId = retorno2[0][0]
                else:
                    RowId = -1
            return str(RowId)
        def AtivoIsStillInDB(ativo):
            retorno, cursor = self.GetDataDB("SELECT Ativo FROM Cotações Where Ativo = (?)",[(ativo)])
            if len(retorno)>0:
                return True
            return False
        # Update Cotação
        try:
            Data = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            ativo = ativo.replace(" ","_")
            if AtivoIsStillInDB(ativo): # Evita BUG quando threads diferentes mexem no mesmo ativo
                # Exemplo: Thread main deleta ativo da tabela enquanto thread de AtualizarCotações tenta update o valor do ativo que acabou de ser deletado: BUG
                self.ModifyDB("UPDATE Cotações SET Cotação = (?) Where Ativo = (?)", [(float(Valor)), ativo])
                self.ModifyDB("UPDATE Cotações SET DataDeAtualização = (?) Where Ativo = (?)", [(Data), ativo])

        except Exception as e:
            if self.HMI.BolsaOuCripto == "Cripto":
                self.AddRowInCurrentDB('Cotações', [('Modo', "Auto"),
                                                    ('DataDeAtualização', Data),
                                                    ('Ativo', ativo+"-USD"),
                                                    ('Cotação', Valor)])

#%% Renames
    def RenameAtivo(self):
        self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
        def GetRowId(Table,ativo):
            retorno, cursor = self.GetDataDB("SELECT rowid, * FROM "+Table)
            retorno = list(filter(lambda x: str(x).find(ativo)>-1, retorno))
            retorno = retorno[0][0]
            return str(retorno)
        # Alter all Tables e linhas que contêm "Ativo"
        try:
            NomeAntigo = self.HMI.ComboBox_Ativo.currentText().replace(" ","_")
            NomeNovo = self.HMI.TextBox_NovoNomeAtivo.text().replace(" ","_")
            ID = GetRowId('Bolsa',NomeAntigo)
            TipoDeAtivo = self.HMI.ComboBox_TipoDeAtivo.currentText()
            SubtipoDeAtivo = self.HMI.ComboBox_SubtipoDeAtivo.currentText()
            Setor = self.HMI.ComboBox_SetorAtivo.currentText()

            if not NomeAntigo == NomeNovo: self.ModifyDB("UPDATE Bolsa SET Ativo = (?) Where rowid = "+ID, [(NomeNovo)])
            self.ModifyDB("UPDATE Bolsa SET TipoDeAtivo = (?) Where rowid = "+ID, [(TipoDeAtivo)])
            self.ModifyDB("UPDATE Bolsa SET SubtipoDeAtivo = (?) Where rowid = "+ID, [(SubtipoDeAtivo)])
            self.ModifyDB("UPDATE Bolsa SET Setor = (?) Where rowid = "+ID, [(Setor)])

            # Update Table Cotações
            Modo = self.HMI.Modo
            if Modo == "Auto": NomeNovo = NomeNovo.upper()
            IDc = GetRowId('Cotações',NomeAntigo)
            DataDeAtualizacao = datetime.strptime(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")
            Cotacao = 0.
            if Modo == "Auto":
                try: Cotacao = self.HMI.YahooFinance.GetCotacao(NomeNovo, self.GetUserCoinCurrency())
                except:pass
            self.ModifyDB("UPDATE Cotações SET Modo = (?) Where rowid = "+IDc, [(Modo)])
            self.ModifyDB("UPDATE Cotações SET DataDeAtualização = (?) Where rowid = "+IDc, [(DataDeAtualizacao)])
            if not NomeAntigo == NomeNovo:
                self.ModifyDB("UPDATE Cotações SET Ativo = (?) Where rowid = "+IDc, [(NomeNovo)])
            self.ModifyDB("UPDATE Cotações SET Cotação = (?) Where rowid = "+IDc, [(Cotacao)])

            TableNameAntiga = str('OPs¨'+NomeAntigo+
                                '¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                                '¨'+self.HMI.BolsaOuCripto+
                                '¨Bruto')
            TableNameNova = str('OPs¨'+NomeNovo+
                                '¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                                '¨'+self.HMI.BolsaOuCripto+
                                '¨Bruto')
            if not NomeAntigo == NomeNovo: self.ModifyDB("ALTER TABLE "+TableNameAntiga+" RENAME TO "+TableNameNova)


            TableNameAntiga = str('OPs¨'+NomeAntigo+
                                '¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                                '¨'+self.HMI.BolsaOuCripto+
                                '¨DT')
            TableNameNova = str('OPs¨'+NomeNovo+
                                '¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                                '¨'+self.HMI.BolsaOuCripto+
                                '¨DT')
            if not NomeAntigo == NomeNovo: self.ModifyDB("ALTER TABLE "+TableNameAntiga+" RENAME TO "+TableNameNova)


            TableNameAntiga = str('OPs¨'+NomeAntigo+
                                '¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                                '¨'+self.HMI.BolsaOuCripto+
                                '¨ST')
            TableNameNova = str('OPs¨'+NomeNovo+
                                '¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                                '¨'+self.HMI.BolsaOuCripto+
                                '¨ST')
            if not NomeAntigo == NomeNovo: self.ModifyDB("ALTER TABLE "+TableNameAntiga+" RENAME TO "+TableNameNova)

            return True
        except: return False

    def RenameCorretora(self):
        self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
        def GetRowId(Table,corretora):
            retorno, cursor = self.GetDataDB("SELECT rowid, * FROM "+Table)
            retorno = list(filter(lambda x: str(x).find(corretora)>-1, retorno))
            retorno = retorno[0][0]
            return str(retorno)
        def CorretoraExists(corretora):
            retorno, cursor = self.GetDataDB("SELECT * FROM Corretoras")
            retorno = list(filter(lambda x: str(corretora+"¨"+self.HMI.BolsaOuCripto).lower() == str(x[0]).lower(), retorno))
            if len(retorno)>0: return True
            return False

        NewCorretoraName = self.HMI.TextBox_NovoNomeCorretora.text().replace(" ","_")
        OldCorretoraName = self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")

        if CorretoraExists(NewCorretoraName): return False
        # Alter all Tables e linhas que contêm "OldCorretoraName"
        # Update Corretora em Table Corretoras
        self.ModifyDB("UPDATE Corretoras SET Corretora = (?) Where rowid = "+GetRowId('Corretoras',OldCorretoraName), [(NewCorretoraName+"¨"+self.HMI.BolsaOuCripto)])
        # Alter all Tables que contêm "OPs_Ativo_Corretora_BolsaOuCripto"
        retorno, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        tables = list(map(lambda x: x[0],retorno))
        tables = list(filter(lambda x: x.find("¨"+OldCorretoraName+"¨")>-1,tables))
        for TableNameAntiga in tables:
            TableNameNova = TableNameAntiga.replace(OldCorretoraName, NewCorretoraName)
            self.ModifyDB("ALTER TABLE "+TableNameAntiga+" RENAME TO "+TableNameNova)
        return True

    def RenameBanco(self):
        def GetRowId(Table,Banco):
            retorno, cursor = self.GetDataDB("SELECT rowid, * FROM "+Table)
            retorno = list(filter(lambda x: str(x).find("¨"+Banco+"¨")>-1, retorno))
            retorno = retorno[0][0]
            return str(retorno)
        def BancoExists(Banco):
            retorno, cursor = self.GetDataDB("SELECT * FROM Bancos")
            retorno = list(filter(lambda x: str("¨"+Banco+"¨").lower() == str(x[0]).lower(), retorno))
            if len(retorno)>0: return True
            return False

        NewBancoName = self.HMI.TextBox_NovoNomeBanco.text().replace(" ","_")
        OldBancoName = self.HMI.ComboBox_Bancos.currentText().replace(" ","_")

        if BancoExists(NewBancoName): return False
        # Update Corretora em Table Corretoras
        self.ModifyDB("UPDATE Bancos SET Banco = (?) Where rowid = "+GetRowId('Bancos',OldBancoName), [("¨"+NewBancoName+"¨")])
        return True

#%% Alterações

    def AlterSetores(self, Setores):
        self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
        Table_Inicial, cursor = self.GetDataDB("SELECT * FROM Setores")
        Table_Inicial = list(map(lambda x: x[0],Table_Inicial))
        if not Table_Inicial == Setores:
            self.ModifyDB("DROP TABLE Setores")
            self.ModifyDB("VACUUM")
            # Create Table Setores
            self.CreateTableInCurrentDB('Setores', [('Setor', 'TEXT')])
            # Adicionar os Setores básicos
            for Setor in Setores:
                self.AddRowInCurrentDB('Setores', [('Setor', Setor)])
            return True
        return False

    def AlterOperacao(self, Item, Data, Tipo, Qqt, Preco, Corretagem, TaxaB3, TaxaB3Per, Obs):
        self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
        def ThereIsAnotherOPWithTheSameDate(TableName, data, rowid):
            data = datetime.strptime(data,"%Y/%m/%d %H:%M:%S")
            Table_Inicial, cursor = self.GetDataDB("SELECT rowid, * FROM "+TableName+"¨Bruto")
            aux = list(filter(lambda x: datetime.strptime(x[1],"%Y-%m-%d %H:%M:%S") == data and not rowid == x[0], Table_Inicial))
            if len(aux)>0: return True
            return False
        Item +=1
        ativo = self.HMI.ComboBox_Ativo.currentText().replace(" ","_")
        TableName = str('OPs¨'+ativo +
                        '¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                        '¨'+self.HMI.BolsaOuCripto)
        TableNameBruto = TableName+'¨Bruto'
        TableNameDT = TableName+'¨DT'
        TableNameST = TableName+'¨ST'

        # Verifica se tem outra operação nessa mesma data
        deuruim = ThereIsAnotherOPWithTheSameDate(TableName, Data, Item)
        if deuruim: return False
        if datetime.strptime(Data, '%Y/%m/%d %H:%M:%S') > datetime.now(): return False
        # Update linha em Table OPs_Ativo_Corretora_Bolsa_DT ou ST, DEPENDE da DATA.
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Data = (?) WHERE rowid = "+str(Item), [(datetime.strptime(Data, '%Y/%m/%d %H:%M:%S'))])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Tipo = (?) WHERE rowid = "+str(Item), [(Tipo)])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Qqt = (?) WHERE rowid = "+str(Item), [(int(Qqt))])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Preço = (?) WHERE rowid = "+str(Item), [(float(Preco))])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Corretagem = (?) WHERE rowid = "+str(Item), [(float(Corretagem))])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET TaxaB3 = (?) WHERE rowid = "+str(Item), [(float(TaxaB3))])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET TaxaB3Per = (?) WHERE rowid = "+str(Item), [(float(TaxaB3Per))])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Obs = (?) WHERE rowid = "+str(Item), [(Obs)])

        # Separar DT e ST se não for FII. Se for FII fazer só pra DT
        if not 'Fundos Imobiliários' == self.GetSubtipoDeAtivoDeAtivo(ativo):
            self.SepararDTeST(TableName, AcabouDeAdd = False)
            # Calcular todas as células automatizadas e fazer update pra cada célula
            self.CalcularCelsAutomatizadas(TableNameBruto)
            self.CalcularCelsAutomatizadas(TableNameDT)
            self.CalcularCelsAutomatizadas(TableNameST)
        else:
            self.CopiarBrutoPraDT(TableName)
            # Calcular todas as células automatizadas e fazer update pra cada célula
            self.CalcularCelsAutomatizadas(TableNameBruto)
            self.CalcularCelsAutomatizadas(TableNameDT)
        self.CalcularTributacao()
        self.UpdatePatrimonioRendimento()
        return True

    def AlterOperacao_Cripto(self, Item, Data, Tipo, ParEsquerdo, ParDireito, Qqt, Preco, Taxa, MoedaDaTaxa, Conversao, Obs):
        self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
        def ThereIsAnotherOPWithTheSameDate(TableName, data, rowid):
            data = datetime.strptime(data,"%Y/%m/%d %H:%M:%S")
            Table_Inicial, cursor = self.GetDataDB("SELECT rowid, * FROM "+TableName+"¨Bruto")
            aux = list(filter(lambda x: datetime.strptime(x[2],"%Y-%m-%d %H:%M:%S") == data and not rowid == x[0], Table_Inicial))
            if len(aux)>0: return True
            return False
        Item +=1
        TableName = str('OPs¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                        '¨'+self.HMI.BolsaOuCripto)
        TableNameBruto = TableName+'¨Bruto'

        # Verifica se tem outra operação nessa mesma data
        deuruim = ThereIsAnotherOPWithTheSameDate(TableName, Data, Item)
        if deuruim: return False
        if datetime.strptime(Data, '%Y/%m/%d %H:%M:%S') > datetime.now(): return False
        # Update linha em Table OPs_Ativo_Corretora_Bolsa_DT ou ST, DEPENDE da DATA.
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Data = (?) WHERE rowid = "+str(Item), [(datetime.strptime(Data, '%Y/%m/%d %H:%M:%S'))])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Tipo = (?) WHERE rowid = "+str(Item), [(Tipo)])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET ParEsquerdo = (?) WHERE rowid = "+str(Item), [(ParEsquerdo)])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET ParDireito = (?) WHERE rowid = "+str(Item), [(ParDireito)])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Qqt = (?) WHERE rowid = "+str(Item), [(float(Qqt))])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Preço = (?) WHERE rowid = "+str(Item), [(float(Preco))])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Taxa = (?) WHERE rowid = "+str(Item), [(float(Taxa))])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET MoedaDaTaxa = (?) WHERE rowid = "+str(Item), [(MoedaDaTaxa)])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Conversão = (?) WHERE rowid = "+str(Item), [(float(Conversao))])
        self.ModifyDB("UPDATE "+TableNameBruto+" SET Observação = (?) WHERE rowid = "+str(Item), [(Obs)])

        # Separar DT e ST se não for FII. Se for FII fazer só pra DT
        self.CalcularCelsAutomatizadas_CriptoRefinado(TableName)
        self.UpdateContaCorrente_Cripto()
        self.CalcularTributacao()
        self.UpdatePatrimonioRendimento()
        return True

#%% Deletes

    def DeleteBanco(self):
        try:
            Banco = self.HMI.ComboBox_Bancos.currentText().replace(" ","_")
            self.ModifyDB("DELETE FROM Bancos WHERE Banco = (?)",[(Banco)])
            self.ModifyDB("VACUUM")
        except:pass
        finally: self.UpdatePatrimonioRendimento()

    def DeleteCorretora(self):
        self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
        def GetRowId(corretora):
            retorno, cursor = self.GetDataDB("SELECT rowid, * FROM Corretoras")
            retorno = list(filter(lambda x: str(corretora+"¨"+self.HMI.BolsaOuCripto).lower() == str(x[1]).lower(), retorno))
            retorno = retorno[0][0]
            return retorno
        def GetRowId2(TableName, ativo):
            retorno, cursor = self.GetDataDB("SELECT rowid, * FROM "+TableName)
            retorno = list(filter(lambda x: str(x).find(ativo)>-1, retorno))
            retorno = retorno[0][0]
            return retorno
        # Delete corretora em Table Corretoras, Cotações, Bolsa, vacuum e todas as tabelas que contêm tal corretora no nome
        try:
            BolsaOuCripto = self.HMI.BolsaOuCripto
            corretora = self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")
            rowid = GetRowId(corretora)
            self.ModifyDB("DELETE FROM Corretoras WHERE rowid = "+str(rowid))
            self.ModifyDB("VACUUM")

            # Delete all Tables que contêm "Corretora_BolsaOuCripto"
            retorno, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
            AllTables = list(map(lambda x: x[0],retorno))
            Tables = list(filter(lambda x: x.find("¨"+corretora+"¨"+BolsaOuCripto)>-1,AllTables))
            AtivosDeletados = list(filter(lambda x: x.find("OPs¨")>-1 and x.find("¨Bolsa¨Bruto")>-1,Tables))
            AtivosDeletados = list(map(lambda x: x.replace("¨"+corretora+"¨"+BolsaOuCripto+"¨Bruto","").replace("OPs¨",""),AtivosDeletados))
            for table in Tables:
                self.ModifyDB("DROP TABLE "+table)

            retorno, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
            AllTables = list(map(lambda x: x[0],retorno))
            for ativo in AtivosDeletados:
                if not ativo in AllTables:
                    self.ModifyDB("DELETE FROM Bolsa WHERE Ativo = (?)",[(ativo)])
                    self.ModifyDB("VACUUM")
                    self.ModifyDB("DELETE FROM Cotações WHERE Ativo = (?)",[(ativo)])
                    self.ModifyDB("VACUUM")
        except:pass
        finally: self.UpdatePatrimonioRendimento()

    def DeleteOperacao(self, Items):
        self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
        if self.HMI.BolsaOuCripto == "Bolsa":
            # Delete linha
            Items = list(map(lambda x: len(self.HMI.HMI_Trades.HMI_Trades_Bolsa.data_23_1)-x,Items)) # Items = list(map(lambda x: x+1,Items)) # Debug: Para quando a tabela de registros é mostrada em ordem crescente
            ativo = self.HMI.ComboBox_Ativo.currentText().replace(" ","_")
            TableName = str('OPs¨'+
                        ativo +
                        '¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                        '¨'+self.HMI.BolsaOuCripto)
            TableNameBruto = TableName+'¨Bruto'
            TableNameDT = TableName+'¨DT'
            TableNameST = TableName+'¨ST'

            for Item in Items:
                self.ModifyDB("DELETE FROM "+TableNameBruto+" WHERE rowid = "+str(Item))

            # Verificar: Se Table vazia, DROP Table, senão: Vacuum
            retornoBruto, cursor = self.GetDataDB("SELECT * FROM "+TableNameBruto)
            if len(retornoBruto)>0:
                self.ModifyDB("VACUUM")
                # Separar DT e ST se não for FII. Se for FII fazer só pra DT
                if not 'Fundos Imobiliários' == self.GetSubtipoDeAtivoDeAtivo(ativo):
                    self.SepararDTeST(TableName, AcabouDeAdd = False)
                    # Calcular todas as células automatizadas e fazer update pra cada célula
                    self.CalcularCelsAutomatizadas(TableNameDT)
                    self.CalcularCelsAutomatizadas(TableNameST)
                else:
                    self.CopiarBrutoPraDT(ativo)
                    # Calcular todas as células automatizadas e fazer update pra cada célula
                    self.CalcularCelsAutomatizadas(TableNameDT)
                self.CalcularTributacao()
            else:
                self.ModifyDB("DROP TABLE "+TableNameBruto)
                self.ModifyDB("DROP TABLE "+TableNameST)
                self.ModifyDB("DROP TABLE "+TableNameDT)
                retorno, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
                ativos = list(map(lambda x: x[0],retorno))
                ativos = list(filter(lambda x: x.find(ativo)>-1,ativos))
                if not len(ativos)>0:
                    self.ModifyDB("DELETE FROM Bolsa WHERE Ativo = (?)",[(ativo)])
                    self.ModifyDB("VACUUM")
                    self.ModifyDB("DELETE FROM Cotações WHERE Ativo = (?)",[(ativo)])
                    self.ModifyDB("VACUUM")

        elif self.HMI.BolsaOuCripto == "Cripto":
            # Delete linha
            Items = list(map(lambda x: len(self.HMI.HMI_Trades.HMI_Trades_Criptomoedas.data_40_1)-x,Items)) # Items = list(map(lambda x: x+1,Items)) # Debug: Para quando a tabela de registros é mostrada em ordem crescente
            TableName = str('OPs¨'+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+
                            '¨'+self.HMI.BolsaOuCripto)
            TableNameBruto = TableName+'¨Bruto'
            TableNameRefinado = TableName+'¨Refinado'

            for Item in Items:
                self.ModifyDB("DELETE FROM "+TableNameBruto+" WHERE rowid = "+str(Item))

            # Verificar: Se Table não vazia: Vacuum
            retornoBruto, cursor = self.GetDataDB("SELECT * FROM "+TableNameBruto)
            if len(retornoBruto)>0: self.ModifyDB("VACUUM")
            self.CalcularCelsAutomatizadas_CriptoRefinado(TableName)
            self.UpdateContaCorrente_Cripto()
            self.CalcularTributacao()
        self.UpdatePatrimonioRendimento()

    def DeleteDepositoOuSaque(self, Items):
        # Delete linha
        Items = list(map(lambda x: len(self.HMI.HMI_Trades.HMI_Trades_Bolsa.data_24_1)-x,Items)) # Items = list(map(lambda x: x+1,Items)) # Debug: Para quando a tabela de registros é mostrada em ordem crescente
        TableName = "¨"+self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")+'¨'+self.HMI.BolsaOuCripto+"¨DepSaq"

        Table, cursor = self.GetDataDB("SELECT * FROM "+TableName)
        for Item in Items: self.ModifyDB("DELETE FROM "+TableName+" WHERE rowid = "+str(Item))
        # Se Table com conteúdo: Vacuum
        retorno, cursor = self.GetDataDB("SELECT * FROM "+TableName)
        if len(retorno)>0: self.ModifyDB("VACUUM")
        self.UpdatePatrimonioRendimento()

#%% Gets

    def GetBancos(self):
        retorno, cursor = self.GetDataDB("SELECT * FROM Bancos")
        bancos = list(map(lambda x: x[0], retorno))
        bancos = list(map(lambda x: x[0].replace("_"," "), retorno))
        bancos = list(map(lambda x: x[0].replace("¨",""), retorno))
        return bancos

    def GetAllCorretoras(self):
        retorno, cursor = self.GetDataDB("SELECT * FROM Corretoras")
        corretoras = list(map(lambda x: x[0], retorno))
        corretoras = list(filter(lambda x: "¨Bolsa" in x or "¨Cripto" in x, corretoras))
        corretoras = list(map(lambda Broker: Broker.replace("¨Bolsa",""), corretoras))
        corretoras = list(map(lambda Broker: Broker.replace("¨Cripto",""), corretoras))
        return corretoras

    def GetAllCorretoras_ComBolsaOuCripto(self):
        retorno, cursor = self.GetDataDB("SELECT * FROM Corretoras")
        corretoras = list(map(lambda x: x[0], retorno))
        corretorasBolsa = list(filter(lambda Broker: "¨Bolsa" in Broker, corretoras))
        corretorasCripto = list(filter(lambda Broker: "¨Cripto" in Broker, corretoras))
        return corretorasBolsa, corretorasCripto

    def GetCorretoras(self, BolsaOuCripto=''):
        if not len(BolsaOuCripto)>0: BolsaOuCripto = self.HMI.BolsaOuCripto
        retorno, cursor = self.GetDataDB("SELECT * FROM Corretoras")
        corretoras = list(map(lambda x: x[0], retorno))
        if BolsaOuCripto == "Bolsa":
            corretoras = list(filter(lambda x: "¨Bolsa" in x, corretoras))
            corretoras = list(map(lambda Broker: Broker.replace("¨Bolsa",""), corretoras))
        else:
            corretoras = list(filter(lambda x: "¨Cripto" in x, corretoras))
            corretoras = list(map(lambda Broker: Broker.replace("¨Cripto",""), corretoras))
        corretoras = list(map(lambda x: x.replace("_"," "), corretoras))
        return corretoras

    def GetAtivos(self, corretora = '', BolsaOuCripto = ''):
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        if not len(BolsaOuCripto)>0: BolsaOuCripto = self.HMI.BolsaOuCripto
        ativos = []

        if BolsaOuCripto == "Bolsa":
            tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
            tabelas = list(map(lambda x: x[0], tabelas))
            tabelas = list(filter(lambda x: x.find("¨"+corretora+'¨'+BolsaOuCripto)>-1, tabelas))
            ativos = list(filter(lambda x: not "¨ST" in x, tabelas))
            ativos = list(filter(lambda x: not "¨DT" in x, ativos))
            ativos = list(filter(lambda x: not "¨DepSaq" in x, ativos))
            ativos = list(map(lambda x: x.replace('¨'+corretora+'¨'+BolsaOuCripto+'¨Bruto',''), ativos))
            ativos = list(map(lambda x: x.replace('OPs¨',''), ativos))

        elif BolsaOuCripto == "Cripto":
            try:
                if len(corretora)>0:
                    TableName = "OPs¨"+corretora+"¨Cripto¨Refinado"
                    retorno, cursor = self.GetDataDB("SELECT * FROM "+TableName)
                    headers = list(map(lambda x: x[0], cursor.description))[13:]
                    for idx, head in enumerate(headers):
                        if (idx+1) % 5 == 0:
                            ativos.append(head.replace("PreçoMédioDe¨",""))
                else:
                    ativos = []
            except: ativos = []
        ativos = list(map(lambda x: x.replace("_"," "), ativos))
        return ativos

    def GetTiposDeAtivo(self):
        retorno, cursor = self.GetDataDB("SELECT * FROM TiposDeAtivo")
        TiposDeATivo = list(map(lambda x: x[0], retorno))
        return TiposDeATivo

    def GetSubtiposDeAtivo(self, TipoDeAtivo = ''):
        if not len(TipoDeAtivo)>0: TipoDeAtivo = self.HMI.ComboBox_TipoDeAtivo.currentText()
        retorno, cursor = self.GetDataDB("SELECT * FROM SubtiposDeAtivo")
        retorno = list(filter(lambda x: str(x).find(TipoDeAtivo)>-1, retorno))
        subtipos = list(map(lambda x: x[1], retorno))
        return subtipos

    def GetSetoresDeAtivo(self):
        retorno, cursor = self.GetDataDB("SELECT * FROM Setores")
        Setores = list(map(lambda x: x[0], retorno))
        return Setores

    def GetSetorDeAtivo(self, ativo):
        retorno, cursor = self.GetDataDB("SELECT * FROM Bolsa")
        Setor = ''
        if len(retorno)>0:
            Setor = list(filter(lambda x: str(x).find(ativo)>-1, retorno))
            if len(Setor) > 0: Setor = Setor[0][3]
            else: Setor = ''
        return Setor

    def GetTipoDeAtivoDeAtivo(self, ativo):
        retorno, cursor = self.GetDataDB("SELECT * FROM Bolsa")
        TipoDeAtivo = ''
        if len(retorno)>0:
            TipoDeAtivo = list(filter(lambda x: str(x).find(ativo)>-1, retorno))
            if len(TipoDeAtivo) > 0: TipoDeAtivo = TipoDeAtivo[0][1]
            else: TipoDeAtivo = ''
        return TipoDeAtivo

    def GetSubtipoDeAtivoDeAtivo(self, ativo):
        retorno, cursor = self.GetDataDB("SELECT * FROM Bolsa")
        SubtipoDeAtivo = ''
        if len(retorno)>0:
            SubtipoDeAtivo = list(filter(lambda x: str(x).find(ativo)>-1, retorno))
            if len(SubtipoDeAtivo) > 0: SubtipoDeAtivo = SubtipoDeAtivo[0][2]
            else: SubtipoDeAtivo = ''
        return SubtipoDeAtivo

    def GetCustosDasOperacoes(self, ativo = '', corretora = '', BolsaOuCripto = ''):
        CustoDaOperacao = 0
        if not len(ativo)>0: ativo = self.HMI.ComboBox_Ativo.currentText().replace(" ","_")
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        if not len(BolsaOuCripto)>0: BolsaOuCripto = self.HMI.BolsaOuCripto

        if BolsaOuCripto == "Bolsa":
            if len(ativo)>0:
                try:
                    retorno, cursor = self.GetDataDB("SELECT * FROM OPs¨"+ativo+"¨"+corretora+"¨"+BolsaOuCripto+"¨Bruto")
                    Corretagem = retorno[-1][4]
                    TaxaB3 = retorno[-1][6]
                    CustoDaOperacao = Corretagem + TaxaB3
                    if CustoDaOperacao == "NULL":
                        CustoDaOperacao = 0
                except: CustoDaOperacao = 0
        return CustoDaOperacao

    def GetCustoDeOperacao(self, idx_operação = -1, ativo = '', corretora = '', BolsaOuCripto = ''): # Alguém vai precisar disso?
        CustoDaOperacao = 0
        if BolsaOuCripto == "Cripto":
            TableName = "OPs¨"+corretora+"¨Cripto¨Refinado"
            retorno, cursor = self.GetDataDB("SELECT * FROM "+TableName)
            # (O custo da operação é a taxa em currency) Pra saber a taxa da operação em currency, deve-se:
                # 1) pego o valor da taxa
                # 2) pego a moeda da taxa
                # 3) acho o preço médio da operação da moeda da taxa
                # 4) taxa em currency = valor da taxa * preço médio da moeda da taxa
            ValorDaTaxa = retorno[idx_operação][8]
            MoedaDaTaxa = retorno[idx_operação][9]
            headers = list(map(lambda x: x[0], cursor.description))
            idxCol_PM_MoedaDaTaxa = headers.index("PreçoMédioDe¨"+ativo)
            PrecoMedioDaMoedaDaTaxa = retorno[idx_operação][idxCol_PM_MoedaDaTaxa]
            CustoDaOperacao = ValorDaTaxa * PrecoMedioDaMoedaDaTaxa
        return CustoDaOperacao

    def GetEstoque(self, ativo = '', corretora = '', BolsaOuCripto = ''):
        estoqueST = 0.
        estoqueDT = 0.
        estoque = 0.
        if not len(ativo)>0: ativo = self.HMI.ComboBox_Ativo.currentText().replace(" ","_")
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        if not len(BolsaOuCripto)>0: BolsaOuCripto = self.HMI.BolsaOuCripto

        if BolsaOuCripto == "Bolsa":
            if len(ativo)>0 and len(corretora)>0:
                try:
                    retorno, cursor = self.GetDataDB("SELECT * FROM OPs¨"+ativo+"¨"+corretora+"¨"+BolsaOuCripto+"¨ST")
                    estoqueST = retorno[-1][8]
                    if estoqueST == "NULL":
                        estoqueST = 0.
                except: estoqueST = 0.
                try:
                    retorno, cursor = self.GetDataDB("SELECT * FROM OPs¨"+ativo+"¨"+corretora+"¨"+BolsaOuCripto+"¨DT")
                    estoqueDT = retorno[-1][8]
                    if estoqueDT == "NULL":
                        estoqueDT = 0.
                except: estoqueDT = 0.
            estoque = int(estoqueST) + int(estoqueDT)

        elif BolsaOuCripto == "Cripto":
            try:
                TableName = "OPs¨"+corretora+"¨Cripto¨Refinado"
                retorno, cursor = self.GetDataDB("SELECT * FROM "+TableName)
                headers = list(map(lambda x: x[0], cursor.description))
                column = headers.index("EstoqueDe¨"+ativo)
                estoque = retorno[-1][column]
            except:pass
        return round(float(estoque), 8)

    def GetAllOperacoes(self, DTeST = '', ativo = ''):
        BolsaOuCripto = self.HMI.BolsaOuCripto
        corretora = self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")
        if self.HMI.BolsaOuCripto == "Bolsa":
            try:
                if not len(ativo)>0: ativo = self.HMI.ComboBox_Ativo.currentText().replace(" ","_")
                if len(ativo)>0:
                    if DTeST == "":
                        retornoAux, cursor = self.GetDataDB("SELECT * FROM OPs¨"+ativo+"¨"+corretora+"¨"+BolsaOuCripto+"¨Bruto")
                        retorno = []
                        for row in retornoAux: retorno.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
                    elif DTeST == "DTeST":
                        retornoAux, cursor = self.GetDataDB("SELECT * FROM OPs¨"+ativo+"¨"+corretora+"¨"+BolsaOuCripto+"¨ST")
                        retorno = []
                        for row in retornoAux: retorno.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],"ST; "+row[7]))
                        retornoAux, cursor = self.GetDataDB("SELECT * FROM OPs¨"+ativo+"¨"+corretora+"¨"+BolsaOuCripto+"¨DT")
                        for row in retornoAux: retorno.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],"DT; "+row[7]))
                    elif DTeST == "DT":
                        retornoAux, cursor = self.GetDataDB("SELECT * FROM OPs¨"+ativo+"¨"+corretora+"¨"+BolsaOuCripto+"¨DT")
                        retorno = []
                        for row in retornoAux: retorno.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
                    elif DTeST == "ST":
                        retornoAux, cursor = self.GetDataDB("SELECT * FROM OPs¨"+ativo+"¨"+corretora+"¨"+BolsaOuCripto+"¨ST")
                        retorno = []
                        for row in retornoAux: retorno.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
                    if not len(retorno)>0: retorno = [('00-00-0000 00:00:00','VAZIO','0','0','0','0','0',' ')]
                else: retorno = [('00-00-0000 00:00:00','VAZIO','0','0','0','0','0',' ')]
                return retorno
            except:
                return [('00-00-0000 00:00:00','VAZIO','0','0','0','0','0',' ')]

        elif self.HMI.BolsaOuCripto == "Cripto":
            try:
                if len(corretora)>0:
                    if DTeST == "":
                        retornoAux, cursor = self.GetDataDB("SELECT * FROM OPs¨"+corretora+"¨"+BolsaOuCripto+"¨Bruto")
                        retorno = []
                        for row in retornoAux:
                            retorno.append((row[1], # Data
                                            row[3]+"/"+row[4] if not row[4] == '' else row[3], # Par
                                            row[2], # Tipo
                                            row[5], # Preço
                                            row[6], # Quantidade
                                            row[7], # Taxa
                                            row[8], # Moeda da taxa
                                            row[9], # Conversão
                                            row[0])) # Observação
                    elif DTeST == "DTeST":
                        retornoAux, cursor = self.GetDataDB("SELECT * FROM OPs¨"+corretora+"¨"+BolsaOuCripto+"¨DT")
                        retorno = []
                        for row in retornoAux:
                            retorno.append((row[2], # Data
                                            row[4]+"/"+row[5], # Par
                                            row[3], # Tipo
                                            row[6], # Preço
                                            row[7], # Quantidade
                                            row[8], # Taxa
                                            row[9], # Moeda da taxa
                                            row[10], # Conversão
                                            "DT; "+row[0])) # Observação
                        retornoAux, cursor = self.GetDataDB("SELECT * FROM OPs¨"+corretora+"¨"+BolsaOuCripto+"¨ST")
                        retorno = []
                        for row in retornoAux:
                            retorno.append((row[2], # Data
                                            row[4]+"/"+row[5], # Par
                                            row[3], # Tipo
                                            row[6], # Preço
                                            row[7], # Quantidade
                                            row[8], # Taxa
                                            row[9], # Moeda da taxa
                                            row[10], # Conversão
                                            "ST; "+row[0])) # Observação
                    elif DTeST == "DT":
                        retornoAux, cursor = self.GetDataDB("SELECT * FROM OPs¨"+corretora+"¨"+BolsaOuCripto+"¨DT")
                        retorno = []
                        for row in retornoAux:
                            retorno.append((row[2], # Data
                                            row[4]+"/"+row[5], # Par
                                            row[3], # Tipo
                                            row[6], # Preço
                                            row[7], # Quantidade
                                            row[8], # Taxa
                                            row[9], # Moeda da taxa
                                            row[10], # Conversão
                                            row[0])) # Observação
                    elif DTeST == "ST":
                        retornoAux, cursor = self.GetDataDB("SELECT * FROM OPs¨"+corretora+"¨"+BolsaOuCripto+"¨ST")
                        retorno = []
                        for row in retornoAux:
                            retorno.append((row[2], # Data
                                            row[4]+"/"+row[5], # Par
                                            row[3], # Tipo
                                            row[6], # Preço
                                            row[7], # Quantidade
                                            row[8], # Taxa
                                            row[9], # Moeda da taxa
                                            row[10], # Conversão
                                            row[0])) # Observação
                    if not len(retorno)>0: retorno = [('00-00-0000 00:00:00','VAZIO','VAZIO','0','0','0','VAZIO','0',' ')]
                else:
                    retorno = [('00-00-0000 00:00:00','VAZIO','VAZIO','0','0','0','VAZIO','0',' ')]
                return retorno
            except Exception as e: return [('00-00-0000 00:00:00','erro','VAZIO','0','0','0','VAZIO','0',' ')]

    def GetImpostoDevidoDeDTUltimoMes(self):
        retorno = []
        aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoDTBolsa") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
        if len(aux) > 0: retorno.append(aux[-1][-2])
        aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoDTCripto") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
        if len(aux) > 0: retorno.append(aux[-1][-2])
        if len(retorno) > 0: return sum(retorno)
        else: return 0

    def GetResultadoLiquidoUltimoMes(self):
        retorno = []
        aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoSTBolsa") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
        if len(aux) > 0: retorno.append(aux[-1][-1])
        aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoSTCripto") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
        if len(aux) > 0: retorno.append(aux[-1][-1])
        aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoDTBolsa") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
        if len(aux) > 0: retorno.append(aux[-1][-1])
        aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoDTCripto") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
        if len(aux) > 0: retorno.append(aux[-1][-1])
        if len(retorno) > 0: return sum(retorno)
        else: return 0

    def GetResultadoGeralLiquido(self):
        retorno = []
        aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoSTBolsa") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
        if len(aux) > 0:
            for row in aux:
                retorno.append(row[1])
                retorno.append(-row[6])

        aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoSTCripto") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
        if len(aux) > 0:
            for row in aux:
                retorno.append(row[1])
                retorno.append(-row[6])

        aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoDTBolsa") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
        if len(aux) > 0:
            for row in aux:
                retorno.append(row[1])
                retorno.append(-row[6])

        aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoDTCripto") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
        if len(aux) > 0:
            for row in aux:
                retorno.append(row[1])
                retorno.append(-row[6])

        if len(retorno) > 0:
            return round(sum(retorno),2)
        else:
            return 0

    def GetMoedasFiat(self):
        MoedasFiat = []
        retorno, cursor = self.GetDataDB("SELECT * FROM MoedasFiat")
        MoedasFiat = list(map(lambda x: x[0], retorno))
        return MoedasFiat

    def GetAllTributacoes(self):
        retorno = []
        if 'ST' in self.HMI.DTeST_51:
            if 'B3' in self.HMI.CriptoeB3_51:
                aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoSTBolsa") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
                if len(aux) > 0:
                    if not self.HMI.DTeST_51 == "DTeST": # Tamanho 8: 'Mês/Ano', 'Resultado líquido', 'Imposto devido', 'Alíquota', 'Lucro mínimo taxável', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final'
                        aux2 = []
                        for row in aux: aux2.append((row[0],row[7],row[6],row[4],row[5],row[1],row[2],row[3]))
                    else: # Tamanho 6: 'Mês/Ano', 'Resultado líquido', 'Imposto devido', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final'
                        aux2 = []
                        for row in aux: aux2.append((row[0],row[7],row[6],row[1],row[2],row[3]))
                    retorno.append(aux2)
            if 'Cripto' in self.HMI.CriptoeB3_51:
                aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoSTCripto") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
                if len(aux) > 0:
                    if not self.HMI.DTeST_51 == "DTeST": # Tamanho 8: 'Mês/Ano', 'Resultado líquido', 'Imposto devido', 'Alíquota', 'Lucro mínimo taxável', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final'
                        aux2 = []
                        for row in aux: aux2.append((row[0],row[7],row[6],row[4],row[5],row[1],row[2],row[3]))
                    else: # Tamanho 6: 'Mês/Ano', 'Resultado líquido', 'Imposto devido', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final'
                        aux2 = []
                        for row in aux: aux2.append((row[0],row[7],row[6],row[1],row[2],row[3]))
                    retorno.append(aux2)
        if 'DT' in self.HMI.DTeST_51:
            if 'B3' in self.HMI.CriptoeB3_51:
                aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoDTBolsa") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
                if len(aux) > 0:
                    if not self.HMI.DTeST_51 == "DTeST": # Tamanho 8: 'Mês/Ano', 'Resultado líquido', 'Imposto devido', 'Alíquota', 'Lucro mínimo taxável', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final'
                        aux2 = []
                        for row in aux: aux2.append((row[0],row[7],row[6],row[4],row[5],row[1],row[2],row[3]))
                    else: # Tamanho 6: 'Mês/Ano', 'Resultado líquido', 'Imposto devido', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final'
                        aux2 = []
                        for row in aux: aux2.append((row[0],row[7],row[6],row[1],row[2],row[3]))
                    retorno.append(aux2)
            if 'Cripto' in self.HMI.CriptoeB3_51:
                aux, cursor = self.GetDataDB("SELECT * FROM TributaçãoDTCripto") # 'Mês/Ano', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final', 'Alíquota', 'Lucro mínimo taxável', 'Imposto devido', 'Resultado líquido'
                if len(aux) > 0:
                    if not self.HMI.DTeST_51 == "DTeST": # Tamanho 8: 'Mês/Ano', 'Resultado líquido', 'Imposto devido', 'Alíquota', 'Lucro mínimo taxável', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final'
                        aux2 = []
                        for row in aux: aux2.append((row[0],row[7],row[6],row[4],row[5],row[1],row[2],row[3]))
                    else: # Tamanho 6: 'Mês/Ano', 'Resultado líquido', 'Imposto devido', 'Resultado bruto', 'Prejuízo acumulado', 'Resultado final'
                        aux2 = []
                        for row in aux: aux2.append((row[0],row[7],row[6],row[1],row[2],row[3]))
                    retorno.append(aux2)
        if len(retorno) > 0:
            retornoAux = retorno
            retorno = retornoAux[0]
            # Somar as colunas das linhas que têm o mesmo indice
            for i, table in enumerate(retornoAux):
                if i == 0:pass
                else:
                    if len(table[0]) == 8:
                        for j, row in enumerate(table):
                            C0 = retorno[j][0]
                            C1 = retorno[j][1] + row[1]
                            C2 = retorno[j][2] + row[2]
                            C3 = retorno[j][3]
                            C4 = retorno[j][4]
                            C5 = retorno[j][5] + row[5]
                            C6 = retorno[j][6] + row[6]
                            C7 = retorno[j][7] + row[7]
                            retorno[j] = (C0,C1,C2,C3,C4,C5,C6,C7)
                    elif len(table[0]) == 6:
                        for j, row in enumerate(table):
                            C0 = retorno[j][0]
                            C1 = retorno[j][1] + row[1]
                            C2 = retorno[j][2] + row[2]
                            C3 = retorno[j][3] + row[3]
                            C4 = retorno[j][4] + row[4]
                            C5 = retorno[j][5] + row[5]
                            retorno[j] = (C0,C1,C2,C3,C4,C5)
            return retorno
        else:
            if not self.HMI.DTeST_51 == "DTeST": # Tamanho 8
                return [(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),0,0,0,0,0,0,0)]
            return [(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),0,0,0,0,0)] # Tamanho 6

    def GetModoCotacao(self, ativo = ''):
        if not len(ativo)>0: ativo = self.HMI.ComboBox_Ativo.currentText().replace(" ","_")
        Modo = 'Manual'
        try:
            ativo = ativo.replace(" ","_")
            retorno, cursor = self.GetDataDB("SELECT Modo FROM Cotações WHERE Ativo = (?)",[(ativo)])
            Modo = retorno[0][0]
        except:pass
        finally: return Modo

    def GetUserCoinCurrency(self):
        if not self.HMI.LoggedIn: return ''
        retorno, cursor = self.GetDataDB("SELECT MoedaCorrente FROM Perfil")
        MoedaCorrente = retorno[0][0]
        return MoedaCorrente

    def GetCorretoraCoinCurrency(self, corretora = ''):
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()+"¨"+self.HMI.BolsaOuCripto
        corretora = corretora.replace(" ","_")
        retorno, cursor = self.GetDataDB("SELECT * FROM Corretoras WHERE Corretora = (?)",[(corretora)])
        MoedaCorrente = ''
        for row in retorno:
            MoedaCorrente = str(row[1])
        return MoedaCorrente

    def GetBancoCoinCurrency(self, banco):
        banco = banco.replace(" ","_")
        MoedaCorrente = ''
        retorno, cursor = self.GetDataDB("SELECT MoedaCorrente FROM Bancos WHERE Banco = (?)",[("¨"+banco+"¨")])
        if len(retorno)>0: MoedaCorrente = retorno[0][0]
        return str(MoedaCorrente)

    def GetCotacao(self, ativo):
        ativo = ativo.replace(" ","_")
        cotacao = 0
        retorno, cursor = self.GetDataDB("SELECT Cotação FROM Cotações WHERE Ativo = (?)",[(ativo)])
        if len(retorno)>0: cotacao = retorno[0][0]
        if cotacao == 0.: cotacao = -1
        return cotacao

    def GetPatrimonioTotalCorretora(self, corretora = '', BolsaOuCripto = ''):
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        if not len(BolsaOuCripto)>0: BolsaOuCripto = self.HMI.BolsaOuCripto
        Patrimonio = 0.
        if BolsaOuCripto == "Bolsa":
            try:
                # Pegar valor em conta-corrente
                Patrimonio = float(self.GetValorEmContaCorrente(corretora, "Bolsa"))
                # Para cada ativo faça:
                # Pegar estoque, multiplicar pela cotação atual, somar ao resultado
                ativos = self.GetAtivos(corretora, BolsaOuCripto)
                for ativo in ativos:
                    Estoque = float(self.GetEstoque(ativo, corretora, BolsaOuCripto))
                    Cotacao = self.GetCotacao(ativo)
                    if not (Cotacao > 0. and Estoque >= 0.): return -1
                    Patrimonio += Estoque*Cotacao
                    Patrimonio -= self.GetCustosDasOperacoes(ativo, corretora, BolsaOuCripto)
            except: Patrimonio = -2

        elif BolsaOuCripto == "Cripto":
            try:
                ativos = self.GetAtivos(corretora, BolsaOuCripto)
                for ativo in ativos:
                    Estoque = float(self.GetEstoque(ativo, corretora, BolsaOuCripto))
                    Cotacao = self.GetCotacao(ativo)
                    if Cotacao == -1: return -1
                    Patrimonio += Estoque*Cotacao
            except: Patrimonio = -2
        return round(Patrimonio, 2)

    def GetTotalInvestidoEmCorretora(self, corretora = '', BolsaOuCripto = ''):
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        if not len(BolsaOuCripto)>0: BolsaOuCripto = self.HMI.BolsaOuCripto
        Investido = 0

        if BolsaOuCripto == "Bolsa":
            retorno, cursor = self.GetDataDB("SELECT * FROM ¨"+corretora+"¨"+BolsaOuCripto+"¨DepSaq")
            retorno = [x[1] for x in retorno]
            Investido = sum(retorno)
        elif BolsaOuCripto == "Cripto":
            retorno, cursor = self.GetDataDB("SELECT * FROM OPs¨"+corretora+"¨"+BolsaOuCripto+"¨Bruto")
            # Pegar o volume das OPs de Depósito
            depositos = list(filter(lambda x: x[2]=="Depósito", retorno))
            depositos = list(map(lambda x: x[9]*x[5]*x[6], depositos)) # Volume
            Investido = sum(depositos)
            saques = list(filter(lambda x: x[2]=="Saque", retorno))
            saques = list(map(lambda x: x[9]*x[5]*x[6], saques)) # Volume
            Investido -= sum(saques)
        return Investido

    def GetAllContasCorrente(self):
        corretorasBolsa, corretorasCripto = self.GetAllCorretoras_ComBolsaOuCripto()
        resposta = []
        self.SumContasCorrentes = 0
        for corretora in corretorasBolsa:
            corretora = corretora.replace("¨Bolsa","")
            valor = self.GetValorEmContaCorrente(corretora, "Bolsa")
            resposta.append((corretora, valor))
            self.SumContasCorrentes += valor
        for corretora in corretorasCripto:
            corretora = corretora.replace("¨Cripto","")
            valor = self.GetValorEmContaCorrente(corretora, "Cripto")
            resposta.append((corretora, valor))
            self.SumContasCorrentes += valor
        for banco in self.GetBancos():
            valor = self.GetValorEmContaCorrente_Banco(banco)
            resposta.append((banco, valor))
            self.SumContasCorrentes += valor
        return resposta

    def GetValorEmContaCorrente(self, corretora = '', BolsaOuCripto = ''):
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        valor = 0.

        retorno, cursor = self.GetDataDB("SELECT * FROM Corretoras")
        for row in retorno:
            if corretora+"¨"+BolsaOuCripto in row[0]: valor = float(row[2])
        return round(valor, 2)

    def GetValorEmContaCorrente_Banco(self, Banco):
        Banco = Banco.replace(" ","_")
        retorno, cursor = self.GetDataDB("SELECT * FROM Bancos")
        valor = 0.
        for row in retorno:
            if "¨"+Banco+"¨" in row[0]: valor = float(row[2])
        return round(valor, 2)

    def GetDataUltimaOPRegistrada(self, corretora = ''):
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        ativos = self.GetAtivos()
        folha = []
        for ativo in ativos: folha.append(self.GetAllOperacoes('', ativo))
        datas = []
        for OPs in folha:
            for OP in OPs: datas.append(OP[0])
        if len(datas)>0: return max(datas)
        else: return "Não há nenhum registro"

    def GetDepositosESaques(self, corretora = ''):
        valor = 0
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        if len(corretora)>0:
            retorno, cursor = self.GetDataDB("SELECT * FROM ¨"+corretora+"¨"+self.HMI.BolsaOuCripto+"¨DepSaq")
            if len(retorno)>0: return retorno[::-1]
        return [(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),0)]

    def GetUltimoDepositoOuSaqueRegistrado(self, corretora = ''):
        valor = 0
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        if len(corretora)>0:
            if self.HMI.BolsaOuCripto == "Bolsa":
                retorno, cursor = self.GetDataDB("SELECT * FROM ¨"+corretora+"¨"+self.HMI.BolsaOuCripto+"¨DepSaq")
                valor = 0
                for row in retorno:
                    valor = float(row[1])
            elif self.HMI.BolsaOuCripto == "Cripto":
                # Pegar último depósito feito da tabela
                retorno, cursor = self.GetDataDB("SELECT * FROM OPs¨"+corretora+"¨"+self.HMI.BolsaOuCripto+"¨Bruto")
                retorno = list(filter(lambda x: "Depósito" in x[2] or "Saque" in x[2], retorno))
                if len(retorno)>0:
                    Preco = retorno[-1][5]
                    Qqt = retorno[-1][6]
                    Conversão = retorno[-1][9]
                    CotacaoCurrency = Conversão * Preco
                    Volume = CotacaoCurrency * Qqt
                    valor = Volume
                    if retorno[-1][2] == "Saque": valor = -valor
        return valor

    def GetTaxaB3Per(self):
        corretora = self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")
        retorno, cursor = self.GetDataDB("SELECT TaxaB3Per FROM Perfil")
        retorno = retorno[0][0]
        return str(retorno)+'%'

    def GetCotacoesManuais(self):
        retorno, cursor = self.GetDataDB("SELECT * FROM Cotações WHERE Modo=(?)",[("Manual")])
        ativos = []
        datas = []
        cotacoes = []
        for row in retorno:
            datas.append(row[1])
            ativos.append(row[2].replace("_"," "))
            cotacoes.append(row[3])
        return ativos, datas, cotacoes

    def GetEmailByUser(self, User):
        Email = ""
        try:
            currdir = os.getcwd() # Get current directory
            conn = sqlite3.connect(currdir+'\\Users.db')
            retorno = list(conn.execute("SELECT * FROM Usuários WHERE Usuário = (?)",[(User)]))
            for row in retorno:
                Email = row[1]
        except:pass
        finally:
            conn.close()
            return Email

    def GetUserByEmail(self, Email):
        User = ""
        try:
            currdir = os.getcwd() # Get current directory
            conn = sqlite3.connect(currdir+'\\Users.db')
            retorno = list(conn.execute("SELECT * FROM Usuários WHERE Email = (?)",[(Email)]))
            for row in retorno:
                User = row[0]
        except:pass
        finally:
            conn.close()
            return User

    def GetPasswdByUser(self, User):
        Passwd = ""
        try:
            conn = sqlite3.connect(User+".db")
            retorno = list(conn.execute("SELECT * FROM Perfil WHERE Usuário = (?)", [(User)]))
            for row in retorno:
                Passwd = row[1]
        except:pass
        finally:
            conn.close()
            return Passwd

    def GetMesesDeReserva(self):
        retorno, cursor = self.GetDataDB("SELECT MesesDeReserva FROM Perfil")
        return retorno[0][0]

    def GetGastoMensal(self):
        retorno, cursor = self.GetDataDB("SELECT GastoMensal FROM Perfil")
        return retorno[0][0]

    def GetMontanteNasCorretoras(self):
        Patrimonio = 0.
        try:
            corretoras = self.HMI.DBManager.GetCorretoras("Bolsa")
            for corretora in corretoras:
                PatrimonioAux = self.HMI.DBManager.GetPatrimonioTotalCorretora(corretora, "Bolsa")
                # print(corretora, PatrimonioAux)
                if PatrimonioAux == -1: return -2
                Patrimonio += PatrimonioAux
            corretoras = self.HMI.DBManager.GetCorretoras("Cripto")
            for corretora in corretoras:
                PatrimonioAux = self.HMI.DBManager.GetPatrimonioTotalCorretora(corretora, "Cripto")
                # print(corretora, PatrimonioAux)
                if PatrimonioAux == -1: return -2
                Patrimonio += PatrimonioAux
        except:
            return -1
        return round(Patrimonio, 2)

    def GetMontanteAplicado(self):
        # É a diferença entre a soma de todos os depósitos e a soma de todos os saques
        Soma = 0

        retorno, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        tables = list(map(lambda x: x[0],retorno))
        tables = list(filter(lambda x: x.find("¨DepSaq")>-1, tables))
        for corretoraDepSaq in tables: # Para Bolsa
            retorno, cursor = self.GetDataDB("SELECT * FROM "+corretoraDepSaq)
            valores = list(map(lambda x: x[1], retorno))
            Soma += sum(valores)
        retorno, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        tables = list(map(lambda x: x[0],retorno))
        tables = list(filter(lambda x: x.find("¨Cripto¨Refinado")>-1, tables))
        for corretoraCriptoRefinado in tables: # Para Criptomoedas
            retorno, cursor = self.GetDataDB("SELECT * FROM "+corretoraCriptoRefinado)
            DepositoRows = list(filter(lambda x: x[3].find("Depósito")>-1, retorno))
            SaqueRows = list(filter(lambda x: x[3].find("Saque")>-1, retorno))
            depositos = list(map(lambda x: x[12], DepositoRows))
            Soma += sum(depositos)
            saques = list(map(lambda x: x[12], SaqueRows))
            Soma -= sum(saques)
            corretora = corretoraCriptoRefinado.replace("¨Cripto¨Refinado","").replace("OPs¨","")
            Soma -= self.GetValorEmContaCorrente(corretora, "Cripto")
        return Soma

    def GetDataForAcoesENegocios(self): # Desenvolver
        Volume_Acoes = 0.
        Volume_Fundos = 0.

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ações e Negócios","Ações Nacionais"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_Acoes = -1.
                    break
                Volume_Acoes += Estoque * Cotacao
            if Volume_Acoes == -1: break

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ações e Negócios","Fundos de investimentos: Ações e Negócios"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_Fundos = -1.
                    break
                Volume_Fundos += Estoque * Cotacao
            if Volume_Fundos == -1.: break

        return Volume_Acoes, Volume_Fundos

    def GetDataForRealEstate(self): # Desenvolver
        Volume_Terras = 0.
        Volume_Predios = 0.
        Volume_Fundos = 0.

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Real Estate","Terrenos"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_Terras = -1.
                    break
                Volume_Terras += Estoque * Cotacao
            if Volume_Terras == -1.: break

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Real Estate","Construções"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_Predios = -1.
                    break
                Volume_Predios += Estoque * Cotacao
            if Volume_Predios == -1.: break

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Real Estate","Fundos Imobiliários"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_Fundos = -1.
                    break
                Volume_Fundos += Estoque * Cotacao
            if Volume_Fundos == -1.: break

        return Volume_Terras, Volume_Predios, Volume_Fundos

    def GetDataForCaixa(self): # Desenvolver
        Volume_RF = 0.
        Volume_TD_TP = 0.
        Volume_PP = 0.
        Volume_COE = 0.
        Volume_Fundos = 0.

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Renda Fixa"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_RF = -1.
                    break
                Volume_RF += Estoque * Cotacao
            if Volume_RF == -1.: break

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Tesouro Direto e Títulos Públicos"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_TD_TP = -1.
                    break
                Volume_TD_TP += Estoque * Cotacao
            if Volume_TD_TP == -1.: break

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Previdência Privada"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_PP = -1.
                    break
                Volume_PP += Estoque * Cotacao
            if Volume_PP == -1.: break

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","COE"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_COE = -1.
                    break
                Volume_COE += Estoque * Cotacao
            if Volume_COE == -1.: break

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Fundos de Investimento: Renda Fixa"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_Fundos = -1.
                    break
                Volume_Fundos += Estoque * Cotacao
            if Volume_Fundos == -1.: break

        return Volume_RF, Volume_TD_TP, Volume_PP, Volume_COE, Volume_Fundos

    def GetDataForAtivosInternacionais(self): # Desenvolver
        Volume_BDR = 0.
        Volume_Fundos = 0.

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ativos Internacionais","BDR"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_BDR = -1.
                    break
                Volume_BDR += Estoque * Cotacao
            if Volume_BDR == -1.: break

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ativos Internacionais","Fundos de Investimento: Ações Internacionais"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    Volume_Fundos = -1.
                    break
                Volume_Fundos += Estoque * Cotacao
            if Volume_Fundos == -1.: break

        return Volume_BDR, Volume_Fundos

    def GetDataForCriptomoedas(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.

        # Pegar o estoque de cada moeda, independente da corretora

        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        TableNamesCriptoRefinado = list(filter(lambda x: x.find("¨Cripto¨Refinado")>-1 and x.find("OPs¨")>-1, Tabelas))
        Coins = []
        for TableName in TableNamesCriptoRefinado:
            retorno, cursor = self.GetDataDB("SELECT ParEsquerdo, ParDireito FROM "+TableName)
            Coins.extend(retorno[0])
            Coins.extend(retorno[1])
        Coins = list(dict.fromkeys(Coins))
        Coins = list(filter(lambda x: not x=="" and not x==self.GetUserCoinCurrency(), Coins))

        Volume_Coins = []
        for coin in Coins:
            Volume = 0.
            for TableName in TableNamesCriptoRefinado:
                try:
                    retorno, cursor = self.GetDataDB("SELECT EstoqueDe¨"+coin+" FROM "+TableName)
                    Estoque = retorno[-1][0]
                    retorno, cursor = self.GetDataDB("SELECT HoldDe¨"+coin+" FROM "+TableName)
                    Estoque += retorno[-1][0]
                    retorno, cursor = self.GetDataDB("SELECT StakeDe¨"+coin+" FROM "+TableName)
                    Estoque += retorno[-1][0]
                    Cotacao = self.GetCotacao(coin)
                    if Estoque < 0. or Cotacao <= 0.:
                        Volume = -1.
                        break
                    Volume += Estoque * Cotacao
                except:pass # Não tem essa moeda nessa corretora
            Volume_Coins.append((coin,Volume))
            if Volume == -1.:
                Volume_Coins = []
                break

        if len(Volume_Coins)>=1:
            Volume_Coins = sorted(Volume_Coins, key=lambda tup: tup[1])
            Volume_Top1 = Volume_Coins[-1][1]
        if len(Volume_Coins)>=2: Volume_Top2 = Volume_Coins[-2][1]
        if len(Volume_Coins)>=3: Volume_Top3 = Volume_Coins[-3][1]
        if len(Volume_Coins)>=4: Volume_Outras = sum([tup[1] for tup in Volume_Coins[:-3]])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForCriptomoedas(self):
        Label_Top1 = ''
        Label_Top2 = ''
        Label_Top3 = ''

        # Pegar o estoque de cada moeda, independente da corretora

        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        TableNamesCriptoRefinado = list(filter(lambda x: x.find("¨Cripto¨Refinado")>-1 and x.find("OPs¨")>-1, Tabelas))
        Coins = []
        for TableName in TableNamesCriptoRefinado:
            retorno, cursor = self.GetDataDB("SELECT ParEsquerdo, ParDireito FROM "+TableName)
            Coins.extend(retorno[0])
            Coins.extend(retorno[1])
        Coins = list(dict.fromkeys(Coins))
        Coins = list(filter(lambda x: not x=="", Coins))

        Label_Coins = []
        for coin in Coins:
            Volume = 0.
            for TableName in TableNamesCriptoRefinado:
                try:
                    retorno, cursor = self.GetDataDB("SELECT EstoqueDe¨"+coin+" FROM "+TableName)
                    Estoque = retorno[-1][0]
                    retorno, cursor = self.GetDataDB("SELECT HoldDe¨"+coin+" FROM "+TableName)
                    Estoque += retorno[-1][0]
                    retorno, cursor = self.GetDataDB("SELECT StakeDe¨"+coin+" FROM "+TableName)
                    Estoque += retorno[-1][0]
                    Cotacao = self.GetCotacao(coin)
                    if Estoque < 0. or Cotacao <= 0.:
                        Volume = -1.
                        break
                    Volume += Estoque * Cotacao
                except:pass # Não tem essa moeda nessa corretora
            Label_Coins.append((coin,Volume))
            if Volume == -1.:
                Label_Coins = []
                break

        if len(Label_Coins)>=1:
            Label_Coins = sorted(Label_Coins, key=lambda tup: tup[1])
            Label_Top1 = Label_Coins[-1][0]
            print(Label_Top1)
        if len(Label_Coins)>=2: Label_Top2 = Label_Coins[-2][0]
        if len(Label_Coins)>=3: Label_Top3 = Label_Coins[-3][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForAcoesNacionais(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ações e Negócios","Ações Nacionais"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForAcoesNacionais(self):
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ações e Negócios","Ações Nacionais"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForFundosAcoesENegocios(self): # Desenvolver
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ações e Negócios","Fundos de investimentos: Ações e Negócios"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForFundosAcoesENegocios(self): # Desenvolver
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ações e Negócios","Fundos de investimentos: Ações e Negócios"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForFII(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Real Estate","Fundos Imobiliários"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForFII(self):
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Real Estate","Fundos Imobiliários"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForTerrenos(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Real Estate","Terrenos"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForTerrenos(self):
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Real Estate","Terrenos"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForConstrucoes(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Real Estate","Construções"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForConstrucoes(self):
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Real Estate","Construções"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForRendaFixa(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Renda Fixa"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForRendaFixa(self):
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Renda Fixa"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForTesouroDiretoETitulosPublicos(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Tesouro Direto e Títulos Públicos"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForTesouroDiretoETitulosPublicos(self):
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Tesouro Direto e Títulos Públicos"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForPrevidenciaPrivada(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Previdência Privada"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForPrevidenciaPrivada(self):
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Previdência Privada"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForCOE(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","COE"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForCOE(self):
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","COE"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForFundosDeRendaFixa(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Fundos de Investimento: Renda Fixa"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForFundosDeRendaFixa(self):
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Caixa","Fundos de Investimento: Renda Fixa"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForBDR(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ativos Internacionais","BDR"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForBDR(self):
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ativos Internacionais","BDR"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetDataForFundosAcoesInternacionais(self):
        Volume_Top1 = 0.
        Volume_Top2 = 0.
        Volume_Top3 = 0.
        Volume_Outras = 0.
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ativos Internacionais","Fundos de Investimento: Ações Internacionais"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Volume_Top1 = sorted_by_volume[0][1]
            if len(sorted_by_volume)>1: Volume_Top2 = sorted_by_volume[1][1]
            if len(sorted_by_volume)>2: Volume_Top3 = sorted_by_volume[2][1]
            if len(sorted_by_volume)>3: Volume_Outras = sum(volume for label, volume in sorted_by_volume[3:])

        return Volume_Top1, Volume_Top2, Volume_Top3, Volume_Outras

    def GetDataLabelsForFundosAcoesInternacionais(self):
        Label_Top1 = '...'
        Label_Top2 = '...'
        Label_Top3 = '...'
        VolumeELabel_Acoes = []

        Ativos, cursor = self.GetDataDB("SELECT Ativo FROM Bolsa WHERE TipoDeAtivo = (?) AND SubtipoDeAtivo = (?)",["Ativos Internacionais","Fundos de Investimento: Ações Internacionais"])
        Ativos = list(map(lambda x: x[0],Ativos))
        Tabelas, cursor = self.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        Tabelas = list(map(lambda x: x[0],Tabelas))
        for ativo in Ativos:
            TableNamesDoAtivo = list(filter(lambda x: x.find("¨Bolsa¨Bruto")>-1 and x.find("OPs¨"+ativo)>-1, Tabelas))
            for TableName in TableNamesDoAtivo:
                Compras, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Compra")])
                Compras = list(map(lambda x: x[0],Compras))
                Vendas, cursor = self.GetDataDB("SELECT Qqt FROM "+TableName+" WHERE Tipo = (?)",[("Venda")])
                Vendas = list(map(lambda x: x[0],Vendas))
                Estoque = sum(Compras) - sum(Vendas)
                Cotacao = self.GetCotacao(ativo)
                if Estoque < 0. or Cotacao <= 0.:
                    VolumeELabel_Acoes = -1.
                    break
                VolumeELabel_Acoes.append((ativo, Estoque * Cotacao))
            if VolumeELabel_Acoes == -1: break

        if not VolumeELabel_Acoes == -1:
            sorted_by_volume = sorted(VolumeELabel_Acoes, key=lambda tup: tup[1])
            if len(sorted_by_volume)>0: Label_Top1 = sorted_by_volume[0][0]
            if len(sorted_by_volume)>1: Label_Top2 = sorted_by_volume[1][0]
            if len(sorted_by_volume)>2: Label_Top3 = sorted_by_volume[2][0]

        return Label_Top1, Label_Top2, Label_Top3

    def GetAllTickers(self):
        retornoBruto, cursor = self.GetDataDB("SELECT * FROM Tickers")
        retorno = list(map(lambda x: x[0], retornoBruto))
        return retorno

#%% Sets

    def SetAllTickers(self, AllTickers):
        try:
            self.ThreadLock.acquire()
            self.CreateTableInCurrentDB('Tickers', [('Ticker', 'TEXT')])
            self.ModifyDB("DELETE FROM Tickers")
            self.ModifyDB("VACUUM")
            ListOfTuples = [(ticker,) for ticker in AllTickers]
            cursor = self.conn.cursor()
            cursor.executemany('INSERT INTO Tickers VALUES(?);', ListOfTuples)
        except:pass
        finally: self.ThreadLock.release()
        # print(self.GetAllTickers()) # Debug

#%% Funções auxiliares

    def CriarDB(self, DB):
        conn = sqlite3.connect(DB)
        conn.close()
        try:os.popen('attrib +h '+os.path.split(DB)[1]) # Torna o arquivo oculto na pasta do APP
        except:pass

    def CreateTableInCurrentDB(self, TableName, ContentType):
        Header = ''
        for item in ContentType: Header += str(item[0])+' '+str(item[1])+","
        Header = Header[:-1]
        self.ModifyDB("CREATE TABLE IF NOT EXISTS "+TableName+" ("+Header+")")
        return True

    def AddRowInCurrentDB(self, TableName, Content):
        # Calcular a quantidade de colunas
        ColCount = ''
        for i in range(len(Content)): ColCount += "?,"
        ColCount = ColCount[:-1]

        # Colocar cada linha de conteúdo em um tuple
        rowcontent = ('',)
        for item in range(len(Content)):
            if rowcontent[0]=='': rowcontent = (Content[item][1],)
            else: rowcontent += (Content[item][1],)

        self.ModifyDB("INSERT INTO "+TableName+" VALUES ("+ColCount+")", rowcontent)
        return True

    def SortByDate(self, TableName):
        try:
            self.ModifyDB("ALTER TABLE "+TableName+" RENAME TO "+TableName+"¨NotSorted") # Transforma a tabela antiga na auxiliar
            if "OPs¨" in TableName:
                if self.HMI.BolsaOuCripto == "Bolsa":
                    self.CreateTableInCurrentDB(TableName, [('Data', 'DATETIME'),
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
                                                            ('Resultado', 'REAL')]) # Cria Nova Tabela pra ser a ordenada
                elif self.HMI.BolsaOuCripto == "Cripto":
                    self.CreateTableInCurrentDB(TableName, [('Observação', 'TEXT'),
                                                            ('Data', 'DATETIME'),
                                                            ('Tipo', 'TEXT'),
                                                            ('ParEsquerdo', 'TEXT'),
                                                            ('ParDireito', 'TEXT'),
                                                            ('Preço', 'REAL'),
                                                            ('Qqt', 'REAL'),
                                                            ('Taxa', 'REAL'),
                                                            ('MoedaDaTaxa', 'TEXT'),
                                                            ('Conversão', 'REAL')])
            elif "¨DepSaq" in TableName:
                self.CreateTableInCurrentDB(TableName, [('Data', 'DATETIME'),('Valor', 'REAL')])
            SortedTable, cursor = self.GetDataDB("SELECT * FROM "+TableName+"¨NotSorted ORDER BY Data ASC")
            content = []
            for row in SortedTable:
                oneRowTupleNotInShape = row
                oneRowListOfTuples = []
                for item in oneRowTupleNotInShape: oneRowListOfTuples.append(('',item))
                content.append(oneRowListOfTuples)
            for row in content: self.AddRowInCurrentDB(TableName, row)
        except Exception as e:pass
        finally: self.ModifyDB("DROP TABLE "+TableName+"¨NotSorted") # Deleta a tabela antiga

    def SepararDTeST(self, TableName, AcabouDeAdd = True):
        def OPEhAMaisRecenteDeTodas(OP, OPs):
            if "¨Bolsa" in TableName: aux = list(filter(lambda x: datetime.strptime(x[0],"%Y-%m-%d %H:%M:%S")>datetime.strptime(OP[0],"%Y-%m-%d %H:%M:%S"), OPs))
            elif "¨Cripto" in TableName: aux = list(filter(lambda x: datetime.strptime(x[1],"%Y-%m-%d %H:%M:%S")>datetime.strptime(OP[1],"%Y-%m-%d %H:%M:%S"), OPs))
            if len(aux)>0: return False
            return True
        def RedefinirDTeST(datas, TableDTeST_sorted):
            if "¨Bolsa" in TableName:
                NovaDT_Reposta = []
                NovaST_Reposta = []
                # Para cada data, começando da mais antiga pra mais recente, faça:
                # print(datas)
                for Data in datas:
                    # Identificar DT
                    OPsNaData = []
                    for OP in TableDTeST_sorted:
                        if Data in OP[0]: OPsNaData.append(OP)
                    if ("Compra" in (i[1] for i in OPsNaData)) and ("Venda" in (i[1] for i in OPsNaData)): # Pode ter tido DT
                        ListaDeIdxDeOPsDeCompraNaData = [(i, item) for i, item in enumerate(OPsNaData) if item[1] == "Compra"]
                        ListaDeIdxDeOPsDeVendaNaData = [(i, item) for i, item in enumerate(OPsNaData) if item[1] == "Venda"]
                        ListaDeIdxDeOPsDeCompraNaData_Variavel = copy.deepcopy(ListaDeIdxDeOPsDeCompraNaData)
                        ListaDeIdxDeOPsDeVendaNaData_Variavel = copy.deepcopy(ListaDeIdxDeOPsDeVendaNaData)
                        for idx, aux in enumerate(ListaDeIdxDeOPsDeVendaNaData):
                            i, V = aux
                            # print(idx)
                            ComprasDoDT = 0
                            VendasNoDT = V[2]
                            PassePraProximaOPDeVenda = False
                            for j, C in ListaDeIdxDeOPsDeCompraNaData:
                                if PassePraProximaOPDeVenda: break
                                elif i>j: # Se nessa mesma data teve compra antes da venda, houve DT
                                    doing = True
                                    while doing:
                                        if len(ListaDeIdxDeOPsDeCompraNaData_Variavel) > 0:
                                            ComprasDoDT += ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][2] # Quantidade de Ações Compradas No mesmo dia antes dessa venda
                                            # Caso mais que suficiente
                                            if ComprasDoDT > VendasNoDT: # Split essa compra em ST e DT
                                                # Calcula a proporção
                                                diferenca = ComprasDoDT - VendasNoDT
                                                ComprasDoDT -= diferenca
                                                proporcao = (ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][2]-diferenca)/ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][2]
                                                # Adiciona a proporção ao DT, op de compra e de venda
                                                AoDT = (ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][0], # Data
                                                        ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][1], # Tipo
                                                        int(round(ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][2]*proporcao,0)), # Qqt
                                                        ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][3], # Preço
                                                        round(ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][4]*proporcao,2), # Corretagem
                                                        ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][5], # TaxaB3Per
                                                        round(ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][6]*proporcao,2), # TaxaB3
                                                        ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][7], # Obs
                                                        'NULL', # Estoque
                                                        round(ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][4]*proporcao,2) + round(ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1][6]*proporcao,2), # Custo da operação
                                                        'NULL', # Custo total
                                                        'NULL', # Custo Médio
                                                        'NULL',) # Resultado
                                                aux = list(ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1])
                                                aux[2] = int(round(aux[2]*(1-proporcao),0))
                                                aux[4] = round(float(aux[4])*(1-proporcao),2)
                                                aux[6] = round(float(aux[6])*(1-proporcao),2)
                                                aux[9] = round(aux[4],2) + round(aux[6],2)
                                                ListaDeIdxDeOPsDeCompraNaData_Variavel[0]=(ListaDeIdxDeOPsDeCompraNaData_Variavel[0][0],tuple(aux))
                                                doing = False
                                                PassePraProximaOPDeVenda = True
                                                # Adiciona uma parte em DT e a outra em ST
                                                # print('Split')
                                                # print("ComprasDoDT > VendasNoDT, Add ao DT:\n",tuple(AoDT),"\ne:\n",V)
                                                AoDT = tuple(AoDT)
                                                NovaDT_Reposta.append([('Data', AoDT[0]),
                                                                       ('Tipo', AoDT[1]),
                                                                       ('Qqt', AoDT[2]),
                                                                       ('Preço', AoDT[3]),
                                                                       ('Corretagem', AoDT[4]),
                                                                       ('TaxaB3Per', AoDT[5]),
                                                                       ('TaxaB3', AoDT[6]),
                                                                       ('Obs', AoDT[7]),
                                                                       ('Estoque', AoDT[8]),
                                                                       ('CustoDaOperação', AoDT[4]+AoDT[6]),
                                                                       ('CustoTotal', AoDT[10]),
                                                                       ('CustoMédio', AoDT[11]),
                                                                       ('Resultado', AoDT[12])])
                                                # (Não faz pop)
                                                AoDT = ListaDeIdxDeOPsDeVendaNaData_Variavel[0][1]
                                                NovaDT_Reposta.append([('Data', AoDT[0]),
                                                                       ('Tipo', AoDT[1]),
                                                                       ('Qqt', AoDT[2]),
                                                                       ('Preço', AoDT[3]),
                                                                       ('Corretagem', AoDT[4]),
                                                                       ('TaxaB3Per', AoDT[5]),
                                                                       ('TaxaB3', AoDT[6]),
                                                                       ('Obs', AoDT[7]),
                                                                       ('Estoque', AoDT[8]),
                                                                       ('CustoDaOperação', AoDT[4]+AoDT[6]),
                                                                       ('CustoTotal', AoDT[10]),
                                                                       ('CustoMédio', AoDT[11]),
                                                                       ('Resultado', AoDT[12])])
                                                ListaDeIdxDeOPsDeVendaNaData_Variavel.pop(0)
                                            # Caso suficiente
                                            elif ComprasDoDT == VendasNoDT: # Caso perfeito
                                                # Adiciona ListaDeIdxDeOPsDeCompraNaData_Variavel[0] e V ao DT
                                                # pop ListaDeIdxDeOPsDeCompraNaData_Variavel[0] da lista ListaDeIdxDeOPsDeCompraNaData_Variavel
                                                # print("Add ao DT:\n",ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1],"\ne:\n",V)
                                                AoDT = ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1]
                                                NovaDT_Reposta.append([('Data', AoDT[0]),
                                                                       ('Tipo', AoDT[1]),
                                                                       ('Qqt', AoDT[2]),
                                                                       ('Preço', AoDT[3]),
                                                                       ('Corretagem', AoDT[4]),
                                                                       ('TaxaB3Per', AoDT[5]),
                                                                       ('TaxaB3', AoDT[6]),
                                                                       ('Obs', AoDT[7]),
                                                                       ('Estoque', AoDT[8]),
                                                                       ('CustoDaOperação', AoDT[4]+AoDT[6]),
                                                                       ('CustoTotal', AoDT[10]),
                                                                       ('CustoMédio', AoDT[11]),
                                                                       ('Resultado', AoDT[12])])
                                                ListaDeIdxDeOPsDeCompraNaData_Variavel.pop(0)
                                                AoDT = ListaDeIdxDeOPsDeVendaNaData_Variavel[0][1]
                                                NovaDT_Reposta.append([('Data', AoDT[0]),
                                                                       ('Tipo', AoDT[1]),
                                                                       ('Qqt', AoDT[2]),
                                                                       ('Preço', AoDT[3]),
                                                                       ('Corretagem', AoDT[4]),
                                                                       ('TaxaB3Per', AoDT[5]),
                                                                       ('TaxaB3', AoDT[6]),
                                                                       ('Obs', AoDT[7]),
                                                                       ('Estoque', AoDT[8]),
                                                                       ('CustoDaOperação', AoDT[4]+AoDT[6]),
                                                                       ('CustoTotal', AoDT[10]),
                                                                       ('CustoMédio', AoDT[11]),
                                                                       ('Resultado', AoDT[12])])
                                                ListaDeIdxDeOPsDeVendaNaData_Variavel.pop(0)
                                                doing = False
                                                PassePraProximaOPDeVenda = True
                                            # Caso insuficiente
                                            else:
                                                # print("Add ao DT:\n",ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1])
                                                if len(ListaDeIdxDeOPsDeCompraNaData_Variavel) == 1 or datetime.strptime(ListaDeIdxDeOPsDeCompraNaData_Variavel[1][1][0],"%Y-%m-%d %H:%M:%S")>datetime.strptime(V[0],"%Y-%m-%d %H:%M:%S"): # Se é a ultima tentativa e ainda assim é insuficiente # Split venda: houve uma parte em DT e outra em ST
                                                    AoDT = ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1]
                                                    NovaDT_Reposta.append([('Data', AoDT[0]),
                                                                           ('Tipo', AoDT[1]),
                                                                           ('Qqt', AoDT[2]),
                                                                           ('Preço', AoDT[3]),
                                                                           ('Corretagem', AoDT[4]),
                                                                           ('TaxaB3Per', AoDT[5]),
                                                                           ('TaxaB3', AoDT[6]),
                                                                           ('Obs', AoDT[7]),
                                                                           ('Estoque', AoDT[8]),
                                                                           ('CustoDaOperação', AoDT[4]+AoDT[6]),
                                                                           ('CustoTotal', AoDT[10]),
                                                                           ('CustoMédio', AoDT[11]),
                                                                           ('Resultado', AoDT[12])])
                                                    # Adiciona PARCIALMENTE ListaDeIdxDeOPsDeCompraNaData_Variavel[0] ao DT
                                                    # pop ListaDeIdxDeOPsDeCompraNaData_Variavel[0] da lista ListaDeIdxDeOPsDeCompraNaData_Variavel
                                                    ListaDeIdxDeOPsDeCompraNaData_Variavel.pop(0)
                                                    AoDT = ListaDeIdxDeOPsDeVendaNaData_Variavel[0][1]
                                                    diferenca = VendasNoDT - ComprasDoDT
                                                    proporcao = (ListaDeIdxDeOPsDeVendaNaData_Variavel[0][1][2]-diferenca)/ListaDeIdxDeOPsDeVendaNaData_Variavel[0][1][2]
                                                    NovaDT_Reposta.append([('Data', AoDT[0]),
                                                                           ('Tipo', AoDT[1]),
                                                                           ('Qqt', int(round(AoDT[2]*proporcao,0))),
                                                                           ('Preço', AoDT[3]),
                                                                           ('Corretagem', round(AoDT[4]*proporcao,2)),
                                                                           ('TaxaB3Per', AoDT[5]),
                                                                           ('TaxaB3', round(AoDT[6]*proporcao,2)),
                                                                           ('Obs', AoDT[7]),
                                                                           ('Estoque', AoDT[8]),
                                                                           ('CustoDaOperação', round(AoDT[4]*proporcao,2)+round(AoDT[6]*proporcao,2)),
                                                                           ('CustoTotal', AoDT[10]),
                                                                           ('CustoMédio', AoDT[11]),
                                                                           ('Resultado', AoDT[12])])
                                                    AoST = ListaDeIdxDeOPsDeVendaNaData_Variavel[0][1]
                                                    NovaST_Reposta.append([('Data', AoST[0]),
                                                                           ('Tipo', AoST[1]),
                                                                           ('Qqt', int(round(AoST[2]*(1-proporcao),0))),
                                                                           ('Preço', AoST[3]),
                                                                           ('Corretagem', round(AoST[4]*(1-proporcao),2)),
                                                                           ('TaxaB3Per', AoST[5]),
                                                                           ('TaxaB3', round(AoST[6]*(1-proporcao),2)),
                                                                           ('Obs', AoST[7]),
                                                                           ('Estoque', AoST[8]),
                                                                           ('CustoDaOperação', round(AoST[4]*(1-proporcao),2)+round(AoST[6]*(1-proporcao),2)),
                                                                           ('CustoTotal', AoST[10]),
                                                                           ('CustoMédio', AoST[11]),
                                                                           ('Resultado', AoST[12])])
                                                    ListaDeIdxDeOPsDeVendaNaData_Variavel.pop(0)
                                                    doing = False
                                                    PassePraProximaOPDeVenda = True

                                                else:
                                                    AoDT = ListaDeIdxDeOPsDeCompraNaData_Variavel[0][1]
                                                    NovaDT_Reposta.append([('Data', AoDT[0]),
                                                                           ('Tipo', AoDT[1]),
                                                                           ('Qqt', AoDT[2]),
                                                                           ('Preço', AoDT[3]),
                                                                           ('Corretagem', AoDT[4]),
                                                                           ('TaxaB3Per', AoDT[5]),
                                                                           ('TaxaB3', AoDT[6]),
                                                                           ('Obs', AoDT[7]),
                                                                           ('Estoque', AoDT[8]),
                                                                           ('CustoDaOperação', AoDT[4]+AoDT[6]),
                                                                           ('CustoTotal', AoDT[10]),
                                                                           ('CustoMédio', AoDT[11]),
                                                                           ('Resultado', AoDT[12])])
                                                    # Adiciona totalmente ListaDeIdxDeOPsDeCompraNaData_Variavel[0] ao DT
                                                    # pop ListaDeIdxDeOPsDeCompraNaData_Variavel[0] da lista ListaDeIdxDeOPsDeCompraNaData_Variavel
                                                    ListaDeIdxDeOPsDeCompraNaData_Variavel.pop(0)
                                                    # Continua buscando no While
                                        else: # Restante que configura ST
                                            # Adiciona totalmente ListaDeIdxDeOPsDeVendaNaData[i] ao ST
                                            # print("Add ao ST:\n",V)
                                            if len(ListaDeIdxDeOPsDeVendaNaData_Variavel) > 0:
                                                AoST = ListaDeIdxDeOPsDeVendaNaData_Variavel[0][1]
                                                NovaST_Reposta.append([('Data', AoST[0]),
                                                                       ('Tipo', AoST[1]),
                                                                       ('Qqt', AoST[2]),
                                                                       ('Preço', AoST[3]),
                                                                       ('Corretagem', AoST[4]),
                                                                       ('TaxaB3Per', AoST[5]),
                                                                       ('TaxaB3', AoST[6]),
                                                                       ('Obs', AoST[7]),
                                                                       ('Estoque', AoST[8]),
                                                                       ('CustoDaOperação', AoST[4]+AoST[6]),
                                                                       ('CustoTotal', AoST[10]),
                                                                       ('CustoMédio', AoST[11]),
                                                                       ('Resultado', AoST[12])])
                                                ListaDeIdxDeOPsDeVendaNaData_Variavel.pop(0)
                                            doing = False
                                else: # Houve ST
                                    # print("else; Add ao ST:\n",V)
                                    if len(ListaDeIdxDeOPsDeVendaNaData_Variavel) > 0:
                                        AoST = ListaDeIdxDeOPsDeVendaNaData_Variavel[0][1]
                                        NovaST_Reposta.append([('Data', AoST[0]),
                                                               ('Tipo', AoST[1]),
                                                               ('Qqt', AoST[2]),
                                                               ('Preço', AoST[3]),
                                                               ('Corretagem', AoST[4]),
                                                               ('TaxaB3Per', AoST[5]),
                                                               ('TaxaB3', AoST[6]),
                                                               ('Obs', AoST[7]),
                                                               ('Estoque', AoST[8]),
                                                               ('CustoDaOperação', AoST[4]+AoST[6]),
                                                               ('CustoTotal', AoST[10]),
                                                               ('CustoMédio', AoST[11]),
                                                               ('Resultado', AoST[12])])
                                        ListaDeIdxDeOPsDeVendaNaData_Variavel.pop(0)
                                    PassePraProximaOPDeVenda = True
                        for OP in ListaDeIdxDeOPsDeCompraNaData_Variavel:
                            # Add OPs de compra restante em ST pois não são DT
                            # print("Add ao ST:\n",OP[1])
                            AoST = OP[1]
                            NovaST_Reposta.append([('Data', AoST[0]),
                                                   ('Tipo', AoST[1]),
                                                   ('Qqt', AoST[2]),
                                                   ('Preço', AoST[3]),
                                                   ('Corretagem', AoST[4]),
                                                   ('TaxaB3Per', AoST[5]),
                                                   ('TaxaB3', AoST[6]),
                                                   ('Obs', AoST[7]),
                                                   ('Estoque', AoST[8]),
                                                   ('CustoDaOperação', AoST[4]+AoST[6]),
                                                   ('CustoTotal', AoST[10]),
                                                   ('CustoMédio', AoST[11]),
                                                   ('Resultado', AoST[12])])
                        if len(ListaDeIdxDeOPsDeVendaNaData) == idx:
                            for OP in ListaDeIdxDeOPsDeVendaNaData_Variavel:
                                # Add OPs de compra restante em ST pois não são DT
                                # print("Add ao ST:\n",OP[1])
                                AoST = OP[1]
                                NovaST_Reposta.append([('Data', AoST[0]),
                                                       ('Tipo', AoST[1]),
                                                       ('Qqt', AoST[2]),
                                                       ('Preço', AoST[3]),
                                                       ('Corretagem', AoST[4]),
                                                       ('TaxaB3Per', AoST[5]),
                                                       ('TaxaB3', AoST[6]),
                                                       ('Obs', AoST[7]),
                                                       ('Estoque', AoST[8]),
                                                       ('CustoDaOperação', AoST[4]+AoST[6]),
                                                       ('CustoTotal', AoST[10]),
                                                       ('CustoMédio', AoST[11]),
                                                       ('Resultado', AoST[12])])

                    else: # Com certeza todas essas OPs são ST
                        for OP in OPsNaData:
                            AoST = OP
                            NovaST_Reposta.append([('Data', AoST[0]),
                                                   ('Tipo', AoST[1]),
                                                   ('Qqt', AoST[2]),
                                                   ('Preço', AoST[3]),
                                                   ('Corretagem', AoST[4]),
                                                   ('TaxaB3Per', AoST[5]),
                                                   ('TaxaB3', AoST[6]),
                                                   ('Obs', AoST[7]),
                                                   ('Estoque', AoST[8]),
                                                   ('CustoDaOperação', AoST[4]+AoST[6]),
                                                   ('CustoTotal', AoST[10]),
                                                   ('CustoMédio', AoST[11]),
                                                   ('Resultado', AoST[12])])
                return NovaDT_Reposta, NovaST_Reposta

            elif "¨Cripto" in TableName:
                NovaDT_Reposta = []
                NovaST_Reposta = []
                # Para cada data, começando da mais antiga pra mais recente, faça:
                for Data in datas:
                    # Identificar DT
                    OPsNaData = []
                    for OP in TableDTeST_sorted:
                        if Data in OP[0]:
                            OPsNaData.append(OP)
                return [],[],[]

        # if "_Bolsa" in TableName:
        NovaDT_Reposta = []
        NovaST_Reposta = []

        self.SortByDate(TableName+"¨Bruto")
        TableBruto_Inicial, cursor = self.GetDataDB("SELECT * FROM "+TableName+"¨Bruto")
        TableDT_Inicial, cursor = self.GetDataDB("SELECT * FROM "+TableName+"¨DT")
        TableST_Inicial, cursor = self.GetDataDB("SELECT * FROM "+TableName+"¨ST")
        TableDTeST_Iniciais = []
        if len(TableST_Inicial)>0: TableDTeST_Iniciais.extend(TableST_Inicial)
        if len(TableDT_Inicial)>0: TableDTeST_Iniciais.extend(TableDT_Inicial)
        # TableDTeST_sorted = sorted(TableBruto_Inicial, key=lambda sub: (datetime.strptime(sub[0],"%Y-%m-%d %H:%M:%S"), sub[1]))
        aux = [t[0][:-9] for t in TableBruto_Inicial]
        datas = list(dict.fromkeys(aux))
        # print('vetor datas:',datas)

        if AcabouDeAdd:
            OPAdded = TableBruto_Inicial[-1]
            # print(100*'-'+"\n\nOPAdded:\n",OPAdded)
            if OPAdded[1] == "Compra":
                if not OPEhAMaisRecenteDeTodas(OPAdded, TableBruto_Inicial): # Reescrever tabelas DT e ST: executar procedimento completo
                    OPsNaData = []
                    for OP in TableBruto_Inicial:
                        if OPAdded[0][:-9] in OP[0]:
                            OPsNaData.append(OP)
                    if ("Compra" in (i[1] for i in OPsNaData)) and ("Venda" in (i[1] for i in OPsNaData)):
                        NovaDT_Reposta, NovaST_Reposta = RedefinirDTeST(datas, TableBruto_Inicial)

            else: # Venda # Reescrever tabelas DT e ST: executar procedimento completo
                OPsNaData = []
                for OP in TableBruto_Inicial:
                    if OPAdded[0][:-9] in OP[0]:
                        OPsNaData.append(OP)
                if ("Compra" in (i[1] for i in OPsNaData)) and ("Venda" in (i[1] for i in OPsNaData)):
                    NovaDT_Reposta, NovaST_Reposta = RedefinirDTeST(datas, TableBruto_Inicial)
        else:
            NovaDT_Reposta, NovaST_Reposta = RedefinirDTeST(datas, TableBruto_Inicial)

        if not (len(NovaDT_Reposta) == 0 and len(NovaST_Reposta) == 0): # Overwrite tables
            # print("\nOverwirting...\n") # Debug
            # print("DT:\n") # Debug
            self.ModifyDB("DROP TABLE "+TableName+"¨DT")
            self.CreateTableInCurrentDB(TableName+"¨DT", [('Data', 'DATETIME'),
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
            for row in NovaDT_Reposta:
                # print(row) # Debug
                # Overwrite DT
                self.AddRowInCurrentDB(TableName+"¨DT", row)

            # print("ST:\n") # Debug

            self.ModifyDB("DROP TABLE "+TableName+"¨ST")
            self.CreateTableInCurrentDB(TableName+"¨ST", [('Data', 'DATETIME'),
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
            for row in NovaST_Reposta:
                # print(row) # Debug
                # Overwrite ST
                self.AddRowInCurrentDB(TableName+"¨ST", row)

        # if "¨Cripto" in TableName:
        #     NovaDT_Reposta = []
        #     NovaST_Reposta = []
        #
        #     self.SortByDate(TableName+"¨Bruto")
        #     TableBruto_Inicial, cursor = self.GetDataDB("SELECT * FROM "+TableName+"¨Bruto")
        #     # TableDTeST_sorted = sorted(TableBruto_Inicial, key=lambda sub: (datetime.strptime(sub[1],"%Y-%m-%d %H:%M:%S"), sub[1]))
        #     aux = [t[1][:-9] for t in TableBruto_Inicial]
        #     datas = list(dict.fromkeys(aux))
        #     print('vetor datas:',datas)
        #     NovaDT_Reposta, NovaST_Reposta, HEADER = RedefinirDTeST(datas, TableBruto_Inicial)

        #
        #     self.ModifyDB("DROP TABLE "+TableName+"¨DT")
        #     self.CreateTableInCurrentDB(TableName+"¨DT", [HEADER])
        #     for row in NovaDT_Reposta:
        #         print("DT: ",row) # Debug
        #         # Overwrite DT
        #         self.AddRowInCurrentDB(TableName+"¨DT", row)

        #
        #     self.ModifyDB("DROP TABLE "+TableName+"¨ST")
        #     self.CreateTableInCurrentDB(TableName+"¨ST", [HEADER])
        #     for row in NovaDT_Reposta:
        #         print("ST: ",row) # Debug
        #         # Overwrite DT
        #         self.AddRowInCurrentDB(TableName+"¨ST", row)

    def CopiarBrutoPraDT(self, TableName):
        self.ModifyDB("DROP TABLE "+TableName+"¨DT") # Deleta a tabela antiga
        self.CreateTableInCurrentDB(TableName+"¨DT", [('Data', 'DATETIME'),
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
        content = []
        TableBruto, cursor = self.GetDataDB("SELECT * FROM "+TableName+"¨Bruto")
        for row in TableBruto:
            content.append([('Data', row[0]),
                            ('Tipo', row[1]),
                            ('Qqt', row[2]),
                            ('Preço', row[3]),
                            ('Corretagem', row[4]),
                            ('TaxaB3Per', row[5]),
                            ('TaxaB3', row[6]),
                            ('Obs', row[7]),
                            ('Estoque', row[8]),
                            ('CustoDaOperação', row[9]),
                            ('CustoTotal', row[10]),
                            ('CustoMédio', row[11]),
                            ('Resultado', row[12])])
        for row in content:
            # print(row) # Debug
            self.AddRowInCurrentDB(TableName+"¨DT", row)

    def CalcularCelsAutomatizadas(self, TableName):
        try:
            self.ModifyDB("ALTER TABLE "+TableName+" RENAME TO "+TableName+"¨NA") # Transforma a tabela antiga na auxiliar
            self.CreateTableInCurrentDB(TableName, [('Data', 'DATETIME'),
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
                                                    ('Resultado', 'REAL')]) # Cria Nova Tabela pra ser a ordenada
            TableNotAnswered, cursor = self.GetDataDB("SELECT * FROM "+TableName+"¨NA")
            content = []
            for i, row in enumerate(TableNotAnswered):
                if row[1] == "Compra":
                    if i == 0:
                        Estoque = row[2]
                        CustoTotal = row[9]+row[2]*row[3]
                        CustoMedio = CustoTotal/Estoque if not Estoque == 0 else 0
                        Resultado = "NULL"
                        content.append([('Data', row[0]),
                                        ('Tipo', row[1]),
                                        ('Qqt', row[2]),
                                        ('Preço', row[3]),
                                        ('Corretagem', row[4]),
                                        ('TaxaB3Per', row[5]),
                                        ('TaxaB3', row[6]),
                                        ('Obs', row[7]),
                                        ('Estoque', Estoque),
                                        ('CustoDaOperação', round(row[4]+row[6],2)),
                                        ('CustoTotal', CustoTotal),
                                        ('CustoMédio', CustoMedio),
                                        ('Resultado', Resultado)])
                    else:
                        Estoque = content[i-1][8][1]+row[2]
                        CustoTotal = content[i-1][10][1]+row[9]+row[2]*row[3]
                        CustoMedio = CustoTotal/Estoque if not Estoque == 0 else 0
                        Resultado = "NULL"
                        content.append([('Data', row[0]),
                                        ('Tipo', row[1]),
                                        ('Qqt', row[2]),
                                        ('Preço', row[3]),
                                        ('Corretagem', row[4]),
                                        ('TaxaB3Per', row[5]),
                                        ('TaxaB3', row[6]),
                                        ('Obs', row[7]),
                                        ('Estoque', Estoque),
                                        ('CustoDaOperação', round(row[4]+row[6],2)),
                                        ('CustoTotal', CustoTotal),
                                        ('CustoMédio', CustoMedio),
                                        ('Resultado', Resultado)])
                else: # Venda
                    if i == 0: # Nunca deve acontecer
                        Estoque = -row[2]
                        CustoTotal = row[9]-row[2]*row[3]
                        CustoMedio = CustoTotal/Estoque if not Estoque == 0 else 0
                        Resultado = "NULL"
                        content.append([('Data', row[0]),
                                        ('Tipo', row[1]),
                                        ('Qqt', row[2]),
                                        ('Preço', row[3]),
                                        ('Corretagem', row[4]),
                                        ('TaxaB3Per', row[5]),
                                        ('TaxaB3', row[6]),
                                        ('Obs', row[7]),
                                        ('Estoque', Estoque),
                                        ('CustoDaOperação', round(row[4]+row[6],2)),
                                        ('CustoTotal', CustoTotal),
                                        ('CustoMédio', CustoMedio),
                                        ('Resultado', Resultado)])
                    else:
                        Estoque = content[i-1][8][1]-row[2]
                        CustoTotal = content[i-1][10][1]-row[2]*content[i-1][11][1]
                        CustoMedio = CustoTotal/Estoque if not Estoque == 0 else 0
                        Resultado = row[2]*(row[3]-content[i-1][11][1])-row[9]
                        content.append([('Data', row[0]),
                                        ('Tipo', row[1]),
                                        ('Qqt', row[2]),
                                        ('Preço', row[3]),
                                        ('Corretagem', row[4]),
                                        ('TaxaB3Per', row[5]),
                                        ('TaxaB3', row[6]),
                                        ('Obs', row[7]),
                                        ('Estoque', Estoque),
                                        ('CustoDaOperação', round(row[4]+row[6],2)),
                                        ('CustoTotal', CustoTotal),
                                        ('CustoMédio', CustoMedio),
                                        ('Resultado', round(Resultado, 2))])
            # print(TableName) # Debug
            for row in content:
                # print(row) # Debug
                self.AddRowInCurrentDB(TableName, row)
        except:pass
        finally:
            self.ModifyDB("DROP TABLE "+TableName+"¨NA") # Deleta a tabela antiga

    def CalcularCelsAutomatizadas_CriptoRefinado(self, TableName):
        TableNameBruto = TableName+"¨Bruto"
        TableNameRefinado = TableName+"¨Refinado"
        self.SortByDate(TableNameBruto)

        Observacao_idx = 0
        Resultado_idx = 1
        Data_idx = 2
        Tipo_idx = 3
        ParEsquerdo_idx = 4
        ParDireito_idx = 5
        Preco_idx = 6
        Quantidade_idx = 7
        Taxa_idx = 8
        MoedaDaTaxa_idx = 9
        Conversao_idx = 10
        CotacaoMoedaCorrente_idx = 11
        Volume_idx = 12
        # 1) Criar as primeiras colunas padrões:   # ('Observação', 'TEXT'),
                                                   # ('Resultado', 'REAL'),
                                                   # ('Data', 'DATETIME'),
                                                   # ('Tipo', 'TEXT'),
                                                   # ('ParEsquerdo', 'TEXT'),
                                                   # ('ParDireito', 'TEXT'),
                                                   # ('Preço', 'REAL'),
                                                   # ('Qqt', 'REAL'),
                                                   # ('Taxa', 'REAL'),
                                                   # ('MoedaDaTaxa', 'TEXT'),
                                                   # ('Conversão', 'REAL'),
                                                   # ('Cotação¨'+MoedaCorrente, 'REAL'),
                                                   # ('Volume', 'REAL')
        # 2) Pegar quantas moedas existem
        # 3) Criar para cada moeda um conjunto de 3 colunas: 'Estoque de '; 'Custo de '; 'Preço Médio de ' exceto para MoedaCorrente
        # 4) Para cada operação faça:
            # 4.1) Copiar a linha anterior numa linha auxiliar
            # 4.2) Somar ou Subtrair os efeitos da operação nas colunas correspondentes
            # 4.3) Escrever linha auxiliar na tabela

        # 1)
        MoedaCorrente = self.GetCorretoraCoinCurrency()
        Header = [('Observação', 'TEXT'),
                  ('Resultado', 'REAL'),
                  ('Data', 'DATETIME'),
                  ('Tipo', 'TEXT'),
                  ('ParEsquerdo', 'TEXT'),
                  ('ParDireito', 'TEXT'),
                  ('Preço', 'REAL'),
                  ('Qqt', 'REAL'),
                  ('Taxa', 'REAL'),
                  ('MoedaDaTaxa', 'TEXT'),
                  ('Conversão', 'REAL'),
                  ('Cotação¨'+MoedaCorrente, 'REAL'),
                  ('Volume', 'REAL')]
        # 2)
        TableBruto, cursor = self.GetDataDB("SELECT * FROM "+TableNameBruto)
        ListaComParesDaEsquerda = [row[3] for row in TableBruto]
        ListaComParesDaDireita = [row[4] for row in TableBruto]
        ListaDeMoedas = ListaComParesDaEsquerda
        ListaDeMoedas.extend(ListaComParesDaDireita)
        ListaDeMoedas = list(dict.fromkeys(ListaDeMoedas))
        try:ListaDeMoedas.remove('')
        except:pass
        # print("Moedas encontradas: ", ListaDeMoedas) # Debug
        # 3)
        for coin in ListaDeMoedas:
            Header.append(('EstoqueDe¨'+coin,'REAL'))
            Header.append(('HoldDe¨'+coin, 'REAL'))
            Header.append(('StakeDe¨'+coin, 'REAL'))
            Header.append(('CustoDe¨'+coin,'REAL'))
            Header.append(('PreçoMédioDe¨'+coin,'REAL'))
        self.ModifyDB("DROP TABLE "+TableNameRefinado)
        self.ModifyDB("VACUUM")
        self.CreateTableInCurrentDB(TableNameRefinado, Header)
        # 4.1)
        if len(TableBruto) > 0: primeiraData = datetime.strptime(TableBruto[0][1], '%Y-%m-%d %H:%M:%S') - timedelta(seconds=1)
        else: primeiraData = datetime.now()
        row = [('Observação', 'NASCIMENTO'),
               ('Resultado', 0),
               ('Data', primeiraData), # Um segundo antes da primeira operação
               ('Tipo', 'EMPTY'),
               ('ParEsquerdo', ''),
               ('ParDireito', ''),
               ('Preço', 0),
               ('Qqt', 0),
               ('Taxa', 0),
               ('MoedaDaTaxa', ''),
               ('Conversão', 0),
               ('Cotação¨'+MoedaCorrente, 0),
               ('Volume', 0)] # Primeira linha é especial
        for coin in ListaDeMoedas:
            row.append(('EstoqueDe¨'+coin, 0))
            row.append(('HoldDe¨'+coin, 0))
            row.append(('StakeDe¨'+coin, 0))
            row.append(('CustoDe¨'+coin, 0))
            row.append(('PreçoMédioDe¨'+coin, 0))
        # print(row) #Debug
        self.AddRowInCurrentDB(TableNameRefinado, row)
        for op in TableBruto:
            # 4.2) Somar ou Subtrair os efeitos da operação nas colunas correspondentes
            row[Observacao_idx] = ('Observação', op[0]) # Observação
            row[Resultado_idx] = ('Resultado', 0) # Resultado, a ser redefinido se preciso for
            row[Data_idx] = ('Data', op[1]) # Data
            row[ParEsquerdo_idx] = ('ParEsquerdo', op[3]) # ParEsquerdo
            row[ParDireito_idx] = ('ParDireito', op[4]) # ParDireito
            row[Tipo_idx] = ('Tipo', op[2]) # Tipo
            row[Preco_idx] = ('Preço', op[5]) # Preço
            row[Quantidade_idx] = ('Quantidade', op[6]) # Quantidade
            row[Taxa_idx] = ('Taxa', op[7]) # Taxa
            row[MoedaDaTaxa_idx] = ('MoedaDaTaxa', op[8]) # MoedaDaTaxa
            row[Conversao_idx] = ('Conversão', op[9]) # Conversão
            row[CotacaoMoedaCorrente_idx] = ('Cotação¨'+MoedaCorrente, row[Conversao_idx][1]*row[Preco_idx][1]) # Cotação MoedaCorrente
            row[Volume_idx] = ('Volume', row[CotacaoMoedaCorrente_idx][1]*row[Quantidade_idx][1]) # Volume

            if row[Tipo_idx][1] == "Compra":
                # 4.2.1) Aumenta Estoque de ParEsquerdo
                # 4.2.2) Diminui Estoque de ParDireito
                # 4.2.3) Aumenta proporcionalmente o Custo de ParEsquerdo
                # 4.2.4) Diminui proporcionalmente o Custo de ParDireito
                # 4.2.5) Calcula Preço Médio ParEsquerdo
                # 4.2.6) Calcula Preço Médio ParDireito

                EstoqueEsquerda_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParEsquerdo_idx][1]][0]
                HoldEsquerda_idx = EstoqueEsquerda_idx + 1; StakeEsquerda_idx = HoldEsquerda_idx + 1; CustoEsquerda_idx = StakeEsquerda_idx + 1; PrecoMedioEsquerda_idx = CustoEsquerda_idx + 1
                EstoqueDireita_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParDireito_idx][1]][0]
                HoldDireita_idx = EstoqueDireita_idx + 1; StakeDireita_idx = HoldDireita_idx + 1; CustoDireita_idx = StakeDireita_idx + 1; PrecoMedioDireita_idx = CustoDireita_idx + 1
                # 4.2.1)
                row[EstoqueEsquerda_idx] = (row[EstoqueEsquerda_idx][0], round(row[EstoqueEsquerda_idx][1] + row[Quantidade_idx][1], 8)) # Estoque
                # 4.2.2)
                EstoqueDireitaAntiga = row[EstoqueDireita_idx][1]
                row[EstoqueDireita_idx] = (row[EstoqueDireita_idx][0], round(row[EstoqueDireita_idx][1] - row[Quantidade_idx][1] * row[Preco_idx][1], 8)) # Estoque
                # 4.2.3)
                if not EstoqueDireitaAntiga == 0:
                    proporcao = (EstoqueDireitaAntiga - row[EstoqueDireita_idx][1]) / EstoqueDireitaAntiga
                else:
                    proporcao = 0
                CustoEsquerdaAntiga = row[CustoEsquerda_idx][1]
                row[CustoEsquerda_idx] = (row[CustoEsquerda_idx][0], round(row[CustoEsquerda_idx][1] + proporcao*row[CustoDireita_idx][1], 8)) # Custo
                # 4.2.4)
                row[CustoDireita_idx] = (row[CustoDireita_idx][0], round(row[CustoDireita_idx][1] - (row[CustoEsquerda_idx][1] - CustoEsquerdaAntiga), 8)) # Custo
                # 4.2.5)
                if row[EstoqueEsquerda_idx][1] > 0:
                    row[PrecoMedioEsquerda_idx] = (row[PrecoMedioEsquerda_idx][0], round(row[CustoEsquerda_idx][1]/(row[EstoqueEsquerda_idx][1]+row[HoldEsquerda_idx][1]+row[StakeEsquerda_idx][1]), 8)) # Preço Médio
                else:
                    row[PrecoMedioEsquerda_idx] = (row[PrecoMedioEsquerda_idx][0], 0) # Preço Médio
                # 4.2.6)
                if (row[EstoqueDireita_idx][1]+row[HoldDireita_idx][1]+row[StakeDireita_idx][1]) > 0:
                    row[PrecoMedioDireita_idx] = (row[PrecoMedioDireita_idx][0], round(row[CustoDireita_idx][1]/(row[EstoqueDireita_idx][1]+row[HoldDireita_idx][1]+row[StakeDireita_idx][1]), 8)) # Preço Médio
                else:
                    row[PrecoMedioDireita_idx] = (row[PrecoMedioDireita_idx][0], 0) # Preço Médio

            elif row[Tipo_idx][1] == "Venda":
                # 4.2.1) Diminui Estoque de ParEsquerdo
                # 4.2.2) Aumenta Estoque de ParDireito
                # 4.2.3) Diminui Custo de ParEsquerdo
                # 4.2.4) Aumenta Custo de ParDireito
                # 4.2.5) Calcula Preço Médio ParEsquerdo
                # 4.2.6) Calcula Preço Médio ParDireito

                EstoqueEsquerda_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParEsquerdo_idx][1]][0]
                HoldEsquerda_idx = EstoqueEsquerda_idx + 1; StakeEsquerda_idx = HoldEsquerda_idx + 1; CustoEsquerda_idx = StakeEsquerda_idx + 1; PrecoMedioEsquerda_idx = CustoEsquerda_idx + 1
                EstoqueDireita_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParDireito_idx][1]][0]
                HoldDireita_idx = EstoqueDireita_idx + 1; StakeDireita_idx = HoldDireita_idx + 1; CustoDireita_idx = StakeDireita_idx + 1; PrecoMedioDireita_idx = CustoDireita_idx + 1
                # 4.2.1)
                EstoqueEsquerdaAntiga = row[EstoqueEsquerda_idx][1]
                row[EstoqueEsquerda_idx] = (row[EstoqueEsquerda_idx][0], round(row[EstoqueEsquerda_idx][1] - row[Quantidade_idx][1], 8)) # Estoque
                # 4.2.2)
                EstoqueDireitaAntiga = row[EstoqueDireita_idx][1]
                row[EstoqueDireita_idx] = (row[EstoqueDireita_idx][0], round(row[EstoqueDireita_idx][1] + row[Quantidade_idx][1] * row[Preco_idx][1], 8)) # Estoque
                # 4.2.4)
                if not EstoqueEsquerdaAntiga == 0:
                    proporcao = (EstoqueEsquerdaAntiga - row[EstoqueEsquerda_idx][1]) / EstoqueEsquerdaAntiga
                else:
                    proporcao = 0
                CustoDireitaAntiga = row[CustoDireita_idx][1]
                row[CustoDireita_idx] = (row[CustoDireita_idx][0], round(row[CustoDireita_idx][1] + proporcao*row[CustoEsquerda_idx][1], 8)) # Custo
                # 4.2.3)
                row[CustoEsquerda_idx] = (row[CustoEsquerda_idx][0], round(row[CustoEsquerda_idx][1] - (row[CustoDireita_idx][1] - CustoDireitaAntiga), 8)) # Custo
                # 4.2.5)
                if row[EstoqueDireita_idx][1] > 0:
                    row[PrecoMedioDireita_idx] = (row[PrecoMedioDireita_idx][0], round(row[CustoDireita_idx][1]/(row[EstoqueDireita_idx][1]+row[HoldDireita_idx][1]+row[StakeDireita_idx][1]), 8)) # Preço Médio
                else:
                    row[PrecoMedioDireita_idx] = (row[PrecoMedioDireita_idx][0], 0) # Preço Médio
                # 4.2.6)
                if (row[EstoqueEsquerda_idx][1]+row[HoldEsquerda_idx][1]+row[StakeEsquerda_idx][1]) > 0:
                    row[PrecoMedioEsquerda_idx] = (row[PrecoMedioEsquerda_idx][0], round(row[CustoEsquerda_idx][1]/(row[EstoqueEsquerda_idx][1]+row[HoldEsquerda_idx][1]+row[StakeEsquerda_idx][1]), 8)) # Preço Médio
                else:
                    row[PrecoMedioEsquerda_idx] = (row[PrecoMedioEsquerda_idx][0], 0) # Preço Médio

            elif row[Tipo_idx][1] == "Depósito":
                # 4.2.1) Aumenta Estoque de ParEsquerdo
                # 4.2.2) Calcula Custo de ParEsquerdo
                # 4.2.3) Calcula Preço Médio ParEsquerdo

                Estoque_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParEsquerdo_idx][1]][0]
                Hold_idx = Estoque_idx + 1; Stake_idx = Hold_idx + 1; Custo_idx = Stake_idx + 1; PrecoMedio_idx = Custo_idx + 1
                # 4.2.1)
                row[Estoque_idx] = (row[Estoque_idx][0], round(row[Estoque_idx][1] + row[Quantidade_idx][1], 8)) # Estoque
                # 4.2.2)
                row[Custo_idx] = (row[Custo_idx][0], round(row[Custo_idx][1] + row[11][1] * row[7][1], 8)) # Custo
                # 4.2.3)
                if (row[Estoque_idx][1]+row[Hold_idx][1]+row[Stake_idx][1]) > 0:
                    row[PrecoMedio_idx] = (row[PrecoMedio_idx][0], round(row[Custo_idx][1] / (row[Estoque_idx][1] + row[Hold_idx][1] + row[Stake_idx][1]), 8)) # Preço Médio
                else:
                    row[PrecoMedio_idx] = (row[PrecoMedio_idx][0], 0) # Preço Médio

            elif row[Tipo_idx][1] == "Saque":
                # 4.2.1) Diminui Estoque de ParEsquerdo
                # 4.2.2) Calcula Custo de ParEsquerdo
                # 4.2.3) Calcula Preço Médio ParEsquerdo
                # 4.2.4) Calcula o Resultado, se for o caso

                Estoque_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParEsquerdo_idx][1]][0]
                Hold_idx = Estoque_idx + 1; Stake_idx = Hold_idx + 1; Custo_idx = Stake_idx + 1; PrecoMedio_idx = Custo_idx + 1
                EstoqueAnterior = row[Estoque_idx][1]
                PrecoMedioAnterior = row[PrecoMedio_idx][1]
                # 4.2.1)
                row[Estoque_idx] = (row[Estoque_idx][0], round(row[Estoque_idx][1] - row[Quantidade_idx][1], 8)) # Estoque
                # 4.2.2)
                row[Custo_idx] = (row[Custo_idx][0], round(row[Custo_idx][1] - (EstoqueAnterior - row[Estoque_idx][1]) / EstoqueAnterior * row[Custo_idx][1], 8)) # Custo
                #### Arrumar o 4.2.2) ??
                # 4.2.3)
                if (row[Estoque_idx][1]+row[Hold_idx][1]+row[Stake_idx][1]) > 0:
                    row[PrecoMedio_idx] = (row[PrecoMedio_idx][0], round(row[Custo_idx][1]/(row[Estoque_idx][1]+row[Hold_idx][1]+row[Stake_idx][1]), 8)) # Preço Médio
                else:
                    row[PrecoMedio_idx] = (row[PrecoMedio_idx][0], 0) # Preço Médio

                # 4.3.4)
                if row[ParEsquerdo_idx][1] == MoedaCorrente:
                    row[Resultado_idx] = (row[Resultado_idx][0], row[Quantidade_idx][1] * (1 - PrecoMedioAnterior)) # Resultado
                    if row[MoedaDaTaxa_idx] == MoedaCorrente:
                        row[Resultado_idx] = (row[Resultado_idx][0], row[Resultado_idx][1] - row[Taxa_idx][1])
                    row[Resultado_idx] = (row[Resultado_idx][0], round(row[Resultado_idx][1], 2))

            elif row[Tipo_idx][1] == "Drop":
                # 4.2.1) Aumenta Estoque de ParEsquerdo
                # 4.2.2) Calcula Preço Médio ParEsquerdo

                Estoque_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParEsquerdo_idx][1]][0]
                Hold_idx = Estoque_idx + 1; Stake_idx = Hold_idx + 1; Custo_idx = Stake_idx + 1; PrecoMedio_idx = Custo_idx + 1
                # 4.2.1)
                row[Estoque_idx] = (row[Estoque_idx][0], round(row[Estoque_idx][1] + row[Quantidade_idx][1], 8)) # Estoque
                # 4.2.2)
                if (row[Estoque_idx][1]+row[Hold_idx][1]+row[Stake_idx][1]) > 0:
                    row[PrecoMedio_idx] = (row[PrecoMedio_idx][0], round(row[Custo_idx][1]/(row[Estoque_idx][1]+row[Hold_idx][1]+row[Stake_idx][1]), 8)) # Preço Médio
                else:
                    row[PrecoMedio_idx] = (row[PrecoMedio_idx][0], 0) # Preço Médio

            elif row[Tipo_idx][1] == "Burn":
                # 4.2.1) Diminui Estoque de ParEsquerdo. Considerar o Hold e o Stake tbm
                # 4.2.2) Calcula Custo de ParEsquerdo
                # 4.2.3) Calcula Preço Médio ParEsquerdo
                # 4.2.4) Calcula o Resultado (o prejuízo)

                Estoque_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParEsquerdo_idx][1]][0]
                Hold_idx = Estoque_idx + 1; Stake_idx = Hold_idx + 1; Custo_idx = Stake_idx + 1; PrecoMedio_idx = Custo_idx + 1
                EstoqueAnterior = row[Estoque_idx][1]
                CustoAnterior = row[Custo_idx][1]
                PrecoMedioAnterior = row[PrecoMedio_idx][1]
                # 4.2.1)
                if not row[Estoque_idx][1] - row[Quantidade_idx][1] < 0:
                    row[Estoque_idx] = (row[Estoque_idx][0], round(row[Estoque_idx][1] - row[Quantidade_idx][1], 8)) # Estoque
                elif not row[Estoque_idx][1] + row[Hold_idx][1] - row[Quantidade_idx][1] < 0:
                    row[Hold_idx] = (row[Hold_idx][0], round(row[Hold_idx][1] + row[Estoque_idx][1] - row[Quantidade_idx][1], 8)) # Hold
                    row[Estoque_idx] = (row[Estoque_idx][0], round(0, 8)) # Estoque
                else:
                    row[Stake_idx] = (row[Stake_idx][0], round(row[Stake_idx][1] + row[Hold_idx][1] + row[Estoque_idx][1] - row[Quantidade_idx][1], 8)) # Hold
                    row[Hold_idx] = (row[Hold_idx][0], round(0, 8)) # Hold
                    row[Estoque_idx] = (row[Estoque_idx][0], round(0, 8)) # Estoque
                # 4.2.2)
                row[Custo_idx] = (row[Custo_idx][0], round(row[Custo_idx][1] - row[Quantidade_idx][1] * PrecoMedioAnterior, 8)) # Custo
                # 4.2.3)
                if (row[Estoque_idx][1]+row[Hold_idx][1]+row[Stake_idx][1]) > 0:
                    row[PrecoMedio_idx] = (row[PrecoMedio_idx][0], round(row[Custo_idx][1] / (row[Estoque_idx][1] + row[Hold_idx][1] + row[Stake_idx][1]), 8)) # Preço Médio
                else:
                    row[PrecoMedio_idx] = (row[PrecoMedio_idx][0], 0) # Preço Médio
                # 4.2.4)
                row[Resultado_idx] = (row[Resultado_idx][0], round( - (CustoAnterior - row[Custo_idx][1]), 8)) # Resultado

            elif row[Tipo_idx][1] == "Stake":
                # 4.2.1) Aumenta StakeDe_ ParEsquerdo
                # 4.2.2) Diminui StakeDe_ ParEsquerdo

                Estoque_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParEsquerdo_idx][1]][0]
                Hold_idx = Estoque_idx + 1; Stake_idx = Hold_idx + 1; Custo_idx = Stake_idx + 1; PrecoMedio_idx = Custo_idx + 1
                # 4.2.1)
                row[Estoque_idx] = (row[Estoque_idx][0], round(row[Estoque_idx][1] - row[Quantidade_idx][1], 8)) # Estoque
                # 4.2.2)
                row[Stake_idx] = (row[Stake_idx][0], round(row[Stake_idx][1] + row[Quantidade_idx][1], 8)) # Stake

            elif row[Tipo_idx][1] == "Unstake":
                # 4.2.1) Diminui StakeDe_ ParEsquerdo
                # 4.2.2) Aumenta StakeDe_ ParEsquerdo

                Estoque_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParEsquerdo_idx][1]][0]
                Hold_idx = Estoque_idx + 1; Stake_idx = Hold_idx + 1; Custo_idx = Stake_idx + 1; PrecoMedio_idx = Custo_idx + 1
                # 4.2.1)
                row[Estoque_idx] = (row[Estoque_idx][0], round(row[Estoque_idx][1] + row[Quantidade_idx][1], 8)) # Estoque
                # 4.2.2)
                row[Stake_idx] = (row[Stake_idx][0], round(row[Stake_idx][1] - row[Quantidade_idx][1], 8)) # Stake

            elif row[Tipo_idx][1] == "Hold":
                # 4.2.1) Aumenta HoldDe_ ParEsquerdo
                # 4.2.2) Diminui HoldDe_ ParEsquerdo

                Estoque_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParEsquerdo_idx][1]][0]
                Hold_idx = Estoque_idx + 1; Stake_idx = Hold_idx + 1; Custo_idx = Stake_idx + 1; PrecoMedio_idx = Custo_idx + 1
                # 4.2.1)
                row[Estoque_idx] = (row[Estoque_idx][0], round(row[Estoque_idx][1] - row[Quantidade_idx][1], 8)) # Estoque
                # 4.2.2)
                row[Hold_idx] = (row[Hold_idx][0], round(row[Hold_idx][1] + row[Quantidade_idx][1], 8)) # Stake

            elif row[Tipo_idx][1] == "Unhold":
                # 4.2.1) Diminui HoldDe_ ParEsquerdo
                # 4.2.2) Aumenta HoldDe_ ParEsquerdo

                Estoque_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[ParEsquerdo_idx][1]][0]
                Hold_idx = Estoque_idx + 1; Stake_idx = Hold_idx + 1; Custo_idx = Stake_idx + 1; PrecoMedio_idx = Custo_idx + 1
                # 4.2.1)
                row[Estoque_idx] = (row[Estoque_idx][0], round(row[Estoque_idx][1] + row[Quantidade_idx][1], 8)) # Estoque
                # 4.2.2)
                row[Hold_idx] = (row[Hold_idx][0], round(row[Hold_idx][1] - row[Quantidade_idx][1], 8)) # Stake

            # Consideração da Taxa para qualquer tipo de operação
            Estoque_idx = [x for x, y in enumerate(row) if y[0] == 'EstoqueDe¨'+row[MoedaDaTaxa_idx][1]][0]
            Hold_idx = Estoque_idx + 1; Stake_idx = Hold_idx + 1; Custo_idx = Stake_idx + 1; PrecoMedio_idx = Custo_idx + 1
            if not row[Estoque_idx][1] - row[Taxa_idx][1] < 0:
                row[Estoque_idx] = (row[Estoque_idx][0], round(row[Estoque_idx][1] - row[Taxa_idx][1], 8))
            else: # Se não tem o suficiente no estoque padrão pra taxa, tira do Hold pra pagar a taxa
                row[Hold_idx] = (row[Hold_idx][0], round(row[Hold_idx][1] + row[Estoque_idx][1] - row[Taxa_idx][1], 8))
                row[Estoque_idx] = (row[Estoque_idx][0], round(0, 8))
            # Recalcula o Preço Médio da moeda que foi usada na Taxa
            if (row[Estoque_idx][1]+row[Hold_idx][1]+row[Stake_idx][1]) > 0:
                row[PrecoMedio_idx] = (row[PrecoMedio_idx][0], round(row[Custo_idx][1]/(row[Estoque_idx][1]+row[Hold_idx][1]+row[Stake_idx][1]), 8)) # Preço Médio
            else:
                row[PrecoMedio_idx] = (row[PrecoMedio_idx][0], 0) # Preço Médio

            self.AddRowInCurrentDB(TableNameRefinado, row)
            # print(row) # Debug

    def CalcularTributacao(self):
        self.FLAG = True
        self.LW = LoadingWindow.LoadingWindow(self.HMI)
        self.LW.show()
        self.Thread_CalcularTributacao = WorkerThread('Thread_CalcularTributacao', self.HMI)
        self.Thread_CalcularTributacao.start()

    def AtualizarCotacoes(self):
        if not self.HMI.AtualizarCotacoes_running: # Impede mais de um requerimento na atualização de cotações
            self.HMI.Movie_AttCotacoes.start()
            # self.Thread_AtualizarCotacoes = WorkerThread('Thread_AtualizarCotações', self.HMI)
            self.Thread_AtualizarCotacoes = BP(ThreadName='Thread_AtualizarCotações', HMI=self.HMI)
            self.Thread_AtualizarCotacoes.start()

    def AtualizarCotacoes_run(self): # Thread
        # Atualizar tabela de cotações, depois atualizar os valores no HMI
        currency = self.GetUserCoinCurrency()

        corretoras = self.GetCorretoras("Bolsa")
        ativos = []
        thread_list = []
        for corretora in corretoras: ativos.extend(self.GetAtivos(corretora, "Bolsa"))
        ativos = list(dict.fromkeys(ativos))
        for idx, ativo in enumerate(ativos):
            if self.GetModoCotacao(ativo) == "Auto":
                thread_list.append(BP(ThreadName='Thread_GetCotacao', HMI=self.HMI, ativo=ativo, currency=currency))

        corretoras = self.GetCorretoras("Cripto")
        ativos = []
        for corretora in corretoras: ativos.extend(self.GetAtivos(corretora, "Cripto"))
        ativos = list(dict.fromkeys(ativos))
        for ativo in ativos:
            if self.GetModoCotacao(ativo) == "Auto":
                thread_list.append(BP(ThreadName='Thread_GetCotacaoCripto', HMI=self.HMI, ativo=ativo, currency=currency))

        for thread in thread_list:
            # self.HMI.ThreadLock.acquire()
            # print(thread.ThreadName, ' start') # Debug
            # self.HMI.ThreadLock.release()
            thread.start()
        for thread in thread_list:
            # self.HMI.ThreadLock.acquire()
            # print(thread.ThreadName, ' join') # Debug
            # self.HMI.ThreadLock.release()
            thread.join()

        # print('waiting') # Debug
        self.UpdatePatrimonioRendimento()
        # print('UpdatePatrimonioRendimento executed') # Debug

    def UpdatePatrimonioRendimento(self):
        Background_Header = 'rgb(20, 20, 40)'
        try:
            currency = self.GetUserCoinCurrency()
            PatrimonioAux = self.HMI.Calcular.Patrimonio()
            if PatrimonioAux >= 0:
                self.HMI.TextBox_Patrimonio.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: green; border: 1px solid '+Background_Header+'}')
                self.HMI.Patrimonio = PatrimonioAux
                self.HMI.TextBox_Patrimonio.setText(currency+str(self.HMI.Patrimonio))
                Rendimento = self.HMI.Calcular.Rendimento()
                if isinstance(Rendimento, float):
                    self.HMI.Rendimento = Rendimento
                    self.HMI.TextBox_Rendimento.setText(str(self.HMI.Rendimento)+'%')
                    if self.HMI.Rendimento >= 0: self.HMI.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: green; border: 1px solid '+Background_Header+'}')
                    else: self.HMI.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: red; border: 1px solid '+Background_Header+'}')
                else:
                    self.HMI.Rendimento = 0
                    self.HMI.TextBox_Rendimento.setText('...')
                    self.HMI.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: yellow; border: 1px solid '+Background_Header+'}')
            elif PatrimonioAux == -1: # Problema desconhecido, talvez conexão com a internet ou talvez um bug qualquer que na próxima atualização resolve
                self.HMI.Patrimonio = 0
                self.HMI.TextBox_Patrimonio.setText("...")
                self.HMI.TextBox_Patrimonio.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: yellow; border: 1px solid '+Background_Header+'}')
                self.HMI.Rendimento = 0
                self.HMI.TextBox_Rendimento.setText('...')
                self.HMI.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: yellow; border: 1px solid '+Background_Header+'}')
            elif PatrimonioAux == -2: # Tabela de cotações tem algum valor igual a zero
                self.HMI.Patrimonio = 0
                self.HMI.TextBox_Patrimonio.setText("Att cotações")
                self.HMI.TextBox_Patrimonio.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: orange; border: 1px solid '+Background_Header+'}')
                self.HMI.Rendimento = 0
                self.HMI.TextBox_Rendimento.setText('Att cotações')
                self.HMI.TextBox_Rendimento.setStyleSheet('QLineEdit {background-color: '+Background_Header+'; color: orange; border: 1px solid '+Background_Header+'}')
        except Exception as e: print(e)

#%% Verificações de coerência

    def VerificarPrimeiraOperacao(self, ativo='', corretora='', BolsaOuCripto=''):
        Status = False
        if not len(BolsaOuCripto)>0: BolsaOuCripto = self.HMI.BolsaOuCripto
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        if not len(ativo)>0 and BolsaOuCripto == "Bolsa": ativo = self.HMI.ComboBox_Ativo.currentText().replace(" ","_")

        try:
            if BolsaOuCripto == "Bolsa":
                retorno, cursor = self.GetDataDB("SELECT * FROM OPs¨"+ativo+"¨"+corretora+"¨"+BolsaOuCripto+"¨Bruto")
                retorno = retorno[0][1]
                if retorno == "Venda": Status = True

            elif BolsaOuCripto == "Cripto":
                TableName = "OPs¨"+corretora+"¨Cripto¨Bruto"
                retorno, cursor = self.GetDataDB("SELECT * FROM "+TableName)
                retorno = retorno[0][2]
                if not retorno in ["Depósito", "Drop"]: Status = True
        except Exception as e: pass
        finally: return Status

    def VerificarSeTemEstoqueNegativo(self, ativo='', corretora='', BolsaOuCripto=''):
        Status = False
        if not len(BolsaOuCripto)>0: BolsaOuCripto = self.HMI.BolsaOuCripto
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        if not len(ativo)>0 and BolsaOuCripto == "Bolsa": ativo = self.HMI.ComboBox_Ativo.currentText().replace(" ","_")
        if not len(ativo)>0: return False

        try:
            if BolsaOuCripto == "Bolsa":
                retorno, cursor = self.GetDataDB("SELECT * FROM OPs¨"+ativo+"¨"+corretora+"¨"+BolsaOuCripto+"¨Bruto")
                retorno = list(filter(lambda x: x[8]<0, retorno))
                if len(retorno) > 0: Status = True

            elif BolsaOuCripto == "Cripto":
                TableName = "OPs¨"+corretora+"¨Cripto¨Refinado"
                retorno, cursor = self.GetDataDB("SELECT * FROM "+TableName)
                headers = list(map(lambda x: x[0], cursor.description))[13:]
                for idx, head in enumerate(headers):
                    if "EstoqueDe¨" in head:
                        retorno = list(filter(lambda x: x[idx+13]<0 or +x[idx+14]<0 or x[idx+15]<0, retorno))
                        if len(retorno) > 0: Status = True
        except:pass
        finally: return Status

    def VerificarSeTemCustoNegativo(self, ativo='', corretora='', BolsaOuCripto=''):
        Status = False
        if not len(BolsaOuCripto)>0: BolsaOuCripto = self.HMI.BolsaOuCripto
        if not len(corretora)>0: corretora = self.HMI.ComboBox_Corretoras.currentText()
        corretora = corretora.replace(" ","_")
        if not len(ativo)>0 and BolsaOuCripto == "Bolsa": ativo = self.HMI.ComboBox_Ativo.currentText().replace(" ","_")
        if not len(ativo)>0: return False

        try:
            if BolsaOuCripto == "Bolsa":
                retorno, cursor = self.GetDataDB("SELECT * FROM OPs¨"+ativo+"¨"+corretora+"¨"+BolsaOuCripto+"¨Bruto")
                retorno = list(filter(lambda x: x[9]<0, retorno))
                if len(retorno) > 0: Status = True

            elif BolsaOuCripto == "Cripto":
                TableName = "OPs¨"+corretora+"¨Cripto¨Refinado"
                retorno, cursor = self.GetDataDB("SELECT * FROM "+TableName)
                headers = list(map(lambda x: x[0], cursor.description))[13:]
                for idx, head in enumerate(headers):
                    if "EstoqueDe¨" in head:
                        retorno = list(filter(lambda x: x[idx+16]<0, retorno))
                        if len(retorno) > 0: Status = True
        except:pass
        finally: return Status

    #%% Interface DB

    def GetDataDB(self, command, params=''):
        try:
            self.ThreadLock.acquire()
            self.HMI.unsetCursor()
            cursor = self.conn.cursor()
            RETORNO = []
            if params=='': RETORNO = list(cursor.execute(command))
            else: RETORNO = list(cursor.execute(command, params))
        except Exception as e: print("Erro GetDataDB: ",str(e))
        finally: self.ThreadLock.release()
        return RETORNO, cursor

    def ModifyDB(self, command, params=''):
        try:
            self.ThreadLock.acquire()
            self.HMI.unsetCursor()
            cursor = self.conn.cursor()
            # print(command, params)
            if params=='': cursor.execute(command)
            else: cursor.execute(command, params)
            self.conn.commit()
        except Exception as e: print("Erro ModifyDB: ",str(e))
        finally: self.ThreadLock.release()