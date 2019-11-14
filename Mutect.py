import os
import sys
import configparser
import argparse

class Myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
    def optionxform(self, optionstr):
        return optionstr


if __name__=="__main__":
    parser=argparse.ArgumentParser("Run GATK Mutect")
    parser.add_argument("-b","--bam",help="bam file",required=True)
    parser.add_argument("-l","--bed",help="target region bed file")
    parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
    parser.add_argument("-p","--prefix",help="prefix of output",default="out")
    parser.add_argument("-c","--config",help="config file",required=True)
    args=parser.parse_args()

config = configparser.RawConfigParser()
config.read("config.ini")
print(config.get('software','GATK3.7'))