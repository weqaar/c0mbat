# -*- coding: utf-8 -*-

#!/usr/bin/env python

__author__ =    "Weqaar Janjua"
__copyright__ = "Copyright (C) 2019 Weqaar Janjua / Slack"
__revision__ =  "$Id$"
__version__ =   "3.6"
__project__ =   "c0mbat"

#imports
from multiprocessing import Pool, Process, Event
from multiprocessing.managers import BaseManager
import time, os, psutil, subprocess, sys, io, signal, argparse, json
import packages.runtime.sysinit as sysinit
from packages.conf.configinit import *
import packages.queue.initqueues as initqueues
import packages.artifacts.initartificats as initartifacts
import packages.inventory.initinventory as initinventory
import packages.remoteaccess.ssh as sshObject
import packages.globalvars as globalvars
import packages.threads.deploymentworker as workerthread
import packages.runtime.cache as hashcache


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
    sysinit.SysInit()

    #Initialize Queues|Topics
    initqueues._init_queues()

    _cli_parser = argparse.ArgumentParser(description='c0mbat cli: ' + sys.argv[0])
    _cli_parser.add_argument('-v', '--validate', help='Validate deployment configurations', action='store_true')
    _cli_parser.add_argument('-d', '--deploy', help='Trigger Deployment(s)', action='store_true')
    _cli_parser.add_argument('-l', '--listhosts', help='List target hosts', action='store_true')
    _cli_args = _cli_parser.parse_args()

    if ((_cli_args.validate is False) and (_cli_args.deploy is False) and (_cli_args.listhosts is False)):
        _cli_parser.print_help()     
        sys.exit(0)
    
    #Spawn Threads
    global plist
    plist = []

    #spawn thread for each host
    if (_cli_args.validate):
        print "\nValidating Inventory..."
        if (initinventory.InitInventory()):
            print "Inventory validation: " + "Passed"
        print "\nValidating Artifacts..."
        if (initartifacts.InitArtifacts()):
            print "Artifacts validation: " + "Passed"
        print "\n"
        
    elif (_cli_args.listhosts):
        #Initialize Inventory and Artifacts cache
        initinventory.InitInventory()
        initartifacts.InitArtifacts()
        print ("\nList of hosts in inventory:\n")
        for _host in globalvars._inventory_cache.keys():
            print str(_host) + ": " + str(globalvars._inventory_cache.get(_host).get("Address")) + ", Disabled: " + \
                  str(globalvars._inventory_cache.get(_host).get("disabled"))
        print "\n"

    elif (_cli_args.deploy):
        #Initialize Inventory and Artifacts cache
        initinventory.InitInventory()
        initartifacts.InitArtifacts()
        _inventory_dict = dict()
        _artifacts_dict = dict()
        _inventory_dict = globalvars._inventory_cache.copy()
        _artifacts_dict = globalvars._artifacts_cache.copy()
        hashcache.Cache()
        ProcessManager.register('getdict_inventory', callable=lambda:_inventory_dict)
        ProcessManager.register('getdict_artifacts', callable=lambda:_artifacts_dict)
        _process_manager = ProcessManager(address=(globalvars._ipc_host, globalvars._ipc_port), authkey=globalvars._ipc_key)
        _process_manager.start()
        _init_process_manager()

        for _host in _inventory_dict.keys():
            if _inventory_dict.get(_host).get("disabled") is False:
                globalvars._mp_queue0.put(_host)
                _thread = Process(name='_thread_' + _host, target=workerthread.DeploymentThread)
                _thread.start()
                plist.append(_thread)

        if len(plist) > 0:
            for process in plist:
                process.join()

    globalvars._stats_logger.debug("Process complete.")
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

