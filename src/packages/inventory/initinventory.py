# -*- coding: utf-8 -*-

import packages.globalvars as globalvars
import sys, traceback, inspect
import json


class InitInventory():

    def __init__(self):
        if (self.syncInventory() is False):
            sys.exit(1)

        if (self.validateInventory() is False):
            sys.exit(1)


    def syncInventory(self):
        try:
            with open(globalvars._inventory_dir + "/" + globalvars._inventory_file, 'r') as inventoryfile:
                globalvars._inventory_cache = json.load(inventoryfile)
            inventoryfile.close()
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

    def validateInventory(self):
        for _item in globalvars._inventory_cache.keys():
            if (globalvars._inventory_cache.get(_item).get("Address") is None):
                globalvars._error_logger.debug("Invalid Inventory Address: " + str(globalvars._inventory_cache.get(_item).get("Address")))
                return False
        return True

