import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.adapters.DEFAULT_RETRIES =10#增加重连次数
from bs4 import BeautifulSoup
import re
import time
import random
import os
from multiprocessing import Process, Pool
#############################在请求头中把User-Agent设置成浏览器中的User-Agent，来伪造浏览器访问
user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
proxy_list =["202.73.51.146:80"]#设置多个代理服务器
vcf="CosmicCodingMuts.vcf"
dict={}
num=[]
infile=open(vcf,"r")
for line in infile:
    line=line.strip()
    if not line.startswith("#"):
        array=line.split("\t")
        pattern=re.compile(r'(\d+)')
        id=pattern.findall(array[2])
        num.append(id[0])
infile.close()
if os.path.exists("cosmic.tsv"):
    outfile=open("cosmic.tsv","r")
    for line in outfile:
        line=line.strip()
        array=line.split()
        dict[array[0]]=1
    outfile.close()
num=0
def run(id,outfile):
    if not id in dict:
        outfile = open("cosmic.tsv", "a+")
        url = 'http://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s' % (id)
        headers = {'User-Agent': random.choice(user_agents)}  # 随机选择一个User-Agent的
        proxy = random.choice(proxy_list)  # 随机选取一个代理服务器
        s = requests.session()
        print(url)
        s.keep_alive = False  # 关闭多余连接
        # s.proxies = {"http":'http://' + proxy}
        try:
            time.sleep(random.randint(0, 1))  # 暂停0~1秒
            res = s.get(url, headers=headers, auth=('yucaifan@chosenmedtech.com', 'Fyc_840924'), verify=False)
            ret = res.text
            soup = BeautifulSoup(ret, 'html.parser')
            dbsnp = soup.find_all(text=re.compile("has been flagged as a SNP."))
            dt = soup.find_all('dt')
            dd = soup.find_all('dd')
            outfile = open("cosmic.tsv", "a+")
            for i in range(len(dt)):
                if dt[i].string == "Ever confirmed somatic?":
                    outfile.write("COSM%s\t%s" % (id, dd[i].get_text()))
            if dbsnp != []:
                outfile.write("COSM%s\tSNP" % (id))
                outfile.close()
        except:
            outfile.close()
            exit(1)
pool = Pool(processes=5)
pool.map(run, num)
print("#This pcocess done.")