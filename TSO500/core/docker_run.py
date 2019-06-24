
import os
import sys
import argparse
import subprocess
def run(input,analysis,samplesheet500,samplesheet170=0):
    subprocess.check_call("cp %s %s/SampleSheet.csv"%(samplesheet500,input),shell=True)
    cmd="/software/TSO500/1.3.1/TruSight_Oncology_500.sh --user=1006 --remove --resourcesFolder=/software/TSO500/1.3.1/resources"
    cmd+=" --analysisFolder %s ----runFolder %s " %(analysis,input)
    subprocess.check_call(cmd,shell=True)
    if samplesheet170 !=0:
        subprocess.check_call("cp %s %s/SampleSheet.csv"%(samplesheet170,input),shell=True)
        cmd="docker run -t -v /etc/localtime:/etc/localtime -v %s:/data/ "%(input)
        cmd+=" -v /software/TST170/version_1.0/genomes:/genomes -v %s:/analysis/ " %(analysis)
        cmd+=" docker-oncology.dockerhub.illumina.com/zodiac/tst170localapp:1.0.1.0 "
        subprocess.check_call(cmd,shell=True)
    else:
        pass


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input",help="data directory",required=True)
    parser.add_argument("-a","--analysis",help="analysis directory",required=True)
    parser.add_argument("-s500","---samplesheet500",help="samplesheet TSO500",required=True)
    parser.add_argument("-s170", "---samplesheet170", help="samplesheet TST170", default="0")
    args=parser.parse_args()
    run(args.input,args.analysis,args.samplesheet500,args.samplesheet170)