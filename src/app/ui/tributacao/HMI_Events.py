# -*- coding: utf-8 -*-
"""
Tributacao behaviour split into a single concern.
HMI_Events - events helpers (inherited by the composition root).
"""
import traceback
import time
from datetime import (datetime)
import dateutil
from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QTableWidget, QInputDialog)
from PyQt5.QtCore import (Qt)
from ui.pages import (PAGE_BY_NAME)
import tkinter
from tkinter import (filedialog)
import xlsxwriter
import win32com.client as win32


class HMI_Events:
    def CalcularTributacao(self):
        self.HMI.DBManager.LW.Label_Titulo.setText("Calculando tributação.\nPor favor aguarde...\n")
        def GenerateListOfMonthsYears(DataInicial, DataFinal):
            Resposta = [DataInicial]
            UmMes = dateutil.relativedelta.relativedelta(months=1)
            while not max(Resposta) == DataFinal:
                Resposta.append(max(Resposta)+UmMes)
            return Resposta
        def GetFirstDate(TabelasTributacao):
            Datas = []
            for TabelaTibutacao_Nome, TabelasOPs_Nome in TabelasTributacao:
                for TabelaOPs_Nome in TabelasOPs_Nome:
                    # Ler tabela
                    TabelaOPs, cursor = self.HMI.DBManager.GetDataDB("SELECT * FROM "+TabelaOPs_Nome)
                    # Selecionar apenas as datas
                    TabelaOPs = [t[0] for t in TabelaOPs]
                    # Adicionar no vetor geral
                    for item in TabelaOPs:
                        Datas.append(item)
            if len(Datas) > 0:
                return datetime.strptime(min(Datas), '%Y-%m-%d %H:%M:%S').replace(day=1, hour=0, minute=0, second=0, microsecond=0) # Retorna a menor data em datetime
            return datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        self.HMI.DBManager.LW.Label_Titulo.setText("Calculando tributação.\nPor favor aguarde...")
        cursor = self.HMI.DBManager.conn.cursor()
        # Definir tabelas de tributação
        retorno, cursor = self.HMI.DBManager.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        retorno = list(map(lambda x: x[0],retorno))
        T1 = list(filter(lambda x: x.find('OPs¨')>-1 and x.find("Bolsa¨DT")>-1, retorno))
        T2 = list(filter(lambda x: x.find('OPs¨')>-1 and x.find("Bolsa¨ST")>-1, retorno))
        T3 = []#list(filter(lambda x: x.find('Operações¨')>-1 and x.find("Cripto¨DT")>-1, retorno))
        T4 = []#list(filter(lambda x: x.find('Operações¨')>-1 and x.find("Cripto¨ST")>-1, retorno))
        TabelasTributacao = [('TributaçãoDTBolsa',T1),('TributaçãoSTBolsa',T2),('TributaçãoDTCripto',T3),('TributaçãoSTCripto',T4)]
        # Definir data inicial da tabela
        DataInicial = GetFirstDate(TabelasTributacao)
        # Definir data final da tabela
        DataFinal = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        MesesAnos = GenerateListOfMonthsYears(DataInicial, DataFinal)
        loading = 1
        self.HMI.DBManager.LW.pbar.setValue(loading)
        # Para cada tabela de tributação, faça
        for TabelaTibutacao_Nome, TabelasOPs_Nome in TabelasTributacao:
            loading += 1
            self.HMI.DBManager.LW.pbar.setValue(loading)
            # Para cada mês/ano, faça
            content = []
            for i, MesAno in enumerate(MesesAnos):
                loading += 23/len(MesesAnos)
                self.HMI.DBManager.LW.pbar.setValue(int(loading))
                self.HMI.DBManager.LW.Label_Titulo.setText("Calculando tributação.\nPor favor aguarde...\n\n"+str(TabelaTibutacao_Nome)+": "+str(MesAno.strftime("%Y/%m")))
                # counter = 0
                # while counter < 1000000/len(MesesAnos): # Tempo pra ver a animação da barra de carregamento ;)
                #     counter+=1
                #### Perfumaria
                if len(MesesAnos) < 20: time.sleep(1/60) # Perfumaria. Comentar linha se preferir performance
                if i == 0: # Primeira linha
                    # Definir o resultado bruto de cada linha
                    ResultadoBruto = 0
                    # Para cada Tabela de Operações de ST ou DT, faça
                    for TabelaOPs_Nome in TabelasOPs_Nome:
                        # Ler tabela
                        TabelaOPs, cursor = self.HMI.DBManager.GetDataDB("SELECT * FROM "+TabelaOPs_Nome)
                        if len(TabelaOPs)>0:
                            # Filtrar linhas que estão dentro do intervalo de datas
                            TabelaOPs = list(filter(lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S').replace(day=1, hour=0, minute=0, second=0, microsecond=0) == MesAno, TabelaOPs))
                            # Filtrar linhas que têm resultado diferente de zero
                            TabelaOPs = list(filter(lambda x: isinstance(x[12], float), TabelaOPs))
                            # Somar todos os resultados
                            TabelaOPs = [t[12] for t in TabelaOPs]
                            ResultadoBruto += sum(TabelaOPs)
                    # Definir 'Prejuízo acumulado'
                    PrejuizoAcumulado = 0
                    # Definir 'Resultado final'
                    ResultadoFinal = 0
                    if not ResultadoBruto == 0:
                        ResultadoFinal = ResultadoBruto + PrejuizoAcumulado
                    # Definir 'Alíquota'
                    Aliquota = 20 if 'DT' in TabelaTibutacao_Nome else 15
                    # Definir 'Lucro mínimo taxável'
                    LucroMinimoTaxavel = 20000
                    # Definir 'Imposto devido'
                    if ResultadoFinal >= LucroMinimoTaxavel:
                        ImpostoDevido = Aliquota*ResultadoFinal/100
                    else:
                        ImpostoDevido = 0
                    # Definir 'Resultado líquido'
                    ResultadoLiquido = ResultadoFinal - ImpostoDevido
                    content.append([('MesAno', MesAno),
                                    ('Resultado', round(ResultadoBruto,2)),
                                    ('PrejuizoAcumulado', round(PrejuizoAcumulado,2)),
                                    ('ResultadoFinal', round(ResultadoFinal,2)),
                                    ('Alíquota', Aliquota),
                                    ('LucroMínimoTaxável', LucroMinimoTaxavel),
                                    ('ImpostoDevido', round(ImpostoDevido,2)),
                                    ('ResultadoLíquido', round(ResultadoLiquido,2))])
                else:
                    # Definir o resultado bruto de cada linha
                    ResultadoBruto = 0
                    # Para cada Tabela de Operações de ST ou DT, faça
                    for TabelaOPs_Nome in TabelasOPs_Nome:
                        # Ler tabela
                        TabelaOPs, cursor = self.HMI.DBManager.GetDataDB("SELECT * FROM "+TabelaOPs_Nome)
                        if len(TabelaOPs)>0:
                            # Filtrar linhas que estão dentro do intervalo de datas
                            TabelaOPs = list(filter(lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S').replace(day=1, hour=0, minute=0, second=0, microsecond=0) == MesAno, TabelaOPs))
                            # Filtrar linhas que têm resultado diferente de zero
                            TabelaOPs = list(filter(lambda x: isinstance(x[12], float), TabelaOPs))
                            # Somar todos os resultados
                            TabelaOPs = [t[12] for t in TabelaOPs]
                            ResultadoBruto += sum(TabelaOPs)
                    # Definir 'Prejuízo acumulado'
                    PrejuizoAcumulado = 0
                    if content[-1][1][1] == 0: # Se não houve resultado no mês anterior, carrega o prejuízo
                        PrejuizoAcumulado = content[-1][2][1]
                    elif content[-1][3][1] < 0:
                        PrejuizoAcumulado = content[-1][3][1]
                    # Definir 'Resultado final'
                    ResultadoFinal = 0
                    if not ResultadoBruto == 0:
                        ResultadoFinal = ResultadoBruto + PrejuizoAcumulado
                    # Definir 'Alíquota'
                    Aliquota = content[-1][4][1]
                    # Definir 'Lucro mínimo taxável'
                    LucroMinimoTaxavel = content[-1][5][1]
                    # Definir 'Imposto devido'
                    if ResultadoFinal >= LucroMinimoTaxavel:
                        ImpostoDevido = Aliquota*ResultadoFinal/100
                    else:
                        ImpostoDevido = 0
                    # Definir 'Resultado líquido'
                    ResultadoLiquido = ResultadoFinal - ImpostoDevido
                    content.append([('MesAno', MesAno),
                                ('Resultado', round(ResultadoBruto,2)),
                                ('PrejuizoAcumulado', round(PrejuizoAcumulado,2)),
                                ('ResultadoFinal', round(ResultadoFinal,2)),
                                ('Alíquota', Aliquota),
                                ('LucroMínimoTaxável', LucroMinimoTaxavel),
                                ('ImpostoDevido', round(ImpostoDevido,2)),
                                ('ResultadoLíquido', round(ResultadoLiquido,2))])
            # print(TabelaTibutacao_Nome, ":\n", content) # Debug
            self.HMI.DBManager.ModifyDB("DELETE FROM "+TabelaTibutacao_Nome)
            for row in content: # Overwrite Tables
                self.HMI.DBManager.AddRowInCurrentDB(TabelaTibutacao_Nome, row)
            self.HMI.DBManager.LW.pbar.setValue(100)
        self.HMI.CalcularTributacao_is_running = False


    def CalcularTributacao_SemThread(self):
        def GenerateListOfMonthsYears(DataInicial, DataFinal):
            Resposta = [DataInicial]
            UmMes = dateutil.relativedelta.relativedelta(months=1)
            while not max(Resposta) == DataFinal:
                Resposta.append(max(Resposta)+UmMes)
            return Resposta
        def GetFirstDate(TabelasTributacao):
            Datas = []
            for TabelaTibutacao_Nome, TabelasOPs_Nome in TabelasTributacao:
                for TabelaOPs_Nome in TabelasOPs_Nome:
                    # Ler tabela
                    TabelaOPs, cursor = self.HMI.DBManager.GetDataDB("SELECT * FROM "+TabelaOPs_Nome)
                    # Selecionar apenas as datas
                    TabelaOPs = [t[0] for t in TabelaOPs]
                    # Adicionar no vetor geral
                    for item in TabelaOPs:
                        Datas.append(item)
            if len(Datas) > 0:
                return datetime.strptime(min(Datas), '%Y-%m-%d %H:%M:%S').replace(day=1, hour=0, minute=0, second=0, microsecond=0) # Retorna a menor data em datetime
            return datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        cursor = self.HMI.DBManager.conn.cursor()
        # Definir tabelas de tributação
        retorno, cursor = self.HMI.DBManager.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
        retorno = list(map(lambda x: x[0],retorno))
        T1 = list(filter(lambda x: x.find('OPs¨')>-1 and x.find("Bolsa¨DT")>-1, retorno))
        T2 = list(filter(lambda x: x.find('OPs¨')>-1 and x.find("Bolsa¨ST")>-1, retorno))
        T3 = []#list(filter(lambda x: x.find('Operações¨')>-1 and x.find("Cripto¨DT")>-1, retorno))
        T4 = []#list(filter(lambda x: x.find('Operações¨')>-1 and x.find("Cripto¨ST")>-1, retorno))
        TabelasTributacao = [('TributaçãoDTBolsa',T1),('TributaçãoSTBolsa',T2),('TributaçãoDTCripto',T3),('TributaçãoSTCripto',T4)]
        # Definir data inicial da tabela
        DataInicial = GetFirstDate(TabelasTributacao)
        # Definir data final da tabela
        DataFinal = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        MesesAnos = GenerateListOfMonthsYears(DataInicial, DataFinal)
        # Para cada tabela de tributação, faça
        for TabelaTibutacao_Nome, TabelasOPs_Nome in TabelasTributacao:
            # Para cada mês/ano, faça
            content = []
            for i, MesAno in enumerate(MesesAnos):
                if i == 0: # Primeira linha
                    # Definir o resultado bruto de cada linha
                    ResultadoBruto = 0
                    # Para cada Tabela de Operações de ST ou DT, faça
                    for TabelaOPs_Nome in TabelasOPs_Nome:
                        # Ler tabela
                        TabelaOPs, cursor = self.HMI.DBManager.GetDataDB("SELECT * FROM "+TabelaOPs_Nome)
                        if len(TabelaOPs)>0:
                            # Filtrar linhas que estão dentro do intervalo de datas
                            TabelaOPs = list(filter(lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S').replace(day=1, hour=0, minute=0, second=0, microsecond=0) == MesAno, TabelaOPs))
                            # Filtrar linhas que têm resultado diferente de zero
                            TabelaOPs = list(filter(lambda x: isinstance(x[12], float), TabelaOPs))
                            # Somar todos os resultados
                            TabelaOPs = [t[12] for t in TabelaOPs]
                            ResultadoBruto += sum(TabelaOPs)
                    # Definir 'Prejuízo acumulado'
                    PrejuizoAcumulado = 0
                    # Definir 'Resultado final'
                    ResultadoFinal = 0
                    if not ResultadoBruto == 0:
                        ResultadoFinal = ResultadoBruto + PrejuizoAcumulado
                    # Definir 'Alíquota'
                    Aliquota = 20 if 'DT' in TabelaTibutacao_Nome else 15
                    # Definir 'Lucro mínimo taxável'
                    LucroMinimoTaxavel = 20000
                    # Definir 'Imposto devido'
                    if ResultadoFinal >= LucroMinimoTaxavel:
                        ImpostoDevido = Aliquota*ResultadoFinal/100
                    else:
                        ImpostoDevido = 0
                    # Definir 'Resultado líquido'
                    ResultadoLiquido = ResultadoFinal - ImpostoDevido
                    content.append([('MesAno', MesAno),
                                    ('Resultado', round(ResultadoBruto,2)),
                                    ('PrejuizoAcumulado', round(PrejuizoAcumulado,2)),
                                    ('ResultadoFinal', round(ResultadoFinal,2)),
                                    ('Alíquota', Aliquota),
                                    ('LucroMínimoTaxável', LucroMinimoTaxavel),
                                    ('ImpostoDevido', round(ImpostoDevido,2)),
                                    ('ResultadoLíquido', round(ResultadoLiquido,2))])
                else:
                    # Definir o resultado bruto de cada linha
                    ResultadoBruto = 0
                    # Para cada Tabela de Operações de ST ou DT, faça
                    for TabelaOPs_Nome in TabelasOPs_Nome:
                        # Ler tabela
                        TabelaOPs, cursor = self.HMI.DBManager.GetDataDB("SELECT * FROM "+TabelaOPs_Nome)
                        if len(TabelaOPs)>0:
                            # Filtrar linhas que estão dentro do intervalo de datas
                            TabelaOPs = list(filter(lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S').replace(day=1, hour=0, minute=0, second=0, microsecond=0) == MesAno, TabelaOPs))
                            # Filtrar linhas que têm resultado diferente de zero
                            TabelaOPs = list(filter(lambda x: isinstance(x[12], float), TabelaOPs))
                            # Somar todos os resultados
                            TabelaOPs = [t[12] for t in TabelaOPs]
                            ResultadoBruto += sum(TabelaOPs)
                    # Definir 'Prejuízo acumulado'
                    PrejuizoAcumulado = 0
                    if content[-1][1][1] == 0: # Se não houve resultado no mês anterior, carrega o prejuízo
                        PrejuizoAcumulado = content[-1][2][1]
                    elif content[-1][3][1] < 0:
                        PrejuizoAcumulado = content[-1][3][1]
                    # Definir 'Resultado final'
                    ResultadoFinal = 0
                    if not ResultadoBruto == 0:
                        ResultadoFinal = ResultadoBruto + PrejuizoAcumulado
                    # Definir 'Alíquota'
                    Aliquota = content[-1][4][1]
                    # Definir 'Lucro mínimo taxável'
                    LucroMinimoTaxavel = content[-1][5][1]
                    # Definir 'Imposto devido'
                    if ResultadoFinal >= LucroMinimoTaxavel:
                        ImpostoDevido = Aliquota*ResultadoFinal/100
                    else:
                        ImpostoDevido = 0
                    # Definir 'Resultado líquido'
                    ResultadoLiquido = ResultadoFinal - ImpostoDevido
                    content.append([('MesAno', MesAno),
                                ('Resultado', round(ResultadoBruto,2)),
                                ('PrejuizoAcumulado', round(PrejuizoAcumulado,2)),
                                ('ResultadoFinal', round(ResultadoFinal,2)),
                                ('Alíquota', Aliquota),
                                ('LucroMínimoTaxável', LucroMinimoTaxavel),
                                ('ImpostoDevido', round(ImpostoDevido,2)),
                                ('ResultadoLíquido', round(ResultadoLiquido,2))])
            # print(TabelaTibutacao_Nome, ":\n", content) # Debug
            self.HMI.DBManager.ModifyDB("DELETE FROM "+TabelaTibutacao_Nome)
            for row in content: # Overwrite Tables
                self.HMI.DBManager.AddRowInCurrentDB(TabelaTibutacao_Nome, row)
        self.HMI.CalcularTributacao_is_running = False


    def OnButtonPressed(self, ButtonPressed):
        if ButtonPressed == 'ChangeDTeST':
            if self.HMI.DTeST == "": self.HMI.DTeST = "DTeST"
            elif self.HMI.DTeST == "DTeST": self.HMI.DTeST = "ST"
            elif self.HMI.DTeST == "ST": self.HMI.DTeST = "DT"
            elif self.HMI.DTeST == "DT": self.HMI.DTeST = ""

            if self.HMI.DTeST == "":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Trades Brutos.png"))
                # Habilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(True)
                self.HMI.Button_DeletarOperacao.setEnabled(True)
            elif self.HMI.DTeST == "DTeST":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Day Trades e Swing Trades.png"))
                # Desabilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(False)
                self.HMI.Button_DeletarOperacao.setEnabled(False)
            elif self.HMI.DTeST == "ST":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas ST.png"))
                # Desabilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(False)
                self.HMI.Button_DeletarOperacao.setEnabled(False)
            elif self.HMI.DTeST == "DT":
                self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas DT.png"))
                # Desabilitar Botões de edição
                self.HMI.Button_AlterarOperacao.setEnabled(False)
                self.HMI.Button_DeletarOperacao.setEnabled(False)

            if self.HMI.PageID == PAGE_BY_NAME['RegistrosBolsa'].page_id:
                self.HMI.Table_Operacoes_Realizadas_com_Ativo.deleteLater()
                self.HMI.Table_Operacoes_Realizadas_com_Ativo = QTableWidget()
                self.HMI.HMI_Trades.HMI_Trades_Bolsa.CreateTable_23_2()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas_com_Ativo, 6, 0, 6, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

            if self.HMI.PageID == PAGE_BY_NAME['RegistrosCripto'].page_id:
                self.HMI.Table_Operacoes_Realizadas.deleteLater()
                self.HMI.Table_Operacoes_Realizadas = QTableWidget()
                self.HMI.HMI_Trades.HMI_Trades_Criptomoedas.CreateTable_40_2()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Operacoes_Realizadas, 6, 0, 6, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

            elif self.HMI.PageID == PAGE_BY_NAME['Tributacao'].page_id:
                if self.HMI.DTeST_51 == "DTeST": self.HMI.DTeST_51 = "ST"
                elif self.HMI.DTeST_51 == "ST": self.HMI.DTeST_51 = "DT"
                elif self.HMI.DTeST_51 == "DT": self.HMI.DTeST_51 = "DTeST"

                if self.HMI.DTeST_51 == "DTeST":
                    self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Day Trades e Swing Trades.png"))
                elif self.HMI.DTeST_51 == "ST":
                    self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas ST.png"))
                elif self.HMI.DTeST_51 == "DT":
                    self.HMI.Button_DTeST.setIcon(QIcon("./images/Visualizar Apenas DT.png"))
                self.HMI.Table_Tributacao_Header.deleteLater()
                self.HMI.Table_Tributacao_Header = QTableWidget()
                self.HMI.HMI_Tributacao.CreateTable_51_1()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Tributacao_Header, 5, 0, 1, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
                self.HMI.Table_Tributacao.deleteLater()
                self.HMI.Table_Tributacao = QTableWidget()
                self.HMI.HMI_Tributacao.CreateTable_51_2()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Tributacao, 6, 0, 6, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        elif ButtonPressed == 'ExportIR':
            def WriteHeader(worksheet, header):
                for column_idx, item in enumerate(header):
                    try:
                        worksheet.write(0, column_idx, item)
                    except Exception as e:
                        print('header: ',e)

            # 1. Ask IR year
            # 2. Ask filepath to be saved
            # 3. Get from DB last estoque of defined year for all shares, for all corretoras
            # 4. Save

            # 1. Ask IR year
            years = []
            for i, item in enumerate(self.data_51_1):
                for j in range(len(item)):
                    if j == 0:
                        years.append(datetime.strptime(item[j], '%Y-%m-%d %H:%M:%S').strftime('%Y'))
            years = sorted(set(years), reverse=True)
            year, answered = QInputDialog.getItem(self.HMI, 'Exportar IR', 'Ano de IR que deseja exportar:', years)

            if answered:
                # 2. Ask filepath to be saved
                if not self.HMI.filedialogIsOpen:
                    root = tkinter.Tk()
                    root.withdraw()  # Used to hide tkinter window
                    self.HMI.filedialogIsOpen = True
                    DB_Path = filedialog.askdirectory()  # Select folder path
                    self.HMI.setCursor(Qt.CursorShape.WaitCursor)
                    self.HMI.filedialogIsOpen = False
                    try:
                        if len(DB_Path) > 0:
                            # 3. Get from DB last estoque of defined year for all shares, for all corretoras
                            sheets, cursor = self.HMI.DBManager.GetDataDB("SELECT name FROM sqlite_master WHERE type='table';")
                            sheets = list(map(lambda x: x[0], sheets))
                            agora = datetime.now().strftime("%Y %m %d")
                            FileName = self.HMI.User + "_ImpostoDeRenda " + year + "_Gerado em " + agora + '.xlsx'
                            workbook = xlsxwriter.Workbook(DB_Path + "/" + FileName)
                            corretoras, corretorasCripto = self.HMI.DBManager.GetAllCorretoras_ComBolsaOuCripto()
                            corretoras.extend(corretorasCripto)
                            for corretora in corretoras:
                                row1=[]; Ativo = '...'; QuantidadeEmYear = 'NAN'; PreçoMedioEmYear = 'NAN'; CustoEmYear = 'NAN'; rows = []; pre_rows = [];

                                try: worksheet = workbook.add_worksheet(name=corretora.replace("¨Bolsa","").replace("¨Cripto","")[0:31]) # Create sheets
                                except Exception as e: print('creating worksheet ',worksheet,': ',e)

                                if "¨Bolsa" in corretora:
                                    SheetsToBeConsidered = list(filter(lambda x: corretora+"¨Bruto" in x, sheets))
                                    corretora = corretora.replace("¨Bolsa", "")
                                    CorretoraCoinCurrency = self.HMI.DBManager.GetCorretoraCoinCurrency(corretora, "Bolsa")
                                    header = ['Ativo', 'Quantidade em ' + year, 'Preço Médio (' + CorretoraCoinCurrency + ')']
                                    WriteHeader(worksheet, header)

                                    for Sheet in SheetsToBeConsidered:
                                        try:
                                            CONTENT, cursor = self.HMI.DBManager.GetDataDB('SELECT * FROM ' + Sheet + ' WHERE Data BETWEEN (?) AND (?);', [min(years) + '-01-01 00:00:00', year + '-12-31 23:59:59'])
                                            if len(CONTENT) == 0: break
                                            Ativo = Sheet.replace(corretora+"¨Bolsa¨Bruto","").replace("OPs¨","").replace("¨","")
                                            QuantidadeEmYear = CONTENT[-1][8]
                                            PreçoMedioEmYear = CONTENT[-1][11]
                                            rows.append([Ativo, QuantidadeEmYear, PreçoMedioEmYear])
                                        except Exception as e: print('writing rows in Bolsa ',[Ativo, QuantidadeEmYear, PreçoMedioEmYear],': ',e)

                                elif "¨Cripto" in corretora:
                                    corretora = corretora.replace("¨Cripto", "")
                                    sheet = "OPs¨" + corretora + "¨Cripto¨Refinado"
                                    CorretoraCoinCurrency = self.HMI.DBManager.GetCorretoraCoinCurrency(corretora, "Cripto")
                                    header = ['Ativo', 'Quantidade em ' + year, 'Preço Médio (' + CorretoraCoinCurrency + ')', 'Custo (' + CorretoraCoinCurrency + ')']
                                    WriteHeader(worksheet, header)

                                    CONTENT, cursor = self.HMI.DBManager.GetDataDB('SELECT * FROM ' + sheet + ' WHERE Data BETWEEN (?) AND (?);', [min(years) + '-01-01 00:00:00', year + '-12-31 23:59:59'])
                                    if len(CONTENT) == 0: break
                                    Headers = list(map(lambda x: x[0], cursor.description))[13:]
                                    for idx, Header in enumerate(Headers):
                                        if "EstoqueDe¨" in Header and CorretoraCoinCurrency in Header:
                                            try:
                                                Ativo = CorretoraCoinCurrency
                                                QuantidadeEmYear = CONTENT[-1][idx + 13] + CONTENT[-1][idx + 14] + CONTENT[-1][idx + 15]
                                                PreçoMedioEmYear = CONTENT[-1][idx + 17]
                                                CustoEmYear = CONTENT[-1][idx + 16]
                                                row1.append([Ativo, QuantidadeEmYear, PreçoMedioEmYear, CustoEmYear])
                                            except Exception as e: print('writing row1 in Cripto ',[Ativo, QuantidadeEmYear, PreçoMedioEmYear, CustoEmYear],': ',e)
                                        elif "EstoqueDe¨" in Header:
                                            try:
                                                Ativo = Header.replace("EstoqueDe¨","")
                                                QuantidadeEmYear = CONTENT[-1][idx + 13] + CONTENT[-1][idx + 14] + CONTENT[-1][idx + 15]
                                                PreçoMedioEmYear = CONTENT[-1][idx + 17]
                                                CustoEmYear = CONTENT[-1][idx + 16]
                                                pre_rows.append([Ativo, QuantidadeEmYear, PreçoMedioEmYear, CustoEmYear])
                                            except Exception as e: print('writing pre_rows in Cripto ',[Ativo, QuantidadeEmYear, PreçoMedioEmYear, CustoEmYear],': ',e)

                                    pre_rows = sorted(pre_rows, key=lambda x: x[3])
                                    if len(row1)>0: pre_rows.extend(row1)
                                    pre_rows = pre_rows[::-1]
                                    for idx in list(range(min(len(pre_rows),6))):
                                        try: rows.append(pre_rows[idx])
                                        except Exception as e: print('writing rows in Cripto ',[Ativo, QuantidadeEmYear, PreçoMedioEmYear, CustoEmYear],': ',e)
                                    if len(pre_rows) > 6:
                                        custos = sum(list(map(lambda x: x[3], pre_rows[6:])))
                                        rows.append(['Outros', "", "", custos])

                                for row_idx, row in enumerate(rows):
                                    for column_idx, item in enumerate(row):
                                        try:
                                            worksheet.write(row_idx+1, column_idx, item)
                                        except Exception as e:
                                            print(e)

                            workbook.close()

                            excel = win32.gencache.EnsureDispatch('Excel.Application')
                            wb = excel.Workbooks.Open(DB_Path + "/" + FileName)
                            for corretora in corretoras:
                                ws = wb.Worksheets(corretora.replace("¨Bolsa","").replace("¨Cripto","")[0:31])
                                ws.Columns.AutoFit()
                            wb.Save()
                            wb.Close(True)
                            # excel.Application.Quit() # Bugado
                    except Exception as e:
                        print(e)
                        try: workbook.close()
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                        try: wb.Close(True)
                        except Exception as e:
                            print(e, traceback.format_exception(None, e, e.__traceback__))
                    finally:
                        self.HMI.unsetCursor()

        elif ButtonPressed == 'ChangeCriptoeB3':
            if self.HMI.PageID == PAGE_BY_NAME['Tributacao'].page_id:
                if self.HMI.CriptoeB3_51 == "CriptoeB3": self.HMI.CriptoeB3_51 = "B3"
                elif self.HMI.CriptoeB3_51 == "B3": self.HMI.CriptoeB3_51 = "Cripto"
                elif self.HMI.CriptoeB3_51 == "Cripto": self.HMI.CriptoeB3_51 = "CriptoeB3"

                if self.HMI.CriptoeB3_51 == "CriptoeB3":
                    self.HMI.Button_CriptoeB3.setIcon(QIcon("./images/Visualizar cripto e B3.png"))
                elif self.HMI.CriptoeB3_51 == "Cripto":
                    self.HMI.Button_CriptoeB3.setIcon(QIcon("./images/Visualizar Apenas cripto.png"))
                elif self.HMI.CriptoeB3_51 == "B3":
                    self.HMI.Button_CriptoeB3.setIcon(QIcon("./images/Visualizar Apenas B3.png"))
                self.HMI.Table_Tributacao_Header.deleteLater()
                self.HMI.Table_Tributacao_Header = QTableWidget()
                self.HMI.HMI_Tributacao.CreateTable_51_1()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Tributacao_Header, 5, 0, 1, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
                self.HMI.Table_Tributacao.deleteLater()
                self.HMI.Table_Tributacao = QTableWidget()
                self.HMI.HMI_Tributacao.CreateTable_51_2()
                self.HMI.F_GLayout[self.HMI.GCount-1].addWidget(self.HMI.Table_Tributacao, 6, 0, 6, 10, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
