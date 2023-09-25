#Email:fanyucai1@126.com
#2019.1.18

import os
import argparse
import subprocess
from multiprocessing import Process

speedseq="export PATH=/data02/software/speedseq/speedseq/bin:\$PATH"
lumpy="/data02/software/LUMPY/lumpy-sv/bin/lumpyexpress"
ref="/data02/database/hg19/ucsc.hg19.fasta"

parser=argparse.ArgumentParser("Find SV using lumpy.")
parser.add_argument("-td","--tdir",help="tumor speedseq align ouput directory)",default=os.getcwd())
parser.add_argument("-nd","--ndir",help="normal speedseq align ouput directory)",default=os.getcwd())
parser.add_argument("-t","--tumor",help="name of tumor",required=True)
parser.add_argument("-n","--normal",help="name of normal",required=True)
parser.add_argument("-o","--outdir",help="outdir",default=os.getcwd())
args=parser.parse_args()

if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
    args.outdir=os.path.abspath(args.outdir)
os.chdir(args.outdir)

if not os.path.exists("%s/%s.bam" %(args.ndir,args.normal)):
    print("%s/%s.bam not exist" % (args.ndir, args.normal))
    exit()
if not os.path.exists("%s/%s.splitters.bam"%(args.ndir,args.normal)):
    print("%s/%s.splitters.bam not exist" % (args.ndir, args.normal))
    exit()
if not os.path.exists("%s/%s.discordants.bam" %(args.ndir,args.normal)):
    print("%s/%s.discordants.bam not exist" % (args.ndir, args.normal))
    exit()

if not os.path.exists("%s/%s.bam"%(args.tdir,args.tumor)):
    print("%s/%s.bam not exist" % (args.tdir, args.tumor))
    exit()
if not os.path.exists("%s/%s.splitters.bam" %(args.tdir,args.tumor)):
    print("%s/%s.splitters.bam not exist" % (args.tdir, args.tumor))
    exit()
if not os.path.exists("%s/%s.discordants.bam" %(args.tdir,args.tumor)):
    print("%s/%s.discordants.bam not exist" %(args.tdir,args.tumor))
    exit()

def run_shell(cmd):
    subprocess.check_call(cmd,shell=True)
p1="%s/%s" %(args.tdir,args.tumor)
p2="%s/%s" %(args.ndir,args.normal)
subprocess.check_call("cd %s && %s -B %s.bam,%s.bam -S %s.splitters.bam,%s.splitters.bam -D %s.discordants.bam,%s.discordants.bam -o %s.%s.vcf"
                      %(args.outdir,lumpy,p1,p2,p1,p2,p1,p2,args.ptumor,args.pnormal),shell=True)



