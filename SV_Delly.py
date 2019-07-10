#Email:fanyucai1@126.com
#2019.1.10

import os
import argparse
import subprocess

delly="/software/Delly/delly_v0.8.1_linux_x86_64bit"
bcftools="/software/Bcftools/bcftools-1.4/"
hg19_exclude="/software/Delly/delly-master/excludeTemplates/human.hg19.excl.tsv"
hg38_exclude="/software/Delly/delly-master/excludeTemplates/human.hg38.excl.tsv"
samtools="/software/samtools/samtools-1.9/bin/samtools"

parser=argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                               description="This script will use Delly to find SV."
                                           "\npython3 -b sample1.bam sample2.bam -l sample.list -r hg19.fa -t somatic"
                                           "\npython3 -b germline.bam -l sample.list -r hg19.fa -t germline")
parser.add_argument('-b',"--bam",type=str,nargs="+",help="bam file(s)",required=True)
parser.add_argument("-r","--ref",help="reference fasta",type=str,required=True)
parser.add_argument("-o","--outdir",help="output directory",type=str,default=os.getcwd())
parser.add_argument("-p","--prefix",help="prefix of output",type=str,default="out")
parser.add_argument("-l","--list",help="tab-delimited sample description file:"
                                       "\nsample1   tumor"
                                       "\nsample2   control",type=str)
parser.add_argument("-t","--type",type=str,help="which type you run",choices=["somatic","germline"],required=True)
parser.add_argument("-e","--ex",type=str,help="bed region(file) your want to exclude, or simply choose hg19\hg38")
result=parser.parse_args()

if result.outdir:
    result.outdir=os.path.abspath(result.outdir)
    subprocess.check_call("mkdir -p %s" %(result.outdir),shell=True)
result.ref=os.path.abspath(result.ref)

exclude=""
if result.ex=="hg19":
    exclude=hg19_exclude
elif result.ex=="hg38":
    exclude=hg38_exclude
else:
    exclude=result.ex
string=""
for key in result.bam:
    if not '%s.bai' %(key):
        subprocess.check_call('%s index %s' %(samtools,key),shell=True)
    string+=" %s " %(key)
if result.type=="somatic" and result.list:
    result.list = os.path.abspath(result.list)
    subprocess.check_call("%s call -x %s -o %s/%s.bcf -g %s %s" %(delly,exclude,result.outdir,result.prefix,result.ref,string),shell=True)
    subprocess.check_call("%s filter -f somatic -o %s/%s.filter.bcf -s %s %s/%s.bcf" %(delly,result.outdir,result.prefix,result.list,result.outdir,result.prefix),shell=True)
    subprocess.check_call("%s/bcftools view %s/%s.filter.bcf > %s/%s.vcf" %(bcftools,result.outdir,result.prefix,result.outdir,result.prefix),shell=True)
else:
    subprocess.check_call("%s call -x %s -o %s/%s.bcf -g %s %s" % (delly, exclude, result.outdir, result.prefix, result.ref, string), shell=True)
    subprocess.check_call("%s/bcftools view %s/%s.bcf > %s/%s.vcf" % (bcftools, result.outdir, result.prefix, result.outdir, result.prefix),shell=True)