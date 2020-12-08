import tkinter as tk

class ImplementoPage:
	def __init__(self, master):
		self.master = master
		self.master.title('Implementos')
		self.frame_inputs = tk.Frame(self.master)
		self.implemento = tk.ttk.Combobox(self.frame_inputs, values=['Arado de aivecas',
																	'Arado de discos',
																	'Subsolador - Ponteira simples',
																	'Subsolador - Ponteira com asas',
																	'Grade de discos - Tandem',
																	'Grade de discos - Offset',
																	'Grade de discos - Single',
																	'Cultivador de campo',
																	'Encanteirador',
																	'Semeadora montada',
																	'Semeadora de arrasto'])
		self.nome = tk.Entry(self.frame_inputs)
		self.valorCompra = tk.Entry(self.frame_inputs)
		self.valorJuro = tk.Entry(self.frame_inputs)
		self.valorSeguro = tk.Entry(self.frame_inputs)
		self.valorGaragem = tk.Entry(self.frame_inputs)
		self.horaAno = tk.Entry(self.frame_inputs)
		self.vidaUtil = tk.Entry(self.frame_inputs)
		self.nome.grid(row=1, column=1)
		self.valorCompra.grid(row=4, column=1)
		self.valorJuro.grid(row=5, column=1)
		self.valorSeguro.grid(row=6, column=1)
		self.valorGaragem.grid(row=7, column=1)
		self.horaAno.grid(row=8, column=1)
		self.vidaUtil.grid(row=9, column=1)
		self.implemento.grid(row=0, column=1)
		self.frame_inputs.pack()

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
		self.frame_buttons.pack()

	def close_windows(self):
		self.master.destroy()

	def submit(self):
		pass

	def update_db(self):
		pass

	def delete(self):
		pass

	def clean(self):
		pass

	def implemento_larg(self):
		self.largura = tk.Entry(self.frame_inputs)
		self.largura.grid()

	def implemento_orgaos(self):
		self.orgaos = tk.Entry(self.frame_inputs)
		self.orgaos.grid()

	def implemento_linhas(self):
		self.linhas = tk.Entry(self.frame_inputs)
		self.linhas.grid()

