import tkinter as tk
from cgitb import text
class gui:
    temp=0
    def __init__(self,winmain):
        #mybutton=tk.Button(winmain,text="Finestra Test").grid()
        self.templabel=tk.Label(winmain,text="Temp.: ").grid()
        self.temptext=tk.Label(winmain,text=self.temp, background="green").grid()

    
    
#Creo l'oggetto finestra principale
winmain=tk.Tk()
termocontr= gui(winmain)
winmain.mainloop()