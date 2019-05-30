#Email:fanyucai1@126.com
#2019.5.23
import os
import argparse
import subprocess
import configparser
import sys
sub=os.path.abspath(__file__)
dir_name=os.path.dirname(sub)
sys.path.append(dir_name)
import core
import time
start=time.time()
########################################################
class Myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
    def optionxform(self, optionstr):
        return optionstr
parser=argparse.ArgumentParser("Run panel 275 analysis.")
parser.add_argument("-i","--input",help="config file",required=True)
args=parser.parse_args()
########################################################
config = configparser.ConfigParser()
config.read(os.path.abspath(args.input))
script = dir_name + "/core/"
par = ""
p1 = config['tumor']['fq1']
p2 = config['tumor']['fq2']
outdir = config['par']['outdir']
prefix = config['par']['tumor_name']
out = outdir + "/" + prefix
if config['par']['type'] == "single":
    core.print_config.tumor_only(p1, p2, prefix, outdir)
    par = " single %s " % (config['par']['tumor_name'])
else:
    p3 = config['normal']['fq1']
    p4 = config['normal']['fq2']
    core.print_config.tumor_normal(p1, p2, prefix, p3, p4, config['par']['normal_name'], outdir)
    par = " tumor-normal %s %s " % (prefix, config['par']['normal_name'])
cmd = "docker run -v /software/qiaseq-dna/data/:/srv/qgen/data/ -v %s:/project/ " \
      "%s python /srv/qgen/code/qiaseq-dna/run_qiaseq_dna.py run_sm_counter_v2.params.txt v2 %s" \
      % (config['par']['outdir'], config['par']['docker'], par)
print(cmd)
#subprocess.check_call(cmd, shell=True)
#########################################prefilter vcf split somatic and germline
cmd = '%s %s/prefilter.py -i %s.smCounter.cut.vcf -p %s -v %s -o %s'\
      % (config['par']['python3'], script, out,prefix, config['par']['vaf'],outdir)
subprocess.check_call(cmd, shell=True)
#######################################anno germline、somatic and all
maf=config['par']['maf']
core.annovar275.anno("%s.somatic.vcf" %(out),"%s.somatic"%(out))
core.annovar275.anno("%s.germline.vcf" %(out),"%s.germline"%(out))
core.annovar275.anno("%s.all.vcf" %(out),"%s.all"%(out))
"""
#####################################filter germline and somatic,respectively
core.filter_annovar275.somatic(maf,"%s.somatic.final.txt" %(out),"%s"%(out))
core.filter_annovar275.germline(maf,"%s.germline.final.txt" %(out),"%s"%(out))
####################################filter gnene
genelist=config['par']['gene_list']
core.split.split_gene(genelist,"%s.filter.annovar.germline"%(out),"%s.germline_275.tsv"%(out))
core.split.split_gene(genelist,"%s.filter.annovar.somatic"%(out),"%s.somatic_275.tsv"%(out))
####################################MSI
core.MSI.run_msi("%s.bam"%(out),"%s"%(out))
#####################################run CNV
###################################filter CNV gene list
cmd = "cd %s && %s %s/cnv.py -v %s.copy-number.vcf -p %s -g %s " % (config['par']['outdir'], config['par']['python3'], 
script, config['par']['tumor_name'], config['par']['tumor_name'],config['par']['gene_list'])
subprocess.check_call(cmd, shell=True)
"""
end=time.time()
print("Elapse time is %g seconds" %(end-start))
