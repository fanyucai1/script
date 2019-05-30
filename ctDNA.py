#Email:fanyucai1@126.com
#2019.5.14

import os
import argparse
import re
import subprocess

annovar="/software/docker_tumor_base/Resource/Annovar"
parser=argparse.ArgumentParser("Delete vcf2 site in vcf1")
parser.add_argument("-v1","--vcf1",help="vcf file",required=True)
parser.add_argument("-v2","--vcf2",help="vcf file",required=True)
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
args=parser.parse_args()
out=args.outdir+"/"+args.prefix
###############################################
dict={}
infile1=open("%s"%(args.vcf1),"r")
infile2=open("%s"%(args.vcf2),"r")
outfile1=open("%s.filter"%(out),"w")
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
    if not line.startswith("#"):
        array = line.split()
        end = int(array[1]) + len(array[3]) - 1
        tmp = array[0] + "_" + array[1] + "_" + array[3] + "_" + array[4]  # chr+pos+ref+alt
        p=re.compile(r'VMF=(\S+)')
        c=p.findall(line)
        if tmp in dict:
            continue
        else:
            d = array[4].split(",")
            MAF=c[0].split(",")
            if d==[]:
                pstr = array[0] + "\t" + array[1] + "\t" + str(end) + "\t" + array[3] + "\t" + array[4] + "\t" + c[0]
                outfile1.write("%s\n" % (pstr))
            else:
                for i in range(len(d)):
                    tmp = array[0] + "_" + array[1] + "_" + array[3] + "_" + d[i]  # chr+pos+ref+alt
                    if not tmp in dict:
                        pstr=array[0]+"\t"+ array[1]+"\t"+str(end)+"\t"+array[3]+"\t"+d[i]+"\t"+MAF[i]
                        outfile1.write("%s\n" % (pstr))
outfile1.close()
infile1.close()
#######################################################
par=" -protocol refGene,cytoBand,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,1000g2015aug_eas,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118 "
par+=" -operation g,r,f,f,f,f,f,f,f,f,f,f,f "
par+=" -nastring . -polish "
subprocess.check_call("cd %s && perl %s/table_annovar.pl %s.filter %s/humandb -buildver hg19 -out %s -remove %s " %(args.outdir,annovar,out,annovar,args.prefix,par),shell=True)
#######################################################
infile1=open("%s.hg19_multianno.txt"%(out),"r")
outfile1=open("%s.final.txt"%(out),"w")
for line in infile1:
    line=line.strip()
    array=line.split("\t")
    if array[5]=="intronic":
        continue
    elif array[5].startswith("UTR"):
        continue
    elif array[8] == "synonymous SNV":
        continue
    else:
        outfile1.write("%s\n"%(line))
infile1.close()
outfile1.close()
#######################################################