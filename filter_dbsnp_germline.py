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
SAO Variant Allele Origin: 0 - unspecified, 1 - Germline, 2 - Somatic, 3 - Both
dbsnp_hg19 download from:ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/
deadline is 2018.4.23,there contains 97747 entries only from somatic in dbsnp.
"""
parser=argparse.ArgumentParser("This script will filter known germline alterations in dbSNP")
parser.add_argument("-d","--dbsnp",type=str,required=True,help="dbsnp vcf file(.gz)")
parser.add_argument("-v","--vcf",type=str,help="your vcf file",required=True)
parser.add_argument("-o","--outdir",type=str,help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",type=str,default="somatic.vcf",help="default:somatic.vcf")

result=parser.parse_args()
result.dbsnp=os.path.abspath(result.dbsnp)
result.vcf=os.path.abspath(result.vcf)
if(result.outdir):
    result.outdir=os.path.abspath(result.outdir)
    subprocess.check_call('mkdir -p %s' %(result.outdir),shell=True)
os.chdir(result.outdir)
#######first get the germline subvcf from dbsnp#######################
if result.dbsnp.endswith("gz"):
    subprocess.check_call("zcat %s|head -1000|grep \"#\" >%s/dbsnp.germline.vcf" %(result.dbsnp,result.outdir),shell=True)
    subprocess.check_call("zcat %s |grep \"SAO=1\" >>%s/dbsnp.germline.vcf" %(result.dbsnp,result.outdir),shell=True)
if result.dbsnp.endswith("vcf"):
    subprocess.check_call("head -1000 %s |grep \"#\" >%s/dbsnp.germline.vcf" %(result.dbsnp,result.outdir),shell=True)
    subprocess.check_call("grep \"SAO=1\" %s >>%s/dbsnp.germline.vcf" % (result.dbsnp,result.outdir), shell=True)
######################index vcf#################################################
if not os.path.exists(("%s.idx") %(result.vcf)):
    subprocess.check_call("export PATH=%s\$PATH && %s IndexFeatureFile %s" %(java,gatk4,result.vcf),shell=True)
subprocess.check_call("%s < %s/dbsnp.germline.vcf >%s/dbsnp.germline.vcf.gz" %(bgzip,result.outdir,result.outdir),shell=True)
subprocess.check_call("%s -p vcf %s/dbsnp.germline.vcf.gz" %(tabix,result.outdir),shell=True)
######first anno vcf use snpeff##################################################
subprocess.check_call("%s -Xmx50G -jar %s Annotate %s/dbsnp.germline.vcf.gz %s >%s/tmp.vcf" %(java,SnpSift,result.outdir,result.vcf,result.outdir),shell=True)
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