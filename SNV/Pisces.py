#Email:fanyucai1@126.com
#2019.3.22

import os
import argparse
import subprocess

dotnet="/software/dotnet/dotnet"
pisces="/software/Pisces/Pisces_5.2.10.49/Pisces.dll"
ref="/data/Database/hg19/ucsc.hg19.fasta"
"""
Dunn T, Berry G, Emig-Agius D, et al. Pisces: An accurate and versatile variant caller for somatic and germline next-generation sequencing data[J]. BioRxiv, 2018: 291641.
"""
parser=argparse.ArgumentParser("Tumor-only workflows.(https://github.com/Illumina/Pisces)")
parser.add_argument("-b","--bam",help="bam file",required=True)
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
args=parser.parse_args()
out=args.outdir
out+=args.prefix
if not os.path.exists(out):
    os.mkdir(out)
cmd="%s %s -bam %s -g %s -o %s" %(dotnet,pisces,args.bam,ref,out)
subprocess.check_call(cmd,shell=True)
