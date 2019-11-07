import subprocess
import sys

env="export PATH=/software/java/jdk1.8.0_202/bin:/software/R/R-v3.5.2/bin/:"
env+="/software/vardict/VarDict-1.6.0/bin/:/software/perl/perl-v5.28.1/bin/:$PATH"
ref="/data/Database/hg19/ucsc.hg19.fasta"

def tumor_only(vaf,bamfile,bedfile,prefix,outdir):
    cmd="%s && VarDict -U -th 10 -q 20 -Q 20 -G %s -f %s -N %s -b %s -z -c 1 -S 2 -E 3 -g 4 %s | teststrandbias.R | var2vcf_valid.pl -d 50 -m 4.25 -N %s -E -f %s >%s/%s.vardict.vcf" \
        %(env,ref,vaf,prefix,bamfile,bedfile,prefix,vaf,outdir,prefix)
    subprocess.check_call(cmd,shell=True)
if __name__=="__main__":
    if len(sys.argv)!=6:
        print("Usgae:")
        print("python3 vardict_single.py vaf bamfile bedfile prefix outdir\n")
        print("Copyright:fanyucai")
        print("Version:1.0")
        sys.exit(-1)
    tumor_only(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
