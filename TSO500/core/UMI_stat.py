import os
import sys
import subprocess
import operator

fastq=sys.argv[1]
prefix=sys.argv[2]
outdir=os.getcwd()

out=outdir+"/"+prefix
if fastq.endswith("gz"):
    subprocess.check_call('zcat %s|grep @ >%s.tmp.seq' % (fastq, out), shell=True)
else:
    subprocess.check_call('grep @ %s >%s.tmp.seq'%(fastq,out),shell=True)
infile=open("%s.tmp.seq"%(out),"r")
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

outfile=open("%s.UMI.stat"%(out),"w")
for key in b:
    outfile.write("%s"%(key))
outfile.close()