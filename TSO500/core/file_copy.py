import os
import sys
import re
import subprocess
samplelist="/data/TSO500/samplelist.csv"
root_dir="/data/TSO500"
outdir="/data/TSO500/stat/normal_tmb"
if not os.path.exists(outdir):
    os.mkdir(outdir)

infile=open(samplelist,"r")
num=0
counts=0
dict={}
for line in infile:
    num+=1
    line=line.strip()
    array=line.split(",")
    if num==1:
        for k in range(len(array)):
            if array[k]=="Remarks":
                counts=k
    else:
        for k in range(len(array)):
            if array[counts] == "N":
                dict[array[0]]=1

for(root,dirs,files) in os.walk(root_dir):
    for file in files:
        tmp=os.path.join(root,file)
        samplename=tmp.split("/")[-2]
        if tmp.endswith("tmb.tsv") and samplename in dict:
            subprocess.check_call("cp %s %s"%(tmp,outdir),shell=True)