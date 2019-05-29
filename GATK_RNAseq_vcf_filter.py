# Email:fanyucai1@126.com
# 2019.1.7

import os
import subprocess
import argparse

GATK4 = "/data02/software/GATK/gatk-4.0.11.0/gatk"
java = "/data02/software/java/jdk1.8.0_191/bin/"

parser = argparse.ArgumentParser("This script will filter vcf.")
parser.add_argument("-v", "--vcf", help="your vcf", type=str, required=True)
parser.add_argument("-r", "--ref", help="reference fasta", type=str, required=True)
parser.add_argument("-o", "--outdir", help="output directory", type=str, default=os.getcwd())
parser.add_argument("-p", "--prefix", help="prefix of output,default:out", type=str, default="out")

result = parser.parse_args()
result.vcf=os.path.abspath(result.vcf)
result.ref=os.path.abspath(result.ref)

if result.outdir:
    result.outdir=os.path.abspath(result.outdir)
    subprocess.check_call("mkdir -p %s" %(result.outdir),shell=True)
os.chdir(result.outdir)

##############################################https://github.com/gatk-workflows/gatk3-4-rnaseq-germline-snps-indels/blob/master/rna-germline-variant-calling.wdl
if result.type == "RNAseq":
    subprocess.check_call(
        "export PATH=%s\$PATH && %s --java-options -Xmx10G VariantFiltration -R %s -V %s -cluster 3 -window 35 -filter-name \"FS\" -filter \"FS > 30.0\" -filter-name \"QD\" -filter \"QD < 2.0\" -O %s/%s.vcf" %(java,GATK4,result.ref,result.vcf,result.out,result.prefix),shell=True)