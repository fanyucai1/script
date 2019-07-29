import os
import sys

def run(tumor,normal,outdir,prefix):
    if os.path.exists(outdir):
        os.mkdir(outdir)
    tumor_file=open(tumor,"r")
    normal_file=open(normal,"r")
    outfile=open("%s/%s.filter.normal.annovar.tsv"%(outdir,prefix),"w")
    dict={}
    for line in normal_file:
        line=line.strip()
        array=line.split("\t")
        tmp=array[0]+"_"+array[1]+"_"+array[2]+"_"+array[3]+"_"+array[4]
        dict[tmp]=1
    normal_file.close()
    num=0
    for line in tumor_file:
        line = line.strip()
        array = line.split("\t")
        num+=1
        if num==1:
            outfile.write("%s\n"%(line))
        else:
            tmp = array[0] + "_" + array[1] + "_" + array[2] + "_" + array[3] + "_" + array[4]
            if not tmp in dict:
                outfile.write("%s\n" % (line))
    outfile.close()

if __name__=="__main__":
    if len(sys.argv)!=5:
        print("usage:python3 %s tumor.annovar.tsv normal.annovar.tsv outdir prefix" %(sys.argv[0]))
        print("\nEmail:fanyucai1@126.com")
    else:
        tumor=sys.argv[1]
        normal=sys.argv[2]
        outdir=sys.argv[3]
        prefix=sys.argv[4]
        run(tumor, normal, outdir, prefix)