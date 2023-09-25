#Email:fanyucai1@126.com
#2019.1.18

import os
import argparse
import subprocess
import time
java="export PATH=/data/fyc_software/java/jdk1.8.0_201/bin/:$PATH"
gatk="/data/fyc_software/GATK/gatk-4.0.12.0/gatk"
gatk3_8="/data/fyc_software/GATK/GenomeAnalysisTK-3.8-1-0-gf15c1c3ef/GenomeAnalysisTK.jar"
dbsnp="/data/fyc_data/hg19/dbsnp_138.hg19.vcf.gz"
mill="/data/fyc_data/hg19/Mills_and_1000G_gold_standard.indels.hg19.sites.vcf.gz"
phase1="/data/fyc_data/hg19/1000G_phase1.indels.hg19.sites.vcf.gz"
ref="/data/fyc_data/hg19/ucsc.hg19.fasta"

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
parser=argparse.ArgumentParser("Run GATK BQSR.")
parser.add_argument("-b","--bam",help="bam file",required=True)
parser.add_argument("-l","--bed",help="target region bed file")
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",help="prefix of output",default="out")

args=parser.parse_args()
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
args.outdir=os.path.abspath(args.outdir)
args.bam=os.path.abspath(args.bam)
par=""
if os.path.exists(args.bed):
    args.bed=os.path.abspath(args.bed)
    par+=" -L %s " %(args.bed)

start=time.time()
##########Realign Indels - Realignment
os.chdir(args.outdir)
cmd="%s && cd %s && java -Xmx40G -jar %s -T RealignerTargetCreator -nt 20 -R %s -I %s -known %s -known %s -o %s.target.list %s" %(java,args.outdir,gatk3_8,ref,args.bam,phase1,mill,args.prefix,par)
subprocess.check_call(cmd,shell=True)
cmd="%s && java -Xmx40G -jar %s -T IndelRealigner -R %s -I %s -targetIntervals %s.target.list -known %s -known %s -o %s.realign.bam" \
    %(java,gatk3_8,ref,args.bam,args.prefix,phase1,mill,args.prefix)
subprocess.check_call(cmd,shell=True)
##########Recalibrate Bases
subprocess.check_call("%s && cd %s && %s --java-options -Xmx40G BaseRecalibrator --use-original-qualities -R %s -I %s.realign.bam --known-sites %s --known-sites %s -O %s.recal_data.table %s"
                      %(java,args.outdir,gatk,ref,args.prefix,dbsnp,mill,args.prefix,par),shell=True)
subprocess.check_call("%s && cd %s && %s --java-options -Xmx40G ApplyBQSR -R %s -I %s.realign.bam --bqsr-recal-file %s.recal_data.table -O %s.recal.bam"
                      %(java,args.outdir,gatk,ref,args.prefix,args.prefix,args.prefix),shell=True)
end=time.time()

print("Elapse time is %g seconds" %(end-start))