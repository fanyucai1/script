import sys
import os
import re

samplelist=sys.argv[1]
dir=sys.argv[2]
outdir=sys.argv[3]

infile=open(samplelist,'r')
sampleID={}
for line in infile:
    line=line.strip()
    array=line.split("\t")
    sampleID[array[0]]=1
cmd="scp "
for (root,dirs,files) in os.walk(dir):
    for name in files:
        file=os.path.join(root, name)
        p=re.compile(r'SmallVariants.genome.vcf$')
        a=p.findall(file)
        if a!=[]:
            cmd+=" %s "%(file)
cmd+=" fanyucai@192.168.1.118:%s "%(outdir)
print(cmd)