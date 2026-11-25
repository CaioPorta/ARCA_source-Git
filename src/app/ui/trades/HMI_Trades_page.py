# -*- coding: utf-8 -*-
"""
HMI_Trades helper. Behaviour is split across several baseless mixin modules
(one file per concern) that are re-composed here so the public surface stays
`from ui.trades.HMI_Trades_page import HMI_Trades` / ... .

    HMI_Events - events helpers (inherited automatically).
    HMI_PageBuilders - pagebuilders helpers (inherited automatically).
"""

from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QToolTip)
import ui.trades.trades_bolsa.HMI_Trades_Bolsa_page as HMI_Trades_Bolsa_page
import ui.trades.trades_criptomoedas.HMI_Trades_Criptomoedas_page as HMI_Trades_Criptomoedas_page
from ui.trades.HMI_Events import HMI_Events
from ui.trades.HMI_PageBuilders import HMI_PageBuilders


class HMI_Trades(HMI_Events, HMI_PageBuilders):
    """Composition root; only lifecycle/state lives here (see module docstring)."""

    def __init__(self, HMI):
        self.HMI = HMI
        QToolTip.setFont(QFont('Arial', 12))
        self.HMI_Trades_Bolsa = HMI_Trades_Bolsa_page.HMI_Trades_Bolsa(HMI)
        self.HMI_Trades_Criptomoedas = HMI_Trades_Criptomoedas_page.HMI_Trades_Criptomoedas(HMI)
