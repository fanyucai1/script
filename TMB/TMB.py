import os
import sys
import re
import subprocess
cosmic_vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.vcf"
annovar="/software/docker_tumor_base/Resource/Annovar/"
database = ['1000g2015aug_all', 'ExAC_ALL', 'esp6500siv2_all','genome_AF','exome_AF']

def run(vcf,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    ####hotspot(CNT>50)################
    hotspot={}
    infile=open(cosmic_vcf,"r")
    for line in infile:
        line=line.strip()
        array=line.split("\t")
        if not line.startswith("#"):
            p=re.compile(r'CNT=(\d+)')
            a=p.findall(array[-1])
            if a!=[] and float(a[0])>=50:
                tmp=array[0]+"_"+array[1]+"_"+array[3]+"_"+array[4]
                hotspot[tmp]=1
    infile.close()
    ####run annovar#########################
    par = " -protocol refGene,cytoBand,snp138,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118"
    par += " -operation g,r,f,f,f,f,f,f,f,f,f,f,f "
    par += " -nastring . -polish "
    subprocess.check_call("perl %s/table_annovar.pl %s %s/humandb -buildver hg19 -out %s -remove %s -vcfinput " % (annovar, vcf, annovar, out, par), shell=True)

if __name__=="__main__":
    if len(sys.argv)!=4:
        print("python3 %s vcf outdir prefix"%(sys.argv[0]))
        print("\nEmail:fanyucai1@126.com")
    else:
        vcf=sys.argv[1]
        outdir=sys.argv[2]
        prefix=sys.argv[3]
        run(vcf, outdir, prefix)