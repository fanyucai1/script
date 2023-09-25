#Email:fanyucai1@126.com
#2019.1.15

import os
import subprocess
import argparse

annovar="/data02/software/ANNOVAR/annovar/"

parser=argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                               description="This script will annotate vcf and filter MAF<0.01 basing frequency of variants database.")
parser.add_argument("-v","--vcf",help="vcf file",type=str,required=True)
parser.add_argument("-m","--maf",type=int,help="minor allele frequency default:0.01",default=0.01)
parser.add_argument("-o","--outdir",help="output directoty",default=os.getcwd())
parser.add_argument("-c","--classify",type=str,help="which type annotate:exon(default) or genome",default="exon")
parser.add_argument("-p","--prefix",help="prefix of output",default="annovar")
result=parser.parse_args()

if not os.path.exists(result.outdir):
    os.mkdir(result.outdir)
result.outdir=os.path.abspath(result.outdir)
result.vcf=os.path.abspath(result.vcf)
os.chdir(result.outdir)
par=""
if result.classify == "exon":
    par=" -protocol refGene,cytoBand,exac03,avsnp150,dbnsfp35c,esp6500siv2_all,gnomad_exome,1000g2015aug_all,cosmic70,clinvar_20180603 "
else:
    par=" -protocol refGene,cytoBand,exac03,avsnp150,dbnsfp35c,esp6500siv2_all,gnomad_genome,1000g2015aug_all,cosmic70,clinvar_20180603 "
par+=" -operation gx,r,f,f,f,f,f,f,f,f "
par+=" -nastring . -polish -xreffile %s/example/gene_xref.txt " %(annovar)
subprocess.check_call("cd %s && perl %s/table_annovar.pl %s %s/humandb -buildver hg19 -out %s -remove %s -vcfinput "
                      %(result.outdir,annovar,result.vcf,annovar,result.prefix,par),shell=True)
infile=open("%s/%s.hg19_multianno.txt" %(result.outdir,result.prefix),"r")
num=0
dict={}
outfile=open("%s/%s.annovar.filter.txt" %(result.outdir,result.prefix),"w")
for line in infile:
    num+=1
    line=line.strip()
    array=line.split("\t")
    if num==1:
        for i in range(len(array)):
            if array[i]=="1000g2015aug_all":
                dict['1000g2015aug_all']=i
            if array[i]=="gnomAD_exome_ALL":
                dict['gnomAD_exome_ALL']=i
            if array[i] == "gnomAD_genome_ALL":
                dict['gnomAD_genome_ALL'] = i
            if array[i]=="ExAC_ALL":
                dict['ExAC_ALL']=i
            if array[i]=="esp6500siv2_all":
                dict['esp6500siv2_all']=i
    else:
        for key in dict:
            if array[dict[key]] ==".":
                pass
            elif float(array[dict[key]]) > result.maf:
                line=""
            else:
                pass
        if line!="":
            outfile.write("%s\n" % (line))
infile.close()
outfile.close()
