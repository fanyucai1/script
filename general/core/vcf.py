#Email:fanyucai1@126.com
#2019.7.10
import os
import re
import argparse
def run(tumor,vcf,outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    infile=open(vcf,"r")
    outfile=open("%s/%s.vcf"%(outdir,tumor),"w")
    outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    name=""
    for line in infile:
        line=line.strip()
        if line.startswith("#CHROM"):
            array=line.split("\t")
            for i in range(len(array)):
                if array[i]==tumor:
                    name=i
                    continue
        print(name)
        if not line.startswith("#"):
            array = line.split("\t")
            info=array[int(name)].split(":")
            GT=info[0]#GT
            p1=re.compile(r',')
            a=p1.findall(array[4])#ALT
            b=p1.findall(info[5])#AD
            c=p1.findall(info[6])#AF
            Ref_Reads=b[0]
            if a!=[]:
                for i in range(len(a)):
                    ALT=a[i]
                    Alt_Reads=b[i+1]
                    Var=c[i]
                    outfile.write("%s\t%s\t%s\t%s\t%s\t.\t.\tGT=%s;Ref_Reads=%s;Alt_Reads=%s;Var=%s\n"
                                  % (array[0], array[1], array[2], array[3], ALT,GT,Ref_Reads,Alt_Reads,Var))
            else:
                outfile.write("%s\t%s\t%s\t%s\t%s\t.\t.\tGT=%s;Ref_Reads=%s;Alt_Reads=%s;Var=%s\n"
                              %(array[0],array[1],array[2],array[3],array[4],GT,Ref_Reads,b[1],info[6]))
    infile.close()
    outfile.close()

if __name__=="__main__":
    parser=argparse.ArgumentParser("Format vcf compile vardict and varscan.")
    parser.add_argument("-v","--vcf",help="vcf file",required=True)
    parser.add_argument("-o","--outdir",help="output directory",required=True)
    parser.add_argument("-t","--tumor",help="tumor sample name in vcf",required=True)
    args=parser.parse_args()
    run(args.tumor,args.vcf,args.outdir)