#Email:fanyucai1@126.com
#2019.1.16
import os
import argparse
import subprocess
java="export PATH=/data02/software/java/jdk1.8.0_191/bin/:\$PATH && "
GATK4="/data02/software/GATK/gatk-4.0.11.0/gatk"
ref="/data02/database/hg19/ucsc.hg19.fasta"
ad="/data02/software/GATK/af-only-gnomad.raw.sites.hg19.vcf.gz"
"""
A small PON is better than no PON,in practice we recommend aiming for a minimum of 40.
https://software.broadinstitute.org/gatk/documentation/article?id=11053
"""
parser=argparse.ArgumentParser("Create a panel of normals (PoN)")
parser.add_argument("-b","--bam",help="normal bam files",nargs="+",required=True)
parser.add_argument("-o","--outdir",help="output dircetory",default=os.getcwd())
parser.add_argument("-pn","--pnormal",help="normal name",nargs="+",required=True)
parser.add_argument("-r","--region",help="target region bed file",type=str)

result=parser.parse_args()
par=""
list=""
if result.region:
    result.region=os.path.abspath(result.region)
    par+=" -L %s --germline-resource %s " %(result.region,ad)

for i in range(len(result.bam)):
    subprocess.check_call(
         "cd %s && %s && %s --java-options \"-Xmx40g\" Mutect2 -R %s -I %s -tumor %s %s --disable-read-filter MateOnSameContigOrNoMappedMateReadFilter -O %s.pon.vcf.gz"
        % (result.outdir, java, GATK4, ref, result.bam[i], result.pnormal[i], par,result.pnormal[i]), shell=True)
    list+=" -vcfs %s/%s.pon.vcf.gz " %(result.outdir,result.pnormal[i])

subprocess.check_call("cd %s && %s && %s --java-options \"-Xmx40g\" CreateSomaticPanelOfNormals %s -O pon.vcf.gz"
                      %(result.outdir,java,GATK4,list),shell=True)