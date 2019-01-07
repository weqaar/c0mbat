# -*- coding: utf-8 -*-

import packages.globalvars as globalvars
import sys, traceback, inspect
import json


class InitArtifacts():

    def __init__(self):
        self.syncArtifacts()

    def syncArtifacts(self):
        try:
            with open(globalvars._artifacts_dir + "/" + globalvars._artifacts_file, 'r') as artifactsfile:
                globalvars._artifacts_cache = json.load(artifactsfile)
            artifactsfile.close()
            return True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            _func_trace = inspect.currentframe().f_back.f_code
            _exception_struct = "Exception:info:" +  "Function:" + str(sys._getframe().f_code.co_name) + "\n" + \
                                "File: " + str(_func_trace.co_filename) + "\n" + \
                                "Line: " + str(exc_tb.tb_lineno) + "\n" + \
                                "StackTrace: " + str(e)
            globalvars._error_logger.debug(_exception_struct)
            return False
        
