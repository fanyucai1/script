#Email:fanyucai1@126.com
#2019.5.24

import os
import argparse
import re
import subprocess

parser=argparse.ArgumentParser("")
parser.add_argument("-d","--dir",help="analyis directory",required=True)
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
parser.add_argument("-s","--samplelist",help="sample list",required=True)
args=parser.parse_args()

infile=open(args.samplelist,"r")
sample=[]
for line in infile:
    line=line.strip()
    array=re.split('[\t,]',line)
    sample.append(array[0])
infile.close()
for id in sample:
    path=args.dir+"/Logs_Intermediates/CNV/%s_CopyNumberVariants.vcf" %(id)
    print (path)
    if os.path.exists(path):
        infile=open(path,"r")
        outfile=open("%s/%s.cnv.tsv" %(args.outdir,id),"w")
        outfile.write("#Chr\tStart\tend\tRef\tType\tGene\n")
        i=0
        for line in infile:
            if not line.startswith("#"):
                line = line.strip()
                array = line.split()
                if array[4]=="<DUP>" or array[4]=="<DEL>":
                    if array[6]=="PASS":
                        i+=1
                        p1=re.compile(r'END=(\d+)')
                        p2=re.compile(r'ANT=(\S+)')
                        a=p1.findall(line)
                        b=p2.findall(line)
                        tmp = array[0] + "\t" + array[1] +"\t"+a[0]+"\t"+array[3]+"\t"+array[4]+"\t"+b[0]
                        outfile.write("%s\n"%(tmp))
        outfile.close()
        if i==0:
            subprocess.check_call("rm -rf %s/%s.cnv.tsv" %(args.outdir,id),shell=True)
            print("sample %s not find CNV"%(id))