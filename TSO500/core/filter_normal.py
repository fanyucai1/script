import os
import re

root_dir="/data/TSO500"
samplelist="/data/TSO500/samplelist.csv"
outdir="/data/TSO500/stat"
normal=[]
infile=open(samplelist,"r")
outfile=open("%s/normal.filter.tsv"%(outdir),"w")
outfile.write("SampleID\tRaw_counts\tFilter\n")
for line in infile:
    line=line.strip()
    array=line.split(",")
    pattern=re.compile(r'NF')
    a=pattern.findall(array[0])
    if a!=[]:
        normal.append(array[0])
infile.close()
for (root,dirs,files) in os.walk(root_dir):
    for file in files:
        tmp=os.path.join(root,file)
        if tmp.endswith("annovar.tsv"):
            p1=re.compile(r'SNV/(\S+).annovar.tsv')
            b=p1.findall(tmp)
            if b[0] in normal:
                infile=open(tmp,"r")
                num=0
                var_num=0
                for line in infile:
                    line=line.strip()
                    array=line.split("\t")
                    num+=1
                    if num!=1:
                        depth=float(array[-2])+float(array[-3])
                        if depth >50:
                            if float(array[-1].strip("%s"))<=40:
                                var_num+=1
                            if float(array[-1].strip("%s")) > 60 and float(array[-1].strip("%s")) < 95:
                                var_num += 1
                infile.close()
                outfile.write("%s\t%s\t%s\n"%(b[0],num,var_num))
outfile.close()