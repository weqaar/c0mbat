# -*- coding: utf-8 -*-

import packages.globalvars as globalvars
import sys, traceback, inspect
import os, sys, signal, json
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

        with open(globalvars._cache_dir + "/" + globalvars._cache_file, 'r') as _hash_file:
            self._hash_file_cache = json.load(_hash_file)
        _hash_file.close()

        self._init_sighandlers()
        self._thread_run(self._hash_file_cache)

    def _init_sighandlers(self):
        signal.signal(signal.SIGUSR1, self.signalHandler)
        globalvars._stats_logger.debug("Initialized process manager, initializing signal handlers")

    def signalHandler(self, signum, stack):
        globalvars._stats_logger.debug("Signal Received: " + str(signum) + ", process info: " + \
                                        str(multiprocessing.current_process().name) + ", " + str(multiprocessing.current_process().pid))
        sys.exit(0)

    def _thread_run(self, _hash_file_cache):
        while True:
            if not globalvars._mp_queue0.empty():
                _host = globalvars._mp_queue0.get()
                globalvars._stats_logger.debug("Thread " + multiprocessing.current_process().name + " processing host: " + str(_host))
                _connection_object = self._create_connection_object(_host)
                _ssh_object = sshObject.SSH()
                _ssh_link = _ssh_object.ssh_connect(_connection_object)
                if _ssh_link is not False:
                    _artifacts_list = self._inventory_dict.get(_host).get("Artifacts")
                    if (len(_artifacts_list) > 0):
                        for _artifact in _artifacts_list:
                            _artifact_object = self._artifacts_dict.get(_artifact)
                            if (self._hash_file_cache[_artifact].get("deployed_host") is None):
                                self._hash_file_cache[_artifact]["deployed_host"] = []
                                self._hash_file_cache[_artifact]["deployed_host"].append(_host)
                            elif (_host not in self._hash_file_cache[_artifact].get("deployed_host")):
                                self._hash_file_cache[_artifact]["deployed_host"].append(_host)
                            elif (_host in self._hash_file_cache[_artifact].get("deployed_host")):
                                #Verify hash
                                if (self._hash_file_cache[_artifact].get("conf_hash_update") is None) and (self._hash_file_cache[_artifact].get("fs_hash_update") is None):
                                    continue
                            #APT handler
                            if "apt" in _artifact_object.get("pkg-type"):
                                if _artifact_object.get("pre-deploy-trigger") is not None:
                                    _datax, _error = _ssh_object._exec_cmd(_ssh_link, \
                                                    self._artifact_manager("apt", _artifact_object.get("pre-deploy-trigger")))
                                _datax, _error = _ssh_object._exec_cmd(_ssh_link, \
                                                _data = self._artifact_manager("apt", _artifact_object.get("pkg-action"), _data = \
                                                _artifact_object.get("pkg-name")))
                                if _artifact_object.get("post-deploy-trigger") is not None:
                                    _datax, _error = _ssh_object._exec_cmd(_ssh_link, \
                                                    _data = self._artifact_manager("service", _artifact_object.get("post-deploy-trigger"), \
                                                    _artifact_object.get("service-name")))
                            
                            #MANUAL handler
                            elif "manual" in _artifact_object.get("pkg-type"):
                                if "install" in _artifact_object.get("pkg-action"):
                                    #check if _artifact_object.get("pkg-path") exists
                                    if _ssh_object._sftp_dir_check(_ssh_link, _artifact_object.get("pkg-path")) is False:
                                        break
                                    _ssh_object._scp_copy(_ssh_link, globalvars._artifacts_dir + "/" + _artifact, _artifact_object.get("pkg-path"))
                                    #Permissions from metadata
                                    _perms = _artifact_object.get("metadata").get("mode")
                                    if (_perms is not None):
                                        _ssh_object._exec_cmd(_ssh_link, _data = "chmod -R " + _perms + " " + _artifact_object.get("pkg-path") + \
                                                              "/*") 
                                elif "remove" in _artifact_object.get("pkg-action"):
                                    _ssh_object._exec_cmd(_ssh_link, _data = "rm -rf " + _artifact_object.get("pkg-path") + "/" + \
                                                        _artifact_object.get("pkg-name"))
                    _ssh_link.close()
                    #Update hash file
                    with open(globalvars._cache_dir + "/" + globalvars._cache_file, 'w') as _f:
                        json.dump(self._hash_file_cache, _f, sort_keys = True, indent = 4, ensure_ascii=True)
                    _f.close()
                else:
                    globalvars._stats_logger.debug("Error in Thread " + multiprocessing.current_process().name + " processing host: " + str(_host))
                break

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
                "host"      : None if _host_inventory.get("Address") is None else _host_inventory.get("Address").strip(),
                "username"  : None if _host_inventory.get("Auth").get("username") is None else _host_inventory.get("Auth").get("username").strip(),
                "password"  : None if _host_inventory.get("Auth").get("password") is None else _host_inventory.get("Auth").get("password").strip(),
                "key"       : None if _host_inventory.get("Auth").get("key") is None else _host_inventory.get("Auth").get("key").strip()
                }
        return _connection_object

    def _artifact_manager(self, _pkgmgr, _action, _data=None):
        if "apt" in _pkgmgr:
            if _data is not None:
                if "remove" in _action.strip():
                    _cmd = "apt-get -y " + "uninstall" + " " + _data.strip()
                else: 
                    _cmd = "apt-get -y " + _action.strip() + " " + _data.strip()
            else:
                _cmd = "apt-get -y " + _action.strip()
        elif "service" in _pkgmgr:
            _valid_service_ations = [x.strip() for x in globalvars._valid_service_ations.split(',')]
            if str(_action.strip()) in _valid_service_ations:
                _cmd = "service " + _data.strip() + " " + _action.strip()
            else:
                globalvars._error_logger.debug("Invalid service action: " + str(_action.strip()))
                _cmd = None
        else:
            _cmd = None
        return _cmd

