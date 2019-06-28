#Email:fanyucai1@126.com
#2019.6.28

import argparse
import os
import re
def run(indir="/data/Panel275/"):
    MSI={}
    sample=[]
    for root,dirs,files in os.walk(indir):
        for file in files:
            pattern = re.compile(r'msi.tsv$')
            if pattern.findall(file):
                filename=os.path.join(root, file)
                sample=file.split(".")
                infile=open(filename,'r')
                num=0
                for line in infile:
                    num+=1
                    line=line.strip()
                    array=line.split()
                    if num==2:
                        MSI[sample[0]]=array[2]
                        print (sample[0],"\t",array[2])

if __name__=="__main__":
    run(indir="/data/Panel275/")




