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
dict1={}
dict2={}
for line in infile:
    line=line.strip()
    array=line.split("\t")
    array1=array[0].split(":")
    UMI=array1[-1].split("+")
    if not UMI[0] in dict1:
        dict1[UMI[0]]=0
    if not UMI[1] in dict2:
        dict2[UMI[1]]=0
    dict1[UMI[0]]+=1
    dict2[UMI[1]]+=1
infile.close()

a=sorted(dict1.items(), key=operator.itemgetter(1),reverse=True)
b=sorted(dict2.items(), key=operator.itemgetter(1),reverse=True)

outfile=open("%s.UMI.1.stat"%(out),"w")
for key in a:
    outfile.write("%s,%s\n"%(key))
outfile.close()

outfile=open("%s.UMI.2.stat"%(out),"w")
for key in b:
    outfile.write("%s,%s\n"%(key))
outfile.close()