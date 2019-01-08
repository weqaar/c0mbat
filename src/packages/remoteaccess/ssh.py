# -*- coding: utf-8 -*-

import packages.globalvars as globalvars
import sys, traceback, inspect
import os, sys, json, time
import paramiko
from paramiko import SSHClient
import getpass


class SSH():

    """
    Connection Object
        {   host:
            username:
            password:
            key:
        }
    """
    """
    def __init__(self, _connection_object=None):
        if (_connection_object is None) or (type(_connection_object) is not dict):
            globalvars._error_logger.debug("SSH: Invalid _connection_object: " + str(_connection_object))
            return False
    """
    def __init__(self):
        pass
        """
        _ssh_link = self.ssh_connect(_connection_object)
        if _ssh_link is False:
            globalvars._error_logger.debug("SSH: Error establishing connection: " + str(_connection_object["host"]))
            sys.exit(1)
        else:
            return _ssh_link
        """

    def ssh_connect(self, _connection_object):
        if (_connection_object is None) or (type(_connection_object) is not dict):
            globalvars._error_logger.debug("SSH: Invalid _connection_object: " + str(_connection_object))
            return False
        if (_connection_object["host"] is None):
            globalvars._error_logger.debug("SSH: Invalid Hostname: " + str(_connection_object["host"]))
            return False
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #Case-1: username = None, Key = None, Password = None|Valid
            if (_connection_object["username"] is None) and (_connection_object["key"] is None):
                client.connect(_connection_object["host"], username=getpass.getuser())
            #Case-2: username = None, Key = Valid, Password = None|Valid
            elif (_connection_object["username"] is None) and (_connection_object["key"] is not None):
                if ((os.path.exists(_connection_object["key"])) and (os.path.getsize(_connection_object["key"]) > 0)):
                    client.connect(_connection_object["host"], username=getpass.getuser(), key_filename=_connection_object["key"])
                else:
                    globalvars._error_logger.debug("SSH: Invalid ssh key: " + str(_connection_object["key"]) + ", host: " + str(_connection_object["host"]))
                    return False
            #Case-3: username = Valid, Key = None, Password = None
            elif (_connection_object["username"] is not None) and (_connection_object["key"] is None) and (_connection_object["password"] is None):
                client.connect(_connection_object["host"], username=_connection_object["username"])
            #Case-4: username = Valid, Key = Valid, Password = None|Valid
            elif (_connection_object["username"] is not None) and (_connection_object["key"] is not None):
                if ((os.path.exists(_connection_object["key"])) and (os.path.getsize(_connection_object["key"]) > 0)):
                    client.connect(_connection_object["host"], username=_connection_object["username"], key_filename=_connection_object["key"])
                else:
                    globalvars._error_logger.debug("SSH: Invalid username/ssh key, username: " + str(_connection_object["username"]) + ", key: " + \
                                                   str(_connection_object["key"]) + ", host: " + str(_connection_object["host"]))
                    return False
            #Case-5: username = Valid, Key = None, Password = Valid [default use case]
            elif (_connection_object["username"] is not None) and (_connection_object["key"] is None) and (_connection_object["password"] is not None):
                client.connect(_connection_object["host"], username=_connection_object["username"], password=_connection_object["password"])
                
            return client
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            _func_trace = inspect.currentframe().f_back.f_code
            _exception_struct = "Exception:info:" +  "Function:" + str(sys._getframe().f_code.co_name) + "\n" + \
                                "File: " + str(_func_trace.co_filename) + "\n" + \
                                "Line: " + str(exc_tb.tb_lineno) + "\n" + \
                                "StackTrace: " + str(e)
            globalvars._error_logger.debug(_exception_struct)
            return False


    def _exec_cmd(self, _ssh_connection_instance, _cmd):
        if _ssh_connection_instance is None:
            print "Problem!!!"
        try:
            stdin, stdout, stderr = _ssh_connection_instance.exec_command(_cmd)
            while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
                time.sleep(1)
 
            _data = stdout.readlines()
            _error = stderr.readlines()
            return (_data, _error)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            _func_trace = inspect.currentframe().f_back.f_code
            _exception_struct = "Exception:info:" +  "Function:" + str(sys._getframe().f_code.co_name) + "\n" + \
                                "File: " + str(_func_trace.co_filename) + "\n" + \
                                "Line: " + str(exc_tb.tb_lineno) + "\n" + \
                                "StackTrace: " + str(e)
            globalvars._error_logger.debug(_exception_struct)
            return False


    def _sftp(self, _ssh_connection_instance, _data):
        sftp = paramiko.SFTPClient.from_transport(_ssh_connection_instance)
        print ("Copying file: %s to path: %s" %("src", "dst"))
        sftp.put("src", "dst")
        sftp.close()
        return True

