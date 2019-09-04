#Email:fanyucai1@126.com
import os
import re

samplelist="/data/TSO500/samplelist.csv"
root_dir="/data/TSO500/"
outdir="/data/TSO500/stat"
dict={}
infile=open(samplelist,"r")
counts=0
name=0
for line in infile:
    counts+=1
    line=line.strip()
    array=line.split(",")
    if counts==1:
        for k in range(len(array)):
            if array[k]=="Remarks":
                name=k
    else:
       if array[name]=="N":
           dict[array[0]]=0
infile.close()
outfile=open("%s/normal_false_somatic.tsv"%(outdir),"w")
outfile.write("SampleID\tIllumina\tOur\tVAF40\tVAF30\tVAF20\tVAF10\tVAF5\n")
for(root,dirs,files) in os.walk(root_dir):
    for file in files:
        tmp=os.path.join(root,file)
        sample=tmp.split("/")
        id=sample[-1].split(".")
        if tmp.endswith(".tmb.tsv") and id[0] in dict:
            Illumina,num,VAF5,VAF10,VAF20,VAF30,VAF40=0,0,0,0,0,0,0
            row=0
            infile=open(tmp,"r")
            f1, f2, f3, f4 ,f5,f6= 0, 0, 0, 0,0,0
            for line in infile:
                line=line.strip()
                array=line.split("\t")
                row+=1
                if row ==1:
                    for k in range(len(array)):
                        if array[k]=="GermlineFilterDatabase":
                            f1=k
                        if array[k] == "SomaticStatus":
                            f2=k
                        if array[k] == "CodingVariant":
                            f3=k
                        if array[k] == "GermlineFilterProxi":
                            f4=k
                        if array[k]=="Nonsynonymous":
                            f5=k
                        if array[k]=="VAF":
                            f6=k
                else:
                    if array[f1]=="False" and array[f2]=="Somatic" and array[f3]=="True" and array[f4]=="False":
                        Illumina+=1
                        if array[f5]=="True":
                            num+=1
                            if float(array[f6])<=5:
                                VAF5+=1
                            if float(array[f6])<=10:
                                VAF10+=1
                            if float(array[f6])<=20:
                                VAF20+=1
                            if float(array[f6])<=30:
                                VAF30+=1
                            if float(array[f6]) <= 40:
                                VAF40+=1
            infile.close()
            outfile.write ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(id[0],Illumina,num,VAF40,VAF30,VAF20,VAF10,VAF5))
outfile.close()