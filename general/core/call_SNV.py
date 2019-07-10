#Email:fanyucai1@126.com

import subprocess
import re
import sys

env="export PATH=/software/java/jdk1.8.0_202/bin:/software/R/R-v3.5.2/bin/:"
env+="/software/vardict/1.5.7/VarDictJava-1.5.7/bin:/software/perl/perl-v5.28.1/bin/:$PATH"
ref="/data/Database/hg19/ucsc.hg19.fasta"

def vardict(vaf,tname,tbam,nbam,bed,nname,outdir):

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
            c3=p3.findall(line)
            if a != [] or b != []:
                outfile.write("%s\n" % (line))
    infile.close()
    outfile.close()

