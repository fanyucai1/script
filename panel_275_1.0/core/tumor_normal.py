import argparse
import re

def run(vcf,outdir,prefix):
    infile=open(vcf,"r")
    somatic=open("%s/%s.somatic.vcf"%(outdir,prefix),"w")
    somatic.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    germline=open("%s/%s.germline.vcf"%(outdir,prefix),"w")
    germline.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    for line in infile:
        line=line.strip()
        if not line.startswith("#"):
            array=line.split("\t")
            pattern=re.compile(r'Germline_Risk')
            a=pattern.findall(array[6])
            info=array[-1].split(":")
            Reads=info[1].split(",")
            if a!=[]:
                germline.write("%s\t%s\t%s\t%s\t%s\t.\t.\tRef_Reads=%s;Alt_Reads=%s;GT=%s;Var=%s\n"
                               %(array[0],array[1],array[2],array[3],array[4],Reads[0],Reads[1],info[0],info[2]))
            else:
                somatic.write("%s\t%s\t%s\t%s\t%s\t.\t.\tRef_Reads=%s;Alt_Reads=%s;GT=%s;Var=%s\n"
                               % (array[0], array[1], array[2], array[3], array[4], Reads[0], Reads[1], info[0], info[2]))
    infile.close()
    somatic.close()
    germline.close()
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-v","--vcf",help="vcf",required=True)
    parser.add_argument("-o","--outdir",help="output directory",required=True)
    parser.add_argument("-p","--prefix",help="prefix output",required=True)
    args=parser.parse_args()
    run(args.vcf,args.outdir,args.prefix)