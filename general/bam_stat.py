import sys
import subprocess
import os
import re
def run(bam,bed,outdir,prefix,samtools="/software/samtools/samtools-1.9/bin/samtools"):
    out=outdir+"/"+prefix
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    cmd="%s flagstat %s >%s.stat"%(samtools,bam,out)
    subprocess.check_call(cmd,shell=True)
    infile=open("%s.stat.txt"%(out),"r")
    num=0
    Mapping_reads,Total_reads=0,0
    for line in infile:
        num+=1
        line=line.strip()
        array=re.split(r'\s',line)
        if num==7:
            Total_reads=int(array[0])*2
        elif num==9:
            Mapping_reads=int(array[0])
        else:
            pass
    Mapping_ration=Mapping_reads/Total_reads*100
    cmd='%s depth -b %s -q 20 -Q 20 -d 0 %s >%s.depth'%(samtools,bed,bam,out)
    subprocess.check_call(cmd,shell=True)



