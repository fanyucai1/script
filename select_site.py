import os
import sys
import re
gene_list="/data/chosenmed_wiki/rst/gene_list/panel_27_gene.list"
bed_file="/data/chosenmed_wiki/rst/bed/panel_27.bed"
cosmic_anno="/data/Database/COSMIC/release_v88/CosmicMutantExport.tsv"
cosmic_vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.vcf"

#############################step1:获得基因list
infile=open(gene_list,"r")
gene={}
for line in infile:
    line=line.strip()
    gene[line]=1
infile.close()
############################step2:获得基因对应的热点cosmicID
infile=open(cosmic_anno,"r")
cosmic,num,name,status={},0,0,0
for line in infile:
    line=line.strip()
    array=re.split(r'[,\t]',line)
    num+=1
    if num==1:
        for i in range(len(array)):
            if array[i]=="Mutation ID":
                name=i
            if array[i]=="Mutation somatic status":
                status=i
    else:
        if array[0] in gene and array[status]=="Confirmed somatic variant":
            cosmic[array[name]]=1
infile.close()
############################step3:获得热点对应的位置
infile=open(cosmic_vcf,"r")
pos={}
for line in infile:
    line = line.strip()
    if not line.startswith("#"):
        array=line.split("\t")
        pattern=re.compile(r'CNT=(\d+)')
        a=pattern.findall(line)
        if array[2] in cosmic and int(a[0])>50:
            print(line)
infile.close()