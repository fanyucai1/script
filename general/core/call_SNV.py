#Email:fanyucai1@126.com

import subprocess
import re
import argparse
import os
from multiprocessing import Process
varscan="/software/VarScan2/VarScan.v2.4.3.jar"
samtools="/software/samtools/samtools-1.9/bin/samtools"
ref="/data/Database/hg19/ucsc.hg19.fasta"
env = "export PATH=/software/java/jdk1.8.0_202/bin:/software/R/R-v3.5.2/bin/:"
env += "/software/vardict/1.5.7/VarDictJava-1.5.7/bin:/software/perl/perl-v5.28.1/bin/:"
env+="/software/samtools/samtools-1.9/bin/:$PATH"
def vardict_pair(args):
    vaf, tname, tbam, nbam, bed, nname, outdir=args.vaf,args.tumor,args.tb,args.nb,args.bed,args.normal,args.prefix
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

def varscan_pair(args):
    vaf, tumor, normal, bed, prefix, outdir=args.vaf,args.tumor,args.normal,args.bed,args.prefix,args.outdir
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    par=""
    if bed!="0":
        par = " -l %s " % (bed)
    def shell_run(cmd):
        subprocess.check_call("%s" % (cmd), shell=True)
    a = "cd %s && %s mpileup -f %s %s %s >%s_normal.mpileup" % (outdir, samtools, ref, par, normal, prefix)
    b = "cd %s && %s mpileup -f %s %s %s >%s_tumor.mpileup" % (outdir, samtools, ref, par, tumor, prefix)
    if __name__ == '__main__':
        p1 = Process(target=shell_run, args=(a,))
        p2 = Process(target=shell_run, args=(b,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        subprocess.check_call(
            "cd %s && java -Xmx10g -jar %s somatic %s_normal.mpileup %s_tumor.mpileup %s --strand-filter 1 --output-vcf 1 --min-var-freq %s --min-coverage 50"
            % (outdir, varscan, prefix, prefix, prefix, vaf), shell=True)
        # filter snp around indel
        subprocess.check_call(
            "cd %s && java -Xmx10g -jar %s somaticFilter %s.snp.vcf --min-coverage 50 --indel-file %s.indel.vcf --output-file %s.filter.snp.vcf --min-var-freq %s"
            % (outdir, varscan, prefix, prefix, prefix,vaf), shell=True)
        # separate a somatic output file by somatic_status (Germline, Somatic, LOH)
        c = "cd %s && java -Xmx10g -jar %s processSomatic %s.filter.snp.vcf --min-tumor-freq %s" % (outdir, varscan, prefix, vaf)
        d = "cd %s && java -Xmx10g -jar %s processSomatic %s.indel.vcf --min-tumor-freq %s" % (outdir, varscan, prefix, vaf)
        p3 = Process(target=shell_run, args=(c,))
        p4 = Process(target=shell_run, args=(d,))
        p3.start()
        p4.start()
        p3.join()
        p4.join()

parser = argparse.ArgumentParser("Call SNV from tumor-normal use vardict and varscan.")
subparsers = parser.add_subparsers(dest='SNV')
parser_a = subparsers.add_parser("vardict",help="vardict call SNV")
parser_a.add_argument("-b", "--bed", help="target bed file", default="0", type=str)
parser_a.add_argument("-t", "--tb", help="tumor bam file", type=str, required=True)
parser_a.add_argument("-n", "--nb", help="normal bam file", type=str, required=True)
parser_a.add_argument("-v", "--vaf", help="vaf", type=float, required=True)
parser_a.add_argument("-tumor", help="tumor name", required=True)
parser_a.add_argument("-normal", help="normal name", required=True)
parser_a.set_defaults(func=vardict_pair)

parser_b = subparsers.add_parser("varscan", help="varscan call SNV")
parser_b.add_argument("-b", "--bed", help="target bed file", default="0",type=str)
parser_b.add_argument("-t", "--tumor", help="tumor bam file", type=str, required=True)
parser_b.add_argument("-n", "--normal", help="normal bam file", type=str, required=True)
parser_b.add_argument("-v", "--vaf", help="vaf", type=float, required=True)
parser_b.add_argument("-o", "--outdir", help="output directory", required=True)
parser_b.add_argument("-p", "--prefix", help="prefix of output", required=True)
parser_b.set_defaults(func=varscan_pair)

args = parser.parse_args()
args.func(args)
