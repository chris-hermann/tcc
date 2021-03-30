import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, re, parameters, math, operacao
import tkinter.font as tkFont
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import Color, gray, green, blue, red, yellow
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib.formatters import DecimalFormatter
import os



class OutputsPage():
	def __init__(self, master):
		self.master = master
		self.master.title('Resultado da simulação')
		self.master.iconbitmap('icon.ico')
		self.master.resizable(False, False)
		self.FonteTitulo = tkFont.Font(family='Helvetica', size=10, weight='bold')
		self.frame_inputs = tk.LabelFrame(self.master, text='Dados de Entrada', font=self.FonteTitulo)
		self.frame_inputsTrator = tk.LabelFrame(self.frame_inputs, text='Trator')
		self.frame_inputsTalhao = tk.LabelFrame(self.frame_inputs, text='Talhão')
		self.frame_inputsImplemento = tk.LabelFrame(self.frame_inputs, text='Implemento')
		self.frame_inputsOperacao = tk.LabelFrame(self.frame_inputs, text='Operação')
		self.frame_infosoperacionais = tk.LabelFrame(self.master, text='Informações operacionais', font=self.FonteTitulo)
		self.frame_custosfixos = tk.LabelFrame(self.master, text='Custos fixos', font=self.FonteTitulo)
		self.frame_custofixotrator = tk.LabelFrame(self.frame_custosfixos, text='Trator')
		self.frame_custofixoImplemento = tk.LabelFrame(self.frame_custosfixos, text='Implemento')
		self.frame_custosop = tk.LabelFrame(self.master, text='Custos operacionais', font=self.FonteTitulo)
		self.frame_custostotais = tk.LabelFrame(self.master, text='Custos totais', font=self.FonteTitulo)
		self.frame_buttons = tk.Frame(self.master)
		self.frame_inputs.grid(row=0, rowspan=4, column=0, padx=5, pady=5)
		self.frame_inputsTrator.grid()
		self.frame_inputsTalhao.grid()
		self.frame_inputsImplemento.grid()
		self.frame_inputsOperacao.grid()
		self.frame_infosoperacionais.grid(row=0, column=1, pady=5, padx=5)
		self.frame_custosfixos.grid(row=1, column=1)
		self.frame_custofixotrator.grid(row=0, column=0, padx=2)
		self.frame_custofixoImplemento.grid(row=0 ,column=1)
		self.frame_custosop.grid(row=2, column=1, padx=5)
		self.frame_custostotais.grid(row=3, column=1, padx=5, pady=2)
		self.frame_buttons.grid()
		self.NomeTalhao = ''
		self.IDTalhao = 0
		self.TexturaTalhao = ''
		self.AreaTalhao = 0.0
		self.NomeTrator = ''
		self.IDTrator = 0
		self.TransmissaoTrator = ''
		self.PotenciaTrator = 0.0
		self.NomeImplemento = ''
		self.IDImplemento = 0
		self.TipoImplemento = ''
		self.LarguraImplemento = 0.0
		self.OrgaoImplemento = 0.0
		self.LinhaImplemento = 0.0
		self.VelocidadeOperacao = 0.0
		self.ProfundidadeOperacao = 0.0
		self.PassadaOperacao = 0
		self.CondicaoSolo = ''
		self.PrecoCombustivel = 0.0
		self.PrecoOleo = 0.0
		self.PrecoTratorista = 0.0
		self.CoeficienteTransmissao = 0.0
		self.ParametroA = 0.0
		self.ParametroB = 0.0
		self.ParametroC = 0.0
		self.ParametroF = 0.0
		self.ForcaReqImplemento = 0.0
		self.PotenciaReqImplementoBT = 0.0
		self.PotenciaReqImplementoTDP = 0.0
		self.PotenciaDispTratorTDP = 0.0
		self.FatorX = 0.0
		self.ConsumoCombEspec = 0.0
		self.ConsumoCombHora = 0.0
		self.EficienciaCampo = 0.0
		self.CapacidadeCampoTeorica = 0.0
		self.CapacidadeCampoEfetiva = 0.0
		self.TempoGasto = 0.0
		self.DepreciacaoTrator = 0.0
		self.JuroTrator = 0.0
		self.GaragemTrator = 0.0
		self.SeguroTrator = 0.0
		self.CustoFixoTrator = 0.0
		self.DepreciacaoImplemento = 0.0
		self.JuroImplemento = 0.0
		self.GaragemImplemento = 0.0
		self.SeguroImplemento = 0.0
		self.CustoFixoImplemento = 0.0
		self.CustoCombHora = 0.0
		self.CustoOleoHora = 0.0
		self.CustoManutencaoHoraTrator = 0.0
		self.CustoOperacional = 0.0
		self.CustoTotalHorario = 0.0
		self.CustoTotalHectare = 0.0
		self.CustoTotal = 0.0
		self.ValorCompraTrator = 0.0
		self.TaxaJurosTrator = 0.0
		self.TaxaGaragemTrator = 0.0
		self.TaxaSeguroTrator = 0.0
		self.VidaUtilHoraTrator = 0.0
		self.ValorCompraImplemento = 0.0
		self.TaxaJurosImplemento = 0.0
		self.TaxaGaragemImplemento = 0.0
		self.TaxaSeguroImplemento = 0.0
		self.VidaUtilHoraImplemento = 0.0
		self.EficienciaCampoMinima = 0.0
		self.EficienciaCampoMaxima = 0.0

		
		#Exibição dos Dados de Entrada na tela
		self.NomeTalhaoLabel = tk.Label(self.frame_inputsTalhao, text='Nome do talhão: ', justify=tk.RIGHT).grid(row=1, column=0)
		self.NomeTalhaoVar = tk.StringVar()
		self.NomeTalhaoVarLabel = tk.Label(self.frame_inputsTalhao, textvariable=self.NomeTalhaoVar, justify=tk.LEFT)
		self.NomeTalhaoVarLabel.grid(row=1, column=1)
		self.areaLabel = tk.Label(self.frame_inputsTalhao, text='Área do talhão (ha): ').grid(row=2, column=0)
		self.AreaTalhaoVar = tk.StringVar()
		self.AreaTalhaoVarLabel = tk.Label(self.frame_inputsTalhao, textvariable=self.AreaTalhaoVar)
		self.AreaTalhaoVarLabel.grid(row=2, column=1)
		self.texturaLabel = tk.Label(self.frame_inputsTalhao, text='Textura do solo: ').grid(row=3, column=0)
		self.TexturaTalhaoVar = tk.StringVar()
		self.TexturaTalhaoVarLabel = tk.Label(self.frame_inputsTalhao, textvariable=self.TexturaTalhaoVar)
		self.TexturaTalhaoVarLabel.grid(row=3, column=1)
		self.NomeTratorLabel = tk.Label(self.frame_inputsTrator, text='Nome do trator: ').grid(row=4, column=0)
		self.NomeTratorVar = tk.StringVar()
		self.NomeTratorVarLabel = tk.Label(self.frame_inputsTrator, textvariable=self.NomeTratorVar)
		self.NomeTratorVarLabel.grid(row=4, column=1)
		self.transmissaoLabel = tk.Label(self.frame_inputsTrator, text='Tipo de transmissão: ').grid(row=5, column=0)
		self.TransmissaoTratorVar = tk.StringVar()
		self.TransmissaoVarLabel = tk.Label(self.frame_inputsTrator, textvariable=self.TransmissaoTratorVar)
		self.TransmissaoVarLabel.grid(row=5, column=1)
		self.potenciaLabel = tk.Label(self.frame_inputsTrator, text='Potência nominal (cv): ').grid(row=6, column=0)
		self.PotenciaTratorVar = tk.DoubleVar()
		self.PotenciaTratorVarLabel = tk.Label(self.frame_inputsTrator, textvariable=self.PotenciaTratorVar)
		self.PotenciaTratorVarLabel.grid(row=6, column=1)
		self.NomeImplementoLabel = tk.Label(self.frame_inputsImplemento, text='Nome do implemento: ').grid(row=7, column=0)
		self.NomeImplementoVar = tk.StringVar()
		self.NomeImplementoVarLabel = tk.Label(self.frame_inputsImplemento, textvariable=self.NomeImplementoVar)
		self.NomeImplementoVarLabel.grid(row=7, column=1)
		self.implementoLabel = tk.Label(self.frame_inputsImplemento, text='Tipo de implemento: ').grid(row=8, column=0)
		self.TipoImplementoVar = tk.StringVar()
		self.tipoImplementoVarLabel = tk.Label(self.frame_inputsImplemento, textvariable=self.TipoImplementoVar)
		self.tipoImplementoVarLabel.grid(row=8, column=1)
		self.larguraLabel = tk.Label(self.frame_inputsImplemento, text='Largura do implemento (m): ').grid(row=9, column=0)
		self.LarguraImplementoVar = tk.DoubleVar()
		self.LarguraImplementoVarLabel = tk.Label(self.frame_inputsImplemento, textvariable=self.LarguraImplementoVar)
		self.LarguraImplementoVarLabel.grid(row=9, column=1)
		self.orgaoLabel = tk.Label(self.frame_inputsImplemento, text='Número de órgãos: ').grid(row=10, column=0)
		self.OrgaoImplementoVar = tk.IntVar()
		self.OrgaoImplementoVarLabel = tk.Label(self.frame_inputsImplemento, textvariable=self.OrgaoImplementoVar)
		self.OrgaoImplementoVarLabel.grid(row=10, column=1)
		self.linhasLabel = tk.Label(self.frame_inputsImplemento, text='Número de linhas: ').grid(row=11, column=0)
		self.LinhaImplementoVar = tk.IntVar()
		self.LinhaImplementoVarLabel = tk.Label(self.frame_inputsImplemento, textvariable=self.LinhaImplementoVar)
		self.LinhaImplementoVarLabel.grid(row=11, column=1)
		self.velLabel = tk.Label(self.frame_inputsOperacao, text='Velocidade de operação (km/h): ').grid(row=12, column=0)
		self.VelocidadeOperacaoVar = tk.DoubleVar()
		self.VelocidadeOperacaoVarLabel = tk.Label(self.frame_inputsOperacao, textvariable=self.VelocidadeOperacaoVar)
		self.VelocidadeOperacaoVarLabel.grid(row=12, column=1)
		self.profLabel = tk.Label(self.frame_inputsOperacao, text='Profundidade de operação (cm): ').grid(row=13, column=0)
		self.ProfundidadeOperacaoVar = tk.DoubleVar()
		self.ProfundidadeOperacaoVarLabel = tk.Label(self.frame_inputsOperacao, textvariable=self.ProfundidadeOperacaoVar)
		self.ProfundidadeOperacaoVarLabel.grid(row=13, column=1)
		self.passadaLabel = tk.Label(self.frame_inputsOperacao, text='Passada da operação: ').grid(row=14, column=0)
		self.PassadaOperacaoVar = tk.IntVar()
		self.PassadaOperacaoVarLabel = tk.Label(self.frame_inputsOperacao, textvariable=self.PassadaOperacaoVar)
		self.PassadaOperacaoVarLabel.grid(row=14, column=1)
		self.condSoloLabel = tk.Label(self.frame_inputsOperacao, text='Condição da superfície do solo: ').grid(row=15, column=0)
		self.CondicaoSoloVar = tk.StringVar()
		self.CondicaoSoloVarLabel = tk.Label(self.frame_inputsOperacao, textvariable=self.CondicaoSoloVar)
		self.CondicaoSoloVarLabel.grid(row=15, column=1)
		self.PrecoCombustivelLabel = tk.Label(self.frame_inputsOperacao, text='Preço do diesel (R$/L): ').grid(row=16, column=0)
		self.PrecoCombustivelVar = tk.DoubleVar()
		self.PrecoCombustivelVarLabel = tk.Label(self.frame_inputsOperacao, textvariable=self.PrecoCombustivelVar)
		self.PrecoCombustivelVarLabel.grid(row=16, column=1)
		self.PrecoOleoLabel = tk.Label(self.frame_inputsOperacao, text='Preço do Lubrificante (R$/L): ').grid(row=17, column=0)
		self.PrecoOleoVar = tk.DoubleVar()
		self.PrecoOleoVarLabel = tk.Label(self.frame_inputsOperacao, textvariable=self.PrecoOleoVar)
		self.PrecoOleoVarLabel.grid(row=17, column=1)
		self.PrecoTratoristaLabel = tk.Label(self.frame_inputsOperacao, text='Preço do tratorista (R$/h): ').grid(row=18, column=0)
		self.PrecoTratoristaVar = tk.DoubleVar()
		self.PrecoTratoristaVarLabel = tk.Label(self.frame_inputsOperacao, textvariable=self.PrecoTratoristaVar)
		self.PrecoTratoristaVarLabel.grid(row=18, column=1)

		#Exibição das Informações operacionais na tela
		self.EficienciaCampoVar = tk.DoubleVar()
		self.EficienciaCampoLabel = tk.Label(self.frame_infosoperacionais, text='Eficiência de campo: ').grid(row=0, column=0)
		self.EficienciaCampoVarLabel = tk.Label(self.frame_infosoperacionais, textvariable=self.EficienciaCampoVar)
		self.EficienciaCampoVarLabel.grid(row=0, column=1)
		self.CapacidadeCampoTeoricaVar = tk.DoubleVar()
		self.CapacidadeCampoTeoricaLabel = tk.Label(self.frame_infosoperacionais, text='Capacidade de campo teórica (ha/h): ').grid(row=1, column=0)
		self.CapacidadeCampoTeoricaVarLabel = tk.Label(self.frame_infosoperacionais, textvariable=self.CapacidadeCampoTeoricaVar)
		self.CapacidadeCampoTeoricaVarLabel.grid(row=1, column=1)
		self.CapacidadeCampoEfetivaVar = tk.DoubleVar()
		self.CapacidadeCampoEfetivaLabel = tk.Label(self.frame_infosoperacionais, text='Capacidade de campo efetiva (ha/h): ').grid(row=2, column=0)
		self.CapacidadeCampoEfetivaVarLabel = tk.Label(self.frame_infosoperacionais, textvariable=self.CapacidadeCampoEfetivaVar)
		self.CapacidadeCampoEfetivaVarLabel.grid(row=2, column=1)
		self.TempoGastoVar = tk.DoubleVar()
		self.TempoGastoLabel = tk.Label(self.frame_infosoperacionais, text='Tempo total gasto (h): ').grid(row=3, column=0)
		self.TempoGastoVarLabel = tk.Label(self.frame_infosoperacionais, textvariable=self.TempoGastoVar)
		self.TempoGastoVarLabel.grid(row=3, column=1)
		self.ConsumoCombEspecVar = tk.DoubleVar()
		self.ConsumoCombEspecLabel = tk.Label(self.frame_infosoperacionais, text='Consumo de combustivel específico (L/kWh): ').grid(row=4, column=0)
		self.ConsumoCombEspecVarLabel = tk.Label(self.frame_infosoperacionais, textvariable=self.ConsumoCombEspecVar)
		self.ConsumoCombEspecVarLabel.grid(row=4, column=1)
		self.ConsumoCombHoraVar = tk.DoubleVar()
		self.ConsumoCombHoraLabel = tk.Label(self.frame_infosoperacionais, text='Consumo de combustivel por hora (L/h): ').grid(row=5, column=0)
		self.ConsumoCombHoraVarLabel = tk.Label(self.frame_infosoperacionais, textvariable=self.ConsumoCombHoraVar)
		self.ConsumoCombHoraVarLabel.grid(row=5, column=1)

		#Exibição dos Custos Fixos
		self.DepreciacaoTratorLabel = tk.Label(self.frame_custofixotrator, text='Depreciação (R$/h): ').grid(row=0, column=0)
		self.DepreciacaoTratorVar = tk.DoubleVar()
		self.DepreciacaoTratorVarLabel = tk.Label(self.frame_custofixotrator, textvariable=self.DepreciacaoTratorVar)
		self.DepreciacaoTratorVarLabel.grid(row=0, column=1)
		self.JuroTratorLabel = tk.Label(self.frame_custofixotrator, text='Juros sobre o capital (R$/h): ').grid(row=1, column=0)
		self.JuroTratorVar = tk.DoubleVar()
		self.JuroTratorVarLabel = tk.Label(self.frame_custofixotrator, textvariable=self.JuroTratorVar)
		self.JuroTratorVarLabel.grid(row=1, column=1)
		self.GaragemTratorLabel = tk.Label(self.frame_custofixotrator, text='Garagem (R$/h): ').grid(row=2, column=0)
		self.GaragemTratorVar = tk.DoubleVar()
		self.GaragemTratorVarLabel = tk.Label(self.frame_custofixotrator, textvariable=self.GaragemTratorVar)
		self.GaragemTratorVarLabel.grid(row=2, column=1)
		self.SeguroTratorLabel = tk.Label(self.frame_custofixotrator, text='Seguro (R$/h): ').grid(row=3, column=0)
		self.SeguroTratorVar = tk.DoubleVar()
		self.SeguroTratorVarLabel = tk.Label(self.frame_custofixotrator, textvariable=self.SeguroTratorVar)
		self.SeguroTratorVarLabel.grid(row=3, column=1)
		self.CustoFixoTratorLabel = tk.Label(self.frame_custofixotrator, text='Total (R$/h): ').grid(row=4, column=0)
		self.CustoFixoTratorVar = tk.DoubleVar()
		self.CustoFixoTratorVarLabel = tk.Label(self.frame_custofixotrator, textvariable=self.CustoFixoTratorVar)
		self.CustoFixoTratorVarLabel.grid(row=4, column=1)
		self.DepreciacaoImplementoLabel = tk.Label(self.frame_custofixoImplemento, text='Depreciação (R$/h): ').grid(row=0, column=0)
		self.DepreciacaoImplementoVar = tk.DoubleVar()
		self.DepreciacaoImplementoVarLabel = tk.Label(self.frame_custofixoImplemento, textvariable=self.DepreciacaoImplementoVar)
		self.DepreciacaoImplementoVarLabel.grid(row=0, column=1)
		self.JuroImplementoLabel = tk.Label(self.frame_custofixoImplemento, text='Juros sobre o capital (R$/h): ').grid(row=1, column=0)
		self.JuroImplementoVar = tk.DoubleVar()
		self.JuroImplementoVarLabel = tk.Label(self.frame_custofixoImplemento, textvariable=self.JuroImplementoVar)
		self.JuroImplementoVarLabel.grid(row=1, column=1)
		self.GaragemImplementoLabel = tk.Label(self.frame_custofixoImplemento, text='Garagem (R$/h): ').grid(row=2, column=0)
		self.GaragemImplementoVar = tk.DoubleVar()
		self.GaragemImplementoVarLabel = tk.Label(self.frame_custofixoImplemento, textvariable=self.GaragemImplementoVar)
		self.GaragemImplementoVarLabel.grid(row=2, column=1)
		self.SeguroImplementoLabel = tk.Label(self.frame_custofixoImplemento, text='Seguro (R$/h): ').grid(row=3, column=0)
		self.SeguroImplementoVar = tk.DoubleVar()
		self.SeguroImplementoVarLabel = tk.Label(self.frame_custofixoImplemento, textvariable=self.SeguroImplementoVar)
		self.SeguroImplementoVarLabel.grid(row=3, column=1)
		self.CustoFixoImplementoLabel = tk.Label(self.frame_custofixoImplemento, text='Total (R$/h): ').grid(row=4, column=0)
		self.CustoFixoImplementoVar = tk.DoubleVar()
		self.CustoFixoImplementoVarLabel = tk.Label(self.frame_custofixoImplemento, textvariable=self.CustoFixoImplementoVar)
		self.CustoFixoImplementoVarLabel.grid(row=4, column=1)

		#Exibição dos Custos Operacionais
		self.CustoCombHoraLabel = tk.Label(self.frame_custosop, text='Custo combustível (R$/h): ').grid(row=0, column=0)
		self.CustoCombHoraVar = tk.DoubleVar()
		self.CustoCombHoraVarLabel = tk.Label(self.frame_custosop, textvariable=self.CustoCombHoraVar)
		self.CustoCombHoraVarLabel.grid(row=0, column=1)
		self.CustoOleoHoraLabel = tk.Label(self.frame_custosop, text='Custo óleo lubrificante (R$/h): ').grid(row=1, column=0)
		self.CustoOleoHoraVar = tk.DoubleVar()
		self.CustoOleoHoraVarLabel = tk.Label(self.frame_custosop, textvariable=self.CustoOleoHoraVar)
		self.CustoOleoHoraVarLabel.grid(row=1, column=1)
		self.CustoTratoristaHoraLabel = tk.Label(self.frame_custosop, text='Custo tratorista (R$/h): ').grid(row=2, column=0)
		self.CustoTratoristaHoraVarLabel = tk.Label(self.frame_custosop, textvariable=self.PrecoTratoristaVar)
		self.CustoTratoristaHoraVarLabel.grid(row=2, column=1)
		self.CustoManutencaoHoraTratorLabel = tk.Label(self.frame_custosop, text='Custo manutenção trator (R$/h): ').grid(row=3, column=0)
		self.CustoManutencaoHoraTratorVar = tk.DoubleVar()
		self.CustoManutencaoHoraTratorVarLabel = tk.Label(self.frame_custosop, textvariable=self.CustoManutencaoHoraTratorVar)
		self.CustoManutencaoHoraTratorVarLabel.grid(row=3, column=1)
		self.CustoOperacionalLabel = tk.Label(self.frame_custosop, text='Total (R$/h): ').grid(row=4, column=0)
		self.CustoOperacionalVar = tk.DoubleVar()
		self.CustoOperacionalVarLabel = tk.Label(self.frame_custosop, textvariable=self.CustoOperacionalVar)
		self.CustoOperacionalVarLabel.grid(row=4, column=1)

		#Exibição dos Custos Totais
		self.CustoTotalHorarioLabel = tk.Label(self.frame_custostotais, text='Custo horário (R$/h): ').grid(row=0, column=0)
		self.CustoTotalHorarioVar = tk.DoubleVar()
		self.CustoTotalHorarioVarLabel = tk.Label(self.frame_custostotais, textvariable=self.CustoTotalHorarioVar)
		self.CustoTotalHorarioVarLabel.grid(row=0, column=1)
		self.CustoTotalHectareLabel = tk.Label(self.frame_custostotais, text='Custo hectare (R$/ha): ').grid(row=1, column=0)
		self.CustoTotalHectareVar = tk.DoubleVar()
		self.CustoTotalHectareVarLabel = tk.Label(self.frame_custostotais, textvariable=self.CustoTotalHectareVar)
		self.CustoTotalHectareVarLabel.grid(row=1, column=1)
		self.CustoTotalLabel = tk.Label(self.frame_custostotais, text='Custo total (R$): ').grid(row=2, column=0)
		self.CustoTotalVar = tk.DoubleVar()
		self.CustoTotalVarLabel = tk.Label(self.frame_custostotais, textvariable=self.CustoTotalVar)
		self.CustoTotalVarLabel.grid(row=2, column=1)
	
		#Botões
		self.quitButton = tk.Button(self.frame_buttons, text = 'Voltar', command=self.master.destroy)
		self.quitButton.grid(row=0, column=2)
		self.exportPDFButton = tk.Button(self.frame_buttons, text = 'Gerar PDF', command=self.GeneratePDF)
		self.exportPDFButton.grid(row=0, column=0)
		self.submitButton = tk.Button(self.frame_buttons, text='Salvar simulação', command=self.submitDB)
		self.submitButton.grid(row=0, column=1)

	def GeneratePDF(self):
		dirname = os.path.dirname(__file__)
		final_dirname = dirname[:-16]
		filename = os.path.join(final_dirname, 'Relatorios\\')
		gray50transparent = Color(0.3,0.3,0.3, alpha=0.3)
		DataHoje = date.today()
		DataHojeString = DataHoje.strftime('%d%m%Y')
		NomePDF = DataHojeString + '_' + str(self.NomeImplemento) + str(self.NomeTalhao)
		pdf = canvas.Canvas(filename + '{}.pdf'.format(NomePDF))
		pdf.setTitle(NomePDF)
		pdf.setFont('Helvetica-Bold', 16)
		pdf.drawString(150, 810, 'RELATÓRIO DETALHADO DE SIMULAÇÃO')
		pdf.setFont('Helvetica-Bold', 12)
		pdf.drawString(160, 770, 'Dados de Entrada')
		pdf.setFont('Helvetica-Bold', 10)
		pdf.drawString(12, 747,'Trator')
		pdf.setFont('Helvetica', 10)
		pdf.drawString(17, 730,'Nome do Trator: {}'.format(self.NomeTrator))
		pdf.drawString(17, 720,'Potência nominal (cv): {}'.format(self.PotenciaTrator))
		pdf.drawString(17, 710,'Tipo de transmissão: {}'.format(self.TransmissaoTrator))
		pdf.drawString(17, 700,'Valor de compra (R$): {}'.format(self.ValorCompraTrator))
		pdf.drawString(17, 690,'Taxa de juros (%): {}'.format(self.TaxaJurosTrator))
		pdf.drawString(17, 680,'Taxa de seguro (%): {}'.format(self.TaxaSeguroTrator))
		pdf.drawString(17, 670,'Taxa de garagem (%): {}'.format(self.TaxaGaragemTrator))
		pdf.drawString(17, 660,'Vida útil esperada (horas): {}'.format(self.VidaUtilHoraTrator))
		pdf.setFont('Helvetica-Bold', 10)
		pdf.drawString(205, 685,'Implemento')
		pdf.setFont('Helvetica', 10)
		x = 668
		pdf.drawString(210, x,'Nome do implemento: {}'.format(self.NomeImplemento))
		pdf.drawString(210, x-10,'Tipo do implemento: {}'.format(self.TipoImplemento))
		pdf.drawString(210, x-20,'Largura de operação (m): {}'.format(self.LarguraImplemento))
		pdf.drawString(210, x-30,'Número de linhas: {}'.format(self.LinhaImplemento))
		pdf.drawString(210, x-40,'Número de órgãos ativos: {}'.format(self.OrgaoImplemento))
		pdf.drawString(210, x-50,'Valor de compra (R$): {}'.format(self.ValorCompraImplemento))
		pdf.drawString(210, x-60,'Taxa de juros (%): {}'.format(self.TaxaJurosImplemento))
		pdf.drawString(210, x-70,'Taxa de seguro (%): {}'.format(self.TaxaSeguroImplemento))
		pdf.drawString(210, x-80,'Taxa de garagem (%): {}'.format(self.TaxaGaragemImplemento))
		pdf.drawString(210, x-90,'Vida útil esperada (horas): {}'.format(self.VidaUtilHoraImplemento))
		pdf.setFont('Helvetica-Bold', 10)
		pdf.drawString(205, 747,'Talhão')
		pdf.setFont('Helvetica', 10)
		pdf.drawString(210, 730,'Nome do talhão: {}'.format(self.NomeTalhao))
		pdf.drawString(210, 720,'Área do talhão (ha): {}'.format(self.AreaTalhao))
		pdf.drawString(210, 710,'Textura do solo: {}'.format(self.TexturaTalhao))
		pdf.setFont('Helvetica-Bold', 10)
		pdf.drawString(12, 635, 'Operação')
		pdf.setFont('Helvetica', 10)
		x=618
		pdf.drawString(17, x,'Velocidade de operação (km/h): {}'.format(self.VelocidadeOperacao))
		pdf.drawString(17, x-10,'Profundidade de operãção (cm): {}'.format(self.ProfundidadeOperacao))
		pdf.drawString(17, x-20,'Passada no solo: {}'.format(self.PassadaOperacao))
		pdf.drawString(17, x-30,'Superfície do solo: {}'.format(self.CondicaoSolo))
		pdf.drawString(17, x-40,'Preço do combustível (R$/L): {}'.format(self.PrecoCombustivel))
		pdf.drawString(17, x-50,'Preço do óleo lubrificante (R$/L): {}'.format(self.PrecoOleo))
		pdf.drawString(17, x-60,'Preço tratorista (R$/h): {}'.format(self.PrecoTratorista))

		pdf.setFillColor(gray50transparent)
		pdf.rect(5, 800, 585, 30, stroke=True, fill=True) #TITULO RESULTADO DETALHADO DA SIMULACAO
		pdf.rect(5, 765, 390, 20, stroke=True, fill=True) #TITULO DADOS DE ENTRADA
		pdf.rect(415, 765, 175, 20, stroke=True, fill=True) #TITULO PARAMETROS DA EQUACAO
		pdf.rect(5, 528, 585, 20, stroke=True, fill=True) #TIULO DADOS DE SAIDA
		pdf.rect(395, 494, 195, 20, stroke=True, fill=True) #TITULO INFORMACOES OPERACIONAIS
		pdf.rect(5, 494, 175, 20, stroke=True, fill=True) #TITULO CUSTO FIXOS
		pdf.rect(200, 494, 175, 20, stroke=True, fill=True) #TITULO CUSTOS OPERACIONAIS
		pdf.rect(200, 345, 390, 20, stroke=True, fill=True) #TITULO CUSTOS TOTAIS
		pdf.rect(5, 243, 180, 20, stroke=True, fill=True)  #TITULO GRAFICO CF TRATOR
		pdf.rect(200, 243, 180, 20, stroke=True, fill=True)  #TITULO GRAFICO CF IMPLEMENTO
		pdf.rect(400, 243, 180, 20, stroke=True, fill=True)  #TITULO GRAFICO CV
		pdf.line(197, 760, 197, 555) #LINHA ENTRE TRATOR E TALHAO
		pdf.line(15, 650, 193, 650) #LINHA ENTRE TRATOR E OPERACAO
		pdf.line(201, 700, 402, 700) #LINHA ENTRE TALHAO E IMPLEMENTO
		pdf.line(405, 760, 405, 555) #LINHA ENTRE IMPLEMENTO E PARAMETROS DAS EQUACOES
		pdf.line(190, 490, 190, 310) #LINHA ENTRE CUSTO FIXO E OPERACIONAL
		pdf.line(385, 490, 385, 383) #LINHA ENTRE CUSTO OPERACIONAL E INFO OPERACIONAIS
		pdf.line(15, 413, 185, 413) #LINHA ENTRE CUSTO FIXO TRATOR E IMPLEMENTO
		


		pdf.setFont('Helvetica-Bold', 12)
		pdf.setFillColor('black')
		pdf.drawString(425, 770, 'Parâmetros das Equações')
		pdf.setFont('Helvetica', 10)
		x = 746
		pdf.drawString(418, x, 'Parâmetro A: {}'.format(self.ParametroA))
		pdf.drawString(418, x-10, 'Parâmetro B: {}'.format(self.ParametroB))
		pdf.drawString(418, x-20, 'Parâmetro C: {}'.format(self.ParametroC))
		pdf.drawString(418, x-30, 'Parâmetro F: {}'.format(self.ParametroF))
		pdf.drawString(418, x-40, 'Coeficiente de transmissão: {}'.format(self.CoeficienteTransmissao))
		pdf.drawString(418, x-50, 'Eficiência de campo mínima (%): {}'.format(self.EficienciaCampoMinima))
		pdf.drawString(418, x-60, 'Eficiência de campo máxima (%): {}'.format(self.EficienciaCampoMaxima))


		pdf.setFont('Helvetica-Bold', 12)
		pdf.drawString(420, 500, 'Informações Operacionais')
		pdf.drawString(250, 533, 'Resultado da simulação')
		pdf.drawString(228, 500, 'Custos Operacionais')
		pdf.setFillColor('red')
		pdf.drawString(350, 350, 'Custos totais')

		pdf.setFillColor('black')
		pdf.setFont('Helvetica-Bold', 12)
		pdf.drawString(50, 500, 'Custos Fixos')
		pdf.setFont('Helvetica-Bold', 10)
		pdf.drawString(12, 480, 'Trator')
		pdf.drawString(12, 400, 'Implemento')
		pdf.setFont('Helvetica', 10)
		x=465
		pdf.drawString(17, x,'Depreciação (R$/h): {}'.format(str("%.2f" % self.DepreciacaoTrator)))
		pdf.drawString(17, x-10,'Juros sobre o capital (R$/h): {}'.format(str("%.2f" % self.JuroTrator)))
		pdf.drawString(17, x-20,'Garagem (R$/h): {}'.format(str("%.2f" % self.GaragemTrator)))
		pdf.drawString(17, x-30,'Seguro (R$/h): {}'.format(str("%.2f" % self.SeguroTrator)))
		pdf.setFillColor('red')
		pdf.drawString(17, x-40,'Total (R$/h): {}'.format(str("%.2f" % self.CustoFixoTrator)))
		x=385
		pdf.setFillColor('black')
		pdf.drawString(17, x,'Depreciação (R$/h): {}'.format(str("%.2f" % self.DepreciacaoImplemento)))
		pdf.drawString(17, x-10,'Juros sobre o capital (R$/h): {}'.format(str("%.2f" % self.JuroImplemento)))
		pdf.drawString(17, x-20,'Garagem (R$/h): {}'.format(str("%.2f" % self.GaragemImplemento)))
		pdf.drawString(17, x-30,'Seguro (R$/h): {}'.format(str("%.2f" % self.SeguroImplemento)))
		pdf.setFillColor('red')
		pdf.drawString(17, x-40,'Total (R$/h): {}'.format(str("%.2f" % self.CustoFixoImplemento)))
		x=480
		pdf.setFillColor('black')
		pdf.drawString(210, x, 'Combustível (R$/h): {}'.format(str("%.2f" % self.CustoCombHora)))
		pdf.drawString(210, x-10, 'Óleo lubrificante (R$/h): {}'.format(str("%.2f" % self.CustoOleoHora)))
		pdf.drawString(210, x-20, 'Manutenção trator (R$/h): {}'.format(str("%.2f" % self.CustoManutencaoHoraTrator)))
		pdf.drawString(210, x-30, 'Tratorista (R$/h): {}'.format(str("%.2f" % self.PrecoTratorista)))
		pdf.setFillColor('red')
		pdf.drawString(210, x-40, 'Total (R$/h): {}'.format(str("%.2f" % self.CustoOperacional)))
		pdf.setFillColor('black')
		pdf.drawString(398, x, 'Força requerida implemento (kN): {}'.format(str("%.2f" % self.ForcaReqImplemento)))
		pdf.drawString(398, x-10, 'Potência requerida BT (kW): {}'.format(str("%.2f" % self.PotenciaReqImplementoBT)))
		pdf.drawString(398, x-20, 'Potência requerida TDP (kW): {}'.format(str("%.2f" % self.PotenciaReqImplementoTDP)))
		pdf.drawString(398, x-30, 'Potência max disponível TDP (kW): {}'.format(str("%.2f" % self.PotenciaDispTratorTDP)))
		pdf.drawString(398, x-40, 'Consumo específico comb (L/kWh): {}'.format(str("%.2f" % self.ConsumoCombEspec)))
		pdf.drawString(398, x-50, 'Consumo horário combustível (L/h): {}'.format(str("%.2f" % self.ConsumoCombHora)))
		pdf.drawString(398, x-70, 'Eficiência de campo: {}'.format(str("%.2f" % self.EficienciaCampo)))
		pdf.drawString(398, x-80, 'Capacidade de campo teórica (ha/h): {}'.format(str("%.2f" % self.CapacidadeCampoTeorica)))
		pdf.drawString(398, x-90, 'Capacidade de campo efetiva (ha/h): {}'.format(str("%.2f" % self.CapacidadeCampoEfetiva)))
		pdf.drawString(398, x-100, 'Tempo total de operação (h): {}'.format(str("%.2f" % self.TempoGasto)))
		pdf.setFillColor('red')
		pdf.drawString(398, x-60, 'Eficiência Tratória: {}'.format(str("%.2f" % self.FatorX)))
		pdf.setFont('Helvetica-Bold', 10)
		pdf.setFillColor('red')
		x = 330
		pdf.drawString(260, x, 'Custo horário da operação (R$/h): {}'.format(str("%.2f" % self.CustoTotalHorario)))
		pdf.drawString(260, x-10, 'Custo hectare da operação (R$/ha): {}'.format(str("%.2f" % self.CustoTotalHectare)))
		pdf.drawString(260, x-20, 'Custo total da operação (R$): {}'.format(str("%.2f" % self.CustoTotal)))
		pdf.rotate(90)
		pdf.setFillColor('black')
		pdf.drawString(95, -410, 'Reais por hora (R$/h)')
		pdf.drawString(95, -210, 'Reais por hora (R$/h)')
		pdf.drawString(95, -15, 'Reais por hora (R$/h)')
		pdf.rotate(-90)
		pdf.drawString(50, 250, 'Custos fixos Trator')
		pdf.drawString(230, 250, 'Custos fixos Implemento')
		pdf.drawString(440, 250, 'Custos operacionais')
		graficoCustoFixoTrator = self.GraficoCustoFixoTrator()
		graficoCustoFixoImplemento = self.GraficoCustoFixoImplemento()
		graficoCustoVariavel = self.GraficoCustoVariavel()
		renderPDF.draw(graficoCustoFixoTrator, pdf, 35, 70)
		renderPDF.draw(graficoCustoFixoImplemento, pdf, 235, 70)
		renderPDF.draw(graficoCustoVariavel, pdf, 430, 70)
		pdf.save()
		messagebox.showinfo(title="Sucesso", message="O arquivo foi salvo na pasta 'Relatorios', localizada onde se encontra o programa.")
		self.master.focus_force()
		return

	def submitDB(self):
		self.conn = sqlite3.connect('database.db')
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS operacao( 
									 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
									 talhao INTEGER NOT NULL,
									 trator INTEGER NOT NULL,
									 implemento INTEGER NOT NULL,
									 nome_talhao TEXT,
									 nome_trator TEXT,
									 nome_implemento TEXT,
									 velocidade REAL,
									 profundidade REAL,
									 superficie TEXT,
									 passada TEXT,
									 diesel REAL,
									 oleo REAL,
									 tratorista REAL)""")
		self.values_db = "INSERT INTO operacao(talhao, trator, implemento, nome_talhao, nome_trator, nome_implemento, velocidade, profundidade, superficie, passada, diesel, oleo, tratorista) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)" #Atribuindo a variavel a sintaxe SQLITE3
		self.c.execute(self.values_db, (self.IDTalhao, self.IDTrator, self.IDImplemento, self.NomeTalhao, self.NomeTrator, self.NomeImplemento, \
			self.VelocidadeOperacao, self.ProfundidadeOperacao, self.CondicaoSolo, self.PassadaOperacao, self.PrecoCombustivel, self.PrecoOleo, \
			self.PrecoTratorista)) #Inserindo os valores de entrada na tabela do banco de dados
		self.conn.commit() #Commitando as alterações
		self.conn.close() #Fechando a conexão

	def GraficoCustoFixoTrator(self):
		grafico = Drawing(200,200)
		dados = [(self.DepreciacaoTrator, self.JuroTrator, self.GaragemTrator, self.SeguroTrator),]
		barras = VerticalBarChart()
		barras.x = 0
		barras.y = 0
		barras.height = 150
		barras.width = 150
		barras.data = dados
		barras.barLabelFormat = DecimalFormatter(2)
		barras.barLabels.nudge = 6
		barras.categoryAxis.categoryNames = ['Depreciação', 'Juros', 'Garagem', 'Seguro']
		barras.categoryAxis.labels.angle = 45
		barras.categoryAxis.labels.boxAnchor = 'ne'
		grafico.add(barras)
		return grafico

	def GraficoCustoFixoImplemento(self):
		grafico = Drawing(200,200)
		dados = [(self.DepreciacaoImplemento, self.JuroImplemento, self.GaragemImplemento, self.SeguroImplemento),]
		barras = VerticalBarChart()
		barras.x = 0
		barras.y = 0
		barras.height = 150
		barras.width = 150
		barras.data = dados
		barras.barLabelFormat = DecimalFormatter(2)
		barras.barLabels.nudge = 6
		barras.categoryAxis.categoryNames = ['Depreciação', 'Juros', 'Garagem', 'Seguro']
		barras.categoryAxis.labels.angle = 45
		barras.categoryAxis.labels.boxAnchor = 'ne'
		grafico.add(barras)
		return grafico

	def GraficoCustoVariavel(self):
		grafico = Drawing(200, 200)
		dados = [(self.CustoCombHora, self.CustoOleoHora, self.CustoManutencaoHoraTrator, self.PrecoTratorista),]
		barras = VerticalBarChart()
		barras.x = 0
		barras.y = 0
		barras.height = 150
		barras.width = 150
		barras.data = dados
		barras.barLabelFormat = DecimalFormatter(2)
		barras.barLabels.nudge = 6
		barras.categoryAxis.categoryNames = ['Combustível', 'Óleo', 'Manutenção', 'Operador']
		barras.categoryAxis.labels.angle = 45
		barras.categoryAxis.labels.boxAnchor = 'ne'
		grafico.add(barras)
		return grafico
	


