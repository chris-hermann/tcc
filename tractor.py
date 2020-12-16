import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import tkinter.font as tkFont


class TratorPage:
	def __init__(self, master):
		self.master = master
		self.master.title('Trator')

		#Configuração da GUI
		self.frame = tk.Frame(self.master)
		self.frame_inputs = tk.Frame(self.master)
		self.nome = tk.Entry(self.frame_inputs)
		self.potencia = tk.Entry(self.frame_inputs)
		self.transmissao = tk.ttk.Combobox(self.frame_inputs, values = ['4x2', '4x2 TDA', '4x4'])
		self.valorCompra = tk.Entry(self.frame_inputs)
		self.valorJuro = tk.Entry(self.frame_inputs)
		self.valorSeguro = tk.Entry(self.frame_inputs)
		self.valorGaragem = tk.Entry(self.frame_inputs)
		self.horaAno = tk.Entry(self.frame_inputs)
		self.vidaUtil = tk.Entry(self.frame_inputs)
		self.nome.grid(row=0, column=1)
		self.potencia.grid(row=1, column=1)
		self.transmissao.grid(row=2, column=1)
		self.valorCompra.grid(row=3, column=1)
		self.valorJuro.grid(row=4, column=1)
		self.valorSeguro.grid(row=5, column=1)
		self.valorGaragem.grid(row=6, column=1)
		self.horaAno.grid(row=7, column=1)
		self.vidaUtil.grid(row=8, column=1)
		self.submitButton = tk.Button(self.frame, text = 'Inserir', width = 25, command = self.submit)
		self.quitButton = tk.Button(self.frame, text = 'Voltar', width = 25, command = self.close_windows)
		self.cleanButton = tk.Button(self.frame, text = 'Limpar', width = 25, command = self.clean)
		self.updateButton = tk.Button(self.frame, text = 'Atualizar', width = 25, command = self.update_db)
		self.deleteButton = tk.Button(self.frame, text = 'Deletar', width = 25, command = self.delete)
		self.submitButton.grid()
		self.cleanButton.grid()
		self.updateButton.grid()
		self.deleteButton.grid()
		self.quitButton.grid()
		self.frame.grid(row = 1, column = 0, columnspan = 2)

		#Labels da página
		self.frame_inputs.grid(row = 0, column = 0)
		self.nome_label = tk.Label(self.frame_inputs, text = 'Nome do trator: ').grid(row=0, column=0)
		self.potencia_label = tk.Label(self.frame_inputs, text = 'Potência nominal (cv): ').grid(row=1, column=0)
		self.transmissao_label = tk.Label(self.frame_inputs, text = 'Tipo de transmissão: ').grid(row=2, column=0)
		self.compra_label = tk.Label(self.frame_inputs, text = 'Valor de compra (R$): ').grid(row=3, column=0)
		self.juro_label = tk.Label(self.frame_inputs, text = 'Juros sobre o capital (%): ').grid(row=4, column=0)
		self.seguro_label = tk.Label(self.frame_inputs, text = 'Taxa de seguro (%): ').grid(row=5, column=0)
		self.garagem_label = tk.Label(self.frame_inputs, text = 'Taxa de garagem (%): ').grid(row=6, column=0)
		self.horaAno_label = tk.Label(self.frame_inputs, text = 'Horas trabalhadas por ano: ').grid(row=7, column=0)
		self.vidaUtil_label = tk.Label(self.frame_inputs, text = 'Vida Útil (anos): ').grid(row=8, column=0)
		self.frame_trv = tk.Frame(self.master)
		self.frame_trv.grid(row=12, column=0, columnspan=3, padx=3, pady=3, sticky=tk.E+tk.W)
		self.spacelabel1 = tk.Label(self.frame_trv).pack()
		self.titlefont = tkFont.Font(family='Helvetica', size=22, weight='bold')
		self.trvLabel = tk.Label(self.frame_trv, text='Histórico', font=self.titlefont, anchor = tk.W).pack()
		self.trvHelper = tk.Label(self.frame_trv, text='Dê um clique duplo em algum item do histórico para editar os valores de entrada').pack()
		self.trv_hist = tk.ttk.Treeview(self.frame_trv, columns=(1,2,3,4,5,6,7,8,9,10), show="headings", height='5', selectmode='browse')
		self.trv_hist.pack(side=tk.TOP)
		self.hozscrlbar = tk.ttk.Scrollbar(self.frame_trv, orient=tk.HORIZONTAL, command=self.trv_hist.xview)
		self.hozscrlbar.pack(side=tk.BOTTOM, fill='x')
		#self.verscrlbar = ttk.Scrollbar(frame_trv, orient=VERTICAL, command=trv_hist.yview)
		#self.verscrlbar.pack(side=RIGHT, fill='y')
		self.trv_hist.configure(xscrollcommand=self.hozscrlbar.set)
		self.trv_hist.heading(1, text="Id")
		self.trv_hist.heading(2, text="Nome")
		self.trv_hist.heading(3, text="Potência (cv)")
		self.trv_hist.heading(4, text="Transmissão")
		self.trv_hist.heading(5, text="Valor de compra (R$)")
		self.trv_hist.heading(6, text="Juros (%)")
		self.trv_hist.heading(7, text="Seguro (%)")
		self.trv_hist.heading(8, text="Garagem (%)")
		self.trv_hist.heading(9, text="Vida útil (anos)")
		self.trv_hist.heading(10, text="Horas trabalhadas média (horas)")
		self.trv_hist.column('1', width=50, minwidth=30, anchor='center')
		self.trv_hist.column('2', width=50, minwidth=60, anchor='center')
		self.trv_hist.column('3', width=50, minwidth=108, anchor='center')
		self.trv_hist.column('4', width=50, minwidth=108, anchor='center')
		self.trv_hist.column('5', width=50, minwidth=170, anchor='center')
		self.trv_hist.column('6', width=50, minwidth=85, anchor='center')
		self.trv_hist.column('7', width=50, minwidth=100, anchor='center')
		self.trv_hist.column('8', width=50, minwidth=110, anchor='center')
		self.trv_hist.column('9', width=50, minwidth=130, anchor='center')
		self.trv_hist.column('10', width=50, minwidth=260, anchor='center')
		self.update_trv()
		self.trv_hist.bind('<Double 1>', self.getrow)

	def close_windows(self):
		self.master.destroy()

	def submit(self):
		conn = sqlite3.connect('database.db') #Criando ou conectando ao banco de dados
		c = conn.cursor() #Configurando o cursor para navegar no banco de dados
		#Criando a tabela no banco de dados, se ela não existir, e seus respectivos campos
		c.execute("""CREATE TABLE IF NOT EXISTS trator( 
									 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
									 nome TEXT NOT NULL,
									 pot REAL NOT NULL,
									 trm TEXT NOT NULL,
									 compra REAL,
									 imposto REAL,
									 seg REAL,
									 gar REAL,
									 vu INTEGER,
									 hora INTEGER)""")
		
		#Checagem de preenchimento dos campos de input
		if self.nome.get() == '' or self.transmissao.get() == '' or self.potencia.get() == '':
			messagebox.showerror(title=None, message="Favor preencha todos os campos!") #Mensagem de erro se algum campo não for preenchido
		else:
			values_db = "INSERT INTO trator(nome, pot, trm, compra, imposto, seg, gar, vu, hora) VALUES (?,?,?,?,?,?,?,?,?)" #Atribuindo a variavel a sintaxe SQLITE3
			c.execute(values_db, (self.nome.get(), self.potencia.get(), self.transmissao.get(), \
								self.valorCompra.get(), self.valorJuro.get(), self.valorSeguro.get(), self.valorGaragem.get(), \
								self.vidaUtil.get(), self.horaAno.get())) #Inserindo os valores de entrada na tabela do banco de dados
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão
		self.update_trv()


	def clean(self):
		self.potencia.delete(0, tk.END)
		self.transmissao.delete(0, tk.END)
		self.nome.delete(0, tk.END)
		self.valorCompra.delete(0, tk.END)
		self.valorJuro.delete(0, tk.END)
		self.valorSeguro.delete(0, tk.END)
		self.valorGaragem.delete(0, tk.END)
		self.horaAno.delete(0, tk.END)
		self.vidaUtil.delete(0, tk.END)

	def update_db(self):
		conn = sqlite3.connect('database.db') #Criando ou conectando ao banco de dados
		c = conn.cursor() #Configurando o cursor para navegar no banco de dados
		query = "UPDATE trator SET nome=?, pot=?, trm=?, compra=?, imposto=?, seg=?, gar=?, vu=?, hora=? WHERE id=?"
		c.execute(query, (self.nome.get(), self.potencia.get(), self.transmissao.get(), self.valorCompra.get(),\
						 self.valorJuro.get(), self.valorSeguro.get(), self.valorGaragem.get(), self.horaAno.get(), self.vidaUtil.get(), self.idtt))
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão
		self.update_trv()

	def delete(self):
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		selection = self.trv_hist.selection()
		query = "DELETE FROM trator WHERE id=?"
		c.execute(query, (self.trv_hist.set(selection, "#1"),))
		conn.commit()
		conn.close()
		self.update_trv()

	def update_trv(self):
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		query = "SELECT * FROM trator"
		c.execute(query)
		row = c.fetchall()
		self.trv_hist.delete(*self.trv_hist.get_children())
		for i in row:
			self.trv_hist.insert('', "end", values=i)
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão

	def getrow(self, event):
		self.nome.delete(0, tk.END)
		self.potencia.delete(0, tk.END)
		self.transmissao.delete(0, tk.END)
		self.valorCompra.delete(0, tk.END)
		self.valorJuro.delete(0, tk.END)
		self.valorSeguro.delete(0, tk.END)
		self.valorGaragem.delete(0, tk.END)
		self.horaAno.delete(0, tk.END)
		self.vidaUtil.delete(0, tk.END)
		self.rowid = self.trv_hist.identify_row(event.y)
		self.item = self.trv_hist.item(self.trv_hist.focus())
		self.idtt = self.item['values'][0]
		self.nome.insert(0, self.item['values'][1])
		self.potencia.insert(0, self.item['values'][2])
		self.transmissao.set(self.item['values'][3])
		self.valorCompra.insert(0, self.item['values'][4])
		self.valorJuro.insert(0, self.item['values'][5])
		self.valorSeguro.insert(0, str(self.item['values'][6]))
		self.valorGaragem.insert(0, str(self.item['values'][7]))
		self.horaAno.insert(0, str(self.item['values'][9]))
		self.vidaUtil.insert(0, str(self.item['values'][8]))

