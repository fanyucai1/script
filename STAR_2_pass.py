#Email:fanyucai1@126.com
#2019.1.29

import os
import subprocess
import argparse
import time

STAR="/data/fyc_software/STAR/STAR-2.6.1d/bin/Linux_x86_64/STAR"
index="/data/fyc_data/hg19/STAR_index"
parser=argparse.ArgumentParser("RNA-Seq Alignment Workflow")
parser.add_argument("-p1","--pe1",help="5 reads(.gz)",required=True)
parser.add_argument("-p2","--pe2",help="3 reads(.gz)",required=True)
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",help="prefix of output",default="STAR")
parser.add_argument("-l","--length",help="read length",required=True,type=int)
args=parser.parse_args()
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
args.outdir=os.path.abspath(args.outdir)
args.pe1=os.path.abspath(args.pe1)
args.pe2=os.path.abspath(args.pe2)
args.length=args.length-1
os.chdir(args.outdir)
start=time.time()
par=""
if args.pe1.endswith(".gz"):
    par+=" --readFilesCommand zcat "
#############################################https://github.com/STAR-Fusion/STAR-Fusion/wiki
par+="--twopassMode Basic --outReadsUnmapped None --chimSegmentMin 12 --chimJunctionOverhangMin 12 "
par+="--alignSJDBoverhangMin 10 --alignMatesGapMax 100000 --alignIntronMax 100000 --chimSegmentReadGapMax 3 "
par+="--alignSJstitchMismatchNmax 5 -1 5 5 --outSAMstrandField intronMotif --chimOutJunctionFormat 1 "
cmd="%s --genomeDir %s --readFilesIn %s %s %s --runThreadN 20 --outFileNamePrefix %s/%s" %(STAR,index,args.pe1,args.pe2,par,args.outdir,args.prefix)
subprocess.check_call(cmd,shell=True)
end=time.time()
print("Elapse time is %g seconds" %(end-start))