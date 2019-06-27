import requests
from bs4 import BeautifulSoup
import re
id=input("please input COSMIC ID(e.g:COSM3677745):")
pattern=re.compile(r'\d+')
num=pattern.findall(id)
url="https://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s" %(num[0])
res=requests.get(url,proxies={"https":"https://14.29.232.142:8082"})
ret = res.text
soup=BeautifulSoup(ret,'html.parser')
dbsnp=soup.find_all(text=re.compile("has been flagged as a SNP."))
dt = soup.find_all('dt')
dd = soup.find_all('dd')
for i in range(len(dt)):
    if dt[i].string == "Ever confirmed somatic?":
        print("%s\t%s" % (id, dd[i].string))
if dbsnp!=[]:
    print("%s\tSNP" % (id))



