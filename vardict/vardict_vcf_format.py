import os
import sys

def run(tumor, vcf, outdir):
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
                Var=float(c[0])*100
                outfile.write("%s\t%s\t%s\t%s\t%s\t.\t.\tGT=%s;Ref_Reads=%s;Alt_Reads=%s;Var=%.2f"
                              % (array[0], array[1], array[2], array[3], array[4], GT, Ref_Reads, b[1],Var))
                outfile.write("%\n")
            else:
                for i in range(len(a)):
                    ALT=a[i]
                    Alt_Reads=b[i+1]
                    Var=float(c[i])*100
                    outfile.write("%s\t%s\t%s\t%s\t%s\t.\t.\tGT=%s;Ref_Reads=%s;Alt_Reads=%s;Var=%.2f"
                                  % (array[0], array[1], array[2], array[3], ALT,GT,Ref_Reads,Alt_Reads,Var))
                    outfile.write("%\n")
    infile.close()
    outfile.close()

if __name__=="__main__":
    if len(sys.argv)!=4:
        print("python3 %s tumor_name vcffile outdir\n"%(sys.argv[0]))
        print("Email:fanyucai1@126.com")
    else:
        tumor=sys.argv[1]
        vcf=sys.argv[2]
        outdir=sys.argv[3]
        run(tumor, vcf, outdir)