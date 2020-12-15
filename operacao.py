import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, re, parameters, math, outputs

class OperacaoPage():
	def __init__(self, master):
		self.master = master
		self.master.title('Simulação de operação agrícola')
		self.frame_inputs = tk.Frame(self.master)
		self.frame_buttons = tk.Frame(self.master)
		self.frame_hist = tk.Frame(self.master)
		self.frame_inputs.grid()
		self.frame_buttons.grid()
		self.frame_hist.grid()
		self.trv_implemento_label = tk.Label(self.frame_inputs, text='Dê um clique duplo no implemento que deseja simular a operação').grid(row=0, column=2)
		self.trv_trator = tk.ttk.Treeview(self.frame_inputs, columns=(1,2,3), show="headings", height='3', selectmode='browse', displaycolumns=('2','3'))
		self.trv_talhao = tk.ttk.Treeview(self.frame_inputs, columns=(1,2,3), show="headings", height='3', selectmode='browse', displaycolumns=('2','3'))
		self.trv_implemento = tk.ttk.Treeview(self.frame_inputs, columns=(1,2,3), show="headings", height='3', selectmode='browse', displaycolumns=('2','3'))
		self.trv_talhao.grid(row=1, column=0, padx=3, pady=3)
		self.trv_trator.column('2', width=20, minwidth=50)
		self.trv_trator.heading(2, text='Nome')
		self.trv_trator.heading(3, text='Potência (cv)')
		self.trv_talhao.heading(2, text='Nome')
		self.trv_talhao.heading(3, text='Área (ha)')
		self.trv_implemento.heading(2, text='Nome')
		self.trv_implemento.heading(3, text='Tipo')
		self.trv_trator.grid(row=1, column=1, padx=2, pady=3)
		self.trv_implemento.grid(row=1, column=2, padx=3, pady=3)
		self.trv_implemento.bind('<Double 1>', self.callback)
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
		self.profundidadeLabel = tk.Label(self.frame_inputs,text='Profundidade de operação (cm):')
		self.simulateButton = tk.Button(self.frame_buttons, text='Simular operação', command=self.simulate)
		self.simulateButton.grid(row=0, column=0, padx=3, pady=7)
		self.quitButton = tk.Button(self.frame_buttons, text='Voltar', command=self.master.destroy)
		self.submitButton = tk.Button(self.frame_buttons, text='Salvar simulação', command=self.submitDB)
		self.submitButton.grid(row=0, column=1, padx=2, pady=7)
		self.quitButton.grid(row=0, column=2, padx=3, pady=7)
		self.trv_hist = tk.ttk.Treeview(self.frame_hist, columns=(1,2,3,4,5,6,7,8,9,10,11), show='headings', height='3', selectmode='browse', displaycolumns=('5','6','7','8','9','10','11'))
		self.trv_hist.heading(5, text='Nome do talhão')
		self.trv_hist.heading(6, text='Nome do trator')
		self.trv_hist.heading(7, text='Nome do implemento')
		self.trv_hist.heading(8, text='Velocidade')
		self.trv_hist.heading(9, text='Profundidade')
		self.trv_hist.heading(10, text='Superficie')
		self.trv_hist.heading(11, text='Passada')
		self.trv_hist.grid(padx=3, pady=3)
		self.trv_hist.bind('<Double 1>', self.view_simulation)
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
		self.transmissaoTrator =self.transmissaoTrator.replace(" ","")
		self.tipoImplemento = str(self.implementoData[2].strip(" '"))
		self.larguraImplemento = float(self.implementoData[3].strip(' '))
		self.orgaosImplemento = self.implementoData[4].strip(' ')
		self.linhasImplemento = self.implementoData[5].strip(' ')
		self.velocidadeOperacao = float(self.velocidade.get())
		self.profundidadeOperacao = float(self.profundidade.get())
		if self.profundidadeOperacao == '':
			self.profundidadeOperacao = 1
		self.passadaOperacao = str(self.passada.get())
		self.soloOperacao = str(self.condicaoSolo.get())
		self.rTranmissaoKey = self.transmissaoTrator + self.soloOperacao
		self.coefTransmissao = parameters.relacaoTransmissao.get(self.rTranmissaoKey)
		if self.tipoImplemento == 'Arado de discos':
			self.parametersKey = 'Aradodediscos'
			self.parametersList = parameters.Parametros.get(self.parametersKey)
			self.parametersList = str(self.parametersList)
			self.parametersList = self.parametersList.split(',')
			if self.texturaTalhao == 'Argilosa':
				self.parametroA = float(self.parametersList[4].strip("[]()' "))
				self.parametroB = float(self.parametersList[5].strip("[]()' "))
			elif self.texturaTalhao == 'Média':
				self.parametroA = float(self.parametersList[4].strip("[]()' "))
				self.parametroB = float(self.parametersList[5].strip("[]()' "))
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
		self.potencia_req_bt = (self.forca_requerida_op * self.velocidadeOperacao) / 3.6
		self.potencia_req_tdp = self.potencia_req_bt / self.coefTransmissao
		self.potencia_disp_tdp = (self.potenciaMotor * 0.83) * 0.735499
		self.teste_tracao(self.potencia_req_tdp, self.potencia_disp_tdp)
		self.fatorX = self.potencia_req_tdp / self.potencia_disp_tdp
		self.raiz = 738 * self.fatorX + 173
		self.consumoCombEspecifico = 2.64 * self.fatorX + 3.91 - 0.203 * math.sqrt(self.raiz)
		self.consumoCombHora = self.consumoCombEspecifico * self.potencia_req_tdp
		self.consumoOleoHora = 0.000566 * (self.potenciaMotor * 0.735499) + 0.02487
		self.eficiencia_campo = self.n_campo(self.parametersKey, self.velocidadeOperacao)
		self.capCampoTeorica = self.velocidadeOperacao * self.larguraImplemento / 10
		self.capCampoEfetiva = self.velocidadeOperacao * self.larguraImplemento * self.eficiencia_campo / 10
		self.horasTrabalhadas = self.areaTalhao / self.capCampoEfetiva
		self.print_results()
		

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
		self.app.areaLabel.config(text='Área do talhão (ha): ' + str("%.2f" % self.areaTalhao))
		self.app.texturaLabel.config(text='Textura do solo: ' + str(self.texturaTalhao))
		self.app.transmissaoLabel.config(text='Tipo de transmissão: ' + str(self.transmissaoTrator))
		self.app.potenciaLabel.config(text='Potência nominal (cv): ' + str(self.potenciaMotor))
		self.app.implementoLabel.config(text= 'Tipo de implemento: ' + str(self.tipoImplemento))
		self.app.larguraLabel.config(text= 'Largura de operação (m): ' + str(self.larguraImplemento))
		self.app.orgaoLabel.config(text= 'Número de órgãos ativos: ' + str(self.orgaosImplemento))
		self.app.linhasLabel.config(text= 'Número de linhas: ' + str(self.linhasImplemento))
		self.app.velLabel.config(text= 'Velocidade da operação (km/h): ' + str(self.velocidadeOperacao))
		self.app.profLabel.config(text= 'Profundidade da operação (cm): ' + str(self.profundidadeOperacao))
		self.app.passadaLabel.config(text= 'Número da passada: ' + str(self.passadaOperacao))
		self.app.condSoloLabel.config(text= 'Superfície do solo:' + str(self.soloOperacao))
		self.app.coefTransLabel.config(text= 'Coeficiente de transmissão: ' + str(self.coefTransmissao))
		if self.tipoImplemento == 'Arado de discos':
			self.app.parCLabel.config(text= 'Parâmetro C: None')
			self.app.parFLabel.config(text= 'Parâmetro F: None')
			self.app.rangeLabel.config(text= 'Variação esperada -+ (%): None')
		else:
			self.app.parCLabel.config(text= 'Parâmetro C: ' + str(self.parametroC))
			self.app.parFLabel.config(text= 'Parâmetro F: ' + str(self.parametroF))
			self.app.rangeLabel.config(text= 'Variação esperada -+ (%): ' + str(self.rangeAcuracia))
		self.app.parALabel.config(text= 'Parâmetro A: ' + str(self.parametroA))
		self.app.parBLabel.config(text= 'Parâmetro B: ' + str(self.parametroB))
		self.app.forcareqLabel.config(text= 'Força requerida na operação (kN): ' + str("%.2f" % self.forca_requerida_op))
		self.app.potreqBTLabel.config(text= 'Potência requerida na Barra de Tração (kW): ' + str("%.2f" % self.potencia_req_bt))
		self.app.potreqTDPLabel.config(text= 'Potência requerida na Tomada de Potência (kW): ' + str("%.2f" % self.potencia_req_tdp))
		self.app.potdispTDPLabel.config(text= 'Potência disponível na Tomada de Potência (kW): ' + str("%.2f" % self.potencia_disp_tdp))
		self.app.fatorxLabel.config(text= 'Fator X: ' + str(self.fatorX))
		self.app.combEspLabel.config(text= 'Consumo de combustível específico (L/kWh): ' + str("%.2f" % self.consumoCombEspecifico))
		self.app.combHoraLabel.config(text= 'Consumo de combustível por hora (L/h): ' + str("%.2f" % self.consumoCombHora))
		self.app.eficCampoLabel.config(text= 'Eficiência de campo (decimal): ' + str("%.2f" % self.eficiencia_campo))
		self.app.capCampoTLabel.config(text= 'Capacidade de campo teórica (ha/h): ' + str("%.2f" % self.capCampoTeorica))
		self.app.capCampoELabel.config(text= 'Capacidade de campo efetiva (ha/h): ' + str("%.2f" % self.capCampoEfetiva))
		self.app.tempoLabel.config(text= 'Tempo total de operação (horas): ' + str("%.2f" % self.horasTrabalhadas))

	def teste_tracao(self, pot_req, pot_disp):
		pot_req += (0.1 * pot_req)
		if pot_req >= pot_disp:
			messagebox.showerror(title=None, message="O trator não tem potência suficiente para tracionar este implemento nestas condições. \
				É necessário mudar o trator ou implemento, ou ainda diminuir a velocidade ou profundidade de operação. A potência disponível \
				na TDP é " + str("%.3f" % pot_disp) + ". Enquanto a potência requerida pela operação é " + str("%.3f" % pot_req))
		else:
			pass

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
		self.id_talhao = self.trv_selection['values'][0]
		self.id_trator = self.trv_selection['values'][1]
		self.id_implemento = self.trv_selection['values'][2]
		for i in self.trv_trator.get_children():
			self.id = self.trv_trator.item(i)['values'][0]
			if self.id == self.id_trator:
				self.trv_trator.selection_set(i)
				self.trv_trator.focus(i)
		for i in self.trv_talhao.get_children():
			self.id = self.trv_talhao.item(i)['values'][0]
			if self.id == self.id_talhao:
				self.trv_talhao.selection_set(i)
				self.trv_talhao.focus(i)
		for i in self.trv_implemento.get_children():
			self.id = self.trv_implemento.item(i)['values'][0]
			if self.id == self.id_implemento:
				self.trv_implemento.selection_set(i)
				self.trv_implemento.focus(i)
		self.velocidade.delete(0, tk.END)
		self.profundidade.delete(0, tk.END)
		self.condicaoSolo.delete(0, tk.END)
		self.passada.delete(0, tk.END)
		self.item = self.trv_hist.item(self.trv_hist.focus())
		self.velocidade.insert(0, self.item['values'][7])
		self.profundidade.insert(0, self.item['values'][8])
		self.condicaoSolo.set(self.item['values'][9])
		self.passada.set(self.item['values'][10])
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
									 passada TEXT)""")
		self.values_db = "INSERT INTO operacao(talhao, trator, implemento, nome_talhao, nome_trator, nome_implemento, velocidade, profundidade, superficie, passada) VALUES (?,?,?,?,?,?,?,?,?,?)" #Atribuindo a variavel a sintaxe SQLITE3
		self.c.execute(self.values_db, (self.idTalhao, self.idTrator, self.idImplemento, self.nomeTalhao, self.nomeTrator, self.nomeImplemento, \
			self.velocidadeOperacao, self.profundidadeOperacao, self.soloOperacao, self.passadaOperacao)) #Inserindo os valores de entrada na tabela do banco de dados
		self.conn.commit() #Commitando as alterações
		self.conn.close() #Fechando a conexão
		self.update_trv()