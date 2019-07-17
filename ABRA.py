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
parser.add_argument("-b","--bam",help="normal bam file",required=True)
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
parser.add_argument("-o","--out",help="output directory",default=os.getcwd())
parser.add_argument("-v","--vcf",help="VCF containing known (or suspected) variant sites.",default=0)
parser.add_argument("-b","--bed",help="target bed region",default=0)

args=parser.parse_args()
args.bam=os.path.abspath(args.bam)
if not os.path.exists(args.out):
    os.mkdir(args.out)
    args.out=os.path.abspath(args.out)
par=" --kmer 43 "
if args.bed!=0:
    par+=" --targets %s"%(args.bed)
if args.vcf !=0:
    par+=" --in-vcf %s "%(args.vcf)
cmd="cd %s && %s -Xmx20G -jar %s --in %s --out %s/%s.abra.bam --ref %s --threads 10 %s --tmpdir ./ >abra.log" \
    %(args.out,java,abra,args.bam,args.out,args.prefix,ref,par)

start=time.time()
subprocess.check_call(cmd,shell=True)
p="%s index %s/%s.abra.bam" %(samtools,args.out,args.prefix)
subprocess.check_call(p,shell=True)
end=time.time()
print("Elapsed time was %g seconds" % (end - start))