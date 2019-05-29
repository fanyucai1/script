#Email:fanyucai1@126.com
#2019.5.23

import os
import argparse
import re

SNV=0.3
Indel=0.2
"""
Mandelker D, Donoghue M T A, Talukdar S, et al. Germline-Focused Analysis of Tumour-Only Sequencing: Recommendations from the ESMO Precision Medicine Working Group[J]. Annals of Oncology, 2019.
"""
parser=argparse.ArgumentParser("Filter panel 275 vcf(VAF>=0.02).")
parser.add_argument("-i","--vcf",help="input vcf file",required=True)
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
parser.add_argument("-v","--vaf",help="default:0.02",required=True,choices=[0.02,0.001,0.005],type=float)
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
args=parser.parse_args()

out=args.outdir+"/"+args.prefix
infile=open(args.vcf,"r")
all=open("%s.all.vcf"%(out),"w")
somatic=open("%s.somatic.vcf"%(out),"w")
germline=open("%s.germline.vcf"%(out),"w")
all.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
somatic.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
germline.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
for line in infile:
    line=line.strip()
    if not line.startswith("#"):
        array=line.split()
        p1=re.compile(r'UMT=([0-9,]+)')
        p2=re.compile(r'VMT=([0-9,]+)')
        p3=re.compile(r'VMF=([0-9,.e-]+)')
        p4=re.compile(r',')
        p5=re.compile(r'TYPE=([A-Za-z,]+)')
        a=p1.findall(line)#UMT
        b=p2.findall(line)#VMT
        c = p3.findall(line)#VMF
        d=p4.findall(array[4])#ALT
        e=p5.findall(line)#SNP or Indel
        up=0
        if a==[] and b==[] and c==[] and d==[]:
            p1 = re.compile(r'DP=([0-9,]+)')
            p2 = re.compile(r'VD=([0-9,]+)')
            p3 = re.compile(r'AF=([0-9.,e-]+)')
            a=p1.findall(line)#DP
            b=p2.findall(line)#VD
            c=p3.findall(line)#AF
        if d ==[]:
            tmp="%s\t%s\t.\t%s\t%s\t.\t.\tUMT=%s;VMT=%s;VMF=%s" % (array[0], array[1], array[3], array[4], a[0],b[0],c[0])
            if float(c[0])>=args.vaf:
               all.write("%s\n"%(tmp))
               if e[0]=="SNP" or e[0]=="SNV":
                    up=SNV
               else:
                   up=Indel
               if float(c[0])<=up:
                   somatic.write("%s\n"%(tmp))
               else:
                   germline.write("%s\n"%(tmp))
        else:
            VMT=b[0].split(",")
            VMF=c[0].split(",")
            ALT=array[4].split(",")
            type=e[0].split(",")
            for i in range(len(VMT)):
                tmp = "%s\t%s\t.\t%s\t%s\t.\t.\tUMT=%s;VMT=%s;VMF=%s" % (array[0], array[1], array[3], ALT[i], a[0], VMT[i], VMF[i])
                if type[i]=="SNP":
                    up=SNV
                elif type[i]=="INDEL":
                    up=Indel
                else:
                    print(line)
                    break
                if float(VMF[i]) >= args.vaf:
                    all.write("%s\n" % (tmp))
                    if float(VMF[i]) <=up:
                        somatic.write("%s\n" % (tmp))
                    else:
                        germline.write("%s\n" % (tmp))
infile.close()
somatic.close()
germline.close()
all.close()