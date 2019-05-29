#Email:fanyucai1@126.com
#2019.1.3
import argparse
import os
import subprocess
"""
TMB was defined as the number of somatic, coding, base substitution, and indel mutations per megabase of genome examined. 
link:Chalmers Z R, Connelly C F, Fabrizio D, et al. Analysis of 100,000 human cancer genomes reveals the landscape of tumor mutational burden[J]. Genome medicine, 2017, 9(1): 34.
"""
parser=argparse.ArgumentParser("This script will compute the tumor mutational burden(TMB).")
parser.add_argument("-v","--vcf",type=str,help="vcf file must only contain sites defined by TMB",required=True)
parser.add_argument("-f","--gff",type=str,help="gff3 file",required=True)
parser.add_argument("-g","--gene",type=str,help="gene name per line",required=True)
parser.add_argument("-o","--outdir",type=str,help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",type=str,help="prefix of output defualt:tMB.txt",default="tMB.txt")

result=parser.parse_args()
result.vcf=os.path.abspath(result.vcf)
result.gene=os.path.abspath(result.gene)
result.gff=os.path.abspath(result.gff)
result.outdir=os.path.abspath(result.outdir)

if(result.outdir):
    result.outdir=os.path.abspath(result.outdir)
    subprocess.check_call('mkdir -p %s' %(result.outdir),shell=True)
os.chdir(result.outdir)

infile1=open(result.gene,"r")
subprocess.check_call('awk \'{if($3==\"exon\") print}\' %s >%s/exon.tmp' %(result.gff,result.outdir),shell=True)
if os.path.exists("%s/gene_and_exon.tmp" %(result.outdir)):
    subprocess.check_call("rm -rf %s/gene_and_exon.tmp" %(result.outdir))
for line in infile1:
    line=line.strip()
    try:
        subprocess.check_call("grep \"=%s;\" %s/exon.tmp >>%s/gene_and_exon.tmp" %(line,result.outdir,result.outdir),shell=True)
    except:
        print("%s not find in gff,please check it\n" % (line))
dict1={}
infile2=open("%s/gene_and_exon.tmp" %(result.outdir),"r")

for line in infile2:
    line=line.strip()
    if not line.startswith("#"):
        array=line.split()
        string=array[0]
        string+=":"
        for j in range(int(array[3]),int(array[4])+1):
                string+=str(j)
                string+=str(array[6])
                dict1[string]=1
total=0
for key in dict1:
    total+=1;
print ("%s total coding-sites\n" %(total))
var=0
infile3=open(result.vcf,"r")
for line in infile3:
    line=line.strip()
    if line.startswith("#"):
        var+=1
print ("%s total var in vcf\n" %(var))
outfile=open("%s/%s" %(result.outdir,result.prefix),"w")
tmb=var/total*10**6
print ("TMB is %s\n" %(tmb))
outfile.write("TMB is %s\n" %(tmb))