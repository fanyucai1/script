#Email:fanyucai1@126.com

import argparse
import os
import subprocess

parser=argparse.ArgumentParser("This script will parse the vcf using ICGC database.")
parser.add_argument("-v","--vcf",type=str,help="input vcf file")
parser.add_argument("-t","--tab",type=str,help="tab file from ICGC")
parser.add_argument("-o","--outdir",type=str,help="output directory")

result=parser.parse_args()

if (result.vcf):
    result.vcf= os.path.abspath(result.vcf)
if (result.tab):
    result.tab=os.path.abspath(result.tab)
if not result.outdir:
    result.outdir=os.getcwd()
else:
    subprocess.check_all('mkdir -p %s' %(result.outdir),shell=True)

os.chdir(result.outdir)

file1=open('%s'%(result.tab),'r')
dict={}
for line in file1:
    if line.startswith("#"):
        continue
    else:
        line=line.strip()
        array=line.split("\t")
        #chr:pos:alt
        dict['chr%s.%s.%s' %(array[8],array[9],array[16])]=line

file2=open('%s' %(result.vcf),"r")
file3=open('%s/result.txt' %(result.outdir),"w")
for line in file2:
    line=line.strip()
    if line.startswith("#"):
        continue
    else:
        array=line.split("\t")
        str='%s.%s.%s' %(array[0],array[1],array[4])
        if str in dict:
            file3.write('%s\n' %(dict[str]))
        else:
            pass