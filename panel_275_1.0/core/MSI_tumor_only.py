import subprocess
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

if __name__=="__main__":
    parser=argparse.ArgumentParser("Run MSI analysis.")
    parser.add_argument("-t", "--tumor", type=str, help="tumor bam file", required=True)
    parser.add_argument("-o", "--outdir", type=str, help="output directory", default=os.getcwd())
    parser.add_argument("-p", "--prefix", type=str, help="prefix of output", default="MSI")
    args = parser.parse_args()
    run_msi(args.tumor,args.outdir,args.prefix)