#Email:fanyucai1@126.com
#2019.1.18

import os
import argparse
import subprocess
import time
import configparser

class Myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
    def optionxform(self, optionstr):
        return optionstr
parser=argparse.ArgumentParser("Run GATK BQSR.")
parser.add_argument("-b","--bam",help="bam file",required=True)
parser.add_argument("-l","--bed",help="target region bed file")
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",help="prefix of output",default="out")
parser.add_argument("-c","--config",help="config file",required=True)

args=parser.parse_args()
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
args.outdir=os.path.abspath(args.outdir)
args.bam=os.path.abspath(args.bam)
par=""
if os.path.exists(args.bed):
    args.bed=os.path.abspath(args.bed)
    par+=" -L %s " %(args.bed)
config = configparser.RawConfigParser()
config.read(args.config)
java=config.get('software','java')
gatk4=config.get('software','gatk4.1.3')
gatk3=config.get('software','gatk3.7')
dbsnp138=config.get('database','dbsnp138')
mill_indel=config.get('database','mill_indel')
phase1_indel=config.get('database','phase1_indel')
hg19_ref=config.get('database','hg19_ref')
start=time.time()
####################Realign Indels - Realignment
os.chdir(args.outdir)
out=args.outdir+"/"+args.prefix
cmd="%s -Xmx40G -jar %s -T RealignerTargetCreator -nt 20 -R %s -I %s -known %s -known %s -o %s.target.list %s" \
    %(java,gatk3,hg19_ref,args.bam,phase1_indel,mill_indel,out,par)
subprocess.check_call(cmd,shell=True)
cmd="%s -Xmx40G -jar %s -T IndelRealigner -R %s -I %s -targetIntervals %s.target.list -known %s -known %s -o %s.realign.bam" \
    %(java,gatk3,hg19_ref,args.bam,out,phase1_indel,mill_indel,out)
subprocess.check_call(cmd,shell=True)
####################Recalibrate Bases
subprocess.check_call("%s -Xmx40G -jar %s BaseRecalibrator --use-original-qualities -R %s -I %s.realign.bam --known-sites %s --known-sites %s -O %s.recal_data.table %s"
                      %(java,gatk4,hg19_ref,out,dbsnp138,mill_indel,out,par),shell=True)
subprocess.check_call("%s -Xmx40G -jar %s ApplyBQSR -R %s -I %s.realign.bam --bqsr-recal-file %s.recal_data.table -O %s.recal.bam"
                      %(java,gatk4,hg19_ref,out,out,out),shell=True)
end=time.time()

print("Elapse time is %g seconds" %(end-start))

"""
URL:
Data pre-processing for variant discovery:
https://software.broadinstitute.org/gatk/best-practices/workflow?id=11165
https://github.com/gatk-workflows/gatk4-data-processing/blob/master/processing-for-variant-discovery-gatk4.b37.wgs.inputs.json

What should I use as known variants/sites for running tool X?
https://software.broadinstitute.org/gatk/documentation/article.php?id=1247

Welcome to Sentieon Appnotes's documentation!
https://support.sentieon.com/appnotes/arguments/

Frampton G M, Fichtenholtz A, Otto G A, et al. Development and validation of a clinical cancer genomic profiling test based on massively parallel DNA sequencing[J]. Nature biotechnology, 2013, 31(11): 1023.
"""