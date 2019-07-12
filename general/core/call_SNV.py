#Email:fanyucai1@126.com

import subprocess
import re
import argparse
import os
from multiprocessing import Process
import configparser
class Myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
    def optionxform(self, optionstr):
        return optionstr
###############################################
def vardict_pair(args):
    bed = args.bed
    tbam = args.tbam
    nbam = args.nbam
    vaf = args.vaf
    tname = args.tumor
    nname = args.normal
    outdir = args.outdir
    cmd="%s && VarDict -q 20 -Q 10 -G %s -f %s -N %s -b \"%s|%s\" -z -c 1 -S 2 -E 3 -g 4 %s |testsomatic.R |var2vcf_paired.pl -N \"%s|%s\" -f %s >%s/%s.vardict.vcf" \
        %(env,ref,vaf,tname,tbam,nbam,bed,tname,nname,vaf,outdir,tname)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
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
###############################################
def varscan_pair(args):
    bed = args.bed
    tumor = args.tbam
    normal = args.nbam
    vaf = args.vaf
    prefix=args.tumor+"_"+args.normal
    outdir = args.outdir
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    par=""
    if bed!="0":
        par = " -l %s " % (bed)
    def shell_run(cmd):
        subprocess.check_call("%s" % (cmd), shell=True)
    a = "%s && samtools mpileup -f %s %s %s >%s_normal.mpileup" % (env, ref, par, normal, out)
    b = "%s && samtools mpileup -f %s %s %s >%s_tumor.mpileup" % (env, ref, par, tumor, out)
    p1 = Process(target=shell_run, args=(a,))
    p2 = Process(target=shell_run, args=(b,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    subprocess.check_call(
        "%s && cd %s && java -Xmx10g -jar %s somatic %s_normal.mpileup %s_tumor.mpileup %s --strand-filter 1 --output-vcf 1 --min-var-freq %s --min-coverage 50"
        % (env,outdir, varscan, prefix, prefix, prefix, vaf), shell=True)
    # filter snp around indel
    subprocess.check_call(
        "%s && cd %s && java -Xmx10g -jar %s somaticFilter %s.snp.vcf --min-coverage 50 --indel-file %s.indel.vcf --output-file %s.filter.snp.vcf --min-var-freq %s"
        % (env,outdir, varscan, prefix, prefix, prefix,vaf), shell=True)
    # separate a somatic output file by somatic_status (Germline, Somatic, LOH)
    c = "%s && cd %s && java -Xmx10g -jar %s processSomatic %s.filter.snp.vcf --min-tumor-freq %s" % (env,outdir, varscan, prefix, vaf)
    d = "%s && cd %s && java -Xmx10g -jar %s processSomatic %s.indel.vcf --min-tumor-freq %s" % (env,outdir, varscan, prefix, vaf)
    p3 = Process(target=shell_run, args=(c,))
    p4 = Process(target=shell_run, args=(d,))
    p3.start()
    p4.start()
    p3.join()
    p4.join()
##########################################################################
parser = argparse.ArgumentParser("Call SNV from tumor-normal use MuTect2,vardict and varscan.")
parser.add_argument("-c","--config",required=True,help="config file")
subparsers = parser.add_subparsers(dest='SNV')
parser_a = subparsers.add_parser("vardict",help="vardict call SNV")
parser_a.add_argument("--bed", help="target bed file", default="0", type=str)
parser_a.add_argument("--tbam", help="tumor bam file", type=str, required=True)
parser_a.add_argument("--nbam", help="normal bam file", type=str, required=True)
parser_a.add_argument("--vaf", help="vaf", type=float, required=True,choices=[0.01,0.02,0.05,0.001])
parser_a.add_argument("-tumor", help="tumor name", required=True)
parser_a.add_argument("-normal", help="normal name", required=True)
parser_a.add_argument("--outdir", help="output directory", required=True)
parser_a.set_defaults(func=vardict_pair)

parser_b = subparsers.add_parser("varscan", help="varscan call SNV")
parser_b.add_argument("--bed", help="target bed file", default="0", type=str)
parser_b.add_argument("--tbam", help="tumor bam file", type=str, required=True)
parser_b.add_argument("--nbam", help="normal bam file", type=str, required=True)
parser_b.add_argument("--vaf", help="vaf", type=float, required=True,choices=[0.01,0.02,0.05,0.001])
parser_b.add_argument("-tumor", help="tumor name", required=True)
parser_b.add_argument("-normal", help="normal name", required=True)
parser_b.add_argument("--outdir", help="output directory", required=True)
parser_b.set_defaults(func=varscan_pair)

args = parser.parse_args()
##############################################
config = Myconf()
config.read(args.config)
java=config['software']['java']
R=config['software']['R']
perl=config['software']['perl']
VarDict=config['software']['VarDict']
samtools=config['software']['samtools']
ref=config['database']['ref']
varscan=config['software']['varscan']
env="export PATH=%s:%s:%s:%s:$PATH" %(java,R,perl,VarDict)
##############################################
args.func(args)
