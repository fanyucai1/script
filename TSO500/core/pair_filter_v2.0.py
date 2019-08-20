import os
import re
root_dir="/data/TSO500"
list="/data/TSO500/samplelist.csv"
outdir="/data/TSO500/tumor_normal_pair"
if not os.path.exists(outdir):
    os.mkdir(outdir)
infile=open(list,"r")
normal,tumor=[],[]
for line in infile:
    line=line.strip()
    array=line.split(",")
    if array[-1]=="DNA":
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
    dict_t, dict_n = {}, {}
    t_unique, n_unique, common = 0, 0, 0
    key1=key.replace("TF","NF")
    for (root,dirs,files) in os.walk(root_dir):
        for file in files:
            path=os.path.join(root,file)
            if re.search(key,path):
                infile = open(path, "r")
                num=0
                for line in infile:
                    num+=1
                    line = line.strip()
                    array = line.split("\t")
                    tmp = array[0] + "_" + array[1] + "_" + array[2] + "_" + array[3] + "_" + array[4]
                    if num!=1:
                        dict_t[tmp] = line
                infile.close()
    ###############################################
    for (root, dirs, files) in os.walk(root_dir):
        for file in files:
            path=os.path.join(root,file)
            if re.search(key1,path):
                 infile=open(path,"r")
                 num=0
                 for line in infile:
                     num+=1
                     line = line.strip()
                     array = line.split("\t")
                     tmp = array[0] + "_" + array[1] + "_" + array[2] + "_" + array[3] + "_" + array[4]
                     if num!=1:
                        dict_n[tmp] = line
                        if tmp in dict_t:
                            common+=1
                        else:
                            n_unique+=1
                     else:
                         pass
                 infile.close()
    for key in dict_t:
        if not key in dict_n:
            t_unique+=1
    out_total.write("%s\t%s\t%s\t%s\t%s\n" % (key, key1, t_unique, common, n_unique))
    out_total.close()