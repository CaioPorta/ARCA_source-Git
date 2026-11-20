"""
graphical_thread - Application entry point / process lifecycle.

Owns the Qt application instance and the main window (IHMmain): it creates the
QApplication, instantiates and initializes IHMmain, runs the event loop and
shuts down cleanly (disconnecting the DB once background work has finished).

Kept separate from HMI.py so that file can focus on widgets/pages while this
module owns startup/shutdown.
"""
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication

from core import DBManager
from ui.before_login.HMI import IHMmain


class graphical_thread:
    def __init__(self,):
        self.mIHM = None
        self.app = None
        self.DBManager = DBManager
        self.AtualizarCotacoes_is_running = False

    def run(self,):
        self.app = QApplication(sys.argv)
        self.app.setStyle("fusion")
        try:
            self.mIHM = IHMmain()
            self.mIHM.initialize()
            self.app.exec_()
            if not getattr(self.DBManager, "CalcularTributacao_is_running", False) or self.AtualizarCotacoes_is_running:
                self.mIHM.DBManager.Disconnect()
            else:
                while getattr(self.DBManager, "CalcularTributacao_is_running", False) or self.AtualizarCotacoes_is_running:
                    pass
                self.mIHM.DBManager.Disconnect()
        except Exception as error:
            if self.mIHM is not None and getattr(self.mIHM, "DBManager", None) is not None:
                self.mIHM.DBManager.Disconnect()
            self.app.quit()
            sys.exit()
            QCoreApplication.quit()
            print('Erro crítico: \n' + repr(error))
