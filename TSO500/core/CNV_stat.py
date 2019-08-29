import os
import re
import subprocess
root_dir="/data/TSO500/"
sample_list="/data/TSO500/samplelist.csv"
outdir="/data/TSO500/stat/CNV"

if not os.path.exists(outdir):
    os.mkdir(outdir)
dict={}
infile=open(sample_list,"r")
num=0
counts=0
for line in infile:
    line = line.strip()
    array = line.split(",")
    num+=1
    if num==1:
        for k in range(len(array)):
            if array[k]=="yes_no_illumina":
                counts=k
    else:
        if array[counts]=="yes":
            dict[array[0]]=1
infile.close()

for (root,dirs,files) in os.walk(root_dir):
    for file in files:
        tmp=os.path.join(root,file)
        if tmp.endswith("CopyNumberVariants.vcf"):
            array=tmp.split("/")
            sample_name=re.sub(r'_CopyNumberVariants.vcf',"",array[-1])
            if sample_name in dict:
                outfile=open("%s.cnv.tsv"%(sample_name),"w")
                infile=open(tmp,"r")
                i=0
                for line in infile:
                    if not line.startswith("#"):
                        line = line.strip()
                        array = line.split("\t")
                        if array[4] == "<DUP>" or array[4] == "<DEL>":
                            i += 1
                            p1 = re.compile(r'END=(\d+)')
                            p2 = re.compile(r'ANT=(\S+)')
                            a = p1.findall(line)
                            b = p2.findall(line)
                            tmp = array[0] + "\t" + array[1] + "\t" + a[0] + "\t" + array[3] + "\t" + array[4] + "\t" + b[0]
                            outfile.write("%s\n" % (tmp))
                    outfile.close()
                    infile.close()
                    if i == 0:
                        subprocess.check_call("rm -rf %s/%s.cnv.tsv" % (outdir, sample_name), shell=True)
                        print("sample %s not find CNV" % (sample_name))