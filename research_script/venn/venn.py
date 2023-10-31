#!/home/fanyucai/software/python/Python-v3.6.4/bin/python3

import fire
import os
import sys
import re
import subprocess
import pandas as pd
import numpy as np

outdir = os.getcwd()
bin = sys.path[0]
family=[]
def venn_plt(group,*key):
    group=os.path.abspath(group)
    file=open("%s"%(group),"r")
    out=open("%s/in_venn.xls" %(outdir),"w")
    out.write("OG")

    for i in key:
        out.write("\t%s" %(i))
    out.write("\n")
    for line in file:
        line=line.strip()
        list=line.split(" ")
        out.write("%s" %(list[0]))
        for i in key:
            patt=r'%s' %(i)
            match = re.findall(patt, line)
            if match:
                out.write("\t1")
                family[i]+=1
            else:
                out.write("\t0")
        out.write("\n")
    out.close()
    file.close()
    subprocess.check_output("perl %s/venn_graph.pl -i %s/in_venn.xls" %(bin,outdir),shell=True)


def gene_family(group,*key):
    group = os.path.abspath(group)
    file = open("%s" % (group), "r")
    out=open("%s/fam_stat.txt" %(outdir),"w")
    data={}
    for i in key:
        data["%s" %(i)]={'single':0,
                         'unique':0,
                         'par':0,
                         'mult':0
                         }
    df=pd.DataFrame.from_dict(data)
    for line in file:
        line=line.strip()
        list=line.split(" ")
        del list[0]
        for i in key:
            pat=r"%s" %(i)
            match = re.findall(i, line)
            if match and len(match) > 1 and len(list) == len(match):#######旁系同源
                df.loc['par', "%s" % (i)] += len(match)
                continue

            if match and len(match) > 1 and len(list) > len(match):
                df.loc['mult', "%s" % (i)]+=len(match)
                continue

            if match and len(match) == 1 and len(list) > len(match):
                df.loc['single', "%s" % (i)] += len(match)
                continue


    print (df)

if __name__=="__main__":
    #fire.Fire(venn_plt)
    fire.Fire(gene_family)