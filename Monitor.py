from Configuration import *
from Tenant_Table import *
from Cgroups import *
import threading
import time
from os.path import join

class monitor(threading.Thread):
    def __init__(self,config:configuration,cgrp:cgroups,table:tenants):
        threading.Thread.__init__(self)
        self.slice=int(config.args['monitoring_slice'])
        self.debug=int(config.args['debug'])
        self.cgroups=cgrp
        self.start_time=time.time()
        self.mode=0
        self.tenant_table=table
        self.log_file=open(join(config.args['log_dir'],config.args['workload']+'.log'),'w')

    def run(self):
        
        while True:
            self.tenant_table.update_min_bw()
            self.tenant_table.chk_active()
            time.sleep(self.slice)
            t=time.time()-self.start_time
            if self.mode==0:
                flag=self.monitor_init()
                if flag:
                    self.mode=1
            else:
                self.monitor_allot()
            
            
    
    def monitor_init(self):
        time.sleep(self.slice*2)
        return True

    def monitor_allot(self):
        active_tenants=[Tenant for Tenant in self.tenant_table.Table if Tenant.active]
        perf=[]
        total_perf=0.0
        for Tenant in active_tenants:
            Tenant:tenant
            p=(Tenant.df.rkbps.mean()+Tenant.df.wkbps.mean())/(Tenant.orig_rkbps+Tenant.orig_wkbps)
            perf.append([Tenant,p])
            total_perf+=p
        n_tenants=len(active_tenants)
        avg_perf=total_perf/n_tenants
        
        for Tenant,p in perf:
            if p>avg_perf:
                rlim=(n_tenants*Tenant.orig_rkbps*p-(n_tenants-1)*Tenant.min_rkbps)*1024
                wlim=(n_tenants*Tenant.orig_wkbps*p-(n_tenants-1)*Tenant.min_wkbps)*1024
                self.cgroups.throttle(Tenant.cname,Tenant.dev,rlim,wlim)
            else:
                self.cgroups.unthrottle(Tenant.cname,Tenant.dev)
        
        self.mode=0
                
                
    
        

