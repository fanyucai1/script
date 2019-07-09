#Email:fanyucai1@126.com
#2019.1.14

import os
import subprocess
import argparse

GATK4="export PATH=/software/java/jdk1.8.0_202/bin/:$PATH && /software/gatk/gatk-4.1.2.0/gatk"
ref="/data/Database/hg19/ucsc.hg19.fasta"
ad="/software/docker_tumor_base/Resource/GATK/af-only-gnomad.raw.sites.hg19.vcf.gz"
"""
###############CreateSomaticPanelOfNormals
https://software.broadinstitute.org/gatk/documentation/tooldocs/4.0.0.0/org_broadinstitute_hellbender_tools_walkers_mutect_CreateSomaticPanelOfNormals.php
###############(How to) Call somatic mutations using GATK4 Mutect2
https://gatkforums.broadinstitute.org/gatk/discussion/11136/how-to-call-somatic-mutations-using-gatk4-mutect2#1.2
###############germline resource
ftp://ftp.broadinstitute.org/bundle/Mutect2/
################--contamination-fraction-to-filter 0.02
https://docs.gdc.cancer.gov/Data/PDF/Data_UG.pdf
"""

parser=argparse.ArgumentParser("This script will call SNV using Mutect2.")
parser.add_argument("-n","--normal",help="normal bam file",type=str,required=True)
parser.add_argument("-t","--tumor",help="tumor bam files",type=str,required=True)
parser.add_argument("-o","--outdir",help="output directory",type=str,default=os.getcwd())
parser.add_argument("-pn","--pnormal",help="name of normal",type=str,required=True)
parser.add_argument("-pt","--ptumor",help="name of tumor",type=str,required=True)
parser.add_argument("-r","--region",help="target egion bed file",type=str)
parser.add_argument("-p","--pon",help="",type=str)
result=parser.parse_args()
if not os.path.exists(result.outdir):
    os.mkdir(result.outdir)
result.tumor=os.path.abspath(result.tumor)
par=" --contamination-fraction-to-filter 0.02 --disable-read-filter MateOnSameContigOrNoMappedMateReadFilter "
if result.region:
    par+=" -L %s --germline-resource %s --af-of-alleles-not-in-resource 0.0000025 " %(result.region,ad)
else:
    par+=" --germline-resource %s  --af-of-alleles-not-in-resource 0.0000025 " %(ad)
if result.pon:
    result.pon=os.path.abspath(result.pon)
    par+="-pon %s " %(result.pon)
#Call somatic short variants and generate a bamout with Mutect2
subprocess.check_call("%s --java-options \"-Xmx40g\" Mutect2 -R %s -I %s -I %s -tumor %s -normal %s -O %s/%s.vcf %s"
                      %(GATK4,ref,result.tumor,result.normal,result.ptumor,result.pnormal,result.outdir,
                        result.ptumor,par),shell=True)
