import sys
import argparse
import os
import subprocess
def run(tbam,nbam,bed,outdir,ref,python2,strelka):
    cmd="cd %s && %s %s/configureStrelkaSomaticWorkflow.py --normalBam %s --tumorBam %s --referenceFasta %s --runDir %s"\
        %(outdir,python2,strelka,nbam,tbam,ref,outdir)
    par=""
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if bed!="0":
        par+=" --targeted --callRegions %s "%(bed)
    cmd+=par
    subprocess.check_call(cmd,shell=True)
    cmd="cd %s && %s %s/runWorkflow.py -m local -j 20"%(outdir,python2,outdir)
    subprocess.check_call(cmd,shell=True)


if __name__=="__main__":
