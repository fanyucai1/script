#Email:fanyucai1@126.com
#2019.5.14

import os
import argparse
import re
import subprocess
annovar="/software/docker_tumor_base/Resource/Annovar"
parser=argparse.ArgumentParser("Analysis panel275 CNV.")
parser.add_argument("-v","--vcf",help="copy number vcf from qiaseq",required=True)
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
parser.add_argument("-g","--genelist",help="gene list",required=True)
parser.add_argument("-o","--outdir",help="output directory",required=True)
args=parser.parse_args()

out=args.outdir+args.prefix
vcf_in=open(args.vcf,"r")
vcf_out=open("%s.cnv.vcf"%(out),"w")
pattern=re.compile(r'PVAL\s+([0-9.]+)\:')
end=re.compile(r'END=(\d+)\;')
CNV={}
CNV_type={}
for line in vcf_in:
    line=line.strip()
    if not line.startswith("#"):
        array=line.split("\t")
        if array[4]!=".":
            a=pattern.findall(line)
            b=end.findall(line)
            CNV[array[0]]=a[0]
            CNV_type[array[0]]=array[4]
            vcf_out.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (array[0],array[1],b[0],"0","0",a[0]))
vcf_in.close()
vcf_out.close()
################################################annotate cnv vcf
cmd="cd %s && perl %s/table_annovar.pl %s.cnv.vcf %s/humandb/ -out %s.cnv" \
    " -remove -protocol refGene -operation g --nastring . -buildver hg19" %(args.outdir,annovar,out,annovar,args.prefix)
subprocess.check_call(cmd,shell=True)
################################################read gene list
dict={}
infile = open(args.genelist, "r")
for line in infile:
    line = line.strip()
    dict[line] = 1
infile.close()
############################################parse cnv file
vcf_in=open("%s.cnv.hg19_multianno.txt" %(out),"r")
vcf_out=open("%s.cnv.final.txt" %(out),"w")
vcf_out.write("Chr\tStart\tEnd\tFunc.refGene\tGene.refGene\tCNV\tType\n")
num=0
for line in vcf_in:
    num+=1
    line=line.strip()
    array=line.split()
    if num !=1 and array[6] in dict:
        vcf_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %(array[0],array[1],array[2],array[5],array[6],CNV[array[0]],CNV_type[array[0]]))
vcf_out.close()
vcf_in.close()
#########################################
subprocess.check_call("rm -rf %s/cnv.hg19_multianno.txt %s/cnv.hg19_multianno.vcf" %(args.outdir,args.outdir),shell=True)
