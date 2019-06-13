import requests
from bs4 import BeautifulSoup
import re
vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.hg19.vcf"
infile=open(vcf,"r")
outfile=open("cosmic.tsv","w")
outfile.write("#ID\tType\n")
dict={}
for line in infile:
    line=line.strip()
    if not line.startswith("#"):
        array=line.split("\t")
        pattern=re.compile(r'(\d+)')
        id=pattern.findall(array[2])
        url = 'https://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s' %(id[0])
        res=requests.get(url)
        ret = res.text
        soup=BeautifulSoup(ret,'html.parser')
        dt=soup.find_all('dt')
        dd=soup.find_all('dd')
        dbsnp = soup.find(text=re.compile(r'has been flagged as a SNP'))
        if dt!=[]:
            for i in range(len(dt)):
                if dt[i].string=="Ever confirmed somatic?":
                    dict[array[2]]=dd[i].string
                    print("%s\t%s"%(array[2],dd[i].string))
                    continue
        else:
            dict[array[2]] = "SNP"
            print("%s\tSNP" % (array[2]))
            continue
infile.close()

for key in dict:
    outfile.write("%s\t%s\n"%(key,dict[key]))
outfile.close()
print("#This pcocess done.")