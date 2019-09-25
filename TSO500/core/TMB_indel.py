import os
import sys
import re
samplelist="/data/TSO500/samplelist.csv"
indir="/data/TSO500/"

infile=open(samplelist,"r")
outfile=open("/data/TSO500/stat/TMB_classify.tsv","w")
outfile.write("SampleID\tRaw_TMB\tSNV_TMB\tInsertion_TMB\tDeletion_TMB\tIndel_TMB\n")
num=0
sampleID={}
rate=0
tumor=0
for line in infile:
    line=line.strip()
    array=line.split(",")
    num+=1
    if num==1:
        for k in range(len(array)):
            if array[k] == "rate":
                rate=k
            if array[k]=="Remarks":
                tumor=k
    else:
        if array[rate]!="E"  and array[tumor]=="T":
            sampleID[array[0]]=1
infile.close()

raw,snv,insertion,deletion,indel={},{},{},{},{}
for root,dirs,files in os.walk(indir):
    for file in files:
        tmp=os.path.join(root,file)
        if tmp.endswith(".tmb.tsv"):
            array=tmp.split("/")
            if array[-2] in sampleID:
                infile=open(tmp,"r")
                num = 0
                indel[array[-2]],raw[array[-2]],snv[array[-2]],insertion[array[-2]],deletion[array[-2]]=0,0,0,0,0
                for line in infile:
                    line = line.strip()
                    array1 = line.split("\t")
                    num+=1
                    if array1[-1]=="True":
                        raw[array[-2]]+=1
                        if array1[8]=="SNV":
                            snv[array[-2]]+=1
                        if array1[8]=="insertion":
                            insertion[array[-2]]+=1
                        if array1[8]=="deletion":
                            deletion[array[-2]]+=1
                indel[array[-2]]=insertion[array[-2]]+deletion[array[-2]]
                infile.close()
for key in snv:
    outfile.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(key,raw[key],snv[key],insertion[key],deletion[key],indel[key]))
outfile.close()
