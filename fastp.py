#Email:fanyucai1@126.com
#2019.1.24

import os
import argparse
import json
import time
import subprocess
fastp="/data/fyc_software/fastp/fastp"
parser=argparse.ArgumentParser("QC using fastp.")
parser.add_argument("-p1","--pe1",help="5 reads",required=True)
parser.add_argument("-p2","--pe2",help="3 reads",required=True)
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",help="prefix of output",default="out.clean")

args=parser.parse_args()

if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
args.outdir=os.path.abspath(args.outdir)
args.pe1=os.path.abspath(args.pe1)
args.pe2=os.path.abspath(args.pe2)
os.chdir(args.outdir)
par=" --detect_adapter_for_pe -W 4 -M 15 -l 75 -w 20 -j %s.json -h %s.html " %(args.prefix,args.prefix)
cmd="%s -i %s -I %s -o %s.R1.fq.gz -O %s.R2.fq.gz %s " %(fastp,args.pe1,args.pe2,args.prefix,args.prefix,par)
start=time.time()
subprocess.check_call(cmd,shell=True)
end=time.time()
print("Elapse time is %g second" %(end-start))