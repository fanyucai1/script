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
        print(url)
        ret = res.text
        soup=BeautifulSoup(ret,'html.parser')
        dt=soup.find_all('dt')
        dd=soup.find_all('dd')
        dbsnp = soup.find(text='The mutation %s has been flagged as a SNP'%(array[2]))
        print (dbsnp)
        if dbsnp =="%s has been flagged as a SNP" %(array[2]):
            dict[array[2]] = "SNP"
            print("%s\tSNP" % (array[2]))
        else:
            for i in range(len(dt)):
                if dt[i].string=="Ever confirmed somatic?":
                    print("%s\t%s" % (array[2], dd[i].string))
                    dict[array[2]]=dd[i].string
infile.close()
for key in dict:
    outfile.write("%s\t%s\n" % (key, dict[key]))
outfile.close()
print("#This pcocess done.")