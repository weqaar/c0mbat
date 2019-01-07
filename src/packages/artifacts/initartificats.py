# -*- coding: utf-8 -*-

import packages.globalvars as globalvars
import sys, traceback, inspect
import os, sys, json


class InitArtifacts():

    def __init__(self):
        if self.syncArtifacts() is False:
            sys.exit(1)
        if self.validateArtifacts() is False:
            sys.exit(1)

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

    def validateArtifacts(self):
        for _artifact in globalvars._artifacts_cache.keys():
            if ("manual" in globalvars._artifacts_cache[_artifact].get("pkg-type")) and (not os.path.isdir(globalvars._artifacts_dir + "/" + _artifact)):
                globalvars._error_logger.debug("Artifact not found: " + _artifact)
                return False
        return True

    def getArtifactsHash(self):
        pass
