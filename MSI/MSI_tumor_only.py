#Email:fanyucai1@126.com
#2019.8.19

import os
import argparse
import subprocess

msisensor="/software/MSIsensor/MSIsensor-v0.6/msisensor-0.6/msisensor"
ref="/data/Database/hg19/ucsc.hg19.fasta"

def single(args):
    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)
    out=args.outdir+"/"+args.prefix
    subprocess.check_call("%s scan -d %s -o %s/microsatellites.list" % (msisensor, ref, args.outdir),shell=True)
    cmd="%s msi -d %s/microsatellites.list -t %s -e %s -o %s" %(msisensor,args.outdir,args.tumor,args.bed,out)
    subprocess.check_call(cmd,shell=True)

def pair(args):
    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)
    out = args.outdir + "/" + args.prefix
    subprocess.check_call("%s scan -d %s -o %s/microsatellites.list" % (msisensor, ref, args.outdir), shell=True)
    cmd = "%s msi -d %s/microsatellites.list -n %s -t %s -e %s -o %s" % (msisensor, args.outdir, args.normal,args.tumor, args.bed, out)
    subprocess.check_call(cmd, shell=True)

parser=argparse.ArgumentParser("microsatellite instability detection using tumor only or paired tumor-normal data.")
parser.add_argument("-o","--outdir",help="output directory")
parser.add_argument("-p","--prefix",help="prefix of output")
parser.add_argument("-b","--bed",help="bed file")
parser.add_argument("-c","--coverage",type=str,help="coverage threshold for msi analysis, WXS: 20; WGS: 15",required=True)
parser.add_argument("-f","--fdr",type=str,help="FDR threshold for somatic sites detection, default=0.05",default=0.05)
subparsers =parser.add_subparsers()

parser_a = subparsers.add_parser("single",help="tumor only")
parser_a.add_argument("-t","--tumor",help="tumor bam file")
parser_a.set_defaults(func=single)

parser_b = subparsers.add_parser("pair",help="tumor vs normal")
parser_b.add_argument("-t","--tumor",help="tumor bam file")
parser_b.add_argument("-n","--normal",help="normal bam file")
parser_a.set_defaults(func=pair)

args = parser.parse_args()
args.func(args)