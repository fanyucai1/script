#Email:fanyucai1@126.com
#2019.6.28

import argparse
import os
import re
def run(samplelist,indir="/data/Panel275/"):
    infile=open(samplelist,"r")
    sample={}
    MSI={}
    for line in infile:
        line=line.strip()
        array=line.split()
        sample[array[0]]=1
    infile.close()
    for root,dirs,files in os.walk(indir):
        for dir in dirs:
            for file in files:
                tmp=root+"/"+dir+"/"+file
                pattern=re.compile(r'msi.tsv')
                if pattern.findall(tmp) and os.path.exists(tmp):
                    infile=open(tmp,'r')
                    num=0
                    for line in infile:
                        num+=1
                        line=line.strip()
                        array=line.split()
                        if num==2:
                            id=file.split(".")
                            MSI[id[0]]=array[2]
                            print (id[0],"\t",array[2])






