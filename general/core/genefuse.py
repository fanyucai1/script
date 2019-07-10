#Email:fanyucai1@126.com

import subprocess
import argparse

def run(genefuse,list,ref,pe1,pe2,prefix,outdir):
    cmd="cd %s && %s -r %s -f %s -1 %s -2 %s -h %s.html >%s.result" \
        %(outdir,genefuse,ref,list,pe1,pe2,prefix,prefix)
    subprocess.check_call(cmd,shell=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-g",help="genefuse bin",default="/software/GeneFuse/genefuse")
    parser.add_argument("-l",help="cancer list",default="/software/GeneFuse/genes/cancer.hg19.csv")
    parser.add_argument("-p1",help="5 reads",required=True)
    parser.add_argument("-p2",help="3 reads",required=True)
    parser.add_argument('-p',help="prefix",required=True)
    parser.add_argument('-o',help="output directory",required=True)
    args=parser.parse_args()