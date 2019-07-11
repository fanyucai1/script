import argparse
import re

def run(anno_vcf,low_vcf,outdir,prefix):
    infile1=open(anno_vcf,"r")
    infile2=open(low_vcf,"r")
    outfile=open("%s/%s.final.vcf","w")
    outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    for line in infile1:
        line=line.strip()
        array=line.split("\t")
        if not line.startswith("#"):
            a=array[4].split(",")
            info=array[-1].split(":")
            GT=info[0]
            Ref
            if len(a)==1:
                outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                          %(array[0],array[1],array[2],array[3],array[4],array[0]))