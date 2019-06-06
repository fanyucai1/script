#Email:fanyucai1@126.com
#2019.6.6

import sys
import re

variant="/data/Database/clinvar_vcf_GRCh37/variant_summary.txt"#ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/var_citations.txt
clinvar="/data/Database/clinvar_vcf_GRCh37/hg19_clinvar.vcf"
def run(ivcf,dir,prefix):
    ###############################################read summary file to get the relationship betwwen allele_id and OriginSimple
    infile=open(variant,"r")
    status={}
    name=[]
    for line in infile:
        line=line.strip()
        array = line.split()
        if line.startswith("#"):
            for i in range(len(array)):
                name.append(array[i])
        else:
            for i in range(len(array)):
                if name[i]=="OriginSimple":
                    status[array[0]]=array[i]#allele_id to OriginSimple
                else:
                    pass
    infile.close()
    ###################################################read clinvar vcf to get relationship between position information and OriginSimple
    infile=open(clinvar,"r")
    dict={}
    for line in infile:
        line=line.strip()
        if not line.startswith("#"):
            pattern=re.compile(r'ALLELEID=(\d+)')
            allele_id=pattern.findall(line)
            array=line.split()
            tmp=array[0]+"_"+array[1]+"_"+array[3]+"_"+array[4]
            dict[tmp]=status[allele_id[0]]#chr_pos_ref_alt to class
    infile.close()
    #################################################
    infile = open(ivcf, "r")
    outfile1=open("%s/%s.germline.vcf"%(dir,prefix),"w")
    outfile2 = open("%s/%s.somatic.vcf" % (dir, prefix), "w")
    outfile3 = open("%s/%s.unknow.vcf" % (dir, prefix), "w")
    for line in infile:
        line = line.strip()
        if not line.startswith("#"):
            outfile1.write("%s\n"%(line))
            outfile2.write("%s\n" % (line))
            outfile3.write("%s\n" % (line))
        else:
            array = line.split("\t")
            tmp = array[0] + "_" + array[1] + "_" + array[3] + "_" + array[4]
            if tmp in dict:
                p1=re.compile(r'somatic',re.I)
                a=p1.findall(dict[tmp])
                if a!=[]:
                    outfile2.write("%s\n" % (line))
                else:
                    p2 = re.compile(r'germline', re.I)
                    b = p2.findall(dict[tmp])
                    if b!=[]:
                        outfile1.write("%s\n" % (line))
                    else:
                        outfile3.write("%s\n" % (line))
            else:
                outfile3.write("%s\n" % (line))

if __name__=="__main__":
    if len(sys.argv)!=4:
        print("Usage:python3 germline_somatic.py input.vcf outdir prefix\n")
        print("Version:1.0")
        print("Email:fanyucai1@126.com")
        sys.exit(-1)
    vcf=sys.argv[1]
    outdir=sys.argv[2]
    prefix=sys.argv[3]
    run(vcf,outdir,prefix)