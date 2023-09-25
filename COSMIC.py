
#Email:fanyucai1@126.com

import argparse
import re
import os
import subprocess
parser=argparse.ArgumentParser("This script will filter annovar result correspoding COSMIC\nhttps://www.oncology-central.com/wp-content/uploads/2017/06/trusight-tumor-170-tmb-analysis-white-paper-1170-2017-0011.pdf")
parser.add_argument("-d","--dropped",type=str,help="annovar ouput from COSMIC(dropped),force",required=True)
parser.add_argument("-f","--filter",type=str,help="annovar output from COSMIC(filtered),force",required=True)
parser.add_argument("-n","--num",type=str,help="mininum number observed in COSMIC default:4",default=4)
parser.add_argument("-o","--outdir",type=str,help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",type=str,help="output of prefix default:COSMIC_observed.tsv",default="COSMIC_observed.tsv")

result=parser.parse_args()
result.dropped=os.path.abspath(result.dropped)
result.filter=os.path.abspath(result.filter)
if(result.outdir):
    result.outdir=os.path.abspath(result.outdir)
    subprocess.check_call('mkdir -p %s' %(result.outdir),shell=True)
os.chdir(result.outdir)
infile=open(result.dropped,"r")
outfile=open(("%s/%s") %(result.outdir,result.prefix),"w")
for line in infile:
    line=line.strip()
    array=line.split("\t")
    pattern = re.compile(r'(\d+)\(')
    a=pattern.findall(array[1])
    sum=0
    for i in a:
        sum+=int(i)
    if sum >result.num:
        outfile.write(("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n") %(array[2],array[3],array[4],array[5],array[6],array[7],array[8],array[9]))
outfile.close()
subprocess.check_call("cat %s >> %s/%s" % (result.filter, result.outdir, result.prefix), shell=True)