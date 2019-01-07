# -*- coding: utf-8 -*-

#!/usr/bin/env python

__author__ =    "Weqaar Janjua"
__copyright__ = "Copyright (C) 2019 Weqaar Janjua / Slack"
__revision__ =  "$Id$"
__version__ =   "1.1"
__project__ =   "c0mbat"

#imports
from multiprocessing import Pool, Process, Event
from multiprocessing.managers import BaseManager
import time, os, psutil, subprocess, gc, sys, io, signal, itertools, re, errno
import thread
import argparse
import json
#from packages.runtime.sysinit import *
import packages.runtime.sysinit as sysinit
from packages.conf.configinit import *
import packages.queue.initqueues as initqueues
import packages.artifacts.initartificats as initartifacts
import packages.inventory.initinventory as initinventory
import packages.globalvars as globalvars


#variables
_log_file_format = 'text/plain'
_log_file_ext = '.txt'
_json_objects_store = 'json_objects_store/'


class ProcessManager(BaseManager): pass

def main():
    _print_header()

    reload(sys)
    sys.setdefaultencoding("utf-8")

    globalvars._global_conf_name =  __project__ + '.conf'

    #initialize Configuration from .conf
    _conf_object = SysConfig(globalvars._global_conf_name)
    _conf_object.runinit()

    #initialize System
    #_sysinit = SysInit()
    sysinit.SysInit()

    #Initialize Queues|Topics
    initqueues._init_queues()

    _cli_parser = argparse.ArgumentParser(description='c0mbat cli: ' + sys.argv[0])
    _cli_parser.add_argument('-v', '--validate', help='Validate deployment configurations\n')
    _cli_parser.add_argument('-d', '--deploy', help='Trigger Deployment(s)')
    _cli_parser.add_argument('-l', '--listhosts', help='List target hosts')
    _cli_args = _cli_parser.parse_args()

    #if (_cli_args.validate is None) or (_cli_args.deploy is None) or (_cli_args.listhosts is None):
    #	_cli_parser.print_help()
    #	sys.exit(1)

    #Initialize Inventory and Artifacts cache
    initinventory.InitInventory()
    initartifacts.InitArtifacts()

    print "Inventory Cache: " + json.dumps(globalvars._inventory_cache)

    #Spawn Threads
    global plist
    plist = []
    _inventory_dict = dict()
    _artifacts_dict = dict()
    ProcessManager.register('getdict_inventory', callable=lambda:_inventory_dict)
    ProcessManager.register('getdict_artifacts', callable=lambda:_artifacts_dict)
    _process_manager = ProcessManager(address=(globalvars._ipc_host, globalvars._ipc_port), authkey=globalvars._ipc_key)
    _process_manager.start()
    _init_process_manager()


    #get no. of hosts
    #spawn thread for each host


    globalvars._stats_logger.debug("Initializing c0mbat...")

    globalvars._stats_logger.debug("Process complete.")
    print "Process complete.\n"
    sys.exit(0)


def _init_process_manager():
    signal.signal(signal.SIGUSR1, signalHandler)
    globalvars._stats_logger.debug("Initialized process manager, initializing signal handlers")


def signalHandler(signum, stack):
    globalvars._stats_logger.debug("Signal Received in main: " + str(signum))
    for _process in plist:
        globalvars._stats_logger.debug("sending signal " + str(signum) + " to: " + str(_process.pid))
        os.kill(_process.pid, signal.SIGUSR1)
    raise SystemExit('Signal Received, Exiting!')


def _print_header():
    _marker = '---------------------------------------------------------'
    _n = '\n'
    print _n + _marker
    print "Process name: " + __file__ + _n
    print "Author: " + __author__ + _n
    print "Copyright: " + __copyright__ + _n
    print "Project: " + __project__ + _n
    print "Version: " + __version__ + _n
    print "Process ID: " + str(os.getpid())
    print _marker + _n
    return

if __name__ == '__main__':
    main()

