import requests
from bs4 import BeautifulSoup
import re
id=input("please input COSMIC ID(e.g:COSM3677745):")
pattern=re.compile(r'\d+')
num=pattern.findall(id)
url="https://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s" %(num[0])
res=requests.get(url,proxies={"https":"https://182.34.17.32:9999"})
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

"""
        tmp=soup.find_all('abbr')#Inheritance Phenotype  mapping key
        str=""
        for i in tmp:
            str+=","
            str+=i.string
        array=re.split(r'(\d+)',str)
        for i in array:
            p1=re.compile(r'[A-Za-z]')
            p2=re.compile(r'(\d+)')
            a=p1.findall(i.strip())
            b=p2.findall(i.strip())
            if i.strip(",")!="":
                if a!=[]:
                    key.append(i.strip(","))
                if b != []:
                    Inheritance.append(i.strip(","))
        outfile = open("omim.tsv", "a+")
        for i in range(len(key)):
            outfile.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(id,Location,Phenotype[i],Phenotype_MIM_number[i],Inheritance[i],key[i]))
        outfile.close()
    except:
        pass
"""

