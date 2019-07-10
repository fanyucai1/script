#Email:fanyucai1@126.com
#2019.7.10
import os
import argparse
def vardict(tumor,vcf,outdir):
    tumor, vcf, outdir = args.tumor, args.vcf, args.outdir
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    infile=open(vcf,"r")
    outfile=open("%s/%s.vcf"%(outdir,tumor),"w")
    outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    name=""
    num=0
    for line in infile:
        line=line.strip()
        if line.startswith("#CHROM"):
            array=line.split("\t")
            for i in range(len(array)):
                if array[i]==tumor:
                    name=i
                if array[i]=="FORMAT":
                    num=i
                    continue
        if not line.startswith("#"):
            array = line.split("\t")
            tmp=array[num].split(":")
            info = array[int(name)].split(":")
            GT,a,b,c="",array[4].split(","),[],[]
            for k in range(len(tmp)):
                if tmp[k]=="GT":
                    GT = info[k]  # GT
                elif tmp[k]=="AD":
                    b = info[k].split(",")  # AD
                elif tmp[k] == "AF":
                    c = info[k].split(",")  # AF
                else:
                    pass
            Ref_Reads=b[0]
            if len(a)==1:
                outfile.write("%s\t%s\t%s\t%s\t%s\t.\t.\tGT=%s;Ref_Reads=%s;Alt_Reads=%s;Var=%s\n"
                              % (array[0], array[1], array[2], array[3], array[4], GT, Ref_Reads, b[1], c[0]))
            else:
                for i in range(len(a)):
                    ALT=a[i]
                    Alt_Reads=b[i+1]
                    Var=c[i]
                    outfile.write("%s\t%s\t%s\t%s\t%s\t.\t.\tGT=%s;Ref_Reads=%s;Alt_Reads=%s;Var=%s\n"
                                  % (array[0], array[1], array[2], array[3], ALT,GT,Ref_Reads,Alt_Reads,Var))
    infile.close()
    outfile.close()

def varscan(args):
    tumor, vcf, outdir=args.tumor,args.vcf,args.outdir
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    infile=open(vcf,"r")
    outfile=open("%s/%s.vcf"%(outdir,tumor),"w")
    outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    name=""
    num=0
    for line in infile:
        line=line.strip()
        if line.startswith("#CHROM"):
            array=line.split("\t")
            for i in range(len(array)):
                if array[i]==tumor:
                    name=i
                if array[i]=="FORMAT":
                    num=i
                    continue
        if not line.startswith("#"):
            array = line.split("\t")
            tmp=array[num].split(":")
            info = array[int(name)].split(":")
            GT,a,b,c,Ref_Reads="",array[4].split(","),[],[],""
            for k in range(len(tmp)):
                if tmp[k]=="GT":
                    GT = info[k]  # GT
                elif tmp[k]=="AD":
                    b = info[k].split(",")  # AD
                elif tmp[k] == "FREQ":
                    c = info[k].split(",")  # AF
                elif tmp[k]=="RD":
                    Ref_Reads=info[k]
                else:
                    pass
            if len(a)==1:
                outfile.write("%s\t%s\t%s\t%s\t%s\t.\t.\tGT=%s;Ref_Reads=%s;Alt_Reads=%s;Var=%s\n"
                              % (array[0], array[1], array[2], array[3], array[4], GT, Ref_Reads, b[0], c[0]))
            else:
                for i in range(len(a)):
                    ALT=a[i]
                    Alt_Reads=b[i]
                    Var=c[i]
                    outfile.write("%s\t%s\t%s\t%s\t%s\t.\t.\tGT=%s;Ref_Reads=%s;Alt_Reads=%s;Var=%s\n"
                                  % (array[0], array[1], array[2], array[3], ALT,GT,Ref_Reads,Alt_Reads,Var))
    infile.close()
    outfile.close()
if __name__=="__main__":
    parser=argparse.ArgumentParser("Format vcf compile vardict and varscan.")
    subparsers=parser.add_subparsers(dest="vcf")

    a=subparsers.add_parser("varscan",help="format varscan vcf")
    a.add_argument("-v","--vcf",help="vcf file",required=True)
    a.add_argument("-o","--outdir",help="output directory",required=True)
    a.add_argument("-t","--tumor",help="tumor sample name in vcf",required=True)
    a.set_defaults(func=varscan)

    b=subparsers.add_parser("vardict",help="format vardict vcf")
    b.add_argument("-v", "--vcf", help="vcf file", required=True)
    b.add_argument("-o", "--outdir", help="output directory", required=True)
    b.add_argument("-t", "--tumor", help="tumor sample name in vcf", required=True)
    b.set_defaults(func=varscan)
    args=parser.parse_args()
    args.func(args)