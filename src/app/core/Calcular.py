# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 23:53:39 2021

@author: caiop
"""

import decimal

import pandas as pd
import numpy as np

class Calcular(object):
    def __init__(self, HMI):
        self.HMI = HMI
        self.ctx = decimal.Context()
        self.ctx.prec = 10

    def Rendimento(self):
        Rendimento = 0.
        Investido = 0.
        try:
            corretoras = self.HMI.DBManager.GetCorretoras("Bolsa")
            for corretora in corretoras:
                Investido += self.HMI.DBManager.GetTotalInvestidoEmCorretora(corretora, "Bolsa")
            corretoras = self.HMI.DBManager.GetCorretoras("Cripto")
            for corretora in corretoras:
                Investido += self.HMI.DBManager.GetTotalInvestidoEmCorretora(corretora, "Cripto") # Tem que somar todos os custos e subtrair todos os volumes de taxa
            MontanteNasCorretoras = self.HMI.DBManager.GetMontanteNasCorretoras()
            if not Investido == 0:
                Rendimento = (MontanteNasCorretoras - Investido) / Investido * 100
            else:
                Rendimento = 0.
            Rendimento = round(Rendimento, 2)
        except:
            return 'Erro'
        return Rendimento

    def Patrimonio(self):
        """
        Retorna a soma do patrimonio em cada corretora.
        Se der problema, retorna -1.
        Se alguma cotação não for encontrada ou for zero, retorna -2.

        """
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
            Bancos = self.HMI.DBManager.GetBancos()
            for Banco in Bancos:
                Patrimonio += self.HMI.DBManager.GetValorEmContaCorrente_Banco(Banco)
        except:
            return -1
        return round(Patrimonio, 2)

    def float_to_str(self, f):
        """
        Convert the given float to a string,
        without resorting to scientific notation
        """
        if isinstance(f, str): return f
        d1 = self.ctx.create_decimal(repr(f))
        return format(d1, 'f')