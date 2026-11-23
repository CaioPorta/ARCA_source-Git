# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:54:52 2021

@author: Caio Moreira Porta
"""

"""Trades -> Bolsa helper (HMI_Trades_Bolsa).

Behaviour is split across several baseless mixin modules (one file per concern)
that are re-composed here so the public surface stays
 `from ui.trades.HMI_Trades_page import HMI_Trades` /
 `trades.trades_bolsa.HMI_Trades_Bolsa_page.HMI_Trades_Bolsa`:

    HMI_Presentation     - table rendering / presentation helpers (CreateTable*)
    HMI_PageBuilders     - per-page widget builders (CreatePage*)
    HMI_Events           - button/event handlers (OnButtonPressed)

Only the lifecycle/state method (__init__) lives in this file; everything else is
defined in the mixins and inherited automatically.
"""

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QToolTip

from ui.trades.trades_bolsa.HMI_Presentation import HMI_Presentation
from ui.trades.trades_bolsa.HMI_PageBuilders import HMI_PageBuilders
from ui.trades.trades_bolsa.HMI_Events import HMI_Events


class HMI_Trades_Bolsa(HMI_Presentation, HMI_PageBuilders, HMI_Events):
    """Trades -> Bolsa helper. Behaviour is composed from the mixins above; only
    lifecycle/state lives here on purpose (see module docstring)."""

    def __init__(self, HMI):
        self.HMI = HMI
        QToolTip.setFont(QFont('Arial', 12))
