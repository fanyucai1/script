import subprocess
import sys
software="export PATH=/software/java/jdk1.8.0_202/bin:/software/R/R-v3.5.2/bin/:"
software+="/software/vardict/1.5.7/VarDictJava-1.5.7/bin:/software/perl/perl-v5.28.1/bin/:$PATH"
hg19="/data/Database/hg19/ucsc.hg19.fasta"
def tumor_normal(vaf,tumor_name,min_reads,tumor_bam,normal_bam,bed,normal_name,outdir,ref=hg19,env=software):
    cmd="%s && VarDict -th 20 -q 20 -Q 20 -G %s -f %s -N %s -r %s -b \"%s|%s\" -z -c 1 -S 2 -E 3 -g 4 %s |testsomatic.R |var2vcf_paired.pl -M -N \"%s|%s\" -f %s >%s/%s.vardict.vcf" \
        %(env,ref,vaf,tumor_name,min_reads,tumor_bam,normal_bam,bed,tumor_name,normal_name,vaf,outdir,tumor_name)
    subprocess.check_call(cmd,shell=True)
if __name__=="__main__":
    if len(sys.argv)<9:
        print("perl %s tumor_bam normal_bam tumor_name normal_name min_reads bed vaf outdir" %(sys.argv[0]))
        print("\n\nEmail:fanyucai1@126.com")
        print("2019.7.16")
    else:
        tumor_bam=sys.argv[1]
        normal_bam=sys.argv[2]
        tumor_name=sys.argv[3]
        normal_name=sys.argv[4]
        min_reads=sys.argv[5]
        bed=sys.argv[6]
        vaf=sys.argv[7]
        outdir=sys.argv[8]
        if len(sys.argv==11):
            ref=sys.argv[9]
            env=sys.argv[10]
        tumor_normal(vaf, tumor_name, min_reads, tumor_bam, normal_bam, bed, normal_name, outdir, ref=hg19,env=software)