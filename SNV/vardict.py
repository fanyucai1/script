import subprocess
import re
import sys

env="export PATH=/software/java/jdk1.8.0_202/bin:/software/R/R-v3.5.2/bin/:"
env+="/software/vardict/1.5.7/VarDictJava-1.5.7/bin:/software/perl/perl-v5.28.1/bin/:$PATH"
ref="/data/Database/hg19/ucsc.hg19.fasta"

def tumor_only(vaf,bamfile,bedfile,prefix,outdir):
    cmd="%s &&  VarDict -q 20 -Q 10 -G %s -f %s -N %s -b %s -z -c 1 -S 2 -E 3 -g 4 %s | teststrandbias.R | var2vcf_valid.pl -N %s -E -f 0 >%s/%s.vardict.vcf" \
        %(env,ref,vaf,prefix,bamfile,bedfile,prefix,outdir,prefix)
    subprocess.check_call(cmd,shell=True)

def tumor_normal(vaf,tname,tbam,nbam,bed,nname,outdir):
    cmd="%s && VarDict -q 20 -Q 10 -G %s -f %s -N %s -b \"%s|%s\" -z -c 1 -S 2 -E 3 -g 4 %s |testsomatic.R |var2vcf_paired.pl -N \"%s|%s\" -f %s >%s/%s.vardict.vcf" \
        %(env,ref,vaf,tname,tbam,nbam,bed,tname,nname,vaf,outdir,tname)
    subprocess.check_call(cmd,shell=True)
    infile = open("%s/%s.vardict.vcf" % (outdir, tname), "r")
    outfile = open("%s/%s.vardict.somatic.vcf" % (outdir, tname), "w")
    for line in infile:
        line = line.strip()
        if line.startswith("#"):
            outfile.write("%s\n" % (line))
        else:
            p1 = re.compile(r'LikelySomatic')
            p2 = re.compile(r'StrongSomatic')
            a = p1.findall(line)
            b = p2.findall(line)
            if a != [] or b != []:
                outfile.write("%s\n" % (line))
    infile.close()
    outfile.close()

if __name__=="__main__":
    if len(sys.argv)!=6 or len(sys.argv)!=8:
        print("Usgae:")
        print("python3 %s single vaf bamfile bedfile prefix outdir\n" %(sys.argv[0]))
        print("python3 %s pair vaf tname tbam nbam bed nname outdir\n" % (sys.argv[0]))
        print("Copyright:fanyucai")
        print("Version:1.0")
        sys.exit(-1)
    if sys.argv[1]=="single":
        tumor_only(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
    elif sys.argv[1]=="pair":
        tumor_normal(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6],sys.argv[7],sys.argv[8])
    else:
        print("check your parameter!!!!")
