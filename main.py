import tkinter as tk
import tractor, talhao, implemento

class MainPage:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.tratorButton = tk.Button(self.frame, text = 'Trator', width = 25, command = self.trator_window)
        self.talhaoButton = tk.Button(self.frame, text = 'Talhão', width = 25, command = self.talhao_window)
        self.implementoButton = tk.Button(self.frame, text = 'Implemento', width = 25, command = self.implemento_window)
        self.quitButton = tk.Button(self.frame, text = 'Sair', width = 25, command = self.destroy_window)
        self.tratorButton.grid()
        self.talhaoButton.grid()
        self.implementoButton.grid()
        self.quitButton.grid()
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


    def destroy_window(self):
    	self.master.destroy()


def main(): 
    root = tk.Tk()
    app = MainPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()