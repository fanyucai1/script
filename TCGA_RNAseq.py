#Email:fanyucai1@126.com

import os
import argparse
import subprocess

parser=argparse.ArgumentParser("This script will do with the files from TCGA.")
parser.add_argument("-i","--input",type=str,help="the file you download",required=True)
parser.add_argument("-s","--sample",type=str,help="sample list",required=True)
parser.add_argument("-t","--type",type=str,help="the type of files you download")
parser.add_argument("-o","--outdir",type=str,help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",type=str,help="prefix of output",default="out")
result=parser.parse_args()

if(result.outdir):
    result.outdir=os.path.abspath(result.outdir)
    subprocess.check_call('mkdir -p %s' %(result.outdir),shell=True)
os.chdir(result.outdir)
##############first unzip the file############
subprocess.check_call('tar xzvf %s -C %s' %(result.input,result.outdir),shell=True)
#####################open sample list###################corresponding files name to sample name
dir2sample={}
dir2file={}
samplefile=open(result.sample,"r")
samplename=[]
num=0
for line in samplefile:
    line=line.strip()
    num+=1
    if num !=1:#comment line
        array=line.split("\t")
        dir2file[array[0]]=array[1]
        if array[1].endswith(".tar.gz"):
            subprocess.check_call("tar xzvf %s/%s/%s" % (result.outdir, array[0], array[1]), shell=True)
        elif array[1].endswith("txt"):
            pass
        elif array[1].endswith(".gz"):
            subprocess.check_call("gunzip %s/%s/%s" % (result.outdir, array[0], array[1]), shell=True)
        else:
            pass
        dir2sample[array[0]]=array[6]
        samplename.append(array[6])
#############################################defined 2D dictionary
def dict2d(thedict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})
############################################
genename={}
dict={}
for key in dir2file:
    dirs=os.listdir("%s/%s" %(result.outdir,key))
    for file in dirs:
        tmp=open("%s/%s/%s" %(result.outdir,key,file),"r")
        for line in tmp:
            line=line.strip()
            array=line.split("\t")
            dict2d(dict,array[0],dir2sample[key],array[1])
            genename[array[0]]=1
subprocess.check_call("rm -rf %s/*" %(result.outdir),shell=True)
outfile=open("%s/out.tsv" %(result.outdir),"w")
for x in samplename:
    outfile.write("\t%s" %(x))
for key in genename:
    outfile.write("\n%s" %(key))
    for x in samplename:
        if x in dict[key]:
            outfile.write("\t%s" %(dict[key][x]))
        else:
            outfile.write("\t0")