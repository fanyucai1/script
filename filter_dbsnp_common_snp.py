#Email:fanyucai1@126.com

import argparse
import subprocess
import os

SnpSift="/data02/software/snpEff/snpEff/SnpSift.jar"
java="/data02/software/java/jdk1.8.0_191/bin/java"
gatk4="/data02/software/GATK/gatk-4.0.11.0/gatk"
tabix="/data02/software/samtools/samtools-1.9/htslib-1.9/tabix"
bgzip="/data02/software/samtools/samtools-1.9/htslib-1.9/bgzip"
"""
dbSNP Columns
##INFO=<ID=COMMON,Number=1,Type=Integer,Description="RS is a common SNP.  
A common SNP is one that has at least one 1000Genomes population with a minor allele of frequency >= 1% and for which 2 or more founders contribute to that minor allele frequency.
dbsnp_hg19 download from:ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/
deadline is 2018.4.23,there contains 37,906,831 entries only from common snp in dbsnp.

Chalmers Z R, Connelly C F, Fabrizio D, et al. Analysis of 100,000 human cancer genomes reveals the landscape of tumor mutational burden[J]. Genome medicine, 2017, 9(1): 34
"""
parser=argparse.ArgumentParser("This script will filter known common alterations in dbSNP")
parser.add_argument("-d","--dbsnp",type=str,required=True,help="dbsnp vcf file(.gz)")
parser.add_argument("-v","--vcf",type=str,help="your vcf file",required=True)
parser.add_argument("-o","--outdir",type=str,help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",type=str,default="filter.dbsnp.common.vcf",help="default:filter.dbsnp.common.vcf")

result=parser.parse_args()
result.dbsnp=os.path.abspath(result.dbsnp)
result.vcf=os.path.abspath(result.vcf)
if(result.outdir):
    result.outdir=os.path.abspath(result.outdir)
    subprocess.check_call('mkdir -p %s' %(result.outdir),shell=True)
os.chdir(result.outdir)
#######first get the common subvcf from dbsnp#######################
if result.dbsnp.endswith("gz"):
    subprocess.check_call("zcat %s|head -1000|grep \"#\" >%s/dbsnp.common.vcf" %(result.dbsnp,result.outdir),shell=True)
    subprocess.check_call("zcat %s |grep \"COMMON=1\" >>%s/dbsnp.common.vcf" %(result.dbsnp,result.outdir),shell=True)
if result.dbsnp.endswith("vcf"):
    subprocess.check_call("head -1000 %s |grep \"#\" >%s/dbsnp.common.vcf" %(result.dbsnp,result.outdir),shell=True)
    subprocess.check_call("grep \"COMMON=1\" %s >>%s/dbsnp.common.vcf" % (result.dbsnp,result.outdir), shell=True)
######################index vcf#################################################
if not os.path.exists(("%s.idx") %(result.vcf)):
    subprocess.check_call("export PATH=%s\$PATH && %s IndexFeatureFile %s" %(java,gatk4,result.vcf),shell=True)
subprocess.check_call("%s < %s/dbsnp.common.vcf >%s/dbsnp.common.vcf.gz" %(bgzip,result.outdir,result.outdir),shell=True)
subprocess.check_call("%s -p vcf %s/dbsnp.common.vcf.gz" %(tabix,result.outdir),shell=True)
######first anno vcf use snpeff##################################################
subprocess.check_call("%s -Xmx50G -jar %s Annotate %s/dbsnp.common.vcf.gz %s >%s/tmp.vcf" %(java,SnpSift,result.outdir,result.vcf,result.outdir),shell=True)
##################################################################################
infile=open("%s/tmp.vcf" %(result.outdir),"r")
outfile=open("%s/%s" %(result.outdir,result.prefix),"w")
for line in infile:
    line=line.strip()
    if line.startswith("#"):
        outfile.write("%s\n" %(line))
    else:
        array=line.split("\t")
        if not array[2].startswith("rs") and array[6] =="PASS":
            outfile.write("%s\n" %(line))
infile.close()
outfile.close()
subprocess.check_call("rm -rf %s/tmp.vcf" %(result.outdir),shell=True)