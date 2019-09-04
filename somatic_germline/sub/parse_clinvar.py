import re
clinvar_vcf="/data/Database/clinvar/variant_summary.txt"
clinvar_anno="/data/Database/clinvar/2019.7.20/clinvar.vcf"

def run():

    AlleleID,dict={},{}
    infile=open(clinvar_anno,"r")
    for line in infile:
        line=line.strip()
        array=line.split("\t")
        if not line.startswith("#"):
            AlleleID[array[0]]=array[2]
    infile.close()
    infile = open(clinvar_vcf, "r")
    for line in infile:
        if not line.startswith("#"):
            p=re.compile(r'ALLELEID=(\d+);')
            line = line.strip()
            array = line.split("\t")
            tmp=array[0]+"\t"+array[1]+"\t"+array[3]+"\t"+array[4]
            a=p.findall(line)
            dict[tmp]=AlleleID[a[0]]
    infile.close()
    return dict