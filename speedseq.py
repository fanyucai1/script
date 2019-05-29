#Email:fanyucai1@126.com
#2019.1.18

import os
import argparse
import subprocess
import time
speedseq="export PATH=/software/speedseq/speedseq/bin:$PATH"
ref="/data/Database/hg19/ucsc.hg19.fasta"

parser=argparse.ArgumentParser("Find SV using lumpy.")
parser.add_argument("-p1","--pe1",help="5 reads(.gz)",required=True)
parser.add_argument("-p2","--pe2",help="3 reads(.gz)",required=True)
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",help="prefix of output,default:out",default="out")

args=parser.parse_args()
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
args.outdir=os.path.abspath(args.outdir)
args.pe1=os.path.abspath(args.pe1)
args.pe2=os.path.abspath(args.pe2)
os.chdir(args.outdir)
start=time.time()
subprocess.check_call("cd %s && %s && speedseq align -t 20 -o %s -R \"@RG\\tID:%s\\tSM:%s\\tLB:lib:\\tPL:Illumina\" %s %s %s"
                      %(args.outdir,speedseq,args.prefix,args.prefix,args.prefix,ref,args.pe1,args.pe2),shell=True)
end=time.time()
print("Elapse time  is %g seconds" %(end-start))