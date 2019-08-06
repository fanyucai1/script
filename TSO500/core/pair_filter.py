import os
import sys
import re
dir="/data/TSO500"
list="/data/TSO500/samplelist.csv"

outdir=os.getcwd()
infile=open(list,"r")
num=0
normal=[]
tumor=[]
for line in infile:
    num+=1
    line=line.strip()
    array=line.split("\t")
    if num!=1:
        t=re.compile(r'(\S+[TF])')
        n=re.compile(r'(\S+[NF])')
        a=t.findall(array[0])
        b=n.findall(array[0])
        if a!=[]:
            tumor.append(array[0])
        if b!=[]:
            normal.append(array[0])
infile.close()
for key in tumor:
    dict={}
    name = re.compile(r'(\S+[TF])')
    for key1 in normal:
        c = name.findall(key1)
        if c!=[]:
            print("tumor %s and normal %s are pair"%(key,key1))
            outfile=open("%s/%s_%s.annovar.tsv"%(outdir,key,key1),"w")
            for (root,dirs,files) in os.walk(dir):
                for dir in dirs:
                    n_path = root + "/" + dir + "/SNV/"+key1+".annovar.tsv"
                    if os.path.exists(n_path):
                        infile=open(n_path,"r")
                        for line in infile:
                            line=line.strip()
                            dict[line]=1
                        infile.close()
                        continue
                for dir in dirs:
                    t_path = root + "/" + dir + "/SNV/" + key + ".annovar.tsv"
                    if os.path.exists(t_path):
                        infile=open(t_path,"r")
                        num=0
                        for line in infile:
                            num+=1
                            line=line.strip()
                            if num==1 or not line in dict:
                                outfile.write("%s\n" % (line))
                        continue
            outfile.close()