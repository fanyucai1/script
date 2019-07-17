#Email:fanyucai1@126.com
#2019.1.21

abra="/software/abra2/abra2-2.19.jar"
java="/software/java/jdk1.8.0_202/bin/java"
ref="/data/Database/hg19/ucsc.hg19.fasta"
samtools="/software/samtools/samtools-1.9/bin/samtools"
"""
https://github.com/mozack/abra2/releases
https://impact-pipeline.readthedocs.io/en/latest/index.html
https://github.com/rhshah/IMPACT-Pipeline/blob/master/bin/Run_ABRArealignment.py
Mose L E, Wilkerson M D, Hayes D N, et al. ABRA: improved coding indel detection via assembly-based realignment[J]. Bioinformatics, 2014, 30(19): 2813-2815.
"""
import os
import argparse
import subprocess
import time
parser=argparse.ArgumentParser("This script will use ABRA to improve coding indel detection via assembly-based realignment")
parser.add_argument("-n","--nbam",help="normal bam file",required=True)
parser.add_argument("-t","--tbam",help="tumal bam file",required=True)
parser.add_argument("-o","--out",help="output directory",default=os.getcwd())
parser.add_argument("-v","--vcf",help="VCF containing known (or suspected) variant sites.",default=0)
parser.add_argument("-b","--bed",help="target bed region")

args=parser.parse_args()
args.nbam=os.path.abspath(args.nbam)
args.tbam=os.path.abspath(args.tbam)
if not os.path.exists(args.out):
    os.mkdir(args.out)
    args.out=os.path.abspath(args.out)
par=" --kmer 43 "
if os.path.exists(args.bed):
    par+=" --targets "
    par+=os.path.abspath(args.bed)
if args.vcf !=0:
    par+=" --in-vcf %s "%(args.vcf)
cmd="cd %s && %s -Xmx20G -jar %s --in %s,%s --out %s.abra.bam,%s.abra.bam --ref %s --threads 20 %s --tmpdir ./ >abra.log" \
    %(args.out,java,abra,args.nbam,args.tbam,args.nbam,args.tbam,ref,par)

start=time.time()
subprocess.check_call(cmd,shell=True)
p1="%s index %s.abra.bam" %(samtools,args.tbam)
p2="%s index %s.abra.bam" %(samtools,args.nbam)
subprocess.check_call(p1,shell=True)
subprocess.check_call(p2,shell=True)
end=time.time()
print("Elapsed time was %g seconds" % (end - start))