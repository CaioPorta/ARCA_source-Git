# -*- coding: utf-8 -*-
"""
Trades behaviour split into a single concern.
HMI_Events - events helpers (inherited by the composition root).
"""


class HMI_Events:
    def OnButtonPressed(self, ButtonPressed):
        if ButtonPressed == 'BancosUpdateCC':
            try:
                teste = float(self.HMI.TextBox_CC.text())
                self.HMI.DBManager.UpdateContaCorrente_Banco()
                self.HMI.TextBox_CC.setStyleSheet('background-color: white; color: green')
                self.HMI.TextBox_CC.setText('')
                self.HMI.TextBox_Msg2.setText(self.HMI.DBManager.GetBancoCoinCurrency(self.HMI.ComboBox_Bancos.currentText())+' '+str(self.HMI.DBManager.GetValorEmContaCorrente_Banco(self.HMI.ComboBox_Bancos.currentText())))
            except:
                self.HMI.TextBox_CC.setStyleSheet('background-color: white; color: red')
