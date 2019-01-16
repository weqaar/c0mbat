# -*- coding: utf-8 -*-

import ConfigParser

class Parser_Functions(object):

    _instance = None
    global conf_file
    conf_map = None
    
    def __new__(cls, *args, **kwargs):
    	if not cls._instance:
	    cls._instance = super(Parser_Functions, cls).__new__(cls, *args, **kwargs)
	return cls._instance

    def __init__(self, _config_file):
        self.conf_file = _config_file
        self.sys_params = {}
        self.parser_init()

    def parser_init(self):
	self.conf = ConfigParser.ConfigParser()
	self.conf.read(self.conf_file)

    def ConfigSectionMap(self):
	sections = self.conf.sections()
	for section in sections:
		options = self.conf.options(section)
		for option in options:
			try:
				self.sys_params[option] = self.conf.get(section, option)
			except:
				self.sys_params[option] = None
	return self.sys_params

    def getSectionOption(self, _section, _option):
	return self.conf.get(_section, _option)

    def getSections(self):
	return self.conf.sections()

    def getSectionsDict(self):
        _config_dict = dict()
        for _section in self.getSections():
            _config_dict[_section] = {}
            for _item in self.conf.items(_section):
                _config_dict[_section].update({_item[0]: _item[1]})
	return _config_dict

    def SyncConfigFileSystem(self, _config_db_instance):
        for _section in _config_db_instance.keys():
            if _section in self.getSections():
                for _param, _value in _config_db_instance.get(_section).iteritems():
                    self.conf.set(_section, _param, _value)
        with open(self.conf_file, 'w') as configfileout:
            self.conf.write(configfileout)
        configfileout.close()

