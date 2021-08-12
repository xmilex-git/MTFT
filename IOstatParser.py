from Configuration import *
from Tenant_Table import *
import subprocess
import time
import threading

class io_stat_parser(threading.Thread):
    def __init__(self,Table:tenants):
        threading.Thread.__init__(self)
        self.Table=Table
        self.time=time.time()

    def run(self):
        iostat_process=subprocess.Popen('iostat -px 1'.split(),stdout=subprocess.PIPE)
        for c in iter(iostat_process.stdout.readline,b''):
            line=c.decode()
            sl=line.split()
            t=time.time()-self.time
            if len(sl)==21 and t>1.5:
                name=sl[0]
                if name in self.Table.devs:
                    rkb,wkb=float(sl[2]),float(sl[8])
                    self.Table.update_tenant(name,rkb,wkb)
            
            
            