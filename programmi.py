import iolib
import schedule
import datetime
class programmatore:
  days={"lun":0,"mar":1,"mer":2,"gio":3,"ven":4,"sab":5,"dom":6}
  programmi=[]
  def leggiProgramma():	
    progrs=iolib.readFile("programmi.cfg")
    for progParams in progrs:	 
      progParam=str(progParams).split(" ")
        programma=[]	    
        for param in progParam:	  
          programma.append(param.rstrip())	  
      programmi.append(programma)

  def attivaProgramma():	
    for prog in programmi:		
      #day of week
      day=datetime.datetime.today().weekday()
      
      #l'ora attuale
      timenow=datetime.datetime.now.time()
      
      #build program time 
      hourMinute=prog[1].slpit(":")
      timecheck tetime.datetime.time(hourMinute[0],hourMinute[1],0,0)
      
      #check if day and time is now return OFF or ON
        if (days[prog[0]]==day & timenow>=timecheck):
          return prog[2]
       return false

#p=programmatore()
#p.leggiProgramma()
#print(attivaProgramma())
		
	


	  
	  
	  
  

