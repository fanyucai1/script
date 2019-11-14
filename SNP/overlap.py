import os
import sys
import re
####################################
infile=open("Contamination.bed","r")
site={}
for line in infile:
    line=line.strip()
    array=line.split("\t")
    tmp=array[0]+"_"+array[2]
    site[tmp]=line
infile.close()
####################################
num=0
infile=open("iSNP.bed","r")
for line in infile:
    line=line.strip()
    array=line.split("\t")
    for i in range(int(array[1]), int(array[2])+1):
        tmp = array[0] + "_" + str(i)
        if tmp in site:
            print(tmp)
            num+=1
infile.close()
print(num)
####################################
"""
final_site={}
counts=0
infile=open("panel_27.bed","r")
for line in infile:
    line = line.strip()
    array = line.split("\t")
    for i in range(int(array[1]),int(array[2])):
        tmp=array[0]+"_"+str(i)
        if tmp in site:
            final_site[tmp]=site[tmp]
            counts+=1
infile.close()
print("There are total %s sites"%(counts))
####################################
root_dir="/data/Project/liaorui/panel_27/"
site_counts={}
for (root,dirs,files) in os.walk(root_dir):
    for file in files:
        tmp=os.path.join(root,file)
        if tmp.endswith("_N.Germline.PASS.Annot.xls") and re.search(r'ana_19',tmp):
            infile=open(tmp,"r")
            for line in infile:
                line = line.strip()
                array = line.split("\t")
                pos=array[0]+"_"+array[1]
                if pos in final_site:
                    if not "%s_%s_%s_%s" % (array[0], array[1], array[3], array[4]) in site_counts:
                        site_counts["%s_%s_%s_%s" % (array[0], array[1], array[3], array[4])]=1
                    else:
                        site_counts["%s_%s_%s_%s"%(array[0],array[1],array[3],array[4])]+=1
            infile.close()
###############################
root_dir="/data/Project/liaorui/panel_599/"
for (root,dirs,files) in os.walk(root_dir):
    for file in files:
        tmp=os.path.join(root,file)

        if tmp.endswith("_N.Germline.PASS.Annot.xls") and re.search(r'ana_19',tmp):
            infile=open(tmp,"r")
            for line in infile:
                line = line.strip()
                array = line.split("\t")
                pos=array[0]+"_"+array[1]
                if pos in final_site:
                    if not "%s_%s_%s_%s" % (array[0], array[1], array[3], array[4]) in site_counts:
                        site_counts["%s_%s_%s_%s" % (array[0], array[1], array[3], array[4])]=1
                    else:
                        site_counts["%s_%s_%s_%s"%(array[0],array[1],array[3],array[4])]+=1
            infile.close()
for key in site_counts:
    print(key,"\t",site_counts[key])
"""