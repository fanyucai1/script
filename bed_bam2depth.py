import os
import sys
import subprocess
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

bedtools="/software/bedtools/bedtools2/bin/bedtools"

def run(bed,bam,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    cmd="%s coverage -a %s -b %s -d >%s.site.depth"%(bedtools,bed,bam,out)
    subprocess.check_call(cmd,shell=True)
    infile=open("%s.site.depth"%(out),"r")
    outfile=open("%s.coverage.tsv"%(out),"w")
    num=0
    x0,x50,x100,x250,x500,x1000,x3500=0,0,0,0,0,0,0
    for line in infile:
        num+=1
        line=line.strip()
        array=line.split("\t")
        if float(array[-1]) < 50:
            x0+=1
        if float(array[-1]) >=50:
            x50+=1
        if float(array[-1]) >= 100:
            x100+=1
        if float(array[-1]) >=250:
            x250+=1
        if float(array[-1]) >= 500:
            x500+=1
        if float(array[-1]) >= 1000:
            x1000+=1

    x0 = x0 / num * 100
    x50=x50/num*100
    x100 = x100 / num * 100
    x250 = x250 / num * 100
    x500 = x500 / num * 100
    x1000 = x1000 / num * 100
    y=[x0,x50,x100,x250,x500,x1000]
    x=["0",'>=50X','>=100X','>=250X','>=500X','>=1000X']
    outfile.write("%%_bases_above_50X\t%s\n" % (x50))
    outfile.write("%%_bases_above_100X\t%s\n" % (x100))
    outfile.write("%%_bases_above_250X\t%s\n" % (x250))
    outfile.write("%%_bases_above_500X\t%s\n" % (x500))
    outfile.write("%%_bases_above_1000X\t%s\n" % (x1000))
    plt.figure(figsize=(18, 10))
    plt.xlabel("Depth(X)")
    plt.ylabel("Coverage")
    sns.lineplot(x=x, y=y)
    plt.savefig('%s.bed_depth.png' % (out), dpi=300)

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