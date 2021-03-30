import tkinter as tk
import tractor, talhao, implemento, cf_simples, operacao, ajuda
from tkPDFViewer import tkPDFViewer 


class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.title('TESTMAQ  v.1.0.0')
        self.master.geometry('280x210')
        self.master.iconbitmap('icon.ico')
        self.frame = tk.Frame(self.master)
        self.tratorButton = tk.Button(self.frame, text = 'Trator', width = 29, command = self.trator_window)
        self.talhaoButton = tk.Button(self.frame, text = 'Talhão', width = 29, command = self.talhao_window)
        self.implementoButton = tk.Button(self.frame, text = 'Implemento', width = 29, command = self.implemento_window)
        self.custofixoButton = tk.Button(self.frame, text = 'Simulação simples de custo-fixo', width = 29, command =self.custofixo_simples_window)
        self.operacaoButton = tk.Button(self.frame, text = 'Simulação de operação agrícola', width = 29, command =self.operacao_window)
        self.quitButton = tk.Button(self.frame, text = 'Sair', width = 29, command = self.destroy_window)
        self.tratorButton.pack(padx=5, pady=3)
        self.talhaoButton.pack(padx=5, pady=2)
        self.implementoButton.pack(padx=5, pady=3)
        self.custofixoButton.pack(padx=5, pady=2)
        self.operacaoButton.pack(padx=5, pady=3)
        self.quitButton.pack(padx=5, pady=2)
        self.frame.pack()
        self.MenuTopo = tk.Menu(self.master)
        self.master.config(menu=self.MenuTopo)
        self.AjudaMenu = tk.Menu(self.MenuTopo, tearoff=False)
        self.MenuTopo.add_cascade(label = 'Ajuda', menu=self.AjudaMenu)
        self.AjudaMenu.add_command(label = 'Guia do Usuário', command=self.ExibirAjuda)
        self.AjudaMenu.add_command(label = 'Nossos contatos', command=self.ExibirContatos)

    def trator_window(self):
        self.tratorWindow = tk.Toplevel(self.master)
        self.app = tractor.TratorPage(self.tratorWindow)

    def implemento_window(self):
    	self.implementoWindow = tk.Toplevel(self.master)
    	self.app = implemento.ImplementoPage(self.implementoWindow)

    def talhao_window(self):
    	self.talhaoWindow = tk.Toplevel(self.master)
    	self.app = talhao.TalhaoPage(self.talhaoWindow)

    def custofixo_simples_window(self):
    	self.cf_simplesWindow = tk.Toplevel(self.master)
    	self.app = cf_simples.CFPage(self.cf_simplesWindow)

    def operacao_window(self):
    	self.op_windows = tk.Toplevel(self.master)
    	self.app = operacao.OperacaoPage(self.op_windows)

    def ExibirAjuda(self):
        self.AjudaViewer = tk.Toplevel(self.master)
        self.app = ajuda.Ajuda(self.AjudaViewer)

    def ExibirContatos(self):
        tk.messagebox.showinfo(title='Contatos', message='Grupo de Estudos em Mecanização e Agricultura de Precisão: gmap@ufsj.edu.br  \n\n' \
                                + 'Christoph Hermann: (31) 99616-3282 | chris.tigges@gmail.com \n\n' \
                                + 'Édio Costa: (31) 99401-3941 | edio@ufsj.edu.br')


    def destroy_window(self):
    	self.master.destroy()



def main(): 
    root = tk.Tk()
    root.resizable(False, False)
    app = MainPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()