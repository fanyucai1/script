import os
import sys
import re

def run(samplesheet,samplelist,analysis,genelist,outdir):
    infile=open(samplesheet,"r")
    sample=[]
    for line in infile:
        line=line.strip()
        array=line.split(",")
        sample.append(array[0])
    infile.close()
    sampleID=[]
    infile=open(samplelist,"r")
    num=0
    for line in infile:
        line = line.strip()
        array = line.split(",")
        num+=1
        if num!=1 and array[0] in sample:
            sampleID.append(array[0])
    infile.close()
    for (root,dirs,files) in os.walk(analysis):
            tmp=os.path.join(root,files)
            array=tmp.split("/")



if __name__=="__main__":
    if len(sys.argv)!=5:
        print("usage:python3 %s SampleSheet.csv samplelist.csv analysis_dir outdir\n"%(sys.argv[0]))
        print("Email:fanyucai1@126.com")
    else:
        samplesheet, samplelist, analysis, outdir=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
        run(samplesheet,samplelist,analysis,outdir)