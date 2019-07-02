import subprocess
import sys
import os
import argparse
def run_msi(bamfile,outdir,prefix):
    MSIsensor = "/software/MSIsensor/msisensor-0.6/msisensor/msisensor.py"
    python2 = "/software/python2/Python-v2.7.9/bin/python"
    models = "/software/MSIsensor/msisensor-0.6/msisensor/models_hg19_275genes"
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    cmd="%s %s msi -t %s -o %s.msi.tsv -M %s" %(python2,MSIsensor,bamfile,out,models)
    subprocess.check_call(cmd,shell=True)


def pairs(ref,tumor,normal,bedfile,coverage,outdir,prefix,fdr=0.05):
    msisensor = "/software/MSIsensor/msisensor-0.5/msisensor"
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    subprocess.check_call("%s scan -d %s -o %s/microsatellites.list" % (msisensor, ref,outdir),shell=True)
    par=" -n %s -e %s -f %s -t %s -o %s -c %s "%(normal,bedfile,fdr,tumor,outdir,coverage)
    subprocess.check_call("%s msi -d %s/microsatellites.list %s " % (msisensor, outdir, par), shell=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser("Run MSI analysis.")
    parser.add_argument("-n", "--normal", type=str, help="normal bam file",default="0")
    parser.add_argument("-r", "--ref", type=str, help="reference genome fasta", required=True)
    parser.add_argument("-t", "--tumor", type=str, help="tumor bam file", required=True)
    parser.add_argument("-o", "--outdir", type=str, help="output directory", default=os.getcwd())
    parser.add_argument("-p", "--prefix", type=str, help="prefix of output", default="MSI")
    parser.add_argument("-e", "--bed", type=str, help="bed file,optional")
    parser.add_argument("-c", "--coverage", type=int, help="WXS: 20; WGS: 15",required=True)
    parser.add_argument("-f", "--fdr", type=float, help="FDR threshold, default=0.05",default=0.05)
    args = parser.parse_args()
    if args.normal!=0:
        run_msi(args.tumor,outdir,prefix)
    else:
