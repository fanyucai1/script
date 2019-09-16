import os
import argparse
import sys
import re
sub=os.path.abspath(__file__)
dir_name=os.path.dirname(sub)
sys.path.append(dir_name)
import subprocess
###################################################run annovar
annovar="/software/docker_tumor_base/Resource/Annovar/"
def run_annovar(vcf,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out = outdir + "/" + prefix
    par = " -protocol refGene,cytoBand,snp138,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118"
    par += " -operation g,r,f,f,f,f,f,f,f,f,f,f,f "
    par += " -nastring . -polish "
    subprocess.check_call("perl %s/table_annovar.pl %s %s/humandb -buildver hg19 -out %s -remove %s -vcfinput " % (annovar, vcf, annovar, out, par), shell=True)
###################################################parse clinvar
clinvar_vcf="/data/Database/clinvar/variant_summary.txt"
clinvar_anno="/data/Database/clinvar/2019.7.20/clinvar.vcf"
def parse_clinvar():
    AlleleID, dict = {}, {}
    infile = open(clinvar_anno, "r")
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        if not line.startswith("#"):
            AlleleID[array[0]] = array[2]
    infile.close()
    infile = open(clinvar_vcf, "r")
    for line in infile:
        if not line.startswith("#"):
            p = re.compile(r'ALLELEID=(\d+);')
            line = line.strip()
            array = line.split("\t")
            tmp = array[0] + "\t" + array[1] + "\t" + array[3] + "\t" + array[4]
            a = p.findall(line)
            dict[tmp] = AlleleID[a[0]]
    infile.close()
    return dict
########################################Canonical transcript info
Canonical_transcript_file="/data/Database/knownCanonical/clinvar_canonical_trans.txt"
def Canonical():
    transcript={}
    infile=open(Canonical_transcript_file,"r")
    for line in infile:
        line=line.strip()
        array=line.split("\t")
        transcript[array[0]]=[]
        for i in range(1,len(array)):
            tmp=array[i].split(".")
            transcript[array[0]].append(tmp[0])
