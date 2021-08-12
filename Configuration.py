import configparser
import argparse
import json
import os

class configuration():
    def __init__(self):
        self.args=dict()
        self.argparser()
        self.configparser()
        self.jsonparser()
        for key in self.args.keys():
            if self.args[key]==None:
                print("WARNING :: Argument %s is None."%(key))
                input("Do you want to continue?..")

    def argparser(self):
        ap=argparse.ArgumentParser()
        ap.add_argument('--monitoring_slice',type=int)
        ap.add_argument('--config',type=str)
        ap.add_argument('--debug',type=int)
        ap.add_argument('--workload',type=str)
        ap.add_argument('--cgroups',type=str)
        ap.add_argument('--tenants',type=str)
        ap.add_argument('--log_dir',type=str)
        ap.add_argument('--practical_windowsz',type=int)
        apdict=vars(ap.parse_args())
        for key in apdict.keys():
            self.args[key]=apdict[key]

    def configparser(self):
        cp=configparser.ConfigParser()
        if self.args['config']==None or not os.path.isfile(self.args['config']):
            return
        cp.read(self.args['config'])
        for section in cp.sections():
            for option in cp.options(section):
                if self.args[option]==None:
                    self.args[option]=cp.get(section,option)

    def jsonparser(self):
        if self.args['tenants']==None or not os.path.isfile(self.args['tenants']):
            return
        f=open(self.args['tenants'])
        jp=json.load(f)
        self.args['Tenants']=jp['Tenants']
