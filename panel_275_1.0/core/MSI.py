import subprocess
import sys
import os

MSIsensor="/software/MSIsensor/msisensor-0.6/msisensor/msisensor.py"
python2="/software/python2/Python-v2.7.9/bin/python"
models="/software/MSIsensor/msisensor-0.6/msisensor/models_hg19_275genes"
def run_msi(bamfile,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    cmd="%s %s msi -t %s -o %s.msi.tsv -M %s" %(python2,MSIsensor,bamfile,out,models)
    subprocess.check_call(cmd,shell=True)

if __name__=="__main__":
    if len(sys.argv)!=4:
        print("python3 MSI.py bamfile outdir prefix\n")
        sys.exit(-1)
    bamfile=sys.argv[1]
    outdir=sys.argv[2]
    prefix=sys.argv[3]
    run_msi(bamfile,outdir,prefix)