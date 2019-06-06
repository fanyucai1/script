import sys


def run(chr_rpts,bcp):
    file1=open(bcp,"r")
    file2=open(chr_rpts,"r")
    outfile=open("OMIM2snp.tsv","r")
    dict={}
    for line in file1:
        line=line.strip()
        array=line.split("\t")
        dict[array[8]]=array[0]#rs to OMIM id
    file1.close()

