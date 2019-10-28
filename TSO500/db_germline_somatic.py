#Email:fanyucai1@126.com
#2019.5.24

import os
import argparse
import re

parser=argparse.ArgumentParser()
parser.add_argument("-d","--dir",help="diretory TSO500 default:/data/TSO500/",default="/data/TSO500")
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
parser.add_argument("-s","--samplelist",help="sample list",required=True)
args=parser.parse_args()
###############################################
infile=open(args.samplelist,"r")
sample,fail=[],0
for line in infile:
    line=line.strip()
    array = re.split('[,\t]', line)
    if line.startswith("Sample_ID"):
        for i in range(len(array)):
            if array[i]=="Failed":
                fail=i
    else:
        if array[fail]!="yes":
            sample.append(array[0])
infile.close()
###############################################
outfile=open("%s/TSO_somatic2germline.tsv"%(args.outdir),"w")
outfile.write("Chr\tPosition\tRef\tAlt\tSomatic-Score\tGermline-Score\tTotal_counts\n")
dict_s,dict_g,dict={},{},{}
for(root,dirs,files) in os.walk(args.dir):
    for file in files:
        tmbfile = os.path.join(root,file)
        if tmbfile.endswith("tmb.tsv") and tmbfile.split("/")[-3]=="Tmb" and tmbfile.split("/")[-2] in sample:
                num,name=0,[]
                infile=open(tmbfile,"r")
                for line in infile:
                    line=line.strip()
                    array=re.split('[,\t]',line)
                    num+=1
                    if num==1:
                        for i in range(len(array)):
                            name.append(array[i])
                    else:
                        tmp=""
                        for i in range(len(array)):
                            if name[i]=="Chromosome":
                                tmp=array[i]
                            if name[i]=="Position" or name[i]=="RefCall" or name[i]=="AltCall":
                                tmp+="_"
                                tmp+=array[i]
                            if name[i]=="SomaticStatus":
                                if array[i]=="Somatic":
                                    dict_s[tmp] =dict_s[tmp]+ 1 if tmp in dict_s else 1
                                else:
                                    dict_g[tmp] = dict_g[tmp]+1 if tmp in dict_g else 1
                        dict[tmp]=1
                infile.close()
for key in dict:
    array=key.split("_")
    for j in range(len(array)):
        if j==0:
            outfile.write(array[j])
        else:
            outfile.write("\t%s"%(array[j]))
    if key in dict_s:
        outfile.write("\t%s" % (dict_s[key]))
    else:
        outfile.write("\t0")
    if key in dict_g:
        outfile.write("\t%s\n" % (dict_g[key]))
    else:
        outfile.write("\t0\n")
outfile.close()