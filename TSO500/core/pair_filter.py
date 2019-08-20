import os
import sys
import re
root_dir="/data/TSO500"
list="/data/TSO500/samplelist.csv"

outdir="/data/TSO500/tumor_normal_pair"
if not os.path.exists(outdir):
    os.mkdir(outdir)
infile=open(list,"r")
num=0
normal=[]
tumor=[]
for line in infile:
    num+=1
    line=line.strip()
    array=line.split(",")
    if num!=1 and array[-2]=="DNA":
        t=re.compile(r'(\S+TF)')
        n=re.compile(r'(\S+NF)')
        a=t.findall(array[0])
        b=n.findall(array[0])
        if a!=[]:
            tumor.append(array[0])
        if b!=[]:
            normal.append(array[0])
infile.close()
out_total=open("%s/tumor_vs_normal.tsv"%(outdir),"w")
out_total.write("Tumor\tNormal\tTumor_unique\tOverlap\tNormal_unique\n")
for key in tumor:
    dict_t={}
    dict_n={}
    name = re.compile(r'(\S+)TF')
    sampleID = name.findall(key)
    t_unique,n_unique,common=0,0,0
    for key1 in normal:
        if re.search(sampleID[0],key1):
            #outfile_t=open("%s/%s.unique.tsv"%(outdir,key),"w")
            #outfile_n=open("%s/%s.unqiue.tsv"%(outdir,key1),"w")
            #overlap=open("%s/%s_common_%s.tsv"%(outdir,key,key1),"w")
            for (root,dirs,files) in os.walk(root_dir):
                for dir in dirs:
                    n_path = root + "/" + dir + "/SNV/"+key1+".annovar.tsv"
                    if os.path.exists(n_path):
                        infile=open(n_path,"r")
                        for line in infile:
                            line=line.strip()
                            array=line.split("\t")
                            tmp=array[0]+"_"+array[1]+"_"+array[2]+"_"+array[3]+"_"+array[4]
                            dict_n[tmp]=line
                        infile.close()
                for dir in dirs:
                    t_path = root + "/" + dir + "/SNV/" + key + ".annovar.tsv"
                    if os.path.exists(t_path):
                        infile=open(t_path,"r")
                        num=0
                        for line in infile:
                            num+=1
                            line=line.strip()
                            array=line.split("\t")
                            tmp=array[0]+"_"+array[1]+"_"+array[2]+"_"+array[3]+"_"+array[4]
                            dict_t[tmp]=line
                            if num == 1:
                                """"""
                                #outfile_t.write("%s\n" % (line))
                                #outfile_n.write("%s\n" % (line))
                                #overlap.write("%s\n" % (line))
                            else:
                                if not tmp in dict_n:
                                    t_unique+=1
                                    #outfile_t.write("%s\n" % (line))
                                else:
                                    common+=1
                                    #overlap.write("%s\n" % (line))
            for tmp1 in dict_n:
                if not tmp1 in dict_t:
                    #outfile_n.write("%s\n" % (dict_n[tmp1]))
                    n_unique+=1
            #outfile_t.close()
            #overlap.close()
            #outfile_n.close()
            out_total.write("%s\t%s\t%s\t%s\t%s\n" % (key, key1,t_unique,common,n_unique))