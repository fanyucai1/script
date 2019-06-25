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
vcf="test50.vcf"
dict={}
if os.path.exists("cosmic.tsv"):
    outfile=open("cosmic.tsv","r")
    for line in outfile:
        line=line.strip()
        array=line.split()
        dict[array[0]]=1
    outfile.close()
#######################
numID=[]
infile=open(vcf,"r")
for line in infile:
    line=line.strip()
    if not line.startswith("#"):
        array=line.split("\t")
        pattern=re.compile(r'(\d+)')
        id=pattern.findall(array[2])
        if not array[2] in dict:
            numID.append(id[0])
infile.close()
def run(id):
    outfile = open("cosmic.tsv", "a+")
    url = 'http://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s' % (id)
    headers = {'User-Agent': random.choice(user_agents)}  # 随机选择一个User-Agent
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    time.sleep(random.randint(0, 1))  # 暂停0~1秒
    try:
        res = s.get(url, headers=headers, auth=('yucaifan@chosenmedtech.com', 'Fyc_840924'), verify=False)
        ret = res.text
        soup = BeautifulSoup(ret, 'html.parser')
        dbsnp = soup.find_all(text=re.compile("has been flagged as a SNP."))
        dt = soup.find_all('dt')
        dd = soup.find_all('dd')
        outfile = open("cosmic.tsv", "a+")
        for i in range(len(dt)):
            if dt[i].string == "Ever confirmed somatic?":
                outfile.write("COSM%s\t%s\n" % (id, dd[i].get_text()))
        if dbsnp != []:
            outfile.write("COSM%s\tSNP\n" % (id))
            outfile.close()
    except:
        print(id)

start=time.time()
pool = Pool(processes=40)
pool.map(run, numID)
end=time.time()
print("Elapse time is %g seconds" %(end-start))
