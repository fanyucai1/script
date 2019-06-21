import sys


def run(chr_rpts,bcp):
    file1=open(bcp,"r")#OmimVarLocusIdSNP.bcp
    file2=open(chr_rpts,"r")#ftp://ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/chr_rpts/
    outfile=open("OMIM2snp.tsv","r")
    dict={}
    for line in file1:
        line=line.strip()
        array=line.split("\t")
        if len(array)==9:
            if not array[8] in dict:
                dict[array[8]]=array[0]#rs to OMIM id
            else:
                dict[array[8]]+="_%s"%(array[0])
    file1.close()
    for line in file2:
        line=line.strip()
        line=line.split("\t")

