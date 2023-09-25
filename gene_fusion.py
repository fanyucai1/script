#Email:fanyucai1@126.com
#2019.1.24

import os
import subprocess
import time
import argparse

FusionCatcher="/data/fyc_software/FusionCatcher/fusioncatcher_v1.00"
seqtk="/data/fyc_software/SeqTK/seqtk/"#1.2-r101c-dirty
BBMap="/data/fyc_software/BBMap/bbmap"#37.28
bowtie2="/data/fyc_software/bowtie2/bowtie2-2.2.9/"#2.2.9
STAR="/data/fyc_software/STAR/STAR-2.5.2b/bin/Linux_x86_64"#2.5.2b
bowtie="/data/fyc_software/bowtie/bowtie-1.1.2/"#1.2.0
python="/data/fyc_software/python2/Python-v2.7.9/bin"
blat="/data/fyc_software/ucsc_bin/"
env="export PATH=%s:%s:%s:%s:%s:%s:%s:%s/bin:$PATH" %(blat,python,seqtk,BBMap,bowtie2,bowtie,STAR,FusionCatcher)

parser=argparse.ArgumentParser("Somatic fusion-genes finder for RNA-seq data")
parser.add_argument("-p1","--pe1",help="5 read",required=True)
parser.add_argument("-p2","--pe2",help="3 read",required=True)
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())

args=parser.parse_args()

if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
os.chdir(args.outdir)
args.outdir=os.path.abspath(args.outdir)
args.pe1=os.path.abspath(args.pe1)
args.pe2=os.path.abspath(args.pe2)

cmd="%s && fusioncatcher -i %s,%s -d %s/data/current/ -o %s" %(env,args.pe1,args.pe2,FusionCatcher,args.outdir)
start=time.time()
subprocess.check_call(cmd,shell=True)
end=time.time()
print("Elapse time is %g seconds" %(end-start))
