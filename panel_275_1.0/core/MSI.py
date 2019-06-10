import subprocess
import sys
MSIsensor="/software/MSIsensor/msisensor-0.6/msisensor/msisensor.py"
python2="/software/python2/Python-v2.7.9/bin/python"
models="/software/MSIsensor/msisensor-0.6/msisensor/models_hg19_275genes"
def run_msi(bamfile,out):
    cmd="%s %s msi -t %s -o %s.msi.tsv -M %s" %(python2,MSIsensor,bamfile,out,models)
    subprocess.check_call(cmd,shell=True)

if __name__=="__main__":
    if len(sys.argv)!=3:
        print("python3 MSI.py bamfile outdir_prefix\n")
        sys.exit(-1)
    bamfile=sys.argv[1]
    out=sys.argv[2]
    run_msi(bamfile,out)