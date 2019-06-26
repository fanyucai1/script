import argparse
import re

def run(vcf,genelist,vaf,outdir,prefix):
    dict={}
    infile = open(genelist, "r")
    for line in infile:
        line = line.strip()
        dict[line] = 1
    infile.close()
    infile=open(vcf,"r")
    somatic=open("%s/%s.somatic.vcf"%(outdir,prefix),"w")
    somatic.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    germline=open("%s/%s.germline.vcf"%(outdir,prefix),"w")
    germline.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    for line in infile:
        line=line.strip()
        if not line.startswith("#"):
            array = line.split("\t")
            gene=array[7].split("|")
            if gene[3] in dict:
                pattern=re.compile(r'Germline_Risk')
                a=pattern.findall(array[6])
                info=array[-1].split(":")
                GT=info[0]
                AD=info[1].split(",")
                VF=info[2].split(",")
                Ref_Reads =AD[0]
                ALT = array[4].split(",")
                if VF==[]:
                    Alt_Reads=AD[1]
                    Var=info[2]
                    if float(Var) >= float(vaf):
                        if a!=[]:#germline
                            germline.write("%s\t%s\t%s\t%s\t%s\t.\t.\tRef_Reads=%s;Alt_Reads=%s;GT=%s;Var=%s\n"%(array[0],array[1],array[2],array[3],array[4],Ref_Reads,Alt_Reads,GT,Var))
                        else:
                            somatic.write("%s\t%s\t%s\t%s\t%s\t.\t.\tRef_Reads=%s;Alt_Reads=%s;GT=%s;Var=%s\n"% (array[0], array[1], array[2], array[3], array[4], Ref_Reads,Alt_Reads,GT,Var))
                else:
                    for i in range(1,len(AD)):
                        Alt_Reads=AD[i]
                        Var=VF[i-1]
                        if float(Var) >= float(vaf):
                            if a != []:  # germline
                                germline.write("%s\t%s\t%s\t%s\t%s\t.\t.\tRef_Reads=%s;Alt_Reads=%s;GT=%s;Var=%s\n" % (array[0], array[1], array[2], array[3], ALT[i-1], Ref_Reads, Alt_Reads, GT, Var))
                            else:
                                somatic.write("%s\t%s\t%s\t%s\t%s\t.\t.\tRef_Reads=%s;Alt_Reads=%s;GT=%s;Var=%s\n" % (array[0], array[1], array[2], array[3], ALT[i-1], Ref_Reads, Alt_Reads, GT, Var))
    infile.close()
    somatic.close()
    germline.close()
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-g","--genelist",help="gene list",required=True)
    parser.add_argument("--vaf",help="VAF",required=True)
    parser.add_argument("--vcf",help="vcf",required=True)
    parser.add_argument("-o","--outdir",help="output directory",required=True)
    parser.add_argument("-p","--prefix",help="prefix output",required=True)
    args=parser.parse_args()
    run(args.vcf,args.genelist,args.vaf,args.outdir,args.prefix)