from Configuration import *
from Cgroups import *
from Tenant_Table import *
from IOstatParser import *
from Monitor import *

if __name__=='__main__':
    CFGS=configuration()
    CGROUPS=cgroups(CFGS)
    TENANT_TABLE=tenants(CFGS)
    IOPARSER=io_stat_parser(TENANT_TABLE)
    MONITOR=monitor(CFGS,CGROUPS,TENANT_TABLE)
    IOPARSER.start()
    MONITOR.start()
    
