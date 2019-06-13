import requests
from bs4 import BeautifulSoup
import re
import time
import os

vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.hg19.vcf"
infile=open(vcf,"r")
outfile=open("cosmic.site.classify.tsv","w")
for line in infile:
    line=line.strip()
    if not line.startswith("#"):
        array=line.split("\t")
        pattern=re.compile(r'(\d+)')
        id=pattern.findall(array[2])
        url = 'https://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s' %(id[0])
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
                    print("%s\t%s\n"%(array[2],dd[i].string))
                    outfile.write("%s\t%s\n"%(array[2],dd[i].string))
        else:
            print("%s\tSNP\n" % (array[2]))
            outfile.write("%s\tSNP\n" % (array[2]))
        time.sleep(2)
infile.close()
outfile.close()