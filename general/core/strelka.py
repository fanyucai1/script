#Email:fanyucai1@126.com

import argparse
import os
import subprocess
def run(tbam,nbam,bed,outdir,ref,python2,strelka,htslib):
    cmd="cd %s && %s %s/configureStrelkaSomaticWorkflow.py --normalBam %s --tumorBam %s --referenceFasta %s --runDir %s"\
        %(outdir,python2,strelka,nbam,tbam,ref,outdir)
    par=""
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if bed!="0":
        subprocess.check_call('cp %s %s/target.bed && %s/bgzip %s/target.bed && %s/tabix -p bed %s/target.bed.gz'
                              %(bed,outdir,htslib,outdir,htslib,outdir),shell=True)
        par+=" --targeted --callRegions %s/target.bed.gz "%(outdir)
    cmd+=par
    subprocess.check_call(cmd,shell=True)
    cmd="cd %s && %s %s/runWorkflow.py -m local -j 20"%(outdir,python2,outdir)
    subprocess.check_call(cmd,shell=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-p","--python2",help="python2 bin",default="/software/python2/Python-v2.7.9/bin/python")
    parser.add_argument("-t","--tbam",help="tumor bam",required=True)
    parser.add_argument("-n","--nbam",help="normal bam",required=True)
    parser.add_argument("-b","--bed",help="bed file",default="0")
    parser.add_argument("-s","--strelka",help="strelka bin",default="/software/strelka/strelka-2.9.10.centos6_x86_64/bin/")
    parser.add_argument("-o","--outdir",help="output directory",required=True)
    parser.add_argument("-r","--ref",help="reference fasta",default="/data/Database/hg19/ucsc.hg19.fasta")
    parser.add_argument('-htslib',"--htslib",help="htslib bin",default="/software/htslib/htslib-v1.9/bin")
    args=parser.parse_args()
    run(args.tbam, args.nbam, args.bed, args.outdir, args.ref, args.python2, args.strelka,args.htslib)