
import re
import subprocess
import sys
import os

annovar="/software/docker_tumor_base/Resource/Annovar"

def run(vcf,sex,genelist,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    vcf_in = open(vcf, "r")
    vcf_out = open("%s.cnv.vcf" % (out), "w")
    pattern = re.compile(r'PVAL\s+([0-9.]+):')
    end = re.compile(r'END=(\d+);')
    CNV = {}
    CNV_type = {}
    for line in vcf_in:
        line = line.strip()
        if not line.startswith("#"):
            array = line.split("\t")
            if array[4] != "." and float(array[5])>50:
                a = pattern.findall(line)
                b = end.findall(line)
                CNV[array[0]] = a[0]
                CNV_type[array[0]] = array[4]
                vcf_out.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (array[0], array[1], b[0], "0", "0", a[0]))
    vcf_in.close()
    vcf_out.close()
    ################################################annotate cnv vcf
    cmd = "cd %s && perl %s/table_annovar.pl %s.cnv.vcf %s/humandb/ -out %s.cnv" \
          " -remove -protocol refGene -operation g --nastring . -buildver hg19" % (
          outdir, annovar, out, annovar, prefix)
    subprocess.check_call(cmd, shell=True)
    ################################################read gene list
    dict = {}
    infile = open(genelist, "r")
    for line in infile:
        line = line.strip()
        dict[line] = 1
    infile.close()
    ############################################parse cnv file
    vcf_in = open("%s.cnv.hg19_multianno.txt" % (out), "r")
    vcf_out = open("%s.cnv.tsv" % (out), "w")
    vcf_filter = open("%s.cnv.filter.tsv" % (out), "w")
    vcf_out.write("Chr\tStart\tEnd\tFunc.refGene\tGene.refGene\tCNV\tType\n")
    vcf_filter.write("Chr\tStart\tEnd\tFunc.refGene\tGene.refGene\tCNV\tType\n")
    num = 0
    for line in vcf_in:
        num += 1
        line = line.strip()
        array = line.split("\t")
        dot=array[6].split(";")
        result = "f"
        filter = "f"
        if num != 1:
            if dot==[]:
                if array[6] in dict:
                    result="t"
            else:
                for i in dot:
                    if i in dict:
                        result="t"
            if sex=="male":
                if array[0]!="chrX" and array[0]!="chrY":
                    if float(CNV[array[0]])>=6 or float(CNV[array[0]]) < 1:
                        filter="t"
            else:
                if array[0]!="chrY":
                        if float(CNV[array[0]])>=6 or float(CNV[array[0]]) < 1:
                            filter = "t"
            if result=="t":
                vcf_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (array[0], array[1], array[2], array[5], array[6], CNV[array[0]], CNV_type[array[0]]))
                if filter=="t":
                    vcf_filter.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (array[0], array[1], array[2], array[5], array[6], CNV[array[0]], CNV_type[array[0]]))
    vcf_out.close()
    vcf_in.close()
    vcf_filter.close()
    #########################################
    subprocess.check_call("rm -rf %s.cnv.hg19_multianno.txt %s.cnv.vcf" % (out, out),shell=True)
if __name__=="__main__":
    if len(sys.argv)!=6:
        print("Usage:python3 %s vcf sex genelist outdir prefix"%(sys.argv[0]))
        print("Email:fanyucai1@126.com")
        print("2019.6.10")
        sys.exit(-1)
    vcf=sys.argv[1]
    sex=sys.argv[2]
    genelist=sys.argv[3]
    outdir=sys.argv[4]
    prefix=sys.argv[5]
    run(vcf,sex,genelist,outdir,prefix)