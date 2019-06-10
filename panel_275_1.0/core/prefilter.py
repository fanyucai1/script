#Email:fanyucai1@126.com
#2019.5.23

import os
import argparse
import re
import sys


def run(vcf,genelist,vaf,outdir,prefix):
    dict = {}
    infile = open(genelist, "r")
    for line in infile:
        line = line.strip()
        dict[line] = 1
    infile.close()
    infile = open(vcf, "r")
    all = open("%s/%s.vaf.%s.vcf" % (outdir, prefix,vaf), "w")
    all.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    for line in infile:
        line = line.strip()
        if not line.startswith("#"):
            array = line.split("\t")
            p1 = re.compile(r'UMT=([0-9,]+)')
            p2 = re.compile(r'VMT=([0-9,]+)')
            p3 = re.compile(r'VMF=([0-9,.e-]+)')
            p4 = re.compile(r',')
            p5 = re.compile(r'ANN=(\S+)')
            GT = array[-1].split(":")
            a = p1.findall(line)  # UMT
            b = p2.findall(line)  # VMT
            c = p3.findall(line)  # VMF
            d = p4.findall(array[4])  # ALT
            e = p5.findall(line)  # ANNO
            gene = e[0].split("|")  # gene name
            if gene != [] and gene[3] in dict:
                if a == [] and b == [] and c == [] and d == []:
                    p1 = re.compile(r'DP=([0-9,]+)')
                    p2 = re.compile(r'VD=([0-9,]+)')
                    p3 = re.compile(r'AF=([0-9.,e-]+)')
                    a = p1.findall(line)  # DP
                    b = p2.findall(line)  # VD
                    c = p3.findall(line)  # AF
                if d == []:
                    tmp = "%s\t%s\t.\t%s\t%s\t.\t.\tUMT=%s;VMT=%s;VMF=%s;GT=%s" % (
                    array[0], array[1], array[3], array[4], a[0], b[0], c[0], GT[0])
                    if float(c[0]) >= vaf:
                        all.write("%s\n" % (tmp))
                else:
                    VMT = b[0].split(",")
                    VMF = c[0].split(",")
                    ALT = array[4].split(",")
                    for i in range(len(VMT)):
                        tmp = "%s\t%s\t.\t%s\t%s\t.\t.\tUMT=%s;VMT=%s;VMF=%s;GT=%s" % (
                        array[0], array[1], array[3], ALT[i], a[0], VMT[i], VMF[i], GT[0])
                        if float(VMF[i]) >= vaf:
                            all.write("%s\n" % (tmp))
    infile.close()
    all.close()

if __name__=="__main__":
    if len(sys.argv)!=6:
        print("Usage:\npython3 %s vcf genelist vaf outdir prefix")
        print("Email:fanyucai1@126.com")
        print("Version:1.0")
        sys.exit(-1)
    vcf=sys.argv[1]
    genelist=sys.argv[2]
    vaf=sys.argv[3]
    outdir=sys.argv[4]
    prefix=sys.argv[5]
    run(vcf,genelist,vaf,outdir,prefix)



