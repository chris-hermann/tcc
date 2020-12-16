import tkinter as tk
import tractor, talhao, implemento, cf_simples, operacao


class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.title('TCC v 0.1')
        self.master.geometry('220x198')
        self.frame = tk.Frame(self.master)
        self.tratorButton = tk.Button(self.frame, text = 'Trator', width = 29, command = self.trator_window)
        self.talhaoButton = tk.Button(self.frame, text = 'Talhão', width = 29, command = self.talhao_window)
        self.implementoButton = tk.Button(self.frame, text = 'Implemento', width = 29, command = self.implemento_window)
        self.custofixoButton = tk.Button(self.frame, text = 'Simulação simples de custo-fixo', width = 29, command =self.custofixo_simples_window)
        self.operacaoButton = tk.Button(self.frame, text = 'Simulação de operação agrícola', width = 29, command =self.operacao_window)
        self.quitButton = tk.Button(self.frame, text = 'Sair', width = 29, command = self.destroy_window)
        self.tratorButton.grid(padx=5, pady=3, sticky=tk.E+tk.W)
        self.talhaoButton.grid(padx=5, pady=2, sticky=tk.E+tk.W)
        self.implementoButton.grid(padx=5, pady=3, sticky=tk.E+tk.W)
        self.custofixoButton.grid(padx=5, pady=2, sticky=tk.E+tk.W)
        self.operacaoButton.grid(padx=5, pady=3, sticky=tk.E+tk.W)
        self.quitButton.grid(padx=5, pady=2, sticky=tk.E+tk.W)
        self.frame.grid()

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

    def destroy_window(self):
    	self.master.destroy()


def main(): 
    root = tk.Tk()
    root.resizable(False, False)
    app = MainPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()