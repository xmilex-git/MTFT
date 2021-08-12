from Configuration import configuration
import pandas as pd
import subprocess
import math

class tenant():
    def __init__(self,workload:str,cfgs:dict):
        self.name=workload
        self.dev=cfgs['dev']
        self.cname=cfgs['cname']
        self.orig_rkbps=cfgs['orig_rkbps']
        self.orig_wkbps=cfgs['orig_wkbps']
        self.raw_data={'rkbps':[],'wkbps':[],'total_kbps':[]}
        self.min_rkbps=0.0
        self.min_wkbps=0.0
        self.active=False
        _raw_data=dict(self.raw_data)
        self.df=pd.DataFrame(_raw_data)
        
    def __str__(self) -> str:
        ret='<Tenant Object>\n'
        d=vars(self)
        for key in d.keys():
            if key!='df':
                ret+='%10s : %10s\n'%(key,str(d[key]))
        return ret
    
    def __repr__(self) -> str:
        return str(self)
    
    

    
class tenants():
    def __init__(self,cfg:configuration):
        ts=cfg.args['Tenants']
        self.devs=[]
        self.Table=[]
        for t in ts:
            for key in t.keys():
                self.Table.append(tenant(key,t[key]))
                self.devs.append(t[key]['dev'])
        self.chk_active()
    
    def chk_active(self):
        fork1=subprocess.Popen("sudo docker ps -a".split(),stdout=subprocess.PIPE)
        ls=fork1.stdout.readlines()
        ret=[]
        for l in ls:
            sl=l.decode().split()
            ret.append(sl)
        for Tenant in self.Table:
            Tenant:tenant
            for l in ret:
                if Tenant.cname in l:
                    if 'Exited' in l:
                        Tenant.active=False
                    else:
                        Tenant.active=True

    def update_tenant(self,dev,rkb,wkb):
        for Tenant in self.Table:
            if dev==Tenant.dev:
                _raw_data={'rkbps':[],'wkbps':[],'total_kbps':[]}
                
                _raw_data['rkbps'].append(rkb)
                _raw_data['wkbps'].append(wkb)
                _raw_data['total_kbps'].append(rkb+wkb)
                Tenant:tenant
                Tenant.df=pd.concat([Tenant.df,pd.DataFrame(_raw_data)],ignore_index=True)
        

    def update_min_bw(self):
        for Tenant in self.Table:
            Tenant:tenant
            if Tenant.active:
                rdf=Tenant.df[Tenant.df['rkbps']!=0.0]
                wdf=Tenant.df[Tenant.df['wkbps']!=0.0]
                
                Tenant.min_rkbps=float(rdf.rkbps.quantile(0.05))
                if math.isnan(Tenant.min_rkbps): Tenant.min_rkbps=0.0

                Tenant.min_wkbps=float(wdf.wkbps.quantile(0.05))
                if math.isnan(Tenant.min_wkbps): Tenant.min_wkbps=0.0
                

