# -*- coding: utf-8 -*-

import os, sys, io
import logging, logging.handlers
from packages.conf.sysconfigx import *
import packages.globalvars as globalvars


class SysInit():

    def __init__(self):
        self._init_fs_struct()
        self.init_loggers()
        self._init_shared_datastructs()

    def init_loggers(self):
        #Stats Logger
        _stats_logger = logging.getLogger(globalvars._LOGTITLE_STATS)
        _stats_logger.setLevel(globalvars._LOGLEVEL)
        _stats_log_file = logging.FileHandler(globalvars._logs_dir + "/" + globalvars._SYSLOGFILE_STATS)
        _stats_log_file.setLevel(globalvars._LOGLEVEL)
        _stats_log_formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        _stats_log_file.setFormatter(_stats_log_formatter)
        _stats_logger.addHandler(_stats_log_file)
        globalvars._stats_logger = _stats_logger
        #Error Logger
        _error_logger = logging.getLogger(globalvars._LOGTITLE_ERROR)
        _error_logger.setLevel(globalvars._LOGLEVEL)
        _error_log_file = logging.FileHandler(globalvars._logs_dir + "/" + globalvars._SYSLOGFILE_ERROR)
        _error_log_file.setLevel(globalvars._LOGLEVEL)
        _error_log_formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        _error_log_file.setFormatter(_error_log_formatter)
        _error_logger.addHandler(_error_log_file)
        globalvars._error_logger = _error_logger
        #Debug Logger
        _debug_logger = logging.getLogger(globalvars._LOGTITLE_DEBUG)
        _debug_logger.setLevel(globalvars._LOGLEVEL)
        _debug_log_file = logging.FileHandler(globalvars._logs_dir + "/" + globalvars._SYSLOGFILE_DEBUG)
        _debug_log_file.setLevel(globalvars._LOGLEVEL)
        _debug_log_formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        _debug_log_file.setFormatter(_debug_log_formatter)
        _debug_logger.addHandler(_debug_log_file)
        globalvars._debug_logger = _debug_logger
        logging.basicConfig()


    def set_working_dir(self):
        try:
            os.chdir(globalvars._firmware_dir)
            globalvars._debug_logger.debug("Switching to working dir: " + os.getcwd())
        except OSError:
            globalvars._error_logger.debug("ERROR Switching to working directory: " + globalvars._firmware_dir + " Exiting.")
            sys.exit(1)


    def _init_fs_struct(self):
        if not os.path.exists(globalvars._runtime_dir):
            os.mkdir(globalvars._runtime_dir)
        if not os.path.exists(globalvars._logs_dir):
            os.mkdir(globalvars._logs_dir)
        if not os.path.exists(globalvars._cache_dir):
            os.mkdir(globalvars._cache_dir)
        with io.open(globalvars._runtime_dir + "/" + globalvars._pidfile, 'w', encoding="ascii") as _f:
            _f.write(unicode(str(os.getpid()) + "\n"))
            _f.close()

    def _init_shared_datastructs(self):
        globalvars._campaigns_dict = dict()

