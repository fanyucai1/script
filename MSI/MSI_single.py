#Email:fanyucai1@126.com
#2019.8.19

import os
import sys
import subprocess

msisensor="/software/MSIsensor/MSIsensor-v0.6/msisensor-0.6/msisensor"
ref="/data/Database/hg19/ucsc.hg19.fasta"

def single(tumor,bed,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    subprocess.check_call("%s scan -d %s -o %s/microsatellites.list" % (msisensor, ref, outdir),shell=True)
    cmd="%s msi -d %s/microsatellites.list -t %s -e %s -o %s" %(msisensor,outdir,tumor,bed,out)
    subprocess.check_call(cmd,shell=True)

if __name__=="__main__":
    if len(sys.argv)!=5:
        print("usage:python3 %s tumor.bam panel.bed outdir prefix\n"%(sys.argv[0]))
        print("Email:fanyucai1@126.com")
    else:
        tumor=sys.argv[1]
        bed=sys.argv[2]
        outdir=sys.argv[3]
        prefix=sys.argv[4]
        single(tumor, bed, outdir, prefix)