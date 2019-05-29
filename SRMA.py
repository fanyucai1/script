#Email:fanyucai1@126.com
#2019.1.21

SRMA="/data/fyc_software/SRMA/java/build/jar/srma-0.1.16.jar"
java="/data02/software/java/jdk1.8.0_191/bin/java"

"""
Aligned reads were realigned for known insertion/deletion envents using SRMA(v0.1.16).
https://github.com/nh13/SRMA
Homer N, Nelson S F. Improved variant discovery through local re-alignment of short-read next-generation sequencing data using SRMA[J]. Genome biology, 2010, 11(10): R99.
"""

import os
import argparse
import subprocess
import time

parser=argparse.ArgumentParser("Aligned reads were realigned for known insertion/deletion envents using SRMA(v0.1.16).")
parser.add_argument("-b","--bam",help="bam files",required=True)
parser.add_argument("-o","--out",help="outdir",default=os.getcwd())
args=parser.parse_args()
if not os.path.exists(args.out):
    os.mkdir(args.out)
    args.out=os.path.abspath(args.out)
args.bam=os.path.abspath(args.bam)
cmd="cd %s && %s -Xmx10G -jar %s I=%s O=%s.re" %(args.out,java,SRMA)

start=time.time()
subprocess.check_call(cmd,shell=True)
end=time.time()
print("Elapsed time was %g seconds " %(end-start))