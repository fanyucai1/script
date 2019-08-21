import os
import sys
import re
import subprocess
cosmic_vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.vcf"
annovar="/software/docker_tumor_base/Resource/Annovar/"
database = ['1000g2015aug_all', 'ExAC_ALL', 'esp6500siv2_all','genome_AF','exome_AF']

def run(panelsize,vcf,outdir,prefix):
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
    par = " -protocol refGene,cytoBand,exac03,esp6500siv2_all,1000g2015aug_all,gnomad211_exome,gnomad211_genome"
    par += " -operation g,r,f,f,f,f,f "
    par += " -nastring . -polish "
    subprocess.check_call("perl %s/table_annovar.pl %s %s/humandb -buildver hg19 -out %s -remove %s -vcfinput " % (annovar, vcf, annovar, out, par), shell=True)
    infile=open("%s.hg19_multianno.vcf"%(out),"r")
    counts=0
    AF_exac=re.compile(r'ExAC_ALL=(\d+.\d+)')
    AF_1000g2015aug_all=re.compile(r'1000g2015aug_all=(\d+.\d+)')
    AF_esp6500siv2_all=re.compile(r'esp6500siv2_all=(\d+.\d+)')
    AF_gnomad211_exome=re.compile(r'exome_AF=(\d+.\d+)')
    AF_gnomad211_genome=re.compile(r'genome_AF=(\d+.\d+)')
    for line in infile:
        result="T"
        line=line.strip()
        if not line.startswith("#"):
            array=line.split("\t")
            tmp=array[0]+"_"+array[1]+"_"+array[3]+"_"+array[4]
            if tmp in hotspot:
                continue
            if not re.search('Func.refGene=exonic',line):
                continue
            a=AF_exac.findall(line)
            b=AF_esp6500siv2_all.findall(line)
            c=AF_gnomad211_exome.findall(line)
            d=AF_gnomad211_genome.findall(line)
            e=AF_1000g2015aug_all.findall(line)
            if a!=[] and float(a[0])>=0.01:
                continue
            if b != [] and float(b[0]) >= 0.01:
                continue
            if c != [] and float(c[0]) >= 0.01:
                continue
            if d != [] and float(d[0]) >= 0.01:
                continue
            if e != [] and float(e[0]) >= 0.01:
                continue
            if result=="T":
                counts+=1
    TMB=counts/panelsize
    print ("Total site is %s"%(counts))
    print("TMB is %s"%(TMB))

if __name__=="__main__":
    if len(sys.argv)!=5:
        print("python3 %s panelsize vcf outdir prefix"%(sys.argv[0]))
        print("\nEmail:fanyucai1@126.com")
    else:
        panelsize=sys.argv[1]
        vcf=sys.argv[2]
        outdir=sys.argv[3]
        prefix=sys.argv[4]
        run(panelsize,vcf, outdir, prefix)