import os
import sys
import subprocess
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

bedtools="/software/bedtools/bedtools2/bin/bedtools"

def run(bed,bam,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    cmd="%s coverage -a %s -b %s -mean >%s.MeanCoverageBED.bedgraph"%(bedtools,bed,bam,out)
    #subprocess.check_call(cmd,shell=True)
    infile=open("%s.MeanCoverageBED.bedgraph"%(out),"r")
    x,y=[],[]
    num=0
    for line in infile:
        num+=1
        x.append(num)
        line=line.strip()
        array=line.split("\t")
        y.append(float(array[-1]))
    plt.figure(figsize=(18, 10))
    plt.xlabel("%s(bins)"%(num))
    plt.ylabel("Mean_Depth")
    sns.lineplot(x=x, y=sorted(y))
    plt.savefig('%s/bed_depth.png' % (outdir), dpi=300)



if __name__=="__main__":
    if len(sys.argv)!=5:
        print("python3 %s bedfile bamfile outdir prefix"%(sys.argv[0]))
        print("#Email:fanyucai1@126.com")
    else:
        bed=sys.argv[1]
        bam=sys.argv[2]
        outdir=sys.argv[3]
        prefix=sys.argv[4]
        run(bed,bam,outdir,prefix)