import subprocess
import os
import argparse


def pairs(tumor, normal, bedfile, coverage, outdir, prefix, fdr=0.05):
    msisensor = "/software/MSIsensor/msisensor-0.5/msisensor"
    ref="/data/Database/hg19/ucsc.hg19.fasta"
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out = outdir + "/" + prefix
    subprocess.check_call("%s scan -d %s -o %s/microsatellites.list" % (msisensor, ref, outdir), shell=True)
    if bedfile!="0":
        par = " -n %s -e %s -f %s -t %s -o %s.MSI -c %s " % (normal, bedfile, fdr, tumor, outdir, coverage)
    else:
        par = " -n %s -f %s -t %s -o %s -c %s " % (normal, fdr, tumor, out, coverage)
    subprocess.check_call("%s msi -d %s/microsatellites.list %s " % (msisensor, outdir, par), shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Run MSI analysis.")
    parser.add_argument("-n", "--normal", type=str, help="normal bam file",required=True)
    parser.add_argument("-t", "--tumor", type=str, help="tumor bam file", required=True)
    parser.add_argument("-o", "--outdir", type=str, help="output directory", default=os.getcwd())
    parser.add_argument("-p", "--prefix", type=str, help="prefix of output")
    parser.add_argument("-e", "--bed", type=str, help="bed file,optional",default="0")
    parser.add_argument("-c", "--coverage", type=int, help="WXS: 20; WGS: 15", required=True)
    parser.add_argument("-f", "--fdr", type=float, help="FDR threshold, default=0.05", default=0.05)
    args = parser.parse_args()
    pairs(args.tumor, args.normal, args.bedfile, args.coverage, args.outdir, args.prefix, fdr=0.05)