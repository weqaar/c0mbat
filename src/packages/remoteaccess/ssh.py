# -*- coding: utf-8 -*-

import packages.globalvars as globalvars
import sys, traceback, inspect
import os, sys, json, time
import paramiko
from paramiko import SSHClient
from scp import SCPClient
import getpass


class SSH():

    def __init__(self):
        pass

    """
    Five (5) Use Cases:
        1 - username = None,    Key = None,     Password = None|Valid
        2 - username = None,    Key = Valid,    Password = None|Valid
        3 - username = Valid,   Key = None,     Password = None
        4 - username = Valid,   Key = Valid,    Password = None|Valid
        5 - username = Valid,   Key = None,     Password = Valid [default use case]
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
            #Case-1
            if (_connection_object["username"] is None) and (_connection_object["key"] is None):
                client.connect(_connection_object["host"], username=getpass.getuser())
            #Case-2
            elif (_connection_object["username"] is None) and (_connection_object["key"] is not None):
                if ((os.path.exists(_connection_object["key"])) and (os.path.getsize(_connection_object["key"]) > 0)):
                    client.connect(_connection_object["host"], username=getpass.getuser(), key_filename=_connection_object["key"])
                else:
                    globalvars._error_logger.debug("SSH: Invalid ssh key: " + str(_connection_object["key"]) + ", host: " + str(_connection_object["host"]))
                    return False
            #Case-3
            elif (_connection_object["username"] is not None) and (_connection_object["key"] is None) and (_connection_object["password"] is None):
                client.connect(_connection_object["host"], username=_connection_object["username"])
            #Case-4
            elif (_connection_object["username"] is not None) and (_connection_object["key"] is not None):
                if ((os.path.exists(_connection_object["key"])) and (os.path.getsize(_connection_object["key"]) > 0)):
                    client.connect(_connection_object["host"], username=_connection_object["username"], key_filename=_connection_object["key"])
                else:
                    globalvars._error_logger.debug("SSH: Invalid username/ssh key, username: " + str(_connection_object["username"]) + ", key: " + \
                                                   str(_connection_object["key"]) + ", host: " + str(_connection_object["host"]))
                    return False
            #Case-5
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


    def _exec_cmd(self, _ssh_connection_instance, _data):
        try:
            stdin, stdout, stderr = _ssh_connection_instance.exec_command(_data)
            while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
                time.sleep(0.5)
 
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


    def _scp_copy(self, _ssh_connection_instance, _src, _dst):
        try:
            scp = SCPClient(_ssh_connection_instance.get_transport(), progress=self._progress_stdout)
            _currdir = os.getcwd()
            os.chdir(_src)
            scp.put(".", recursive=True, remote_path=_dst) 
            scp.close()
            os.chdir(_currdir)
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

    def _progress_stdout(self, filename, size, sent):
        print ("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100))

    def _sftp_dir_check(self, _ssh_connection_instance, _data):
        try:
            sftp = _ssh_connection_instance.open_sftp()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            _func_trace = inspect.currentframe().f_back.f_code
            _exception_struct = "Exception:info:" +  "Function:" + str(sys._getframe().f_code.co_name) + "\n" + \
                                "File: " + str(_func_trace.co_filename) + "\n" + \
                                "Line: " + str(exc_tb.tb_lineno) + "\n" + \
                                "StackTrace: " + str(e)
            globalvars._error_logger.debug(_exception_struct)
            return False
        try: 
            sftp.stat(_data)
        except Exception as e:
            globalvars._stats_logger.debug("creating dir that did not exist on remote: " + str(_data))
            self.exec_cmd(_ssh_connection_instance, "mkdir -p " + _data)
            return True

