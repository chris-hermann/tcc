import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk
import tkinter.font as tkFont

class ImplementoPage:
	def __init__(self, master):
		self.master = master
		self.master.title('Implementos')

		#GUI dos inputs
		self.frame_inputs = tk.Frame(self.master)
		self.implemento = tk.ttk.Combobox(self.frame_inputs, width=50, values=['',
																	'Arado de aivecas',
																	'Arado de discos',
																	'Subsolador - ponteira simples',
																	'Subsolador - ponteira com asas',
																	'Grade de discos - ação dupla em X - Tandem',
																	'Grade de discos - ação dupla em V - Offset',
																	'Grade de discos - ação simples',
																	'Cultivador de campo',
																	'Sulcador',
																	'Semeadora montada (sementes graúdas)',
																	'Semeadora de arrasto (sementes graúdas)',
																	'Semeadora de arrasto - adubadora - pulverizadora (sementes graúdas)',
																	'Semeadora montada (sementes miúdas)',
																	'Semeadora de arrasto (sementes miúdas)'])
		self.nome = tk.Entry(self.frame_inputs)
		self.valorCompra = tk.Entry(self.frame_inputs)
		self.valorJuro = tk.Entry(self.frame_inputs)
		self.valorSeguro = tk.Entry(self.frame_inputs)
		self.valorGaragem = tk.Entry(self.frame_inputs)
		self.horaAno = tk.Entry(self.frame_inputs)
		self.vidaUtil = tk.Entry(self.frame_inputs)
		self.implementoLabel = tk.Label(self.frame_inputs, text='Tipo de Implemento:').grid(row=0, column=0)
		self.nomeLabel = tk.Label(self.frame_inputs, text='Nome:').grid(row=1, column=0)
		self.compralabel = tk.Label(self.frame_inputs, text = 'Valor de compra (R$): ').grid(row=4, column=0)
		self.jurolabel = tk.Label(self.frame_inputs, text = 'Juros sobre o capital (%): ').grid(row=5, column=0)
		self.segurolabel = tk.Label(self.frame_inputs, text = 'Taxa de seguro (%): ').grid(row=6, column=0)
		self.garagemlabel = tk.Label(self.frame_inputs, text = 'Taxa de garagem (%): ').grid(row=7, column=0)
		self.horaAnolabel = tk.Label(self.frame_inputs, text = 'Horas trabalhadas por ano: ').grid(row=8, column=0)
		self.vidaUtillabel = tk.Label(self.frame_inputs, text = 'Vida Útil (anos): ').grid(row=9, column=0)
		self.implemento.grid(row=0, column=1)
		self.nome.grid(row=1, column=1)
		self.valorCompra.grid(row=4, column=1)
		self.valorJuro.grid(row=5, column=1)
		self.valorSeguro.grid(row=6, column=1)
		self.valorGaragem.grid(row=7, column=1)
		self.horaAno.grid(row=8, column=1)
		self.vidaUtil.grid(row=9, column=1)
		self.frame_inputs.grid()
		self.distancia = tk.Entry(self.frame_inputs)
		self.largura = tk.Entry(self.frame_inputs)
		self.orgaos = tk.Entry(self.frame_inputs)
		self.linhas = tk.Entry(self.frame_inputs)
		self.linhasLabel = tk.Label(self.frame_inputs, text = 'Número de linhas:')		
		self.larguraLabel = tk.Label(self.frame_inputs, text = 'Largura de operação (m):')
		self.orgaosLabel = tk.Label(self.frame_inputs, text = 'Número de órgãos ativos:')
		self.distanciaLabel = tk.Label(self.frame_inputs, text = 'Distância entre órgãos/linhas (m):')

		#self.spacer = tk.Entry(self.frame_inputs, width=50).grid(row=2, column=0, columnspan=2)

		#GUI dos botões#
		self.frame_buttons = tk.Frame(self.master)
		self.quitButton = tk.Button(self.frame_buttons, text = 'Voltar', width = 25, command = self.close_windows)
		self.submitButton = tk.Button(self.frame_buttons, text = 'Inserir', width =25, command = self.submit)
		self.updateButton = tk.Button(self.frame_buttons, text = 'Atualizar', width =25, command = self.update_db)
		self.cleanButton = tk.Button(self.frame_buttons, text = 'Limpar', width =25, command = self.clean)
		self.deleteButton = tk.Button(self.frame_buttons, text = 'Deletar', width =25, command = self.delete)
		self.submitButton.pack()
		self.updateButton.pack()
		self.cleanButton.pack()
		self.deleteButton.pack()
		self.quitButton.pack()
		self.frame_buttons.grid()
		self.implemento.bind('<<ComboboxSelected>>', self.callback)

		self.frame_trv = tk.Frame(self.master)
		self.frame_trv.grid()
		self.spacelabel1 = tk.Label(self.frame_trv).grid()
		self.titlefont = tkFont.Font(family='Helvetica', size=22, weight='bold')
		self.trvLabel = tk.Label(self.frame_trv, text='Histórico', font=self.titlefont, anchor = tk.W).grid()
		self.trvHelper = tk.Label(self.frame_trv, text='Dê um clique duplo em algum item do histórico para editar os valores de entrada').grid()
		self.trv_hist = tk.ttk.Treeview(self.frame_trv, columns=(1,2,3,4,5,6,7,8,9,10,11,12), show="headings", height='9')
		self.trv_hist.grid(row=7, column=0, columnspan=3, ipadx=150, pady=10)
		self.trv_hist.heading(1, text="ID")
		self.trv_hist.heading(2, text="Nome")
		self.trv_hist.heading(3, text="Tipo")
		self.trv_hist.heading(4, text="Largura (m)")
		self.trv_hist.heading(5, text="Nº de órgãos")
		self.trv_hist.heading(6, text="Nº de linhas")
		self.trv_hist.heading(7, text="Valor de compra (R$)")
		self.trv_hist.heading(8, text="Juros")
		self.trv_hist.heading(9, text="Seguro")
		self.trv_hist.heading(10, text="Garagem")
		self.trv_hist.heading(11, text="Horas Ano")
		self.trv_hist.heading(12, text="Vida Util")
		self.trv_hist.column('1', width=20, minwidth=80)
		self.trv_hist.column('2', width=40, minwidth=80)
		self.trv_hist.column('3', width=40, minwidth=80)
		self.trv_hist.column('4', width=20, minwidth=80)
		self.trv_hist.column('5', width=20, minwidth=80)
		self.trv_hist.column('6', width=20, minwidth=80)
		self.trv_hist.column('7', width=20, minwidth=115)
		self.trv_hist.column('8', width=20, minwidth=80)
		self.trv_hist.column('9', width=20, minwidth=80)
		self.trv_hist.column('10', width=20, minwidth=80)
		self.trv_hist.column('11', width=20, minwidth=80)
		self.trv_hist.column('12', width=20, minwidth=80)
		self.update_trv()
		#self.#historico = Listbox(windowip, selectmode=SINGLE, xscrollcommand=scrollbarx.set)
		self.scrollbarx = tk.Scrollbar(self.frame_trv, orient=tk.HORIZONTAL, command=self.trv_hist.xview)
		self.trv_hist.configure(xscrollcommand=self.scrollbarx.set)
		#self.#historico.grid(row=0, rowspan=6, column=3, ipadx=70, ipady=150, pady=10)
		self.scrollbarx.grid(row=7, column=0, columnspan=3, sticky=tk.E+tk.W+tk.S)
		self.trv_hist.bind('<Double 1>', self.getrow)

	def close_windows(self):
		self.master.destroy()

	def submit(self):
		conn = sqlite3.connect('database.db') #Criando ou conectando ao banco de dados
		c = conn.cursor() #Configurando o cursor para navegar no banco de dados
		#Cria uma tabela no banco de dados se já nao existir
		c.execute("""CREATE TABLE IF NOT EXISTS implemento( 
								 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
								 nome TEXT NOT NULL,
								 tipo TEXT NOT NULL,
								 larg REAL NOT NULL,
								 org INTEGER,
								 linhas INTEGER,
								 compra REAL,
								 imposto REAL,
								 seg REAL,
								 gar REAL,
								 vu INTEGER,
								 hora INTEGER)""")
		#Rotina para inserir os valores no banco de dados dependendo do tipo de implemento
		if self.implemento.get() == '' or self.nome.get() == '':
			messagebox.showerror(title=None, message="Favor preencha todos os campos!") 
		elif self.implemento.get() == 'Arado de aivecas' or self.implemento.get() == 'Arado de discos' or self.implemento.get() == 'Grade de discos - ação dupla em X - Tandem' \
			 or self.implemento.get() == 'Grade de discos - ação dupla em V - Offset' or self.implemento.get() == 'Grade de disco - ação simples':
			values_db = "INSERT INTO implemento(nome, tipo, larg, compra, imposto, seg, gar, vu, hora) VALUES (?,?,?,?,?,?,?,?,?)"
			c.execute(values_db, (self.nome.get(), self.implemento.get(), self.largura.get(), self.valorCompra.get(), self.valorJuro.get(), self.valorSeguro.get(), \
					self.valorGaragem.get(), self.vidaUtil.get(), self.horaAno.get()))
		elif self.implemento.get() == 'Subsolador - ponteira simples' or self.implemento.get() == 'Subsolador - ponteira com asas' or self.implemento.get() == 'Cultivador de campo':
			mult = float(self.orgaos.get()) * float(self.distancia.get())
			values_db = "INSERT INTO implemento(nome, tipo, larg, org, compra, imposto, seg, gar, vu, hora) VALUES (?,?,?,?,?,?,?,?,?,?)"
			c.execute(values_db, (self.nome.get(), self.implemento.get(), mult, self.orgaos.get(), self.valorCompra.get(), self.valorJuro.get(), self.valorSeguro.get(), \
					self.valorGaragem.get(), self.vidaUtil.get(), self.horaAno.get()))
		elif self.implemento.get() == 'Encanteirador' or self.implemento.get() == 'Semeadora montada (sementes graúdas)' or \
			self.implemento.get() == 'Semeadora de arrasto (sementes graúdas)' or self.implemento.get() == 'Semeadora de arrasto - adubadora - pulverizadora (sementes graúdas)' \
			or self.implemento.get() == 'Semeadora montada (sementes miúdas)' or self.implemento.get() == 'Semeadora de arrasto (sementes miúdas)' :
			mult = float(self.linhas.get()) * float(self.distancia.get())
			values_db = "INSERT INTO implemento(nome, tipo, larg, linhas, compra, imposto, seg, gar, vu, hora) VALUES (?,?,?,?,?,?,?,?,?,?)"
			c.execute(values_db, (self.nome.get(), self.implemento.get(), mult, self.linhas.get(), self.valorCompra.get(), self.valorJuro.get(), self.valorSeguro.get(), \
					self.valorGaragem.get(), self.vidaUtil.get(), self.horaAno.get()))
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão
		self.update_trv()

	def update_db(self):
		conn = sqlite3.connect('database.db') #Criando ou conectando ao banco de dados
		c = conn.cursor() #Configurando o cursor para navegar no banco de dados
		if self.implemento.get() == 'Arado de aivecas' or self.implemento.get() == 'Arado de discos' or self.implemento.get() == 'Grade de discos - ação dupla em X - Tandem' \
			 or self.implemento.get() == 'Grade de discos - ação dupla em V - Offset' or self.implemento.get() == 'Grade de disco, ação simples':
			query = "UPDATE implemento SET nome=?, tipo=?, larg=?, compra=?, imposto=?, seg=?, gar=?, vu=?, hora=? WHERE id=?"
			c.execute(query, (self.nome.get(), self.implemento.get(), self.largura.get(), self.valorCompra.get(), self.valorJuro.get(), self.valorSeguro.get(), \
					self.valorGaragem.get(), self.vidaUtil.get(), self.horaAno.get(), self.id))
		elif self.implemento.get() == 'Subsolador - ponteira simples' or self.implemento.get() == 'Subsolador - ponteira com asas' or self.implemento.get() == 'Cultivador de campo':
			mult = float(self.orgaos.get()) * float(self.distancia.get())
			values_db = "UPDATE implemento SET nome=?, tipo=?, larg=?, org=?, compra=?, imposto=?, seg=?, gar=?, vu=?, hora=? WHERE id=?"
			c.execute(values_db, (self.nome.get(), self.implemento.get(), mult, self.orgaos.get(), self.valorCompra.get(), self.valorJuro.get(), self.valorSeguro.get(), \
					self.valorGaragem.get(), self.vidaUtil.get(), self.horaAno.get(), self.id))
		elif self.implemento.get() == 'Encanteirador' or self.implemento.get() == 'Semeadora montada (sementes graúdas)' or \
			self.implemento.get() == 'Semeadora de arrasto (sementes graúdas)' or self.implemento.get() == 'Semeadora de arrasto - adubadora - pulverizadora (sementes graúdas)' \
			or self.implemento.get() == 'Semeadora montada (sementes miúdas)' or self.implemento.get() == 'Semeadora de arrasto (sementes miúdas)' :
			mult = float(self.linhas.get()) * float(self.distancia.get())
			values_db = "UPDATE implemento SET nome=?, tipo=?, larg=?, linhas=?, compra=?, imposto=?, seg=?, gar=?, vu=?, hora=? WHERE id=?"
			c.execute(values_db, (self.nome.get(), self.implemento.get(), mult, self.linhas.get(), self.valorCompra.get(), self.valorJuro.get(), self.valorSeguro.get(), \
					self.valorGaragem.get(), self.vidaUtil.get(), self.horaAno.get(), self.id))
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão
		self.update_trv()

	def delete(self):
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		selection = self.trv_hist.selection()
		query = "DELETE FROM implemento WHERE id=?"
		c.execute(query, (self.trv_hist.set(selection, "#1"),))
		conn.commit()
		conn.close()
		self.update_trv()

	def clean(self):
		self.nome.delete(0, tk.END)
		self.implemento.set(value='')
		self.largura.delete(0, tk.END)
		self.orgaos.delete(0, tk.END)
		self.linhas.delete(0, tk.END)
		self.distancia.delete(0, tk.END)
		self.valorCompra.delete(0, tk.END)
		self.valorJuro.delete(0, tk.END)
		self.valorSeguro.delete(0, tk.END)
		self.valorGaragem.delete(0, tk.END)
		self.horaAno.delete(0, tk.END)
		self.vidaUtil.delete(0, tk.END)
		self.orgaos.grid_forget()
		self.orgaosLabel.grid_forget()
		self.linhas.grid_forget()
		self.linhasLabel.grid_forget()
		self.largura.grid_forget()
		self.larguraLabel.grid_forget()
		self.distancia.grid_forget()
		self.distanciaLabel.grid_forget()

	def callback(self, eventObject):
		
		implemento = eventObject.widget.get()
		if implemento == 'Arado de aivecas' or implemento == 'Arado de discos' or implemento == 'Grade de discos - ação dupla em X - Tandem' or \
		implemento == 'Grade de discos - ação dupla em V - Offset' or implemento == 'Grade de discos - ação simples':
			self.implemento_larg()
		elif implemento == 'Subsolador - ponteira simples' or implemento == 'Subsolador - ponteira com asas' or implemento == 'Cultivador de campo':
			self.implemento_orgaos()
		elif self.implemento.get() == 'Encanteirador' or self.implemento.get() == 'Semeadora montada (sementes graúdas)' or \
			self.implemento.get() == 'Semeadora de arrasto (sementes graúdas)' or self.implemento.get() == 'Semeadora de arrasto - adubadora - pulverizadora (sementes graúdas)' \
			or self.implemento.get() == 'Semeadora montada (sementes miúdas)' or self.implemento.get() == 'Semeadora de arrasto (sementes miúdas)' :
			self.implemento_linhas()
		elif implemento == '':
			self.cleaning()

	def implemento_larg(self):
		self.orgaos.grid_forget()
		self.orgaosLabel.grid_forget()
		self.linhas.grid_forget()
		self.linhasLabel.grid_forget()
		self.distancia.grid_forget()
		self.distanciaLabel.grid_forget()
		self.largura.grid(row=2, column=1)
		self.larguraLabel.grid(row=2, column=0)

	def implemento_orgaos(self):
		self.largura.grid_forget()
		self.larguraLabel.grid_forget()
		self.linhas.grid_forget()
		self.linhasLabel.grid_forget()
		self.orgaos.grid(row=2, column=1)
		self.orgaosLabel.grid(row=2, column=0)
		self.distancia.grid(row=3, column=1)
		self.distanciaLabel.grid(row=3, column=0)

	def implemento_linhas(self):
		self.largura.grid_forget()
		self.larguraLabel.grid_forget()
		self.orgaos.grid_forget()
		self.orgaosLabel.grid_forget()
		self.linhas.grid(row=2, column=1)
		self.linhasLabel.grid(row=2, column=0)
		self.distancia.grid(row=3, column=1)
		self.distanciaLabel.grid(row=3, column=0)

	def update_trv(self):
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		query = "SELECT * FROM implemento"
		c.execute(query)
		row = c.fetchall()
		self.trv_hist.delete(*self.trv_hist.get_children())
		for i in row:
			self.trv_hist.insert('', "end", values=i)
		conn.close()

	def getrow(self, event):
		self.clean()
		self.rowid = self.trv_hist.identify_row(event.y)
		self.item = self.trv_hist.item(self.trv_hist.focus())
		self.id = self.item['values'][0]
		if self.item['values'][4] == 'None' and self.item['values'][5] == 'None':
			self.implemento_larg()
		elif self.item['values'][4] != 'None':
			self.implemento_orgaos()
			self.distancia.insert(0, float(self.item['values'][3]) / float(self.item['values'][4]))
		elif self.item['values'][5] != 'None':
			self.implemento_linhas()
			self.distancia.insert(0, float(self.item['values'][3]) / float(self.item['values'][5]))

		self.nome.insert(0, self.item['values'][1])
		self.implemento.set(self.item['values'][2])
		self.largura.insert(0, self.item['values'][3])
		self.orgaos.insert(0, self.item['values'][4])
		self.linhas.insert(0, self.item['values'][5])
		self.valorCompra.insert(0, str(self.item['values'][6]))
		self.valorJuro.insert(0, str(self.item['values'][7]))
		self.valorSeguro.insert(0, str(self.item['values'][8]))
		self.valorGaragem.insert(0, str(self.item['values'][9]))
		self.horaAno.insert(0, str(self.item['values'][10]))
		self.vidaUtil.insert(0, str(self.item['values'][11]))

	def cleaning(self):
		self.orgaos.grid_forget()
		self.orgaosLabel.grid_forget()
		self.linhas.grid_forget()
		self.linhasLabel.grid_forget()
		self.largura.grid_forget()
		self.larguraLabel.grid_forget()
		self.distancia.grid_forget()
		self.distanciaLabel.grid_forget()