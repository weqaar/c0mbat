# -*- coding: utf-8 -*-

import packages.globalvars as globalvars
import sys, traceback, inspect
import os, sys, json, signal
import paramiko
from paramiko import SSHClient
import getpass
from multiprocessing.managers import BaseManager
import packages.remoteaccess.ssh as sshObject
import multiprocessing

class ProcessManager(BaseManager): pass

class DeploymentThread():

    def __init__(self):
        ProcessManager.register('getdict_inventory')
        ProcessManager.register('getdict_artifacts')
        self._process_manager = ProcessManager(address=(globalvars._ipc_host, globalvars._ipc_port), authkey=globalvars._ipc_key)
        self._process_manager.connect()
        self._inventory_dict = self._process_manager.getdict_inventory()
        self._artifacts_dict = self._process_manager.getdict_artifacts()
        self._init_sighandlers()
        self._thread_run()

    def _init_sighandlers(self):
        signal.signal(signal.SIGUSR1, self.signalHandler)
        globalvars._stats_logger.debug("Initialized process manager, initializing signal handlers")

    def signalHandler(self, signum, stack):
        globalvars._stats_logger.debug("Signal Received: " + str(signum) + ", process info: " + \
                                        str(multiprocessing.current_process().name) + ", " + str(multiprocessing.current_process().pid))
        sys.exit(0)

    def _thread_run(self):
        while True:
            if not globalvars._mp_queue0.empty():
                _host = globalvars._mp_queue0.get()
                _connection_object = self._create_connection_object(_host)
                _ret_status = sshObject.SSH(_connection_object)
                print "SSH Status for host: " + str(_host) + " = " + str(_ret_status)
                break;

    """
    Connection Object
    {   host:
        username:
        password:
        key:
    }
    """
    def _create_connection_object(self, _host):
        _host_inventory = self._inventory_dict.get(_host)

        _connection_object = {
                "host"      : _host_inventory.get("Address"),
                "username"  : _host_inventory.get("Auth").get("username"),
                "password"  : _host_inventory.get("Auth").get("password"),
                "key"       : _host_inventory.get("Auth").get("key")
                }
        return _connection_object

