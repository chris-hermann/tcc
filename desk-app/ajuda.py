
from tkinter import *
from tkPDFViewer import tkPDFViewer as pdf 
  

class Ajuda():
	def __init__(self, master):
		self.master = master
		self.master.resizable = (False,False)
		self.master.title('Ajuda')
		self.master.iconbitmap('icon.ico')
		v1 = pdf.ShowPdf() 
  		# Adding pdf location and width and height. 
		v2 = v1.pdf_view(master, 
		                 pdf_location = r"TESTMAQ_GuiaUsuario.pdf",  
		                 width = 75, height = 40) 
		  
		# Placing Pdf in my gui. 
		v2.pack() 