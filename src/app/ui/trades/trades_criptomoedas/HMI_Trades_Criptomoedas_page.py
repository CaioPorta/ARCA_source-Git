# -*- coding: utf-8 -*-
"""
HMI_Trades_Criptomoedas helper. Behaviour is split across several baseless mixin modules
(one file per concern) that are re-composed here so the public surface stays
`from ui.trades.HMI_Trades_page import HMI_Trades` / ... .

    HMI_Events - events helpers (inherited automatically).
    HMI_PageBuilders - pagebuilders helpers (inherited automatically).
    HMI_Presentation - presentation helpers (inherited automatically).
"""

from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QToolTip)
from ui.trades.trades_criptomoedas.HMI_Events import HMI_Events
from ui.trades.trades_criptomoedas.HMI_PageBuilders import HMI_PageBuilders
from ui.trades.trades_criptomoedas.HMI_Presentation import HMI_Presentation


class HMI_Trades_Criptomoedas(HMI_Events, HMI_PageBuilders, HMI_Presentation):
    """Composition root; only lifecycle/state lives here (see module docstring)."""

    def __init__(self, HMI):
        self.HMI = HMI
        QToolTip.setFont(QFont('Arial', 12))
