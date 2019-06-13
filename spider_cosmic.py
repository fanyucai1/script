import requests
from bs4 import BeautifulSoup
import re
import time
import os

vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.hg19.vcf"
dict={}
if os.path.exists("cosmic.site.classify.tsv"):
    infile=open("cosmic.site.classify.tsv","r")
    for line in infile:
        line=line.strip()
        array=line.split("\t")
        dict[array[0]]=1
    infile.close()
infile=open(vcf,"r")
outfile=open("cosmic.site.classify.tsv","a")
for line in infile:
    line=line.strip()
    if not line.startswith("#"):
        array=line.split("\t")
        if array[2] in dict:
            continue
        else:
            pattern=re.compile(r'(\d+)')
            id=pattern.findall(array[2])
            url = 'https://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s' %(id)
            print (url)
            res=requests.get(url)
            ret=res.text
            soup=BeautifulSoup(ret,'html.parser')
            dt=soup.find_all('dt')
            dd=soup.find_all('dd')
            dbsnp = soup.find(text=re.compile(r'has been flagged as a SNP'))
            if not dbsnp:
                for i in range(len(dt)):
                    if dt[i].string=="Ever confirmed somatic?":
                        outfile.write("%s\t%s\n"%(array[2],dd[i].string))
            else:
                outfile.write("%s\tSNP\n" % (array[2]))
            time.sleep(2)
infile.close()
outfile.close()