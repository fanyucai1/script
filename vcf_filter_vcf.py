#Email:fanyucai1@126.com
#2019.5.14

import os
import argparse

parser=argparse.ArgumentParser("Delete vcf2 site in vcf1")
parser.add_argument("-v1","--vcf1",help="vcf file",required=True)
parser.add_argument("-v2","--vcf2",help="vcf file",required=True)
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
args=parser.parse_args()

dict={}
infile1=open("%s"%(args.vcf1),"r")
infile2=open("%s"%(args.vcf2),"r")
outfile=open("%s.filter.vcf"%(args.prefix),"w")
for line in infile2:
    if not line.startswith("#"):
        line=line.strip()
        array=line.split()
        a=array[4].split(",")
        for i in a:
            tmp=array[0]+"_"+array[1]+"_"+array[3]+"_"+i#chr+pos+ref+alt
            dict[tmp]=1
infile2.close()
for line in infile1:
    line = line.strip()
    if line.startswith("#"):
        outfile.write("%s\n"%(line))
    else:
        array = line.split()
        a = array[4].split(",")
        for i in a:
            tmp = array[0] + "_" + array[1] + "_" + array[3] + "_" + i  # chr+pos+ref+alt
        if not tmp in dict:
            outfile.write("%s\n" % (line))