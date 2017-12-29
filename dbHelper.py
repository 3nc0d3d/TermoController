import sqlite3
class dbHelper:
    def open(self,dbname):        
        conn= sqlite3.connect(dbname)
        self.connection = conn

    def excute_query(self,query):
        curs = self.connection.cursor()
        print (query)
        curs.execute(query)
        return curs.fetchall
    def insert(self,table,campi,values):
        query="INSERT INTO "+table + "(" + campi + ") values (" + values +")"

 class Task(dbHelper,name):
         maxposition=parent.execute_query("select max(position) from task")
         parent.insert("task",["name","data","time","durarion","position","parenttask","category""busy"],[n)
    



    


