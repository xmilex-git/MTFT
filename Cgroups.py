from Configuration import configuration
import subprocess
from os.path import join,isfile

class cgroups():
    def __init__(self,cfg:configuration):
        self.cgroup_path=cfg.args['cgroups']

        self.cid_map=self.get_cid_map()
        self.dev_map=self.get_dev_map()
        
    def throttle(self,cname:str,dev:str,rb:int,wb:int):
        cid=self.cid_map[cname]
        dmajor,dminor=self.dev_map[dev[:-2]]
        path=join(self.cgroup_path,cid)
        if rb>0:
            rpath=join(path,'blkio.throttle.read_bps_device')
            if isfile(rpath):
                with open(rpath,'w') as f:
                    l='%d:%d %d'%(dmajor,dminor,rb)
                    f.write(l)
        if wb>0:
            wpath=join(path,'blkio.throttle.write_bps_device')
            if isfile(wpath):
                with open(wpath,'w') as f:
                    l='%d:%d %d'%(dmajor,dminor,wb)
                    f.write(l)
    
    def unthrottle(self,cname:str,dev:str):
        cid=self.cid_map[cname]
        dmajor,dminor=self.dev_map[dev[:-2]]
        path=join(self.cgroup_path,cid)
        rpath=join(path,'blkio.throttle.read_bps_device')
        wpath=join(path,'blkio.throttle.write_bps_device')
        rb=1024**4
        wb=1024**4
        if isfile(rpath):
                with open(rpath,'w') as f:
                    l='%d:%d %d'%(dmajor,dminor,rb)
                    f.write(l)
        if isfile(wpath):
                with open(wpath,'w') as f:
                    l='%d:%d %d'%(dmajor,dminor,wb)
                    f.write(l)

    def get_cid_map(self):
        fork1=subprocess.Popen("sudo docker ps -a --no-trunc".split(),stdout=subprocess.PIPE)
        ls=fork1.stdout.readlines()
        ret={}
        for l in ls:
            sl=l.decode().split()
            ret[sl[-1]]=sl[0]
        return ret

    def get_dev_map(self):
        map=dict()
        with open("/proc/partitions","r") as f:
            lines=f.readlines()
            for line in lines:
                if line == lines[0] or line == lines[1]:
                    continue
                splited_line=line.split()
                map[splited_line[3]]=(int(splited_line[0]),int(splited_line[1]))
        return map

