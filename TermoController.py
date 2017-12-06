
import usbrelaycontroller as usbc
import shlex, subprocess
from subprocess import call
import datetime
import time
import threading
import curses
import logging

tempList=[]
usbc.init()
g_temp=0
flagRelayOpen=False
stopThr=False
powerOn=False
status={"powerOn":False,"maxTemp":20,"minTemp":17,"maxPowerOn":30,"temp":0.0,"timeStart":datetime.datetime.now(),"timeStop":datetime.datetime.now(),"timeNow":datetime.datetime.now()}



def closeAll():
 stopThr=True
 if (flagRelayOpen):
   usbc.closeRelay()
 usbc.close()

def execute(command):
  proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()
  return out



def getTemper():
  rawTemp=execute(["temper-poll"])
  temp = float(str(rawTemp,'utf-8')[27:31])
  return temp

#-------------------------------------------COURSES INIT-------------------------------------------
def initKey():
  Lstdscr = curses.initscr()
  curses.start_color()
  curses.cbreak()
  curses.curs_set(0)
  Lstdscr.keypad(1)
  
  return Lstdscr


#-------------------------------------------MENU-------------------------------------------
def colorizeOnOff(switch,ultra=False):
  modeDefault=curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
  modeUltraOn= curses.init_pair(2,curses.COLOR_RED,curses.COLOR_WHITE)
  modeOn= curses.A_BOLD
  if (switch):
    if (ultra):
      return curses.color_pair(2)
    else:
      return modeOn
  else:
    return curses.color_pair(1)
  
	
def statusMenu(x,y):
  win2=stdscr.subwin(9,60,13,0)
  win2.addstr(1,0,"Power on: {0}    ".format(status["powerOn"]),colorizeOnOff(status["powerOn"],True))
  win2.addstr(2,0,"Max Time Power on: {0}    ".format(status["maxPowerOn"]),colorizeOnOff(status["maxPowerOn"]))
  win2.addstr(3,0,"Max Temp On: {0}    ".format(str(functionOn[checkMaxTemp])),colorizeOnOff(functionOn[checkMaxTemp]))
  win2.addstr(4,0,"Min Temp On: {0}    ".format(str(functionOn[checkMinTemp])),colorizeOnOff(functionOn[checkMinTemp]))
  win2.addstr(5,0,"Max Temperature: {0}°".format(status["maxTemp"]))
  win2.addstr(6,0,"Min Temperature: {0}°".format(status["minTemp"]))
  win2.addstr(7,0,"Max Time on func: {0} min.".format(status["maxPowerOn"]))
  win2.addstr(8,0,"Start Time : {0}      ".format(status["timeStart"]))
  stdscr.refresh()


def mainMenu():
  win1=stdscr.subwin(12,60,0,0)
  win1.addstr(1,0,"- Time: {0}         ".format(status["timeNow"]))
  win1.addstr(2,0,"- Current Temperature: {0}        ".format(status["temp"]),curses.A_BOLD)  
  win1.addstr(3,0,"- Power [on/off]: Acende / spegne On/Off")
  win1.addstr(4,0,"- poweron [on/off]: tempo di massima accensione on/off")
  win1.addstr(5,0,"- setMaxPowerOn [min]: imposta minuti di massima accensione")
  win1.addstr(6,0,"- MaxTempOn [on/off]: Accende/Spegne il controllo spegnimento a rangiungimento della massima temperatura")
  win1.addstr(7,0,"- SetMaxTemp [temp]: Imposta la massima temperatura superata la quale si spegne")
  win1.addstr(8,0,"- MinTempOn [on/off]: Accende/Spegne il controllo accensione a rangiungimento della minima temperatura")
  win1.addstr(9,0,"- SetMaxTemp [temp]: Imposta la minima temperatura sotto la quale si accende")
  win1.addstr(10,0,"- Quit   - Quit")
  stdscr.refresh()
#----------------------------------------------------------------------------------------



#-------------------------------------------GESTION SENSORE TEMPERATURA------------------------------------------
def controlTermo():
  temp=getTemper()
  status["temp"]=temp
  status["timeNow"]=datetime.datetime.now()
  mainMenu()
  executeFunction()


def quit(param):
  closeAll()
  curses.endwin()

#-------------------------------------------POWER ----------------------------------------------------------
def power(param):
  if param=='off':
    usbc.closeRelay()
    status["powerOn"]=False
    status["timeStop"]=datetime.datetime.now()
  elif param=='on':
    usbc.openRelay()
    status["powerOn"]=True
    status["timeStart"]=datetime.datetime.now()


#------------------------------------------MAX TEMP SETTING-------------------------------------------------
#Attiva o disattiva la funzione
def activeMaxTemp(param):
  if param=='off':
    functionOn[checkMaxTemp]=False
  elif param=='on':
    functionOn[checkMaxTemp]=True

#Verifica quando spegnere
def checkMaxTemp():
  if (status["temp"]>status["maxTemp"]): #spegni
    usbc.closeRelay()

def setMaxTemp(param):
  status["maxTemp"]=float(param)

#------------------------------------------Min TEMP SETTING-------------------------------------------------

#Attiva o disattiva la funzione
def activeMinTemp(param):
  if param=='off':
    functionOn[checkMinTemp]=False
  elif param=='on':
    functionOn[checkMinTemp]=True

#Verifica quando accendere
def checkMinTemp():
  if (status["temp"]<status["minTemp"]): #accendi
    usbc.openrelay()

def setMinTemp(param):
  status["minTemp"]=float(param)


#------------------------------------------MAX TIME ON SETTING-------------------------------------------------
#
def maxPowerOn():
  log("maxpoweron: {0}".format(status["maxPowerOn"]))
  tdelta=datetime.datetime.now()-status["timeStart"]
  log(tdelta.seconds)
  if(tdelta.seconds>int(status["maxPowerOn"])*60):
    power('off')

def setMaxPowerOn(param):
  status["maxPowerOn"]=param

def activeMaxPowerOn(param):
  if param=='on':
    functionOn[maxPowerOn]=True
  if param=='off':
    functionOn[maxPowerOn]=False






#---------------------- EXECUTE FUNCTION ---------------------------------------------------------------------
functionOn = {checkMaxTemp:True,checkMinTemp:False,maxPowerOn:True}
def executeFunction():
  for func in functionOn:
    if functionOn[func]:
      func()

def executeCommand(command,param):
  log("execute cimman2")
  curses.beep()
  #try:
  command(param)
  statusMenu(1,1)


#---------------------- GESTIONE INPUT COMANDI ---------------------------------------------------------------------
def inputControl():
  win3=stdscr.subwin(1,79,12,0)
  win3.bkgdset(".")
  command=''
  while(command != 'quit'):
    l=0
    s=""
    while (l<1):
      try:	
        win3.addstr(0,0,"c o m m a n d:                                                               ")
        s = str(win3.getstr(0,15),'utf-8').lower()
      except:
        pass

      sParam=s.split(' ')
      l=len(sParam)
      log("l:"+str(l))
      if l>0:
        command=sParam[0]
      if l>1:
        param=sParam[1]

    if command == "quit":
      executeCommand(quit(''))

    elif command  == "power":
      executeCommand(power,(str(param)))

    #massimo temp di accensione
    elif command  == "setmaxpoweron":
      executeCommand(setMaxPowerOn,(str(param)))
    elif command == "poweron":
      executeCommand(activeMaxPowerOn,(str(param)))

    #impostazione della temperatura massima raggiunta la quale si spegne
    elif command == "setmaxtemp":
      executeCommand(setMaxTemp,(str(param)))
    elif command  == "maxtempon":
      executeCommand(activeMaxTimeOn,(str(param)))

    #impostazione della temperatura minima raggiunta la quale si accende
    elif command == "setmintemp":
      executeCommand(setMinTemp,(str(param)))
    elif command  == "mintempon":
      executeCommand(activeMinTimeOn,(str(param)))


   




#-----------------------------------------GESTIONE LOG------------------------------------------
ri=0
def initLog(filelog='termolog.txt'):
  logging.basicConfig(filename=filelog,level=logging.DEBUG)
  logging.info('Start logging')

def log(info):
  logging.debug(str(info))

  


#Funzione thread lettura temperatura
def f():
  # do something here ...
  while (stopThr==False):
    controlTermo()
    #if stopThr==False:
    #  myThread.run()

if __name__ == '__main__':
  #Inizializzazione
  initLog()
  stdscr=initKey()
  mainMenu()
  statusMenu(10,1)

  # Esecuzione Thread lettura temperatura
  #myThread = threading.Timer(5, f)  # timer is set to 3 seconds
  myThread = threading.Thread(target=f)
  myThread.start()
  #myThread.run()

  # Esecuzione Thread input caratteri
  inputThread = threading.Thread(target=inputControl)
  inputThread.start()


