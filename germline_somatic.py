#Email:fanyucai1@126.com
#2019.6.6

import sys
import re

variant="/data/Database/clinvar/variant_summary.txt"#ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/var_citations.txt
clinvar="/data/Database/clinvar/hg19_clinvar.vcf"
def run_split(ivcf,out):
    ###############################################read summary file to get the relationship betwwen allele_id and OriginSimple
    infile=open(variant,"r")
    status={}
    name=[]
    for line in infile:
        line=line.strip()
        array = line.split("\t")
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
    infile2=open(clinvar,"rb")
    dict={}
    for line in infile2:
        line=line.strip()
        if not line.startswith("#"):
            array = line.split("\t")
            pattern=re.compile(r'ALLELEID=(\d+)')
            allele_id=pattern.findall(line)
            tmp=array[0]+"_"+array[1]+"_"+array[3]+"_"+array[4]
            if allele_id[0] in status:
                dict[tmp]=status[allele_id[0]]#chr_pos_ref_alt to class
    infile2.close()
    #################################################
    infile = open(ivcf, "r")
    outfile1=open("%s.germline.vcf"%(out),"w")
    outfile2 = open("%s.somatic.vcf" % (out), "w")
    outfile3 = open("%s.unknow.vcf" % (out), "w")
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
    infile.close()
    outfile1.close()
    outfile2.close()
    outfile3.close()

if __name__=="__main__":
    if len(sys.argv)!=3:
        print("Usage:python3 germline_somatic.py input.vcf outdir/prefix\n")
        print("Version:1.0")
        print("Email:fanyucai1@126.com")
        sys.exit(-1)
    else:
        vcf=sys.argv[1]
        out=sys.argv[2]
        run_split(vcf,out)