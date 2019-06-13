import requests
from bs4 import BeautifulSoup
import re
vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.hg19.vcf"
infile=open(vcf,"r")
for line in infile:
    line=line.strip()
    if not line.startswith("#"):
        array=line.split("\t")
        pattern=re.compile(r'(\d+)')
        id=pattern.findall(array[2])
        url = 'https://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s' %(id[0])
        print("#%s"%(url))
        res=requests.get(url,timeout=0.01)
        if res.status_code==200:
            ret=res.text
            soup=BeautifulSoup(ret,'html.parser')
            dt=soup.find_all('dt')
            dd=soup.find_all('dd')
            dbsnp = soup.find(text=re.compile(r'has been flagged as a SNP'))
            if not dbsnp:
                for i in range(len(dt)):
                    if dt[i].string=="Ever confirmed somatic?":
                        print("%s\t%s"%(array[2],dd[i].string))
            else:
                print("%s\tSNP" % (array[2]))
infile.close()