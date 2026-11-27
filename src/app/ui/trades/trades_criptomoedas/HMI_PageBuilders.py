# -*- coding: utf-8 -*-
"""
Criptomoedas behaviour split into a single concern.
HMI_PageBuilders - pagebuilders helpers (inherited by the composition root).
"""
from datetime import (datetime)
import traceback
from PyQt5.QtGui import (QCursor, QIcon, QMovie, QDoubleValidator)
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QHBoxLayout,
    QToolTip,
    QMessageBox,
    QTableWidget,
)
from PyQt5.QtCore import (QSize, Qt)
from ui.pages import (PAGE_BY_NAME)


class HMI_PageBuilders:
    def CreatePage19(self): # Edição das negociações em criptomoedas
        self.HMI.BolsaOuCripto = "Cripto" # Variável usada no DBManager

        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        Background_3 = QLabel()
        Background_3.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Edição das negociações em criptomoedas')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Button_AddCorretora = QPushButton()
        self.HMI.Button_AddCorretora.setToolTip("Adicionar corretora")
        self.HMI.Button_AddCorretora.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.HMI.Button_AddCorretora.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['AdicionarCorretoraCripto'].page_id))
        self.HMI.Button_AddCorretora.setFixedSize(40,40)
        self.HMI.Button_AddCorretora.setIconSize(QSize(35, 35))
        self.HMI.Button_AddCorretora.setIcon(QIcon("./images/add_user.png"))
        self.HMI.Button_AddCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_DeleteCorretora = QPushButton()
        self.HMI.Button_DeleteCorretora.setToolTip("Deletar corretora")
        self.HMI.Button_DeleteCorretora.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.HMI.Button_DeleteCorretora.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['ConfirmarDeletarCorretoraCripto'].page_id))
        self.HMI.Button_DeleteCorretora.setFixedSize(40,40)
        self.HMI.Button_DeleteCorretora.setIconSize(QSize(35, 35))
        self.HMI.Button_DeleteCorretora.setIcon(QIcon("./images/delete_broker.png"))
        self.HMI.Button_DeleteCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.ComboBox_Corretoras = QComboBox()
        self.HMI.ComboBox_Corretoras.setFont(self.HMI.font16)
        self.HMI.ComboBox_Corretoras.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.ComboBox_Corretoras.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(255, 255, 255);")
        self.HMI.ComboBox_Corretoras.activated[str].connect(lambda pct: self.HMI.UpdatePage())
        corretoras = self.HMI.DBManager.GetCorretoras(self.HMI.BolsaOuCripto)
        for idx, corretora in enumerate(corretoras):
            self.HMI.ComboBox_Corretoras.addItem(corretora)
            try:
                if getattr(self.HMI, 'TextBox_NovaCorretora', None) is not None and corretora == self.HMI.TextBox_NovaCorretora.text(): self.HMI.idxCorretora = idx
            except Exception as e:
                print(e, traceback.format_exception(None, e, e.__traceback__))
        if self.HMI.idxCorretora < len(corretoras):
            self.HMI.ComboBox_Corretoras.setCurrentIndex(self.HMI.idxCorretora)

        UserCoin = self.HMI.DBManager.GetCorretoraCoinCurrency(self.HMI.BolsaOuCripto, self.HMI.ComboBox_Corretoras.currentText())

        self.HMI.Button_RenameCorretora = QPushButton()
        self.HMI.Button_RenameCorretora.setToolTip("Renomear corretora")
        self.HMI.Button_RenameCorretora.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}")
        self.HMI.Button_RenameCorretora.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['RenomearCorretoraCripto'].page_id))
        self.HMI.Button_RenameCorretora.setFixedSize(40,40)
        self.HMI.Button_RenameCorretora.setIconSize(QSize(35, 35))
        self.HMI.Button_RenameCorretora.setIcon(QIcon("./images/Rename.png"))
        self.HMI.Button_RenameCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Label_Title11 = QLabel()
        self.HMI.Label_Title11.setText('Editar\noperações da')
        self.HMI.Label_Title11.setStyleSheet('color: white')
        self.HMI.Label_Title11.setFont(self.HMI.font24)
        self.HMI.Label_Title11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Title2 = QLabel()
        self.HMI.Label_Title2.setText(self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Title2.setStyleSheet('color: green')
        self.HMI.Label_Title2.setFont(self.HMI.font26)

        self.HMI.Label_Msg1 = QLabel()
        self.HMI.Label_Msg1.setText("Visão geral")
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font22)

        self.HMI.Label_Msg2 = QLabel()
        self.HMI.Label_Msg2.setText("Patrimônio:")
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.TextBox_Msg2 = QLineEdit()
        self.HMI.TextBox_Msg2.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        self.HMI.TextBox_Msg2.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg2.setEnabled(False)
        self.HMI.TextBox_Msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_Msg2.setText(UserCoin+' ~'+str(self.HMI.DBManager.GetPatrimonioTotalCorretora(self.HMI.ComboBox_Corretoras.currentText(),
                                                                                                       self.HMI.BolsaOuCripto,
                                                                                                       )))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg2.setEchoMode(QLineEdit.Password)

        self.HMI.Label_Msg6 = QLabel()
        self.HMI.Label_Msg6.setText("Investido:")
        self.HMI.Label_Msg6.setStyleSheet('color: white')
        self.HMI.Label_Msg6.setFont(self.HMI.font16)
        self.HMI.Label_Msg6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.TextBox_Msg6 = QLineEdit()
        self.HMI.TextBox_Msg6.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        self.HMI.TextBox_Msg6.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg6.setEnabled(False)
        self.HMI.TextBox_Msg6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Investido = round(self.HMI.DBManager.GetTotalInvestidoEmCorretora(self.HMI.ComboBox_Corretoras.currentText(), "Cripto"), 2)
        self.HMI.TextBox_Msg6.setText(UserCoin+' ~'+str(Investido))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg6.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg6.setEchoMode(QLineEdit.Password)

        self.HMI.Label_Msg3 = QLabel()
        self.HMI.Label_Msg3.setText("Conta-Corrente:")
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font16)
        self.HMI.Label_Msg3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.TextBox_Msg3 = QLineEdit()
        self.HMI.TextBox_Msg3.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        self.HMI.TextBox_Msg3.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg3.setEnabled(False)
        self.HMI.TextBox_Msg3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_Msg3.setText(UserCoin+' '+str(self.HMI.DBManager.GetValorEmContaCorrente("Cripto",
                                                                                                  self.HMI.ComboBox_Corretoras.currentText(),
                                                                                                  )))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg3.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg3.setEchoMode(QLineEdit.Password)

        self.HMI.Label_Msg4 = QLabel()
        self.HMI.Label_Msg4.setText("Última operação:")
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font16)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.TextBox_Msg4 = QLabel()
        self.HMI.TextBox_Msg4.setStyleSheet('color: green')
        self.HMI.TextBox_Msg4.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_Msg4.setText(self.HMI.DBManager.GetDataUltimaOPRegistrada(self.HMI.BolsaOuCripto, self.HMI.ComboBox_Corretoras.currentText()))

        self.HMI.Label_Msg5 = QLabel()
        self.HMI.Label_Msg5.setText("Último depósito/saque:")
        self.HMI.Label_Msg5.setStyleSheet('color: white')
        self.HMI.Label_Msg5.setFont(self.HMI.font16)
        self.HMI.Label_Msg5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.TextBox_Msg5 = QLineEdit()
        self.HMI.TextBox_Msg5.setFont(self.HMI.font16)
        self.HMI.TextBox_Msg5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HMI.TextBox_Msg5.setEnabled(False)
        valor = round(self.HMI.DBManager.GetUltimoDepositoOuSaqueRegistrado(self.HMI.ComboBox_Corretoras.currentText()),2)
        if valor >= 0: self.HMI.TextBox_Msg5.setStyleSheet('QLineEdit {background-color: black; color: green;}')
        else: self.HMI.TextBox_Msg5.setStyleSheet('QLineEdit {background-color: black; color: orange;}')
        self.HMI.TextBox_Msg5.setText(UserCoin+' '+str(valor))
        if self.HMI.ShowValues:
            self.HMI.TextBox_Msg5.setEchoMode(QLineEdit.Normal)
        else:
            self.HMI.TextBox_Msg5.setEchoMode(QLineEdit.Password)

        self.HMI.Label_Title3 = QLabel()
        self.HMI.Label_Title3.setText("Editar operações")
        self.HMI.Label_Title3.setStyleSheet('color: white')
        self.HMI.Label_Title3.setFont(self.HMI.font24)

        self.HMI.Gif_AlterarOPCriptomoedas = QLabel()
        self.HMI.Movie_AlterarOPCriptomoedas = QMovie("./images/GIF_Registro.gif")
        self.HMI.Movie_AlterarOPCriptomoedas.setScaledSize(QSize().scaled(int(self.HMI.frameGeometry().width()*12/20),int(self.HMI.frameGeometry().height()*7/10*.95-60), Qt.KeepAspectRatio))
        self.HMI.Gif_AlterarOPCriptomoedas.setMovie(self.HMI.Movie_AlterarOPCriptomoedas)
        self.HMI.Movie_AlterarOPCriptomoedas.start()

        self.HMI.Button_AlterarOPCriptomoedasInvisivel = QPushButton()
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.setToolTip("Alterar operações de criptomoedas")
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['RegistrosCripto'].page_id))
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.setFixedSize(int(self.HMI.frameGeometry().width()*12/20),int(self.HMI.frameGeometry().height()*7/10*.95))
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_AlterarOPCriptomoedas = QPushButton("Registros")
        self.HMI.Button_AlterarOPCriptomoedas.setToolTip("Alterar operações de criptomoedas")
        self.HMI.Button_AlterarOPCriptomoedas.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['RegistrosCripto'].page_id))
        self.HMI.Button_AlterarOPCriptomoedas.setStyleSheet('QPushButton{background-color: black; color: white; border: 1px solid rgb(0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_AlterarOPCriptomoedas.setFont(self.HMI.font16)
        self.HMI.Button_AlterarOPCriptomoedas.setFixedSize(int(self.HMI.frameGeometry().width()*12/20),int(self.HMI.frameGeometry().height()*1/10*.95))
        self.HMI.Button_AlterarOPCriptomoedas.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        if self.HMI.ComboBox_Corretoras.currentText() == '':
            ButtonsEnabled = False
            color = 'red'
        else:
            ButtonsEnabled = True
            color = 'white'
        self.HMI.Button_AlterarOPCriptomoedas.setEnabled(ButtonsEnabled)
        self.HMI.Button_AlterarOPCriptomoedasInvisivel.setEnabled(ButtonsEnabled)
        self.HMI.Button_AlterarOPCriptomoedas.setStyleSheet('background-color: black; color: '+color+'; border: 1px solid rgb(0, 0, 0)')

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.HMI.InsertGridLayout(2, 0, 1, 8)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 0, 0, 15, 4)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AddCorretora, 0, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DeleteCorretora, 1, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_Corretoras, 0, 1, 2, 2, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RenameCorretora, 0, 3, 2, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Title11, 2, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Title2, 3, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 4, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 5, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg2, 6, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg6, 7, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg6, 8, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 9, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg3, 10, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 11, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg4, 12, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 13, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_Msg5, 14, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.HMI.InsertGridLayout(2, 8, 1, 12)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_3, 0, 0, 5, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Title3, 0, 0, 3, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Gif_AlterarOPCriptomoedas, 1, 0, 3, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AlterarOPCriptomoedasInvisivel, 1, 0, 3, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AlterarOPCriptomoedas, 4, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        if len(corretoras) == 0:
            self.HMI.Button_RenameCorretora.setEnabled(False)
            self.HMI.Button_DeleteCorretora.setEnabled(False)


    def CreatePage37(self): # Adicionar nova corretora de criptomoedas
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Adicionar nova corretora de criptomoedas')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Insira o nome da nova corretora:')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font16)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.TextBox_NovaCorretora = QLineEdit()
        self.HMI.TextBox_NovaCorretora.returnPressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['EdicaoNegociacoesCripto_'].page_id))
        self.HMI.TextBox_NovaCorretora.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))

        self.HMI.Label_Msg2 = QLabel('Moeda Corrente:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.ComboBox_Currency = QComboBox()
        self.HMI.ComboBox_Currency.setFont(self.HMI.font16)
        self.HMI.ComboBox_Currency.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.ComboBox_Currency.setStyleSheet("background-color: rgb(10, 10, 10) ; color: rgb(0, 255, 0);")
        idxUserCoin = 0
        UserCoin = self.HMI.DBManager.GetUserCoinCurrency()
        for idx, coin in enumerate(self.HMI.DBManager.GetMoedasFiat()):
            self.HMI.ComboBox_Currency.addItem(coin)
            if coin == UserCoin: idxUserCoin = idx
        self.HMI.ComboBox_Currency.setCurrentIndex(idxUserCoin)

        self.HMI.Button_AdicionarCorretora = QPushButton('Seguinte')
        self.HMI.Button_AdicionarCorretora.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['EdicaoNegociacoesCripto_'].page_id))
        self.HMI.Button_AdicionarCorretora.setFont(self.HMI.font16)
        self.HMI.Button_AdicionarCorretora.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_AdicionarCorretora.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_AdicionarCorretora.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_AdicionarCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_AdicionarCorretora.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 19, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 7, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_NovaCorretora, 8, 0, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 10, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.ComboBox_Currency, 11, 0, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AdicionarCorretora, 12, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter)
        self.HMI.TextBox_NovaCorretora.setFocus()


    def CreatePage38(self): # Deletar corretora
        MessageBox_Msg1 = QMessageBox()
        MessageBox_Msg1.setWindowTitle("Deletar corretora (cripto)")
        MessageBox_Msg1.setText("Tem certeza que deseja deletar a "+self.HMI.ComboBox_Corretoras.currentText())
        MessageBox_Msg1.setIcon(QMessageBox.Question)
        MessageBox_Msg1.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
        MessageBox_Msg1.setDefaultButton(QMessageBox.Cancel)
        MessageBox_Msg1.setWindowIcon(QIcon(".\\images\\logoARCA.png"))

        returnValue = MessageBox_Msg1.exec()
        if returnValue == QMessageBox.Yes:
            self.HMI.DBManager.DeleteCorretora(self.HMI.BolsaOuCripto, self.HMI.ComboBox_Corretoras.currentText())
            self.HMI.HMI_ARCA.Flag_RecalcularGraficos = True
            self.HMI.CreatePage(PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id)


    def CreatePage39(self): # Renomear corretora de criptomoedas
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)

        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Renomear corretora de criptomoedas')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Renomear corretora \n'+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font22)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Msg2 = QLabel('Insira o novo nome da corretora:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font16)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.TextBox_NovoNomeCorretora = QLineEdit()
        self.HMI.TextBox_NovoNomeCorretora.returnPressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['EdicaoNegociacoesCripto_'].page_id))
        self.HMI.TextBox_NovoNomeCorretora.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))

        self.HMI.Button_RenomearCorretora = QPushButton('Seguinte')
        self.HMI.Button_RenomearCorretora.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['EdicaoNegociacoesCripto_'].page_id))
        self.HMI.Button_RenomearCorretora.setFont(self.HMI.font16)
        self.HMI.Button_RenomearCorretora.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_RenomearCorretora.setFixedWidth(int(self.HMI.frameGeometry().width()/3*0.9))
        self.HMI.Button_RenomearCorretora.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_RenomearCorretora.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_RenomearCorretora.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 19, 1)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 7, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 9, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.TextBox_NovoNomeCorretora, 10, 0, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RenomearCorretora, 12, 0, 2, 1, Qt.AlignmentFlag.AlignHCenter)


    def CreatePage40(self): # Registros
        self.item = -1

        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)
        Background_3 = QLabel()
        Background_3.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Registros')
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Button_AddOperacao = QPushButton('Adicionar operação')
        self.HMI.Button_AddOperacao.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id))
        self.HMI.Button_AddOperacao.setFixedSize(160,40)
        self.HMI.Button_AddOperacao.setIconSize(QSize(35, 35))
        self.HMI.Button_AddOperacao.setIcon(QIcon("./images/add_user.png"))
        self.HMI.Button_AddOperacao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_AddOperacao.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)}')

        self.HMI.Button_AlterarOperacao = QPushButton('Alterar operação')
        self.HMI.Button_AlterarOperacao.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['AlterarOperacaoCripto'].page_id))
        self.HMI.Button_AlterarOperacao.setFixedSize(160,40)
        self.HMI.Button_AlterarOperacao.setIconSize(QSize(35, 35))
        self.HMI.Button_AlterarOperacao.setIcon(QIcon("./images/iconeAdjustDB.png"))
        self.HMI.Button_AlterarOperacao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_AlterarOperacao.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)}')

        self.HMI.Button_DeletarOperacao = QPushButton('Deletar operação')
        self.HMI.Button_DeletarOperacao.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['DeletarOperacaoCripto'].page_id))
        self.HMI.Button_DeletarOperacao.setFixedSize(160,40)
        self.HMI.Button_DeletarOperacao.setIconSize(QSize(35, 35))
        self.HMI.Button_DeletarOperacao.setIcon(QIcon("./images/delete_broker.png"))
        self.HMI.Button_DeletarOperacao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_DeletarOperacao.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)}')

        self.HMI.Button_DTeST = QPushButton()
        self.HMI.Button_DTeST.setToolTip("Alterar apresentação de DT e ST")
        self.HMI.Button_DTeST.pressed.connect(lambda: self.OnButtonPressed('ChangeDTeST'))
        self.HMI.Button_DTeST.setFixedSize(70*3+5,35*3+5)
        self.HMI.Button_DTeST.setIconSize(QSize(70*3, 35*3))
        self.HMI.Button_DTeST.setStyleSheet('QPushButton{background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0)} QToolTip {background-color: black; color: white;border: black solid 1px}')
        self.HMI.Button_DTeST.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if self.HMI.DTeST == "NotDefined":
            self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Trades Brutos.png"))
            self.HMI.DTeST = ""
        elif self.HMI.DTeST == "": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Trades Brutos.png"))
        elif self.HMI.DTeST == "DTeST": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Day Trades e Swing Trades.png"))
        elif self.HMI.DTeST == "ST": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas ST.png"))
        elif self.HMI.DTeST == "DT": self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas DT.png"))

        self.HMI.Label_Msg1 = QLabel('Operações realizadas na '+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font20)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.HMI.Table_Operacoes_RealizadasHeader = QTableWidget()
        self.HMI.Table_Operacoes_Realizadas = QTableWidget()

        self.HMI.Table_EstoqueHeader = QTableWidget()
        self.HMI.Table_Estoque = QTableWidget()

        self.CreateTable_40_1() # Table_Operacoes_RealizadasHeader
        self.CreateTable_40_2() # Table_Operacoes_Realizadas (Criada com uma thread)

        self.CreateTable_40_3()  # Table_EstoqueHeader
        self.CreateTable_40_4()  # Table_Estoque (Criada com uma thread)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 3, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_3, 4, 0, 8, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 10, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_EstoqueHeader, 1, 0, 1, 5, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Estoque, 2, 0, 2, 5, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AddOperacao, 1, 5, 1, 5, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_AlterarOperacao, 2, 5, 1, 5, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DeletarOperacao, 3, 5, 1, 5, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        # self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DTeST, 1, 8, 3, 1, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 4, 0, 1, 10, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_RealizadasHeader, 5, 0, 1, 10, Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas, 6, 0, 6, 10, Qt.AlignmentFlag.AlignTop)


    def CreatePage41(self): # Informar nova operação
        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        black = "rgb(0,0,0)"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Informar nova operação na '+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Msg2 = QLabel('Data:')
        self.HMI.Label_Msg2.setStyleSheet('color: white')
        self.HMI.Label_Msg2.setFont(self.HMI.font14)
        self.HMI.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.Selecao_Ano = str(datetime.now().year)
        self.HMI.Selecao_Mes = str(datetime.now().month)
        self.HMI.Selecao_Dia = str(datetime.now().day)

        self.HMI.Button_Calendario = QPushButton(self.HMI.Selecao_Ano+"/"+self.HMI.Selecao_Mes+"/"+self.HMI.Selecao_Dia)
        self.HMI.Button_Calendario.setFont(self.HMI.font16)
        self.HMI.Button_Calendario.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.Button_Calendario.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Calendario.pressed.connect(lambda: self.HMI.OnButtonPressed("Abrir Calendário"))

        self.HMI.Selecao_Hora = str(datetime.now().hour)
        self.HMI.Selecao_Minuto = '00'
        self.HMI.Selecao_Segundo = '00'

        self.HMI.Button_Relogio = QPushButton(self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo)
        self.HMI.Button_Relogio.setFont(self.HMI.font16)
        self.HMI.Button_Relogio.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.Button_Relogio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Relogio.pressed.connect(lambda: self.HMI.OnButtonPressed("Abrir Relógio"))

        self.HMI.Label_Msg3 = QLabel('Tipo:')
        self.HMI.Label_Msg3.setStyleSheet('color: white')
        self.HMI.Label_Msg3.setFont(self.HMI.font14)
        self.HMI.Label_Msg3.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.Button_Compra = QPushButton('COMPRA')
        self.HMI.Button_Compra.pressed.connect(lambda: self.OnButtonPressed('Compra_Cripto'))
        self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Compra.setFont(self.HMI.font20)
        self.HMI.Button_Compra.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.TipoDeOperacao = 'Compra'

        self.HMI.Button_Venda = QPushButton('venda')
        self.HMI.Button_Venda.pressed.connect(lambda: self.OnButtonPressed('Venda_Cripto'))
        self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Venda.setFont(self.HMI.font16)
        self.HMI.Button_Venda.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Deposito = QPushButton('depósito')
        self.HMI.Button_Deposito.pressed.connect(lambda: self.OnButtonPressed('Depósito_Cripto'))
        self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Deposito.setFont(self.HMI.font16)
        self.HMI.Button_Deposito.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Saque = QPushButton('saque')
        self.HMI.Button_Saque.pressed.connect(lambda: self.OnButtonPressed('Saque_Cripto'))
        self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Saque.setFont(self.HMI.font16)
        self.HMI.Button_Saque.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Drop = QPushButton('drop')
        self.HMI.Button_Drop.pressed.connect(lambda: self.OnButtonPressed('Drop_Cripto'))
        self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Drop.setFont(self.HMI.font16)
        self.HMI.Button_Drop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Burn = QPushButton('burn')
        self.HMI.Button_Burn.pressed.connect(lambda: self.OnButtonPressed('Burn_Cripto'))
        self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Burn.setFont(self.HMI.font16)
        self.HMI.Button_Burn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Stake = QPushButton('stake')
        self.HMI.Button_Stake.pressed.connect(lambda: self.OnButtonPressed('Stake_Cripto'))
        self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Stake.setFont(self.HMI.font16)
        self.HMI.Button_Stake.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Unstake = QPushButton('unstake')
        self.HMI.Button_Unstake.pressed.connect(lambda: self.OnButtonPressed('Unstake_Cripto'))
        self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Unstake.setFont(self.HMI.font16)
        self.HMI.Button_Unstake.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Hold = QPushButton('hold')
        self.HMI.Button_Hold.pressed.connect(lambda: self.OnButtonPressed('Hold_Cripto'))
        self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Hold.setFont(self.HMI.font16)
        self.HMI.Button_Hold.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Button_Unhold = QPushButton('unhold')
        self.HMI.Button_Unhold.pressed.connect(lambda: self.OnButtonPressed('Unhold_Cripto'))
        self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_Unhold.setFont(self.HMI.font16)
        self.HMI.Button_Unhold.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.HMI.Label_Msg10 = QLabel('Par:')
        self.HMI.Label_Msg10.setStyleSheet('color: white')
        self.HMI.Label_Msg10.setFont(self.HMI.font14)
        self.HMI.Label_Msg10.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.TextBox_Par_Esquerda = QLineEdit()
        self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
        self.HMI.TextBox_Par_Esquerda.returnPressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id))
        self.HMI.TextBox_Par_Esquerda.textChanged.connect(self.Auto_Capital_Par_Esquerda)

        self.HMI.Label_Msg12 = QLabel('/')
        self.HMI.Label_Msg12.setStyleSheet('color: white')
        self.HMI.Label_Msg12.setFont(self.HMI.font14)
        self.HMI.Label_Msg12.setFixedWidth(int(self.HMI.frameGeometry().width()/20*0.9))
        self.HMI.Label_Msg12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.TextBox_Par_Direita = QLineEdit()
        self.HMI.TextBox_Par_Direita.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Par_Direita.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Par_Direita.setFont(self.HMI.font14)
        self.HMI.TextBox_Par_Direita.returnPressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id))
        self.HMI.TextBox_Par_Direita.textChanged.connect(self.Auto_Capital_Par_Direita)

        self.HMI.Label_Msg4 = QLabel('Quantidade:')
        self.HMI.Label_Msg4.setStyleSheet('color: white')
        self.HMI.Label_Msg4.setFont(self.HMI.font14)
        self.HMI.Label_Msg4.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.TextBox_Qqt = QLineEdit()
        self.HMI.TextBox_Qqt.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_Qqt.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Qqt.setFont(self.HMI.font14)
        self.HMI.TextBox_Qqt.returnPressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id))

        self.HMI.Label_Msg5 = QLabel('Preço:')
        self.HMI.Label_Msg5.setStyleSheet('color: white')
        self.HMI.Label_Msg5.setFont(self.HMI.font14)
        self.HMI.Label_Msg5.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.TextBox_Preco = QLineEdit()
        self.HMI.TextBox_Preco.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_Preco.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Preco.setFont(self.HMI.font14)
        self.HMI.TextBox_Preco.returnPressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id))

        self.HMI.Label_Msg6 = QLabel('Taxa:')
        self.HMI.Label_Msg6.setStyleSheet('color: white')
        self.HMI.Label_Msg6.setFont(self.HMI.font14)
        self.HMI.Label_Msg6.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.TextBox_Taxa = QLineEdit('0')
        self.HMI.TextBox_Taxa.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_Taxa.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Taxa.setFont(self.HMI.font14)
        self.HMI.TextBox_Taxa.returnPressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id))

        self.HMI.Label_Msg7 = QLabel('Moeda da taxa:')
        self.HMI.Label_Msg7.setStyleSheet('color: white')
        self.HMI.Label_Msg7.setFont(self.HMI.font14)
        self.HMI.Label_Msg7.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.TextBox_MoedaDaTaxa = QLineEdit(self.HMI.DBManager.GetUserCoinCurrency())
        self.HMI.TextBox_MoedaDaTaxa.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_MoedaDaTaxa.setFont(self.HMI.font14)
        self.HMI.TextBox_MoedaDaTaxa.returnPressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id))
        self.HMI.TextBox_MoedaDaTaxa.textChanged.connect(self.Auto_Capital_MoedaDaTaxa)

        self.HMI.Label_Msg11 = QLabel('Conversão:')
        self.HMI.Label_Msg11.setStyleSheet('color: white')
        self.HMI.Label_Msg11.setFont(self.HMI.font14)
        self.HMI.Label_Msg11.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.TextBox_Conversao = QLineEdit('1')
        self.HMI.TextBox_Conversao.setValidator(QDoubleValidator(0.99,99.99,2))
        self.HMI.TextBox_Conversao.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
        self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Conversao.setFont(self.HMI.font14)
        self.HMI.TextBox_Conversao.returnPressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id))

        self.HMI.Button_BuscarConversao = QPushButton('Buscar')
        self.HMI.Button_BuscarConversao.pressed.connect(lambda: self.OnButtonPressed('BuscarConversaoAutomaticamente'))
        self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.Button_BuscarConversao.setFont(self.HMI.font16)
        self.HMI.Button_BuscarConversao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_BuscarConversao.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))

        self.HMI.Label_Msg8 = QLabel('Observação:')
        self.HMI.Label_Msg8.setStyleSheet('color: white')
        self.HMI.Label_Msg8.setFont(self.HMI.font14)
        self.HMI.Label_Msg8.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.HMI.TextBox_Obs = QLineEdit()
        self.HMI.TextBox_Obs.setFixedWidth(int(self.HMI.frameGeometry().width()*4/7*0.9))
        self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
        self.HMI.TextBox_Obs.setFont(self.HMI.font14)
        self.HMI.TextBox_Obs.returnPressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id))

        self.HMI.Button_LimparCampos = QPushButton('Limpar\ncampos')
        self.HMI.Button_LimparCampos.pressed.connect(lambda: self.HMI.LimparPage())
        self.HMI.Button_LimparCampos.setFont(self.HMI.font16)
        self.HMI.Button_LimparCampos.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_LimparCampos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_LimparCampos.setStyleSheet("background-color: rgb(100, 100, 100)")

        self.HMI.Button_RegistrarOperacao = QPushButton('Registrar\noperação')
        self.HMI.Button_RegistrarOperacao.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id))
        self.HMI.Button_RegistrarOperacao.setFont(self.HMI.font16)
        self.HMI.Button_RegistrarOperacao.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_RegistrarOperacao.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_RegistrarOperacao.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_RegistrarOperacao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_RegistrarOperacao.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Button_Info3 = QPushButton()
        self.HMI.Button_Info3.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info3'].page_id))
        self.HMI.Button_Info3.setFixedSize(40,40)
        self.HMI.Button_Info3.setIconSize(QSize(35, 35))
        self.HMI.Button_Info3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Info3.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info3.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info14 = QPushButton()
        self.HMI.Button_Info14.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info14'].page_id))
        self.HMI.Button_Info14.setFixedSize(40,40)
        self.HMI.Button_Info14.setIconSize(QSize(35, 35))
        self.HMI.Button_Info14.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Info14.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info14.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info15 = QPushButton()
        self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info15'].page_id))
        self.HMI.Button_Info15.setFixedSize(40,40)
        self.HMI.Button_Info15.setIconSize(QSize(35, 35))
        self.HMI.Button_Info15.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info12 = QPushButton()
        self.HMI.Button_Info12.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info12'].page_id))
        self.HMI.Button_Info12.setFixedSize(40,40)
        self.HMI.Button_Info12.setIconSize(QSize(35, 35))
        self.HMI.Button_Info12.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Info12.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info12.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info13 = QPushButton()
        self.HMI.Button_Info13.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info13'].page_id))
        self.HMI.Button_Info13.setFixedSize(40,40)
        self.HMI.Button_Info13.setIconSize(QSize(35, 35))
        self.HMI.Button_Info13.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Info13.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info13.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info11 = QPushButton()
        self.HMI.Button_Info11.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info11'].page_id))
        self.HMI.Button_Info11.setFixedSize(40,40)
        self.HMI.Button_Info11.setIconSize(QSize(35, 35))
        self.HMI.Button_Info11.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Info11.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info11.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info10 = QPushButton()
        self.HMI.Button_Info10.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info10'].page_id))
        self.HMI.Button_Info10.setFixedSize(40,40)
        self.HMI.Button_Info10.setIconSize(QSize(35, 35))
        self.HMI.Button_Info10.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Info10.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info10.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info9 = QPushButton()
        self.HMI.Button_Info9.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info9'].page_id))
        self.HMI.Button_Info9.setFixedSize(40,40)
        self.HMI.Button_Info9.setIconSize(QSize(35, 35))
        self.HMI.Button_Info9.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Info9.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info9.setIcon(QIcon("./images/Info.png"))

        self.HMI.Button_Info8 = QPushButton()
        self.HMI.Button_Info8.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info8'].page_id))
        self.HMI.Button_Info8.setFixedSize(40,40)
        self.HMI.Button_Info8.setIconSize(QSize(35, 35))
        self.HMI.Button_Info8.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Info8.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
        self.HMI.Button_Info8.setIcon(QIcon("./images/Info.png"))

        self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
        self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
        self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
        self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
        self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)

        self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
        self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
        self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)

        self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
        self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
        self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
        self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
        self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
        self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
        self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
        self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)
        self.HMI.setTabOrder(self.HMI.Button_Info8,self.HMI.TextBox_Par_Esquerda)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 8)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 9, 8)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 8, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 1, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Data
        self.HMI.HBoxLayout_Data = QHBoxLayout()
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Calendario, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Relogio, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Info3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Data, 1, 1, 1, 7, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 2, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Tipo
        self.HMI.HBoxLayout_Tipo = QHBoxLayout()
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Compra, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Venda, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Deposito, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Saque, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Drop, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Burn, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Stake, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Unstake, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Hold, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Unhold, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Info14, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Tipo, 2, 1, 1, 7, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg10, 3, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Par
        self.HMI.HBoxLayout_Par = QHBoxLayout()
        self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
        self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
        self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)

        if self.HMI.TipoDeOperacao in ['Compra', 'Venda']:
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Label_Msg12, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Direita, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Par_Direita)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Direita,self.HMI.TextBox_Qqt)

        self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 3, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 4, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Qqt
        self.HMI.HBoxLayout_Qqt = QHBoxLayout()
        self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.TextBox_Qqt)
        self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.Button_Info13)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Qqt, 4, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 5, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Preço
        self.HMI.HBoxLayout_Preco = QHBoxLayout()
        self.HMI.HBoxLayout_Preco.addWidget(self.HMI.TextBox_Preco)
        self.HMI.HBoxLayout_Preco.addWidget(self.HMI.Button_Info12)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Preco, 5, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg6, 6, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Taxa
        self.HMI.HBoxLayout_Taxa = QHBoxLayout()
        self.HMI.HBoxLayout_Taxa.addWidget(self.HMI.TextBox_Taxa)
        self.HMI.HBoxLayout_Taxa.addWidget(self.HMI.Button_Info11)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Taxa, 6, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg7, 7, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Moeda da taxa
        self.HMI.HBoxLayout_MoedaDaTaxa = QHBoxLayout()
        self.HMI.HBoxLayout_MoedaDaTaxa.addWidget(self.HMI.TextBox_MoedaDaTaxa)
        self.HMI.HBoxLayout_MoedaDaTaxa.addWidget(self.HMI.Button_Info10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_MoedaDaTaxa, 7, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg11, 8, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Conversão
        self.HMI.HBoxLayout_Conversao = QHBoxLayout()
        self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.TextBox_Conversao)
        self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.Button_BuscarConversao)
        self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.Button_Info9)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Conversao, 8, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg8, 9, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Observação
        self.HMI.HBoxLayout_Obs = QHBoxLayout()
        self.HMI.HBoxLayout_Obs.addWidget(self.HMI.TextBox_Obs)
        self.HMI.HBoxLayout_Obs.addWidget(self.HMI.Button_Info8)
        self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Obs, 9, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_LimparCampos, 3, 6, 3, 2, Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RegistrarOperacao, 7, 6, 3, 2, Qt.AlignmentFlag.AlignTop)

        self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
        self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
        self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
        self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
        self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
        self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
        self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
        self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
        self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
        self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
        self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
        self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
        self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
        self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
        self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
        self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

        self.HMI.TextBox_Par_Esquerda.setFocus()


    def CreatePage43(self): # Alterar operações
        self.item += 1

        BackgroundLineEdit = "rgb(0,10,30)"
        FontColorLineEdit = "green"
        black = "rgb(0,0,0)"
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Alterar operações na '+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Operacoes=[]
        for idx in self.HMI.Table_Operacoes_Realizadas.selectedIndexes():
            self.Operacoes.append(idx.row())
        self.Operacoes = list(dict.fromkeys(self.Operacoes))

        if len(self.Operacoes) > 0:

            self.HMI.Label_Msg1 = QLabel('Alteração na operação '+str(self.item+1)+' de '+str(len(self.Operacoes)))
            self.HMI.Label_Msg1.setStyleSheet('color: white')
            self.HMI.Label_Msg1.setFont(self.HMI.font24)
            self.HMI.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.HMI.Table_Operacoes_SelecionadasHeader = QTableWidget()
            self.HMI.Table_Operacoes_Selecionadas = QTableWidget()

            self.CreateTable_43_1() # Table_Operacoes_SelecionadasHeader
            self.CreateTable_43_2() # Table_Operacoes_Selecionadas (Mostra apenas o item selecionado)

            self.HMI.Label_Msg2 = QLabel('Data:')
            self.HMI.Label_Msg2.setStyleSheet('color: white')
            self.HMI.Label_Msg2.setFont(self.HMI.font14)
            self.HMI.Label_Msg2.setAlignment(Qt.AlignmentFlag.AlignRight)

            self.HMI.Selecao_Ano = str('%02d' % (datetime.now().year,))
            self.HMI.Selecao_Mes = str('%02d' % (datetime.now().month,))
            self.HMI.Selecao_Dia = str('%02d' % (datetime.now().day,))

            self.HMI.Button_Calendario = QPushButton(self.HMI.Selecao_Ano+"/"+self.HMI.Selecao_Mes+"/"+self.HMI.Selecao_Dia)
            self.HMI.Button_Calendario.setFont(self.HMI.font16)
            self.HMI.Button_Calendario.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.Button_Calendario.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_Calendario.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Calendario.pressed.connect(lambda: self.HMI.OnButtonPressed("Abrir Calendário"))

            self.HMI.Selecao_Hora = str('%02d' % (datetime.now().hour,))
            self.HMI.Selecao_Minuto = str('%02d' % (0,))
            self.HMI.Selecao_Segundo = str('%02d' % (0,))

            self.HMI.Button_Relogio = QPushButton(self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo)
            self.HMI.Button_Relogio.setFont(self.HMI.font16)
            self.HMI.Button_Relogio.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.Button_Relogio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_Relogio.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Relogio.pressed.connect(lambda: self.HMI.OnButtonPressed("Abrir Relógio"))

            self.HMI.Label_Msg3 = QLabel('Tipo:')
            self.HMI.Label_Msg3.setStyleSheet('color: white')
            self.HMI.Label_Msg3.setFont(self.HMI.font14)
            self.HMI.Label_Msg3.setAlignment(Qt.AlignmentFlag.AlignRight)

            self.HMI.Button_Compra = QPushButton('COMPRA')
            self.HMI.Button_Compra.pressed.connect(lambda: self.OnButtonPressed('Compra_Cripto'))
            self.HMI.Button_Compra.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Compra.setFont(self.HMI.font20)
            self.HMI.Button_Compra.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.TipoDeOperacao = 'Compra'

            self.HMI.Button_Venda = QPushButton('venda')
            self.HMI.Button_Venda.pressed.connect(lambda: self.OnButtonPressed('Venda_Cripto'))
            self.HMI.Button_Venda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Venda.setFont(self.HMI.font16)
            self.HMI.Button_Venda.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.HMI.Button_Deposito = QPushButton('depósito')
            self.HMI.Button_Deposito.pressed.connect(lambda: self.OnButtonPressed('Depósito_Cripto'))
            self.HMI.Button_Deposito.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Deposito.setFont(self.HMI.font16)
            self.HMI.Button_Deposito.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.HMI.Button_Saque = QPushButton('saque')
            self.HMI.Button_Saque.pressed.connect(lambda: self.OnButtonPressed('Saque_Cripto'))
            self.HMI.Button_Saque.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Saque.setFont(self.HMI.font16)
            self.HMI.Button_Saque.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.HMI.Button_Drop = QPushButton('drop')
            self.HMI.Button_Drop.pressed.connect(lambda: self.OnButtonPressed('Drop_Cripto'))
            self.HMI.Button_Drop.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Drop.setFont(self.HMI.font16)
            self.HMI.Button_Drop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.HMI.Button_Burn = QPushButton('burn')
            self.HMI.Button_Burn.pressed.connect(lambda: self.OnButtonPressed('Burn_Cripto'))
            self.HMI.Button_Burn.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Burn.setFont(self.HMI.font16)
            self.HMI.Button_Burn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.HMI.Button_Stake = QPushButton('stake')
            self.HMI.Button_Stake.pressed.connect(lambda: self.OnButtonPressed('Stake_Cripto'))
            self.HMI.Button_Stake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Stake.setFont(self.HMI.font16)
            self.HMI.Button_Stake.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.HMI.Button_Unstake = QPushButton('unstake')
            self.HMI.Button_Unstake.pressed.connect(lambda: self.OnButtonPressed('Unstake_Cripto'))
            self.HMI.Button_Unstake.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unstake.setFont(self.HMI.font16)
            self.HMI.Button_Unstake.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.HMI.Button_Hold = QPushButton('hold')
            self.HMI.Button_Hold.pressed.connect(lambda: self.OnButtonPressed('Hold_Cripto'))
            self.HMI.Button_Hold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Hold.setFont(self.HMI.font16)
            self.HMI.Button_Hold.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.HMI.Button_Unhold = QPushButton('unhold')
            self.HMI.Button_Unhold.pressed.connect(lambda: self.OnButtonPressed('Unhold_Cripto'))
            self.HMI.Button_Unhold.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_Unhold.setFont(self.HMI.font16)
            self.HMI.Button_Unhold.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.HMI.Label_Msg10 = QLabel('Par:')
            self.HMI.Label_Msg10.setStyleSheet('color: white')
            self.HMI.Label_Msg10.setFont(self.HMI.font14)
            self.HMI.Label_Msg10.setAlignment(Qt.AlignmentFlag.AlignRight)

            self.HMI.TextBox_Par_Esquerda = QLineEdit()
            self.HMI.TextBox_Par_Esquerda.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Esquerda.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Esquerda.setFont(self.HMI.font14)
            self.HMI.TextBox_Par_Esquerda.textChanged.connect(self.Auto_Capital_Par_Esquerda)

            self.HMI.Label_Msg12 = QLabel('/')
            self.HMI.Label_Msg12.setStyleSheet('color: white')
            self.HMI.Label_Msg12.setFont(self.HMI.font14)
            self.HMI.Label_Msg12.setFixedWidth(int(self.HMI.frameGeometry().width()/20*0.9))
            self.HMI.Label_Msg12.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.HMI.TextBox_Par_Direita = QLineEdit()
            self.HMI.TextBox_Par_Direita.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Par_Direita.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Par_Direita.setFont(self.HMI.font14)
            self.HMI.TextBox_Par_Direita.textChanged.connect(self.Auto_Capital_Par_Direita)

            self.HMI.Label_Msg4 = QLabel('Quantidade:')
            self.HMI.Label_Msg4.setStyleSheet('color: white')
            self.HMI.Label_Msg4.setFont(self.HMI.font14)
            self.HMI.Label_Msg4.setAlignment(Qt.AlignmentFlag.AlignRight)

            self.HMI.TextBox_Qqt = QLineEdit()
            self.HMI.TextBox_Qqt.setValidator(QDoubleValidator(0.99,99.99,2))
            self.HMI.TextBox_Qqt.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Qqt.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Qqt.setFont(self.HMI.font14)

            self.HMI.Label_Msg5 = QLabel('Preço:')
            self.HMI.Label_Msg5.setStyleSheet('color: white')
            self.HMI.Label_Msg5.setFont(self.HMI.font14)
            self.HMI.Label_Msg5.setAlignment(Qt.AlignmentFlag.AlignRight)

            self.HMI.TextBox_Preco = QLineEdit()
            self.HMI.TextBox_Preco.setValidator(QDoubleValidator(0.99,99.99,2))
            self.HMI.TextBox_Preco.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Preco.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Preco.setFont(self.HMI.font14)

            self.HMI.Label_Msg6 = QLabel('Taxa:')
            self.HMI.Label_Msg6.setStyleSheet('color: white')
            self.HMI.Label_Msg6.setFont(self.HMI.font14)
            self.HMI.Label_Msg6.setAlignment(Qt.AlignmentFlag.AlignRight)

            self.HMI.TextBox_Taxa = QLineEdit()
            self.HMI.TextBox_Taxa.setValidator(QDoubleValidator(0.99,99.99,2))
            self.HMI.TextBox_Taxa.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Taxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Taxa.setFont(self.HMI.font14)

            self.HMI.Label_Msg7 = QLabel('Moeda da taxa:')
            self.HMI.Label_Msg7.setStyleSheet('color: white')
            self.HMI.Label_Msg7.setFont(self.HMI.font14)
            self.HMI.Label_Msg7.setAlignment(Qt.AlignmentFlag.AlignRight)

            self.HMI.TextBox_MoedaDaTaxa = QLineEdit()
            self.HMI.TextBox_MoedaDaTaxa.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_MoedaDaTaxa.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_MoedaDaTaxa.setFont(self.HMI.font14)
            self.HMI.TextBox_MoedaDaTaxa.textChanged.connect(self.Auto_Capital_MoedaDaTaxa)

            self.HMI.Label_Msg11 = QLabel('Conversão:')
            self.HMI.Label_Msg11.setStyleSheet('color: white')
            self.HMI.Label_Msg11.setFont(self.HMI.font14)
            self.HMI.Label_Msg11.setAlignment(Qt.AlignmentFlag.AlignRight)

            self.HMI.TextBox_Conversao = QLineEdit()
            self.HMI.TextBox_Conversao.setValidator(QDoubleValidator(0.99,99.99,2))
            self.HMI.TextBox_Conversao.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))
            self.HMI.TextBox_Conversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Conversao.setFont(self.HMI.font14)

            self.HMI.Button_BuscarConversao = QPushButton('Buscar')
            self.HMI.Button_BuscarConversao.pressed.connect(lambda: self.OnButtonPressed('BuscarConversaoAutomaticamente'))
            self.HMI.Button_BuscarConversao.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.Button_BuscarConversao.setFont(self.HMI.font16)
            self.HMI.Button_BuscarConversao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_BuscarConversao.setFixedWidth(int(self.HMI.frameGeometry().width()/7*0.9))

            self.HMI.Label_Msg8 = QLabel('Observação:')
            self.HMI.Label_Msg8.setStyleSheet('color: white')
            self.HMI.Label_Msg8.setFont(self.HMI.font14)
            self.HMI.Label_Msg8.setAlignment(Qt.AlignmentFlag.AlignRight)

            self.HMI.TextBox_Obs = QLineEdit()
            self.HMI.TextBox_Obs.setFixedWidth(int(self.HMI.frameGeometry().width()*4/7*0.9))
            self.HMI.TextBox_Obs.setStyleSheet("background-color: "+BackgroundLineEdit+"; color: "+FontColorLineEdit+";")
            self.HMI.TextBox_Obs.setFont(self.HMI.font14)

            self.HMI.Button_LimparCampos = QPushButton('Limpar\ncampos')
            self.HMI.Button_LimparCampos.pressed.connect(lambda: self.HMI.LimparPage())
            self.HMI.Button_LimparCampos.setFont(self.HMI.font16)
            self.HMI.Button_LimparCampos.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
            self.HMI.Button_LimparCampos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_LimparCampos.setStyleSheet("background-color: rgb(100, 100, 100)")

            self.HMI.Button_RegistrarOperacao = QPushButton('Registrar\noperação')
            self.HMI.Button_RegistrarOperacao.pressed.connect(lambda: self.OnButtonPressed('Page43_Next'))
            self.HMI.Button_RegistrarOperacao.setFont(self.HMI.font16)
            self.HMI.Button_RegistrarOperacao.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
            self.HMI.Button_RegistrarOperacao.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
            self.HMI.Button_RegistrarOperacao.setIcon(QIcon("./images/log_in.png"))
            self.HMI.Button_RegistrarOperacao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_RegistrarOperacao.setStyleSheet("background-color: rgb(20, 120, 30)")

            self.HMI.Button_Info3 = QPushButton()
            self.HMI.Button_Info3.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info3'].page_id))
            self.HMI.Button_Info3.setFixedSize(40,40)
            self.HMI.Button_Info3.setIconSize(QSize(35, 35))
            self.HMI.Button_Info3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_Info3.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info3.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info14 = QPushButton()
            self.HMI.Button_Info14.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info14'].page_id))
            self.HMI.Button_Info14.setFixedSize(40,40)
            self.HMI.Button_Info14.setIconSize(QSize(35, 35))
            self.HMI.Button_Info14.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_Info14.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info14.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info15 = QPushButton()
            self.HMI.Button_Info15.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info15'].page_id))
            self.HMI.Button_Info15.setFixedSize(40,40)
            self.HMI.Button_Info15.setIconSize(QSize(35, 35))
            self.HMI.Button_Info15.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_Info15.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info15.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info12 = QPushButton()
            self.HMI.Button_Info12.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info12'].page_id))
            self.HMI.Button_Info12.setFixedSize(40,40)
            self.HMI.Button_Info12.setIconSize(QSize(35, 35))
            self.HMI.Button_Info12.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_Info12.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info12.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info13 = QPushButton()
            self.HMI.Button_Info13.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info13'].page_id))
            self.HMI.Button_Info13.setFixedSize(40,40)
            self.HMI.Button_Info13.setIconSize(QSize(35, 35))
            self.HMI.Button_Info13.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_Info13.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info13.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info11 = QPushButton()
            self.HMI.Button_Info11.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info11'].page_id))
            self.HMI.Button_Info11.setFixedSize(40,40)
            self.HMI.Button_Info11.setIconSize(QSize(35, 35))
            self.HMI.Button_Info11.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_Info11.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info11.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info10 = QPushButton()
            self.HMI.Button_Info10.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info10'].page_id))
            self.HMI.Button_Info10.setFixedSize(40,40)
            self.HMI.Button_Info10.setIconSize(QSize(35, 35))
            self.HMI.Button_Info10.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_Info10.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info10.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info9 = QPushButton()
            self.HMI.Button_Info9.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info9'].page_id))
            self.HMI.Button_Info9.setFixedSize(40,40)
            self.HMI.Button_Info9.setIconSize(QSize(35, 35))
            self.HMI.Button_Info9.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_Info9.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info9.setIcon(QIcon("./images/Info.png"))

            self.HMI.Button_Info8 = QPushButton()
            self.HMI.Button_Info8.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['Info8'].page_id))
            self.HMI.Button_Info8.setFixedSize(40,40)
            self.HMI.Button_Info8.setIconSize(QSize(35, 35))
            self.HMI.Button_Info8.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.Button_Info8.setStyleSheet("background-color: "+black+"; border: 1px solid rgb(0, 0, 0)")
            self.HMI.Button_Info8.setIcon(QIcon("./images/Info.png"))

            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 9)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 13, 9)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 9, Qt.AlignmentFlag.AlignCenter)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 1, 9, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_SelecionadasHeader, 2, 0, 1, 9, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Selecionadas, 3, 0, 1, 9, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg2, 5, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Data

            self.HMI.HBoxLayout_Data = QHBoxLayout()
            self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Calendario, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Relogio, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Data.addWidget(self.HMI.Button_Info3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Data, 5, 1, 1, 8, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg3, 6, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Tipo
            self.HMI.HBoxLayout_Tipo = QHBoxLayout()
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Compra, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Venda, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Deposito, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Saque, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Drop, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Burn, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Stake, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Unstake, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Hold, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Unhold, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.HBoxLayout_Tipo.addWidget(self.HMI.Button_Info14, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Tipo, 6, 1, 1, 8, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg10, 7, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Par
            self.HMI.HBoxLayout_Par = QHBoxLayout()
            self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Esquerda, Qt.AlignmentFlag.AlignLeft)
            self.HMI.setTabOrder(self.HMI.Button_Calendario,self.HMI.Button_Relogio)
            self.HMI.setTabOrder(self.HMI.Button_Relogio,self.HMI.TextBox_Par_Esquerda)
            self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Qqt)

            if self.HMI.TipoDeOperacao in ['Compra', 'Venda']:
                self.HMI.HBoxLayout_Par.addWidget(self.HMI.Label_Msg12, Qt.AlignmentFlag.AlignLeft)
                self.HMI.HBoxLayout_Par.addWidget(self.HMI.TextBox_Par_Direita, Qt.AlignmentFlag.AlignLeft)
                self.HMI.setTabOrder(self.HMI.TextBox_Par_Esquerda,self.HMI.TextBox_Par_Direita)
                self.HMI.setTabOrder(self.HMI.TextBox_Par_Direita,self.HMI.TextBox_Qqt)

            self.HMI.HBoxLayout_Par.addWidget(self.HMI.Button_Info15, Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Par, 7, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg4, 8, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Qqt
            self.HMI.HBoxLayout_Qqt = QHBoxLayout()
            self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.TextBox_Qqt)
            self.HMI.HBoxLayout_Qqt.addWidget(self.HMI.Button_Info13)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Qqt, 8, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg5, 9, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Preço
            self.HMI.HBoxLayout_Preco = QHBoxLayout()
            self.HMI.HBoxLayout_Preco.addWidget(self.HMI.TextBox_Preco)
            self.HMI.HBoxLayout_Preco.addWidget(self.HMI.Button_Info12)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Preco, 9, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg6, 10, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Taxa
            self.HMI.HBoxLayout_Taxa = QHBoxLayout()
            self.HMI.HBoxLayout_Taxa.addWidget(self.HMI.TextBox_Taxa)
            self.HMI.HBoxLayout_Taxa.addWidget(self.HMI.Button_Info11)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Taxa, 10, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg7, 11, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Moeda da taxa
            self.HMI.HBoxLayout_MoedaDaTaxa = QHBoxLayout()
            self.HMI.HBoxLayout_MoedaDaTaxa.addWidget(self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.HBoxLayout_MoedaDaTaxa.addWidget(self.HMI.Button_Info10)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_MoedaDaTaxa, 11, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg11, 12, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Conversão
            self.HMI.HBoxLayout_Conversao = QHBoxLayout()
            self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.TextBox_Conversao)
            self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.Button_BuscarConversao)
            self.HMI.HBoxLayout_Conversao.addWidget(self.HMI.Button_Info9)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Conversao, 12, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg8, 13, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # Observação
            self.HMI.HBoxLayout_Obs = QHBoxLayout()
            self.HMI.HBoxLayout_Obs.addWidget(self.HMI.TextBox_Obs)
            self.HMI.HBoxLayout_Obs.addWidget(self.HMI.Button_Info8)
            self.HMI.F_GLayout[self.HMI.GCount-1].addLayout(self.HMI.HBoxLayout_Obs, 13, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_LimparCampos, 7, 7, 3, 2, Qt.AlignmentFlag.AlignBottom)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_RegistrarOperacao, 11, 7, 3, 2, Qt.AlignmentFlag.AlignTop)
            self.HMI.TextBox_Par_Esquerda.setFocus()

            # Completar os textBoxes
            for i, item in enumerate(self.data_40_1):
                if i == self.Operacoes[self.item]:
                    data = str(item[0])
                    data = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
                    ano = str('%02d' % (data.year,))
                    mes = str('%02d' % (data.month,))
                    dia = str('%02d' % (data.day,))
                    hora = str('%02d' % (data.hour,))
                    minuto = str('%02d' % (data.minute,))
                    segundo = str('%02d' % (data.second,))
                    Tipo = str(item[2])
                    if "/" in item[1]:
                        ParEsquerdo = item[1][:item[1].index("/",0)]
                        ParDireito = item[1][item[1].index("/",0)+1:]
                    else:
                        ParEsquerdo = item[1]
                        ParDireito = ''
                    Preco = str('%.8f' % item[3])
                    Qqt = str('%.8f' % item[4])
                    Taxa = str('%.8f' % item[5])
                    MoedaDaTaxa= str(item[6])
                    Conversao = str('%.8f' % item[7])
                    Obs = str(item[8])
            self.HMI.TextBox_Obs.setText(Obs)
            self.HMI.Button_Calendario.setText(ano+"/"+mes+"/"+dia)
            self.HMI.Button_Relogio.setText(hora+":"+minuto+":"+segundo)
            self.HMI.Selecao_Ano = ano
            self.HMI.Selecao_Mes = mes
            self.HMI.Selecao_Dia = dia
            self.HMI.Selecao_Hora = hora
            self.HMI.Selecao_Minuto = minuto
            self.HMI.Selecao_Segundo = segundo
            if Tipo == "Compra": self.OnButtonPressed('Compra_Cripto')
            elif Tipo == "Venda": self.OnButtonPressed('Venda_Cripto')
            elif Tipo == "Depósito": self.OnButtonPressed('Depósito_Cripto')
            elif Tipo == "Saque": self.OnButtonPressed('Saque_Cripto')
            elif Tipo == "Drop": self.OnButtonPressed('Drop_Cripto')
            elif Tipo == "Burn": self.OnButtonPressed('Burn_Cripto')
            elif Tipo == "Stake": self.OnButtonPressed('Stake_Cripto')
            elif Tipo == "Unstake": self.OnButtonPressed('Unstake_Cripto')
            elif Tipo == "Hold": self.OnButtonPressed('Hold_Cripto')
            elif Tipo == "Unhold": self.OnButtonPressed('Unhold_Cripto')
            self.HMI.TextBox_Par_Esquerda.setText(ParEsquerdo)
            self.HMI.TextBox_Par_Direita.setText(ParDireito)
            self.HMI.TextBox_Preco.setText(Preco)
            self.HMI.TextBox_Qqt.setText(Qqt)
            self.HMI.TextBox_Taxa.setText(Taxa)
            self.HMI.TextBox_MoedaDaTaxa.setText(MoedaDaTaxa)
            self.HMI.TextBox_Conversao.setText(Conversao)

            self.HMI.setTabOrder(self.HMI.TextBox_Qqt,self.HMI.TextBox_Preco)
            self.HMI.setTabOrder(self.HMI.TextBox_Preco,self.HMI.TextBox_Taxa)
            self.HMI.setTabOrder(self.HMI.TextBox_Taxa,self.HMI.TextBox_MoedaDaTaxa)
            self.HMI.setTabOrder(self.HMI.TextBox_MoedaDaTaxa,self.HMI.TextBox_Conversao)
            self.HMI.setTabOrder(self.HMI.TextBox_Conversao,self.HMI.TextBox_Obs)
            self.HMI.setTabOrder(self.HMI.TextBox_Obs,self.HMI.Button_LimparCampos)
            self.HMI.setTabOrder(self.HMI.Button_LimparCampos,self.HMI.Button_RegistrarOperacao)
            self.HMI.setTabOrder(self.HMI.Button_RegistrarOperacao,self.HMI.Button_Info3)
            self.HMI.setTabOrder(self.HMI.Button_Info3,self.HMI.Button_Info14)
            self.HMI.setTabOrder(self.HMI.Button_Info14,self.HMI.Button_Info15)
            self.HMI.setTabOrder(self.HMI.Button_Info15,self.HMI.Button_Info13)
            self.HMI.setTabOrder(self.HMI.Button_Info13,self.HMI.Button_Info12)
            self.HMI.setTabOrder(self.HMI.Button_Info12,self.HMI.Button_Info11)
            self.HMI.setTabOrder(self.HMI.Button_Info11,self.HMI.Button_Info10)
            self.HMI.setTabOrder(self.HMI.Button_Info10,self.HMI.Button_Info9)
            self.HMI.setTabOrder(self.HMI.Button_Info9,self.HMI.Button_Info8)

            self.HMI.TextBox_Qqt.setFocus()

        else:
            self.HMI.Label_Msg1 = QLabel('Nenhuma operação foi selecionada na página anterior.')
            self.HMI.Label_Msg1.setStyleSheet('color: white')
            self.HMI.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 10)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 11, 10)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 10, Qt.AlignmentFlag.AlignCenter)
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 1, 0, 1, 10, Qt.AlignmentFlag.AlignCenter)
            self.HMI.unsetCursor()


    def CreatePage44(self): # Deletar operações
        black = 'rgb(0, 0, 0)'
        Background_1 = QLabel()
        Background_1.setStyleSheet("background-color: "+black)
        Background_2 = QLabel()
        Background_2.setStyleSheet("background-color: "+black)

        self.HMI.Label_Titulo = QLabel('Deletar operações na '+self.HMI.ComboBox_Corretoras.currentText())
        self.HMI.Label_Titulo.setStyleSheet('color: white')
        self.HMI.Label_Titulo.setFont(self.HMI.font30)
        self.HMI.Label_Titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HMI.Label_Msg1 = QLabel('Operações selecionadas para serem deletadas:')
        self.HMI.Label_Msg1.setStyleSheet('color: white')
        self.HMI.Label_Msg1.setFont(self.HMI.font24)
        self.HMI.Label_Msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Operacoes = [] # Será usada para fazer a tabela dessa pagina, com apenas os itens selecionados
        for idx in self.HMI.Table_Operacoes_Realizadas.selectedIndexes():
            self.Operacoes.append(idx.row())
        self.Operacoes = list(dict.fromkeys(self.Operacoes))

        self.HMI.Button_Cancelar = QPushButton('Cancelar')
        self.HMI.Button_Cancelar.pressed.connect(lambda: self.HMI.CreatePage(PAGE_BY_NAME['RegistrosCripto'].page_id))
        self.HMI.Button_Cancelar.setFont(self.HMI.font16)
        self.HMI.Button_Cancelar.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_Cancelar.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_Cancelar.setIcon(QIcon("./images/Voltar.png"))
        self.HMI.Button_Cancelar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_Cancelar.setStyleSheet("background-color: rgb(200, 100, 100)")

        self.HMI.Button_DeletarOperacoes = QPushButton('Deletar\noperações')
        self.HMI.Button_DeletarOperacoes.pressed.connect(lambda: self.OnButtonPressed('Deletar Ativos da Pagina 44'))
        self.HMI.Button_DeletarOperacoes.setFont(self.HMI.font16)
        self.HMI.Button_DeletarOperacoes.setIconSize(QSize(int(self.HMI.frameGeometry().height()/10*0.9),int(self.HMI.frameGeometry().height()/10*0.9)))
        self.HMI.Button_DeletarOperacoes.setFixedSize(int(self.HMI.frameGeometry().width()*2/10*0.9),int(self.HMI.frameGeometry().width()*1/10*0.9))
        self.HMI.Button_DeletarOperacoes.setIcon(QIcon("./images/log_in.png"))
        self.HMI.Button_DeletarOperacoes.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.HMI.Button_DeletarOperacoes.setStyleSheet("background-color: rgb(20, 120, 30)")

        self.HMI.Table_Operacoes_SelecionadasHeader = QTableWidget()
        self.HMI.Table_Operacoes_Selecionadas = QTableWidget()

        self.CreateTable_44_1() # Table_Operacoes_SelecionadasHeader
        self.CreateTable_44_2() # Table_Operacoes_Selecionadas (Mostra apenas os itens selecionados)

        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_1, 0, 0, 1, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(Background_2, 1, 0, 13, 10)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Titulo, 0, 0, 1, 10, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Label_Msg1, 2, 0, 1, 10, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_SelecionadasHeader, 3, 0, 1, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Selecionadas, 4, 0, 6, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_Cancelar, 12, 0, 1, 6, Qt.AlignmentFlag.AlignCenter)
        self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_DeletarOperacoes, 12, 5, 1, 6, Qt.AlignmentFlag.AlignCenter)
