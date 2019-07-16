import subprocess
import argparse
env="export PATH=/software/java/jdk1.8.0_202/bin:/software/R/R-v3.5.2/bin/:"
env+="/software/vardict/1.5.7/VarDictJava-1.5.7/bin:/software/perl/perl-v5.28.1/bin/:$PATH"

def tumor_normal(args):
    cmd="%s && VarDict -q 20 -Q 20 -G %s -f %s -N %s -r %s -b \"%s|%s\" -z -c 1 -S 2 -E 3 -g 4 %s |testsomatic.R |var2vcf_paired.pl -M -N \"%s|%s\" -f %s >%s/%s.vardict.vcf" \
        %(env,args.ref,args.vaf,args.tn,args.min,args.tb,args.nb,args.bed,args.tm,args.nn,args.vaf,args.outdir,args.tn)
    subprocess.check_call(cmd,shell=True)
if __name__=="__main__":
    parser=argparse.ArgumentParser("Vardict call CNV.")
    parser.add_argument("-m","--min",help="The minimum # of variant reads, default 5",required=True,default=5,type=int)
    parser.add_argument("-tb","--tb",help="tumor bam file",required=True)
    parser.add_argument("-nb","--nb",help="normal bam file",required=True)
    parser.add_argument("-v","--vaf",help="The threshold for allele frequenc",choices=[0.01,0.001,0.02,0.05,0.005],required=True,type=float)
    parser.add_argument("-tn","--tn",required=True,help="tumor sample name")
    parser.add_argument("-nn", "--nn", required=True, help="normal sample name")
    parser.add_argument("-o","--outdir",required=True,help="output directory")
    parser.add_argument("-b","--bed",required=True,help="bed file")
    parser.add_argument("-r","--ref",help="reference fasta",default="/data/Database/hg19/ucsc.hg19.fasta")
    parser.set_defaults(func=tumor_normal)
    args=parser.parse_args()
    args.func()