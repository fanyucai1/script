import os
import argparse
import subprocess
import configparser
class Myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
    def optionxform(self, optionstr):
        return optionstr

parser=argparse.ArgumentParser("This script will run Tumor panel.")
parser.add_argument('-i',"--ini",help="config ini file",required=True)
result=parser.parse_args()
result.ini=os.path.abspath(result.ini)

cfg =Myconf()
cfg.read(result.ini)
#################print shell command ##########################
os.chdir(cfg['dir']['outdir'])
subprocess.check_call("mkdir -p %s/shell" %(cfg['dir']['outdir']),shell=True)
################first run quality control #####################
file=open("%s/shell/QC.1.sh" %(cfg['dir']['outdir']),"w")
if not os.path.exists("%s/1.QC" %(cfg['dir']['outdir'])):
    os.mkdir("%s/1.QC" %(cfg['dir']['outdir']))
for key in cfg['sample']:
    array=cfg['sample']["%s" %(key)].split("|")
    file.write("perl %s -pe1 %s -pe2 %s -p %s -o %s/1.QC -r %s -minL %s -a %s\n"
                         %(cfg['sub']['qc'],array[0],array[1],key,cfg['dir']['outdir'],cfg['par']['readlen'],cfg['par']['minlen'],cfg['par']['adaptor']))
###############second run pre GATK###############################
file=open("%s/shell/pre_GATK.2.sh" %(cfg['dir']['outdir']),"w")
if not os.path.exists("%s/2.Mapping" %(cfg['dir']['outdir'])):
    os.mkdir("%s/2.Mapping" %(cfg['dir']['outdir']))
for key in cfg['sample']:
    if os.path.exists("%s" % (cfg['bed']['target'])):
        file.write("perl %s -a %s/1.QC/%s_1.clean.fq.gz -b %s/1.QC/%s_2.clean.fq.gz -p %s -o %s/2.Mapping -l %s\n"
                   %(cfg['sub']['pre_GATK'],cfg['dir']['outdir'],key,cfg['dir']['outdir'],key,key,cfg['dir']['outdir'],cfg['bed']['target']))
    else:
        file.write("perl %s -a %s/1.QC/%s_1.clean.fq.gz -b %s/1.QC/%s_2.clean.fq.gz -p %s -o %s/2.Mapping\n"
                   % (cfg['sub']['pre_GATK'], cfg['dir']['outdir'], key, cfg['dir']['outdir'], key, key,cfg['dir']['outdir']))
###################call snp using Mutect2##########################################
file=open("%s/shell/MuTect2.3.sh" %(cfg['dir']['outdir']),"w")
if not os.path.exists("%s/3.vcf" %(cfg['dir']['outdir'])):
    os.mkdir("%s/3.vcf" %(cfg['dir']['outdir']))
for key in cfg['somatic']:
    array=cfg['somatic']['%s' %(key)].split(",")
    if os.path.exists("%s" % (cfg['bed']['target'])):
        file.write("cd %s && %s %s -t 2.Mapping/%s.recal.bam -n 2.Mapping/%s.recal.bam -o 3.vcf -pt %s -pn %s -r %s"
                   %(cfg['dir']['outdir'],cfg['software']['python3'],cfg['sub']['Mutect2'],array[0],array[1],array[0],array[1],cfg['bed']['target']))
    else:
        file.write("cd %s && %s %s -t 2.Mapping/%s.recal.bam -n 2.Mapping/%s.recal.bam -o 3.vcf -pt %s -pn %s -r %s"
                   % (cfg['dir']['outdir'], cfg['software']['python3'], cfg['sub']['Mutect2'], array[0], array[1],
                      array[0], array[1], cfg['bed']['target']))

