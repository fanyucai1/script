import os
import sys
import re
root_dir="/data/TSO500"
list="/data/TSO500/samplelist.csv"

outdir=os.getcwd()
infile=open(list,"r")
num=0
normal=[]
tumor=[]
for line in infile:
    num+=1
    line=line.strip()
    array=line.split(",")
    if num!=1:
        t=re.compile(r'(\S+TF)')
        n=re.compile(r'(\S+NF)')
        a=t.findall(array[0])
        b=n.findall(array[0])
        if a!=[]:
            tumor.append(array[0])
        if b!=[]:
            normal.append(array[0])
infile.close()
for key in tumor:
    dict_t={}
    dict_n={}
    name = re.compile(r'(\S+)TF')
    sampleID = name.findall(key)
    for key1 in normal:
        if re.search(sampleID[0],key1):
            print("tumor %s and normal %s are pair"%(key,key1))
            outfile_t=open("%s/%s_%s.annovar.tsv"%(outdir,key,key1),"w")
            outfile_n=open("%s/%s_%s.annovar.tsv"%(outdir,key1,key),"w")
            overlap=open("%s/%s_overlap_%s.annovar.tsv"%(outdir,key1,key),"w")
            for (root,dirs,files) in os.walk(root_dir):
                for dir in dirs:
                    n_path = root + "/" + dir + "/SNV/"+key1+".annovar.tsv"
                    if os.path.exists(n_path):
                        infile=open(n_path,"r")
                        for line in infile:
                            line=line.strip()
                            dict_n[line]=1
                        infile.close()
                for dir in dirs:
                    t_path = root + "/" + dir + "/SNV/" + key + ".annovar.tsv"
                    if os.path.exists(t_path):
                        infile=open(t_path,"r")
                        num=0
                        for line in infile:
                            num+=1
                            line=line.strip()
                            dict_t[line]=1
                            if num == 1:
                                outfile_t.write("%s\n" % (line))
                                outfile_n.write("%s\n" % (line))
                                overlap.write("%s\n" % (line))
                            else:
                                if not line in dict:
                                    outfile_t.write("%s\n" % (line))
                                else:
                                    overlap.write("%s\n" % (line))
            for line in dict_n:
                if not line in dict_t:
                    outfile_n.write("%s\n" % (line))

            outfile_t.close()
            overlap.close()
            outfile_n.close()