'''
Created on 18 nov 2019

@author: sasanelli
'''

import shlex, subprocess
from subprocess import call

class temp_reader(object):
    '''
    contiene un thread che legge sempre la temperatura
    '''
    def execute(self,command):
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        print(err)
        return out
    
    def readTemp(self):
        rawTemp=self.execute(["temper-poll"])
        print(rawTemp)
        temp = float(str(rawTemp,'utf-8')[27:31])
        return temp

    def __init__(self):
        '''
        Constructor
        '''
tr=temp_reader()
print(str(tr.readTemp()))