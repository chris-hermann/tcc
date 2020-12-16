import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class CFPage:
	def __init__(self, master):
		self.master = master
		self.master.title('Simulação simples do custo fixo')
		self.frame_inputs = tk.Frame(self.master)
		self.spacerFrame1 = tk.Frame(self.master)
		self.frame_trv = tk.Frame(self.master)
		self.frame_buttons = tk.Frame(self.master)
		self.spacerFrame1.grid()
		self.frame_inputs.grid()
		self.frame_trv.grid()
		self.frame_buttons.grid()

		self.combo = tk.ttk.Combobox(self.frame_inputs, values=['Tratores', 'Implementos'])
		self.combo.grid(row=0, column=1)
		self.combo.bind('<<ComboboxSelected>>', self.combo_action)
		self.labelSpacer1 = tk.Label(self.spacerFrame1).grid()
		self.labelSpacer2 = tk.Label(self.frame_inputs).grid()

		self.trv = tk.ttk.Treeview(self.frame_trv, columns=(1,2,3), displaycolumns=('2','3'), show='headings', height='3', selectmode='browse')
		self.trv.grid()
		self.trv_label = tk.Label(self.frame_trv)
		self.trv_label.grid()

		self.actionButton = tk.Button(self.frame_buttons, text='Simular custo fixo simples', command=self.simulate)
		self.actionButton.grid(row=0, column=0, padx=5, pady=5)
		self.quitButton = tk.Button(self.frame_buttons, text='Voltar', command=self.master.destroy)
		self.quitButton.grid(row=0, column=1, padx=5, pady=5)
		
		self.cf_horaLabel = tk.Label(self.frame_buttons)
		self.cf_totalLabel = tk.Label(self.frame_buttons)
		self.cf_depreciacaoLabel = tk.Label(self.frame_buttons)
		self.cf_juroLabel = tk.Label(self.frame_buttons)
		self.cf_seguroLabel = tk.Label(self.frame_buttons)
		self.cf_garagemLabel = tk.Label(self.frame_buttons)
		self.cf_totalLabel.grid()
		self.cf_depreciacaoLabel.grid()
		self.cf_juroLabel.grid()
		self.cf_seguroLabel.grid()
		self.cf_garagemLabel.grid()
		self.cf_horaLabel.grid()
		self.comboLabel = tk.Label(self.frame_inputs, text='Selecione uma opção: ').grid(row=0, column=0)
		


		

	def combo_action(self, eventObject):
		self.trv_label.config(text='Selecione o trator ou implemento e clique no botão abaixo')
		self.combo = eventObject.widget.get()
		if self.combo == 'Tratores':
			self.trv.heading(2, text='Nome')
			self.trv.heading(3, text='Potência')
			conn = sqlite3.connect('database.db')
			c = conn.cursor()
			query = "SELECT id, nome, pot FROM trator"
			c.execute(query)
			row = c.fetchall()
			self.trv.delete(*self.trv.get_children())
			for i in row:
				self.trv.insert('', "end", values=i)
			conn.commit() #Commitando as alterações
			conn.close() #Fechando a conexão
		elif self.combo == 'Implementos':
			self.trv.heading(2, text='Nome')
			self.trv.heading(3, text='Tipo')
			conn = sqlite3.connect('database.db')
			c = conn.cursor()
			query = "SELECT id, nome, tipo FROM implemento"
			c.execute(query)
			row = c.fetchall()
			self.trv.delete(*self.trv.get_children())
			for i in row:
				self.trv.insert('', "end", values=i)
			conn.commit() #Commitando as alterações
			conn.close() #Fechando a conexão

	def simulate(self):
		self.trv_label.grid_forget()
		if self.combo == 'Tratores':
			conn = sqlite3.connect('database.db')
			c = conn.cursor()
			self.trv_selection = self.trv.item(self.trv.focus())
			self.id = self.trv_selection['values'][0]
			c.execute("SELECT * FROM trator WHERE id LIKE '%"+str(self.id)+"%'")
			self.data = c.fetchall()
			conn.commit()
			conn.close()
			self.data = str(self.data)
			self.data = self.data.split(',')
			self.vCompra = float(self.data[4].strip(' '))
			self.vJuro = float(self.data[5].strip(' '))
			self.vSeguro = float(self.data[6].strip(' '))
			self.vGaragem = float(self.data[7].strip(' '))
			self.vidaUtil = float(self.data[8].strip(' '))
			self.horaAno = float(self.data[9].strip('[]() '))
			self.calculate()
		elif self.combo == 'Implementos':
			conn = sqlite3.connect('database.db')
			c = conn.cursor()
			self.trv_selection = self.trv.item(self.trv.focus())
			self.id = self.trv_selection['values'][0]
			c.execute("SELECT * FROM implemento WHERE id LIKE '%"+str(self.id)+"%'")
			self.data = c.fetchall()
			conn.commit()
			conn.close()
			self.data = str(self.data)
			self.data = self.data.split(',')
			self.vCompra = float(self.data[6].strip(' '))
			self.vJuro = float(self.data[7].strip(' '))
			self.vSeguro = float(self.data[8].strip(' '))
			self.vGaragem = float(self.data[9].strip(' '))
			self.vidaUtil = float(self.data[10].strip(' '))
			self.horaAno = float(self.data[11].strip("[]() '"))			
			self.calculate()			

	def calculate(self):
		self.depreciacao = self.vCompra - (self.vCompra * 0.1)
		self.juro = (self.vJuro / 100) * ((self.vCompra + (self.vCompra + 0.1)) / 2)
		self.garagem = (self.vGaragem / 100) * self.vCompra
		self.seguro = (self.vSeguro / 100) * self.vCompra
		self.cfsimples_total = self.depreciacao + self.juro + self.garagem + self.seguro
		self.cfsimples_hora = self.cfsimples_total / (self.vidaUtil * self.horaAno)
		self.cf_totalLabel.config(text='O custo fixo total será de ' + str("%.3f" % self.cfsimples_total) + ' reais ao longo de toda a vida útil especificada.')
		self.cf_depreciacaoLabel.config(text='   O custo de depreciação será de ' + str("%.3f" % self.depreciacao) + ' reais.')
		self.cf_juroLabel.config(text='   O custo de juro sobre o capital será de ' + str("%.3f" % self.juro) + ' reais.')
		self.cf_garagemLabel.config(text='   O custo com garagem será de ' + str("%.3f" % self.garagem) + ' reais.')
		self.cf_seguroLabel.config(text='   O custo com seguro será de ' + str("%.3f" % self.seguro) + ' reais.')
		self.cf_horaLabel.config(text='O custo fixo diluido nas horas trabalhadas será de ' + str("%.3f" % self.cfsimples_hora) + ' reais.')
