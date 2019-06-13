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
        array=line.split()
        dict[array[0]]=1
    infile.close()
infile=open(vcf,"r")
outfile=open("cosmic.site.classify.tsv","a")
for line in infile:
    line=line.strip()
    array=line.split()
    if array[2] in dict:
        continue
    else:
        url = 'https://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s' %(array[2])
        res=requests.get(url)
        ret=res.text
        soup=BeautifulSoup(ret,'html.parser')
        dt=soup.find_all('dt')
        dd=soup.find_all('dd')
        dbsnp = soup.find(text=re.compile(r'has been flagged as a SNP'))
        if not dbsnp:
            for i in range(len(dt)):
                if dt[i].string=="Ever confirmed somatic?":
                    print (dt[i].string,"\t",dd[i].string)
        else:
            print(array[2],"\t","SNP")
        time.sleep(2)
infile.close()
outfile.close()