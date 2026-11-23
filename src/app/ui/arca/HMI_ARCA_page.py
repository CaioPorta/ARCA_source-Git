# -*- coding: utf-8 -*-
"""
HMI_ARCA helper. Behaviour is split across several baseless mixin modules
(one file per concern) that are re-composed here so the public surface stays
`from ui.trades.HMI_Trades_page import HMI_Trades` / ... .

    HMI_Events - events helpers (inherited automatically).
    HMI_PageBuilders - pagebuilders helpers (inherited automatically).
    HMI_Presentation - presentation helpers (inherited automatically).
"""

from ui.arca.HMI_Events import HMI_Events
from ui.arca.HMI_PageBuilders import HMI_PageBuilders
from ui.arca.HMI_Presentation import HMI_Presentation


class HMI_ARCA(HMI_Events, HMI_PageBuilders, HMI_Presentation):
    """Composition root; only lifecycle/state lives here (see module docstring)."""

    def __init__(self, HMI):
        self.HMI = HMI
        self.Flag_RecalcularGraficos = True
        self.GraficoEspecifico_Name = ""
        self.MontanteEmAplicacao = 0
        self.MostrarValoresMaioresQue = 1
