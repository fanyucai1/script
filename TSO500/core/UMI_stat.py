import os
import sys
import subprocess
import operator

fastq=sys.argv[1]
prefix=sys.argv[2]
outdir=os.getcwd()

subprocess.check_call('grep @ %s >%s/tmp.seq'%(fastq,outdir),shell=True)
infile=open("%s/tmp.seq"%(outdir),"r")
dict={}
for line in infile:
    line=line.strip()
    array=line.split("\t")
    array1=array[0].split(":")
    UMI=array1[-1].split("+")
    dict[UMI[0]]+=1
    dict[UMI[1]] += 1
infile.close()
b = sorted(dict.items(), key=operator.itemgetter(1),reverse=True)

outfile=open("%s/UMI.stat"%(outdir),"w")
for key in b:
    outfile.write("%s"%(key))
outfile.close()