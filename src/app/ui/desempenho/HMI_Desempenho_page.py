# -*- coding: utf-8 -*-
"""
HMI_Desempenho helper. Behaviour is split across several baseless mixin modules
(one file per concern) that are re-composed here so the public surface stays
`from ui.trades.HMI_Trades_page import HMI_Trades` / ... .

    HMI_PageBuilders - pagebuilders helpers (inherited automatically).
"""

from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QToolTip)
from ui.desempenho.HMI_PageBuilders import HMI_PageBuilders


class HMI_Desempenho(HMI_PageBuilders):
    """Composition root; only lifecycle/state lives here (see module docstring)."""

    def __init__(self, HMI):
        self.HMI = HMI
        QToolTip.setFont(QFont('Arial', 12))
