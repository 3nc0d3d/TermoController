
#Restituisce le righe di un file testo
def readFile(fileName):
  file=open(fileName,"r")
  return file.readlines() 
