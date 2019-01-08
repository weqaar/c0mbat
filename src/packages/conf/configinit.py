# -*- coding: utf-8 -*-

from packages.conf.sysconfigx import *
import packages.globalvars as globalvars
import sys
from datetime import datetime, timedelta


class SysConfig():

    _instance = None

    def __init__(self, _conf=None):
        if _conf is None:
            print "Please specify config file.\n"
            sys.exit(1)
        else:
            _config_file = _conf
        #Parse Config Options
        globalvars._config_obj = Parser_Functions(_config_file)
        globalvars._config_obj.conf_map = globalvars._config_obj.ConfigSectionMap()


    def __new__(cls, *args, **kwargs):
    	if not cls._instance:
	    cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
	return cls._instance
    

    def runinit(self):
        #System Wide
        _section = 'SYSTEM'
        globalvars._runtime_dir = globalvars._config_obj.getSectionOption(_section, 'rundir')
        globalvars._pidfile = globalvars._config_obj.getSectionOption(_section, 'pidfile')
        globalvars._firmware_dir = globalvars._config_obj.getSectionOption(_section, 'firmware_dir')
        globalvars._ipc_key = globalvars._config_obj.getSectionOption(_section, 'ipc_key')
        globalvars._ipc_host = globalvars._config_obj.getSectionOption(_section, 'ipc_host')
        globalvars._ipc_port = int(globalvars._config_obj.getSectionOption(_section, 'ipc_port'))
        #SYSLOG
        _section = 'SYSLOG'
        globalvars._logs_dir = globalvars._config_obj.getSectionOption(_section, 'syslogdir')
        globalvars._LOGLEVEL = int(globalvars._config_obj.getSectionOption(_section, 'loglevel'))
        globalvars._SYSLOGFILE_STATS = sys.argv[0] + "." + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.stats.log'
        globalvars._SYSLOGFILE_ERROR = sys.argv[0] + "." + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.error.log'
        globalvars._SYSLOGFILE_DEBUG = sys.argv[0] + "." + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.debug.log'
        globalvars._LOGTITLE_STATS = globalvars._config_obj.getSectionOption(_section, 'logtitlestats')
        globalvars._LOGTITLE_DEBUG = globalvars._config_obj.getSectionOption(_section, 'logtitledebug')
        globalvars._LOGTITLE_ERROR = globalvars._config_obj.getSectionOption(_section, 'logtitleerror')
        #DEPLOYMENT
        _section = 'DEPLOYMENT'
        globalvars._inventory_dir = globalvars._config_obj.getSectionOption(_section, 'inventory_dir')
        globalvars._inventory_file = globalvars._config_obj.getSectionOption(_section, 'inventory_file')
        globalvars._artifacts_dir = globalvars._config_obj.getSectionOption(_section, 'artifacts_dir')
        globalvars._artifacts_file = globalvars._config_obj.getSectionOption(_section, 'artifacts_file')
        #SERVICE
        _section = 'SERVICE'
        globalvars._valid_service_ations = globalvars._config_obj.getSectionOption(_section, 'valid_service_ations')

    def ipcdict(self):
        return globalvars._config_obj.getSectionsDict()

