import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TalhaoPage:
	def __init__(self, master):
		self.master = master
		self.master.title('Talhão')
		self.master.geometry('500x500')
		self.frame_buttons = tk.Frame(self.master)
		self.frame_inputs = tk.Frame(self.master)
		self.nome = tk.Entry(self.frame_inputs)
		self.area = tk.Entry(self.frame_inputs)
		self.textura = tk.ttk.Combobox(self.frame_inputs, values = ['Arenosa', 'Média', 'Argilosa'])
		self.nomeLabel = tk.Label(self.frame_inputs, text = 'Nome: ')
		self.areaLabel = tk.Label(self.frame_inputs, text = 'Área (ha): ')
		self.texturaLabel = tk.Label(self.frame_inputs, text = 'Textura do solo: ')
		self.submitButton = tk.Button(self.frame_buttons, text = 'Inserir', width = 25, command = self.submit)
		self.updateButton = tk.Button(self.frame_buttons, text = 'Atualizar', width = 25, command = self.update_db)
		self.cleanButton = tk.Button(self.frame_buttons, text = 'Limpar', width = 25, command = self.clean)
		self.deleteButton = tk.Button(self.frame_buttons, text = 'Deletar', width = 25, command = self.delete)
		self.quitButton = tk.Button(self.frame_buttons, text = 'Voltar', width = 25, command = self.close_windows)
		self.nomeLabel.grid(row = 0, column = 0)
		self.areaLabel.grid(row = 1, column = 0)
		self.texturaLabel.grid(row = 2, column = 0)
		self.nome.grid(row = 0, column = 1)
		self.area.grid(row = 1, column = 1)
		self.textura.grid(row = 2, column = 1)
		self.submitButton.pack()
		self.updateButton.pack()
		self.cleanButton.pack()
		self.deleteButton.pack()
		self.quitButton.pack()
		self.frame_inputs.grid()
		self.frame_buttons.grid()

		self.frame_trv = tk.Frame(self.master)
		self.frame_trv.grid(row=5, column=0, columnspan=3, padx=3, pady=3, sticky=tk.E+tk.W)
		self.trv_hist = tk.ttk.Treeview(self.frame_trv, columns=(1,2,3,4), show="headings", height='5', selectmode='browse')
		self.trv_hist.pack(side=tk.TOP)
		self.hozscrlbar = tk.ttk.Scrollbar(self.frame_trv, orient=tk.HORIZONTAL, command=self.trv_hist.xview)
		self.hozscrlbar.pack(side=tk.BOTTOM, fill='x')
		#self.verscrlbar = ttk.Scrollbar(frame_trv, orient=VERTICAL, command=trv_hist.yview)
		#self.verscrlbar.pack(side=RIGHT, fill='y')
		self.trv_hist.configure(xscrollcommand=self.hozscrlbar.set)

		self.trv_hist.heading(1, text="Id")
		self.trv_hist.heading(2, text="Nome")
		self.trv_hist.heading(3, text="Área (ha)")
		self.trv_hist.heading(4, text="Textura")
		self.trv_hist.column('1', width=50, minwidth=30, anchor='center')
		self.trv_hist.column('2', width=50, minwidth=60, anchor='center')
		self.trv_hist.column('3', width=50, minwidth=108, anchor='center')
		self.trv_hist.column('4', width=50, minwidth=108, anchor='center')
		self.update_trv()
		self.trv_hist.bind('<Double 1>', self.getrow)

	def close_windows(self):
		self.master.destroy()

	def submit(self):
		conn = sqlite3.connect('database.db') #Criando ou conectando ao banco de dados
		c = conn.cursor() #Configurando o cursor para navegar no banco de dados
		c.execute("""CREATE TABLE IF NOT EXISTS talhao( 
								 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
								 nome TEXT NOT NULL,
								 area REAL NOT NULL,
								 textura REAL NOT NULL)""")
		values_db = "INSERT INTO talhao(nome, area, textura) VALUES (?,?,?)" 
		c.execute(values_db, (self.nome.get(), self.area.get(), self.textura.get()))
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão
		self.update_trv()


	def update_db(self):
		conn = sqlite3.connect('database.db') #Criando ou conectando ao banco de dados
		c = conn.cursor() #Configurando o cursor para navegar no banco de dados
		query = "UPDATE talhao SET nome=?, area=?, textura=? WHERE id=?"
		c.execute(query, (self.nome.get(), self.area.get(), self.textura.get(), self.id))
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão
		self.update_trv()

	def update_trv(self):
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		query = "SELECT * FROM talhao"
		c.execute(query)
		row = c.fetchall()
		self.trv_hist.delete(*self.trv_hist.get_children())
		for i in row:
			self.trv_hist.insert('', "end", values=i)
		conn.commit() #Commitando as alterações
		conn.close() #Fechando a conexão

	def getrow(self, event):
		self.nome.delete(0, tk.END)
		self.area.delete(0, tk.END)
		self.textura.delete(0, tk.END)
		self.rowid = self.trv_hist.identify_row(event.y)
		self.item = self.trv_hist.item(self.trv_hist.focus())
		self.id = self.item['values'][0]
		self.nome.insert(0, self.item['values'][1])
		self.area.insert(0, self.item['values'][2])
		self.textura.set(self.item['values'][3])

	def clean(self):
		self.nome.delete(0, tk.END)
		self.area.delete(0, tk.END)
		self.textura.delete(0, tk.END)

	def delete(self):
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		selection = self.trv_hist.selection()
		query = "DELETE FROM talhao WHERE id=?"
		c.execute(query, (self.trv_hist.set(selection, "#1"),))
		conn.commit()
		conn.close()
		self.update_trv()



