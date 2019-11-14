import os
import sys
import configparser
class Myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
    def optionxform(self, optionstr):
        return optionstr
config = configparser.RawConfigParser()
config.read("config.ini")
print(config.get('software','GATK3.7'))