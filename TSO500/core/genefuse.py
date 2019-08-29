import os
import sys
import re
import subprocess
samplelist="/data/TSO500/samplelist.csv"
root_dir="/data/TSO500/"
outdir="/data/TSO500/fuse"
genefuse="/software/GeneFuse/genefuse"
ref="/data/Database/hg19/ucsc.hg19.fasta"
fusion="/software/GeneFuse/genes/cancer.hg19.csv"
dict={}
infile=open(samplelist,"r")
for line in infile:
    line=line.strip()
    array=line.split(",")
    dict[array[0]]=2
infile.close()

if not os.path.exists(outdir):
    os.mkdir(outdir)
if not os.path.exists("%s/json"%(outdir)):
    os.mkdir("%s/json" %(outdir))
if not os.path.exists("%s/html" % (outdir)):
    os.mkdir("%s/html" % (outdir))

for (root,dirs,files) in os.walk(root_dir):
    for file in files:
        tmp1=os.path.join(root,file)
        R1,R2="",""
        array=tmp1.split("/")
        sample_name = array[-2]
        out=outdir+"/"+sample_name
        if sample_name in dict and dict[sample_name]!=0:
            if tmp1.endswith("L001_R1_001.fastq.gz"):
                dict[sample_name] -= 1
                tmp2=re.sub(r'L001',"L002",tmp1)
                tmp3 = re.sub(r'L001', "L003", tmp1)
                tmp4 = re.sub(r'L001', "L004", tmp1)
                cmd1="zcat %s %s %s %s >%s_R1.fastq"%(tmp1,tmp2,tmp3,tmp4,out)
                cmd2=re.sub(r'_R1',"_R2",cmd1)
                cmd3="%s --read1 %s_R1.fastq --read2 %s_R2.fastq --ref %s --html %s/html/%s.html --json %s/json/%s.json --fusion %s --thread 10 --unique 3 >%s.txt"\
                     %(genefuse,out,out,ref,outdir,sample_name,outdir,sample_name,fusion,out)
                cmd=cmd1+" && "+cmd2+" && "+cmd3
                print(cmd)
