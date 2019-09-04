import os
import argparse
import subprocess
import re

def run(dir,samplelist,vaf,outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    #####################################get sample ID
    sample_ID=["TS19355NF","TS19067NF","TS19348NF","TS19353NF"]
    ######################################get SNV information
    for key in sample_ID:
        path=dir+"/Logs_Intermediates/Tmb/%s/%s.tmb.tsv"%(key,key)
        vcf=dir+"/Logs_Intermediates/SmallVariantFilter/%s/%s_SmallVariants.genome.vcf"%(key,key)
        if os.path.exists(path):
            infile=open(path,"r")
            outfile=open("%s/%s.snv.tmp.vcf"%(outdir,key),"w")
            outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
            num=0
            name=[]
            dict={}
            for line in infile:
                line=line.strip()
                num+=1
                array=line.split("\t")
                tmp = array[0] + "\t" + array[1] + "\t" + array[2] + "\t" + array[3]
                dict[tmp]=1
            infile.close()
            infile=open(vcf,"r")
            for line in infile:
                line=line.strip()
                if not line.startswith("#"):
                    array=line.split("\t")
                    tmp=array[0] + "\t" + array[1] + "\t" + array[3] + "\t" + array[4]
                    if tmp in dict:
                        info=array[-1].split(":")
                        outfile.write("%s\t%s\t.\t%s\t%s\t.\t.\tGT=%s;AD=%s;Var=%s\n"%(array[0],array[1],array[3],array[4],info[0],info[2],info[4]))
            infile.close()
            outfile.close()