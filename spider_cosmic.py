import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.adapters.DEFAULT_RETRIES =10#增加重连次数
from bs4 import BeautifulSoup
import re
import time
import random
import os
#############################在请求头中把User-Agent设置成浏览器中的User-Agent，来伪造浏览器访问
user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
               'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
               "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
               "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124"]
vcf="CosmicCodingMuts.vcf"
dict={}
infile=open(vcf,"r")
if os.path.exists("cosmic.tsv"):
    outfile=open("cosmic.tsv","r")
    for line in outfile:
        line=line.strip()
        array=line.split()
        dict[array[0]]=1
    outfile.close()
num=0
for line in infile:
    line=line.strip()
    if not line.startswith("#"):
        array=line.split("\t")
        pattern=re.compile(r'(\d+)')
        id=pattern.findall(array[2])
        if not array[2] in dict:
            outfile = open("cosmic.tsv", "a+")
            url = 'http://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s' %(id[0])
            headers = {'User-Agent': random.choice(user_agents)}#随机选择一个User-Agent的
            s = requests.session()
            print (url)
            s.keep_alive = False#关闭多余连接
            time.sleep(random.randint(0, 2)) # 暂停0~2秒
            res=s.get(url,headers=headers,auth=('yucaifan@chosenmedtech.com', 'Fyc_840924'), verify=False)
            if res.status_code==200:
                ret = res.text
                soup=BeautifulSoup(ret,'html.parser')
                dbsnp = soup.find_all(text=re.compile("has been flagged as a SNP."))
                dt = soup.find_all('dt')
                dd = soup.find_all('dd')
                outfile = open("cosmic.tsv", "a+")
                for i in range(len(dt)):
                    if dt[i].string == "Ever confirmed somatic?":
                        outfile.write("%s\t%s\n" % (array[2], dd[i].get_text()))
                if dbsnp!=[]:
                    outfile.write("%s\tSNP\n" % (array[2]))
                outfile.close()
            else:
                print("%s faile"%(array[2]))
                continue
infile.close()
print("#This pcocess done.")