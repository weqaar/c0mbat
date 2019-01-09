# -*- coding: utf-8 -*-

import packages.globalvars as globalvars
import sys, traceback, inspect
import os, sys, json, time, copy
import checksumdir
import hashlib, md5
from shutil import copyfile

class Cache():

    def __init__(self):
        self.hashInit()

    """
    {
        artifact : {
            conf_hash : <>,
            fs_hash : <>,
            deployed_host : []
            },
        artifact : {
            conf_hash : <>,
            fs_hash : <>,
            deployed_host : []
            }
    }
    """

    def hashInit(self):
        
        _hash_object = {}

        #Read hash file
        if os.path.isfile(globalvars._cache_dir + "/" + globalvars._cache_file):
            with open(globalvars._cache_dir + "/" + globalvars._cache_file, 'r') as _hash_file:
                _hash_file_cache = json.load(_hash_file)
            _hash_file.close()
            _hash_object = copy.deepcopy(_hash_file_cache)

            #Take hash of Artifacts conf section
            for _artifact in globalvars._artifacts_cache.keys():
                _conf_hash = hashlib.md5(json.dumps(globalvars._artifacts_cache.get(_artifact), sort_keys=True)).hexdigest()
                _hash_object[_artifact]["conf_hash"] = _conf_hash
                if _conf_hash == _hash_file_cache.get(_artifact).get("conf_hash"):
                    _hash_object[_artifact]["conf_hash_update"] = None
                else:
                    _hash_object[_artifact]["conf_hash_update"] = 1
            #Take hash of Artifact FS
            for _artifact in globalvars._artifacts_cache.keys():
                if ("manual" in globalvars._artifacts_cache.get(_artifact).get("pkg-type")) \
                        and ("remove" not in globalvars._artifacts_cache.get(_artifact).get("pkg-action")):
                    _fs_hash = checksumdir.dirhash(globalvars._artifacts_dir + "/" + _artifact)
                    _hash_object[_artifact]["fs_hash"] = _fs_hash
                    if _fs_hash == _hash_file_cache.get(_artifact).get("fs_hash"):
                        _hash_object[_artifact]["fs_hash_update"] = None
                    else:
                        _hash_object[_artifact]["fs_hash_update"] = 1
        else:
            _hash_file_cache = copy.deepcopy(_hash_object)
            #Take hash of Artifacts conf section
            for _artifact in globalvars._artifacts_cache.keys():
                _conf_hash = hashlib.md5(json.dumps(globalvars._artifacts_cache.get(_artifact), sort_keys=True)).hexdigest()
                _hash_object.update( {_artifact : {"conf_hash" : _conf_hash }} )
                _hash_object[_artifact].update( {"conf_hash_update": None} )
            #Take hash of Artifact FS
            for _artifact in globalvars._artifacts_cache.keys():
                if ("manual" in globalvars._artifacts_cache.get(_artifact).get("pkg-type")) \
                        and ("remove" not in globalvars._artifacts_cache.get(_artifact).get("pkg-action")):
                    _fs_hash = checksumdir.dirhash(globalvars._artifacts_dir + "/" + _artifact)
                    _hash_object[_artifact].update( {"fs_hash" : _fs_hash } )
                    _hash_object[_artifact].update( {"fs_hash_update": None} )

        if os.path.isfile(globalvars._cache_dir + "/" + globalvars._cache_file):
            copyfile(globalvars._cache_dir + "/" + globalvars._cache_file, globalvars._cache_dir + "/" + globalvars._cache_file + ".last")

        with open(globalvars._cache_dir + "/" + globalvars._cache_file, 'w') as _f:
            json.dump(_hash_object, _f, sort_keys = True, indent = 4, ensure_ascii=True)
        _f.close()

        #For Dedugging the JSON Object (dump on stdout) uncomment the next line
        #print json.dumps(_hash_object, _f, sort_keys = True, indent = 4, ensure_ascii=True)
