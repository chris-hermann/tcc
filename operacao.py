import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, re, parameters, math, outputs
import tkinter.font as tkFont

class OperacaoPage():
	def __init__(self, master):
		self.master = master
		self.master.title('Simulação de operação agrícola')
		self.master.iconbitmap('icon.ico')
		self.master.resizable(False, False)
		self.frame_inputs = tk.Frame(self.master)
		self.frame_buttons = tk.Frame(self.master)
		self.frame_hist = tk.Frame(self.master)
		self.frame_inputs.grid()
		self.frame_buttons.grid()
		self.frame_hist.grid()
		self.spaceLabel3 = tk.Label(self.frame_inputs, text = "    ").grid()
		self.trv_implemento_label = tk.Label(self.frame_inputs, text='Selecione um talhão, trator e implemento abaixo').grid(row=0, column=0, columnspan=3)
		self.trv_trator = tk.ttk.Treeview(self.frame_inputs, columns=(1,2,3), show="headings", height='3', selectmode='browse', displaycolumns=('2','3'))
		self.trv_talhao = tk.ttk.Treeview(self.frame_inputs, columns=(1,2,3), show="headings", height='3', selectmode='browse', displaycolumns=('2','3'))
		self.trv_implemento = tk.ttk.Treeview(self.frame_inputs, columns=(1,2,3), show="headings", height='3', selectmode='browse', displaycolumns=('2','3'))
		self.trv_talhao.grid(row=1, column=0, padx=3, pady=3)
		self.trv_talhao.column('2', width=80, anchor='center')
		self.trv_talhao.column('3', width=80, anchor='center')
		self.trv_trator.column('2', width=80, anchor='center', minwidth=50)
		self.trv_trator.column('3', width=80, anchor='center', minwidth=50)
		self.trv_implemento.column('2', width=110, anchor='center', minwidth=50)
		self.trv_implemento.column('3', width=370, anchor='center', minwidth=50)
		self.trv_trator.heading(2, text='Nome')
		self.trv_trator.heading(3, text='Potência (cv)')
		self.trv_talhao.heading(2, text='Nome')
		self.trv_talhao.heading(3, text='Área (ha)')
		self.trv_implemento.heading(2, text='Nome')
		self.trv_implemento.heading(3, text='Tipo')
		self.trv_trator.grid(row=1, column=1, padx=2, pady=3)
		self.trv_implemento.grid(row=1, column=2, padx=3, pady=3)
		self.trv_implemento.bind('<ButtonRelease-1>', self.callback)
		self.trv_implementoPop()
		self.trv_tratorPop()
		self.trv_talhaoPop()
		self.spacerLabel1 = tk.Label(self.frame_inputs).grid(row=1)
		self.velocidadeLabel = tk.Label(self.frame_inputs, text='Velocidade de operação (km/h):').grid(row=2, column=0)
		self.velocidade = tk.Entry(self.frame_inputs)
		self.velocidade.grid(row=2, column=1)
		self.condicaosoloLabel = tk.Label(self.frame_inputs, text='Condição da superfície do solo:').grid(row=3, column=0)
		self.condicaoSolo = tk.ttk.Combobox(self.frame_inputs, values=['Firme','Arado','Gradeado'])
		self.condicaoSolo.grid(row=3, column=1)
		self.profundidade = tk.Entry(self.frame_inputs)
		self.passada = tk.ttk.Combobox(self.frame_inputs, values=['Primeira', 'Segunda'])
		self.passadaLabel = tk.Label(self.frame_inputs, text='Passada?')
		self.precoDiesel = tk.Entry(self.frame_inputs)
		self.precoOleo = tk.Entry(self.frame_inputs)
		self.precoTratorista = tk.Entry(self.frame_inputs)
		self.precoDieselLabel = tk.Label(self.frame_inputs, text='Preço do diesel (R$/L): ')
		self.precoOleoLabel = tk.Label(self.frame_inputs, text='Preço do óleo (R$/L): ')
		self.precoTratoristaLabel = tk.Label(self.frame_inputs, text='Preço do tratorista (R$/h): ')
		self.profundidadeLabel = tk.Label(self.frame_inputs,text='Profundidade de operação (cm):')
		self.simulateButton = tk.Button(self.frame_buttons, text='Simular operação', command=self.simulate)
		self.simulateButton.grid(row=0, column=0, padx=3, pady=7)
		self.quitButton = tk.Button(self.frame_buttons, text='Voltar', command=self.master.destroy)
		self.submitButton = tk.Button(self.frame_buttons, text='Salvar simulação', command=self.submitDB, state=tk.DISABLED)
		self.submitButton.grid(row=0, column=1, padx=2, pady=7)
		self.quitButton.grid(row=0, column=2, padx=3, pady=7)
		self.titlefont = tkFont.Font(family='Helvetica', size=22, weight='bold')
		self.spacerLabel2 = tk.Label(self.frame_buttons).grid(row=1)
		self.trvLabel = tk.Label(self.frame_hist, text='Histórico', font=self.titlefont, anchor = tk.W).grid()
		self.trvHelper = tk.Label(self.frame_hist, text='Dê um clique duplo em algum item do histórico para editar os valores de entrada').grid()
		self.trv_hist = tk.ttk.Treeview(self.frame_hist, columns=(1,2,3,4,5,6,7,8,9,10,11,12,13,14), show='headings', height='3', selectmode='browse', displaycolumns=('5','6','7','8','9','10','11','12','13','14'))
		self.trv_hist.heading(5, text='Nome do talhão')
		self.trv_hist.heading(6, text='Nome do trator')
		self.trv_hist.heading(7, text='Nome do implemento')
		self.trv_hist.heading(8, text='Velocidade')
		self.trv_hist.heading(9, text='Profundidade')
		self.trv_hist.heading(10, text='Superficie')
		self.trv_hist.heading(11, text='Passada')
		self.trv_hist.heading(12, text='Preço diesel')
		self.trv_hist.heading(13, text='Preço óleo')
		self.trv_hist.heading(14, text='Preço tratorista')
		self.trv_hist.column('5', minwidth=30, width=95, anchor='center')
		self.trv_hist.column('6', minwidth=30, width=95, anchor='center')
		self.trv_hist.column('7', minwidth=30, width=130, anchor='center')
		self.trv_hist.column('8', minwidth=30, width=70, anchor='center')
		self.trv_hist.column('9', minwidth=30, width=80, anchor='center')
		self.trv_hist.column('10', minwidth=30, width=70, anchor='center')
		self.trv_hist.column('11', minwidth=30, width=70, anchor='center')
		self.trv_hist.column('12', minwidth=30, width=70, anchor='center')
		self.trv_hist.column('13', minwidth=30, width=70, anchor='center')
		self.trv_hist.column('14', minwidth=30, width=95, anchor='center')
		self.trv_hist.grid(padx=3, pady=3)
		self.trv_hist.bind('<Double 1>', self.view_simulation)
		self.hozscrlbar = tk.ttk.Scrollbar(self.frame_hist, orient=tk.HORIZONTAL, command=self.trv_hist.xview)
		self.hozscrlbar.grid(sticky=tk.S, columnspan=2)
		self.trv_hist.configure(xscrollcommand=self.hozscrlbar.set)
		self.update_trv()
	
	def trv_tratorPop(self):
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		query = "SELECT id, nome, pot FROM trator"
		c.execute(query)
		row = c.fetchall()
		self.trv_trator.delete(*self.trv_trator.get_children())
		for i in row:
			self.trv_trator.insert('', "end", values=i)
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão

	def trv_implementoPop(self):
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		query = "SELECT id, nome, tipo FROM implemento"
		c.execute(query)
		row = c.fetchall()
		self.trv_implemento.delete(*self.trv_implemento.get_children())
		for i in row:
			self.trv_implemento.insert('', "end", values=i)
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão

	def trv_talhaoPop(self):
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		query = "SELECT id, nome, area FROM talhao"
		c.execute(query)
		row = c.fetchall()
		self.trv_talhao.delete(*self.trv_talhao.get_children())
		for i in row:
			self.trv_talhao.insert('', "end", values=i)
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão

	def callback(self, event):
		self.passada.delete(0, tk.END)
		self.profundidade.grid_forget()
		self.profundidadeLabel.grid_forget()
		self.passada.grid_forget()
		self.passadaLabel.grid_forget()
		self.trv_selection = self.trv_implemento.item(self.trv_implemento.focus())
		self.tipo = self.trv_selection['values'][2]
		if self.tipo == 'Arado de aivecas' or self.tipo == 'Arado de discos' or self.tipo == 'Subsolador - ponteira simples' or \
						self.tipo == 'Subsolador - ponteira com asas' or self.tipo == 'Cultivador de campo' or self.tipo == 'Sulcador' or \
						self.tipo == 'Grade de discos - ação dupla em X - Tandem' or self.tipo == 'Grade de discos - ação dupla em V - Offset'or \
						self.tipo == 'Grade de discos - ação simples' or self.tipo == 'Cultivador de campo':
			self.profundidade.grid(row=4, column=1)
			self.profundidadeLabel.grid(row=4, column=0)			

		if self.tipo == 'Grade de discos - ação dupla em X - Tandem' or self.tipo == 'Grade de discos - ação dupla em V - Offset'or \
						self.tipo == 'Grade de discos - ação simples' or self.tipo == 'Cultivador de campo':
			self.passada.grid(row=5, column=1)
			self.passadaLabel.grid(row=5, column=0)
		self.precoDieselLabel.grid(row=6, column=0)
		self.precoOleoLabel.grid(row=7, column=0)
		self.precoTratoristaLabel.grid(row=8, column=0)
		self.precoDiesel.grid(row=6, column=1)
		self.precoOleo.grid(row=7, column=1)
		self.precoTratorista.grid(row=8, column=1)

	def simulate(self):
		self.talhao_selection = self.trv_talhao.item(self.trv_talhao.focus())
		self.idTalhao = self.talhao_selection['values'][0]
		self.nomeTalhao = self.talhao_selection['values'][1]
		self.trator_selection = self.trv_trator.item(self.trv_trator.focus())
		self.idTrator = self.trator_selection['values'][0]
		self.nomeTrator = self.trator_selection['values'][1]
		self.implemento_selection = self.trv_implemento.item(self.trv_implemento.focus())
		self.idImplemento = self.implemento_selection['values'][0]
		self.nomeImplemento = self.implemento_selection['values'][1]
		self.talhaoData = self.searchDB(self.idTalhao, 'talhao')
		self.tratorData = self.searchDB(self.idTrator, 'trator')
		self.implementoData = self.searchDB(self.idImplemento, 'implemento')
		self.talhaoData = str(self.talhaoData)
		self.tratorData = str(self.tratorData)
		self.implementoData = str(self.implementoData)
		self.talhaoData = self.talhaoData.split(',')
		self.tratorData = self.tratorData.split(',')
		self.implementoData = self.implementoData.split(',')
		self.areaTalhao = float(self.talhaoData[2].strip(' '))
		self.texturaTalhao =  str(self.talhaoData[3].strip("[]()' "))
		self.potenciaMotor = float(self.tratorData[2].strip())
		self.transmissaoTrator = str(self.tratorData[3].strip("[]()' "))
		self.transmissaoTrator = self.transmissaoTrator.replace(" ","")
		self.tipoImplemento = str(self.implementoData[2].strip(" '"))
		self.larguraImplemento = float(self.implementoData[3].strip(' '))
		self.orgaosImplemento = self.implementoData[4].strip(' ')
		self.linhasImplemento = self.implementoData[5].strip(' ')
		self.velocidadeOperacao = float(self.velocidade.get())
		self.profundidadeOperacao = self.profundidade.get()
		if self.profundidadeOperacao == '':
			self.profundidadeOperacao = 1
		else:
			self.profundidadeOperacao = float(self.profundidadeOperacao)
		self.passadaOperacao = str(self.passada.get())
		self.soloOperacao = str(self.condicaoSolo.get())
		self.rTranmissaoKey = self.transmissaoTrator + self.soloOperacao
		self.coefTransmissao = parameters.relacaoTransmissao.get(self.rTranmissaoKey)
		if self.tipoImplemento == 'Arado de discos':
			self.parametersKey = 'Aradodediscos'
			self.parametersList = parameters.Parametros.get(self.parametersKey)
			self.parametersList = str(self.parametersList)
			self.parametersList = self.parametersList.split(',')
			self.rangeAcuracia = float(self.parametersList[6].strip("[]()' "))
			if self.texturaTalhao == 'Argilosa':
				self.parametroA = float(self.parametersList[4].strip("[]()' "))
				self.parametroB = float(self.parametersList[5].strip("[]()' "))
			elif self.texturaTalhao == 'Média':
				self.parametroA = float(self.parametersList[2].strip("[]()' "))
				self.parametroB = float(self.parametersList[3].strip("[]()' "))
			else:
				self.parametroA = float(self.parametersList[0].strip("[]()' "))
				self.parametroB = float(self.parametersList[1].strip("[]()' "))
			self.forca_requerida_op = (self.profundidadeOperacao * self.larguraImplemento * 100) * (self.parametroA + self.parametroB * (math.pow(self.velocidadeOperacao,2)))/1000
		else:
			self.parametersKey = self.tipoImplemento + self.passadaOperacao
			self.parametersKey = self.parametersKey.replace(" ","")
			self.parametersKey = self.parametersKey.replace("-","")
			self.parametersKey = self.parametersKey.replace(")","")
			self.parametersKey = self.parametersKey.replace("(","")
			self.parametersList = parameters.Parametros.get(self.parametersKey)
			self.parametersList = str(self.parametersList)
			self.parametersList = self.parametersList.split(',')
			self.parametroA = float(self.parametersList[0].strip("[]()' "))
			self.parametroB = float(self.parametersList[1].strip("[]()' "))
			self.parametroC = float(self.parametersList[2].strip("[]()' "))
			self.rangeAcuracia = float(self.parametersList[6].strip("[]()' "))
			self.parametroF = self.getting_f(self.texturaTalhao)
			self.forca_requerida_op = self.forca_requerida(self.parametroA, self.parametroB, self.parametroC, self.parametroF, \
															self.velocidadeOperacao, self.profundidadeOperacao, self.larguraImplemento, \
															self.orgaosImplemento, self.linhasImplemento)
		self.potencia_disp_tdp = (self.potenciaMotor * 0.83) * 0.735499
		self.potencia_req_bt = (self.forca_requerida_op * self.velocidadeOperacao) / 3.6
		self.potencia_req_tdp = self.potencia_req_bt / self.coefTransmissao
		self.TesteResult1 = self.teste_tracao(self.potencia_req_tdp, self.potencia_disp_tdp, self.rangeAcuracia)
		if self.TesteResult1 == True:
			pass
		if self.TesteResult1 == False:
			self.RetornoMensagem = messagebox.askretrycancel(title="Erro", message="O trator não tem potência suficiente para tracionar o implemento nestas condições. \n\n" \
				+ "Potência disponível na TDP: " + str("%.2f" % self.potencia_disp_tdp) + "\n" + "Potência requerida na TDP: " + str("%2.f" % self.potencia_req_tdp) + "\n\n" \
				+ "Todas as estimativas possuem uma variação esperada, você gostaria de tentar resimular?")
			if self.RetornoMensagem == True:
				self.forca_requerida_op = self.forca_requerida_op - (self.forca_requerida_op * (self.rangeAcuracia/100))
				self.potencia_req_bt = (self.forca_requerida_op * self.velocidadeOperacao) / 3.6
				self.potencia_req_tdp = self.potencia_req_bt / self.coefTransmissao
				self.TesteResult2 = self.teste_tracao(self.potencia_req_tdp, self.potencia_disp_tdp, self.rangeAcuracia)
				if self.TesteResult2 == True:
					pass
				if self.TesteResult2 == False:
					messagebox.showerror(title='Erro', message='O trator não traciona o implemento mesmo considerando o cenário mais baixo de força requerida pelo implemento. ' \
						+ "\n\nÉ necessário compabitilizar o trator ou o implemento, alguns métodos são: \n\n" \
						+ "  - Redimensionar o implemento utilizado, diminuindo sua largura de trabalho. \n" \
						+ "  - Reduzir a velocidade e profundidade de operação. \n" \
						+ "  - Utilizar um trator mais potente. \n\n" \
						+ 'Caso você realizou essa operação em campo com sucesso, entre em contato conosco.')
					return
			if self.RetornoMensagem == False:
				self.master.focus_force()
				return	
			
		self.fatorX = self.potencia_req_tdp / self.potencia_disp_tdp
		self.consumoCombEspecifico = self.CalcularConsumoEspecifico(self.fatorX)
		self.consumoCombHora = self.consumoCombEspecifico * self.potencia_req_tdp
		self.consumoOleoHora = 0.000566 * (self.potenciaMotor * 0.735499) + 0.02487
		self.eficiencia_campo = self.n_campo(self.parametersKey, self.velocidadeOperacao)
		self.capCampoTeorica = self.velocidadeOperacao * self.larguraImplemento / 10
		self.capCampoEfetiva = self.velocidadeOperacao * self.larguraImplemento * self.eficiencia_campo / 10
		self.horasTrabalhadas = self.areaTalhao / self.capCampoEfetiva
		self.custoCombustivel = self.consumoCombHora * float(self.precoDiesel.get())
		self.custoOleo = self.consumoOleoHora * float(self.precoOleo.get())
		self.custoTratorista = float(self.precoTratorista.get())
		self.trTrator = self.transmissaoTrator[2]
		self.custoManutencao = self.maintenace(self.trTrator)
		self.custoVariavel = self.custoCombustivel + self.custoOleo + self.custoTratorista + self.custoManutencao
		self.submitButton.config(state=tk.ACTIVE)
		self.CustoFixoTrator()
		self.CustoFixoImplemento()
		self.CustoTotalHorario = self.CustoFixoT + self.CustoFixoImp + self.custoVariavel
		self.CustoTotalHectare = self.CustoTotalHorario/self.capCampoEfetiva
		self.CustoTotal = self.CustoTotalHorario * self.horasTrabalhadas
		self.print_results()

	def CalcularConsumoEspecifico(self,eficiencia_tratoria):
		if eficiencia_tratoria > 0.856:
			self.consumo = 0.411
		else:
			self.raiz = 738 * self.fatorX + 173
			self.consumo = 2.64 * self.fatorX + 3.91 - 0.203 * math.sqrt(self.raiz)
		return self.consumo

	def maintenace(self, tr):
		if tr == '2':
			self.RF1 = 0.007
			self.RF2 = 2
		elif tr == '4': 
			self.RF1 = 0.003
			self.RF2 = 2
		if self.tratorData[3] != '':
			self.precoTrator = float(self.tratorData[4].strip("[]()' "))
			self.horaAno = float(self.tratorData[9].strip("[]()' "))
			self.vidaUtil = float(self.tratorData[8].strip("[]()' "))
		self.manutencaoHora = ((self.RF1*math.pow(self.vidaUtil*self.horaAno/1000,2))*self.precoTrator)/(self.horaAno * self.vidaUtil)
		return self.manutencaoHora

	def searchDB(self, id, table):
		self.conn = sqlite3.connect('database.db')
		self.c = self.conn.cursor()
		self.c.execute("SELECT * FROM '"+table+"' WHERE id LIKE '%"+str(id)+"%'")
		self.data = self.c.fetchall()
		self.conn.commit()
		self.conn.close()
		return self.data

	def getting_f(self, textura):
		if textura == 'Argilosa':
			self.parametroF = float(self.parametersList[3].strip("[]()' "))
		elif textura == 'Média':
			self.parametroF = float(self.parametersList[4].strip("[]()' "))
		elif textura == 'Arenosa':
			self.parametroF = float(self.parametersList[5].strip("[]()' "))
		return self.parametroF

	def forca_requerida(self, a, b, c, f, v, p, larg, o, linhas):
		if o == 'None' and linhas == 'None':
			self.forca_requerida_op = f*(a+b*v+c*(v*v))*larg*p
		elif o == 'None' and linhas != 'None':
			self.forca_requerida_op = f*(a+b*v+c*(v*v))*float(linhas)*p
		elif o != 'None' and linhas == 'None':
			self.forca_requerida_op = f*(a+b*v+c*(v*v))*float(o)*p
		return self.forca_requerida_op/1000

	def n_campo(self, key, vel):
		self.eficienceList = parameters.Eficiencia.get(key)
		self.eficienceList = str(self.eficienceList)
		self.eficienceList = self.eficienceList.split(',')
		self.nmin = float(self.eficienceList[0].strip("[]()' "))
		self.nmax = float(self.eficienceList[1].strip("[]()' "))
		self.vmin = float(self.eficienceList[2].strip("[]()' "))
		self.vmax = float(self.eficienceList[3].strip("[]()' "))
		self.nvariation = self.nmax - self.nmin
		self.vvariation = self.vmax - self.vmin
		if vel > self.vmax:
			self.ncampo = self.nmax
		elif vel < self.vmin:
			self.ncampo = self.nmin
		else:
			self.ncampo = ((vel - self.vmin) * self.nvariation) / self.vvariation + self.nmin
		return self.ncampo/100

	def print_results(self):
		self.outputsPage = tk.Toplevel(self.master)
		self.app = outputs.OutputsPage(self.outputsPage)
		self.app.IDTalhao = self.idTalhao
		self.app.NomeTalhao = self.nomeTalhao
		self.app.NomeTalhaoVar.set(self.nomeTalhao)
		self.app.AreaTalhao = self.areaTalhao
		self.app.AreaTalhaoVar.set(self.areaTalhao)
		self.app.TexturaTalhao = self.texturaTalhao
		self.app.TexturaTalhaoVar.set(self.texturaTalhao)
		self.app.IDTrator = self.idTrator
		self.app.NomeTrator = self.nomeTrator
		self.app.NomeTratorVar.set(self.nomeTrator)
		self.app.TransmissaoTrator = self.transmissaoTrator
		self.app.TransmissaoTratorVar.set(self.transmissaoTrator)
		self.app.PotenciaTrator = self.potenciaMotor
		self.app.PotenciaTratorVar.set(self.potenciaMotor)
		self.app.IDImplemento = self.idImplemento
		self.app.NomeImplemento = self.nomeImplemento
		self.app.NomeImplementoVar.set(self.nomeImplemento)
		self.app.TipoImplemento = self.tipoImplemento
		self.app.TipoImplementoVar.set(self.tipoImplemento)
		self.app.LarguraImplemento = self.larguraImplemento
		self.app.LarguraImplementoVar.set(self.larguraImplemento)
		self.app.OrgaoImplemento = self.orgaosImplemento
		self.app.OrgaoImplementoVar.set(self.orgaosImplemento)
		self.app.LinhaImplemento = self.linhasImplemento
		self.app.LinhaImplementoVar.set(self.linhasImplemento)
		self.app.VelocidadeOperacao = self.velocidadeOperacao
		self.app.VelocidadeOperacaoVar.set(self.velocidadeOperacao)
		self.app.ProfundidadeOperacao = self.profundidadeOperacao
		self.app.ProfundidadeOperacaoVar.set(self.profundidadeOperacao)
		self.app.PassadaOperacao = self.passadaOperacao
		self.app.PassadaOperacaoVar.set(self.passadaOperacao)
		self.app.CondicaoSolo = str(self.condicaoSolo.get())
		self.app.CondicaoSoloVar.set(str(self.condicaoSolo.get()))
		self.app.PrecoCombustivel = float(self.precoDiesel.get())
		self.app.PrecoCombustivelVar.set(float(self.precoDiesel.get()))
		self.app.PrecoOleo = float(self.precoOleo.get())
		self.app.PrecoOleoVar.set(float(self.precoOleo.get()))
		self.app.PrecoTratorista = float(self.precoTratorista.get())
		self.app.PrecoTratoristaVar.set(float(self.precoTratorista.get()))
		self.app.EficienciaCampo = self.eficiencia_campo
		self.app.EficienciaCampoVar.set(str("%.2f" % self.eficiencia_campo))
		self.app.CapacidadeCampoTeorica = self.capCampoTeorica
		self.app.CapacidadeCampoTeoricaVar.set(str("%.2f" % self.capCampoTeorica))
		self.app.CapacidadeCampoEfetiva = self.capCampoEfetiva
		self.app.CapacidadeCampoEfetivaVar.set(str("%.2f" % self.capCampoEfetiva))
		self.app.TempoGasto = self.horasTrabalhadas
		self.app.TempoGastoVar.set(str("%.2f" % self.horasTrabalhadas))
		self.app.ConsumoCombEspec =self.consumoCombEspecifico
		self.app.ConsumoCombEspecVar.set(str("%.4f" % self.consumoCombEspecifico))
		self.app.ConsumoCombHora = self.consumoCombHora
		self.app.ConsumoCombHoraVar.set(str("%.4f" % self.consumoCombHora))
		self.app.DepreciacaoTrator = self.DepreciacaoTrator
		self.app.DepreciacaoTratorVar.set(str("%.2f" % self.DepreciacaoTrator))
		self.app.JuroTrator = self.JurosTrator
		self.app.JuroTratorVar.set(str("%.2f" % self.JurosTrator))
		self.app.GaragemTrator = self.GaragemTrator
		self.app.GaragemTratorVar.set(str("%.2f" % self.GaragemTrator))
		self.app.SeguroTrator = self.SeguroTrator
		self.app.SeguroTratorVar.set(str("%.2f" % self.SeguroTrator))
		self.app.CustoFixoTrator = self.CustoFixoT
		self.app.CustoFixoTratorVar.set(str("%.2f" % self.CustoFixoT))
		self.app.DepreciacaoImplemento = self.DepreciacaoImplemento
		self.app.DepreciacaoImplementoVar.set(str("%.2f" % self.DepreciacaoImplemento))
		self.app.JuroImplemento = self.JurosImplemento
		self.app.JuroImplementoVar.set(str("%.2f" % self.JurosImplemento))
		self.app.GaragemImplemento = self.GaragemImplemento
		self.app.GaragemImplementoVar.set(str("%.2f" % self.GaragemImplemento))
		self.app.SeguroImplemento = self.SeguroImplemento
		self.app.SeguroImplementoVar.set(str("%.2f" % self.SeguroImplemento))
		self.app.CustoFixoImplemento = self.CustoFixoImp
		self.app.CustoFixoImplementoVar.set(str("%.2f" % self.CustoFixoImp))
		self.app.CustoCombHora = self.custoCombustivel
		self.app.CustoCombHoraVar.set(str("%.2f" % self.custoCombustivel))
		self.app.CustoOleoHora = self.custoOleo
		self.app.CustoOleoHoraVar.set(str("%.2f" % self.custoOleo))
		self.app.CustoManutencaoHoraTrator = self.custoManutencao
		self.app.CustoManutencaoHoraTratorVar.set(str("%.2f" % self.custoManutencao))
		self.app.CustoOperacional = self.custoVariavel
		self.app.CustoOperacionalVar.set(str("%.2f" % self.custoVariavel))
		self.app.CustoTotalHorario = self.CustoTotalHorario
		self.app.CustoTotalHorarioVar.set(str("%.2f" % self.CustoTotalHorario))
		self.app.CustoTotalHectare = self.CustoTotalHectare
		self.app.CustoTotalHectareVar.set(str("%.2f" % self.CustoTotalHectare))
		self.app.CustoTotal = self.CustoTotal
		self.app.CustoTotalVar.set(str("%.2f" % self.CustoTotal))
		self.app.CoeficienteTransmissao = self.coefTransmissao
		if self.tipoImplemento == 'Arado de discos':
			self.app.ParametroC = 0.0
			self.app.ParametroF = 0.0
		else:
			self.app.ParametroC = self.parametroC
			self.app.ParametroF = self.parametroF
		self.app.ParametroA = self.parametroA
		self.app.ParametroB =  self.parametroB
		self.app.ForcaReqImplemento = self.forca_requerida_op
		self.app.PotenciaReqImplementoBT = self.potencia_req_bt
		self.app.PotenciaReqImplementoTDP = self.potencia_req_tdp
		self.app.PotenciaDispTratorTDP = self.potencia_disp_tdp
		self.app.FatorX = self.fatorX
		self.app.ValorCompraTrator = self.ValorCompraTrator
		self.app.TaxaJurosTrator = self.ValorJuroTrator
		self.app.TaxaGaragemTrator = self.ValorGaragemTrator
		self.app.TaxaSeguroTrator = self.ValorSeguroTrator
		self.app.VidaUtilHoraTrator = self.VidaUtilTrator * self.HoraAnoTrator
		self.app.ValorCompraImplemento = self.ValorCompraImplemento
		self.app.TaxaJurosImplemento = self.ValorJuroImplemento
		self.app.TaxaGaragemImplemento = self.ValorGaragemImplemento
		self.app.TaxaSeguroImplemento = self.ValorSeguroImplemento
		self.app.VidaUtilHoraImplemento = self.VidaUtilImplemento * self.HoraAnoImplemento
		self.app.EficienciaCampoMinima = self.nmin
		self.app.EficienciaCampoMaxima = self.nmax

		

	def teste_tracao(self, pot_req, pot_disp, variacao):
		
		safe_pot_req = pot_req + (0.1 * pot_req)
		if safe_pot_req >= pot_disp:
			return False
		else:
			return True

	def update_trv(self):
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		query = "SELECT * FROM operacao"
		c.execute(query)
		row = c.fetchall()
		self.trv_hist.delete(*self.trv_hist.get_children())
		for i in row:
			self.trv_hist.insert('', "end", values=i)
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão

	def view_simulation(self, event):
		self.trv_selection = self.trv_hist.item(self.trv_hist.focus())
		self.id_talhao = self.trv_selection['values'][1]
		self.id_trator = self.trv_selection['values'][2]
		self.id_implemento = self.trv_selection['values'][3]
		for i in self.trv_trator.get_children():
			self.id_trv_trator = self.trv_trator.item(i)['values'][0]
			if self.id_trv_trator == self.id_trator:
				self.trv_trator.selection_set(i)
				self.trv_trator.focus(i)
				pass
		for i in self.trv_talhao.get_children():
			self.id_trv_talhao = self.trv_talhao.item(i)['values'][0]
			if self.id_trv_talhao == self.id_talhao:
				self.trv_talhao.selection_set(i)
				self.trv_talhao.focus(i)
				pass
		for i in self.trv_implemento.get_children():
			self.id_trv_implemento = self.trv_implemento.item(i)['values'][0]
			if self.id_trv_implemento == self.id_implemento:
				self.trv_implemento.selection_set(i)
				self.trv_implemento.focus(i)
				pass
		self.velocidade.delete(0, tk.END)
		self.profundidade.delete(0, tk.END)
		self.condicaoSolo.delete(0, tk.END)
		self.passada.delete(0, tk.END)
		self.precoDiesel.delete(0, tk.END)
		self.precoOleo.delete(0, tk.END)
		self.precoTratorista.delete(0, tk.END)
		self.item = self.trv_hist.item(self.trv_hist.focus())
		self.velocidade.insert(0, self.item['values'][7])
		self.profundidade.insert(0, self.item['values'][8])
		self.condicaoSolo.set(self.item['values'][9])
		self.passada.set(self.item['values'][10])
		self.precoDiesel.insert(0, self.item['values'][11])
		self.precoOleo.insert(0, self.item['values'][12])
		self.precoTratorista.insert(0, self.item['values'][13])
		self.simulate()

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
		self.c.execute(self.values_db, (self.idTalhao, self.idTrator, self.idImplemento, self.nomeTalhao, self.nomeTrator, self.nomeImplemento, \
			self.velocidadeOperacao, self.profundidadeOperacao, self.soloOperacao, self.passadaOperacao, self.precoDiesel.get(), self.precoOleo.get(), \
			self.precoTratorista.get())) #Inserindo os valores de entrada na tabela do banco de dados
		self.conn.commit() #Commitando as alterações
		self.conn.close() #Fechando a conexão
		self.update_trv()

	def CustoFixoTrator(self):
		self.conn = sqlite3.connect('database.db')
		self.c = self.conn.cursor()
		self.c.execute("SELECT * FROM trator WHERE id LIKE '%"+str(self.idTrator)+"%'")
		self.data = self.c.fetchall()
		self.data = str(self.data)
		self.data = self.data.split(',')
		self.ValorCompraTrator = float(self.data[4].strip(' '))
		self.ValorJuroTrator = float(self.data[5].strip(' '))
		self.ValorSeguroTrator = float(self.data[6].strip(' '))
		self.ValorGaragemTrator = float(self.data[7].strip(' '))
		self.VidaUtilTrator = float(self.data[8].strip(' '))
		self.HoraAnoTrator = float(self.data[9].strip("[]() '"))
		self.DepreciacaoTrator = (self.ValorCompraTrator - (self.ValorCompraTrator * 0.1))/(self.VidaUtilTrator * self.HoraAnoTrator)
		self.Ano=1
		self.ValorInicial = self.ValorCompraTrator
		self.JuroTotal = 0
		while self.Ano<=self.VidaUtilTrator:
			self.ValorFinal = self.ValorInicial-((self.DepreciacaoTrator*self.HoraAnoTrator))
			self.JuroAnual = ((self.ValorInicial+self.ValorFinal)/2) * (self.ValorJuroTrator/100)
			self.JuroTotal = self.JuroTotal + self.JuroAnual
			self.ValorInicial = self.ValorFinal
			self.Ano = self.Ano + 1
		self.JurosTrator = self.JuroTotal/(self.VidaUtilTrator*self.HoraAnoTrator)
		self.GaragemTrator = ((self.ValorGaragemTrator / 100) * self.ValorCompraTrator)/(self.VidaUtilTrator * self.HoraAnoTrator)
		self.SeguroTrator = ((self.ValorSeguroTrator / 100) * self.ValorCompraTrator)/(self.VidaUtilTrator * self.HoraAnoTrator)
		self.CustoFixoT = self.DepreciacaoTrator + self.JurosTrator + self.GaragemTrator + self.SeguroTrator
		self.conn.commit()
		self.conn.close()

	def CustoFixoImplemento(self):
		self.conn = sqlite3.connect('database.db')
		self.c = self.conn.cursor()
		self.c.execute("SELECT * FROM implemento WHERE id LIKE '%"+str(self.idImplemento)+"%'")
		self.data = self.c.fetchall()
		self.data = str(self.data)
		self.data = self.data.split(',')
		self.ValorCompraImplemento = float(self.data[6].strip(' '))
		self.ValorJuroImplemento = float(self.data[7].strip(' '))
		self.ValorSeguroImplemento = float(self.data[8].strip(' '))
		self.ValorGaragemImplemento = float(self.data[9].strip(' '))
		self.VidaUtilImplemento = float(self.data[10].strip(' '))
		self.HoraAnoImplemento = float(self.data[11].strip("[]() '"))
		self.DepreciacaoImplemento = (self.ValorCompraImplemento - (self.ValorCompraImplemento * 0.1))/(self.VidaUtilImplemento * self.HoraAnoImplemento)
		self.Ano = 1
		self.ValorInicial = self.ValorCompraImplemento
		self.JuroTotal = 0
		while self.Ano<=self.VidaUtilImplemento:
			self.ValorFinal = self.ValorInicial-((self.DepreciacaoImplemento*self.HoraAnoImplemento))
			self.JuroAnual = ((self.ValorInicial+self.ValorFinal)/2) * (self.ValorJuroImplemento/100)
			self.JuroTotal = self.JuroTotal + self.JuroAnual
			self.ValorInicial = self.ValorFinal
			self.Ano = self.Ano + 1
		self.JurosImplemento = self.JuroTotal/(self.VidaUtilImplemento*self.HoraAnoImplemento)
		self.GaragemImplemento = ((self.ValorGaragemImplemento / 100) * self.ValorCompraImplemento)/(self.VidaUtilImplemento * self.HoraAnoImplemento)
		self.SeguroImplemento = ((self.ValorSeguroImplemento / 100) * self.ValorCompraImplemento)/(self.VidaUtilImplemento * self.HoraAnoImplemento)
		self.CustoFixoImp = self.DepreciacaoImplemento + self.JurosImplemento + self.GaragemImplemento + self.SeguroImplemento
		self.conn.commit()
		self.conn.close()