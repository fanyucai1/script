import os
import sys
import subprocess
from datetime import date

Pindel="/software/Pindel"
ref="/data/Database/hg19/ucsc.hg19.fasta"
#Run Pindel for Long Indels & MNPS (32bp-350bp)
def run(bam,insert_size,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    subprocess.check_call("echo %s %s %s >%s/config.file"%(bam,insert_size,prefix,outdir),shell=True)
    cmd="%s/pindel -f %s -p -T 8 -x 2 -M 5 -i %s/config.file -o %s -r false -t false -I false"%(Pindel,ref,outdir,out)
    subprocess.check_call(cmd,shell=True)
    day = date.today()
    today = day.isoformat()
    today = today.replace("-", "")
    cmd="%s/pindel2vcf -p %s -r %s -R hg19 -d %s -v %s -b true --gatk_compatible"%(Pindel,out,ref,today,out)
    subprocess.check_call(cmd,shell=True)

if __name__=="__main__":
    if len(sys.argv)!=5:
        print("Run Pindel for Long Indels & MNPS (32bp-350bp)\n")
        print("usage:python3 %s bamfile insert_size outdir prefix\n"%(sys.argv[0]))
        print("https://github.com/rhshah/IMPACT-Pipeline/blob/master/bin/Run_Pindel.py\n")
        print("#Email:fanyucai1@126.com\n")
    else:
        bam, insert_size, outdir, prefix=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
        run(bam, insert_size, outdir, prefix)
