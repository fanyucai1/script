#Email:fanyucai1@126.com
#2019.5.23

import argparse
import re

def run(genelist,vaf,vcf,outdir,prefix):
    dict={}
    infile = open(genelist, "r")
    for line in infile:
        line = line.strip()
        dict[line] = 1
    infile.close()
    infile=open(vcf,"r")
    all = open("%s/%s.vaf.%s.vcf" % (outdir, prefix, vaf), "w")
    all.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    for line in infile:
        line=line.strip()
        if not line.startswith("#"):
            p = re.compile(r'ANN=(\S+)')
            gene=p.findall(line)
            if gene[3] in dict:
                array=line.split("\t")
                info=array[-1].split(":")
                GT=info[0]
                AD=info[1].split(",")
                VF=info[2].split(",")
                Ref_Reads =AD[0]
                if VF==[]:
                    Alt_Reads=AD[1]
                    Var=info[2]
                    if float(Var) >= vaf:
                        all.write("%s\t%s\t%s\t%s\t%s\t.\t.\tRef_Reads=%s;Alt_Reads=%s;GT=%s;Var=%s\n"%(array[0],array[1],array[2],array[3],array[4],Ref_Reads,Alt_Reads,GT,Var))
                    for i in range(1,len(AD)):
                        Alt_Reads=AD[i]
                        Var=VF[i-1]
                        if float(Var)>=vaf:
                            all.write("%s\t%s\t%s\t%s\t%s\t.\t.\tRef_Reads=%s;Alt_Reads=%s;GT=%s;Var=%s\n" % (array[0], array[1], array[2], array[3], array[4], Ref_Reads, Alt_Reads, GT, Var))
    infile.close()
    all.close()
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-g","--genelist",help="gene list",required=True)
    parser.add_argument("-v","--vaf",help="VAF",required=True)
    parser.add_argument("-v","--vcf",help="vcf",required=True)
    parser.add_argument("-o","--outdir",help="output directory",required=True)
    parser.add_argument("-p","--prefix",help="prefix output",required=True)
    args=parser.parse_args()
    run(args.genelist,args.vaf,args.vcf,args.outdir,args.prefix)
