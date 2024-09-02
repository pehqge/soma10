from tkinter import *

class ActorPlayer:
	def __init__(self):
		self.mainWindow = Tk()
		self.mainWindow.title("Jogo da velha")
		self.mainWindow.iconbitmap("images/icon.ico")
		self.mainWindow.geometry("375x415")
		self.mainWindow.resizable(False, False)
		self.mainWindow["bg"]="gray"

		self.mainFrame = Frame(self.mainWindow, padx=32, pady=25, bg="gray")
		self.messageFrame = Frame(self.mainWindow, padx=4, pady=1, bg="gray")

		self.empty = PhotoImage(file="images/empty.gif")		#pyimage1
		self.white = PhotoImage(file="images/white.gif")		#pyimage2
		self.red = PhotoImage(file="images/red.gif")			#pyimage3

		self.boardView=[]
		for y in range(3):
		    viewTier = []
		    for x in range(3):
		    	aLabel = Label(self.mainFrame, bd=2, relief="solid", image=self.empty)
		    	aLabel.grid(row=x , column=y)
		    	aLabel.bind("<Button-1>", lambda event, line=y+1, column=x+1: self.click(event, line, column))
		    	viewTier.append(aLabel)
		    self.boardView.append(viewTier)

		self.labelMessage = Label(self.messageFrame, bg="gray", text='Clique em qualquer posiÃ§Ã£o para iniciar', font="arial 14")
		self.labelMessage.grid(row=0, column=0, columnspan=3)
		self.mainFrame.grid(row=0 , column=0)
		self.messageFrame.grid(row=1 , column=0) 

		self.whiteTurn=True

		self.mainWindow.mainloop()


	def click(self, event, linha, coluna):
		label=self.boardView[linha-1][coluna-1]
		if label['imag']=='pyimage1':
			if self.whiteTurn:
				label['imag']=self.white
				self.whiteTurn=False
			else:
				label['imag']=self.red
				self.whiteTurn=True

ActorPlayer()
