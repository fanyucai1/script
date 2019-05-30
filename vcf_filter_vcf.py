#Email:fanyucai1@126.com
#2019.5.14

import os
import argparse
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn2_circles
from matplotlib_venn import venn3, venn3_circles
import seaborn as sns
sns.set(style="ticks")
parser=argparse.ArgumentParser("Compare between two vcf files")
parser.add_argument("-v1","--vcf1",help="vcf file",required=True)
parser.add_argument("-v2","--vcf2",help="vcf file",required=True)
args=parser.parse_args()

dict1,dict2={},{}
infile1=open("%s"%(args.vcf1),"r")
for line in infile1:
    if not line.startswith("#"):
        line=line.strip()
        array=line.split()
        a=array[4].split(",")
        end=str(int(array[1])+len(array[3])-1)
        if a!=[]:
            for i in a:
                tmp=array[0]+"_"+array[1]+"_"+end+"_"+array[3]+"_"+i#chr+pos+ref+alt
                dict1[tmp]=1
        else:
            tmp = array[0] + "_" + array[1] + "_"+end+"_" + array[3] + "_" + array[4]
            dict1[tmp] = 1
infile1.close()
infile2=open("%s"%(args.vcf2),"r")
for line in infile2:
    if not line.startswith("#"):
        line=line.strip()
        array=line.split()
        a=array[4].split(",")
        end = str(int(array[1]) + len(array[3]) - 1)
        if a != []:
            for i in a:
                tmp = array[0] + "_" + array[1] + "_" + end + "_" + array[3] + "_" + i  # chr+pos+ref+alt
                dict2[tmp] = 1
        else:
            tmp = array[0] + "_" + array[1] + "_" + end + "_" + array[3] + "_" + array[4]
            dict2[tmp] = 1
infile2.close()
unique1,unique2,common=0,0,0
outfile1=open("%s.common.%s.vcf"%(args.vcf1,args.vcf2),"w")
outfile2=open("%s.unique.vcf"%(args.vcf1),"w")
outfile3=open("%s.unique.vcf"%(args.vcf2),"w")
for i in dict2:
    if i in dict1:
        common+=1
        array=i.split("_")
        l=0
        for j in range(len(array)):
            l+=1
            if l==1:
                outfile1.write("%s"%(array[j]))
            else:
                outfile1.write("\t%s"%(array[j]))
        outfile1.write("\n")
    else:
        unique2+=1
        array = i.split("_")
        l = 0
        for j in range(len(array)):
            l += 1
            if l == 1:
                outfile3.write("%s" % (array[j]))
            else:
                outfile3.write("\t%s" % (array[j]))
        outfile3.write("\n")
outfile1.close()
outfile3.close()
for i in dict1:
    if i in dict2:
        pass
    else:
        unique1+=1
        array = i.split("_")
        l = 0
        for j in range(len(array)):
            l += 1
            if l == 1:
                outfile2.write("%s" % (array[j]))
            else:
                outfile2.write("\t%s" % (array[j]))
        outfile2.write("\n")
outfile2.close()
##########################################