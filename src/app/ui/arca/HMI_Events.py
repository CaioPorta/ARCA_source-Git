# -*- coding: utf-8 -*-
"""
ARCA behaviour split into a single concern.
HMI_Events - events helpers (inherited by the composition root).
"""
import numpy as np
from PyQt5.QtGui import (QFont, QCursor)
from PyQt5.QtWidgets import (QPushButton)
from PyQt5.QtCore import (Qt)
from ui.pages import (PAGE_BY_NAME)


class HMI_Events:
    def CallCreatePage(self):
        if self.GraficoEspecifico_Name in ["Ações Nacionais", "Fundos de investimentos: Ações e Negócios"]:
            self.HMI.CreatePage(PAGE_BY_NAME['AcoesNegocios'].page_id)
        elif self.GraficoEspecifico_Name in ["Fundos Imobiliários", "Terrenos", "Construções"]:
            self.HMI.CreatePage(PAGE_BY_NAME['RealEstate'].page_id)
        elif self.GraficoEspecifico_Name in ["Renda Fixa", "Tesouro Direto e Títulos Públicos", "Previdência Privada", "COE", "Fundos de Investimento: Renda Fixa"]:
            self.HMI.CreatePage(PAGE_BY_NAME['Caixa'].page_id)
        elif self.GraficoEspecifico_Name in ["BDR", "Fundos de Investimento: Ações Internacionais"]:
            self.HMI.CreatePage(PAGE_BY_NAME['AtivosInternacionais'].page_id)
        elif self.GraficoEspecifico_Name in ["Criptomoedas"]:
            self.HMI.CreatePage(PAGE_BY_NAME['CriptoARCA'].page_id)


    def ProximoGraficoEspecifico(self, TipoDeAtivo):
        if TipoDeAtivo == "Ações e Negócios":
            Subtipos = ["Ações Nacionais", "Fundos de investimentos: Ações e Negócios"]
            if self.GraficoEspecifico_Name in Subtipos:
                CurrentIndex = Subtipos.index(self.GraficoEspecifico_Name)
                if len(Subtipos) > CurrentIndex+1: index = CurrentIndex+1
                else: index = 0
                self.GraficoEspecifico_Name = Subtipos[index]
            else:
                self.GraficoEspecifico_Name = Subtipos[0]
        elif TipoDeAtivo == "Real Estate":
            Subtipos = ["Fundos Imobiliários", "Terrenos", "Construções"]
            if self.GraficoEspecifico_Name in Subtipos:
                CurrentIndex = Subtipos.index(self.GraficoEspecifico_Name)
                if len(Subtipos) > CurrentIndex+1: index = CurrentIndex+1
                else: index = 0
                self.GraficoEspecifico_Name = Subtipos[index]
            else:
                self.GraficoEspecifico_Name = Subtipos[0]
        elif TipoDeAtivo == "Caixa":
            Subtipos = ["Renda Fixa", "Tesouro Direto e Títulos Públicos", "Previdência Privada", "COE", "Fundos de Investimento: Renda Fixa"]
            if self.GraficoEspecifico_Name in Subtipos:
                CurrentIndex = Subtipos.index(self.GraficoEspecifico_Name)
                if len(Subtipos) > CurrentIndex+1: index = CurrentIndex+1
                else: index = 0
                self.GraficoEspecifico_Name = Subtipos[index]
            else:
                self.GraficoEspecifico_Name = Subtipos[0]
        elif TipoDeAtivo == "Ativos Internacionais":
            Subtipos = ["BDR", "Fundos de Investimento: Ações Internacionais", "Criptomoedas"]
            if self.GraficoEspecifico_Name in Subtipos:
                CurrentIndex = Subtipos.index(self.GraficoEspecifico_Name)
                if len(Subtipos) > CurrentIndex+1: index = CurrentIndex+1
                else: index = 0
                self.GraficoEspecifico_Name = Subtipos[index]
            else:
                self.GraficoEspecifico_Name = Subtipos[0]
        self.CreateGraph_Page11_Especifica()


    def OnButtonPressed(self, ButtonPressed):
        FontColorLineEdit = "green"
        if ButtonPressed == "Change Carteira Graph":
            self.Flag_RecalcularGraficos = True
            self.HMI.GraphWidget_Carteira.deleteLater()
            if self.CarteiraGraph_id == 'pie': self.HMI.GraphWidget_Carteira = self.CreateGraph_Page11_Carteira_bar()
            elif self.CarteiraGraph_id == 'bar': self.HMI.GraphWidget_Carteira = self.CreateGraph_Page11_Carteira_pie()
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.GraphWidget_Carteira, 2, 2, 2, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            if self.HMI.frameGeometry().width() / self.HMI.frameGeometry().height() < 1.9577: proporcao = 1 / 6
            elif self.HMI.frameGeometry().width() / self.HMI.frameGeometry().height() < 2.6202: proporcao = 1 / 8
            else: proporcao = 1 / 10
            self.HMI.GraphWidget_Carteira.setFixedSize(int(self.HMI.frameGeometry().width() * proporcao), int(self.HMI.frameGeometry().width() * proporcao))
            self.HMI.Button_CarteiraInvisivel.deleteLater()
            self.HMI.Button_CarteiraInvisivel = QPushButton()
            self.HMI.Button_CarteiraInvisivel.pressed.connect(lambda: self.OnButtonPressed('Change Carteira Graph'))
            self.HMI.Button_CarteiraInvisivel.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white; border: 1px solid rgba(0, 0, 0, 0); border: none; outline: none;')
            self.HMI.Button_CarteiraInvisivel.setFixedSize(int(self.HMI.frameGeometry().width() * proporcao), int(self.HMI.frameGeometry().width() * proporcao))
            self.HMI.Button_CarteiraInvisivel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Button_CarteiraInvisivel, 2, 2, 2, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        elif ButtonPressed == "TextBox_GastoMensal":
            try:
                aux = float(self.HMI.TextBox_GastoMensal.text())
                self.HMI.TextBox_MesesDeReserva.setFocus()
                self.HMI.DBManager.Update_GastoMensal(aux)
            except:
                self.HMI.TextBox_GastoMensal.setText(str(self.HMI.DBManager.GetGastoMensal()))

        elif ButtonPressed == "TextBox_MesesDeReserva":
            try:
                aux = int(float(self.HMI.TextBox_MesesDeReserva.text()))
                self.HMI.TextBox_MesesDeReserva.setText(str(aux))
                self.HMI.TextBox_MesesDeReserva.clearFocus()
                self.HMI.DBManager.Update_MesesDeReserva(aux)
            except:
                self.HMI.TextBox_MesesDeReserva.setText(str(self.HMI.DBManager.GetMesesDeReserva()))

        elif ButtonPressed == "MostrarValoresMaioresQue":
            self.MostrarValoresMaioresQue = float(self.HMI.TextBox_MostrarValoresMaioresQue.text())
            self.HMI.UpdatePage()
            self.HMI.TextBox_MostrarValoresMaioresQue.clearFocus()

        elif ButtonPressed == "Visão Geral":
            self.MainGraphIsShowing = "Visão Geral"
            self.HMI.UpdatePage()
            self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
            self.HMI.Button_VisaoGeral.setFont(QFont('Times New Roman', 18, QFont.Bold))
            self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
            try:
                self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
            except:pass
            try:
                self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_Setor.setFont(self.HMI.font16)
            except:pass

        elif ButtonPressed == "Ativo por corretora":
            self.MainGraphIsShowing = "Ativo por corretora"
            self.HMI.UpdatePage()
            self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_VisaoGeral.setFont(self.HMI.font16)
            self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
            self.HMI.Button_AtivoPorCorretora.setFont(QFont('Times New Roman', 18, QFont.Bold))
            try:
                self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
            except:pass
            try:
                self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_Setor.setFont(self.HMI.font16)
            except:pass

        elif ButtonPressed == "Ativo por setor":
            self.MainGraphIsShowing = "Ativo por setor"
            self.HMI.UpdatePage()
            self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_VisaoGeral.setFont(self.HMI.font16)
            self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
            try:
                self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
            except:pass
            try:
                self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
                self.HMI.Button_Setor.setFont(QFont('Times New Roman', 18, QFont.Bold))
            except:pass

        elif ButtonPressed == "Total de UserCoin por corretora":
            self.MainGraphIsShowing = "Total de UserCoin por corretora"
            self.HMI.UpdatePage()
            self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_VisaoGeral.setFont(self.HMI.font16)
            self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
            try:
                self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none; border: 1px solid rgba(0, 255, 0, 1)")
                self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(QFont('Times New Roman', 18, QFont.Bold))
            except:pass
            try:
                self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_Setor.setFont(self.HMI.font16)
            except:pass

        elif ButtonPressed == "Desempenho do ativo":
            self.MainGraphIsShowing = "Desempenho do ativo"
            self.HMI.UpdatePage()
            self.HMI.Button_VisaoGeral.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_VisaoGeral.setFont(self.HMI.font16)
            self.HMI.Button_AtivoPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
            self.HMI.Button_AtivoPorCorretora.setFont(self.HMI.font16)
            try:
                self.HMI.Button_TotalDeUserCoinPorCorretora.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_TotalDeUserCoinPorCorretora.setFont(self.HMI.font16)
            except:pass
            try:
                self.HMI.Button_Setor.setStyleSheet("background-color: black; color: "+FontColorLineEdit+"; outline: none;")
                self.HMI.Button_Setor.setFont(self.HMI.font16)
            except:pass


    def getPercentage(self, pct, allvalues):
        absolute = float(pct / 100.*np.sum(allvalues))
        if self.HMI.ShowValues: retorno = "{:.1f}%\n({}{:.2f})".format(pct, self.HMI.DBManager.GetUserCoinCurrency(), absolute)
        else: retorno = "{:.1f}%".format(pct)
        return retorno
