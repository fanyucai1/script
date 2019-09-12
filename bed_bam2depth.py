import os
import sys
import subprocess


bedtools="/software/bedtools/bedtools2/bin/bedtools"

def run(bed,bam,outdir,prefix):
    if os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    cmd="%s coverage -a %s -b %s -mean >%s/MeanCoverageBED.bedgraph"%(bedtools,bed,bam,out)
    subprocess.check_call(cmd,shell=True)


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