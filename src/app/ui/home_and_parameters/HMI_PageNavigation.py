"""
Created on Sun Sep  5 01:44:04 2021

@author: Caio Moreira Porta
"""
import os
import traceback
import sys
from datetime import datetime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtCore import Qt
from ui.popup import LoadingWindow
from ui.popup import OperacaoRegistradaComSucesso
from core.BackgroundProcesses import WorkerThread
from ui.pages import PAGE_BY_NAME
from src.app.core.logger_setup import logger


class HMI_PageNavigation:
    def CreatePage_Decisao(self):
        """
            Pages Creation
        """
        if self.PageID== PAGE_BY_NAME['AdicionarNovoAtivo'].page_id:
            if len(self.TextBox_NomeNovoAtivo.text())>0 and len(self.TextBox_NomeNovoAtivo.text())<7 and not self.TextBox_NomeNovoAtivo.text().upper() == "USD":
                self.setCursor(Qt.CursorShape.WaitCursor)
                if self.TextBox_NomeNovoAtivo.text() in self.DBManager.GetAllTickers(): # Otimizador
                    IsShare, self.Cache_Cotacao = self.YahooFinance.isShare(self.TextBox_NomeNovoAtivo.text())
                    self.unsetCursor()
                    if IsShare: self.CreatePage(PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id)
                    else: self.CreatePage(PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id)
                else:
                    # Perguntar se mesmo assim quer buscar
                    MessageBox_Msg1 = QMessageBox()
                    MessageBox_Msg1.setWindowTitle("Escolha um")
                    MessageBox_Msg1.setText("O ativo não está contido na lista de pré-checagem.\nDeseja mesmo assim tentar buscar a cotação online?\n(Isso pode levar alguns minutos)")
                    MessageBox_Msg1.setIcon(QMessageBox.Warning)
                    MessageBox_Msg1.setStandardButtons(QMessageBox.No|QMessageBox.Yes|QMessageBox.Cancel)
                    MessageBox_Msg1.setDefaultButton(QMessageBox.Yes)
                    MessageBox_Msg1.setWindowIcon(QIcon(".\\images\\logoARCA.png"))
                    returnValue = MessageBox_Msg1.exec()

                    if returnValue == QMessageBox.Yes:
                        IsShare, self.Cache_Cotacao = self.YahooFinance.isShare(self.TextBox_NomeNovoAtivo.text())
                        self.unsetCursor()
                        if IsShare: self.CreatePage(PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id)
                        else: self.CreatePage(PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id)
                    elif returnValue == QMessageBox.No:
                        IsShare = False; self.Cache_Cotacao = 0.
                        self.unsetCursor()
                        if IsShare: self.CreatePage(PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id)
                        else: self.CreatePage(PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id)
            else:
                try: self.Label_Erro1.deleteLater()
                except Exception as e:
                    print(e, traceback.format_exception(None, e, e.__traceback__))
                self.Label_Erro1 = QLabel()
                self.Label_Erro1.setStyleSheet('color: red')
                self.Label_Erro1.setFont(self.font12)
                self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.Label_Erro1.setText("Insira um ticker válido com até 6 caracteres.\nPara 'USD' utilize 'USDT' ou equivalente.") # Substitui a string do erro mais provável
                self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 17, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        elif self.PageID== PAGE_BY_NAME['RenomearAtivo'].page_id:
            if len(self.TextBox_NovoNomeAtivo.text())>0 and len(self.TextBox_NovoNomeAtivo.text())<7 and not self.TextBox_NovoNomeAtivo.text().upper() == "USD":
                self.setCursor(Qt.CursorShape.WaitCursor)
                if self.TextBox_NovoNomeAtivo.text() in self.DBManager.GetAllTickers(): # Otimizador
                    IsShare, self.Cache_Cotacao = self.YahooFinance.isShare(self.TextBox_NovoNomeAtivo.text())
                    self.unsetCursor()
                    if IsShare: self.CreatePage(PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id)
                    else: self.CreatePage(PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id)
                else:
                    # Perguntar se mesmo assim quer buscar
                    MessageBox_Msg1 = QMessageBox()
                    MessageBox_Msg1.setWindowTitle("Escolha um")
                    MessageBox_Msg1.setText("O ativo não está contido na lista de pré-checagem.\nDeseja mesmo assim tentar buscar a cotação online?\n(Isso pode levar alguns minutos)")
                    MessageBox_Msg1.setIcon(QMessageBox.Warning)
                    MessageBox_Msg1.setStandardButtons(QMessageBox.No|QMessageBox.Yes|QMessageBox.Cancel)
                    MessageBox_Msg1.setDefaultButton(QMessageBox.Yes)
                    MessageBox_Msg1.setWindowIcon(QIcon(".\\images\\logoARCA.png"))
                    returnValue = MessageBox_Msg1.exec()

                    if returnValue == QMessageBox.Yes:
                        IsShare, self.Cache_Cotacao = self.YahooFinance.isShare(self.TextBox_NovoNomeAtivo.text())
                        self.unsetCursor()
                        if IsShare: self.CreatePage(PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id)
                        else: self.CreatePage(PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id)
                    elif returnValue == QMessageBox.No:
                        IsShare = False; self.Cache_Cotacao = 0.
                        self.unsetCursor()
                        if IsShare: self.CreatePage(PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id)
                        else: self.CreatePage(PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id)
            else:
                try: self.Label_Erro1.deleteLater()
                except Exception as e:
                    print(e, traceback.format_exception(None, e, e.__traceback__))
                self.Label_Erro1 = QLabel()
                self.Label_Erro1.setStyleSheet('color: red')
                self.Label_Erro1.setFont(self.font12)
                self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.Label_Erro1.setText("Insira um ticker válido com até 6 caracteres.\nPara 'USD' utilize 'USDT' ou equivalente.") # Substitui a string do erro mais provável
                self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 17, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

    def CreatePage(self, PageID):
        if self.OutraJanelaAberta:
            MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra janela aberta.\nFeche a janela aberta e tente novamente.')
            if self.CalendarWindowOpen:
                self.Window_Calendario.close()
                self.Window_Calendario.show()
            elif self.ClockWindowOpen:
                self.Window_Relogio.close()
                self.Window_Relogio.show()
        else:
            if PageID== PAGE_BY_NAME['Login'].page_id:
                if self.PageIDAux== PAGE_BY_NAME['ConfirmacaoLogout'].page_id:
                    if self.TextBox_CodigoDeConfirmacao.text() == self.CodigoDeConfirmacaoGerado:
                        if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                            self.LoggedIn = self.DBManager.DeleteUserDB()
                            if not self.LoggedIn:
                                if os.path.exists(os.getcwd()+"\\images\\ProfilePhoto_"+self.User+".jpg"):
                                    os.remove(os.getcwd()+"\\images\\ProfilePhoto_"+self.User+".jpg")

                                os.execl(sys.executable, sys.executable, *sys.argv) # Reboot app | It doesn't work when running by script, only by .exe
                    # self.InicializacaoUsuario()
                        else:
                            MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
                    else:
                        try: self.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro1 = QLabel()
                        self.Label_Erro1.setStyleSheet('color: red')
                        self.Label_Erro1.setFont(self.font12)
                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Label_Erro1.setText('O código não confere.')
                        self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 13, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                        self.TextBox_CodigoDeConfirmacao.setFocus()
                elif self.PageID == "1":
                    self.DBManager.Disconnect()
                    self.ClearPage()
                    self.PageID= PAGE_BY_NAME['Login'].page_id
                    self.PageIDAux = ''
                    self.InsertGridLayout(0, 0, 1, 20)
                    self.InicializacaoUsuario()
                    self.CreatePage0()
                    self.PutHeader()
                else:
                    self.InicializacaoUsuario()
                    self.ClearPage()
                    self.PageID= PAGE_BY_NAME['Login'].page_id
                    self.PageIDAux = ''
                    self.InsertGridLayout(0, 0, 1, 20)
                    self.CreatePage0()
                    self.PutHeader()
            elif PageID== PAGE_BY_NAME['Home'].page_id:
                if self.PageID== PAGE_BY_NAME['AlteracaoSenha'].page_id:
                    if (self.TextBox_NovaSenha1.text() == self.TextBox_NovaSenha2.text() and
                        len(self.TextBox_NovaSenha1.text())>3): # Condições para passar pra página 1
                            self.LoggedIn = self.DBManager.ConnectTo(self.User, self.DBManager.GetPasswdByUser(self.User))
                            self.DBManager.ChangePassword(self.TextBox_NovaSenha1.text())
                            self.ClearPage()
                            self.PageID= PAGE_BY_NAME['Home'].page_id
                            self.PageIDAux = ''
                            self.InsertGridLayout(1, 0, 1, 20)
                            self.CreatePage1()
                            self.PutHeader()
                            self.YahooFinance.Thread_GetAllTickers()
                            self.DBManager.UpdatePatrimonioRendimento()
                            # self.DBManager.AtualizarCotacoes()
                    else:
                        if not self.TextBox_NovaSenha1.text() == self.TextBox_NovaSenha2.text():
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('As senhas digitadas não são iguais.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 13, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                            self.TextBox_NovaSenha1.setFocus()
                        elif not len(self.TextBox_NovaSenha1.text())>3:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('A senha tem que ter pelo menos 4 caracteres.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 13, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                            self.TextBox_NovaSenha1.setFocus()
                elif self.PageID== PAGE_BY_NAME['ConfirmacaoEmailCriar'].page_id:
                    if self.TextBox_CodigoDeConfirmacao.text() == self.CodigoDeConfirmacaoGerado: # Condições para passar pra página 1
                        user = self.TextBox_NomeDeUsuario.text()
                        senha = self.TextBox_Senha1.text()
                        email = self.TextBox_Email.text().lower()
                        moedacorrente = self.ComboBox_Currency.currentText()
                        userpath = self.TextBox_Path.text()
                        self.LoggedIn = self.DBManager.CriarNovoPerfil(user = user,
                                                                       senha = senha,
                                                                       email = email.lower(),
                                                                       moedacorrente = moedacorrente,
                                                                       userpath = userpath,
                                                                       )
                        if self.LoggedIn:
                            self.User = user
                            self.Email = email
                            if self.DBManager.CheckIfUserExists(self.User) == "Arquivo não encontrado":
                                logger.error("""Arquivo não encontrado. Comentei esse trem aqui embaixo pq nao lembro porque ele existe. 
                                             Se der ruim, descomentar e procurar um jeito mais elegante de fazer isso.""")
                            #     def UpdateUserPath(UserName, PathNovo):
                            #         currdir = os.getcwd()
                            #         conn = sqlite3.connect(currdir+'\\Users.db')
                            #         cursor = conn.cursor()
                            #         cursor.execute("UPDATE Usuários SET Path = (?) Where Usuário = (?)", [(PathNovo), UserName])
                            #         conn.commit()
                            #         conn.close()
                            #     self.DBManager.ThreadLock.acquire()
                            #     UpdateUserPath(self.User, self.TextBox_Path.text())
                            #     self.DBManager.ThreadLock.release()
                            self.ClearPage()
                            self.PageID= PAGE_BY_NAME['Home'].page_id
                            self.PageIDAux = ''
                            self.InsertGridLayout(1, 0, 1, 20)
                            self.CreatePage1()
                            self.PutHeader()
                            self.YahooFinance.Thread_GetAllTickers()
                            self.DBManager.UpdatePatrimonioRendimento()
                            # self.DBManager.AtualizarCotacoes()
                        else:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('Ocorreu um erro inesperado. Tente novamente mais tarde.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 12, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                            # self.TextBox_NomeDeUsuario.setFocus()
                            self.TextBox_CodigoDeConfirmacao.setFocus()
                    else:
                        try: self.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro1 = QLabel()
                        self.Label_Erro1.setStyleSheet('color: red')
                        self.Label_Erro1.setFont(self.font12)
                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Label_Erro1.setText('O código não confere.')
                        self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 12, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                        self.TextBox_NomeDeUsuario.setFocus()
                elif self.PageID== PAGE_BY_NAME['Login'].page_id:
                    Resposta = self.DBManager.ConnectTo(self.TextBox_NomeDeUsuario.text(), self.TextBox_Senha.text())
                    if Resposta == "Arquivo não existe":
                        self.LoggedIn = False
                        try: self.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro1 = QLabel()
                        self.Label_Erro1.setStyleSheet('color: red')
                        self.Label_Erro1.setFont(self.font12)
                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Label_Erro1.setText('Usuário não encontrado.\nVerifique se o arquivo está no local declarado.')
                        self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 13, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                        self.TextBox_NomeDeUsuario.setFocus()
                    elif Resposta: # Condições para passar pra página 1
                        self.LoggedIn = True
                        self.User = self.DBManager.User
                        self.Email = self.DBManager.Email
                        self.ClearPage()
                        self.PageID= PAGE_BY_NAME['Home'].page_id
                        self.PageIDAux = ''
                        self.InsertGridLayout(1, 0, 1, 20)
                        self.CreatePage1()
                        self.PutHeader()
                        self.YahooFinance.Thread_GetAllTickers()
                        self.DBManager.UpdatePatrimonioRendimento()
                        # self.DBManager.AtualizarCotacoes()
                    else:
                        self.LoggedIn = False
                        try: self.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro1 = QLabel()
                        self.Label_Erro1.setStyleSheet('color: red')
                        self.Label_Erro1.setFont(self.font12)
                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Label_Erro1.setText('Usuário ou senha incorreto.')
                        self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 13, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                        self.TextBox_NomeDeUsuario.setFocus()
                else:
                    self.ClearPage()
                    self.PageID= PAGE_BY_NAME['Home'].page_id
                    self.PageIDAux = ''
                    self.InsertGridLayout(1, 0, 1, 20)
                    self.CreatePage1()
                    self.PutHeader()
            elif PageID== PAGE_BY_NAME['AuxilioSenha'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AuxilioSenha'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.CreatePage2()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['ImportarUsuario'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['ImportarUsuario'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.CreatePage3()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['ImportacaoUsuario'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['ImportacaoUsuario'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.CreatePage3b()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['CriarUsuario'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['CriarUsuario'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.CreatePage4()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['AnaliseMercado'].page_id: # Cria a mesma página da 13
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AnaliseMercado'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Mercado.CreatePage5()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['RecuperacaoEmail'].page_id:
                if "@" in self.TextBox_EmailOuUsuario.text(): isEmail = True
                else: isEmail = False

                if isEmail: # Recovering By Email
                    if self.DBManager.CheckIfEmailExists(self.TextBox_EmailOuUsuario.text().lower()):
                        self.Email = self.TextBox_EmailOuUsuario.text().lower()
                        self.User = self.DBManager.GetUserByEmail(self.TextBox_EmailOuUsuario.text())
                        self.ClearPage()
                        self.PageID= PAGE_BY_NAME['RecuperacaoEmail'].page_id
                        self.PageIDAux = ''
                        self.InsertGridLayout(1, 0, 1, 20)
                        self.CreatePage6(self.Email, self.User)
                        self.PutHeader()
                    else:
                        try: self.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro1 = QLabel()
                        self.Label_Erro1.setStyleSheet('color: red')
                        self.Label_Erro1.setFont(self.font12)
                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Label_Erro1.setText('Email não encontrado.')
                        self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 11, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                        self.TextBox_EmailOuUsuario.setFocus()

                else: # Recovering By User
                    if self.DBManager.CheckIfUserExists(self.TextBox_EmailOuUsuario.text()):
                        self.Email = self.DBManager.GetEmailByUser(self.TextBox_EmailOuUsuario.text())
                        self.User = self.TextBox_EmailOuUsuario.text()
                        self.ClearPage()
                        self.PageID= PAGE_BY_NAME['RecuperacaoEmail'].page_id
                        self.PageIDAux = ''
                        self.InsertGridLayout(1, 0, 1, 20)
                        self.CreatePage6(self.Email, self.User)
                        self.PutHeader()
                    else:
                        try: self.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro1 = QLabel()
                        self.Label_Erro1.setStyleSheet('color: red')
                        self.Label_Erro1.setFont(self.font12)
                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Label_Erro1.setText('Usuário não encontrado.')
                        self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 11, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                        self.TextBox_EmailOuUsuario.setFocus()
            elif PageID== PAGE_BY_NAME['AlteracaoSenha'].page_id:
                if self.TextBox_CodigoDeConfirmacao.text() == self.CodigoDeConfirmacaoGerado:
                    self.ClearPage()
                    self.PageID= PAGE_BY_NAME['AlteracaoSenha'].page_id
                    self.PageIDAux = ''
                    self.InsertGridLayout(1, 0, 1, 20)
                    self.CreatePage7()
                    self.PutHeader()
                else:
                    try: self.Label_Erro1.deleteLater()
                    except Exception as e:
                        print(e, traceback.format_exception(None, e, e.__traceback__))
                    self.Label_Erro1 = QLabel()
                    self.Label_Erro1.setStyleSheet('color: red')
                    self.Label_Erro1.setFont(self.font12)
                    self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.Label_Erro1.setText('Código não confere.')
                    self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 11, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                    self.TextBox_CodigoDeConfirmacao.setFocus()
            elif PageID== PAGE_BY_NAME['ConfirmacaoEmailCriar'].page_id:
                if (len(self.TextBox_NomeDeUsuario.text())>0 and
                    not "@"  in self.TextBox_NomeDeUsuario.text() and
                    not ","  in self.TextBox_NomeDeUsuario.text() and
                    (not self.DBManager.CheckIfUserExists(self.TextBox_NomeDeUsuario.text()) or
                     self.DBManager.CheckIfUserExists(self.TextBox_NomeDeUsuario.text()) == "Arquivo não encontrado") and
                    "@" in self.TextBox_Email.text() and
                    not "'\'" in self.TextBox_Email.text() and
                    not "," in self.TextBox_Email.text() and
                    len(self.TextBox_Email.text())>3 and
                    not self.DBManager.CheckIfEmailExists(self.TextBox_Email.text()) and
                    self.TextBox_Senha1.text() == self.TextBox_Senha2.text() and
                    len(self.TextBox_Senha1.text())>3 and
                    not self.TextBox_Senha1.text().isnumeric() and
                    not self.TextBox_Senha1.text().isalpha()): # Condições para passar pra página 8
                        self.ClearPage()
                        self.PageID= PAGE_BY_NAME['ConfirmacaoEmailCriar'].page_id
                        self.PageIDAux = ''
                        self.InsertGridLayout(1, 0, 1, 20)
                        self.CreatePage8()
                        self.PutHeader()
                else:
                        try: self.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro1 = QLabel()
                        self.Label_Erro1.setStyleSheet('color: red')
                        self.Label_Erro1.setFont(self.font12)
                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        if not len(self.TextBox_NomeDeUsuario.text()) > 0:
                            self.Label_Erro1.setText('Insira um nome de usuário')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_NomeDeUsuario.setFocus()
                        elif ("@" in self.TextBox_NomeDeUsuario.text() or
                            "," in self.TextBox_NomeDeUsuario.text() or
                            "'\'" in self.TextBox_NomeDeUsuario.text()):
                            self.Label_Erro1.setText("@ '\' , não são permitidos\nno nome de usuário.")
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_NomeDeUsuario.setFocus()
                        elif self.DBManager.CheckIfUserExists(self.TextBox_NomeDeUsuario.text()):
                            self.Label_Erro1.setText('Esse nome de usuário já existe.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_NomeDeUsuario.setFocus()

                        try: self.Label_Erro2.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro2 = QLabel()
                        self.Label_Erro2.setStyleSheet('color: red')
                        self.Label_Erro2.setFont(self.font12)
                        if (not "@" in self.TextBox_Email.text() or
                            "'\'" in self.TextBox_Email.text() or
                            "," in self.TextBox_Email.text()):
                            self.Label_Erro2.setText("Confira se seu email está correto.\n@ '\' , não são permitidos.")
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro2, 8, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_Email.setFocus()
                        elif self.DBManager.CheckIfEmailExists(self.TextBox_Email.text()):
                            self.Label_Erro2.setText('Esse endereço de email já possiu uma conta.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro2, 8, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_Email.setFocus()

                        try: self.Label_Erro3.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro3 = QLabel()
                        self.Label_Erro3.setStyleSheet('color: red')
                        self.Label_Erro3.setFont(self.font12)
                        if not self.TextBox_Senha1.text() == self.TextBox_Senha2.text():
                            self.Label_Erro3.setText('As senhas digitadas não são iguais.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro3, 10, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_Senha1.setFocus()
                        elif not len(self.TextBox_Senha2.text()) > 3:
                            self.Label_Erro3.setText('A senha tem que ter pelo menos 4 caracteres.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro3, 10, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_Senha1.setFocus()
                        elif not self.TextBox_Senha1.text().isnumeric() or not self.TextBox_Senha1.text().isalpha():
                            self.Label_Erro3.setText('A senha precisa ter pelo menos um número e uma letra ou símbolo.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro3, 10, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_NomeDeUsuario.setFocus()
            elif PageID== PAGE_BY_NAME['ConfirmacaoEmailImportar'].page_id:
                if (len(self.TextBox_NomeDeUsuario.text())>0 and
                    not "@"  in self.TextBox_NomeDeUsuario.text() and
                    not ","  in self.TextBox_NomeDeUsuario.text() and
                    (not self.DBManager.CheckIfUserExists(self.TextBox_NomeDeUsuario.text()) or
                     self.DBManager.CheckIfUserExists(self.TextBox_NomeDeUsuario.text()) == "Arquivo não encontrado") and
                    "@" in self.TextBox_Email.text() and
                    not "'\'" in self.TextBox_Email.text() and
                    not "," in self.TextBox_Email.text() and
                    len(self.TextBox_Email.text())>3 and
                    not self.DBManager.CheckIfEmailExists(self.TextBox_Email.text()) and
                    self.TextBox_Senha1.text() == self.TextBox_Senha2.text() and
                    len(self.TextBox_Senha1.text())>3 and
                    not self.TextBox_Senha1.text().isnumeric() and
                    not self.TextBox_Senha1.text().isalpha()): # Condições para passar pra página 8
                        self.ClearPage()
                        self.PageID= PAGE_BY_NAME['ConfirmacaoEmailImportar'].page_id
                        self.PageIDAux = ''
                        self.InsertGridLayout(1, 0, 1, 20)
                        self.CreatePage8b()
                        self.PutHeader()
                else:
                        try: self.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro1 = QLabel()
                        self.Label_Erro1.setStyleSheet('color: red')
                        self.Label_Erro1.setFont(self.font12)
                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        if not len(self.TextBox_NomeDeUsuario.text()) > 0:
                            self.Label_Erro1.setText('Insira um nome de usuário')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_NomeDeUsuario.setFocus()
                        elif ("@" in self.TextBox_NomeDeUsuario.text() or
                            "," in self.TextBox_NomeDeUsuario.text() or
                            "'\'" in self.TextBox_NomeDeUsuario.text()):
                            self.Label_Erro1.setText("@ '\' , não são permitidos\nno nome de usuário.")
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_NomeDeUsuario.setFocus()
                        elif self.DBManager.CheckIfUserExists(self.TextBox_NomeDeUsuario.text()):
                            self.Label_Erro1.setText('Esse nome de usuário já existe.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_NomeDeUsuario.setFocus()

                        try: self.Label_Erro2.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro2 = QLabel()
                        self.Label_Erro2.setStyleSheet('color: red')
                        self.Label_Erro2.setFont(self.font12)
                        if (not "@" in self.TextBox_Email.text() or
                            "'\'" in self.TextBox_Email.text() or
                            "," in self.TextBox_Email.text()):
                            self.Label_Erro2.setText("Confira se seu email está correto.\n@ '\' , não são permitidos.")
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro2, 8, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_Email.setFocus()
                        elif self.DBManager.CheckIfEmailExists(self.TextBox_Email.text()):
                            self.Label_Erro2.setText('Esse endereço de email já possiu uma conta.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro2, 8, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_Email.setFocus()

                        try: self.Label_Erro3.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro3 = QLabel()
                        self.Label_Erro3.setStyleSheet('color: red')
                        self.Label_Erro3.setFont(self.font12)
                        if not self.TextBox_Senha1.text() == self.TextBox_Senha2.text():
                            self.Label_Erro3.setText('As senhas digitadas não são iguais.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro3, 10, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_Senha1.setFocus()
                        elif not len(self.TextBox_Senha2.text()) > 3:
                            self.Label_Erro3.setText('A senha tem que ter pelo menos 4 caracteres.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro3, 10, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_Senha1.setFocus()
                        elif not self.TextBox_Senha1.text().isnumeric() or not self.TextBox_Senha1.text().isalpha():
                            self.Label_Erro3.setText('A senha precisa ter pelo menos um número e uma letra ou símbolo.')
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro3, 10, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
                            self.TextBox_NomeDeUsuario.setFocus()
            elif PageID== PAGE_BY_NAME['ImportandoDadosExcel'].page_id:
                if self.TextBox_CodigoDeConfirmacao.text() == self.CodigoDeConfirmacaoGerado: # Condições para passar pra página 1
                    # self.ClearPage()
                    # self.PageID= PAGE_BY_NAME['ImportandoDadosExcel'].page_id
                    # self.PageIDAux = ''
                    # self.InsertGridLayout(1, 0, 1, 20)
                    # self.CreatePageImportFromExcel()
                    # self.PutHeader()
                    self.OnButtonPressed('ImportFromExcel')
                else:
                    try: self.Label_Erro1.deleteLater()
                    except Exception as e:
                        print(e, traceback.format_exception(None, e, e.__traceback__))
                    self.Label_Erro1 = QLabel()
                    self.Label_Erro1.setStyleSheet('color: red')
                    self.Label_Erro1.setFont(self.font12)
                    self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.Label_Erro1.setText('O código não confere.')
                    self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 12, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                    self.TextBox_CodigoDeConfirmacao.setFocus()
            elif PageID in [PAGE_BY_NAME['Perfil'].page_id, '9_']: # Perfil, Tem ID especial
                if PageID == PAGE_BY_NAME['Perfil_'].page_id:
                    if self.PageIDAux== PAGE_BY_NAME['MudarSenha'].page_id:
                        if not self.DBManager.CalcularTributacao_is_running:
                            if self.TextBox_SenhaAtual.text() == self.DBManager.GetPasswdByUser(self.User):
                                if self.TextBox_Senha1.text() == self.TextBox_Senha2.text() and len(self.TextBox_Senha1.text())>3 and not self.TextBox_Senha1.text().isnumeric() and not self.TextBox_Senha1.text().isalpha():
                                    self.DBManager.ChangePassword(self.TextBox_Senha1.text())
                                    self.ClearPage()
                                    self.PageIDAux= PAGE_BY_NAME['Perfil'].page_id
                                    self.InsertGridLayout(1, 0, 1, 3)
                                    self.CreatePage9()
                                    self.PutHeader()
                                else:
                                    try: self.Label_Erro1.deleteLater()
                                    except Exception as e:
                                        print(e, traceback.format_exception(None, e, e.__traceback__))
                                    self.Label_Erro1 = QLabel()
                                    self.Label_Erro1.setStyleSheet('color: red')
                                    self.Label_Erro1.setFont(self.font12)
                                    self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                    self.Label_Erro1.setText('As senhas digitadas não são iguais.' if not self.TextBox_Senha1.text() == self.TextBox_Senha2.text() else "A senha tem que ter pelo menos 4 caracteres,\nter pelo menos um número e uma letra ou símbolo.")
                                    self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 13, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                                    self.TextBox_Senha2.setFocus()
                            else:
                                try: self.Label_Erro1.deleteLater()
                                except Exception as e:
                                    print(e, traceback.format_exception(None, e, e.__traceback__))
                                self.Label_Erro1 = QLabel()
                                self.Label_Erro1.setStyleSheet('color: red')
                                self.Label_Erro1.setFont(self.font12)
                                self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                self.Label_Erro1.setText('Senha atual não confere.')
                                self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 13, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                                self.TextBox_SenhaAtual.setFocus()
                        else:
                            MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')
                    elif self.PageIDAux== PAGE_BY_NAME['ConfirmacaoEmailPosMudanca'].page_id:
                        if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                            if self.TextBox_CodigoDeConfirmacao.text() == self.CodigoDeConfirmacaoGerado: # Condições para passar pra página 9
                                # Mudar Email
                                self.DBManager.UpdateEmail(self.TextBox_Email.text())
                                self.ClearPage()
                                self.PageIDAux= PAGE_BY_NAME['Perfil'].page_id
                                self.InsertGridLayout(1, 0, 1, 3)
                                self.CreatePage9()
                                self.PutHeader()
                            else:
                                try:
                                    self.Label_Erro1.deleteLater()
                                except:
                                    pass
                                self.Label_Erro1 = QLabel()
                                self.Label_Erro1.setStyleSheet('color: red')
                                self.Label_Erro1.setFont(self.font12)
                                self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                self.Label_Erro1.setText('O código não confere.')
                                self.F_GLayout[self.GCount - 1].addWidget(self.Label_Erro1, 12, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
                                self.TextBox_NomeDeUsuario.setFocus()
                        else:
                            MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
                else:
                    self.ClearPage()
                    self.PageIDAux= PAGE_BY_NAME['Perfil'].page_id
                    self.InsertGridLayout(1, 0, 1, 3)
                    self.CreatePage9()
                    self.PutHeader()
            elif PageID== PAGE_BY_NAME['EdicaoNegociacoes'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['EdicaoNegociacoes'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.CreatePage10()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['ARCA'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['ARCA'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_ARCA.CreatePage11()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['Desempenho'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['Desempenho'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Desempenho.CreatePage12()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['AnaliseMercadoDup'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AnaliseMercadoDup'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Mercado.CreatePage13()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['MudarEmail'].page_id:
                if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                    self.ClearPage()
                    self.PageIDAux= PAGE_BY_NAME['MudarEmail'].page_id
                    self.InsertGridLayout(1, 0, 1, 20)
                    self.CreatePage14()
                    self.PutHeader()
                else:
                    MessageBox_Msg1 = QMessageBox.about(self, 'Aviso', 'Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
            elif PageID== PAGE_BY_NAME['MudarSenha'].page_id: # Derivação do perfil, Tem ID especial
                self.ClearPage()
                self.PageIDAux= PAGE_BY_NAME['MudarSenha'].page_id
                self.InsertGridLayout(1, 0, 1, 20)
                self.CreatePage15()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['ConfirmarEncerrarConta'].page_id: # MessageBox, não tem ID
                self.CreatePage16()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['ConfirmacaoEmailPosMudanca'].page_id: # Derivação do perfil, Tem ID especial
                if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                    self.ClearPage()
                    self.PageIDAux= PAGE_BY_NAME['ConfirmacaoEmailPosMudanca'].page_id
                    self.InsertGridLayout(1, 0, 1, 20)
                    self.CreatePage17a()
                    self.PutHeader()
                else:
                    MessageBox_Msg1 = QMessageBox.about(self, 'Aviso', 'Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
            elif PageID== PAGE_BY_NAME['ConfirmacaoLogout'].page_id: # Derivação do perfil, Tem ID especial
                self.ClearPage()
                self.PageIDAux= PAGE_BY_NAME['ConfirmacaoLogout'].page_id
                self.InsertGridLayout(1, 0, 1, 20)
                self.CreatePage17b()
                self.PutHeader()
            elif PageID in [PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id,'18_']:
                if PageID == PAGE_BY_NAME['EdicaoNegociacoesBolsa_'].page_id:
                    if self.PageID== PAGE_BY_NAME['AdicionarCorretoraBolsa'].page_id:
                        if len(self.TextBox_NovaCorretora.text())>0 and len(self.TextBox_NovaCorretora.text())<9:
                            if not self.DBManager.CalcularTributacao_is_running:
                                BolsaOuCripto = self.BolsaOuCripto
                                Corretora = self.TextBox_NovaCorretora.text().replace(" ","_")
                                MoedaCorrente = self.ComboBox_Currency.currentText()
                                Executado = self.DBManager.AddCorretora(BolsaOuCripto, Corretora, MoedaCorrente)
                                if Executado:
                                    self.HMI_ARCA.Flag_RecalcularGraficos = True
                                    self.ClearPage()
                                    self.PageID= PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id
                                    self.PageIDAux = ''
                                    self.InsertGridLayout(1, 0, 1, 20)
                                    self.HMI_Trades.HMI_Trades_Bolsa.CreatePage18()
                                    self.PutHeader()
                                else:
                                    try: self.Label_Erro1.deleteLater()
                                    except Exception as e:
                                        print(e, traceback.format_exception(None, e, e.__traceback__))
                                    self.Label_Erro1 = QLabel()
                                    self.Label_Erro1.setStyleSheet('color: red')
                                    self.Label_Erro1.setFont(self.font12)
                                    self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                    self.Label_Erro1.setText('Corretora já existe.') # Substitui a string do erro mais provável
                                    self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 11, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                            else:
                                MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')
                        else:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('Insira um nome válido com até 8 caracteres.') # Substitui a string do erro mais provável
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 11, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                    elif self.PageID== PAGE_BY_NAME['RenomearCorretoraBolsa'].page_id:
                        if len(self.TextBox_NovoNomeCorretora.text())>0 and len(self.TextBox_NovoNomeCorretora.text())<9:
                            if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                                Executado = self.DBManager.RenameCorretora()
                                if Executado:
                                    self.HMI_ARCA.Flag_RecalcularGraficos = True
                                    self.ClearPage()
                                    self.PageID= PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id
                                    self.PageIDAux = ''
                                    self.InsertGridLayout(1, 0, 1, 20)
                                    self.HMI_Trades.HMI_Trades_Bolsa.CreatePage18()
                                    self.PutHeader()
                                else:
                                     try: self.Label_Erro1.deleteLater()
                                     except Exception as e:
                                        print(e, traceback.format_exception(None, e, e.__traceback__))
                                     self.Label_Erro1 = QLabel()
                                     self.Label_Erro1.setStyleSheet('color: red')
                                     self.Label_Erro1.setFont(self.font12)
                                     self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                     self.Label_Erro1.setText('Corretora já existe.') # Substitui a string do erro mais provável
                                     self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 11, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                            else:
                                MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
                        else:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('Insira um nome válido com até 8 caracteres.') # Substitui a string do erro mais provável
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 11, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                    elif self.PageID== PAGE_BY_NAME['SaldoContaCorrenteBolsa'].page_id:
                        try:
                            if not self.DBManager.CalcularTributacao_is_running:
                                self.DBManager.UpdateContaCorrente()
                                self.ClearPage()
                                self.PageID= PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id
                                self.PageIDAux = ''
                                self.InsertGridLayout(1, 0, 1, 20)
                                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage18()
                                self.PutHeader()
                            else:
                                MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')
                        except:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('Insira um valor válido.') # Substitui a string do erro mais provável
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 4, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
                else:
                    self.ClearPage()
                    self.PageID= PAGE_BY_NAME['EdicaoNegociacoesBolsa'].page_id
                    self.PageIDAux = ''
                    self.InsertGridLayout(1, 0, 1, 20)
                    self.HMI_Trades.HMI_Trades_Bolsa.CreatePage18()
                    self.PutHeader()
            elif PageID in [PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id,'19_']:
                if PageID == PAGE_BY_NAME['EdicaoNegociacoesCripto_'].page_id:
                    if self.PageID== PAGE_BY_NAME['AdicionarCorretoraCripto'].page_id:
                        if len(self.TextBox_NovaCorretora.text())>0 and len(self.TextBox_NovaCorretora.text())<12:
                            if not self.DBManager.CalcularTributacao_is_running:
                                BolsaOuCripto = self.BolsaOuCripto
                                Corretora = self.TextBox_NovaCorretora.text().replace(" ","_")
                                MoedaCorrente = self.ComboBox_Currency.currentText()
                                Executado = self.DBManager.AddCorretora(BolsaOuCripto, Corretora, MoedaCorrente)
                                if Executado:
                                    self.HMI_ARCA.Flag_RecalcularGraficos = True
                                    self.ClearPage()
                                    self.PageID= PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id
                                    self.PageIDAux = ''
                                    self.HMI_Trades.HMI_Trades_Criptomoedas.CreatePage19()
                                    self.PutHeader()
                                else:
                                    try: self.Label_Erro1.deleteLater()
                                    except Exception as e:
                                        print(e, traceback.format_exception(None, e, e.__traceback__))
                                    self.Label_Erro1 = QLabel()
                                    self.Label_Erro1.setStyleSheet('color: red')
                                    self.Label_Erro1.setFont(self.font12)
                                    self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                    self.Label_Erro1.setText('Corretora já existe.') # Substitui a string do erro mais provável
                                    self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 14, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                            else:
                                MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')
                        else:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('Insira um nome válido com até 11 caracteres.') # Substitui a string do erro mais provável
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 14, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                    elif self.PageID== PAGE_BY_NAME['RenomearCorretoraCripto'].page_id:
                        if len(self.TextBox_NovoNomeCorretora.text())>0 and len(self.TextBox_NovoNomeCorretora.text())<12:
                            if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                                Executado = self.DBManager.RenameCorretora()
                                if Executado:
                                    self.HMI_ARCA.Flag_RecalcularGraficos = True
                                    self.ClearPage()
                                    self.PageID= PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id
                                    self.PageIDAux = ''
                                    self.HMI_Trades.HMI_Trades_Criptomoedas.CreatePage19()
                                    self.PutHeader()
                                else:
                                     try: self.Label_Erro1.deleteLater()
                                     except Exception as e:
                                        print(e, traceback.format_exception(None, e, e.__traceback__))
                                     self.Label_Erro1 = QLabel()
                                     self.Label_Erro1.setStyleSheet('color: red')
                                     self.Label_Erro1.setFont(self.font12)
                                     self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                     self.Label_Erro1.setText('Corretora já existe.') # Substitui a string do erro mais provável
                                     self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 11, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                            else:
                                MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
                        else:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('Insira um nome válido com até 11 caracteres.') # Substitui a string do erro mais provável
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 11, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                else:
                    self.ClearPage()
                    self.PageID= PAGE_BY_NAME['EdicaoNegociacoesCripto'].page_id
                    self.PageIDAux = ''
                    self.HMI_Trades.HMI_Trades_Criptomoedas.CreatePage19()
                    self.PutHeader()
            elif PageID in [PAGE_BY_NAME['EditacaoContasCorrentesBancos'].page_id, 'Bancos_']:
                if PageID == PAGE_BY_NAME['EditacaoContasCorrentesBancos_'].page_id:
                    if self.PageID== PAGE_BY_NAME['AdicionarNovoBanco'].page_id:
                        if len(self.TextBox_NovoBanco.text())>0 and len(self.TextBox_NovoBanco.text())<12:
                            if not self.DBManager.CalcularTributacao_is_running:
                                Banco = self.TextBox_NovoBanco.text().replace(" ","_")
                                MoedaCorrente = self.ComboBox_Currency.currentText()
                                UserMoedaCorrente = self.DBManager.GetUserCoinCurrency()
                                Modo = None
                                Cotacao = None
                                if MoedaCorrente != UserMoedaCorrente and not self.DBManager.AtivoExisteNaTabelaDeCotacoes(MoedaCorrente):
                                    Cotacao = 0.
                                    Modo = "Manual"
                                    try:
                                        MessageBox_Msg1 = QMessageBox.about(self,'Aviso',"Identificamos uma nova moeda na base de dados.\nA operação seguinte pode levar alguns minutos,\npois irá buscar online a cotação atual dessa moeda.\nNÃO FECHE O PROGRAMA DURANTE O PROCESSO SEGUINTE!")
                                        Cotacao, _ = self.YahooFinance.GetCotacaoCripto(MoedaCorrente, UserMoedaCorrente)
                                        if Cotacao > 0: Modo = "Auto"
                                    except Exception as e:
                                        print(e, traceback.format_exception(None, e, e.__traceback__))
                                Executado = self.DBManager.AddBanco(Banco, MoedaCorrente, Modo, Cotacao)
                                if Executado:
                                    self.ClearPage()
                                    self.PageID= PAGE_BY_NAME['EditacaoContasCorrentesBancos'].page_id
                                    self.PageIDAux = ''
                                    self.InsertGridLayout(1, 0, 1, 20)
                                    self.HMI_Trades.CreatePageBancos()
                                    self.PutHeader()
                                else:
                                    try: self.Label_Erro1.deleteLater()
                                    except Exception as e:
                                        print(e, traceback.format_exception(None, e, e.__traceback__))
                                    self.Label_Erro1 = QLabel()
                                    self.Label_Erro1.setStyleSheet('color: red')
                                    self.Label_Erro1.setFont(self.font12)
                                    self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                    self.Label_Erro1.setText('Banco já existe.') # Substitui a string do erro mais provável
                                    self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 14, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                            else:
                                MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')
                        else:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('Insira um nome válido com até 11 caracteres.') # Substitui a string do erro mais provável
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 14, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                    elif self.PageID== PAGE_BY_NAME['RenomearBanco'].page_id:
                        if len(self.TextBox_NovoNomeBanco.text())>0 and len(self.TextBox_NovoNomeBanco.text())<12:
                            if not self.DBManager.CalcularTributacao_is_running:
                                Executado = self.DBManager.RenameBanco()
                                if Executado:
                                    self.ClearPage()
                                    self.PageID= PAGE_BY_NAME['EditacaoContasCorrentesBancos'].page_id
                                    self.PageIDAux = ''
                                    self.InsertGridLayout(1, 0, 1, 20)
                                    self.HMI_Trades.CreatePageBancos()
                                    self.PutHeader()
                                else:
                                     try: self.Label_Erro1.deleteLater()
                                     except Exception as e:
                                        print(e, traceback.format_exception(None, e, e.__traceback__))
                                     self.Label_Erro1 = QLabel()
                                     self.Label_Erro1.setStyleSheet('color: red')
                                     self.Label_Erro1.setFont(self.font12)
                                     self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                     self.Label_Erro1.setText('Banco já existe.') # Substitui a string do erro mais provável
                                     self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 11, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                            else:
                                MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')
                        else:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('Insira um nome válido com até 11 caracteres.') # Substitui a string do erro mais provável
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 11, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                else:
                    self.ClearPage()
                    self.PageID= PAGE_BY_NAME['EditacaoContasCorrentesBancos'].page_id
                    self.PageIDAux = ''
                    self.InsertGridLayout(1, 0, 1, 20)
                    self.HMI_Trades.CreatePageBancos()
                    self.PutHeader()
            elif PageID== PAGE_BY_NAME['AdicionarNovoBanco'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AdicionarNovoBanco'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.CreatePageBancosAdd()
                self.PutHeader()
            elif PageID == PAGE_BY_NAME['BancosDelete'].page_id:
                self.HMI_Trades.CreatePageBancosDelete()
            elif PageID== PAGE_BY_NAME['RenomearBanco'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['RenomearBanco'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.CreatePageBancosRename()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['AdicionarCorretoraBolsa'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AdicionarCorretoraBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage20()
                self.PutHeader()
            elif PageID == PAGE_BY_NAME['ConfirmarDeletarCorretoraBolsa'].page_id: # MessageBox
                if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                    self.HMI_Trades.HMI_Trades_Bolsa.CreatePage21()
                else:
                    MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
            elif PageID== PAGE_BY_NAME['RenomearCorretoraBolsa'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['RenomearCorretoraBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage22()
                self.PutHeader()
            elif PageID in [PAGE_BY_NAME['RegistrosBolsa'].page_id, '23_', '_23_']:
                if self.PageID== PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id:
                    if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                        if PageID == PAGE_BY_NAME['_RegistrosBolsa_'].page_id:
                            self.Modo = 'Manual'
                            self.DBManager.RenameAtivo()
                            self.HMI_ARCA.Flag_RecalcularGraficos = True
                        elif PageID == PAGE_BY_NAME['RegistrosBolsa_'].page_id:
                            self.Modo = 'Auto'
                            self.DBManager.RenameAtivo()
                            self.HMI_ARCA.Flag_RecalcularGraficos = True
                    else:
                        MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
                elif self.PageID== PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id:
                    if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                        if PageID == PAGE_BY_NAME['RegistrosBolsa_'].page_id:
                            self.Modo = 'Manual'
                            self.DBManager.RenameAtivo()
                            self.HMI_ARCA.Flag_RecalcularGraficos = True
                    else:
                        MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['RegistrosBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage23()
                self.PutHeader()

                if self.DBManager.VerificarSeTemEstoqueNegativo(): MessageBox_Msg1 = QMessageBox.about(self,'Aviso','ESTOQUE NEGATIVO! VERIFIQUE AS SUAS OPERAÇÕES!')
                elif self.DBManager.VerificarSeTemCustoNegativo(): MessageBox_Msg1 = QMessageBox.about(self,'Aviso','CUSTO NEGATIVO! VERIFIQUE AS SUAS OPERAÇÕES!')
            elif PageID in [PAGE_BY_NAME['InformarDepositosSaqBolsa'].page_id, '24_']:
                if PageID  == '24_':
                    try:
                        Data = str(self.Selecao_Ano+'/'+self.Selecao_Mes+'/'+self.Selecao_Dia+' '+self.Selecao_Hora+':'+self.Selecao_Minuto+':'+self.Selecao_Segundo)
                        Data = datetime.strptime(Data, '%Y/%m/%d %H:%M:%S')
                        sinal = 1 if self.Deposito else -1
                        Valor = float(self.TextBox_Valor.text())*sinal
                        if not self.DBManager.CalcularTributacao_is_running:
                            if self.DBManager.AddDepositoOuSaque(Data, Valor):
                                self.TextBox_Valor.setText('')
                                self.OnButtonPressed('Deposito')
                                self.HMI_Trades.HMI_Trades_Bolsa.CreateTable_24_2()
                                self.TextBox_Valor.setFocus()
                            else:
                                MessageBox_Msg1 = QMessageBox.about(self,'Informação','Movimentação não registrada.\nJá tem registro nessa data.')
                                self.TextBox_Valor.setFocus()
                        else:
                            MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nTente novamente mais tarde.')
                    except Exception as e:
                        print("Erro: Bolsa; Depósitos e Saques:\n",e)
                        self.TextBox_Valor.setStyleSheet('color: red')
                        self.TextBox_Valor.setFocus()
                else:
                    self.ClearPage()
                    self.PageID= PAGE_BY_NAME['InformarDepositosSaqBolsa'].page_id
                    self.PageIDAux = ''
                    self.InsertGridLayout(1, 0, 1, 20)
                    self.HMI_Trades.HMI_Trades_Bolsa.CreatePage24()
                    self.PutHeader()
            elif PageID== PAGE_BY_NAME['SaldoContaCorrenteBolsa'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['SaldoContaCorrenteBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage25()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['AdicionarNovoAtivo'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AdicionarNovoAtivo'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage26()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['RenomearAtivo'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['RenomearAtivo'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage27()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id:
                try: self.Label_Erro1.deleteLater()
                except Exception as e:
                    print(e, traceback.format_exception(None, e, e.__traceback__))
                if self.PageID== PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id:
                    # Registrar na DBManager a operação
                    try:
                        # Verificar se os dados inseridos são coerentes e só então registrar na DB
                        data = self.Selecao_Dia+"/"+self.Selecao_Mes+"/"+self.Selecao_Ano+" "+self.Selecao_Hora+":"+self.Selecao_Minuto+":"+self.Selecao_Segundo
                        data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
                        if data <= datetime.now():
                            if "%" in self.TextBox_TaxaB3.text():
                                TaxaB3Per = float(self.TextBox_TaxaB3.text().replace("%",""))
                                TaxaB3 = round(TaxaB3Per/100*int(self.TextBox_Qqt.text())*float(self.TextBox_Preco.text()),2)
                            else:
                                TaxaB3 = float(self.TextBox_TaxaB3.text())
                                TaxaB3Per = round(TaxaB3/int(self.TextBox_Qqt.text())/float(self.TextBox_Preco.text())*100,2)
                            check = int(self.TextBox_Qqt.text())
                            check = float(self.TextBox_Preco.text())
                            check = float(self.TextBox_Corretagem.text())
                            if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                                if self.PageID in ['36a','36b']:
                                    ativo = self.TextBox_NomeNovoAtivo.text().replace(" ","_")
                                elif self.PageID == PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id:
                                    ativo = self.ComboBox_Ativos.currentText().replace(" ","_")
                                Corretora = self.ComboBox_Corretoras.currentText().replace(" ","_")
                                data = self.HMI.Selecao_Dia+"/"+self.HMI.Selecao_Mes+"/"+self.HMI.Selecao_Ano+" "+self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo
                                data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
                                TaxaB3_text = self.HMI.TextBox_TaxaB3.text()
                                Qqt_text = self.HMI.TextBox_Qqt.text()
                                Preco_text = self.HMI.TextBox_Preco.text()
                                TipoDeOperacao = self.HMI.TipoDeOperacao
                                Corretagem_text = self.HMI.TextBox_Corretagem.text()
                                Obs_text = self.HMI.TextBox_Obs.text()

                                deubom = self.DBManager.AddOperacao_Bolsa(Corretora = Corretora,
                                                                          data = data,
                                                                          Preco_text = Preco_text,
                                                                          Qqt_text = Qqt_text,
                                                                          ativo = ativo,
                                                                          TipoDeOperacao = TipoDeOperacao,
                                                                          TaxaB3_text = TaxaB3_text,
                                                                          Corretagem_text = Corretagem_text,
                                                                          Obs_text = Obs_text
                                                                          )
                                if deubom:
                                    self.HMI_ARCA.Flag_RecalcularGraficos = True
                                    try:
                                        self.Msg = OperacaoRegistradaComSucesso.OperacaoRegistradaComSucesso(self, 4)
                                        self.LimparPage()
                                    except Exception as e:
                                        print(e)
                                else:
                                    try: self.Label_Erro1.deleteLater()
                                    except Exception as e:
                                        print(e, traceback.format_exception(None, e, e.__traceback__))
                                    self.Label_Erro1 = QLabel()
                                    self.Label_Erro1.setStyleSheet('color: red')
                                    self.Label_Erro1.setFont(self.font12)
                                    self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                    self.Label_Erro1.setText('Data inválida.\nTalvez já tenha uma operação nesse momento.') # Substitui a string do erro mais provável
                                    self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 4, 1, 3, Qt.AlignmentFlag.AlignRight)
                            else:
                                MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
                        else:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('Data inválida.') # Substitui a string do erro mais provável
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 4, 1, 3, Qt.AlignmentFlag.AlignRight)
                    except:
                        try: self.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro1 = QLabel()
                        self.Label_Erro1.setStyleSheet('color: red')
                        self.Label_Erro1.setFont(self.font12)
                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Label_Erro1.setText('Confira os valores inseridos.') # Substitui a string do erro mais provável
                        self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 4, 1, 3, Qt.AlignmentFlag.AlignRight)

                elif self.PageID in [PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id,PAGE_BY_NAME['AlterarNovaOperacaoManualBolsa'].page_id]:
                    try: self.Label_Erro1.deleteLater()
                    except Exception as e:
                        print(e, traceback.format_exception(None, e, e.__traceback__))
                    # Registrar na DBManager o ativo TextBox_NomeNovoAtivo
                    try:
                        # Verificar se os dados inseridos são coerentes e só então registrar na DB
                        data = self.Selecao_Dia+"/"+self.Selecao_Mes+"/"+self.Selecao_Ano+" "+self.Selecao_Hora+":"+self.Selecao_Minuto+":"+self.Selecao_Segundo
                        data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
                        if data<=datetime.now():
                            if "%" in self.TextBox_TaxaB3.text():
                                TaxaB3Per = float(self.TextBox_TaxaB3.text().replace("%",""))
                                TaxaB3 = round(TaxaB3Per/100*int(self.TextBox_Qqt.text())*float(self.TextBox_Preco.text()),2)
                            else:
                                TaxaB3 = float(self.TextBox_TaxaB3.text())
                                TaxaB3Per = round(TaxaB3/int(self.TextBox_Qqt.text())/float(self.TextBox_Preco.text())*100,2)
                            check = int(self.TextBox_Qqt.text())
                            check = float(self.TextBox_Preco.text())
                            check = float(self.TextBox_Corretagem.text())

                            if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                                try:
                                    self.HMI_ARCA.Flag_RecalcularGraficos = True
                                    ativo = self.TextBox_NomeNovoAtivo.text()
                                    ModoManualAtivo = self.ModoManualAtivo
                                    TipoDeAtivo = self.HMI.ComboBox_TipoDeAtivo.currentText()
                                    SubtipoDeAtivo = self.HMI.ComboBox_SubtipoDeAtivo.currentText()
                                    Setor = self.HMI.ComboBox_SetorAtivo.currentText()
                                    Cotacao = self.HMI.Cache_Cotacao
                                    Corretora = self.HMI.ComboBox_Corretoras.currentText().replace(" ","_")
                                    BolsaOuCripto = self.HMI.BolsaOuCripto
                                    self.DBManager.AddAtivo(ativo,
                                                            ModoManualAtivo,
                                                            TipoDeAtivo,
                                                            SubtipoDeAtivo,
                                                            Setor,
                                                            Cotacao,
                                                            Corretora,
                                                            BolsaOuCripto
                                                            )
                                    
                                    self.HMI_ARCA.Flag_RecalcularGraficos = True
                                    if self.PageID in ['36a','36b']:
                                        ativo = self.TextBox_NomeNovoAtivo.text().replace(" ","_")
                                    elif self.PageID == PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id:
                                        ativo = self.ComboBox_Ativos.currentText().replace(" ","_")
                                    Corretora = self.ComboBox_Corretoras.currentText().replace(" ","_")
                                    data = self.HMI.Selecao_Dia+"/"+self.HMI.Selecao_Mes+"/"+self.HMI.Selecao_Ano+" "+self.HMI.Selecao_Hora+":"+self.HMI.Selecao_Minuto+":"+self.HMI.Selecao_Segundo
                                    data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
                                    TaxaB3_text = self.HMI.TextBox_TaxaB3.text()
                                    Qqt_text = self.HMI.TextBox_Qqt.text()
                                    Preco_text = self.HMI.TextBox_Preco.text()
                                    TipoDeOperacao = self.HMI.TipoDeOperacao
                                    Corretagem_text = self.HMI.TextBox_Corretagem.text()
                                    Obs_text = self.HMI.TextBox_Obs.text()

                                    self.DBManager.AddOperacao_Bolsa(Corretora = Corretora,
                                                                     data = data,
                                                                     Preco_text = Preco_text,
                                                                     Qqt_text = Qqt_text,
                                                                     ativo = ativo,
                                                                     TipoDeOperacao = TipoDeOperacao,
                                                                     TaxaB3_text = TaxaB3_text,
                                                                     Corretagem_text = Corretagem_text,
                                                                     Obs_text = Obs_text
                                                                     ) # Sempre vai dar bom na criação do ativo
                                    self.AcabouDeRegistrarNovoAtivo = True
                                    self.ComboBox_Ativos.clear()
                                    ativos = self.DBManager.GetAtivos()
                                    for idx, ativo in enumerate(ativos):
                                        self.ComboBox_Ativos.addItem(ativo)
                                        if ativo == self.TextBox_NomeNovoAtivo.text():
                                            self.idxAtivo = idx
                                    self.ComboBox_Ativos.setCurrentIndex(self.idxAtivo)

                                    self.ClearPage()
                                    self.PageID= PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id
                                    self.PageIDAux = ''
                                    self.InsertGridLayout(1, 0, 1, 20)
                                    self.HMI_Trades.HMI_Trades_Bolsa.CreatePage28()
                                    self.PutHeader()
                                    self.Msg = OperacaoRegistradaComSucesso.OperacaoRegistradaComSucesso(self, 7)
                                except Exception as e:
                                    print(e)
                            else:
                                MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
                        else:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('Data inválida.') # Substitui a string do erro mais provável
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 5, 1, 1, Qt.AlignmentFlag.AlignCenter)
                    except:
                        try: self.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro1 = QLabel()
                        self.Label_Erro1.setStyleSheet('color: red')
                        self.Label_Erro1.setFont(self.font12)
                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Label_Erro1.setText('Confira os valores inseridos.') # Substitui a string do erro mais provável
                        self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 5, 1, 1, Qt.AlignmentFlag.AlignCenter)

                elif len(self.ComboBox_Ativos)>0:
                    self.ClearPage()
                    self.PageID= PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id
                    self.PageIDAux = ''
                    self.InsertGridLayout(1, 0, 1, 20)
                    self.HMI_Trades.HMI_Trades_Bolsa.CreatePage28()
                    self.PutHeader()
            elif PageID== PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AlterarOperacoesBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage29()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['DeletarOperacoesBolsa'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['DeletarOperacoesBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage30()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['NaoImplementada31a'].page_id: MessageBox_Msg1 = QMessageBox.about(self,'Informação','Funcionalidade ainda não implementada.')
            elif PageID== PAGE_BY_NAME['NaoImplementada31b'].page_id: MessageBox_Msg1 = QMessageBox.about(self,'Informação','Funcionalidade ainda não implementada.')
            elif PageID== PAGE_BY_NAME['NaoImplementada32a'].page_id: MessageBox_Msg1 = QMessageBox.about(self,'Informação','Funcionalidade ainda não implementada.')
            elif PageID== PAGE_BY_NAME['NaoImplementada32b'].page_id: MessageBox_Msg1 = QMessageBox.about(self,'Informação','Funcionalidade ainda não implementada.')
            elif PageID == PAGE_BY_NAME['33'].page_id:
                try:
                    self.LW = LoadingWindow.LoadingWindow(self)
                    self.LW.show()
                    self.Thread_BuscarSetoresExistentes = WorkerThread('Thread_BuscarSetoresExistentes', self)
                    self.Thread_BuscarSetoresExistentes.start()
                except Exception as e: print(e)
            elif PageID== PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['CotacaoEncontradaBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage34a()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['CotacaoEncontradaManualBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage34b()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['CotacaoNaoEncontradaBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage35a()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['CotacaoNaoEncontradaManualBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage35b()
                self.PutHeader()
            elif PageID == PAGE_BY_NAME['InformarNovaOperacaoManualBolsa_Auto'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.ModoManualAtivo = False
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage36a()
                self.PutHeader()
            elif PageID == PAGE_BY_NAME['InformarNovaOperacaoManualBolsa_Manual'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['InformarNovaOperacaoManualBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.ModoManualAtivo = True
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage36a()
                self.PutHeader()
            elif PageID == PAGE_BY_NAME['ImportarUsuario'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AlterarNovaOperacaoManualBolsa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.ModoManualAtivo = True
                self.HMI_Trades.HMI_Trades_Bolsa.CreatePage36a()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['AdicionarCorretoraCripto'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AdicionarCorretoraCripto'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Criptomoedas.CreatePage37()
                self.PutHeader()
            elif PageID == PAGE_BY_NAME['ConfirmarDeletarCorretoraCripto'].page_id: # MessageBox
                self.HMI_Trades.HMI_Trades_Criptomoedas.CreatePage38()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['RenomearCorretoraCripto'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['RenomearCorretoraCripto'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Criptomoedas.CreatePage39()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['RegistrosCripto'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['RegistrosCripto'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Criptomoedas.CreatePage40()
                self.PutHeader()

                if self.DBManager.VerificarPrimeiraOperacao(): MessageBox_Msg1 = QMessageBox.about(self,'Aviso','A primeira operação deve ser do tipo DEPÓSITO ou DROP.')
                elif self.DBManager.VerificarSeTemEstoqueNegativo(): MessageBox_Msg1 = QMessageBox.about(self,'Aviso','ESTOQUE NEGATIVO! VERIFIQUE AS SUAS OPERAÇÕES!')
                elif self.DBManager.VerificarSeTemCustoNegativo(): MessageBox_Msg1 = QMessageBox.about(self,'Aviso','CUSTO NEGATIVO! VERIFIQUE AS SUAS OPERAÇÕES!')
            elif PageID== PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id:
                try: self.Label_Erro1.deleteLater()
                except Exception as e:
                    print(e, traceback.format_exception(None, e, e.__traceback__))
                if self.PageID== PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id:
                    # Registrar na DBManager a operação
                    try:
                        # Verificar se os dados inseridos são coerentes e só então registrar na DB
                        data = self.Selecao_Dia+"/"+self.Selecao_Mes+"/"+self.Selecao_Ano+" "+self.Selecao_Hora+":"+self.Selecao_Minuto+":"+self.Selecao_Segundo
                        data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
                        if len(self.TextBox_Taxa.text())>0: check = float(self.TextBox_Taxa.text())
                        check = float(self.TextBox_Qqt.text())
                        check = float(self.TextBox_Preco.text())
                        if len(self.TextBox_Conversao.text())>0: check = float(self.TextBox_Conversao.text())
                        if not self.TextBox_Par_Esquerda.text() == self.TextBox_Par_Direita.text():
                            if not self.TextBox_Par_Esquerda.text() == '' or not self.TextBox_Par_Direita.text() == '':
                                if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                                    if self.PageID in ['36a','36b']:
                                        ativo = self.TextBox_NomeNovoAtivo.text().replace(" ","_")
                                    elif self.PageID == PAGE_BY_NAME['InformarNovaOperacaoBolsa'].page_id:
                                        ativo = self.ComboBox_Ativos.currentText().replace(" ","_")
                                    Corretora = self.ComboBox_Corretoras.currentText().replace(" ","_")
                                    data = self.Selecao_Dia+"/"+self.Selecao_Mes+"/"+self.Selecao_Ano+" "+self.Selecao_Hora+":"+self.Selecao_Minuto+":"+self.Selecao_Segundo
                                    data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
                                    TaxaB3_text = self.TextBox_TaxaB3.text()
                                    Qqt_text = self.TextBox_Qqt.text()
                                    Preco_text = self.TextBox_Preco.text()
                                    TipoDeOperacao = self.TipoDeOperacao
                                    Corretagem_text = self.TextBox_Corretagem.text()
                                    Obs_text = self.TextBox_Obs.text()
                                    Taxa_text = self.TextBox_Taxa.text()
                                    MoedaDaTaxa_text = self.TextBox_MoedaDaTaxa.text()
                                    Conversao_text = self.TextBox_Conversao.text()
                                    Par_Esquerda_text = self.TextBox_Par_Esquerda.text()
                                    Par_Direita_text = self.TextBox_Par_Direita.text()

                                    deubom = self.DBManager.AddOperacao_Cripto(Corretora = Corretora,
                                                                               data = data,
                                                                               TaxaB3_text = TaxaB3_text,
                                                                               Qqt_text = Qqt_text,
                                                                               Preco_text = Preco_text,
                                                                               TipoDeOperacao = TipoDeOperacao,
                                                                               Corretagem_text = Corretagem_text,
                                                                               Obs_text = Obs_text,
                                                                               Taxa_text = Taxa_text,
                                                                               MoedaDaTaxa_text = MoedaDaTaxa_text,
                                                                               Conversao_text = Conversao_text,
                                                                               Par_Esquerda_text = Par_Esquerda_text,
                                                                               Par_Direita_text = Par_Direita_text,
)
                                    if deubom:
                                        self.HMI_ARCA.Flag_RecalcularGraficos = True
                                        try:
                                            self.Msg = OperacaoRegistradaComSucesso.OperacaoRegistradaComSucesso(self, 5)
                                            self.LimparPage()
                                        except Exception as e:
                                            print(e)
                                    else:
                                        try: self.Label_Erro1.deleteLater()
                                        except Exception as e:
                                            print(e, traceback.format_exception(None, e, e.__traceback__))
                                        self.Label_Erro1 = QLabel()
                                        self.Label_Erro1.setStyleSheet('color: red')
                                        self.Label_Erro1.setFont(self.font12)
                                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                        self.Label_Erro1.setText('Data inválida.\nTalvez já tenha uma operação nesse momento.') # Substitui a string do erro mais provável
                                        self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 4, 1, 3, Qt.AlignmentFlag.AlignCenter)
                                else:
                                    MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
                            else:
                                try: self.Label_Erro1.deleteLater()
                                except Exception as e:
                                    print(e, traceback.format_exception(None, e, e.__traceback__))
                                self.Label_Erro1 = QLabel()
                                self.Label_Erro1.setStyleSheet('color: red')
                                self.Label_Erro1.setFont(self.font12)
                                self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                self.Label_Erro1.setText('As moedas devem ser declaradas.') # Substitui a string do erro mais provável
                                self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 4, 1, 3, Qt.AlignmentFlag.AlignCenter)
                        else:
                            try: self.Label_Erro1.deleteLater()
                            except Exception as e:
                                print(e, traceback.format_exception(None, e, e.__traceback__))
                            self.Label_Erro1 = QLabel()
                            self.Label_Erro1.setStyleSheet('color: red')
                            self.Label_Erro1.setFont(self.font12)
                            self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.Label_Erro1.setText('As moedas nos pares não podem ser iguais.') # Substitui a string do erro mais provável
                            self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 4, 1, 3, Qt.AlignmentFlag.AlignCenter)
                    except:
                        try: self.Label_Erro1.deleteLater()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        self.Label_Erro1 = QLabel()
                        self.Label_Erro1.setStyleSheet('color: red')
                        self.Label_Erro1.setFont(self.font12)
                        self.Label_Erro1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.Label_Erro1.setText('Confira os valores inseridos.') # Substitui a string do erro mais provável
                        self.F_GLayout[self.GCount-1].addWidget(self.Label_Erro1, 6, 4, 1, 3, Qt.AlignmentFlag.AlignCenter)
                else:
                    self.ClearPage()
                    self.PageID= PAGE_BY_NAME['InformarNovaOperacaoCripto'].page_id
                    self.PageIDAux = ''
                    self.InsertGridLayout(1, 0, 1, 20)
                    self.HMI_Trades.HMI_Trades_Criptomoedas.CreatePage41()
                    self.PutHeader()
            elif PageID == PAGE_BY_NAME['IdeiaAbandonada'].page_id: # Ideia abandonada
                # self.ClearPage()
                # self.PageID = PAGE_BY_NAME['IdeiaAbandonada'].page_id:
                # self.PageIDAux = ''
                # self.InsertGridLayout(1, 0, 1, 20)
                # self.HMI_Trades.HMI_Trades_Criptomoedas.CreatePage42()
                # self.PutHeader()
                pass
            elif PageID== PAGE_BY_NAME['AlterarOperacaoCripto'].page_id: # Alter Cripto Operation
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AlterarOperacaoCripto'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Criptomoedas.CreatePage43()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['DeletarOperacaoCripto'].page_id: # Delete Cripto Operation
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['DeletarOperacaoCripto'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Trades.HMI_Trades_Criptomoedas.CreatePage44()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['InsercaoCotacoesManuais'].page_id:
                if not self.DBManager.CalcularTributacao_is_running and not self.AtualizarCotacoes_is_running:
                    self.ClearPage()
                    self.PageIDAux= PAGE_BY_NAME['InsercaoCotacoesManuais'].page_id # Tem ID especial, porque é compartilhado com outros ramos
                    self.InsertGridLayout(1, 0, 1, 20)
                    self.CreatePage45()
                    self.PutHeader()
                else:
                    MessageBox_Msg1 = QMessageBox.about(self,'Aviso','Existe outra operação em andamento.\nPode ser que a tabela de cotações\nesteja sendo atualizada\n\nTente novamente mais tarde.')
            elif PageID== PAGE_BY_NAME['AcoesNegocios'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AcoesNegocios'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_ARCA.CreatePage46()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['RealEstate'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['RealEstate'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_ARCA.CreatePage47()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['Caixa'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['Caixa'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_ARCA.CreatePage48()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['AtivosInternacionais'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['AtivosInternacionais'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_ARCA.CreatePage49()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['CriptoARCA'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['CriptoARCA'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_ARCA.CreatePage50()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['Tributacao'].page_id:
                self.ClearPage()
                self.PageID= PAGE_BY_NAME['Tributacao'].page_id
                self.PageIDAux = ''
                self.InsertGridLayout(1, 0, 1, 20)
                self.HMI_Tributacao.CreatePage51()
                self.PutHeader()
            elif PageID== PAGE_BY_NAME['EscolhaMoeda'].page_id:
                self.ClearPage()
                self.PageIDAux= PAGE_BY_NAME['EscolhaMoeda'].page_id # Derivação do perfil, Tem ID especial
                self.InsertGridLayout(1, 0, 1, 20)
                self.CreatePageChooseCurrency()
                self.PutHeader()
            elif PageID =='Confirmar email':
                pass
            elif PageID == PAGE_BY_NAME['Inserir nova senha'].page_id:
                pass
            elif PageID == PAGE_BY_NAME['Info1'].page_id: self.CreatePageInfo1()
            elif PageID == PAGE_BY_NAME['Info2'].page_id: self.CreatePageInfo2()
            elif PageID == PAGE_BY_NAME['Info3'].page_id: self.CreatePageInfo3()
            elif PageID == PAGE_BY_NAME['Info4'].page_id: self.CreatePageInfo4()
            elif PageID == PAGE_BY_NAME['Info5'].page_id: self.CreatePageInfo5()
            elif PageID == PAGE_BY_NAME['Info6'].page_id: self.CreatePageInfo6()
            elif PageID == PAGE_BY_NAME['Info7'].page_id: self.CreatePageInfo7()
            elif PageID == PAGE_BY_NAME['Info8'].page_id: self.CreatePageInfo8()
            elif PageID == PAGE_BY_NAME['Info9'].page_id: self.CreatePageInfo9()
            elif PageID == PAGE_BY_NAME['Info10'].page_id: self.CreatePageInfo10()
            elif PageID == PAGE_BY_NAME['Info11'].page_id: self.CreatePageInfo11()
            elif PageID == PAGE_BY_NAME['Info12'].page_id: self.CreatePageInfo12()
            elif PageID == PAGE_BY_NAME['Info13'].page_id: self.CreatePageInfo13()
            elif PageID == PAGE_BY_NAME['Info14'].page_id: self.CreatePageInfo14()
            elif PageID == PAGE_BY_NAME['Info15'].page_id: self.CreatePageInfo15()
            elif PageID == PAGE_BY_NAME['Info16'].page_id: self.CreatePageInfo16()
            elif PageID == PAGE_BY_NAME['Info17'].page_id: self.CreatePageInfo17()
            elif PageID == PAGE_BY_NAME['Info18'].page_id: self.CreatePageInfo18()
            elif PageID == PAGE_BY_NAME['Info19'].page_id: self.CreatePageInfo19()
            elif PageID == PAGE_BY_NAME['Info20'].page_id: self.CreatePageInfo20()
            elif PageID == PAGE_BY_NAME['Info21'].page_id: self.CreatePageInfo21()
            elif PageID == PAGE_BY_NAME['Info22'].page_id: self.CreatePageInfo22()
            elif PageID == PAGE_BY_NAME['Info23'].page_id: self.CreatePageInfo23()
            elif PageID == PAGE_BY_NAME['Info24'].page_id: self.CreatePageInfo24()
            elif PageID == PAGE_BY_NAME['Info25'].page_id: self.CreatePageInfo25()
            elif PageID == PAGE_BY_NAME['Info26'].page_id: self.CreatePageInfo26()
            elif PageID == PAGE_BY_NAME['Info27'].page_id: self.CreatePageInfo27()
