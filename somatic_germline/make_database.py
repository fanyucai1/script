import os
import re
import sys

cosmic_anno="/data/Database/COSMIC/release_v88/CosmicMutantExport.tsv"
cosmic_vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.vcf"
clinvar_vcf="/data/Database/clinvar/clinvar.vcf"
clinvar_anno="/data/Database/clinvar/variant_summary.txt"

def run(outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    outfile1=open("%s.somatic.vcf"%(out),"w")
    outfile2 = open("%s.germline.vcf"%(out), "w")
    outfile3 = open("%s.snp.vcf"%(out), "w")
    outfile1.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    outfile2.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    outfile3.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    dict={}
    ############################cosmic
    infile=open(cosmic_anno,"r")
    id_num,status,num,cosmicID= 0,0,0,{}
    for line in infile:
        num += 1
        line = line.strip()
        array = line.split("\t")
        if num == 1:
            for i in range(len(array)):
                if array[i] == "Mutation ID":
                    id_num = i
                if array[i] == "Mutation somatic status":
                    status = i
        else:
            if array[status]=="Confirmed somatic variant":
                cosmicID[id_num]=1
    infile.close()
    print("done1")
    infile=open(cosmic_vcf,"r")
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        if not line.startswith("#"):
            tmp=array[0]+"\t"+array[1]+"\t"+array[3]+"\t"+array[4]
            if re.search(r'SNP',line):
                outfile3.write("chr%s\n"%(line))
            elif array[2] in cosmicID:
                outfile1.write("chr%s\n"%(line))
                dict[tmp]=1
            else:
                pass
    infile.close()
    print("done2")
    ############################clinvar
    status,AlleleID_somatic,AlleleID_germline=0,{},{}
    infile=open(clinvar_anno,"r")
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        if line.startswith("#"):
            for i in range(len(array)):
                if array[i] == "OriginSimple":
                    status = i
        else:
            if re.search(r'GRCh37',line) and re.search(r'somatic',array[status]):
                AlleleID_somatic[array[0]]=1
            else:
                if re.search(r'GRCh37', line) and re.search(r'germline', array[status]):
                    AlleleID_germline[array[0]]=1
    infile.close()
    print("done3")
    infile=open(clinvar_vcf,"r")
    p=re.compile(r'ALLELEID=(\d+)')
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        if not line.startswith("#"):
            tmp = array[0] + "\t" + array[1] + "\t" + array[3] + "\t" + array[4]
            if not tmp in dict:
                a=p.findall(line)
                if a[0] in AlleleID_somatic:
                    outfile1.write("chr%s\n"%(line))
                if a[0] in AlleleID_germline:
                    outfile2.write("chr%s\n" % (line))
    outfile1.close()
    outfile2.close()
    outfile3.close()
    print("done4")
if __name__=="__main__":
    if len(sys.argv)!=3:
        print("usage:python3 %s outdir prefix\n"%(sys.argv[0]))
        print("#Email:fanyucai1@126.com")
    else:
        outdir=sys.argv[1]
        prefix=sys.argv[2]
        run(outdir,prefix)