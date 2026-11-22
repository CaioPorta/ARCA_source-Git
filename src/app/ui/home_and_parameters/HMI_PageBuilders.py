"""
Created on Sun Sep  5 01:44:04 2021

@author: Caio Moreira Porta
"""
import os
import traceback
import _thread
import random
from datetime import datetime, timedelta
from PyQt5.QtGui import QBrush, QColor, QCursor, QIcon, QMovie
from PyQt5.QtWidgets import (QAbstractScrollArea, QComboBox, QHBoxLayout, QLabel,
                             QLineEdit, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import QSize, Qt
from ui.pages import PAGE_BY_NAME


class HMI_PageBuilders:
    def LimparPage(self):
        if self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id, PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id, PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id]:
            self.TextBox_Qqt.setText('')
            self.TextBox_Preco.setText('')
            self.TextBox_Corretagem.setText('')
            if "%" in self.TextBox_TaxaB3.text(): self.DBManager.UpdateTaxa(float(self.TextBox_TaxaB3.text().replace('%','')))
            else: self.TextBox_TaxaB3.setText(self.DBManager.GetTaxaB3Per())
            self.TextBox_Obs.setText('')
            self.TextBox_Qqt.setFocus()
            try: self.Label_Erro1.deleteLater()
            except Exception as e:
                print(e, traceback.format_exception(None, e, e.__traceback__))
        elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id]:
            self.TextBox_Par_Esquerda.setText('')
            self.TextBox_Par_Direita.setText('')
            self.TextBox_Qqt.setText('')
            if self.TipoDeOperacao in ['Compra', 'Venda']: self.TextBox_Preco.setText('')
            else: self.TextBox_Preco.setText('1')
            self.TextBox_Taxa.setText('0')
            self.TextBox_MoedaDaTaxa.setText(self.DBManager.GetUserCoinCurrency())
            self.TextBox_Conversao.setText('1')
            self.TextBox_Obs.setText('')
            self.TextBox_Par_Esquerda.setFocus()
            try: self.Label_Erro1.deleteLater()
            except Exception as e:
                print(e, traceback.format_exception(None, e, e.__traceback__))

    def CreatePage0(self):
        black = 'rgb(0, 0, 0)'
        self.Background_1 = QLabel()
        self.Background_1.setStyleSheet("background-color: "+black)

        self.Background_Entrar = QLabel()
        Background_Entrar = 'rgb(20, 20, 30)'
        self.Background_Entrar.setStyleSheet("background-color: "+Background_Entrar)

        self.Label_Titulo = QLabel()
        self.Label_Titulo.setText('Entrar')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)

        self.Label_NomeDeUsuario = QLabel()
        self.Label_NomeDeUsuario.setText('  Nome de usuário:')
        self.Label_NomeDeUsuario.setStyleSheet('color: white')
        self.Label_NomeDeUsuario.setFont(self.font16)

        self.TextBox_NomeDeUsuario = QLineEdit()
        self.TextBox_NomeDeUsuario.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['MinhaCarteira'].page_id))
        self.TextBox_NomeDeUsuario.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Label_Senha = QLabel()
        self.Label_Senha.setText('  Senha:')
        self.Label_Senha.setStyleSheet('color: white')
        self.Label_Senha.setFont(self.font16)

        self.TextBox_Senha = QLineEdit()
        self.TextBox_Senha.setEchoMode(QLineEdit.Password)
        self.TextBox_Senha.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['MinhaCarteira'].page_id))
        self.TextBox_Senha.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Button_LogIn = QPushButton()
        self.Button_LogIn.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['MinhaCarteira'].page_id))
        self.Button_LogIn.setFont(self.font16)
        self.Button_LogIn.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_LogIn.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.Button_LogIn.setIcon(QIcon("./images/log_in.png"))
        self.Button_LogIn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_LogIn.setStyleSheet("QPushButton {background-color: rgb(20, 120, 30); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_LogIn.setToolTip("Log in")

        self.Button_EsqueciASenha = QPushButton("Esqueci a senha")
        self.Button_EsqueciASenha.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['AuxilioSenha'].page_id))
        self.Button_EsqueciASenha.setFont(self.font12)
        self.Button_EsqueciASenha.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_EsqueciASenha.setToolTip("Esqueci a senha")
        self.Button_EsqueciASenha.setStyleSheet('QToolTip {background-color: black; color: white;border: black solid 1px}')

        self.Button_ImportarUsuario = QPushButton("Importar usuário")
        self.Button_ImportarUsuario.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ImportarUsuario'].page_id))
        # self.Button_ImportarUsuario.pressed.connect(lambda: self.OnButtonPressed('ImportFromDB'))
        self.Button_ImportarUsuario.setFont(self.font12)
        self.Button_ImportarUsuario.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ImportarUsuario.setToolTip("Importar usuário")
        self.Button_ImportarUsuario.setStyleSheet('QToolTip {background-color: black; color: white;border: black solid 1px}')

        self.Button_CriarUsuario = QPushButton("Criar novo usuário")
        self.Button_CriarUsuario.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['CriarUsuario'].page_id))
        self.Button_CriarUsuario.setFont(self.font12)
        self.Button_CriarUsuario.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_CriarUsuario.setToolTip("Criar novo usuário")
        self.Button_CriarUsuario.setStyleSheet('QToolTip {background-color: black; color: white;border: black solid 1px}')

        self.Button_VersionInfo = QPushButton()
        self.Button_VersionInfo.pressed.connect(lambda: QMessageBox.about(self,'Informação', self.APPVersion))
        self.Button_VersionInfo.setIcon(QIcon("./images/Info.png"))
        self.Button_VersionInfo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_VersionInfo.setStyleSheet("QPushButton {background-color: none; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_VersionInfo.setToolTip("Versão")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_Entrar, 0, 0, 20, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 5, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_NomeDeUsuario, 7, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_NomeDeUsuario, 8, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Senha, 9, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Senha, 10, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_LogIn, 11, 0, 2, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_EsqueciASenha, 17, 0, Qt.AlignmentFlag.AlignLeft)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ImportarUsuario, 18, 0, Qt.AlignmentFlag.AlignLeft)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_CriarUsuario, 19, 0, Qt.AlignmentFlag.AlignLeft)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_VersionInfo, 19, 1, Qt.AlignmentFlag.AlignRight)

        self.Gif_Mercado = QLabel()
        self.Movie_Mercado = QMovie("./images/AnaliseDoMercadoGifIcone.gif")
        self.Movie_Mercado.setScaledSize(QSize().scaled(int(self.frameGeometry().width()*3/4*.90),int(self.frameGeometry().height()*3/4*.95), Qt.KeepAspectRatio))
        self.Gif_Mercado.setMovie(self.Movie_Mercado)
        self.Movie_Mercado.start()

        self.Button_MercadoInvisivel = QPushButton()
        self.Button_MercadoInvisivel.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['AnaliseMercado'].page_id))
        self.Button_MercadoInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_MercadoInvisivel.setFixedSize(int(self.frameGeometry().width()*3/4*.90),int(self.frameGeometry().height()*3/4*.95))
        self.Button_MercadoInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_MercadoInvisivel.setToolTip("Ir para aba Mercado")

        self.Button_Mercado = QPushButton("Análise do\nMercado")
        self.Button_Mercado.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['AnaliseMercado'].page_id))
        self.Button_Mercado.setFont(self.font30)
        self.Button_Mercado.setStyleSheet('QPushButton {background-color: black; color: white; border: none; outline: } QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_Mercado.setFixedSize(int(self.frameGeometry().width()*3/4*.9),int(self.frameGeometry().height()/4*.95))
        self.Button_Mercado.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Mercado.setToolTip("Ir para aba Mercado")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 2, 20, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Gif_Mercado, 0, 2, 15, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_MercadoInvisivel, 0, 2, 15, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_Mercado, 15, 2, 5, 1, Qt.AlignmentFlag.AlignCenter)

        self.TextBox_NomeDeUsuario.setFocus()

        self.unsetCursor()

    def CreatePage1(self):
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Background_2 = QLabel()
        Background_2 = 'rgb(0, 0, 0)'
        self.Background_2.setStyleSheet("background-color: "+Background_2)

        self.Background_3 = QLabel()
        Background_3 = 'rgb(0, 0, 0)'
        self.Background_3.setStyleSheet("background-color: "+Background_3)

        self.Background_4 = QLabel()
        Background_4 = 'rgb(0, 0, 0)'
        self.Background_4.setStyleSheet("background-color: "+Background_4)

        self.Label_Titulo = QLabel('Minha carteira')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Gif_Negociações = QLabel()
        self.Movie_Negociações = QMovie("./images/Trade_Icon.gif")
        self.Movie_Negociações.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20), Qt.KeepAspectRatio))
        self.Gif_Negociações.setMovie(self.Movie_Negociações)
        self.Movie_Negociações.start()

        self.Button_Negociações = QPushButton("Negociações")
        self.Button_Negociações.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['EdicaoNegociacoes'].page_id))
        self.Button_Negociações.setFont(self.font24)
        self.Button_Negociações.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_Negociações.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
        self.Button_Negociações.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Negociações.setToolTip("Ir para aba Negociações")

        self.Button_NegociaçõesInvisivel = QPushButton()
        self.Button_NegociaçõesInvisivel.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['EdicaoNegociacoes'].page_id))
        self.Button_NegociaçõesInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_NegociaçõesInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-160))
        self.Button_NegociaçõesInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_NegociaçõesInvisivel.setToolTip("Ir para aba Negociações")

        self.Gif_Tributacao = QLabel()
        self.Movie_Tributacao = QMovie("./images/GIF_Tributacao.gif")
        self.Movie_Tributacao.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20), Qt.KeepAspectRatio))
        self.Gif_Tributacao.setMovie(self.Movie_Tributacao)
        self.Movie_Tributacao.start()

        self.Button_Tributacao = QPushButton("Tributação")
        self.Button_Tributacao.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Tributacao'].page_id))
        self.Button_Tributacao.setFont(self.font24)
        self.Button_Tributacao.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_Tributacao.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
        self.Button_Tributacao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Tributacao.setToolTip("Ir para aba Tributação")

        self.Button_TributacaoInvisivel = QPushButton()
        self.Button_TributacaoInvisivel.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Tributacao'].page_id))
        self.Button_TributacaoInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_TributacaoInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-160))
        self.Button_TributacaoInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_TributacaoInvisivel.setToolTip("Ir para aba Tributação")

        self.Gif_ARCA = QLabel()
        self.Movie_ARCA = QMovie("./images/ArcaGifIcone.gif")
        self.Movie_ARCA.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20), Qt.KeepAspectRatio))
        self.Gif_ARCA.setMovie(self.Movie_ARCA)
        self.Movie_ARCA.start()

        self.Button_ARCA = QPushButton("ARCA")
        self.Button_ARCA.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ARCA'].page_id))
        self.Button_ARCA.setFont(self.font24)
        self.Button_ARCA.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_ARCA.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
        self.Button_ARCA.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ARCA.setToolTip("IR para aba ARCA")

        self.Button_ARCAInvisivel = QPushButton()
        self.Button_ARCAInvisivel.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ARCA'].page_id))
        self.Button_ARCAInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_ARCAInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20))
        self.Button_ARCAInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ARCAInvisivel.setToolTip("Ir para aba ARCA")

        self.Gif_Desempenho = QLabel()
        self.Movie_Desempenho = QMovie("./images/Análise_de_Desempenho_Icon.gif")
        self.Movie_Desempenho.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20), Qt.KeepAspectRatio))
        self.Gif_Desempenho.setMovie(self.Movie_Desempenho)
        self.Movie_Desempenho.start()

        self.Button_Desempenho = QPushButton("Desempenho")
        self.Button_Desempenho.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Desempenho'].page_id))
        self.Button_Desempenho.setFont(self.font24)
        self.Button_Desempenho.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_Desempenho.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
        self.Button_Desempenho.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Desempenho.setToolTip("Ir para aba Desempenho")

        self.Button_DesempenhoInvisivel = QPushButton()
        self.Button_DesempenhoInvisivel.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Desempenho'].page_id))
        self.Button_DesempenhoInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_DesempenhoInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.80),int(self.frameGeometry().height()/5*.95-20))
        self.Button_DesempenhoInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_DesempenhoInvisivel.setToolTip("Ir para aba Desempenho")

        self.Gif_Mercado = QLabel()
        self.Movie_Mercado = QMovie("./images/AnaliseDoMercadoGifIcone.gif")
        self.Movie_Mercado.setScaledSize(QSize().scaled(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-110), Qt.KeepAspectRatio))
        self.Gif_Mercado.setMovie(self.Movie_Mercado)
        self.Movie_Mercado.start()

        self.Button_Mercado = QPushButton("Análise do\nMercado")
        self.Button_Mercado.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['AnaliseMercadoDup'].page_id))
        self.Button_Mercado.setFont(self.font24)
        self.Button_Mercado.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_Mercado.setFixedSize(int(self.frameGeometry().width()/3*.96),int(self.frameGeometry().height()/5))
        self.Button_Mercado.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Mercado.setToolTip("Ir para aba Análise do Mercado")

        self.Button_MercadoInvisivel = QPushButton()
        self.Button_MercadoInvisivel.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['AnaliseMercadoDup'].page_id))
        self.Button_MercadoInvisivel.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_MercadoInvisivel.setFixedSize(int(self.frameGeometry().width()/3*.98),int(self.frameGeometry().height()*4/5-110))
        self.Button_MercadoInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_MercadoInvisivel.setToolTip("Ir para aba Análise do Mercado")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 1, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Background_2, 0, 0, 5, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Background_3, 0, 1, 5, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Background_4, 0, 2, 5, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Gif_Negociações, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_NegociaçõesInvisivel, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_Negociações, 2, 0, 1, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Gif_Tributacao, 3, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_TributacaoInvisivel, 3, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_Tributacao, 4, 0, 1, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Gif_ARCA, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ARCAInvisivel, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ARCA, 2, 1, 1, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Gif_Desempenho, 3, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_DesempenhoInvisivel, 3, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_Desempenho, 4, 1, 1, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Gif_Mercado, 0, 2, 4, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_MercadoInvisivel, 0, 2, 4, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_Mercado, 4, 2, 1, 1)

    def CreatePage2(self):
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Auxílio de senha')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg1 = QLabel('Insira o email associado à sua conta ou o nome de usuário:')
        self.Label_Msg1.setStyleSheet('color: white')
        self.Label_Msg1.setFont(self.font16)
        self.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TextBox_EmailOuUsuario = QLineEdit()
        self.TextBox_EmailOuUsuario.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['RecuperacaoEmail'].page_id))
        self.TextBox_EmailOuUsuario.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Button_ConfirmacaoDeEmail = QPushButton('Seguinte')
        self.Button_ConfirmacaoDeEmail.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['RecuperacaoEmail'].page_id))
        self.Button_ConfirmacaoDeEmail.setFont(self.font16)
        self.Button_ConfirmacaoDeEmail.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_ConfirmacaoDeEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.Button_ConfirmacaoDeEmail.setIcon(QIcon("./images/log_in.png"))
        self.Button_ConfirmacaoDeEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ConfirmacaoDeEmail.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 6, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg1, 9, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_EmailOuUsuario, 10, 0, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ConfirmacaoDeEmail, 12, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter)
        self.TextBox_EmailOuUsuario.setFocus()

    def CreatePage3(self):
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Background_2 = QLabel()
        Background_2 = 'rgb(0, 0, 0)'
        self.Background_2.setStyleSheet("background-color: "+Background_2)

        self.Background_3 = QLabel()
        Background_3 = 'rgb(0, 0, 0)'
        self.Background_3.setStyleSheet("background-color: "+Background_3)

        self.Background_4 = QLabel()
        Background_4 = 'rgb(0, 0, 0)'
        self.Background_4.setStyleSheet("background-color: "+Background_4)

        self.Label_Titulo = QLabel('Importar usuário')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Button_ImportDBToExcel = QPushButton()
        self.Button_ImportDBToExcel.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ImportacaoUsuario'].page_id))
        self.Button_ImportDBToExcel.setStyleSheet('QPushButton {background-color: rgb(0, 0, 0); color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_ImportDBToExcel.setFixedSize(int(self.frameGeometry().width()*2/5),int(self.frameGeometry().height()-160))
        self.Button_ImportDBToExcel.setIconSize(QSize(int(self.frameGeometry().width()*2/5),int(self.frameGeometry().height())))
        self.Button_ImportDBToExcel.setIcon(QIcon("./images/import_from_excel_icon.png"))
        self.Button_ImportDBToExcel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ImportDBToExcel.setToolTip(r"Importar base de dados via arquivo .xlsx")

        self.Button_ImportDBToDB = QPushButton()
        self.Button_ImportDBToDB.pressed.connect(lambda: self.OnButtonPressed('ImportFromDB'))
        self.Button_ImportDBToDB.setStyleSheet('QPushButton {background-color: rgb(0, 0, 0); color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_ImportDBToDB.setFixedSize(int(self.frameGeometry().width()*2/5),int(self.frameGeometry().height()-160))
        self.Button_ImportDBToDB.setIconSize(QSize(int(self.frameGeometry().width()*2/5),int(self.frameGeometry().height())))
        self.Button_ImportDBToDB.setIcon(QIcon("./images/import_from_db_icon.png"))
        self.Button_ImportDBToDB.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ImportDBToDB.setToolTip(r"Importar base de dados via arquivo .db")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_2, 0, 0, 1, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Background_3, 0, 0, 2, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Background_4, 0, 1, 2, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ImportDBToExcel, 1, 0, 2, 1, Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ImportDBToDB, 1, 1, 2, 1, Qt.AlignmentFlag.AlignTop)

    def CreatePage3b(self):
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Importação de usuário')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_NomeDeUsuario = QLabel()
        self.Label_NomeDeUsuario.setStyleSheet('color: white')
        self.Label_NomeDeUsuario.setFont(self.font16)
        self.Label_NomeDeUsuario.setAlignment(Qt.AlignmentFlag.AlignCenter)

        minimo = 24
        maximo = 36
        a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
        b = self.screen_width-(a/minimo)
        razao = (self.frameGeometry().width()-b)/a
        self.Label_NomeDeUsuario.setText('Nome de usuário:'+str((' ')*int(self.frameGeometry().width()*razao)))

        self.TextBox_NomeDeUsuario = QLineEdit()
        self.TextBox_NomeDeUsuario.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailImportar'].page_id))
        self.TextBox_NomeDeUsuario.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Label_Email = QLabel()
        self.Label_Email.setStyleSheet('color: white')
        self.Label_Email.setFont(self.font16)
        self.Label_Email.setAlignment(Qt.AlignmentFlag.AlignCenter)
        minimo = 19
        maximo = 21
        a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
        b = self.screen_width-(a/minimo)
        razao = (self.frameGeometry().width()-b)/a
        self.Label_Email.setText('Email:'+str((' ')*int(self.frameGeometry().width()*razao)))

        self.TextBox_Email = QLineEdit()
        self.TextBox_Email.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailImportar'].page_id))
        self.TextBox_Email.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Label_Senha1 = QLabel()
        self.Label_Senha1.setStyleSheet('color: white')
        self.Label_Senha1.setFont(self.font16)
        self.Label_Senha1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        minimo = 19
        maximo = 21
        a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
        b = self.screen_width-(a/minimo)
        razao = (self.frameGeometry().width()-b)/a
        self.Label_Senha1.setText('Senha:'+str((' ')*int(self.frameGeometry().width()*razao)))

        self.TextBox_Senha1 = QLineEdit()
        self.TextBox_Senha1.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailImportar'].page_id))
        self.TextBox_Senha1.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.TextBox_Senha1.setEchoMode(QLineEdit.Password)

        self.Label_Senha2 = QLabel()
        self.Label_Senha2.setStyleSheet('color: white')
        self.Label_Senha2.setFont(self.font16)
        self.Label_Senha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        minimo = 24
        maximo = 39
        a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
        b = self.screen_width-(a/minimo)
        razao = (self.frameGeometry().width()-b)/a
        self.Label_Senha2.setText('Confirme a senha:'+str((' ')*int(self.frameGeometry().width()*razao)))

        self.TextBox_Senha2 = QLineEdit()
        self.TextBox_Senha2.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailImportar'].page_id))
        self.TextBox_Senha2.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.TextBox_Senha2.setEchoMode(QLineEdit.Password)

        self.ComboBox_Currency = QComboBox()
        self.ComboBox_Currency.setFont(self.font16)
        self.ComboBox_Currency.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.ComboBox_Currency.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(0, 255, 0);")
        for idx, coin in enumerate(self.DBManager.series_BasicInfo_MoedasFiat):
            self.ComboBox_Currency.addItem(coin)

        self.Label_Path = QLabel('Local de armazenamento:')
        self.Label_Path.setStyleSheet('color: white')
        self.Label_Path.setFont(self.font14)
        self.Label_Path.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.Button_PathPadrao = QPushButton('PADRÃO')
        self.Button_PathPadrao.pressed.connect(lambda: self.OnButtonPressed('Path Padrão'))
        self.Button_PathPadrao.setStyleSheet("QPushButton {background-color: green; color: white;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_PathPadrao.setFont(self.font16)
        self.Button_PathPadrao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_PathPadrao.setToolTip(r"Usar o caminho padrão")

        self.Button_PathEspecifico = QPushButton('específico')
        self.Button_PathEspecifico.pressed.connect(lambda: self.OnButtonPressed('Path Específico'))
        self.Button_PathEspecifico.setStyleSheet("QPushButton {background-color: black; color: white;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_PathEspecifico.setFont(self.font16)
        self.Button_PathEspecifico.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_PathEspecifico.setToolTip(r"Informar o caminho específico")

        self.TextBox_Path = QLineEdit()
        self.TextBox_Path.setFixedWidth(int(self.frameGeometry().width()*0.9))
        self.TextBox_Path.setEnabled(False)
        self.TextBox_Path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.TextBox_Path.setStyleSheet("background-color: black; color: white;")

        self.Button_ConfirmacaoDeEmail = QPushButton()
        self.Button_ConfirmacaoDeEmail.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailImportar'].page_id))
        self.Button_ConfirmacaoDeEmail.setFont(self.font16)
        self.Button_ConfirmacaoDeEmail.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_ConfirmacaoDeEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.Button_ConfirmacaoDeEmail.setIcon(QIcon("./images/log_in.png"))
        self.Button_ConfirmacaoDeEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ConfirmacaoDeEmail.setStyleSheet("QPushButton {background-color: rgb(20, 120, 30)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_ConfirmacaoDeEmail.setToolTip(r"Próxima etapa")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 3, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_NomeDeUsuario, 6, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_NomeDeUsuario, 7, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Email, 8, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Email, 9, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Senha1, 10, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Senha1, 11, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Senha2, 12, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Senha2, 13, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.ComboBox_Currency, 14, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Path, 15, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_PathPadrao, 16, 0, Qt.AlignmentFlag.AlignRight)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_PathEspecifico, 16, 1, Qt.AlignmentFlag.AlignLeft)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Path, 17, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ConfirmacaoDeEmail, 18, 0, 2, 2, Qt.AlignmentFlag.AlignCenter)
        self.TextBox_NomeDeUsuario.setFocus()

    def CreatePage4(self):
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Criação de usuário')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_NomeDeUsuario = QLabel()
        self.Label_NomeDeUsuario.setStyleSheet('color: white')
        self.Label_NomeDeUsuario.setFont(self.font16)
        self.Label_NomeDeUsuario.setAlignment(Qt.AlignmentFlag.AlignCenter)

        minimo = 24
        maximo = 36
        a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
        b = self.screen_width-(a/minimo)
        razao = (self.frameGeometry().width()-b)/a
        self.Label_NomeDeUsuario.setText('Nome de usuário:'+str((' ')*int(self.frameGeometry().width()*razao)))

        self.TextBox_NomeDeUsuario = QLineEdit()
        self.TextBox_NomeDeUsuario.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailCriar'].page_id))
        self.TextBox_NomeDeUsuario.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Label_Email = QLabel()
        self.Label_Email.setStyleSheet('color: white')
        self.Label_Email.setFont(self.font16)
        self.Label_Email.setAlignment(Qt.AlignmentFlag.AlignCenter)
        minimo = 19
        maximo = 21
        a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
        b = self.screen_width-(a/minimo)
        razao = (self.frameGeometry().width()-b)/a
        self.Label_Email.setText('Email:'+str((' ')*int(self.frameGeometry().width()*razao)))

        self.TextBox_Email = QLineEdit()
        self.TextBox_Email.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailCriar'].page_id))
        self.TextBox_Email.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Label_Senha1 = QLabel()
        self.Label_Senha1.setStyleSheet('color: white')
        self.Label_Senha1.setFont(self.font16)
        self.Label_Senha1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        minimo = 19
        maximo = 21
        a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
        b = self.screen_width-(a/minimo)
        razao = (self.frameGeometry().width()-b)/a
        self.Label_Senha1.setText('Senha:'+str((' ')*int(self.frameGeometry().width()*razao)))

        self.TextBox_Senha1 = QLineEdit()
        self.TextBox_Senha1.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailCriar'].page_id))
        self.TextBox_Senha1.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.TextBox_Senha1.setEchoMode(QLineEdit.Password)

        self.Label_Senha2 = QLabel()
        self.Label_Senha2.setStyleSheet('color: white')
        self.Label_Senha2.setFont(self.font16)
        self.Label_Senha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        minimo = 24
        maximo = 39
        a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
        b = self.screen_width-(a/minimo)
        razao = (self.frameGeometry().width()-b)/a
        self.Label_Senha2.setText('Confirme a senha:'+str((' ')*int(self.frameGeometry().width()*razao)))

        self.TextBox_Senha2 = QLineEdit()
        self.TextBox_Senha2.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailCriar'].page_id))
        self.TextBox_Senha2.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.TextBox_Senha2.setEchoMode(QLineEdit.Password)

        self.ComboBox_Currency = QComboBox()
        self.ComboBox_Currency.setFont(self.font16)
        self.ComboBox_Currency.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.ComboBox_Currency.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(0, 255, 0);")
        for idx, coin in enumerate(self.DBManager.series_BasicInfo_MoedasFiat):
            self.ComboBox_Currency.addItem(coin)

        self.Label_Path = QLabel('Local de armazenamento:')
        self.Label_Path.setStyleSheet('color: white')
        self.Label_Path.setFont(self.font14)
        self.Label_Path.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.Button_PathPadrao = QPushButton('PADRÃO')
        self.Button_PathPadrao.pressed.connect(lambda: self.OnButtonPressed('Path Padrão'))
        self.Button_PathPadrao.setStyleSheet("QPushButton {background-color: green; color: white;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_PathPadrao.setFont(self.font16)
        self.Button_PathPadrao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_PathPadrao.setToolTip(r"Usar o caminho padrão")

        self.Button_PathEspecifico = QPushButton('específico')
        self.Button_PathEspecifico.pressed.connect(lambda: self.OnButtonPressed('Path Específico'))
        self.Button_PathEspecifico.setStyleSheet("QPushButton {background-color: black; color: white;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_PathEspecifico.setFont(self.font16)
        self.Button_PathEspecifico.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_PathEspecifico.setToolTip(r"Informar o caminho específico")

        self.TextBox_Path = QLineEdit()
        self.TextBox_Path.setFixedWidth(int(self.frameGeometry().width()*0.9))
        self.TextBox_Path.setEnabled(False)
        self.TextBox_Path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.TextBox_Path.setStyleSheet("background-color: black; color: white;")

        self.Button_ConfirmacaoDeEmail = QPushButton()
        self.Button_ConfirmacaoDeEmail.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailCriar'].page_id))
        self.Button_ConfirmacaoDeEmail.setFont(self.font16)
        self.Button_ConfirmacaoDeEmail.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_ConfirmacaoDeEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.Button_ConfirmacaoDeEmail.setIcon(QIcon("./images/log_in.png"))
        self.Button_ConfirmacaoDeEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ConfirmacaoDeEmail.setStyleSheet("QPushButton {background-color: rgb(20, 120, 30)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_ConfirmacaoDeEmail.setToolTip(r"Próxima etapa")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 3, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_NomeDeUsuario, 6, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_NomeDeUsuario, 7, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Email, 8, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Email, 9, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Senha1, 10, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Senha1, 11, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Senha2, 12, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Senha2, 13, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.ComboBox_Currency, 14, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Path, 15, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_PathPadrao, 16, 0, Qt.AlignmentFlag.AlignRight)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_PathEspecifico, 16, 1, Qt.AlignmentFlag.AlignLeft)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Path, 17, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ConfirmacaoDeEmail, 18, 0, 2, 2, Qt.AlignmentFlag.AlignCenter)
        self.TextBox_NomeDeUsuario.setFocus()

    def CreatePage6(self, Email, NomeDeUsuario):
        def Thread(threadname, parametros):
            self.setCursor(Qt.CursorShape.WaitCursor)
            Email, NomeDeUsuario = parametros
            # Geração do código de confirmação
            self.CodigoDeConfirmacaoGerado = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
            self.EnviarEmailDeConfirmacao(Email, NomeDeUsuario, self.CodigoDeConfirmacaoGerado)
            self.unsetCursor()
            self.TextBox_CodigoDeConfirmacao.setFocus()
        _thread.start_new_thread(Thread, ('NiceThread',(Email, NomeDeUsuario)))

        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Confirmação de email')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg1 = QLabel('Mandamos para '+Email[:3]+'***@***'+Email[-4:]+' um código de confirmação da conta.')
        self.Label_Msg1.setStyleSheet('color: white')
        self.Label_Msg1.setFont(self.font16)
        self.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TextBox_CodigoDeConfirmacao = QLineEdit()
        self.TextBox_CodigoDeConfirmacao.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['AlteracaoSenha'].page_id))
        self.TextBox_CodigoDeConfirmacao.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Button_ResendEmail = QPushButton("Reenviar email")
        self.Button_ResendEmail.pressed.connect(lambda: _thread.start_new_thread(Thread, ('NiceThread',(Email, NomeDeUsuario))))
        self.Button_ResendEmail.setFont(self.font12)
        self.Button_ResendEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ResendEmail.setFixedHeight(int(self.frameGeometry().height()/10*.99))
        self.Button_ResendEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9*2/3))
        self.Button_ResendEmail.setToolTip(r"Clique aqui se não recebeu o email")
        self.Button_ResendEmail.setStyleSheet('QToolTip {background-color: black; color: white;border: black solid 1px}')

        self.Button_ConfirmacaoDeEmail = QPushButton('Seguinte')
        self.Button_ConfirmacaoDeEmail.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['AlteracaoSenha'].page_id))
        self.Button_ConfirmacaoDeEmail.setFont(self.font16)
        self.Button_ConfirmacaoDeEmail.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_ConfirmacaoDeEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9*2/3))
        self.Button_ConfirmacaoDeEmail.setIcon(QIcon("./images/log_in.png"))
        self.Button_ConfirmacaoDeEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ConfirmacaoDeEmail.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg1, 9, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_CodigoDeConfirmacao, 10, 0, 1, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ResendEmail, 12, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignRight)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ConfirmacaoDeEmail, 12, 1, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignLeft)
        self.TextBox_CodigoDeConfirmacao.setFocus()

    def CreatePage7(self):
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Alteração de senha')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg1 = QLabel('Digite uma nova senha:')
        self.Label_Msg1.setStyleSheet('color: white')
        self.Label_Msg1.setFont(self.font16)
        self.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TextBox_NovaSenha1 = QLineEdit()
        self.TextBox_NovaSenha1.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['MinhaCarteira'].page_id))
        self.TextBox_NovaSenha1.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.TextBox_NovaSenha1.setEchoMode(QLineEdit.Password)

        self.Label_Msg2 = QLabel('Digite novamente a senha:')
        self.Label_Msg2.setStyleSheet('color: white')
        self.Label_Msg2.setFont(self.font16)
        self.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TextBox_NovaSenha2 = QLineEdit()
        self.TextBox_NovaSenha2.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['MinhaCarteira'].page_id))
        self.TextBox_NovaSenha2.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.TextBox_NovaSenha2.setEchoMode(QLineEdit.Password)

        self.Button_ConfirmacaoDeEmail = QPushButton('Recuperar')
        self.Button_ConfirmacaoDeEmail.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['MinhaCarteira'].page_id))
        self.Button_ConfirmacaoDeEmail.setFont(self.font16)
        self.Button_ConfirmacaoDeEmail.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_ConfirmacaoDeEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.Button_ConfirmacaoDeEmail.setIcon(QIcon("./images/log_in.png"))
        self.Button_ConfirmacaoDeEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ConfirmacaoDeEmail.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 6, 0, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg1, 9, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_NovaSenha1, 10, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg2, 11, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_NovaSenha2, 12, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ConfirmacaoDeEmail, 14, 0, Qt.AlignmentFlag.AlignHCenter)
        self.TextBox_NovaSenha1.setFocus()

    def CreatePage8(self):
        Email = self.TextBox_Email.text()
        NomeDeUsuario = self.TextBox_NomeDeUsuario.text()

        # Envio de email com o código
        def Thread(threadname, parametros):
            self.setCursor(Qt.CursorShape.WaitCursor)
            Email, NomeDeUsuario = parametros
            # Geração do código de confirmação
            self.CodigoDeConfirmacaoGerado = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
            self.EnviarEmailDeConfirmacao(Email, NomeDeUsuario, self.CodigoDeConfirmacaoGerado)
            self.unsetCursor()
            self.TextBox_CodigoDeConfirmacao.setFocus()
        _thread.start_new_thread(Thread, ('NiceThread',(Email, NomeDeUsuario)))

        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Confirmação de email')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg1 = QLabel('Mandamos para '+Email[:3]+'***@***'+Email[-4:]+' um código de confirmação da conta.')
        self.Label_Msg1.setStyleSheet('color: white')
        self.Label_Msg1.setFont(self.font16)
        self.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg2 = QLabel('Insira no campo abaixo o código de confirmação:')
        self.Label_Msg2.setStyleSheet('color: white')
        self.Label_Msg2.setFont(self.font16)
        self.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TextBox_CodigoDeConfirmacao = QLineEdit()
        self.TextBox_CodigoDeConfirmacao.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['MinhaCarteira'].page_id))
        self.TextBox_CodigoDeConfirmacao.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Button_ResendEmail = QPushButton("Reenviar email")
        self.Button_ResendEmail.pressed.connect(lambda: _thread.start_new_thread(Thread, ('NiceThread',(Email, NomeDeUsuario))))
        self.Button_ResendEmail.setFont(self.font12)
        self.Button_ResendEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ResendEmail.setFixedHeight(int(self.frameGeometry().height()/10*.99))
        self.Button_ResendEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9*2/3))
        self.Button_ResendEmail.setToolTip(r"Clique aqui se não recebeu o email")
        self.Button_ResendEmail.setStyleSheet('QToolTip {background-color: black; color: white;border: black solid 1px}')

        self.Button_ConfirmacaoDeEmail = QPushButton('Confirmar')
        self.Button_ConfirmacaoDeEmail.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['MinhaCarteira'].page_id))
        self.Button_ConfirmacaoDeEmail.setFont(self.font16)
        self.Button_ConfirmacaoDeEmail.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_ConfirmacaoDeEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9*2/3))
        self.Button_ConfirmacaoDeEmail.setIcon(QIcon("./images/log_in.png"))
        self.Button_ConfirmacaoDeEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ConfirmacaoDeEmail.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg1, 8, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg2, 10, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_CodigoDeConfirmacao, 11, 0, 1, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ResendEmail, 13, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignRight)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ConfirmacaoDeEmail, 13, 1, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignLeft)
        self.TextBox_CodigoDeConfirmacao.setFocus()

    def CreatePage8b(self):
        Email = self.TextBox_Email.text()
        NomeDeUsuario = self.TextBox_NomeDeUsuario.text()

        # Envio de email com o código
        def Thread(threadname, parametros):
            self.setCursor(Qt.CursorShape.WaitCursor)
            Email, NomeDeUsuario = parametros
            # Geração do código de confirmação
            self.CodigoDeConfirmacaoGerado = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
            self.EnviarEmailDeConfirmacao(Email, NomeDeUsuario, self.CodigoDeConfirmacaoGerado)
            self.unsetCursor()
            self.TextBox_CodigoDeConfirmacao.setFocus()
        _thread.start_new_thread(Thread, ('NiceThread',(Email, NomeDeUsuario)))

        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Confirmação de email')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg1 = QLabel('Mandamos para '+Email[:3]+'***@***'+Email[-4:]+' um código de confirmação da conta.')
        self.Label_Msg1.setStyleSheet('color: white')
        self.Label_Msg1.setFont(self.font16)
        self.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg2 = QLabel('Insira no campo abaixo o código de confirmação:')
        self.Label_Msg2.setStyleSheet('color: white')
        self.Label_Msg2.setFont(self.font16)
        self.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TextBox_CodigoDeConfirmacao = QLineEdit()
        self.TextBox_CodigoDeConfirmacao.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ImportandoDadosExcel'].page_id))
        self.TextBox_CodigoDeConfirmacao.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Button_ResendEmail = QPushButton("Reenviar email")
        self.Button_ResendEmail.pressed.connect(lambda: _thread.start_new_thread(Thread, ('NiceThread',(Email, NomeDeUsuario))))
        self.Button_ResendEmail.setFont(self.font12)
        self.Button_ResendEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ResendEmail.setFixedHeight(int(self.frameGeometry().height()/10*.99))
        self.Button_ResendEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9*2/3))
        self.Button_ResendEmail.setToolTip(r"Clique aqui se não recebeu o email")
        self.Button_ResendEmail.setStyleSheet('QToolTip {background-color: black; color: white;border: black solid 1px}')

        self.Button_ConfirmacaoDeEmail = QPushButton('Confirmar')
        self.Button_ConfirmacaoDeEmail.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ImportandoDadosExcel'].page_id))
        self.Button_ConfirmacaoDeEmail.setFont(self.font16)
        self.Button_ConfirmacaoDeEmail.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_ConfirmacaoDeEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9*2/3))
        self.Button_ConfirmacaoDeEmail.setIcon(QIcon("./images/log_in.png"))
        self.Button_ConfirmacaoDeEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ConfirmacaoDeEmail.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg1, 8, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg2, 10, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_CodigoDeConfirmacao, 11, 0, 1, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ResendEmail, 13, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignRight)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ConfirmacaoDeEmail, 13, 1, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignLeft)
        self.TextBox_CodigoDeConfirmacao.setFocus()

    def CreatePageImportFromExcel(self):
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Importando dados do excel')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.OnButtonPressed('ImportFromExcel')

    def CreatePage9(self):
        try:
            self.ComboBox_Ativos.setEnabled(False)
            self.ComboBox_Ativos.deleteLater()
        except:pass
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Background_2 = QLabel()
        Background_2 = 'rgb(0, 0, 0)'
        self.Background_2.setStyleSheet("background-color: "+Background_2)

        self.Background_3 = QLabel()
        Background_3 = 'rgb(0, 0, 0)'
        self.Background_3.setStyleSheet("background-color: "+Background_3)

        self.Background_4 = QLabel()
        Background_4 = 'rgb(0, 0, 0)'
        self.Background_4.setStyleSheet("background-color: "+Background_4)

        self.Label_Titulo1 = QLabel('Perfil')
        self.Label_Titulo1.setStyleSheet('color: white')
        self.Label_Titulo1.setFont(self.font30)
        self.Label_Titulo1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Button_ProfilePhoto = QPushButton()
        self.Button_ProfilePhoto.pressed.connect(lambda: self.OnButtonPressed("ChangeProfilePhoto"))
        if os.path.exists(os.getcwd()+"\\images\\ProfilePhoto_"+self.User+".jpg"):
            self.Button_ProfilePhoto.setIcon(QIcon("./images/ProfilePhoto_"+self.User+".jpg"))
        else:
            self.Button_ProfilePhoto.setIcon(QIcon("./images/ProfilePhoto.jpg"))
        self.Button_ProfilePhoto.setFixedSize(int(self.frameGeometry().width()/8),int(self.frameGeometry().width()/8))
        self.Button_ProfilePhoto.setIconSize(QSize(int(self.frameGeometry().width()/8*.95),int(self.frameGeometry().width()/8*.95)))
        self.Button_ProfilePhoto.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ProfilePhoto.setToolTip(r"Clique aqui para escolher uma foto")
        self.Button_ProfilePhoto.setStyleSheet('QToolTip {background-color: black; color: white;border: black solid 1px}')

        self.Label_UserEmail = QLabel()
        self.Label_UserEmail.setText(self.User+'\n'+self.Email)
        self.Label_UserEmail.setStyleSheet('color: white')
        self.Label_UserEmail.setFont(self.font12)
        self.Label_UserEmail.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Button_MudarEmail = QPushButton("Mudar o email")
        self.Button_MudarEmail.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['MudarEmail'].page_id))
        self.Button_MudarEmail.setStyleSheet('background-color: rgb(10, 10, 20); color: white')
        self.Button_MudarEmail.setFont(self.font12)
        self.Button_MudarEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.Button_MudarSenha = QPushButton("Mudar a senha")
        self.Button_MudarSenha.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['MudarSenha'].page_id))
        self.Button_MudarSenha.setStyleSheet('background-color: rgb(10, 10, 20); color: white')
        self.Button_MudarSenha.setFont(self.font12)
        self.Button_MudarSenha.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.Button_MudarPath = QPushButton("Mudar o caminho")
        self.Button_MudarPath.pressed.connect(lambda: self.OnButtonPressed('Change UserPath'))
        self.Button_MudarPath.setStyleSheet('background-color: rgb(10, 10, 20); color: white')
        self.Button_MudarPath.setFont(self.font12)
        self.Button_MudarPath.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.Button_EndAccount = QPushButton('Encerrar a conta')
        self.Button_EndAccount.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmarEncerrarConta'].page_id))
        self.Button_EndAccount.setStyleSheet('background-color: rgb(20, 10, 10); color: white')
        self.Button_EndAccount.setFixedHeight(40)
        self.Button_EndAccount.setIconSize(QSize(35, 35))
        self.Button_EndAccount.setIcon(QIcon("./images/closeAccount_icon.png"))
        self.Button_EndAccount.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.Button_VersionInfo = QPushButton()
        self.Button_VersionInfo.pressed.connect(lambda: QMessageBox.about(self,'Informação', self.APPVersion+"\n\nCaminho do usuário:\n"+self.DBManager.UserPath+"/"+self.User+".db"))
        self.Button_VersionInfo.setIcon(QIcon("./images/Info.png"))
        self.Button_VersionInfo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_VersionInfo.setStyleSheet("QPushButton {background-color: black; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_VersionInfo.setToolTip(r"Versão")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 10, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo1, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ProfilePhoto, 2, 0, 2, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_UserEmail, 4, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_MudarEmail, 5, 0, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_MudarSenha, 6, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_MudarPath, 7, 0, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_EndAccount, 9, 0, 1, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_VersionInfo, 9, 0, Qt.AlignmentFlag.AlignRight)

        self.InsertGridLayout(1, 3, 1, 17)

        self.Label_Titulo2 = QLabel('Exportar Base de Dados')
        self.Label_Titulo2.setStyleSheet('color: white')
        self.Label_Titulo2.setFont(self.font30)
        self.Label_Titulo2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Button_ExportDBToExcel = QPushButton()
        self.Button_ExportDBToExcel.pressed.connect(lambda: self.OnButtonPressed('ExportToExcel'))
        self.Button_ExportDBToExcel.setStyleSheet('QPushButton {background-color: rgb(0, 0, 0); color: white; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_ExportDBToExcel.setFixedSize(int(self.frameGeometry().width()*2/5),int(self.frameGeometry().height()-160))
        self.Button_ExportDBToExcel.setIconSize(QSize(int(self.frameGeometry().width()*2/5),int(self.frameGeometry().height())))
        self.Button_ExportDBToExcel.setIcon(QIcon("./images/export_to_excel_icon.png"))
        self.Button_ExportDBToExcel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ExportDBToExcel.setToolTip(r"Exportar base de dados no formato .xlsx")

        self.Button_ExportDBToDB = QPushButton()
        self.Button_ExportDBToDB.pressed.connect(lambda: self.OnButtonPressed('ExportToDB'))
        self.Button_ExportDBToDB.setStyleSheet('QPushButton {background-color: rgb(0, 0, 0); color: white; border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.Button_ExportDBToDB.setFixedSize(int(self.frameGeometry().width()*2/5),int(self.frameGeometry().height()-160))
        self.Button_ExportDBToDB.setIconSize(QSize(int(self.frameGeometry().width()*2/5),int(self.frameGeometry().height())))
        self.Button_ExportDBToDB.setIcon(QIcon("./images/export_to_db_icon.png"))
        self.Button_ExportDBToDB.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ExportDBToDB.setToolTip(r"Exportar base de dados no formato .db")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_2, 0, 0, 1, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Background_3, 0, 0, 2, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Background_4, 0, 1, 2, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo2, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ExportDBToExcel, 1, 0, 2, 1, Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ExportDBToDB, 1, 1, 2, 1, Qt.AlignmentFlag.AlignTop)

    def CreatePage14(self):
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Alteração de email')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg1 = QLabel('Seu email atual é o\n'+self.Email[:3]+'***@***'+self.Email[-4:])
        self.Label_Msg1.setStyleSheet('color: white')
        self.Label_Msg1.setFont(self.font16)
        self.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg2 = QLabel('Digite o seu novo email:')
        self.Label_Msg2.setStyleSheet('color: white')
        self.Label_Msg2.setFont(self.font16)
        self.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TextBox_Email = QLineEdit()
        self.TextBox_Email.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailPosMudanca'].page_id))
        self.TextBox_Email.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Button_ConfirmacaoDeEmail = QPushButton('Seguinte')
        self.Button_ConfirmacaoDeEmail.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['ConfirmacaoEmailPosMudanca'].page_id))
        self.Button_ConfirmacaoDeEmail.setFont(self.font16)
        self.Button_ConfirmacaoDeEmail.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_ConfirmacaoDeEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.Button_ConfirmacaoDeEmail.setIcon(QIcon("./images/log_in.png"))
        self.Button_ConfirmacaoDeEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ConfirmacaoDeEmail.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 6, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg1, 8, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg2, 9, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Email, 10, 0, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ConfirmacaoDeEmail, 12, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter)
        self.TextBox_Email.setFocus()

    def CreatePage15(self):
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Alteração de senha')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_SenhaAtual = QLabel()
        self.Label_SenhaAtual.setStyleSheet('color: white')
        self.Label_SenhaAtual.setFont(self.font16)
        self.Label_SenhaAtual.setAlignment(Qt.AlignmentFlag.AlignLeft)
        minimo = 24
        maximo = 43
        a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
        b = self.screen_width-(a/minimo)
        razao = (self.frameGeometry().width()-b)/a
        self.Label_SenhaAtual.setText('Insira a senha atual:'+str((' ')*int(self.frameGeometry().width()*razao)))

        self.TextBox_SenhaAtual = QLineEdit()
        self.TextBox_SenhaAtual.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Perfil_'].page_id))
        self.TextBox_SenhaAtual.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.TextBox_SenhaAtual.setEchoMode(QLineEdit.Password)

        self.Label_Senha1 = QLabel()
        self.Label_Senha1.setStyleSheet('color: white')
        self.Label_Senha1.setFont(self.font16)
        self.Label_Senha1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        minimo = 24
        maximo = 47
        a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
        b = self.screen_width-(a/minimo)
        razao = (self.frameGeometry().width()-b)/a
        self.Label_Senha1.setText('Crie uma nova senha:'+str((' ')*int(self.frameGeometry().width()*razao)))

        self.TextBox_Senha1 = QLineEdit()
        self.TextBox_Senha1.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Perfil_'].page_id))
        self.TextBox_Senha1.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.TextBox_Senha1.setEchoMode(QLineEdit.Password)

        self.Label_Senha2 = QLabel()
        self.Label_Senha2.setStyleSheet('color: white')
        self.Label_Senha2.setFont(self.font16)
        self.Label_Senha2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        minimo = 23
        maximo = 43
        a = (int(self.screen_width*0.5))/((1/minimo)-(1/maximo))
        b = self.screen_width-(a/minimo)
        razao = (self.frameGeometry().width()-b)/a
        self.Label_Senha2.setText('Confirme a senha:'+str((' ')*int(self.frameGeometry().width()*razao)))

        self.TextBox_Senha2 = QLineEdit()
        self.TextBox_Senha2.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Perfil_'].page_id))
        self.TextBox_Senha2.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.TextBox_Senha2.setEchoMode(QLineEdit.Password)

        self.Button_Alterar = QPushButton()
        self.Button_Alterar.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Perfil_'].page_id))
        self.Button_Alterar.setFont(self.font16)
        self.Button_Alterar.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_Alterar.setFixedWidth(int(self.frameGeometry().width()/3*0.9))
        self.Button_Alterar.setIcon(QIcon("./images/log_in.png"))
        self.Button_Alterar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Alterar.setStyleSheet("QPushButton {background-color: rgb(20, 120, 30)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.Button_Alterar.setToolTip(r"Alterar")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 1)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 3, 0, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_SenhaAtual, 7, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_SenhaAtual, 8, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Senha1, 9, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Senha1, 10, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Senha2, 11, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_Senha2, 12, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_Alterar, 14, 0, 2, 1, Qt.AlignmentFlag.AlignCenter)
        self.TextBox_SenhaAtual.setFocus()

    def CreatePage16(self):
        MessageBox_Msg1 = QMessageBox()
        MessageBox_Msg1.setWindowTitle("Encerrar conta")
        MessageBox_Msg1.setText("Tem certeza que deseja encerrar a sua conta?\n\nNote que esse processo é irreversível!\n")
        MessageBox_Msg1.setIcon(QMessageBox.Warning)
        MessageBox_Msg1.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
        MessageBox_Msg1.setDefaultButton(QMessageBox.Cancel)
        MessageBox_Msg1.setWindowIcon(QIcon(".\\images\\logoARCA.png"))

        returnValue = MessageBox_Msg1.exec()
        if returnValue == QMessageBox.Yes:
            self.CreatePage(PAGE_BY_NAME['ConfirmacaoLogout'].page_id)

        self.unsetCursor()

    def CreatePage17a(self):
        Email = self.TextBox_Email.text().lower()
        NomeDeUsuario = self.DBManager.User
        # Envio de email com o código
        def Thread(threadname, parametros):
            self.setCursor(Qt.CursorShape.WaitCursor)
            Email, NomeDeUsuario = parametros
            # Geração do código de confirmação
            self.CodigoDeConfirmacaoGerado = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
            self.EnviarEmailDeConfirmacao(Email, NomeDeUsuario, self.CodigoDeConfirmacaoGerado)
            self.unsetCursor()
            self.TextBox_CodigoDeConfirmacao.setFocus()
        _thread.start_new_thread(Thread, ('NiceThread', (Email, NomeDeUsuario)))

        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Confirmação de email')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg1 = QLabel('Mandamos para '+Email+' um código de confirmação da conta.')
        self.Label_Msg1.setStyleSheet('color: white')
        self.Label_Msg1.setFont(self.font16)
        self.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg2 = QLabel('Insira no campo abaixo o código de confirmação:')
        self.Label_Msg2.setStyleSheet('color: white')
        self.Label_Msg2.setFont(self.font16)
        self.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TextBox_CodigoDeConfirmacao = QLineEdit()
        self.TextBox_CodigoDeConfirmacao.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Perfil_'].page_id))
        self.TextBox_CodigoDeConfirmacao.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Button_ResendEmail = QPushButton("Reenviar email")
        self.Button_ResendEmail.pressed.connect(lambda: _thread.start_new_thread(Thread, ('NiceThread', (Email, NomeDeUsuario))))
        self.Button_ResendEmail.setFont(self.font12)
        self.Button_ResendEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ResendEmail.setFixedHeight(int(self.frameGeometry().height()/10*.99))
        self.Button_ResendEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9*2/3))
        self.Button_ResendEmail.setToolTip(r"Clique aqui se não recebeu o email")
        self.Button_ResendEmail.setStyleSheet('QToolTip {background-color: black; color: white;border: black solid 1px}')

        self.Button_ConfirmacaoDeEmail = QPushButton('Alterar')
        self.Button_ConfirmacaoDeEmail.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Perfil_'].page_id))
        self.Button_ConfirmacaoDeEmail.setFont(self.font16)
        self.Button_ConfirmacaoDeEmail.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_ConfirmacaoDeEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9*2/3))
        self.Button_ConfirmacaoDeEmail.setIcon(QIcon("./images/log_in.png"))
        self.Button_ConfirmacaoDeEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ConfirmacaoDeEmail.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg1, 8, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg2, 10, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_CodigoDeConfirmacao, 11, 0, 1, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ResendEmail, 13, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignRight)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ConfirmacaoDeEmail, 13, 1, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignLeft)
        self.TextBox_CodigoDeConfirmacao.setFocus()

    def CreatePage17b(self):
        Email = self.Email
        NomeDeUsuario = self.User

        # Envio de email com o código
        def Thread(threadname, parametros):
            self.setCursor(Qt.CursorShape.WaitCursor)
            Email, NomeDeUsuario = parametros
            # Geração do código de confirmação
            self.CodigoDeConfirmacaoGerado = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
            self.EnviarEmailDeConfirmacao(Email, NomeDeUsuario, self.CodigoDeConfirmacaoGerado)
            self.unsetCursor()
            self.TextBox_CodigoDeConfirmacao.setFocus()
        _thread.start_new_thread(Thread, ('NiceThread',(Email, NomeDeUsuario)))

        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Confirmação de email')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg1 = QLabel('Mandamos para '+Email[:3]+'***@***'+Email[-4:]+' um código.\nEssa etapa é só pra ter certeza que é você mesmo que está decidindo encerrar a conta.')
        self.Label_Msg1.setStyleSheet('color: white')
        self.Label_Msg1.setFont(self.font16)
        self.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Label_Msg2 = QLabel('Insira no campo abaixo o código de confirmação:')
        self.Label_Msg2.setStyleSheet('color: white')
        self.Label_Msg2.setFont(self.font16)
        self.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TextBox_CodigoDeConfirmacao = QLineEdit()
        self.TextBox_CodigoDeConfirmacao.returnPressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Home'].page_id))
        self.TextBox_CodigoDeConfirmacao.setFixedWidth(int(self.frameGeometry().width()/3*0.9))

        self.Button_ResendEmail = QPushButton("Reenviar email")
        self.Button_ResendEmail.pressed.connect(lambda: _thread.start_new_thread(Thread, ('NiceThread',(Email, NomeDeUsuario))))
        self.Button_ResendEmail.setFont(self.font12)
        self.Button_ResendEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ResendEmail.setFixedHeight(int(self.frameGeometry().height()/10*.99))
        self.Button_ResendEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9*2/3))
        self.Button_ResendEmail.setToolTip(r"Clique aqui se não recebeu o email")
        self.Button_ResendEmail.setStyleSheet('QToolTip {background-color: black; color: white;border: black solid 1px}')

        self.Button_ConfirmacaoDeEmail = QPushButton('Encerrar conta')
        self.Button_ConfirmacaoDeEmail.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Home'].page_id))
        self.Button_ConfirmacaoDeEmail.setFont(self.font16)
        self.Button_ConfirmacaoDeEmail.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_ConfirmacaoDeEmail.setFixedWidth(int(self.frameGeometry().width()/3*0.9*2/3))
        self.Button_ConfirmacaoDeEmail.setIcon(QIcon("./images/log_in.png"))
        self.Button_ConfirmacaoDeEmail.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_ConfirmacaoDeEmail.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 20, 2)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg1, 8, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg2, 10, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.F_GLayout[self.GCount-1].addWidget(self.TextBox_CodigoDeConfirmacao, 11, 0, 1, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ResendEmail, 13, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignRight)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_ConfirmacaoDeEmail, 13, 1, 2, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignLeft)
        self.TextBox_CodigoDeConfirmacao.setFocus()

    def CreatePage45(self):
        self.Background_1 = QLabel()
        Background_1 = 'rgb(0, 0, 0)'
        self.Background_1.setStyleSheet("background-color: "+Background_1)

        self.Label_Titulo = QLabel('Inserção das cotações manualmente')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Button_Update = QPushButton('Update')
        self.Button_Update.setFont(self.font22)
        self.Button_Update.setIconSize(QSize(int(self.frameGeometry().height() / 10 * 0.9), int(self.frameGeometry().height() / 10 * 0.9)))
        self.Button_Update.setIcon(QIcon("./images/update.png"))
        self.Button_Update.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Update.setStyleSheet("background-color: rgb(120, 120, 120)")
        self.Button_Update.pressed.connect(lambda: self.OnButtonPressed('RemoveUnusedAtivosFromCotacoes'))

        self.Button_Pronto = QPushButton('Pronto')
        self.Button_Pronto.setFont(self.font22)
        self.Button_Pronto.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_Pronto.setIcon(QIcon("./images/log_in.png"))
        self.Button_Pronto.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Pronto.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.Button_Voltar = QPushButton('Voltar')
        self.Button_Voltar.setFont(self.font22)
        self.Button_Voltar.setIconSize(QSize(int(self.frameGeometry().height()/10*0.9),int(self.frameGeometry().height()/10*0.9)))
        self.Button_Voltar.setIcon(QIcon("./images/voltar.png"))
        self.Button_Voltar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Button_Voltar.setStyleSheet("background-color: rgb(120, 20, 30)")
        self.Button_Voltar.pressed.connect(lambda: self.CreatePage(self.PageID))

        self.F_GLayout[self.GCount-1].addWidget(self.Background_1, 0, 0, 6, 4)
        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 0, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_Update, 1, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.F_GLayout[self.GCount-1].addWidget(self.Button_Pronto, 2, 3, 2, 1, Qt.AlignmentFlag.AlignCenter)

        Ativos, Datas, Valores = self.DBManager.GetCotacoesManuais()
        if len(Ativos)>0:
            self.Button_Pronto.pressed.connect(lambda: self.OnButtonPressed('Atualizar Tabela de Cotações'))
            self.F_GLayout[self.GCount-1].addWidget(self.Button_Voltar, 4, 3, 2, 1, Qt.AlignmentFlag.AlignCenter)
            HHeader = ['Ativo',
                       'Última atualização',
                       'Cotação em '+self.DBManager.GetUserCoinCurrency()]
            self.Table_CotaçõesManuaisHeader = QTableWidget()
            self.Table_CotaçõesManuaisHeader.setVisible(False)
            self.Table_CotaçõesManuaisHeader.setShowGrid(False)
            self.Table_CotaçõesManuaisHeader.setFont(self.font20)
            self.Table_CotaçõesManuaisHeader.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                            color: white;
                                                                            border: 1px solid rgba(0, 0, 0, 0);}
                                                              QTableView {border-top: 2px solid white;
                                                                          border-right: 2px dashed white;
                                                                          border-left: 2px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
            self.Table_CotaçõesManuaisHeader.setRowCount(1)
            self.Table_CotaçõesManuaisHeader.setColumnCount(3)
            self.Table_CotaçõesManuaisHeader.verticalHeader().hide()
            self.Table_CotaçõesManuaisHeader.horizontalHeader().hide()

            celula0 = QTableWidgetItem(str(HHeader[0]))
            celula0.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            celula0.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            self.Table_CotaçõesManuaisHeader.setItem(0, 0, celula0)
            celula1 = QTableWidgetItem(str(HHeader[1]))
            celula1.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            celula1.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            self.Table_CotaçõesManuaisHeader.setItem(0, 1, celula1)
            celula2 = QTableWidgetItem(str(HHeader[2]))
            celula2.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
            celula2.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            self.Table_CotaçõesManuaisHeader.setItem(0, 2, celula2)

            self.Table_CotaçõesManuaisHeader.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            self.Table_CotaçõesManuaisHeader.setFixedHeight(int(self.frameGeometry().height()*1/20))
            self.Table_CotaçõesManuaisHeader.resizeColumnsToContents()

            self.Table_CotaçõesManuais = QTableWidget()
            self.Table_CotaçõesManuais.setVisible(False)
            self.Table_CotaçõesManuais.setShowGrid(False)
            self.Table_CotaçõesManuais.setFont(self.font16)
            self.Table_CotaçõesManuais.setStyleSheet('''QTableWidget {background-color: rgb(0, 0, 0);
                                                                      color: white;
                                                                      border: 1px solid rgba(0, 0, 0, 0);}
                                                        QTableView {border-bottom: 2px dashed white;
                                                                    border-right: 1px solid white;
                                                                    border-left: 1px solid white;}
                                                        QTableView::item {border-bottom: 1px dashed white;}''') # gridline-color: rgba(255, 255, 255, 0)
            self.Table_CotaçõesManuais.setRowCount(len(Datas))
            self.Table_CotaçõesManuais.setColumnCount(3)
            self.Table_CotaçõesManuais.verticalHeader().hide()
            self.Table_CotaçõesManuais.horizontalHeader().hide()

            for n, item in enumerate(Ativos):
                it = QTableWidgetItem(str(item))
                it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
                it.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.Table_CotaçõesManuais.setItem(n, 0, it)

            for n, item in enumerate(Datas):
                it = QTableWidgetItem(str(item))
                it.setFlags(Qt.ItemFlags(Qt.ItemFlag.ItemIsSelectable))
                it.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                item = datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
                if datetime.now() - item <= timedelta(days=2): it.setForeground(QBrush(QColor('green')))
                elif datetime.now() - item <= timedelta(days=5): it.setForeground(QBrush(QColor('orange')))
                else: it.setForeground(QBrush(QColor('red')))
                self.Table_CotaçõesManuais.setItem(n, 1, it)

            for n, item in enumerate(Valores):
                it = QTableWidgetItem(str(item))
                it.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                if item <= 0: it.setForeground(QBrush(QColor('red')))
                self.Table_CotaçõesManuais.setItem(n, 2, it)

            self.data_45_1 = []
            for i, item in enumerate(Datas):
                self.data_45_1.append((Ativos[i], Datas[i], Valores[i]))

            self.Table_CotaçõesManuais.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            self.Table_CotaçõesManuais.setFixedHeight(int(self.frameGeometry().height()*6/10))
            self.Table_CotaçõesManuais.resizeColumnsToContents()

            SizeCol0, SizeCol1, SizeCol2 = self.GetSizeOfTableColumns(self.data_45_1, HHeader)

            self.SetTableWidth_45_1(SizeCol0, SizeCol1, SizeCol2)

            self.F_GLayout[self.GCount-1].addWidget(self.Table_CotaçõesManuaisHeader, 1, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            self.F_GLayout[self.GCount-1].addWidget(self.Table_CotaçõesManuais, 2, 0, 3, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        else:
            self.Label_Msg1 = QLabel('Legal!\nEstá tudo no automático pra você!\nNão há nada para fazer aqui :)')
            self.Label_Msg1.setStyleSheet('color: white')
            self.Label_Msg1.setFont(self.font24)
            self.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.F_GLayout[self.GCount-1].addWidget(self.Label_Msg1, 1, 0, 2, 3, Qt.AlignmentFlag.AlignCenter)

            self.Button_Pronto.pressed.connect(lambda: self.CreatePage(self.PageID))

            self.Button_Joinha = QPushButton()
            self.Button_Joinha.setFixedSize(300,300)
            self.Button_Joinha.setIconSize(QSize(295, 295))
            self.Button_Joinha.setStyleSheet('QPushButton {background-color: black; color: white; border: 1px solid black} QToolTip {background-color: black; color: white;border: black solid 1px}')
            self.Button_Joinha.setIcon(QIcon("./images/Joinha.png"))
            self.Button_Joinha.setToolTip(r"Ok")
            self.F_GLayout[self.GCount-1].addWidget(self.Button_Joinha, 3, 0, 2, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

    def CreatePageChooseCurrency(self):
        self.Label_Titulo = QLabel('Escolha a sua moeda corrente')
        self.Label_Titulo.setStyleSheet('color: white')
        self.Label_Titulo.setFont(self.font30)
        self.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.F_GLayout[self.GCount-1].addWidget(self.Label_Titulo, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.ComboBox_Currency = QComboBox()
        self.ComboBox_Currency.setFont(self.font16)
        self.ComboBox_Currency.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.ComboBox_Currency.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(0, 255, 0);")
        # self.ComboBox_Currency.activated[str].connect(lambda pct: self.AtualizarPagina())
        for idx, coin in enumerate(self.DBManager.GetMoedasFiat()):
            self.ComboBox_Currency.addItem(coin)

        self.F_GLayout[self.GCount-1].addWidget(self.ComboBox_Currency, 1, 0, 4, 1, Qt.AlignmentFlag.AlignCenter)

    def CreatePageInfo1(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','    Quando um ativo tem o modo manual ativado,\nserá solicitada a sua cotação durante procedimentos\n           que atualizam a Tabela de Cotações.')

    def CreatePageInfo2(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Tipo?\n\nAqui se indica se foi realizada uma operação de compra ou de venda.')

    def CreatePageInfo3(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Data?\n\nAqui se indica quando a operação foi realizada.')

    def CreatePageInfo4(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Qqt (Quantidade)?\n\nAqui se indica quantos papeis do ativo foi comprado ou vendido nessa operação.')

    def CreatePageInfo5(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Preço?\n\nAqui se indica o preço unitário do ativo que foi comprada ou vendida nessa operação.')

    def CreatePageInfo6(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Corretagem?\n\nAqui se indica, em valores brutos, quanto a corretora cobrou para realizar essa operação.')

    def CreatePageInfo7(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Taxa B3?\n\nAqui se indica em valores brutos ou em porcentagem (com o simbolo "%") quanto de taxa que foi cobrada pela B3 para realizar essa operação.')

    def CreatePageInfo8(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Obervação?\n\nAqui se pode deixar qualquer comentário sobre essa operação. Ela não será levada em consideração em cálculo algum.')

    def CreatePageInfo9(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Conversão?\n\nAqui se indica a cotação da segunda moeda no par com relação á sua moeda corrente.\nExemplo: Se o par é BTCUSDT e a sua moeda corrente é BRL, então deve-se indicar o preço de USDTBRL no momento da operação.\nSe o par é BTCBRL e a sua moeda corrente é BRL, então deve-se inserir 1.')

    def CreatePageInfo10(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Moeda da Taxa?\n\nAqui se indica qual moeda foi usada para pagar a taxa. Se não houve taxa, pode deixar vazio.')

    def CreatePageInfo11(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Taxa?\n\nAqui se indica o valor cobrado na taxa, sem converter moedas. O valor será subtraído do seu estoque da Moeda da Taxa.')

    def CreatePageInfo12(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Preço?\n\nAqui se indica o preço unitário do ativo no momento da operação.\nA referência de preço é a mesma do par em questão.\nPor exemplo: Se o par é BTCUSDT e a sua moeda corrente BRL, indique o preço do BTC em USDT. Apenas ignore a sua moeda corrente neste momento.')

    def CreatePageInfo13(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Qqt (Quantidade)?\n\nAqui se indica quantas moedas (ou uma fração dela) foi operada.')

    def CreatePageInfo14(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Tipo?\n\nAqui se indica o que fez com a moeda em questão.\nSe COMPROU, se VENDEU.\nTambém é possível declarar se tal quantidade foi colocada ou retirada de bloqueio (STAKE ou UNSTAKE), se foi segurada ou liberada (HOLD ou UNHOLD), apenas para sua organização. É NECESSÁRIO declarar todos os DEPÓSITOS e SAQUES, assim como ganhos (DROP) e perdas (BURN).\nBurn pode ser multas, roubos, furtos, confisco etc.')

    def CreatePageInfo15(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que inserir em Par?\n\nAqui se indica qual a moeda ou moedas que foram operadas. ATENÇÃO na importãncia da ordem. Veja o seguinte exemplo:\nBTCUSDT COMPRA -> Significa diminuir o estoque de USDT e aumentar o estoque de BTC.\nEm operações de DEPÓSITO, SAQUE, STAKE, UNSTAKE, HOLD, UNHOLD, DROP e BURN admite-se somente uma moeda no par.')

    def CreatePageInfo16(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que é nota de equilíbrio?\n\nNota de equilíbrio é um indicador que avalia a variedade da sua carteira.\nEla leva em consideração o volume nos diferentes\ntipos de ativos, sub-tipos e setores.')

    def CreatePageInfo17(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que é Gasto Mensal?\n\nGasto Mensal é aproximadamente a sua despeza mensal.\nCom esse valor, calcular-se-á o valor\nque deve ser investido ou retirado de investimentos\npara manter uma reserva segura.')

    def CreatePageInfo18(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que é Meses de Reserva?\n\nMeses de Reserva é o tempo que querer que\na sua reserva cubra seus Gastos Mensais em\ncaso de instabilidade econômica pessoal.')

    def CreatePageInfo19(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação',"O que é 'Aplicar'?\n\nÉ o valor calculado para se aplicar ou retirar de investimento.\nA conta é:\n(Patrimônio - MesesDeReserva * GastoMensal) - MontanteNasCorretoras")

    def CreatePageInfo20(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que é Montante Aplicado?\n\nÉ a diferença entre a soma de depósitos e a soma de saques\nefetuados em cada corretora.')

    def CreatePageInfo21(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que é Montante em Aplicação?\n\nÉ a diferença entre o patrimônio nas\ncorretoras e as suas contas-correntes.\nDesconsidera-se os bancos.')

    def CreatePageInfo22(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação',"O que é RNB?\n\nRendimento Nominal Bruto é o rendimento percentual\nsem considerar a tributação.\n\n(MontanteNasCorretoras - Investido) / Investido * 100 (%)\n\nMontanteNasCorretoras = SomaPorCorretora(Conta-Corrente + EstoqueAtivos*Cotação)\nInvestido = SomaPorCorretora(Depósitos totais - Saques totais)")

    def CreatePageInfo23(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação','O que é Patrimônio?\n\nÉ a soma de todos os valores declarados.\nConsidera-se as cotações adquiridas online\nou as cotações informadas na tabela manual\n(Atalho: tecla C).\nNão considera-se o desconto de tributação.')

    def CreatePageInfo24(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação',"                                             Ações e Negócios\n\nNada mais rentável do que negócios.\nAplicação convexa, limite de perda, ganhos infinitos.\n\nO que olhar:\nLucratividade, endividamento, preço, crescimento, governança corporativa.\n\nChecklist:\nP/L; PEG RATIO; P/VP; ROE; ROA; ROIC; MG. BRUTA; MG. LUCRO;\nDL/PL; DL/EBIT; LIQUIDEZ CORRENTE; DIVIDA BRUTA/EBIT;\nCAGR EBIT; CAGR LUCRO; SALDO DOS ACIONISTAS.")

    def CreatePageInfo25(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação',"                                                   Real Estate\n\nRendimentos mensais isentos de imposto de renda para pessoa física.\nFluxo de caixa, efeito bola de neve.\n\nO que olhar:\nTipo de fundo imobiliário, localização, vacância, inquilinos, rendimento por cotas.\n\nChecklist:\nP/VP; NÚMERO DE NEGÓCIOS; VACÂNCIA FINANCEIRA; VACÂNCIA\nFÍSICA; CAP RATE; DIVIDEND YIELD; VALOR DO M2/ALUGUEL.")

    def CreatePageInfo26(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação',"                                                   Caixa\n\nCaixa é a parcela da sua carteira utilizada para aproveitar oportunidades.\nSanidade mental em momentos de crise.\n\nO que olhar:\nAplicações conservadoras, de alta liquidez e baixa/média rentabilidade.\n\nCheclist:\nRATING/RISCO; PRÊMIO X BENCHMARK; PRAZO.")

    def CreatePageInfo27(self): MessageBox_Msg1 = QMessageBox.about(self,'Informação',"                                             Ativos Internacionais\n\nNada mais rentável do que negócios em dólar.\nProteção à crises locais.\n\nO que olhar:\nLucratividade, endividamento, preço, crescimento, governança corporativa.\n\nChecklist:\nP/L; PEG RATIO; P/VP; ROE; ROA; ROIC; MG. BRUTA; MG. LUCRO;\nDL/PL; DL/EBIT; LIQUIDEZ CORRENTE; DIVIDA BRUTA/EBIT;\nCAGR EBIT; CAGR LUCRO; SALDO DOS ACIONISTAS.\n\n                                                 Criptomoedas\n\nExposição de altíssimo risco.\nMuito volátil, aplicação convexa.\n\nDica de estratégia saudável:\n50 a 60% em BTC\n10% em ETH\n10% em BNB\nO restante divide-se nas pimentinhas.")
