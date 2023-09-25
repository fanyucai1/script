#Email:fanyucai1@126.com
#2019.1.17

import os
import argparse
import subprocess
from multiprocessing import Process

java="/data/fyc_software/java/jdk1.8.0_201/bin/java"
#https://github.com/dkoboldt/varscan
varscan="/data/fyc_software/Varscan2/varscan/VarScan.v2.4.3.jar"
samtools="/data/fyc_software/samtools/samtools-1.9/bin/samtools"
ref="/data/fyc_data/hg19/ucsc.hg19.fasta"
"""
Koboldt D C, Larson D E, Wilson R K. Using VarScan 2 for germline variant calling and somatic mutation detection[J]. Current protocols in bioinformatics, 2013, 44(1): 15.4. 1-15.4. 17.
Li S, Garrett-Bakelman F E, Chung S S, et al. Distinct evolution and dynamics of epigenetic and genetic heterogeneity in acute myeloid leukemia[J]. Nature medicine, 2016, 22(7): 792.
McGranahan N, Furness A J S, Rosenthal R, et al. Clonal neoantigens elicit T cell immunoreactivity and sensitivity to immune checkpoint blockade[J]. Science, 2016, 351(6280): 1463-1469.
"""
parser=argparse.ArgumentParser("This script will call SNV from tumor-normal.")
parser.add_argument("-b","--bed",help="target bed file",type=str)
parser.add_argument("-t","--tb",help="tumor bam file",type=str,required=True)
parser.add_argument("-n","--nb",help="normal bam file",type=str,required=True)
parser.add_argument("-o","--outdir",help="output directory",type=str,default=os.getcwd())
parser.add_argument("-p","--prefix",help="prefix of output",default="out")
args=parser.parse_args()
par=""
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
    args.outdir=os.path.abspath(args.outdir)
if args.bed:
    args.bed=os.path.abspath(args.bed)
    par=" -l %s " %(args.bed)
args.tb=os.path.abspath(args.tb)
args.nb=os.path.abspath(args.nb)
def shell_run(cmd):
    subprocess.check_call("%s" %(cmd),shell=True)

a="cd %s && %s mpileup -f %s %s %s >%s_normal.mpileup" %(args.outdir,samtools,ref,par,args.nb,args.prefix)
b="cd %s && %s mpileup -f %s %s %s >%s_tumor.mpileup" %(args.outdir,samtools,ref,par,args.tb,args.prefix)
if __name__ == '__main__':
    p1=Process(target=shell_run,args=(a,))
    p2 = Process(target=shell_run, args=(b,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    subprocess.check_call("cd %s && %s -Xmx10g -jar %s somatic %s_normal.mpileup %s_tumor.mpileup %s --strand-filter 1 --output-vcf 1 --min-var-freq 0.001 --min-coverage 100"
                      %(args.outdir,java,varscan,args.prefix,args.prefix,args.prefix),shell=True)
    #filter snp around indel
    subprocess.check_call("cd %s && %s -Xmx10g -jar %s somaticFilter %s.snp.vcf --min-var-freq 0.001 --min-coverage 100 --indel-file %s.indel.vcf --output-file %s.filter.snp.vcf"
                          %(args.outdir,java,varscan,args.prefix,args.prefix,args.prefix),shell=True)
    #separate a somatic output file by somatic_status (Germline, Somatic, LOH)
    c="cd %s && %s -Xmx10g -jar %s processSomatic %s.filter.snp.vcf --min-tumor-freq 0.001" %(args.outdir,java,varscan,args.prefix)
    d="cd %s && %s -Xmx10g -jar %s processSomatic %s.indel.vcf --min-tumor-freq 0.001" % (args.outdir, java, varscan, args.prefix)
    p3=Process(target=shell_run,args=(c,))
    p4=Process(target=shell_run,args=(d,))
    p3.start()
    p4.start()
    p3.join()
    p4.join()